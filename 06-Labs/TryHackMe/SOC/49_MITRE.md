# MITRE Frameworks and ATT&CK — Detailed Study Notes

**Platform:** TryHackMe
**Topic:** MITRE ATT&CK, CAR, D3FEND and related MITRE resources
**Date:** 28 September 2026

---

# 1. Introduction to MITRE

## What is MITRE?

MITRE is a not-for-profit organization that conducts research and development in several areas, including:

* Cybersecurity
* Artificial intelligence
* Healthcare
* Space systems
* Other technology and security-related areas

Its overall mission is:

> **"To solve problems for a safer world."**

In cybersecurity, MITRE is particularly important because it provides frameworks and knowledge bases that help security professionals understand **how attackers behave** and how defenders can detect and respond to them.

Some important MITRE cybersecurity resources include:

* **MITRE ATT&CK**
* **Cyber Analytics Repository (CAR)**
* **MITRE D3FEND**
* **MITRE Engage**
* **Adversary Emulation resources**
* **MITRE Caldera**
* **AADAPT**
* **ATLAS**

For a SOC analyst, the most important one to understand first is:

> **MITRE ATT&CK**

---

# 2. MITRE ATT&CK

## What is MITRE ATT&CK?

MITRE ATT&CK is a globally accessible knowledge base that documents:

> **Adversary tactics and techniques based on real-world observations.**

In simple words:

**ATT&CK is a large reference describing how real attackers operate.**

Instead of simply saying:

> "A hacker attacked the company."

ATT&CK allows us to describe the attack much more precisely.

For example:

An attacker might:

1. Send a phishing email
2. Get the victim to open a malicious attachment
3. Execute malicious code
4. Steal credentials
5. Move to another computer
6. Collect sensitive files
7. Exfiltrate those files

Each of these activities can be mapped to specific ATT&CK tactics and techniques.

This gives security teams a common language for describing attacks.

---

# 3. Why Was ATT&CK Created?

MITRE recognized that attackers, especially Advanced Persistent Threat (APT) groups, repeatedly use certain behaviors and techniques.

Security researchers needed a standardized way to document these behaviors.

Instead of every organization describing attacks differently, ATT&CK provides:

* Standard names
* Unique IDs
* Tactics
* Techniques
* Sub-techniques
* Procedure examples
* Threat group information
* Software information
* Mitigations
* Detection information

This makes threat intelligence easier to understand and share.

---

# 4. TTPs

One of the most important terms in cybersecurity is:

> **TTP = Tactics, Techniques and Procedures**

These three words describe different levels of attacker behavior.

---

## 4.1 Tactic

A **tactic** represents the attacker's:

> **Goal or objective**

Think of a tactic as:

> **WHY is the attacker doing this?**

For example:

An attacker wants to obtain a victim's credentials.

The goal is:

**Credential Access**

That is the tactic.

---

## 4.2 Technique

A **technique** explains:

> **HOW the attacker achieves the goal**

For example, the attacker wants credentials.

They might use:

* Credential dumping
* Keylogging
* Phishing
* Password attacks

The specific method is the technique.

So:

**Tactic = Why**

**Technique = How**

---

## 4.3 Procedure

A procedure explains:

> **How the technique was actually implemented by the attacker.**

For example:

Technique:

**Credential Dumping**

Procedure:

An attacker uses a particular tool or command to extract credentials from a compromised system.

The procedure is therefore much more specific.

---

# 5. Easy Way to Remember TTP

Think about a robbery.

### Tactic

The thief wants to:

> Get money.

**WHY?**

---

### Technique

The thief breaks into a safe.

**HOW?**

---

### Procedure

The thief uses a particular tool to bypass the safe's lock.

**HOW EXACTLY?**

So:

| Concept   | Meaning     |
| --------- | ----------- |
| Tactic    | Why         |
| Technique | How         |
| Procedure | How exactly |

This distinction is extremely important when working with MITRE ATT&CK.

---

# 6. Evolution of ATT&CK

ATT&CK originally focused heavily on the **Windows environment**.

Over time, it expanded significantly.

It now covers environments such as:

* Windows
* Linux
* macOS
* Cloud
* Enterprise environments
* Mobile
* Industrial Control Systems (ICS)

There are specialized matrices for different environments.

For example:

### Enterprise

Used for enterprise IT environments.

### Mobile

