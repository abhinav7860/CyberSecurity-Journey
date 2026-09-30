# Detecting Web Attacks

**Platform:** TryHackMe
**Focus:** SOC / Blue Team
**Topic:** Detecting attacks against web applications
**Date:** 29 September 2026

---

# 1. Introduction

Web applications are one of the most common attack surfaces for an organisation.

Examples include:

* Banking applications
* E-commerce websites
* Login portals
* Employee portals
* APIs
* Customer dashboards
* Web-based administration panels

An attacker can target either:

1. **The user's browser/device** → Client-side attacks
2. **The web application/server/backend** → Server-side attacks

For a SOC analyst, understanding the difference is extremely important because the **visibility and evidence available to the SOC are different**.

---

# 2. Client-Side Attacks

## What is a client-side attack?

A **client-side attack** targets the user, their browser, or their device rather than directly attacking the web server.

The attacker tries to make the victim's browser perform an unintended action.

A simplified flow is:

```text
Attacker
   |
   v
Malicious content
   |
   v
Legitimate Website
   |
   v
Victim's Browser
   |
   v
Malicious Action
```

The important point is:

> The website may be legitimate, but malicious content causes something unwanted to happen in the victim's browser.

---

# 3. Why Client-Side Attacks Are Difficult for SOC Analysts

This is one of the most important concepts from this room.

A SOC normally has visibility into things such as:

* Server logs
* Firewall logs
* Network traffic
* DNS logs
* Authentication logs
* Endpoint logs
* SIEM events

However, these sources may provide **little or no visibility into what is actually happening inside the browser**.

For example:

```text
User
 |
 v
Browser
 |
 | JavaScript executes
 | Cookie/session manipulated
 | DOM modified
 |
 v
Website
```

The malicious activity can happen locally inside the browser.

Therefore, the SOC may not see an obvious malicious network request.

This creates a visibility problem.

### Example

Suppose an attacker manages to inject JavaScript into a trusted website.

The victim visits:

```text
https://example.com
```

The browser loads the page and executes the malicious JavaScript.

The malicious script could potentially attempt to access information available to the browser or manipulate the user's interaction with the page.

From the SOC's perspective, the request may simply look like:

```text
GET /products
200 OK
```

There may be nothing obviously malicious in the HTTP request itself.

---

# 4. Common Client-Side Attacks

The room highlights three important client-side attacks:

1. Cross-Site Scripting (XSS)
2. Cross-Site Request Forgery (CSRF)
3. Clickjacking

---

## 4.1 Cross-Site Scripting — XSS

### What is XSS?

**Cross-Site Scripting (XSS)** occurs when an attacker is able to inject malicious JavaScript into a trusted website and cause that JavaScript to execute in a victim's browser.

For example, imagine a website has a comment box.

An attacker enters:

```html
Hello <script>alert('You have been hacked');</script>
```

If the application does not properly handle the input, another user visiting the page could cause the JavaScript to execute.

Instead of a harmless alert, a real attacker could attempt to perform malicious actions within the victim's browser context.

### Basic idea

```text
Attacker
   |
   | malicious JavaScript
   v
Website
   |
   | stores/displays content
   v
Victim
   |
   | opens page
   v
Browser executes script
```

### Why XSS matters to a SOC

Depending on the situation, XSS can potentially lead to:

* Account compromise
* Session abuse
* Data theft
* Unauthorized actions
* Malicious redirects
* Browser manipulation

### Important SOC limitation

The malicious JavaScript may execute **inside the browser**.

Therefore, traditional server-side logging may not clearly reveal what happened.

---

# 5. Cross-Site Request Forgery — CSRF

## What is CSRF?

**Cross-Site Request Forgery (CSRF)** tricks a victim's browser into sending an unauthorized request to a website where the victim is already authenticated.

The important concept is:

> The attacker abuses the victim's existing authenticated session.

Imagine:

```text
Victim logs into bank.com
        |
        v
Browser has authenticated session
        |
        v
Victim visits malicious website
        |
        v
Malicious website causes browser
to send a request to bank.com
```

The server may receive the request from the victim's authenticated browser.

Therefore, the server may believe that the legitimate user initiated it.

---

# 6. Clickjacking

## What is clickjacking?

Clickjacking involves manipulating the visual interface so that the victim believes they are clicking one thing while actually interacting with another hidden or overlaid element.

For example:

```text
Visible button:
"Play Video"

Hidden underneath:
"Change Account Setting"
```

The user thinks they are clicking the video button, but their click is actually being applied to another element.

---

