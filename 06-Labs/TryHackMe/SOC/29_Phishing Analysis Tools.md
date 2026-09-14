# Phishing Analysis Tools --- TryHackMe


**Room:** Phishing Analysis Tools\
**Date:** 14 September 2026\

------------------------------------------------------------------------

# About This Room

I completed the **Phishing Analysis Tools** room to move from basic
phishing identification into actual phishing investigation.

In the previous rooms I learned how to recognize suspicious emails. In
this room, I started working more like a SOC analyst by collecting
artifacts and using tools to investigate them.

The main things I practiced were:

-   Extracting email header artifacts
-   Finding sender and recipient information
-   Checking sender IP addresses
-   Investigating Return-Path and Reply-To information
-   Extracting URLs from email bodies
-   Generating SHA256 hashes for attachments
-   Checking IP/domain/file reputation
-   Using malware sandboxes
-   Using ANY.RUN reports
-   Understanding phishing attachments
-   Using PhishTool for centralized email analysis
-   Documenting and resolving a phishing case

I also documented **how I got each answer**, instead of only listing the
answers.

> **Sanitization:** Suspicious domains, URLs, and IP addresses are
> defanged in the public-facing sections of this README. Hashes are
> retained because they are useful non-executable identifiers for
> threat-intelligence work.

------------------------------------------------------------------------

# Task 2 --- Identifying Artifacts

The first step in phishing analysis is to collect artifacts.

These artifacts become the starting point for further investigation.

## Header Artifacts

When I receive a suspicious email, I should collect:

  Artifact       Why I Check It
  -------------- -------------------------------------------
  Sender email   Helps identify the claimed origin
  Sender IP      Helps investigate the infrastructure
  Subject        May reveal urgency or social engineering
  Recipient      Shows who was targeted
  Reply-To       Shows where replies are directed
  Return-Path    Can reveal the actual mail-return address
  Date/time      Useful for investigation timelines

------------------------------------------------------------------------

## Body Artifacts

From the email body I should look for:

### URLs

I need to identify every hyperlink and determine where it really leads.

A shortened URL can hide the final destination.

### Attachments

I should collect:

-   Filename
-   Extension
-   File type
-   Hash
-   Any embedded URLs

### File Hash

A hash gives me a unique identifier that can be checked against
threat-intelligence sources.

For example:

``` bash
sha256sum suspicious_file.pdf
```

The important point is that I should analyze attachments in a
**controlled environment**.

------------------------------------------------------------------------

# Task 3 --- Email Header Analysis

Email headers contain information that is not always visible in the
normal email client.

The room introduces several tools for automating header analysis.

## Google Messageheader

The Google Admin Toolbox **Messageheader** tool can analyze a complete
email header and help identify:

-   Sender IP
-   Routing path
-   Header information
-   Possible configuration issues

The basic process is:

``` text
Raw email header
       |
       v
Paste into header analyzer
       |
       v
Review routing information
       |
       v
Identify useful artifacts
```

------------------------------------------------------------------------

## Message Header Analyzer

Another tool covered in the room is **Message Header Analyzer**.

It can provide similar information and make it easier to understand the
path an email took between mail servers.

------------------------------------------------------------------------

# IP Reputation Analysis

Once I have a sender IP, I can investigate it further.

## IPinfo

IPinfo can provide information such as:

-   Geographic location
-   Organization
-   ASN/network information
-   IP ownership information

This can help me determine whether an IP is consistent with the
organization claiming to send the email.

------------------------------------------------------------------------

# URLScan

**URLScan.io** is useful for investigating websites without directly
browsing to them from my own machine.

It can provide:

-   Screenshot of the page
-   Network requests
-   Domains contacted
-   Page behavior
-   Redirect information

This is useful when a phishing email contains a suspicious URL.

The general idea is:

``` text
Suspicious URL
      |
      v
URLScan
      |
      +---- Screenshot
      +---- Requests
      +---- Domains
      +---- Page behavior
```

