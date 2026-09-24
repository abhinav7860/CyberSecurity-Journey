# Cyber Kill Chain

**Platform:** TryHackMe  
**Topic:** Cyber Kill Chain  
**Author:** Abhinav Sabu  
**Completion Date:** 24 September 2026

---

## 1. Introduction

The Cyber Kill Chain is a framework used to understand the different phases of a cyber attack.

The concept of a **kill chain** originally comes from the military. In cybersecurity, the framework was established by Lockheed Martin in 2011 and describes the steps adversaries can follow during an attack.

The seven phases covered in this lesson are:

1. Reconnaissance
2. Weaponization
3. Delivery
4. Exploitation
5. Installation
6. Command & Control
7. Actions on Objectives

The framework helps security professionals recognise intrusion attempts, understand attacker goals, identify missing security controls, and improve defensive capabilities.

---

## 2. Why the Cyber Kill Chain Is Important

The Cyber Kill Chain provides a structured way to understand how an attack develops.

It can help security professionals:

- Recognise intrusion attempts
- Understand an intruder's goals and objectives
- Assess network and system security
- Identify missing security controls
- Identify security gaps
- Improve protection against ransomware, security breaches and Advanced Persistent Threats (APTs)

For a SOC analyst, understanding the attack lifecycle is useful because an alert can represent activity occurring at a particular stage of an attack.

---

## 3. The Seven Phases

```text
Reconnaissance
      |
      v
Weaponization
      |
      v
Delivery
      |
      v
Exploitation
      |
      v
Installation
      |
      v
Command & Control
      |
      v
Actions on Objectives
```

---

# 4. Phase 1 — Reconnaissance

Reconnaissance is the **research and planning phase** of an attack.

An adversary gathers information about the target to decide what to do next. Information may include:

- Infrastructure details
- Employee information
- Business processes
- Exposed technologies

Reconnaissance can often be passive and difficult for the target to detect.

### OSINT

**OSINT — Open-Source Intelligence** involves gathering information from publicly available sources.

Examples include:

- Search engines
- Print and online media
- Social media accounts
- Online forums and blogs
- Online public record databases
- WHOIS and technical data

### Passive Reconnaissance

Passive reconnaissance involves gathering information without directly interacting with the target.

Examples:

- WHOIS lookups
- Social media scraping
- Reviewing breach data

### Active Reconnaissance

Active reconnaissance involves directly interacting with the target.

Examples:

- Social engineering
- Port scanning
- Banner grabbing
- Probing open services

### Email Harvesting

Email harvesting is the process of obtaining email addresses from public, paid, or free services. Attackers can use harvested addresses when preparing phishing or social-engineering attacks.

The lesson mentions:

- **theHarvester** — gathers emails, names, subdomains, IPs and URLs from public sources.
- **Hunter.io** — obtains contact information associated with a domain.
- **OSINT Framework** — provides collections of OSINT tools organised into categories.

---

# 5. Phase 2 — Weaponization

After reconnaissance, the attacker turns collected information into an actionable attack.

Weaponization involves preparing malware, exploits and payloads for use against the target.

### Important Terms

**Malware:** Software designed to damage, disrupt, or gain unauthorised access to a computer.

**Exploit:** A program or code that takes advantage of a vulnerability or flaw.

**Payload:** Malicious code that the attacker runs on the system.

### Weaponization Examples

- Creating infected Microsoft Office documents containing malicious macros or VBA scripts
- Creating malicious payloads or worms and placing them on USB drives
- Setting up Command & Control infrastructure
- Installing a backdoor
- Creating convincing phishing templates or OAuth-consent applications

```text
Reconnaissance
      |
      v
Raw Information
      |
      v
Weaponization
      |
      v
Actionable Attack Tool
```

---

# 6. Phase 3 — Delivery

Delivery is the stage where the attacker chooses how to transmit the malware or payload to the target environment.

### Phishing Email

A malicious email can contain:

- A malicious link
- A malicious attachment

A targeted phishing attack against a particular person can be referred to as **spear phishing**.

### USB Drops

A USB device can be physically placed where potential victims may find it, such as coffee shops, car parks, or streets.

### Watering Hole Attacks

A watering hole attack targets a group of people by compromising a website they commonly visit. Victims may then be redirected or encouraged to download malicious software.

---

# 7. Phase 4 — Exploitation

Exploitation occurs when the attacker's code executes on the target by taking advantage of a vulnerability.

Examples include:

- **Malicious macro execution** — malicious code executes when a victim opens a malicious document.
- **Zero-day exploits** — exploits unknown or unpatched flaws.
- **Known CVEs** — exploitation of known vulnerabilities that remain unpatched.

After gaining access, attackers may exploit software, systems, or servers to escalate privileges or move laterally through the network.

### Signs of Exploitation

Defenders can look for:

- Unexpected process spawns
- Registry changes
- New services
- Suspicious command-line arguments in system logs

---

# 8. Phase 5 — Installation

After gaining access, an attacker may want to maintain access even if the original access method is removed.

A **persistent backdoor** can allow an attacker to regain access to a previously compromised system.

