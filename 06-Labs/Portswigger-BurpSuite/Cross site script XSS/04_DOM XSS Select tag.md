# PortSwigger Lab: DOM XSS in `document.write` Sink Using `location.search` Inside a Select Element

**Platform:** PortSwigger Web Security Academy\
**Difficulty:** Practitioner\
**Status:** Solved\
**Date completed:** 13 October 2026\
**Date documented:** 13 October 2026\
**Category:** Web Security / Cross-Site Scripting (XSS) / DOM-based XSS

## 1. What I Worked On

I completed the PortSwigger Web Security Academy lab **"DOM XSS in
`document.write` sink using source `location.search` inside a select
element."**

The lab contained a stock-checking feature with a DOM-based cross-site
scripting vulnerability. The page read a value from the URL's query
string and inserted it into the HTML of a dropdown using JavaScript's
`document.write()` function.

My goal was to understand the flow of data from the URL to the
HTML-writing function, identify why the surrounding HTML context
mattered, and demonstrate JavaScript execution by triggering `alert(1)`.

I performed this work in the intentionally vulnerable PortSwigger lab
environment.

## 2. What Is DOM-Based XSS?

DOM-based Cross-Site Scripting (DOM XSS) occurs when client-side
JavaScript processes data that an attacker can influence and uses it in
an unsafe way. The vulnerability can happen in the browser even when the
server does not directly insert the dangerous input into its response
HTML.

To understand DOM XSS, I learned to follow this flow:

**Source → Processing → Sink → Browser interpretation → Possible
JavaScript execution**

-   **Source:** Where the input comes from, such as a URL query
    parameter.
-   **Processing:** The JavaScript code that reads, transforms, or moves
    the input.
-   **Sink:** A function or property that uses the input in a
    potentially dangerous way.
-   **Browser interpretation:** How the browser interprets the resulting
    string, such as HTML markup or ordinary text.
-   **Execution:** If the input changes the document structure in a way
    that creates executable JavaScript, the vulnerability may be
    exploitable.

A URL parameter by itself is not proof of a vulnerability. I need to
trace where the value goes and understand how the application uses it.

## 3. Understanding the Lab

The lab's stock checker displayed a product page with a dropdown for
selecting a store. The lab description explained that the page used:

-   `location.search` as the source.
-   `document.write()` as the sink.
-   A `<select>` element as the surrounding HTML context.

The task was to escape the select-element context and trigger
`alert(1)`.

## 4. Step 1 --- Opened a Product Page

I opened a product page in the lab. My URL initially looked similar to:

``` text
/product?productId=5
```

The `productId=5` parameter identified the product being displayed.

I scrolled down to the stock checker, where I could see a dropdown and a
**Check stock** button. Clicking the button did not add a useful
parameter to the URL, so I investigated the page's HTML and JavaScript
instead.

## 5. Step 2 --- Inspected the HTML in DevTools

I right-clicked the page and selected **Inspect** to open Chrome
DevTools. In the **Elements** panel, I examined the stock-checking form.

I found markup similar to:

``` html
<form id="stockCheckForm" action="/product/stock" method="POST">
    <input required type="hidden" name="productId" value="5">
    <script>
        <!-- inline JavaScript that creates the store dropdown -->
    </script>
    <select name="storeId"></select>
    <button type="submit" class="button">Check stock</button>
</form>
```

The important observation was:

``` html
<select name="storeId">
```

This told me that the dropdown was associated with a parameter named
`storeId`. It did not, by itself, prove that the page was vulnerable,
but it gave me a useful clue about the input to investigate.

I also noticed two JavaScript files associated with the stock checker:

-   `/resources/js/stockCheckPayload.js`
-   `/resources/js/stockCheck.js`

## 6. Step 3 --- Inspected the JavaScript Files

I opened the **Sources** panel in DevTools and examined both files.

### `stockCheckPayload.js`

The visible code included:

``` javascript
window.contentType = 'application/x-www-form-urlencoded';

function payload(data) {
    return new URLSearchParams(data).toString();
}
```

I understood that this helper converts data into URL-encoded form data.
It was not the `document.write()` sink described in the lab.

