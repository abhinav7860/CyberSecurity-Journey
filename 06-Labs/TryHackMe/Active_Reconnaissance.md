# Active Reconnaissance

**Platform:** TryHackMe  
**Module:** Network Security  
**Date:** 10 July 2026

---

# Objective

In this room, I learned about **Active Reconnaissance**, where information is gathered by directly interacting with the target. Unlike passive reconnaissance, active recon sends packets, makes network connections, and communicates with services, making it easier for defenders to detect.

This room introduced tools like browsers, ping, traceroute, telnet, and netcat that are commonly used during the initial phase of a penetration test.

---

# What is Active Reconnaissance?

Active reconnaissance is the process of directly communicating with a target to gather information.

Examples include:

- Visiting websites
- Pinging hosts
- Tracing network routes
- Connecting to open ports
- Banner grabbing
- Service enumeration

Since packets are sent to the target, these activities can be logged or detected.

---

# Passive vs Active Recon

## Passive Reconnaissance

- No direct interaction
- Uses public information
- Difficult to detect
- Low risk

Examples:

- WHOIS
- DNS
- Shodan
- Certificate Transparency Logs

---

## Active Reconnaissance

- Direct interaction
- Sends packets
- Easier to detect
- Higher risk

Examples:

- Ping
- Traceroute
- Telnet
- Netcat
- Nmap

---

# Browser as a Recon Tool

A normal web browser is one of the safest tools for reconnaissance because web traffic looks like normal user traffic.

Useful Developer Tool sections:

## Network

Shows:

- Request Headers
- Response Headers
- Cookies
- Status Codes
- Server Information

---

## Sources

Useful for finding:

- JavaScript files
- API endpoints
- Hidden directories
- Internal URLs
- Developer comments

---

## Application

Shows:

- Cookies
- Local Storage
- Session Storage
- Tokens

---

## Security

Displays:

- SSL Certificate
- Certificate Issuer
- Expiration Date
- Subject Alternative Names (SANs)

Sometimes SANs reveal additional subdomains.

---

# Browser Extensions

Some useful browser extensions for reconnaissance:

- Wappalyzer
- BuiltWith
- FoxyProxy
- User-Agent Switcher
- WhatRuns

These help identify technologies used by websites.

---

# Ping

Ping checks whether a target is reachable.

It uses:

```
ICMP Echo Request
```

and receives

```
ICMP Echo Reply
```

---

## Linux

```bash
ping -c 5 target_ip
```

---

## Windows

```cmd
ping -n 5 target_ip
```

---

## IPv4 Only

```bash
ping -4 -c 5 target_ip
```

---

## IPv6

```bash
ping -6 target_ipv6
```

---

## Practical Example

I tested

```bash
ping -c 10 MACHINE_IP
```

Result:

- 10 replies received
- Target reachable
- No packet loss

---

# Understanding TTL

TTL stands for

```
Time To Live
```

It decreases by one every time a packet passes through a router.

Common default values:

Linux

```
64
```

Windows

```
128
```

TTL values can provide clues about the target operating system.

---

# Ping Results

Successful ping means:

- Host is online
- Network is reachable
- ICMP is allowed

Possible failures:

- Firewall blocks ICMP
- Host offline
- Routing issue
- ICMP disabled

---

# Traceroute

Traceroute discovers the path packets take to reach the destination.

Unlike ping, traceroute shows every router (hop) between you and the target.

---

## Linux

```bash
traceroute target_ip
```

---

## Windows

```cmd
tracert target_ip
```

---

## TCP Mode

```bash
traceroute -T target_ip
```

---

## ICMP Mode

```bash
traceroute -I target_ip
```

---

## IPv6

```bash
traceroute -6 target_ipv6
```

---

# How Traceroute Works

Traceroute sends packets with increasing TTL values.

Example:

TTL = 1

↓

Router 1 drops packet

↓

Replies with ICMP Time Exceeded

Next packet:

TTL = 2

↓

Router 2 replies

This continues until the destination is reached.

---

# Reading Traceroute

Each numbered line represents one hop.

Sometimes

```
*
```

appears.

This usually means:

- Router blocked ICMP
- Firewall filtering
- No response received

---

## Practical Example

I observed:

- Different traceroute runs followed different paths.
- Routes can change because of load balancing and dynamic routing.
- Not every router responds to traceroute.

---

# Telnet

Telnet is an old remote administration protocol.

Default Port

```
23
```

Problem:

All communication is sent in **plain text**, including usernames and passwords.

Because of this, SSH has replaced Telnet in most environments.

---

# Banner Grabbing using Telnet

Telnet can still be useful for reconnaissance.

Example:

```bash
telnet MACHINE_IP 80
```

After connecting:

```http
GET / HTTP/1.1
Host: test
```

The server responds with information such as:

```
Server: nginx/1.6.2
```

This reveals the software running on the server.

---

## Practical Example

I learned that banner grabbing helps identify:

- Web Server
- Version Number
- HTTP Headers

These versions can later be checked for known vulnerabilities.

---

# Netcat (nc)

Netcat is one of the most useful networking tools.

It supports:

- TCP
- UDP
- Client Mode
- Server Mode
- Banner Grabbing
- File Transfer
- Simple Chat Server

---

# Connecting to a Service

```bash
nc MACHINE_IP 80
```

Like Telnet, we can manually send:

```http
GET / HTTP/1.1
Host: test
```

and inspect the response.

---

# Listening on a Port

```bash
nc -lvnp 1234
```

Options:

```
-l   Listen

-v   Verbose

-n   Numeric Mode

-p   Port Number
```

---

# Connecting to Listener

```bash
nc MACHINE_IP 1234
```

After connecting, anything typed on one terminal appears on the other.

---

# Banner Grabbing

Common ports:

HTTP

```bash
nc MACHINE_IP 80
```

FTP

```bash
nc MACHINE_IP 21
```

SMTP

```bash
nc MACHINE_IP 25
```

The goal is to identify:

- Software
- Version
- Service running

---

# Why Netcat is Better than Telnet

Netcat supports:

- TCP
- UDP
- IPv6
- Better scripting
- File transfer
- Listening mode

Modern versions also support SSL.

---

# Commands Practiced

Ping

```bash
ping -c 10 MACHINE_IP
```

Traceroute

```bash
traceroute MACHINE_IP
```

TCP Traceroute

```bash
traceroute -T MACHINE_IP
```

ICMP Traceroute

```bash
traceroute -I MACHINE_IP
```

Telnet

```bash
telnet MACHINE_IP 80
```

Netcat Client

```bash
nc MACHINE_IP 80
```

Netcat Listener

```bash
nc -lvnp 1234
```

HTTP Headers

```bash
curl -I http://MACHINE_IP
```

HTTPS Headers

```bash
curl -I https://MACHINE_IP
```

---
