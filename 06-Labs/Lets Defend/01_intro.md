# LetsDefend SOC Fundamentals
## 01 - Introduction to SOC

**Platform:** LetsDefend  
**Study Date:** 29 October 2026  
**Topic:** Introduction to Security Operations Center (SOC)

---

## 1. Introduction

Today, I started studying SOC Fundamentals on the LetsDefend platform.

This lesson introduced the structure of a Security Operations Center, its different operating models, SOC roles, analyst responsibilities, and the security tools used during investigations.

The main objective of this lesson was to understand how a SOC operates and how security analysts use tools such as SIEM, Log Management, EDR, and SOAR to detect and investigate security threats.

I learned that working as a SOC analyst requires more than monitoring security alerts. Analysts must understand operating systems, networking, security logs, detection techniques, and investigation procedures.

## 2. What is a SOC?

A Security Operations Center (SOC) is a team responsible for monitoring an organization's security environment, detecting suspicious activities, investigating security alerts, and responding to cybersecurity incidents.

The primary objectives of a SOC are:

- Monitor the organization's security environment.
- Detect suspicious and malicious activities.
- Investigate security alerts.
- Identify potential security incidents.
- Support incident response and remediation.
- Improve security monitoring and detection.

A SOC combines people, processes, and technology to maintain the organization's security.

## 3. Types of SOC

### In-house SOC

An in-house SOC is operated by an organization's internal security team.

The organization manages its security analysts, infrastructure, security tools, and operational processes.

### Virtual SOC

A virtual SOC operates without requiring all analysts to work from one permanent physical facility.

Analysts may work remotely from different locations.

### Co-managed SOC

A co-managed SOC combines an organization's internal security team with an external security provider.

Both teams coordinate their security operations and responsibilities.

### Command SOC

A command SOC provides centralized coordination or oversight for multiple SOC teams or security operations across different locations.

## 4. People, Process, and Technology

A successful SOC requires three important components.

### People

SOC personnel monitor alerts, investigate suspicious activities, manage security technologies, and coordinate incident response.

Security analysts must continuously improve their knowledge because attack techniques and security threats change over time.

### Process

Processes define how security operations are performed.

Examples include:

- Alert triage procedures.
- Incident escalation procedures.
- Incident response workflows.
- Security investigation documentation.
- Detection and response standards.

Standardized processes help ensure that investigations are consistent and important steps are not missed.

### Technology

SOC teams use security technologies to collect data, detect threats, investigate incidents, and support response activities.

Examples include SIEM, EDR, Log Management, and SOAR.

The most suitable security technology depends on the organization's requirements, infrastructure, operational needs, and budget.

**Key takeaway:** A successful SOC requires trained personnel, standardized processes, and suitable security technologies working together.

## 5. SOC Roles

### SOC Analyst

SOC analysts monitor security alerts, investigate suspicious activities, classify findings, and escalate incidents when necessary.

SOC analysts are commonly organized into different levels.

- L1: Initial alert monitoring, triage, and escalation.
- L2: Detailed investigation and incident analysis.
- L3: Advanced investigations and specialized security analysis.

Responsibilities vary depending on the organization.

### Incident Responder

Incident responders investigate and handle security incidents.

Their responsibilities may include containment, eradication, recovery, and coordinating incident response activities.

### Threat Hunter

Threat hunters proactively search for suspicious activities that may not have generated security alerts.

They use security logs, endpoint information, network data, and threat intelligence to identify potential threats.

### Security Engineer

Security engineers design, configure, integrate, and maintain security infrastructure.

For example, they may configure SIEM integrations, maintain security detection systems, and develop automated security workflows.

### SOC Manager

SOC managers oversee SOC operations, staffing, budgets, priorities, and team performance.

They coordinate the operational activities of the security team.

## 6. SOC Analyst Responsibilities

A SOC analyst is often the first person to investigate a security alert.

The analyst must determine whether the activity is suspicious, benign, or potentially malicious.

Typical responsibilities include:

1. Review security alerts.
2. Identify the affected systems and users.
3. Examine relevant security logs.
4. Investigate suspicious network and endpoint activity.
5. Determine whether the alert represents a security threat.
6. Escalate confirmed or suspected incidents when required.
7. Document investigation findings.

### Event, Alert, and Incident

An event is an activity recorded by a system.

An alert is a notification generated when activity matches a detection rule or condition.

An incident is a security event or series of events that requires investigation and response because it may compromise security.

Not every event becomes an alert, and not every alert represents a confirmed incident.

## 7. Skills Required for a SOC Analyst

### Operating Systems

I need to understand how Windows and Linux systems normally operate.

Important areas include:

- Processes and services.
- User accounts and permissions.
- System logs.
- Process execution.
- Operating system behavior.
- Suspicious system activity.

Understanding normal system behavior helps me identify unusual or potentially malicious activity.

### Networking

Networking knowledge is important when investigating suspicious IP addresses, URLs, and network connections.

Important concepts include:

- IP addressing.
- TCP and UDP.
- Ports and protocols.
- DNS.
- HTTP and HTTPS.
- Firewall behavior.
- Network traffic analysis.

An analyst should understand which devices communicate with suspicious destinations and whether those connections indicate malicious activity.

### Malware Analysis

Malware analysis helps identify the behavior and purpose of malicious software.

Important investigation areas include:

- File hashes.
- Process behavior.
- Suspicious executable files.
- Network connections.
- Persistence mechanisms.
- Command-and-control communication.

Command and Control (C2) infrastructure allows attackers to communicate with or control compromised systems.

Identifying suspicious C2 communication can help determine whether an endpoint is compromised.

## 8. What is SIEM?

