# Intro to Log Analysis --- Detailed Walkthrough & Notes

> **TryHackMe Room:** Intro to Log Analysis\
> **Date completed:** 6 October 2026\
> **Focus:** Log analysis, investigation methodology, command-line
> analysis, regex, CyberChef, Sigma and YARA\
> **Style:** My own step-by-step notes for revising the room later

------------------------------------------------------------------------

## 1. What this room taught me

This room helped me understand what log analysis actually looks like
from an analyst's point of view.

A log is basically a record of something that happened. A computer,
server, firewall, web server, application, or security tool can create
logs whenever an event occurs.

As a SOC analyst, I don't want to simply read logs line by line. I want
to turn those raw events into an understandable story:

``` text
Raw logs
   ↓
Find useful fields
   ↓
Filter unnecessary information
   ↓
Search for suspicious activity
   ↓
Count and compare events
   ↓
Correlate different events
   ↓
Build a timeline
   ↓
Decide what happened
```

One of the biggest lessons for me was that I do not always need a SIEM
to start an investigation. Linux command-line tools such as `grep`,
`cut`, `sort`, `uniq`, `awk`, and `sed` can already do a lot of useful
work.

------------------------------------------------------------------------

# Task 2 --- Log Analysis Basics

## 2.1 What is a log?

A **log** is a time-sequenced record of an event or transaction.

A log entry can tell me things such as:

-   When something happened
-   Which system generated the event
-   Which IP address was involved
-   What action occurred
-   What application was involved
-   Whether the action succeeded or failed
-   How serious the event was

For example:

``` text
Jul 28 17:45:02 10.10.0.4 FW-1: %WARNING% general: Unusual network activity detected from IP 10.10.0.15 to IP 203.0.113.25. Source Zone: Internal, Destination Zone: External, Application: web-browsing, Action: Alert.
```

I can break this down into smaller pieces:

``` text
Jul 28 17:45:02
        ↓
Timestamp

10.10.0.4
        ↓
System that generated the log

%WARNING%
        ↓
Severity

10.10.0.15
        ↓
Source IP

203.0.113.25
        ↓
Destination IP

web-browsing
        ↓
Application

Alert
        ↓
Action
```

The important idea is that one log entry contains several pieces of
evidence. My job is to understand what each field means and then compare
it with other events.

------------------------------------------------------------------------

## 2.2 Why logs are important

### System troubleshooting

Logs can tell IT teams why an application or system failed.

### Cybersecurity

Security logs can reveal:

-   Failed authentication
-   Brute-force attempts
-   Malware activity
-   Unauthorized access
-   Suspicious network traffic
-   Privilege changes
-   Data theft

### Threat hunting

Threat hunters can search logs for suspicious behaviour that did not
necessarily generate an existing alert.

For example:

``` text
Known malicious IP
Known malicious domain
Known hash
Suspicious process
Unusual login
```

### Compliance

Organizations may need logs to prove that systems are being monitored
and that security controls are operating correctly.

Examples from the room include GDPR, HIPAA and PCI DSS.

------------------------------------------------------------------------

## 2.3 Types of logs

Different components create different logs.

  Log type           What I can learn from it
  ------------------ ---------------------------------------------------
  Application logs   Application status, errors, warnings and activity
  Audit logs         User actions and system changes
  Security logs      Authentication, permissions and security events
  Server logs        Server operations and access activity
  System logs        Kernel, boot, hardware and system events
  Network logs       Connections, traffic and data transfers
  Database logs      Queries, updates and database activity
  Web server logs    IPs, URLs, methods, status codes and User-Agents

For a SOC analyst, web server and authentication logs are especially
useful because they can show what an external user or attacker was
attempting to do.

------------------------------------------------------------------------

# Task 3 --- Investigation Theory

## 3.1 Timeline

A timeline is simply a chronological representation of events.

For example:

``` text
10:00 — Successful login
10:02 — Suspicious command executed
10:04 — File downloaded
10:05 — Process started
10:06 — Outbound connection created
10:10 — Persistence created
```

This is extremely useful during incident response because I can ask:

-   What happened first?
-   Where did the attacker enter?
-   What did they do after entering?
-   What happened immediately before the alert?
-   What happened after the suspicious event?

