# IP and Domain Threat Intel --- TryHackMe

**Date:** 18 September 2026\
**Path:** SOC Level 1 → IP and Domain Threat Intel

## What I learned

This room taught me how to investigate **IP addresses and domains** as a
SOC L1 analyst.

The main workflow is:

``` text
Verify
  ↓
Enrich
  ↓
Decide
```

When the alert contains a domain or IP, I should not immediately block
it.

I should first ask:

``` text
Who owns it?
Where is it hosted?
How old is it?
What does it resolve to?
What services are exposed?
Is it associated with malware or C2?
Is the IP a VPN / proxy / Tor node?
```

The room mainly taught me to use:

-   DNS / NSLookup
-   WHOIS / RDAP
-   VirusTotal
-   BGP.Tools
-   GeoIP
-   Shodan
-   Censys
-   TLS certificates
-   IP2Proxy
-   Spur

For the practical questions, I used the uploaded ZIP containing the
room's exported PDF reports and screenshots as the primary source. I
also cross-checked the practical workflow and answers against a Medium
walkthrough.

------------------------------------------------------------------------

# Task 2 --- Domain Enrichment

## What is DNS?

DNS stands for:

``` text
Domain Name System
```

DNS converts human-readable names into IP addresses.

For example:

``` text
tryhackme.com
      ↓
IP address
```

A computer needs the IP address to communicate with the server.

As a SOC analyst, DNS is useful because I can start with a domain and
pivot to:

``` text
Domain
  ↓
IP
  ↓
ASN
  ↓
Hosting provider
  ↓
Reputation
  ↓
Related infrastructure
```

------------------------------------------------------------------------

# A and AAAA Records

## A record

An **A record** maps a domain to an IPv4 address.

Example:

``` text
example.com → 192.0.2.10
```

## AAAA record

An **AAAA record** maps a domain to an IPv6 address.

So:

``` text
A    → IPv4
AAAA → IPv6
```

------------------------------------------------------------------------

# TXT Records

TXT records contain text information associated with a domain.

They can contain things such as:

-   SPF
-   DKIM-related information
-   Domain verification
-   Other service configuration

For a SOC analyst, TXT records can sometimes provide useful information
about the organisation and its email infrastructure.

------------------------------------------------------------------------

# WHOIS / RDAP

WHOIS/RDAP can tell me information such as:

-   Registrar
-   Creation date
-   Expiration date
-   Name servers
-   Registration status
-   Ownership/organisation information

One of the most useful pieces of information is **domain age**.

A newly created domain deserves more attention when it appears in a
suspicious alert.

However:

``` text
New domain ≠ automatically malicious
```

It is only one piece of evidence.

------------------------------------------------------------------------

# DNS Attack Techniques

## CDN abuse

Attackers can use legitimate CDNs such as Cloudflare to hide the real
origin server.

This means an IP belonging to Cloudflare does not automatically mean the
underlying domain is safe.

## Typosquatting

Attackers create domains that look similar to legitimate domains.

Example:

``` text
tryhackme.com
tryhakme.com
```

The second one is visually similar but different.

## IDN / Homograph attacks

Attackers can use characters from other alphabets that look similar to
normal characters.

The domain can look legitimate to a human while actually being
different.

Punycode can help identify these domains.

------------------------------------------------------------------------

# Task 2 --- SOC Practice

The suspicious domain was:

``` text
purematrixa[.]com
```

The room told me to use the attached PDF reports because live domain
information can change.

## Step 1 --- Check DNS

I opened:

``` text
Tasks → Task 2 → NSLookup.pdf
```

The report showed:

``` text
Cloudflare
```

as the DNS/CDN infrastructure.

The A records were also in Cloudflare's network:

``` text
188.114.96.0
188.114.97.0
```

So the answer to the CDN question was:

``` text
Cloudflare
```

### How I got it

``` text
purematrixa.com
      ↓
NSLookup report
      ↓
A records / Cloudflare infrastructure
      ↓
CDN = Cloudflare
```

## Step 2 --- Check WHOIS

