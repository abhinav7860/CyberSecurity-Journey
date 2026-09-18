# File and Hash Threat Intel --- TryHackMe

**Date:** 18 September 2026\
**Path:** SOC Level 1 → File and Hash Threat Intel

## What I learned

This room taught me how to investigate suspicious files from the first
clue to useful threat intelligence.

My basic workflow is:

``` text
Verify → Enrich → Decide
```

File and hash intelligence mainly belongs to the **enrich** stage.

A filename alone does not prove that a file is malicious. I need to
collect more evidence:

``` text
Filename / Path
      ↓
File Hash
      ↓
VirusTotal / MalwareBazaar
      ↓
Sandbox
      ↓
Behaviour
      ↓
MITRE ATT&CK
      ↓
Actionable Intelligence
```

I used Medium walkthroughs to cross-check the practical steps and
answers. The walkthroughs confirm the same investigation flow and
answers used below.

------------------------------------------------------------------------

# Task 2 --- Filenames and Paths

## Why filenames and paths matter

A suspicious file's filename, extension and location are some of the
first clues available to a SOC analyst.

They are **clues, not proof**.

Attackers can make malicious files look normal by renaming them or
placing them in locations that look legitimate.

Common locations worth investigating include:

``` text
C:\Users\Public\
C:\Windows\Temp\
C:\ProgramData\
```

## Filename tricks

### Double extensions

Example:

``` text
invoice.pdf.exe
```

The attacker wants the victim to think the file is a PDF, while the real
extension is `.exe`.

### System binary impersonation

Example:

``` text
scvhost.exe
```

This looks similar to the legitimate:

``` text
svchost.exe
```

### Random names

Example:

``` text
jh8F21.exe
```

Random-looking names can be seen in malware campaigns.

### Masquerading

A malicious executable can be given a normal-looking business filename
such as:

``` text
backup-2300.exe
```

------------------------------------------------------------------------

## My investigation

I opened:

``` text
Desktop → CTI Files
```

and checked the files and their properties.

The suspicious file was:

``` text
payroll.pdf
```

The indicator was:

``` text
double extensions
```

### Answer

``` text
payroll.pdf, double extensions
```

The important lesson is that I should check the **real file type**, not
just trust the filename.

------------------------------------------------------------------------

# Task 3 --- File Hash Lookup

## Why hashes matter

Attackers can rename malware easily:

``` text
malware.exe
    ↓
invoice.exe
    ↓
svchost.exe
```

The filename changes, but the file's bytes remain the same.

A cryptographic hash acts like a fingerprint for those bytes.

For this room I mainly used:

``` text
SHA256
MD5
```

The important relationship is:

``` text
Same bytes → Same hash
Changed bytes → Different hash
```

Even a small change to a file changes its hash.

## Generate SHA256

### Windows CMD

``` powershell
certutil -hashfile bl0gger.exe SHA256
```

### PowerShell

``` powershell
Get-FileHash -Algorithm SHA256 bl0gger.exe
```

### Linux

``` bash
sha256sum bl0gger.exe
```

------------------------------------------------------------------------

# VirusTotal

I can search VirusTotal using a hash instead of uploading or executing a
suspicious file.

Useful information includes:

-   Detection score
-   Threat labels
-   File type
-   File size
-   Submission history
-   Domains and IPs
-   Related files
-   Behaviour
-   MITRE ATT&CK techniques

The hash becomes a pivot point for the investigation.

------------------------------------------------------------------------

## bl0gger.exe --- Step by step

### Step 1 --- Get the hash

The SHA256 was:

``` text
2672b6688d7b32a90f9153d2ff607d6801e6cbde61f509ed36d0450745998d58
```

### Step 2 --- Search VirusTotal

I pasted the hash into VirusTotal.

The threat classification was:

``` text
trojan.graftor/blackmoon
```

### Step 3 --- Check history

I opened the file's details/history and checked its first submission.

``` text
2025-05-15 12:03:49 UTC
```

------------------------------------------------------------------------

# Morse-Code-Analyzer

The next step was to investigate another file using its hash.

The workflow was:

``` text
Morse-Code-Analyzer
        ↓
SHA256
        ↓
MalwareBazaar / VirusTotal
        ↓
Vendor information
        ↓
Behaviour
```

## MalwareBazaar

I searched MalwareBazaar using:

``` text
sha256:<file_hash>
```

The vendor that classified the file as non-malicious was:

``` text
CyberFortress
```

## VirusTotal behaviour

