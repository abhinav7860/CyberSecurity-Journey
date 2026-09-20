# Log Analysis with SIEM --- TryHackMe

**Date:** 20 September 2026\
**Room:** Log Analysis with SIEM\
**Focus:** SIEM fundamentals, Splunk, Windows logs, Linux logs, web
logs, correlation, pivoting and SOC investigation.

------------------------------------------------------------------------

# 1. What I Learned

This room taught me how a SOC L1 analyst uses a SIEM to analyse logs and
build an incident timeline.

The main workflow I learned is:

``` text
Alert
  ↓
Search the SIEM
  ↓
Find the relevant event
  ↓
Extract useful fields
  ↓
Pivot using an IOC
  ↓
Correlate related events
  ↓
Build a timeline
  ↓
Identify the behaviour
  ↓
Document / Escalate
```

The important lesson is that an alert is only the starting point. I need
to understand what happened before, during and after it.

------------------------------------------------------------------------

# 2. SIEM

SIEM means **Security Information and Event Management**.

A SIEM collects logs from many sources and gives analysts one place to
search them.

``` text
Windows ──┐
Linux ────┤
Firewall ─┤
VPN ──────┤
DNS ──────┤──→ SIEM / Splunk → SOC Analyst
Web ──────┤
IDS/IPS ──┘
```

A SIEM is useful because it provides:

-   centralisation
-   correlation
-   historical searching
-   detection rules
-   alerting
-   dashboards
-   investigation and hunting capabilities

------------------------------------------------------------------------

# 3. Task 2 --- Benefits of SIEM

## 3.1 Centralisation

**Answer: Centralisation**

Centralisation means collecting and storing logs from multiple systems
in one unified location.

Without a SIEM I might need to check:

``` text
Windows Event Viewer
Linux /var/log
Firewall console
VPN console
EDR console
Web server logs
```

With Splunk, I can search many sources from one place.

A Medium walkthrough for this room gives **Centralisation** as the
answer to this question.\
Source:
https://medium.com/@birdv/tryhackme-log-analysis-with-siem-walkthrough-cf5515ab41d7

------------------------------------------------------------------------

## 3.2 Correlation

**Answer: Correlation**

Correlation means linking events from different sources to understand
relationships between them.

For example:

``` text
IDS
 ↓
10.10.10.50 performed a scan

Windows logs
 ↓
User = John

Sysmon
 ↓
Process = nmap.exe
```

Together:

``` text
John
 ↓
Workstation
 ↓
nmap.exe
 ↓
Network scan
```

One log alone gives limited information. Correlation connects the
pieces.

------------------------------------------------------------------------

## 3.3 Historical Events

A SIEM also lets me search previous events.

If I receive:

``` text
Suspicious login
```

I can investigate:

``` text
Were there failed logins before it?
Has the IP appeared before?
What happened after the login?
Was a process started?
Was persistence created?
```

This helps me build an incident timeline.

------------------------------------------------------------------------

# 4. Task 3 --- Log Sources

The main log-source categories in this room are:

``` text
Host-Based
Network-Based
Web-Based
```

Other organisations may also send cloud, identity-provider and
application logs to the SIEM.

------------------------------------------------------------------------

## 4.1 Host-Based Logs

Host-based logs come from individual devices such as:

-   Windows workstations
-   Linux servers
-   application servers
-   database servers
-   DNS servers

They help answer:

``` text
Who logged in?
What process ran?
What file was created?
What account was created?
What service started?
```

The room's answer for a source useful for detecting malicious script
execution is:

``` text
Host-Based
```

------------------------------------------------------------------------

## 4.2 Network-Based Logs

Network logs come from:

-   firewalls
-   routers
-   IDS
-   IPS
-   VPN
-   DNS
-   proxy servers

They help answer:

> Who is communicating with whom?

Examples:

``` text
Source IP
Destination IP
Source Port
Destination Port
Protocol
Action
```

They can help detect:

-   port scanning
-   suspicious external connections
-   unusual ports
-   brute-force attempts
-   C2 communication
-   suspicious DNS activity

------------------------------------------------------------------------

## 4.3 Web-Based Logs

Web logs come from:

-   web servers
-   WAFs
-   API gateways
-   CDNs
-   web applications
-   load balancers

They can reveal:

-   SQL injection
-   brute force
-   scanning
-   web shells
-   DDoS
-   suspicious requests

