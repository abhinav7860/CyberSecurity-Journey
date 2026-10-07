# Boogeyman 2 --- DFIR Investigation Notes

**Date:** 2026-10-07\
**Platform:** TryHackMe\
**Room:** Boogeyman 2\
**Investigation Focus:** Phishing → VBA Macro → JavaScript Downloader →
Malicious Binary → C2 → Persistence\
**Primary Tools:** `olevba`, Volatility 3, Linux command-line utilities
such as `grep` and `strings`

> **Sanitization note:** This document is intended as a personal
> learning/revision record. Victim email addresses and lab host IP
> addresses have been removed or generalized. Malicious infrastructure
> indicators are **defanged** where appropriate. File names, commands,
> process IDs, paths, and investigation methodology are retained because
> they are useful for understanding and reproducing the forensic
> workflow inside the authorised TryHackMe lab.

------------------------------------------------------------------------

## 1. What this room was about

This investigation was a practical DFIR exercise involving a Windows
workstation that had been compromised through a phishing email.

The overall attack chain we reconstructed was:

``` text
Phishing Email
    |
    v
Malicious Word Document
    |
    v
VBA AutoOpen Macro
    |
    v
Download update.js
    |
    v
wscript.exe executes update.js
    |
    v
update.js downloads update.exe
    |
    v
Saved as C:\Windows\Tasks\updater.exe
    |
    v
updater.exe executes
    |
    v
C2 communication
    |
    v
Scheduled Task persistence
```

The important lesson from this room was that no single artefact gave us
the complete story. We had to correlate evidence from the email, Office
macro, process tree, process memory, network connections, file objects,
command lines, and persistence artefacts.

TryHackMe describes Boogeyman 2 as an investigation into the threat
group's tactics, techniques and procedures, with a phishing email and a
memory dump provided as the primary artefacts. The room specifically
provides Volatility and Olevba for the investigation.

------------------------------------------------------------------------

# 2. Investigation environment

The investigation was performed in the TryHackMe AttackBox.

The artefacts were located under:

``` text
/home/ubuntu/Desktop/Artefacts
```

The important files were:

``` text
Resume - Application for Junior IT Analyst Role.eml
WKSTN-2961.raw
```

The first file was the phishing email.

The second file was the raw memory image of the compromised Windows
workstation.

The official room documentation also identifies
`/home/ubuntu/Desktop/Artefacts` as the location of the provided
phishing email and workstation memory dump, and lists Volatility and
Olevba as the main investigation tools.

------------------------------------------------------------------------

# 3. Initial approach

Before jumping into commands, I treated the investigation as a timeline
reconstruction problem.

I wanted to answer:

1.  What was the initial access method?
2.  What file was delivered to the victim?
3.  What did the malicious document do?
4.  What process executed the next stage?
5.  What binary was ultimately executed?
6.  What process established C2?
7.  Which IP and port were contacted?
8.  Where was the malicious binary stored?
9.  How did the attacker maintain persistence?
10. What exact commands were used?

This approach prevented me from looking at isolated strings and assuming
that the first suspicious-looking value was automatically the answer.

------------------------------------------------------------------------

# 4. Step 1 --- Inspecting the phishing email

The first artefact was:

``` text
Resume - Application for Junior IT Analyst Role.eml
```

The email was designed to look like a job application.

The sender used an Outlook-style address and the recipient was an
employee of the fictional organisation used in the room.

The subject was:

``` text
Resume - Application for Junior IT Analyst Role
```

The message contained a Microsoft Word attachment.

The attachment filename was:

``` text
Resume_WesleyTaylor.doc
```

The email headers showed that the message passed SPF, but this did not
make the email trustworthy.

This was an important lesson:

> Authentication results such as SPF passing do not automatically mean
> that the message is safe.

An attacker can use infrastructure that passes email authentication
while still delivering a malicious attachment.

------------------------------------------------------------------------

# 5. Step 2 --- Extracting the Word attachment

The email contained a MIME attachment.

The attachment was identified as:

``` text
application/msword
```

with the filename:

``` text
Resume_WesleyTaylor.doc
```

The normal `munpack` utility was not available in the environment, so
the attachment was extracted using Python instead.

This was a useful troubleshooting moment because forensic work does not
always go exactly according to the planned toolset.

The important principle was:

> If one extraction utility is unavailable, preserve the original
> artefact and use another method that performs the same forensic task.

After extraction, the Word document was analysed for embedded VBA.

------------------------------------------------------------------------

# 6. Step 3 --- Analysing the malicious Office document

The main tool used here was:

``` bash
olevba
```

The purpose of Olevba is to inspect Office documents and identify
embedded VBA macros.

The basic command was:

``` bash
olevba Resume_WesleyTaylor.doc
```

The analysis revealed a VBA module:

``` text
NewMacros.bas
```

Inside it was:

``` text
Sub AutoOpen()
```

This was extremely important.

`AutoOpen` means that the macro is designed to execute automatically
when the document is opened under the relevant Office macro-execution
conditions.

The macro therefore provided the initial execution mechanism.

------------------------------------------------------------------------

