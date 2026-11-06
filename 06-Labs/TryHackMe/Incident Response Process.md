# Incident Response Process --- Walkthrough Notes

**Study date:** 6 November 2026\
**Topic:** Incident Response Lifecycle\
**Source:** TryHackMe --- Incident Response Process (Tasks 2--5)

------------------------------------------------------------------------

## 1. What is Incident Response?

Incident Response (IR) is the set of processes and technologies an
organisation uses to detect, investigate, contain, and recover from
cyber threats, security breaches, or attacks.

An organisation should maintain a documented **Incident Response Plan
(IRP)** describing how teams identify incidents, limit their impact,
remove threats, restore systems, and learn from what happened.

The lesson introduces two frameworks:

-   **NIST Incident Response Framework:** four broad phases.
-   **SANS Incident Response 101:** six phases, because it separates
    containment, eradication, and recovery.

### NIST's four phases

1.  **Preparation** --- establish and maintain the ability to respond.
2.  **Detection and Analysis** --- identify an incident and understand
    its scope and impact.
3.  **Containment, Eradication, and Recovery** --- limit damage, remove
    the threat, and restore operations.
4.  **Post-Incident Activity** --- review the incident, document
    lessons, and improve the response process.

### SANS six-step model

1.  Preparation
2.  Identification
3.  Containment
4.  Eradication
5.  Recovery
6.  Lessons learned

Both models describe similar work at different levels of detail. NIST
groups three operational activities into one phase; SANS lists them
separately.

## 2. Incident Response Is a Continuous Lifecycle

Incident response is not a checklist that ends when a machine is
cleaned. It is a repeating cycle.

For example, an incident involving a malicious Office macro may reveal
gaps in endpoint detection, web filtering, or employee awareness. The
organisation should use those findings to improve its preparation and
response plan.

Post-incident activity must feed information back into preparation. Each
incident should make the organisation better prepared for the next one.

## 3. The Incident Responder's Mindset

An incident responder may be called after a SIEM, EDR, firewall, IT
team, or user has raised an alert. The responder may therefore enter the
lifecycle during Detection and Analysis rather than at the beginning.

During an incident, urgency can make responders focus only on stopping
the immediate threat. The lesson emphasises two goals:

1.  **Eradicate the current threat** and limit its impact.
2.  **Prevent the same threat from affecting the organisation again.**

Documentation supports both goals. Record actions and evidence before
deleting files, stopping processes, or changing system settings.

Useful details include file names and paths, process names and PIDs,
user accounts, IP addresses and ports, URLs, file hashes, registry
locations and values, timestamps, and actions taken.

Do not destroy useful evidence simply to make the machine look clean.

------------------------------------------------------------------------

## 4. Scenario: A Slow Windows Workstation

A user's Windows laptop became extremely slow. Restarting did not solve
the problem.

The IT team found unusually high CPU usage even after the user closed
applications. The SOC team checked its monitoring systems:

-   No SIEM or EDR alert had been raised for the workstation.
-   The perimeter firewall showed outbound connections from the
    workstation.
-   The connections occurred every second and repeatedly targeted the
    same destination IP.
-   The user did not recognise the connection attempts.

The SOC escalated the case to the Incident Response Team (IRT).

The lab states that pre-response steps had already been completed:
backups were created to preserve evidence, and the machine was detached
from the organisational network to reduce the risk of further spread.

**Important:** No SIEM or EDR alert does not prove that a machine is
clean. The user report, high CPU usage, and unusual network traffic were
enough to justify investigation.

## 5. Detection and Analysis

### 5.1 Detection

Detection relies on preparation. Monitoring and detection systems can
include:

-   **SIEM:** collects and correlates logs to identify suspicious
    activity.
-   **IDS:** monitors network or system activity for signs of malicious
    behaviour.
-   **EDR:** monitors endpoint activity and supports investigation and
    response.

Policies and procedures must ensure that alerts and suspicious reports
reach the correct teams.

