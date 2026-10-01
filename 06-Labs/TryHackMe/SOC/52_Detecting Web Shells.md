# Detecting Web Shells --- SOC Learning Notes

**Date:** 29 September 2026\
**Focus:** SOC / Blue Team / Web Attack Detection\
**Source:** TryHackMe --- Detecting Web Shells

------------------------------------------------------------------------

## 1. What Is a Web Shell?

A **web shell** is a malicious program or script uploaded to a web
server that allows an attacker to execute commands remotely through web
requests.

In simple terms:

``` text
Attacker
   ↓
HTTP Request
   ↓
Web Shell
   ↓
Web Server
   ↓
Operating System
   ↓
Command Execution
   ↓
Output returned to attacker
```

A simple web shell may accept a parameter such as:

``` text
?cmd=whoami
```

The server-side script reads the value, executes it, and returns the
result.

A possible result is:

``` text
www-data
```

This can indicate the account under which the web server is running.

### Why Web Shells Are Dangerous

Once a web shell is available, an attacker may be able to:

-   Perform reconnaissance
-   Discover files and directories
-   Execute operating-system commands
-   Attempt privilege escalation
-   Move laterally
-   Access sensitive information
-   Exfiltrate data
-   Establish or maintain persistence
-   Modify files
-   Execute additional tools

The exact capabilities depend on the web server, operating system,
permissions, and shell functionality.

------------------------------------------------------------------------

## 2. Web Shells in the Attack Chain

A common sequence is:

``` text
Find vulnerable application
        ↓
Exploit vulnerability
        ↓
Upload web shell
        ↓
Web server stores shell
        ↓
Attacker accesses shell
        ↓
Execute commands
        ↓
Reconnaissance
        ↓
Privilege escalation
        ↓
Lateral movement
        ↓
Data access / exfiltration
```

A web shell can therefore be associated with **initial access** as well
as **persistence**.

The TryHackMe material references MITRE ATT&CK techniques including:

-   **T1190 --- Exploit Public-Facing Application**
-   **T1505.003 --- Web Shell**

The important SOC lesson is to understand the behavior represented by
these techniques, not only memorize their IDs.

------------------------------------------------------------------------

## 3. How Web Shells Are Deployed

One common route is an insecure file-upload feature.

Imagine a website that allows users to upload pet photos. The
application expects:

``` text
dog.jpg
cat.png
```

If the application does not properly validate the uploaded file, an
attacker may attempt to upload executable server-side code such as:

``` text
shell.php
```

If the server executes PHP files in that location, the uploaded file may
become a remotely accessible command-execution point.

### Why File Validation Matters

A secure upload mechanism should carefully validate:

-   File type
-   File extension
-   File contents
-   Destination directory
-   Permissions
-   Whether uploaded files can be executed

A suspicious example is:

``` text
image.jpg.php
```

A double extension may be an attempt to disguise an executable file.

------------------------------------------------------------------------

## 4. Web Shells as Persistence

A web shell can remain on a server after the original vulnerability has
been fixed:

``` text
Attacker exploits vulnerability
        ↓
Uploads web shell
        ↓
Original vulnerability gets patched
        ↓
Web shell remains
        ↓
Attacker accesses it later
```

Therefore, incident response should not stop at patching the original
vulnerability.

Investigate:

-   Newly created files
-   Recently modified files
-   Suspicious scripts
-   Upload directories
-   File ownership
-   File permissions
-   Web-server activity after the initial compromise

------------------------------------------------------------------------

## 5. Examples Mentioned in the Room

### Hafnium and ProxyLogon

The TryHackMe material describes Hafnium as a threat group associated
with exploiting Microsoft Exchange and deploying `.aspx` web shells.

The useful detection lesson is the pattern:

``` text
Exploit exposed application
        ↓
Deploy web shell
        ↓
Execute commands
        ↓
Reconnaissance
        ↓
Credential access
        ↓
Persistence
        ↓
Lateral movement
        ↓
Exfiltration
```

### Conti

The material also describes Conti ransomware operators abusing a
Microsoft Exchange vulnerability to upload an ASP.NET web shell.

The SOC lesson is:

> Application exploitation followed by suspicious file creation and
> web-shell access should be investigated as a connected sequence.

------------------------------------------------------------------------

## 6. Anatomy of a Web Shell

Web shells often abuse legitimate programming functions.

For example, PHP provides functions such as:

``` text
shell_exec()
exec()
system()
passthru()
```

These functions are not inherently malicious. The security problem
occurs when untrusted input is allowed to reach them.

The basic flow is:

``` text
User supplies command
        ↓
Application reads command
        ↓
Server-side code executes command
        ↓
Output is returned
```

------------------------------------------------------------------------

## 7. Understanding a Simple PHP Web Shell

A simplified implementation works conceptually like this:

1.  Check whether the `cmd` parameter exists.
2.  Read the supplied command.
3.  Pass it to a system-execution function.
4.  Capture the output.
5.  Display the output.

For example:

``` text
/awebshell.php?cmd=whoami
```

The flow is:

``` text
HTTP request
     ↓
cmd=whoami
     ↓
PHP reads "whoami"
     ↓
shell_exec("whoami")
     ↓
Operating system
     ↓
www-data
     ↓
HTTP response
```

The result `www-data` can indicate the account under which the web
server is running on a Linux system.

------------------------------------------------------------------------

## 8. Web Shell Complexity

Web shells can be extremely simple or sophisticated.

### Simple

``` text
shell.php?cmd=whoami
```

### More advanced

A web shell may contain:

-   Password protection
-   Command interface
-   File manager
-   File upload/download
-   Directory browsing
-   Database interaction
-   Multiple command functions
-   Graphical interface

A malicious web shell may therefore be only a few lines of code and may
not look like an obvious hacking dashboard.

------------------------------------------------------------------------

## 9. URL Encoding

Commands sent through URLs may require URL encoding.

For example:

``` text
ls -la
```

can be represented as:

``` text
ls%20-la
```

because:

``` text
%20 = space
```

During investigation, consider encoded or obfuscated input.

The TryHackMe room recommends CyberChef for decoding and analyzing
encoded values.

------------------------------------------------------------------------

# Task 4 --- Log-Based Detection

## 10. Web Server Access Logs

Web server logs are one of the first places a SOC analyst can
investigate.

Access logs commonly contain information such as:

-   Client IP
-   Timestamp
-   Requested resource
-   HTTP method
-   Status code
-   Response size
-   Referrer
-   User-Agent

The exact format varies by web server and logging configuration.

------------------------------------------------------------------------

## 11. Client IP

The client IP tells us where a request originated.

An unexpected external IP may be interesting if the application normally
receives only internal traffic.

However:

> An unfamiliar IP address alone does not prove malicious activity.

Always investigate it in context.

------------------------------------------------------------------------

## 12. Timestamp

Timestamps help reconstruct an attack timeline.

Example:

``` text
10:15:01  GET /uploads
10:15:02  POST /upload.php
10:15:03  GET /uploads/shell.php
10:15:04  GET /uploads/shell.php?cmd=whoami
```

The sequence is often more useful than any individual event.

------------------------------------------------------------------------

## 13. HTTP Status Codes

Common status codes include:

``` text
200 OK
404 Not Found
403 Forbidden
302 Found
500 Internal Server Error
```

### 200

The resource was successfully returned.

### 404

The resource was not found. Repeated 404 responses can indicate scanning
or directory discovery.

### 403

Access was refused.

### 302

A redirect occurred. In the earlier web-attack investigation, a
successful login produced a 302 redirect to an account page.

A status code must therefore be interpreted in context.

------------------------------------------------------------------------

## 14. Response Size

Unusual response sizes can be useful indicators.

For example, if normal responses are around 20 KB and one request
produces a very large response, it may deserve investigation.

Response size alone does not prove malicious activity.

------------------------------------------------------------------------

## 15. Referrer

The Referrer can show the page from which a request originated.

Normal navigation might look like:

``` text
/home
   ↓
/products
   ↓
/checkout
```

A direct request to:

``` text
/uploads/webshell.php
```

with no referrer can be interesting.

However, missing referrer information also has legitimate causes, such
as privacy controls or direct navigation.

------------------------------------------------------------------------

## 16. User-Agent

The User-Agent identifies the client software.

Examples:

``` text
Mozilla/5.0 ...
curl/...
wget/...
sqlmap/...
```

Potentially suspicious User-Agents include:

-   Known security tools
-   Automated tools
-   Very old clients
-   Modified browser strings

But:

> User-Agent values can be spoofed.

Never treat a User-Agent alone as proof of compromise.

------------------------------------------------------------------------

## 17. Web Indicators of Web-Shell Activity

Look for:

### Repeated GET requests

Could indicate probing or interaction.

### POST requests to upload locations

Especially interesting when followed by suspicious file creation.

### Repeated access to the same file

For example:

``` text
GET /uploads/awebshell.php
GET /uploads/awebshell.php
GET /uploads/awebshell.php
```

This becomes more suspicious when command parameters are present.

------------------------------------------------------------------------

