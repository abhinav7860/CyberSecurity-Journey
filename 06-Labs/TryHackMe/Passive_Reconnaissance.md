# Passive Reconnaissance

**Platform:** TryHackMe    
**Date:** 10 July 2026

---

# Objective

In this room, I learned how to gather information about a target **without directly interacting with it**. This type of reconnaissance is called **Passive Reconnaissance** because all information is collected from publicly available sources.

Passive reconnaissance is the first phase of penetration testing, bug bounty hunting, and security assessments because it is stealthy and does not alert the target.

---

# What is Reconnaissance?

Reconnaissance (Recon) is the process of collecting information about a target before attempting any security testing.

Its main goal is to understand:

- Target infrastructure
- Domains
- Public IP addresses
- DNS records
- Technologies used
- Publicly exposed services

The better the reconnaissance, the easier it becomes to identify possible attack surfaces.

---

# Types of Reconnaissance

## Passive Reconnaissance

Passive reconnaissance means collecting information **without directly contacting the target**.

Examples:

- WHOIS lookup
- DNS queries
- Certificate Transparency logs
- DNSDumpster
- Shodan
- Public GitHub repositories
- Search engines

Advantages

- Difficult to detect
- No traffic reaches the target
- Safe first step
- Legal when performed on public information

---

## Active Reconnaissance

Active reconnaissance involves directly interacting with the target.

Examples:

- Ping Scan
- Port Scanning
- Nmap
- Directory Brute Force
- Vulnerability Scanning
- Web Enumeration

Disadvantages

- Easily detected
- Logged by IDS/IPS
- Can trigger alerts
- Requires authorization

---

# Passive vs Active Recon

| Passive Recon | Active Recon |
|---------------|--------------|
| No interaction with target | Direct interaction |
| Hard to detect | Easily detected |
| Public information | Sends packets |
| Low risk | Higher risk |

---

# WHOIS

WHOIS is a protocol used to obtain registration information about a domain.

It works on:

```
TCP Port 43
```

The information returned may include:

- Domain Registrar
- Registration Date
- Expiration Date
- Updated Date
- Name Servers
- Domain Status
- Abuse Contact

Nowadays most owner information is hidden because of GDPR and privacy protection.

---

# WHOIS Command

Basic syntax

```bash
whois domain.com
```

Example

```bash
whois tryhackme.com
```

---

## Practical Example

I tested:

```bash
whois tryhackme.com
```

Interesting information discovered:

- Registrar: Namecheap
- Created: 2018
- Domain Status:
  ```
  clientTransferProhibited
  ```
- Name Servers listed
- Registrant information hidden

---

# RDAP

RDAP (Registration Data Access Protocol) is the modern replacement for WHOIS.

Advantages:

- Uses HTTPS
- JSON output
- Easier to automate
- Better privacy
- Better security

Example

```bash
curl -s https://rdap.verisign.com/com/v1/domain/tryhackme.com | jq .
```

---

# DNS

DNS (Domain Name System) converts domain names into IP addresses.

Example

```
google.com
↓

142.250.x.x
```

---

# DNS Query Tools

Two common tools:

- nslookup
- dig

Although both work, **dig** is preferred because it provides cleaner output and more detailed information.

---

# nslookup

Syntax

```bash
nslookup domain
```

Example

```bash
nslookup tryhackme.com
```

---

## Query Specific Records

### A Record

```bash
nslookup -type=A tryhackme.com
```

Returns IPv4 addresses.

---

### MX Record

```bash
nslookup -type=MX tryhackme.com
```

Shows mail servers.

---

### TXT Record

```bash
nslookup -type=TXT tryhackme.com
```

Shows

- SPF
- DKIM
- DMARC
- Verification records

---

# dig

General Syntax

```bash
dig domain TYPE
```

Example

```bash
dig tryhackme.com A
```

---

### MX Records

```bash
dig tryhackme.com MX
```

---

### TXT Records

```bash
dig tryhackme.com TXT
```

---

### Using Cloudflare DNS

```bash
dig @1.1.1.1 tryhackme.com MX
```

---

## Practical Example

I queried

```bash
dig tryhackme.com MX
```

Output showed:

- Google Mail Servers
- Mail priorities
- TTL values
- Query time

This tells me the organization uses Google Workspace for email.

---

# Common DNS Records

| Record | Purpose |
|---------|----------|
| A | IPv4 Address |
| AAAA | IPv6 Address |
| MX | Mail Server |
| TXT | Text Records (SPF, DKIM, DMARC) |
| CNAME | Alias |
| SOA | Start of Authority |

---

# Subdomain Enumeration

A normal DNS lookup only works if you already know the hostname.

For example:

```
blog.tryhackme.com
```

If you don't know it exists, DNS cannot tell you.

Passive tools solve this problem.

---

# DNSDumpster

DNSDumpster collects public DNS information.

It can reveal:

- Subdomains
- MX Records
- TXT Records
- CNAME Records
- IP Addresses
- Network Map

Example search

```
tryhackme.com
```

---

# Certificate Transparency Logs (crt.sh)

Every SSL certificate issued on the Internet is logged publicly.

Website:

```
https://crt.sh
```

Search

```
%.tryhackme.com
```

This wildcard returns every certificate issued for TryHackMe subdomains.

Example discoveries

```
blog.tryhackme.com

admin.tryhackme.com

api.tryhackme.com
```

(if certificates exist)

---

# Why CT Logs Matter

Many forgotten subdomains still have SSL certificates.

These may expose:

- Old applications
- Test environments
- Admin portals
- APIs

without ever touching the target.

---

# Shodan

Shodan is a search engine for Internet-connected devices.

Instead of indexing websites like Google, it indexes:

- Servers
- Routers
- Cameras
- Firewalls
- IoT Devices
- Web Servers

Website

```
https://shodan.io
```

---

## Information Available

Shodan shows:

- Public IP
- Open Ports
- Operating System
- Hosting Provider
- ASN
- Country
- Services
- HTTP Headers
- SSL Information

---

## Useful Search Filters

Hostname

```
hostname:tryhackme.com
```

Organization

```
org:"TryHackMe"
```

Port

```
port:443
```

Country

```
country:US
```

---

# Practical Example

I searched one of TryHackMe's public IP addresses.

Observed:

- Cloudflare Hosting
- HTTPS Service
- Open Ports
- Country
- Server Banner

This information was available publicly without scanning the target.

---

# Commands Practiced

WHOIS

```bash
whois tryhackme.com
```

RDAP

```bash
curl -s https://rdap.verisign.com/com/v1/domain/tryhackme.com | jq .
```

DNS Lookup

```bash
nslookup tryhackme.com
```

A Record

```bash
nslookup -type=A tryhackme.com
```

MX Record

```bash
nslookup -type=MX tryhackme.com
```

TXT Record

```bash
nslookup -type=TXT tryhackme.com
```

dig

```bash
dig tryhackme.com A
```

Cloudflare Resolver

```bash
dig @1.1.1.1 tryhackme.com MX
```

---

