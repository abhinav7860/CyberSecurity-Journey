# Windows Fundamentals
**Platform:** InfoSecLab  
**Category:** Windows Basics 

---

# 1. Windows File System

Unlike Linux, Windows organizes storage using **drive letters** such as **C:** or **D:**.

Example:

```
C:\
│
├── Windows
├── Program Files
├── Program Files (x86)
└── Users
```

---

## Important Directories

### C:\

- Default Windows installation drive.
- Contains the operating system.

---

### C:\Windows\System32

Contains critical Windows system files.

Examples:

- cmd.exe
- taskmgr.exe
- DLL files

---

### C:\Users

Contains user profiles.

Each profile stores:

- Desktop
- Documents
- Downloads
- AppData (hidden)

AppData often contains:

- Browser history
- Application settings
- Temporary files

This folder is commonly examined during forensic investigations.

---

### C:\Program Files

Stores installed **64-bit applications**.

---

### C:\Program Files (x86)

Stores **32-bit applications**.

---

# Windows File Systems

## NTFS (New Technology File System)

Default Windows file system.

Features:

- File permissions
- Encryption (EFS)
- Compression
- Alternate Data Streams (ADS)
- Access Control Lists (ACL)

---

## FAT32

Older file system.

Limitations:

- Maximum file size = **4 GB**
- No security permissions

Mostly used for:

- USB drives
- Older devices

---

## exFAT

Designed for flash storage.

Features:

- Supports files larger than 4 GB
- Cross-platform compatibility

Limitation:

- No detailed security permissions

---

# Alternate Data Streams (ADS)

NTFS supports multiple hidden data streams inside a file.

Example:

```cmd
echo "Hidden Data" > normal.txt:hidden.exe
```

The file appears normal.

To view ADS:

```cmd
dir /R
```

Example:

```
normal.txt
normal.txt:hidden.exe:$DATA
```

Attackers sometimes use ADS to hide malware.

---

# Access Control Lists (ACL)

Windows uses ACLs to define who can access files and folders.

Useful command:

```cmd
icacls C:\Windows\System32
```

Used to:

- View permissions
- Modify permissions

---

# Summary

- Windows system drive is **C:**
- NTFS supports permissions and encryption
- FAT32 maximum file size is **4 GB**
- ADS can hide data
- ACLs manage permissions

---

# 2. User Account Control (UAC)

User Account Control prevents programs from silently gaining administrator privileges.

Even administrators normally run with **Medium Integrity**.

Administrative actions require user approval.

---

# UAC Shield Colors

### Blue Shield

- Trusted application
- Microsoft application
- Digitally signed

---

### Yellow / Orange Shield

- Unknown publisher
- Unsigned application

---

### Red Shield

- Blocked application
- Restricted by policy

---

# UAC Levels

## Always Notify

Most secure setting.

Prompts for:

- Software installation
- System changes
- Windows settings

---

## Notify (Default)

Prompts only when applications make changes.

---

## Notify (No Desktop Dim)

Same as default.

Does not switch to Secure Desktop.

Less secure.

---

## Never Notify

Least secure.

Programs can elevate without confirmation.

---

# Integrity Levels

Windows separates processes into integrity levels.

## System

Highest privilege.

Examples:

- Windows kernel
- Core services

---

## High

Administrator processes.

---

## Medium

Normal user applications.

---

## Low

Sandboxed applications.

Example:

- Web browsers

---

# Security Note

Attackers often abuse Windows auto-elevating binaries (such as **fodhelper.exe**) to bypass UAC.

---

# Summary

- UAC = User Account Control
- Blue shield = Trusted
- Always Notify = Most secure
- Medium Integrity = Standard user
- High Integrity = Administrator

---

# 3. Windows Registry

The Windows Registry is a hierarchical database storing operating system and application settings.

GUI tool:

```
regedit
```

Command line:

```cmd
reg query
```

PowerShell:

```powershell
Get-ItemProperty
```

---

# Registry Hives

## HKLM

HKEY_LOCAL_MACHINE

Stores:

- System-wide settings
- Drivers
- Installed software

---

## HKCU

HKEY_CURRENT_USER

Stores:

- User preferences
- Desktop settings
- Wallpapers

---

## HKCR

File associations.

Example:

```
.pdf
.docx
```

---

## HKU

All loaded user profiles.

---

## HKCC

Current hardware configuration.

---

# Registry Data Types

## REG_SZ

Stores text strings.

---

## REG_DWORD

Stores 32-bit integers.

Usually:

```
0 = Disabled

1 = Enabled
```

---

## REG_BINARY

Binary data.

---

## REG_MULTI_SZ

Multiple strings.

---

# Registry Persistence

Attackers often use Run Keys.

Example:

```
HKLM\Software\Microsoft\Windows\CurrentVersion\Run
```

Anything placed here executes automatically after login.

---

# Useful Forensic Artifacts

### USBSTOR

History of USB devices.

---

### ShellBags

Folders previously opened.

---

### ShimCache / AmCache