In this scenario, the user reported an anomaly to IT. IT recognised that
it could be security-related and escalated it to the SOC. Human
reporting contributed to detection even though automated tools had not
generated an alert.

### 5.2 Inspect running processes with Task Manager

The responder opens Windows Task Manager and selects **More details** to
view background processes and resource usage.

The lesson's example identifies a suspicious process:

-   Process: `3d33es454e.exe`
-   Location: `C:\Users\IRUser\AppData\Local\Temp`
-   User: `IRUser`
-   Example PID shown in the lesson: `6872`

The process consumes an unusually large amount of CPU even though no
normal application appears to be doing so.

Why is this suspicious?

-   The process name looks random rather than like a recognisable
    application.
-   It is using substantial CPU resources.
-   It is running from a user's temporary directory.

A process running from a Temp folder is not automatically malware, and a
strange name alone is not proof. Together, however, these observations
justify further investigation.

### 5.3 Check the process's network connections

Obtain the process ID (PID):

1.  In Task Manager, right-click the suspicious process.
2.  Select **Go to details**.
3.  Record the PID.

Open Command Prompt and run the following, replacing the example PID
with the PID from the machine:

``` cmd
netstat -aofn | find "6872"
```

What the switches mean:

-   `-a` --- show listening ports and active connections.
-   `-o` --- include the owning process ID (PID).
-   `-f` --- show fully qualified domain names for foreign addresses
    where available.
-   `-n` --- show addresses and port numbers numerically.
-   `find "6872"` --- filter the output for the selected PID.

The lesson's example output is:

``` text
TCP    10.10.17.57:49793      1.2.3.4:23123          SYN_SENT        6872
```

  -----------------------------------------------------------------------
  Field                               Meaning
  ----------------------------------- -----------------------------------
  `TCP`                               The connection uses TCP

  `10.10.17.57:49793`                 Local workstation IP and local port

  `1.2.3.4:23123`                     Remote destination IP and port

  `SYN_SENT`                          The workstation sent a TCP
                                      connection request and is waiting
                                      for a response

  `6872`                              PID associated with the connection
  -----------------------------------------------------------------------

The repeated outbound connection to an unusual destination is another
suspicious indicator. In the scenario, the destination IP and port are
treated as a possible connection to a **Command and Control (C2)**
server.

A C2 server is infrastructure an attacker uses to communicate with
compromised systems, send instructions, or receive information.

### 5.4 Record and use the IoC

An **Indicator of Compromise (IoC)** is an observable clue that may
indicate malicious activity.

The IP address and port are useful IoCs. The response team can:

1.  Block the destination IP at the organisation's perimeter firewall,
    following the organisation's response procedure.
2.  Search network traffic logs for other connections to the same IP.
3.  Create SIEM detections for future attempts to contact the
    destination.
4.  Use appropriate EDR controls to detect or block related activity.

An IoC is useful beyond the single infected endpoint: searching across
the organisation may reveal other affected machines.

The lesson assumes further malware analysis confirms that the executable
is a **cryptocurrency miner**. A miner can consume substantial CPU
resources to perform cryptocurrency-related calculations, explaining the
workstation's poor performance.

## 6. Identify the Infection Vector

After confirming an incident, responders need to identify how the
attacker initially gained access. This is the **initial access vector**
or infection vector.

Examples in the lesson include:

-   Exploiting vulnerabilities in internet-facing systems
-   Phishing and social engineering
-   Credential stuffing and brute-force attacks
-   Drive-by downloads
-   Supply-chain attacks

For a workstation, user activity can be relevant. A user may click a
phishing link, open a malicious attachment, or visit a compromised
website.

### 6.1 Inspect browser download history

The user was browsing the web and working on documents shortly before
the computer became slow.

The responder checks Microsoft Edge's download history by opening:

``` text
edge://downloads/all
```

The lesson's example shows:

``` text
invoice n. 37484567 (1).docm
```

Downloaded from:

``` text
http://172.234.25.65
```

Why is this suspicious?

-   The file name resembles an invoice, which may encourage a user to
    open it.
