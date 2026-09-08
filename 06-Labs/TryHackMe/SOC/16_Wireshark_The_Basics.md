# TryHackMe - Wireshark: The Basics

**Date:** 2026-09-08  
**Room:** Wireshark: The Basics

## Task 1 - Introduction

Wireshark is an open-source, cross-platform packet analyser used to capture and investigate network traffic and PCAP files.

I learned that it can be used for:
- Network troubleshooting
- Detecting suspicious traffic
- Investigating protocols
- Analysing packet captures

Wireshark is **not an IDS**. It mainly allows me to inspect packets, so detecting anomalies depends on my analysis.

---

# Task 2 - Tool Overview

## Main GUI Sections

| Section | Purpose |
|---|---|
| Toolbar | Capture, filter, sort, export and other actions |
| Display Filter Bar | Filter packets |
| Recent Files | Recently opened captures |
| Capture Interfaces | Available network interfaces |
| Status Bar | Capture and packet information |

## Packet Panes

**Packet List Pane** - Shows packet number, source, destination, protocol and information.

**Packet Details Panel** - Shows the protocols and fields inside the selected packet.

**Packet Bytes Pane** - Shows the raw packet in hexadecimal and ASCII.

## Other Features

### Traffic capture
```text
Blue shark → Start
Red button → Stop
Green button → Restart
```

### Merge PCAP
```text
File → Merge
```

### Capture File Properties
```text
Statistics → Capture File Properties
```

This can show the capture hash, time, comments, interface and statistics.

### Packet colouring
Colouring rules help identify protocols and unusual traffic quickly.

## Task 2 Answers

Using `Exercise.pcapng`:

**Capture file comments / flag**
```text
TryHackMe_Wireshark_Demo
```

**Total packets**
```text
58620
```

**SHA256**
```text
f446de335565fb0b0ee5e5a3266703c778b2f3dfad7efeaeccb2da5641a6d6eb
```

---

# Task 3 - Packet Dissection

Packet dissection means breaking a packet down into its protocols and fields.

A packet can be viewed roughly as:

```text
Frame
 ↓
MAC / Ethernet
 ↓
IP
 ↓
TCP / UDP
 ↓
Application Protocol
 ↓
Application Data
```

Important information includes MAC addresses, IP addresses, ports, protocol details and application data.

## Task 3 Answers

I inspected **packet 38**.

**Markup language used under HTTP**
```text
extensible markup language
```

**Arrival date**
```text
05/13/2004
```

**TTL**
```text
47
```

**TCP payload size**
```text
424
```

**E-tag**
```text
9a01a-4696-7e354b00
```

---

# Task 4 - Packet Navigation

## Go to Packet

I can jump directly to a packet using:

```text
Go → Go to Packet
```

Packet numbers make it easier to return to an event during an investigation.

## Find Packets

I can search packet contents through:

```text
Edit → Find Packet
```

Search types include:
- Display filter
- Hex
- String
- Regex

I need to choose the correct search field because the information may exist in the packet list, packet details or packet bytes.

## Mark Packets

Interesting packets can be marked using the right-click menu or **Edit**.

Marks help me keep track of important packets during the current session.

## Packet Comments

Packet comments can be added to record investigation notes and can remain in the capture file.

## Export Objects

For transferred files I can use:

```text
File → Export Objects → HTTP
```

This is useful for extracting files from HTTP traffic.

## Expert Information

I can check:

```text
Analyze → Expert Information
```

Severity levels include Chat, Note, Warn and Error.

## Task 4 Answers

### Artist 1

I searched the packet details for:

```text
r4w
```

**Artist 1:**
```text
r4w8178
```

### Packet 12 / MD5

I went to **packet 12** and read its packet comment. It pointed me to **packet 39765**.

I then:

1. Went to packet 39765.
2. Expanded **JPEG File Interchange Format**.
3. Right-clicked it.
4. Selected **Export Packet Bytes**.
5. Saved the extracted file.
6. Calculated its MD5:

```bash
md5sum <filename>
```

**MD5:**
```text
911cd574a42865a956ccde2d04495ebf
```

### TXT file

I used:

```text
File → Export Objects → HTTP
```

and found:

```text
note.txt
```

The alien's name was:

```text
packetmaster
```

### Expert Information warnings

I opened:

```text
Analyze → Expert Information
```

and checked the **Warning** count.

**Warnings:**
```text
1636
```

---

# Task 5 - Packet Filtering

Wireshark has two main filtering approaches:

**Capture filters** - limit packets while capturing.

**Display filters** - control which packets are shown during analysis.

## Apply as Filter

I can right-click a packet field and select:

```text
Apply as Filter
```

Wireshark creates the display filter automatically.

## Conversation Filter

Useful for focusing on all packets belonging to a particular conversation.

```text
Analyze → Conversation Filter
```

## Colourise Conversation

Highlights packets belonging to the same conversation without removing other packets.

## Prepare as Filter

Creates the filter without immediately applying it, allowing me to modify it first.

## Apply as Column

Adds a selected field as a column in the Packet List pane.

## Follow Stream

This reconstructs the application-level conversation.

```text
Right-click → Follow → TCP/UDP/HTTP Stream
```

It is useful for investigating requests, responses and unencrypted data such as credentials or transferred information.

## Basic Display Filters

### Protocol

```text
http
```

### TCP port

```text
tcp.port == 80
```

### UDP port

```text
udp.port == 53
```

### IP address

```text
ip.addr == 192.168.1.2
```

## Task 5 Answers

### Packet 4 - HTTP filter

I went to packet 4 and:

```text
Right-click → Hypertext Transfer Protocol → Apply as Filter
```

The filter was:

```text
http
```

**Displayed packets:**
```text
1089
```

### Packet 33790 - HTTP stream

I went to:

```text
Packet 33790
```

Then followed the HTTP stream and checked the server response.

**Total number of artists:**
```text
3
```

**Second artist:**
```text
blad3
```

---

# Useful Wireshark Workflow

When I receive a PCAP for investigation, I can follow this basic process:

```text
Open PCAP
 ↓
Check capture properties
 ↓
Check packet count / timestamps
 ↓
Inspect protocols
 ↓
Apply display filters
 ↓
Find suspicious packets
 ↓
Follow the relevant stream
 ↓
Export objects if required
 ↓
Inspect packet details and payload
 ↓
Record important evidence
```

# Final Takeaway

This room taught me the basics of using Wireshark for packet analysis.

The main things I learned were:
- Opening and inspecting PCAP files
- Understanding packet layers
- Navigating to packet numbers
- Searching packet contents
- Using display filters
- Following network streams
- Exporting transferred files
- Using Expert Information
- Checking packet comments and capture metadata

For SOC work, the important part is not just knowing filters. I need to understand what the traffic means and then use Wireshark to investigate the suspicious activity.