# 7. Client-Side Attack Detection — SOC Perspective

Client-side attacks are difficult because:

```text
Server logs
     |
     X
Limited visibility into browser execution
```

Additional browser or endpoint security controls can improve visibility.

For a SOC analyst, this teaches an important lesson:

> No single telemetry source gives complete visibility.

You may need to combine:

* Endpoint telemetry
* Browser security controls
* Network traffic
* Web server logs
* Authentication logs
* EDR
* SIEM alerts

---

# 8. Server-Side Attacks

Server-side attacks target the:

* Web server
* Application
* Backend
* Database
* Server-side logic
* Application configuration

Instead of attacking the user's browser, the attacker attempts to manipulate the application or server.

Simplified:

```text
Attacker
   |
   | malicious request
   v
Web Application
   |
   v
Backend
   |
   v
Database / Operating System
```

---

# 9. Why Server-Side Attacks Are Easier to Investigate

One advantage for defenders is that server-side attacks usually generate evidence.

Every request sent to the application can potentially leave traces in:

* Web access logs
* Error logs
* Application logs
* Firewall logs
* Network traffic
* WAF logs
* SIEM
* EDR

For example:

```text
Attacker
   |
   | HTTP request
   v
Web Server
   |
   +----> Access Log
   |
   +----> Error Log
   |
   +----> Network Traffic
   |
   +----> WAF
   |
   v
Application
```

This gives a SOC analyst multiple sources of evidence.

---

# 10. Common Server-Side Attacks

The room focuses on:

1. Brute-force attacks
2. SQL Injection
3. Command Injection

---

# 11. Brute-Force Attacks

A brute-force attack involves repeatedly trying different credentials until valid credentials are discovered.

Example:

```text
POST /login

username=admin
password=123456
```

Then:

```text
POST /login

username=admin
password=password
```

Then:

```text
POST /login

username=admin
password=password123
```

The attacker may automate this process.

---

## What does brute force look like in logs?

A SOC analyst may notice:

```text
POST /login
POST /login
POST /login
POST /login
POST /login
POST /login
```

within a very short period.

Potential indicators include:

* Many authentication attempts
* Same source IP
* Many usernames
* Many passwords
* Unusual User-Agent
* Sudden successful login after many failures
* Login attempts from unusual locations

The important point is that **one failed login is usually not suspicious by itself**.

The pattern is what matters.

---

# 12. SQL Injection — SQLi

## What is SQL Injection?

SQL Injection occurs when an application improperly handles user input and allows an attacker to manipulate the SQL query sent to a database.

The room explains that this commonly occurs when applications construct SQL queries using string concatenation instead of parameterized queries.

Conceptually:

```text
User Input
    |
    v
Web Application
    |
    v
SQL Query
    |
    v
Database
```

If the application does not properly separate data from SQL instructions, attacker-controlled input may alter the intended query.

---

## Example payload from the room

The room demonstrates payloads such as:

```text
' OR '1'='1
```

and:

```text
1' OR 'a'='a
```

These are examples of SQL injection payloads used in the lab.

The important SOC lesson is not simply memorizing the payload.

Instead, understand the pattern:

> Unexpected SQL syntax appearing in web requests can be an indicator of SQL injection attempts.

---

# 13. Command Injection

Command Injection occurs when a web application passes user-controlled input to the operating system without properly validating or handling it.

Conceptually:

```text
User Input
     |
     v
Web Application
     |
     v
Operating System Command
```

If attacker-controlled input becomes part of an operating system command, the attacker may cause the server to execute unintended commands.

This can be extremely serious because the commands execute with the permissions of the application or process.

---

# 14. Log-Based Detection

Logs are one of the most important sources of evidence for a SOC analyst.

Web servers commonly maintain **access logs**.

An access log records information about requests received by the server.

A simplified entry might contain:

```text
Client IP
Timestamp
HTTP Request
Status Code
Response Size
Referrer
User-Agent
```

---

# 15. Understanding Access Log Fields

## 1. Client IP Address

Example:

```text
10.10.10.100
```

This identifies the apparent source of the request.

A SOC analyst may investigate:

* Is the IP internal or external?
* Is it known?
* Is it associated with malicious activity?
* Is the traffic expected?
* Is the IP making unusually large numbers of requests?

### Important

An IP address alone does **not** prove that an attack occurred.

It is an indicator that needs context.

---

# 16. Timestamp

The timestamp tells us when the request occurred.

This allows analysts to build a timeline.

For example:

```text
14:00 - Directory scanning
14:02 - Login attempts
14:03 - Successful login
14:04 - SQL injection
14:07 - Sensitive data access
```

