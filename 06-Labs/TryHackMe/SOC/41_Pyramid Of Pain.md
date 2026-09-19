# Pyramid of Pain --- TryHackMe

**Date:** 19 September 2026\
**Room:** Pyramid of Pain\
**Focus:** Understanding different types of Indicators of Compromise
(IOCs) and how difficult they are for an attacker to change.

------------------------------------------------------------------------

## What I Learned

The **Pyramid of Pain** shows different types of indicators that a
defender can detect.

As I move higher up the pyramid:

-   the indicators generally become more useful for detection
-   they become harder for an attacker to change
-   detecting higher-level indicators can force the attacker to change
    more of their operation

``` text
                 TTPs
              ───────────
                Tools
             ─────────────
          Network Artifacts
         ───────────────────
           Host Artifacts
        ─────────────────────
            Domain Names
       ───────────────────────
             IP Addresses
      ─────────────────────────
             Hash Values
```

The basic idea I took from the room is that lower-level indicators are
easier for an attacker to change, while higher-level indicators require
more effort to change.

------------------------------------------------------------------------

# Task 2 --- Hash Values

## What is a Hash?

A hash is a fixed-length value generated from data using a hashing
algorithm.

I can use a hash to identify a specific file. Security analysts commonly
use hashes to:

-   identify malware samples
-   search for known malicious files
-   reference suspicious files
-   investigate malware reports

The room covers three common hashing algorithms.

### MD5

MD5 produces a **128-bit** hash.

MD5 is no longer considered cryptographically secure because attacks
such as hash collisions are possible.

### SHA-1

SHA-1 produces a **160-bit** hash, normally represented as 40
hexadecimal characters.

SHA-1 has been deprecated for security-sensitive use.

### SHA-256

SHA-256 belongs to the SHA-2 family and produces a **256-bit** hash
represented as 64 hexadecimal characters.

------------------------------------------------------------------------

## Why Hashes Are Useful

If I know the hash of a malicious file, I can search for that exact hash
in threat-intelligence services such as VirusTotal and MetaDefender
Cloud.

The important limitation is that changing even a tiny part of a file can
produce a completely different hash.

------------------------------------------------------------------------

## Hash Modification Example

The room demonstrates this with PowerShell.

First, the original file hash was calculated:

``` powershell
Get-FileHash .\OpenVPN_2.5.1_I601_amd64.msi -Algorithm MD5
```

Original MD5:

``` text
D1A008E3A606F24590A02B853E955CF7
```

Then a string was appended:

``` powershell
echo "AppendTheHash" >> .\OpenVPN_2.5.1_I601_amd64.msi
```

The hash was calculated again:

``` powershell
Get-FileHash .\OpenVPN_2.5.1_I601_amd64.msi -Algorithm MD5
```

New MD5:

``` text
9D52B46F5DE41B73418F8E0DACEC5E9F
```

So I understood the basic problem with hash-based detection:

``` text
Same malware
      ↓
Small file modification
      ↓
Different hash
      ↓
Hash-based detection may no longer match
```

That is why hash values are at the bottom of the Pyramid of Pain. They
are useful, but relatively easy for an attacker to change.

------------------------------------------------------------------------

# Task 3 --- IP Addresses

An IP address identifies a device on a network.

From a defensive perspective, I can use a malicious IP address as an IOC
and block it using controls such as firewalls.

``` text
Malicious IP
     ↓
Firewall rule
     ↓
Block connection
```

However, this is not a perfect solution because an attacker can change
infrastructure and use a different public IP address.

## Fast Flux

The room introduces **Fast Flux**.

Fast Flux involves associating many changing IP addresses with a domain.

The purpose is to make malicious infrastructure more difficult to
discover and take down.

``` text
                Domain
                  |
       ┌──────────┼──────────┐
       ↓          ↓          ↓
      IP 1       IP 2       IP 3
       ↓          ↓          ↓
       changes over time
```

Fast Flux can be used to hide:

-   phishing infrastructure
-   malware delivery
-   proxy infrastructure
-   command-and-control communication

**Safety note:** the room specifically warns not to interact with the
malicious IP addresses shown in its examples.

------------------------------------------------------------------------