A timeline can help me reconstruct the attack instead of looking at
isolated events.

------------------------------------------------------------------------

## 3.2 Timestamps and time zones

Time is one of the easiest things to get wrong during an investigation.

Different systems may use different time zones:

``` text
System A → UTC
System B → Local time
System C → Another time zone
```

If I compare the timestamps without considering the time zone, I could
put events in the wrong order.

Splunk handles indexed timestamps using its `_time` field, which makes
correlation easier.

My takeaway:

> Before creating a timeline, I should understand the timestamp format
> and time zone used by every important log source.

------------------------------------------------------------------------

## 3.3 Super timelines

A **super timeline** or consolidated timeline combines evidence from
multiple sources.

Instead of looking at:

``` text
Windows logs
Linux logs
Firewall logs
Web logs
Application logs
```

individually, I can combine events into one chronological timeline.

For example:

``` text
Authentication event
      ↓
Web request
      ↓
Firewall connection
      ↓
File creation
      ↓
Process execution
```

This can reveal relationships that are difficult to see when every log
source is investigated separately.

The room introduces **Plaso / log2timeline** as an open-source tool that
can automate timeline creation from many forensic data sources.

------------------------------------------------------------------------

## 3.4 Data visualization

Tools such as Splunk and Kibana can turn raw log data into graphs and
dashboards.

For example, if I want to monitor failed logins, I could visualize the
number of failures over time.

A sudden spike could look like:

``` text
Failed logins
     ↑
     |             █
     |             █
     |      █      █
     | █    █      █
     +----------------→ Time
```

Visualization helps me notice patterns quickly, but I still need to
investigate the underlying events.

------------------------------------------------------------------------

## 3.5 Log monitoring and alerting

A SOC cannot manually watch every log line forever.

SIEM platforms can create alerts when certain conditions occur.

Examples:

``` text
Many failed logins
Privilege escalation
Sensitive file access
Suspicious process
Known malicious IP
Known malicious domain
```

An alert is not automatically proof of an attack. It is a signal that
should be investigated.

A good SOC workflow is:

``` text
Event
 ↓
Detection
 ↓
Alert
 ↓
SOC L1 triage
 ↓
Escalation if required
 ↓
L2 / Incident Response
```

------------------------------------------------------------------------

## 3.6 Threat intelligence and logs

Threat intelligence can give me known indicators such as:

``` text
IP addresses
Domains
File hashes
URLs
```

I can then search for those indicators in my logs.

Example:

``` bash
grep "54.36.149.64" logfile.txt
```

If the IP appears, I investigate the surrounding events.

Important lesson:

> A threat-intelligence match is evidence, not automatically a verdict.
> I still need context.

------------------------------------------------------------------------

# Task 4 --- Detection Engineering

## 4.1 Common log locations

Some common Linux log locations from the room are:

### Nginx

``` text
/var/log/nginx/access.log
/var/log/nginx/error.log
```

### Apache

``` text
/var/log/apache2/access.log
/var/log/apache2/error.log
```

### MySQL

``` text
/var/log/mysql/error.log
```

### PostgreSQL

``` text
/var/log/postgresql/postgresql-{version}-main.log
```

### Linux

``` text
/var/log/syslog
/var/log/auth.log
```

### Snort

``` text
/var/log/snort/
```

These are common locations, not guaranteed locations. Configuration can
change where logs are stored.

------------------------------------------------------------------------

## 4.2 Abnormal user behaviour

One important detection idea is comparing current behaviour with normal
behaviour.

Examples:

### Multiple failed logins

``` text
Many failures in a short time
```

Possible explanation:

``` text
Brute force
Password spraying
User mistakes
```

### Unusual login time

A user normally logs in during the day but suddenly logs in at an
unusual time.

This is suspicious, but it is not automatically malicious.

### Geographic anomaly

A user logs in from an unexpected location.

Possible explanations include:

``` text
Compromised credentials
VPN
Travel
Account sharing
```

### Unusual User-Agent

Some automated tools identify themselves in HTTP logs.

The room mentions examples such as Nmap's scripting engine and Hydra.

