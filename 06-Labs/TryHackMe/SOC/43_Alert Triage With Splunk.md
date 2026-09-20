# Alert Triage With Splunk --- TryHackMe

**Date:** 20 September 2026\
**Room:** Alert Triage With Splunk\
**Focus:** SOC alert triage, Linux brute force, privilege escalation,
persistence, Windows scheduled tasks, process trees, discovery, web
brute force, web shells, and Splunk investigation.

------------------------------------------------------------------------

# 1. What I Learned

This room felt much more like a real SOC L1 investigation than simply
answering questions. I worked through three alerts:

``` text
1. Linux Initial Access Alert
2. Windows Persistence Alert
3. Web Shell Alert
```

My investigation mindset was:

``` text
Alert
 ↓
Understand context
 ↓
Search the correct Splunk index
 ↓
Filter events
 ↓
Extract useful fields
 ↓
Pivot using evidence
 ↓
Build a timeline
 ↓
Classify the activity
 ↓
Escalate if required
```

The official TryHackMe room describes the same main goals: investigate
Linux brute force, Windows persistence, web-shell activity, and use
Splunk to triage all three scenarios.

------------------------------------------------------------------------

# 2. What Is Alert Triage?

Alert triage means taking a security alert and determining what actually
happened.

An alert does **not** automatically mean that an attack succeeded. I
need evidence.

``` text
Alert
 ↓
Validate
 ↓
Investigate
 ↓
Classify
 ↓
Escalate
```

## True Positive

A True Positive means the alert correctly identified suspicious or
malicious activity.

Example:

``` text
500 failed SSH attempts
        ↓
Successful login
        ↓
Privilege escalation
        ↓
Persistence
```

## False Positive

A False Positive is an alert triggered by activity that turns out to be
legitimate or non-malicious.

The important SOC lesson is that I should make the decision from
evidence and context, not just the alert title.

------------------------------------------------------------------------

# 3. Splunk Concepts I Used

## `index`

``` spl
index="linux-alert"
```

An index is a logical place where Splunk stores/searches a set of
events.

## `sourcetype`

``` spl
sourcetype="linux_secure"
```

This helps me restrict the search to a particular type of log data.

## Pipe `|`

``` spl
index=task
| stats count
| sort -count
```

The pipe sends the output of one command into the next command.

Think:

``` text
Search → Process → Sort
```

## `search`

``` spl
| search "Failed password"
```

Filters events after the initial search.

## `stats`

``` spl
| stats count by username
```

Calculates statistics and groups results.

## `count`

``` spl
| stats count
```

Counts events.

## `values()`

``` spl
values(src_ip)
```

Returns the distinct values found in a field.

## `by`

``` spl
| stats count by username
```

Groups the calculation by a field.

## `sort`

``` spl
| sort + _time
```

Sorts ascending.

``` spl
| sort - _time
```

Sorts descending.

## `table`

``` spl
| table _time clientip useragent uri_path method status
```

Displays only the fields I want to inspect.

## `rex`

``` spl
| rex field=_raw "..."
```

Extracts structured fields from raw text using a regular expression.

## `eval`

``` spl
| eval process="sshd"
```

Creates or calculates a field.

## `earliest()` and `latest()`

``` spl
earliest(_time)
latest(_time)
```

Find the first and last timestamps in a result set. This is useful for
calculating attack duration.

## `!=`

``` spl
useragent!="Mozilla/5.0 (Hydra)"
```

Excludes matching events.

## `AND` / `OR`

``` spl
condition1 AND condition2
```

Both conditions must match.

``` spl
condition1 OR condition2
```

Either condition can match.

------------------------------------------------------------------------

# 4. Task 2 --- Initial Access Alert

## Alert Details

``` text
Alert: Brute Force Activity Detection
Time: 17/09/2025 9:00:21 AM
Target Host: tryhackme-2404
Source IP: 10.10.242.248
Index: linux-alert
```

The source IP is an internal/local address. That makes the alert
interesting because the source could already be inside the organisation,
for example through a compromised host or VPN access.

The time itself is normal working time, so I cannot decide that it is
malicious based only on the timestamp.

I need the logs.

------------------------------------------------------------------------

## 4.1 First Search --- Authentication Activity