# 7. Step 4 --- Understanding the VBA macro

The macro used COM objects associated with HTTP communication and stream
handling.

The important objects included:

``` text
Microsoft.XMLHTTP
Adodb.Stream
```

The macro created an HTTP request, retrieved content from an
attacker-controlled server, wrote that content to disk, and then
executed it.

The download destination was:

``` text
C:\ProgramData\update.js
```

The downloaded URL was:

``` text
https://files[.]boogeymanisback[.]lol/aa2a9c53cbb80416d3b47d85538d9971/update.png
```

The macro then executed:

``` text
wscript.exe C:\ProgramData\update.js
```

This gave us the first major execution chain:

``` text
WINWORD.EXE
    |
    v
VBA AutoOpen
    |
    v
Download update.js
    |
    v
wscript.exe
    |
    v
C:\ProgramData\update.js
```

------------------------------------------------------------------------

# 8. Why the extension was suspicious

The macro downloaded a file from a URL ending in:

``` text
update.png
```

However, the response was not simply a harmless image.

The content was saved as:

``` text
update.js
```

This demonstrates an important malware-analysis concept:

> The URL extension does not necessarily tell you what the downloaded
> content actually is.

Attackers can use misleading extensions, arbitrary filenames, or
benign-looking resource names to make network traffic and files appear
less suspicious.

------------------------------------------------------------------------

# 9. Step 5 --- Moving from static analysis to memory forensics

At this point we knew that the document executed JavaScript through:

``` text
wscript.exe
```

The next question was:

> Did the memory image contain evidence of this execution?

This is where Volatility 3 became the main tool.

The memory image was:

``` text
WKSTN-2961.raw
```

A basic process listing was performed using:

``` bash
vol -f WKSTN-2961.raw windows.pslist
```

To specifically locate Windows Script Host:

``` bash
vol -f WKSTN-2961.raw windows.pslist | grep -i wscript
```

This returned:

``` text
wscript.exe    PID 4260
```

Therefore:

``` text
wscript.exe PID = 4260
```

------------------------------------------------------------------------

# 10. Step 6 --- Building the process tree

Finding a process ID alone was not enough.

We needed to understand how the process was created.

The command used was:

``` bash
vol -f WKSTN-2961.raw windows.pstree
```

The relevant process relationship was:

``` text
OUTLOOK.EXE
    |
    v
WINWORD.EXE
    |
    +---- wscript.exe
              |
              v
          updater.exe
```

The important PIDs were:

``` text
WINWORD.exe   PID 1124
wscript.exe   PID 4260
updater.exe   PID 6216
```

The process tree showed that `wscript.exe` was created by the Office
process, which connected the email attachment and macro execution to the
next stage.

The process tree also showed:

``` text
wscript.exe PID 4260
    |
    v
updater.exe PID 6216
```

This was the point where the investigation moved from the script stage
to the binary stage.

------------------------------------------------------------------------

# 11. Step 7 --- Identifying the malicious binary

The process created by `wscript.exe` was:

``` text
updater.exe
```

Its PID was:

``` text
6216
```

The process command line later confirmed:

``` text
6216 updater.exe "C:\Windows\Tasks\updater.exe"
```

Therefore the full path of the malicious binary was:

``` text
C:\Windows\Tasks\updater.exe
```

This is an important forensic distinction:

-   `wscript.exe` was the script execution process.
-   `update.js` was the stage-2 JavaScript payload.
-   `updater.exe` was the malicious binary.
-   `updater.exe` was the process that established the C2 connection.

------------------------------------------------------------------------

# 12. Step 8 --- Investigating network activity

After identifying PID 6216, the next step was to find its network
connections.

The command used was:

``` bash
vol -f WKSTN-2961.raw windows.netscan | grep -E '4260|6216'
```

The results showed repeated connections associated with:

``` text
updater.exe
PID 6216
```

The destination was:

``` text
128[.]199[.]95[.]189:8080
```

Therefore the C2 endpoint was:

``` text
128[.]199[.]95[.]189:8080
```

The connections appeared repeatedly in the memory snapshot.

This allowed us to establish:

``` text
updater.exe
    |
    v
128[.]199[.]95[.]189:8080
```

The important lesson here was that `netscan` allowed us to connect a
process ID to network activity.

------------------------------------------------------------------------

# 13. Step 9 --- Dumping and investigating process memory

At this point, we knew:

``` text
wscript.exe = PID 4260
updater.exe = PID 6216
C2 = 128[.]199[.]95[.]189:8080
```

However, we still needed to understand how the second-stage script
downloaded the executable.

The key process for this question was not `updater.exe`.

It was:

``` text
wscript.exe PID 4260
```

because this process was responsible for executing:

``` text
C:\ProgramData\update.js
```

We first confirmed the process:

``` bash
vol -f WKSTN-2961.raw windows.pslist --pid 4260
```

The result confirmed:

``` text
4260  ...  wscript.exe
```

with the corresponding creation time.

------------------------------------------------------------------------

# 14. Step 10 --- Dumping the memory mappings

We then used:

``` bash
vol -f WKSTN-2961.raw windows.memmap --pid 4260 --dump
```

