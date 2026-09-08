# TryHackMe - Wireshark: Traffic Analysis

**Date:** 2026-09-08  
**Platform:** TryHackMe  
**Room:** Wireshark: Traffic Analysis  
**Tool:** Wireshark  
**Status:** Part 1 completed — Part 2 pending

---

## Introduction

I continued my Wireshark learning with the **Wireshark: Traffic Analysis** room after completing **Wireshark: The Basics** and **Wireshark: Packet Operations**.

This room moved more towards actual security investigation. Instead of only learning the interface and basic filtering, I had to identify patterns produced by network scans, ARP attacks, host discovery and tunnelling.

The main topics covered in Part 1 were:

- Nmap scans
- ARP poisoning / spoofing
- Man-in-the-Middle attacks
- DHCP, NetBIOS and Kerberos host identification
- ICMP and DNS tunnelling
- Using Wireshark filters to identify suspicious traffic

The main thing I am taking from this room is that traffic analysis is about recognising **patterns and relationships between packets**, not simply looking for one suspicious packet.

---

# Task 2 - Nmap Scans

## What I learned

Nmap is widely used for network discovery and service enumeration. Because different Nmap scan types generate different packet patterns, a SOC analyst can use Wireshark to identify possible scanning activity.

The room covered:

- TCP Connect scans
- TCP SYN scans
- UDP scans

Understanding TCP flags is important for recognising these patterns.

## Useful TCP Flag Filters

```text
tcp
udp

tcp.flags == 2
tcp.flags.syn == 1

tcp.flags == 16
tcp.flags.ack == 1

tcp.flags == 18
(tcp.flags.syn == 1) and (tcp.flags.ack == 1)

tcp.flags == 4
tcp.flags.reset == 1

tcp.flags == 20
(tcp.flags.reset == 1) and (tcp.flags.ack == 1)

tcp.flags == 1
tcp.flags.fin == 1
```

## TCP Connect Scan

A TCP Connect scan is normally performed using:

```text
nmap -sT
```

It completes the TCP three-way handshake.

For an open port, I expect:

```text
SYN
SYN, ACK
ACK
```

For a closed port:

```text
SYN
RST, ACK
```

A useful filter for identifying TCP Connect scan patterns is:

```text
tcp.flags.syn==1 and tcp.flags.ack==0 and tcp.window_size > 1024
```

## TCP SYN Scan

A SYN scan is normally performed using:

```text
nmap -sS
```

The handshake is not completed.

Open port:

```text
SYN
SYN, ACK
RST
```

Closed port:

```text
SYN
RST, ACK
```

Useful filter:

```text
tcp.flags.syn==1 and tcp.flags.ack==0 and tcp.window_size <= 1024
```

## UDP Scan

A UDP scan is normally performed using:

```text
nmap -sU
```

UDP does not use the TCP three-way handshake.

For a closed UDP port, the host can return:

```text
ICMP Type 3, Code 3
```

which means:

```text
Destination unreachable - Port unreachable
```

Useful filter:

```text
icmp.type==3 and icmp.code==3
```

## Task 2 Answers

**Total TCP Connect scans:**

```text
1000
```

**Scan type used to scan TCP port 80:**

```text
TCP connect
```

**UDP close-port messages:**

```text
1083
```

**Open UDP port in the 55-70 range:**

```text
68
```

---

# Task 3 - ARP Poisoning & Man-In-The-Middle

## What I learned

ARP, or Address Resolution Protocol, is used on a local network to associate IP addresses with MAC addresses.

ARP does not provide authentication, which means an attacker on the local network can send forged ARP messages. This can manipulate the IP-to-MAC table and redirect traffic through the attacker's machine.

This technique is known as **ARP poisoning/spoofing** and can be used to perform a **Man-in-the-Middle (MITM)** attack.

## Useful ARP Filters

```text
arp
```

ARP requests:

```text
arp.opcode == 1
```

ARP replies:

```text
arp.opcode == 2
```

Possible duplicate-address detection:

```text
arp.duplicate-address-detected
```

```text
arp.duplicate-address-frame
```

## How I Identified the Attack

The suspicious MAC address was:

```text
00:0c:29:e2:18:b4
```

It was associated with:

```text
192.168.1.25
```

but it also claimed the possible gateway address:

```text
192.168.1.1
```

The legitimate gateway MAC was:

```text
50:78:b3:f3:cd:f4
```

This meant two different MAC addresses were claiming the same IP address, which was an important ARP spoofing clue.

The suspicious MAC also generated many ARP requests against a range of IP addresses. Later, I added MAC addresses as columns to the packet list and noticed that the suspicious MAC was receiving the HTTP traffic associated with the victim.

This connected the ARP anomaly with the HTTP traffic and showed the likely MITM behaviour.

### Investigation notes

```text
Attacker:
MAC: 00:0c:29:e2:18:b4
IP: 192.168.1.25

Gateway:
MAC: 50:78:b3:f3:cd:f4
IP: 192.168.1.1

Victim:
IP: 192.168.1.12
```

The important lesson here was that looking only at IP addresses would not have been enough. Looking at MAC addresses helped reveal what was actually happening.

## Task 3 Answers

**ARP requests crafted by attacker:**

```text
[NOT PROVIDED / ADD AFTER VERIFYING]
```

**HTTP packets received by attacker:**

```text
90
```

**Sniffed username/password entries:**

```text
6
```

**Password of Client986:**

```text
clientnothere!
```

**Comment provided by Client354:**

```text
nice work!
```

---

# Task 4 - Identifying Hosts: DHCP, NetBIOS and Kerberos

## What I learned

During an investigation, an IP address alone may not tell me which machine or user is involved. DHCP, NetBIOS and Kerberos can provide additional information that helps identify hosts and users.

## DHCP

DHCP automatically assigns IP addresses and other network configuration information.

Basic filter:

```text
dhcp
```

or:

```text
bootp
```

Useful DHCP message filters:

```text
dhcp.option.dhcp == 3
```

DHCP Request

```text
dhcp.option.dhcp == 5
```

DHCP ACK

```text
dhcp.option.dhcp == 6
```

DHCP NAK

Useful options include:

- Option 12 = Hostname
- Option 50 = Requested IP
- Option 51 = Lease time
- Option 61 = Client MAC
- Option 15 = Domain name
- Option 56 = Message/rejection details

Example:

```text
dhcp.option.hostname contains "keyword"
```

## NetBIOS / NBNS

Basic filter:

```text
nbns
```

Useful search:

```text
nbns.name contains "keyword"
```

This can help identify workstation names and other NetBIOS information.

## Kerberos

Kerberos is commonly used for authentication in Windows domains.

Basic filter:

```text
kerberos
```

The `CNameString` field can contain usernames or hostnames.

To exclude computer accounts ending in `$`:

```text
kerberos.CNameString and !(kerberos.CNameString contains "$")
```

Other useful filters:

```text
kerberos.pvno == 5
```

```text
kerberos.realm contains ".org"
```

```text
kerberos.SNameString == "krbtg"
```

## Task 4 Answers

**MAC address of Galaxy A30:**

```text
9a:81:41:cb:96:6c
```

**NetBIOS registration requests from LIVALJM:**

```text
16
```

**Host that requested 172.16.13.85:**

```text
galaxy-a12
```

**IP address of user u5 (defanged):**

```text
10[.]1[.]12[.]2
```

**Hostname of the available host in Kerberos packets:**

```text
xp1$
```

---

# Task 5 - Tunnelling Traffic: DNS and ICMP

## What I learned

Traffic tunnelling is a technique where data or another protocol is carried inside a different protocol.

Attackers can abuse trusted protocols such as **ICMP** and **DNS** for command and control or data exfiltration.

This is important for a SOC analyst because these protocols are common in normal network traffic, so malicious tunnelling can be difficult to notice.

---

## ICMP Tunnelling

ICMP is normally used for network diagnostics and error reporting, such as ping.

However, ICMP packets can carry additional data. Attackers can abuse this payload to transfer data or tunnel another protocol.

Possible indicators include:

- Unusually large ICMP packets
- Large amounts of ICMP traffic
- Suspicious payloads
- Data that resembles another protocol

