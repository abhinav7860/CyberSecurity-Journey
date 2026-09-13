# Snort 

**Platform:** TryHackMe\
**Room:** Snort\
**Date:** 13 September 2026\


------------------------------------------------------------------------

# My Notes

I started the **Snort** room to understand how Snort works as an IDS/IPS
and to get more comfortable with its different operating modes.

This part mainly focused on:

-   IDS vs IPS
-   NIDS vs HIDS
-   NIPS, HIPS and WIPS
-   Signature, behaviour and policy-based detection
-   Snort capabilities
-   Checking the Snort installation
-   Testing Snort configuration files
-   Sniffer mode
-   Packet logger mode
-   Reading Snort logs
-   Using BPF filters
-   Investigating a generated Snort log

I also practiced the commands instead of only reading the theory. That
helped me understand what each Snort option actually does.

> **Sanitisation note:** I kept the technical methodology and answers
> useful for revision, but masked lab-specific IP addresses where they
> were not necessary. No personal credentials, API keys, tokens, or
> other private information are included.

------------------------------------------------------------------------

# Task 1 --- Introduction

## What is Snort?

Snort is an open-source, rule-based **Network Intrusion Detection and
Prevention System (NIDS/NIPS)**.

It uses rules to identify network traffic that matches known malicious
patterns.

The basic idea is:

``` text
Network Traffic
       ↓
     Snort
       ↓
   Snort Rules
       ↓
Matching Activity?
    ↙       ↘
  No         Yes
  ↓           ↓
Continue     Alert
              /
          Prevent
```

Depending on how Snort is configured, it can either detect and alert on
suspicious traffic or operate inline and help prevent malicious traffic.

------------------------------------------------------------------------

# Task 3 --- Introduction to IDS/IPS

Before working with Snort, I reviewed the difference between IDS and
IPS.

## IDS --- Intrusion Detection System

An IDS is a **passive monitoring solution**. It watches traffic or
system activity and generates an alert when suspicious behaviour is
detected.

### NIDS

A **Network Intrusion Detection System** monitors traffic across
different parts of a network.

``` text
Network Traffic
      ↓
     NIDS
      ↓
Detection
      ↓
Alert
```

### HIDS

A **Host-based Intrusion Detection System** monitors activity on a
particular endpoint.

``` text
Individual Host
      ↓
     HIDS
      ↓
Detection
      ↓
Alert
```

## IPS --- Intrusion Prevention System

An IPS is an **active protection solution**. Instead of only reporting
suspicious activity, it can take action such as stopping or terminating
the connection.

``` text
Network Traffic
      ↓
     IPS
      ↓
Detection
      ↓
Block / Stop
```

### Types of IPS

-   **NIPS:** protects traffic across a network and can terminate
    malicious connections.
-   **Behaviour-Based IPS / Network Behaviour Analysis:** uses a
    baseline of normal network behaviour and looks for anomalies.
-   **WIPS:** focuses on protecting wireless traffic.
-   **HIPS:** protects an individual endpoint and can actively stop
    suspicious activity.

For behaviour-based prevention, the system needs a useful baseline of
normal activity. A poor training period can lead to false positives or
poor detection.

------------------------------------------------------------------------

# IDS vs IPS

  IDS                         IPS
  --------------------------- ------------------------------
  Detects                     Detects and prevents
  Passive                     Active
  Generates alerts            Can block/terminate activity
  Requires analyst response   Can automatically respond

The easiest way I remember it:

``` text
IDS = "Something suspicious happened."
IPS = "Something suspicious happened, and I will stop it."
```

------------------------------------------------------------------------

# Detection / Prevention Techniques

## 1. Signature-Based

Signature-based detection uses known patterns of malicious behaviour.

``` text
Traffic
   ↓
Known Signatures
   ↓
Match?
   ↓
Alert / Prevention
```

It is effective for known threats.

## 2. Behaviour-Based

Behaviour-based detection compares current activity against known or
learned normal behaviour. It can help identify new or previously unknown
threats that do not have an existing signature.

