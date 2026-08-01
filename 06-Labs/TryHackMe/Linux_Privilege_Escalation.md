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