This is useful because the User-Agent can become an investigation clue.

------------------------------------------------------------------------

# 4.3 Common attack signatures

## SQL Injection

Example:

``` text
GET /products.php?q=books' UNION SELECT ...
```

Things I might look for include:

``` text
'
UNION
SELECT
--
#
SLEEP()
WAITFOR DELAY
```

Attackers can also URL-encode payloads, so the visible log text may not
look exactly like the original payload.

------------------------------------------------------------------------

## Cross-Site Scripting

Example:

``` text
GET /products.php?search=<script>alert(1);</script>
```

Interesting patterns include:

``` text
<script>
onerror
onclick
onmouseover
```

------------------------------------------------------------------------

## Path Traversal

Example:

``` text
GET /../../../../../etc/passwd
```

Interesting indicators include:

``` text
../
../../
/etc/passwd
/etc/shadow
```

URL encoding can hide the same characters.

For example:

``` text
%2E → .
%2F → /
```

Therefore, detection should consider both normal and encoded forms.

------------------------------------------------------------------------

# Task 5 --- Automated vs Manual Analysis

## 5.1 Automated analysis

Automated analysis uses software to process large amounts of data.

### Advantages

``` text
Fast
Scales to large datasets
Can identify repeated patterns
Can automate alerting
Can use AI/ML techniques
```

### Disadvantages

``` text
Can be expensive
Can generate false positives
Can miss new or unusual activity
Quality depends on the detection logic
```

------------------------------------------------------------------------

## 5.2 Manual analysis

Manual analysis means that I investigate logs directly using commands or
tools.

Examples:

``` bash
grep
cut
sort
uniq
awk
sed
```

### Advantages

``` text
Cheap
Flexible
Good for small investigations
Good for understanding raw evidence
```

### Disadvantages

``` text
Time-consuming
Hard to scale
Easy to miss events in very large datasets
```

The best SOC approach is normally a combination:

``` text
Automation finds interesting events
            ↓
Analyst investigates the evidence manually
            ↓
Analyst decides what happened
```

------------------------------------------------------------------------

# Task 6 --- Log Analysis Tools: Command Line

This was one of the most practical parts of the room for me.

The lab provides `apache.log` under:

``` text
/root/Rooms/introloganalysis/task6
```

The idea is to use normal Linux commands to investigate the web server
log.

------------------------------------------------------------------------

## 6.1 `cat`

`cat` displays the contents of a file.

``` bash
cat apache.log
```

This is useful for small files.

For large logs, however, the output can become difficult to read.

------------------------------------------------------------------------

## 6.2 `less`

`less` allows me to read a file page by page.

``` bash
less apache.log
```

Useful controls:

``` text
Arrow keys       → move
Page Up/Down     → scroll
q                → quit
```

For large log files, I would normally start with `less` rather than
`cat`.

------------------------------------------------------------------------

## 6.3 `tail`

`tail` displays the end of a file.

``` bash
tail apache.log
```

By default, it shows the last 10 lines.

I can specify the number of lines:

``` bash
tail -n 5 apache.log
```

### Live monitoring

``` bash
tail -f apache.log
```

The `-f` option keeps watching the file and displays new lines as they
are added.

This is useful when monitoring a live service.

------------------------------------------------------------------------

## 6.4 `head`

`head` displays the beginning of a file.

``` bash
head apache.log
```

Or:

``` bash
head -n 20 apache.log
```

------------------------------------------------------------------------

## 6.5 `wc`

`wc` gives quick statistics about a file.

``` bash
wc apache.log
```

Example:

``` text
70 1562 14305 apache.log
```

This means:

``` text
70    → lines
1562  → words
14305 → characters
```

It is useful when I first receive a log because I immediately know
roughly how much data I am dealing with.

------------------------------------------------------------------------

## 6.6 `cut`

`cut` extracts fields from a line.

Apache logs are separated into fields, so I can use a space as a
delimiter.

To extract the first field, which is the source IP in this log format:

``` bash
cut -d ' ' -f 1 apache.log
```

Breakdown:

``` text
-d ' '
  ↓
Use a space as the delimiter

-f 1
  ↓
Return field 1
```

