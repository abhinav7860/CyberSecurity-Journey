# Data Exfiltration Detection

**Platform:** TryHackMe\
**Room:** Data Exfiltration Detection\
**Date:** 11 September 2026\
**Focus:** Detecting data exfiltration through DNS, FTP, HTTP and ICMP

------------------------------------------------------------------------

## My Notes

This room focused on **data exfiltration**, which is the unauthorized
transfer of sensitive information from a system or network to an
external destination controlled by an attacker.

The main thing I learned is that detecting exfiltration is not always
about one obvious alert. I need to look for unusual patterns in network
traffic and logs, then correlate them with the compromised host.

A simplified flow is:

``` text
Sensitive Data
     ↓
Discovery / Collection
     ↓
Staging / Compression
     ↓
Exfiltration
     ↓
External Attacker
```

Attackers can abuse normal protocols such as DNS, FTP, HTTP/HTTPS and
ICMP because they can blend into legitimate traffic.

------------------------------------------------------------------------

# Task 3 --- Data Exfil: Overview, Techniques and Indicators

## What is Data Exfiltration?

Data exfiltration is the unauthorized transfer of data from an
organization to an external destination controlled by an adversary.

It can happen because of:

-   Malware
-   Compromised credentials
-   Insider activity
-   Compromised systems

## Why Attackers Exfiltrate Data

Attackers may steal data for:

-   **Financial gain** --- sensitive information can be sold or used for
    fraud.
-   **Espionage** --- intellectual property, trade secrets or classified
    information may be targeted.
-   **Ransomware and extortion** --- data can be stolen before
    encryption and then used to threaten a leak.
-   **Disruption and sabotage** --- leaking information can damage an
    organization's reputation or operations.
-   **Persistence and reconnaissance** --- stolen information can help
    attackers understand the environment.

## Common Exfiltration Phases

``` text
Discovery / Collection
        ↓
Staging / Compression
        ↓
Exfiltration Transport
        ↓
C2 Coordination
```

The data may be aggregated, compressed, encrypted or encoded using
formats/techniques such as ZIP, RAR, 7z, tar, Base64 or steganography.

## Techniques and Indicators

### Network-based

Examples include HTTP/HTTPS uploads, FTP/SFTP/SCP, DNS tunneling, ICMP
and custom TCP/UDP traffic.

Useful sources:

-   Proxy/web gateway logs
-   Firewall/NGFW logs
-   NetFlow
-   DNS logs

### Host-based

Examples include PowerShell, `Invoke-WebRequest`, `rclone`, `awscli`,
`curl`, `wget`, archive creation and removable media.

Useful sources include Sysmon/EDR, Windows Security logs, Linux
auditd/shell history and removable-media events.

### Cloud exfiltration

Attackers may upload data to S3, Azure Blob, Google Cloud Storage, Drive
or SharePoint. Useful sources include CloudTrail, Azure Activity logs,
GCP Audit logs and cloud storage access logs.

### Covert and encoding

Attackers may use DNS tunneling, Base64, chunked data, steganography or
many small requests to hide the transfer.

## General Indicators

I should look for:

-   Large outbound data transfers
-   Frequent outbound uploads
-   Unknown external destinations
-   Suspicious domains
-   Long/high-entropy DNS queries
-   Large HTTP POST requests
-   Suspicious processes creating archives
-   Many file reads followed by outbound connections
-   Multipart or streamed uploads
-   Removable-media activity

For L1 triage, I should identify **who/what host or user, what data, how
much, where it went, which process was involved, and what supporting
evidence exists**.

### Task 3 Answer

**Question:** Exfiltrating data through HTTP comes under which
technique?

``` text
Network-based
```

------------------------------------------------------------------------

# Task 4 --- Detection: Data Exfil Through DNS Tunneling

## DNS Exfiltration

DNS exfiltration abuses the DNS protocol to transfer data inside DNS
queries or responses.

DNS is attractive because it is used constantly, is commonly allowed
through networks, can blend with normal requests, and can carry encoded
data inside subdomain labels or TXT responses.

### Indicators

-   Many queries to one external domain
-   Long subdomain labels or full query names
-   High-entropy/Base32/Base64-like strings
-   Unusual TXT/NULL records
-   Frequent NXDOMAIN responses
-   Large responses or fragmentation
-   Regular query timing

## Wireshark Investigation

PCAP:

``` text
dns_exfil.pcap
```

Location:

``` text
/data_exfil/dns_exfil/
```

### 1. Filter DNS traffic

``` text
dns
```

### 2. Show DNS queries

``` text
dns.flags.response == 0
```

### 3. Find large DNS packets

``` text
dns && frame.len > 70
```

### 4. Filter the suspicious domain

``` text
dns && dns.qry.name contains <suspicious-domain>
```

The investigation showed multiple internal hosts sending data in chunks
through DNS to one external domain.

## Splunk Investigation

``` spl
index=data_exfil sourcetype=DNS_logs
```

Count queries by source:

``` spl
index="data_exfil" sourcetype="DNS_logs" | stats count by src_ip
```

Find queries with the highest counts:

``` spl
index="data_exfil" sourcetype="dns_logs" | stats count by query | sort -count
```

Find long query names:

``` spl
index="data_exfil" sourcetype="DNS_logs" | where len(query) > 30
```

## Answers

-   **Suspicious domain:** `tunnelcorp.net`
-   **Suspicious DNS tunneling traffic/logs:** `315`
-   **Local IP with maximum suspicious requests:** `192.168.1.103`

------------------------------------------------------------------------

# Task 5 --- Detection: Data Exfil Through FTP

## FTP Exfiltration

FTP can be abused to move large amounts of data outside a network.
Attackers may use legitimate FTP servers, misconfigured servers,
compromised credentials, service accounts, non-standard ports or
tunneling.

### Important FTP Indicators

``` text
USER
PASS
STOR
RETR
```

`USER` and `PASS` show authentication activity. `STOR` indicates a file
upload, while `RETR` indicates a download.

## Wireshark Investigation

PCAP:

``` text
ftp-lab.pcap
```

Location:

``` text
/data_exfil/ftp_exfil/
```

### Isolate FTP

``` text
ftp || ftp-data
```

### Find login attempts

``` text
ftp.request.command == "USER" || ftp.request.command == "PASS"
```

### Find file uploads

``` text
ftp contains "STOR"
```

### Follow a TCP stream

``` text
Right-click packet → Follow → TCP Stream
```

### Search for CSV files

``` text
ftp contains "csv"
```

### Find large FTP packets

``` text
ftp && frame.len > 90
```

## Answers

-   **Guest account connections:** `5`
-   **Customer-related file from root account:** `customer_data.xlsx`
-   **Internal IP sending the largest payload:** `192.168.1.105`
-   **FTP flag:** `THM{ftp_exfil_hidden_flag}`

------------------------------------------------------------------------

# Task 6 --- Detection: Data Exfil via HTTP

## HTTP Exfiltration

HTTP is commonly abused for exfiltration because it is normal web
traffic and can pass through firewalls and proxies.

Attackers may use:

-   POST uploads
-   GET requests containing encoded data
-   Custom headers
-   Chunked/multipart transfers
-   HTTPS/TLS
-   Cloud services

### Indicators

-   Unusually large POST requests
-   Rare or suspicious external domains
-   Frequent small requests/beaconing
-   Beaconing followed by large uploads
-   Chunked or multipart transfers

## Splunk Investigation

View HTTP logs:

``` spl
index="data_exfil" sourcetype="http_logs"
```

Focus on POST requests:

``` spl
index="data_exfil" sourcetype="http_logs" method=POST
```

Compare payload sizes:

``` spl
index="data_exfil" sourcetype="http_logs" method=POST | stats count avg(bytes_sent) max(bytes_sent) min(bytes_sent) by domain | sort - count
```

Find large POST uploads:

``` spl
index="data_exfil" sourcetype="http_logs" method=POST bytes_sent > 600 | table _time src_ip uri domain dst_ip bytes_sent | sort - bytes_sent
```

## Wireshark Investigation

PCAP:

``` text
http_lab.pcap
```

Location:

``` text
/data_exfil/http_exfil/
```

Filter HTTP:

``` text
http
```

Filter POST requests:

``` text
http.request.method == "POST"
```

Find larger POST packets:

``` text
http.request.method == "POST" and frame.len > 500
```

Narrow it further:

``` text
http.request.method == "POST" and frame.len > 750
```

I then inspected the HTTP stream to view the transferred content.

## Answers

-   **Internal compromised host:** `192.168.1.103`
-   **HTTP flag:** `THM{http_raw_3xf1ltr4t10n_succ3ss}`

------------------------------------------------------------------------

# Task 7 --- Detection: Data Exfiltration via ICMP

