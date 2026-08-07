# Networking Essentials
**Platform:** InfoSecLab  
**Category:** Networking Fundamentals  
**Date:** 07 August 2026

---

# OSI Model (Open Systems Interconnection)

The OSI Model is a conceptual framework that explains how data travels across a network. It divides communication into seven layers, each responsible for a specific task.

| Layer | Name | PDU | Main Responsibility |
|------|------|------|--------------------|
| 7 | Application | Data | User-facing protocols (HTTP, FTP, SMTP, DNS) |
| 6 | Presentation | Data | Encryption, Compression, Data Formatting |
| 5 | Session | Data | Establishes and Manages Sessions |
| 4 | Transport | Segments | Reliable Data Transfer (TCP/UDP) |
| 3 | Network | Packets | Routing using IP Addresses |
| 2 | Data Link | Frames | MAC Address Communication |
| 1 | Physical | Bits | Physical Transmission over Cable/Wireless |

### Mnemonic

```
Please
Do
Not
Throw
Sausage
Pizza
Away
```

---

# Security Attacks by OSI Layer

| Layer | Common Attacks |
|---------|----------------|
| Application | SQL Injection, XSS, Phishing |
| Presentation | SSL Bypass |
| Session | Session Hijacking |
| Transport | SYN Flood, Port Scanning |
| Network | IP Spoofing |
| Data Link | ARP Spoofing, MAC Spoofing |
| Physical | Wire Tapping, Cable Cutting |

---

# Encapsulation

When sending data:

```
Application Data
      ↓
Transport Header Added
      ↓
Segment
      ↓
IP Header Added
      ↓
Packet
      ↓
MAC Header Added
      ↓
Frame
      ↓
Bits
```

Each lower layer adds its own header before transmission.

---

# Decapsulation

At the destination:

```
Bits
 ↓
Frame
 ↓
Packet
 ↓
Segment
 ↓
Application Data
```

Headers are removed layer by layer until the application receives the original data.

---

# TCP/IP Model

The Internet actually uses the TCP/IP Model instead of the OSI model.

| TCP/IP Layer | OSI Equivalent |
|--------------|----------------|
| Application | L5, L6, L7 |
| Transport | L4 |
| Internet | L3 |
| Network Access | L1 & L2 |

---

# TCP (Transmission Control Protocol)

TCP is connection-oriented and reliable.

Features:

- Reliable
- Ordered Delivery
- Error Checking
- Acknowledgements
- Flow Control

Used by:

- HTTPS
- SSH
- FTP
- SMTP

---

# TCP Three-Way Handshake

Before communication begins:

```
Client                     Server

SYN  --------------------->

      <------------------  SYN-ACK

ACK  --------------------->
```

Connection Established

---

# SYN Flood Attack

Attackers continuously send SYN packets but never complete the handshake.

Result:

- Server resources become exhausted.
- Legitimate users cannot connect.

---

# UDP (User Datagram Protocol)

UDP is connectionless.

Characteristics:

- No Handshake
- Faster
- Less Reliable
- No Error Recovery

Common Uses:

- DNS
- VoIP
- Video Streaming
- Online Gaming

---

# TCP vs UDP

| TCP | UDP |
|------|------|
| Reliable | Fast |
| Connection-Oriented | Connectionless |
| Error Checking | Minimal Error Checking |
| Uses ACK | No ACK |
| Slower | Faster |

---

# IPv4

IPv4 consists of:

- 32 Bits
- Four Octets
- Example:

```
192.168.1.10
```

Each octet ranges from:

```
0-255
```

---

# IPv6

IPv6 solves IPv4 exhaustion.

Characteristics:

- 128 Bits
- Hexadecimal
- Larger Address Space

Example:

```
2001:db8::1
```

---

# Public vs Private IP Addresses

Private IP ranges cannot be accessed directly over the Internet.

| Class | Range |
|--------|-------------------------|
| A | 10.0.0.0 – 10.255.255.255 |
| B | 172.16.0.0 – 172.31.255.255 |
| C | 192.168.0.0 – 192.168.255.255 |

Public IPs are globally unique.

---

# NAT (Network Address Translation)

NAT allows multiple private devices to share one public IP address.

Example:

```
Laptop
192.168.1.10

↓

Router

↓

Public IP

203.x.x.x

↓

Internet
```

Benefits:

- Conserves IPv4 addresses
- Hides internal network
- Allows Internet access

---

# Special IP Addresses

### Loopback

```
127.0.0.1
```

Represents the local machine (localhost).

Used for:

- Testing
- Local services

---

### APIPA

```
169.254.x.x
```

Automatically assigned when DHCP is unavailable.

---

# Subnetting

Subnetting divides a large network into smaller networks.

Benefits:

- Better Security
- Less Broadcast Traffic
- Easier Management
- Better Performance

---

# CIDR Notation

CIDR indicates how many bits belong to the network.

Examples:

| CIDR | Subnet Mask |
|-------|-------------|
| /8 | 255.0.0.0 |
| /16 | 255.255.0.0 |
| /24 | 255.255.255.0 |

---

# Reserved Addresses

Every subnet reserves:

First Address

```
Network Address
```

Last Address

```
Broadcast Address
```

These cannot be assigned to hosts.

---

# Host Calculation

Formula:

```
Usable Hosts = 2^(32-CIDR) - 2
```

Example:

```
/24

Host Bits = 8

2^8 = 256

256 - 2 = 254 Hosts
```

---

# Common Subnets

| CIDR | Usable Hosts |
|-------|--------------|
| /24 | 254 |
| /25 | 126 |
| /26 | 62 |
| /30 | 2 |

---

# DNS (Domain Name System)

DNS translates domain names into IP addresses.

Example:

```
google.com

↓

142.x.x.x
```

Without DNS, users would have to remember IP addresses.

---

# DNS Record Types

| Record | Purpose |
|---------|----------|
| A | Maps Domain → IPv4 |
| AAAA | Maps Domain → IPv6 |
| MX | Mail Server |
| TXT | Verification, SPF, DKIM, DMARC |
| CNAME | Alias Record |

---

# DHCP (Dynamic Host Configuration Protocol)

DHCP automatically assigns:

- IP Address
- Subnet Mask
- Gateway
- DNS Server

Without DHCP, every device would require manual configuration.

---

# DHCP DORA Process

```
Discover

↓

Offer

↓

Request

↓

Acknowledge
```

Client discovers DHCP server, receives an offer, requests the address, and receives confirmation.

---

# ARP (Address Resolution Protocol)

ARP converts:

```
IP Address

↓

MAC Address
```

Switches require MAC addresses for local communication.

Example:

```
192.168.1.10

↓

00:1A:2B:3C:4D:5E
```

---

