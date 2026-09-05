# PortSwigger Web Security Academy – Reflected XSS into HTML Context with Most Tags and Attributes Blocked

## Lab Information

- **Difficulty:** Practitioner
- **Vulnerability:** Reflected Cross-Site Scripting (XSS)
- **Protection:** Web Application Firewall (WAF)
- **Goal:** Execute `print()` without user interaction

## 1. Objective

This lab contained a reflected XSS vulnerability in the search functionality. A WAF blocked many common XSS tags and attributes.

The goal was to bypass those restrictions and cause `print()` to execute automatically.

The important lesson was not memorizing one payload, but learning how to discover what a WAF allows and then build an exploit from those allowed components.

## 2. Initial Test

I first tested the standard payload:

```html
<img src=1 onerror=print()>
```

The application returned:

```text
"Tag is not allowed"
```

This showed that the WAF was blocking the obvious XSS vector.

## 3. Sending the Request to Burp Intruder

I sent the search request to:

```text
Burp → Intruder
```

The search value was changed to:

```html
<>
```

I placed an Intruder payload position between the angle brackets:

```text
<§§>
```

This allowed Intruder to test many HTML tags automatically.

## 4. Finding an Allowed HTML Tag

I used the PortSwigger XSS Cheat Sheet and copied its tag list into:

```text
Intruder → Payloads → Payload configuration → Paste
```

The list contained 143 tags.

I started the attack and compared the HTTP status codes.

Most tags returned:

```text
400
```

One important result returned:

```text
body → 200
```

Therefore I discovered that:

```html
<body>
```

was allowed by the WAF.

The important methodology was:

```text
Test many tags
    ↓
Compare responses
    ↓
Find a different/allowed response
    ↓
Identify an allowed tag
```

## 5. Finding an Allowed Event Handler

Finding `<body>` was not enough. I still needed an event handler that could execute JavaScript.

The lab provided the next template:

```html
<body%20=1>
```

`%20` is URL encoding for a space, so conceptually this represents:

```html
<body =1>
```

I placed the Intruder position before the `=`:

```html
<body%20§§=1>
```

This allowed Intruder to test different event-handler names.

I cleared the previous payload list and pasted the event-handler list from the PortSwigger XSS Cheat Sheet.

I started the second attack.

Most events returned:

```text
400
```

The important result was:

```text
onresize → 200
```

So I had discovered two useful pieces:

```text
Allowed tag   → body
Allowed event → onresize
```

## 6. Understanding Why `onresize` Was Chosen

`onresize` was not randomly selected.

It was selected because the Intruder scan showed that the WAF allowed it.

Conceptually, I could now form:

```html
<body onresize=JavaScript>
```

For this lab, the required JavaScript was:

```text
print()
```

However, the lab specifically said that manually causing `print()` to run in my own browser would not solve it.

Therefore I needed the resize event to happen automatically.

## 7. The Exploit Server

I used the PortSwigger Exploit Server to deliver a crafted HTML page to the simulated victim.

The exploit used an iframe that loaded the vulnerable lab page.

The iframe also changed its own width when it loaded.

The important idea was:

```text
iframe loads
    ↓
its width changes automatically
    ↓
a resize event occurs
    ↓
the allowed onresize handler executes
    ↓
print() runs
```

I did not need the victim to click or manually resize anything.

## 8. Final Exploit Concept

I am intentionally not treating the final exploit string as something to memorize.

The exploit was a combination of:

```text
Reflected search input
        +
HTML injection
        +
WAF-allowed <body> tag
        +
WAF-allowed onresize event
        +
print()
        +
automatic iframe resize
```

The URL used encoded characters such as:

```text
%22 → "
%3C → <
%3E → >
%20 → space
```

This allowed the required HTML structure to be represented safely inside the URL parameter.

## 9. Delivering the Exploit

In the Exploit Server I placed the iframe-based exploit in the **Body** field.

I then:

1. Clicked **Store**.
2. Clicked **Deliver exploit to victim**.
3. Waited for the simulated victim to load the page.
4. The iframe automatically changed size.
5. The resize event triggered the XSS.
6. `print()` executed.
7. The lab detected the successful exploit.

The lab was then solved.

## 10. Complete Attack Flow

```text
Normal XSS attempt
        ↓
WAF blocks it
        ↓
Send search request to Intruder
        ↓
Test HTML tags
        ↓
<body> returns 200
        ↓
Test event handlers on <body>
        ↓
onresize returns 200
        ↓
Build an XSS using body + onresize
        ↓
Need automatic execution
        ↓
Use iframe + automatic width change
        ↓
Resize event fires
        ↓
print() executes
        ↓
Deliver exploit to victim
        ↓
Lab solved
```

