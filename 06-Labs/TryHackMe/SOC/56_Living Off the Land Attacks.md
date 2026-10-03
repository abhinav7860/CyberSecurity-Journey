# Malware Analysis & Living Off the Land — SOC L1 Notes

> Personal SOC L1 study notes based on the TryHackMe material provided in this conversation.

## 1. Malware Classification

### What is Malware?
Malware means malicious software: software or code created with a malicious purpose such as damaging systems, stealing information, or enabling unauthorised access.

### Common categories
- **Adware** — displays unwanted advertisements. Example: Fireball.
- **Spyware** — secretly collects information. Example: Hermit / Pegasus.
- **Ransomware** — encrypts or locks data and demands payment. Examples: WannaCry, Akira.
- **Wiper** — destroys data or systems rather than primarily extorting payment. Examples: PathWiper, Shamoon.
- **C2 malware** — enables attacker communication and remote control. Example: Emotet.
- **Data stealer** — steals credentials, files, documents, cookies, or other sensitive information. Examples: Lumma Stealer, Agent Tesla.
- **Keylogger** — records keystrokes. Examples: Zeus, RedLine.
- **Cryptominer** — abuses system resources to mine cryptocurrency. Example: Coinhive.

### SOC recognition
- Ads → investigate unwanted software and browser activity.
- Secret collection → investigate spyware.
- Mass encryption + ransom note → investigate ransomware.
- Destruction/overwriting → investigate wiper activity.
- Strange outbound connections + remote commands → investigate C2.
- Sensitive files leaving the endpoint → investigate a stealer/exfiltration.
- Credential abuse + keystroke capture → investigate keylogging.
- Sustained high CPU + suspicious process → investigate cryptomining.

## 2. Malware Families and Examples

A **malware family** is a group of malicious programs sharing an origin/codebase and similar behaviour. Family knowledge helps analysts understand likely delivery, behaviour, infrastructure, indicators, and detection opportunities.

### Pegasus — Spyware
The material describes Pegasus as mobile spyware capable of collecting messages, location data, emails, microphone recordings, and camera recordings.

MITRE ATT&CK mentioned: **TA0009 Collection**, **TA0010 Exfiltration**.

### Akira — Ransomware
The material describes phishing, stolen credentials, and remote access software as possible access methods. Akira can spread, encrypt files, display a ransom note, and threaten data leakage.

MITRE ATT&CK mentioned: **TA0040 Impact**, **TA0011 Command and Control**.

### Shamoon — Wiper
Shamoon is described as destructive malware that overwrites files, making systems unusable.

MITRE ATT&CK mentioned: **TA0040 Impact**.

### Agent Tesla — Data Stealer
The material describes phishing attachments, keystrokes, screenshots, browser credentials, email credentials, and exfiltration to attacker-controlled servers.

MITRE ATT&CK mentioned: **TA0010 Exfiltration**.

### RedLine Stealer — Keylogger / Stealer
The material describes collection of keystrokes, browser cookies, and cryptocurrency wallet information followed by exfiltration.

MITRE ATT&CK mentioned: **TA0006 Credential Access**, **TA0010 Exfiltration**.

### QakBot — C2 RAT
QakBot is described as a modular RAT delivered through phishing links or attachments, capable of C2 communication, credential theft, lateral movement, data theft, and delivery of additional malware.

MITRE ATT&CK mentioned: **TA0011 Command and Control**, **TA0002 Execution**, **TA0006 Credential Access**.

## 3. Binary vs Script-Based Malware

### Binary malware
Usually compiled executables such as `.exe` and `.dll`. Delivery can occur through email attachments, downloads, removable media, or another infection. Misleading names/extensions may disguise executables, e.g. `invoice.pdf.exe`.

Hashes such as MD5, SHA-1, and SHA-256 can identify a particular binary sample.

### Script-based malware
Can use JavaScript, VBScript, batch, or PowerShell. Scripts are easy to modify and can sometimes execute code directly through an interpreter.

