# TryHackMe - Networking Concepts

**Date:** July 16, 2026

# OSI Model (Open Systems Interconnection)

The **OSI Model** is a conceptual framework created by ISO to explain how computers communicate over a network.

It consists of **7 layers**, each responsible for a specific task.

A simple way to remember the layers from bottom to top is:

> **Please Do Not Throw Spinach Pizza Away**

| Layer | Name | Main Purpose |
|--------|----------------------|--------------------------------|
| 7 | Application | Provides services to applications |
| 6 | Presentation | Data encoding, encryption, compression |
| 5 | Session | Manages communication sessions |
| 4 | Transport | End-to-end communication |
| 3 | Network | Routing packets between networks |
| 2 | Data Link | Communication within the same network |
| 1 | Physical | Physical transmission of bits |

---

# Layer 1 — Physical Layer

This layer is responsible for physically transmitting data.

Examples include:

- Ethernet cables
- Fiber optic cables
- Wi-Fi radio signals
- Electrical signals
- Optical signals

Without this layer, devices cannot communicate physically.

---

# Layer 2 — Data Link Layer

The Data Link Layer allows communication between devices connected to the **same local network**.

It uses **MAC Addresses** to identify devices.

Examples:

- Ethernet (802.3)
- Wi-Fi (802.11)

### MAC Address

A MAC Address:

- Is 48 bits (6 bytes)
- Written in hexadecimal
- Example:

```
00:1A:2B:3C:4D:5E
```

The first three bytes identify the manufacturer.

Every Ethernet frame contains:

- Source MAC Address
- Destination MAC Address

---

# Layer 3 — Network Layer

The Network Layer connects **different networks**.

Its main responsibilities are:

- Logical addressing
- Routing
- Selecting the best path

Protocols include:

- IP
- ICMP
- IPSec

Routers operate at this layer.

Unlike MAC addresses, this layer uses **IP Addresses**.

---

# Layer 4 — Transport Layer

The Transport Layer enables communication between applications running on different computers.

Main responsibilities:

- Reliable communication
- Error checking
- Flow control
- Segmentation

Protocols:

- TCP
- UDP

---

# Layer 5 — Session Layer

This layer establishes and manages communication sessions.

Responsibilities include:

- Starting sessions
- Maintaining sessions
- Ending sessions
- Synchronizing communication

Examples:

- RPC
- NFS

---

# Layer 6 — Presentation Layer

The Presentation Layer prepares data for the application.

It handles:

- Encoding
- Compression
- Encryption

Examples include:

- Unicode
- ASCII
- JPEG
- PNG
- MIME

Without this layer, applications may not understand received data.

---

# Layer 7 — Application Layer

This is the layer users interact with directly.

It provides network services to applications.

Protocols include:

- HTTP
- HTTPS
- FTP
- DNS
- SMTP
- POP3
- IMAP

Example:

When opening a website, the browser communicates using HTTP or HTTPS at this layer.

---

# OSI Model Summary

| Layer | Protocol Examples |
|--------|-------------------|
| Application | HTTP, FTP, DNS |
| Presentation | JPEG, PNG, MIME |
| Session | RPC, NFS |
| Transport | TCP, UDP |
| Network | IP, ICMP |
| Data Link | Ethernet, Wi-Fi |
| Physical | Cable, Radio Signals |

---

# TCP/IP Model

Unlike the OSI Model, the TCP/IP Model is the practical networking model used on the Internet.

It has **4 layers**.

| TCP/IP Layer | Equivalent OSI Layer(s) |
|--------------|-------------------------|
| Application | Layers 5, 6, 7 |
| Transport | Layer 4 |
| Internet | Layer 3 |
| Link | Layers 1 & 2 |

---

# Mapping Between Models

| OSI | TCP/IP |
|------|---------|
| Application | Application |
| Presentation | Application |
| Session | Application |
| Transport | Transport |
| Network | Internet |
| Data Link | Link |
| Physical | Link |

---

# IP Addresses

Every device connected to a network needs a unique IP Address.

Think of an IP address as a home address.

Without it, data wouldn't know where to go.

---

## IPv4 Address

