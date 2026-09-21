# Alert Triage With Elastic — TryHackMe

**Date:** 21 September 2026  
**Platform:** TryHackMe  
**Role:** SOC L1 Analyst  
**Tool:** Elastic / Kibana  
**Room:** Alert Triage With Elastic

------------------------------------------------------------------------

## 1. What I Did in This Room

In this room, I investigated a simulated attack against a company called
**SomeCorp** using **Elastic/Kibana**.

The main goal was not just to answer questions. I had to think like a
SOC analyst:

1.  Start with an alert.
2.  Find the related logs.
3.  Filter the logs using KQL.
4.  Look at the important fields.
5.  Correlate different log sources.
6.  Build a timeline of what the attacker did.
7.  Decide whether the alert is a True Positive.
8.  Collect enough evidence to escalate the incident.

This room was especially useful because I had already done alert triage
with Splunk. The investigation idea is very similar, but the query
language and interface are different.

------------------------------------------------------------------------

# 2. Elastic and Kibana Basics

## What is Elastic?

Elastic is a platform used to collect, search, analyze, and visualize
large amounts of data such as security logs.

For SOC work, Elastic can help me answer questions such as:

- Who logged in?
- From which IP?
- What process was executed?
- What command was executed?
- Was a new account created?
- Was a user added to a privileged group?
- What web requests were made?
- What happened immediately before and after an alert?

## What is Kibana?

**Kibana** is the interface I used to search and investigate the data
stored in Elasticsearch.

I can think of it like this:

``` text
Logs → Elasticsearch → Kibana → SOC Analyst
```

Elasticsearch stores and searches the data, while Kibana gives me the
interface where I can investigate it.

------------------------------------------------------------------------

# 3. KQL — Kibana Query Language

The main thing I used in this room was **KQL (Kibana Query Language)**.

KQL is used to filter events.

For example:

``` text
client.ip:203.0.113.55
```

means:

> Show me events where the `client.ip` field is `203.0.113.55`.

I can combine conditions using operators such as:

``` text
and
or
```

Example:

``` text
_index:weblogs and client.ip:203.0.113.55
```

This means:

> Search the `weblogs` index and only show events from that IP.

Another example:

``` text
winlog.event_id:4624 and host.name:winserv2019.some.corp
```

This means:

> Show Windows logon events on the specified host.

------------------------------------------------------------------------

# 4. Important Kibana Investigation Skills

## Data View

The room provides a data view called:

``` text
Alert Triage With Elastic
```

The data view tells Kibana which data sources/indices I am allowed to
search.

## Time Range

For the initial investigation, I selected:

``` text
Entire data range
```

This is important because if I accidentally select only the last 15
minutes, I may completely miss the attack.

Later, I can narrow the time range to the exact alert window.

## Adding Fields as Columns

Kibana lets me click the `+` beside a field and add it as a table
column.

This is extremely useful because instead of opening every event
individually, I can create a readable table containing fields such as:

``` text
_time
client.ip
user.agent
http.request.method
url.path
http.response.status_code
```

For SOC investigations, this makes patterns much easier to spot.

## Sorting Events

I frequently used **Old-New** sorting.

That means the oldest events appear first.

This is useful when reconstructing an attack because I want to
understand:

``` text
First event
   ↓
Next event
   ↓
Next event
   ↓
Persistence
   ↓
Privilege changes
   ↓
Post-exploitation
```

------------------------------------------------------------------------

# Task 2 — Scenario Briefing

## Step 1 — Access Kibana

I started the TryHackMe machine and waited for Elastic/Kibana to become
available.

Then I opened the room’s provided Kibana URL.

I selected:

``` text
Data view: Alert Triage With Elastic
Time range: Entire data range
```

The room’s data view contains multiple indices.

For the web investigation, I started with:

``` text
_index:weblogs
```

## What does `_index` mean?

The `_index` field tells me which Elasticsearch index contains the
event.

So:

``` text
_index:weblogs
```

means:

> Only show events stored in the `weblogs` index.

This was useful because I wanted to isolate the IIS web server logs
first.

## Answers

### Total logs available

``` text
1467
```

### `client.ip` value in the `weblogs` index

``` text
203.0.113.55
```

This IP becomes very important because I later followed it from the web
logs into the Windows logs.

------------------------------------------------------------------------

# Task 3 — Investigating Web Attacks

This was my first real alert investigation.

The first alert showed multiple POST requests to:

``` text
proxyLogon.ecp
```

from:

``` text
203.0.113.55
```

The room identifies this activity as related to **ProxyLogon**
exploitation.

The important SOC lesson here is that I did not need to know every
detail of the vulnerability before investigating. I could start with the
observable evidence:

``` text
Source IP
HTTP method
URL path
User-Agent
HTTP status
Timestamp
```

## Step 1 — Find POST requests

I used:

``` text
_index:weblogs and client.ip:203.0.113.55 and http.request.method:POST
```

This filters the logs down to POST requests from the suspicious IP.

Then I added these fields as columns:

``` text
client.ip
user.agent
http.request.method
url.path
http.response.status_code
```

This made the activity easier to read.

## Why the User-Agent mattered

The requests used:

``` text
python-requests/2.25.1
```

This is a strong clue that the traffic was generated by a Python HTTP
client rather than a normal browser.

The room also explains that the request pattern was related to automated
ProxyLogon exploitation.

## Answer — POST requests to proxyLogon.ecp

``` text
3
```

## Answer — User-Agent

``` text
python-requests/2.25.1
```

------------------------------------------------------------------------

# Investigating the Web Shell

The next alert happened only a few minutes later.

The suspicious URL was:

``` text
errorEE.aspx
```

with a query parameter:

``` text
cmd=
```

A URL such as:

``` text
errorEE.aspx?cmd=hostname
```

is suspicious because it can indicate that commands are being passed
directly to a server-side web shell.

## Query I used

``` text
_index:weblogs and client.ip:203.0.113.55 and http.request.method:GET and errorEE.aspx
```

Then I sorted the results:

``` text
Old-New
```

This allowed me to see the commands in chronological order.

## Why `cmd=` is important

A normal web page usually does not allow a user to pass arbitrary
operating-system commands through a URL parameter.

If I see something like:

``` text
?cmd=whoami
?cmd=hostname
?cmd=ipconfig
```

I should investigate it as possible command execution.

## Number of logs containing `cmd=`

``` text
20
```

## Command executed at the specified timestamp

At:

``` text
Jul 20, 2025 @ 04:45:50.000
```

the command was:

``` text
hostname
```

This was important evidence because it showed that the web shell was
actually being used to execute commands.

## Triage conclusion for Task 3

At this point, the two web alerts were no longer just suspicious-looking
events.

I had evidence of:

``` text
203.0.113.55
      ↓
POST requests to proxyLogon.ecp
      ↓
Possible exploitation
      ↓
GET requests to errorEE.aspx
      ↓
cmd= parameter
      ↓
hostname command executed
```

The room therefore treats both alerts as **True Positives** and says
they should be escalated.

------------------------------------------------------------------------

# Task 4 — Uncovering Account Activity

Now I moved from web logs to **Windows host logs**.

This is an important SOC technique:

> Do not investigate each alert in isolation. Pivot using indicators
> such as IP addresses, usernames, timestamps, and hostnames.

The same suspicious IP from the web investigation appeared again:

``` text
203.0.113.55
```

This time it was associated with an Administrator logon.

------------------------------------------------------------------------

## Windows Event ID 4624

The room uses:

``` text
winlog.event_id:4624
```

Event ID **4624** represents a successful Windows logon.

The investigation query was:

``` text
@timestamp >= "2025-07-20T05:11:22" and winlog.event_id:4624 and host.name:winserv2019.some.corp and winlog.event_data.TargetUserName:Administrator
```

I added these fields to the table:

