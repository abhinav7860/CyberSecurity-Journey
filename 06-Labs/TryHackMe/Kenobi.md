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



# Part 2 - Initial Access and Privilege Escalation

---

# Exploitation Overview

After completing enumeration, I had gathered enough information to understand how the different services were related.

Instead of attacking a single service directly, the compromise relied on combining information obtained from multiple sources.

The attack chain looked like this:

```text
SMB
│
├── Username (kenobi)
├── ProFTPD Information
└── SSH Key Information
        │
        ▼
FTP (ProFTPD)
        │
        ▼
Known Vulnerability Research
        │
        ▼
NFS Export (/var)
        │
        ▼
SSH Authentication
        │
        ▼
User Shell
```

This room demonstrated that successful penetration tests are often the result of combining several small findings rather than discovering one critical vulnerability.

---

# Initial User Access

After leveraging the identified weakness and retrieving the SSH private key from the exported directory, I authenticated to the target using SSH.

Once connected, I verified the current user.

```bash
whoami
```

Output:

```text
kenobi
```

At this stage I had obtained a normal user shell.

The first objective was complete.

---

# Capturing the User Flag

The user flag was stored inside the user's home directory.

Reading the file confirmed that initial access had been achieved successfully.

This marks the transition from **Initial Access** to **Privilege Escalation**.

---

# Beginning Privilege Escalation

The first thing I learned was:

> Never attempt privilege escalation immediately.

Instead, perform another round of enumeration.

Even though I already had shell access, I still knew very little about the operating system.

The enumeration phase starts again.

---

# Enumerating the System

Some of the first commands I used included:

```bash
whoami
hostname
id
pwd
```

These commands provide basic information about:

* Current user
* Groups
* Hostname
* Working directory

Although simple, they help build a picture of the environment before searching for privilege escalation vectors.

---

# Enumerating SUID Files

One of the most important Linux privilege escalation techniques involves SUID binaries.

I searched for them using:

```bash
find / -perm -u=s -type f 2>/dev/null
```

---

## What is SUID?

Normally, programs execute with the permissions of the current user.

Example:

```text
User
    │
    ▼
Program
    │
    ▼
Runs as User
```

A SUID binary behaves differently.

```text
User
    │
    ▼
SUID Program
    │
    ▼
Runs as File Owner
```

If the owner is **root**, then the program executes with root privileges.

This mechanism is required for legitimate programs such as:

* passwd
* su
* sudo

However, custom SUID binaries may introduce security vulnerabilities if they are poorly written.

---

# Identifying an Unusual Binary

Among the standard Linux binaries, one file immediately stood out:

```text
/usr/bin/menu
```

Unlike common utilities such as `passwd` or `su`, this binary was not part of a standard Linux installation.

Whenever I encounter an unfamiliar SUID executable, I treat it as suspicious and investigate further.

---

# Investigating the Binary

I first executed the program to understand its behaviour.

It displayed a simple menu containing three options.

Running the program alone did not reveal how it worked internally.

To gather more information, I inspected it using:

```bash
strings /usr/bin/menu
```

---

# Why Use strings?

`strings` extracts human-readable text from compiled binaries.

Although a compiled executable consists mostly of machine code, it still contains readable text such as:

* Error messages
* Menu options
* File paths
* Library names
* External commands

This makes `strings` one of the quickest and safest methods for investigating an unknown binary.

---

# Important Discovery

The output revealed several external commands referenced by the program.

This indicated that the binary relied on other system utilities instead of implementing all functionality internally.

This observation became the key to understanding the privilege escalation path.

---

# Understanding PATH

Linux uses the PATH environment variable to locate executables.

Viewing the current PATH:

```bash
echo $PATH
```

Example:

```text
/home/kenobi/bin
/usr/local/bin
/usr/bin
/bin
...
```

When a user types a command without specifying its full location, Linux searches each directory in PATH until it finds a matching executable.

This behaviour is convenient, but it can become dangerous when a privileged program relies on PATH.

---

# PATH Hijacking

The custom SUID binary executed external commands without using absolute paths.

Instead of calling a specific executable directly, it relied on the PATH search order.

This created an opportunity for PATH hijacking.

PATH hijacking occurs when an attacker places a malicious executable earlier in the search path than the legitimate one.

When the vulnerable application attempts to launch a program, Linux executes the attacker's version first.

Because the vulnerable binary was running with elevated privileges, the replacement executable inherited those privileges.

---

# Mistake I Made

Initially, I assumed the original privilege escalation method described in older write-ups would work immediately.

However, the deployed machine behaved differently.

Instead of obtaining a root shell, I encountered unexpected behaviour.

Rather than assuming the exploit was incorrect, I began troubleshooting.

---

# Troubleshooting Process

I verified:

* The current PATH
* Which executable Linux was locating
* File permissions
* Symbolic links
* Behaviour of the replacement executable

This process taught me an important lesson.

Penetration testing is not simply following commands.

It involves understanding how the operating system behaves and adjusting when the environment differs from documentation.

---

# Root Access

After correcting the issue, the custom SUID binary executed the replacement program with root privileges.

The shell prompt changed from:

```text
kenobi@kenobi:~$
```

to

```text
root@kenobi:~#
```

At this point I verified the current user:

```bash
whoami
```

Output:

```text
root
```

This confirmed successful privilege escalation.

---

# Capturing the Root Flag

With administrative access obtained, I accessed the root directory and retrieved the final flag.

This completed the room.

---

# Part 3 - Reflection, Lessons Learned & References

---

# Commands Used During the Room

## Reconnaissance