------------------------------------------------------------------------

## 4.4 Time Pitfalls

Different systems can use different time zones.

For example:

``` text
Server → UTC
SIEM → UTC
My computer → UTC+5:30
```

An event may therefore appear at different clock times without actually
being delayed.

When investigating, I need to know:

``` text
What timezone is this log using?
```

Otherwise I could build the wrong timeline.

------------------------------------------------------------------------

## 4.5 Log Normalisation

Different systems produce different formats:

``` text
Windows → Event/XML format
Linux → plain text
Applications → JSON
Firewall → vendor-specific format
```

**Normalisation** converts different formats into a consistent
structure.

**Answer: Normalisation**

Think of it as:

``` text
Different formats
      ↓
Normalisation
      ↓
Common structure
      ↓
Easier searching and correlation
```

Medium walkthroughs for this room also identify Normalisation and
Host-Based as the relevant Task 3 answers.\
Source:
https://medium.com/@Sle3pyHead/log-analysis-with-siem-walkthrough-notes-tryhackme-60c63f3cf588

------------------------------------------------------------------------

# 5. Task 4 --- Windows Logs

The room focuses on:

``` text
WinEventLogs
Sysmon
```

Sysmon provides detailed visibility into Windows activity.

Important event codes used here:

``` text
EventCode 1 → Process Creation
EventCode 3 → Network Connection
```

------------------------------------------------------------------------

## 5.1 Sysmon EventCode 1 --- Process Creation

The room gives:

``` spl
index=winenv EventCode=1 *powershell* AND *EncodedCommand*
| table _time ComputerName ParentUser ParentImage ParentCommandLine Image CommandLine
```

### Breaking it down

``` spl
index=winenv
```

Searches the `winenv` index.

``` spl
EventCode=1
```

Looks for Sysmon process-creation events.

``` spl
*powershell*
```

Uses `*` as a wildcard to find values containing PowerShell.

``` spl
AND
```

Requires both conditions.

``` spl
| 
```

Passes the results to the next command.

``` spl
table
```

Displays only the fields I selected.

The fields are:

``` text
_time
ComputerName
ParentUser
ParentImage
ParentCommandLine
Image
CommandLine
```

This helps answer:

``` text
What process ran?
Who started it?
What was its parent?
What command line was used?
```

------------------------------------------------------------------------

## 5.2 Why Parent Processes Matter

Suppose I find:

``` text
update_config.js
      ↓
cmd.exe
      ↓
powershell.exe
      ↓
EncodedCommand
```

That is much more informative than simply finding PowerShell.

The parent process helps me understand how the suspicious process
started.

------------------------------------------------------------------------

## 5.3 Sysmon EventCode 3 --- Network Connection

The room gives:

``` spl
index=winenv EventCode=3 ComputerName=WINHOST05
| table _time ComputerName Image SourceIp SourcePort DestinationIp DestinationPort Protocol
```

EventCode 3 helps me identify:

``` text
Process
Source IP
Source Port
Destination IP
Destination Port
Protocol
```

This connects endpoint activity to network activity.

------------------------------------------------------------------------

## 5.4 Windows Security Logs

Security logs can contain:

-   authentication
-   account creation
-   account modification
-   file access
-   registry access
-   process activity
-   audit changes
-   log clearing

The room demonstrates:

``` text
4720 → User created
4722 → User enabled
```

Example:

``` spl
index=winenv EventCode=4720 OR EventCode=4722
| table _time EventCode ComputerName Subject_Account_Name Target_Account_Name New_Account_Account_Name Keywords
```

------------------------------------------------------------------------

## 5.5 Windows System Logs

The room focuses on:

``` text
7045 → Service creation
7036 → Service start/stop
```

Query:

``` spl
index=winenv EventCode=7045 OR EventCode=7036 ComputerName=WINHOST05
| table _time EventCode ComputerName Service_Name Service_Account Service_File_Name Message
```

A suspicious service running a file from a temporary directory under
SYSTEM should be investigated because services can be abused for
persistence or privilege escalation.

------------------------------------------------------------------------

# 6. Task 4 --- Windows Practical Scenario

The alert says:

``` text
Host = WIN-105
Suspicious port = 5678
```

The logs are in:

``` text
task4
```

I start with:

``` spl
index=task4
```

But I can immediately narrow the search using the information from the
alert.

------------------------------------------------------------------------