``` spl
index="linux-alert" sourcetype="linux_secure" 10.10.242.248
| search "Accepted password for" OR "Failed password for" OR "Invalid user"
| sort + _time
```

### Why I search these three things

``` text
Accepted password
→ Successful login

Failed password
→ Failed authentication

Invalid user
→ Possible username enumeration
```

An attacker may first test usernames and then concentrate the brute
force on a valid account.

``` text
Invalid user
Invalid user
Invalid user
      ↓
Find valid username
      ↓
Brute force valid account
```

------------------------------------------------------------------------

# 5. Counting Attempts Per Username

The room uses `rex` to turn raw SSH log lines into useful fields:

``` spl
index="linux-alert" sourcetype="linux_secure" 10.10.242.248
| rex field=_raw "^\d{4}-\d{2}-\d{2}T[^\s]+\s+(?<log_hostname>\S+)"
| rex field=_raw "sshd\[\d+\]:\s*(?<action>Failed|Accepted)\s+\S+\s+for(?: invalid user)? (?<username>\S+) from (?<src_ip>\d{1,3}(?:\.\d{1,3}){3})"
| eval process="sshd"
| stats count values(src_ip) as src_ip values(log_hostname) as hostname values(process) as process by username
```

## What `rex` is doing

It extracts fields from `_raw`, including:

``` text
action
username
src_ip
log_hostname
```

A raw event such as:

``` text
sshd[1234]: Failed password for john.smith from 10.10.242.248
```

can become:

``` text
action = Failed
username = john.smith
src_ip = 10.10.242.248
```

Then `stats` groups the events by username so I can compare the attack
volume.

The account receiving the large number of failed attempts is:

``` text
john.smith
```

------------------------------------------------------------------------

# 6. Question 1 --- Failed Login Attempts

I can narrow the search directly to the target user:

``` spl
index="linux-alert" sourcetype="linux_secure" "Failed password for john.smith"
| stats count as Failed_Attempts
```

This means:

``` text
Find Linux authentication events
        ↓
Find failed passwords for john.smith
        ↓
Count them
```

The result is:

``` text
500
```

**Answer: `500`**

A Medium walkthrough confirms this answer and uses the same focused
`stats count` approach.

------------------------------------------------------------------------

# 7. Question 2 --- Brute Force Duration

I need the first and last relevant timestamps.

A useful Splunk query is:

``` spl
index="linux-alert" sourcetype="linux_secure" "Failed password for john.smith"
| stats earliest(_time) as start latest(_time) as end
| eval duration_mins=round((end-start)/60,2)
```

### How this works

``` text
earliest(_time)
→ first event

latest(_time)
→ last event

end - start
→ duration in seconds

/ 60
→ minutes
```

The brute-force activity lasted:

``` text
5 minutes
```

**Answer: `5`**

Medium walkthroughs also show the attack beginning around 09:01:50 and
ending around 09:06:35, giving approximately five minutes.

------------------------------------------------------------------------

# 8. Question 3 --- Privilege Escalation

The next question is not just whether the attacker logged in. I need to
know what happened after access.

The room shows the attacker used:

``` text
sudo su root
```

to switch to the root account.

The account they escalated to was:

``` text
root
```

**Answer: `root`**

The attack chain is therefore:

``` text
Brute force
 ↓
Successful SSH login
 ↓
john.smith
 ↓
sudo / su
 ↓
root
```

------------------------------------------------------------------------

# 9. Question 4 --- Persistence Account

After gaining root, I need to ask:

> How did the attacker maintain access?

The attacker created a new Linux user account:

``` text
system-utm
```

**Answer: `system-utm`**

Creating an additional account can provide persistence because the
attacker may be able to authenticate using that account later.

The full Task 2 answer set is independently confirmed by a Medium
write-up:

``` text
500
5
root
system-utm
```

------------------------------------------------------------------------

# 10. Linux Attack Timeline

``` text
10.10.242.248
       ↓
Username enumeration
       ↓
Brute force against john.smith
       ↓
500 failed attempts
       ↓
5-minute attack
       ↓
Successful login
       ↓
Privilege escalation
       ↓
root
       ↓
Create persistence account
       ↓
system-utm
```

This is why the original alert is a **True Positive** and should be
escalated to L2.

