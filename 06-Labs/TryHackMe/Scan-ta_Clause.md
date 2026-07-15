# TryHackMe - Network Discovery: Scan-ta Clause

**Date:** July 15, 2026

---

# What is Network Discovery?

Network Discovery is the process of identifying devices, open ports, running services, and accessible resources on a target machine.

Before attacking a system, a penetration tester needs to answer questions like:

- Is the host alive?
- Which ports are open?
- Which services are running?
- Which services are vulnerable?
- Are there any hidden services?

Without this information, exploitation becomes much harder.

---

# Scenario

The fictional company **TBFC** had its QA server compromised by **HopSec**.

Our goal was to:

- Discover exposed services
- Find three hidden keys
- Combine the keys
- Access the admin console
- Enumerate internal services
- Retrieve the final flag from the MySQL database

---

# Step 1 - Initial Port Scan

The first thing I did was scan the target using Nmap.

Command:

```bash
nmap 10.48.133.225
```

Output:

```
22/tcp  SSH

80/tcp  HTTP
```

This is the default Nmap scan.

It scans the **Top 1000 TCP ports**.

At first glance only two services appeared:

- SSH
- HTTP

The website displayed:

```
Pwned by HopSec
```

which indicated the server had been compromised.

---

# Understanding Default Nmap Scan

By default, Nmap:

- Scans Top 1000 TCP ports
- Detects open ports
- Does not identify hidden services outside those ports

Many beginners stop here.

Today's lesson showed why that is a mistake.

---

# Step 2 - Full Port Scan

To check every TCP port, I used:

```bash
nmap -p- --script=banner 10.48.133.225
```

Option explanation:

```
-p-
```

Scan all **65,535 TCP ports**.

```
--script=banner
```

Attempts to grab service banners.

---

# Banner Grabbing

A banner is information that a service reveals after connecting.

It usually contains:

- Software name
- Version
- Service type

Example:

```
SSH-2.0-OpenSSH_9.6p1
```

This tells us:

- Service = SSH
- Version = OpenSSH 9.6p1

Banner grabbing is an important reconnaissance technique because attackers can search for known vulnerabilities affecting that specific version.

---

# New Services Discovered

The full scan revealed:

```
22     SSH

80     HTTP

21212  FTP

25251  Custom TBFC Service
```

The interesting finding was that FTP was **not running on the default port (21)**.

Instead it was listening on:

```
21212
```

This demonstrates that services can run on any port.

Never assume a service always uses its default port.

---

# FTP Enumeration

To connect:

```bash
ftp 10.48.133.225 21212
```

Login:

```
Username:

anonymous
```

FTP allowed anonymous access.

Listing files:

```bash
ls
```

Downloaded file:

```
tbfc_qa_key1
```

Retrieved:

```
KEY1

3aster_
```

This showed why anonymous FTP is considered a security risk.

Anyone could access the files without authentication.

---

# Netcat Enumeration

Next, I connected to the unknown service.

Command:

```bash
nc -v 10.48.133.225 25251
```

The server displayed:

```
TBFC maintd v0.2

Type HELP for commands
```

Running:

```
HELP
```

Displayed:

```
HELP

STATUS

GET KEY

QUIT
```

Using:

```
GET KEY
```

returned:

```
KEY2

15_th3_
```

This demonstrated that **Netcat** is a universal client capable of communicating with unknown TCP services.

---

# TCP vs UDP

Until this point,

I had only scanned TCP ports.

However,

Every machine also has **65,535 UDP ports**.

Important UDP services include:

- DNS
- DHCP
- SNMP
- NTP

Many important services use UDP instead of TCP.

---

# UDP Scan

Command:

```bash
nmap -sU 10.48.133.225
```

Output:

```
53/udp

DNS
```

This showed that the target was running a DNS server.

---

# DNS Enumeration

Instead of using a browser,

I queried the DNS server directly using:

```bash
dig @10.48.133.225 TXT key3.tbfc.local +short
```

Output:

```
n3w_xm45
```

This was:

```
KEY3
```

This demonstrated that DNS can store much more than domain names.

It can also store:

- TXT records
- SPF records
- DKIM
- Verification tokens
- Hidden information

---

# Combining the Keys

The three collected keys were:

```
KEY1

3aster_
```

```
KEY2

15_th3_
```

```
KEY3

n3w_xm45
```

Combined:

```
3aster_15_th3_n3w_xm45
```

This unlocked the hidden admin console.

---

# On-Host Enumeration

Once inside the system,

there was no need to scan externally anymore.

Instead,

I asked Linux which ports were listening.

Command:

```bash
ss -tunlp
```

Meaning:

```
-t

TCP
```

```
-u

UDP
```

```
-n

Numeric output
```

```
-l

Listening ports
```

```
-p

Show associated processes
```

This listed every listening service directly from the operating system.

---

# Internal Services

The command revealed:

```
127.0.0.1:3306

MySQL
```

This was important because:

```
127.0.0.1
```

means:

Only accessible from the local machine.

External scanners cannot reach it.

---

# Enumerating MySQL

Since I already had local access,

I connected directly.

List databases:

```bash
mysql -D tbfcqa01 -e "show tables;"
```

Output:

```
flags
```

Read table:

```bash
mysql -D tbfcqa01 -e "select * from flags;"
```

Output:

```
THM{4ll_s3rvice5_d1sc0vered}
```

This completed the room.

---

# Commands Learned Today

## Basic Port Scan

```bash
nmap TARGET
```

Scans the Top 1000 TCP ports.

---

## Full Port Scan

```bash
nmap -p- TARGET
```

Scans all TCP ports.

---

## Banner Grabbing

```bash
nmap --script=banner TARGET
```

Displays service banners.

---

## UDP Scan

```bash
nmap -sU TARGET
```

Scans UDP ports.

---

## FTP

```bash
ftp TARGET PORT
```

Connects to an FTP server.

---

## Netcat

```bash
nc -v TARGET PORT
```

Connects to any TCP service.

---

## DNS Query

```bash
dig @SERVER TXT DOMAIN +short
```

Queries DNS TXT records.

---

## List Listening Ports

```bash
ss -tunlp
```

Shows open ports directly from Linux.

---

## MySQL

Show tables:

```bash
mysql -D DATABASE -e "show tables;"
```

Read data:

```bash
mysql -D DATABASE -e "select * from TABLE;"
```

---

# Key Concepts Learned

## Network Discovery

Finding hosts and exposed services before attempting exploitation.

---

## Banner Grabbing

Reading service information to identify software and versions.

---

## FTP Enumeration

Checking whether anonymous access exposes sensitive files.

---

## Netcat

A versatile tool for interacting with unknown TCP services.

---

## UDP Scanning

Many important services run on UDP and require separate scanning.

---

## DNS Enumeration

DNS can reveal hidden information such as TXT records.

---

## On-Host Enumeration

Once access is obtained, tools like `ss` provide a more accurate view than external scanning.

---

## Localhost Services

Services listening on:

```
127.0.0.1
```

are accessible only from the host itself.

---

