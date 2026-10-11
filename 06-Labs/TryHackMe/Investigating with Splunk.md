# TryHackMe — Investigating with Splunk

**Date:** 2026-10-08  
**Platform:** TryHackMe  
**Focus:** Splunk-based Windows log investigation / SOC analysis

> **Sanitized study notes:** This write-up records the investigation workflow, reasoning, Splunk queries, findings, and lessons learned. Sensitive lab-specific details such as live lab access information are intentionally omitted. The indicators and answers below are retained because they are necessary to reproduce the learning outcome.

---

## 1. Room Objective

The scenario involved a SOC analyst investigating anomalous activity on several Windows machines. The logs had already been ingested into Splunk under the `main` index.

The objective was to examine the Windows telemetry, identify the adversary's activity, understand how the backdoor account was created, determine the affected hosts, investigate PowerShell activity, and recover the URL contacted by an encoded PowerShell script.

---

## 2. Initial Event Count

The first question asked how many events were collected and ingested into the `main` index.

### Query

```spl
index=main | stats count
```

### Result

**12,256 events**

This was an important first step because it confirmed that the expected dataset was available in Splunk.

---

## 3. Finding the Backdoor User

The scenario stated that an adversary had successfully created a backdoor user.

Windows account creation events can be investigated using **Event ID 4720**, which represents a user account being created.

### Useful query

```spl
index=main EventID=4720
```

The relevant event showed that the newly created account was:

```text
A1berto
```

The name is important because it visually resembles the legitimate account **Alberto**. The attacker used the digit `1` in `A1berto`, making the malicious account easy to confuse with the legitimate username.

### Finding

**Backdoor username: `A1berto`**

---

## 4. Registry Activity Associated With the Backdoor

The next task asked for the registry key associated with the newly created account.

The investigation showed Sysmon registry activity involving `A1berto`.

A useful search was:

```spl
index=main A1berto (EventID=12 OR EventID=13)
| table EventID TargetObject
```

The relevant registry path was:

```text
HKLM\SAM\SAM\Domains\Account\Users\Names\A1berto
```

Event ID 12 represented registry key creation/deletion activity, while Event ID 13 represented a registry value being set.

### Finding

**Registry key: `HKLM\SAM\SAM\Domains\Account\Users\Names\A1berto`**

The important lesson here was to inspect the `TargetObject` field for Sysmon registry events because it identifies the registry object involved.

---

## 5. Identifying the User Being Impersonated

The attacker did not choose a completely random username. The malicious account was designed to resemble a legitimate account.

The malicious username was:

```text
A1berto
```

The legitimate username it was attempting to imitate was:

```text
Alberto
```

This is a useful example of a **look-alike account / homoglyph-style deception technique**. A human analyst scanning account names could easily overlook the difference between the digit `1` and the lowercase letter `l`.

### Finding

**Impersonated user: `Alberto`**

---

## 6. Understanding the Remote Backdoor-Creation Command

The investigation then moved from account creation to the method used to create the account remotely.

The relevant activity involved **WMIC**, which was used to execute a process on another Windows host.

The command observed in the logs was:

```text
C:\Windows\System32\Wbem\WMIC.exe /node:WORKSTATION6 process call create "net user /add A1berto paw0rd1"
```

The important pieces are:

- `WMIC.exe` — Windows Management Instrumentation command-line utility.
- `/node:WORKSTATION6` — specifies the remote computer.
- `process call create` — requests creation of a process on the remote system.
- `net user /add` — creates a Windows user.
- `A1berto` — the malicious account name.
- The following value was the password supplied to the new account.

### Finding

The attacker remotely executed a `net user /add` command through WMIC to create the backdoor account.

---

## 7. Investigating Login Attempts From the Backdoor

The next question asked how many times a login attempt from `A1berto` was observed.

Successful and failed Windows logons are commonly represented by:

- **4624** — successful logon
- **4625** — failed logon

A useful investigation query was:

```spl
index=main EventID=4624 OR EventID=4625 A1berto
```

No matching login events were observed.

### Finding

**Observed login attempts: `0`**

This was an important distinction: the account was created, but the logs did not show the backdoor account actually being used for a login.

---

## 8. Identifying the Infected Host With Suspicious PowerShell

The investigation then shifted to PowerShell activity.

A broad search for the relevant PowerShell events was useful:

```spl
index=main EventID=4103 OR EventID=4104
```

The suspicious PowerShell activity was associated with the host:

```text
James.browne
```

One of the important lessons from this investigation was not to blindly rely on Splunk's built-in `host` field. In this dataset, the Splunk host field could represent the log-forwarding/source system rather than the actual Windows computer. The actual machine name was available in the event's `Hostname` field.

### Finding

**Infected host: `James.browne`**

---

## 9. PowerShell Logging and Event Count

The room asked how many events were logged for the malicious PowerShell execution.

The relevant PowerShell logging event was **Event ID 4103**.

### Query

```spl
index=main EventID=4103
| stats count
```

### Result

**79 events**

This was one of the places where the exact field and event ID mattered. Earlier searches using `EventCode` or a hostname filter did not give the correct result because this dataset uses `EventID`, and some relevant events did not contain the expected hostname field.

### Finding

**Malicious PowerShell events: `79`**

---

## 10. Investigating the Encoded PowerShell Command

The final investigation question involved an encoded PowerShell script that initiated a web request.

The PowerShell activity could be narrowed with:

```spl
index=main EventID=4103 OR EventID=4104
```

The `ContextInfo` field contained the PowerShell host application information.

A useful extraction query was:

```spl
index=main EventID=4103 OR EventID=4104
| rex field=ContextInfo "Host Application = (?<Command>[^\r\n]+)"
| table Command
| dedup Command
```

