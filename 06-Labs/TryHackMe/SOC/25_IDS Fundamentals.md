# IDS Fundamentals

**Platform:** TryHackMe\
**Room:** IDS Fundamentals\
**Date:** 12 September 2026\
**Focus:** IDS concepts, HIDS vs NIDS, detection modes, Snort, rules,
and PCAP analysis

------------------------------------------------------------------------

# My Notes

This room introduced me to **Intrusion Detection Systems (IDS)** and how
they are used to detect suspicious or malicious activity inside a
network.

A simple way I remember the difference is:

``` text
Firewall = Gatekeeper
IDS = Security Camera
```

A firewall controls whether connections are allowed or blocked. An IDS
monitors activity and generates alerts when it detects suspicious
behaviour.

------------------------------------------------------------------------

# Task 1 --- What Is an IDS?

An **Intrusion Detection System (IDS)** monitors network or host
activity and looks for suspicious behaviour.

If an attacker bypasses a firewall using a legitimate-looking connection
and then performs malicious activity, an IDS can detect that activity
and alert security administrators.

The important point is that an IDS is mainly a **detection and
alerting** solution. It does not automatically take action on the
detection like an IPS would.

------------------------------------------------------------------------

# Task 2 --- Types of IDS

IDS can be categorized by:

1.  Deployment mode
2.  Detection mode

## Deployment Modes

### HIDS --- Host Intrusion Detection System

A HIDS is installed on individual hosts and monitors activity associated
with that particular host.

**Advantages:** - Detailed host visibility - Host-specific monitoring

**Disadvantages:** - Needs to be managed on individual systems - Can be
resource-intensive in large environments

### NIDS --- Network Intrusion Detection System

A NIDS monitors network traffic across the network and provides a
centralized view of detections.

``` text
Multiple Hosts
      ↓
Network Traffic
      ↓
     NIDS
      ↓
Detections / Alerts
```

------------------------------------------------------------------------

# Detection Modes

## Signature-Based IDS

Signature-based detection compares traffic against known attack patterns
stored in a signature database.

``` text
Traffic
   ↓
Compare with signatures
   ↓
Match found
   ↓
Alert
```

It is effective for known threats but cannot reliably detect new or
zero-day attacks that have no existing signature.

## Anomaly-Based IDS

Anomaly-based detection first learns normal behaviour and then looks for
deviations from that baseline.

``` text
Normal Behaviour
       ↓
Baseline
       ↓
Current Activity
       ↓
Deviation?
       ↓
Alert
```

It can potentially detect new attacks, but unusual legitimate activity
can also generate false positives.

## Hybrid IDS

A hybrid IDS combines signature-based and anomaly-based detection.

``` text
Signature Detection
        +
Anomaly Detection
        ↓
    Hybrid IDS
```

------------------------------------------------------------------------

# Quick Comparison

  -----------------------------------------------------------------------
  Type              Main Idea         Main Strength     Main Limitation
  ----------------- ----------------- ----------------- -----------------
  HIDS              Monitors          Detailed host     Harder to manage
                    individual hosts  visibility        at scale

  NIDS              Monitors network  Centralized       Less
                    traffic           visibility        host-specific

  Signature-Based   Matches known     Fast known-threat Weak against
                    patterns          detection         unknown threats

  Anomaly-Based     Detects deviation Can detect new    More false
                    from baseline     behaviour         positives

  Hybrid            Combines both     Uses strengths of More complex
                                      both              
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Task 3 --- IDS Example: Snort

**Snort** is an open-source IDS solution.

It uses rules to identify suspicious or malicious network traffic. It
includes built-in rules, and custom rules can also be created for
specific detection requirements.

## Snort Modes

### 1. Packet Sniffer Mode

Reads and displays network packets without performing IDS analysis.

Useful for: - Network monitoring - Troubleshooting - Understanding
traffic flow

### 2. Packet Logging Mode

Logs network traffic as PCAP files for later analysis.

Useful for: - Forensic investigations - Root cause analysis - Historical
traffic analysis

### 3. NIDS Mode

This is the main IDS mode. Snort monitors traffic in real time and
applies its rules. When traffic matches a rule, an alert is generated.

``` text
Network Traffic
      ↓
Snort Rules
      ↓
Rule Match
      ↓
Alert
```

------------------------------------------------------------------------

# Task 4 --- Snort Usage

## Snort Directory

The main Snort directory in the lab was:

``` text
/etc/snort
```

I checked it with:

``` shell
ls /etc/snort
```

Important files included:

``` text
snort.lua
snort.conf
rules/
classification.config
reference.config
threshold.conf
```

The exact location can differ between installations, but this TryHackMe
machine used `/etc/snort`.

------------------------------------------------------------------------

# Snort Configuration

The main configuration file used in the lab was:

``` text
/etc/snort/snort.lua
```

The rule files were stored under:

``` text
/etc/snort/rules
```

The configuration controls settings such as enabled rules and the
network range being monitored.

------------------------------------------------------------------------

# Understanding a Snort Rule

The sample rule was:

``` text
alert icmp any any -> $HOME_NET any (msg:"Ping Detected"; sid:10001; rev:1;)
```