-   The download source is an IP address rather than a recognisable
    domain.
-   The `.docm` extension identifies a macro-enabled Microsoft Word
    document.

A `.docm` file can contain VBA macros. Macros can automate legitimate
tasks, but an attacker can abuse them to run commands or download
malware.

### 6.2 Inspect the Word document and its macro

The document's visible text asks the user to visit a page to retrieve an
invoice. The lesson notes that the page does not exist in the expected
way and that Word does not show the usual macro warning.

The responder opens **View → Macros**, finds a macro named:

``` text
AutoOpen
```

The macro is opened in the VBA editor for inspection.

`AutoOpen` is important because it is designed to run automatically when
the document is opened. This can make malicious activity happen without
the user explicitly choosing to run a macro.

### 6.3 Understand what the VBA macro does

The lesson explains the macro's behaviour in stages:

1.  **Automatic execution:** `AutoOpen` runs when the document is
    opened.
2.  **Process check:** the macro checks whether a process with the
    malware's name is already running. If it finds one, it stops,
    avoiding another download and execution.
3.  **Set the download URL:** a variable named `strURL` receives the URL
    from which the malware will be downloaded.
4.  **Set the destination path:** `strFilePath` is built using the
    system's temporary directory and the malware filename.
5.  **Download with Certutil:** the macro constructs a command that uses
    the Windows `certutil` utility to download the executable.
6.  **Run invisibly:** the command is launched in a hidden window. The
    macro waits ten seconds and then launches the downloaded executable
    in a hidden window.
7.  **Establish persistence:** the macro creates a value under the
    current user's Windows Run registry key so the executable starts
    again when the user logs in.

### 6.4 Why use Certutil?

`certutil` is a legitimate Windows command-line utility used for
certificate-related administration. The lesson shows that it can also be
abused to download a file.

This is an example of **living off the land**: an attacker uses a tool
already present on the system instead of necessarily dropping a separate
downloader. A legitimate utility can be abused for malicious purposes,
so responders must consider the command's context and behaviour rather
than assuming a built-in tool is always safe.

### 6.5 Understand the persistence mechanism

The macro adds the malware to this registry location:

``` text
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

The full Registry Editor path shown in the lesson is:

``` text
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

-   `HKCU` means **HKEY_CURRENT_USER**.
-   The `Run` key contains entries for programs that should start
    automatically when that user logs in.
-   Malware can abuse this location to survive a reboot and run again at
    the next login.

This explains why restarting the laptop did not solve the problem: the
malware had a persistence mechanism that caused it to start again.

### 6.6 Reconstruct the attack chain

The evidence supports this sequence:

1.  The user downloads a suspicious macro-enabled Word document.
2.  The user opens the document.
3.  Its `AutoOpen` macro runs.
4.  The macro checks whether the miner process is already running.
5.  It uses `certutil` to download the executable into the user's Temp
    directory.
6.  It launches the executable in a hidden window.
7.  It adds a value to the user's Run registry key.
8.  The miner consumes CPU resources and attempts to contact its C2
    destination.
9.  After a reboot, the Run key launches the miner again.

This is the incident's likely infection chain as described by the lab.

------------------------------------------------------------------------

## 7. Containment

Containment aims to limit the incident's impact and stop the threat from
spreading or continuing its activity.

The lab's pre-response work already included detaching the workstation
from the organisational network. This reduces the chance of the
compromised machine communicating with other internal systems.

The lesson then describes stopping the malicious process through Task
Manager:

1.  Open Task Manager.
2.  Locate the suspicious process.
3.  Right-click it.
4.  Select **End task**.

**Evidence-first reminder:** Before stopping the process or deleting
files, record relevant details such as the process name, PID, file path,
timestamps, and collected indicators. In a real incident, follow the
organisation's evidence-preservation and forensic procedures.

### 7.1 Contain beyond one endpoint

Responders must not focus only on the known infected workstation. Use
the collected IoCs to search across the organisation.

The scenario's IoCs include:

-   C2 server IP address and destination port
-   URL used to download the macro-enabled Word document
-   URL embedded in the macro that downloaded the malware
-   Hash of the malware executable

Search relevant SIEM, EDR, firewall, and network telemetry for these
indicators. This can identify other infected endpoints or attempted
infections.

The organisation can also add suitable detections or blocks so the same
infrastructure is recognised if it appears again.

## 8. Eradication and Recovery

These activities are related but have different purposes:

-   **Eradication:** remove the malicious files, persistence mechanisms,
    and other components of the threat.
-   **Recovery:** restore the affected system to a trusted working state
    and confirm that it is safe to return to service.

The lab describes the following cleanup actions.

### 8.1 Remove the malware and malicious document

After preserving the evidence and recording the artefacts:

-   Delete the malware executable from the temporary folder where it was
    running.
-   Delete the macro-enabled Word document from the Downloads folder.
-   Clear the browser download history to reduce the chance of the user
    accidentally using the same download link again.

The lesson presents these as actions for its lab scenario. In a real
organisation, follow approved forensic, evidence-retention, and recovery
procedures before removing artefacts or clearing history.

### 8.2 Remove the persistence entry

Open Registry Editor by searching for `regedit`.

Navigate to:

``` text
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

The lesson's example shows a value named `MyApp` pointing to:

``` text
C:\Users\IRUser\AppData\Local\Temp\3d33es454e.exe
```

The responder identifies the value associated with the malware and
deletes that value.

**Be careful:** Do not delete the entire `Run` key. It may contain
legitimate startup applications. Only remove the confirmed malicious
value, after recording it and following the organisation's procedures.

### 8.3 Verify the system before returning it to service

The lesson says that, assuming malware analysis did not identify other
persistence mechanisms or dropped artefacts, these actions restore the
machine to a clean state.

The important condition is "assuming there are no other artefacts."
Removing one executable and one Run entry is not proof that every threat
component has been removed. A real recovery process should verify that
the known IoCs and persistence mechanisms are gone, check for additional
affected systems, and confirm the endpoint is safe before reconnecting
it.

## 9. Post-Incident Activity --- Closing the Cycle

Post-incident activity is where the organisation reviews the incident
and improves its future response capability.

The team should:

-   Document what happened and the incident timeline.
-   Record how the incident was detected and investigated.
-   Preserve the IoCs and relevant evidence.
-   Record containment, eradication, and recovery actions.
-   Identify what worked and what failed.
-   Document lessons learned.
-   Update the Incident Response Plan.

The aim is not simply to close the ticket. It is to reduce the chance
and impact of a similar incident in the future.

### 9.1 Improvements suggested by the lab

For this crypto-miner and malicious-macro incident, the lesson suggests:

1.  **Implement EDR:** use endpoint detection and response capable of
    detecting relevant behaviour, including crypto miners and malicious
    macros.
2.  **Improve web-browsing controls:** prevent or restrict access to
    unsafe websites.
3.  **Provide employee awareness training:** educate employees about
    macro-enabled Office documents and suspicious links.
4.  **Consider a macro execution policy:** discuss blocking macros as a
    countermeasure, while checking that the policy will not disrupt
    legitimate business operations.

These are preparation improvements based on what the incident revealed.

## 10. Important Terms to Remember

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  IR                                  Incident Response: processes and
                                      technologies used to handle
                                      security incidents

  IRP                                 Incident Response Plan: the
                                      documented plan for responding to
                                      incidents

  IRT                                 Incident Response Team: the team
                                      responsible for investigating and
                                      responding

  SOC                                 Security Operations Center:
                                      monitors and investigates security
                                      events

  SIEM                                Collects and correlates logs to
                                      help identify suspicious activity

  IDS                                 Detects suspicious activity in
                                      network or system traffic

  EDR                                 Monitors endpoint activity and
                                      supports endpoint investigation and
                                      response

  IoC                                 Indicator of Compromise: an
                                      observable clue associated with
                                      possible malicious activity

  C2                                  Command and Control: attacker
                                      infrastructure used to communicate
                                      with compromised systems

  PID                                 Process ID: the identifier assigned
                                      to a running process

  VBA                                 Visual Basic for Applications, used
                                      for Office macros

  `certutil`                          A legitimate Windows certificate
                                      utility that can be abused to
                                      download files

  `.docm`                             A macro-enabled Word document
                                      format

  `AutoOpen`                          A Word macro name that can cause
                                      code to run when a document is
                                      opened

  Registry Run key                    A Windows registry location used to
                                      configure programs to run at user
                                      logon

  Persistence                         A technique that allows malicious
                                      activity to continue after events
                                      such as a reboot or login
  -----------------------------------------------------------------------

## 11. Commands and Locations --- Quick Revision

### Check connections for a process

``` cmd
netstat -aofn | find "PID"
```

Replace `PID` with the process ID you recorded.

### Open Edge download history

``` text
edge://downloads/all
```

### Registry persistence location

``` text
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

