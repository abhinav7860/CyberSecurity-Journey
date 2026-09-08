# TryHackMe - Wireshark: Packet Operations

**Date:** 2026-09-08  
**Platform:** TryHackMe  
**Room:** Wireshark: Packet Operations  
**Tool:** Wireshark

---

## Introduction

I continued my Wireshark learning with the **Wireshark: Packet Operations** room. This room went beyond the basic packet inspection I learned in **Wireshark: The Basics** and focused more on using Wireshark's statistics, protocol information, filtering, advanced operators, profiles, and filtering buttons.

The main idea I took from this room is that a large PCAP can contain a huge amount of traffic, so manually checking every packet is not practical. Wireshark gives me different ways to reduce that noise and focus on the traffic that matters during an investigation.

I worked with the `Exercise.pcapng` capture throughout the room.

---

# Task 2 - Statistics | Summary

The Statistics menu is useful when I first want to understand the overall capture instead of immediately investigating individual packets.

I can access these options from:

```text
Statistics
```

The statistics provide information about hosts, protocols, conversations, endpoints and other details in the capture. This is useful for building an initial understanding of what is happening in the network.

## Resolved Addresses

The **Resolved Addresses** option shows IP addresses and the hostnames associated with them. The hostname information can come from DNS answers contained in the capture.

I can open it using:

```text
Statistics → Resolved Addresses
```

This is useful because it can quickly show me which domains or hosts were contacted.

## Protocol Hierarchy

The **Protocol Hierarchy** view breaks the capture down into the protocols it contains. It shows protocols in a tree structure together with packet counts and percentages.

```text
Statistics → Protocol Hierarchy
```

This gives me a quick overview of the types of traffic present in the PCAP.

## Conversations

A conversation represents traffic exchanged between two endpoints.

```text
Statistics → Conversations
```

Wireshark provides conversation information for Ethernet, IPv4, IPv6, TCP and UDP.

This is useful when I want to identify which hosts are communicating and how much traffic is being exchanged.

## Endpoints

The **Endpoints** option shows unique endpoints from the capture.

```text
Statistics → Endpoints
```

Wireshark can also resolve known MAC addresses to manufacturer names, which can provide a useful clue about the device or vendor involved.

## Name Resolution

Wireshark supports name resolution for IP addresses, ports and MAC addresses.

```text
Edit → Preferences → Name Resolution
```

Wireshark can also use GeoIP/MaxMind databases to provide geographical information for IP addresses. The TryHackMe lab does not have an active Internet connection, so the GeoIP map cannot be used normally in the lab.

## Task 2 Answers

### IP address of the hostname starting with `bbc`

```text
199.232.24.81
```

### Number of IPv4 conversations

```text
435
```

### Bytes (k) transferred from the `Micro-St` MAC address

```text
7474
```

### Number of IP addresses linked with `Kansas City`

```text
4
```

### IP address linked with `Blicnet` AS Organisation

```text
188.246.82.7
```

---

# Task 3 - Statistics | Protocol Details

This task focused on protocol-specific statistics. Instead of looking at all traffic together, Wireshark allows me to focus on IPv4, IPv6, DNS and HTTP traffic separately.

## IPv4 and IPv6 Statistics

Wireshark has separate statistics for IPv4 and IPv6.

```text
Statistics → IPv4 Statistics
Statistics → IPv6 Statistics
```

This is useful when an investigation requires me to concentrate on one version of IP traffic.

## DNS Statistics

DNS statistics provide a breakdown of DNS activity in the capture.

```text
Statistics → DNS
```

I can use this to investigate DNS queries, responses, query types, response codes and other DNS activity.

This can be useful during investigations because DNS requests can reveal which domains a system attempted to access.

## HTTP Statistics

HTTP statistics provide a summary of HTTP activity.

```text
Statistics → HTTP
```

This can help identify HTTP requests, responses and hosts without manually checking every HTTP packet.

## Task 3 Answers

### Most used IPv4 destination address

```text
10.100.1.33
```

### Maximum DNS service request-response time

```text
0.467897
```

### HTTP Requests made by `rad[.]msn[.]com`

```text
39
```

---

# Task 4 - Packet Filtering | Principles