------------------------------------------------------------------------

# Cisco Talos Reputation Center

Cisco Talos can be used to investigate:

-   IP addresses
-   Domains
-   Networks
-   File hashes

The result can provide reputation information that helps determine
whether an indicator has been associated with malicious activity.

------------------------------------------------------------------------

# Task 4 --- Email Body Analysis

After analyzing the headers, I move to the body.

This is often where the phishing action is hidden.

The two major things I look for are:

``` text
Links
Attachments
```

------------------------------------------------------------------------

## Investigating Links Safely

Instead of clicking a link, I can right-click it and use:

``` text
Copy link address
```

Then I can analyze the copied URL separately.

This is much safer than opening the destination.

### Why this matters

A visible link might say:

``` text
Update Account
```

but the actual URL could lead somewhere completely unrelated.

------------------------------------------------------------------------

# URL Extraction

If an email contains many links, manually checking every link can be
time-consuming.

The room demonstrates URL extraction tools and CyberChef.

The general workflow is:

``` text
Raw email/source
       |
       v
Extract URLs
       |
       v
Review each URL
       |
       v
Expand/analyze redirects
       |
       v
Check reputation
```

------------------------------------------------------------------------

# Attachment Analysis

Attachments should **not** be downloaded and opened casually.

I should first move the investigation into a controlled environment such
as:

-   TryHackMe lab
-   Sandbox
-   Isolated VM

Once the file is safely obtained, I can calculate its SHA256 hash.

Example:

``` bash
sha256sum shady_attachment.pdf
```

Example output from the room:

``` text
025ba9ce4a2118a9ca7b115c8869ff73bc16bad3732ba359cef1e60ad8f961f9  shady_attachment.pdf
```

The hash can then be searched in reputation services.

------------------------------------------------------------------------

# VirusTotal

VirusTotal can be used to investigate:

-   File hashes
-   Files
-   URLs
-   IP addresses
-   Domains

It aggregates detections from many security vendors.

A useful workflow is:

``` text
Suspicious attachment
        |
        v
Calculate SHA256
        |
        v
Search hash in VirusTotal
        |
        v
Review vendor detections
        |
        v
Look for related IOCs
```

------------------------------------------------------------------------

# Task 5 --- Malware Sandboxes

Sometimes a hash or reputation lookup is not enough.

I may need to understand **what the file actually does**.

This is where malware sandboxes are useful.

A sandbox executes the suspicious file in an isolated environment and
records its behavior.

I can look for:

-   Processes
-   Network connections
-   DNS requests
-   Files created
-   Registry changes
-   URLs contacted
-   Downloaded payloads
-   Indicators of compromise

------------------------------------------------------------------------

## ANY.RUN

**ANY.RUN** is an interactive malware-analysis sandbox.

It allows an analyst to observe suspicious files or URLs while they
execute in a controlled environment.

Things I can investigate include:

``` text
File
 ↓
Processes
 ↓
Network connections
 ↓
DNS
 ↓
Files/registry
 ↓
Threat indicators
```

The interactive nature is useful because I can follow the behavior while
the sample is running.

------------------------------------------------------------------------

## Hybrid Analysis

Hybrid Analysis is another sandboxing platform.

It can provide information about:

-   Process behavior
-   Network activity
-   System changes
-   Indicators of compromise
-   Threat classification

------------------------------------------------------------------------

## Joe Sandbox

Joe Sandbox performs static and dynamic malware analysis.

It can generate detailed reports containing:

-   Behavior
-   Network activity
-   IOCs
-   Threat classifications

------------------------------------------------------------------------

# Task 6 --- Using PhishTool

PhishTool is designed specifically for phishing investigations.

Instead of manually jumping between multiple places, it can bring
several useful artifacts together.

When an email is uploaded, I can inspect:

-   Rendered HTML
-   Raw HTML
-   Message source
-   Authentication results
-   Transmission information
-   URLs
-   Attachments
-   Threat-intelligence results

------------------------------------------------------------------------

## Why PhishTool Is Useful

A phishing investigation can involve many different artifacts.

PhishTool helps organize them into one investigation.

``` text
Email
  |
  +--> Headers
  |
  +--> Authentication
  |
  +--> Transmission
  |
  +--> URLs
  |
  +--> Attachments
  |
  +--> Threat Intelligence
```

The room also demonstrates VirusTotal integration.

------------------------------------------------------------------------

# Resolving a Case

After completing the investigation, I can document the findings.

The case can be marked as malicious and important artifacts can be
flagged.

Typical findings may include:

-   Sender address
-   Sender IP
-   Suspicious domains
-   URLs
-   Attachment hashes
-   Malware behavior

This is similar to how a SOC analyst would document and close a phishing
investigation.

------------------------------------------------------------------------

# Task 7 --- Your Account Is on Hold

This was my first hands-on phishing case in the room.

I had to act as a **Level 1 SOC analyst** and investigate the file:

``` text
Phish3Case1.eml
```

The email is designed to impersonate a reputable brand.

------------------------------------------------------------------------

## Question 7.1

### What reputable brand is this email tailored to impersonate?

**Answer: `Netflix`**

### How I Got It

I inspected the email's visual branding and message content.

The email was designed to look like a Netflix account/billing message.

The screenshot also shows that **Netflix** was accepted by TryHackMe.

``` text
Email branding
      ↓
Netflix-style billing/account message
      ↓
Impersonation target = Netflix
```

------------------------------------------------------------------------

## Question 7.2

### Based on the email headers, who is the intended recipient?

**Lab answer:**

``` text
redacted@yahoo.com
```

### How I Got It

I checked the recipient information in the email headers.

The relevant recipient field identifies the target mailbox.

For the public version of this README, I am intentionally keeping the
address redacted because it is not necessary to expose a real-looking
email address.

``` text
Header
  ↓
To / recipient field
  ↓
Intended recipient
```

------------------------------------------------------------------------

## Question 7.3

### What is the `Received: from` IP address?

**Lab answer:**

``` text
10.197.37.234
```

### Public-safe version

``` text
10[.]197[.]37[.]234
```

### How I Got It

I opened the email source in Thunderbird:

``` text
View → Message Source
```

Then I searched for the:

``` text
Received: from
```

header.

The IP address following this field was:

``` text
10.197.37.234
```

This is why raw email source is important: the normal email view may not
expose the full routing information.

------------------------------------------------------------------------

## Question 7.4

### What domain of interest is found in the `Return-Path` field?

**Lab answer:**

``` text
etekno.xyz
```

### Public-safe version

``` text
etekno[.]xyz
```

### How I Got It

I searched the message source for:

``` text
Return-Path
```

The domain associated with that field was:

``` text
etekno.xyz
```

This is suspicious because the email is supposed to represent Netflix,
but the Return-Path domain does not match Netflix.

That mismatch is a useful phishing indicator.

------------------------------------------------------------------------

## Question 7.5

### What is the shortened URL behind the `UPDATE ACCOUNT NOW` button?

**Lab answer:**

``` text
https://t.co/yuxfZm8KPg?amp=1
```

### Public-safe version

``` text
hxxps[://]t[.]co/yuxfZm8KPg?amp=1
```

### How I Got It

I investigated the HTML/source behind the:

``` text
UPDATE ACCOUNT NOW
```

button.

Instead of trusting the visible button text, I checked the actual
hyperlink.

The link used the `t.co` URL-shortening service.

This means the visible button did not reveal the final destination.

### Important lesson

``` text
Visible button
      ↓
Shortened URL
      ↓
Hidden destination
```

I should investigate the redirect chain safely rather than clicking the
URL directly.

------------------------------------------------------------------------