As an L1 analyst, I would document the evidence and pass the case
forward rather than trying to perform the entire incident-response
process myself.

------------------------------------------------------------------------

# 11. Task 3 --- Persistence Alert

## Alert Details

``` text
Alert: Potential Task Scheduler Persistence Identified
Time: 30/08/2025 10:06:07 AM
Host: WIN-H015
User: oliver.thompson
Task: AssessmentTaskOne
Index: win-alert
```

Before searching Splunk, I should understand the context.

The room treats `WIN-H015` as a workstation based on the naming
convention and identifies `oliver.thompson` as a System Engineer.

This context matters because the same activity could have a different
meaning depending on the user's role and the type of host.

------------------------------------------------------------------------

# 12. Event ID 4698 --- Scheduled Task Creation

The room uses:

``` spl
index="win-alert" EventCode=4698 AssessmentTaskOne
| table _time EventCode user_name host Task_Name Message
```

Event ID 4698 represents scheduled-task creation.

I then inspect the `Message` field, especially:

``` text
Triggers
Exec
Principals
```

------------------------------------------------------------------------

# 13. Understanding the Scheduled Task

## Triggers

Triggers tell me **when** the task runs.

The task runs every day, which by itself is not necessarily malicious.
The important question is what it does.

## Exec

The task uses:

``` text
certutil
```

to download:

``` text
rv.exe
```

from the suspicious `tryhotme` domain and save it as:

``` text
DataCollector.exe
```

It then launches the file using PowerShell:

``` text
Start-Process
```

## Principals

The task executes under:

``` text
oliver.thompson
```

So the behaviour becomes:

``` text
Scheduled Task
      ↓
certutil
      ↓
Download remote executable
      ↓
DataCollector.exe
      ↓
PowerShell Start-Process
      ↓
Execute payload
```

That is strong evidence of malicious persistence.

------------------------------------------------------------------------

# 14. Why `certutil` Matters

`certutil` is a legitimate Windows utility. This is important because
attackers can abuse legitimate tools already installed on the system.

This is commonly described as **living off the land**.

The lesson is:

``` text
Legitimate tool
      ≠
Automatically legitimate activity
```

I need to examine the context.

Here the context is suspicious because I have:

``` text
Scheduled task
+
External download
+
Executable payload
+
PowerShell execution
+
Persistence
```

------------------------------------------------------------------------

# 15. Question 1 --- ProcessId

The scheduled-task creation event can be correlated with process
information.

The relevant process ID is:

``` text
5816
```

**Answer: `5816`**

A Medium walkthrough shows the same investigation by searching the
scheduled-task event and reviewing the process information.

------------------------------------------------------------------------

# 16. Process ID vs Parent Process ID

This distinction is very important.

### Process ID

A PID identifies a process.

``` text
PID = 4128
```

### Parent Process ID

The parent process ID identifies the process that launched another
process.

Think:

``` text
Parent
  ↓
Child
```

For example:

``` text
cmd.exe
   ↓
powershell.exe
```

The process tree tells me **how the suspicious process started**.

------------------------------------------------------------------------

# 17. Question 2 --- Parent Process

I pivot using the process information.

A Medium walkthrough demonstrates a search like:

``` spl
index="win-alert" ProcessId=4128
```

and then reviews the parent-process information.

The parent process is:

``` text
cmd.exe
```

**Answer: `cmd.exe`**

This gives me:

``` text
cmd.exe
   ↓
Process creating task
   ↓
AssessmentTaskOne
```

------------------------------------------------------------------------

# 18. Question 3 --- Local Group Enumeration

After finding the parent process, I investigate commands it executed.

``` spl
index="win-alert" ParentProcessId=4128
| table _time ParentCommandLine CommandLine
```

I inspect the command-line activity for discovery behaviour.

The attacker enumerated:

``` text
Administrators
```

**Answer: `Administrators`**

This is an example of **discovery**.

The attacker is trying to learn which accounts/groups have
administrative privileges.

------------------------------------------------------------------------

# 19. Question 4 --- Source Workstation

Now I want to know where the threat actor logged in from.

Windows successful logon events are useful here.

The important event is:

``` text
Event ID 4624
```

A search can start with:

``` spl
index="win-alert" EventCode=4624
```

I inspect the relevant successful logon and its workstation/source
information.

