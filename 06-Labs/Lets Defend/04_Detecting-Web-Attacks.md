# Detecting Web Attacks – SOC Analyst Study Notes

**Platform:** LetsDefend  
**Course area:** SOC Fundamentals / Detecting Web Attacks  
**Study date:** 13 November 2026  
**Focus:** Understanding HTTP, OWASP risks, attack behaviour, log analysis, and SOC detection

---

## 1. Why Detecting Web Attacks Is Important

We use web applications every day. Examples include music and video platforms, online shopping, banking portals, social networks, healthcare portals, and internal company applications.

Organisations also depend on web applications to store and process important information. A web application may connect to databases, authentication systems, payment services, file storage, and internal business systems. This makes it an attractive target.

A web application is not just a website that displays pages. It is a system that receives user input, processes requests, accesses data, performs actions, and returns responses. Every place where data enters the application or where the application communicates with another system can become an attack surface if it is not designed and secured correctly.

### Why attackers target web applications

Attackers may target web applications because they can:

- Access sensitive customer or business information.
- Steal credentials or session information.
- Perform actions as another user.
- Modify or delete stored information.
- Execute commands on the server if a serious vulnerability exists.
- Use a compromised web server as a starting point for further attacks.
- Disrupt services and affect business operations.

### Why this matters to a SOC analyst

A SOC analyst may receive evidence of a web attack from several sources:

- Web server access logs.
- Web application logs.
- Web Application Firewall (WAF) alerts.
- Intrusion Prevention System (IPS) alerts.
- SIEM correlation rules.
- Reverse proxy or CDN logs.
- Network security monitoring.
- Endpoint telemetry from the web server.

The analyst's job is not simply to search for a suspicious word. The analyst must understand what the request was trying to do, whether the application behaved unexpectedly, whether the request reached the application, and whether there is evidence of impact.

### Prevention and detection are different

Security controls work at different points:

- **Secure development** reduces the chance that vulnerabilities are introduced.
- **WAF** inspects web traffic and can block or alert on requests that match configured rules.
- **IPS** can detect and prevent certain malicious network activity.
- **SIEM** collects and correlates logs and alerts from multiple systems.
- **EDR** can help investigate the web server if suspicious processes or files appear.

A WAF or SIEM alert is not automatically proof that an attack succeeded. It is a signal that must be investigated.

> **Main idea:** Web attack detection is important because a single vulnerable web application can expose data, users, servers, and other parts of an organisation's environment.

---

## 2. OWASP and the OWASP Top 10

The **Open Worldwide Application Security Project (OWASP)** is a non-profit foundation that provides resources, guidance, and projects intended to improve software and application security.

OWASP is useful for developers, penetration testers, security engineers, and SOC analysts because it explains common web application security weaknesses and how they can be prevented.

### OWASP Top 10 – 2021

The course material refers to the 2021 edition. Its categories are:

1. **Broken Access Control** – users can access data or perform actions beyond their authorised permissions.
2. **Cryptographic Failures** – sensitive information is not properly protected, often because of weak or missing encryption.
3. **Injection** – untrusted input is interpreted as part of a command or query, such as SQL or operating-system commands.
4. **Insecure Design** – security weaknesses exist in the application's design or business logic.
5. **Security Misconfiguration** – systems or applications have unsafe settings, unnecessary features, exposed files, or insecure defaults.
6. **Vulnerable and Outdated Components** – the application uses components with known vulnerabilities or unsupported versions.
7. **Identification and Authentication Failures** – weaknesses allow attackers to impersonate users or compromise authentication.
8. **Software and Data Integrity Failures** – the application does not adequately verify the integrity of software, updates, or critical data.
9. **Security Logging and Monitoring Failures** – important activity is not properly recorded, monitored, or investigated.
10. **Server-Side Request Forgery (SSRF)** – an attacker can cause a server to make requests to unintended destinations.

The OWASP Top 10 is an awareness document, not a complete list of every possible web vulnerability. It helps us understand major risk areas, but a SOC analyst must still investigate the actual behaviour seen in logs.