## Question 1 --- Which IP Address?

Query:

``` spl
index=task4 EventCode=3 DestinationPort=5678
| table _time ComputerName Image SourceIp SourcePort DestinationIp DestinationPort Protocol
```

I look at:

``` text
DestinationIp
```

Result:

``` text
10.10.114.80
```

**Answer:**

``` text
10.10.114.80
```

### Investigation logic

``` text
Known port = 5678
        ↓
Find EventCode 3
        ↓
Find destination port 5678
        ↓
Read DestinationIp
        ↓
10.10.114.80
```

------------------------------------------------------------------------

## Question 2 --- Which Process Initiated the Connection?

In the same event, I look at the `Image` field.

Result:

``` text
SharePoInt.exe
```

**Answer:**

``` text
SharePoInt.exe
```

This name is worth investigating because it resembles a legitimate
Microsoft product name but is oddly written.

------------------------------------------------------------------------

## Question 3 --- MD5 Hash

Now I pivot from the process.

I can search:

``` spl
index=task4 *SharePoInt*
```

or narrow further:

``` spl
index=task4 *SharePoInt* *MD5*
```

The MD5 is:

``` text
770D14FFA142F09730B415506249E7D1
```

**Answer:**

``` text
770D14FFA142F09730B415506249E7D1
```

Medium walkthroughs use the same process-to-hash pivot for this
question.\
Sources:\
https://medium.com/@birdv/tryhackme-log-analysis-with-siem-walkthrough-cf5515ab41d7\
https://medium.com/@Sle3pyHead/log-analysis-with-siem-walkthrough-notes-tryhackme-60c63f3cf588

------------------------------------------------------------------------

## Question 4 --- Scheduled Task

Now I investigate persistence.

A useful search is:

``` spl
index=task4 *SharePoInt* *scheduler*
```

or:

``` spl
index=task4 *scheduled*
```

The task created was:

``` text
Office365 Install
```

**Answer:**

``` text
Office365 Install
```

### Why is this important?

A scheduled task can provide persistence:

``` text
Attacker gets access
       ↓
Creates scheduled task
       ↓
Task executes malicious file
       ↓
Attacker maintains access
```

------------------------------------------------------------------------

# 7. Windows Investigation Timeline

The practical task can now be reconstructed as:

``` text
WIN-105
   ↓
Network connection
   ↓
Destination port 5678
   ↓
Destination IP 10.10.114.80
   ↓
Process SharePoInt.exe
   ↓
MD5 770D14FFA142F09730B415506249E7D1
   ↓
Scheduled task
   ↓
Office365 Install
```

This is SIEM correlation in practice.

------------------------------------------------------------------------

# 8. Task 5 --- Linux Logs

The two important Linux sources are:

``` text
auth.log
syslog
```

------------------------------------------------------------------------

## 8.1 auth.log

`auth.log` contains authentication-related activity.

It can help investigate:

-   SSH logins
-   failed passwords
-   successful logins
-   sudo
-   `su`
-   authentication failures
-   privilege escalation

The room uses:

``` spl
index=linux source="auth.log" *ubuntu* process=sshd
| search "Accepted password" OR "Failed password"
```

### Explanation

``` spl
index=linux
```

Searches Linux events.

``` spl
source="auth.log"
```

Limits the source.

``` spl
*ubuntu*
```

Looks for Ubuntu-related events.

``` spl
process=sshd
```

Focuses on SSH.

``` spl
| search "Accepted password" OR "Failed password"
```

Finds successful or failed password events.

------------------------------------------------------------------------

## 8.2 Failed + Successful Login Pattern

A sequence such as:

``` text
Failed
Failed
Failed
Failed
Successful
```

can indicate a brute-force attempt followed by a successful login.

I should then investigate what happened after the login.

------------------------------------------------------------------------

## 8.3 Privilege Escalation

The room uses:

``` spl
index=linux source="auth.log" *su*
| sort + _time
```

`su` means switching to another user.

If the logs show:

``` text
jack-brown
    ↓
root
```

I know a privilege transition occurred.

However, `auth.log` alone may not tell me exactly how the user obtained
root. I may need additional sources such as auditd or process logs.

------------------------------------------------------------------------

# 9. Linux System Logs

`syslog` contains general system activity.

It can show:

-   services
-   cron
-   background processes
-   system activity

This makes it useful for persistence investigations.