Useful filter:

```text
data.len > 64 and icmp
```

I opened:

```text
Desktop/exercise-pcaps/dns-icmp/icmp-tunnel.pcap
```

After filtering the large ICMP packets, I inspected the packet bytes and found SSH-related strings such as:

```text
SSH
OpenSSH
```

This showed that SSH traffic was being carried inside ICMP.

**Answer:**

```text
SSH
```

---

## DNS Tunnelling

DNS normally translates domain names into IP addresses, but attackers can abuse it to transfer information or communicate with a C2 server.

A common DNS tunnelling pattern is a long, random-looking subdomain:

```text
encoded-data.maliciousdomain.com
```

The subdomain may contain encoded data.

Useful filters:

```text
dns
```

```text
dns contains "dnscat"
```

```text
dns.qry.name.len > 15 and !mdns
```

I opened:

```text
Desktop/exercise-pcaps/dns-icmp/dns.pcap
```

Then I used:

```text
dns.qry.name.len > 15 and !mdns
```

The results contained long and unusual DNS queries.

I selected a suspicious packet and expanded:

```text
Domain Name System
→ Queries
→ Name
```

The query contained a long subdomain followed by:

```text
dataexfil.com
```

The main suspicious domain was therefore:

```text
dataexfil.com
```

Because the question required a defanged address, I changed the dot to `[.]`.

**Answer:**

```text
dataexfil[.]com
```

---

# Important Filters I Learned

## Nmap

```text
tcp.flags.syn==1 and tcp.flags.ack==0 and tcp.window_size > 1024
```

```text
tcp.flags.syn==1 and tcp.flags.ack==0 and tcp.window_size <= 1024
```

```text
icmp.type==3 and icmp.code==3
```

## ARP

```text
arp
arp.opcode == 1
arp.opcode == 2
arp.duplicate-address-detected
arp.duplicate-address-frame
```

## DHCP

```text
dhcp
dhcp.option.dhcp == 3
dhcp.option.dhcp == 5
dhcp.option.dhcp == 6
dhcp.option.hostname contains "keyword"
```

## NetBIOS

```text
nbns
nbns.name contains "keyword"
```

## Kerberos

```text
kerberos
kerberos.CNameString contains "keyword"
kerberos.CNameString and !(kerberos.CNameString contains "$")
kerberos.pvno == 5
kerberos.realm contains ".org"
kerberos.SNameString == "krbtg"
```

## ICMP Tunnelling

```text
icmp
data.len > 64 and icmp
```

## DNS Tunnelling

```text
dns
dns contains "dnscat"
dns.qry.name.len > 15 and !mdns
```

---

# What I Learned From Part 1

This part of the room helped me connect the Wireshark filtering skills from the previous rooms with real attack techniques.

For **Nmap**, I learned that different scan types produce different TCP/UDP patterns. By looking at flags, window sizes and responses, I can identify possible scanning activity.

For **ARP poisoning**, I learned that IP-to-MAC relationships are important. If multiple MAC addresses claim the same IP, I should investigate further and correlate it with the surrounding traffic.

For **host identification**, DHCP, NetBIOS and Kerberos can provide information that is not obvious from an IP address alone. This can help connect suspicious traffic to a particular machine or user.

For **tunnelling**, I learned that trusted protocols such as ICMP and DNS can be abused to hide other traffic or transfer information. Large ICMP payloads and long/random DNS queries are useful starting points for investigation.

The biggest lesson for me is that **traffic analysis is about recognising patterns and correlating evidence**. One unusual packet is not automatically an attack. I need to look at the protocol, endpoints, timing, packet contents and surrounding traffic together.

---

# Part 2 - Remaining Room Content

> **Reserved for Part 2. I will continue this same README when I send the remaining tasks.**

## Part 2 Tasks

```text
[To be added]
```

## Part 2 Investigation Notes

```text
[To be added]
```

## Part 2 Questions & Answers

```text
[To be added]
```

## Part 2 Important Filters

```text
[To be added]
```

---

# Room Progress

**Part 1:** Completed — `2026-09-08`

**Part 2:** Pending

**Overall status:** In Progress