# Task 8 --- Update Payment Details

This case uses **ANY.RUN** to investigate a suspicious PDF attachment
from a phishing email.

The sample is designed to impersonate Netflix and appears to be related
to payment/account information.

------------------------------------------------------------------------

## Question 8.1

### How does ANY.RUN classify this suspected phishing email?

**Answer:**

``` text
Suspicious activity
```

### How I Got It

I checked the classification shown in the ANY.RUN analysis.

The TryHackMe screenshot confirms that:

``` text
Suspicious activity
```

was accepted.

------------------------------------------------------------------------

# Question 8.2

### What is the name of the PDF attachment?

**Answer:**

``` text
Payment-updateid.pdf
```

### How I Got It

I inspected the file information in the ANY.RUN analysis.

The filename shown for the attachment is:

``` text
Payment-updateid.pdf
```

The public ANY.RUN report also identifies the file as
`Payment-updateid.pdf`. citeturn1search5

------------------------------------------------------------------------

# Question 8.3

### What is the SHA256 hash of the PDF?

**Answer:**

``` text
cc6f1a04b10bcb168aeec8d870b97bd7c20fc161e8310b5bce1af8ed420e2c24
```

### How I Got It

I opened the file information in ANY.RUN and looked for the SHA256
field.

The hash matched:

``` text
CC6F1A04B10BCB168AEEC8D870B97BD7C20FC161E8310B5BCE1AF8ED420E2C24
```

ANY.RUN's report independently shows the same SHA256 value.
citeturn1search5turn1search11

### Why the hash is useful

The hash gives me a stable identifier for the attachment.

I can use it to search:

-   VirusTotal
-   ANY.RUN
-   Threat-intelligence platforms
-   Internal security tools

without repeatedly uploading or executing the file.

------------------------------------------------------------------------

# Question 8.4

### Which IP address associated with `AcroRd32.exe` is flagged as malicious?

**Answer accepted by my TryHackMe lab:**

``` text
2.16.107.24
```

### Public-safe version

``` text
2[.]16[.]107[.]24
```

### How I Got It

I opened the ANY.RUN text report and checked the network connections
associated with:

``` text
AcroRd32.exe
```

The connection to:

``` text
2.16.107.24
```

was marked malicious.

The public ANY.RUN report also shows `AcroRd32.exe` connecting to
`2.16.107.24`, with the connection classified as malicious.
citeturn0search0turn0search4

### Note about walkthrough differences

Some older walkthroughs for this room report **two** malicious IPs,
including `2.16.107.83`, while the question shown in my screenshot asks
for the IP associated with `AcroRd32.exe` and accepts `2.16.107.24`.

For my documentation, I am recording the **answer accepted by my
TryHackMe attempt**.

------------------------------------------------------------------------

# Question 8.5

### Which Windows process is classed as `Potentially Bad Traffic`?

**Answer:**

``` text
svchost.exe
```

### How I Got It

I continued down the ANY.RUN text report and checked the **Threats**
section.

The process associated with the `Potentially Bad Traffic` classification
was:

``` text
svchost.exe
```

The important lesson is that the process name alone does not
automatically mean malicious activity.

`svchost.exe` is a legitimate Windows process, so I need to examine:

-   Which service started it
-   Parent process
-   Network connections
-   Command line
-   Destination IP/domain
-   Timing
-   Other correlated indicators

This is an important SOC-analysis mindset.

------------------------------------------------------------------------

# Task 9 --- Excel Executable

This case uses another ANY.RUN analysis, this time involving an Excel
attachment.

The attachment is classified as malicious and attempts to exploit a
known Microsoft Office vulnerability.

------------------------------------------------------------------------

# Question 9.1

### How does ANY.RUN classify the `.xlsx` attachment?

**Answer:**

``` text
Malicious activity
```

### How I Got It

I checked the verdict/classification shown in the ANY.RUN analysis.

