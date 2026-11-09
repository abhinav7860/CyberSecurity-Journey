# LetsDefend — SOC Fundamentals

## Study Session 02: EDR, SOAR & Threat Intelligence

**Date:** 04 November 2026  
**Platform:** LetsDefend  
**Purpose:** Personal SOC learning notes

---

## Overview

This session focuses on three technologies that support modern Security Operations Center (SOC) investigations:

- **Endpoint Detection and Response (EDR)** — endpoint visibility, investigation, and containment.
- **Security Orchestration, Automation and Response (SOAR)** — integration of security tools, automated workflows, and playbooks.
- **Threat Intelligence** — reputation data and indicators that help provide context during investigations.

I also reviewed common SOC analyst mistakes, especially relying too heavily on a single security tool or outdated intelligence.

> **Core lesson:** No single alert, reputation score, or tool result should determine an investigation outcome. Analysts need to correlate evidence from multiple sources.

## Learning Objectives

By the end of this session, I aimed to understand how to:

- Investigate endpoint activity using process, network, and device information.
- Search for Indicators of Compromise (IOCs) across multiple endpoints.
- Understand endpoint isolation and its purpose during incident containment.
- Explain how SOAR integrations and playbooks support SOC workflows.
- Use threat intelligence as supporting evidence rather than conclusive proof.
- Recognise the limitations of reputation services and sandbox analysis.
- Correlate endpoint and centralised log evidence to understand incident scope.

---

## 1. Endpoint Detection and Response (EDR)

EDR continuously monitors endpoint activity, collects security telemetry, detects suspicious behaviour, and provides investigation and response capabilities.

Endpoints include desktops, laptops, servers, and workstations.

### What can an analyst investigate?

| EDR capability | Investigation value |
|---|---|
| Endpoint information | Hostname, IP address, operating system, and device details |
| Process list | Running processes and potentially suspicious execution |
| Network connections | Connections established by an endpoint and their destinations |
| Browser history | Available browser activity relevant to an investigation |
| IOC search | Search for hashes, filenames, IP addresses, and other indicators across endpoints |
| Live investigation | Examine endpoint activity and artefacts further |
| Containment | Restrict a compromised endpoint from normal network communication |

### Process investigation

A process is a program currently executing on a computer. Common Windows examples include:

`explorer.exe` · `notepad.exe` · `powershell.exe` · `cmd.exe`

During process investigation, I should consider:

- Process name and command line.
- Parent-child process relationships.
- Execution timestamps.
- User context.

**Example:** Microsoft Word launching PowerShell with an encoded command may be suspicious because a document could be attempting to execute code. This behaviour requires investigation; it is not automatically proof of malware.

### IOC search across endpoints

An **Indicator of Compromise (IOC)** is an observable artefact that may indicate a security compromise.

Examples include:

- File hashes.
- Suspicious IP addresses.
- Malicious domains.
- Filenames.
- URLs.

If a suspicious file hash is found on one endpoint, searching for that hash across other endpoints can help determine whether the same file exists elsewhere and establish the possible scope of the incident. A match is an investigative lead and must be validated with additional evidence.

### Live investigation and containment

EDR platforms may provide remote investigation capabilities to inspect processes, files, system activity, suspicious commands, and other endpoint artefacts.

Containment limits the impact and spread of an incident. An EDR solution may isolate a compromised endpoint from normal network communication while retaining a management connection to the EDR infrastructure, where supported.

> **Operational note:** Endpoint isolation can interrupt business operations. It should follow the organisation's incident-response procedures and authorisation requirements.

**Key takeaway:** EDR helps answer the question: *What happened on the endpoint?*

---

## 2. Security Orchestration, Automation and Response (SOAR)

SOAR connects security tools and automates repetitive investigation and response tasks. It coordinates workflows so analysts can spend more time evaluating evidence and making decisions.

| Component | Purpose |
|---|---|
| Orchestration | Integrates security products and coordinates their operations |
| Automation | Performs repetitive tasks through predefined workflows |
| Response | Supports appropriate actions based on findings and procedures |