The main challenge is avoiding false positives.

## 3. Policy-Based

Policy-based detection compares activity against configured security
policies. It helps identify policy violations.

------------------------------------------------------------------------

# Snort Capabilities

The room covered these Snort capabilities:

-   Live traffic analysis
-   Attack and probe detection
-   Packet logging
-   Protocol analysis
-   Real-time alerting
-   Modules and plugins
-   Pre-processors
-   Cross-platform support

## Snort Modes

Snort has three main modes I focused on in this part:

1.  **Sniffer Mode** --- reads and displays packets.
2.  **Packet Logger Mode** --- captures and stores traffic for later
    analysis.
3.  **NIDS/NIPS Mode** --- uses rules to detect malicious traffic and,
    depending on configuration, log or drop matching packets.

------------------------------------------------------------------------

# Task 4 --- First Interaction with Snort

## Check the Snort Version

I first verified that Snort was installed:

``` shell
snort -V
```

This displays the installed Snort version and build information.

### Answer

``` text
149
```

### How I Got It

I ran:

``` shell
snort -V
```

Then I looked at the Snort banner for the **Build** value. The build
number shown in the lab was **149**.

------------------------------------------------------------------------

# Test the Snort Configuration

Before using a configuration, I can check whether it is valid with:

``` shell
sudo snort -c /etc/snort/snort.conf -T
```

The options mean:

``` text
-c → specify the configuration file
-T → test the configuration
```

### Answer

``` text
4151 rules
```

### How I Got It

I ran the configuration self-test and checked the output for the number
of rules loaded. The current build loaded **4151 rules** from
`snort.conf`.

This is useful because it confirms that the configuration and its rules
can be loaded before I use it for actual detection.

------------------------------------------------------------------------

# Test the Second Configuration

The room also asked me to test another configuration:

``` text
/etc/snort/snortv2.conf
```

Command:

``` shell
sudo snort -c /etc/snort/snortv2.conf -T
```

### Answer

``` text
1 rule
```

### How I Got It

I ran the same configuration test against `snortv2.conf` and checked the
rule-loading information in the output. It showed that this
configuration loaded **1 rule**.

This showed me that different configuration files can load different
rule sets.

------------------------------------------------------------------------

# Important Snort Parameters

  Parameter            Purpose
  -------------------- ----------------------------
  `-V` / `--version`   Show Snort version/build
  `-c`                 Specify configuration file
  `-T`                 Test configuration
  `-q`                 Quiet mode

Normally Snort displays its banner and initialization information. The
`-q` option suppresses that extra output.

------------------------------------------------------------------------

# Task 5 --- Operation Mode 1: Sniffer Mode

Sniffer mode is similar to using a packet-sniffing tool. It allows me to
see network traffic directly in the console.

## Sniffer Parameters

  Parameter   Meaning
  ----------- --------------------------------------------
  `-v`        Verbose packet information
  `-d`        Display packet payload/data
  `-e`        Display link-layer headers
  `-X`        Display full packet details in hexadecimal
  `-i`        Select the network interface

------------------------------------------------------------------------

## `-i` --- Select an Interface

Example:

``` shell
sudo snort -v -i eth0
```

The `-i` option tells Snort which interface to listen on. This matters
when a system has multiple interfaces.

------------------------------------------------------------------------

## `-v` --- Verbose Mode

Command:

``` shell
sudo snort -v
```

This provides tcpdump-like packet information such as source/destination
IPs, ports, protocol, TTL and packet length.

Example structure:

``` text
<LAB-IP>:34316 -> <LAB-IP>:53
UDP TTL:64
```

The main thing I learned is that `-v` gives a high-level view of packet
headers.

------------------------------------------------------------------------

## `-d` --- Display Packet Data

Command:

``` shell
sudo snort -d
```

The `-d` option displays packet payload/data in addition to packet
information.

For example, a DNS packet may show readable domain-related data inside
the payload.

``` text
-v = packet information
-d = packet information + payload
```

------------------------------------------------------------------------