A timeline can reveal the progression of an attack.

---

# 17. Requested Page

Example:

```text
/login.php
```

or:

```text
/changeusername.php
```

The requested resource can provide important context.

For example:

```text
/login.php
```

combined with hundreds of POST requests could indicate authentication abuse.

---

# 18. HTTP Status Code

HTTP status codes provide information about the server's response.

Examples:

```text
200 OK
```

The request succeeded.

```text
404 Not Found
```

The requested resource could not be found.

```text
302 Found
```

The server redirected the client.

In the TryHackMe scenario, a sequence of repeated login attempts followed by a different response code helped indicate a successful login.

### Important SOC lesson

A status code by itself is not malicious.

You need to understand it **in context**.

---

# 19. Response Size

The response size can sometimes reveal unusual activity.

For example:

```text
Normal response:
532 bytes
```

while another request returns:

```text
250000 bytes
```

A large difference could deserve investigation.

Again, this is an indicator rather than proof.

---

# 20. Referrer

The Referrer field can show where the request originated from.

Unexpected navigation patterns can sometimes provide additional context.

For example:

```text
Normal:
Homepage -> Product -> Checkout
```

versus:

```text
Unknown external page -> sensitive endpoint
```

The referrer must always be interpreted carefully because it can be missing or manipulated.

---

# 21. User-Agent

The User-Agent identifies the software making the HTTP request.

Normal example:

```text
Mozilla/5.0
```

Security tools may identify themselves.

Examples from the room include:

```text
sqlmap
wpscan
```

The TryHackMe investigation also identified:

```text
ffuf v2.1.0
```

during directory fuzzing.

A suspicious User-Agent can therefore provide valuable evidence.

However:

> User-Agent values can be changed or spoofed.

Therefore, they should not be treated as definitive proof.

---

# 22. Attack Sequence in Web Logs

The TryHackMe scenario demonstrates an entire attack chain.

The attacker first performs:

### Step 1 — Directory Fuzzing

The attacker searches for valid directories, files, forms, or endpoints.

For example:

```text
GET /admin
GET /login.php
GET /backup
GET /config
```

The attacker looks for responses indicating that interesting resources exist.

The room notes that `200` responses can indicate valid finds.

---

# 23. Step 2 — Brute Force

After discovering:

```text
/login.php
```

the attacker repeatedly submits login requests.

For example:

```text
POST /login.php
POST /login.php
POST /login.php
POST /login.php
POST /login.php
```

The requests occur rapidly.

This creates a recognizable pattern.

---

# 24. Step 3 — Successful Authentication

Eventually one request receives a different response.

The room uses:

```text
302 Found
```

as an indication of a successful login attempt in this scenario.

The attacker is then redirected to:

```text
/account
```

This is an important point in investigation.

A sequence like:

```text
Many failed attempts
        ↓
Different response
        ↓
Redirect
        ↓
Account page
```

can indicate credential compromise.

---

# 25. Step 4 — SQL Injection

After gaining access, the attacker targets another form.

The room gives examples such as:

```text
' OR '1'='1
```

and:

```text
1' OR 'a'='a
```

The attacker attempts to manipulate the database query.

In the investigation, the decoded SQL injection payload was:

```text
%' OR '1'='1
```

on:

```text
/changeusername.php
```

---

# 26. Attack Chain — SOC View

The entire attack can therefore be represented as:

```text
Directory Fuzzing
       |
       v
Discover login.php
       |
       v
Brute Force
       |
       v
Successful Login
       |
       v
Access Account
       |
       v
SQL Injection
       |
       v
Database Access
       |
       v
Sensitive Data
```

This is exactly the kind of sequence a SOC analyst should learn to recognize.

Instead of investigating each log independently, connect them into a **timeline**.

---

# 27. Log Limitations

Logs are extremely useful, but they are not perfect.

One important limitation is that access logs may not contain the entire HTTP request.

For example:

```text
POST /login HTTP/1.1
```

may be logged.

But the actual POST body may not be logged.

Therefore, the analyst may know:

> A login attempt happened.

But may not know:

> Exactly which username and password were submitted.

---

# 28. GET vs POST Visibility

GET requests commonly place parameters in the URL.

Example:

```text
GET /search?q=test
```

The query string may appear in an access log.

POST requests normally place data inside the request body.

Example:

```text
POST /login

username=admin&password=password123
```

The access log may only show:

```text
POST /login
```

without the submitted credentials.

Therefore:

```text
Access logs
     |
     +---- Request metadata
     |
     X---- May not contain POST body
```