Focused on mobile platforms.

### ICS

Focused on Industrial Control Systems.

This expansion is important because modern organizations no longer operate only traditional Windows networks.

They may have:

* Windows endpoints
* Linux servers
* Cloud infrastructure
* Mobile devices
* SaaS applications
* Industrial systems

---

# 7. MITRE ATT&CK Matrix

The ATT&CK Matrix is a visual representation of attacker behavior.

The matrix organizes:

**Tactics → Techniques → Sub-techniques**

Tactics appear across the matrix.

Under each tactic are the techniques associated with that goal.

Some techniques have additional sub-techniques.

---

# 8. Example: Active Scanning

The TryHackMe material uses **Active Scanning** as an example.

Imagine an attacker wants information about a target.

### Tactic

Reconnaissance

The attacker's goal is to gather information.

### Technique

Active Scanning

The attacker actively interacts with the target to gather information.

### Sub-techniques

Active Scanning can be broken down into more specific methods such as:

* Scanning IP Blocks
* Vulnerability Scanning
* Wordlist Scanning

Therefore:

```text
Reconnaissance
       ↓
Active Scanning
       ↓
Specific scanning method
```

This hierarchy makes ATT&CK much easier to organize.

---

# 9. ATT&CK Technique Pages

Each ATT&CK technique has its own detailed page.

A technique page can contain information such as:

* Technique name
* Technique ID
* Description
* Sub-techniques
* Procedure examples
* Groups
* Software
* Campaigns
* Mitigations
* Detection information
* References

The unique technique ID is particularly useful.

For example:

**T1595 = Active Scanning**

When you see an ATT&CK ID such as:

```text
T1595
```

you can use that ID to identify the technique.

---

# 10. Why ATT&CK Matters

ATT&CK is extremely useful because cybersecurity professionals often describe the same attacker behavior using different terminology.

ATT&CK provides standardized terminology and IDs.

This creates a common language.

For example, instead of saying:

> "The attacker did some credential stealing."

An analyst can document:

> "The observed behavior maps to an ATT&CK Credential Access technique."

This is much more precise.

---

# 11. ATT&CK and Threat Intelligence

Threat intelligence often contains information about:

* Threat actors
* Malware
* Infrastructure
* Victims
* Attack methods
* Indicators of compromise
* Campaigns

ATT&CK helps turn this information into something structured.

For example:

A threat report might say:

> An attacker used phishing to gain initial access, created scheduled tasks for persistence, and transferred tools onto the victim machine.

A defender can map those behaviors to ATT&CK techniques.

This gives the organization a clearer picture of the attack.

---

# 12. Who Uses MITRE ATT&CK?

ATT&CK is useful to many cybersecurity teams.

## Cyber Threat Intelligence Teams

CTI teams collect and analyze threat information.

They can use ATT&CK to:

* Profile threat actors
* Map observed attacker behavior
* Compare different groups
* Understand attack campaigns
* Produce actionable intelligence

---

## SOC Analysts

SOC analysts investigate alerts.

ATT&CK helps them:

* Understand attacker behavior
* Add context to alerts
* Identify the tactic involved
* Identify the technique involved
* Understand where an alert fits in an attack

For example:

A suspicious PowerShell alert by itself might not tell the complete story.

Mapping it to ATT&CK can help an analyst understand what role the behavior might play in the attack.

---

## Detection Engineers

Detection engineers create security detections.

They can map:

```text
SIEM Rule
     ↓
ATT&CK Technique
     ↓
Attacker Behavior
```

This helps determine whether the organization has detection coverage for important attacker behaviors.

---

## Incident Responders

Incident responders investigate confirmed incidents.

They can map the attack timeline to ATT&CK.

For example:

```text
Phishing
   ↓
Execution
   ↓
Credential Access
   ↓
Lateral Movement
   ↓
Collection
   ↓
Exfiltration
```

This provides a structured view of the incident.

---

## Red and Purple Teams

Red teams emulate attackers.

They can use ATT&CK to:

* Select techniques
* Build attack scenarios
* Test defenses
* Simulate adversary behavior

Purple teams can then work with defenders to determine:

> Did our security controls detect the simulated attacker?

---

# 13. ATT&CK Navigator

The **ATT&CK Navigator** is a tool that allows analysts to visualize and annotate ATT&CK techniques.

It displays the ATT&CK matrix and allows techniques to be highlighted.

