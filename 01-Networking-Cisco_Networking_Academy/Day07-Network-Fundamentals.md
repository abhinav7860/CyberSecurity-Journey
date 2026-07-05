# Day 7 - Static & Dynamic IP Address Assignment (DHCP)

Today I learned how devices get IP addresses and how DHCP works.

---

# 1. Static IP Address

A Static IP Address is assigned manually by the network administrator.

The following information needs to be entered manually:

- IP Address
- Subnet Mask
- Default Gateway

### Example

Servers, printers and routers usually use static IP addresses because their address should not change.

### Advantages

- Permanent IP address
- Easy to access important devices

### Disadvantages

- Time-consuming to configure
- Easy to make configuration mistakes

---

# 2. Dynamic IP Address

A Dynamic IP Address is assigned automatically using **DHCP (Dynamic Host Configuration Protocol).**

Instead of configuring every device manually, the DHCP server assigns:

- IP Address
- Subnet Mask
- Default Gateway
- DNS Server

### Advantages

- Automatic configuration
- Reduces human errors
- Saves time
- IP addresses can be reused

---

# 3. DHCP

Think of DHCP as a **receptionist**.

Whenever a new device joins the network, it asks the DHCP server for an IP address.

The DHCP server checks its available IP pool and assigns one to the device.

---

# 4. DHCP Process (DORA)

The DHCP process happens in four steps.

### DHCP Discover

The client searches for a DHCP server.

> "Is there any DHCP server available?"

---

### DHCP Offer

The DHCP server replies with an available IP address.

> "Yes, you can use this IP."

---

### DHCP Request

The client accepts the offered IP address.

> "I would like to use this IP."

---

### DHCP Acknowledgement (ACK)

The DHCP server confirms the assignment.

> "Done! This IP address is now yours."

Easy way to remember:

**DORA**

- D → Discover
- O → Offer
- R → Request
- A → Acknowledge

---

# 5. DHCP Server

A DHCP server can be:

- Dedicated Server
- Router
- Wireless Router

In most home networks, the Wi-Fi router acts as the DHCP server.

It receives a public IP from the ISP and assigns private IP addresses to devices inside the home network.

---

# 6. Router as a Gateway

A router connects two or more different networks.

If a device wants to communicate with another network (like the Internet), it sends the data to the router.

The router then forwards the data to the correct destination.

### Example

If my laptop wants to open Google, it first sends the request to the router.

The router forwards it to the Internet.

---

# 7. Default Gateway

A Default Gateway is the IP address of the router inside my local network.

Every device uses the default gateway to communicate with other networks.

### Example

```
Laptop IP          : 192.168.1.101
Subnet Mask        : 255.255.255.0
Default Gateway    : 192.168.1.1
```

Here, **192.168.1.1** is the router's IP address.

---

# 8. Router as a Network Boundary

A router separates the **internal network** from the **external network (Internet).**

### Internal Network

- Uses private IP addresses.
- Example: `192.168.1.x`

### External Network

- Uses public IP addresses provided by the ISP.

The router acts as the boundary between these two networks.

---

# 9. NAT (Network Address Translation)

Private IP addresses cannot directly communicate over the Internet.

The router converts the private IP address into its public IP address before sending the packet to the Internet.

This process is called **NAT**.

When the reply comes back, the router translates the public IP back to the correct private IP.

---
