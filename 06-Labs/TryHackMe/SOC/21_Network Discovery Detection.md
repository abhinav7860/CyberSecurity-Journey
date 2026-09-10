# Network Discovery Detection

**Platform:** TryHackMe\
**Room:** Network Discovery Detection\
**Date:** 10 September 2026\
**Focus:** Network discovery, external/internal scanning,
horizontal/vertical scans, and scan detection

------------------------------------------------------------------------

## My Notes

This room focuses on how attackers perform **network discovery** before
exploiting a target.

The main idea I learned is that attackers need to understand their
target before they can attack it. They may look for:

-   Accessible assets
-   IP addresses
-   Open ports
-   Operating systems
-   Running services
-   Service versions
-   Vulnerable services

As a SOC analyst, I also need to understand these behaviours so I can
distinguish **legitimate scanning** from malicious reconnaissance.

------------------------------------------------------------------------

# Task 1 --- Introduction

Network discovery is often one of the first activities performed during
an attack.

A simplified attack path can look like:

``` text
Reconnaissance → Resource Development → Initial Access → Execution
                                                ↓
                                           Persistence
                                                ↓
                                        Privilege Escalation
                                                ↓
                                          Defense Evasion
                                                ↓
                                          Credential Access
                                                ↓
                                            Discovery
                                                ↓
                                        Lateral Movement
                                                ↓
                                           Collection
                                                ↓
                                          Exfiltration
                                                ↓
                                       Command & Control
                                                ↓
                                             Impact
```

For this room, the main focus is the **Discovery / reconnaissance** part
of the attack chain.

------------------------------------------------------------------------

# Task 2 --- Network Discovery

## Attackers and Network Discovery

Before attacking a network, attackers try to understand its attack
surface.

They may want to know:

-   What assets can I access?
-   What IP addresses exist?
-   Which ports are open?
-   What operating systems are being used?
-   What services are running?
-   What versions of those services are running?
-   Does a service have a vulnerability that can be exploited?

The goal is basically to find an opening that can eventually be used for
initial access.

### What else do attackers scan?

Apart from IP addresses, ports and OS versions, attackers can scan for:

``` text
Services
```

**Answer:** `services`

## Defenders and Network Discovery

Network discovery is not always malicious. Defenders also perform
scanning to:

-   Maintain an inventory of assets
-   Find unknown/rogue systems
-   Identify unnecessary open ports
-   Identify unnecessary services
-   Find vulnerabilities
-   Reduce the attack surface
-   Verify security controls

This creates a challenge for SOC analysts because legitimate security
scanners can look similar to attacker reconnaissance.

### How SOC Teams Differentiate Scanning

**Allowlisting:** Known internal and trusted external scanners can be
allowlisted.

**Threat Intelligence:** Threat intelligence can identify scanning
sources known to be malicious or suspicious.

**Behaviour-Based Detection:** Generic scanning patterns can be detected
instead of relying only on known malicious IP addresses.

------------------------------------------------------------------------

# Task 3 --- External vs Internal Scanning

## External Scanning

External scanning occurs when a source **outside the organization's
network** scans systems inside the organization.

``` text
External IP
     ↓
Internal/Public-facing IP
```

External scanning usually indicates the attacker is still in the
**Reconnaissance** phase and may not have a foothold yet.

A SOC analyst can investigate the source, check threat intelligence,
review what was targeted and block the source if appropriate. However,
attackers can change or hide their source IP.

## Internal Scanning

Internal scanning occurs when both the source and destination are inside
the organization's network.

``` text
Internal IP
     ↓
Other Internal IPs
```

This is more serious because it may indicate that an attacker already
has a foothold.

Internal scanning maps to the MITRE ATT&CK **Discovery** tactic and can
represent internal reconnaissance before lateral movement.

After confirming the activity is not authorized, the analyst should
escalate and investigate the source system. Simply blocking the source
at the perimeter is not enough because the source is already inside the
network.

## External vs Internal

  -----------------------------------------------------------------------
  External Scanning                   Internal Scanning
  ----------------------------------- -----------------------------------
  External source → internal target   Internal source → internal target

  Usually reconnaissance              Discovery/internal reconnaissance

  Attacker may not have access yet    May indicate an existing foothold

  Lower severity generally            Higher severity generally

  Perimeter controls are useful       Endpoint + network investigation is
                                      needed
  -----------------------------------------------------------------------

## Identifying Scanning in Firewall Logs

The CSV logs were located in:

``` text
/home/ubuntu/Downloads/logs
```

I used the `head` command to understand the structure:

``` bash
head -n2 log-session-1.csv
```

Important fields included:

``` text
source.ip
source.port
destination.ip
destination.port
rule.name
rule.category
rule.action
network.protocol
event.dataset
```

The logs also contained Zeek connection fields such as:

``` text
id.orig_h
id.orig_p
id.resp_h
id.resp_p
proto
conn_state
orig_pkts
resp_pkts
```

### Answers

**Internal scanning log file:** `log-session-2.csv`\
**Internal scanning log entries:** `2276`\
**External scanning IP:** `203.0.113.25`

------------------------------------------------------------------------

# Task 4 --- Horizontal vs Vertical Scanning

## Horizontal Scanning

A horizontal scan targets the **same port across many destination IP
addresses**.

