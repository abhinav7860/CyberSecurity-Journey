# Day 7 - Routing and Creating a LAN

Today I learned why routers are important in networking, how routing works, what a routing table is, how the default gateway is used, and how Local Area Networks (LANs) are designed.

---

## 1. Why Do We Need Routing?

Devices on the same network can communicate directly using their MAC addresses.

But if the destination is on a **different network**, the packet cannot reach it directly. That's where a **router** comes in.

Routing is the process of finding the best path for a packet to reach its destination.

### Example

- PC1 → 192.168.1.10
- PC2 → 192.168.1.20

Both are on the same network, so they communicate directly.

But if:

- PC1 → 192.168.1.10
- Server → 10.0.0.5

Since they are on different networks, the packet must first go to the router.

---

## 2. Switch vs Router

A **Switch** works using **MAC addresses** (Layer 2).

A **Router** works using **IP addresses** (Layer 3).

Simple way to remember:

- Switch → "Who is this device?"
- Router → "Which network should this packet go to?"

---

## 3. Routing Table

Every router keeps a **Routing Table**.

It stores:

- Network Address
- Interface to use
- Best path to reach that network

Whenever a packet arrives, the router checks the **Destination IP Address** and looks for the matching network in its routing table.

If no route is found, the router drops the packet unless a **Default Route** exists.

---

## 4. Default Route

A **Default Route** is used when the router doesn't know where the destination network is.

Instead of dropping the packet immediately, it forwards it through the default route.

Think of it as:

> "I don't know exactly where this network is, so I'll send it to my next router."

---

## 5. Default Gateway

Every host must know where to send packets that are meant for another network.

That router's local interface IP is called the **Default Gateway**.

Example:

```
PC IP:           192.168.1.10
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.1.1
```

If the destination is outside `192.168.1.0/24`, the PC sends the packet to `192.168.1.1`.

Without a default gateway, the PC can only communicate with devices on the same network.

---

## 6. Local Area Network (LAN)

A **LAN (Local Area Network)** is a group of devices connected together under one administration.

Examples:

- Home network
- School lab
- Office network

Most LANs use:

- Ethernet
- Wi-Fi

---

## 7. One Large LAN vs Multiple LANs

### Single LAN

Advantages

- Easy to set up
- Lower cost
- Devices can communicate directly
- Good for small networks

Disadvantages

- One large broadcast domain
- More broadcast traffic
- Harder to secure
- Performance decreases as more devices are added

---

### Multiple LANs

Advantages

- Smaller broadcast domains
- Better performance
- Better security
- Easier to organize departments

Disadvantages

- Requires routers
- More configuration
- Slight routing delay
- Higher cost

---

## 8. What I Practiced

Today I also completed the Packet Tracer labs:

- Created a simple LAN
- Connected PCs using switches
- Assigned IPv4 addresses
- Configured subnet masks
- Verified connectivity using ping
- Observed packet flow between devices
- Learned how routing changes communication between different networks

---

## important things -need to remember 

- Switch forwards using **MAC Address**
- Router forwards using **IP Address**
- Routing finds the best path to another network
- Routing Table stores network paths
- Default Route is used for unknown networks
- Default Gateway is the router IP used by hosts
- LAN is a group of connected local devices
- Large networks are divided into smaller LANs for better performance and security

---

