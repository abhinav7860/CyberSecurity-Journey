# Arcite Notes - Information Gathering Commands
**Date:** 06 July 2026

Today I learned some of the basic reconnaissance commands used during the information gathering phase of a penetration test.

---

# Host & Network Information

### ifconfig

Displays all available network interfaces along with their IP addresses and network details.

**Example**

```bash
ifconfig
```

---

### ip addr

Shows the IP address assigned to every network interface.

**Example**

```bash
ip addr
```

---

### ip route

Displays the routing table and shows where network traffic will be forwarded.

**Example**

```bash
ip route
```

---

### hostname

Displays the hostname of the current machine.

**Example**

```bash
hostname
```

---

### hostname -I

Displays the local IP address of the system.

**Example**

```bash
hostname -I
```

---

### arp -a

Displays the ARP table, showing the mapping between IP addresses and MAC addresses.

**Example**

```bash
arp -a
```

---

### netstat -tulnp

Shows all listening ports along with the services using them.

**Example**

```bash
netstat -tulnp
```

---

### ss -tulnp

Displays active network connections and listening ports. It is a faster alternative to netstat.

**Example**

```bash
ss -tulnp
```

---

### ping

Checks whether a target host is reachable.

**Example**

```bash
ping 8.8.8.8
```

---

### traceroute

Shows every hop a packet takes before reaching the destination.

**Example**

```bash
traceroute 8.8.8.8
```

---

# DNS Information Gathering

### nslookup

Performs a basic DNS lookup for a domain.

**Example**

```bash
nslookup google.com
```

---

### dig

Provides detailed DNS information such as A, MX, and NS records.

**Example**

```bash
dig google.com
```

---

### host

Displays the IP address and DNS information of a domain.

**Example**

```bash
host google.com
```

---

### whois

Displays domain registration details like owner, registrar, and expiry date.

**Example**

```bash
whois google.com
```

---

# Nmap Scanning

### Host Discovery

Checks whether a host is alive without scanning ports.

```bash
nmap -sn 192.168.1.10
```

---

### Basic Port Scan

Scans the most common ports.

```bash
nmap 192.168.1.10
```

---

### Specific Port Scan

Scans only the selected port.

```bash
nmap -p 80 192.168.1.10
```

---

### Full TCP Port Scan

Scans all 65535 TCP ports.

```bash
nmap -p- 192.168.1.10
```

---

### Service Detection

Identifies the version of services running on open ports.

```bash
nmap -sV 192.168.1.10
```

---

### OS Detection

Attempts to identify the target operating system.

```bash
nmap -O 192.168.1.10
```

---

### Aggressive Scan

Performs OS detection, version detection, script scanning, and traceroute.

```bash
nmap -A 192.168.1.10
```

---

### Fast Scan

Scans only the most common ports.

```bash
nmap -F 192.168.1.10
```

---

### Vulnerability Scan

Runs Nmap's vulnerability detection scripts.

```bash
nmap --script vuln 192.168.1.10
```

---

# Web Information Gathering

### WhatWeb

Identifies technologies used by a website.

```bash
whatweb https://example.com
```

---

### Nikto

Scans a web server for common vulnerabilities.

```bash
nikto -h https://example.com
```

---

### curl

Displays the HTTP response headers of a website.

```bash
curl -I https://example.com
```

---

### wget

Downloads files or webpages.

```bash
wget https://example.com
```

---

### HTTrack

Creates a local copy of an entire website.

```bash
httrack https://example.com
```

---

# Subdomain Enumeration

### Subfinder

Finds passive subdomains.

```bash
subfinder -d example.com
```

---

### Assetfinder

Discovers subdomains using public sources.

```bash
assetfinder example.com
```

---

### Amass

Performs advanced subdomain enumeration.

```bash
amass enum -d example.com
```

---

### Sublist3r

Discovers subdomains from multiple search engines.

```bash
sublist3r -d example.com
```

---

# OSINT Tools

### Sherlock

Searches for a username across multiple social media platforms.

```bash
sherlock johndoe
```

---

### Maigret

Looks for usernames on hundreds of websites.

```bash
maigret johndoe
```

---

### Recon-ng

A framework used for OSINT and reconnaissance.

```bash
recon-ng
```

---

### Maltego

A graphical OSINT tool used to visualize relationships between people, domains, and organizations.

```bash
maltego
```

---

# Network Enumeration

### Netdiscover

Discovers live hosts on a local network.

```bash
netdiscover -r 192.168.1.0/24
```

---

### Enum4linux

Enumerates SMB shares, users, groups, and other information from Linux or Windows systems.

```bash
enum4linux -a 192.168.1.20
```

---

### SMBClient

Lists the available SMB shares on a target machine.

```bash
smbclient -L //192.168.1.20 -N
```

---
