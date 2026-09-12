# Man-in-the-Middle Detection

**Platform:** TryHackMe\
**Room:** Man-in-the-Middle Detection\
**Date:** 12 September 2026\
**Focus:** MITM attacks, ARP spoofing, DNS spoofing, SSL stripping, and
Wireshark detection

------------------------------------------------------------------------

## My Notes

This room focused on **Man-in-the-Middle (MITM)** attacks and how to
detect them from network traffic.

A MITM attack happens when an attacker places themselves between two
legitimate communication endpoints. The attacker can then intercept,
monitor, modify, or redirect traffic.

The main attack chain I investigated was:

``` text
ARP Spoofing
     ↓
DNS Spoofing
     ↓
SSL Stripping
     ↓
Plaintext Credential Capture
```

------------------------------------------------------------------------

# Task 1 --- Introduction

A MITM attack allows an attacker to secretly position themselves between
two communicating parties.

The attacker may:

-   Intercept traffic
-   Read sensitive information
-   Modify traffic
-   Redirect traffic
-   Inject malicious content
-   Capture credentials

From a SOC perspective, detecting MITM attacks requires looking at
multiple layers, including network traffic, ARP behaviour, DNS
responses, TLS/SSL traffic, certificates, and communication patterns.

------------------------------------------------------------------------

# Task 3 --- MITM Attacks: An Overview

## How MITM Attacks Work

MITM attacks generally involve two stages:

### 1. Interception

The attacker inserts themselves into the communication path using
techniques such as:

``` text
ARP spoofing
DNS spoofing
IP spoofing
Rogue Wi-Fi
```

### 2. Manipulation / Decryption

Once positioned in the middle, the attacker may:

-   Read traffic
-   Modify requests/responses
-   Redirect users
-   Downgrade encrypted connections
-   Inject malicious content
-   Capture credentials

## Common MITM Types

-   **Packet sniffing:** Capturing unencrypted packets.
-   **Session hijacking:** Stealing session tokens.
-   **SSL stripping:** Downgrading HTTPS to HTTP.
-   **DNS spoofing:** Sending forged DNS responses.
-   **IP spoofing:** Making traffic appear to come from a trusted IP.
-   **Rogue Wi-Fi:** Creating a fake wireless network.

------------------------------------------------------------------------

# MITM and the Cyber Kill Chain

The Cyber Kill Chain phases covered in the room are:

``` text
Reconnaissance
      ↓
Weaponization
      ↓
Delivery
      ↓
Exploitation
      ↓
Installation
      ↓
Command & Control
      ↓
Actions on Objectives
```

MITM can be useful during the **Exploitation** and **Installation**
phases.

For example, after establishing a MITM position, an attacker can use the
traffic path to inject malicious content or deliver additional payloads.

------------------------------------------------------------------------

# Task 4 --- Detecting ARP Spoofing

## What is ARP?

ARP stands for **Address Resolution Protocol**.

It maps:

``` text
IP Address → MAC Address
```

A device can ask:

``` text
Who has this IP?
```

and the device owning that IP responds with its MAC address.

## What is ARP Spoofing?

ARP has no authentication, so an attacker can send forged ARP replies.

For example, the attacker can claim:

``` text
192.168.10.1 is at ATTACKER_MAC
```

when `192.168.10.1` is actually the gateway.

If the victim accepts this mapping, traffic intended for the gateway can
pass through the attacker.

------------------------------------------------------------------------

## ARP Spoofing Indicators

I looked for:

-   Multiple MAC addresses associated with one IP
-   Unsolicited ARP replies
-   High ARP traffic volume
-   Repeated gateway advertisements
-   Suspicious MAC addresses claiming the gateway IP
-   Duplicate IP-to-MAC mappings
-   Traffic being redirected through an unexpected MAC

------------------------------------------------------------------------

## Network Information

The investigated network contained:

  Role                     Information
  ------------------------ ------------------------------
  Gateway                  `192.168.10.1`
  Legitimate Gateway MAC   `02:aa:bb:cc:00:01`
  Domain                   `corp-login.acme-corp.local`

------------------------------------------------------------------------

# Wireshark ARP Investigation

The PCAP was:

``` text
network-traffic.pcap
```

in the:

``` text
mitm_traffic
```

folder.

## Show ARP Traffic

``` text
arp
```

## Show ARP Requests

``` text
arp.opcode == 1
```

## Show ARP Replies

``` text
arp.opcode == 2
```

## Find Gratuitous ARP

``` text
arp.isgratuitous
```

## Check Legitimate Gateway Traffic

``` text
arp && arp.src.proto_ipv4 == 192.168.10.1 && eth.src == 02:aa:bb:cc:00:01
```

