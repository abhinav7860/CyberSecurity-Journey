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

# What I Understood Today

- Static IP addresses are configured manually.
- Dynamic IP addresses are assigned automatically using DHCP.
- DHCP follows the DORA process:
  - Discover
  - Offer
  - Request
  - Acknowledge
- Home routers usually act as DHCP servers.