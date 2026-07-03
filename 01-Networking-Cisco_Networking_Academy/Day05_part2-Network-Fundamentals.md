# Day 5 evening - Unicast, Broadcast & Multicast

Today I learned the different ways devices send data in a network.

---

## 1. Unicast

Unicast means **one device sends data to one other device**.

Only the destination device receives the data.

Example:
- Opening a website.
- Sending a message to one person.

```
Laptop  ------->  Server
```

### Points to remember

- One sender → One receiver.
- Most internet communication uses unicast.
- Source IP address is always a unicast address.

---

## 2. Broadcast

Broadcast means **one device sends data to every device in the same network**.

Every device receives the packet.


### Types

**Directed Broadcast**

Sent to all devices in a specific network.

Example:

```
172.16.4.255
```

**Limited Broadcast**

Sent to every device in the local network.

Example:

```
255.255.255.255
```

### Points to remember

- One sender → Everyone.
- Creates more network traffic.
- Routers don't forward broadcast packets.
- IPv6 doesn't use broadcast.

---

## 3. Multicast

Multicast means **one device sends data only to a selected group of devices**.

Only devices that joined that group receive the packet.

Example:

A teacher starts an online class.

Only the students who joined the meeting receive the class.

### Multicast IP Range (important)

```
224.0.0.0 - 239.255.255.255
```

Example:

```
224.0.0.5
```

---
## 4. Public IP Address

A Public IP Address is used to communicate over the Internet.

- It is unique across the Internet.
- It is assigned by an ISP.
- Anyone on the Internet can reach a public IP.

Example:

```
8.8.8.8
```

---

## 5. Private IP Address

A Private IP Address is used only inside a local network.

It cannot directly access the Internet.

The three private IP ranges are:

```
10.0.0.0 - 10.255.255.255
```

```
172.16.0.0 - 172.31.255.255
```

```
192.168.0.0 - 192.168.255.255
```

Example:

My home Wi-Fi usually gives my laptop an IP like:

```
192.168.1.10
```

---

## 6. NAT (Network Address Translation)

Since private IP addresses cannot communicate directly with the Internet, the router changes the private IP into a public IP.

This process is called **NAT**.

Without NAT, devices using private IP addresses cannot access the Internet.

---

## 7. Special IPv4 Addresses

### Loopback Address

```
127.0.0.1
```

Used to test my own computer.

If I run

```
ping 127.0.0.1
```

I'm basically checking whether my own network configuration is working properly.

---

### Link-Local Address (APIPA)

```
169.254.x.x
```

If a computer cannot get an IP address from DHCP, Windows automatically assigns an APIPA address.

This usually means there is a problem with the network connection or DHCP server.

---

## 8. Classful Addressing

Earlier, IPv4 addresses were divided into different classes.

### Class A

- Large networks
- More than 16 million hosts

### Class B

- Medium-sized networks
- Around 65,000 hosts

### Class C

- Small networks
- Up to 254 hosts

There are also:

- Class D → Multicast
- Class E → Experimental

Nowadays classful addressing is no longer used.

Today we use **Classless Addressing (CIDR)** because it uses IPv4 addresses more efficiently.

---

## 9. IP Address Assignment

Public IP addresses are managed by **IANA (Internet Assigned Numbers Authority).**

IANA allocates IP address blocks to Regional Internet Registries (RIRs).

These RIRs then allocate addresses to ISPs and organizations.

Some RIRs are:

- APNIC (Asia-Pacific)
- ARIN (North America)
- RIPE NCC (Europe)
- LACNIC (Latin America)
- AfriNIC (Africa)

---