## 18. HTTP Methods and Possible Abuse

  Method    Normal Usage                            Possible Abuse
  --------- --------------------------------------- ---------------------------------
  GET       Retrieve a resource                     Recon or web-shell interaction
  POST      Submit data                             Upload or web-shell interaction
  PUT       Upload/replace a resource               Uploading a web shell
  DELETE    Remove a resource                       Cleanup
  OPTIONS   Ask which methods are supported         Reconnaissance
  HEAD      Request headers without full response   Resource discovery

An HTTP method itself is not malicious. Context determines whether it is
suspicious.

------------------------------------------------------------------------

## 19. Example Web-Shell Attack Sequence

A possible sequence:

``` text
Directory fuzzing
      ↓
Find valid directory
      ↓
Find upload functionality
      ↓
Upload web shell
      ↓
Access web shell
      ↓
Execute commands
```

Possible evidence:

``` text
GET /random
404

GET /uploads
200

POST /upload.php
200

GET /uploads/awebshell.php
200

GET /uploads/awebshell.php?cmd=whoami
200
```

The sequence is much more meaningful than any one request.

------------------------------------------------------------------------

## 20. Suspicious User-Agents and IPs

Examples mentioned in the room include:

``` text
curl/1.XX.X
wget/1.XX.X
```

These may be suspicious depending on the environment.

An external IP may also be suspicious when a server normally receives
only internal traffic.

Remember:

``` text
Suspicious ≠ confirmed malicious
```

------------------------------------------------------------------------

## 21. Query Strings

A query string contains parameters after `?`.

Example:

``` text
example.php?query=somequery
```

Potentially interesting parameters include:

``` text
cmd=
exec=
shell=
```

For example:

``` text
shell.php?cmd=whoami
```

is highly relevant when investigating web-shell activity.

------------------------------------------------------------------------

## 22. Encoded Query Strings

Attackers can encode values.

The investigation process is:

``` text
Collect suspicious parameter
        ↓
Decode it
        ↓
Understand the content
        ↓
Determine whether it is malicious
```

CyberChef can help with Base64, URL encoding, and other transformations.

------------------------------------------------------------------------

## 23. Auditd

`auditd` is a native Linux auditing utility that records system events.

Rules can be configured to monitor:

-   File creation
-   File modification
-   Program execution
-   Specific directories
-   Specific conditions

For example:

``` bash
ausearch -k web_shell
```

can search for events associated with an audit rule named `web_shell`.

A result might contain:

``` text
name = /uploads/webshell.php
```

and:

``` text
OGID = www-data
```

This gives host-level evidence about the file and account involved.

------------------------------------------------------------------------

## 24. Web Logs + Auditd Correlation

This is one of the most important SOC concepts.

Suppose web logs show:

``` text
POST /upload.php
```

Auditd then shows:

``` text
File created:
/var/www/html/uploads/webshell.php
```

Then web logs show:

``` text
GET /uploads/webshell.php?cmd=whoami
```

The timeline becomes:

``` text
Upload Request
      ↓
File Created
      ↓
Web Shell Accessed
      ↓
Command Execution
```

This is stronger than relying on one indicator.

------------------------------------------------------------------------

## 25. SIEM Correlation

A SIEM can centralize and correlate multiple sources:

``` text
Apache/Nginx logs
        ↓
      SIEM
        ↑
Auditd logs
        ↑
Endpoint telemetry
        ↑
Network telemetry
```

A conceptual detection could combine:

``` text
Suspicious upload
+
New executable web file
+
Web-shell access
+
Command parameter
+
Command execution
```

This can produce a high-priority alert for investigation.

------------------------------------------------------------------------

# Task 5 --- Beyond Logs

## 26. File-System Analysis

A web shell must be stored somewhere on the server.

Common web-root locations include:

### Apache

``` text
/var/www/html/
```

### Nginx

``` text
/usr/share/nginx/html/
```

Applications may also use:

``` text
/uploads/
/images/
/admin/
```

Temporary directories can also be abused if permissions are insecure.

------------------------------------------------------------------------

## 27. Suspicious Files

Investigate:

``` text
.php
.jsp
.aspx
```

especially where executable scripts are not expected.

Also investigate:

``` text
image.jpg.php
```

and unusual random filenames.

For example:

``` text
/var/www/html/uploads/awebshell.php
```

would deserve investigation if it appeared unexpectedly.

------------------------------------------------------------------------

## 28. Finding Recently Modified PHP Files

The room provides:

``` bash
find /var/www -type f -name "*.php" -newerct "2025-07-01" ! -newerct "2025-08-01"
```

The purpose is to locate PHP files modified between two dates.