This is a very useful command because I can extract only the part of the
log I need.

------------------------------------------------------------------------

## 6.7 `sort`

`sort` sorts the output.

Example:

``` bash
cut -d ' ' -f 1 apache.log | sort -n
```

The important part here is the pipe:

``` text
cut
 ↓
output
 ↓
sort
```

Reverse order:

``` bash
cut -d ' ' -f 1 apache.log | sort -n -r
```

`-r` means reverse.

------------------------------------------------------------------------

## 6.8 `uniq`

`uniq` removes adjacent duplicate lines.

It is usually most useful after sorting:

``` bash
cut -d ' ' -f 1 apache.log | sort | uniq
```

To count occurrences:

``` bash
cut -d ' ' -f 1 apache.log | sort | uniq -c
```

Example:

``` text
1 221.90.64.76
6 203.64.78.90
```

The number on the left tells me how many times the value appeared.

This is extremely useful for finding high-volume IP addresses.

------------------------------------------------------------------------

## 6.9 `sed`

`sed` is a stream editor used to transform text.

Example:

``` bash
sed 's/31\/Jul\/2023/July 31, 2023/g' apache.log
```

This replaces the old date format with the new text.

By default, the command prints the transformed output without changing
the original file.

Be careful with:

``` bash
sed -i
```

because `-i` can modify the original file. During forensic
investigations, preserving original evidence is important.

------------------------------------------------------------------------

## 6.10 `awk`

`awk` is excellent when I want to make decisions based on fields.

Example:

``` bash
awk '$9 >= 400' apache.log
```

In the room's Apache format, `$9` represents the HTTP status code.

Therefore, this means:

> Show me entries where the HTTP status code is 400 or higher.

This can quickly identify error responses.

------------------------------------------------------------------------

## 6.11 `grep`

`grep` is one of the most important commands for SOC work.

Basic search:

``` bash
grep "admin" apache.log
```

It returns lines containing `admin`.

### Count matches

``` bash
grep -c "admin" apache.log
```

### Show line numbers

``` bash
grep -n "admin" apache.log
```

### Reverse the search

``` bash
grep -v "/index.php" apache.log
```

This returns lines that do **not** contain `/index.php`.

------------------------------------------------------------------------

# 6.12 Understanding the pipe `|`

The pipe is extremely important.

It sends the output of one command into another command.

For example:

``` bash
cut -d ' ' -f 1 apache.log | sort | uniq -c | sort -nr
```

I can read this from left to right:

``` text
Extract IPs
    ↓
Sort IPs
    ↓
Count duplicates
    ↓
Sort counts from highest to lowest
```

This is a complete mini-investigation pipeline.

------------------------------------------------------------------------

# 6.13 My Task 6 Investigation

## Question 1 --- Flag in a unique URL

I wanted to extract the URL field from the Apache log.

I used:

``` bash
cut -d ' ' -f 7 apache.log
```

Then I searched for URLs containing `flag`:

``` bash
cut -d ' ' -f 7 apache.log | grep flag
```

The result was:

``` text
/index.php?flag=c701d43cc5a3acb9b5b04db7f1be94f6
```

Therefore my answer was:

``` text
c701d43cc5a3acb9b5b04db7f1be94f6
```

### What I learned

I did not need to read the entire log manually. I extracted the URL
field and then searched only that output.

------------------------------------------------------------------------

## Question 2 --- Number of HTTP 200 responses

I used:

``` bash
grep -c "200" apache.log
```

The result was:

``` text
52
```

Therefore:

``` text
52 HTTP 200 responses
```

The `-c` option is useful when I want the number of matching lines
rather than the actual lines.

------------------------------------------------------------------------

## Question 3 --- IP generating the most traffic

My answer was:

``` text
145.76.33.201
```

A general command I can use for this kind of investigation is:

``` bash
cut -d ' ' -f 1 apache.log | sort | uniq -c | sort -nr
```

The pipeline means:

``` text
1. Extract IP addresses
2. Sort them
3. Count repetitions
4. Sort by count, highest first
```

The IP at the top is the strongest candidate for the highest traffic
volume.

------------------------------------------------------------------------

## Question 4 --- Timestamp for `/login.php`