```bash
nmap <IP>
```

Purpose:

* Discover open ports
* Identify running services
* Build the initial attack surface

---

## SMB Enumeration

```bash
nmap -p445 --script=smb-enum-shares.nse,smb-enum-users.nse <IP>
```

Purpose:

* Discover SMB shares
* Identify accessible resources

---

```bash
smbclient //<IP>/anonymous -N
```

Purpose:

* Connect to the anonymous share
* Browse available files

---

## FTP Enumeration

```bash
nc <IP> 21
```

Purpose:

* Perform banner grabbing
* Identify the FTP software and version

---

## Vulnerability Research

```bash
searchsploit ProFTPD 1.3.5
```

Purpose:

* Search Exploit-DB locally
* Identify publicly known vulnerabilities

---

## NFS Enumeration

```bash
nmap -p111 --script=nfs-ls,nfs-showmount,nfs-statfs <IP>
```

Purpose:

* Discover exported directories
* Gather additional attack surface information

---

## SSH Access

```bash
ssh -i id_rsa kenobi@<IP>
```

Purpose:

* Authenticate using the recovered SSH private key

---

## Linux Enumeration

```bash
whoami
id
hostname
pwd
```

Purpose:

* Identify the current user
* Confirm groups
* Gather basic system information

---

## SUID Enumeration

```bash
find / -perm -u=s -type f 2>/dev/null
```

Purpose:

* Locate files that execute with the owner's privileges
* Identify possible privilege escalation vectors

---

## Binary Analysis

```bash
strings /usr/bin/menu
```

Purpose:

* Extract readable strings
* Identify external commands
* Understand program behaviour

---

## PATH Inspection

```bash
echo $PATH
which <command>
```

Purpose:

* Understand how Linux searches for executables
* Verify which executable will be launched

---

# Mistakes I Made

## 1. Focusing on Exploitation Too Early

Initially, I wanted to jump directly into exploiting the FTP service.

After completing the room, I understood that penetration testing starts with **enumeration**, not exploitation.

Good enumeration makes exploitation much easier.

---

## 2. Not Understanding Why NFS Was Important

At first I wondered why the room asked me to enumerate NFS when I already had useful information from SMB.

Later I realised that the exported `/var` directory became an important part of the attack chain.

This taught me that every exposed service deserves investigation.

---

## 3. Confusion About PATH

I initially believed Linux always knew where commands were stored.

After studying the PATH variable, I understood that Linux searches directories in order until it finds the first matching executable.

This concept explained why PATH hijacking works.

---

## 4. Confusion About strings

I originally thought `strings` was a random command used only for this room.

Now I understand that it is one of the quickest ways to investigate an unfamiliar binary.

It can reveal:

* Hardcoded commands
* Error messages
* File paths
* Library names
* Interesting strings

---

## 5. Following Commands Without Understanding Them

At several points I copied commands before fully understanding why they worked.

By stopping to ask questions and understanding each step, I learned much more than simply completing the room.

---

# Important Concepts Learned

## Enumeration

Enumeration is the process of collecting as much information as possible before attempting exploitation.

Good enumeration often reveals:

* Services
* Users
* Shares
* Versions
* Configurations
* Misconfigurations

---

## SMB

SMB allows systems to share resources across a network.

Commonly shared resources include:

* Documents
* Backups
* Configuration files
* Printers

Anonymous shares frequently expose sensitive information.

---

## Banner Grabbing

Many network services reveal their software version when a connection is established.

Knowing the exact version allows targeted vulnerability research.

---

## NFS

NFS allows Linux systems to share directories over a network.

Unlike SMB, it primarily shares Linux filesystem paths.

If misconfigured, NFS can expose sensitive files or directories.

---

## SUID

SUID allows a program to execute with the permissions of its owner instead of the user running it.

This feature is necessary for some administrative utilities but can become dangerous if custom programs are written insecurely.

---

## PATH

PATH is an environment variable that tells Linux where to search for commands.

The search happens from left to right.

The first matching executable is launched.

---

## PATH Hijacking

PATH hijacking occurs when a privileged program executes another program without specifying its absolute path.

If an attacker controls an earlier directory in PATH, they may be able to influence which executable is launched.

---

# MITRE ATT&CK Mapping

| Technique                         | Description                          |
| --------------------------------- | ------------------------------------ |
| Active Scanning                   | Service discovery and reconnaissance |
| Network Share Discovery           | SMB enumeration                      |
| Software Discovery                | Service version identification       |
| Valid Accounts                    | SSH authentication                   |
| Abuse Elevation Control Mechanism | SUID privilege escalation            |

---

# Real-World Relevance

Although Kenobi is a training room, the concepts appear frequently in real environments.

Examples include:

* Exposed SMB shares containing confidential information
* Outdated software with publicly known vulnerabilities
* Misconfigured NFS exports
* Custom administrative utilities running with elevated privileges
* Insecure handling of environment variables

The specific software versions may differ, but the methodology remains applicable.

---

# What I Learned

This room changed the way I approach penetration testing.

Before completing Kenobi, I thought exploitation was mainly about finding a vulnerability and running an exploit.

After completing the room, I understood that penetration testing is a structured process.

Each stage builds on the previous one:

1. Reconnaissance
2. Enumeration
3. Information Gathering
4. Vulnerability Research
5. Exploitation
6. Privilege Escalation
7. Post-Exploitation

I also became much more comfortable with Linux fundamentals, especially:

* File permissions
* SSH
* SUID
* PATH
* Binary analysis

Most importantly, I learned that understanding **why** a technique works is far more valuable than memorising commands.

---

