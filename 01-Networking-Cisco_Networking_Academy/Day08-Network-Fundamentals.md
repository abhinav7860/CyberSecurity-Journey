# Day 08 - MAC Address, ARP & Broadcast Domains

# 1. MAC Address vs IP Address

Every device on a network has two important addresses.

### IP Address (Logical Address)

- Used to identify a device on a network.
- Used for communication between different networks.
- Can change depending on the network.

### MAC Address (Physical Address)

- Unique address assigned to the Network Interface Card (NIC).
- Used for communication within the same local network.
- Does not normally change.

---

# 2. Communication on the Same Network

If both devices are on the same network:

- Source IP = Sender's IP
- Destination IP = Receiver's IP
- Source MAC = Sender's MAC
- Destination MAC = Receiver's MAC

The sender directly sends the frame to the destination device.

---

# 3. Communication on a Different Network

If the destination is on another network:

- Source IP stays the same.
- Destination IP stays the same.
- Source MAC changes at every hop.
- Destination MAC becomes the MAC address of the default gateway (router).

The router receives the packet, removes the old MAC addresses, adds new MAC addresses, and forwards it to the next device.

**Important:**

- IP addresses remain the same from source to destination.
- MAC addresses change every time the packet passes through a router.

---

# 4. Broadcast Domain

A broadcast domain is a group of devices that receive the same broadcast message.

When a device sends a broadcast:

- Every device connected to the same switch receives it.
- Devices on other networks do not receive it because routers block broadcasts.

If a network becomes too large, broadcast traffic also increases.

Routers are used to split one large broadcast domain into multiple smaller broadcast domains.

---

# 5. Address Resolution Protocol (ARP)

ARP is used when a device knows the destination IP address but does not know its MAC address.

ARP works only inside the local network.

### ARP Process

**Step 1**

The sender broadcasts:

> "Who has this IP address?"

---

**Step 2**

Every device checks the IP address.

Only the device with the matching IP replies.

---

**Step 3**

The destination sends back its MAC address.

---

**Step 4**

The sender stores the IP and MAC mapping in the **ARP Table**.

Next time, it can communicate directly without sending another ARP request.

---

# 6. ARP Table

The ARP table stores:

- IP Address
- MAC Address

This avoids sending an ARP request every time communication happens.

---

# Things to Remember

### Same Network

Destination MAC = Destination Device's MAC

---

### Different Network

Destination MAC = Router's MAC (Default Gateway)

---

### Ethernet Broadcast MAC Address

```
FF:FF:FF:FF:FF:FF
```

---

### ARP Uses

ARP converts:

```
IP Address
      ↓
MAC Address
```

---