I searched for the IP and endpoint:

``` bash
grep "110.122.65.76" apache.log | grep "/login.php"
```

The matching log entry contained:

``` text
[31/Jul/2023:12:34:40 +0000]
```

My answer was:

``` text
31/Jul/2023:12:34:40 +0000
```

This was a good example of narrowing a large log down using two simple
filters.

------------------------------------------------------------------------

# Task 7 --- Regular Expressions

## 7.1 What is regex?

A regular expression is a pattern used to find text that follows a
particular structure.

Instead of searching only for one exact string, I can search for a whole
category of values.

For example:

``` text
Find every IPv4 address
Find every URL
Find post IDs 10–19
Find suspicious parameters
```

------------------------------------------------------------------------

## 7.2 Regex with grep

The room demonstrates:

``` bash
grep -E 'post=1[0-9]' apache-ex2.log
```

`-E` enables extended regular expressions.

The pattern:

``` text
post=1[0-9]
```

means:

``` text
post=1
+
one digit from 0 to 9
```

So it matches:

``` text
post=10
post=11
post=12
...
post=19
```

------------------------------------------------------------------------

## 7.3 IPv4 regex

The room uses this simplified IPv4 pattern:

``` text
\b([0-9]{1,3}\.){3}[0-9]{1,3}\b
```

Breaking it down:

``` text
\b
```

Word boundary.

``` text
[0-9]{1,3}
```

One to three digits.

``` text
\.
```

A literal dot.

``` text
([0-9]{1,3}\.){3}
```

Repeat the digit-and-dot group three times.

Then:

``` text
[0-9]{1,3}
```

matches the final octet.

This is a practical matching pattern, not a strict IPv4 validator,
because it can technically match values above 255.

------------------------------------------------------------------------

# Task 8 --- CyberChef

## 8.1 What is CyberChef?

CyberChef is a web-based data analysis and transformation tool created
by GCHQ.

I can use it for:

-   Base64 decoding
-   Encoding
-   Hashing
-   Encryption/decryption operations
-   Regex
-   File processing
-   Data extraction
-   Other transformations

I think of it as a toolbox where I build a recipe from operations.

------------------------------------------------------------------------

## 8.2 CyberChef interface

### Operations

The available transformations.

### Recipe

The operations I have selected.

### Input

The data I want to process.

### Output

The final result.

Basic workflow:

``` text
Input
 ↓
Operation / Recipe
 ↓
Output
```

------------------------------------------------------------------------

## 8.3 Base64 decoding

The room demonstrates:

``` text
dHJ5aGFja21l
```

which decodes to:

``` text
tryhackme
```

For Base64 data, I select:

``` text
From Base64
```

If I do not know what encoding I am looking at, CyberChef's **Magic**
operation can help me make an educated guess.

------------------------------------------------------------------------

## 8.4 CyberChef regex

CyberChef can also apply regex to uploaded logs.

For IPv4 extraction, I can use:

``` text
\b([0-9]{1,3}\.){3}[0-9]{1,3}\b
```

Then I can select:

``` text
Output format → List matches
```

This gives me a clean list of matching IP addresses rather than the
complete log.

------------------------------------------------------------------------

## 8.5 Uploading a file

A useful CyberChef workflow is:

``` text
Download / locate file
        ↓
Open CyberChef
        ↓
Upload file
        ↓
Choose operation
        ↓
Process data
        ↓
Inspect output
```

CyberChef can also work with compressed files such as ZIP and TAR/GZIP
through appropriate operations.

------------------------------------------------------------------------

# 8.6 My Task 8 Investigation

## Question 1 --- IP beginning with 212

I uploaded `access.log` to CyberChef.

I used a regular expression to find IPv4 addresses:

``` text
\b([0-9]{1,3}\.){3}[0-9]{1,3}\b
```

I selected:

``` text
Output format → List matches
```

Then I looked through the extracted IP list for the address beginning
with `212`.

My answer was:

``` text
212.14.17.145
```

------------------------------------------------------------------------

## Question 2 --- Decode the Base64 request

I took the Base64-encoded request from the log and opened CyberChef.

I selected:

``` text
From Base64
```

The decoded value was:

``` text
THM{CYBERCHEF_WIZARD}
```

This demonstrated why encoded data in logs should not immediately be
treated as meaningless text. An attacker or application may encode
useful information.

------------------------------------------------------------------------

## Question 3 --- Extract the MAC address

I first decoded `encodedflag.txt` using CyberChef.

After decoding, I used the following regex:

``` text
([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}
```

The pattern means:

``` text
2 hexadecimal characters
        ↓
-
        ↓
repeat five times
        ↓
final 2 hexadecimal characters
```

I selected the output option to list the matches.

The extracted value was:

``` text
08-2E-9A-4B-7F-61
```

------------------------------------------------------------------------

# Task 9 --- Sigma and YARA

## 9.1 Sigma

Sigma is an open-source, structured way of describing log detections.

It is useful because the detection idea can be represented independently
of one particular SIEM implementation.

A Sigma rule can help:

``` text
Describe a detection
        ↓
Search log events
        ↓
Identify suspicious behaviour
        ↓
Convert/use it in SIEM tooling
```

------------------------------------------------------------------------

## 9.2 Understanding a Sigma rule

Example:

``` yaml
title: Failed SSH Logins
description: Searches sshd logs for failed SSH login attempts
status: experimental
author: CMNatic
logsource:
    product: linux
    service: sshd

detection:
    selection:
        type: 'sshd'
        a0|contains: 'Failed'
        a1|contains: 'Illegal'
    condition: selection

falsepositives:
    - Users forgetting or mistyping their credentials

level: medium
```

### `title`

Names the detection.

### `description`

Explains the purpose.

### `status`

Shows the maturity of the rule.

### `author`

Identifies the author.

### `logsource`

Defines the log source.

### `detection`

Defines what the rule searches for.

### `falsepositives`

Documents legitimate reasons the detection might trigger.

This is important because:

``` text
Detection triggered ≠ confirmed attack
```

### `level`

Represents the severity of the detection.

------------------------------------------------------------------------

# 9.3 YARA

YARA is a rule-based pattern-matching tool that is commonly used for
malware analysis.

The room also demonstrates how it can be applied to log-like data.

Example:

``` text
rule IPFinder {
    meta:
        author = "CMNatic"
    strings:
        $ip = /([0-9]{1,3}\.){3}[0-9]{1,3}/ wide ascii
    condition:
        $ip
}
```

The main parts are:

``` text
rule
 ↓
Name of rule

meta
 ↓
Information about the rule

strings
 ↓
Patterns to search for

condition
 ↓
When the rule should trigger
```

Running the room's example:

``` bash
yara ipfinder.yar apache2.txt
```

can produce a result such as:

``` text
IPFinder apache2
```

which means the rule matched the file.

------------------------------------------------------------------------

# 10. My SOC Investigation Method From This Room

I can now combine everything I learned into one simple workflow.

## Step 1 --- Understand the source

First I ask:

``` text
What type of log is this?
Who generated it?
What does each field mean?
```

## Step 2 --- Check the size

``` bash
wc logfile
```

This tells me how much data I have.

## Step 3 --- Inspect the format

``` bash
head logfile
```

or:

``` bash
less logfile
```

## Step 4 --- Identify useful fields

For an Apache log, this could be:

``` text
IP
Timestamp
Method
URL
Status
User-Agent
```

## Step 5 --- Search

``` bash
grep "keyword" logfile
```

## Step 6 --- Extract

``` bash
cut -d ' ' -f 1 logfile
```

## Step 7 --- Count

``` bash
sort | uniq -c
```

## Step 8 --- Rank

``` bash
sort -nr
```

## Step 9 --- Decode when necessary

Use CyberChef for:

``` text
Base64
URL encoding
Other transformations
```

## Step 10 --- Use regex for patterns

For example:

``` text
IP addresses
MAC addresses
URLs
Suspicious parameters
```

## Step 11 --- Correlate

Compare the evidence with:

``` text
Threat intelligence
Other log sources
Known attack patterns
User behaviour
Timeline
```

## Step 12 --- Decide

Finally:

``` text
Benign?
Suspicious?
Malicious?
Needs escalation?
```