## ICMP Exfiltration

ICMP is normally used for diagnostics such as ping. Attackers can abuse
it by placing encoded data inside ICMP payloads and sending it to a
remote listener.

A simple model is:

``` text
Compromised Host
      |
      | ICMP + encoded data
      ↓
Attacker-controlled system
```

### Techniques

-   ICMP Echo Request/Reply tunneling
-   Custom ICMP types/codes
-   Fragmentation and reassembly
-   Encoding/encryption

### Indicators

-   Persistent ICMP sessions to an unusual external host
-   Large ICMP payloads
-   High-entropy or encoded payloads
-   Frequent ICMP packets
-   Regular timing
-   Fragmented ICMP traffic

## Wireshark Investigation

PCAP:

``` text
icmp_lab.pcap
```

Location:

``` text
/data_exfil/icmp/exfil
```

### 1. Filter all ICMP

``` text
icmp
```

### 2. Isolate Echo Requests

``` text
icmp.type == 8
```

### 3. Find large Echo Requests

``` text
icmp.type == 8 and frame.len > 100
```

This filter helped isolate unusually large ICMP packets. I then
inspected the packet contents to find the hidden data.

## Answer

**ICMP exfiltration flag:**

``` text
THM{1cmp_3ch0_3xf1ltr4t10n_succ3ss}
```

------------------------------------------------------------------------

# Final Answers

  Task   Question                                    Answer
  ------ ------------------------------------------- ---------------------------------------
  3      HTTP exfiltration technique                 `Network-based`
  4      Suspicious DNS domain                       `tunnelcorp.net`
  4      DNS tunneling traffic/logs                  `315`
  4      Local IP with maximum suspicious requests   `192.168.1.103`
  5      Guest account connections                   `5`
  5      Customer-related file                       `customer_data.xlsx`
  5      Largest FTP payload source                  `192.168.1.105`
  5      FTP flag                                    `THM{ftp_exfil_hidden_flag}`
  6      Compromised HTTP exfiltration host          `192.168.1.103`
  6      HTTP flag                                   `THM{http_raw_3xf1ltr4t10n_succ3ss}`
  7      ICMP flag                                   `THM{1cmp_3ch0_3xf1ltr4t10n_succ3ss}`

------------------------------------------------------------------------

# Detection Workflow I Want to Remember

``` text
1. Find unusual outbound traffic
            ↓
2. Identify source host/user
            ↓
3. Identify destination
            ↓
4. Check protocol
            ↓
5. Check traffic volume/payload size
            ↓
6. Look for suspicious timing/patterns
            ↓
7. Inspect packet contents
            ↓
8. Correlate with SIEM/host logs
            ↓
9. Confirm whether sensitive data was transferred
```

------------------------------------------------------------------------

# Protocol Detection Cheatsheet

  Protocol   What I should look for
  ---------- ------------------------------------------------------------
  DNS        Long/random queries, high query counts, suspicious domains
  FTP        `USER`, `PASS`, `STOR`, large transfers
  HTTP       Large POSTs, suspicious domains, encoded/chunked data
  ICMP       Large payloads, frequent Echo Requests, regular timing

------------------------------------------------------------------------

# What I Learned

### 1. Exfiltration can hide inside normal protocols

Attackers do not always need a custom protocol. They can abuse protocols
that are already allowed in the network.

### 2. Size matters

Large or unusual payloads can be an important clue, especially for HTTP,
FTP and ICMP.

### 3. DNS can be a covert channel

Long and unusual DNS queries, especially high-volume requests to one
domain, can indicate DNS tunneling.

### 4. Correlation is important

A suspicious packet becomes much more meaningful when I can connect it
to a compromised host, suspicious process/user, unusual destination and
large transfer.

### 5. Wireshark and Splunk complement each other

``` text
Splunk → Find suspicious patterns in logs
Wireshark → Inspect the actual network traffic
```

Using both gives a clearer picture of the incident.

------------------------------------------------------------------------

# Final Takeaway

The biggest thing I learned from this room is that **data exfiltration
detection is mainly about recognizing abnormal behaviour and correlating
evidence**.

An attacker may try to hide stolen data inside:

``` text
DNS
FTP
HTTP
ICMP
```

As a SOC analyst, I need to ask:

``` text
Who sent it?
What was sent?
Where did it go?
How much data was transferred?
Which protocol was used?
Was the activity normal?
What other evidence supports the alert?
```

------------------------------------------------------------------------