### Persistence Examples

**Web Shell:** A malicious script placed on a web server, potentially written in ASP, PHP, or JSP.

**Backdoor:** An access mechanism that provides continued or unauthorised access. The lesson uses Meterpreter as an example of a Metasploit payload that can provide an interactive shell.

**Windows Services:** Attackers can create or modify Windows services to execute malicious scripts or payloads. The lesson associates this with MITRE ATT&CK technique **T1543.003**.

**Registry Run Keys / Startup Folder:** A malicious payload can be configured to execute when a user logs in.

**Timestomping:** File timestamps can be modified to make malicious files appear legitimate or make forensic investigation more difficult. The lesson identifies this as **T1070.006**.

---

# 9. Phase 6 — Command & Control

After establishing persistence and executing malware, the attacker can establish a **Command and Control (C2)** channel.

C2 allows an attacker to remotely control and manipulate a compromised system.

### C2 Beaconing

A compromised machine can repeatedly communicate with an external server controlled by the attacker. This repeated communication is commonly described as **beaconing**.

```text
Compromised Host
       |
       | Repeated communication
       v
Attacker C2 Server
       |
       | Commands
       v
Compromised Host
```

### Common C2 Channels

**HTTP / HTTPS**

- HTTP — port 80
- HTTPS — port 443

These protocols can make malicious communication blend with legitimate traffic.

**DNS**

An infected system can make repeated DNS requests to attacker-controlled infrastructure. The lesson describes this as **DNS Tunneling**.

The C2 infrastructure may be owned by the adversary or may itself be a compromised host.

---

# 10. Phase 7 — Actions on Objectives

This is the final phase of the Cyber Kill Chain. After progressing through the earlier phases, the attacker works toward the original objective.

Examples include:

- Collecting user credentials
- Privilege escalation
- Internal reconnaissance
- Lateral movement
- Collecting and exfiltrating sensitive data
- Deleting backups and shadow copies
- Overwriting or corrupting data

### Credential Collection

The attacker may collect user credentials to access additional systems or accounts.

### Privilege Escalation

Privilege escalation involves gaining higher levels of access, such as obtaining domain administrator access by exploiting a misconfiguration.

### Internal Reconnaissance

The attacker can investigate the internal environment to identify systems, software, vulnerabilities, and additional targets.

### Lateral Movement

The attacker can move from the initially compromised system to other systems within the environment.

### Data Collection and Exfiltration

Attackers may collect sensitive information and transfer it outside the organisation.

### Destruction and Impact

Attackers may also delete backups, delete shadow copies, overwrite data, or corrupt data.

---

# 11. Complete Cyber Kill Chain

```text
+----------------------+
| 1. RECONNAISSANCE    |
| Research the target  |
+----------+-----------+
           |
           v
+----------------------+
| 2. WEAPONIZATION     |
| Prepare malware,     |
| exploit and payload  |
+----------+-----------+
           |
           v
+----------------------+
| 3. DELIVERY          |
| Get payload to       |
| the target           |
+----------+-----------+
           |
           v
+----------------------+
| 4. EXPLOITATION      |
| Exploit a weakness   |
| and execute code     |
+----------+-----------+
           |
           v
+----------------------+
| 5. INSTALLATION      |
| Establish persistence|
+----------+-----------+
           |
           v
+----------------------+
| 6. COMMAND & CONTROL |
| Remote communication |
+----------+-----------+
           |
           v
+----------------------+
| 7. ACTIONS ON        |
| OBJECTIVES           |
| Achieve the goal     |
+----------------------+
```

---

# 12. Attacker Perspective

The lesson follows a fictional attacker named **Megatron** to demonstrate how the phases connect.

```text
Megatron
   |
   v
Research target
   |
   v
Gather OSINT
   |
   v
Prepare payload
   |
   v
Deliver payload
   |
   v
Exploit vulnerability
   |
   v
Install persistence
   |
   v
Establish C2
   |
   v
Achieve objective
```

This demonstrates that an attack can be a sequence of activities that build upon one another rather than a single event.

---

# 13. Defensive Perspective

The Cyber Kill Chain can also be used from the defender's perspective.

| Kill Chain Phase | Defensive Question |
|---|---|
| **Reconnaissance** | What information is publicly exposed? |
| **Weaponization** | Can malicious files or payloads be detected? |
| **Delivery** | Can phishing, malicious links and attachments be blocked? |
| **Exploitation** | Are vulnerabilities patched and exploitation monitored? |
| **Installation** | Are persistence mechanisms being detected? |
| **C2** | Are unusual outbound connections or beaconing being detected? |
| **Actions on Objectives** | Are privilege escalation, lateral movement, data theft and destructive actions being monitored? |

This gives defenders multiple opportunities to detect or interrupt an attack.

---

# 14. Detection Opportunities

### Reconnaissance

- Unexpected scanning
- Suspicious probing
- Public information exposure

### Exploitation

- Unexpected process creation
- Registry changes
- New services
- Suspicious command-line arguments

### Installation