## 11. What the Exploit Means

The exploit was not a single magical payload.

It was a **WAF-bypass strategy**.

The WAF blocked common XSS vectors, but it did not block every possible combination of HTML and browser events.

I used Burp Intruder to discover:

```text
What is blocked?
What is allowed?
```

Then I combined the allowed components into an executable HTML context.

This is the main skill I want to remember.

## 12. How I Can Use This Idea in Other Labs

I should not copy the exact payload blindly.

When I encounter a similar XSS/WAF challenge, I can use this process:

### Step 1 — Identify the injection context

Ask where my input appears:

```text
HTML body
HTML attribute
JavaScript
URL
CSS
```

The context determines which techniques may work.

### Step 2 — Try a simple proof of concept

Start with a harmless XSS test appropriate for the context.

The goal is to determine whether my input can become executable.

### Step 3 — Study the filter

If the WAF blocks the obvious payload, determine what it is actually blocking:

```text
Tags?
Attributes?
Event handlers?
Characters?
Keywords?
```

### Step 4 — Test systematically

If there are many possibilities, use Burp Intruder to test them and compare responses.

A response such as `200` can be a useful clue, but it is not automatically proof of execution.

### Step 5 — Combine allowed components

If an allowed tag and event handler can form a valid HTML/JavaScript context, reason about how they can be combined.

### Step 6 — Consider automatic triggering

If the challenge requires no user interaction, think about browser events that can occur automatically.

### Step 7 — Deliver the exploit

In PortSwigger labs, the Exploit Server can be used when the lab requires delivery to the simulated victim.

## 13. Where This Methodology Is Useful

### Reflected XSS

Useful for inputs such as:

- Search parameters
- Query parameters
- Error messages
- Filters
- URL parameters
- Form values

### Stored XSS

Similar reasoning can apply to:

- Comments
- Reviews
- Profiles
- Forum posts
- Support tickets
- Chat messages

The difference is that stored XSS is saved by the application and executed later.

### WAF Testing

Useful when a WAF blocks common payloads.

Instead of asking:

```text
"What payload can I copy?"
```

ask:

```text
"What does the filter reject?
What does it still allow?
Can the allowed pieces produce executable HTML?"
```

Only perform this testing against systems where I have authorization.

## 14. Mistakes and Lessons

### Mistake 1 — Expecting the normal payload to work

The standard `<img>`/`onerror` payload was blocked.

**Lesson:** A WAF may block common vectors, so I need to understand its behavior.

### Mistake 2 — Thinking `onresize` was arbitrary

It was discovered through the second Intruder scan.

**Lesson:** The final exploit was based on evidence from the application's responses.

### Mistake 3 — Not understanding `%20`

`%20` simply represents a URL-encoded space.

**Lesson:** URL encoding is important when working with payloads inside query parameters.

### Mistake 4 — Manually triggering the event

The lab required automatic execution.

**Lesson:** When a lab says no user interaction, the exploit needs an automatic trigger.

## 15. Key Concepts

### Reflected XSS

```text
User input
    ↓
Server response
    ↓
Input reflected into HTML
    ↓
Browser interprets it
    ↓
JavaScript executes
```

### WAF

A WAF can block known attack patterns, but it should not be considered a replacement for secure application design and output encoding.

### Burp Intruder

Useful for systematically testing many possible values and identifying differences in application behavior.

### Exploit Server

Useful in PortSwigger labs for hosting a crafted page and delivering it to the simulated victim.

### Event Handlers

HTML event handlers execute JavaScript when browser events occur.

In this lab:

```text
resize event
    ↓
onresize
    ↓
print()
```

## 16. Final Result

```text
Vulnerability: Reflected XSS
Protection: WAF

Allowed tag discovered:
<body>

Allowed event discovered:
onresize

Required function:
print()

Delivery:
Exploit Server + iframe

Result:
✅ LAB SOLVED
```

## 17. Final Takeaway

The most important thing I learned was the methodology:

```text
Understand the context
        ↓
Test the obvious approach
        ↓
Observe what the WAF blocks
        ↓
Systematically discover what it allows
        ↓
Combine the allowed components
        ↓
Find an automatic trigger
        ↓
Deliver the exploit
```

This approach is more useful than memorizing a single XSS payload because the exact allowed tag, attribute, event, and injection context can change from one application or lab to another.

---