``` text
winlog.event_id
host.name
winlog.event_data.TargetUserName
winlog.logon.type
winlog.event_data.IpAddress
```

### Why these fields matter

`winlog.event_id`

Tells me what Windows event occurred.

`host.name`

Tells me which machine was affected.

`TargetUserName`

Tells me which account logged in.

`winlog.logon.type`

Tells me how the account accessed the machine.

`IpAddress`

Tells me where the login came from.

The important correlation was:

``` text
Administrator
    ↓
winserv2019.some.corp
    ↓
203.0.113.55
```

That was the same IP involved in the earlier web attack.

------------------------------------------------------------------------

# Sysmon Event ID 1 — Process Creation

The room then pivots to Sysmon.

Query:

``` text
@timestamp >= "2025-07-20T05:11:22" and winlog.event_id:1 and user.name:Administrator
```

Sysmon Event ID **1** represents **Process Creation**.

I added:

``` text
user.name
process.parent.name
process.command_line
```

These fields help me understand the process tree.

For example:

``` text
Administrator
      ↓
Parent Process
      ↓
Child Process
      ↓
Command
```

This is much more useful than simply knowing that a login occurred.

## Answers

### Administrator 4624 `winlog.record_id`

``` text
17166
```

### Sysmon Event ID 1 `process.pid`

At:

``` text
Jul 20, 2025 @ 05:11:27.996
```

PID:

``` text
964
```

------------------------------------------------------------------------

# Investigating the New User Account

The next alert showed that a new account was created.

I used:

``` text
@timestamp >= "2025-07-20T05:13:10.000" and winlog.channel:Security and winlog.task:User Account Management
```

The useful fields were:

``` text
winlog.event_id
winlog.task
message
```

I sorted the results **Old-New** so I could reconstruct the sequence.

## Event ID 4720

The new account creation event was:

``` text
4720
```

Windows Event ID 4720 represents a new user account being created.

The newly created account was:

``` text
svc_backup
```

This was an important persistence clue.

The attacker had moved from:

``` text
Web exploitation
      ↓
Administrator access
      ↓
New account creation
```

------------------------------------------------------------------------

# Task 5 — Exposing Command Execution

The next alert showed suspicious command-line activity involving:

``` text
C:\Windows\system32\cmd.exe
```

The room recommends starting with:

``` text
@timestamp >= "2025-07-20T05:13:15" and process.parent.name:cmd.exe and user.name:Administrator
```

I added:

``` text
process.command_line
process.name
process.parent.name
```

This lets me see what commands were executed by processes launched from
`cmd.exe`.

------------------------------------------------------------------------

# Correlating Security Event ID 4732

The next query was:

``` text
@timestamp >= "2025-07-20T05:13:15" and (winlog.event_id:4732 or process.parent.name:cmd.exe)
```

This is an important example of **cross-source correlation**.

I am asking Elastic to show either:

``` text
winlog.event_id:4732
```

OR

``` text
process.parent.name:cmd.exe
```

That lets me place the process activity and security-group activity next
to each other.

## What is Event ID 4732?

Windows Security Event ID **4732** represents a member being added to a
security-enabled local group.

This is important because attackers may add a newly created account to a
privileged group.

------------------------------------------------------------------------

# PowerShell Investigation

The attacker did not stop after using CMD.

The room tells me to investigate PowerShell Script Block Logging using:

``` text
@timestamp >= "2025-07-20T05:13:15" and event.module:powershell and event.code:4104
```

Then I added:

``` text
powershell.file.script_block_text
```

as a column.

## Event Code 4104

PowerShell event **4104** is associated with Script Block Logging.

The useful part is that the script block text can show the actual
PowerShell commands that were executed.

The first commands I saw included:

``` text
whoami
whoami /priv
```

These are classic discovery commands.

### Why `whoami`?

It tells the attacker:

> Which account am I currently running as?

### Why `whoami /priv`?

It shows the privileges available to the current account.

This helps an attacker understand what they can do next.

------------------------------------------------------------------------

# No Alert Created — Rar.exe