## `-de` --- Payload + Link-Layer Headers

Command:

``` shell
sudo snort -de
```

This combines:

``` text
-d → packet data
-e → link-layer headers
```

The output can include MAC addresses together with IP/transport
information and payload.

------------------------------------------------------------------------

## `-X` --- Full Packet Dump

Command:

``` shell
sudo snort -X
```

This displays full packet details in hexadecimal.

Example:

``` text
0x0000: ...
0x0010: ...
0x0020: ...
```

This is useful when I need to inspect raw packet contents.

------------------------------------------------------------------------

## Combining Parameters

Examples:

``` shell
snort -v
snort -vd
snort -de
snort -v -d -e
snort -X
```

The options can be combined depending on how much packet information I
need.

------------------------------------------------------------------------

# Generating Traffic

Snort needs traffic to observe. The room provided a `traffic-generator`
script in the exercise folder.

My workflow was:

``` text
Start Snort
    ↓
Run traffic generator
    ↓
Generate ICMP / HTTP traffic
    ↓
Observe packets
    ↓
Stop Snort with CTRL+C
```

This made the difference between the sniffer options much easier to
understand.

------------------------------------------------------------------------

# Task 6 --- Operation Mode 2: Packet Logger Mode

Packet logger mode allows Snort to capture traffic and save it for later
analysis.

## Packet Logger Parameters

  Parameter    Meaning
  ------------ ---------------------------------------
  `-l`         Set log/output directory
  `-K ASCII`   Store logs in ASCII format
  `-r`         Read a previously generated log
  `-n`         Process a specified number of packets

The default Snort log directory mentioned in the room was:

``` text
/var/log/snort
```

------------------------------------------------------------------------

# File Ownership

Snort generally needs elevated privileges to capture network traffic.
When I run it with `sudo`, generated files may be owned by `root`.

If necessary, ownership can be changed with:

``` shell
sudo chown username file
```

or recursively:

``` shell
sudo chown username -R directory
```

This is useful to remember if my normal user cannot access generated
logs.

------------------------------------------------------------------------

# Logging with `-l`

The room used:

``` shell
sudo snort -dev -K ASCII -l .
```

The `.` means the current directory. This is convenient for keeping each
exercise's logs inside its own folder.

Without ASCII output, Snort can create a binary/tcpdump-format log such
as:

``` text
snort.log.<timestamp>
```

That format can be read by Snort, tcpdump or Wireshark rather than
treated as normal text.

------------------------------------------------------------------------

# ASCII Logging

Command:

``` shell
sudo snort -dev -K ASCII -l .
```

With `-K ASCII`, Snort creates human-readable, categorized output. The
resulting structure can contain IP-address-based directories and
protocol/session files.

### Binary vs ASCII

  Binary                               ASCII
  ------------------------------------ ------------------------------
  Packet-oriented binary log           Human-readable text output
  Similar to tcpdump/PCAP format       Categorized text files
  Read using Snort/tcpdump/Wireshark   Can be inspected directly
  Good for packet-level analysis       Convenient for quick reading

------------------------------------------------------------------------

# Reading a Generated Log with `-r`

The `-r` option reads a previously generated binary Snort log.

Example:

``` shell
sudo snort -r snort.log.<timestamp>
```

For the exercise, the log was:

``` text
snort.log.1640048004
```

I remember this as:

``` text
-r = read captured traffic
```

------------------------------------------------------------------------

# Filtering a Log with BPF

Snort can use **Berkeley Packet Filter (BPF)** expressions while reading
a log.

Examples:

``` shell
sudo snort -r logname.log icmp
```

``` shell
sudo snort -r logname.log tcp
```

``` shell
sudo snort -r logname.log 'udp and port 53'
```

This lets me narrow a large capture down to the traffic I actually need.

------------------------------------------------------------------------

# Limiting Packets with `-n`

The `-n` option specifies how many packets Snort should process.

Example:

``` shell
sudo snort -dvr logname.log -n 10
```

This processes the first 10 packets.

