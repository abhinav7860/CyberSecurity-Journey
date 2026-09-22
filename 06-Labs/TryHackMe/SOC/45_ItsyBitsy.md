# TryHackMe — ItsyBitsy

## SOC Investigation Walkthrough
**Date:** 22 September 2026 
**Platform:** TryHackMe  
**Room:** ItsyBitsy  
**Category:** SOC / Blue Team / SIEM Investigation  
**Tool:** Elastic Kibana  
**Index:** `connection_logs`

---

## 1. Scenario

During normal SOC monitoring, Analyst John observed an IDS alert indicating possible Command and Control (C2) communication from a user named **Browne** in the HR department.

A suspicious file was accessed that contained a pattern in the format:

```text
THM{_____}
```

A week of HTTP connection logs was collected and ingested into the Kibana index:

```text
connection_logs
```

My objective was to investigate the network activity, identify the infected host, trace the C2 communication, identify the accessed file, and recover the secret code.

---

# 2. Investigation

## Step 1 — Open the `connection_logs` index

I opened **Kibana → Discover** and selected:

```text
connection_logs
```

Initially, the time range was set to the current period, so there were no results.

Since the room's activity was from **March 2022**, I changed the time range to:

```text
March 1, 2022 00:00:00
→
March 31, 2022 23:59:59
```

I then searched the index with:

```text
*
```

Kibana returned:

```text
1482 hits
```

### Answer

```text
1482
```

This established the correct investigation timeframe and confirmed that the logs were being loaded correctly.

---

# 3. Finding the Suspected User's IP

The next question asked for the IP associated with the suspected user.

I examined the available fields and found:

```text
source_ip
```

This field represents the source IP address that generated each network connection.

The main source IPs included:

```text
192.166.65.52
192.166.65.54
```

Instead of assuming that the IP with the most traffic was malicious, I investigated the less common address.

I filtered the logs using:

```text
source_ip : "192.166.65.54"
```

This returned only **2 events** during the relevant period.

The events showed traffic from:

```text
source_ip: 192.166.65.54
```

to:

```text
destination_ip: 104.23.99.190
```

The traffic was directed toward:

```text
host: pastebin.com
```

This made `192.166.65.54` the suspicious source IP associated with the investigation.

### Answer

```text
192.166.65.54
```

---

# 4. Identifying the Windows Binary

The next question asked which legitimate Windows binary was used to download the file from the C2 server.

I expanded the suspicious event and inspected the available fields.

One important field was:

```text
user_agent
```

The value was:

```text
bitsadmin
```

This was an important clue because **BITSAdmin** is a legitimate Windows command-line utility associated with Background Intelligent Transfer Service (BITS) and can be used to transfer files.

The HTTP request therefore showed that the suspicious connection was made using:

```text
user_agent: bitsadmin
```

### Answer

```text
bitsadmin
```

### SOC takeaway

This is a good example of **Living off the Land** activity: an attacker can abuse a legitimate operating-system utility instead of introducing a custom downloader.

---

# 5. Identifying the C2 / File-Sharing Site

The same suspicious events contained a field called:

```text
host
```

The value was:

```text
pastebin.com
```

This answered the question about the famous file-sharing service being used as the C2.

### Answer

```text
pastebin.com
```

The investigation chain was now:

```text
192.166.65.54
        ↓
bitsadmin
        ↓
pastebin.com
```

---

# 6. Finding the Full C2 URL

I then inspected the:

```text
uri
```

field of the suspicious GET request.

The value was:

```text
/yTg0Ah6a
```

The host was:

```text
pastebin.com
```

I combined the host and URI:

```text
pastebin.com + /yTg0Ah6a
```

Result:

```text
pastebin.com/yTg0Ah6a
```

### Answer

```text
pastebin.com/yTg0Ah6a
```

The HTTP request details were essentially:

```text
Source IP:       192.166.65.54
Destination IP:  104.23.99.190
Host:            pastebin.com
URI:             /yTg0Ah6a
Method:          GET
User-Agent:      bitsadmin
Status:          200
```

This showed that the infected host successfully retrieved content from the identified C2 resource.

---

# 7. Finding the Accessed File

The next question asked for the name of the file accessed on the file-sharing site.

The Kibana connection logs did not contain a dedicated `filename` field.

However, the GET request showed:

```text
resp_mime_types: text/plain
```

This indicated that the retrieved content was plain text, giving us a useful clue that the accessed file was likely a `.txt` file.

I then followed the C2 resource in the isolated TryHackMe environment:

```text
pastebin.com/yTg0Ah6a
```

The content revealed the accessed file name:

```text
secret.txt
```

### Answer

```text
secret.txt
```

> In a real incident, I would avoid opening an unknown C2 URL directly from a normal workstation. An isolated sandbox or controlled analysis environment should be used.

---

# 8. Finding the Secret Code

The final question stated that the file contained a secret code in the format:

```text
THM{_____}
```

After viewing the contents of `secret.txt`, the secret code was:

```text
THM{SECRET__CODE}
```

### Answer

```text
THM{SECRET__CODE}
```

---

# 9. Complete Investigation Timeline

```text
IDS Alert
   │
   ▼
Potential C2 communication involving Browne
   │
   ▼
Kibana → connection_logs
   │
   ▼
Set timeframe to March 2022
   │
   ▼
1482 HTTP events
   │
   ▼
Investigate source_ip
   │
   ▼
192.166.65.54
   │
   ▼
Only 2 suspicious events
   │
   ▼
user_agent = bitsadmin
   │
   ▼
host = pastebin.com
   │
   ▼
uri = /yTg0Ah6a
   │
   ▼
pastebin.com/yTg0Ah6a
   │
   ▼
secret.txt
   │
   ▼
THM{SECRET__CODE}
```

---

# 10. Indicators of Compromise

| Type | Indicator |
|---|---|
| Source IP | `192.166.65.54` |
| Destination IP | `104.23.99.190` |
| User-Agent | `bitsadmin` |
| C2 / Host | `pastebin.com` |
| URI | `/yTg0Ah6a` |
| C2 URL | `pastebin.com/yTg0Ah6a` |
| File | `secret.txt` |
| Flag | `THM{SECRET__CODE}` |

---

# 11. KQL Queries Used

### View all events

```kql
*
```

### Identify the suspicious source IP

```kql
source_ip : "192.166.65.54"
```

### Search specifically for the C2 URI

```kql
uri : "/yTg0Ah6a"
```

### Investigate GET requests

```kql
method : "GET"
```

A more targeted query can also be used:

```kql
source_ip : "192.166.65.54" AND method : "GET"
```

---

# 12. Final Answers

| Question | Answer |
|---|---|
| How many events were returned for March 2022? | `1482` |
| What is the IP associated with the suspected user? | `192.166.65.54` |
| What legitimate Windows binary was used? | `bitsadmin` |
| What file-sharing site was used as C2? | `pastebin.com` |
| What is the full C2 URL? | `pastebin.com/yTg0Ah6a` |
| What file was accessed? | `secret.txt` |
| What secret code was inside the file? | `THM{SECRET__CODE}` |

---

# 13. What I Learned

This room helped me practice a basic SOC investigation workflow using Kibana.

### Key skills practiced

- Working with an Elastic/Kibana `connection_logs` index
- Selecting the correct investigation timeframe
- Using KQL to filter network events
- Investigating `source_ip`
- Identifying suspicious outlier traffic
- Understanding the `user_agent` field
- Recognizing `bitsadmin` as a legitimate Windows utility that can be abused
- Investigating HTTP `host` and `uri` fields
- Reconstructing a C2 URL
- Using MIME type information as an additional investigation clue
- Pivoting from SIEM data to an external resource in a controlled environment
- Extracting an IOC and malicious file information
- Building an investigation timeline

---

# 14. SOC Investigation Method

The biggest lesson from this room was not simply finding the answers. It was understanding how to move from one piece of evidence to the next:

```text
Start with the alert
        ↓
Establish the correct timeframe
        ↓
Examine the available fields
        ↓
Identify unusual source activity
        ↓
Filter the suspicious IP
        ↓
Inspect the user agent
        ↓
Identify the destination host
        ↓
Inspect the URI
        ↓
Reconstruct the C2 URL
        ↓
Investigate the retrieved resource
        ↓
Identify the file
        ↓
Extract the malicious code / flag
```

This is the same general approach I can apply to real SOC investigations: **filter → correlate → pivot → validate → document**.

---

## Conclusion

The ItsyBitsy room was a useful introduction to investigating potential C2 activity through HTTP connection logs.

I started with **1,482 events**, narrowed the activity down to the suspicious source IP `192.166.65.54`, identified the use of `bitsadmin`, traced the connection to `pastebin.com/yTg0Ah6a`, identified `secret.txt`, and recovered the `THM{SECRET__CODE}` flag.

The investigation demonstrated how seemingly small pieces of network metadata — such as a source IP, user agent, host, and URI — can be correlated to reconstruct an attack path.
