# TryHackMe — What is Networking?

**Room:** What is Networking?  
**Platform:** TryHackMe  

---

# Overview

This room introduced the fundamentals of networking. I learned what a network is, how the Internet works, how devices are identified using IP and MAC addresses, and how the `ping` command checks connectivity.

---

# Task 1 — What is Networking?

## What is a Network?

A network is simply a group of connected devices that communicate with each other.

Examples:
- Computers
- Phones
- Servers
- Cameras
- Smart devices

### Key Points

- Networks can contain **2 devices or billions of devices**.
- Networking is the foundation of cybersecurity because almost every attack happens over a network.

---

# Task 2 — What is the Internet?

The Internet is a **network of networks**.

It connects thousands of private networks together so devices around the world can communicate.

### Types of Networks

- **Private Network** → Home, office, school network
- **Public Network** → Internet

### Important Fact

- **World Wide Web (WWW)** was invented by **Tim Berners-Lee** in **1989**.

---

# Task 3 — Identifying Devices

Every device on a network has two identities:

## 1. IP Address

Used to identify a device on a network.

Example:

```
192.168.1.10
```

### IPv4

- 4 sections called **octets**
- Example:

```
192.168.1.10
```

### Public IP

Used to communicate over the Internet.

### Private IP

Used inside local networks.

Examples:

```
192.168.x.x

10.x.x.x

172.16.x.x - 172.31.x.x
```

---

## IPv6

Created because IPv4 addresses are running out.

Benefits:

- Huge number of addresses
- More efficient than IPv4

---

## 2. MAC Address

MAC stands for:

> **Media Access Control**

A MAC address is the physical address of a network interface.

Example:

```
a4:c3:f0:85:ac:2d
```

Structure:

- First 6 characters → Vendor
- Last 6 characters → Unique device identifier

### MAC Spoofing

A device can change (spoof) its MAC address to impersonate another device.

This is why relying only on MAC addresses for security is not a good idea.

---

## Practical

I spoofed Bob's MAC address to match Alice's and successfully accessed the restricted network.

**Flag:**

```
THM{YOU_GOT_ON_TRYHACKME}
```

---

# Task 4 — Ping (ICMP)

`ping` is a basic networking command used to check if another device is reachable.

It uses:

> **ICMP (Internet Control Message Protocol)**

### Example

```bash
ping 8.8.8.8
```

or

```bash
ping google.com
```

Ping tells us:

- Whether the host is reachable
- Response time (latency)
- Packet loss

---

## Practical

Pinged:

```bash
8.8.8.8
```

**Flag:**

```
THM{I_PINGED_THE_SERVER}
```

---

# Commands Learned

```bash
ping 10.10.10.10
```

---

# Key Terms

| Term | Meaning |
|------|---------|
| Network | Connected devices communicating together |
| Internet | Network of networks |
| IP Address | Logical address used for communication |
| Octet | One section of an IPv4 address |
| IPv4 | 32-bit addressing (4 octets) |
| IPv6 | 128-bit addressing |
| MAC Address | Physical hardware address |
| MAC Spoofing | Changing a device's MAC address |
| ICMP | Protocol used by ping |
| Ping | Checks connectivity between devices |

---
