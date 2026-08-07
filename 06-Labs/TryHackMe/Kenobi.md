# Kenobi - TryHackMe Walkthrough

> **Difficulty:** Easy
> **Platform:** TryHackMe
> **Category:** Linux, Enumeration, Exploitation, Privilege Escalation

---

# Objective

The goal of this room was to compromise a Linux machine by performing proper enumeration, identifying vulnerable services, gaining an initial foothold, and finally escalating privileges to root.

Unlike many beginner CTFs, Kenobi demonstrates that penetration testing is not about finding one vulnerability. Instead, it teaches how to combine multiple small pieces of information into a complete attack chain.

---

# Skills Learned

* Network Enumeration
* SMB Enumeration
* FTP Enumeration
* NFS Enumeration
* Service Version Detection
* Vulnerability Research
* SSH Authentication
* Linux File Permissions
* SUID Privilege Escalation
* PATH Hijacking
* Basic Binary Analysis

---

# Tools Used

* Nmap
* SMBClient
* SMBGet
* Netcat
* Searchsploit
* Showmount
* Mount
* SSH
* Strings
* Find
* Bash

---

# Attack Flow

```text
Port Scan
      │
      ▼
SMB Enumeration
      │
      ▼
Read log.txt
      │
      ▼
Discover ProFTPD + User "kenobi"
      │
      ▼
Enumerate NFS
      │
      ▼
Discover /var Export
      │
      ▼
Research ProFTPD Vulnerability
      │
      ▼
Copy SSH Private Key
      │
      ▼
Mount NFS Share
      │
      ▼
Retrieve id_rsa
      │
      ▼
SSH Login
      │
      ▼
User Flag
      │
      ▼
SUID Enumeration
      │
      ▼
PATH Hijacking
      │
      ▼
Root Shell
      │
      ▼
Root Flag
```

---

# Step 1 - Initial Reconnaissance

Every penetration test starts with identifying what services are exposed.

I began by scanning the target using Nmap.

```bash
nmap 10.49.xxx.xxx
```

Output:

```
21 FTP
22 SSH
80 HTTP
111 RPCBind
139 SMB
445 SMB
2049 NFS
```

---

## Why Nmap?

Nmap is used to identify:

* Open Ports
* Running Services
* Possible Attack Surface

Without enumeration, exploitation becomes guessing.

The first lesson I learned in this room is:

> **Never exploit before enumeration.**

---

# Step 2 - SMB Enumeration

Since ports **139** and **445** were open, the next logical step was to enumerate SMB.

I used:

```bash
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse <IP>
```

This revealed three shares.

```
print$
anonymous
IPC$
```

---

## Why Enumerate SMB?

SMB often exposes:

* Shared files
* Backups
* Configuration files
* Credentials
* Sensitive documents

Anonymous shares are especially interesting because they do not require authentication.

---

# Step 3 - Connecting to the Share

I connected using:

```bash
smbclient //<IP>/anonymous -N
```

The **-N** option tells SMBClient to connect without a password.

Listing files showed:

```
log.txt
```

---

## What I Learned

Finding a share is only the beginning.

The next step is always to inspect its contents.

Information leakage is one of the most common security issues.

---

# Step 4 - Reading log.txt

After downloading the file, I opened it.

Inside I found several important pieces of information.

### Username

```
kenobi
```

### FTP Service

```
ProFTPD
```

### SSH Key Generation

The log also contained details about an SSH key being generated for the **kenobi** user.

---

## Why is this Important?

This was the first major clue.

The log told me:

* A user exists.
* FTP runs as that user.
* SSH keys exist.

At this point I still could not access the system.

However, I now knew what to investigate next.

---

# Step 5 - FTP Enumeration

The log mentioned ProFTPD.

Instead of assuming anything, I confirmed it.

Using Netcat:

```bash
nc <IP> 21
```

The FTP banner displayed:

```
ProFTPD 1.3.5
```

---

## Why Use Netcat?

Netcat connects directly to a TCP port.

Many services immediately display a banner containing:

* Product Name
* Version Number

This process is called **Banner Grabbing**.

Banner grabbing helps identify software versions before researching vulnerabilities.

---

# Step 6 - Searching for Vulnerabilities

After identifying the version, I searched Exploit-DB.

```bash
searchsploit ProFTPD 1.3.5
```

Results:

```
ProFTPD 1.3.5 - mod_copy
```

Several exploits existed.

---

## Why Searchsploit?

Penetration testers rarely memorize vulnerabilities.

Instead they follow a process.

```
Identify Service

↓

Identify Version

↓

Research Vulnerabilities

↓

Verify Applicability

↓

Exploit
```

This workflow is much more important than remembering CVE numbers.

---

# Step 7 - NFS Enumeration

During the initial Nmap scan I noticed:

```
111 RPCBind
2049 NFS
```

Rather than ignoring these services, I enumerated them.

```bash
nmap -p111 --script=nfs-ls,nfs-showmount,nfs-statfs <IP>
```

Output:

```
/var
```

---

## What is NFS?

NFS (Network File System) allows Linux machines to share directories across a network.

It works similarly to SMB but is designed primarily for Unix/Linux systems.

Instead of sharing:

```
anonymous
```

like SMB,

NFS exports directories such as:

```
/var
```

---

## Why Enumerate NFS?

The goal was not to exploit it immediately.

The goal was to answer:

> What directories are exposed?

Enumeration always comes before exploitation.

---

# Important Concept

At this point I had gathered information from three different services.

## SMB

Provided:

* Username
* FTP Information
* SSH Key Information

## FTP

Provided:

* Exact software version

## NFS

Provided:

* Exported directory

None of these individually gave me access.

However, together they formed the attack path.

This is one of the biggest lessons from Kenobi:

> Successful penetration tests often combine multiple small findings instead of relying on a single critical vulnerability.

---

# Mistakes I Made During Enumeration

### Mistake 1

I tried using:

```bash
smbget -R smb://IP/anonymous
```

It produced a warning.

### Fix

Instead of relying on smbget, I used:

```bash
smbclient
```

which allowed me to browse the share interactively.

---

### Mistake 2

I did not initially understand why I needed to enumerate NFS.

I thought:

> "I already found FTP. Why enumerate another service?"

After studying the room, I understood that every open service should be investigated because you do not know which one will become useful later.

NFS eventually became a critical part of the exploit chain.

---

### Mistake 3

I initially focused on finding vulnerabilities before understanding the services.

After completing this part of the room, I realized the correct workflow is:

```
Recon

↓

Enumeration

↓

Research

↓

Exploitation
```

instead of immediately searching for exploits.

---