### Example: automated IP enrichment

1. A SIEM generates an alert containing a suspicious IP address.
2. SOAR extracts the IP address from the alert.
3. A configured workflow queries VirusTotal or another intelligence source.
4. The workflow collects reputation results.
5. The results are added to the investigation case for analyst review.

Automation reduces repetitive work, but the analyst still needs to interpret the results and decide what they mean in context.

### SOAR playbooks

A **playbook** is a predefined sequence of investigation or response steps for a particular scenario. It may contain automated actions, manual analyst tasks, and decision points.

A phishing investigation playbook may include:

1. Identify the sender and examine email headers.
2. Extract URLs and attachments.
3. Check domain and URL reputation.
4. Analyse attachment hashes.
5. Identify other affected recipients or users.
6. Document findings and escalate when necessary.

Playbooks help standardise investigations and reduce the chance of missing important steps.

### SOAR in LetsDefend

LetsDefend provides a **Case Management** feature that simulates aspects of a SOAR-assisted workflow. Cases can have associated playbooks that guide analysts through investigation steps.

Case Management and SOAR are related, but they are not interchangeable in every context. A full SOAR platform typically includes integrations, orchestration, automation, and response capabilities.

### Products mentioned

- Splunk Phantom (now part of Splunk SOAR).
- IBM Resilient.
- Logsign.
- Demisto (now Palo Alto Networks Cortex XSOAR).

**Key takeaway:** SOAR helps answer the question: *How can investigation and response workflows be coordinated and made more consistent?*

---

## 3. Threat Intelligence

Threat Intelligence is information collected and analysed to help organisations understand and respond to cybersecurity threats.

Threat Intelligence Feeds provide indicators and information associated with previously observed malicious activity.

| Indicator | Description |
|---|---|
| File hash | A digital fingerprint of a file, such as MD5 or SHA-256 |
| IP address | A network address associated with suspicious activity |
| Domain | A domain associated with potentially malicious infrastructure |
| URL | A web address associated with suspicious or malicious content |
| C2 indicator | Infrastructure associated with attacker command-and-control communication |

### Intelligence sources