Warning signs include:
- Downloading or executing files from the Internet.
- Changing system settings or disabling security tools.
- Encoded or obfuscated commands.
- Unexpectedly launching PowerShell or CMD.

A useful detection pattern is:

`Script interpreter → network download → payload execution`

## 4. Intro to Malware Analysis

Malware analysis examines suspicious software to determine what it is, what it does, what systems it affects, what indicators it leaves, and how defenders can detect/respond to it.

### Who uses it?
- **SOC teams** — write detections.
- **Incident Response** — determine damage and support remediation.
- **Threat Hunting** — extract IOCs and hunt for related activity.
- **Malware Researchers** — improve security-product detections.
- **Threat Research / OS vendors** — understand exploited vulnerabilities and improve security.

## 5. Malware Analysis Safety

Never analyse live malware on a normal personal machine.

Recommended precautions from the material:
1. Use a dedicated analysis machine/VM.
2. Keep samples in password-protected archives when not being analysed.
3. Extract samples only inside the isolated environment.
4. Use clean snapshots.
5. Close or closely monitor Internet connectivity.
6. Revert the VM after analysis.
7. Be careful with shared folders because malware may affect shared files.

## 6. Static vs Dynamic Analysis

### Static analysis
Examines a sample **without executing it**.

Examples:
- File type
- Strings
- Hashes
- PE headers
- Imports/exports
- Sections
- Disassembly

### Dynamic analysis
Observes a sample **while it executes in a controlled environment**.

Examples:
- Processes
- Files
- Registry changes
- Network connections
- Child processes
- Persistence

### Advanced analysis
Uses disassemblers and debuggers to inspect assembly, execution, memory, and CPU state. The supplied material notes this is covered in a later module.

## 7. Basic Static Analysis

### `file`
Use:

```bash
file <filename>
```

This identifies the actual file type rather than trusting the extension. Example output for WannaCry in the supplied material identifies a PE32 Windows executable for Intel 80386.

### `strings`
Use:

```bash
strings <filename>
```

Strings may reveal URLs, paths, API names, messages, library names, and other useful context. For example, `URLDownloadToFile` can suggest downloading a file.

Large output can be redirected:

```bash
strings sample > str
```

or viewed with `more` / `less`.

### Hashing
Common commands:

```bash
md5sum <filename>
sha1sum <filename>
sha256sum <filename>
```

The supplied WannaCry sample had MD5:

`84c82835a5d21bbcf75a61706d8ab549`

Hashes are useful for identifying samples, sharing IOCs, and searching threat-intelligence services. A small file change can produce a different hash.

## 8. VirusTotal

VirusTotal can provide antivirus detections, metadata, submission history, behaviour, relationships, and community comments.

The material recommends searching for a sample's **hash** before uploading a file. This helps avoid unnecessarily exposing sensitive samples.

## 9. PE File Header

PE means **Portable Executable**. Windows executables commonly use this format.

### Imports
Imports are functions used from external libraries. Examples from the material include:
- `RegQueryValue` → Registry interaction.
- `InternetOpen` → Internet communication capability.
- `URLDownloadToFile` → file-download capability.

An imported API indicates capability; it is not by itself proof that the function was actually used during execution.

### Exports
Exports are functions exposed by a PE file for other binaries to use. They are especially associated with DLLs.

### Common sections
- **`.text`** — generally executable CPU instructions.
- **`.data`** — global variables and other data.
- **`.rsrc`** — resources such as icons and images.

Sections can vary with compiler/packer.

## 10. `pecheck`

The supplied Remnux environment includes `pecheck`:

```bash
pecheck <filename>
```

It can show hashes, entropy, sections, PE header information, imports, and warnings.

### Entropy
Entropy is shown from 0.0 to 8.0 in the material. High entropy can be a clue for compressed/encrypted/packed data, but high entropy alone does not prove malware or packing.

## 11. Basic Dynamic Analysis and Sandboxes

Dynamic analysis executes a sample in a controlled environment and observes behaviour.

A useful sandbox can include:
- Lab VM
- Snapshots/revert capability
- Process monitoring
- File monitoring
- Registry monitoring
- Network monitoring
- Controlled DNS/web services