Previously executed programs.

Useful during malware investigations.

---

# Summary

- GUI tool = regedit
- HKLM = System settings
- HKCU = Current user
- REG_SZ = Text
- Run Keys provide persistence

---

# 4. Active Directory

Active Directory (AD) is Microsoft's centralized directory service.

It manages:

- Users
- Computers
- Groups
- Printers
- Shared resources

---

# Domain Controller (DC)

The Domain Controller authenticates:

- Users
- Computers

It also enforces security policies.

Database:

```
ntds.dit
```

---

# Active Directory Structure

## Objects

Examples:

- User
- Computer
- Group

---

## Organizational Units (OUs)

Logical containers.

Example:

```
Finance
HR
IT
```

Used to apply policies.

---

## Domains

Logical security boundary.

Example:

```
company.local
```

---

## Trees

Collection of related domains.

---

## Forests

Collection of multiple domain trees.

Highest AD boundary.

---

# Authentication Protocols

## NTLM

Legacy protocol.

Uses:

Challenge-Response authentication.

Weaknesses:

- Pass-the-Hash
- Offline cracking

---

## Kerberos

Default AD authentication protocol.

Uses tickets.

---

### Kerberos Workflow

1. User logs in.
2. DC issues TGT.
3. User requests TGS.
4. User accesses service.

---

# Common AD Attacks

- Kerberoasting
- Golden Ticket

---

# Summary

- AD = Centralized identity management
- DC authenticates users
- Kerberos is the primary authentication protocol
- NTLM is legacy

---

# 5. PowerShell Fundamentals

PowerShell is Microsoft's object-oriented command-line shell.

---

# Cmdlets

Naming format:

```
Verb-Noun
```

Examples:

```powershell
Get-Service

Get-Process

Start-Process

Set-ExecutionPolicy
```

---

# Useful Aliases

```
ls

↓

Get-ChildItem
```

```
cat

↓

Get-Content
```

```
ps

↓

Get-Process
```

---

# PowerShell Pipeline

Unlike CMD, PowerShell passes **objects**, not plain text.

Example:

```powershell
Get-Process |
Sort-Object CPU -Descending |
Select-Object -First 5
```

---

# PowerShell Scripts

Extension:

```
.ps1
```

---

# Execution Policies

## Restricted

No scripts allowed.

---

## RemoteSigned

Local scripts allowed.

Downloaded scripts must be signed.

---

## Bypass

Everything runs.

No warnings.

---

# Security Note

Execution Policy is **not** a security boundary.

Attackers can bypass it.

Example:

```powershell
powershell.exe -ExecutionPolicy Bypass
```

---

# PowerShell Logging

SOC analysts often investigate:

**Event ID 4104**

Script Block Logging records executed PowerShell commands.

---

# Summary

- Cmdlets use Verb-Noun format
- Pipeline passes objects
- Script extension = .ps1
- Event ID 4104 records PowerShell execution

---

# 6. Windows Event Logs

Windows records important system activities inside **Event Logs**.

GUI tool:

```
eventvwr.msc
```

Log files use:

```
.evtx
```

---

# Main Log Categories

## Security

Records:

- Login attempts
- Account changes
- Privilege assignments

Most important for security investigations.

---

## System

Records:

- Drivers
- Hardware
- Services
- System events

---

## Application

Records application events.

Examples:

- SQL errors
- Software crashes

---

# Important Event IDs

| Event ID | Description |
|----------|-------------|
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4672 | Administrator privileges assigned |
| 4720 | User account created |
| 1102 | Audit logs cleared |
| 7045 | Service installed |

---

# Logon Types

## Type 2

Interactive logon.

Physical keyboard login.

---

## Type 3

Network logon.

Example:

Shared folders.

---

## Type 10

Remote Desktop (RDP).

---

# Sysmon

Microsoft Sysinternals tool providing advanced logging.

Important Event IDs:

Event ID 1

- Process Creation

---

Event ID 3

- Network Connections

---

Event ID 22

- DNS Queries

---

# Summary

- Event Viewer = eventvwr.msc
- Security log stores authentication events
- Event ID 4624 = Successful login
- Event ID 4625 = Failed login
- Sysmon provides advanced telemetry

---

# Commands Learned

## Windows

```cmd
dir /R

icacls

reg query

eventvwr.msc
```

---

## PowerShell

```powershell
Get-Process

Get-Service

Get-ChildItem

Get-Content

Sort-Object

Select-Object
```

---

# Key Concepts Learned

- Windows File System
- NTFS
- FAT32
- exFAT
- Alternate Data Streams
- Access Control Lists
- User Account Control (UAC)
- Integrity Levels
- Windows Registry
- Registry Hives
- Registry Persistence
- Active Directory
- Domain Controller
- Kerberos
- NTLM
- Organizational Units
- PowerShell Cmdlets
- PowerShell Pipeline
- Execution Policies
- Windows Event Logs
- Sysmon
- Event IDs
- Digital Forensics
- Windows Administration

---