``` text
Attacker
   |
   +----→ 10.0.0.1:445
   +----→ 10.0.0.2:445
   +----→ 10.0.0.3:445
   +----→ 10.0.0.4:445
```

### Detection pattern

``` text
Same source IP
+
Same destination port
+
Multiple destination IPs
```

A common example is scanning port `445` across a subnet to find hosts
exposing SMB.

## Vertical Scanning

A vertical scan targets **one host across multiple ports**.

``` text
Attacker
   |
   +----→ 10.0.0.50:22
   +----→ 10.0.0.50:80
   +----→ 10.0.0.50:443
   +----→ 10.0.0.50:445
```

### Detection pattern

``` text
Same source IP
+
Same destination IP
+
Multiple destination ports
```

The attacker is usually trying to discover the services exposed by one
particular host.

## Answers

**Horizontal scan range:** `203.0.113.0/24`\
**Vertical scan target:** `192.168.230.127`\
**Ports scanned:** `80, 445, 3389`

------------------------------------------------------------------------

# Task 5 --- The Mechanics of Scanning

## Ping Sweep

A ping sweep identifies hosts that are online using **ICMP**.

``` text
Scanner → ICMP Echo Request → Host
Scanner ← ICMP Echo Reply  ← Host
```

ICMP can be blocked by security controls, so no response does not always
mean a host is offline.

## TCP SYN Scan

A normal TCP connection uses:

``` text
SYN → SYN-ACK → ACK
```

A SYN scanner sends a SYN and observes the response. A SYN-ACK generally
indicates that the host is reachable and the port is open.

SYN scanning can be relatively stealthy because the scanner does not
necessarily complete the full TCP connection.

## UDP Scan

A UDP scanner sends a UDP packet to the target.

If the port is closed, the target may return:

``` text
ICMP Port Unreachable
```

If there is no response, the port may be considered open/filtered
depending on the scanner and conditions.

UDP scanning is generally slower and less reliable because it relies
heavily on responses and timeouts.

------------------------------------------------------------------------

# Identifying Scan Types in Kibana

The room provided Kibana to analyse the firewall logs.

The general workflow was:

``` text
Open Kibana
    ↓
Discover
    ↓
Select "All logs"
    ↓
Search entire time range
    ↓
Add useful fields as columns
    ↓
Filter source/destination values
    ↓
Analyse the traffic pattern
```

Useful fields included:

``` text
source.ip
destination.ip
source.port
destination.port
network.protocol
```

For Zeek connection logs, I also looked at:

``` text
conn_state
```

This helped identify connection behaviour associated with scanning.

## Answers

**Ping sweep source IP:** `192.168.230.145`\
**Scan type used by 203.0.113.25 against 192.168.230.145:**
`TCP SYN scan`\
**UDP scanning attempt:** `N`

------------------------------------------------------------------------

# How I Can Recognize Scanning

### Ping Sweep

``` text
One source
   ↓
Many IP addresses
   ↓
ICMP traffic
```

### Horizontal Scan

``` text
One source
   ↓
Many destination IPs
   ↓
Same destination port
```

### Vertical Scan

``` text
One source
   ↓
One destination IP
   ↓
Many destination ports
```

### TCP SYN Scan

Look for TCP connection attempts where the scanner sends SYN packets and
the connection does not progress like a normal completed connection.

### UDP Scan

Look for UDP probes and responses such as ICMP port-unreachable
messages, or repeated UDP traffic with no response.

------------------------------------------------------------------------

# SOC Analyst Perspective

Scanning does **not automatically mean an attack is happening**.

I need to determine:

-   Who is scanning?
-   Is the source authorized?
-   Is it an internal vulnerability scanner?
-   Is it an external security service?
-   What is being scanned?
-   How many systems are being targeted?
-   Which ports are being targeted?
-   Is the scan horizontal or vertical?
-   Did the scanner receive successful responses?
-   Is there evidence of follow-up exploitation?

For example:

``` text
Known vulnerability scanner
        ↓
Internal assets
        ↓
Scheduled scan
        ↓
Likely legitimate
```

Compared with:

``` text
Unknown external IP
        ↓
Many internal hosts
        ↓
Many ports
        ↓
No authorized reason
        ↓
Potential reconnaissance
```

------------------------------------------------------------------------

# Useful Commands

### Preview a log

``` bash
head -n2 log-session-1.csv
```

### Filter an IP

``` bash
cat firewall.log | grep "IP_ADDRESS"
```

### Search IDS scan alerts

``` bash
cat ids_alerts.log | grep "SCAN"
```

The general investigation approach is:

``` text
Filter → Group → Count → Identify pattern → Pivot
```

------------------------------------------------------------------------

# Key Takeaways

-   Network discovery is an important early stage of an attack.
-   Attackers look for IPs, ports, OS information, services and service
    versions.
-   Defenders also perform network discovery, so context is important.
-   **External scanning** comes from outside the network.
-   **Internal scanning** originates from an internal system and can
    indicate a compromised host.
-   Horizontal scanning targets one port across many hosts.
-   Vertical scanning targets many ports on one host.
-   Ping sweeps use ICMP to identify reachable hosts.
-   TCP SYN scans use SYN responses to identify reachable/open TCP
    ports.
-   UDP scans are generally slower and less reliable.
-   A SOC analyst should correlate scanning activity with authorization,
    timing, source, destination and follow-up activity.

------------------------------------------------------------------------