Tools mentioned include **Procmon, Process Explorer, Regshot, Wireshark, and tcpdump**.

### Cuckoo Sandbox
The material describes Cuckoo as a well-known open-source sandbox but notes that the original project is archived and does not support Python 3.

### CAPE Sandbox
Presented as a more advanced alternative with debugging and memory-dumping capabilities and Python 3 support.

### Online sandboxes
Examples mentioned:
- Online Cuckoo Sandbox
- Any.Run
- Intezer
- Hybrid Analysis

Search for a sample's hash before uploading when possible.

## 12. Reading a Sandbox Report

A sandbox report may contain:
- Verdict
- AV detections
- MITRE ATT&CK mappings
- Processes
- File activity
- Network activity
- Extracted files
- Community comments

The supplied Hybrid Analysis example showed process activity, command execution, file/backup deletion, network analysis, extracted strings/files, and ATT&CK mappings.

## 13. Anti-Analysis Techniques

### Packing and obfuscation
Packing may compress, encrypt, or obfuscate a sample. This can hide meaningful strings and imports.

Possible indicators in the supplied example included:
- Very high entropy.
- Mostly garbage strings.
- Few useful imports.
- No normal `.text` section.
- Sections with both execute and write permissions.

Multiple indicators together are more useful than one indicator alone.

### Sandbox evasion
The material describes:
- **Long sleep calls** — wait until a sandbox times out.
- **User activity detection** — check mouse/keyboard activity.
- **User activity footprinting** — check browser history, Office history, user files, etc.
- **VM detection** — look for virtual-machine artifacts and terminate or change behaviour.

## 14. Living Off the Land (LoL)

Living Off the Land means abusing legitimate tools already present on a system rather than relying entirely on custom binaries.

Why attackers use LoL:
- Built-in tools are trusted.
- They are widely available.
- They may be allowed by default controls.
- They can reduce obvious new-file activity.
- Their activity can resemble legitimate administration.
- They support execution, persistence, reconnaissance, and lateral movement.

## 15. Common LoL Tools

### PowerShell
Can be abused for scripting, automation, downloads, and in-memory execution.

### WMI / WMIC
Can be used for system queries, local/remote command execution, and persistence.

### Certutil
A legitimate Windows utility that can be abused for file retrieval and encoding/decoding operations.

### Mshta
Can execute HTA content or scripts and can be abused to bootstrap malicious activity.

### Rundll32
Can invoke DLL exports and can be abused to execute malicious functionality.

### Scheduled Tasks / `schtasks`
Can execute programs at logon or on a schedule and can therefore be abused for persistence.

### Sysinternals
The material mentions tools such as **PsExec** for remote execution and **Autoruns** for persistence discovery/manipulation.

### Linux/Unix equivalents
- **LOLBAS** — Windows living-off-the-land binaries.
- **GTFOBins** — Unix/Linux binaries that can be abused.

## 16. Defending Against LoL

The material recommends:
- Layered endpoint, network, and identity controls.
- Application control such as AppLocker or Windows Defender Application Control.
- Least privilege.
- Network rules and DNS filtering.
- Clear containment playbooks.
- Regular review of permissions, logging, and control lists.

For SOC detection, capture:
- Process creation.
- Full command lines.
- Parent/child process relationships.
- Network connections.
- DNS activity.
- Authentication context.

## 17. Real-World LoL Examples

### APT29 / Nobelium
The material describes PowerShell combined with WMI event subscriptions for persistence and execution, including payload data stored in WMI.

MITRE technique mentioned: **T1546.003 — WMI Event Subscription**.

### BlackCat / ALPHV
The material describes use of legitimate tools including PowerShell, PsExec, and certutil for execution, lateral movement, and payload handling.

### QakBot / IcedID / Cobalt Strike
The material describes loaders such as QakBot and IcedID staging or delivering Cobalt Strike components and attackers abusing signed Windows binaries such as `rundll32.exe` and `mshta.exe`.

## 18. SOC Investigation Mindset

Do not assume:

> “This is a legitimate Windows executable, so it is safe.”

Instead ask:

> “Is this legitimate executable behaving normally in this context?”

Example suspicious process chain:

```text
WINWORD.EXE
    ↓
powershell.exe
    ↓
certutil.exe
    ↓
downloaded payload
```

The individual programs can be legitimate while the overall process chain is suspicious.

## 19. High-Value SOC Indicators

### Process
- Process name
- Parent process
- Child processes
- Full command line
- User account
- Integrity level

### File
- Filename
- Extension
- Path
- Hash
- Creation/modification time
- Digital signature
- PE sections
- Entropy

### Network
- Destination IP
- Domain
- DNS requests
- Port/protocol
- Process responsible for the connection

### Persistence
- Scheduled tasks
- Services
- Registry locations
- WMI event subscriptions
- Startup locations

### Behaviour
- File encryption
- File deletion
- Credential access
- Data collection
- Data exfiltration
- Suspicious PowerShell
- Unusual administrative utilities

## 20. Static vs Dynamic Quick Table

| Feature | Static | Dynamic |
|---|---|---|
| Executes malware? | No | Yes |
| Hashes | Yes | Not the main purpose |
| Strings | Yes | Runtime-generated data may appear |
| PE headers | Yes | Not the main focus |
| Imports | Yes | Actual API activity can be observed |
| Process activity | No | Yes |
| Network activity | No | Yes |
| File changes | No | Yes |
| Registry changes | No | Yes |
| Sandbox | Not required | Commonly used |
| Safety risk | Lower, but isolation is still recommended | Higher |

## 21. Malware Analysis Workflow

```text
Suspicious Sample
       ↓
Isolate / Secure Environment
       ↓
Identify File Type
       ↓
Calculate Hashes
       ↓
Inspect Strings
       ↓
Inspect PE Header
       ↓
Review Imports / Sections / Entropy
       ↓
Search Hash in Threat Intelligence
       ↓
If needed → Dynamic Analysis
       ↓
Monitor Processes / Files / Registry / Network
       ↓
Check MITRE ATT&CK Mapping
       ↓
Extract IOCs
       ↓
Create Detection / Response Actions
```

## 22. Living Off the Land Investigation Workflow

```text
Alert
  ↓
Identify Process
  ↓
Check Parent Process
  ↓
Review Full Command Line
  ↓
Check User / Privileges
  ↓
Check Files Created
  ↓
Check Network Connections
  ↓
Check Persistence
  ↓
Compare With Expected Admin Activity
  ↓
Determine Malicious / Benign Context
  ↓
Contain + Investigate if Malicious
```

## 23. Most Important SOC L1 Takeaways

1. Malware categories are distinguished by behaviour and purpose.
2. Static analysis examines a sample without executing it.
3. Dynamic analysis observes a sample while it executes in a controlled environment.
4. Never execute live malware on your everyday machine.
5. Hashes are useful identifiers and IOCs.
6. Strings provide clues but can be hidden by packing/obfuscation.
7. PE imports can reveal possible capabilities.
8. High entropy can suggest packing/encryption but is not proof.
9. Sandbox reports can reveal process, file, network, and ATT&CK behaviour.
10. Malware can evade sandboxes using sleep, user-activity checks, and VM detection.
11. Living Off the Land abuses legitimate built-in tools.
12. PowerShell, WMI, certutil, mshta, rundll32, and scheduled tasks require contextual scrutiny.
13. A legitimate executable can be maliciously used.
14. Process trees and full command lines are extremely valuable during SOC investigations.
15. Context matters more than simply looking at an executable name.

## 24. Final SOC Mindset

The important skill is not memorising every malware name or every Windows utility. The important skill is recognising **behaviour and context**.

Ask:

- What process started this?
- What command did it execute?
- Who executed it?
- What files did it touch?
- What network connection did it make?
- Did it establish persistence?
- Is this normal for this user and machine?
- Does the activity match known malicious behaviour?

This mindset connects malware analysis directly to SOC alert triage, threat hunting, detection engineering, and incident response.