### `stockCheck.js`

This file contained a `checkStock()` function that used `fetch()` to
send a request and then updated the stock-check result on the page. That
helped me understand the stock-checking request, but it was not the key
code path I needed to investigate for this particular DOM XSS issue.

I then returned to the **Elements** panel and expanded the inline
`<script>` directly beneath the hidden `productId` input. This was the
important discovery.

## 7. Step 4 --- Found the Source-to-Sink Flow

The inline script contained code equivalent to the following:

``` javascript
var stores = ["London", "Paris", "Milan"];

var store = (new URLSearchParams(window.location.search))
    .get('storeId');

document.write('<select name="storeId">');

if (store) {
    document.write('<option selected>' + store + '</option>');
}

for (var i = 0; i < stores.length; i++) {
    if (stores[i] === store) {
        continue;
    }

    document.write('<option>' + stores[i] + '</option>');
}

document.write('</select>');
```

This was the key to understanding the vulnerability.

### The source: `window.location.search`

``` javascript
window.location.search
```

This reads the query string from the current URL.

For example:

``` text
/product?productId=5&storeId=mango
```

The query string contains `productId=5` and `storeId=mango`.

### Extracting the value: `.get('storeId')`

``` javascript
(new URLSearchParams(window.location.search)).get('storeId')
```

This parses the query string and retrieves the value of the `storeId`
parameter. In the example above, the variable `store` becomes the string
`mango`.

### The sink: `document.write()`

The most important line was:

``` javascript
document.write('<option selected>' + store + '</option>');
```

The code combines a fixed HTML string with the value from the URL and
passes the result to `document.write()`. The browser interprets the
resulting string as HTML.

The application did not safely encode the supplied value before
inserting it into this HTML context. That meant specially crafted input
could affect the structure of the document rather than being treated
only as ordinary text.

## 8. Step 5 --- Tested Whether the URL Controlled the Dropdown

I added a test value to the URL:

``` text
/product?productId=5&storeId=mango
```

After loading the page, I saw `mango` appear as the selected dropdown
option.

This was a useful observation because it showed that the `storeId` query
parameter influenced the rendered page.

However, **seeing my input appear in the dropdown was not enough to
prove XSS**. It only showed that the input reached the page. I still
needed to understand the HTML context and verify whether the browser
could be made to interpret the input as markup.

## 9. Step 6 --- Understood the HTML Context

The vulnerable code inserted the value between the opening and closing
tags of an option element, inside a select element. Conceptually, the
page was constructing HTML like this:

``` html
<select name="storeId">
    <option selected>USER_INPUT</option>
    <option>London</option>
    <option>Paris</option>
    <option>Milan</option>
</select>
```

This surrounding structure mattered. An input that is placed inside an
existing HTML element must be evaluated in that context. I could not
simply assume that any HTML tag would work wherever I inserted it.

For this lab, the intended approach was to escape the existing
option/select context and introduce markup that could trigger JavaScript
execution.

## 10. Step 7 --- Demonstrated JavaScript Execution

For the lab, I used the supplied lab guidance to construct a value in
the `storeId` parameter that escaped the existing HTML context, closed
the select element, and introduced an image element with an error event
handler.

The lab's example was:

``` text
/product?productId=1&storeId="></select><img%20src=1%20onerror=alert(1)>
```

I adapted the product ID to match the product page I was testing. The
important ideas behind this test were:

-   The input had to account for the HTML context where it was inserted.
-   The existing select element had to be closed so that the new element
    was interpreted in the intended context.
-   The image source was deliberately invalid, causing an error event.
-   The `onerror` event handler called `alert(1)` as proof of JavaScript
    execution.

When the browser displayed an alert containing `1`, I had confirmed that
JavaScript executed. The lab status changed to **Solved**.

I performed this test only in the authorized PortSwigger Web Security
Academy lab.

## 11. Why the Lab Was Vulnerable

The core issue was not that the page had a `storeId` parameter. The
issue was the way the application handled the parameter.

The vulnerable sequence was:

1.  JavaScript read the URL query string.
2.  It extracted the `storeId` value.
3.  It concatenated that value directly into an HTML string.
4.  It passed the string to `document.write()`.
5.  The browser interpreted the constructed string as markup.