- New or modified services
- Suspicious startup entries
- Web shells
- Unexpected backdoors
- Modified timestamps

### Command & Control

- Repeated outbound connections
- Suspicious HTTP/HTTPS communication
- Unusual DNS activity
- Beaconing patterns

### Actions on Objectives

- Credential collection
- Privilege escalation
- Lateral movement
- Large-scale data collection
- Data exfiltration
- Backup deletion
- Data corruption

---

# 15. Cyber Kill Chain and SOC Work

As someone learning toward a SOC role, the Cyber Kill Chain is useful because it gives context to security alerts.

Instead of looking at an alert as an isolated event, I can ask:

1. Which stage could this activity belong to?
2. What happened before it?
3. What could happen next?
4. What is the attacker trying to achieve?
5. Where can the attack be interrupted?

For example:

```text
Suspicious Email
      |
      v
Delivery
      |
      v
Malicious Code Execution
      |
      v
Exploitation
      |
      v
Persistence
      |
      v
C2 Beaconing
      |
      v
Data Theft
```

Connecting alerts into a sequence can provide a clearer incident picture.

---

# 16. Key Terminology

| Term | Meaning |
|---|---|
| **Reconnaissance** | Research and information gathering about the target |
| **OSINT** | Open-Source Intelligence |
| **Weaponization** | Preparing malware, exploits and payloads |
| **Malware** | Software designed to damage, disrupt or gain unauthorised access |
| **Exploit** | Code that takes advantage of a vulnerability |
| **Payload** | Malicious code executed on the target |
| **Delivery** | Transmitting the payload to the target |
| **Exploitation** | Executing malicious code by taking advantage of a weakness |
| **Installation** | Establishing persistence or continued access |
| **Backdoor** | Access mechanism that allows continued or unauthorised access |
| **C2** | Command and Control |
| **Beaconing** | Repeated communication between a compromised host and C2 infrastructure |
| **Lateral Movement** | Moving from one compromised system to another |
| **Exfiltration** | Taking data out of the environment |
| **Actions on Objectives** | Activities performed to achieve the attacker's final goal |

---

# 17. What I Learned

Today I learned that:

1. The Cyber Kill Chain is a framework for understanding cyber attacks.
2. The framework contains seven phases.
3. Reconnaissance is the research and planning phase.
4. OSINT can provide valuable information about a target.
5. Reconnaissance can be passive or active.
6. Weaponization involves preparing malware, exploits and payloads.
7. Delivery is how the attacker gets the payload to the target.
8. Phishing, USB drops and watering hole attacks are examples of delivery methods.
9. Exploitation occurs when malicious code executes by taking advantage of a vulnerability.
10. Installation establishes continued access or persistence.
11. C2 provides communication between the attacker and compromised host.
12. Beaconing is repeated communication with C2 infrastructure.
13. Actions on Objectives are the attacker's final activities.
14. Attackers can perform credential collection, privilege escalation, internal reconnaissance, lateral movement and data exfiltration.
15. The Kill Chain helps SOC analysts understand where activity may fit in an attack.
16. Understanding the attack lifecycle helps defenders identify detection and prevention opportunities.

---

# 18. Quick Revision

```text
Reconnaissance
= Research the target

Weaponization
= Prepare the attack

Delivery
= Send the payload

Exploitation
= Execute by exploiting a weakness

Installation
= Establish persistence

Command & Control
= Communicate with the compromised system

Actions on Objectives
= Achieve the attacker's goal
```

### Easy Memory Chain

**R → W → D → E → I → C → A**

**Reconnaissance → Weaponization → Delivery → Exploitation → Installation → Command & Control → Actions on Objectives**

---

# 19. Final Understanding

My biggest takeaway from this lesson is that a cyber attack can be understood as a sequence of stages rather than a single event.

The attacker first learns about the target, prepares an attack, delivers it, exploits a weakness, establishes continued access, creates communication with the compromised system, and finally works toward the objective.

```text
WHO / TARGET?
     |
     v
RECONNAISSANCE
     |
     v
WEAPONIZATION
     |
     v
DELIVERY
     |
     v
EXPLOITATION
     |
     v
INSTALLATION
     |
     v
COMMAND & CONTROL
     |
     v
ACTIONS ON OBJECTIVES
```

As a SOC analyst, I can use this structure to think about:

- What happened?
- Which stage is occurring?
- What evidence should I look for?
- What could happen next?
- Where can the attack be stopped?

This makes the Cyber Kill Chain an important framework for understanding attacker behaviour and defensive opportunities.

---

# 20. Conclusion

The Cyber Kill Chain gave me a structured way to understand the lifecycle of a cyber attack.

The seven phases are:

1. **Reconnaissance**
2. **Weaponization**
3. **Delivery**
4. **Exploitation**
5. **Installation**
6. **Command & Control**
7. **Actions on Objectives**

This lesson connects strongly with my SOC learning because it provides a high-level structure for understanding attacker behaviour.

I can now use the Kill Chain to organise suspicious activity into a sequence and think about where defenders can detect, investigate and interrupt an attack.

---

