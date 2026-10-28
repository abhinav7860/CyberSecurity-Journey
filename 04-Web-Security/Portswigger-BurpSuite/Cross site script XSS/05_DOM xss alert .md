# PortSwigger Web Security Academy — DOM XSS in `document.write` Sink Using `location.search`

## Lab Details

- **Platform:** PortSwigger Web Security Academy
- **Lab:** DOM XSS in `document.write` sink using source `location.search`
- **Difficulty:** Apprentice
- **Category:** Cross-Site Scripting (XSS) — DOM-based
- **Objective:** Trigger `alert(1)` through the vulnerable search functionality
- **Observed result:** The browser displayed an alert containing `1`.
- **Final lab status:** Check the PortSwigger badge after dismissing the alert to confirm it says **Solved**.

---

## 1. What Is the DOM?

DOM stands for **Document Object Model**.

When a browser loads a webpage, it represents the page as a structured collection of objects. JavaScript can read and change these objects after the page loads.

For example, a page may contain:

```html
<h1>Welcome</h1>
<p>This is my website.</p>
```

JavaScript can change the heading without requesting a new page:

```javascript
document.querySelector("h1").textContent = "Hello!";
```

The browser updates the heading in the current page. This is why the DOM matters: client-side JavaScript can dynamically change the page after the original HTML response has arrived.

## 2. What Is DOM-Based XSS?

**DOM-based Cross-Site Scripting (DOM XSS)** occurs when client-side JavaScript takes data that an attacker can influence and uses it in an unsafe way, allowing the browser to interpret it as HTML or executable code.

A common example is JavaScript reading information from the URL and placing it into the page without safely handling it.

The general flow is:

```text
Attacker-controlled input
        ↓
JavaScript reads the input
        ↓
Input reaches an unsafe operation
        ↓
Browser interprets the result
        ↓
Possible JavaScript execution
```

DOM XSS does not necessarily require the server to reflect the malicious input into the original HTML response. The vulnerable processing can happen in JavaScript running in the browser.

## 3. Understanding Source and Sink

The most important concept I learned was how to identify a **source** and a **sink**.

### Source — where the data comes from

A source is a place where JavaScript obtains data that may be controlled by a user.

Examples include:

- `location.search` — the URL query string
- `location.hash` — the fragment after `#`
- `window.location` — information about the current URL

In this lab, the source was:

```javascript
location.search
```

My search URL looked like:

```text
https://<lab-id>.web-security-academy.net/?search=mango
```

The query string `?search=mango` contains the value I entered in the search box.

### Sink — where the data is used

A sink is a function or property that receives and uses the data. Some sinks can interpret input as HTML or JavaScript.

The sink in this lab was:

```javascript
document.write()
```

`document.write()` writes content into the document, where the browser may interpret the content as HTML.

### Source-to-sink flow in this lab

```text
Search term in URL
        ↓
location.search                 SOURCE
        ↓
Client-side JavaScript
        ↓
document.write()                SINK
        ↓
HTML is written into the page
        ↓
Potential DOM XSS
```

A source and a sink alone do not automatically mean that a vulnerability exists. The data must reach the sink in a way that permits unsafe interpretation or execution.

## 4. DOM XSS Compared with Reflected and Stored XSS

| Type | General behavior |
|---|---|
| Reflected XSS | User input is returned in the server response and interpreted unsafely by the browser. |
| Stored XSS | User input is saved by the application and later delivered to users in an unsafe context. |
| DOM-based XSS | Client-side JavaScript processes data unsafely, creating the vulnerability in the browser. |

These categories can overlap. The important part of investigating DOM XSS is tracing the client-side source-to-sink data flow.

## 5. Lab Objective and Initial Test

The lab description explained that the search-query tracking functionality used `document.write()` with data from `location.search`.

The objective was to execute:

```javascript
alert(1)
```

I opened the lab and searched for a harmless word:

```text
mango
```

The browser URL then contained:

```text
?search=mango
```

At this stage, I had a simple input that I could recognize when inspecting the page.

## 6. Inspecting the DOM in Chrome

I opened Chrome Developer Tools using **F12** and selected the **Elements** tab.

I expanded the page's DOM structure until I found this line:

```html
<img src="/resources/images/tracker.gif?searchTerms=mango">
```

This was an important discovery.

It showed that my search term, `mango`, appeared in the image's `src` attribute in the current DOM.

### What the line meant

- `<img>` creates an image element.
- `src` specifies the image URL.
- `tracker.gif` was the image resource.
- `searchTerms=mango` showed that my search term had been included in the tracking URL.

The Elements panel shows the current DOM, including changes made by JavaScript. This is useful for DOM XSS testing because the page can be modified after the original server response.

### Why this was useful

I now knew where my input appeared and the HTML context in which it appeared: inside an image `src` attribute.

That gave me a concrete place to investigate instead of guessing where the input was being used.

The screenshot showed the resulting DOM. The lab description identified `document.write()` as the sink; the DOM inspection helped me see the result of the processing.

## 7. Understanding the HTML Context

The ordinary input resulted in markup conceptually similar to:

```html
<img src="mango">
```

In a normal case, the browser treats `mango` as part of the attribute value.