------------------------------------------------------------------------

# 10. Cron and Persistence

The room gives:

``` spl
index=linux sourcetype=syslog ("CRON" OR "cron")
| search ("python" OR "perl" OR "ruby" OR ".sh" OR "bash" OR "nc")
```

The first part:

``` spl
sourcetype=syslog
```

limits the search to syslog-type events.

Then:

``` spl
("CRON" OR "cron")
```

finds cron-related events.

Then:

``` spl
("python" OR "perl" OR "ruby" OR ".sh" OR "bash" OR "nc")
```

looks for suspicious execution patterns.

Cron is important because it can execute commands automatically.

For example:

``` text
Every 5 minutes
      ↓
Run malicious script
      ↓
Persistence
```

------------------------------------------------------------------------

# 11. Task 5 --- Linux Practical Scenario

The alert says:

> Possible persistence through creation of a new remote-SSH user.

The logs are in:

``` text
task5
```

Start with:

``` spl
index=task5
```

Then pivot through authentication and system activity.

------------------------------------------------------------------------

## Question 1 --- Remote-SSH Account Creation Timestamp

Search for account-creation activity:

``` spl
index=task5
| search "Account Created" OR "new user" OR "useradd"
| table _time _raw
```

The timestamp is:

``` text
2025-08-12 09:52:57
```

**Answer:**

``` text
2025-08-12 09:52:57
```

------------------------------------------------------------------------

## Question 2 --- Who Escalated to Root?

Search for privilege-related activity:

``` spl
index=task5 (su OR sudo)
| table _time _raw
```

The user was:

``` text
jack-brown
```

**Answer:**

``` text
jack-brown
```

Timeline:

``` text
jack-brown
    ↓
Privilege escalation
    ↓
root
    ↓
Account creation
```

------------------------------------------------------------------------

## Question 3 --- Source IP

Now pivot using the username:

``` spl
index=task5 source="auth.log" "jack-brown" "Accepted password"
```

The source IP was:

``` text
10.14.94.82
```

**Answer:**

``` text
10.14.94.82
```

------------------------------------------------------------------------

## Question 4 --- Failed Login Attempts

Search the same user's authentication events:

``` spl
index=task5 source="auth.log" "jack-brown"
| search "Failed password" OR "Accepted password"
```

Inspect the timestamps and event details.

The answer is:

``` text
4
```

**Answer:**

``` text
4
```

### Important duplicate-log detail

One Medium walkthrough explains that some SSH entries can be duplicated
or represented as repeated messages. After accounting for the
duplicate/repeated event representation, the correct number of failed
attempts before the successful login is **4**.

Source:
https://medium.com/@joshuabpointer1/log-analysis-with-siem-259e691e6daa

------------------------------------------------------------------------

## Question 5 --- Persistence Port

Search syslog for port information:

``` spl
index=task5 source="syslog" *port*
| table _time _raw
```

The persistence mechanism connects to:

``` text
7654
```

**Answer:**

``` text
7654
```

This answer is also confirmed by multiple Medium walkthroughs.\
Sources:\
https://medium.com/@corlissS/tryhackme-log-analysis-with-siem-thm-1811810fe7eb\
https://medium.com/@abbasmurshidm/tryhackme-log-analysis-with-siem-db98b0c4137a

------------------------------------------------------------------------

# 12. Linux Investigation Timeline

I can reconstruct the attack as:

``` text
10.14.94.82
      ↓
SSH login attempts
      ↓
4 failed attempts
      ↓
Successful login
      ↓
jack-brown
      ↓
Privilege escalation
      ↓
jack-brown → root
      ↓
Persistence
      ↓
Remote-SSH account created
      ↓
2025-08-12 09:52:57
      ↓
Persistence connects to port 7654
```

This is a useful example of using authentication + system logs together.

------------------------------------------------------------------------

# 13. Task 6 --- Web Application Logs

Web logs can contain fields such as:

``` text
clientip
method
uri_path
status
useragent
referer_domain
_time
```

These can reveal:

-   brute force
-   scanning
-   web shells
-   SQL injection
-   DDoS
-   suspicious requests

------------------------------------------------------------------------

# 14. Brute-Force Detection Query

The room gives:

``` spl
index=* method=POST uri_path="/wp-login.php"
| bin _time span=5m
| stats values(referer_domain) as referer_domain values(status) as status values(useragent) as UserAgent values(uri_path) as uri_path count by clientip _time
| where count > 25
| table referer_domain clientip UserAgent uri_path count status
```