The parts are:

  Part          Meaning
  ------------- ---------------------
  `alert`       Action to take
  `icmp`        Protocol
  `any`         Source IP
  `any`         Source port
  `->`          Traffic direction
  `$HOME_NET`   Destination network
  `any`         Destination port
  `msg`         Alert message
  `sid`         Signature ID
  `rev`         Rule revision

## Rule Metadata

Example:

``` text
(msg:"Ping Detected"; sid:10001; rev:1;)
```

### `msg`

``` text
msg:"Ping Detected"
```

Describes what the rule detected.

### `sid`

``` text
sid:10001
```

The **Signature ID** uniquely identifies the rule.

### `rev`

``` text
rev:1
```

The **revision number** tracks changes to the rule.

------------------------------------------------------------------------

# Rule Creation

I opened the local rules file with:

``` shell
sudo nano /etc/snort/rules/local.rules
```

The room asked me to add:

``` text
alert icmp any any -> 127.0.0.1 any (msg:"Loopback Ping Detected"; sid:10003; rev:1;)
```

This rule detects ICMP traffic going to the loopback address:

``` text
127.0.0.1
```

I kept the existing rules because they were needed later.

------------------------------------------------------------------------

# Testing the Rule

I started Snort with:

``` shell
sudo snort -q -l /var/log/snort -i lo -A alert_fast -c /etc/snort/snort.lua
```

Important options:

``` text
-q             → quiet mode
-l              → log directory
-i              → network interface
-A alert_fast   → fast alert output
-c              → configuration file
```

The lab used the loopback interface:

``` text
lo
```

Then I generated ICMP traffic:

``` shell
ping 127.0.0.1
```

Snort generated alerts similar to:

``` text
[**] [1:1000001:1] "Loopback Ping Detected" [**]
[Priority: 0] {ICMP} 127.0.0.1 -> 127.0.0.1
```

This confirmed that the custom rule was working.

------------------------------------------------------------------------

# Running Snort Against PCAP Files

Snort can also analyze historical network traffic stored in a PCAP.

Command:

``` shell
sudo snort -q -l /var/log/snort -r Task.pcap -A alert_fast -c /etc/snort/snort.lua
```

Here:

``` text
-r Task.pcap
```

tells Snort to read the PCAP file.

This is useful during forensic investigations when I need to investigate
previously captured traffic.

------------------------------------------------------------------------

# Promiscuous Mode

The room also explained promiscuous mode.

Normally, an interface captures traffic intended for the host. For
network-wide monitoring, the interface can use promiscuous mode so the
IDS can observe relevant traffic from across the network.

This is especially important for a **NIDS**, because the goal is to
monitor network activity rather than only traffic addressed to the IDS
itself.

------------------------------------------------------------------------

# Final Answers

  Question                                     Answer
  -------------------------------------------- --------------
  Where is the main directory of Snort?        `/etc/snort`
  Which field indicates the revision number?   `rev`

------------------------------------------------------------------------

# Important Commands

## List Snort Files

``` shell
ls /etc/snort
```

## Edit Local Rules

``` shell
sudo nano /etc/snort/rules/local.rules
```

## Run Snort for Detection

``` shell
sudo snort -q -l /var/log/snort -i lo -A alert_fast -c /etc/snort/snort.lua
```

## Generate Test ICMP Traffic

``` shell
ping 127.0.0.1
```

## Analyze a PCAP

``` shell
sudo snort -q -l /var/log/snort -r Task.pcap -A alert_fast -c /etc/snort/snort.lua
```

------------------------------------------------------------------------

# Snort Rule Cheatsheet

Basic structure:

``` text
action protocol source_ip source_port -> destination_ip destination_port (rule_options)
```

Example:

``` text
alert icmp any any -> $HOME_NET any (msg:"Ping Detected"; sid:10001; rev:1;)
```

Remember:

``` text
alert       → action
icmp        → protocol
any         → source IP
any         → source port
$HOME_NET   → destination network
any         → destination port
msg         → alert message
sid         → signature ID
rev         → revision number
```

------------------------------------------------------------------------

# What I Learned

### 1. IDS and firewall are different

A firewall controls access, while an IDS monitors activity and generates
alerts.

### 2. HIDS focuses on hosts

HIDS gives visibility into individual systems.

### 3. NIDS focuses on network traffic

NIDS provides centralized network visibility.

### 4. Signature-based detection is good for known threats

It is fast, but depends on existing signatures.

### 5. Anomaly-based detection looks for unusual behaviour

It can detect new behaviour but may generate more false positives.

### 6. Snort rules define what traffic should trigger alerts

Understanding the rule structure helps me understand exactly what Snort
is looking for.

### 7. `sid` and `rev` are different

``` text
sid = identifies the rule
rev = identifies the rule revision
```

### 8. Snort can analyze PCAP files

Snort is not limited to live monitoring. I can also use it to
investigate historical traffic during a forensic investigation.

------------------------------------------------------------------------

# SOC Investigation Mindset

When using an IDS such as Snort, I can think about the process like
this:

``` text
Network Traffic
      ↓
IDS Sensor
      ↓
Detection Rules
      ↓
Rule Match?
   ↙       ↘
 No         Yes
 ↓           ↓
Continue    Alert
              ↓
        SOC Investigation
              ↓
        Correlate Evidence
              ↓
        Determine Severity
              ↓
        Respond / Escalate
```

An IDS alert is a **starting point for investigation**, not
automatically proof that an incident has occurred.

------------------------------------------------------------------------

