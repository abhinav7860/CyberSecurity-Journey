# PortSwigger Lab – Reflected XSS into HTML Context with Nothing Encoded

**Difficulty:** Apprentice
**Vulnerability:** Reflected Cross-Site Scripting (XSS)
**Function Tested:** Search functionality
**Goal:** Execute `alert(1)`

---

## 1. Understanding the Lab

The lab had a search functionality that was vulnerable to **Reflected XSS**.

The main idea was:

```text
My input
   ↓
Search request
   ↓
Server
   ↓
Input reflected back in response
   ↓
Browser
   ↓
JavaScript executes
```

The lab was specifically an **HTML context** XSS vulnerability where the input was **not encoded**.

---

## 2. Testing the Search Function

First, I used the search box normally.

I entered:

```text
hello
```

After clicking **Search**, the website displayed my input in the search results.

This showed that my input was being reflected back by the application.

So I understood that the search parameter was potentially vulnerable to reflected XSS.

---

## 3. Understanding Where My Input Was Going

The important thing was that my input was being inserted into the HTML response.

Conceptually, the page was doing something like:

```html
<p>Search results for: hello</p>
```

If the application safely encoded my input, HTML tags would be treated as normal text.

But this lab said that **nothing was encoded**.

So I could try putting HTML into the search input.

---

## 4. Testing JavaScript Execution

The lab specifically asked me to execute the `alert()` function.

I used this payload:

```html
<script>alert(1)</script>
```

I entered it directly into the search box.

---

## 5. What Happened

The application reflected my input into the HTML response.

Instead of the browser treating it as normal text, it interpreted:

```html
<script>
    alert(1)
</script>
```

as JavaScript.

The browser then executed:

```javascript
alert(1)
```

and an alert box appeared.

---

## 6. Why This Worked

The vulnerability can be understood like this:

```text
<script>alert(1)</script>
        ↓
Search input
        ↓
HTTP request
        ↓
Vulnerable server
        ↓
Input reflected into HTML
        ↓
Browser receives HTML
        ↓
<script> is interpreted
        ↓
alert(1) executes
```

The application failed to properly handle the user-controlled input before putting it into the HTML response.

---

## 7. Why Is It Called Reflected XSS?

It is called **Reflected XSS** because my input was:

```text
sent to the server
       ↓
reflected back immediately
       ↓
in the HTTP response
```

It wasn't stored in a database first.

In a real-world attack, an attacker could create a malicious URL containing the payload and try to get another user to visit it.

For this lab, I tested the vulnerability directly in my own browser.

---

## 8. Payload Used

```html
<script>alert(1)</script>
```

### Result:

**JavaScript executed successfully and the lab was solved.**

---

## 9. What I Learned

* XSS happens when user-controlled input can be interpreted as executable content.
* Reflected XSS involves input coming through a request and being reflected in the immediate response.
* The location/context where the input is reflected is important.
* In this lab, the input was reflected directly into an **HTML context**.
* Because the input was not encoded, the `<script>` tag was interpreted by the browser.
* `alert(1)` was used as a proof that JavaScript execution was possible.

---

## Quick Revision

```text
Vulnerability:
Reflected XSS

Input:
Search box

Payload:
<script>alert(1)</script>

Context:
HTML

Encoding:
None

Result:
JavaScript executed → alert appeared → Lab solved
```