I opened:

``` text
Tasks → Task 2 → WHOIS.pdf
```

The report showed:

``` text
Created on: 2026-05-31
```

It also explicitly showed:

``` text
1 days old
```

The alert scenario was on June 1, 2026.

Therefore:

``` text
Domain age = 1 days old
```

### Task 2 answers

``` text
CDN:
Cloudflare

Domain age:
1 days old
```

------------------------------------------------------------------------

# Task 3 --- IP Enrichment

## Why IP enrichment matters

An IP address by itself tells me very little.

It could be:

-   A home user
-   A cloud server
-   A CDN
-   A VPN
-   A compromised device
-   A malware C2 server
-   A legitimate company server

So I enrich it with several sources.

The room focuses on:

``` text
VirusTotal
AbuseIPDB
BGP.Tools
GeoIP
```

------------------------------------------------------------------------

# VirusTotal for IPs

VirusTotal can provide:

-   Reputation
-   Detection count
-   Community comments
-   Associated malware
-   C2 information
-   Related infrastructure

One important lesson is:

> I should not rely on one source alone.

I should correlate information.

------------------------------------------------------------------------

# Autonomous Systems

An **Autonomous System (AS)** is a collection of IP prefixes controlled
by one organisation.

Each AS has an:

``` text
ASN = Autonomous System Number
```

The ASN can give me context about the IP.

For example, an IP may belong to:

``` text
Residential ISP
Cloud provider
CDN
Server hosting company
VPN provider
```

This matters because the same malicious activity means different things
depending on where the IP is hosted.

------------------------------------------------------------------------

# GeoIP

GeoIP gives an approximate geographic location.

I can use it for questions such as:

``` text
Does this login location make sense?
```

For example:

``` text
User normally works in India
        ↓
Login suddenly appears from Europe
```

That deserves investigation.

But geolocation is not perfect.

A VPN or proxy can make the apparent location different from the user's
real location.

------------------------------------------------------------------------

# Task 3 --- SOC Practice

The suspicious IP was:

``` text
2[.]58[.]56[.]50
```

## Step 1 --- Check VirusTotal

I used the uploaded:

``` text
Tasks → Task 3 → VirusTotal.pdf
```

The report showed:

``` text
8 / 91 security vendors flagged this IP as malicious
```

More importantly, the community comments contained:

``` text
Remcos Found
C2: 2[.]58[.]56[.]50:2404
Country: The Netherlands
ASN: 1337 Services GmbH
```

So the C2 was:

``` text
Remcos
```

The country was:

``` text
Netherlands
```

### How I got the answers

``` text
2.58.56.50
      ↓
VirusTotal PDF
      ↓
Community comments
      ↓
Remcos C2
      ↓
Country = Netherlands
      ↓
ASN = 1337 Services GmbH
```

## Step 2 --- Check BGP.Tools

I opened:

``` text
Tasks → Task 3 → BGPTools.pdf
```

The report showed:

``` text
AS Number: 210558
1337 Services GmbH
```

It also showed the tags:

``` text
Server Hosting
Tor services
```

Therefore the two requested tags were:

``` text
Server Hosting, Tor services
```

### Task 3 answers

``` text
Country:
Netherlands

C2:
Remcos

Autonomous System:
1337 Services GmbH

BGP.Tools tags:
Server Hosting, Tor services
```

------------------------------------------------------------------------

# Task 4 --- Service Exposure

## Why exposed services matter

If an IP has open ports, those services tell me what the machine exposes
to the internet.

For example:

``` text
22    → SSH
3389  → RDP
80    → HTTP
443   → HTTPS
```

An exposed service can tell me:

-   What software is running
-   What version may be running
-   Whether remote access is enabled
-   Whether the server may have a vulnerable service
-   Whether the service leaks information about malware infrastructure

------------------------------------------------------------------------

# Shodan

Shodan continuously scans internet-connected systems and records
information such as:

-   Open ports
-   Service banners
-   Software
-   Versions
-   TLS information