The TryHackMe screenshot confirms:

``` text
Malicious activity
```

was accepted.

The ANY.RUN report for the sample also identifies the analysis as
**Malicious activity** and records two threats. citeturn1search2

------------------------------------------------------------------------

# Question 9.2

### What is the filename of the Excel attachment?

**Answer:**

``` text
CBJ200620039539.xlsx
```

### How I Got It

I checked the file information in the ANY.RUN analysis.

The exact filename is:

``` text
CBJ200620039539.xlsx
```

The public ANY.RUN report uses the same filename. citeturn1search2

------------------------------------------------------------------------

# Question 9.3

### What is the SHA256 hash?

**Answer:**

``` text
5f94a66e0ce78d17afc2dd27fc17b44b3ffc13ac5f42d3ad6a5dcfb36715f3eb
```

### How I Got It

I inspected the file information in ANY.RUN and copied the SHA256 value.

The hash also appears in the public ANY.RUN report for this sample.
citeturn1search2

------------------------------------------------------------------------

# Question 9.4

### What IP address is associated with the malicious domain `biz9holdings.com`?

**Answer:**

``` text
204.11.56.48
```

### Public-safe version

``` text
204[.]11[.]56[.]48
```

### How I Got It

I checked the **HTTP requests / network activity** in the ANY.RUN
report.

The report shows:

``` text
biz9holdings.com
        ↓
204.11.56.48
```

The connection is associated with `EQNEDT32.EXE` and is classified as
malicious. citeturn1search2

------------------------------------------------------------------------

# Question 9.5

### Which other domain is classified as malicious?

**Answer:**

``` text
findresults.site
```

### Public-safe version

``` text
findresults[.]site
```

### How I Got It

I checked the other malicious network requests in the ANY.RUN report.

The report shows:

``` text
findresults.site
```

and marks its HTTP activity as malicious. citeturn1search2

The domain also appears in older security reporting as a malware-related
domain, which provides additional context for why it is considered
suspicious. citeturn1search28

------------------------------------------------------------------------

# Question 9.6

### What vulnerability does this malicious attachment attempt to exploit?

**Answer:**

``` text
CVE-2017-11882
```

### How I Got It

The attachment uses Microsoft Office's legacy **Equation Editor**
component.

The ANY.RUN report shows the process:

``` text
EQNEDT32.EXE
```

making malicious network requests.

This is strongly associated with exploitation of **CVE-2017-11882**, a
known Microsoft Office Equation Editor vulnerability that can allow code
execution through a specially crafted document.

The room's accepted answer is:

``` text
CVE-2017-11882
```

The ANY.RUN report shows `EQNEDT32.EXE` making the malicious requests
and the related sample analysis. citeturn1search2

------------------------------------------------------------------------

# Understanding the Excel Attack Chain

This case is especially useful because I can see the attack moving
through several stages.

``` text
Phishing Email
      |
      v
Malicious Excel Attachment
      |
      v
Office / Equation Editor
      |
      v
EQNEDT32.EXE
      |
      v
CVE-2017-11882 Exploitation
      |
      v
Malicious Network Request
      |
      +----> findresults[.]site
      |
      +----> biz9holdings[.]com
      |
      v
Additional Payload
```

The ANY.RUN report shows `EQNEDT32.EXE` making HTTP requests to the
malicious infrastructure and identifies the relevant threat activity.
citeturn1search2

------------------------------------------------------------------------

# Complete Answer Sheet

## Task 7 --- Your Account Is on Hold

  Question                       Answer
  ------------------------------ ---------------------------------
  Reputable brand impersonated   `Netflix`
  Intended recipient             `redacted@yahoo.com`
  `Received: from` IP            `10.197.37.234`
  Return-Path domain             `etekno.xyz`
  Shortened URL                  `https://t.co/yuxfZm8KPg?amp=1`

**Public-safe IOCs:**