This generated temporary Volatility dump files.

Because the output was large, it was redirected:

``` bash
vol -f WKSTN-2961.raw windows.memmap --pid 4260 --dump > memmap4260.txt
```

This made it easier to inspect the generated output.

The command produced temporary files similar to:

``` text
tmp_yu061gyn.vol3
tmp_urlqmc2x.vol3
```

Each dump was approximately 1 MB in this investigation.

------------------------------------------------------------------------

# 15. Step 11 --- An important troubleshooting moment

Initially, I tried searching for a file with a guessed name such as:

``` text
pid.4260.dmp
```

That failed because Volatility had not created a file with that name.

The error was essentially:

``` text
No such file
```

Instead of assuming the dump failed, we checked the directory for
recently created files.

A useful command was:

``` bash
find ~/Desktop/Artefacts -type f -newermt "07:01" -ls
```

This revealed the temporary `.vol3` files.

This was a valuable lesson:

> When a forensic tool generates temporary output, do not assume the
> filename. Verify the filesystem and identify the actual generated
> artefact.

------------------------------------------------------------------------

# 16. Step 12 --- Searching dumped memory with strings

After locating the dump files, we searched them using `strings`.

For example:

``` bash
strings -a tmp_urlqmc2x.vol3 | grep -Ei 'ProgramData|update\.js|XMLHTTP|ADODB|ServerXMLHTTP|CreateObject|Run|Shell|SaveToFile'
```

This revealed strings associated with:

``` text
wscript.exe C:\ProgramData\update.js
```

and Windows COM objects used for HTTP communication and file writing.

This initially gave us useful evidence but not the exact download URL.

------------------------------------------------------------------------

# 17. Step 13 --- Why UTF-16 strings mattered

The major breakthrough came from searching UTF-16 encoded strings.

The command used was:

``` bash
strings -a -el tmp_urlqmc2x.vol3 | grep -Ei 'http|https|boogeyman|\.exe|\.lol|128\.199'
```

The `-el` option was important because Windows applications frequently
store strings as UTF-16LE.

A normal ASCII `strings` search can miss these values.

The search exposed strings including:

``` text
/aa2a9c53cbb80416d3b47d85538d9971/update.exe
```

and:

``` text
files.boogeymanisback.lol
```

and most importantly:

``` text
https://files.boogeymanisback.lol/aa2a9c53cbb80416d3b47d85538d9971/update.exe
```

This was the URL used by the stage-2 JavaScript to download the
malicious executable.

------------------------------------------------------------------------

# 18. Step 14 --- Understanding the stage-2 download

The memory strings showed that the script used:

``` text
MSXML2.XMLHTTP
```

and:

``` text
IServerXMLHTTPRequest2
```

The script performed an HTTP request and accessed:

``` text
responseBody
```

The response was then written to disk using:

``` text
_Stream.SaveToFile(...)
```

The destination was:

``` text
C:\Windows\Tasks\updater.exe
```

The relevant sequence was effectively:

``` text
Create HTTP object
       |
       v
Request update.exe
       |
       v
Receive responseBody
       |
       v
SaveToFile
       |
       v
C:\Windows\Tasks\updater.exe
       |
       v
Execute updater.exe
```

------------------------------------------------------------------------

# 19. Step 15 --- Confirming that the downloaded content was an executable

The memory dump also contained an HTTP response similar to:

``` text
HTTP/1.1 200 OK
Content-Type: application/x-msdos-program
Content-Length: 36864
```

The content type was consistent with an executable rather than a normal
image.

This helped confirm that the network response associated with the
stage-2 request was intended to deliver executable content.

The key forensic lesson is:

> Network metadata and process memory can complement each other. The URL
> tells us where the content came from, while the HTTP response metadata
> helps explain what type of content was received.

------------------------------------------------------------------------

# 20. Step 16 --- Confirming the malicious binary path

The memory evidence showed:

``` text
_Stream.SaveToFile("C:\Windows\Tasks\updater.exe", "2")
```

and then:

``` text
IWshShell3.Run("C:\Windows\Tasks\updater.exe")
```

This directly connected the downloaded payload to the process we later
observed in the process tree.

Therefore:

``` text
Downloaded executable:
C:\Windows\Tasks\updater.exe
```

and:

``` text
Process:
updater.exe
PID 6216
```

This is strong correlation because the same path appeared in:

1.  The stage-2 script memory.
2.  The process command line.
3.  The process tree.
4.  The network activity associated with PID 6216.

------------------------------------------------------------------------

# 21. Step 17 --- Avoiding a wrong answer

One of the most useful mistakes during the investigation happened when
identifying the URL used to download the malicious binary.

The first suspicious URL found in the `updater.exe` memory was:

``` text
http://128[.]199[.]95[.]189:8080/index.jsp
```

It was tempting to submit that as the download URL.

However, that was incorrect.

Why?

Because the strings came from the memory associated with:

``` text
updater.exe PID 6216
```

Those URLs described C2/web requests made by the already-running
malicious binary.

They did **not** prove that the URL was used to download `updater.exe`.

The correct approach was to move one stage backward in the execution
chain:

``` text
wscript.exe PID 4260
```

and inspect its memory.

That revealed the actual download URL:

``` text
https://files[.]boogeymanisback[.]lol/aa2a9c53cbb80416d3b47d85538d9971/update.exe
```

This was one of the most important lessons from the room:

> Always associate an artefact with the process and stage that generated
> it before deciding what it means.

------------------------------------------------------------------------

# 22. Step 18 --- Finding the malicious email attachment path

Another important mistake occurred when determining the full path of the
original malicious email attachment.

A cached executable path appeared in memory:

``` text
C:\Users\<victim>\AppData\Local\Microsoft\Windows\INetCache\IE\7VAV29FC\update[1].exe
```

It was initially tempting to interpret this as the malicious email
attachment.

However, this was actually associated with the downloaded executable.

The question was specifically asking for the path of the original Word
attachment.

Therefore we used Volatility's file scanning capability:

``` bash
vol -f WKSTN-2961.raw windows.filescan | grep -Ei 'Resume_WesleyTaylor|Resume'
```

This returned the cached Outlook attachment:

``` text
\Users\maxine.beck\AppData\Local\Microsoft\Windows\INetCache\Content.Outlook\WQHGZCFI\Resume_WesleyTaylor (002).doc
```

The full lab path was therefore:

``` text
C:\Users\maxine.beck\AppData\Local\Microsoft\Windows\INetCache\Content.Outlook\WQHGZCFI\Resume_WesleyTaylor (002).doc
```

For sanitized documentation, this can be represented as:

``` text
C:\Users\<victim>\AppData\Local\Microsoft\Windows\INetCache\Content.Outlook\WQHGZCFI\Resume_WesleyTaylor (002).doc
```

This was a good demonstration of why `windows.filescan` is useful during
memory forensics: it can locate file objects and paths that may no
longer be obvious from the normal filesystem view.

------------------------------------------------------------------------

# 23. Step 19 --- Investigating persistence

After identifying the C2 process, the investigation moved to
persistence.

The question was essentially asking:

> What command did the attacker use to create a scheduled task that
> maintained access?

A first search was performed across the memory image:

``` bash
strings WKSTN-2961.raw | grep -i schtasks
```

This generated a lot of unrelated strings and noise.

However, among the results were strings indicating:

``` text
SUCCESS: The scheduled task "Updater" has successfully been created.
```

and:

``` text
Schtasks persistence established using listener http stored in HKCU:\Software\Microsoft\Windows\CurrentVersion\debug with Updater daily trigger at 09:00.
```

This confirmed that the attacker had created a scheduled task named:

``` text
Updater
```

with a daily trigger at:

``` text
09:00
```

------------------------------------------------------------------------

# 24. Step 20 --- Confirming process command lines

To connect the persistence investigation back to the malicious
processes, we also checked command-line information:

``` bash
vol -f WKSTN-2961.raw windows.cmdline | grep -Ei -C 5 'updater|schtasks|task|Windows\\Tasks'
```

Relevant results included:

``` text
4260  wscript.exe  wscript.exe C:\ProgramData\update.js
```

and:

``` text
6216  updater.exe  "C:\Windows\Tasks\updater.exe"
```

This confirmed the relationship between the script and executable
stages.

------------------------------------------------------------------------

# 25. Step 21 --- The scheduled task persistence command

The full scheduled task command identified during the investigation was:

``` text
schtasks /Create /F /SC DAILY /ST 09:00 /TN Updater /TR 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NonI -W hidden -c \"IEX ([Text.Encoding]::UNICODE.GetString([Convert]::FromBase64String((gp HKCU:\Software\Microsoft\Windows\CurrentVersion debug).debug)))\"'
```

This command is extremely important to understand rather than simply
memorise.

------------------------------------------------------------------------

# 26. Breaking down the persistence command

## `schtasks`

``` text
schtasks
```

This is the Windows command-line utility used to create and manage
scheduled tasks.

------------------------------------------------------------------------

## `/Create`

``` text
/Create
```

This tells Windows to create a new scheduled task.

------------------------------------------------------------------------

## `/F`

``` text
/F
```

This forces the creation and allows an existing task with the same name
to be overwritten.

------------------------------------------------------------------------

## `/SC DAILY`

``` text
/SC DAILY
```

This sets the schedule frequency to daily.

------------------------------------------------------------------------

## `/ST 09:00`

``` text
/ST 09:00
```

This specifies the start time.

The attacker therefore configured the task to run at:

``` text
09:00
```

every day.

------------------------------------------------------------------------

## `/TN Updater`

``` text
/TN Updater
```

This assigns the task name:

``` text
Updater
```

The name was intentionally generic and could appear less suspicious than
a clearly malicious task name.

------------------------------------------------------------------------

## `/TR`

``` text
/TR
```

This defines the command that the scheduled task executes.

The attacker configured it to launch:

``` text
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
```

------------------------------------------------------------------------

# 27. Understanding the PowerShell persistence payload

The PowerShell command used:

``` text
-NonI
```

to run non-interactively.

It also used:

``` text
-W hidden
```

to hide the PowerShell window.