One of the most important lessons in this room was that **not every
malicious action generates an alert**.

The room points out that `Rar.exe` was used by the newly created
account.

Rar is legitimate software, so the SOC may not automatically flag it.

This is an example of why context matters.

A legitimate executable can still be used for malicious purposes.

For example:

``` text
Legitimate tool
      ↓
Used by suspicious account
      ↓
Used after compromise
      ↓
Creates an archive
      ↓
Potential data staging
```

The investigation query was:

``` text
process.name: "Rar.exe"
```

I then investigated the surrounding events to determine who launched it
and what archive was created.

The archive was:

``` text
finance_it_archive.rar
```

This is an important example of **data staging**.

An attacker may collect files and compress them into an archive before
attempting to move them elsewhere.

------------------------------------------------------------------------

# Answers

| Question                           | Answer                              |
|------------------------------------|-------------------------------------|
| Total logs in entire time range    | `1467`                              |
| `client.ip` in `weblogs`           | `203.0.113.55`                      |
| POST requests to `proxyLogon.ecp`  | `3`                                 |
| User-Agent for POST requests       | `python-requests/2.25.1`            |
| Logs containing `cmd=`             | `20`                                |
| Command at 04:45:50                | `hostname`                          |
| Administrator 4624 record ID       | `17166`                             |
| Sysmon 1 PID at 05:11:27.996       | `964`                               |
| New-account event ID               | `4720`                              |
| New account                        | `svc_backup`                        |
| 4732 record ID                     | `17254`                             |
| PowerShell command at 05:16:14.628 | `net group "Domain Admins" /domain` |
| Archive created with Rar.exe       | `finance_it_archive.rar`            |

------------------------------------------------------------------------

# Important Answer Note — Remote Desktop Users Question

There is one discrepancy worth recording instead of silently changing
it.

The question in the room asks:

> What command does the attacker use to add the new account to the
> **Remote Desktop Users** group?

The answer provided in the supplied notes was:

``` text
net localgroup Administrators svc_backup /add
```

However, the Medium walkthroughs I checked give the command as:

``` text
net localgroup "Remote Desktop Users" svc_backup /add
```

The latter matches the wording of the question. I should verify this
directly in my own TryHackMe Kibana results before treating the
discrepancy as resolved.

I am deliberately recording both values here so I do not accidentally
lose the discrepancy when revisiting the room.

------------------------------------------------------------------------

# Attack Timeline I Reconstructed

This was the most important part of the room for me.

I can reconstruct the attack like this:

``` text
1. External attacker
       |
       | 203.0.113.55
       v
2. Web server
       |
       | POST requests
       | proxyLogon.ecp
       v
3. ProxyLogon exploitation
       |
       v
4. errorEE.aspx web shell
       |
       | cmd=hostname and other commands
       v
5. Administrator access
       |
       | Windows 4624
       | Source IP = 203.0.113.55
       v
6. Process creation
       |
       | Sysmon Event ID 1
       v
7. New account created
       |
       | Event ID 4720
       | svc_backup
       v
8. Group modification
       |
       | Event ID 4732
       v
9. PowerShell discovery
       |
       | whoami
       | whoami /priv
       v
10. Further command execution
       |
       v
11. Rar.exe
       |
       v
12. finance_it_archive.rar
```

This shows why correlation is so important.

If I looked only at one log source, I might see something that looks
harmless.

But when I connect the events together, the story becomes much clearer.

------------------------------------------------------------------------

# Concepts I Learned

## 1. Alert Triage

Alert triage means quickly investigating an alert to determine what
happened and whether it requires escalation.

My basic process is:

``` text
Alert
 ↓
Scope
 ↓
Search logs
 ↓
Find evidence
 ↓
Correlate
 ↓
Determine True/False Positive
 ↓
Escalate if necessary
```

------------------------------------------------------------------------

## 2. True Positive

A True Positive means the alert correctly detected suspicious or
malicious activity.

