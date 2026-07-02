# Network Basics & IP Addressing

**Date:** 02 July 2026

## What I Learned Today

Today was my introduction to computer networking, which is one of the most important topics in cybersecurity. Before learning how to secure a network, I first need to understand how devices communicate with each other.

I learned about different types of computer networks, common networking devices, network topologies, IP addressing, MAC addresses, and some basic cyber attacks.

---

# Types of Networks

Different networks are designed for different sizes and purposes.

## PAN (Personal Area Network)

A PAN is a very small network used around a single person.

Example:
- Bluetooth headphones
- Smartwatch connected to a phone

---

## LAN (Local Area Network)

A LAN connects devices inside a small area like a home, classroom, or office.

Example:
- Home Wi-Fi
- College computer lab

This is probably the type of network I'll work with the most while practicing cybersecurity.

---

## CAN (Campus Area Network)

A CAN connects multiple LANs inside a campus.

Example:
- University network connecting different buildings

---

## MAN (Metropolitan Area Network)

A MAN covers an entire city.

Example:
- City-wide internet infrastructure

---

## WAN (Wide Area Network)

A WAN connects networks across countries or continents.

The Internet is the biggest example of a WAN.

---

## GAN (Global Area Network)

A GAN provides worldwide communication.

Example:
- Satellite communication
- Global mobile networks

---

# Network Components

I also learned about the hardware devices that make a network work.

## Hub

A hub simply sends incoming data to every connected device.

It doesn't know who the actual receiver is, so every computer receives the data.

---

## Switch

A switch is smarter than a hub.

It sends data only to the intended device using its MAC address.

Most modern LANs use switches instead of hubs.

---

## Router

A router connects different networks together.

It is responsible for directing internet traffic.

Example:
The Wi-Fi router in my house connects my local network to the Internet.

---

## Access Point

Provides wireless connectivity so devices can join a Wi-Fi network.

---

## Bridge

Connects two separate LAN segments together.

---

## Gateway

Acts as a translator between different types of networks.

---

## Firewall

A firewall protects a network by allowing or blocking network traffic based on security rules.

This is one of the most important security devices.

---

## Modem

A modem converts signals from my Internet Service Provider into a form that my router can understand.

---

## Repeater

A repeater strengthens weak network signals so they can travel longer distances.

---

# Network Topologies

A network topology describes how devices are connected.

I learned about:

- Bus Topology
- Star Topology
- Ring Topology
- Mesh Topology
- Hybrid Topology

Among these, Star Topology is the one I see most often because almost every home or office network uses a switch or router in the center.

---

# IP Address

Every device connected to a network needs an IP address.

An IP address is the logical address used for communication.

Without an IP address, devices cannot communicate over a network.

Example:

```
192.168.1.10
```

---

## IPv4

- 32-bit address
- Written in dotted decimal format
- Example:

```
192.168.1.100
```

---

## IPv6

IPv6 was introduced because IPv4 addresses are running out.

Features:

- 128-bit address
- Written in hexadecimal

Example:

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

---

# MAC Address

Unlike an IP address, a MAC address is permanently assigned to a network device.

It is also called the physical address.

Example:

```
00:1A:2B:3C:4D:5E
```

Every Network Interface Card (NIC) has its own MAC address.

---

# Network Interface Card (NIC)

A NIC is the hardware that allows a computer to connect to a network.

Examples include:

- Ethernet card
- Wi-Fi adapter
- USB network dongle

---

# Static IP

A Static IP never changes unless someone manually changes it.

Usually used for:

- Servers
- CCTV systems
- Network devices

---

# Dynamic IP

A Dynamic IP is automatically assigned by a DHCP server.

Most home Wi-Fi networks use Dynamic IP addresses.

---

# Private IP Address

Private IP addresses are used only inside local networks.

They cannot be accessed directly from the Internet.

Example range:

```
192.168.x.x
```

---

# Public IP Address

A Public IP address is assigned by the Internet Service Provider (ISP).

This address is visible on the Internet.

I can check it by searching:

```
What is my IP
```

---

# Lab Activity

Today's practical task was using:

```bash
ipconfig
```

This command displays:

- IPv4 Address
- Default Gateway
- DNS Server
- Subnet Mask

This will probably be one of the commands I'll use frequently during networking and penetration testing labs.

---

# Common Cyber Attacks

We also got introduced to some basic cyber attacks.

## Malware

Malware is malicious software designed to damage systems or steal data.

Examples:

- Virus
- Worm
- Trojan
- Ransomware

---

## Phishing

Phishing tricks users into revealing sensitive information through fake emails or websites.

Usually the attacker wants:

- Passwords
- Banking information
- Personal details

---

## DoS Attack

A Denial of Service (DoS) attack floods a server with traffic so that legitimate users cannot access it.

The goal is to make the service unavailable.

---

## Man-in-the-Middle (MITM)

In a MITM attack, an attacker secretly intercepts communication between two users without them knowing.

The attacker may:

- Read messages
- Modify data
- Steal credentials

---