The security question was whether carefully crafted input could change how the browser interpreted this HTML.

The idea was to attempt to leave the existing quoted attribute, close the current tag, and introduce a new element. This is why understanding the surrounding HTML context matters when investigating XSS.

## 8. Proof of Concept Used in the Lab

For this authorized PortSwigger lab, I submitted the following value through the search functionality:

```html
"><svg onload=alert(1)>
```

### What each part was intended to do

| Part | Purpose |
|---|---|
| `"` | Attempts to close the existing quoted attribute. |
| `>` | Attempts to close the current HTML tag. |
| `<svg ...>` | Introduces an SVG element into the HTML. |
| `onload` | Defines an event handler that runs when the element loads. |
| `alert(1)` | Provides a visible proof that JavaScript executed. |

The key idea was not simply to enter unusual characters. It was to change the browser's interpretation from an ordinary attribute value to a new HTML element with an event handler.

## 9. Observed Result

After submitting the proof of concept, Chrome displayed a JavaScript alert containing:

```text
1
```

This confirmed that the JavaScript proof of concept executed.

The lab badge in the screenshot still displayed **Not solved** while the alert was open. After dismissing the alert, I needed to check the lab status again to confirm that PortSwigger marked it as solved.

## 10. Complete Investigation Flow

```text
1. Open the PortSwigger lab
        ↓
2. Search for "mango"
        ↓
3. Observe ?search=mango in the URL
        ↓
4. Open Chrome Developer Tools with F12
        ↓
5. Select Elements
        ↓
6. Expand the DOM
        ↓
7. Find the tracker image containing searchTerms=mango
        ↓
8. Identify the HTML context: image src attribute
        ↓
9. Use the lab proof of concept in the search box
        ↓
10. Submit the search
        ↓
11. Browser displays alert(1)
        ↓
12. Check the final lab status
```

## 11. How to Apply This Method to Other DOM XSS Labs

The objective is to reuse the investigation method, not blindly copy a payload.

### Step 1 — Identify a possible source

Look for data that may be controlled by the user, such as URL query parameters or fragments.

### Step 2 — Find where the value appears or is used

For HTML-related flows, inspect the live DOM in Developer Tools. For JavaScript execution sinks, search the loaded source code and trace the value using the debugger.

### Step 3 — Identify the sink

Determine whether the data reaches an operation that interprets it as HTML or executable code, such as `innerHTML`, `document.write()`, or `eval()`.

These sinks have different behaviors, so context matters.

### Step 4 — Understand the context

Determine whether the input is inside ordinary text, a quoted attribute, JavaScript code, a URL, or another context.

### Step 5 — Verify safely in the authorized lab

Use the lab's stated objective and a harmless proof of concept to confirm whether the input can cause JavaScript execution.

### Step 6 — Record evidence

Note the source, sink, HTML context, input used, browser behavior, and final lab status.

## 12. Where This Knowledge Is Useful

This method is useful when learning to test:

- Search parameters
- URL query strings
- URL fragments
- Client-side tracking code
- Dynamic HTML rendering
- DOM manipulation
- Input handling and output encoding
- Client-side JavaScript data flows

Only test applications where I have explicit authorization.

## 13. Security Lessons

### Lesson 1 — A URL can be a source

The URL is not always just navigation information. Client-side JavaScript can read it and use its values elsewhere in the page.

### Lesson 2 — The sink determines how data is interpreted

`document.write()` writes content into the document. When untrusted input is included without appropriate handling, the browser may interpret it as HTML.

### Lesson 3 — Inspect the live DOM

The Elements panel can show changes made by JavaScript after the original page load. It is therefore useful when investigating DOM-based behavior.

### Lesson 4 — Context matters

Finding input in the DOM is only the beginning. I need to identify its exact context to understand whether it can change the page's structure.

### Lesson 5 — Confirm execution and lab status separately

The alert confirmed that the proof of concept ran. The PortSwigger lab badge is a separate check for whether the challenge has been marked solved.

## 14. Defensive Takeaways

Developers should avoid inserting untrusted data into HTML-parsing sinks such as `document.write()` when possible.

For plain text, safer APIs such as `textContent` should be preferred. Where dynamic HTML is genuinely required, use an appropriate, well-maintained sanitization approach and apply context-aware output handling.

Input validation alone is not a substitute for safe output handling.

## 15. Summary

- **Vulnerability:** DOM-based Cross-Site Scripting
- **Source:** `location.search`
- **Sink:** `document.write()`
- **Input location observed:** `img` element's `src` attribute
- **Proof-of-concept objective:** Execute `alert(1)`
- **Observed result:** Browser displayed an alert containing `1`
- **Final lab status:** Verify the badge after dismissing the alert

## Final Takeaway

The most valuable part of this lab was learning to follow the data:

```text
Where does the input come from?
        ↓
Where does JavaScript send it?
        ↓
How does the browser interpret it?
        ↓
Can that interpretation cause execution?
```

That source-to-sink reasoning is more reusable than memorizing a single payload.

---

**Platform:** PortSwigger Web Security Academy  
**Lab:** DOM XSS in `document.write` sink using source `location.search`