This is particularly useful when analyzing a threat group.

For example:

```text
Threat Group
     ↓
Techniques used by group
     ↓
Highlight techniques in Navigator
     ↓
Identify attack behavior
     ↓
Compare against defensive coverage
```

---

# 14. Mustang Panda Example

The TryHackMe room uses **Mustang Panda (G0129)** as an example of threat intelligence mapping.

The group has been mapped to several ATT&CK techniques.

The material highlights behaviors such as:

* Phishing
* Scheduled tasks
* Obfuscation
* Ingress Tool Transfer

The important lesson is not simply memorizing Mustang Panda.

The important lesson is learning how to:

1. Find a threat group
2. Open its ATT&CK page
3. Examine its techniques
4. Open the Navigator layer
5. Understand the techniques used
6. Determine how defenders could detect or mitigate them

---

# 15. ATT&CK for Threat Intelligence

ATT&CK can be used to transform threat intelligence into defensive knowledge.

Imagine an organization receives a report:

> APT group X targets organizations in our industry.

The security team can investigate:

* What techniques does the group use?
* What tactics are involved?
* What software does the group use?
* What infrastructure does it use?
* What techniques are relevant to our environment?
* Do we have detections for those techniques?
* Do we have mitigations?

This becomes particularly important when an organization is migrating infrastructure to the cloud.

---

# 16. Scenario: Aviation Sector

The TryHackMe scenario places us in the role of a security analyst in the aviation sector.

The organization is migrating infrastructure to the cloud.

The task is to:

1. Identify APT groups known to target aviation.
2. Examine their behavior.
3. Identify their tactics and techniques.
4. Use the ATT&CK Navigator.
5. Identify possible defensive coverage gaps.

The completed exercise identified:

### APT Group

**APT33**

### Important sub-technique

**Cloud Accounts**

### Associated tool

**Ruler**

### Mitigation

**User Account Management**

### Detection Strategy

**DETECT-056**

The important SOC lesson is that ATT&CK can connect:

```text
Threat Group
     ↓
Technique
     ↓
Software / Tool
     ↓
Mitigation
     ↓
Detection
```

That makes threat intelligence actionable.

---

# 17. APT33 Example — Understanding the Investigation

The exercise is useful because it demonstrates a real CTI workflow.

Instead of simply searching:

> "Who attacks aviation companies?"

you investigate systematically.

### Step 1 — Identify the threat group

APT33 is associated with activity targeting the aviation sector.

### Step 2 — Examine its ATT&CK techniques

The group page shows techniques and sub-techniques associated with the group.

### Step 3 — Identify the relevant cloud behavior

The exercise highlights:

**Cloud Accounts**

This is particularly relevant to organizations using cloud services such as Office 365.

### Step 4 — Identify associated software

The ATT&CK data links the behavior to:

**Ruler**

### Step 5 — Find mitigation

The exercise identifies:

**User Account Management**

### Step 6 — Find detection information

The exercise identifies:

**DETECT-056**

This demonstrates how threat intelligence can move from:

```text
Threat Actor
       ↓
Observed Behavior
       ↓
ATT&CK Mapping
       ↓
Detection
       ↓
Defense
```

---

# 18. Cyber Analytics Repository (CAR)

Another MITRE resource is:

> **Cyber Analytics Repository (CAR)**

CAR contains analytics designed around the MITRE ATT&CK model.

In simple language:

> **CAR provides examples of how defenders can detect attacker behavior.**

ATT&CK mainly helps answer:

> "What does the attacker do?"

CAR helps move toward:

> "How can I detect that behavior?"

---

# 19. Why CAR Is Useful for a SOC Analyst

Imagine ATT&CK tells you:

> An attacker may abuse scheduled tasks.

That's useful, but a SOC analyst needs another question:

> "What should I look for in my logs?"

CAR helps bridge this gap.

It provides analytics that can contain:

* Detection logic
* Pseudocode
* Tool-specific implementations
* References
* ATT&CK mappings

Some implementations can include examples for:

* Splunk
* EQL
* Other security platforms

---

# 20. CAR Example

The TryHackMe room uses:

**CAR-2020-09-001: Scheduled Task - File Access**

The CAR page provides information about the analytic and its associated ATT&CK techniques.

The implementation section can contain:

### Pseudocode

A human-readable representation of the detection logic.

