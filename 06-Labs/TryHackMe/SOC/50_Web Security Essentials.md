# Web Security Essentials

> **Goal:** Understand how modern web applications work, why they are attractive targets for attackers, what components make up a web service, and how defenders protect those components.

---

# 1. Why Web?

## 1.1 Evolution of Applications

The way we use software has changed significantly over the years.

### 1990s — Desktop Applications

During the 1990s, applications were mainly installed and executed directly on a user's computer.

For example:

* Microsoft Office
* Desktop games
* Locally installed business applications
* Local database applications

Internet connectivity was slower and less widely available, so applications did not depend heavily on web technologies.

### 2000s — Dynamic Web Applications

As Internet connectivity improved, web applications became much more common.

Instead of installing software locally, users could interact with applications through a browser.

Examples included:

* Email services
* Social networks
* Online banking
* Online shopping

This introduced a major change:

> The application was no longer necessarily running entirely on the user's computer. Much of the functionality was running on remote servers.

### 2010s — Cloud and SaaS

Cloud computing and Software as a Service (SaaS) became increasingly important.

Users could access powerful applications without installing everything locally.

Examples include:

* Cloud storage
* Online document editors
* Web-based development environments
* Streaming services
* Cloud-hosted business applications

Today, many activities that traditionally required installed software can be performed directly through a browser.

---

# 2. Why Are Web Applications Important From a Security Perspective?

Web applications provide several major advantages:

* Easy accessibility
* Fast updates
* Compatibility across different devices
* Reduced resource requirements on the user's machine

However, these advantages also create security risks.

A web application is often:

> **Publicly accessible, continuously available, and connected to valuable backend systems.**

This makes it an attractive target for attackers.

The source notes that web applications are among the common entry points for attackers because they are exposed to the Internet and may connect to databases and other infrastructure.

---

# 3. Web Application Owner vs Web Application User

Security affects both sides.

## 3.1 Risks for a Web Application Owner

A web application owner has to consider:

### Always-online exposure

A web application may need to be available 24/7.

Therefore, security cannot simply be enabled during business hours.

Attackers can attempt attacks at any time.

### Global accessibility

A public web application can potentially be accessed by users around the world.

This means the application is exposed to a much larger pool of potential attackers.

### User data protection

Applications may store sensitive information such as:

* Names
* Email addresses
* Passwords
* Financial information
* Personal information

The application owner has a responsibility to protect this data.

### Constantly changing threats

New vulnerabilities and attack techniques appear regularly.

Therefore, security is not a one-time task.

It is an ongoing process involving:

* Patching
* Monitoring
* Logging
* Detection
* Secure development
* Incident response

---

# 4. Risks for Web Application Users

Users also face security consequences.

If an application is compromised, user information may be exposed.

Possible consequences include:

* Identity theft
* Financial loss
* Account compromise
* Privacy violations
* Exposure of personal information

A compromised browser or web session can also put multiple accounts at risk, especially when users have several accounts accessible through the same browser.

The source specifically highlights the possibility of identity theft, financial loss, and permanent privacy compromise.

---

# 5. Real-World Examples

## 5.1 Equifax — 2017

In 2017, Equifax experienced a major data breach.

According to the provided material, sensitive customer information of nearly 150 million Americans was compromised through exploitation of an Apache vulnerability, CVE-2017-5638.

The attackers were able to access internal databases containing valuable customer information.

### Security lesson

A vulnerability in an Internet-facing application or service can eventually provide attackers with access to valuable backend data.

This demonstrates why:

> **Web application security is not only about protecting the webpage itself.**

It is also about protecting the systems and data behind it.

---

# 6. Capital One — 2019

Capital One experienced a major breach in 2019.

The provided material describes a misconfigured Web Application Firewall (WAF) that exposed sensitive personal and financial information belonging to more than 100 million customers.

The misconfiguration allowed access into cloud infrastructure and databases.

### Security lesson

Security controls themselves must also be configured correctly.

Simply having a:

* Firewall
* WAF
* Cloud environment
* Security product

does not automatically make an environment secure.

Incorrect configuration can introduce serious weaknesses.

---

# 7. Web Infrastructure

## 7.1 The Request-Response Model

One of the most important concepts in web security is understanding how a web request works.

When I visit a website:

```text
My Browser
    |
    | HTTP/HTTPS Request
    v
Web Server
    |
    | Process Request
    v
Application
    |
    | Generate Response
    v
Web Server
    |
    | HTTP/HTTPS Response
    v
My Browser
```

For example, when I visit:

```text
https://example.com/login
```

my browser sends a request to the server.

The server processes the request and returns a response.

The response could contain:

* HTML
* CSS
* JavaScript
* Images
* JSON
* Account information
* Search results

The request-response cycle is the foundation of web communication.

---

# 8. Why Attackers Care About the Request-Response Cycle

Attackers can attempt to manipulate this communication.

For example, they might try to:

* Send extremely large numbers of requests
* Bypass access controls
* Submit malicious input
* Exploit application vulnerabilities
* Trick the server into executing unintended commands

Therefore, understanding normal HTTP communication is extremely important for a SOC analyst.

If I understand what normal traffic looks like, suspicious traffic becomes easier to recognize.

---

# 9. Three Main Components of a Web Service

The source identifies three important components:

1. Application
2. Web Server
3. Host Machine

Let's understand each one.

---

# 10. Application

The application contains the actual functionality of the website.

It can include:

* Application code
* HTML
* CSS
* JavaScript
* Images
* Icons
* Backend logic

For example, a banking application might contain functionality for:

```text
Login
    ↓
Authentication
    ↓
Account Dashboard
    ↓
Balance
    ↓
Transactions
    ↓
Money Transfer
```

If the application contains a vulnerability, an attacker may abuse the application's functionality.

Examples include:

* Injection vulnerabilities
* Broken access control
* Authentication weaknesses
* Insecure input handling

---

# 11. Web Server

The web server receives HTTP requests and returns responses.

Common web servers mentioned in the source include:

### Apache

Apache is widely used for hosting websites and applications.

It is particularly common with websites such as WordPress installations.

### Nginx

Nginx is commonly used for high-performance web applications.

It can also act as:

* Web server
* Reverse proxy
* Load balancer

### Microsoft IIS

Internet Information Services (IIS) is Microsoft's web server.

It is commonly encountered in Microsoft/Windows enterprise environments.

---

# 12. Host Machine

The host machine is the underlying operating system that runs the web server and application.

It could be:

```text
Linux
```

or:

```text
Windows
```

For example:

```text
Host Machine
      |
      +-- Operating System
      |
      +-- Web Server
      |
      +-- Web Application
```

If the host machine itself is compromised, an attacker may potentially gain control over the web server and application.

---

# 13. Protecting the Web

Security controls can be applied to all three components:

```text
Application
     |
     v
Web Server
     |
     v
Host Machine
```

The source separates protection into these three areas.

---

# 14. Protecting the Application

## 14.1 Secure Coding

Developers should avoid insecure programming practices.

Secure coding includes:

* Avoiding insecure functions
* Handling errors properly
* Protecting sensitive information
* Designing authentication securely
* Handling user input safely

A secure application should not expose unnecessary internal information.

---

# 15. Input Validation and Sanitization

Applications frequently receive input from users.

For example:

```text
Username
Password
Search Query
File Upload
Comment
URL Parameter
```

This input should not automatically be trusted.

The application should validate and sanitize it.

Why?

Because attackers may attempt to submit malicious input.

For example:

```text
Normal input:
hello

Potentially malicious input:
<script>...</script>
```

or SQL-related input.

Input validation and sanitization are therefore important defenses against injection-style attacks.

The source specifically identifies them as protections against injection attacks.

---

# 16. Access Control

Access control determines:

> **Who is allowed to do what?**

For example:

```text
Normal User
    |
    +-- View own profile
    +-- Edit own information

Administrator
    |
    +-- Manage users
    +-- View administrative data
    +-- Change system settings
```

A normal user should not automatically have administrator privileges.

Poor access control can allow attackers to access functionality or information they should not have access to.

---

# 17. Protecting the Web Server

## 17.1 Logging

Web servers can record requests.

These logs provide visibility into activity occurring against the server.

They can contain information such as:

* Client IP
* Timestamp
* Requested resource
* HTTP method
* Response status
* User-Agent

These logs are extremely useful during security investigations.

---

# 18. Web Application Firewall — WAF

A WAF is a security control designed specifically to inspect web traffic.

It examines HTTP requests and can:

* Allow legitimate traffic
* Detect suspicious traffic
* Block malicious requests
* Log suspicious activity

A simple way to remember it:

> **WAF = Security filter for web application traffic.**

The source compares a WAF to a bouncer checking people before they enter a club.

---

# 19. Content Delivery Network — CDN

A CDN distributes cached content through servers located closer to users.

Instead of every user communicating directly with one central origin server:

```text
                 Origin Server
                      |
        +-------------+-------------+
        |             |             |
     Edge Server   Edge Server   Edge Server
        |             |             |
      Users         Users         Users
```

This can improve:

* Performance
* Availability
* Scalability

But CDNs can also provide security benefits.

---

# 20. Protecting the Host Machine

## 20.1 Least Privilege

Services should run with only the permissions they require.

For example, if a web application only needs to read certain files, it should not run with unrestricted administrator privileges.

This follows the principle:

> **Give a process only the permissions it actually needs.**

If the application is compromised, least privilege can limit the damage.

---

# 21. System Hardening

System hardening means reducing unnecessary attack surface.

Examples include:

* Disable unnecessary services
* Close unused ports
* Remove unnecessary software
* Apply security updates
* Restrict unnecessary access

The goal is simple:

> **Reduce the number of things an attacker can attack.**

---

# 22. Antivirus

Antivirus software provides endpoint-level protection.

It can help detect and block known malicious:

* Files
* Programs
* Malware
* Post-exploitation tools

The source emphasizes that antivirus is only one layer of security and should be used as part of a broader defense-in-depth strategy.

---

# 23. Security Measures That Apply Everywhere

## 23.1 Strong Authentication

Sensitive resources should not be accessible to unauthorized users.

Examples:

* Admin panels
* Source code
* Server management interfaces
* Host machines

Strong authentication helps prevent unauthorized access.

---

# 24. Patch Management

Software regularly receives security updates.

This includes:

```text
Web Application
       +
Dependencies
       +
Web Server
       +
Operating System
```

All of these need to remain updated.

A vulnerability in an old dependency can potentially expose the entire application.

Therefore:

> **Patch management is an ongoing security responsibility.**

---

# 25. Logging

Logging is particularly important for a SOC analyst.

A web server can record every request it receives.

These are commonly called:

> **Access Logs**

They can contain:

| Field              | Meaning                                  |
| ------------------ | ---------------------------------------- |
| Client IP          | Address of the system making the request |
| Timestamp          | When the request occurred                |
| Requested resource | What the client requested                |
| HTTP method        | What operation was requested             |
| Status code        | Result of the request                    |
| User-Agent         | Information about the client/browser     |

---

# 26. GET vs POST

Two HTTP methods mentioned in the material are:

## GET

GET is commonly used to retrieve a resource.

Example:

```http
GET /index.html
```

This could mean:

> "Give me the index page."

## POST

POST is commonly used to submit data to the server.

For example:

```http
POST /login
```

could contain login information.

The source specifically uses GET for retrieving resources and POST for submitting credentials.

---

# 27. Example Web Request Sequence

Imagine a user accessing a website.

### Step 1 — Homepage

```text
10.10.10.100
      |
      +-- GET /index.html
```

The user requests the homepage.

### Step 2 — Login Page

```text
10.10.10.100
      |
      +-- GET /login.html
```

### Step 3 — Login

```text
10.10.10.100
      |
      +-- POST /login.html
```

The user submits credentials.

### Step 4 — Account

```text
10.10.10.100
      |
      +-- GET /myaccount.html
```

The user accesses their account.

The provided material uses this sequence to demonstrate how logs can reconstruct a user's activity.

---

# 28. Why Logs Matter to a SOC Analyst

Imagine that instead of normal activity, the logs showed:

```text
GET /login
POST /login
POST /login
POST /login
POST /login
POST /login
```

within a very short period.

That could be worth investigating.

Another example:

```text
GET /admin
GET /admin
GET /admin/config
GET /backup.zip
GET /database.sql
```

This could provide useful context during an investigation.

The important lesson is:

> **Individual log entries may look harmless, but the sequence of events can reveal attacker behavior.**

---

# 29. Content Delivery Network — CDN

A CDN stores and serves cached content from servers closer to users.

Instead of every user having to communicate directly with the origin server, a nearby edge server can provide cached content.