# Task 4 --- Domain Names

The next level is **Domain Names**.

A domain can look like:

``` text
evilcorp.com
```

or:

``` text
tryhackme.evilcorp.com
```

Domains are generally more difficult for an attacker to change than a
simple IP address because the attacker may need to:

1.  obtain/register a domain
2.  configure DNS
3.  modify DNS records
4.  move the malicious infrastructure

------------------------------------------------------------------------

## Punycode Attacks

The room explains **Punycode** attacks.

Punycode is a way of representing Unicode characters using
ASCII-compatible encoding.

The room's example uses:

``` text
adıdas.de
```

with the Punycode representation:

``` text
xn--addas-o4a.de
```

This can be abused to make a malicious domain look similar to a
legitimate website.

------------------------------------------------------------------------

## URL Shorteners

Attackers can also hide malicious domains behind URL-shortening
services.

Examples mentioned in the room include:

``` text
bit.ly
goo.gl
ow.ly
s.id
smarturl.it
tiny.pl
tinyurl.com
x.co
```

A shortened URL may hide the real destination.

The room explains that some shortened links can expose their destination
by adding:

``` text
+
```

to the URL.

The SOC lesson for me is that I should not automatically trust a
shortened URL just because the visible URL looks harmless.

------------------------------------------------------------------------

## Investigating Domains in Any.Run

Any.Run can show network activity produced when a sample is executed in
its sandbox.

### HTTP Requests

This shows HTTP requests made by the sample.

I can use this to identify:

-   downloaded resources
-   payloads
-   callbacks

### Connections

This shows communications made by the sample.

This can help identify:

-   C2 traffic
-   file transfers
-   connections to suspicious hosts

### DNS Requests

This shows DNS lookups made by the sample.

Malware may make DNS requests to:

-   locate infrastructure
-   communicate with C2
-   check whether internet access is available

I should never directly interact with suspicious IP addresses or URLs
found in malware reports.

------------------------------------------------------------------------

# Task 5 --- Host Artifacts

**Host artifacts** are traces left behind on a compromised system.

Examples include:

-   registry values
-   suspicious process execution
-   files created or modified
-   malicious applications
-   attack patterns
-   other system-level indicators

For example:

``` text
Microsoft Word
      ↓
Suspicious process
      ↓
Malicious application
      ↓
Files modified/dropped
```

If an attacker is detected because of a host artifact, they may have to
change more than just an IP address or file hash.

They may need to:

-   change the attack tool
-   change the execution method
-   modify dropped files
-   change persistence
-   change their overall approach

------------------------------------------------------------------------

# Task 6 --- Network Artifacts

Network artifacts are also in the **yellow section** of the Pyramid of
Pain.

A network artifact is something observable in network traffic.

Examples include:

-   User-Agent strings
-   C2 information
-   URI patterns
-   unusual HTTP POST requests
-   other suspicious network behaviour

## User-Agent

A **User-Agent** is part of an HTTP request and gives information about
the software making the request.

If malware uses an unusual User-Agent that is not normally seen in an
environment, it can become a useful detection indicator.

------------------------------------------------------------------------

## Detecting Network Artifacts with Wireshark/TShark

Network artifacts can be investigated using:

-   Wireshark
-   TShark
-   Snort
-   IDS alerts

The room gives this TShark example:

``` bash
tshark --Y http.request -T fields -e http.host -e http.user_agent -r analysis_file.pcap
```

This extracts the HTTP host and User-Agent from HTTP requests in a PCAP.

------------------------------------------------------------------------

# Task 7 --- Tools

At this level, the attacker has to deal with detection of the tools they
use.

Attackers may use tools to:

-   create malicious documents
-   create backdoors
-   establish C2
-   create custom EXE/DLL payloads
-   perform password cracking
-   deliver malware

Useful defensive detections include:

-   antivirus signatures
-   detection rules
-   YARA rules
-   malware feeds
-   fuzzy hashing

## MalwareBazaar and Malshare

The room mentions:

-   MalwareBazaar
-   Malshare

These resources can provide:

-   malware samples
-   malicious feeds
-   YARA-related information
-   threat-hunting data

## Detection Rules

