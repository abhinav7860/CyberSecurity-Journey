# TryHackMe - Windows Threat Detection 3

**Date:** 2026-09-07  
**Room:** Windows Threat Detection 3

## What this room was about

This room completed my Windows Threat Detection journey. I focused on:

- Command and Control (C2)
- Persistence
- Impact
- Detecting these activities using Windows Security and Sysmon logs

---

# Task 1 - Introduction

After gaining Initial Access, attackers may want to stay on the system and maintain control.

A typical attack can look like:

```text
Initial Access → C2 → Persistence → Further Activity → Impact
```

The three main tactics covered in this room were **Command and Control, Persistence, and Impact**.

---

# Task 2 - Command and Control

## What is C2?

Command and Control (C2) is the communication channel between an attacker and a compromised machine.

An attacker may initially use a phishing attachment to establish C2, or download another C2 malware and hide it somewhere on the system.

Typical chain:

```text
Phishing Attachment
       ↓
Download C2 Malware
       ↓
Hide Malware
       ↓
Execute Malware
       ↓
Connect to C2 Server
```

## Practice

Log file:

```text
C:\Users\Administrator\Desktop\Practice\Task 2\Sysmon.evtx
```

### Which suspicious archive did the user download?

```text
URGENT!.zip
```

### Where did the attackers hide the C2 malware file?

```text
C:\Users\Administrator\AppData\Roaming\update.exe
```

### What is the domain of the C2 server?

```text
route.m365officesync.workers.dev
```

---

# Task 3 - Persistence Overview

## What is Persistence?

Persistence allows attackers to maintain access even after events such as a reboot or password change.

One method is creating a new backdoor user and adding it to a privileged group.

### Create a user

```cmd
net user "mr.backd00r" "p@ssw0rd!" /add
```

### Add the user to Administrators

```cmd
net localgroup Administrators "mr.backd00r" /add
```

## Important Security Event IDs

| Event ID | Meaning |
|---|---|
| **4720** | User account created |
| **4732** | User added to a local security group |
| **4724** | Password reset |

## Practice

Log file:

```text
C:\Users\Administrator\Desktop\Practice\Task 3\Security.evtx
```

### How many times did the threat actor fail to log in to Administrator?

```text
6
```

### Which backdoor user did the attacker create?

```text
support
```

### Which privileged group was the backdoor user added to?

```text
Administrators
```

Attack chain:

```text
Failed Logins
    ↓
Successful Login
    ↓
Create support User
    ↓
Add to Administrators
    ↓
Persistent Privileged Account
```

---

# Task 4 - Persistence: Tasks and Services

Attackers can abuse Windows Services and Scheduled Tasks to make malware run automatically.

## Windows Services

Example:

```cmd
sc create "BadService" binpath= "C:\malware.exe" start= auto
```

Useful events:

```text
Sysmon Event ID 1 → Launch of sc.exe
Security Event ID 4697 → Service creation
System Event ID 7045 → New service
```

## Scheduled Tasks

Example:

```cmd
schtasks /create /tn "BadTask" /tr "C:\malware.exe" /sc onstart /ru System
```

Useful events:

```text
Sysmon Event ID 1 → schtasks.exe
Security Event ID 4698 → Scheduled task creation
```

## Practice

Folder:

```text
C:\Users\Administrator\Desktop\Practice\Task 4\
```

### Which Windows service was created to persist the Nessie malware?

```text
GoogleChromeElevationService
```

### Which scheduled task was created to persist the Troy malware?

```text
AmazonSync
```

### What flag did I get after finding and running Troy?

```text
THM{c2_is_on_schedule!}
```

---

# Task 5 - Persistence: Run Keys and Startup

## Startup Folder

A program placed in the Startup folder can automatically run when the user logs in.

User Startup folder:

```text
C:\Users\<USER>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\
```

All users:

```text
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```

Startup file creation can be detected with:

```text
Sysmon Event ID 11
```

## Run Keys

User Run key:

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

All users:

```text
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
```

Example:

```cmd
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v BadKey /t REG_SZ /d "C:\malware.exe"
```

Registry changes can be detected with:

```text
Sysmon Event ID 13
```

## Practice

Folder:

```text
C:\Users\Administrator\Desktop\Practice\Task 5\
```

### What is the parent process image of the Odin malware?

```text
C:\Windows\explorer.exe
```

### What is the last line that Odin outputs?

```text
done doing bad stuff
```

### What flag did I get after finding and running Kitten?

```text
THM{persisting_in_basket!}
```

Important detection points:

```text
Event ID 11 → Suspicious file in Startup folder
Event ID 13 → Suspicious Run key modification
```

---

# Task 6 - Impact and Threat Detection Recap

## Why Persistence Matters

Attackers may maintain persistence because they want to:

1. Add the host to a botnet
2. Spy on the victim
3. Use the host as an entry point into a larger network
4. Continue attacking the environment
5. Deploy ransomware

## Active Directory and Ransomware

Corporate Windows environments commonly use Active Directory. Once an attacker gets a foothold, they may move through the network, steal credentials and eventually deploy ransomware.

Ransomware can:

- Encrypt systems
- Disrupt business operations
- Steal data
- Affect many systems at once

## Final Questions

### What is the biggest threat to most corporate Windows networks?

```text
ransomware
```

### At which stage is it best to detect and stop the attack?

```text
initial access
```

---

# Important Windows Event IDs

| Event ID | Log | What it shows |
|---|---|---|
| **1** | Sysmon | Process creation |
| **11** | Sysmon | File creation |
| **13** | Sysmon | Registry value modification |
| **4720** | Security | User account creation |
| **4724** | Security | Password reset |
| **4732** | Security | User added to local group |
| **4697** | Security | Service installation |
| **4698** | Security | Scheduled task creation |
| **7045** | System | New service installed |

---

# My Main Takeaway

This room completed my Windows Threat Detection series.

The overall attack flow I learned was:

```text
Initial Access
      ↓
Discovery
      ↓
Collection
      ↓
Command & Control
      ↓
Persistence
      ↓
Impact
```

The main lesson for me is that I should correlate events instead of looking at them individually.

For example:

```text
Suspicious Process
      ↓
File Creation
      ↓
Registry Change
      ↓
Network Connection
      ↓
Persistence / C2
```

A legitimate command or tool is not automatically malicious. The important things are the **parent process, command line, timing, destination, file activity and what happens next**.

The earlier I detect the attack, ideally during **Initial Access**, the better chance I have of stopping it before persistence, data theft or ransomware deployment.