I opened the **Behavior** section and checked persistence and privilege
escalation.

The flagged technique was:

``` text
DLL Side-Loading
```

DLL side-loading is a technique where a legitimate program can be abused
to load a malicious DLL.

------------------------------------------------------------------------

# Task 4 --- Sandbox Analysis

## Static vs Dynamic Analysis

Static analysis looks at the file without executing it.

Examples:

``` text
Hash
Filename
Strings
Imports
Metadata
```

Dynamic analysis looks at what happens when the file runs.

Examples:

``` text
Processes
Files created
Registry changes
Network connections
Commands
DNS requests
```

A sandbox provides an isolated environment where suspicious files can be
executed and observed.

The main questions are:

``` text
Does the file execute?
What does it change?
What does it connect to?
What processes does it create?
What ATT&CK techniques does it show?
```

------------------------------------------------------------------------

# Hybrid Analysis --- bl0gger.exe

I searched Hybrid Analysis using the SHA256 hash.

## Step 1 --- Find the tags

I opened the report overview and checked the tags.

The tags were:

``` text
BlackMoon
Discovery
windows-server-utility
```

## Step 2 --- Find the stealth command

I checked the **Anti-detection / Stealthness** section.

The command was:

``` text
regsvr32 %WINDIR%\Media\ActiveX.ocx /s
```

`regsvr32` is a legitimate Windows utility that can be abused by
attackers.

`%WINDIR%` refers to the Windows directory.

`/s` makes the operation silent.

## Step 3 --- Check the process tree

The process tree showed:

``` text
werfault.exe
```

Process trees are useful because they show parent-child relationships
between processes.

------------------------------------------------------------------------

# payroll.pdf --- Continue the Investigation

This was the same suspicious file I found in Task 2.

Now I used its hash to investigate it in the sandbox.

## Step 1 --- Get the hash

I generated the file hash so I could search for the exact binary.

``` text
payroll.pdf
     ↓
SHA256
     ↓
Hybrid Analysis
```

## Step 2 --- Find the original filename

In the file properties I checked the original name.

The application was masquerading as:

``` text
svchost.exe
```

This is suspicious because `svchost.exe` is a legitimate Windows system
process.

A SOC analyst should not trust a filename just because it looks like a
Windows file. The path, hash and actual file properties also matter.

## Step 3 --- Find the associated URL

I opened the **Associated URLs** section.

The associated URL was:

``` text
hxxp://121.182.174.27:3000/server.exe
```

I keep the URL defanged here so it cannot be accidentally opened.

This gives me another IOC.

## Step 4 --- Check extracted strings

I opened the extracted strings information.

The sandbox identified:

``` text
454
```

strings.

Strings can reveal useful clues such as:

-   URLs
-   Commands
-   File paths
-   Domains
-   Registry paths

------------------------------------------------------------------------

# Task 5 --- Threat Intelligence Challenge

The final investigation used:

``` text
Challenge.bin.sample
```

This task made me use everything I had learned.

------------------------------------------------------------------------

## Step 1 --- Find the SHA256

The SHA256 hash was:

``` text
43b0ac119ff957bb209d86ec206ea1ec3c51dd87bebf7b4a649c7e6c7f3756e7
```

I used this hash as my main pivot.

------------------------------------------------------------------------

## Step 2 --- Search VirusTotal

I searched the SHA256 in VirusTotal.

The family labels were:

``` text
akira
filecryptor
```

These labels give me context about the malware family associated with
the sample.

I should still correlate labels with behaviour rather than relying on
one label alone.

------------------------------------------------------------------------

## Step 3 --- Find the first recorded date

I checked the historical information.

The first time the file was recorded in the wild was:

``` text
2024-10-30 17:17:24 UTC
```

This gives me useful timeline information.

------------------------------------------------------------------------

## Step 4 --- Check the sandbox behaviour

Next I checked the execution behaviour.

The malware dropped:

``` text
akira_readme.txt
```

A dropped file is another runtime IOC.

My investigation now looked like:

``` text
Challenge.bin.sample
        ↓
SHA256
        ↓
VirusTotal
        ↓
akira / filecryptor
        ↓
Sandbox
        ↓
akira_readme.txt
```

------------------------------------------------------------------------

## Step 5 --- Find the PowerShell command

I opened the behaviour/activity information and checked the processes
created.

The PowerShell command was:

``` powershell
Get-WmiObject Win32_Shadowcopy | Remove-WmiObject
```

### Understanding it

First:

``` powershell
Get-WmiObject Win32_Shadowcopy
```

This retrieves information about Windows **Volume Shadow Copies**.

Shadow Copies are snapshots that can help with system recovery.

Then:

``` text
|
```

The pipe sends the result into the next command.

Finally:

``` powershell
Remove-WmiObject
```

removes the objects returned by the first command.

So, in simple terms:

``` text
Find Shadow Copies
       ↓
Remove Shadow Copies
```

This is important in a ransomware investigation because removing
recovery copies can make system recovery harder.

------------------------------------------------------------------------

## Step 6 --- Map it to MITRE ATT&CK

I now had a specific behaviour:

``` text
Remove Volume Shadow Copies
```

I mapped that behaviour to MITRE ATT&CK.

The technique ID was:

``` text
T1490
```

The technique name is:

``` text
Inhibit System Recovery
```

So the complete reasoning is:

``` text
PowerShell
    ↓
Get Shadow Copies
    ↓
Remove Shadow Copies
    ↓
Make recovery harder
    ↓
MITRE ATT&CK
    ↓
T1490 — Inhibit System Recovery
```

------------------------------------------------------------------------

# Final Threat Intelligence Chain

This is the investigation process I want to remember:

``` text
Suspicious File
      ↓
Filename / Path Analysis
      ↓
SHA256
      ↓
VirusTotal
      ↓
MalwareBazaar
      ↓
Sandbox
      ↓
Process / Network / File Behaviour
      ↓
Extract IOCs
      ↓
MITRE ATT&CK
      ↓
Actionable Threat Intelligence
```

------------------------------------------------------------------------

# All Answers

## Task 2

``` text
payroll.pdf, double extensions
```

## Task 3

``` text
SHA256:
2672b6688d7b32a90f9153d2ff607d6801e6cbde61f509ed36d0450745998d58

Threat classification:
trojan.graftor/blackmoon

First submission:
2025-05-15 12:03:49 UTC

Non-malicious vendor:
CyberFortress

MITRE technique:
DLL Side-Loading
```

## Task 4

``` text
Tags:
BlackMoon, Discovery, windows-server-utility

Stealth command:
regsvr32 %WINDIR%\Media\ActiveX.ocx /s

Spawned process:
werfault.exe

payroll.pdf masquerading as:
svchost.exe

Associated URL:
hxxp://121.182.174.27:3000/server.exe

Extracted strings:
454
```

## Task 5

``` text
SHA256:
43b0ac119ff957bb209d86ec206ea1ec3c51dd87bebf7b4a649c7e6c7f3756e7

Family labels:
akira, filecryptor

First recorded:
2024-10-30 17:17:24 UTC

Dropped file:
akira_readme.txt

PowerShell command:
Get-WmiObject Win32_Shadowcopy | Remove-WmiObject

MITRE ATT&CK:
T1490

Technique:
Inhibit System Recovery
```

------------------------------------------------------------------------

# What I should remember

### 1. Filename ≠ identity

A malware file can be renamed.

### 2. Hash = fingerprint

``` text
Filename can change
Hash identifies the exact file bytes
```

### 3. VirusTotal = enrichment

It can give me detections, labels, history, relationships and behaviour.

### 4. MalwareBazaar = malware intelligence

I can search using:

``` text
sha256:<hash>
```

### 5. Sandbox = behaviour

``` text
Static analysis → What is the file?
Dynamic analysis → What does the file do?
```

### 6. Process trees matter

They help me answer:

``` text
Who started what?
```

### 7. Legitimate Windows tools can be abused

For example:

``` text
regsvr32
```

is legitimate, but its use in a suspicious chain can be important.

### 8. Map behaviour to ATT&CK

Instead of only saying:

``` text
The malware removed shadow copies.
```

I can report:

``` text
T1490 — Inhibit System Recovery
```

------------------------------------------------------------------------

# My takeaway

The biggest lesson from this room is that threat intelligence is a
**chain of evidence**.

I should not stop at:

``` text
"I found a suspicious file."
```

I should continue:

``` text
Suspicious file
      ↓
Check filename/path
      ↓
Calculate SHA256
      ↓
Search VirusTotal
      ↓
Search MalwareBazaar
      ↓
Check sandbox reports
      ↓
Investigate processes and network activity
      ↓
Extract useful IOCs
      ↓
Map behaviour to MITRE ATT&CK
      ↓
Build an actionable threat picture
```

That is how I want to approach file-based alerts as a SOC L1 analyst.
