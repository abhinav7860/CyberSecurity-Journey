# Invite Only --- TryHackMe

**Date:** 18 September 2026\
**Path:** SOC Level 1 → Threat Intelligence / Incident Response

## My objective

In this room I acted as a SOC analyst supporting an L3 analyst during an
incident-response investigation.

I was given two suspicious indicators:

``` text
Flagged IP:
101[.]99[.]76[.]120

Flagged SHA256:
5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f
```

The main tool provided by the room was:

``` text
TryDetectThis2.0
```

The goal was not just to identify one malicious file. I had to **pivot
from one IOC to another**, follow execution relationships, investigate
dropped files, connect the IP to a malware family, and finally use
Google and the original threat-research report to understand the larger
campaign.

The practical workflow I followed was:

``` text
Flagged SHA256
      ↓
TryDetectThis2.0
      ↓
File information
      ↓
Relations
      ↓
Execution parents
      ↓
Dropped files
      ↓
Second hash
      ↓
More dropped files
      ↓
Flagged IP
      ↓
Related files
      ↓
Malware family
      ↓
Google / original report
      ↓
Campaign TTPs
```

I used Medium walkthroughs to understand the intended navigation through
TryDetectThis2.0 and to cross-check the answers. I also checked the
original Check Point Research report because the room specifically asked
me to find the original report.
citeturn0search5turn0search6turn0search2

------------------------------------------------------------------------

# What this room is teaching

The important skill here is **pivoting**.

A SOC analyst often starts with one indicator:

``` text
Hash
```

But that hash can lead to:

``` text
File
 ↓
Parent process
 ↓
Dropped file
 ↓
Another hash
 ↓
IP
 ↓
Other related files
 ↓
Malware family
 ↓
Threat report
 ↓
Attack technique
```

This is how a single alert can become a much bigger threat-intelligence
picture.

------------------------------------------------------------------------

# Step 1 --- Start the Lab Machine

I first clicked:

``` text
Start Lab Machine
```

After the VM started, I opened the launcher on the desktop.

This launched:

``` text
TryDetectThis2.0
```

The room describes TryDetectThis2.0 as the threat-intelligence search
application I should use to investigate the supplied indicators.

------------------------------------------------------------------------

# Step 2 --- Search the flagged SHA256

The first major indicator was:

``` text
5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f
```

I copied this hash into TryDetectThis2.0.

The first thing I wanted to know was:

``` text
What file is this hash associated with?
```

The result showed:

``` text
syshelpers.exe
```

So the flagged SHA256 belongs to:

``` text
syshelpers.exe
```

### Why this matters

A SHA256 hash is a fingerprint of a file.

Instead of trusting a filename, I can search using the hash:

``` text
SHA256
   ↓
Exact file/sample
```

This is useful because malware can easily be renamed.

------------------------------------------------------------------------

# Question 1 --- File name

### Answer

``` text
syshelpers.exe
```

### How I found it

``` text
TryDetectThis2.0
      ↓
Search flagged SHA256
      ↓
File information
      ↓
syshelpers.exe
```

------------------------------------------------------------------------

# Step 3 --- Check the file type

I stayed on the information for the same hash and checked the file
properties.

The file type was:

``` text
Win32 EXE
```

This tells me that the sample is a Windows executable.

### Answer

``` text
Win32 EXE
```

------------------------------------------------------------------------

# Step 4 --- Open the Relations tab

This was one of the most important parts of the room.

I opened the:

``` text
Relations
```

section for the flagged hash.

The Relations tab lets me see connections around the file, such as:

``` text
Execution Parents
Dropped Files
Communication
Domains
IP addresses
Other related files
```

This is where the investigation changed from:

``` text
"What is this file?"
```

to:

``` text
"How did this file get executed and what did it do?"
```

------------------------------------------------------------------------

# Step 5 --- Find the execution parents

I looked at the:

``` text
Execution Parents
```

section.

The two parent processes appeared chronologically as:

``` text
361GJX7J
installer.exe
```

So the answer was:

``` text
361GJX7J,installer.exe
```

