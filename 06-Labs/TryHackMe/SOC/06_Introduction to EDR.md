# TryHackMe — Introduction to EDR

**Date:** September 4, 2026  
**Room:** Introduction to EDR  
**Focus:** Endpoint Detection and Response (EDR), visibility, detection, telemetry, agents, and response capabilities.

## Task 2 — What is an EDR?

EDR is a security solution that continuously monitors endpoints, detects suspicious or malicious activity, and provides response capabilities.

### Three pillars of EDR

1. **Visibility** — detailed endpoint activity and full detection context.
2. **Detection** — signature, behaviour, anomaly, IOC, MITRE ATT&CK, and ML-based detection.
3. **Response** — isolate hosts, terminate processes, quarantine files, remotely access hosts, and collect artefacts.

### Visibility

EDR can collect:

- Process modifications
- Registry modifications
- File/folder modifications
- User actions
- Network activity
- Process relationships
- Historical endpoint activity

A **process tree** shows parent-child relationships between processes and helps reconstruct what happened.

### Task 2 answers

**Which feature provides complete context for detections?**
```text
Visibility
```

**Which process spawned sc.exe?**
```text
cmd.exe
```

---

## Task 3 — Beyond the Antivirus

Traditional antivirus mainly relies on known signatures and basic endpoint protection. EDR continuously records endpoint behaviour and provides much richer context.

### Attack chain from the room

```text
Phishing Email
      ↓
Malicious Word Document
      ↓
WINWORD.EXE
      ↓
PowerShell
      ↓
Obfuscated PowerShell
      ↓
Second-stage Payload
      ↓
Process Injection into svchost.exe
      ↓
Remote Access
```

A suspicious parent-child relationship such as:

```text
WINWORD.EXE
      ↓
PowerShell.exe
```

can be detected by EDR because the behaviour is unusual.

### Task 3 answers

**What represents AV in the analogy?**
```text
Immigration check
```

**Which legitimate process was hijacked?**
```text
svchost.exe
```

**Which solution might mark the activity as clean?**
```text
antivirus
```

---

## Task 4 — How an EDR Works

The basic architecture is:

```text
Endpoint
   ↓
EDR Agent / Sensor
   ↓
EDR Console
   ↓
SOC Analyst
```

### EDR Agent

The agent is installed on the endpoint and acts as the **eyes and ears** of the EDR.

It collects endpoint activity and sends telemetry to the central console in real time.

An EDR agent is also known as a:

```text
Sensor
```

### EDR Console

The console is the central place where endpoint data is correlated and analysed using detection logic, machine learning, and threat intelligence.

After a detection, the SOC analyst can:

1. Acknowledge and prioritize the alert.
2. Review the detection details.
3. Decide whether it is a False Positive or True Positive.
4. Take response actions if necessary.

### Task 4 answers

**Which component collects endpoint telemetry?**
```text
agent
```

**An EDR agent is also known as a?**
```text
sensor
```

---

## Task 5 — EDR Telemetry

Telemetry is the data collected by the EDR agent from an endpoint. I think of it as the endpoint's **black box** because it contains the information needed to understand what happened.

### Main telemetry types

#### 1. Process executions and terminations

Useful for finding:

- Suspicious parent-child relationships
- Suspicious executables
- Malware payloads
- Unusual process chains

#### 2. Network connections

Useful for detecting:

- C2 communications
- Unusual port usage
- Data exfiltration
- Lateral movement

#### 3. Command line activity

EDR records commands executed through CMD, PowerShell, etc.

This can reveal:

- Malicious commands
- Obfuscated PowerShell
- Download commands
- Suspicious scripts

#### 4. File and folder modifications

Useful for detecting:

- Malware dropping files
- Data staging
- Ransomware activity
- Suspicious file creation

#### 5. Registry modifications

The Windows Registry stores important system configuration information. Registry changes can reveal malicious activity such as persistence.

### Task 5 answers

**Which telemetry helps detect C2 communications?**
```text
Network Connections
```

**Where are Windows configuration settings primarily stored?**
```text
registry
```

---

## Task 6 — Detection and Response Capabilities

### Detection techniques

#### Behavioural Detection

Looks at what a process does instead of only checking its signature.

Example:

```text
WINWORD.EXE
      ↓
PowerShell.exe
```

#### Anomaly Detection

Compares activity with the normal baseline of an endpoint and flags unusual deviations.

#### IOC Matching

Compares endpoint activity with known Indicators of Compromise such as hashes, IP addresses, and domains.

Example:

```text
Executable
   ↓
Hash
   ↓
Threat Intelligence
   ↓
Known IOC
   ↓
Detection
```