### Splunk Query

An example of implementing the detection in Splunk.

### LogPoint Search

Another example of implementing the analytic.

Some CAR analytics may also include:

### Unit Tests

These can help validate whether the analytic behaves as expected.

---

# 21. What Is Pseudocode?

Pseudocode is not a programming language.

It is a human-readable description of logic.

For example:

```text
IF
    suspicious process accesses a sensitive file
AND
    process behavior matches known suspicious pattern
THEN
    generate alert
```

The exact implementation can later be converted into a real SIEM query.

This is useful because the detection logic can be understood before worrying about syntax.

---

# 22. CAR and ATT&CK

CAR also provides an ATT&CK Navigator layer.

This allows analysts to visualize which ATT&CK techniques have analytics associated with them.

This can help answer:

> "Which attacker techniques can our available analytics detect?"

This is useful for detection engineering and SOC maturity.

---

# 23. MITRE D3FEND

MITRE D3FEND approaches cybersecurity from the defensive side.

A simple way to remember the difference:

```text
ATT&CK
"What can the attacker do?"

D3FEND
"How can the defender defend against it?"
```

D3FEND stands for:

> **Detection, Denial, and Disruption Framework Empowering Network Defense**

It provides a structured framework for describing defensive techniques.

---

# 24. D3FEND Matrix

D3FEND contains seven major defensive areas:

1. Model
2. Harden
3. Detect
4. Isolate
5. Deceive
6. Evict
7. Restore

These describe different ways defenders can protect systems.

---

# 25. D3FEND — Model

**Model** focuses on understanding the environment.

Before defending something, defenders need to understand:

* Systems
* Assets
* Relationships
* Network architecture
* Digital artifacts
* How systems communicate

In simple terms:

> You cannot effectively defend something you don't understand.

---

# 26. D3FEND — Harden

**Harden** means making systems more difficult to compromise.

Examples include:

* Strengthening authentication
* Removing unnecessary services
* Restricting permissions
* Applying security configurations
* Reducing unnecessary attack surface

The goal is to prevent or reduce successful attacks.

---

# 27. D3FEND — Detect

**Detect** focuses on identifying malicious or suspicious activity.

Examples include:

* SIEM detections
* Endpoint monitoring
* Network monitoring
* Log analysis
* Behavioral detections

This is particularly relevant to SOC analysts.

A SOC spends a significant amount of time in this area.

---

# 28. D3FEND — Isolate

Isolation means separating potentially compromised systems or resources.

For example:

```text
Normal Network

     ↓

Compromised Endpoint

     ↓

Isolate Endpoint
```

This can prevent an attacker from spreading further.

---

# 29. D3FEND — Deceive

Deception involves creating conditions that can mislead or detect attackers.

The objective is to make attacker activity easier to identify or disrupt.

The key idea is:

> Instead of only waiting for attackers to attack real assets, defenders can use deceptive mechanisms to increase visibility or waste attacker effort.

---

# 30. D3FEND — Evict

Eviction focuses on removing attackers or malicious artifacts from the environment.

For example, defenders may need to:

* Remove malicious persistence
* Remove malware
* Disable compromised accounts
* Remove attacker access
* Clean compromised systems

The objective is to get the attacker out.

---

# 31. D3FEND — Restore

After an incident, systems may need to be returned to a trusted operational state.

Restoration can involve:

* Recovering systems
* Restoring data
* Rebuilding compromised machines
* Returning services to normal operation

This is an important part of incident recovery.

---

# 32. D3FEND Example — Credential Rotation

The TryHackMe material uses:

**Credential Rotation**

as an example.

The basic idea is:

> Regularly changing credentials can prevent attackers from continuing to use stolen credentials.

For example:

```text
Attacker steals credential
          ↓
Credential rotated
          ↓
Old credential becomes unusable
          ↓
Attacker loses access
```

D3FEND provides information about:

* What the defensive technique is
* How it works
* What needs to be considered
* Relationships with digital artifacts
* Relationships with ATT&CK techniques

This allows defenders to connect offensive behavior with defensive controls.

---

# 33. ATT&CK vs D3FEND

A simple comparison:

| Framework | Main Perspective |
| --------- | ---------------- |
| ATT&CK    | Attacker         |
| D3FEND    | Defender         |

Think:

```text
ATTACKER
   ↓
ATT&CK
   ↓
"What can the attacker do?"

        VS

DEFENDER
   ↓
D3FEND
   ↓
"How can we defend against it?"
```

They complement each other.

---

# 34. Adversary Emulation

MITRE also provides an **Adversary Emulation Library**.

Adversary emulation means:

> Simulating the behavior of a real-world threat actor in a controlled environment.

Instead of randomly running attacks, a security team can reproduce techniques associated with a known threat group.

For example:

```text
Real Threat Group
       ↓
Known ATT&CK techniques
       ↓
Emulation plan
       ↓
Controlled attack simulation
       ↓
Test defensive controls
       ↓
Improve detections
```

---

# 35. Why Adversary Emulation Is Useful

Suppose an organization knows that a particular threat group is relevant to its industry.

The organization can simulate techniques associated with that group.

Then the SOC can ask:

* Did our SIEM detect it?
* Did our EDR detect it?
* Did an alert trigger?
* Did the analyst recognize it?
* Did our response procedure work?
* Where are the gaps?

This is much more useful than simply assuming that security controls work.

---

# 36. MITRE Caldera

**MITRE Caldera** is an automated adversary emulation platform.

It can simulate attacker behavior using the ATT&CK framework.

It can be used by security teams to test:

* Detection
* Monitoring
* Incident response
* Security controls
* Defensive coverage

It supports controlled red-team and blue-team exercises.

---

# 37. Simple Caldera Workflow

A simplified view:

```text
Choose attacker behavior
        ↓
Map behavior to ATT&CK
        ↓
Run controlled simulation
        ↓
Generate telemetry
        ↓
SIEM / EDR receives telemetry
        ↓
SOC investigates
        ↓
Measure detection
        ↓
Improve defenses
```

This makes Caldera especially useful for purple-team exercises.

---

# 38. Purple Team Connection

A purple team brings offensive and defensive teams together.

For example:

### Red Team

Simulates:

> Credential access

### Blue Team

Attempts to detect:

> Credential access behavior

### Purple Team

Analyzes:

> Did the detection work?

Then the organization improves the detection.

This creates a continuous improvement cycle.

---

# 39. AADAPT

MITRE also develops specialized frameworks.

One example is:

> **AADAPT — Adversarial Actions in Digital Asset Payment Technologies**

It focuses on adversarial behavior related to digital asset technologies.

The framework can help defenders understand threats involving areas such as:

* Blockchain
* Smart contracts
* Digital wallets
* Digital asset systems

It follows a structure similar to ATT&CK.

---

# 40. ATLAS

Another MITRE framework is:

> **ATLAS — Adversarial Threat Landscape for AI Systems**

ATLAS focuses specifically on threats against:

* Artificial intelligence systems
* Machine learning systems

It documents areas such as:

* Attack techniques
* Vulnerabilities
* Adversarial behavior
* Mitigations

This is becoming increasingly relevant as organizations deploy AI systems.

---

# 41. Big Picture — MITRE Ecosystem

The different resources can be understood like this:

```text
                    MITRE
                      |
       +--------------+--------------+
       |              |              |
     ATT&CK          CAR          D3FEND
       |              |              |
  Understand       Detect        Defend
  attackers        behavior      against
       |
       |
 Threat Intelligence
       |
       ↓
ATT&CK Navigator
       |
       ↓
Adversary Emulation
       |
       ↓
     Caldera
       |
       ↓
 Test defenses
```

This is not a replacement for understanding each framework individually, but it is a useful mental model.

---

# 42. SOC Analyst Perspective

As a SOC analyst, you will frequently see MITRE ATT&CK concepts in:

* SIEM alerts
* EDR alerts
* Threat intelligence reports
* Incident reports
* Detection rules
* Threat hunting
* Security dashboards
* Purple-team exercises

For example, an alert may say:

```text
MITRE ATT&CK:
T1059
Command and Scripting Interpreter
```

Instead of treating that as just a technical ID, you should ask:

1. What tactic does this belong to?
2. What does the technique mean?
3. What behavior caused the detection?
4. Is the activity expected?
5. Which user performed it?
6. Which process executed it?
7. What host was involved?
8. What happened before it?
9. What happened after it?
10. Could this be part of a larger attack chain?

This is where ATT&CK becomes useful during alert triage.

---

# 43. ATT&CK as an Investigation Map

Suppose a SOC alert indicates suspicious execution.