The workstation was:

``` text
DEV-QA-SERVER
```

**Answer: `DEV-QA-SERVER`**

------------------------------------------------------------------------

# 20. Windows Attack Timeline

``` text
DEV-QA-SERVER
       ↓
Threat actor logs into WIN-H015
       ↓
Discovery
       ↓
Administrators enumeration
       ↓
cmd.exe
       ↓
Process creates scheduled task
       ↓
ProcessId 5816
       ↓
AssessmentTaskOne
       ↓
certutil download
       ↓
DataCollector.exe
       ↓
PowerShell Start-Process
       ↓
Persistence
```

This is why I should investigate beyond Event ID 4698 itself.

------------------------------------------------------------------------

# 21. Task 4 --- Web Shell Alert

## Alert Details

``` text
Alert: Potential Web Shell Upload Detected
Time: 14/09/2025 09:31:51 AM
Resource: http://web.trywinme.thm
Suspicious IP: 171.251.232.40
Index: web-alert
```

The room first recommends checking the IP in threat-intelligence sources
such as AbuseIPDB. That gives useful reputation context, but I still
need to determine what the IP actually did in the web logs.

------------------------------------------------------------------------

# 22. First Web Search

``` spl
index=web-alert 171.251.232.40
| table _time clientip useragent uri_path method status
| sort + _time
```

Important fields:

``` text
clientip
→ source IP

useragent
→ claimed client/tool

uri_path
→ requested resource

method
→ HTTP method

status
→ HTTP response

_time
→ timeline
```

------------------------------------------------------------------------

# 23. Detecting Hydra

The suspicious IP generated many requests and used:

``` text
Mozilla/5.0 (Hydra)
```

against:

``` text
/wp-login.php
```

Hydra is commonly used for password guessing/brute-force activity.

So the first part of the attack is:

``` text
Hydra
 ↓
WordPress login
 ↓
Brute force
```

------------------------------------------------------------------------

# 24. Filtering Hydra Out

The room then uses:

``` spl
index=web-alert 171.251.232.40 useragent!="Mozilla/5.0 (Hydra)"
| table _time clientip useragent uri_path referer referer_domain method status
```

The important part is:

``` spl
useragent!="Mozilla/5.0 (Hydra)"
```

`!=` means **not equal to**.

I am effectively saying:

> Show me what this IP did apart from the obvious Hydra traffic.

This is a useful SOC technique because it removes known noise and
exposes the next stage of the attack.

------------------------------------------------------------------------

# 25. Finding the Web Shell

After filtering Hydra, the interesting event is a POST request to:

``` text
admin-ajax.php
```

with a referer containing:

``` text
theme-editor.php?file=b374k.php
```

That is suspicious because the WordPress theme editor is being
associated with an arbitrary PHP file.

The room identifies:

``` text
b374k.php
```

as the web shell.

A Medium walkthrough confirms the same pivot: filtering out Hydra
reveals the `admin-ajax.php` request and the
`theme-editor.php?file=b374k.php` referer.

------------------------------------------------------------------------

# 26. What Is a Web Shell?

A web shell is malicious server-side code that gives an attacker a way
to interact with a compromised web server.

Simple idea:

``` text
Normal PHP
 ↓
Website functionality

Web shell
 ↓
Attacker-controlled server interaction
```

In this task:

``` text
b374k.php
```

is the web shell.

The room also recommends researching the name externally, which provides
additional confirmation that it is a known web-shell family/tool.

------------------------------------------------------------------------

# 27. Searching Directly for b374k.php

Once I have the filename, I pivot:

``` spl
index=web-alert 171.251.232.40 b374k.php
| table _time clientip useragent uri_path referer referer_domain method status
| sort + _time
```

This gives me the events involving the web shell.

The investigation becomes:

``` text
Suspicious IP
 ↓
Interesting referer
 ↓
b374k.php
 ↓
Search all activity involving b374k.php
```

------------------------------------------------------------------------

# 28. Question 1 --- When Did Hydra Brute Force Begin?

I start with the chronological IP search:

``` spl
index=web-alert 171.251.232.40
| table _time clientip useragent uri_path method status
| sort + _time
```

Then I identify the earliest Hydra activity against the WordPress login
page.

The start time is:

``` text
2025-09-14 21:20:27
```

**Answer: `2025-09-14 21:20:27`**

This timestamp is confirmed by the Medium walkthrough.

------------------------------------------------------------------------

# 29. Question 2 --- User-Agent Used With the Web Shell

Now I pivot specifically to `b374k.php`:

``` spl
index=web-alert 171.251.232.40 b374k.php
| table _time clientip useragent uri_path referer referer_domain method status
| sort + _time
```

I inspect the `useragent` field.

The attacker used:

``` text
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
```

**Answer:**

``` text
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
```

This is interesting because the attacker changed from an obvious Hydra
User-Agent to a browser-like Chrome User-Agent for web-shell
interaction.

User-Agent values can be spoofed, so I treat this as evidence rather
than absolute proof of the actual browser.

------------------------------------------------------------------------

# 30. Question 3 --- Number of Web-Shell Requests

I only want POST requests involving the web shell:

``` spl
index=web-alert 171.251.232.40 b374k.php method=POST
| stats count
```

The result is:

``` text
4
```

**Answer: `4`**

The room describes these as four successful POST requests through the
web shell.

------------------------------------------------------------------------

# 31. Web Attack Timeline

``` text
171.251.232.40
        ↓
Hydra
        ↓
/wp-login.php
        ↓
Brute-force activity
        ↓
WordPress access
        ↓
theme-editor.php?file=b374k.php
        ↓
b374k.php web shell
        ↓
Chrome 138 User-Agent
        ↓
4 POST requests
        ↓
Web-shell interaction
```

This is much more useful than simply saying "web shell detected".

------------------------------------------------------------------------

# 32. Key SOC Concepts

## Initial Access

How the attacker first enters an environment.

Examples here:

``` text
SSH brute force
Web application compromise
```

## Brute Force

Repeated credential attempts intended to discover a valid password.

``` text
Failed
Failed
Failed
...
Successful
```

## Username Enumeration

Trying usernames to discover which accounts exist.

``` text
Invalid user
Invalid user
Valid user
```

## Privilege Escalation

Moving from a lower-privileged account to a more powerful account.

``` text
john.smith → root
```

## Persistence

Maintaining access after initial compromise.

Examples from this room:

``` text
Linux → system-utm account
Windows → Scheduled Task
```

## Discovery

Learning about the environment.

Example:

``` text
Administrators group enumeration
```

## Process Tree

Shows parent-child relationships:

``` text
cmd.exe
   ↓
powershell.exe
   ↓
malicious.exe
```

This helps explain how a process started.

## Living Off the Land

Using legitimate tools already present on the system for malicious
purposes.

Example:

``` text
certutil
PowerShell
```

## Web Shell

Malicious server-side code that gives an attacker remote interaction
with a web server.

Example:

``` text
b374k.php
```

------------------------------------------------------------------------

# 33. My Reusable Alert-Triage Workflow

## Step 1 --- Read the alert

Extract:

``` text
What happened?
When?
Where?
Who?
Source?
```

## Step 2 --- Establish context

Ask:

``` text
Workstation or server?
Is the user expected to do this?
Internal or external IP?
Normal working hours?
```

## Step 3 --- Search the correct index

``` spl
index=...
```

## Step 4 --- Use the alert's IOC

``` spl
index=... suspicious_ip
```

## Step 5 --- Extract useful fields

``` spl
| rex ...
```

## Step 6 --- Aggregate

``` spl
| stats count by username
```

## Step 7 --- Build a timeline

``` spl
| sort + _time
```

or:

``` spl
earliest(_time)
latest(_time)
```

## Step 8 --- Pivot

``` text
IP
 ↓
User
 ↓
Process
 ↓
Hash
 ↓
Command
 ↓
Persistence
```

## Step 9 --- Classify

``` text
True Positive
False Positive
Needs escalation
```

## Step 10 --- Escalate

For confirmed malicious activity:

``` text
L1
 ↓
L2
 ↓
Incident Response
```

------------------------------------------------------------------------

# 34. Final Answers

## Task 2 --- Initial Access Alert

  Question                                 Answer
  ---------------------------------------- ----------------
  Failed login attempts for `john.smith`   **500**
  Brute-force duration                     **5 minutes**
  Account escalated to                     **root**
  Persistence account                      **system-utm**