This task introduced the two major types of Wireshark filters:

1. Capture filters
2. Display filters

Understanding the difference between these is important because they are used at different stages of packet analysis.

## Capture Filters

A capture filter is used when traffic is being captured. It determines which packets should be captured in the first place.

Example:

```text
tcp port 80
```

This captures TCP traffic associated with port 80.

Capture filters should be planned carefully because traffic that is not captured cannot be investigated later from that capture.

## Display Filters

Display filters work on packets that are already present in the capture and only control which packets are currently displayed.

Example:

```text
tcp.port == 80
```

This displays packets involving TCP port 80 from the existing capture.

The important difference I learned is:

> Capture filters decide what gets captured, while display filters decide what gets displayed.

I should not confuse the syntax between the two.

## Comparison Operators

Wireshark display filters support several comparison operators.

| Operator | Meaning |
|---|---|
| `==` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

Example:

```text
ip.src == 10.10.10.100
```

Another example:

```text
ip.ttl < 10
```

## Logical Operators

Wireshark also supports:

```text
AND / &&
OR / ||
NOT / !
```

Example:

```text
(ip.src == 10.10.10.100) OR (ip.src == 10.10.10.111)
```

The filter bar uses colours to show filter status:

- Green = valid
- Red = invalid
- Yellow = warning/unreliable

---

# Task 5 - Packet Filtering | Protocol Filters

This task focused on filtering traffic using protocol-specific fields.

## IP Filters

```text
ip
```

Shows IP packets.

```text
ip.addr == 10.10.10.111
```

Shows packets containing the specified IP.

```text
ip.src == 10.10.10.111
```

Shows packets originating from the IP.

```text
ip.dst == 10.10.10.111
```

Shows packets sent to the IP.

An important difference I learned is that `ip.addr` does not care about direction, while `ip.src` and `ip.dst` specifically identify the direction.

## TCP and UDP Filters

Examples:

```text
tcp.port == 80
udp.port == 53
tcp.srcport == 1234
tcp.dstport == 80
udp.dstport == 5353
```

These allow me to narrow traffic based on ports.

## HTTP Filters

```text
http
```

Shows HTTP traffic.

```text
http.response.code == 200
```

Shows HTTP responses with status code 200.

```text
http.request.method == "GET"
```

Shows HTTP GET requests.

```text
http.request.method == "POST"
```

Shows HTTP POST requests.

## DNS Filters

```text
dns
```

Shows DNS traffic.

```text
dns.flags.response == 0
```

Shows DNS requests.

```text
dns.flags.response == 1
```

Shows DNS responses.

```text
dns.qry.type == 1
```

Shows DNS A-record queries.

## Display Filter Expressions

I don't need to memorise every Wireshark filter.

The **Display Filter Expression** option provides the available protocol fields and accepted values.

```text
Analyze → Display Filter Expression
```

This is useful when I know what I want to investigate but don't remember the exact filter syntax.

## Task 5 Answers

### Number of IP packets

```text
81420
```

### Packets with TTL less than 10

```text
66
```

### Packets using TCP port 4444

```text
632
```

### HTTP GET requests sent to port 80

```text
527
```

### Type A DNS queries

```text
51
```

---

# Task 6 - Advanced Filtering

This task introduced more advanced display filter operators and functions.

## `contains`

The `contains` operator searches for a value inside a field.

```text
http.server contains "Apache"
```

This searches HTTP server fields containing `Apache`.

`contains` is case-sensitive.

## `matches`

The `matches` operator can be used with regular expressions.

```text
http.host matches "\.(php|html)"
```

This can find HTTP hosts containing `.php` or `.html`.

## `in`

The `in` operator checks whether a value belongs to a set of values.

```text
tcp.port in {80 443 8080}
```

This finds TCP packets using ports 80, 443 or 8080.

## `upper`

The `upper()` function converts a string to uppercase.

```text
upper(http.server) contains "APACHE"
```

## `lower`

The `lower()` function converts a string to lowercase.

```text
lower(http.server) contains "apache"
```

## `string`

The `string()` function converts a value into a string.

Example:

```text
string(frame.number) matches "[13579]$"
```

This allows string/regex operations on values that are normally numeric.