The important execution component was:

``` text
IEX
```

which stands for `Invoke-Expression`.

The command retrieved a value from:

``` text
HKCU:\Software\Microsoft\Windows\CurrentVersion\debug
```

using:

``` text
gp
```

which is the PowerShell alias for `Get-ItemProperty`.

The relevant part was:

``` text
(gp HKCU:\Software\Microsoft\Windows\CurrentVersion debug).debug
```

The value stored in the registry was Base64 encoded.

The attacker then decoded it:

``` text
[Convert]::FromBase64String(...)
```

The bytes were interpreted as Unicode:

``` text
[Text.Encoding]::UNICODE.GetString(...)
```

Finally, `IEX` executed the resulting PowerShell code.

So the persistence mechanism can be understood as:

``` text
Scheduled Task
      |
      v
Hidden PowerShell
      |
      v
Read HKCU registry value
      |
      v
Extract "debug" value
      |
      v
Base64 decode
      |
      v
Convert bytes to Unicode string
      |
      v
IEX
      |
      v
Execute attacker-controlled PowerShell
```

This is a strong example of layered obfuscation.

------------------------------------------------------------------------

# 28. Important distinction: two different persistence-related commands

During the investigation, another command appeared in the JavaScript
memory:

``` text
cmd.exe /c reg.exe add "HKEY_CURRENT_USERSoftwareMicrosoftWindowsCurrentVersionExplorer User Shell Folders" /v C:\Windows\Tasks /f
```

This should **not** be confused with the scheduled task creation
command.

The JavaScript used Windows registry functionality around the
`Explorer User Shell Folders` area.

The actual scheduled task persistence command was the separate:

``` text
schtasks /Create /F /SC DAILY /ST 09:00 /TN Updater /TR ...
```

This distinction mattered because both commands were related to attacker
activity, but they performed different actions.

------------------------------------------------------------------------

# 29. Reconstructed attack timeline

The investigation allowed the following sequence to be reconstructed.

### Stage 1 --- Phishing

The victim received a job-application-themed email.

The attachment was:

``` text
Resume_WesleyTaylor.doc
```

------------------------------------------------------------------------

### Stage 2 --- Malicious document

The document contained:

``` text
NewMacros.bas
```

with:

``` text
Sub AutoOpen()
```

------------------------------------------------------------------------

### Stage 3 --- Initial payload download

The macro used HTTP-related COM objects to download a payload.

The URL was:

``` text
https://files[.]boogeymanisback[.]lol/aa2a9c53cbb80416d3b47d85538d9971/update[.]png
```

The content was saved as:

``` text
C:\ProgramData\update.js
```

------------------------------------------------------------------------

### Stage 4 --- Script execution

The macro executed:

``` text
wscript.exe C:\ProgramData\update.js
```

Observed process:

``` text
wscript.exe
PID 4260
```

------------------------------------------------------------------------

### Stage 5 --- Executable download

The JavaScript contacted:

``` text
https://files[.]boogeymanisback[.]lol/aa2a9c53cbb80416d3b47d85538d9971/update.exe
```

The response was saved to:

``` text
C:\Windows\Tasks\updater.exe
```

------------------------------------------------------------------------

### Stage 6 --- Malicious binary execution

The script executed:

``` text
C:\Windows\Tasks\updater.exe
```

Observed PID:

``` text
6216
```

------------------------------------------------------------------------

### Stage 7 --- C2

The malicious binary initiated network communication with:

``` text
128[.]199[.]95[.]189:8080
```

------------------------------------------------------------------------

### Stage 8 --- Persistence

The attacker created a scheduled task:

``` text
Updater
```

The task was configured to execute daily at:

``` text
09:00
```

The task launched hidden PowerShell which retrieved an encoded payload
from a registry value and executed it.

------------------------------------------------------------------------

# 30. Key forensic artefacts and what they told us

  ------------------------------------------------------------------------------------------------------------------
  Artefact                         Evidence                                                  What it told us
  -------------------------------- --------------------------------------------------------- -----------------------
  `.eml` phishing email            Job-application-themed message                            Initial access vector

  `.doc` attachment                `Resume_WesleyTaylor.doc`                                 Malicious document
                                                                                             delivery

  VBA macro                        `Sub AutoOpen()`                                          Automatic macro
                                                                                             execution

  `Microsoft.XMLHTTP`              HTTP object                                               Network download
                                                                                             capability

  `Adodb.Stream`                   Stream object                                             Saving downloaded
                                                                                             content

  `update.js`                      `C:\ProgramData\update.js`                                Stage-2 script

  `wscript.exe`                    PID 4260                                                  Script execution
                                                                                             process

  `updater.exe`                    PID 6216                                                  Malicious executable

  `C:\Windows\Tasks\updater.exe`   File path                                                 Location of malicious
                                                                                             binary

  `windows.netscan`                `128[.]199[.]95[.]189:8080`                               C2 endpoint

  UTF-16 memory strings            `update.exe` URL                                          Stage-2 binary download
                                                                                             URL

  `windows.filescan`               Outlook cache path                                        Original email
                                                                                             attachment location

  `schtasks` strings               `Updater` task                                            Persistence

  Registry path                    `HKCU:\Software\Microsoft\Windows\CurrentVersion\debug`   Stored encoded
                                                                                             persistence payload
  ------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 31. Important commands used