As a SOC analyst, I can use Shodan to understand the public exposure of
an IP.

------------------------------------------------------------------------

# Censys

Censys is another useful source for internet-facing infrastructure.

It can provide:

-   Open services
-   Ports
-   Software
-   TLS certificates
-   Certificate names
-   Network information

The room's Task 4 evidence was provided as screenshots rather than PDFs.

------------------------------------------------------------------------

# TLS Certificates

A TLS certificate can contain useful information such as:

``` text
Subject
Issuer
Validity
Names
Fingerprint
```

A suspicious certificate can sometimes reveal the software or C2
framework running behind an unknown service.

This is exactly what happened in this task.

------------------------------------------------------------------------

# Task 4 --- Step-by-step

The IP was:

``` text
64[.]89[.]160[.]44
```

## Step 1 --- Open the Censys screenshot

I used:

``` text
Tasks → Task 4 → ip1.png
```

The Censys result showed:

``` text
9 Total Services
```

The exposed ports included:

``` text
135
139
445
1000
3389
7777
27015
27152
27383
```

The remote access service was:

``` text
RDP
```

because port:

``` text
3389
```

was exposed.

Therefore:

``` text
Remote access service = RDP
```

## Step 2 --- Count the open ports

The Censys screenshot explicitly showed:

``` text
9 Total Services
```

Therefore:

``` text
Open ports/services = 9
```

## Step 3 --- Investigate the unknown service

Port:

``` text
1000/TCP
```

was an unknown service.

I opened the second Censys screenshot:

``` text
Tasks → Task 4 → ip2.png
```

The TLS certificate showed:

``` text
Subject DN: CN=AsyncRAT Server
```

That exposed the C2 name:

``` text
AsyncRAT
```

### How I got it

``` text
64.89.160.44
      ↓
Censys
      ↓
Unknown TCP 1000 service
      ↓
TLS certificate
      ↓
CN=AsyncRAT Server
      ↓
C2 = AsyncRAT
```

## Step 4 --- Certificate validity

I then checked the TLS certificate screenshot.

The certificate information showed a validity period of:

``` text
3935 days
```

Therefore:

``` text
Certificate validity = 3935 days
```

The screenshot showed the certificate dates as:

``` text
FEB 20, 2025
      ↓
NOV 30, 2035
```

and explicitly calculated:

``` text
3935 days
```

### Task 4 answers

``` text
Remote access service:
RDP

Open ports:
9

C2:
AsyncRAT

Certificate validity:
3935 days
```

------------------------------------------------------------------------

# Task 5 --- VPN Detection

## Why VPN detection matters

Imagine a user normally logs in from:

``` text
London
```

The SIEM sees another login:

``` text
London
```

At first this may look normal.

But the IP could belong to a VPN provider.

That means:

``` text
Location looks normal
        ≠
Real user location is confirmed
```

Attackers can use VPNs and proxies to hide their real location.

------------------------------------------------------------------------

# IP2Proxy and Spur

Two tools introduced in the room are:

``` text
IP2Proxy
Spur
```

They can help identify:

-   VPN
-   Proxy
-   Tor exit nodes
-   Other anonymisation infrastructure

This is important because GeoIP alone can be misleading.

------------------------------------------------------------------------

# SOC Analyst Workflow

My basic workflow from this room is:

## Step 1 --- Investigate the domain

Ask:

``` text
Does the domain look legitimate?
Is it a typosquat?
What is its reputation?
When was it registered?
What IP does it resolve to?
```

## Step 2 --- Investigate the IP

Ask:

``` text
Is it a CDN?
What is its reputation?
Where is it located?
Is it a VPN/proxy/Tor node?
Which ASN owns it?
What type of network is it?
```

## Step 3 --- Investigate exposed services

Ask:

``` text
What ports are open?
What services are running?
What software/version is exposed?
Are there TLS certificates?
Does a certificate reveal a C2 framework?
```

## Step 4 --- Correlate everything

The important part is not one answer.

I want to build a picture:

``` text
Domain
  ↓
IP
  ↓
ASN
  ↓
Country
  ↓
Reputation
  ↓
Services
  ↓
Certificate
  ↓
C2 / infrastructure
```

------------------------------------------------------------------------

# Task 6 --- Challenge

The malicious domain was:

``` text
raytracingengine[.]com
```

The room said to start with the online tools and fall back to the
attached incident reports if the live infrastructure was unavailable.

Because infrastructure changes quickly, I used the uploaded reports as
the main evidence.

------------------------------------------------------------------------

## Step 1 --- Resolve the domain

I opened:

``` text
Tasks → Challenge → NSLookup.pdf
```

The A record showed:

``` text
35.188.105.97
```

The report also showed:

``` text
AS name: Google
```

and the location:

``` text
Council Bluffs, Iowa, United States
```

Therefore:

``` text
IP = 35.188.105.97
Cloud provider = Google
Country = United States
```

### How I got it

``` text
raytracingengine.com
        ↓
NSLookup report
        ↓
A record
        ↓
35.188.105.97
        ↓
Google infrastructure
        ↓
United States
```

------------------------------------------------------------------------

# Step 2 --- Find the creation date

I opened:

``` text
Tasks → Challenge → WHOIS.pdf
```

The WHOIS report showed:

``` text
Created:
2/21/2026
```

Therefore the requested date is:

``` text
21.02.2026
```

The registrar was:

``` text
Dynadot Inc
```

and the IP listed in the report was also:

``` text
35.188.105.97
```

------------------------------------------------------------------------

# Step 3 --- Investigate the exposed service

I opened:

``` text
Tasks → Challenge → Censys.pdf
```

The Censys report showed the host:

``` text
35.188.105.97
```

and an exposed:

``` text
SSH 22/TCP
```

The software was shown as:

``` text
OpenBSD OpenSSH
```

The room's expected answer for the attack server OS was:

``` text
Linux
```

I cross-checked the room walkthrough, which gives **Linux** as the
expected answer.

### Important distinction

The Censys evidence directly tells me the exposed service/software:

``` text
SSH 22/TCP
OpenBSD OpenSSH
```

The answer expected by the room is:

``` text
Linux
```

So I should remember that the Censys service banner and the room's OS
answer are not exactly the same type of information.

------------------------------------------------------------------------

# Task 6 --- Final Answers

``` text
IP:
35.188.105.97

Cloud provider:
Google Cloud

Country:
United States

Domain creation date:
21.02.2026

Attack server OS:
Linux
```

------------------------------------------------------------------------

# Full Room Investigation Workflow

This is the workflow I want to remember from this room.

``` text
                DOMAIN ALERT
                     │
                     ▼
              DNS / NSLookup
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
       A / AAAA             TXT / NS
          │
          ▼
        IP
          │
          ▼
    ┌───────────────┐
    │ IP Reputation │
    └───────┬───────┘
            │
      ┌─────┼─────┐
      ▼     ▼     ▼
 VirusTotal BGP  GeoIP
            │
            ▼
           ASN
            │
            ▼
     Service Exposure
            │
      ┌─────┴─────┐
      ▼           ▼
    Shodan      Censys
                    │
                    ▼
             TLS Certificates
                    │
                    ▼
              C2 / Framework
                    │
                    ▼
            Final Threat Picture
```

------------------------------------------------------------------------

# Important Concepts I Learned

## 1. DNS

DNS converts:

``` text
Domain → IP
```

This lets me pivot from a domain to its infrastructure.

------------------------------------------------------------------------

## 2. A vs AAAA

``` text
A    → IPv4
AAAA → IPv6
```

------------------------------------------------------------------------

## 3. WHOIS / RDAP

Useful for:

``` text
Registrar
Creation date
Expiration date
Name servers
Registration information
```

Domain age is especially useful during suspicious-domain investigations.

------------------------------------------------------------------------

## 4. ASN

An ASN tells me which autonomous system controls an IP prefix.

I can use it to understand whether the IP belongs to:

``` text
Residential ISP
Cloud
CDN
Server hosting
VPN
```

