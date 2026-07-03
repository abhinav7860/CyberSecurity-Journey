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