## List processes

``` bash
vol -f WKSTN-2961.raw windows.pslist
```

------------------------------------------------------------------------

## Find wscript

``` bash
vol -f WKSTN-2961.raw windows.pslist | grep -i wscript
```

------------------------------------------------------------------------

## View process tree

``` bash
vol -f WKSTN-2961.raw windows.pstree
```

------------------------------------------------------------------------

## Find network connections

``` bash
vol -f WKSTN-2961.raw windows.netscan | grep -E '4260|6216'
```

------------------------------------------------------------------------

## Inspect a specific process

``` bash
vol -f WKSTN-2961.raw windows.pslist --pid 4260
```

------------------------------------------------------------------------

## Dump process memory mappings

``` bash
vol -f WKSTN-2961.raw windows.memmap --pid 4260 --dump
```

------------------------------------------------------------------------

## Save the mapping output

``` bash
vol -f WKSTN-2961.raw windows.memmap --pid 4260 --dump > memmap4260.txt
```

------------------------------------------------------------------------

## Search for recently created files

``` bash
find ~/Desktop/Artefacts -type f -newermt "07:01" -ls
```

------------------------------------------------------------------------

## Search ASCII strings

``` bash
strings -a tmp_urlqmc2x.vol3
```

------------------------------------------------------------------------

## Search for useful malware strings

``` bash
strings -a tmp_urlqmc2x.vol3 | grep -Ei 'ProgramData|update\.js|XMLHTTP|ADODB|ServerXMLHTTP|CreateObject|Run|Shell|SaveToFile'
```

------------------------------------------------------------------------

## Search UTF-16LE strings

``` bash
strings -a -el tmp_urlqmc2x.vol3 | grep -Ei 'http|https|boogeyman|\.exe|\.lol|128\.199'
```

This was one of the most important commands in the investigation.

------------------------------------------------------------------------

## Search for the original attachment

``` bash
vol -f WKSTN-2961.raw windows.filescan | grep -Ei 'Resume_WesleyTaylor|Resume'
```

------------------------------------------------------------------------

## Search for scheduled-task activity

``` bash
strings WKSTN-2961.raw | grep -i schtasks
```

------------------------------------------------------------------------

## Search command-line information

``` bash
vol -f WKSTN-2961.raw windows.cmdline | grep -Ei -C 5 'updater|schtasks|task|Windows\\Tasks'
```

------------------------------------------------------------------------

# 32. Final investigation findings

### Initial access

``` text
Spear-phishing email
```

with a malicious Word attachment.

### Attachment

``` text
Resume_WesleyTaylor.doc
```

### Macro

``` text
NewMacros.bas
Sub AutoOpen()
```

### First-stage download

``` text
https://files[.]boogeymanisback[.]lol/aa2a9c53cbb80416d3b47d85538d9971/update[.]png
```

### First-stage saved file

``` text
C:\ProgramData\update.js
```

### Script execution process

``` text
wscript.exe
PID 4260
```

### Stage-2 binary download

``` text
https://files[.]boogeymanisback[.]lol/aa2a9c53cbb80416d3b47d85538d9971/update.exe
```

### Malicious binary

``` text
C:\Windows\Tasks\updater.exe
```

### Malicious process PID

``` text
6216
```

### C2

``` text
128[.]199[.]95[.]189:8080
```

### Persistence

``` text
Scheduled Task: Updater
Trigger: Daily at 09:00
```

### Persistence command

``` text
schtasks /Create /F /SC DAILY /ST 09:00 /TN Updater /TR 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NonI -W hidden -c \"IEX ([Text.Encoding]::UNICODE.GetString([Convert]::FromBase64String((gp HKCU:\Software\Microsoft\Windows\CurrentVersion debug).debug)))\"'
```

------------------------------------------------------------------------

# 33. What I learned from this room

## 33.1 Phishing analysis is not only about email headers

At first glance, an email can look legitimate.

The real value came from following the attachment into the document and
then into the macro.

The important question is not just:

> Who sent the email?

It is also:

> What does the attachment actually do when opened?

------------------------------------------------------------------------

## 33.2 Office macros can act as malware launchers

The `AutoOpen` macro acted as the bridge between the malicious document
and the next-stage payload.

It did not need to contain the final malware directly.

Instead, it downloaded another payload and executed it.

This is a common concept in multi-stage malware.

------------------------------------------------------------------------

## 33.3 Process trees are extremely valuable

The process tree gave us the relationship:

``` text
WINWORD.EXE
    |
    v
wscript.exe
    |
    v
updater.exe
```

That was much more informative than looking at each process
independently.

------------------------------------------------------------------------

## 33.4 Memory forensics can recover information that is difficult to find elsewhere

The exact stage-2 URL was recovered from the memory of `wscript.exe`.

The memory also exposed:

-   URLs
-   file paths
-   COM objects
-   HTTP request information
-   save operations
-   execution commands
-   persistence-related strings

