# TryHackMe — DNS in Detail

**Platform:** TryHackMe  
**Room:** DNS in Detail  
**Date:** July 19, 2026

---

# What is DNS?

**DNS (Domain Name System)** converts domain names into IP addresses.

Instead of remembering an IP address like:

```
104.26.10.229
```

I can simply visit:

```
tryhackme.com
```

DNS finds the correct IP address for me.

---

# Domain Hierarchy

DNS is organized in a hierarchy.

Example:

```
admin.tryhackme.com
```

- **.com** → Top-Level Domain (TLD)
- **tryhackme** → Second-Level Domain (SLD)
- **admin** → Subdomain

### Top-Level Domain (TLD)

The last part of a domain.

Examples:

- `.com`
- `.org`
- `.edu`
- `.gov`

There are two main types:

- **gTLD** (Generic TLD)
  - .com
  - .org
  - .edu

- **ccTLD** (Country Code TLD)
  - .uk
  - .in
  - .ca

### Second-Level Domain (SLD)

The main registered name.

Example:

```
tryhackme.com
```

Here,

```
tryhackme
```

is the Second-Level Domain.

Maximum length:

- **63 characters**

### Subdomain

A subdomain is created before the Second-Level Domain.

Example:

```
admin.tryhackme.com
blog.google.com
mail.microsoft.com
```

Maximum length:

- **63 characters**

Allowed characters:

- a-z
- 0-9
- hyphen (-)

Cannot use:

- `_`

Maximum complete domain length:

- **253 characters**

---

# Common DNS Record Types

## A Record

Maps a domain to an **IPv4 address**.

Example:

```
website.thm → 10.10.10.10
```

---

## AAAA Record

Maps a domain to an **IPv6 address**.

---

## CNAME Record

Points one domain to another domain.

Example:

```
shop.website.thm
        ↓
shops.myshopify.com
```

The browser performs another lookup to get the final IP address.

---

## MX Record

Specifies the mail server responsible for receiving emails.

MX records also contain a **priority value**.

Lower number = Higher priority.

Example:

```
30 alt4.aspmx.l.google.com
```

---

## TXT Record

Stores text information.

Common uses:

- SPF
- DMARC
- Domain verification
- Email authentication

Example:

```
website.thm

TXT

THM{7012BBA60997F35A9516C2E16D2944FF}
```

---

# How DNS Lookup Works

When I visit a website, DNS resolves the domain in this order:

```
Browser Cache
        ↓
Recursive DNS Server
        ↓
Root DNS Server
        ↓
TLD Server
        ↓
Authoritative DNS Server
        ↓
IP Address Returned
```

### Recursive DNS Server

Usually provided by the ISP.

Checks its cache before asking other DNS servers.

---

### Root DNS Server

Knows where every Top-Level Domain server is.

Example:

```
.com
.org
.gov
```

---

### TLD Server

Knows which **Authoritative DNS Server** manages a domain.

---

### Authoritative DNS Server

Stores the actual DNS records.

This is where records like:

- A
- AAAA
- MX
- TXT
- CNAME

are stored.

---

### TTL (Time To Live)

TTL tells DNS resolvers **how long a record should stay cached** before requesting it again.

TTL is measured in **seconds**.

---

# DNS Enumeration with nslookup

Basic syntax:

```bash
nslookup <domain>
```

Example:

```bash
nslookup website.thm
```

---

## Lookup an A Record

```bash
nslookup --type=A website.thm
```

Result:

```
10.10.10.10
```

---

## Lookup a CNAME Record

```bash
nslookup --type=CNAME shop.website.thm
```

Result:

```
shops.myshopify.com
```

---

## Lookup a TXT Record

```bash
nslookup --type=TXT website.thm
```

Result:

```
THM{7012BBA60997F35A9516C2E16D2944FF}
```

---

## Lookup an MX Record

```bash
nslookup --type=MX website.thm
```

Result:

```
Priority: 30
Mail Server: alt4.aspmx.l.google.com
```

---

# Practical

### Task 1

Learned that DNS translates domain names into IP addresses.

---

### Task 2

Understood the DNS hierarchy:

- Root Domain
- TLD
- Second-Level Domain
- Subdomain

---

### Task 3

Learned the purpose of common DNS records:

- A
- AAAA
- CNAME
- MX
- TXT

---

### Task 4

Learned how a DNS request travels:

Browser

↓

Recursive DNS Server

↓

Root Server

↓

TLD Server

↓

Authoritative DNS Server

↓

Response returned to browser

Also learned that **TTL** controls how long DNS responses stay cached.

---

### Task 5

Used `nslookup` to query different DNS records.

Commands used:

```bash
nslookup website.thm

nslookup --type=A website.thm

nslookup --type=CNAME shop.website.thm

nslookup --type=TXT website.thm

nslookup --type=MX website.thm
```

Observed:

- A Record → `10.10.10.10`
- CNAME → `shops.myshopify.com`
- TXT → `THM{7012BBA60997F35A9516C2E16D2944FF}`
- MX Priority → `30`

---

