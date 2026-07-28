# Wireshark - Capture & Display Filters

**Source:** Arcite Cyber Security Training  
**Tool:** Wireshark  
**Topic:** Capture Filters & Display Filters  
**Date:** 28 July 2026

---

# Overview

Wireshark uses two different types of filters:

| Filter Type | Purpose | Applied |
|-------------|---------|---------|
| **Capture Filter** | Captures only specific packets before they are recorded. | Before starting packet capture |
| **Display Filter** | Displays only selected packets from an existing capture. | After packet capture |

---

# Capture Filters

Capture filters reduce the amount of traffic captured by specifying what should be recorded.

---

## Capture Traffic to or from a Specific Host

```bash
host 172.18.5.4
```

Captures all traffic where:

- Source = 172.18.5.4
- Destination = 172.18.5.4

---

## Capture Traffic from a Network

CIDR notation

```bash
net 192.168.0.0/24
```

Subnet mask notation

```bash
net 192.168.0.0 mask 255.255.255.0
```

Captures all traffic within the specified network.

---

## Capture Only Source Network

```bash
src net 192.168.0.0/24
```

or

```bash
src net 192.168.0.0 mask 255.255.255.0
```

Captures packets whose **source IP** belongs to the specified network.

---

## Capture Only Destination Network

```bash
dst net 192.168.0.0/24
```

or

```bash
dst net 192.168.0.0 mask 255.255.255.0
```

Captures packets whose **destination IP** belongs to the specified network.

---

## Capture DNS Traffic

```bash
port 53
```

Captures only DNS packets.

---

## Capture Everything Except HTTP and SMTP

```bash
host www.example.com and not (port 80 or port 25)
```

Equivalent expression:

```bash
host www.example.com and not port 80 and not port 25
```

---

## Capture Everything Except DNS and ARP

```bash
port not 53 and not arp
```

Useful for removing common network noise.

---

## Capture a Range of TCP Ports

```bash
tcp portrange 1501-1549
```

Captures traffic between TCP ports **1501** and **1549**.

---

## Capture Only IPv4 Traffic

```bash
ip
```

Useful for filtering out protocols such as:

- ARP
- STP

---

## Capture Only Unicast Traffic

```bash
not broadcast and not multicast
```

Removes broadcast and multicast traffic from the capture.

---

# Display Filters

Display filters are used after packets have already been captured.

---

## Show SMTP and ICMP Traffic

```text
tcp.port == 25 or icmp
```

Displays:

- SMTP packets
- ICMP packets

---

## Show Only Internal LAN Traffic

```text
ip.src == 192.168.0.0/16 and ip.dst == 192.168.0.0/16
```

Displays only communication occurring within the LAN.

---

## Detect TCP Receive Window Full

```text
tcp.window_size == 0 && tcp.flags.reset != 1
```

Meaning:

- Receiver's TCP buffer is full.
- Sender is instructed to temporarily stop sending data.
- Ignores TCP Reset packets.

---

## Filter by Protocol While Excluding Specific IP Addresses

Example:

```text
ip.src != xxx.xxx.xxx.xxx &&
ip.dst != xxx.xxx.xxx.xxx &&
sip
```

Displays only SIP traffic while excluding packets involving the specified IP address.

---

# Important Wireshark Filter Fields

Some display filter fields automatically match both source and destination values.

---

## ip.addr

```text
ip.addr == 10.43.54.65
```

Equivalent to:

```text
ip.src == 10.43.54.65
or
ip.dst == 10.43.54.65
```

It matches either the source or destination IP.

---

## tcp.port

Similarly,

```text
tcp.port == 80
```

matches:

- Source Port 80
- Destination Port 80

---

## udp.port

Matches both:

- Source UDP Port
- Destination UDP Port

---

## eth.addr

Matches:

- Source MAC Address
- Destination MAC Address

---

# Common Mistake with "!="

Many beginners write:

```text
ip.addr != 10.43.54.65
```

This does **not** completely exclude traffic involving that IP.

Instead, Wireshark interprets it as:

```text
ip.src != 10.43.54.65
or
ip.dst != 10.43.54.65
```

This may still allow packets where one side matches the IP.

---

# Correct Way to Exclude an IP

Use:

```text
!(ip.addr == 10.43.54.65)
```

Equivalent to:

```text
!(ip.src == 10.43.54.65
or
ip.dst == 10.43.54.65)
```

This correctly removes **all** packets involving that IP address.

---

# Commonly Used Filters

| Purpose | Filter |
|---------|--------|
| Specific Host | `host 172.18.5.4` |
| Network | `net 192.168.0.0/24` |
| Source Network | `src net 192.168.0.0/24` |
| Destination Network | `dst net 192.168.0.0/24` |
| DNS | `port 53` |
| IPv4 Only | `ip` |
| Exclude Broadcast | `not broadcast and not multicast` |
| TCP Port Range | `tcp portrange 1501-1549` |
| SMTP or ICMP | `tcp.port == 25 or icmp` |
| LAN Only | `ip.src==192.168.0.0/16 and ip.dst==192.168.0.0/16` |
| TCP Window Full | `tcp.window_size == 0 && tcp.flags.reset != 1` |

---