``` text
10[.]197[.]37[.]234
etekno[.]xyz
hxxps[://]t[.]co/yuxfZm8KPg?amp=1
```

------------------------------------------------------------------------

## Task 8 --- Update Payment Details

  --------------------------------------------------------------------------------------------------------
  Question                            Answer
  ----------------------------------- --------------------------------------------------------------------
  ANY.RUN classification              `Suspicious activity`

  PDF filename                        `Payment-updateid.pdf`

  SHA256                              `cc6f1a04b10bcb168aeec8d870b97bd7c20fc161e8310b5bce1af8ed420e2c24`

  Malicious IP associated with        `2.16.107.24`
  `AcroRd32.exe`                      

  Potentially Bad Traffic process     `svchost.exe`
  --------------------------------------------------------------------------------------------------------

**Public-safe IP:**

``` text
2[.]16[.]107[.]24
```

------------------------------------------------------------------------

## Task 9 --- Excel Executable

  --------------------------------------------------------------------------------------------------------
  Question                            Answer
  ----------------------------------- --------------------------------------------------------------------
  ANY.RUN classification              `Malicious activity`

  Excel filename                      `CBJ200620039539.xlsx`

  SHA256                              `5f94a66e0ce78d17afc2dd27fc17b44b3ffc13ac5f42d3ad6a5dcfb36715f3eb`

  `biz9holdings.com` IP               `204.11.56.48`

  Other malicious domain              `findresults.site`

  Vulnerability                       `CVE-2017-11882`
  --------------------------------------------------------------------------------------------------------

**Public-safe IOCs:**

``` text
204[.]11[.]56[.]48
findresults[.]site
```

------------------------------------------------------------------------

# How I Would Investigate a Phishing Email as a SOC Analyst

After completing this room, my investigation process looks like this:

``` text
                 Suspicious Email
                        |
                        v
                1. Preserve Evidence
                        |
                        v
                2. Analyze Headers
                        |
             +----------+----------+
             |                     |
             v                     v
         Sender IP            Recipient
             |
             v
       Return-Path
             |
             v
          Reply-To
                        |
                        v
                3. Analyze Body
                        |
             +----------+----------+
             |                     |
             v                     v
           URLs              Attachments
             |                     |
             v                     v
        URL Analysis          SHA256 Hash
             |                     |
             v                     v
      Reputation Check       Reputation Check
             |                     |
             +----------+----------+
                        |
                        v
                 4. Sandbox
                        |
                        v
                 5. Observe
                        |
             +----------+----------+
             |          |           |
             v          v           v
          Process     Network     Files
             |          |           |
             +----------+-----------+
                        |
                        v
                  6. Collect IOCs
                        |
                        v
                 7. Determine Verdict
                        |
                        v
                  8. Document Case
                        |
                        v
                     Resolve
```

------------------------------------------------------------------------

# Useful Commands

## Calculate SHA256

``` bash
sha256sum suspicious_file.pdf
```

## Extract URLs with CyberChef

Conceptually:

``` text
Email/source
   ↓
Extract URLs
   ↓
Review suspicious URLs
```

## Safe URL Investigation

Instead of opening a suspicious URL directly:

``` text
Copy link
   ↓
Defang it
   ↓
Analyze with URLScan / reputation tools
   ↓
Inspect redirects and behavior
```

------------------------------------------------------------------------

# Tools I Learned

  Tool                      Main Use
  ------------------------- --------------------------------------------------
  Google Messageheader      Email header/routing analysis
  Message Header Analyzer   Header investigation
  IPinfo                    IP information and organization
  URLScan.io                Safe URL/page investigation
  Cisco Talos               IP/domain/file reputation
  VirusTotal                Multi-vendor reputation
  ANY.RUN                   Interactive malware sandbox
  Hybrid Analysis           Malware sandbox
  Joe Sandbox               Static/dynamic malware analysis
  PhishTool                 Centralized phishing investigation
  CyberChef                 URL extraction/defanging and data transformation