------------------------------------------------------------------------

## 5. GeoIP

GeoIP provides an approximate geographic location.

But:

``` text
GeoIP ≠ exact physical location
```

VPNs, proxies and CDNs can make the result misleading.

------------------------------------------------------------------------

## 6. CDN

A CDN can sit between users and the actual origin server.

Therefore:

``` text
Malicious domain
       ↓
Cloudflare
       ↓
Shared CDN IP
```

The CDN IP itself may not be malicious.

------------------------------------------------------------------------

## 7. VirusTotal

For an IP, VirusTotal can provide:

``` text
Detection score
Community comments
C2 information
Malware associations
```

In this room, the comments were what revealed:

``` text
Remcos
```

------------------------------------------------------------------------

## 8. BGP.Tools

BGP.Tools helped me understand:

``` text
ASN
Organisation
Network type
Tags
Prefixes
```

For AS210558:

``` text
1337 Services GmbH
```

the relevant tags were:

``` text
Server Hosting
Tor services
```

------------------------------------------------------------------------

## 9. Shodan / Censys

These tools help me answer:

``` text
What is exposed to the internet?
```

I can investigate:

``` text
Ports
Services
Software
Certificates
```

------------------------------------------------------------------------

## 10. TLS Certificates

Certificates can reveal more than encryption.

They can expose:

``` text
Subject
Issuer
Software/framework name
Validity
Names
Fingerprint
```

In this room:

``` text
CN=AsyncRAT Server
```

was the clue that revealed the C2.

------------------------------------------------------------------------

## 11. VPN / Proxy / Tor detection

A suspicious login from a normal-looking location can still be
suspicious if the IP belongs to:

``` text
VPN
Proxy
Tor
```

That is why I should not rely on GeoIP alone.

------------------------------------------------------------------------

# My Takeaway

The biggest lesson from this room is:

> **An IP address or domain is only the starting point of an
> investigation.**

I should keep pivoting.

For a domain:

``` text
Domain
 ↓
DNS
 ↓
IP
 ↓
ASN
 ↓
Country
 ↓
Reputation
 ↓
Services
 ↓
TLS
 ↓
C2 / Infrastructure
```

For an IP:

``` text
IP
 ↓
VirusTotal / AbuseIPDB
 ↓
ASN
 ↓
GeoIP
 ↓
VPN / Proxy / Tor
 ↓
Shodan / Censys
 ↓
Open ports
 ↓
Services
 ↓
Certificates
 ↓
Threat infrastructure
```

The important SOC skill is not memorising every website.

It is learning **how to pivot from one piece of evidence to the next and
explain why each lookup matters**.

------------------------------------------------------------------------

# Quick Revision

``` text
Verify → Enrich → Decide

DNS:
Domain → IP

A:
IPv4

AAAA:
IPv6

WHOIS/RDAP:
Domain ownership + age

ASN:
Network ownership/context

GeoIP:
Approximate location

VirusTotal:
Reputation + community intelligence

BGP.Tools:
ASN/network information

Shodan:
Internet-facing services

Censys:
Services + certificates

IP2Proxy / Spur:
VPN / Proxy / Tor detection

TLS certificate:
Issuer + subject + validity + useful service clues
```

## Answers at a glance

  Task                          Answer
  ----------------------------- --------------------------------
  2 --- CDN                     `Cloudflare`
  2 --- Domain age              `1 days old`
  3 --- Country                 `Netherlands`
  3 --- C2                      `Remcos`
  3 --- ASN                     `1337 Services GmbH`
  3 --- ASN tags                `Server Hosting, Tor services`
  4 --- Remote access service   `RDP`
  4 --- Open ports/services     `9`
  4 --- C2                      `AsyncRAT`
  4 --- Certificate validity    `3935 days`
  6 --- Resolved IP             `35.188.105.97`
  6 --- Cloud provider          `Google Cloud`
  6 --- Country                 `United States`
  6 --- Creation date           `21.02.2026`
  6 --- OS                      `Linux`

