# Day 5 - IPv4 Address

Today I learned about IPv4 addresses, octets, dotted-decimal notation, network IDs, host IDs, and subnet masks.

---

## 1. IPv4 Address

Every device connected to a network needs an **IPv4 address**.

It is a **logical address** that helps identify a device on a network.

Examples of devices that have IPv4 addresses:
- Computer
- Laptop
- Server
- Printer
- IP Phone
- Router

Every packet sent over the internet contains:
- Source IP Address
- Destination IP Address

This helps the packet reach the correct destination and also allows the receiver to send a reply.

---

## 2. IPv4 Address Format

An IPv4 address is **32 bits** long.

It is divided into **4 parts**, and each part is called an **octet**.

Example in binary:

```
11010001.10100101.11001000.00000001
```

Since binary is difficult to read, it is converted into **dotted-decimal notation**.

Example:

```
209.165.200.1
```

Each octet can have a value from **0 to 255**.

---

## 3. Network ID and Host ID

An IPv4 address has two parts.

### Network ID

- Identifies the network.
- Devices with the same Network ID belong to the same network.

### Host ID

- Identifies a specific device inside that network.
- Every host should have a unique Host ID.

Example:

```
IP Address : 192.168.5.11
Subnet Mask: 255.255.255.0
```

Network ID:

```
192.168.5
```

Host ID:

```
11
```

---

## 4. Subnet Mask

A subnet mask helps identify which part of an IP address is the **Network ID** and which part is the **Host ID**.

Example:

```
IP Address : 192.168.18.57
Subnet Mask: 255.255.255.0
```

Network:

```
192.168.18.0
```

Host:

```
57
```

---

## 5. Same Network

Devices can communicate directly only if they are on the same network.

Example:

```
192.168.1.10
192.168.1.25
192.168.1.100
```

These are on the same network because the first three octets are the same.

Example:

```
192.168.1.10
192.168.2.15
```

These are different networks and need a **router** to communicate.

---

## 6. What I Practiced

Today I also solved some questions to identify:

- Network Address
- Host Address
- Devices on the same network

### Example

```
IP Address : 10.5.4.100
Subnet Mask: 255.255.255.0
```

Network Address:

```
10.5.4.0
```

Devices on the same network:

```
10.5.4.1
10.5.4.99
```

---