------------------------------------------------------------------------

# 11. Useful Command Cheat Sheet

  Command          What I use it for
  ---------------- -----------------------------------
  `cat file`       Display file contents
  `less file`      Read a large file page by page
  `head file`      View the beginning
  `tail file`      View the end
  `tail -f file`   Monitor new log entries
  `wc file`        Count lines, words and characters
  `cut`            Extract fields
  `sort`           Sort output
  `uniq`           Remove adjacent duplicates
  `uniq -c`        Count duplicates
  `grep`           Search for text/patterns
  `grep -c`        Count matching lines
  `grep -n`        Show matching line numbers
  `grep -v`        Exclude matches
  `sed`            Transform text
  `awk`            Process fields and conditions
  `\|`             Send output to another command

------------------------------------------------------------------------

# 12. Final Answers

## Task 6 --- Command Line

  ------------------------------------------------------------------------
  Question                            Answer
  ----------------------------------- ------------------------------------
  Flag in unique URL                  `c701d43cc5a3acb9b5b04db7f1be94f6`

  Total HTTP 200 responses            `52`

  IP generating most traffic          `145.76.33.201`

  Timestamp for `110.122.65.76`       `31/Jul/2023:12:34:40 +0000`
  accessing `/login.php`              
  ------------------------------------------------------------------------

## Task 8 --- CyberChef

  Question                Answer
  ----------------------- -------------------------
  IP beginning with 212   `212.14.17.145`
  Decoded Base64 value    `THM{CYBERCHEF_WIZARD}`
  Extracted MAC address   `08-2E-9A-4B-7F-61`

------------------------------------------------------------------------

# 13. What I Took Away From This Room

The biggest thing I learned is that log analysis is not just about
reading a log.

It is about asking questions of the data.

For example:

``` text
Who?
 ↓
Which IP / user / process?

What?
 ↓
What action happened?

When?
 ↓
What was the timestamp?

Where?
 ↓
Which system / URL / destination?

How often?
 ↓
Is this normal or unusually frequent?

What happened before and after?
 ↓
Build the timeline

Is it known malicious activity?
 ↓
Threat intelligence / correlation
```

I also learned that very simple tools can be powerful when I combine
them correctly.

For example:

``` bash
cut -d ' ' -f 1 apache.log | sort | uniq -c | sort -nr
```

looks simple, but it answers a real SOC-style question: **which IP
appears most frequently?**

Similarly:

``` bash
grep "110.122.65.76" apache.log | grep "/login.php"
```

quickly narrows thousands of possible log entries down to the event I
actually care about.

------------------------------------------------------------------------

# 14. Quick Revision Before an Interview

### What is log analysis?

The process of examining recorded events to understand system activity
and identify anomalies or security incidents.

### Why are timelines important?

They help reconstruct the sequence of events and understand how an
incident developed.

### What does `grep` do?

Searches text for matching strings or patterns.

### What does `cut` do?

Extracts selected fields from structured text.

### What does `sort` do?

Sorts the output.

### What does `uniq -c` do?

Groups adjacent duplicate values and counts them.

### Why use pipes?

To send one command's output into another command and build an
investigation pipeline.

### What is regex?

A pattern language for searching and matching text.

### What is CyberChef?

A general-purpose data transformation and analysis tool useful for
decoding, extraction, regex and many other operations.

### What is Sigma?

A structured, portable format for describing log detections.

### What is YARA?

A rule-based pattern-matching tool commonly used for identifying
characteristics in files and other data.

------------------------------------------------------------------------

# 15. Final Investigation Mindset

The workflow I want to remember from this room is:

``` text
COLLECT
   ↓
UNDERSTAND THE LOG FORMAT
   ↓
FILTER THE NOISE
   ↓
EXTRACT USEFUL FIELDS
   ↓
SEARCH FOR INDICATORS
   ↓
COUNT / SORT / COMPARE
   ↓
DECODE WHEN NECESSARY
   ↓
CORRELATE EVENTS
   ↓
BUILD A TIMELINE
   ↓
CHECK THREAT INTELLIGENCE
   ↓
ASSESS THE ACTIVITY
   ↓
ESCALATE IF REQUIRED
```