This is one of the most important queries in the room.

------------------------------------------------------------------------

## 14.1 `bin`

``` spl
| bin _time span=5m
```

Groups events into 5-minute time buckets.

For example:

``` text
10:00–10:05
10:05–10:10
10:10–10:15
```

This allows me to detect spikes.

------------------------------------------------------------------------

## 14.2 `stats`

``` spl
| stats ...
```

`stats` calculates information from events.

Here:

``` spl
count by clientip _time
```

means:

> Count the requests separately for each IP and each time bucket.

------------------------------------------------------------------------

## 14.3 `values()`

``` spl
values(useragent)
```

Collects the different values seen in the User-Agent field.

This can help identify the software making the requests.

------------------------------------------------------------------------

## 14.4 `as`

``` spl
values(useragent) as UserAgent
```

Renames the output field to `UserAgent`.

------------------------------------------------------------------------

## 14.5 `where`

``` spl
| where count > 25
```

Only keeps groups with more than 25 requests.

So:

``` text
5 requests → ignore
10 requests → ignore
80 requests → investigate
```

------------------------------------------------------------------------

## 14.6 `table`

``` spl
| table referer_domain clientip UserAgent uri_path count status
```

Shows only the fields I need.

------------------------------------------------------------------------

# 15. Web Shell Detection

The room also teaches how to hunt for possible web shells.

A web shell is malicious code placed on a web server that can allow an
attacker to execute commands remotely.

The room searches for script/executable paths and successful responses.

Example:

``` spl
index=*
| search status=200 AND uri_path IN(*.php, *.phtm, *.asp, *.aspx, *.jsp, *.exe) AND (method=POST AND method=GET)
| stats values(status) as status values(useragent) as UserAgent values(method) as method values(uri) as uri values(clientip) as clientip count by referer_domain
| where count > 2
| table referer_domain count method status clientip UserAgent uri
```

The room's example highlights:

``` text
505.php
```

for further investigation.

------------------------------------------------------------------------

# 16. DDoS Detection

The room also demonstrates looking for:

``` text
HTTP 503
```

combined with a very large number of requests in a short period.

Query:

``` spl
index=* status=503
| bin _time span=10m
| stats values(referer_domain) as referer_domain values(status) as status values(useragent) as UserAgent values(uri_path) as uri_path count by clientip _time
| where count > 100000
| table _time referer_domain clientip UserAgent uri_path count status
```

The logic is:

``` text
503 responses
+
Huge request volume
+
Short time window
=
Possible DDoS
```

------------------------------------------------------------------------

# 17. Task 6 --- Practical Web Investigation

The logs are in:

``` text
task6
```

Start with:

``` spl
index=task6
```

------------------------------------------------------------------------

## Question 1 --- Highest Request URI

I count requests by URI:

``` spl
index=task6
| stats count by uri_path
| sort -count
```

### What happens?

``` text
stats count by uri_path
```

counts each URI.

``` text
sort -count
```

sorts from highest to lowest.

The top URI is:

``` text
/wp-login.php
```

**Answer:**

``` text
/wp-login.php
```

Medium walkthroughs use this same count-and-sort method.\
Sources:\
https://medium.com/@abbasmurshidm/tryhackme-log-analysis-with-siem-db98b0c4137a\
https://medium.com/@darshan331740_89257/log-analysis-with-siem-tryhackme-write-up-c77370958973

------------------------------------------------------------------------

## Question 2 --- Source IP

Now I know the targeted URI.

So I pivot:

``` spl
index=task6 uri_path="/wp-login.php"
| stats count by clientip
| sort -count
```

This means:

``` text
Find wp-login.php requests
        ↓
Group by source IP
        ↓
Count
        ↓
Sort highest first
```

The source is:

``` text
10.10.243.134
```

**Answer:**

``` text
10.10.243.134
```

------------------------------------------------------------------------

## Question 3 --- Classification

Now I need to understand the behaviour.

I can use the room's detailed query:

``` spl
index=task6 method=POST uri_path="/wp-login.php"
| bin _time span=5m
| stats values(referer_domain) as referer_domain values(status) as status values(useragent) as UserAgent values(uri_path) as uri_path count by clientip _time
| where count > 25
| table referer_domain clientip UserAgent uri_path count status
```