This exposed an encoded PowerShell command.

The command contained Base64-encoded content. The investigation required decoding the PowerShell payload, taking into account that PowerShell encoded commands are commonly represented using UTF-16LE after Base64 encoding.

After decoding the relevant Base64 content, the script revealed a web request.

The decoded host portion was:

```text
hxxp[://]10[.]10[.]10[.]5
```

The script then referenced:

```text
/news.php
```

Combining those components produced the full defanged URL:

```text
hxxp[://]10[.]10[.]10[.]5/news[.]php
```

### Finding

**Full URL: `hxxp[://]10[.]10[.]10[.]5/news[.]php`**

The URL is intentionally defanged in these notes so that it cannot be accidentally opened.

---

# 11. Investigation Timeline

The investigation can be reconstructed at a high level as follows:

1. The Windows logs were ingested into Splunk's `main` index.
2. The dataset contained **12,256 events**.
3. A suspicious account named **`A1berto`** was created.
4. The account name closely resembled the legitimate user **`Alberto`**.
5. Registry activity was recorded for the account under the Windows SAM registry area.
6. The account was remotely created through WMIC.
7. The remote command used `net user /add` to create the account.
8. No login attempts by `A1berto` were observed.
9. Suspicious PowerShell activity was identified on **`James.browne`**.
10. **79** malicious PowerShell logging events were observed.
11. An encoded PowerShell command was extracted from the PowerShell telemetry.
12. Decoding the payload revealed a web request to **`hxxp[://]10[.]10[.]10[.]5/news[.]php`**.

---

# 12. Final Answers

| Question | Finding |
|---|---|
| Total events in `main` | **12,256** |
| Backdoor username | **A1berto** |
| Registry key | **HKLM\SAM\SAM\Domains\Account\Users\Names\A1berto** |
| User being impersonated | **Alberto** |
| Remote backdoor creation method | **WMIC → process creation → `net user /add`** |
| Login attempts from backdoor user | **0** |
| Infected host | **James.browne** |
| Malicious PowerShell events | **79** |
| Full URL | **hxxp[://]10[.]10[.]10[.]5/news[.]php** |

---

# 13. Important Splunk Lessons From This Room

## EventID vs EventCode

One of the biggest troubleshooting lessons was that the dataset exposed the Windows event identifier as:

```text
EventID
```

rather than the field we initially tried:

```text
EventCode
```

For this dataset, queries such as:

```spl
index=main EventID=4720
```

worked where an equivalent `EventCode` search did not.

Always inspect the available fields before assuming the field name used by another Splunk dataset.

---

## `host` vs `Hostname`

Another important lesson was that Splunk's internal `host` field did not necessarily represent the actual infected Windows computer.

The actual Windows hostname appeared in:

```text
Hostname
```

This prevented us from incorrectly identifying `server` as the infected machine.

The correct infected host was:

```text
James.browne
```

---

## Use the Right Event ID for the Question

Different Windows and Sysmon activities have different Event IDs.

Examples encountered during this investigation:

```text
4720 → User account created
4726 → User account deleted
4624 → Successful logon
4625 → Failed logon
4103 → PowerShell module logging
4104 → PowerShell script block logging
12   → Sysmon registry object activity
13   → Sysmon registry value activity
```

Knowing what each event represents makes it much easier to construct targeted searches.

---

## Search Broadly Before Narrowing

When a query returns zero results, the problem is not necessarily that the activity did not happen.

Possible reasons include:

- Wrong field name
- Wrong Event ID
- Incorrect hostname field
- Overly restrictive search terms
- Missing fields in some events
- Different sourcetype/field extraction

A better workflow is:

```text
Broad search
    ↓
Identify relevant event
    ↓
Inspect fields
    ↓
Determine EventID / field names
    ↓
Narrow the search
    ↓
Count or extract the required value
```

---

# 14. SOC Investigation Takeaways

This room demonstrated several techniques that are directly relevant to SOC L1 work:

### Account Creation Detection

Unexpected account creation should be investigated, particularly when:

- The username resembles a legitimate account.
- The account is created remotely.
- The account is added to a group.
- A password is immediately configured.
- The account is quickly removed.

### Remote Execution Detection

WMIC can be abused for remote process execution. A command such as:

```text
wmic /node:<host> process call create ...
```

should receive additional scrutiny when it creates users or executes administrative commands.

### PowerShell Detection

PowerShell is legitimate administration tooling, but encoded commands and suspicious network activity can indicate malicious execution.

Useful fields include:

```text
CommandLine
ParentProcessName
ContextInfo
Hostname
EventID
```

### Encoded PowerShell

Base64 encoding is not automatically malicious, but an encoded PowerShell command should be investigated because attackers frequently use encoding to obscure commands.

The investigation process is:

```text
Find PowerShell event
        ↓
Extract command
        ↓
Identify encoded payload
        ↓
Base64 decode
        ↓
Decode using the correct character encoding when required
        ↓
Read the resulting PowerShell
        ↓
Extract URLs / IPs / commands
        ↓
Defang indicators for documentation
```

---

# 15. What I Would Remember From This Lab

The most useful mental model from this room is:

**Account creation → Registry activity → Remote execution → PowerShell → Encoded payload → Network request**

The attacker did not necessarily need to successfully log in with the newly created account for the activity to be suspicious. The creation and manipulation of a look-alike account, combined with remote execution and PowerShell activity, already provided multiple detection opportunities.

The investigation also reinforced an important SOC habit: **do not assume that a failed search means the activity is absent. First verify the field names, event IDs, and data structure.**

---