The Medium walkthroughs also show these two parents and recommend saving
their hashes because the next questions require pivoting into the second
parent. citeturn0search5turn0search6

## Hashes I saved for later

I noted the hashes:

``` text
361GJX7J
047c5eec0445746862710d20e50a5dd04510b7e625fa5c1f5d48ce078001c0de
```

and:

``` text
installer.exe
fa102d4e3cfbe85f5189da70a52c1d266925f3efd122091cdc8fe0fc39033942
```

### Why I needed these

The room was deliberately making me follow the chain.

The important parent was:

``` text
installer.exe
```

I needed its hash for the next investigation.

------------------------------------------------------------------------

# Question 3 --- Execution parents

### Answer

``` text
361GJX7J,installer.exe
```

### Investigation path

``` text
Flagged SHA256
      ↓
syshelpers.exe
      ↓
Relations
      ↓
Execution Parents
      ↓
361GJX7J
      ↓
installer.exe
```

------------------------------------------------------------------------

# Step 6 --- Find the dropped file

While investigating the relations of `syshelpers.exe`, I checked the:

``` text
Dropped Files
```

section.

The file being dropped was:

``` text
AClient.exe
```

I also saved its hash for later reference:

``` text
dd02c105809e4ca41a5489e585ba025eddb89a91703b73a566c9903e6406a08c
```

### Why this matters

A dropped file is another IOC.

The original suspicious file was:

``` text
syshelpers.exe
```

but after execution another executable appeared:

``` text
AClient.exe
```

That means the investigation is becoming a **multi-stage execution
chain**.

------------------------------------------------------------------------

# Question 4 --- Dropped file

### Answer

``` text
AClient.exe
```

### Investigation path

``` text
syshelpers.exe
      ↓
Relations
      ↓
Dropped Files
      ↓
AClient.exe
      ↓
Save its hash
```

------------------------------------------------------------------------

# Step 7 --- Investigate installer.exe

The next clue came from Question 3.

I had already saved:

``` text
installer.exe
```

hash:

``` text
fa102d4e3cfbe85f5189da70a52c1d266925f3efd122091cdc8fe0fc39033942
```

I searched this second hash in TryDetectThis2.0.

This gave me another set of relationships.

I looked at the dropped files.

The tool showed several dropped files, but I only needed the malicious
ones.

The four malicious files appeared in this order:

``` text
searchhost.exe
syshelpers.exe
nat.vbs
runsys.vbs
```

------------------------------------------------------------------------

# Question 5 --- Four malicious dropped files

### Answer

``` text
searchhost.exe,syshelpers.exe,nat.vbs,runsys.vbs
```

### How I found them

``` text
installer.exe hash
       ↓
TryDetectThis2.0
       ↓
Relations
       ↓
Dropped Files
       ↓
Identify malicious/red-marked files
       ↓
Read from top to bottom
```

I had to preserve the order because the question specifically asked for
the files in the order they appeared.

The Medium walkthrough also confirms these four files.
citeturn0search5turn0search11

------------------------------------------------------------------------

# Why the execution chain matters

At this point I could draw the investigation like this:

``` text
361GJX7J
    ↓
installer.exe
    ↓
syshelpers.exe
    ↓
AClient.exe
```

And the installer also dropped:

``` text
searchhost.exe
syshelpers.exe
nat.vbs
runsys.vbs
```

This tells me that this is not simply:

``` text
One malicious file
```

It is a **multi-stage payload chain**.

------------------------------------------------------------------------

# Step 8 --- Investigate the flagged IP

The second major IOC supplied by the room was:

``` text
101[.]99[.]76[.]120
```

I searched this IP in the threat-intelligence application.

The goal was to see which files and malware were associated with this
infrastructure.

The relations showed multiple files communicating with or associated
with the IP.

I compared the related files and looked at their malware information.

The family connecting the files was:

``` text
AsyncRAT
```

------------------------------------------------------------------------

# Question 6 --- Malware family

### Answer

``` text
asyncrat
```

### How I got it

``` text
Flagged IP
101.99.76.120
       ↓
TryDetectThis2.0
       ↓
Related / communication files
       ↓
Check file information
       ↓
Common malware family
       ↓
AsyncRAT
```