## Find Multiple MAC Addresses Claiming the Gateway

``` text
arp.opcode == 2 && arp.src.proto_ipv4 == 192.168.10.1
```

## Find Gateway Advertisement

``` text
arp.opcode == 2 && _ws.col.info contains "192.168.10.1 is at"
```

## Check Duplicate Address Detection

``` text
arp.duplicate-address-detected || arp.duplicate-address-frame
```

------------------------------------------------------------------------

# ARP Answers

### ARP packets from the legitimate gateway MAC

``` text
10
```

### Attacker MAC impersonating the gateway

``` text
02:fe:fe:fe:55:55
```

### Gratuitous ARP replies for `192.168.10.1`

``` text
2
```

### Unique MAC addresses claiming `192.168.10.1`

``` text
2
```

### Total ARP spoofing packets from the attacker

``` text
14
```

------------------------------------------------------------------------

# Task 5 --- Unmasking DNS Spoofing

## What is DNS Spoofing?

DNS translates domain names into IP addresses.

DNS spoofing happens when an attacker sends a forged DNS response and
redirects the victim to an attacker-controlled IP.

The attack can look like:

``` text
Victim
  ↓
DNS Query
  ↓
Legitimate DNS + Forged Response
  ↓
Victim
  ↓
Attacker IP
```

In this room, DNS spoofing followed the ARP spoofing stage.

------------------------------------------------------------------------

## DNS Spoofing Indicators

I learned to look for:

-   Multiple DNS responses for the same query
-   Responses from an unexpected DNS source
-   Suspiciously short TTL values
-   Unsolicited DNS responses

The strongest indicator here was a response from a source other than the
legitimate DNS server.

------------------------------------------------------------------------

# Wireshark DNS Investigation

## Show DNS Traffic

``` text
dns
```

## Show Legitimate Responses

The legitimate DNS server was:

``` text
8.8.8.8
```

Filter:

``` text
dns.flags.response == 1 && ip.src == 8.8.8.8
```

## Show All DNS Responses

``` text
dns.flags.response == 1
```

## Investigate the Target Domain

``` text
dns && dns.qry.name == "corp-login.acme-corp.local"
```

## Check Legitimate Responses for the Domain

``` text
dns.flags.response == 1 && ip.src == 8.8.8.8 && dns.qry.name == "corp-login.acme-corp.local"
```

## Find Responses from Other Sources

``` text
dns.flags.response == 1 && ip.src != 8.8.8.8 && dns.qry.name == "corp-login.acme-corp.local"
```

The forged DNS response redirected the domain to:

``` text
192.168.10.55
```

------------------------------------------------------------------------

# DNS Answers

### DNS responses for `corp-login.acme-corp.local`

``` text
211
```

### DNS responses from IPs other than `8.8.8.8`

``` text
2
```

### IP returned by the attacker's forged DNS response

``` text
192.168.10.55
```

------------------------------------------------------------------------

# Attack Chain So Far

At this point I could correlate:

``` text
ARP Spoofing
     ↓
Attacker impersonates gateway
192.168.10.1
     ↓
DNS Spoofing
     ↓
corp-login.acme-corp.local
     ↓
192.168.10.55
     ↓
SSL Stripping
```

This correlation gave much stronger evidence than investigating each
event separately.

------------------------------------------------------------------------

# Task 6 --- Spotting SSL Stripping in Action

## What is SSL Stripping?

SSL stripping is a MITM technique where an attacker interferes with an
HTTPS connection and causes the victim to communicate using HTTP.

The attacker can maintain HTTPS communication with the real server while
the victim communicates with the attacker over HTTP.

``` text
Victim
  |
  | HTTP
  ↓
Attacker
  |
  | HTTPS
  ↓
Real Server
```

Because the victim's side is unencrypted, sensitive information can
potentially be captured.

------------------------------------------------------------------------

## SSL Stripping Indicators

I looked for:

-   HTTPS traffic followed by HTTP traffic
-   HTTP requests to a service that should use HTTPS
-   Redirects from HTTPS to HTTP
-   Certificate problems in some scenarios
-   Sensitive information appearing in plaintext HTTP

The key indicator in this room was plaintext HTTP communication after
DNS spoofing.

------------------------------------------------------------------------

# Wireshark SSL Stripping Investigation

## Show TLS/SSL Traffic

``` text
tls || ssl
```

## Confirm the Domain Uses TLS

``` text
tls.handshake.type == 1 && tls.handshake.extensions_server_name == "corp-login.acme-corp.local"
```

## Show the Attacker's Forged DNS Response