You might investigate:

```text
Execution
   ↓
What process executed?
   ↓
Who executed it?
   ↓
What parent process started it?
   ↓
What command line was used?
   ↓
What network connections followed?
   ↓
Were credentials accessed?
   ↓
Was another machine contacted?
   ↓
Was data collected?
```

ATT&CK helps you understand where individual behaviors fit into the larger attack.

---

# 44. ATT&CK Is Not a Step-by-Step Attack Recipe

An important concept to remember:

ATT&CK does not mean every attack follows:

```text
1 → 2 → 3 → 4 → 5
```

Attackers can:

* Skip phases
* Repeat techniques
* Move backward
* Return to earlier activities
* Change techniques
* Adapt based on defenses

For example:

```text
Initial Access
      ↓
Execution
      ↓
Discovery
      ↓
Credential Access
      ↓
Lateral Movement
      ↓
Discovery AGAIN
      ↓
Credential Access AGAIN
```

This is why ATT&CK is better thought of as a behavioral knowledge base rather than a simple checklist.

---

# 45. ATT&CK and Threat Hunting

Threat hunting is the proactive search for suspicious activity.

ATT&CK can help build hunting hypotheses.

For example:

> "Could an attacker be using suspicious scheduled tasks for persistence?"

The analyst can then investigate:

* Scheduled task creation
* Task names
* Task paths
* Creating process
* User account
* Command line
* Execution history

This can lead to a structured hunt.

---

# 46. ATT&CK and Detection Engineering

Detection engineers can use ATT&CK to identify coverage gaps.

For example:

```text
Technique A → Detection exists
Technique B → Detection exists
Technique C → No detection
Technique D → Partial detection
```

This can reveal weaknesses in the organization's monitoring.

The organization can then prioritize detection development.

---

# 47. ATT&CK Coverage

Imagine an organization wants to understand its defensive visibility.

They can map:

```text
ATT&CK Technique
        ↓
Can we observe it?
        ↓
Do we have logs?
        ↓
Do we have a detection?
        ↓
Does the detection generate useful alerts?
        ↓
Can SOC analysts investigate it?
```

This is much more meaningful than simply saying:

> "We have a SIEM."

Having a SIEM does not automatically mean every attacker behavior is detected.

---

# 48. ATT&CK IDs

One thing I need to remember from this room is that ATT&CK IDs are extremely useful.

Examples from the material include:

```text
T1595
```

for Active Scanning.

Groups also have IDs.

For example:

```text
G0129
```

for Mustang Panda.

Detection strategies can also have IDs such as:

```text
DETECT-056
```

These IDs make it easier to reference specific information.

---

# 49. Important Terminology

## Threat Actor

A person or group conducting malicious activity.

---

## APT

**Advanced Persistent Threat**

A term commonly used for threat groups that conduct sophisticated and persistent operations.

---

## Tactic

The attacker's objective.

**WHY**

---

## Technique

The method used to achieve the objective.

**HOW**

---

## Sub-technique

A more specific variation of a technique.

---

## Procedure

The actual implementation of a technique.

---

## TTP

Tactics, Techniques and Procedures.

---

## IOC

Indicator of Compromise.

Examples can include:

* IP addresses
* Domains
* File hashes
* URLs

---

## ATT&CK Matrix

A visual organization of tactics and techniques.

---

## ATT&CK Navigator

A tool for exploring, highlighting and analyzing ATT&CK techniques.

---

## Threat Intelligence

Information about threats that can help an organization understand and defend against attackers.

---

## Detection

A security mechanism designed to identify suspicious or malicious behavior.

---

## Mitigation

A defensive measure intended to reduce the likelihood or impact of an attack technique.

---

# 50. Complete Mental Model

The easiest way for me to understand the entire MITRE ecosystem is:

```text
                ATTACKER
                   |
                   ↓
             What do they do?
                   |
                   ↓
              MITRE ATT&CK
                   |
        +----------+----------+
        |          |          |
      Tactic    Technique   Procedure
        |          |          |
       WHY        HOW       HOW EXACTLY
        |
        ↓
 Threat Intelligence
        |
        ↓
 ATT&CK Navigator
        |
        ↓
 Identify attacker behavior
        |
        ↓
 CAR
        |
        ↓
 Build / understand detections
        |
        ↓
 D3FEND
        |
        ↓
 Select defensive techniques
        |
        ↓
 Adversary Emulation
        |
        ↓
 Caldera / controlled testing
        |
        ↓
 Test defenses
        |
        ↓
 Find gaps
        |
        ↓
 Improve SOC
```

