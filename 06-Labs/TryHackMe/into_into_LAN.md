# TryHackMe — Intro to LAN

**Room:** Intro to LAN  
**Platform:** TryHackMe  

---
# Task 1 — LAN Topologies

## LAN

**LAN (Local Area Network)** is a network that connects devices within a limited area like a home, office, or school.

---

## Network Topologies

### Star Topology

- All devices connect to a central **Switch/Hub**
- Most commonly used today

**Pros**
- Easy to expand
- Reliable
- Easy to isolate device failures

**Cons**
- More expensive
- If the central switch fails, the network goes down

---

### Bus Topology

- All devices share one backbone cable

**Pros**
- Cheap
- Easy to set up

**Cons**
- Single point of failure
- Performance decreases with more traffic
- Hard to troubleshoot

---

### Ring Topology

- Devices form a loop
- Data travels around the ring

**Pros**
- Less traffic collisions
- Easier to locate faults

**Cons**
- One broken cable/device can break the whole network

---

## Switch

A switch connects multiple devices in a LAN and forwards packets only to the correct destination.

Unlike a hub, it doesn't broadcast packets to every device.

---

## Router

A router connects different networks together.

Its main job is:

> **Routing** — finding the best path for data between networks.

---

# Task 2 — Subnetting

Subnetting means dividing one large network into smaller networks.

### Benefits

- Better organization
- Improved security
- Better performance
- Easier management

---

## Important Addresses

### Network Address

Identifies the network itself.

Example:

```
192.168.1.0
```

---

### Host Address

Identifies an individual device.

Example:

```
192.168.1.100
```

---

### Default Gateway

The device responsible for sending traffic outside the local network.

Usually:

```
192.168.1.1
```

or

```
192.168.1.254
```

---

## Subnet Mask

- Used to divide networks
- 32 bits long
- Each octet ranges from **0–255**

Example:

```
255.255.255.0
```

---

# Task 3 — ARP

**ARP (Address Resolution Protocol)** maps an IP address to its MAC address.

When a device knows an IP but not its MAC address, ARP is used.

---

## ARP Process

### 1. ARP Request

Broadcast message:

> "Who has this IP address?"

---

### 2. ARP Reply

The device owning that IP replies with its MAC address.

The sender stores this mapping in its **ARP Cache** for future communication.

---

# Task 4 — DHCP

**DHCP (Dynamic Host Configuration Protocol)** automatically assigns IP addresses to devices joining a network.

Instead of configuring IP addresses manually, the DHCP server does it automatically.

---

## DHCP Process (DORA)

### 1. DHCP Discover

Device searches for a DHCP server.

---

### 2. DHCP Offer

Server offers an available IP address.

---

### 3. DHCP Request

Device requests to use the offered IP.

---

### 4. DHCP ACK

Server confirms the assignment.

The device can now use the IP address.

---

# Key Terms

| Term | Meaning |
|------|---------|
| LAN | Local Area Network |
| Switch | Connects devices inside a LAN |
| Router | Connects different networks |
| Routing | Sending packets between networks |
| Subnetting | Dividing a network into smaller networks |
| Network Address | Identifies the network |
| Host Address | Identifies a device |
| Default Gateway | Sends traffic outside the LAN |
| ARP | Maps IP → MAC |
| ARP Cache | Stores IP and MAC mappings |
| DHCP | Automatically assigns IP addresses |
| DHCP Discover | Device searches for DHCP server |
| DHCP Offer | Server offers an IP |
| DHCP Request | Device requests offered IP |
| DHCP ACK | Server confirms the IP assignment |

---