``` text
dns.flags.response == 1 && ip.src == 192.168.10.55 && dns.qry.name == "corp-login.acme-corp.local"
```

## Check HTTP Traffic Between Victim and Attacker

``` text
http && ip.src == 192.168.10.10 && ip.dst == 192.168.10.55
```

This showed that the victim was communicating with the attacker's IP
over HTTP.

## Find the Credential POST

``` text
http.request.method == "POST" && http.host == "corp-login.acme-corp.local"
```

There was one POST request. I followed the HTTP stream and found the
victim's credentials in plaintext.

For this public-facing README, I have intentionally redacted the lab
password.

------------------------------------------------------------------------

# SSL Stripping Answers

### POST requests for `corp-login.acme-corp.local`

``` text
1
```

### Victim password

``` text
[REDACTED — LAB CREDENTIAL]
```

The password was visible in plaintext in the HTTP stream after following
the POST request.

------------------------------------------------------------------------

# Task 7 --- Conclusion and Room Wrap-Up

The room demonstrated a complete MITM attack where several techniques
were chained together.

The attack timeline was:

``` text
ARP Spoofing
     ↓
Attacker poisons gateway mapping
     ↓
DNS Spoofing
     ↓
Victim is redirected to attacker IP
     ↓
SSL Stripping
     ↓
HTTPS is downgraded to HTTP
     ↓
Credential POST observed
     ↓
Credentials captured in plaintext
```

------------------------------------------------------------------------

# Detection Cheatsheet

## ARP Spoofing

Look for:

``` text
Multiple MAC addresses → Same IP
```

Useful filters:

``` text
arp
```

``` text
arp.opcode == 2
```

``` text
arp.isgratuitous
```

``` text
arp.duplicate-address-detected || arp.duplicate-address-frame
```

## DNS Spoofing

Look for:

``` text
Multiple/conflicting DNS responses
```

Useful filter:

``` text
dns.flags.response == 1 && ip.src != 8.8.8.8
```

For the target domain:

``` text
dns.flags.response == 1 && ip.src != 8.8.8.8 && dns.qry.name == "corp-login.acme-corp.local"
```

## SSL Stripping

Look for:

``` text
HTTPS expected
      ↓
HTTP appears
      ↓
Sensitive data in plaintext
```

Useful filter:

``` text
http && ip.src == 192.168.10.10 && ip.dst == 192.168.10.55
```

POST detection:

``` text
http.request.method == "POST" && http.host == "corp-login.acme-corp.local"
```

------------------------------------------------------------------------

# Final Answers

  Task   Question                                  Answer
  ------ ----------------------------------------- -------------------------------
  4      ARP packets from legitimate gateway MAC   `10`
  4      Attacker MAC impersonating gateway        `02:fe:fe:fe:55:55`
  4      Gratuitous ARP replies                    `2`
  4      MAC addresses claiming gateway IP         `2`
  4      ARP spoofing packets from attacker        `14`
  5      DNS responses for target domain           `211`
  5      Responses from non-legitimate DNS IPs     `2`
  5      Forged DNS response IP                    `192.168.10.55`
  6      POST requests for target domain           `1`
  6      Victim password                           `[REDACTED — LAB CREDENTIAL]`

------------------------------------------------------------------------

# What I Learned

### 1. ARP has no authentication

Because ARP trusts replies, attackers can associate their MAC address
with another device's IP.

### 2. Duplicate IP-to-MAC mappings are important

If the gateway IP appears to belong to multiple MAC addresses, I should
investigate.

### 3. DNS spoofing can redirect victims

A forged DNS response can send a victim to an attacker-controlled IP.

### 4. Unexpected DNS responders are suspicious

I should compare DNS response sources with the organization's legitimate
DNS infrastructure.

### 5. SSL stripping can expose plaintext credentials

If a service should use HTTPS but sensitive information is being sent
over HTTP, that is a serious indicator.

### 6. Correlation is the key

The strongest evidence in this room came from connecting:

``` text
ARP Spoofing
    +
DNS Spoofing
    +
HTTP instead of HTTPS
    +
Plaintext credentials
```

Together these showed a complete MITM attack.

------------------------------------------------------------------------

# SOC Investigation Mindset

When investigating a possible MITM attack, I can follow this process:

``` text
1. Check for unexpected MAC addresses
              ↓
2. Check duplicate IP-to-MAC mappings
              ↓
3. Look for unexpected DNS responders
              ↓
4. Check for conflicting DNS answers
              ↓
5. Look for HTTPS → HTTP downgrade
              ↓
6. Check for plaintext sensitive data
              ↓
7. Correlate the events into one attack chain
```

------------------------------------------------------------------------