| Source | Use |
|---|---|
| [VirusTotal](https://www.virustotal.com/) | Examine files, URLs, domains, and IP addresses using multiple security engines and other analysis information |
| [Cisco Talos Intelligence](https://talosintelligence.com/) | Review threat intelligence and reputation information |

### Limitations to remember

**A clean result does not prove a file is safe.** A result such as `0 detections` does not guarantee that a file is harmless. New malware, obfuscation, and antivirus-evasion techniques may prevent detection.

**IP addresses can change ownership.** An IP address previously used for malicious command-and-control activity may later be reassigned to a legitimate customer. Historical reputation alone does not establish that current activity is malicious.

When reviewing an indicator, I should consider its age, context, current behaviour, and other available evidence.

**Key takeaway:** Threat Intelligence helps answer the question: *Has this indicator been associated with known malicious activity?* It is an investigative lead, not conclusive proof of compromise.

---

## 4. Common SOC Analyst Mistakes

| Mistake | Why it is a problem | Better investigation practice |
|---|---|---|
| Over-reliance on VirusTotal | Zero detections does not prove a file is harmless | Examine behaviour and correlate endpoint and network evidence |
| Hasty sandbox analysis | Short analysis periods may miss delayed behaviour, user interaction, or evasion | Review execution duration and behavioural indicators |
| Inadequate log analysis | Investigating only the endpoint in the alert may miss other affected devices | Search centralised logs for related activity across the environment |
| Overlooking VirusTotal dates | Historical or cached results may not reflect current conditions | Check last analysis date, submission history, recent detections, and context |

**Key takeaway:** Good investigations require current evidence, contextual analysis, and correlation across multiple sources.

---

## 5. How SOC Technologies Work Together

Consider a suspicious executable detected on an employee's workstation.

1. A SIEM alert identifies a suspicious executable.
2. The SOC analyst starts the investigation.
3. EDR provides process and endpoint information.
4. The analyst obtains the suspicious file hash.
5. Threat Intelligence adds reputation context.
6. Log Management checks whether other devices show related activity.
7. A SOAR playbook guides the investigation and may automate enrichment.
8. The analyst evaluates the evidence and decides on the next steps.
9. Escalation and authorised containment follow when required.

| Technology | Question it helps answer |
|---|---|
| SIEM | What suspicious activity was detected? |
| EDR | What happened on the endpoint? |
| Threat Intelligence | Has this indicator been associated with known malicious activity? |
| Log Management | Are other systems involved? |
| SOAR | What predefined investigation or response steps should be followed? |

The technologies provide different types of evidence. They work together to support a more complete investigation.

---

## 6. Key Terminology

| Term | Meaning |
|---|---|
| Endpoint | A device connected to a network |
| EDR | Endpoint Detection and Response |
| IOC | Indicator of Compromise |
| Parent process | A process that creates another process |
| Process tree | A representation of parent-child process relationships |
| Containment | Limiting the impact and spread of an incident |
| SOAR | Security Orchestration, Automation and Response |
| Playbook | A predefined investigation or response procedure |
| Threat Intelligence | Information about threats used to support security decisions |
| C2 | Command and Control |
| Sandbox | An isolated environment for analysing suspicious files |
| Static analysis | Examining a file without executing it |
| Dynamic analysis | Examining a file while it executes in a controlled environment |
| IOC hunting | Searching an environment for known indicators of compromise |

---

## 7. Key Takeaways

- EDR provides endpoint visibility and investigation capabilities.
- Process lists and network connections are important sources of endpoint evidence.
- IOC searches help identify suspicious indicators across multiple endpoints.
- Containment helps prevent compromised systems from causing further damage.
- SOAR integrates security products and automates repetitive tasks.
- Playbooks help standardise investigation procedures.
- Threat Intelligence provides context about known malicious indicators.
- VirusTotal results should not be treated as conclusive proof that a file is safe.
- Sandbox analysis can miss delayed or environment-dependent malware behaviour.
- Log analysis should cover the wider environment, not just the endpoint mentioned in an alert.
- Threat Intelligence results must be evaluated based on their freshness and context.

---

## 8. Knowledge Check

Use these questions to review the concepts from this session. Expand each answer when you are ready to check your understanding.

**1. An EDR alert identifies a suspicious executable on one workstation. How can I determine whether the same file exists on other endpoints?**

Search for the file hash across endpoints using the EDR IOC-search capability.

**2. A SIEM alert contains a suspicious IP. SOAR queries VirusTotal and returns zero detections. Can I close the alert as harmless?**

No. Zero detections do not prove that an indicator is safe. Further investigation and contextual evidence are necessary.

**3. A compromised endpoint is isolated through EDR. What is the primary objective?**

To limit unauthorised communication and lateral movement while preserving EDR management access where supported.

**4. Why should an analyst check the last analysis date in VirusTotal?**

Historical or cached results may not represent the current state of a file, domain, or IP address.

**5. Malware communicates with a suspicious domain. What should happen next?**

Search centralised logs for other devices communicating with the domain, then investigate related endpoint and network evidence.

---

## 9. Learning Reflection

In this lesson, I developed a better understanding of how SOC analysts use EDR, SOAR, and Threat Intelligence during security investigations.

The EDR section helped me understand the importance of endpoint visibility, especially process investigation, network connection monitoring, IOC searching, and endpoint isolation.

The SOAR section introduced me to automated investigation workflows and playbooks. I understood how automation can reduce repetitive tasks while maintaining consistency across SOC investigations.

The Threat Intelligence section helped me understand why external reputation sources are useful but should never be treated as the only source of evidence.

One important lesson I took away is that a SOC analyst should not depend entirely on automated tools or a single investigation result. Evidence must be correlated across endpoints, network activity, and available security logs. This lesson also connected with my previous studies involving Windows logging, Splunk, Mini EDR development, and network traffic analysis.

---