This demonstrated why memory is valuable during incident response.

------------------------------------------------------------------------

## 33.5 Windows strings are often Unicode

The first `strings` search did not immediately reveal the information we
wanted.

The breakthrough came from:

``` bash
strings -a -el
```

This searches UTF-16LE strings, which are common in Windows processes
and applications.

This is something I should remember for future Windows memory
investigations.

------------------------------------------------------------------------

## 33.6 Context matters more than suspicious strings

The incorrect `index.jsp` answer was a good lesson.

The URL looked suspicious, but it came from the wrong process and wrong
stage.

The correct question was:

> Which process was responsible for downloading the malicious binary?

That led us back to:

``` text
wscript.exe PID 4260
```

and eventually to the correct `update.exe` URL.

------------------------------------------------------------------------

## 33.7 Do not confuse the payload with the delivery mechanism

There were multiple stages:

``` text
Word document
    ↓
VBA
    ↓
JavaScript
    ↓
Executable
    ↓
C2
    ↓
Persistence
```

Each stage had a different purpose.

Understanding this distinction made the investigation much easier.

------------------------------------------------------------------------

## 33.8 Scheduled-task persistence can hide behind legitimate Windows tools

The attacker did not need to install a custom persistence service.

Instead, they used:

``` text
schtasks
```

and:

``` text
PowerShell
```

These are legitimate Windows utilities.

The malicious behaviour came from how they were configured and what
payload they executed.

------------------------------------------------------------------------

# 34. My investigation methodology to reuse in future rooms

When investigating a similar Windows intrusion, I can use this sequence:

``` text
1. Start with the initial artefact.
        |
        v
2. Identify the suspicious file or activity.
        |
        v
3. Determine what executed it.
        |
        v
4. Build the process tree.
        |
        v
5. Identify child processes.
        |
        v
6. Map suspicious processes to network activity.
        |
        v
7. Dump/review relevant process memory.
        |
        v
8. Search ASCII and UTF-16 strings.
        |
        v
9. Identify files, URLs, commands and registry locations.
        |
        v
10. Investigate persistence.
        |
        v
11. Correlate all artefacts into a timeline.
        |
        v
12. Only then answer the investigation question.
```

The most important part is correlation.

I should avoid answering a question simply because I found a suspicious
string. I need to understand **which process, which stage, and which
action** produced the evidence.

------------------------------------------------------------------------

# 35. Lessons from mistakes during the investigation

## Mistake 1 --- Treating the first suspicious URL as the download URL

I initially found:

``` text
http://128[.]199[.]95[.]189:8080/index.jsp
```

and assumed it was the URL used to download the malicious binary.

That was wrong.

It belonged to the C2/web activity of the already-running malicious
binary.

### Correction

Go back to the process that performed the download:

``` text
wscript.exe PID 4260
```

Then inspect its memory.

------------------------------------------------------------------------

## Mistake 2 --- Guessing the Volatility dump filename

I tried to work with a guessed dump filename:

``` text
pid.4260.dmp
```

It did not exist.

### Correction

Check the actual files created by Volatility:

``` bash
find ~/Desktop/Artefacts -type f -newermt "07:01" -ls
```

This revealed the temporary `.vol3` files.

------------------------------------------------------------------------

## Mistake 3 --- Confusing the cached executable with the original email attachment

A cached `update[1].exe` file appeared in the memory evidence.

It was tempting to submit that as the malicious attachment.

### Correction

Search specifically for the original attachment name:

``` bash
vol -f WKSTN-2961.raw windows.filescan | grep -Ei 'Resume_WesleyTaylor|Resume'
```

This recovered the Outlook cache path of the Word document.

------------------------------------------------------------------------

# 36. Practical SOC/DFIR skills demonstrated

This room helped me practise several skills that are relevant to a SOC
analyst or DFIR role.

### Phishing analysis

I analysed:

-   sender information
-   headers
-   attachment
-   document behaviour
-   macro execution

### Malware triage

I identified:

-   malicious script
-   malicious executable
-   process IDs
-   execution paths
-   C2 infrastructure

### Memory forensics

I used:

``` text
windows.pslist
windows.pstree
windows.netscan
windows.memmap
windows.filescan
windows.cmdline
```

### Command-line investigation

I used:

``` text
grep
strings
find
```

and combined them with Volatility output.

### IOC extraction

I extracted:

-   URLs
-   domain
-   IP address
-   port
-   filenames
-   process names
-   file paths
-   registry path
-   scheduled task name

### Persistence analysis

I identified:

-   scheduled task
-   execution time
-   PowerShell
-   registry-based payload storage
-   Base64 decoding
-   hidden execution

------------------------------------------------------------------------

# 37. IOC summary

The following indicators were identified during the investigation.

## Domains

``` text
files[.]boogeymanisback[.]lol
```

## C2 IP

``` text
128[.]199[.]95[.]189
```

## C2 port

``` text
8080
```

## Stage-1 resource

``` text
/aa2a9c53cbb80416d3b47d85538d9971/update[.]png
```

## Stage-2 executable resource