SIEM stands for Security Information and Event Management.

A SIEM collects security-related logs and events from different sources, analyzes the collected information, and helps detect suspicious activities.

Common sources include:

- Windows and Linux systems.
- Firewalls.
- Network devices.
- Applications.
- Endpoint security products.
- Authentication systems.

Popular SIEM solutions include Splunk, IBM QRadar, ArcSight, and FortiSIEM.

### SIEM Detection Rules

SIEM detection rules identify activity that matches predefined conditions.

For example, a rule may detect repeated failed login attempts within a short period.

If an account experiences 20 failed login attempts within 10 seconds, the SIEM may generate an alert.

This activity could indicate a brute-force attack.

However, repeated failed logins can also occur because of legitimate issues, such as an expired password or a misconfigured application.

Therefore, the analyst must investigate the activity before determining whether it is malicious.

### SIEM and SOC Analyst Relationship

The SIEM generates alerts based on collected events and detection rules.

The SOC analyst investigates those alerts using available security tools and evidence.

The analyst determines whether the activity is malicious, benign, or requires further investigation.

The SIEM supports detection, but the analyst is responsible for evaluating the evidence and making an appropriate classification.

## 9. Alert Ownership and Investigation

LetsDefend provides a simulated SOC environment where analysts can work with security alerts.

The Main Channel contains shared alerts.

When an analyst selects an alert and takes ownership, the alert is assigned to that analyst for investigation.

This helps the SOC team:

- Identify who is investigating an alert.
- Avoid duplicate investigations.
- Coordinate alert handling.
- Track investigation progress.

The analyst can review alert details such as hostname, IP address, file hashes, and other available evidence.

Taking ownership is an important part of organizing security investigations.

## 10. False Positive Example

A SIEM rule may generate alerts whenever a URL contains the keyword `union`.

This keyword can be associated with SQL injection attacks.

However, a legitimate user may search for SQL information using a URL containing the same keyword.

The SIEM may generate an alert even though the activity is benign.

This demonstrates that detection rules can sometimes generate false positives.

A SOC analyst should examine the request context, identify the reason for the alert, and determine whether the activity represents an actual threat.

If the rule is too broad, the analyst can provide feedback to the detection team.

**Key takeaway:** An alert is an indication that activity requires investigation. It is not automatic proof of malicious activity.

## 11. What is Log Management?

Log Management provides access to collected logs from different systems and security devices.

It allows analysts to search and examine information from multiple sources in one place.

Common log sources include:

- Windows.
- Linux.
- Firewall.
- Proxy.
- Email systems.
- EDR.

Centralized log access makes investigations more efficient because analysts do not need to manually access every individual system.

### SIEM vs. Log Management

SIEM primarily focuses on security monitoring, detection, and alert generation.

Log Management primarily focuses on collecting, organizing, storing, and searching logs.

These capabilities can overlap because many SIEM products also provide centralized log management and search functionality.

## 12. Practical Investigation: Suspicious IP Address

LetsDefend introduced an example involving a suspicious IP address:

`122.194.229.59`

A security alert indicates that a device may be communicating with this address and potentially leaking data.

The analyst should investigate the suspicious destination and determine whether other devices are communicating with it.

### Investigation Approach

1. Review the security alert.
2. Identify the affected hostname and IP address.
3. Examine the suspicious destination IP.
4. Search the destination IP in Log Management.
5. Identify other devices communicating with the same destination.
6. Examine the available network and endpoint evidence.
7. Determine whether the activity is suspicious or malicious.
8. Document the findings and escalate when required.

### Why Search Other Devices?

An alert may identify only one affected endpoint.

However, other devices may also be communicating with the same suspicious destination.

Searching centralized logs helps identify additional systems that may require investigation.

This helps the analyst understand the potential scope of the activity instead of focusing only on the original alert.

## 13. Security Tools and Their Purposes

| Tool | Purpose |
|---|---|
| SIEM | Collects security events, detects suspicious activity, and generates alerts. |
| Log Management | Provides centralized access to logs for investigation. |
| EDR | Monitors endpoint activity, detects threats, and supports endpoint investigation and response. |
| SOAR | Automates and coordinates security workflows and response activities. |

These tools support different parts of the SOC investigation process.

A SOC analyst uses the available evidence from these tools to understand suspicious activity and determine the appropriate next action.

## 14. Key Takeaways

From this lesson, I learned:

- A SOC monitors, detects, investigates, and responds to security threats.
- A successful SOC requires people, processes, and technology.
- SOC teams can operate using different organizational models.
- SOC analysts investigate alerts and determine whether activity is suspicious or malicious.
- SIEM solutions detect suspicious activity and generate alerts.
- Log Management helps analysts investigate activity across multiple systems.
- EDR provides endpoint visibility and supports endpoint investigations.
- SOAR helps automate and coordinate security workflows.
- Detection rules can generate false positives.
- Analysts must investigate the context before classifying alerts.
- Searching for suspicious indicators across multiple devices helps identify the potential scope of an incident.

## 15. Personal Learning Reflection

Today, I started learning SOC Fundamentals through LetsDefend.

This lesson helped me understand how a Security Operations Center operates and how SOC analysts use security tools during investigations.

I learned the difference between SIEM and Log Management and understood why analysts need to investigate alerts instead of automatically treating every alert as a confirmed threat.

The suspicious IP address example helped me understand the importance of searching centralized logs to identify other devices communicating with the same destination.

I also learned how alert ownership helps SOC teams coordinate their investigations.

This lesson connected with my previous learning in networking, Windows logging, Splunk, SIEM, and defensive security.

My next step is to continue studying the technical side of SOC operations and apply these concepts through LetsDefend practical exercises.

---