An IPv4 address contains:

- 4 Octets
- 32 Bits

Example:

```
192.168.1.100
```

Each octet ranges from:

```
0 - 255
```

---

# Network Address

Example:

```
192.168.1.0
```

Identifies the network itself.

---

# Broadcast Address

Example:

```
192.168.1.255
```

A packet sent here reaches every device on the network.

---

# Subnet Mask

Example:

```
255.255.255.0
```

Can also be written as:

```
/24
```

Meaning:

The first 24 bits represent the network portion.

Available host range:

```
192.168.1.1
to
192.168.1.254
```

---

# Private IP Address Ranges

These addresses cannot be reached directly from the Internet.

| Range |
|--------|
| 10.0.0.0 – 10.255.255.255 |
| 172.16.0.0 – 172.31.255.255 |
| 192.168.0.0 – 192.168.255.255 |

These are commonly used inside:

- Homes
- Offices
- Schools

Routers use **NAT (Network Address Translation)** to allow private devices to access the Internet.

---

# Public IP Address

Public IPs are globally reachable.

Example:

```
8.8.8.8
```

Anyone on the Internet can communicate with a public IP.

---

# Router

A Router operates at **Layer 3**.

Its job is to:

- Read destination IP addresses
- Choose the best path
- Forward packets toward their destination

It acts like a postal office directing mail.

---

# UDP (User Datagram Protocol)

UDP is a lightweight transport protocol.

Characteristics:

- Connectionless
- Faster
- No error checking
- No acknowledgement
- No guaranteed delivery

Used for:

- Streaming
- Online Games
- Voice Calls
- DNS

Think of UDP like sending a normal letter without delivery confirmation.

---

# TCP (Transmission Control Protocol)

TCP is a reliable transport protocol.

Characteristics:

- Connection-Oriented
- Reliable
- Ordered Delivery
- Error Checking
- Acknowledgements

Used for:

- Web Browsing
- Email
- File Transfer
- SSH

---

# TCP Three-Way Handshake

Before communication starts, TCP establishes a connection.

The three steps are:

### Step 1

Client sends:

```
SYN
```

---

### Step 2

Server replies:

```
SYN + ACK
```

---

### Step 3

Client responds:

```
ACK
```

Connection established.

This process ensures both devices are ready to communicate.

---

# Port Numbers

Ports identify applications running on a computer.

Range:

```
1 - 65535
```

Common ports:

| Port | Service |
|------|----------|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |

---

# Encapsulation

When data travels through the network, every layer adds its own header.

The process is called **Encapsulation**.

Flow:

```
Application Data
        ↓
TCP Segment / UDP Datagram
        ↓
IP Packet
        ↓
Ethernet Frame
```

At the receiving end, these headers are removed in reverse order.

---

# Life of a Packet

When visiting a website:

1. User enters URL
2. Browser creates HTTP request
3. TCP establishes connection
4. IP adds source and destination addresses
5. Ethernet/Wi-Fi creates frame
6. Routers forward the packet
7. Destination removes headers
8. Server processes request
9. Response returns the same way

---

# Telnet

Telnet is an old protocol used for remote command-line communication.

Default Port:

```
23
```

Although insecure today, it is useful for learning networking concepts and banner grabbing.

---

# Practical Exercises

### Echo Server (Port 7)

Whatever was typed was echoed back.

Example:

```
Hi

Hi
```

---

### Daytime Server (Port 13)

Returned the current server time.

---

### HTTP Server (Port 80)

Connected using:

```bash
telnet MACHINE_IP 80
```

Sent:

```http
GET / HTTP/1.1
Host: telnet.thm
```

The server responded with:

```
HTTP/1.1 200 OK
```

Server identified itself as:

```
lighttpd/1.4.63
```

Flag obtained:

```
THM{TELNET_MASTER}
```

---

# Key Commands Learned

Check IP Address:

Linux

```bash
ifconfig
```

or

```bash
ip a
```

Windows

```cmd
ipconfig
```

Connect using Telnet

```bash
telnet MACHINE_IP PORT
```

Example:

```bash
telnet 10.10.10.10 80
```

---
