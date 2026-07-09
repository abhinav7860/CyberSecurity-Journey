# Day 1 - Bug Bounty Fundamentals & Nmap Basics

**Date:** July 9, 2026

Today was my first day learning Bug Bounty. Instead of trying to find vulnerabilities immediately, I focused on understanding the reconnaissance (Recon) phase. I learned that bug bounty starts with gathering information about a target before performing any testing.

---

# Reconnaissance Workflow

The mindset I learned today is:

```
Target Domain
      │
      ▼
WHOIS
      │
      ▼
DNS Lookup
      │
      ▼
Technology Detection
      │
      ▼
Subdomain Enumeration
      │
      ▼
Port Scanning
      │
      ▼
Service Enumeration
```

Every tool answers **one question**. Instead of memorizing commands, I should first ask:

> "What information do I want?"

Then choose the appropriate tool.

---

# 1. WHOIS

### Command

```bash
whois agoda.com
```

### Purpose

To find registration information about a domain.

### Information Obtained

* Domain registrar
* Creation date
* Expiration date
* Name servers
* Domain status
* Administrative information

### What I Learned

WHOIS tells me **who owns and manages the domain**, not whether it is vulnerable.

---

# 2. DIG

### Command

```bash
dig agoda.com
```

### Purpose

Find the IP address associated with a domain.

### Learned

```
agoda.com
↓

103.6.182.20
```

A domain is a human-readable name.

DNS converts it into an IP address.

---

# 3. HOST

### Command

```bash
host agoda.com
```

### Purpose

Quick DNS lookup.

### Information

* IP Address
* Mail Server (MX)
* HTTP Service Bindings

---

# 4. WhatWeb

### Command

```bash
whatweb agoda.com
```

### Purpose

Identify technologies used by a website.

### Information Found

* HTTP Server
* Cookies
* Security Headers
* Redirects
* Technologies
* Framework hints

### What I Learned

Before testing a web application, I should understand what technologies it is using.

---

# 5. Nikto

### Command

```bash
nikto -h https://www.agoda.com/
```

### Purpose

Gather security-related information about a web server.

### Information Found

* Missing security headers
* Cookie attributes
* SSL information
* robots.txt
* HTTP headers
* General observations

### What I Learned

Nikto performs automated security checks and highlights areas that may deserve further investigation. Findings are not automatically vulnerabilities.

---

# 6. Subfinder

### Command

```bash
subfinder -d agoda.com
```

### Purpose

Discover publicly known subdomains.

### Question Answered

> What public subdomains belong to this domain?

Example:

```
www.agoda.com
api.agoda.com
partner.agoda.com
```

---

# 7. Assetfinder

### Command

```bash
assetfinder agoda.com
```

### Purpose

Discover publicly visible assets and subdomains from different data sources.

### Learned

Different reconnaissance tools use different public sources.

Using multiple tools often discovers more assets.

---

# 8. Sublist3r

### Command

```bash
sublist3r -d agoda.com
```

### Purpose

Enumerate subdomains using multiple public sources.

### Sources Used

* Google
* Bing
* Yahoo
* Netcraft
* SSL Certificates
* PassiveDNS
* VirusTotal
* DNSDumpster

### Result

Found several Agoda subdomains including:

* [www.agoda.com](http://www.agoda.com)
* flights.agoda.com
* partners.agoda.com
* searchapi.agoda.com

---

# 9. Sherlock

### Command

```bash
sherlock username
```

### Purpose

OSINT tool for checking where a username exists across public websites.

### Information

Checks websites like:

* GitHub
* Reddit
* HackerOne
* TryHackMe
* GitLab
* Medium

### What I Learned

Sherlock searches for **usernames**, not domains.

---

# 10. Recon-ng

### What I Learned

Recon-ng is a **framework**, not a single reconnaissance tool.

It works like a toolbox.

First:

Choose a module.

Then:

Provide a target.

Finally:

Run the module.

---

# Nmap

The biggest topic I learned today.

---

## Host Discovery

### Command

```bash
nmap -sn <IP>
```

### Question

> Is the host alive?

---

## Default Scan

### Command

```bash
nmap <IP>
```

### Question

> Which common TCP ports are open?

---

## Scan Specific Port

```bash
nmap -p 80 <IP>
```

Question:

> Is port 80 open?

---

## Scan Multiple Ports

```bash
nmap -p 80,443 <IP>
```

Question:

> Are ports 80 and 443 open?

---

## Scan All Ports

```bash
nmap -p- <IP>
```

Question:

> Which ports are open across all 65,535 TCP ports?

---

## Scan Multiple Hosts

```bash
nmap IP1 IP2
```

Question:

> Scan multiple targets in one command.

---

## Scan Domain

```bash
nmap agoda.com
```

Nmap first performs DNS resolution:

```
agoda.com

↓

103.6.182.20

↓

Port Scan
```

---

## SYN Scan

```bash
nmap -sS <IP>
```

Question:

> Which TCP ports are open using SYN packets?

Fast TCP scan that doesn't complete the full TCP handshake.

---

## TCP Connect Scan

```bash
nmap -sT <IP>
```

Question:

> Which TCP ports are open using a full TCP connection?

Completes the three-way handshake.

---

## UDP Scan

```bash
nmap -sU <IP>
```

Question:

> Which UDP ports are open?

Usually slower because UDP often doesn't respond.

---

## OS Detection

```bash
nmap -O <IP>
```

Question:

> What operating system appears to be running?

Results should always be interpreted carefully because they may not be reliable.

---

## Version Detection

```bash
nmap -sV <IP>
```

Question:

> What services and versions are running on open ports?

---

## Fast Scan

```bash
nmap -F <IP>
```

Question:

> Scan only the most common ports quickly.

---

## Top Ports

```bash
nmap --top-ports 100 <IP>
```

Question:

> Scan only the specified number of most common ports.

---

## ACK Scan

```bash
nmap -sA <IP>
```

Question:

> Is a firewall filtering my probes?

---

## Window Scan

```bash
nmap -sW <IP>
```

Question:

> Can TCP window size behavior reveal additional information about port states?

---

## Default Scripts

```bash
nmap -sC <IP>
```

Question:

> Can Nmap automatically gather more information using its default NSE scripts?

Examples:

* HTTP Title
* SSL Certificate
* SSH Host Keys
* Service Information

---

## Safe Scripts

```bash
nmap --script=safe <IP>
```

Runs scripts designed for safe information gathering.

---

## Specific Script

```bash
nmap --script=http-title <IP>
```

Runs only one selected NSE script.

---

# Important Concepts Learned

## Open

A service is actively listening.

Example:

```
80/tcp open http
```

---

## Closed

The port exists, but no service is listening.

---

## Filtered

A firewall or another network device prevented Nmap from determining the port state.

---

## Open|Filtered

Mostly seen with UDP scans.

Nmap cannot confidently determine whether the port is open or simply filtered because UDP often provides no response.

---

# Biggest Lesson of the Day

The most valuable lesson I learned today was **not to memorize commands**.

Instead, I should always think:

1. What information do I need?
2. Which tool answers that question?
3. What did the output teach me?
4. What is my next question?

Every reconnaissance tool answers a specific question. By asking the right questions first, I can choose the correct tool and better understand the target before moving on to deeper analysis.

---

# Commands Practiced

```bash
whois agoda.com

dig agoda.com

host agoda.com

whatweb agoda.com

nikto -h https://www.agoda.com/

subfinder -d agoda.com

assetfinder agoda.com

sublist3r -d agoda.com

sherlock username

recon-ng

nmap -sn <IP>

nmap <IP>

nmap -p 80 <IP>

nmap -p 80,443 <IP>

nmap -p- <IP>

nmap -sS <IP>

nmap -sT <IP>

nmap -sU <IP>

nmap -O <IP>

nmap -sV <IP>

nmap -F <IP>

nmap --top-ports 100 <IP>

nmap -sA <IP>

nmap -sW <IP>

nmap -sC <IP>

nmap --script=safe <IP>

nmap --script=http-title <IP>
```