---

# Bookmarks and Filtering Buttons

Wireshark allows filters to be saved as **bookmarks** or **filter buttons**.

This is useful because during an investigation I may repeatedly use the same filter. Instead of typing it every time, I can save it and apply it quickly.

This becomes especially useful when working with long or complicated display filters.

---

# Profiles

Wireshark profiles allow me to save different configurations for different investigation scenarios.

A profile can contain things such as:

- Display settings
- Colouring rules
- Filter buttons
- Preferences
- Other Wireshark configuration

I can manage profiles from:

```text
Edit → Configuration Profiles
```

This is useful because I can create a configuration for one investigation and switch to another profile without manually changing everything again.

---

# Task 6 Answers

## 1. Microsoft IIS servers - packets not originating from port 80

I filtered the Microsoft IIS server traffic and then checked the packets that were not originating from port 80.

**Answer:**

```text
21
```

## 2. Microsoft IIS servers - packets with version 7.5

I checked the IIS server version information and filtered for version `7.5`.

**Answer:**

```text
71
```

## 3. Packets using ports 3333, 4444 or 9999

I used the `in` operator:

```text
tcp.port in {3333 4444 9999}
```

**Answer:**

```text
2235
```

## 4. Packets with even TTL numbers

I used:

```text
string(ip.ttl) matches "[02468]$"
```

Here `ip.ttl` gets the TTL, `string()` converts it to text, and `[02468]$` checks whether the last digit is even.

**Answer:**

```text
77289
```

## 5. Bad TCP Checksum packets

I changed the Wireshark profile:

```text
Edit → Configuration Profiles → Checksum Control
```

Then I checked the packets marked with bad TCP checksums.

**Answer:**

```text
34185
```

## 6. Existing filtering button

I used the existing:

```text
gif/jpeg with http-200
```

filtering button.

The filter applied was:

```text
(http.response.code == 200) && (http.content_type matches "image(gif||jpeg)")
```

After applying it, I checked the **Displayed** packet count.

**Answer:**

```text
261
```

---

# Important Filters to Remember

These are the filters from this room that I want to remember for future investigations:

```text
ip
ip.addr == 10.10.10.111
ip.src == 10.10.10.111
ip.dst == 10.10.10.111

tcp.port == 80
udp.port == 53
tcp.srcport == 1234
tcp.dstport == 80

http
http.response.code == 200
http.request.method == "GET"
http.request.method == "POST"

dns
dns.flags.response == 0
dns.flags.response == 1
dns.qry.type == 1

ip.ttl < 10
tcp.port in {80 443 8080}

http.server contains "Apache"
http.host matches "\.(php|html)"

upper(http.server) contains "APACHE"
lower(http.server) contains "apache"

string(frame.number) matches "[13579]$"
string(ip.ttl) matches "[02468]$"
```

---

# What I Learned

This room made me more comfortable with using Wireshark for actual investigation rather than just looking at individual packets.

The first important thing I learned was how useful the **Statistics** menu can be. Instead of immediately opening individual packets, I can first check resolved addresses, protocol hierarchy, conversations, endpoints and protocol-specific statistics. This gives me an idea of what is happening inside the capture.

The second major thing was **packet filtering**. A PCAP can contain a very large number of packets, so looking at everything at once creates a lot of noise. Display filters allow me to narrow the investigation down to the traffic that matters.

I also understood the difference between **capture filters and display filters**. Capture filters affect what is captured, while display filters work on traffic that has already been captured.

Another useful part was learning advanced filtering. Operators such as `contains`, `matches` and `in` make it possible to search for patterns and multiple values more efficiently. Functions such as `upper()`, `lower()` and `string()` give me more control when the field type or letter case makes a normal filter difficult.

The room also showed me that I don't have to memorise every possible Wireshark filter. The **Display Filter Expression** feature can help me find the correct field and construct filters.

Finally, I learned about **filter buttons, bookmarks and profiles**. These can save time during repeated investigations because I can store commonly used filters and configurations instead of recreating them every time.

Overall, this room helped me move from simply reading packets to thinking more like an analyst: **understand the capture, reduce the noise, identify interesting traffic, filter it, and then investigate the relevant packets.**