------------------------------------------------------------------------

# Important SOC Lessons

## 1. Collect Before Concluding

I should not immediately decide that an email is malicious based only on
appearance.

First I should collect:

``` text
Headers
URLs
Domains
IP addresses
Attachments
Hashes
```

Then correlate the evidence.

------------------------------------------------------------------------

## 2. Sender Identity Can Be Forged

A display name such as:

``` text
Netflix
Apple Support
DHL Express
```

does not prove that the email originated from that company.

I need to inspect:

-   Actual sender
-   Domain
-   Return-Path
-   Reply-To
-   Received headers

------------------------------------------------------------------------

## 3. Don't Open Attachments on My Normal Machine

A suspicious attachment should be handled in:

``` text
Isolated VM
      or
Malware sandbox
```

This is especially important when the attachment is executable,
macro-enabled, or capable of exploiting a software vulnerability.

------------------------------------------------------------------------

## 4. A Hash Is an Excellent Investigation Pivot

Once I have:

``` text
SHA256
```

I can search that value across threat-intelligence platforms.

This can reveal:

-   Previous detections
-   Malware family
-   Related infrastructure
-   Sandbox reports
-   Other associated IOCs

------------------------------------------------------------------------

## 5. Process Names Need Context

A process such as:

``` text
svchost.exe
```

is a legitimate Windows process.

But if it appears in a suspicious context, I should investigate:

``` text
Parent process
Command line
Network connections
Destination
User context
Timing
Related processes
```

This prevents me from treating every legitimate Windows process as
malicious.

------------------------------------------------------------------------

## 6. Network Activity Can Reveal the Attack

The Excel case showed how network activity can reveal the attack
infrastructure.

``` text
EQNEDT32.EXE
      |
      +--> findresults[.]site
      |
      +--> biz9holdings[.]com
```

This is much more useful than simply saying:

> "The Excel file is malicious."

I can now identify the infrastructure associated with the activity.

------------------------------------------------------------------------

# Sanitization

For my public GitHub documentation, I should keep useful technical
evidence while avoiding unnecessary exposure.

### I kept

-   File hashes
-   Process names
-   CVE
-   Tool names
-   Analysis methods
-   Defanged IOCs
-   Lab answers

### I masked/defanged

-   Email addresses
-   IP addresses
-   Malicious domains
-   URLs
-   Other clickable indicators

### Why I keep hashes

Hashes such as SHA256 values are useful for identifying a file and
searching threat-intelligence databases. They do not directly execute
the file.

### Why I defang URLs/IPs

Instead of:

``` text
https://malicious.example/login
```

I document:

``` text
hxxps[://]malicious[.]example/login
```

And instead of:

``` text
192.0.2.10
```

I use:

``` text
192[.]0[.]2[.]10
```

This keeps the information useful without making it accidentally
clickable.

------------------------------------------------------------------------

# Final Takeaway

This room was an important step for me because I moved from
**recognizing phishing** to actually **investigating phishing
artifacts**.

The workflow I want to remember is:

``` text
Email
 ↓
Headers
 ↓
Artifacts
 ↓
URLs
 ↓
Attachments
 ↓
Hashes
 ↓
Reputation
 ↓
Sandbox
 ↓
Behavior
 ↓
IOCs
 ↓
Verdict
 ↓
Documentation
```

The biggest lesson for me is that a phishing investigation should be
**evidence-driven**.

I should not rely on:

-   How professional the email looks
-   Grammar alone
-   The display name
-   A familiar brand logo

Instead, I should correlate:

``` text
Header information
+
URL/domain reputation
+
Attachment hash
+
Process behavior
+
Network activity
+
Threat intelligence
```

That gives me a much stronger basis for deciding whether an email is
malicious and for producing useful findings for the rest of the SOC
team.

------------------------------------------------------------------------