A few walkthroughs explain the same pivot: search the flagged IP,
inspect related/communication files, and use the malware
information/comments to identify the family.
citeturn0search11turn0search12

------------------------------------------------------------------------

# What is AsyncRAT?

AsyncRAT is a **Remote Access Trojan (RAT)**.

A RAT is malware that can provide an attacker with remote control or
surveillance capabilities on a compromised machine.

Depending on the sample and configuration, a RAT may be able to perform
actions such as:

-   Execute commands
-   Manipulate files
-   Collect information
-   Capture keystrokes
-   Access system resources
-   Communicate with a command-and-control server

For this room, the important point is not to memorise every capability.

The important SOC lesson is:

``` text
IP
 ↓
Related files
 ↓
Common malware family
 ↓
AsyncRAT
```

Now the IP has much more context.

------------------------------------------------------------------------

# Step 9 --- Search for the original report

The room then asked me to find the **original report** where these
indicators were mentioned.

I could see references to the campaign from the threat-intelligence
information.

Instead of stopping at the name of the malware, I searched Google for:

``` text
101.99.76.120
```

and related indicators such as:

``` text
5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f
AsyncRAT Discord
```

The search led me to the original Check Point Research report.

The title is:

``` text
From Trust to Threat: Hijacked Discord Invites Used for Multi-Stage Malware Delivery
```

Check Point Research published the report on June 12, 2025 and describes
a campaign abusing expired/released Discord invite links to redirect
users to malicious servers. citeturn1view0

------------------------------------------------------------------------

# Question 7 --- Original report

### Answer

``` text
From Trust to Threat: Hijacked Discord Invites Used for Multi-Stage Malware Delivery
```

### How I found it

``` text
Flagged IP / IOC
      ↓
Google
      ↓
Threat reports / references
      ↓
Check Point Research
      ↓
Original report
```

The report was especially useful because the remaining questions were
about the actual attack campaign.

------------------------------------------------------------------------

# Step 10 --- Read the report for Chrome cookie theft

Now I moved from the TryDetectThis2.0 application to the original
research report.

I used the browser's:

``` text
Ctrl + F
```

and searched for:

``` text
cookie
```

The report discussed attackers bypassing Chrome's App Bound Encryption
using an adapted tool called:

``` text
ChromeKatz
```

The purpose was to steal cookies from Chromium-based browsers.

The report and independent summaries of it identify ChromeKatz as the
cookie-stealing tool. citeturn2search1turn2search0

------------------------------------------------------------------------

# Question 8 --- Cookie theft tool

### Answer

``` text
ChromeKatz
```

### How I found it

``` text
Original Check Point report
        ↓
Ctrl + F
        ↓
Search "cookie"
        ↓
ChromeKatz
```

------------------------------------------------------------------------

# What is ChromeKatz?

ChromeKatz is an adapted credential/cookie-stealing tool discussed in
the campaign.

The important SOC concept is:

``` text
Browser cookies
      ↓
Can represent authenticated sessions
      ↓
Stealing them can allow session abuse
```

That is why browser-cookie theft is important during incident response.

------------------------------------------------------------------------

# Step 11 --- Find the phishing technique

The next question asked which phishing technique the attackers used.

Again, I stayed in the original Check Point report.

I used:

``` text
Ctrl + F
```

and searched:

``` text
phishing
```

The report described the use of:

``` text
ClickFix
```

The campaign used a fake verification/CAPTCHA-style page to convince the
victim to perform an action that ultimately led to malicious command
execution.

Check Point reporting and other independent summaries identify this as
**ClickFix phishing**. citeturn2search0turn2search11

------------------------------------------------------------------------

# Question 9 --- Phishing technique

### Answer

``` text
ClickFix
```

### How I found it

``` text
Check Point report
      ↓
Ctrl + F
      ↓
Search "phishing"
      ↓
ClickFix
```

------------------------------------------------------------------------

# What is ClickFix?

ClickFix is a social-engineering technique where a fake page convinces
the victim that something needs to be "fixed" or verified.