Example:

``` text
/var/www/html/uploads/awebshell.php
```

This is useful when the approximate attack window is known.

The broader technique is:

> Use timestamps to connect file-system events with network and web-log
> events.

------------------------------------------------------------------------

## 29. Searching for Suspicious Code

The room demonstrates:

``` bash
grep -r "eval(" wp-content
```

This recursively searches for `eval(`.

The result may identify a suspicious PHP file.

Important:

> Finding a suspicious function does not automatically prove that a file
> is malicious. Investigate the surrounding code and context.

------------------------------------------------------------------------

## 30. Network Traffic Analysis

Network traffic analysis lets analysts inspect communication between a
client and server.

A packet capture can potentially reveal:

-   HTTP headers
-   Request methods
-   URLs
-   POST data
-   Cookies
-   Uploaded content
-   Downloaded content
-   User-Agent
-   Application data

This can provide much more detail than a basic access log.

------------------------------------------------------------------------

## 31. HTTP vs HTTPS

Plain HTTP traffic is not encrypted, so application data may be visible
in a packet capture.

HTTPS uses TLS encryption.

Without appropriate decryption capability, a normal capture will not
expose the plaintext application payload.

Conceptually:

``` text
HTTP:
Client → Plain HTTP → Server
             ↓
       Payload visible

HTTPS:
Client → TLS encrypted → Server
             ↓
       Payload protected
```

This is why SOC teams need multiple telemetry sources.

------------------------------------------------------------------------

## 32. Useful Wireshark Filters

### Find POST requests

``` text
http.request.method == "POST"
```

### Find PHP requests

``` text
http.request.uri contains ".php"
```

### Investigate User-Agent

``` text
http.user_agent
```

These filters help reduce the amount of traffic that needs to be
inspected.

------------------------------------------------------------------------

## 33. Detecting Web-Shell Interaction in Wireshark

A suspicious sequence could look like:

``` text
GET /uploads/awebshell.php?cmd=whoami
GET /uploads/awebshell.php?cmd=pwd
GET /uploads/awebshell.php?cmd=ls
```

The important behavior is repeated access to the same script with
different command parameters.

This can indicate interactive command execution.

------------------------------------------------------------------------

# 34. Full Web-Shell Attack Chain

``` text
                    ATTACKER
                       |
                       v
               Website Recon/Fuzzing
                       |
                       v
                Find Upload Point
                       |
                       v
                Upload Web Shell
                       |
                       v
              File Created on Server
                       |
                       v
                Access Web Shell
                       |
                       v
                Execute Commands
                       |
            +----------+----------+
            |          |          |
            v          v          v
          Recon     Privilege   Data Access
                    Escalation
                       |
                       v
                 Lateral Movement
                       |
                       v
                   Exfiltration
```

Evidence may come from:

``` text
Web Logs
+
Auditd
+
File System
+
Network Traffic
+
Endpoint Telemetry
+
SIEM Correlation
```

------------------------------------------------------------------------

# 35. SOC Investigation Mindset

When investigating suspected web-shell activity, ask:

### 1. What happened?

What request or event triggered the investigation?

### 2. Who did it?

Which IP, user, process, or account was involved?

### 3. What was accessed?

Was it a normal webpage, upload endpoint, or suspicious script?

### 4. Was a file created?

Check:

-   Name
-   Location
-   Timestamp
-   Owner
-   Permissions

### 5. What happened next?

Did the same source access the new file?

### 6. Was a command executed?

Look for:

-   Auditd events
-   Process creation
-   Child processes
-   Command-line telemetry

### 7. What happened afterward?

Investigate:

-   Reconnaissance
-   Credential access
-   Privilege escalation
-   Lateral movement
-   Data access
-   Exfiltration

------------------------------------------------------------------------

# 36. Indicator vs Evidence

This distinction is very important.

## Weak indicator

``` text
User-Agent: curl
```

This could be:

-   Administrator
-   Developer
-   Monitoring system
-   Attacker

Therefore:

``` text
curl ≠ attacker
```

## Stronger evidence

Consider:

``` text
External IP
     +
Directory fuzzing
     +
Upload request
     +
New PHP file
     +
Access to new PHP file
     +
cmd=whoami
     +
Web-server command execution
```

This provides a much stronger picture of a possible attack.

The lesson is:

> Do not rely on one indicator. Correlate multiple pieces of evidence.

------------------------------------------------------------------------

# 37. Web-Shell Detection Checklist

## Web Logs

Look for:

-   Repeated requests
-   Directory fuzzing
-   Upload requests
-   Requests to suspicious scripts
-   Repeated access to the same script
-   Suspicious query parameters
-   `cmd=`
-   `exec=`
-   `shell=`
-   Suspicious User-Agents
-   Suspicious source IPs
-   Encoded parameters
-   Unusual HTTP methods

## File System

Look for:

-   Unexpected `.php` files
-   Unexpected `.jsp` files
-   Unexpected `.aspx` files
-   Recently created scripts
-   Recently modified scripts
-   Random filenames
-   Double extensions
-   Scripts in upload directories
-   Unexpected files in web roots

## Endpoint / Host Telemetry

Look for:

-   Web-server processes spawning command interpreters
-   Unexpected child processes
-   File creation
-   File modification
-   Command execution
-   Suspicious process trees

## Network Traffic

Look for:

-   Upload requests
-   Requests to suspicious scripts
-   Repeated requests to the same file
-   Command parameters
-   Encoded commands
-   Suspicious User-Agents
-   Unexpected protocols or ports
-   Suspicious outbound connections

## SIEM

Correlate:

``` text
Web Logs
+
File Events
+
Auditd
+
Endpoint Events
+
Network Events
```

------------------------------------------------------------------------

# 38. Final Learning Summary --- 29 September 2026

Today I studied **Detecting Web Shells** as part of my SOC learning
journey.

The main thing I learned is that a web shell gives an attacker a way to
execute commands on a compromised web server through HTTP requests.

I learned how attackers can deploy web shells through insecure
file-upload functionality and how a web shell can become both an initial
foothold and a persistence mechanism.

I also learned that detecting web shells requires more than looking for
one suspicious string or one suspicious IP address. A better approach is
to reconstruct the attack chain by correlating different types of
telemetry.

The attack chain I want to remember is:

``` text
Recon/Fuzzing
     ↓
Find Upload Function
     ↓
Upload Web Shell
     ↓
File Created
     ↓
Web Shell Access
     ↓
Command Execution
     ↓
Post-Exploitation
```

From a SOC perspective, I should investigate:

``` text
Web Server Logs
File System
Auditd
Network Traffic
Endpoint Telemetry
SIEM
```

The biggest lesson for me is:

> **Don't investigate indicators in isolation. Correlate events and
> build the attack timeline.**

This connects directly with the SIEM and detection work I have already
been learning. The goal is to take scattered telemetry and turn it into
a clear picture of what the attacker did.

------------------------------------------------------------------------

# 39. Quick Revision

### What is a web shell?

A malicious server-side script that allows an attacker to execute
commands remotely through web requests.

### How can it be deployed?

Often through an insecure file-upload function, vulnerable application,
misconfiguration, or previous access.

### Why is it dangerous?

It can provide remote command execution and become a foothold for
further compromise.

### What should I investigate in web logs?

Requests, methods, timestamps, status codes, IPs, User-Agents,
referrers, query strings, uploads, and repeated access patterns.

### What should I investigate on the file system?

New or modified executable scripts, suspicious filenames, double
extensions, and files in upload/web-root directories.

### What can Auditd provide?

Host-level evidence such as file creation, modification, and command
execution.

### Why use PCAP?

It can reveal details of network communications that may not appear in
ordinary web logs.

### Why is HTTPS important?

TLS encrypts application data, limiting what can be seen in a normal
packet capture.

### What is the strongest detection approach?

Correlating:

``` text
Web Logs
+
File System
+
Auditd
+
Endpoint Telemetry
+
Network Traffic
+
SIEM
```

------------------------------------------------------------------------

# 40. One-Page SOC Cheat Sheet

``` text
WEB SHELL
│
├── What?
│   └── Malicious server-side script for remote command execution
│
├── Deployment
│   ├── File upload vulnerability
│   ├── Misconfiguration
│   └── Existing compromise
│
├── Web Log Indicators
│   ├── Upload requests
│   ├── Repeated requests
│   ├── Suspicious paths
│   ├── cmd=
│   ├── exec=
│   ├── Suspicious User-Agent
│   └── Suspicious IP
│
├── File System
│   ├── New .php/.jsp/.aspx
│   ├── Random filenames
│   ├── Double extensions
│   ├── Upload directories
│   └── Recently modified files
│
├── Host Telemetry
│   ├── File creation
│   ├── File modification
│   ├── Process execution
│   └── Web server → command shell
│
├── Network
│   ├── HTTP requests
│   ├── POST uploads
│   ├── Web-shell requests
│   ├── Encoded commands
│   └── Suspicious User-Agent
│
└── SIEM
    ├── Collect
    ├── Correlate
    ├── Investigate
    └── Build attack timeline
```
