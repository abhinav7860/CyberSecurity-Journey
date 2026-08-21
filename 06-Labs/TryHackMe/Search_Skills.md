# TryHackMe - Search Skills

## Room

**Room:** Search Skills  
**Platform:** TryHackMe  
**Date Added:** 21 August 2026  
**Status:** Completed

---

## What I learned

This room was mainly about different sources and tools that can be used to find information during security work.

The main things I worked with were:

- Shodan
- VirusTotal
- CVE / vulnerability databases
- Linux MAN pages
- GitHub

I liked this room because it showed that during security work, I don't always need to start by scanning or running complicated tools. Sometimes the information I need is already available through search engines, security databases, documentation, or public repositories.

---

## Task 2 - Shodan

Shodan is basically a search engine for devices and services that are exposed on the internet.

It can show things like:

- IP addresses
- Open ports
- Hostnames
- Domains
- Running services
- Software versions
- Organisations and locations

### Search used

```text
apache
```

I checked the first result and looked at the information shown for the IP:

```text
185.243.115.47
```

The domain associated with it was:

```text
tryhackme.thm
```

### Answer

**What domain is associated with 185.243.115.47?**

`tryhackme.thm`

---

## Task 3 - VirusTotal

VirusTotal is useful for checking suspicious files, URLs, domains and hashes.

It compares the submitted item against a large number of security vendors. It isn't something I would treat as absolute proof by itself, but seeing many vendors detect the same file is a strong warning sign.

### Search used

```text
invoice_payment.exe
```

The result showed:

```text
52 / 72 security vendors
```

So 52 vendors detected the file as malicious.

### Answer

**How many security vendors identified the file as dangerous?**

`52`

---

## Task 4 - Vulnerability Databases / CVE

CVE stands for **Common Vulnerabilities and Exposures**.

A CVE gives a specific identifier to a known vulnerability, using a format like:

```text
CVE-YEAR-NUMBER
```

I searched the vulnerability database for:

```text
CVE-2026-1337
```

The vulnerability was marked as **Critical** and the CVSS score shown was:

```text
10 / 10
```

The page also showed that the vulnerability could be exploited remotely without authentication, which made the severity clear.

### Answer

**What CVSS classification did the vulnerability get?**

`10`

---

## Task 5 - MAN Pages

This part was about Linux MAN pages.

MAN pages are built-in documentation for commands and tools in Linux. Instead of immediately searching the internet whenever I don't know a command, I can use:

```bash
man <command>
```

For example:

```bash
man nc
```

I searched the MAN page for `nc` (netcat) and looked at the examples at the bottom.

The example for opening a connection to `host.example.com` on port `42` was:

```bash
nc host.example.com 42
```

### Answer

**What is the example command?**

`nc host.example.com 42`

---

## GitHub - Vulnerability Research

The last part showed how GitHub can also be useful when researching vulnerabilities.

Searching for a CVE can sometimes lead to repositories containing:

- Proof-of-concept code
- Scripts
- Technical analysis
- Vulnerability research
- Documentation

For this task, I checked the repository for:

```text
CVE-2026-1337
```

After reading the README, I found that the script used to demonstrate the vulnerability was:

```text
exploit.py
```

### Answer

**What is the name of the script?**

`exploit.py`

---
