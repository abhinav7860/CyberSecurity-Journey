# PortSwigger Lab: DOM XSS in jQuery Selector Sink Using a `hashchange` Event

**Date:** 14 October 2026  
**Platform:** PortSwigger Web Security Academy  
**Difficulty:** Apprentice  
**Topic:** DOM-based Cross-Site Scripting (DOM XSS)  
**Status:** Solved

## 1. Objective

The goal of this lab was to exploit a DOM-based XSS vulnerability on the blog home page. The page uses jQuery's `$()` selector to locate a post based on the URL hash and automatically scroll to it. I used the Exploit Server to deliver a page that triggered the vulnerable behavior and called `print()` in the browser, as required by the lab.

## 2. Understanding the Vulnerable Pattern

The lab describes code similar to:

```javascript
$(window).on('hashchange', function() {
    var element = $(location.hash);
    element[0].scrollIntoView();
});
```

The intended behavior is to scroll to a post whose identifier matches the URL hash. The security issue is that, in vulnerable jQuery versions or usage patterns, specially crafted input passed to `$()` may be interpreted as HTML rather than only as a selector.

- **Source — `location.hash`:** Reads the part of the URL after `#`.
- **Sink — `$(location.hash)`:** Passes the hash to jQuery's selector function.
- **Trigger — `hashchange`:** Runs the handler when the URL hash changes.
- **Intended behavior:** Find a post and scroll it into view.
- **Required proof:** The browser calls `print()`.

## 3. Exploit Procedure

1. I opened the PortSwigger lab and visited the blog home page.
2. I searched DevTools for `hashchange`, but the search returned no results. I did not confirm why the search failed, so I moved on using the lab's provided exploit pattern.
3. From the lab banner, I opened the **Exploit Server**.
4. In the **Body** field, I entered the following HTML, replacing the placeholder with the active lab hostname:

   ```html
   <iframe src="https://YOUR-LAB-ID.web-security-academy.net/#"
           onload="this.src+='<img src=x onerror=print()>'"></iframe>
   ```

5. I clicked **Store**, then **View exploit** to test it.
6. The iframe loaded the vulnerable page. Its `onload` handler changed the URL hash by appending the image markup.
7. After testing the exploit, I returned to the Exploit Server and clicked **Deliver to victim**.
8. The lab was marked **Solved**.

## 4. How the Payload Works

### Part A — Load the vulnerable page

```html
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/#">
```

The iframe loads the lab's blog page with an empty hash.

### Part B — Trigger a hash change automatically

```javascript
onload="this.src+='<img src=x onerror=print()>'"
```

The iframe's `onload` handler runs when the iframe finishes loading. It appends text to the iframe URL. Since the appended text follows `#`, the hash changes and triggers the vulnerable page's `hashchange` handler without requiring the victim to click a link.

### Part C — Trigger JavaScript execution

```html
<img src=x onerror=print()>
```

- `<img>` creates an image element.
- `src=x` attempts to load an invalid or unavailable image resource.
- `onerror=print()` calls `print()` when the image fails to load.
- `print()` opens the browser's print dialog, which is the behavior the lab asks us to trigger.

In the vulnerable pattern, the crafted hash reaches jQuery's `$()` selector. Under the vulnerable behavior, the injected markup can be interpreted as HTML, causing the image error handler to execute.

## 5. Full Data Flow

`Exploit Server page → iframe loads lab page → iframe onload changes URL hash → hashchange event fires → location.hash reaches jQuery $() → injected image is interpreted → image error event calls print()`

The iframe was used to trigger the hash change automatically, which caused the vulnerable code to run without user interaction.

## 6. Why DevTools Search Did Not Help

I searched for `hashchange` in DevTools, but it returned no matches. I did not establish the exact reason. A failed search does not by itself mean the lab is broken. I continued using the lab description and supplied exploit pattern, then verified the behavior through the Exploit Server.

## 7. How Developers Can Prevent This

1. **Avoid passing untrusted strings into jQuery `$()` as selectors.** Use APIs that treat input as an identifier or value, not as HTML.
2. **Validate hash values.** If the page expects a post ID, validate it against the expected format before using it.
3. **Use direct DOM lookups.** For an expected element ID, use a validated ID with `document.getElementById()` rather than passing arbitrary input to a selector that may parse HTML.
4. **Keep data separate from markup.** Avoid allowing URL-controlled strings to be interpreted as HTML.
5. **Update dependencies.** Modern jQuery versions include protections against some historical selector-related injection patterns. Updating helps, but application code must still be reviewed.

### Safer illustrative pattern

```javascript
$(window).on('hashchange', function() {
    const id = location.hash.slice(1);

    if (!/^[a-zA-Z0-9_-]+$/.test(id)) {
        return;
    }

    const element = document.getElementById(id);
    if (element) {
        element.scrollIntoView();
    }
});
```

This example is illustrative. Real validation should match the application's legitimate post identifier format.

## 8. What I Learned

- `location.hash` is a user-controllable source.
- jQuery's `$()` can be a dangerous sink in certain historical usage patterns.
- `hashchange` runs the vulnerable handler when the URL hash changes.
- An iframe can load a page and change its hash automatically.
- `onerror` can trigger a proof of JavaScript execution when an image fails to load.
- DevTools search is useful, but if it does not find a string, I can try another investigation path and use the lab's supplied hints.
- A successful exploit requires understanding the source, sink, and trigger—not just copying a payload.

## 9. Reusable Methodology

1. Identify the input source, such as `location.search` or `location.hash`.
2. Identify where the input is used, such as `innerHTML`, `document.write`, an attribute setter, or a selector.
3. Determine what event or action triggers the vulnerable code.
4. Start with harmless input to confirm the data flow when possible.
5. In an authorized lab, test the required proof-of-execution behavior.
6. If source search fails, try another inspection method or use the lab's supplied hints.
7. Verify the lab status and document both the exploit chain and the defensive fix.

