# Network Footprint Report – BostonFreelanceWriter.com

## Overview

This report documents a passive reconnaissance assessment of **bostonfreelancewriter.com** using publicly available Open Source Intelligence (OSINT) techniques. The objective was to identify the target's publicly exposed infrastructure, DNS configuration, domain registration details, hosting environment, and technology stack without directly interacting with the target systems.

> **Assessment Type:** Passive Reconnaissance (OSINT)  
> **Analyst:** Abhinav Sabu  
> **Date:** 01 August 2026

---

# Methodology

The assessment followed the reconnaissance process below:

```
DNS Enumeration
        ↓
WHOIS Lookup
        ↓
Certificate Transparency
        ↓
Technology Fingerprinting
        ↓
Analysis & Reporting
```

### Tools Used

- `dig`
- `whois`
- DNSDumpster
- BuiltWith
- crt.sh *(Unavailable during assessment due to 504 Bad Gateway)*

---

# Target Summary

| Field | Value |
|--------|-------|
| Target | bostonfreelancewriter.com |
| Website Type | Freelance Writing Services |
| Scope | Passive Reconnaissance Only |
| Interaction | None |

---

# Executive Summary

The target maintains a relatively small public attack surface appropriate for a professional business website. DNS records indicate that the website is hosted on Squarespace infrastructure while DNS management is provided through both Squarespace DNS and NSONE. WHOIS information shows that the domain has been registered since June 2019 with privacy protection enabled. No email-related DNS records were identified during the assessment.

---

# DNS Records

## A Records

```
198.185.159.145
198.185.159.144
198.49.23.144
198.49.23.145
```

### MX Records

```
No MX records found
```

### TXT Records

```
No TXT records found
```

### Name Servers

```
dns1.p06.nsone.net
dns2.p06.nsone.net
dns3.p06.nsone.net
dns4.p06.nsone.net
ns01.squarespacedns.com
ns02.squarespacedns.com
ns03.squarespacedns.com
ns04.squarespacedns.com
```

### Observations

- Multiple A records provide redundancy and load balancing.
- DNS infrastructure is managed by NSONE and Squarespace.
- No email infrastructure was publicly configured.

---

# WHOIS Information

| Property | Value |
|----------|-------|
| Registrar | Tucows Domains Inc. |
| Registration Provider | Squarespace |
| Registration Date | 01 June 2019 |
| Last Updated | 18 May 2026 |
| Expiration Date | 01 June 2027 |
| Registrant | Contact Privacy Inc. |
| DNSSEC | Unsigned |
| Domain Age | ~7 Years |

---

# Certificate Transparency

Unfortunately, **crt.sh** was returning **504 Bad Gateway** errors throughout the assessment period.

Because certificate transparency data could not be retrieved, the following information could not be verified:

- Certificate count
- Certificate Authority
- Publicly issued subdomains

**Note:** Rather than assuming or inventing information, this limitation has been documented as part of the assessment.

---

# Technology Profile

## Hosting

- Squarespace

## DNS Provider

- Squarespace DNS
- NSONE

## Web Platform

- Squarespace

## Analytics

- Google Analytics
- Google Universal Analytics

## Performance

- Chrome UX Report (CrUX)

## Search / AI

- Common Crawl
- AI Visibility Index

## APIs

- Google Font API

## Tag Management

- Google Tag Manager

## Libraries

- Adobe Typekit

## Language

- English

Approximately **70 technologies** were identified by BuiltWith.

---

# Observations

- The target has a minimal public-facing infrastructure.
- WHOIS privacy protection prevents disclosure of registrant information.
- Multiple A records improve availability through redundancy.
- No email infrastructure was identified via DNS.
- Squarespace hosting significantly reduces infrastructure exposure compared to self-managed hosting.
- Certificate Transparency analysis could not be completed because the public service was unavailable.

---

# Recommendations

- Monitor Certificate Transparency logs once the service becomes available.
- Continue maintaining WHOIS privacy protection.
- Periodically audit DNS records and remove unused entries.
- If email services are introduced, implement SPF, DKIM, and DMARC.
- Regularly review Squarespace security settings and website configuration.

---

# Assessment Summary

| Metric | Result |
|---------|--------|
| Assessment Type | Passive Reconnaissance |
| Estimated Time | 40 Minutes |
| Hardest Step | Certificate Transparency (Service Unavailable) |
| Most Interesting Finding | Website uses redundant Squarespace infrastructure with a relatively small public attack surface. |

---