An important detail: `-n 10` does **not** mean "show packet 10 only". It
means process the first ten packets, after which I can inspect the
required packet in that sequence.

------------------------------------------------------------------------

# Task 6 Exercise --- Investigating the Snort Log

I navigated to the Task 6 exercise folder and started ASCII logging:

``` shell
sudo snort -dev -K ASCII -l .
```

Then I ran:

``` shell
sudo ./traffic-generator.sh
```

and selected:

``` text
TASK-6 Exercise
```

After the traffic finished, I stopped Snort and investigated the
generated logs.

The binary log used for the questions was:

``` text
snort.log.1640048004
```

------------------------------------------------------------------------

# Question 1 --- Source Port Connecting to Port 53

### Question

What is the source port used to connect to port 53?

### Answer

``` text
3009
```

### How I Got It

I read the generated log with:

``` shell
snort -r snort.log.1640048004
```

I looked for DNS traffic where the destination port was:

``` text
53
```

Then I checked the source port of that client-to-DNS connection. The
source port was **3009**.

The traffic pattern I was looking for was essentially:

``` text
Client:<source-port> → DNS-server:53
```

The client source port is normally an ephemeral/temporary port, while
DNS uses destination port 53.

------------------------------------------------------------------------

# Question 2 --- IP ID of the 10th Packet

### Question

What is the IP ID of the 10th packet?

### Answer

``` text
49313
```

### How I Got It

I limited Snort to the first ten packets:

``` shell
snort -r snort.log.1640048004 -n 10
```

I then counted through the displayed packets and inspected the 10th
packet's IP header.

The output showed:

``` text
ID: 49313
```

So the answer was:

``` text
49313
```

------------------------------------------------------------------------

# Question 3 --- Referer of the 4th Packet

### Question

What is the Referer of the 4th packet?

### Answer

``` text
http://www.ethereal.com/development.html
```

### How I Got It

I used:

``` shell
snort -r snort.log.1640048004 -n 4 -X
```

Here:

``` text
-n 4 → process the first four packets
-X   → display full packet contents in hexadecimal
```

I inspected the fourth packet for HTTP headers and found the `Referer`
value:

``` text
http://www.ethereal.com/development.html
```

The HTTP `Referer` header can provide context about the page that led to
a request.

------------------------------------------------------------------------

# Question 4 --- ACK Number of the 8th Packet

### Question

What is the ACK number of the 8th packet?

### Answer

``` text
0x38AFFFF3
```

### How I Got It

I used:

``` shell
snort -r snort.log.1640048004 -n 8
```

I inspected the TCP header of the 8th packet and located its ACK value.

The value shown was:

``` text
0x38AFFFF3
```

So the answer was the hexadecimal ACK number above.

------------------------------------------------------------------------

# Question 5 --- Number of TCP Port 80 Packets

### Question

What is the number of **TCP port 80** packets?

### Answer

``` text
41
```

### How I Got It

Instead of manually counting packets, I used a BPF filter:

``` shell
snort -r snort.log.1640048004 'tcp and port 80'
```

This tells Snort to read the log and display only TCP traffic associated
with port 80.

The resulting packet count was:

``` text
41
```

Therefore:

``` text
TCP port 80 packets = 41
```

This was a good example of why filtering is important during packet
analysis. A filter can reduce a large amount of traffic to exactly what
I want to investigate.

------------------------------------------------------------------------

# Final Answers --- Part 1

  --------------------------------------------------------------------------------
  Question                            Answer
  ----------------------------------- --------------------------------------------
  Snort build number                  `149`

  Rules loaded with `snort.conf`      `4151`

  Rules loaded with `snortv2.conf`    `1`

  Source port connecting to DNS port  `3009`
  53                                  

  IP ID of the 10th packet            `49313`

  Referer of the 4th packet           `http://www.ethereal.com/development.html`

  ACK number of the 8th packet        `0x38AFFFF3`

  Number of TCP port 80 packets       `41`
  --------------------------------------------------------------------------------

------------------------------------------------------------------------

# Command Cheatsheet

## Check Version