## Task 3 --- Persistence Alert

  Question                 Answer
  ------------------------ --------------------
  ProcessId                **5816**
  Parent process           **cmd.exe**
  Local group enumerated   **Administrators**
  Source workstation       **DEV-QA-SERVER**

## Task 4 --- Web Shell Alert

  -----------------------------------------------------------------------
  Question                            Answer
  ----------------------------------- -----------------------------------
  Hydra brute-force start             **2025-09-14 21:20:27**

  Web-shell User-Agent                **Mozilla/5.0 (Windows NT 10.0;
                                      Win64; x64) AppleWebKit/537.36
                                      (KHTML, like Gecko)
                                      Chrome/138.0.0.0 Safari/537.36**

  Web-shell requests                  **4**
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 35. Quick Revision

``` text
ALERT TRIAGE
    ↓
Read Alert
    ↓
Understand Context
    ↓
Search Splunk
    ↓
Filter
    ↓
Extract Fields
    ↓
Pivot
    ↓
Correlate
    ↓
Build Timeline
    ↓
Classify
    ↓
Escalate
```

### Linux

``` text
500 failed logins
        ↓
john.smith
        ↓
5 minutes
        ↓
Successful login
        ↓
root
        ↓
system-utm
```

### Windows

``` text
DEV-QA-SERVER
        ↓
WIN-H015
        ↓
Administrators enumeration
        ↓
cmd.exe
        ↓
ProcessId 5816
        ↓
AssessmentTaskOne
        ↓
certutil download
        ↓
PowerShell
        ↓
Persistence
```

### Web

``` text
171.251.232.40
        ↓
Hydra
        ↓
wp-login.php
        ↓
Brute force
        ↓
theme-editor.php
        ↓
b374k.php
        ↓
Chrome User-Agent
        ↓
4 POST requests
```

------------------------------------------------------------------------

# 36. My Main Takeaway

The biggest lesson I took from this room is that **alert triage is not
just finding the answer to the alert**.

I need to keep asking:

``` text
What happened?
Why did it happen?
Who did it?
Where did it come from?
What happened before?
What happened after?
Did the attacker succeed?
Did they escalate privileges?
Did they create persistence?
What evidence should I send to L2?
```

The three scenarios showed me three connected parts of SOC
investigation:

``` text
Initial Access
      ↓
Privilege Escalation
      ↓
Persistence
      ↓
Execution
```

The most useful mindset for me is:

> **Don't just investigate the alert. Investigate the story behind the
> alert.**

------------------------------------------------------------------------

# 37. Sources Used for Cross-Checking

I used the official TryHackMe room plus Medium walkthroughs to
cross-check the practical investigation steps and answers. I kept the
explanations in my own first-person revision style.

### TryHackMe

Official room: https://tryhackme.com/room/alerttriagewithsplunk

### Medium

**Darshan --- Alert Triage With Splunk TryHackMe Write-up**\
https://medium.com/@darshan331740_89257/alert-triage-with-splunk-tryhackme-write-up-3864449197ea

**0xOG --- Alert Triage With Splunk Walkthrough**\
https://medium.com/%400xOG/alert-triage-with-splunk-tryhackme-walkthrough-79d332bfb04f

**Arfrd --- Alert Triage With Splunk**\
https://medium.com/@Arfrd/tryhackme-alert-triage-with-splunk-44bc86aeab9f

**AbbasMurshid --- TryHackMe Alert Triage With Splunk**\
https://medium.com/@abbasmurshidm/tryhackmealert-triage-with-splunk-3e5432aaf60d

**Leyla --- Alert Triage With Splunk Practical SOC Analysis**\
https://medium.com/@leyla310300/tryhackme-alert-triage-with-splunk-practical-soc-analysis-4f4b72bf7c67

**Axoloth / T3CH --- Alert Triage With Splunk**\
https://medium.com/h7w/tryhackme-alert-triage-with-splunk-writeup-192e675debff

------------------------------------------------------------------------

# 38. Sanitisation Note

The IPs, usernames, hostnames and hashes in this README belong to the
TryHackMe training environment and are retained where they are useful
for revision. I should still avoid adding real credentials, API keys,
tokens, or private information if I later adapt these notes to a public
environment.