#### MITRE ATT&CK Mapping

Maps suspicious activity to tactics and techniques.

Example:

```text
Scheduled Task
     ↓
Persistence
     ↓
Scheduled Task/Job
```

#### Machine Learning

ML can identify complex patterns across multiple events and can help detect fileless and multi-stage attacks.

---

## Response capabilities

### Isolate Host

Disconnects a compromised endpoint from the network to help prevent lateral movement and further communication.

### Terminate Process

Stops a malicious process. This should be done carefully because terminating a legitimate process can disrupt business operations.

### Quarantine

Moves a malicious file to an isolated location so it cannot execute.

### Remote Access

Allows analysts to access the endpoint remotely, run commands/scripts, and collect information.

### Artefact Collection

Useful forensic artefacts include:

- Memory dumps
- Event logs
- Specific folder contents
- Registry hives

### Task 6 answer recorded

**Which feature helps identify threats based on known malicious behaviours?**
```text
IOC matching
```

**Important distinction:** IOC matching is specifically about matching known indicators, while behavioural detection focuses on suspicious behaviour patterns. I recorded the room answer above as provided in the notes.

---

# EDR Investigation Examples From the Lab

One screenshot showed a process chain:

```text
WINWORD.EXE
      ↓
CMD.EXE
      ↓
cURL.EXE
      ↓
INSTALL.EXE
```

The document was:

```text
invoice.docm
```

The EDR displayed useful investigation information such as:

- Process path
- Command line
- PID
- Parent process
- User
- SHA256 hash
- Start/end time
- Threat intent
- Behaviour

Another detection showed:

```text
UpdateAgent.exe
```

with a path under:

```text
C:\Users\daniel.richards\AppData\Roaming\UpdateAgent.exe
```

Important observations included that it was unsigned, launched by `explorer.exe`, and initiated an outbound HTTP connection to `10.10.20.5` on port `8080`.

This shows how a SOC analyst can combine:

```text
Process Information
        +
Network Activity
        +
Threat Intelligence
        +
File Information
        =
Better Investigation
```

---

# EDR vs Antivirus — Quick Comparison

| Antivirus | EDR |
|---|---|
| Mainly known threats/signatures | Behaviour + signatures + anomaly + IOC + ML |
| Limited endpoint context | Detailed endpoint telemetry |
| May miss new/obfuscated activity | Can detect suspicious behaviour |
| Limited attack-chain visibility | Process trees and event timelines |
| Basic response | Host isolation, process termination, quarantine, remote response |
| Mostly prevention/detection | Detection + investigation + response |

---

# The SOC Analyst View

The most important thing I learned is that EDR is not just "another antivirus".

The main advantage is **visibility and context**.

Instead of only asking:

```text
"Is this file malicious?"
```

EDR helps answer:

```text
What happened?
Which process started it?
What command was executed?
What files changed?
What registry changes happened?
Where did the endpoint connect?
What happened before and after the detection?
How can I contain it?
```

That context is what makes EDR extremely useful during SOC investigations.

---

# Quick Revision Cheat Sheet

| Concept | Remember |
|---|---|
| EDR | Endpoint Detection and Response |
| Three pillars | Visibility, Detection, Response |
| Agent | Collects endpoint telemetry |
| Sensor | Another name for the EDR agent |
| Console | Central analysis/detection point |
| Telemetry | Data collected from endpoints |
| Process tree | Shows parent-child process relationships |
| Network telemetry | Useful for detecting C2 |
| Registry | Stores Windows configuration |
| Behavioural detection | Detects suspicious behaviour |
| Anomaly detection | Detects deviations from normal |
| IOC matching | Matches known malicious indicators |
| MITRE ATT&CK | Maps activity to tactics/techniques |
| ML | Detects complex patterns |
| Host isolation | Separates compromised host from network |
| Terminate process | Stops a process |
| Quarantine | Isolates a malicious file |
| Remote access | Lets analyst interact with endpoint |
| Artefact collection | Collects forensic evidence |

---

# Attack Chain to Remember

```text
Phishing
   ↓
Malicious Document
   ↓
WINWORD.EXE
   ↓
PowerShell / CMD
   ↓
Payload Download
   ↓
Process Injection
   ↓
C2 / Remote Access
```

The key idea is that EDR tries to see the **whole chain**, not just one suspicious file.

---

# Final Answers

```text
Task 2:
Visibility
cmd.exe

Task 3:
immigration check
svchost.exe
antivirus

Task 4:
agent
sensor

Task 5:
Network Connections
registry

Task 6:
IOC matching
```