In this room, the web alerts became strong True Positive cases because
the logs showed actual command execution through the web shell.

------------------------------------------------------------------------

## 3. Initial Access

The attacker first gained access through web application exploitation
involving ProxyLogon.

Conceptually:

``` text
External attacker
      ↓
Web application
      ↓
Vulnerability exploitation
      ↓
Initial foothold
```

------------------------------------------------------------------------

## 4. Web Shell

A web shell is malicious server-side code that allows an attacker to
interact with the underlying system through web requests.

The important indicator in this room was:

``` text
errorEE.aspx?cmd=...
```

The `cmd=` parameter was a strong clue that commands were being passed
through the web application.

------------------------------------------------------------------------

## 5. Process Tree Analysis

Process tree analysis helps me understand which process launched another
process.

For example:

``` text
explorer.exe
     ↓
cmd.exe
     ↓
net.exe
```

If `cmd.exe` appears during suspicious activity, I should inspect its
child processes and command lines.

Useful Elastic fields include:

``` text
process.name
process.parent.name
process.command_line
process.pid
```

------------------------------------------------------------------------

## 6. Account Creation

Windows Event ID:

``` text
4720
```

This tells me a new user account was created.

In this room:

``` text
svc_backup
```

was created after the Administrator compromise.

A service-looking name does not automatically make an account
legitimate. I need to investigate its timing, creator, group membership,
and activity.

------------------------------------------------------------------------

## 7. Security Group Modification

Windows Event ID:

``` text
4732
```

This is important because attackers may add accounts to privileged
groups.

That can turn a newly created low-privilege account into a persistence
or privilege mechanism.

------------------------------------------------------------------------

## 8. PowerShell Discovery

The commands:

``` text
whoami
whoami /priv
```

help an attacker understand their current identity and privileges.

These commands are not inherently malicious. The important part is the
**context**:

``` text
Compromised server
      +
New account
      +
Suspicious process tree
      +
Privilege/group changes
      +
Discovery commands
```

Together, the activity becomes much more suspicious.

------------------------------------------------------------------------

## 9. Living-off-the-Land / Legitimate Tools

One thing I learned from the `Rar.exe` section is that attackers do not
always need custom malware.

They can abuse legitimate programs already available on the machine.

This is why:

``` text
process.name: "Rar.exe"
```

by itself does not automatically mean malware.

I have to ask:

- Who launched it?
- When was it launched?
- What was its parent process?
- What account executed it?
- What files did it create?
- What happened before and after it?

------------------------------------------------------------------------

## 10. Data Staging

The archive:

``` text
finance_it_archive.rar
```

is an example of possible data staging.

An attacker may gather files into one archive before attempting
exfiltration.

The archive itself does not prove exfiltration happened, but it is an
important artifact that should be investigated in context.

------------------------------------------------------------------------

# My Elastic Investigation Cheat Sheet

## Search an index

``` text
_index:weblogs
```

## Search an IP

``` text
client.ip:203.0.113.55
```

## Combine conditions

``` text
_index:weblogs and client.ip:203.0.113.55
```

## Search POST requests

``` text
http.request.method:POST
```

## Search GET requests

``` text
http.request.method:GET
```

## Search a specific URL/file

``` text
errorEE.aspx
```

## Search Windows logon events

``` text
winlog.event_id:4624
```

## Search process creation

``` text
winlog.event_id:1
```

## Search account creation

``` text
winlog.event_id:4720
```

## Search group membership changes

``` text
winlog.event_id:4732
```

## Search PowerShell Script Block Logging

``` text
event.module:powershell and event.code:4104
```

## Search a process

``` text
process.name:"Rar.exe"
```

## Search a parent process

``` text
process.parent.name:cmd.exe
```

## Search by user

``` text
user.name:Administrator
```

## Search after a timestamp

``` text
@timestamp >= "2025-07-20T05:13:15"
```

## Combine OR conditions

``` text
winlog.event_id:4732 or process.parent.name:cmd.exe
```

------------------------------------------------------------------------

