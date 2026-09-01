# SOC Fundamentals – TryHackMe

## Part 1 – Purpose, People, Process & Technology

### Purpose and Components

The main focus of a **SOC (Security Operations Center)** is **Detection and Response**.

A SOC continuously monitors an organization's network, systems, and security solutions from a centralized location so that security incidents can be detected and responded to quickly.

### Detection

The SOC can detect:

- **Vulnerabilities** – weaknesses that attackers can exploit.
- **Unauthorized activity** – suspicious or unauthorized logins or actions.
- **Policy violations** – activities that go against an organization's security policies.
- **Intrusions** – unauthorized access to systems or networks.

### Response

Once an incident is detected, the SOC supports the **incident response** process by helping minimize the impact and investigate the root cause.

### Three Pillars of a SOC

1. **People**
2. **Process**
3. **Technology**

These three work together to make a SOC effective at detecting and responding to security incidents.

---

## People

People are still important even when security tools and automation are being used. Security solutions can generate a lot of alerts, and analysts are needed to determine which alerts are actually harmful.

### SOC Roles

**SOC Analyst – Level 1**
- First responder to alerts.
- Performs basic alert triage.
- Determines whether an alert is harmful.
- Reports/escalates relevant detections.

**SOC Analyst – Level 2**
- Performs deeper investigation.
- Correlates information from multiple sources.
- Helps Level 1 analysts investigate suspicious activity.

**SOC Analyst – Level 3**
- More experienced analyst.
- Performs proactive threat hunting.
- Supports incident response activities.

**Security Engineer**
- Deploys and configures security solutions.
- Makes sure the security tools work properly.

**Detection Engineer**
- Works on the rules and logic used to detect suspicious activity.
- Helps establish alerting rules for security solutions.

**SOC Manager**
- Manages SOC processes and supports the SOC team.
- Communicates the SOC's security posture and activities to the CISO.

> The roles can vary depending on the size and requirements of the organization.

---

## Process

### Alert Triage

Alert triage is one of the basic processes in a SOC.

The analyst investigates an alert and determines its severity and priority.

A useful way to approach an alert is the **5 Ws**:

- **What?** – What happened?
- **When?** – When did it happen?
- **Where?** – Where did it happen?
- **Who?** – Who was involved?
- **Why?** – Why did it happen?

### Reporting

Harmful alerts are escalated to the appropriate analysts through tickets.

A report should contain the relevant **5 Ws**, investigation details, and evidence such as screenshots when appropriate.

### Incident Response and Forensics

Some detections can indicate serious malicious activity.

In these cases, higher-level teams may start an **incident response** process.

Forensics can also be required to investigate system or network artifacts and determine the root cause of an incident.

---

## Technology

Technology refers to the security solutions used by the SOC to improve detection and response.

### SIEM

**SIEM – Security Information and Event Management**

A SIEM collects logs from different devices and systems.

It can use detection rules to identify suspicious activity by correlating information from multiple log sources.

> **SIEM provides Detection capabilities in a SOC environment.**

### EDR

**EDR – Endpoint Detection and Response**

EDR provides visibility into endpoint activity.

It can help analysts investigate endpoint activity and perform automated responses.

### Firewall

A **firewall** monitors incoming and outgoing network traffic.

It acts as a barrier between internal and external networks and can filter unauthorized or suspicious traffic.

Other security technologies can also be used in a SOC, such as:

- Antivirus
- EPP
- IDS/IPS
- XDR
- SOAR

---

## Questions I Answered

### 1. The SOC team discovers an unauthorized user trying to log in to an account. Which capability is this?

**Answer:** Detection

### 2. What are the three pillars of a SOC?

**Answer:** People, Process, Technology

### 3. Alert triage and reporting is the responsibility of?

**Answer:** SOC Analyst – Level 1

### 4. Which role works on establishing rules for alerting security solutions?

**Answer:** Detection Engineer

### 5. John attempted to steal the system's data. Which 'W' does this answer?

**Answer:** Who

### 6. The SOC detected a large amount of data exfiltration. Which 'W' does this answer?

**Answer:** What

### 7. Which security solution monitors incoming and outgoing network traffic?

**Answer:** Firewall

---

## My Takeaway

Today I learned the basic structure of a **SOC** and how its **People, Process and Technology** work together.

The main goal of a SOC is **Detection and Response**.

I also learned about different SOC roles, especially the responsibilities of Level 1, Level 2 and Level 3 analysts, Security Engineers, Detection Engineers and SOC Managers.

For the process side, I learned about **alert triage, the 5 Ws, reporting, incident response and forensics**.

On the technology side, I learned the basic purpose of **SIEM, EDR and Firewalls**.

The main things I want to remember:

> **SOC = Detection + Response**

> **3 Pillars = People + Process + Technology**

> **L1 = First-level alert triage**

> **SIEM = Detection**

> **Firewall = Monitors incoming and outgoing traffic**

---


# Part 2 – Practical Exercise of SOC

## Scenario

This practical exercise uses **People, Processes, and Technology** and gives a practical walkthrough of the role of a **Level 1 SOC Analyst**.

In the scenario, an alert is received that **port scanning activity** has been observed on a host in the network.

The vulnerability assessment team reported that they were running a port scan from the host:

`10.0.0.8`

As a Level 1 SOC Analyst, the task was to investigate the alert using the available **SIEM** solution and answer the **5 Ws**.

---

## Alert Investigation – 5 Ws

### What? – Activity that triggered the alert

**Port Scan**

The alert was triggered because port scanning activity was detected.

### When? – Time of the activity

**June 12, 2024 17:24**

### Where? – Destination host IP

**10.0.0.3**

### Who? – Source host name

**Nessus**

### Why? – Reason for the activity

**Intended**

The activity was part of an intended vulnerability assessment rather than a malicious attack.

---

## Additional Investigation

### Has any response been sent back to the port scanner IP?

**Yes**

---

## Alert Closure

After investigating the alert and confirming that the port scan was intentional, the alert could be closed.

### Flag

`THM{000_INTRO_TO_SOC}`

---

## What I Learned

This practical exercise helped me understand how a **Level 1 SOC Analyst** handles an alert in practice.

The main process was:

1. Receive the alert.
2. Identify the activity that triggered it.
3. Investigate the **5 Ws**.
4. Check the source and destination information.
5. Determine whether the activity was **intended or malicious**.
6. Check for any response to the activity.
7. Close the alert after completing the investigation.

The important part for me was understanding that **not every alert is malicious**. A port scan can look suspicious, but in this scenario it was caused by the vulnerability assessment team using **Nessus**, so the activity was intended.

This is why **alert triage** is important in a SOC — the analyst needs to investigate the available information before deciding how an alert should be handled.

---

## Quick Notes

| Question | Answer |
|---|---|
| What? | Port Scan |
| When? | June 12, 2024 17:24 |
| Where? | 10.0.0.3 |
| Who? | Nessus |
| Why? | Intended |
| Response sent back? | Yes |
| Flag | `THM{000_INTRO_TO_SOC}` |

---