The page can make the victim perform an action such as:

``` text
Copy something
      ↓
Open a system utility
      ↓
Paste it
      ↓
Run it
```

The important SOC lesson is that the user is being manipulated into
helping execute the attack.

In this campaign, the fake verification flow was associated with a
Discord-themed experience and manual command execution.
citeturn2search11

------------------------------------------------------------------------

# Step 12 --- Identify the redirect platform

The final question asked:

> What platform was used to redirect a user to malicious servers?

I already knew from the report title:

``` text
Hijacked Discord Invites
```

I searched the report for:

``` text
Discord
```

The campaign abused expired/released Discord invite links to redirect
users toward attacker-controlled servers.

The answer was:

``` text
Discord
```

Check Point Research explicitly describes the campaign as exploiting
expired and released Discord invite links to redirect users to malicious
servers. citeturn1view0

------------------------------------------------------------------------

# Question 10 --- Redirect platform

### Answer

``` text
Discord
```

### How I found it

``` text
Google
 ↓
Check Point Research report
 ↓
Discord invite abuse
 ↓
Malicious server redirection
 ↓
Discord
```

------------------------------------------------------------------------

# Complete Investigation Chain

After finishing the room, I could connect everything together.

``` text
Flagged SHA256
5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f
        ↓
TryDetectThis2.0
        ↓
syshelpers.exe
        ↓
Win32 EXE
        ↓
Execution Parents
        ↓
361GJX7J
        ↓
installer.exe
        ↓
Dropped File
        ↓
AClient.exe
```

Then I pivoted into the second parent:

``` text
installer.exe
        ↓
Dropped Files
        ↓
searchhost.exe
syshelpers.exe
nat.vbs
runsys.vbs
```

Then I investigated the other IOC:

``` text
Flagged IP
101.99.76.120
        ↓
Related Files
        ↓
AsyncRAT
```

Then I pivoted from the indicators to open-source intelligence:

``` text
IOC
 ↓
Google
 ↓
Check Point Research
 ↓
Original campaign report
```

And finally:

``` text
Discord
   ↓
Hijacked invite
   ↓
Malicious server
   ↓
ClickFix phishing
   ↓
Multi-stage malware
   ↓
AsyncRAT
   ↓
ChromeKatz
   ↓
Cookie theft
```

This is the main CTI lesson from the room.

------------------------------------------------------------------------

# Understanding the Attack Story

The individual answers make much more sense when I put them into one
story.

## 1. Initial trust

The attacker abused:

``` text
Discord invite links
```

The link could appear trustworthy because Discord is a legitimate and
familiar platform.

## 2. Redirect

The victim was redirected to an attacker-controlled server.

## 3. Fake verification

The attacker used a fake verification/CAPTCHA-style page.

## 4. ClickFix

The victim was manipulated into performing an action that helped execute
the attack.

## 5. Multi-stage payload

The malware did not necessarily arrive as one obvious final payload.

Instead, the investigation showed a chain involving:

``` text
installer.exe
      ↓
syshelpers.exe
      ↓
AClient.exe
```

and other dropped files such as:

``` text
searchhost.exe
nat.vbs
runsys.vbs
```

## 6. AsyncRAT

One of the important malware families associated with the infrastructure
was:

``` text
AsyncRAT
```

## 7. Credential/session theft

The campaign also used:

``` text
ChromeKatz
```

to target browser cookies.

------------------------------------------------------------------------

# Important Concepts I Learned

## Hash pivoting

A hash is one of the best starting points for identifying an exact file.

``` text
SHA256
  ↓
File
  ↓
Relations
```

------------------------------------------------------------------------

## Execution parents

Execution parents answer:

> What process launched this file?

For example:

``` text
Parent
  ↓
Child
```

Knowing the parent helps me understand the infection chain.

------------------------------------------------------------------------

## Dropped files

If malware creates another executable or script, that new file becomes
another IOC.

Example:

``` text
installer.exe
      ↓
AClient.exe
```

I can take the new file's hash and investigate it separately.

------------------------------------------------------------------------

## Relations