# How I Should Approach Similar Elastic Alerts

When I get an alert in a real SOC environment, I can use this checklist:

### 1. Read the alert carefully

Extract:

``` text
Time
Host
User
Source IP
Destination
Process
Alert type
```

### 2. Search the exact indicator

For example:

``` text
client.ip:203.0.113.55
```

### 3. Narrow by time

Do not search the entire environment forever.

Use the alert timestamp to create a useful investigation window.

### 4. Look at the surrounding events

The event immediately before or after an alert can explain what
happened.

### 5. Pivot between log sources

For example:

``` text
Web logs
   ↓
Windows Security
   ↓
Sysmon
   ↓
PowerShell
```

### 6. Build the process tree

Ask:

``` text
Who launched this?
What did it launch?
What command was executed?
Which account ran it?
```

### 7. Check persistence

Look for:

``` text
New accounts
Group changes
Scheduled tasks
Services
Registry changes
Startup locations
SSH keys
```

### 8. Look for post-exploitation

Examples:

``` text
whoami
whoami /priv
net user
net localgroup
PowerShell
Archive creation
Credential access
Data staging
```

### 9. Correlate everything

One suspicious event may be harmless.

Ten connected events telling the same story are much stronger evidence.

### 10. Document and escalate

If the evidence supports malicious activity, preserve the important
indicators and escalate according to the SOC process.

------------------------------------------------------------------------

# Final Takeaway

The biggest lesson I got from this room is that **alert triage is not
just about answering what one alert says**.

I have to connect the dots.

In this investigation, the same IP appeared across multiple stages:

``` text
203.0.113.55
```

First it appeared in web activity involving ProxyLogon.

Then I found a web shell and command execution.

After that, the same activity connected to an Administrator login.

Then a new account appeared:

``` text
svc_backup
```

Then I saw group modification, PowerShell discovery, and finally archive
creation using `Rar.exe`.

The complete picture was only visible after correlating multiple
sources:

``` text
IIS/Web Logs
      +
Windows Security Logs
      +
Sysmon
      +
PowerShell Logs
      +
Process Information
      ↓
Attack Timeline
```

This is exactly the type of thinking I need as a SOC L1 analyst: **start
from the alert, investigate the evidence, correlate the logs, understand
the timeline, and escalate with evidence.**

------------------------------------------------------------------------

# Sources / Walkthrough References

I used the TryHackMe room material as the primary source for the
commands and investigation flow. I also checked multiple walkthroughs to
cross-check the room answers and investigation approach.

- TryHackMe — Alert Triage With Elastic:
  https://tryhackme.com/room/alerttriagewithelastic
- Medium — Lintu Oommen walkthrough:
  https://medium.com/%40oomensusan/alert-triage-with-elastic-tryhackme-walkthrough-1ce82775c91d
- Medium — Darshan walkthrough:
  https://medium.com/%40darshan331740_89257/alert-triage-with-elastic-tryhackme-write-up-ec46a99af738
- Medium — Axoloth / T3CH walkthrough:
  https://medium.com/h7w/tryhackme-alert-triage-with-elastic-writeup-761820485779
- Medium — AbbasMurshid walkthrough:
  https://medium.com/%40abbasmurshidm/tryhackme-alert-triage-with-elastic-6777141f16eb
- Medium — Shyroot walkthrough:
  https://medium.com/%40shyroot1/alert-triage-with-elastic-walkthrough-tryhackme-f8daf3a7b8d3

The Medium walkthroughs confirm the main answer set and the overall
investigation flow. Where my supplied notes and an external walkthrough
differed on the Remote Desktop Users command, I explicitly preserved the
discrepancy rather than silently changing it.

------------------------------------------------------------------------

# Sanitization Note

This README is intended as a learning document and portfolio-style
record.

The lab-specific infrastructure details and temporary environment
identifiers should not be treated as real production indicators. The
investigation logic, KQL queries, Windows event IDs, process-analysis
techniques, and attack-chain reasoning are the important reusable parts.