This is one reason network captures can provide additional evidence.

---

# 29. Network-Based Detection

Network traffic analysis allows analysts to inspect the actual communication between systems.

Tools such as **Wireshark** can provide much more detailed information than a basic access log.

Depending on the protocol and encryption, network captures may reveal:

* HTTP headers
* HTTP requests
* HTTP responses
* POST bodies
* Cookies
* Files
* User-Agent
* Parameters
* Application data

---

# 30. Why Network Traffic Can Be More Useful

Compare:

### Web access log

```text
POST /login HTTP/1.1
200
```

versus network capture:

```text
POST /login HTTP/1.1

username=admin
password=password123
```

The second contains much more information.

This can allow the analyst to understand **what the attacker actually sent**.

---

# 31. Important Limitation — Encryption

HTTPS encrypts application traffic.

Therefore, a network capture may not provide the plaintext contents of HTTPS traffic unless the analyst has appropriate access to decrypt the traffic.

Conceptually:

```text
HTTP
 |
 v
Readable packet contents

HTTPS
 |
 v
Encrypted application data
```

Therefore, network visibility depends heavily on the protocol and available decryption capabilities.

---

# 32. Wireshark Investigation

The TryHackMe scenario follows the same attack sequence:

```text
Directory fuzzing
       ↓
Brute force
       ↓
Successful login
       ↓
SQL Injection
```

Wireshark allows the analyst to inspect the individual packets associated with these actions.

---

# 33. HTTP User-Agent Filtering

The room demonstrates filtering network traffic based on:

```text
http.user_agent
```

This can help identify traffic generated by particular tools.

For example:

```text
sqlmap
```

or:

```text
ffuf
```

This is useful because it narrows a large packet capture down to traffic matching a specific characteristic.

---

# 34. Investigating the Brute Force

The analyst can examine the login requests.

Unlike the basic access log, the packet can reveal the actual submitted values.

In the TryHackMe example, packet 13 contained the successful login attempt.

The discovered password was:

```text
password123
```

and the account was an admin account.

This demonstrates why weak credentials can make brute-force attacks successful.

---

# 35. Investigating SQL Injection Through Network Traffic

The network capture can reveal the SQL injection payload itself.

For example:

```text
' OR '1'='1
```

The analyst can then inspect the response.

In the TryHackMe example, the SQL injection resulted in the Users table being exposed, including:

* First name
* Surname

This is valuable evidence because the analyst can see not only:

> An SQL injection attempt occurred.

but also:

> What the attacker attempted and what information was returned.

---

# 36. Web Application Firewall — WAF

A **Web Application Firewall (WAF)** is a security control designed to inspect and filter HTTP/HTTPS requests to web applications.

Think of a WAF as a security checkpoint:

```text
Internet
   |
   v
+-------+
|  WAF  |
+-------+
   |
   | Allowed
   v
Web Application
```

Suspicious traffic can be blocked before reaching the application.

---

# 37. WAF vs Traditional Firewall

A traditional network firewall generally focuses on network-level information such as:

* IP addresses
* Ports
* Protocols

A WAF focuses specifically on web application traffic.

It can inspect things such as:

* HTTP methods
* URLs
* Headers
* Parameters
* User-Agent
* Request content
* Known attack patterns

---

# 38. WAF Rules

The room describes several types of rules.

## 38.1 Block Common Attack Patterns

The WAF can look for known malicious patterns.

For example:

```text
sqlmap
```

in a User-Agent.

---

# 39. Deny Known Malicious Sources

A WAF can use:

* Threat intelligence
* IP reputation
* Known malicious IP addresses
* Geographic restrictions

For example:

```text
Known malicious IP
       |
       v
      WAF
       |
       v
     BLOCK
```

---

# 40. Custom Rules

Organisations can create application-specific rules.

For example:

```text
If request is not GET or POST
to /login
    |
    v
BLOCK
```

Custom rules can be useful because every application has different normal behavior.

---

# 41. Rate Limiting

Rate limiting restricts how frequently a client can perform an action.

Example:

```text
Maximum:
5 login attempts / minute / IP
```

If the attacker exceeds the limit:

```text
Too many requests
       |
       v
Challenge / Block
```

This can help mitigate:

* Brute-force attacks
* Automated scanning
* Bot activity
* Request abuse

---

# 42. WAF Challenge-Response Mechanisms

A WAF does not always have to completely block a request.

It can challenge suspicious traffic.

For example:

```text
Suspicious request
       |
       v
     CAPTCHA
       |
   +---+---+
   |       |
Pass      Fail
 |         |
 v         v
Allow     Block
```

This is useful when completely blocking traffic could accidentally block legitimate users.

---

# 43. Threat Intelligence + WAF

Modern WAF solutions can incorporate threat intelligence.

For example:

```text
Threat Intelligence
        |
        v
Known malicious IPs
Known botnets
Suspicious sources
Known attack indicators
        |
        v
       WAF
```

The WAF can then use this information when deciding whether traffic should be allowed or blocked.

---

# 44. Complete SOC Detection Picture

The biggest lesson from this room is that a SOC should not depend on only one source of telemetry.

Think about the same attack from multiple perspectives.

```text
                    ATTACKER
                       |
              +--------+--------+
              |                 |
          Web Requests       Network Traffic
              |                 |
              v                 v
         Access Logs        Packet Capture
              |                 |
              +--------+--------+
                       |
                       v
                     SIEM
                       |
                       v
                 SOC Analyst
                       |
              +--------+--------+
              |                 |
          Investigation       Response
```

---

# 45. Client-Side vs Server-Side

| Feature                    | Client-Side                | Server-Side                    |
| -------------------------- | -------------------------- | ------------------------------ |
| Main target                | Browser/user               | Web server/application         |
| Example                    | XSS                        | SQL Injection                  |
| Other examples             | CSRF, Clickjacking         | Brute force, Command Injection |
| SOC visibility             | Often limited              | Usually better                 |
| Server logs                | May not show full activity | Often useful                   |
| Network evidence           | Sometimes limited          | Often useful                   |
| Endpoint/browser telemetry | Very useful                | Also useful                    |
| WAF visibility             | Depends on attack          | Often useful                   |

---

# 46. How a SOC Analyst Should Investigate a Web Attack

When a web attack alert appears, do not immediately focus on one log entry.

Build a timeline.

### Step 1 — Identify the source

Look at:

```text
Source IP
User-Agent
Timestamp
```

---

### Step 2 — Identify the target

Determine:

```text
Destination IP
Hostname
URL
Endpoint
Application
```

---

### Step 3 — Identify the request pattern

Look for:

```text
Repeated requests
Unusual methods
Rapid requests
Suspicious parameters
Unexpected endpoints
```

---

### Step 4 — Look for scanning

Determine whether the attacker was discovering:

```text
Directories
Files
Login pages
Administrative endpoints
Other application functionality
```

---

### Step 5 — Check authentication activity

Look for:

```text
Multiple failures
Multiple usernames
Multiple passwords
Successful login after failures
Unusual account activity
```

---

### Step 6 — Check for exploitation

Look for indicators associated with:

```text
SQL Injection
Command Injection
XSS
Other application attacks
```

---

### Step 7 — Determine what happened after exploitation

This is extremely important.

Ask:

> Did the attacker actually gain access?

Then:

> What did they do after gaining access?

For example:

```text
Scanning
   ↓
Brute force
   ↓
Successful login
   ↓
SQL injection
   ↓
Data access
```

---

### Step 8 — Determine potential impact

Investigate whether:

* Accounts were compromised
* Sensitive information was accessed
* Data was modified
* Data was downloaded
* Additional systems were accessed

---

# 47. Key Indicators to Remember

### Directory fuzzing

Look for:

```text
Large numbers of GET requests
Many different paths
High number of 404 responses
Automated User-Agent
Rapid request rate
```

---

### Brute force

Look for:

```text
Repeated POST /login
Many failed attempts
Short time intervals
Multiple usernames/passwords
Successful login after failures
```

---

### SQL Injection

Look for:

```text
SQL syntax in parameters
Unexpected quotes
Boolean SQL expressions
Database-related keywords
Repeated unusual requests
```

The exact payload is not as important as recognizing the pattern of SQL manipulation.

---

### Command Injection

Look for:

```text
Unexpected OS command syntax
Suspicious parameters
Application errors
Unexpected process creation
Web server spawning unusual processes
```

---

### Suspicious automation

Look for User-Agents such as:

```text
sqlmap
wpscan
ffuf
```

But remember:

> User-Agent values can be spoofed.

---

# 48. Important Investigation Principle

Never conclude that something is malicious based on **one indicator alone**.

For example:

```text
User-Agent = sqlmap
```

is suspicious.

But a stronger investigation would correlate:

```text
sqlmap User-Agent
       +
SQL injection-like request
       +
Repeated requests
       +
Unusual endpoint
       +
Database-related response
```

The more independent evidence you have, the stronger your conclusion becomes.

---