Because the input was not safely handled for the HTML context, the input
could alter the page's structure and enable JavaScript execution.

## 12. What I Learned About Sources and Sinks

### Source

A source is where data enters the program or becomes available to it. In
this lab, the source was:

``` javascript
window.location.search
```

The value came from the URL, which a user can modify.

### Sink

A sink is a function or property where data is used in a way that may be
dangerous if the data is untrusted. In this lab, the sink was:

``` javascript
document.write(...)
```

It writes a string into the document and interprets it as HTML.

### Why the connection matters

Neither the source nor the sink alone tells the whole story. I had to
trace the value from the URL, through the JavaScript variable, into the
HTML-writing function, and then consider the surrounding HTML context.

This source-to-sink approach is useful when manually investigating
DOM-based XSS.

## 13. How I Can Apply This Method in Future Assessments

When assessing an application I am authorized to test, I can use the
following workflow:

1.  **Map user-controlled inputs.** Check URL parameters, fragments,
    form fields, and other data that the application processes.
2.  **Use a harmless marker.** Supply a unique value such as
    `test123marker` so I can locate it in the rendered page.
3.  **Inspect the live DOM.** Use DevTools **Elements** to see how the
    browser currently represents the page. The live DOM may differ from
    the original page source after JavaScript has run.
4.  **Inspect JavaScript.** Search the relevant source files for the
    input and for potentially unsafe operations.
5.  **Trace the data flow.** Determine how the value is extracted,
    transformed, and passed to a sink.
6.  **Identify the context.** Work out whether the value is inside HTML
    text, an attribute, a JavaScript string, or another context.
7.  **Test safely.** Use a harmless proof of concept in a permitted test
    environment and verify the result.
8.  **Document the evidence.** Record the source, sink, relevant code,
    observed behavior, impact, and recommended fix.

I should not assume every use of `document.write()` is automatically
exploitable, nor that every URL parameter creates an XSS vulnerability.
The surrounding code, input handling, and execution context all matter.

## 14. How Developers Can Prevent This Vulnerability

The safest approach is to avoid writing untrusted data into HTML
strings.

For example, when inserting a value as ordinary text, developers can
create an element and use `textContent`:

``` javascript
const option = document.createElement('option');
option.textContent = store;
select.appendChild(option);
```

This treats `store` as text rather than parsing it as HTML. Developers
should also validate that store identifiers belong to the expected set
of allowed values, such as `London`, `Paris`, or `Milan`.

Other important defenses include:

-   Avoid using `document.write()` with untrusted input.
-   Use context-appropriate output encoding when rendering data.
-   Prefer safe DOM APIs such as `textContent` when the intended result
    is text.
-   Validate input against expected values where practical.
-   Use a Content Security Policy as an additional defense-in-depth
    measure, not as a replacement for safe coding.

## 15. Final Takeaways

By completing this lab, I learned how to:

-   Investigate a stock-checking feature using Chrome DevTools.
-   Inspect HTML in the **Elements** panel.
-   Find and read inline JavaScript in the **Sources** panel.
-   Identify `window.location.search` as a source.
-   Identify `document.write()` as a potentially dangerous sink.
-   Trace a URL parameter into HTML that the browser interprets.
-   Understand why the surrounding `<option>` and `<select>` elements
    matter.
-   Verify DOM-based XSS by observing JavaScript execution.
-   Recognize safer ways to insert untrusted data into the DOM.

My main takeaway is that I should not rely on memorizing payloads. I
should first understand where the input comes from, how the application
processes it, where it is used, and how the browser interprets it.

## Lab Reference

-   **Lab:** DOM XSS in `document.write` sink using source
    `location.search` inside a select element
-   **Platform:** PortSwigger Web Security Academy
-   **Difficulty:** Practitioner
-   **Status:** Solved
-   **Completed:** 13 October 2026
-   **Lab entry point:**
    https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink-inside-select-element

------------------------------------------------------------------------

*These notes document my own learning process in an intentionally
vulnerable training lab. I will use the techniques only in systems where
I have permission to test.*
