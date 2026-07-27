# TryHackMe - Traffic Analysis Essentials

**Platform:** TryHackMe  
**Room:** Traffic Analysis Essentials  
**Module:** Network Security  
**Date:** 27 July 2026

---

# Overview

This room introduces the fundamentals of **Network Security** and **Network Traffic Analysis (NTA)**. It explains how organizations protect their networks using different security controls, how network traffic is analyzed to detect attacks, and the differences between flow analysis and packet analysis.

Traffic Analysis is one of the core skills for SOC analysts because network traffic provides valuable evidence during incident investigations and threat hunting.

---

# Network Security and Network Data

## What is Network Security?

Network Security is the practice of protecting:

- Data
- Applications
- Systems
- Devices
- Network Infrastructure

Its primary goals are:

- Confidentiality
- Integrity
- Availability
- Reliability

---

# Network Security Control Levels

There are three primary security control levels.

| Control Level | Purpose |
|--------------|---------|
| **Physical** | Protect networking devices, cables, racks, and hardware from unauthorized physical access. |
| **Technical** | Protect network communications and data using technologies such as encryption, VPNs, and firewalls. |
| **Administrative** | Establish security policies, user access levels, authentication processes, and operational procedures. |

### Answer

**Which Security Control Level covers creating security policies?**

```
Administrative
```

---

# Main Network Security Approaches

Network Security consists of two major approaches.

## 1. Access Control

Ensures only authorized users and devices can access network resources.

### Common Access Control Technologies

### Firewall

- Controls incoming and outgoing traffic
- Blocks malicious traffic
- Allows legitimate traffic

---

### Network Access Control (NAC)

Checks whether a device complies with security requirements before allowing network access.

---

### Identity and Access Management (IAM)

Manages:

- User identities
- Authentication
- Authorization

---

### Load Balancing

Distributes workloads across multiple servers.

Benefits:

- Improved performance
- Better resource utilization
- High availability

### Answer

```
Load Balancing
```

---

### Network Segmentation

Divides a network into smaller segments.

Benefits:

- Improves security
- Limits attacker movement
- Protects sensitive assets

---

### Virtual Private Network (VPN)

Creates encrypted communication channels between devices.

Common use:

- Secure remote access

---

### Zero Trust

Core principle:

> Never Trust, Always Verify

Users receive only the minimum permissions required.

---

# 2. Threat Control

Focuses on detecting and preventing attacks.

---

## Intrusion Detection & Prevention

### IDS

- Detects attacks
- Generates alerts

### IPS

- Detects attacks
- Blocks malicious traffic automatically

---

## Data Loss Prevention (DLP)

Monitors traffic to prevent sensitive data from leaving the organization.

---

## Endpoint Protection

Protects endpoints using:

- Antivirus
- Anti-malware
- Encryption
- DLP
- IDS/IPS

---

## Cloud Security

Protects cloud resources through:

- Encryption
- VPNs
- Security controls

---

## SIEM

Security Information and Event Management

Functions:

- Log collection
- Event correlation
- Alert generation
- Incident monitoring

---

## SOAR

Security Orchestration, Automation and Response

Functions:

- Automates security workflows
- Coordinates multiple security tools
- Improves incident response

### Answer

```
SOAR
```

---

## Network Detection & Response (NDR)

Analyzes network traffic to identify:

- Threats
- Anomalies
- Suspicious behavior

---

# Network Security Operations

Typical network security operations include:

| Phase | Activities |
|--------|------------|
| Deployment | Install devices and software |
| Configuration | Configure security policies, NAT, VPNs |
| Management | Threat mitigation and automation |
| Monitoring | User activity, logs, traffic analysis |
| Maintenance | Updates, patches, rule tuning |

---

# Managed Security Services (MSS)

Organizations often outsource security operations to Managed Security Service Providers (MSSPs).

Common MSS services include:

- Network Penetration Testing
- Vulnerability Assessment
- Incident Response
- Behavioral Analysis

---

# Traffic Analysis

## What is Traffic Analysis?

Traffic Analysis is the process of:

- Capturing network traffic
- Monitoring communications
- Recording packets
- Analyzing network behavior

Its objectives are:

- Detect anomalies
- Detect attacks
- Investigate incidents
- Improve network performance

---

# Where is Traffic Analysis Used?

Traffic Analysis supports several security disciplines.

- Packet Analysis (Wireshark)
- Network Monitoring (Zeek)
- IDS/IPS (Snort, Suricata)
- Network Forensics (NetworkMiner)
- Threat Hunting (Brim)

---

# Types of Traffic Analysis

## 1. Flow Analysis

Collects metadata about communications.

Examples:

- Source IP
- Destination IP
- Ports
- Number of packets
- Session duration

### Advantages

- Fast
- Easy to analyze
- Requires less storage

### Limitations

- No packet contents
- Cannot fully explain an attack

---

## 2. Packet Analysis (Deep Packet Inspection)

Captures the complete packet.

Includes:

- Headers
- Payload
- Protocol information

### Advantages

- Complete visibility
- Better root-cause analysis
- Detects sophisticated attacks

### Limitations

- Requires more storage
- More time-consuming
- Requires skilled analysts

---

# Flow Analysis vs Packet Analysis

| Flow Analysis | Packet Analysis |
|--------------|----------------|
| Metadata only | Complete packets |
| Fast | Detailed |
| Low storage | High storage |
| Limited investigation | Full investigation |
| Statistical analysis | Deep Packet Inspection (DPI) |

---

# Benefits of Traffic Analysis

Traffic analysis provides:

- Complete network visibility
- Asset discovery
- Baseline creation
- Threat detection
- Incident investigation
- Performance monitoring
- Network troubleshooting

---

# Why Traffic Analysis Still Matters

Although much internet traffic is encrypted, traffic analysis remains valuable because analysts can still observe:

- Communication patterns
- Connection frequency
- Traffic volume
- Timing
- Destination servers
- Protocol usage

Even encrypted traffic can reveal suspicious behavior.

---

# Practical Exercise

The room includes interactive firewall exercises.

## Exercise 1

Objective:

Block the **two malicious source IP addresses** attempting to compromise the server.

The suspicious hosts identified were:

```
10.10.99.99
10.10.99.62
```

These systems generated alerts such as:

- Metasploit Traffic
- Bad Traffic
- Multiple Login Attempts

---

## Exercise 2

Objective:

Block the **destination ports** used by the malicious services.

The ports to filter were:

```
21
2222
7777
```

These represent services associated with suspicious traffic destined for the server.

---

# Questions & Answers

| Question | Answer |
|----------|--------|
| Which security control level creates security policies? | Administrative |
| Which access control element manages traffic using data metrics? | Load Balancing |
| Which technology correlates different tool outputs? | SOAR |

---