The Relations tab is extremely useful because it lets me pivot between
indicators.

I can move from:

``` text
File
 ↓
IP
 ↓
Domain
 ↓
Parent
 ↓
Dropped File
```

This is exactly the type of pivoting I should become comfortable with as
a SOC analyst.

------------------------------------------------------------------------

## Malware family attribution

I did not decide the malware family from the filename.

Instead:

``` text
IP
 ↓
Related files
 ↓
Threat-intelligence information
 ↓
Common family
 ↓
AsyncRAT
```

That is much stronger than simply guessing from a filename.

------------------------------------------------------------------------

## OSINT / Google pivoting

When a threat-intelligence platform gives me an IOC, I can search the
IOC on the public internet.

For example:

``` text
101.99.76.120
```

or:

``` text
5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f
```

This can lead me to:

-   Threat reports
-   Research blogs
-   Vendor reports
-   Malware analysis
-   Other IOCs
-   Campaign information

------------------------------------------------------------------------

# All Answers

  ----------------------------------------------------------------------------------------------------------------------------
  Question                            Answer
  ----------------------------------- ----------------------------------------------------------------------------------------
  1\. File identified by SHA256       `syshelpers.exe`

  2\. File type                       `Win32 EXE`

  3\. Execution parents               `361GJX7J,installer.exe`

  4\. Dropped file                    `AClient.exe`

  5\. Four malicious dropped files    `searchhost.exe,syshelpers.exe,nat.vbs,runsys.vbs`

  6\. Malware family                  `asyncrat`

  7\. Original report                 `From Trust to Threat: Hijacked Discord Invites Used for Multi-Stage Malware Delivery`

  8\. Chrome cookie-stealing tool     `ChromeKatz`

  9\. Phishing technique              `ClickFix`

  10\. Redirect platform              `Discord`
  ----------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Hashes I Saved During the Investigation

These were useful pivots during the investigation:

### Flagged SHA256

``` text
5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f
```

### 361GJX7J

``` text
047c5eec0445746862710d20e50a5dd04510b7e625fa5c1f5d48ce078001c0de
```

### installer.exe

``` text
fa102d4e3cfbe85f5189da70a52c1d266925f3efd122091cdc8fe0fc39033942
```

### AClient.exe

``` text
dd02c105809e4ca41a5489e585ba025eddb89a91703b73a566c9903e6406a08c
```

### Flagged IP

``` text
101[.]99[.]76[.]120
```

------------------------------------------------------------------------

# My SOC Investigation Method

This room gave me a good practical method for future threat-intelligence
investigations.

When I receive a suspicious hash:

``` text
1. Search the hash
       ↓
2. Identify the file
       ↓
3. Check file type
       ↓
4. Open Relations
       ↓
5. Check execution parents
       ↓
6. Save parent hashes
       ↓
7. Check dropped files
       ↓
8. Save important hashes
       ↓
9. Investigate each important hash
       ↓
10. Pivot to IPs/domains
       ↓
11. Identify malware family
       ↓
12. Search the IOC on Google
       ↓
13. Find the original threat report
       ↓
14. Extract campaign TTPs
       ↓
15. Build the final threat picture
```

------------------------------------------------------------------------

# My Takeaway

The biggest thing I learned from this room is that **threat intelligence
is about connecting the dots**.

I started with only:

``` text
One SHA256
+
One IP
```

But by pivoting through the intelligence platform, I found:

``` text
syshelpers.exe
      ↓
Execution parents
      ↓
installer.exe
      ↓
AClient.exe
      ↓
searchhost.exe
syshelpers.exe
nat.vbs
runsys.vbs
      ↓
AsyncRAT
      ↓
Check Point Research report
      ↓
Discord
      ↓
ClickFix
      ↓
ChromeKatz
```

So I am not just saying:

> "This hash is malicious."

I can now explain:

> **What the file is, how it was executed, what it dropped, what malware
> family it belongs to, what campaign it is connected to, how the victim
> was targeted, and what the attackers were trying to achieve.**

That is the kind of **L1 → L3 escalation support** this room was trying
to teach me.

------------------------------------------------------------------------