Reference: [OWASP](https://owasp.org/)

---

## 3. How Web Applications Communicate: HTTP

Before detecting abnormal web traffic, I need to understand how normal web communication works.

A web browser and a web server communicate using **HTTP (Hypertext Transfer Protocol)**. HTTP defines how a client requests resources and how a server responds.

Examples of resources include:

- HTML pages.
- Images.
- Videos.
- JavaScript and CSS files.
- JSON data returned by an API.
- Documents and downloadable files.

### 3.1 HTTP and the OSI model

HTTP is an application-layer protocol, commonly associated with Layer 7 of the OSI model.

For a typical web connection, several layers work together:

- **Application layer:** HTTP defines the web request and response.
- **Transport layer:** TCP commonly carries HTTP/1.1 and HTTP/2 traffic. HTTP/3 uses QUIC over UDP.
- **Network layer:** IP carries packets between networks.
- **Link layer:** Ethernet or Wi-Fi carries frames across the local network.

When HTTPS is used, TLS protects HTTP communication while it travels between the client and server. HTTPS is HTTP carried over a protected connection; it does not automatically mean the website or its content is trustworthy.

### 3.2 Client and server

The basic communication process is:

1. The client, usually a browser or application, requests a resource.
2. The request travels through the network to the web server.
3. The server receives and interprets the request.
4. The application may check authentication and authorisation.
5. The application may read from or write to a database, call another service, or process submitted data.
6. The server creates an HTTP response.
7. The client receives the response and displays or processes the result.

This is the normal request-response cycle. Attackers abuse the same process by sending requests containing unexpected input or by manipulating values that the application trusts.

### 3.3 Why HTTP knowledge helps a SOC analyst

If I see a suspicious request in an access log, I should be able to identify:

- Which resource was requested.
- Which HTTP method was used.
- Which parameters were supplied.
- Which headers were included.
- Whether a request body may contain additional input.
- What response status the server returned.
- Whether the same client sent other related requests.

Without understanding the structure of HTTP, it is difficult to recognise where an attack payload has been placed.

---

## 4. Understanding an HTTP Request

An HTTP request is a message sent by a client to a server. It usually contains a **request line**, **headers**, a blank line separating the headers from the body, and sometimes a **request body**.

### 4.1 Request line

The request line contains:

- The HTTP method.
- The requested path or resource.
- The HTTP version.

For example, a browser may request the root path `/` using the GET method.

The path `/` commonly represents the site's main page, although the exact meaning depends on the application and server configuration.

### 4.2 Common HTTP methods

| Method | General purpose | Security investigation context |
|---|---|---|
| GET | Retrieve a resource | Often used to request pages, search results, or API data |
| POST | Submit data for processing | Common in login forms, uploads, and form submissions |
| PUT | Create or replace a resource | Unexpected use may deserve investigation |
| PATCH | Partially update a resource | Can be relevant when investigating unauthorised changes |
| DELETE | Delete a resource | May be suspicious if the user is not expected to delete data |
| HEAD | Request response headers without the usual response body | Can be used for legitimate checks or reconnaissance |
| OPTIONS | Ask which methods or communication options are supported | May appear during application discovery or cross-origin checks |

A method is not malicious by itself. Its meaning depends on the application, endpoint, user, and expected behaviour.

### 4.3 Request headers

Headers provide additional information about the request.

| Header | Meaning | SOC relevance |
|---|---|---|
| Host | Identifies the hostname the client wants to reach | Useful when several websites share an IP address |
| Cookie | Sends stored browser data, often including a session identifier | Session-related data must be protected |
| User-Agent | Describes the client software, often including browser and operating-system details | Can reveal scripts, scanners, libraries, or unusual clients |
| Accept | Describes the response content types the client can process | Helps explain the expected response format |
| Accept-Encoding | Lists supported compression formats | Usually normal browser metadata |
| Accept-Language | Indicates preferred languages | May help identify client preferences |
| Connection | Provides connection-management information in HTTP/1.1 | Values such as `close` or `keep-alive` may appear |
| Upgrade-Insecure-Requests | Indicates that the client prefers secure navigation where supported | Common in browser requests |

A User-Agent value can be changed or forged. A browser-like User-Agent does not prove that the request came from a real browser, and a tool name in the User-Agent is a clue rather than definitive attribution.

### 4.4 Cookies and sessions

A cookie is a small piece of data stored by the browser and sent back to a website on later requests when the cookie's scope matches.

Web applications commonly use cookies to maintain a session after login. Instead of sending the username and password with every request, the browser sends a session identifier. The server uses that identifier to recognise the authenticated session.

This is why session cookies are sensitive. If an attacker steals a valid session token, they may be able to act as the user until the session expires or is invalidated.

Secure cookie settings can reduce risk:

- `Secure` limits cookie transmission to secure connections.
- `HttpOnly` prevents ordinary client-side JavaScript from reading the cookie.
- `SameSite` controls when cookies are sent with cross-site requests.

These controls help, but they do not replace secure application design or protection against XSS and session compromise.

### 4.5 Request body

The request body contains data sent to the application. It is common with POST, PUT, and PATCH requests, although exact behaviour depends on the method and application.

A body may contain:

- Login form fields.
- Search or profile data.
- JSON API content.
- Uploaded file data.
- Other application parameters.

An important SOC lesson is that malicious input can appear in more than the URL. It may be in a query parameter, a form field, a JSON body, a cookie, or a header such as User-Agent.

---

## 5. Understanding an HTTP Response

An HTTP response is the message sent by the server after it processes a request. It usually contains a **status line**, **response headers**, a blank line, and sometimes a **response body**.

### 5.1 Status line and status-code groups

The status line contains the HTTP version and a status code describing the result of the request.

| Status-code range | Meaning | Examples |
|---|---|---|
| 100–199 | Informational | The request process is continuing |
| 200–299 | Successful | `200 OK`, `201 Created`, `204 No Content` |
| 300–399 | Redirection | `301 Moved Permanently`, `302 Found`, `304 Not Modified` |
| 400–499 | Client error | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| 500–599 | Server error | `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable` |

A status code must be interpreted in context.

For example:

- A `200` response means the server successfully returned a response. It does not prove that the request was harmless.
- A `403` may indicate that access was denied, but the request may still represent an attack attempt.
- A `404` may be a normal missing page or part of reconnaissance.
- A `302` redirect does not automatically mean an attack failed. Applications legitimately redirect users after login, and attackers can also abuse redirects.

### 5.2 Response headers

| Header | Meaning |
|---|---|
| Date | Time the server generated the response |
| Connection | Connection-management information |
| Server | May identify server software, though it can be hidden or modified |
| Last-Modified | Time the resource was last modified, often used with caching |
| Content-Type | Type of content returned, such as HTML or JSON |
| Content-Length | Size of the response body in bytes, when provided |

The `Server` header may reveal software information, but it can be inaccurate, deliberately hidden, or changed by a proxy.

### 5.3 Response body

The response body contains the resource or data returned by the server. It may contain HTML, JSON, an image, a file, or another type of content.

For a SOC analyst, the response body can sometimes help determine whether an attack succeeded. However, security teams do not always retain response bodies because they can contain sensitive information, require substantial storage, or create privacy concerns.

When response bodies are unavailable, analysts may use status codes, response sizes, application logs, database audit logs, and endpoint evidence. These are clues, not perfect substitutes.

---

## 6. Web Server Access Logs and Investigation

An access log records requests handled by a web server or web infrastructure component. The exact fields depend on the logging configuration.

Common fields include:

- Source IP address.
- Timestamp.
- HTTP method.
- Requested path and query string.
- HTTP status code.
- Response size.
- User-Agent.
- Referrer.
- Virtual host or hostname.

### 6.1 A practical way to read access logs

When I receive web access logs, I should work through them systematically:

1. **Establish the time window.** Identify when the suspicious activity began and ended. Confirm the timezone.
2. **Identify the target.** Determine the hostname, page, API endpoint, or parameter being requested.
3. **Group related requests.** Compare source IPs, session identifiers where safely available, User-Agent values, paths, and timestamps.
4. **Decode carefully.** URL-encoded characters may hide the actual input.
5. **Look for patterns.** Repeated parameters, payload variations, sequential object identifiers, and unusual request rates may indicate scanning or exploitation attempts.
6. **Check the response.** Review status codes and response sizes, but do not treat them as conclusive proof.
7. **Correlate other logs.** Check WAF, proxy, application, database, authentication, DNS, and endpoint records.
8. **Determine impact.** Establish whether data was accessed, changed, deleted, or whether code ran on the server.
9. **Document confidence and uncertainty.** Separate what the logs prove from what is only suspected.

### 6.2 URL encoding and decoding

URLs cannot always contain every character in its raw form. Special characters are often represented using percent encoding.

For example, a space may appear as `%20`. Other characters, including quotation marks and angle brackets, may also be encoded.

This matters because an attack payload may not be immediately readable in an access log. A SOC analyst may need to decode the URL to understand the actual input.

**Safety and privacy:** Avoid uploading real company logs to public online URL decoders. Logs can contain internal IP addresses, usernames, session identifiers, personal data, and sensitive URL parameters. Use approved local tools or organisation-approved analysis platforms.

### 6.3 Important limitations of access logs

Access logs usually show that a request reached a particular logging point. They may not show everything that happened inside the application.

For example:

- A reverse proxy may record the client-facing request, while the application server records a different internal request.
- A WAF may block a request before it reaches the application.
- A CDN may cause the logged source IP to belong to the CDN rather than the original client.
- A request may return an error while still triggering some application-side activity.
- A successful HTTP response does not necessarily mean the attacker's objective was achieved.

Always understand which device generated the log and what stage of the request path it represents.

---

## 7. Cross-Site Scripting (XSS)

### 7.1 What is XSS?

**Cross-Site Scripting (XSS)** is a web vulnerability in which an application allows attacker-controlled content to be interpreted as executable script in another user's browser.

The important point is that XSS generally affects the browser of a person who views the vulnerable page. The attacker causes the trusted website to deliver content that the browser interprets as script.

This is different from command injection, where the goal is to make the server's operating system execute commands.

### 7.2 Understand the browser's role

A browser receives HTML and builds a Document Object Model (DOM), which represents the page. The browser also processes scripts that the page is allowed to run.

If an application takes untrusted input and inserts it into a page in an unsafe way, the browser may interpret that input as HTML or JavaScript rather than ordinary text.

For example, imagine a greeting page that displays the value supplied in a `user` parameter.

- If the value is `Abhinav`, the page displays a normal greeting.
- If the application inserts untrusted input into the page as executable markup, an attacker may supply script content.
- The victim's browser may then execute that content in the context of the vulnerable website.

The root problem is not simply that the user entered unusual characters. The root problem is that the application placed untrusted data into an unsafe browser context without the correct output encoding or sanitisation.

### 7.3 The three main types of XSS

#### Reflected XSS (Non-Persistent)

Reflected XSS occurs when attacker-controlled input is included in the server's immediate response.

A typical flow is:

1. An attacker creates a URL containing malicious input.
2. The victim opens the URL.
3. The application reads the input and places it unsafely into the response.
4. The victim's browser interprets the injected content.

It is called reflected because the input is sent to the server and reflected back in the response. It is non-persistent because the payload is not necessarily stored by the application.

#### Stored XSS (Persistent)

Stored XSS occurs when attacker-controlled content is saved by the application and later displayed to other users.

A typical flow is:

1. An attacker submits content to a comment, profile, message, or other storage feature.
2. The application stores the content.
3. Another user opens the affected page.
4. The application retrieves the stored content and renders it unsafely.
5. The victim's browser interprets the injected script.

Stored XSS can affect many users because the malicious content remains in the application until it is removed or neutralised.

#### DOM-Based XSS

DOM-based XSS occurs when client-side JavaScript handles untrusted data in an unsafe way and changes the page's DOM so that the browser interprets the data as executable content.

The vulnerability may occur entirely in the browser. The server may not need to reflect the malicious value in its response.

This makes DOM-based XSS important for SOC analysts because a server access log may show the URL but may not contain enough evidence to prove that the browser executed the payload.

### 7.4 What can attackers achieve with XSS?

Depending on the application and browser protections, XSS may allow an attacker to:

- Perform actions as the victim within the vulnerable website.
- Read sensitive page content available to the victim.
- Capture information entered into a vulnerable page.
- Attempt to access session-related information that is exposed to scripts.
- Display fraudulent content or redirect the victim.
- Abuse the trust a user places in the legitimate website.

Modern cookie protections such as `HttpOnly` can prevent JavaScript from directly reading certain cookies. Therefore, it is not accurate to assume that every XSS vulnerability automatically exposes a session cookie. XSS can still be serious even when cookies are protected.

### 7.5 How to prevent XSS

- Treat all user-controlled data as untrusted.
- Apply context-appropriate output encoding before displaying data.
- Use safe templating features and framework protections correctly.
- Avoid unsafe DOM operations that interpret untrusted strings as HTML.
- Use sanitisation when the application intentionally accepts HTML.
- Keep frameworks and libraries updated.
- Apply a suitable Content Security Policy (CSP) as an additional defensive layer.
- Use secure cookie attributes.

Input validation is useful, but it is not a replacement for correct output encoding. A string that looks harmless in one context may be dangerous in another.

### 7.6 How a SOC analyst can detect XSS attempts

Look for patterns such as:

- Script-related words or markup.
- HTML tags and event-handler-like attributes.
- Encoded angle brackets or quotation marks.
- JavaScript-related strings.
- Unusual input in search parameters, comments, profile fields, or other user-controlled locations.
- Repeated requests that test many variations of possible payloads.

Words such as `script`, `alert`, or `prompt` can be clues, but they are not proof. A developer, security scanner, or normal application feature may legitimately include similar strings.

### 7.7 Understanding the WordPress access-log example

The course example describes Apache access logs from a WordPress application. The requests target the `/blog/` page and change the `s` parameter. WordPress commonly uses this parameter for search terms.

The investigation process is:

1. Notice that many requests target the same page.
2. Observe that the `s` parameter changes between requests.
3. Notice URL-encoded special characters.
4. Decode the values using an approved method.
5. Identify script-related content in the decoded values.
6. Compare timestamps and User-Agent values.
7. Determine whether the traffic resembles automated vulnerability scanning.

The example reports that requests arrived every few seconds and that the User-Agent identified a Python `urllib` library. This supports the conclusion that the traffic was generated by a script or automated client.

The example also notes that the source IPs belonged to Cloudflare. This is important: when a website is behind a CDN or reverse proxy, the web server may record the proxy's address rather than the original visitor's address. The analyst must consult the trusted proxy configuration and the appropriate CDN logs to identify the original client where possible.

**What can we conclude?**

- The requests contained XSS-style test input.
- The traffic was consistent with automated scanning.
- The application was the target of the requests.
- The logs alone did not prove that the payload executed in a victim's browser.

To establish success, I would need additional evidence such as application behaviour, response content, browser-side telemetry, WAF details, or evidence of a victim interacting with the affected page.

---

## 8. Command Injection

### 8.1 What is command injection?

Command injection occurs when an application takes untrusted input and passes it to an operating-system command interpreter in an unsafe way.

For example, an application may offer a feature that copies a user-selected file to a temporary directory. If the application constructs a shell command by joining a fixed command with a user-controlled filename, the filename may be interpreted as part of the command rather than as a simple filename.

The core problem is that **data supplied by the user becomes part of an instruction executed by the operating system**.

### 8.2 Understand the difference between data and commands

Imagine an application is designed to copy a file.

The developer intends the filename to be treated only as data. However, if the application builds a shell command by concatenating strings, special shell characters in the filename may change how the shell interprets the command.

Some command interpreters use metacharacters to separate commands, redirect output, or connect commands. If untrusted input is passed into a shell without safe handling, an attacker may be able to alter the intended operation.

The exact behaviour depends on the operating system, shell, application code, and execution environment.

### 8.3 Why command injection is serious

The injected command runs with the privileges of the application process.

If the web application runs with excessive privileges, the consequences can be severe. Depending on those privileges, an attacker may be able to:

- Read files accessible to the application account.
- Modify or delete files.
- Discover system information.
- Access application secrets.
- Create or alter system resources.
- Establish further access.
- Disrupt the service.
- Attempt to move deeper into the environment.

Command injection does not automatically give an attacker administrator or root privileges. The attacker is initially limited by the permissions of the vulnerable application process, unless another weakness allows privilege escalation.

### 8.4 How to prevent command injection

- Avoid invoking an operating-system shell when a safe library or API can perform the task.
- Use APIs that pass executable arguments separately instead of building a shell command from strings.
- Validate input against a strict allowlist of permitted values.
- Treat filenames and other apparently harmless fields as untrusted.
- Run the web application with the minimum privileges required.
- Restrict access to sensitive files and operating-system resources.
- Keep software and dependencies updated.
- Log and monitor unexpected child-process creation.

Using containers or virtualisation can add isolation, but it does not fix vulnerable command construction. A vulnerable application can still be exploited inside a container.

### 8.5 How a SOC analyst can detect command injection

Look for:

- Operating-system command names appearing in unexpected request fields.
- Shell metacharacters in user-controlled input.
- Unusual combinations of separators, paths, and command arguments.
- Suspicious command content in headers such as User-Agent.
- A web server process spawning shells or unexpected utilities.
- Unexpected child processes such as command interpreters, scripting engines, or file-management tools.
- Web server processes reading sensitive files or making unusual network connections.

Do not rely only on keywords such as `ls`, `cat`, `dir`, or `cp`. These strings can appear in legitimate data. Process telemetry and application context are important.

### 8.6 The Shellshock example

The course shows a request in which the User-Agent header contains a suspicious Bash-related expression and an attempt to read `/etc/passwd`.

This is associated with **Shellshock**, a Bash vulnerability disclosed in 2014. The vulnerability involved Bash incorrectly processing specially crafted environment-variable definitions that could lead to command execution.

Why is this important for detection?

- The User-Agent is normally metadata describing the client.
- In this example, it contains shell-related syntax rather than an ordinary browser identification.
- The payload attempts to cause server-side command execution.
- A vulnerable server may execute the command in the context of the affected service.

The key SOC lesson is that an attack payload can be placed in an HTTP header, not just in a URL or form field.

**What should I check next?**

- Was the targeted server running a vulnerable Bash version?
- Did the request reach the vulnerable component?
- Did the web server or related process spawn Bash or another unexpected process?
- Were sensitive files accessed?
- Did the server make unusual outbound connections?
- Are there related requests from the same source or infrastructure?

A suspicious request proves an attempt was made. Process and host evidence are needed to determine whether command execution actually occurred.

---

## 9. Insecure Direct Object Reference (IDOR) and Broken Access Control

### 9.1 What is IDOR?

**Insecure Direct Object Reference (IDOR)** occurs when an application uses an identifier supplied by a user to access an object but fails to check whether that user is authorised to access it.

An object could be:

- A user profile.
- An invoice.
- A document.
- An order.
- A support ticket.
- A medical record.
- A stored image or file.

The identifier may be a number, username, filename, UUID, or another reference.

IDOR is an example of **Broken Access Control**, which was the first category in the OWASP Top 10 2021 list.

### 9.2 Understand the authorisation problem

Imagine a web application that displays account information using an identifier in the request.

The application receives the identifier and retrieves the matching record. That is not inherently unsafe. The vulnerability occurs if the application does not verify that the currently authenticated user is allowed to access that record.

For example:

- User A is authenticated and should be able to view only User A's invoice.
- The request contains an invoice identifier.
- User A changes the identifier to refer to User B's invoice.
- The application returns User B's invoice without checking ownership or permissions.

The problem is not that the identifier is predictable. The problem is the missing server-side authorisation check.

### 9.3 What attackers can do with IDOR

Depending on the affected feature, an attacker may:

- Read another user's personal information.
- Access private documents.
- View another user's orders or invoices.
- Modify another user's data.
- Delete records.
- Perform actions that should be restricted to another account.

IDOR may expose read-only information or permit changes. The actual impact depends on the application's functionality and the missing authorisation checks.

### 9.4 How to prevent IDOR

- Check authorisation on the server for every object access.
- Verify that the authenticated user is allowed to perform the requested action on the specific object.
- Do not rely on hiding identifiers in the browser.
- Do not assume that unpredictable identifiers replace access-control checks.
- Use the authenticated session to determine the current user where appropriate.
- Apply access-control checks to read, update, and delete operations.
- Test access controls using different user roles and accounts.

Removing unnecessary user-supplied identifiers may reduce exposure in some designs, but it is not a complete replacement for server-side authorisation.

### 9.5 Why IDOR is difficult to detect

Unlike SQL injection or XSS, IDOR may not contain a recognisable attack payload. A request can look completely normal.

For example, a request to view an invoice may contain an ordinary identifier. The suspicious behaviour becomes clear only when the analyst knows:

- Which user made the request.
- Which object belongs to which user.
- Whether the user is allowed to access it.
- Whether the application returned data belonging to someone else.

This is why identity, application audit logs, and access-control context are important.

### 9.6 How a SOC analyst can detect possible IDOR

Look for:

- Repeated requests to the same endpoint with changing object identifiers.
- Sequential or predictable identifiers being tested.
- One account requesting many users' records.
- Unusual access to profile, invoice, document, or account-management endpoints.
- A high number of requests in a short period.
- Access patterns inconsistent with the user's normal activity.
- Evidence that a user received or modified an object belonging to another user.

A sequence such as `id=1`, `id=2`, `id=3` may suggest enumeration, but it is not enough by itself to confirm IDOR. Some applications legitimately request multiple records.

### 9.7 Understanding the WordPress user-edit example

The course example describes requests to a WordPress user-edit page with different `user_id` values.

The investigation observes:

1. The same endpoint is requested repeatedly.
2. The `user_id` parameter changes across requests.
3. Many requests occur within a short time.
4. The User-Agent identifies `wfuzz/3.1.0`, which supports the hypothesis of automated testing.
5. The logged source address belongs to Cloudflare, meaning the application may be behind that service.

This pattern is consistent with automated enumeration or access-control testing.

The course then considers response status and response size. A redirect response may indicate that the application redirected the request, perhaps because the user was not authorised. Similar response sizes across many requests may also suggest that the same generic page was returned.

However, response size and status code are only clues. A `302` does not universally mean failure, and equal response sizes do not prove that no data was exposed.

**What would strengthen the conclusion?**

- Application audit logs showing the authenticated user and requested object.
- Authorisation decision logs.
- Evidence of which user record was returned.
- Response body or application-level result, where safely available.
- Database audit logs showing whether records were read or modified.
- Confirmation from the application owner or a controlled reproduction.

---

## 10. Local File Inclusion (LFI) and Remote File Inclusion (RFI)

### 10.1 What is file inclusion?

Some web applications load files dynamically. For example, an application may choose which language file or page template to load based on a parameter.

This feature can be legitimate. The risk appears when the application uses untrusted user input to determine which file should be included, without restricting the value safely.

### 10.2 Local File Inclusion (LFI)

**LFI** occurs when an application can be made to include or access an unintended file located on the same server.

An attacker may attempt to use path manipulation to escape the intended directory and access files elsewhere on the server.

The course describes directory traversal using parent-directory references. The basic idea is that the attacker attempts to move from the application's intended folder to another location in the filesystem.

Potential impact includes:

- Reading sensitive local files.
- Exposing configuration information.
- Revealing credentials or secrets stored in files.
- Accessing application source code.
- In some application-specific situations, contributing to code execution.

LFI does not automatically mean that arbitrary code execution is possible. The outcome depends on the programming language, file-inclusion behaviour, permissions, and server configuration.

### 10.3 Remote File Inclusion (RFI)

**RFI** occurs when an application can be made to include a file from a remote system, such as a file hosted on an attacker-controlled server.

If the application is configured to retrieve and interpret remote content unsafely, the attacker may be able to cause the server to process content that it should never trust.

Potential impact can include:

- Execution of attacker-controlled code, depending on the application.
- Disclosure of information.
- Further compromise of the web server.
- Service disruption.

RFI is not the same as a normal browser redirect. In RFI, the vulnerable server-side application is made to include or process remote content.

### 10.4 How LFI and RFI happen

A vulnerable application might use a parameter to choose a language file.

Under normal conditions, a value such as `en` selects the intended English-language file.

The design becomes unsafe if the application directly combines the supplied value with a filesystem path or remote resource location. An attacker may then try to supply path characters or a remote URL to make the application load something unintended.

The root cause is trusting user-controlled input when selecting files or resources.

### 10.5 LFI versus RFI

| Feature | LFI | RFI |
|---|---|---|
| File location | On the vulnerable server | On a remote server |
| Typical attacker goal | Read or include unintended local files | Cause the application to include remote content |
| Common clues | Traversal patterns, filesystem paths, sensitive filenames | Remote URL schemes or external hostnames in file-related parameters |
| Potential impact | Local information disclosure; sometimes further compromise | Remote content processing and, in vulnerable configurations, code execution |

### 10.6 How to prevent LFI and RFI

- Do not build file paths directly from untrusted input.
- Use an allowlist that maps safe user choices to known files.
- Canonicalise and validate paths before use.
- Restrict file access to the intended application directory.
- Disable unnecessary remote file inclusion features.
- Apply least-privilege permissions to the web application.
- Keep frameworks and runtime environments updated.
- Implement server-side validation; client-side checks can be bypassed.

### 10.7 How a SOC analyst can detect LFI and RFI

Look for:

- Repeated parent-directory traversal patterns.
- Unusual path separators and encoded traversal characters.
- References to sensitive operating-system or application files.
- File-related parameters containing unexpected paths.
- Remote URL schemes or external hostnames in parameters used to select files.
- Repeated attempts against the same endpoint using different path variations.
- Web server processes accessing files outside their normal directories.

The presence of a slash, dot, or URL is not enough to prove an attack. Many legitimate requests contain these characters. The analyst must understand which parameter is being used and how the application handles it.

### 10.8 Investigating possible LFI/RFI attempts

1. Identify the endpoint and parameter receiving the suspicious value.
2. Decode URL-encoded input safely.
3. Determine whether the value resembles path traversal or an unexpected remote resource.
4. Check whether the request was blocked by a WAF or reached the application.
5. Review application errors and file-access telemetry.
6. Check whether sensitive files were accessed.
7. For possible RFI, review outbound network connections from the web server.
8. Look for unexpected child processes or files created by the web server process.
9. Escalate if there is evidence of sensitive file access or code execution.

---

## 11. SQL Injection (SQLi)

This section incorporates the supplied lesson on detecting SQL Injection attacks because it is another major web attack that SOC analysts should recognise.

### 11.1 What is SQL Injection?

SQL Injection occurs when an application includes untrusted user input directly in a SQL query in a way that allows the input to change the query's intended meaning.

SQL is the language many applications use to communicate with relational databases. A web application may use SQL to:

- Authenticate users.
- Search for products.
- Retrieve account information.
- Display orders.
- Create or update records.

The vulnerability appears when the application treats user input as part of the SQL instruction rather than safely treating it as data.

### 11.2 Understand the normal login process

Imagine a login form that asks for a username and password.

The application needs to check whether a matching account exists in the users table. Conceptually, it searches for a record whose username and password match the supplied values.

In a vulnerable design, the application may build a SQL statement by joining text with the user's input. If the input contains SQL syntax, it may change the structure or logic of the query.

A safer design uses parameterised queries or prepared statements. These keep the SQL instruction separate from the values supplied by the user.

### 11.3 Why an apostrophe can matter

In SQL, quotation marks are often used to delimit text values. If an application inserts a user-provided value directly inside a quoted SQL string, an unexpected quotation mark may break the intended structure.

The resulting database error can reveal that the application is constructing a query unsafely. Error messages may disclose database details, but a well-configured application should not expose internal database errors to users.

### 11.4 How a logic-based injection works

The supplied lesson demonstrates a classic example in which an attacker attempts to alter a login condition so that it evaluates as true.

The important concept is not memorising a particular payload. It is understanding the logic:

- The application expects a username value.
- The application inserts that value into a SQL query.
- The attacker supplies input that changes the query's condition.
- The database evaluates the altered condition.
- If the application trusts the result, authentication may be bypassed.

The root cause is unsafe query construction, not simply the presence of a particular character.

### 11.5 Types of SQL Injection

#### In-band SQL Injection

The attacker sends the SQL injection input and receives the result through the same communication channel.

For example, the web page itself may display database information or an error resulting from the injected query.

This is often easier to observe because the result is returned in the normal HTTP response.

#### Inferential or Blind SQL Injection

The attacker cannot directly see the database result. Instead, they infer information from differences in application behaviour.

The application might respond differently depending on whether a condition is true or false, or it may respond at different times. The attacker uses these differences to infer information.

It is called blind SQLi because the database output is not directly displayed.

#### Out-of-band SQL Injection

The attacker causes the database or server to communicate through a different channel from the original web request.

For example, a vulnerable system might be induced to make a DNS request that the attacker can observe. The result is communicated outside the normal HTTP response channel.

Whether this is possible depends on the database, its configuration, network access, and available features.

### 11.6 What attackers may achieve with SQLi

Depending on the database and application permissions, SQL injection may allow:

- Authentication bypass.
- Unauthorised reading of sensitive records.
- Modification or deletion of database entries.
- Disclosure of database structure or metadata.
- Access to other data stored in the database.
- In some configurations, operating-system command execution through database features.

SQL injection does not automatically provide operating-system access. That depends on database capabilities, privileges, and additional configuration.

### 11.7 How to prevent SQL Injection

- Use parameterised queries or prepared statements.
- Avoid building SQL commands by concatenating untrusted input.
- Use an ORM or framework safely and follow its security guidance.
- Validate input according to expected data types and formats.
- Use least-privilege database accounts.
- Avoid exposing detailed database errors to users.
- Keep frameworks, database software, and dependencies updated.
- Review all user-controlled input, not just form fields.

Input validation is useful, but parameterisation is the key protection against changing the structure of a SQL query.

### 11.8 How a SOC analyst can detect SQL Injection

Look for:

- SQL keywords appearing in unexpected user-controlled fields.
- Unusual quotation marks, comments, parentheses, and operators.
- Encoded special characters in query strings.
- Repeated requests that vary the same parameter.
- Database error messages.
- Unusual response sizes or status-code patterns.
- Requests containing known scanner indicators.
- Unexpected database activity following suspicious web requests.

Potential SQL-related terms include `SELECT`, `UNION`, `WHERE`, `INSERT`, and `UPDATE`. These words can also appear in legitimate application data, so their presence alone does not prove SQL injection.

### 11.9 Detecting automated SQL injection tools

The supplied lesson mentions tools such as sqlmap. A SOC analyst can look for several clues:

- **User-Agent:** Some automated tools identify themselves in the User-Agent string. However, this value can be changed.
- **Request frequency:** Automated scanners may send many requests in a short period.
- **Payload variation:** Scanners often test many input variations against the same parameter.
- **Payload complexity:** Automated tools may generate long or complex test strings.
- **Repeated target behaviour:** The same endpoint and parameter may be tested many times.

No single clue proves that a tool was used. A legitimate scanner or authorised penetration test can generate similar traffic. Check asset ownership, approved testing windows, and change records before classifying the activity as malicious.

### 11.10 Understanding the SQL injection access-log example

The supplied lesson describes web access logs containing requests to a page with an `id` parameter.

The investigation proceeds as follows:

1. Identify the requested pages and notice repeated requests to the same application resource.
2. Observe percent-encoded characters in the URLs.
3. Decode the values using an approved method.
4. Identify SQL-related terms and patterns in the decoded input.
5. Compare timestamps and request frequency.
6. Review the User-Agent and payload complexity for signs of automated scanning.
7. Check the response status and response size where available.
8. Correlate with application and database logs to assess impact.

The example reports more than 50 requests in one second. This strongly supports automated activity, although request rate alone does not prove malicious intent.

The course example identifies a source address and concludes that SQL injection testing occurred against the `id` parameter. However, because reliable response-size information was unavailable, it could not determine whether the injection succeeded.

**Important:** A detected SQL injection attempt is not the same as confirmed database compromise. To establish success, look for database audit events, application behaviour, unusual data access, data changes, or other corroborating evidence.

---

## 12. Comparing the Web Attacks

These vulnerabilities can look similar in access logs because attackers may place payloads in URLs, parameters, headers, or request bodies. The underlying weakness and impact are different.

| Attack | Main weakness | What the attacker tries to influence | Possible impact |
|---|---|---|---|
| XSS | Unsafe handling of untrusted content in a browser context | The victim's browser | Script execution in a user's browser, account actions, or information exposure |
| Command Injection | Unsafe passing of input to an operating-system command interpreter | The web server's operating system | Command execution with the application's privileges |
| IDOR | Missing object-level authorisation | Which record or object the application returns or changes | Unauthorised access, modification, or deletion of data |
| LFI | Unsafe selection or inclusion of local files | Files on the web server | Local file disclosure and, in some cases, further compromise |
| RFI | Unsafe inclusion of remote content | Content hosted on another system | Remote content processing and possible code execution in vulnerable configurations |
| SQL Injection | Unsafe construction of database queries | The database query | Unauthorised data access, modification, deletion, or possible further impact |

### A simple way to remember the difference

- **XSS:** The attacker's input is interpreted by a victim's browser.
- **Command Injection:** The attacker's input changes a command executed by the server's operating system.
- **IDOR:** The application fails to check whether the user is allowed to access a particular object.
- **LFI:** The application is tricked into including or accessing an unintended local file.
- **RFI:** The application is tricked into including or processing content from a remote location.
- **SQLi:** The attacker's input changes the meaning of a database query.

---

## 13. A SOC Analyst's Web Attack Investigation Workflow

When a WAF, SIEM, or web server alert identifies a possible web attack, I can follow this workflow.

### Step 1 – Validate the alert

- Identify which security control generated the alert.
- Understand the rule name and why it triggered.
- Check whether the alert is from a WAF, IPS, SIEM, web server, or application log.
- Determine whether the request was blocked, allowed, or only observed.

### Step 2 – Understand the HTTP request

- Identify the hostname, endpoint, method, and parameters.
- Inspect the request headers.
- Check the request body if it is available and authorised for review.
- Identify where the suspicious input appears.
- Decode URL-encoded content safely.

### Step 3 – Identify the likely attack category

Ask what the input appears to be trying to influence:

- Browser interpretation: possible XSS.
- Operating-system command execution: possible command injection.
- Database query logic: possible SQL injection.
- Object identifier or record access: possible IDOR.
- Local filesystem path: possible LFI.
- Remote resource location: possible RFI.

This is an initial classification, not a final conclusion.

### Step 4 – Establish context

- Is the source a known scanner, CDN, proxy, or internal testing system?
- Is there an approved vulnerability assessment or penetration test?
- Is the endpoint expected to receive this kind of input?
- Has the same source targeted other endpoints?
- Are multiple users or systems involved?

### Step 5 – Review the response and application behaviour

- Check HTTP status codes.
- Compare response sizes where meaningful.
- Look for application errors.
- Check whether the request was redirected or blocked.
- Review application logs and audit records.
- Do not assume a `200` means success or a `403` means the attack had no impact.

### Step 6 – Correlate with other telemetry

Depending on the suspected attack, review:

- WAF and reverse proxy logs.
- Web server access and error logs.
- Application logs.
- Database audit logs.
- DNS and network connection logs.
- EDR process and file telemetry.
- Authentication and identity logs.
- CDN logs, when traffic passes through a CDN.

### Step 7 – Determine whether the attack succeeded

Look for evidence that the intended action actually happened:

- For XSS: evidence of unsafe content being rendered or script execution in a browser.
- For command injection: unexpected child processes or operating-system activity.
- For IDOR: evidence that one user accessed another user's object.
- For LFI: evidence of sensitive local file access.
- For RFI: outbound retrieval of remote content or processing of that content.
- For SQLi: database activity or application evidence showing that the query was altered and data was accessed or changed.

If the available logs do not prove success, state that the attempt was detected but the outcome is undetermined.

### Step 8 – Document and escalate

A useful case report should include:

- Alert name and detection source.
- Date and time, including timezone.
- Affected hostname, application, and endpoint.
- Source IP and any proxy/CDN context.
- HTTP method and suspicious parameter or header.
- Relevant decoded indicators.
- Request frequency and related activity.
- Response status and size, if available.
- Correlated WAF, application, database, network, and endpoint evidence.
- Whether the request was blocked or allowed.
- Assessment of success, failure, or unknown outcome.
- Confidence level and reason for escalation.

---

## 14. Important SOC Investigation Lessons

1. **A suspicious request is evidence of an attempt, not proof of success.**
2. **HTTP methods and status codes must be interpreted in application context.**
3. **Attack payloads can appear anywhere in an HTTP request:** URL, query string, body, cookies, or headers.
4. **URL encoding can hide suspicious input.** Decode it before drawing conclusions.
5. **Do not rely only on keywords.** Legitimate content can contain strings that resemble attack payloads.
6. **User-Agent values can be forged.** Treat them as clues, not trusted identity.
7. **High request frequency may indicate automation**, but authorised scanners can generate similar traffic.
8. **A CDN or reverse proxy can hide the original client IP.** Use trusted proxy and CDN logs to investigate attribution.
9. **A `200` response does not prove an attack succeeded.** A `302`, `403`, or `404` does not automatically prove it failed.
10. **Response size can support an investigation**, but it is not definitive proof of what data was returned.
11. **Correlate multiple sources.** Web access logs alone may not show database or operating-system activity.
12. **Check for authorised testing.** Vulnerability scanners and penetration tests can resemble attacks.
13. **Protect log data.** Do not upload sensitive organisation logs to public decoding or analysis websites.
14. **Record uncertainty honestly.** If the evidence cannot establish the outcome, say so.

---

## 15. Glossary

| Term | Simple explanation |
|---|---|
| HTTP | Protocol used by clients and web servers to exchange requests and responses |
| HTTPS | HTTP protected by TLS encryption |
| Client | The browser or application making a request |
| Server | The system receiving and processing the request |
| Request line | Part of an HTTP request containing the method, path, and protocol version |
| Header | Metadata included in an HTTP request or response |
| Request body | Data sent by the client to the server |
| Response body | Content returned by the server |
| Status code | Number describing the result of an HTTP request |
| Cookie | Data stored by a browser and sent to a website when applicable |
| Session | Server-recognised state associated with a user's interaction or login |
| User-Agent | Header describing the client software |
| Access log | Record of requests handled by a web server or web infrastructure component |
| URL encoding | Representation of special characters using percent-encoded values |
| WAF | Web Application Firewall; inspects web traffic for suspicious or prohibited requests |
| IPS | Intrusion Prevention System; detects and may block suspicious activity |
| SIEM | Platform that collects and correlates security logs and alerts |
| XSS | Cross-Site Scripting; unsafe content is interpreted as script in a user's browser |
| DOM | Document Object Model; browser representation of a web page |
| Command Injection | User input changes a command executed by the operating system |
| IDOR | Insecure Direct Object Reference; missing authorisation check for an object |
| LFI | Local File Inclusion; unintended local file is accessed or included |
| RFI | Remote File Inclusion; remote content is included or processed unsafely |
| SQLi | SQL Injection; user input changes the meaning of a database query |
| CDN | Content Delivery Network; distributes content and may act as a reverse proxy |
| Reverse proxy | An intermediary that receives client requests and forwards them to backend servers |
| Enumeration | Systematically testing or listing identifiers, accounts, or resources |
| Payload | Input crafted to trigger or test a particular behaviour |
| False positive | An alert that identifies benign activity as suspicious |
| Correlation | Combining evidence from multiple sources to understand an event |

---

## 16. Learning Reflection

In this lesson, I learned why web applications are important targets and why SOC analysts need to understand the normal behaviour of HTTP before they can recognise suspicious requests.

I now understand that an HTTP request is made up of more than just a URL. The method, headers, cookies, parameters, and request body can all contain information that matters during an investigation. The server's response also provides useful clues through its status code, headers, and response size, although none of these values should be treated as conclusive proof on their own.

I studied several important web application attacks:

- XSS helped me understand how unsafe input can become executable script in a victim's browser.
- Command Injection showed me how unsafe input can affect commands executed by the web server's operating system.
- IDOR helped me understand that authentication is not enough; an application must also verify whether a user is authorised to access each object.
- LFI and RFI showed me how unsafe file selection can expose local files or cause remote content to be included.
- SQL Injection helped me understand how unsafe query construction can allow user input to change database logic.

The most important SOC lesson is that detecting an attack attempt and confirming a successful compromise are two different tasks. Access logs can reveal suspicious patterns, payloads, request rates, and target parameters. However, I may need application logs, database audit records, WAF logs, network telemetry, and EDR evidence to understand the actual impact.

I should investigate carefully, correlate evidence, consider authorised scanning activity, and clearly document what is known and what remains uncertain.

---

## 17. Study Record

| Field | Details |
|---|---|
| Platform | LetsDefend |
| Topic | Detecting Web Attacks |
| Study date | 13 November 2026 |
| Main concepts | HTTP, OWASP Top 10, XSS, Command Injection, IDOR, LFI, RFI, SQL Injection |
| Practical focus | Understanding HTTP requests, responses, access logs, payload patterns, automation, and attack success |
| Status | Study notes prepared |

---

## 18. Further Reading

- [OWASP](https://owasp.org/)
- [OWASP Top 10 – 2021](https://owasp.org/Top10/)
- [OWASP Cross Site Scripting Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [MDN – HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)

---

*Personal SOC learning notes — understand the behaviour, investigate the evidence, and never confuse an attempted attack with a confirmed compromise.*