### Example malware location from the lesson

``` text
C:\Users\IRUser\AppData\Local\Temp
```

### Example registry value target from the lesson

``` text
C:\Users\IRUser\AppData\Local\Temp\3d33es454e.exe
```

These filenames, IP addresses, ports, and paths are examples from the
lesson. The actual lab VM may use different artefacts.

## 12. Quick Revision Questions

**1. What are the four NIST incident response phases?**\
Preparation; Detection and Analysis; Containment, Eradication, and
Recovery; Post-Incident Activity.

**2. How many steps are in the SANS model described in this lesson?**\
Six: Preparation, Identification, Containment, Eradication, Recovery,
and Lessons Learned.

**3. Why is incident response a continuous lifecycle?**\
Because lessons from one incident must improve preparation and response
for future incidents.

**4. Why was the suspicious process investigated?**\
It consumed unusually high CPU resources, had an unusual name, and ran
from a temporary directory.

**5. What does the `-o` option in `netstat -aofn` show?**\
The PID associated with a connection.

**6. What does `SYN_SENT` mean in the example?**\
The host has sent a TCP connection request and is waiting for a
response.

**7. What is an IoC?**\
An observable indicator that may help identify a compromised system or
malicious activity.

**8. Why was the `.docm` file suspicious?**\
It was a macro-enabled Word document downloaded from a suspicious
IP-based URL.

**9. What does `AutoOpen` do in this scenario?**\
It runs automatically when the Word document is opened.

**10. Why was `certutil` relevant?**\
The macro abused this legitimate Windows utility to download the
malware.

**11. How did the malware maintain persistence?**\
It created a value under the current user's `Run` registry key so the
executable would launch at logon.

**12. Why did restarting the workstation not fix the issue?**\
The Run registry entry caused the malware to start again when the user
logged in.

**13. What is the difference between containment and eradication?**\
Containment limits the threat's impact; eradication removes the threat
and its components.

**14. Why search the organisation for the collected IoCs?**\
Other endpoints may have been exposed to the same malware or attacker
infrastructure.

**15. What is the purpose of post-incident activity?**\
To document lessons and improve the organisation's incident response
capability and security posture.

## 13. My Key Takeaways

Today I learned that incident response is a continuous process, not just
an emergency action to stop malware. The NIST model groups the work into
four phases, while the SANS model separates containment, eradication,
and recovery into individual steps.

I followed how an apparently simple performance complaint can become a
security incident. High CPU usage led to process investigation. The
suspicious executable's temporary-folder location and its outbound
connection provided further evidence. The browser history then revealed
a suspicious macro-enabled Word document.

The most important part of the investigation was reconstructing the
infection chain: the document's `AutoOpen` macro used `certutil` to
download a miner, executed it in a hidden window, and added it to the
user's Run registry key for persistence.

I also learned that responders must preserve and document evidence
before stopping processes or deleting artefacts. Containment must
consider the whole organisation, not only the first infected endpoint.
Finally, post-incident lessons should improve preparation through better
EDR coverage, web controls, user awareness, and carefully considered
macro policies.