``` text
/aa2a9c53cbb80416d3b47d85538d9971/update.exe
```

## Script

``` text
C:\ProgramData\update.js
```

## Executable

``` text
C:\Windows\Tasks\updater.exe
```

## Processes

``` text
wscript.exe — PID 4260
updater.exe — PID 6216
```

## Scheduled task

``` text
Updater
```

## Registry location

``` text
HKCU:\Software\Microsoft\Windows\CurrentVersion\debug
```

------------------------------------------------------------------------

# 38. Investigation conclusion

The evidence supports a multi-stage phishing compromise.

The attacker delivered a malicious Word document through a
job-application-themed email. The document contained an `AutoOpen` VBA
macro. When executed, the macro downloaded a JavaScript payload and
launched it through Windows Script Host.

The JavaScript then downloaded an executable named `update.exe`, saved
it as:

``` text
C:\Windows\Tasks\updater.exe
```

and executed it.

The resulting process was:

``` text
updater.exe
PID 6216
```

This process established communication with:

``` text
128[.]199[.]95[.]189:8080
```

After establishing the C2 connection, the attacker created a scheduled
task named `Updater`. The task was configured to execute daily at 09:00
and launch hidden PowerShell. The PowerShell code retrieved an encoded
payload from a registry value, decoded it, and executed it.

The overall attack can therefore be summarised as:

``` text
Spear Phishing
      ↓
Malicious Word Attachment
      ↓
VBA AutoOpen
      ↓
Download JavaScript
      ↓
wscript.exe
      ↓
Download update.exe
      ↓
updater.exe
      ↓
C2
      ↓
Scheduled Task Persistence
      ↓
Hidden PowerShell
      ↓
Registry + Base64 Payload
```

------------------------------------------------------------------------

# 39. Final revision checklist

Before considering this investigation fully understood, I should be able
to explain all of these without looking at the notes:

-   [ ] Why the phishing email was suspicious.
-   [ ] What the attachment was called.
-   [ ] Why `AutoOpen` was important.
-   [ ] What `Microsoft.XMLHTTP` was doing.
-   [ ] What `Adodb.Stream` was doing.
-   [ ] Where `update.js` was saved.
-   [ ] Why `wscript.exe` was involved.
-   [ ] How PID 4260 was identified.
-   [ ] How the process tree connected Word, WScript and updater.
-   [ ] How PID 6216 was identified.
-   [ ] How `windows.netscan` linked the process to C2.
-   [ ] Why the first `index.jsp` URL was not the correct download URL.
-   [ ] Why UTF-16 string searching was necessary.
-   [ ] How the `update.exe` URL was recovered.
-   [ ] How `updater.exe` was saved.
-   [ ] How the original Word attachment path was recovered with
    `windows.filescan`.
-   [ ] How scheduled-task persistence was identified.
-   [ ] What `/SC DAILY` means.
-   [ ] What `/ST 09:00` means.
-   [ ] What `/TN Updater` means.
-   [ ] What `/TR` does.
-   [ ] Why `-W hidden` was suspicious.
-   [ ] How the registry value was retrieved.
-   [ ] Why Base64 decoding was used.
-   [ ] What `IEX` does.
-   [ ] How all the artefacts form one timeline.

------------------------------------------------------------------------

# 40. Quick answer sheet

For personal revision after completing the room:

  -------------------------------------------------------------------------------------------------------------------------
  Question / Finding                  Answer
  ----------------------------------- -------------------------------------------------------------------------------------
  Malicious attachment                `Resume_WesleyTaylor.doc`

  Macro                               `NewMacros.bas` / `Sub AutoOpen()`

  Stage-2 script                      `C:\ProgramData\update.js`

  Script process                      `wscript.exe`

  Script PID                          `4260`

  Malicious binary                    `updater.exe`

  Malicious binary path               `C:\Windows\Tasks\updater.exe`

  Malicious binary PID                `6216`

  C2                                  `128[.]199[.]95[.]189:8080`

  Stage-2 executable URL              `https://files[.]boogeymanisback[.]lol/aa2a9c53cbb80416d3b47d85538d9971/update.exe`

  Scheduled task                      `Updater`

  Schedule                            Daily at `09:00`

  Persistence mechanism               Scheduled task + hidden PowerShell

  Registry payload location           `HKCU:\Software\Microsoft\Windows\CurrentVersion\debug`
  -------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 41. Final takeaway

The biggest thing I learned from this room is that **forensic
investigation is about connecting evidence**.

A single string can be misleading.

A single process can look harmless.

A single URL can belong to a different stage of the attack.

But when I connect:

``` text
Email
→ Attachment
→ Macro
→ Script
→ Process
→ Child Process
→ Network Connection
→ File Path
→ Memory Strings
→ Persistence
```

the complete attack story becomes visible.

This is the methodology I want to carry into future SOC and DFIR
investigations.

**Do not just find an IOC. Find the story behind the IOC.**

------------------------------------------------------------------------

## Reference

Official TryHackMe room:

https://tryhackme.com/room/boogeyman2

This document is my own investigation and learning record based on the
authorised TryHackMe lab work performed on **2026-10-07**.
