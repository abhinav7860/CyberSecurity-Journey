# PortSwigger Lab: DOM XSS in jQuery Anchor `href` Attribute Sink Using `location.search`

**Date:** 13 October 2026  
**Platform:** PortSwigger Web Security Academy  
**Difficulty:** Apprentice  
**Topic:** DOM-based Cross-Site Scripting (DOM XSS)  
**Status:** Solved

## 1. Objective

In this lab, I investigated a DOM XSS vulnerability in the Submit feedback page. The page used a URL query parameter to set the destination of its **Back** link through jQuery. I solved the lab by making the Back link execute JavaScript that displayed `document.cookie` in an alert.

## 2. Understanding the Vulnerability

The page reads a value from the URL and uses it as the `href` attribute of an anchor element.

The lab describes code with this general pattern:

```javascript
$(function() {
    $('#backLink').attr(
        "href",
        (new URLSearchParams(window.location.search)).get('returnUrl')
    );
});
```

The important parts are:

- **Source — `location.search` / `window.location.search`:** The URL query string, which can contain user-controlled input.
- **Parameter extraction — `URLSearchParams`:** Reads a named parameter from the query string.
- **Sink — jQuery `.attr("href", value)`:** Sets the destination of the Back link.
- **Trigger — clicking the link:** The supplied value is activated when the user clicks the link.

In the actual lab instructions and URL, the parameter was named `returnPath`. The key issue was that the page accepted a user-controlled destination without safely restricting the URL scheme.

## 3. Investigation Steps

### Step 1: Open the Submit feedback page

I opened the lab and navigated to the Submit feedback page. I located the **Back** link at the bottom of the form.

### Step 2: Test whether the URL controls the link

The starting URL ended with:

```text
/feedback?returnPath=/
```

I changed the parameter to include a harmless test path:

```text
/feedback?returnPath=/test123
```

I reloaded the page, right-clicked the Back link, and selected **Inspect** to examine its HTML in Chrome DevTools.

The purpose of this test was to see whether `/test123` appeared in the link's `href` attribute. This is a simple way to trace user-controlled input without immediately trying an exploit.

### Step 3: Identify the source and sink

I inspected the page in DevTools. The page loaded the jQuery library and a script named `submitFeedback.js`. The lab description explained that the page reads the URL query string and changes the Back link's `href` using jQuery.

This established the relevant data flow:

`URL query parameter → client-side JavaScript → Back link href`

### Step 4: Test the JavaScript URL

In the lab, I changed the `returnPath` value to:

```text
javascript:alert(document.cookie)
```

The resulting URL was:

```text
/feedback?returnPath=javascript:alert(document.cookie)
```

I reloaded the page and clicked the **Back** link. The browser executed the JavaScript URL and displayed an alert containing the cookies accessible through `document.cookie`. The lab was then marked **Solved**.

## 4. Why the Payload Worked

The payload was:

```javascript
javascript:alert(document.cookie)
```

- **`javascript:`** is a URL scheme that can cause JavaScript to execute when used in a link context that permits it.
- **`alert(...)`** opens a browser alert dialog.
- **`document.cookie`** reads cookies available to JavaScript for the current page. Cookies marked `HttpOnly` cannot be read this way.

The vulnerable code put the attacker-controlled value into the link's `href`. When I clicked the link, the browser interpreted the `javascript:` URL as code rather than navigating to a normal page.

The alert was proof of JavaScript execution. This was an authorized training lab, and the payload was used only to demonstrate the vulnerability.

## 5. Source, Sink, and Trigger

| Component | Meaning in this lab |
|---|---|
| Source | `location.search` / `window.location.search` |
| Parameter | `returnPath` in the lab URL |
| Sink | jQuery `.attr("href", value)` |
| Affected element | The Back link |
| Trigger | Clicking the Back link |
| Proof of execution | An alert displaying `document.cookie` |

**Important distinction:** The lab's descriptive example uses the name `returnUrl`, while the actual lab instructions use `returnPath`. I followed the actual lab's `returnPath` parameter.

## 6. What I Observed in DevTools

- The Submit feedback page contained a Back link.
- Chrome DevTools let me inspect the link and its `href` attribute.
- The page loaded jQuery (`jquery_1-8-2.js`) and `submitFeedback.js`.
- A harmless path such as `/test123` was useful for checking whether URL input reached the link.
- After supplying the JavaScript URL and clicking Back, an alert appeared and the lab was solved.

I used DevTools to understand the relationship between the URL parameter and the link, rather than treating the payload as a string to copy without understanding it.

## 7. How Developers Can Prevent This

1. **Validate link destinations.** Accept only expected paths or explicitly permitted URL schemes.
2. **Reject dangerous schemes.** Do not allow user-controlled `javascript:` URLs to become active link destinations.
3. **Use allowlists.** If the Back link should point only to the site homepage or known internal pages, map a small set of allowed values to fixed destinations rather than accepting arbitrary input.
4. **Treat client-side input as untrusted.** URL parameters can be modified by anyone; they should not be trusted simply because they are processed by JavaScript or jQuery.
5. **Use defense in depth.** A Content Security Policy can reduce the impact of some XSS attacks, but it is not a replacement for validating destinations and fixing the unsafe data flow.

### Safer design example

Instead of assigning an arbitrary URL parameter directly to `href`, validate the value against an allowlist of permitted paths and use a safe default if it does not match. For example:

```javascript
const allowedPaths = ["/", "/feedback"];
const requestedPath = new URLSearchParams(window.location.search)
    .get("returnPath");

const safePath = allowedPaths.includes(requestedPath)
    ? requestedPath
    : "/";

document.querySelector("#backLink").setAttribute("href", safePath);
```

This example is illustrative: the allowed paths should match the application's intended navigation behavior.

## 8. What I Learned

- DOM XSS can happen when client-side JavaScript uses URL-controlled data unsafely.
- The source tells me where the input comes from; the sink tells me where it is used.
- An `href` attribute is not automatically safe just because it belongs to a link. The URL scheme matters.
- The vulnerability was triggered by clicking the link, not merely by loading the page.
- A harmless marker such as `/test123` helps confirm the data flow before testing a proof-of-execution payload.
- Developers should validate and restrict link destinations instead of accepting arbitrary user input.

## 9. Reusable Methodology

For similar DOM XSS labs, I can use this process:

1. Locate the feature and the relevant element.
2. Try a harmless marker in the URL parameter.
3. Inspect the element in DevTools to see whether the marker reaches an attribute or another DOM sink.
4. Trace the source, transformation, sink, and trigger.
5. In the authorized lab, use a minimal payload appropriate to the context.
6. Observe the result and verify the lab's status.
7. Record both the exploit mechanism and a practical mitigation.

## 10. Summary

I solved the PortSwigger Apprentice lab by demonstrating that a URL parameter controlled the Back link's `href`. The page accepted a `javascript:` URL, and clicking the link executed `alert(document.cookie)`. This showed how unsafe handling of URL-controlled input in a DOM attribute can lead to DOM-based XSS. The main defensive lesson is to validate link destinations against an allowlist and reject dangerous URL schemes.