The room also mentions the **SOC Prime Threat Detection Marketplace** as
a source for detection rules.

## Fuzzy Hashing

Normal hashing changes when a file is modified.

Fuzzy hashing allows **similarity analysis** between files.

One example is:

``` text
SSDeep
```

Conceptually:

``` text
Original malware
      ↓
Small modifications
      ↓
Different normal hash
      ↓
Fuzzy hash may still show similarity
```

This makes fuzzy hashing useful for malware analysis and threat hunting.

------------------------------------------------------------------------

# Task 8 --- TTPs

The top of the Pyramid of Pain is **TTPs**.

TTP stands for:

``` text
Tactics
Techniques
Procedures
```

TTPs describe how an attacker operates rather than only identifying one
file, IP, or tool.

The room connects this level with the **MITRE ATT&CK Matrix**.

An attack can involve many stages:

``` text
Phishing
   ↓
Initial Access
   ↓
Execution
   ↓
Persistence
   ↓
Privilege Escalation
   ↓
Lateral Movement
   ↓
Command and Control
   ↓
Exfiltration
```

If I detect the attacker's behaviour or technique instead of only
looking for one specific artifact, the detection can remain useful even
when the attacker changes:

-   malware
-   file hash
-   IP
-   domain
-   tool

## Example --- Pass-the-Hash

The room gives **Pass-the-Hash** as an example.

If I can detect Pass-the-Hash behaviour through Windows event monitoring
and respond to it, I may be able to identify a compromised host and stop
further lateral movement.

The main idea is:

``` text
Detect the artifact
        ↓
Detect the tool
        ↓
Detect the behaviour
        ↓
Detect the technique
```

------------------------------------------------------------------------

# My SOC Takeaway

The biggest thing I learned from the Pyramid of Pain is that **not every
IOC has the same defensive value**.

  Level              Example                                            Attacker effort to change
  ------------------ -------------------------------------------------- ---------------------------
  Hash               SHA-256 of malware                                 Trivial
  IP Address         C2 IP                                              Easy
  Domain             Malicious C2 domain                                More effort
  Host Artifact      Dropped file/process/persistence                   More annoying
  Network Artifact   User-Agent/URI/C2 pattern                          More annoying
  Tool               Specific malware/tool                              Challenging
  TTP                Pass-the-Hash / phishing / persistence technique   Tough

The exact usefulness of an indicator depends on the environment and
detection strategy. A hash can still be very useful for identifying a
known malware sample even though an attacker can modify the file.

------------------------------------------------------------------------

# How I Can Apply This in SOC Work

When investigating an alert, I should not stop after finding one IOC.

I can keep moving upward:

``` text
Hash
 ↓
What file is this?

IP
 ↓
What host is it communicating with?

Domain
 ↓
What infrastructure is behind it?

Host Artifact
 ↓
What happened on the endpoint?

Network Artifact
 ↓
What communication pattern was used?

Tool
 ↓
What malware/tool is involved?

TTP
 ↓
What technique is the attacker using?
```

This gives me a better picture of the incident.

This room connects directly with things I have already practiced:

-   Windows Event Logs
-   Linux logs
-   Wireshark
-   Snort
-   SIEM investigations
-   Threat Intelligence
-   Malware analysis
-   MITRE ATT&CK
-   IOC investigation

------------------------------------------------------------------------

# Quick Revision

``` text
Pyramid of Pain

1. Hash Values
   → Easy to change

2. IP Addresses
   → Can be blocked, but attackers can change infrastructure

3. Domain Names
   → More effort to replace

4. Host Artifacts
   → System traces such as files, registry and processes

5. Network Artifacts
   → User-Agent, URI patterns, C2 communication

6. Tools
   → Malware, backdoors, payload builders, password crackers

7. TTPs
   → Attacker tactics, techniques and procedures
   → Hardest level to change
```

## Main Lesson

The Pyramid of Pain helped me understand that SOC detection should not
depend only on simple IOCs such as hashes and IP addresses.

I can use those indicators for quick detection, but I should also try to
understand the **behaviour and techniques behind the attack**.

That gives me more context during an investigation and can make
detections more resilient when attackers change individual artifacts.