The important indicators are:

``` text
POST requests
      ↓
/wp-login.php
      ↓
Many requests
      ↓
Same source IP
      ↓
Short time window
```

This activity is classified as:

``` text
Brute Force
```

**Answer:**

``` text
Brute Force
```

Multiple Medium walkthroughs reach the same classification using request
volume, the login endpoint and the User-Agent information.\
Sources:\
https://medium.com/@birdv/tryhackme-log-analysis-with-siem-walkthrough-cf5515ab41d7\
https://medium.com/@lawvye/log-analysis-with-siem-thm-tryhackme-writeup-924263adfddc

------------------------------------------------------------------------

## Question 4 --- Tool Used

Now I pivot from:

``` text
Source IP = 10.10.243.134
```

to the User-Agent.

Query:

``` spl
index=task6 uri_path="/wp-login.php" clientip="10.10.243.134"
| table _time uri_path useragent
```

Or:

``` spl
index=task6 uri_path="/wp-login.php" clientip="10.10.243.134"
| bin span=5m _time
| stats values(useragent) as USER_AGENT count by clientip
```

The User-Agent identifies:

``` text
WPScan
```

**Answer:**

``` text
WPScan
```

WPScan is a WordPress security-testing/scanning tool. In this
investigation, its presence in the request metadata helps identify the
tool involved.

Medium walkthroughs use the User-Agent field to reach the same answer.\
Sources:\
https://medium.com/@abbasmurshidm/tryhackme-log-analysis-with-siem-db98b0c4137a\
https://medium.com/@darshan331740_89257/log-analysis-with-siem-tryhackme-write-up-c77370958973

------------------------------------------------------------------------

# 18. Complete Web Attack Timeline

``` text
Web server activity spike
          ↓
High request volume
          ↓
/wp-login.php
          ↓
Source IP
10.10.243.134
          ↓
Repeated POST requests
          ↓
High request count in a short period
          ↓
Brute-force behaviour
          ↓
User-Agent
WPScan
```

This is the investigation chain I want to remember.

------------------------------------------------------------------------

# 19. Splunk Commands I Learned

## `index`

``` spl
index=task4
```

Searches a specific index.

------------------------------------------------------------------------

## `search`

``` spl
| search "Failed password"
```

Filters events.

------------------------------------------------------------------------

## `stats`

``` spl
| stats count by clientip
```

Calculates statistics and groups results.

------------------------------------------------------------------------

## `count`

``` spl
count
```

Counts events.

------------------------------------------------------------------------

## `values()`

``` spl
values(useragent)
```

Returns unique values.

------------------------------------------------------------------------

## `by`

``` spl
| stats count by clientip
```

Groups the calculation by the specified field.

------------------------------------------------------------------------

## `sort`

``` spl
| sort -count
```

Sorts descending.

``` spl
| sort +count
```

Sorts ascending.

------------------------------------------------------------------------

## `where`

``` spl
| where count > 25
```

Filters results after a calculation.

------------------------------------------------------------------------

## `bin`

``` spl
| bin _time span=5m
```

Creates 5-minute time buckets.

------------------------------------------------------------------------

## `table`

``` spl
| table _time clientip uri_path useragent
```

Displays only selected fields.

------------------------------------------------------------------------

## `AND`

``` spl
*powershell* AND *EncodedCommand*
```

Requires both conditions.

------------------------------------------------------------------------

## `OR`

``` spl
"Accepted password" OR "Failed password"
```

Matches either condition.

------------------------------------------------------------------------

## Wildcard `*`

``` spl
*powershell*
```

Matches values containing the search term.

------------------------------------------------------------------------

## Pipe `|`

``` spl
index=task6
| stats count by uri_path
| sort -count
```

The pipe passes the result of one command into another.

Think:

``` text
Search
 ↓
Calculate
 ↓
Sort
```

------------------------------------------------------------------------

# 20. My SOC Investigation Method

This room gave me a reusable investigation method.

## Step 1 --- Start with the alert

Example:

``` text
Suspicious connection
Port 5678
Host WIN-105
```

## Step 2 --- Search the correct index

``` spl
index=task4
```

## Step 3 --- Use the information already available

``` spl
index=task4 EventCode=3 DestinationPort=5678
```

## Step 4 --- Extract an IOC

Example:

``` text
10.10.114.80
```

