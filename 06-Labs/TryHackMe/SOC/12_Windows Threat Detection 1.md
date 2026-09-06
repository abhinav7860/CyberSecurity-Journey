# TryHackMe - Windows Threat Detection 1

**Date:** 2026-09-06  
**Room:** Windows Threat Detection 1  
**Platform:** TryHackMe

---

## What this room was about

In this room, I used the Windows logging knowledge from the **Windows Logging for SOC** room to investigate common **Initial Access** techniques.

The main techniques I covered were:

- Initial Access through exposed services
- RDP brute force
- Phishing attachments
- Malicious LNK files
- Double-extension files
- Sysmon process/file/network events
- USB-based Initial Access

The main thing I learned was how to take Windows logs and reconstruct what happened during an attack.

---

# Task 1 - Introduction

This room focuses on detecting common Initial Access techniques using Windows event logs.

As a SOC analyst, I need to understand:

- What the attacker did
- How they gained access
- Which user was involved
- Which process was executed
- What files were created
- Where the malware connected
- How the attack continued after Initial Access

The Windows logs learned in the previous room are used throughout this investigation.

---

# Task 2 - Intro to Initial Access

## What is Initial Access?

**Initial Access** is the stage where a threat actor first gains access to a system or environment.

There are many ways this can happen, but in this room I grouped them into two main categories:

### 1. Exposed Services

These are services that are accessible from the Internet.

Examples:

- RDP
- Mail servers
- Web applications
- MS SQL

Attackers can scan exposed systems and look for:

- Weak passwords
- Vulnerable software
- Misconfigurations

Two important MITRE ATT&CK techniques are:

- **T1133 - External Remote Services**
- **T1190 - Exploit Public-Facing Application**

### 2. User-Driven Methods

These attacks depend on the victim interacting with something malicious.

Examples:

- Phishing emails
- Malicious attachments
- Infected USB devices
- Malicious links

Important MITRE techniques include:

- **T1566 - Phishing**
- **T1091 - Replication Through Removable Media**

## Questions

### Which MITRE technique describes Initial Access via a vulnerable mail server?

```text
T1190
```

### Which Initial Access method relies on a user opening a malicious email attachment?

```text
phishing
```

---

# Task 3 - Initial Access via RDP

## Risks of Exposed RDP

RDP allows users to remotely access Windows systems.

If RDP is exposed directly to the Internet and weak credentials are used, attackers can discover the service and attempt to brute-force it.

A large number of failed login attempts can generate many **4625** events.

If the attacker eventually succeeds, a **4624** successful logon event can reveal the account used.

## Detecting an RDP Brute Force

I used the following process:

1. Open the Security logs.
2. Filter for Event ID `4625`.
3. Look for Logon Type `3` and `10`.
4. Check the Source IP.
5. Look for repeated failed attempts.
6. Identify the account being targeted.
7. Switch to Event ID `4624`.
8. Find the successful RDP login.
9. Check the account that was accessed.
10. Record the Logon ID.
11. Use the Logon ID to correlate later activity.

### Useful Logon Types

```text
3  = Network Logon
10 = Remote Interactive / RDP Logon
```

## Practice - RDP Case

I investigated:

```text
C:\Users\Administrator\Desktop\Practice\RDP Case\RDP-Security.evtx
```

### Which user seems to be most actively brute-forced by botnets?

```text
administrator
```

### Which IP managed to breach the host via RDP (Logon Type 10)?

```text
203.205.34.107
```

### What was the real Workstation Name (hostname) of the threat actor?

```text
DESKTOP-QNBC4UU
```

## What I learned

The important part here was not just finding the successful login.

I had to connect:

```text
4625 Failed Logons
        ↓
Brute Force
        ↓
4624 Successful Logon
        ↓
Logon Type 10
        ↓
Source IP
        ↓
Workstation Name
```

This gives me a much better picture of how the attacker gained access.

---

# Task 4 - Initial Access via Phishing

## Phishing

Phishing is one of the most common user-driven Initial Access techniques.

Instead of directly attacking a server, the attacker tricks a user into opening something malicious.

Two examples covered in this task were:

- Malicious binary attachments
- Malicious LNK attachments

## Malicious Binary Attachments

Windows supports many executable file extensions.

Examples include:

```text
.exe
.com
.scr
.cpl
```

Attackers can also use **double extensions** to make malicious files look legitimate.

Example:

```text
invoice.pdf.exe
```

Windows can hide known file extensions, which makes the file appear more trustworthy to an inexperienced user.

## LNK Attachments

LNK files are Windows shortcut files.

Attackers can modify the **Target** field of an LNK file so that clicking it launches a malicious command instead of the expected program.

A simplified attack chain is:

```text
LNK
 ↓
PowerShell
 ↓
Download malware
 ↓
Execute malware
```

## Phishing Case 1

I ran the `www.skype.com` file from the **Phishing Case 1** folder.

### Flag

```text
THM{misleading_extension}
```

## Phishing Case 2

I investigated the second attachment.

### URL from which the malicious LNK downloaded the next-stage malware

```text
http://wp16.hqywlqpa.thm:8000/cgi-bin/f
```

## Phishing Case 3

I checked the contents of the third phishing case.

### Double-extension file

```text
best-cat.jpg.exe
```

The `.jpg.exe` naming makes the file look like an image at first glance, while it is actually an executable.

---

# Task 5 - Continuing the Phishing Topic

## Detecting Malicious Downloads

Sysmon is useful for reconstructing a malicious download because several events can appear in sequence.

A typical chain can look like:

```text
1. Web browser starts
        ↓
2. Archive downloaded
        ↓
3. Archive extracted
        ↓
4. Suspicious executable appears
        ↓
5. Executable launched
```

## Example Sysmon Chain

### Event ID 1 - Browser launched

```text
Image:
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
```

### Event ID 11 - Archive downloaded

```text
TargetFilename:
C:\Users\User\Downloads\invoice.zip
```

### Event ID 11 - Suspicious file extracted

```text
TargetFilename:
C:\Users\User\Downloads\invoice.pdf.exe
```

### Event ID 1 - Malware launched

```text
Image:
C:\Users\User\Downloads\invoice.pdf.exe
```

This sequence can help me identify the complete attack chain.

## LNK Investigation

LNK execution can be harder to identify because the execution may appear as:

```text
explorer.exe
    ↓
powershell.exe
```

The LNK itself may not leave an obvious process creation event.

Because of this, I should also look for the preceding file creation event showing that the LNK appeared in the Downloads folder.

## Practice - Phishing Case 3

I investigated:

```text
C:\Users\Administrator\Desktop\Practice\Phishing Case 3\Phishing-Sysmon.evtx
```

### Which file did the user download via the web browser?

```text
C:\Users\Administrator\Downloads\top-cats.zip
```

### In which folder did the user unarchive the suspicious file?

```text
C:\Users\Administrator\Pictures
```

### What is the Process ID of the launched phishing malware?

```text
5484
```

### Which malicious domain did the malware try to connect to?

```text
rjj.store
```

## Attack Chain

```text
Web Browser
    ↓
top-cats.zip downloaded
    ↓
Archive extracted
    ↓
Suspicious file placed in Pictures
    ↓
Phishing malware launched
    ↓
PID 5484
    ↓
Connection attempt
    ↓
rjj.store
```

---

# Task 6 - Initial Access via USB

## Risks of Removable Media

USB devices can also be used for Initial Access.

An infected USB can bypass many network security controls because the malicious content is introduced directly into the computer.

A common attack scenario is:

```text
Attacker infects USB
        ↓
USB is delivered to victim
        ↓
Victim plugs USB into PC
        ↓
Victim opens malicious file
        ↓
Malware executes
        ↓
Infection spreads
```

## Common USB Malware Techniques

Attackers can make malicious files look legitimate.

Examples include:

```text
RECOVERY.lnk
Photos.exe
photo_2024_1_12.jpg.exe
```

They may also hide legitimate files and replace them with malicious shortcuts.

## Detecting USB Execution

One useful clue in Sysmon Event ID `1` is the drive letter.

For example:

```text
E:\malware.exe
```

An executable starting from `E:` instead of the normal system drive can indicate that it was launched from a removable device.

However, the drive letter alone is not enough. I should correlate it with other events to understand the attack.

## Practice - USB Case

I investigated:

```text
C:\Users\Administrator\Desktop\Practice\USB Case\USB-Sysmon.evtx
```

### Which USB file was launched by the user?

```text
E:\Open Sandisk 4GB USB.exe
```

### Which suspicious file did the malware drop to the disk?

```text
C:\Users\Public\Documents\winupdate.exe
```

### To which other USB did the malware propagate?

```text
F:
```

## Attack Chain

```text
User launches:
E:\Open Sandisk 4GB USB.exe
        ↓
Malware executes
        ↓
Drops:
C:\Users\Public\Documents\winupdate.exe
        ↓
Malware propagates
        ↓
F:
```

---

# Important Things I Learned

## 1. Initial Access can happen in different ways

I learned to think about Initial Access in two broad categories:

```text
Exposed Services
    ├── RDP
    ├── Mail Server
    └── Public-Facing Applications

User-Driven
    ├── Phishing
    └── USB / Removable Media
```

## 2. Event ID 4625 is useful for brute-force detection

A large number of failed logons can indicate brute force or password spraying.

I should check:

- Username
- Source IP
- Logon Type
- Number of attempts
- Time pattern

## 3. Event ID 4624 can reveal successful Initial Access

After identifying a brute-force attack, I can search for a successful `4624` event.

For RDP, I should pay attention to:

```text
Logon Type: 10
```

I can then use the Logon ID to correlate further events.

## 4. Sysmon helps reconstruct the attack

Sysmon provides useful information such as:

- Process ID
- Parent Process ID
- Process path
- Command line
- File creation
- Network connections
- DNS queries

This makes it possible to build an attack timeline.

## 5. File names can be misleading

Examples such as:

```text
invoice.pdf.exe
best-cat.jpg.exe
```

show why I should not trust the displayed filename alone.

I need to check the actual extension and investigate the process that launched the file.

---

# Useful Event IDs

| Event ID | Source | Meaning |
|---|---|---|
| **4624** | Security | Successful Logon |
| **4625** | Security | Failed Logon |
| **4688** | Security | Process Creation |
| **1** | Sysmon | Process Creation |
| **3** | Sysmon | Network Connection |
| **11** | Sysmon | File Create |
| **22** | Sysmon | DNS Query |

---

# My Main Takeaway

The biggest thing I learned from this room is how to move from a single suspicious event to a complete attack story.

For example:

```text
Brute Force
    ↓
Successful RDP Login
    ↓
Compromised Account
    ↓
Malicious Process
    ↓
File Creation
    ↓
Network Connection
```

Or for phishing:

```text
Browser
    ↓
Malicious Download
    ↓
Archive Extraction
    ↓
Executable
    ↓
Process Creation
    ↓
C2 Connection
```

As a SOC analyst, I should not just look at one event and make a decision. I should **correlate related events, check the timeline, identify the user/process involved, and determine what happened before and after the suspicious activity.**