This improves performance and can add a security layer.

---

# 30. CDN Security Benefits

## 30.1 IP Masking

A CDN can hide the origin server's IP address.

This makes it harder for attackers to directly target the origin server.

---

## 30.2 DDoS Protection

A CDN can absorb large amounts of traffic.

This can reduce the impact of certain denial-of-service attacks.

---

## 30.3 HTTPS

Many CDNs support or enforce HTTPS/TLS.

This protects communication between users and the service by encrypting traffic.

---

## 30.4 Integrated WAF

Many CDN providers can integrate WAF functionality.

The source gives examples including:

* Cloudflare
* Amazon CloudFront
* Azure Front Door

---

# 31. Web Application Firewall — WAF

A WAF sits between users and the web application and examines HTTP traffic.

A simplified architecture looks like:

```text
User
 |
 v
Internet
 |
 v
WAF
 |
 |---- Block malicious request
 |
 |---- Allow legitimate request
 v
Web Server
 |
 v
Web Application
```

The WAF therefore acts as an additional security layer.

---

# 32. Types of WAF

The source describes three types.

## 32.1 Cloud-Based WAF / Reverse Proxy

This sits in front of the web server.

```text
User
 |
 v
Cloud WAF
 |
 v
Web Server
```

Advantages include:

* Easy deployment
* Scalability
* Ability to handle large amounts of traffic

---

## 32.2 Host-Based WAF

A host-based WAF runs directly on the web server.

This can provide application-specific control.

Architecture:

```text
Host Machine
 |
 +-- WAF
 |
 +-- Web Server
 |
 +-- Application
```

---

## 32.3 Network-Based WAF

A network-based WAF can be deployed as a physical or virtual appliance near the network perimeter.

This approach is commonly associated with larger enterprise environments.

---

# 33. How Does a WAF Detect Attacks?

A WAF can use several detection approaches.

---

## 33.1 Signature-Based Detection

The WAF looks for known patterns associated with attacks.

For example, a request containing a known suspicious User-Agent:

```text
sqlmap/1.8.1
```

could be flagged.

Important point:

> Signature-based detection works particularly well when the attack pattern is already known.

---

# 34. Heuristic-Based Detection

Heuristic detection examines characteristics of a request rather than simply matching one known signature.

For example:

```text
/search?q=%3Cscript%20(1)
```

A suspiciously long query containing unusual characters could be flagged.

This approach attempts to recognize suspicious characteristics.

---

# 35. Anomaly and Behavioral Analysis

Instead of looking only at the content of one request, the WAF can examine behavior.

For example:

```text
IP: 10.10.10.50

10:00:01  Login attempt
10:00:02  Login attempt
10:00:03  Login attempt
10:00:04  Login attempt
10:00:05  Login attempt
...
```

A large number of login attempts within a short period may be suspicious.

The important idea is:

> **Normal behavior creates a baseline. Significant deviations from that baseline can be investigated.**

---

# 36. Location and IP Reputation Filtering

A WAF can also use:

* IP reputation
* Threat intelligence
* Geographic information

For example, an organization might identify traffic from an IP address associated with malicious activity.

The WAF could use that information when deciding whether to allow or block traffic.

The source notes that detection methods are not limited to these examples and that custom rules can also be created.

---

# 37. Antivirus

Antivirus is primarily designed to protect endpoints.

Examples of endpoints include:

* Desktops
* Laptops
* Servers

Traditional antivirus commonly uses signatures to compare files against known malware patterns.

For example:

```text
File
 |
 v
Antivirus
 |
 +---- Known malicious pattern? ---- YES ---> Block/Alert
 |
 +---- NO -------------------------------> Continue
```

---

# 38. Why Antivirus Still Matters for Web Security

A web attack may eventually reach the host machine.

For example:

```text
Attacker
   |
   v
Web Application
   |
   v
Web Server
   |
   v
Malicious File
   |
   v
Host Machine
```

An attacker may attempt to place malicious files such as:

* Web shells
* Malware
* Post-exploitation tools

on the server.

Endpoint protection can therefore provide another layer of defense.

However:

> **Antivirus should not be considered the only security control.**

The source explicitly describes it as one part of a broader defense-in-depth strategy.

---

# 39. Defense in Depth

One of the biggest concepts to remember from this room is:

> **Do not depend on a single security control.**

A stronger architecture uses multiple layers.

For example:

```text
                 ATTACKER
                    |
                    v
                 Internet
                    |
                    v
                  CDN
                    |
                    v
                  WAF
                    |
                    v
              Web Server
                    |
                    v
             Web Application
                    |
                    v
              Host Machine
                    |
                    v
                   AV
                    |
                    v
                  Logs
                    |
                    v
                   SIEM
                    |
                    v
              SOC Analyst
```

Each layer has a different purpose.

---

# 40. How This Connects to SOC Work

For a SOC analyst, this room is important because web applications generate a large amount of security telemetry.

A SOC analyst may investigate:

### Web server logs

Questions:

* Which IP made the request?
* What endpoint was requested?
* When did it happen?
* What HTTP method was used?
* What status code was returned?
* What User-Agent was used?

### WAF alerts

Questions:

* Why did the WAF block the request?
* Was it an injection attempt?
* Was the source IP malicious?
* Was this a false positive?
* Were multiple requests involved?

### Endpoint/AV alerts

Questions:

* Was a suspicious file created?
* Was malware detected?
* Which process created it?
* Which user account was involved?

---

# 41. Putting Everything Together

A realistic simplified attack might look like:

```text
1. Attacker discovers web application
              |
              v
2. Sends malicious HTTP request
              |
              v
3. WAF examines request
              |
        +-----+-----+
        |           |
     Block        Allow
        |           |
        v           v
      Alert     Web Server
                    |
                    v
              Web Application
                    |
                    v
              Host Machine
                    |
                    v
             Possible Malware
                    |
                    v
                  AV
                    |
                    v
                 Logs
                    |
                    v
                  SIEM
                    |
                    v
              SOC Analyst
```

This demonstrates how multiple defensive technologies can work together.

---

# 42. Key Concepts I Need to Remember

| Concept          | Simple Meaning                                       |
| ---------------- | ---------------------------------------------------- |
| Web Application  | Software accessed through a browser                  |
| Web Server       | Receives web requests and sends responses            |
| Host Machine     | Operating system running the web server/application  |
| HTTP             | Protocol used for web communication                  |
| GET              | Usually retrieves a resource                         |
| POST             | Usually submits data                                 |
| Access Log       | Record of web requests                               |
| WAF              | Filters web application traffic                      |
| CDN              | Distributes content through edge servers             |
| Antivirus        | Endpoint protection against malicious files/programs |
| Least Privilege  | Give only necessary permissions                      |
| Hardening        | Reduce unnecessary attack surface                    |
| Patch Management | Keep software and dependencies updated               |
| Input Validation | Check whether submitted data is acceptable           |
| Access Control   | Decide who can access what                           |
| Defense in Depth | Use multiple security layers                         |

---

# 43. SOC Analyst Perspective

The most important thing I take from this room is that web security is not only about attacking or protecting a website.

As a SOC analyst, I need to understand the complete path:

```text
User
 ↓
Internet
 ↓
CDN
 ↓
WAF
 ↓
Web Server
 ↓
Application
 ↓
Host Machine
 ↓
Database / Backend
```

Each layer can produce different security events.

If something suspicious happens, I need to use those events to reconstruct what happened.

For example:

```text
WAF Alert
   ↓
Web Server Access Log
   ↓
Application Log
   ↓
Host/Endpoint Alert
   ↓
Timeline
   ↓
Investigation
```

This is why understanding normal web traffic is so important for SOC work.

---

# 44. Final Understanding

The main lesson from **Web Security Essentials** is that modern web applications are powerful but highly exposed systems.

A web application is not just a webpage.

It is an ecosystem involving:

```text
Application
     +
Web Server
     +
Operating System
     +
Network
     +
Users
     +
Backend Systems
```

An attacker may target any weak point in this ecosystem.

Therefore, defenders use multiple controls:

```text
Secure Coding
      +
Input Validation
      +
Access Control
      +
Logging
      +
WAF
      +
CDN
      +
Least Privilege
      +
System Hardening
      +
Antivirus
      +
Patch Management
```

No single control is enough.

The goal is to create multiple layers so that if one control fails, another control can detect, limit, or stop the attack.

For a SOC analyst, the most valuable takeaway is the ability to connect **web traffic → logs → security controls → alerts → investigation**.
