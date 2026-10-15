# PortSwigger Lab: DOM XSS in `innerHTML` Sink Using Source `location.search`

**Date:** 13 October 2026  
**Platform:** PortSwigger Web Security Academy  
**Difficulty:** Apprentice  
**Topic:** DOM-based Cross-Site Scripting (DOM XSS)  
**Status:** Solved

## 1. Objective

The objective of this lab was to exploit a DOM-based XSS vulnerability in the blog search functionality. The page used data from the URL query string (`location.search`) and inserted it into a `div` using `innerHTML`. I solved the lab by making the browser execute JavaScript that displayed an alert.

## 2. Understanding the Source and Sink

- **Source — `location.search`:** Provides the query-string portion of the current URL. User-controlled values can enter the page through this source.
- **Sink — `innerHTML`:** Sets an element's HTML content. If untrusted input is inserted into it without appropriate handling, the browser may parse that input as HTML.
- **DOM-based XSS:** The vulnerable behavior happens in the browser when client-side JavaScript processes input and sends it to an unsafe DOM sink.

The important data flow was:

`URL query string → location.search → innerHTML → browser parses injected HTML → event handler executes`

## 3. How I Tested the Search Input

1. I opened the lab and used the blog search functionality.
2. I first searched for a harmless test term, `mango`, to see how the search feature behaved.
3. I inspected the page with Chrome DevTools. In the **Elements** panel, I looked for where the search term appeared in the rendered page.
4. The lab description identified the vulnerable flow as data from `location.search` being used to update a `div` through `innerHTML`. This gave me a source to trace and a sink to inspect.
5. I then tested the lab's HTML injection behavior using this payload in the search box:

   ```html
   <img src=1 onerror=alert(1)>
   ```

6. I clicked **Search**. The browser displayed an alert, confirming that the injected event handler executed JavaScript.

## 4. Why the Payload Worked

The payload was:

```html
<img src=1 onerror=alert(1)>
```

- `<img>` creates an image element.
- `src=1` points to an invalid or unavailable image resource in this context.
- `onerror=alert(1)` runs when the image fails to load.
- If the page inserts this input into `innerHTML` without safe handling, the browser parses it as an image element and registers its event handler.

The image-loading error triggers the handler, which calls `alert(1)`. The alert is proof that JavaScript execution was achieved through the DOM injection.

### Why I did not rely on `<script>` or `<svg onload>`

In this lab context, script elements inserted through `innerHTML` do not execute in modern browsers, and the lab notes that an SVG `onload` handler does not fire in this context. An image element with an `onerror` handler is a suitable test because it uses an event triggered by a failed resource load.

## 5. What I Observed in DevTools

- I used the **Elements** panel to inspect the rendered page and understand where the search term appeared.
- I connected the lab's stated source, `location.search`, to the sink, `innerHTML`.
- After submitting the payload, I observed the JavaScript alert.
- The alert demonstrated successful JavaScript execution. I then confirmed that the lab was marked **Solved**.

**Note:** These notes record the observed result from this lab run; they do not include a copied source-code listing because I did not save the full page script as an artifact.

## 6. How Developers Can Prevent This Vulnerability

1. **Prefer `textContent` for plain text.** If the search term only needs to be displayed as text, use `element.textContent = userInput` instead of `element.innerHTML = userInput`.
2. **Avoid putting untrusted input into HTML-parsing sinks.** Do not concatenate user-controlled data into HTML strings that are assigned to `innerHTML`.
3. **Use safe DOM construction when HTML is required.** Create elements with DOM APIs and set text using `textContent` rather than building markup from untrusted strings.
4. **Sanitize HTML when rich HTML is genuinely required.** Use a reputable, maintained HTML sanitizer configured for the application's needs. Encoding alone is not a universal substitute when intentionally accepting HTML.
5. **Apply defense in depth.** A well-configured Content Security Policy (CSP) can reduce the impact of some XSS payloads, but it should not replace fixing the unsafe DOM data flow.

### Safer example

Vulnerable pattern:

```javascript
result.innerHTML = userInput;
```

Safer when displaying plain text:

```javascript
result.textContent = userInput;
```

The safe choice depends on the intended behavior. For a search-result label or echoed search term, plain-text rendering is usually sufficient.

## 7. What I Learned

- A DOM XSS vulnerability can occur entirely in client-side code.
- The **source** is where attacker-controlled data enters the client-side flow; the **sink** is where that data is used in a potentially dangerous way.
- `location.search` can contain user-controlled query-string data.
- `innerHTML` parses input as HTML, which can turn an input string into active markup.
- An event handler such as `onerror` can execute JavaScript when its triggering event occurs.
- The right fix is to avoid unsafe HTML insertion, especially when plain text is all that is needed.

## 8. Reusable Methodology for Similar Labs

1. Start with a harmless marker such as `mango`.
2. Inspect where the marker appears in the page using DevTools **Elements**.
3. Use **Sources** or the available scripts to trace how the value is read and where it is inserted.
4. Identify the source and sink rather than guessing payloads immediately.
5. In an authorized lab, test a minimal proof-of-execution payload suited to the sink's behavior.
6. Observe the result and verify the lab's final status.
7. Document the data flow, the reason the test worked, and a safe coding alternative.

## 9. Summary

I solved the Apprentice DOM XSS lab by testing the blog search input with `<img src=1 onerror=alert(1)>`. The browser parsed the injected markup through the vulnerable `innerHTML` flow, the image failed to load, and its `onerror` handler displayed `alert(1)`. The key defensive lesson is to use `textContent` for plain-text output and avoid passing untrusted input into `innerHTML`.