---

# 51. What I Learned From This Room

The main thing I learned is that MITRE is not just a website containing a list of hacking techniques.

It is an ecosystem that helps security professionals understand the complete relationship between:

```text
Threat Actor
      ↓
Behavior
      ↓
ATT&CK Technique
      ↓
Detection
      ↓
Defense
      ↓
Testing
```

ATT&CK provides the attacker perspective.

CAR helps with analytics and detection.

D3FEND provides the defensive perspective.

Adversary emulation and Caldera help organizations test whether their defenses actually work.

---

# 52. Most Important Takeaways for a SOC Analyst

### 1. Learn to recognize ATT&CK IDs

When you see something like:

```text
Txxxx
```

understand that it identifies an ATT&CK technique or sub-technique.

---

### 2. Understand tactics before techniques

Do not only memorize technique names.

Understand:

> What was the attacker trying to achieve?

---

### 3. Think in attack chains

A single alert may be only one part of a much larger attack.

Always ask:

> What happened before this?

and:

> What happened after this?

---

### 4. Use ATT&CK during investigations

When investigating an alert, mapping behavior to ATT&CK can help determine:

* What the attacker may be trying to accomplish
* What other activity to investigate
* What related techniques may appear
* What telemetry should exist

---

### 5. Use ATT&CK for threat hunting

ATT&CK can turn vague questions into specific hunting hypotheses.

---

### 6. Use ATT&CK for detection coverage

Organizations can determine:

> Which attacker behaviors can we detect?

and:

> Which behaviors are currently invisible to us?

---

### 7. Understand the difference between ATT&CK and D3FEND

Remember:

```text
ATT&CK = attacker behavior

D3FEND = defensive behavior
```

---

# 53. Quick Revision Sheet

## MITRE

Cybersecurity research and knowledge organization providing frameworks and resources.

---

## ATT&CK

Knowledge base of real-world adversary behavior.

---

## Tactic

**Why**

The attacker's objective.

---

## Technique

**How**

The method used to accomplish the objective.

---

## Sub-technique

More specific version of a technique.

---

## Procedure

The specific implementation of the technique.

---

## ATT&CK Matrix

Visual representation of tactics and techniques.

---

## ATT&CK Navigator

Tool for visualizing and analyzing ATT&CK techniques.

---

## CAR

Cyber Analytics Repository.

Helps translate attacker behavior into detection analytics.

---

## D3FEND

Defensive framework describing defensive techniques.

---

## Adversary Emulation

Controlled simulation of real-world attacker behavior.

---

## Caldera

Automated adversary emulation platform.

---

## AADAPT

Framework focused on adversarial actions involving digital asset payment technologies.

---

## ATLAS

Framework focused on adversarial threats against AI and ML systems.

---

# 54. Final Understanding

Before this topic, I could think of an attack mainly as a sequence of tools and commands.

After studying MITRE, I understand that a better way to analyze an attack is through **behavior**.

For example:

```text
Attacker
   ↓
Objective
   ↓
Tactic
   ↓
Technique
   ↓
Procedure
   ↓
Telemetry
   ↓
Detection
   ↓
Investigation
   ↓
Mitigation / Response
```

This is especially important for a SOC analyst because the job is not simply to recognize malware or suspicious commands.

The analyst needs to understand:

> **What is happening, why it is happening, how it fits into the attack, and what evidence should be investigated next.**

MITRE ATT&CK provides a common language for doing exactly that.

---

# 55. Practical SOC Connection

The biggest practical connection I take from this room is:

```text
SIEM Alert
    ↓
Identify Behavior
    ↓
Map to ATT&CK
    ↓
Identify Tactic
    ↓
Identify Technique
    ↓
Investigate Related Activity
    ↓
Determine if Malicious
    ↓
Respond
    ↓
Document
```

This connects directly with the SOC skills I have already been learning, especially:

* SIEM
* Alert Triage
* Windows Logging
* Threat Detection
* Network Traffic Analysis
* Phishing Analysis
* Incident Reporting
* Threat Intelligence

MITRE ATT&CK acts as a bridge between many of these topics.

---