``` shell
snort -V
```

## Test Configuration

``` shell
sudo snort -c /etc/snort/snort.conf -T
```

## Test Another Configuration

``` shell
sudo snort -c /etc/snort/snortv2.conf -T
```

## Verbose Sniffing

``` shell
sudo snort -v
```

## Select Interface

``` shell
sudo snort -v -i eth0
```

## Show Packet Payload

``` shell
sudo snort -d
```

## Show Link-Layer Headers + Payload

``` shell
sudo snort -de
```

## Full Hex Dump

``` shell
sudo snort -X
```

## ASCII Packet Logging

``` shell
sudo snort -dev -K ASCII -l .
```

## Read a Binary Snort Log

``` shell
sudo snort -r snort.log.<timestamp>
```

## Read First 10 Packets

``` shell
sudo snort -r snort.log.<timestamp> -n 10
```

## Read Only ICMP

``` shell
sudo snort -r snort.log.<timestamp> icmp
```

## Read Only TCP

``` shell
sudo snort -r snort.log.<timestamp> tcp
```

## Filter UDP DNS Traffic

``` shell
sudo snort -r snort.log.<timestamp> 'udp and port 53'
```

## Filter TCP Port 80

``` shell
sudo snort -r snort.log.<timestamp> 'tcp and port 80'
```

------------------------------------------------------------------------

# Snort Options I Want to Remember

``` text
-V        → version/build
-c        → configuration file
-T        → configuration test
-q        → quiet mode
-i        → interface
-v        → verbose packet output
-d        → packet payload
-e        → link-layer headers
-X        → full packet hex
-l        → logging directory
-K ASCII  → ASCII logging
-r        → read log
-n        → number of packets to process
```

A quick memory trick:

``` text
-V  → Version
-c  → Config
-T  → Test
-i  → Interface
-v  → View
-d  → Data
-e  → Ethernet
-X  → Hex
-l  → Log
-r  → Read
-n  → Number
```

------------------------------------------------------------------------

# What I Learned From Part 1

## 1. IDS and IPS are different

IDS mainly detects and alerts, while IPS can detect and actively prevent
or terminate suspicious activity.

## 2. Snort has multiple uses

Snort can work as a:

``` text
Packet Sniffer
Packet Logger
NIDS
NIPS
```

depending on its configuration.

## 3. Configuration testing is important

Before relying on a configuration, I can use:

``` shell
sudo snort -c /etc/snort/snort.conf -T
```

This helps confirm that the configuration and rules can be loaded
correctly.

## 4. Sniffer parameters control visibility

I learned this progression:

``` text
-v
 ↓
Basic packet information

-d
 ↓
Packet information + payload

-de
 ↓
Payload + link-layer information

-X
 ↓
Full packet details in HEX
```

## 5. Logs can be investigated later

Snort is not limited to live traffic. I can save traffic and investigate
the generated log later using:

``` shell
snort -r <log>
```

## 6. BPF filters save time

Instead of manually checking every packet, I can narrow traffic with
filters such as:

``` shell
'tcp and port 80'
```

or:

``` shell
'udp and port 53'
```

This becomes increasingly important when the capture is large.

------------------------------------------------------------------------

# My Investigation Workflow

The workflow I took from this part is:

``` text
1. Check Snort installation
          ↓
2. Check version/build
          ↓
3. Validate configuration
          ↓
4. Choose Snort mode
          ↓
5. Capture / read traffic
          ↓
6. Apply filters when needed
          ↓
7. Inspect packet details
          ↓
8. Extract useful evidence
          ↓
9. Continue investigation
```

For a SOC analyst, the important part is not just memorising commands. I
need to understand **why I am using a particular option or filter**.

For example:

``` text
Need version?
→ -V

Need to validate config?
→ -T

Need live packet visibility?
→ -v / -d / -e / -X

Need to save traffic?
→ -l

Need to investigate saved traffic?
→ -r

Need only specific traffic?
→ BPF filter

Need only the first few packets?
→ -n
```

------------------------------------------------------------------------