## Step 5 --- Pivot

``` text
IP
 ↓
Process
```

## Step 6 --- Pivot again

``` text
Process
 ↓
Hash
```

## Step 7 --- Look for persistence

``` text
Process
 ↓
Scheduled task / service / account
```

## Step 8 --- Build a timeline

``` text
Authentication
 ↓
Execution
 ↓
Network activity
 ↓
Privilege escalation
 ↓
Persistence
```

## Step 9 --- Identify the behaviour

Examples:

``` text
Brute Force
Scanning
Persistence
Privilege Escalation
Web Shell
DDoS
```

## Step 10 --- Document and escalate

Record:

``` text
Time
Host
User
Source IP
Destination IP
Process
Hash
Command
Persistence
Evidence
```

------------------------------------------------------------------------

# 21. Pivoting

**Pivoting** is one of the most important SOC skills I practiced.

It means using something I discovered to find more information.

Example:

``` text
Alert
 ↓
IP address
 ↓
Process
 ↓
Hash
 ↓
Persistence
```

Web example:

``` text
Alert
 ↓
URI
 ↓
Source IP
 ↓
User-Agent
 ↓
Tool
 ↓
Attack classification
```

Linux example:

``` text
Suspicious account
 ↓
Username
 ↓
SSH login
 ↓
Source IP
 ↓
Failed attempts
 ↓
Privilege escalation
 ↓
Persistence
```

------------------------------------------------------------------------

# 22. Final Answers

## Task 2

  Question                             Answer
  ------------------------------------ --------------------
  Linking data from multiple sources   **Correlation**
  Collecting logs into one location    **Centralisation**

## Task 3

  Question                                       Answer
  ---------------------------------------------- -------------------
  Converting logs into a common format           **Normalisation**
  Source useful for malicious script execution   **Host-Based**

## Task 4 --- Windows

  Question         Answer
  ---------------- ------------------------------------
  IP address       `10.10.114.80`
  Process          `SharePoInt.exe`
  MD5              `770D14FFA142F09730B415506249E7D1`
  Scheduled task   `Office365 Install`

## Task 5 --- Linux

  Question                     Answer
  ---------------------------- -----------------------
  Account creation timestamp   `2025-08-12 09:52:57`
  User who escalated to root   `jack-brown`
  Source IP                    `10.14.94.82`
  Failed attempts              `4`
  Persistence port             `7654`

## Task 6 --- Web

  Question                Answer
  ----------------------- -----------------
  Highest-requested URI   `/wp-login.php`
  Source IP               `10.10.243.134`
  Classification          **Brute Force**
  Tool                    **WPScan**

------------------------------------------------------------------------

# 23. Quick Revision

``` text
SIEM
 ↓
Centralised logs
 ↓
Search
 ↓
Filter
 ↓
Correlate
 ↓
Pivot
 ↓
Timeline
 ↓
Identify behaviour
 ↓
Document / Escalate
```

### Windows

``` text
Sysmon Event 1 → Process Creation
Sysmon Event 3 → Network Connection
4720 → User Created
4722 → User Enabled
7045 → Service Created
7036 → Service Started/Stopped
```

### Linux

``` text
auth.log
→ SSH / authentication / sudo / su

syslog
→ system activity / cron / services
```

### Web

``` text
clientip
→ Source IP

uri_path
→ Requested resource

method
→ GET / POST

status
→ HTTP response

useragent
→ Client/tool information

_time
→ Timeline
```

### Most Important Splunk Commands

``` text
index=
search
stats
count
values()
by
sort
where
bin
table
```

------------------------------------------------------------------------

# 24. Final Takeaway

The biggest thing I learned from this room is that I should not treat
SIEM alerts as isolated events.

For a Windows alert:

``` text
Network connection
 ↓
Process
 ↓
Hash
 ↓
Persistence
```

For a Linux alert:

``` text
SSH
 ↓
Failed attempts
 ↓
Successful login
 ↓
Privilege escalation
 ↓
Persistence
```

For a web alert:

``` text
URI
 ↓
Source IP
 ↓
Request volume
 ↓
User-Agent
 ↓
Tool
 ↓
Attack classification
```

The goal of an L1 analyst is to turn individual log entries into a
meaningful story.

**Alert → Evidence → Correlation → Timeline → Classification →
Escalation**

That is the main SOC skill I took away from this room.

------------------------------------------------------------------------

