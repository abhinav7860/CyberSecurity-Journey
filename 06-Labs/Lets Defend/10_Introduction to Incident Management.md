# Introduction to Incident Management

**LetsDefend study notes \| 18 November 2026**

## 1. What is incident management?

Incident management is the structured process an organization uses to
receive, assess, investigate, document, respond to, and close security
incidents.

The lesson references the National Cyber Security Centre (NCSC)
definition of a cyber incident as a breach of a system's security policy
intended to affect integrity or availability, and/or unauthorized access
or attempted access to a system or systems.

It also references NIST Special Publication 800-61, which describes an
incident as a violation or imminent threat of violation of computer
security policies, acceptable-use policies, or standard security
practices.

A SIEM collects and processes data and generates alerts. An Incident
Management System (IMS) helps the SOC organize the investigation, assign
ownership, record evidence and actions, and document the outcome.

## 2. Five basic definitions

### Alert

An **alert** is a notification generated when a SIEM or another security
product detects activity matching a configured rule or condition. The
alert is a reason to investigate, not automatic proof of an attack.

Example: A SIEM collects web logs, parses request fields, and detects a
request matching an SQL injection rule. It generates an alert and sends
it to the IMS.

### Event

An **event** is any observable occurrence in a system or network.

Examples: - A user connects to a file share. - A server receives a
web-page request. - A user sends an email. - A firewall blocks a
connection attempt.

Events are individual records of activity. Most events are normal; their
meaning depends on context and correlation.

### Incident

An **incident** is a violation, or imminent threat of violation, of
security policy, acceptable-use policy, or standard security practices.
It may involve many events, alerts, users, devices, and actions.

Examples include unauthorized account access, malware execution,
attempted exploitation, unauthorized privileged access changes, or
activity threatening confidentiality, integrity, or availability.

### True Positive

A **True Positive (TP)** occurs when an alert correctly identifies the
activity it was designed to detect.

Example: A detection is intended to identify SQL injection attempts. A
request contains an actual SQL injection payload and the rule correctly
triggers.

The lesson includes the SQL expression `' OR 1=1` in a URL example. The
analyst must examine the request and context; suspicious-looking text
alone is not enough to establish what happened.

### False Positive

A **False Positive (FP)** occurs when an alert triggers even though the
activity it was intended to detect is not present.

Example: A rule detects the keyword `Union` as a possible SQL injection
indicator. A normal URL about the football club FC Union Berlin contains
that word and triggers the rule. The alert is false positive because the
request is not an SQL injection attempt.

  -----------------------------------------------------------------------
  Classification          Meaning                 Example
  ----------------------- ----------------------- -----------------------
  True Positive           Alert correctly         A real SQL injection
                          identifies the activity attempt triggers the
                          it was designed to      rule
                          detect                  

  False Positive          Alert triggers on       A normal URL containing
                          benign activity         `Union` triggers a
                                                  keyword rule
  -----------------------------------------------------------------------

**Important:** A true-positive alert does not necessarily mean the
attack succeeded or that a system was compromised. A blocked SQL
injection attempt can be a true-positive detection even when the
application was not exploited.

Do not confuse: - **False Positive:** An alert is raised for benign
activity. - **False Negative:** The detection fails to alert on activity
it should have detected.

## 3. How an alert becomes a case

A simplified workflow:

1.  Systems and security products generate events.
2.  SIEM collects and processes the data.
3.  A detection rule matches activity and generates an alert.
4.  The alert is sent to an Incident Management System.
5.  A ticket or case is created.
6.  An analyst investigates and records evidence.
7.  The case is updated and closed according to the findings and
    process.

SIEM is primarily responsible for collecting, searching, and detecting.
The IMS organizes the investigation and its documentation.

## 4. Incident Management Systems (IMS)

An **Incident Management System** is a platform SOC teams use to manage
investigations and record actions taken when potential incidents occur.

Examples in the lesson: - **TheHive:** An open-source incident response
and case-management platform. - **LetsDefend Case Management:** The
case-management feature in the training environment.

An IMS can help teams: - Create and track cases. - Assign ownership. -
Record evidence and investigation notes. - Track status and actions. -
Attach alerts and observables. - Follow playbooks. - Integrate with
Threat Intelligence and SOAR. - Record final decisions and closure
details.

Case data can come from SIEM, EDR, email security, network security
products, or other integrated tools. A case may be created manually by
an analyst or automatically through an integration.

## 5. Threat Intelligence and SOAR integrations

### Threat Intelligence

Threat Intelligence (TI) provides context about indicators such as IP
addresses, domains, URLs, file hashes, malware families, and attacker
infrastructure.

The lesson's example is a suspicious domain, `letsdefend.io`. If the IMS
is integrated with a TI platform, the domain's reputation may be queried
automatically and attached to the case. Without an integration, the
analyst may check a source such as VirusTotal manually.

A reputation result is supporting context, not a final verdict. Results
may be incomplete, stale, or incorrect. Consider source reliability,
freshness, and the activity's context.

### SOAR

SOAR means **Security Orchestration, Automation, and Response**. It
connects security products and automates approved workflows.

The lesson lists integrations with: - Firewalls - IPS - WAF - Proxy -
Email gateways - Email security products

Example workflow: 1. An analyst investigates a suspicious domain. 2.
Evidence indicates that it is harmful. 3. The organization decides to
block access. 4. A SOAR workflow communicates with an integrated proxy
and requests the block. 5. The action and result are recorded.

Blocking must be authorized and validated. Incorrectly blocking a domain
or IP can disrupt legitimate services, especially when infrastructure is
shared.

### How the platforms work together

  Platform              Main role
  --------------------- --------------------------------------------------------------
  SIEM                  Collects and analyses data; generates alerts
  IMS                   Organizes cases, ownership, investigation notes, and actions
  Threat Intelligence   Adds context about indicators and threats
  SOAR                  Coordinates tools and automates approved response actions

## 6. Case creation in LetsDefend

The lesson's workflow: 1. Open the **Monitoring** page. 2. Review
available alerts. 3. Select an alert. 4. Click **Create Case**. 5. A new
record appears in **Case Management**. 6. Use the case to document the
investigation.

Creating a case moves the alert into a structured investigation process.

## 7. Case and alert naming

Consistent titles help analysts find historical records, review previous
investigations, and produce statistics.

The lesson's LetsDefend naming format is:

`EventID: {Alert ID Number} - [{Alert Name}]`

Other possible title fields include: 1. Alert category. 2. Event source.
3. Description.

A title such as `Suspicious Activity` is not very informative. A
consistent title containing the alert ID and name makes the record
easier to identify.

## 8. Playbooks

A **playbook** is a documented workflow that guides an analyst through
investigating a particular alert or incident type.

SOC alerts may involve web attacks, malware, ransomware, phishing,
endpoint activity, or authentication attacks. Each type requires
different checks. A playbook provides repeatable steps.

### Why playbooks matter

**Guidance:** A new analyst may not know every step. A playbook provides
a structured sequence and reduces the chance of missing important
checks.

**Consistency:** Different analysts may otherwise investigate the same
alert differently. For example, after analysing malware, one analyst may
check for command-and-control (C2) communication while another may
forget. A common playbook helps maintain team standards.

### Examples

A malware playbook may direct analysts to examine process execution,
file changes, registry activity, DNS queries, outbound connections, and
possible C2 communication.

A phishing playbook may guide analysts to review sender details,
headers, URLs, attachments, reputation, user interaction, and related
endpoint or identity activity.

The lesson references a Microsoft phishing playbook as an example.

### Playbook versus automation

-   **Manual playbook:** Guides an analyst through actions.
-   **Automated workflow:** Uses SOAR or integrations to execute
    approved tasks.
-   **Hybrid playbook:** Combines analyst decisions with automated
    collection or response.

A playbook standardizes the process; automation executes selected tasks.
Human review remains important for decisions requiring context or
authorization.

## 9. What a SOC analyst does when an alert occurs

The analyst reviews alerts generated by SIEM or other security products.
Not every alert is a real incident. Some are false positives, so
analysts must examine evidence and provide feedback to the detection
team.

### 9.1 Prioritize alerts

In a simulation, an analyst may choose any alert for practice. In a real
SOC, prioritize using factors such as: - Severity. - Asset
criticality. - Account privilege. - Detection confidence. - Potential
business impact. - Whether activity is ongoing. - Number of affected
systems.

The lesson specifically recommends starting with high-severity alerts in
real environments. Severity should not be the only factor; a
medium-severity alert affecting a critical identity system may deserve
urgent attention.

### 9.2 Take ownership

The **Take Ownership** function assigns responsibility for an alert and
helps avoid duplicate investigations.

The lesson's example: there are 10 active alerts. An analyst takes
ownership of Event ID 63. Other team members can see that it is being
handled and choose another alert.

In a real SOC, ownership may be manual, automatic, or queue-based.

### 9.3 Investigation Channel

In the LetsDefend workflow, an alert taken into ownership appears in the
**Investigation Channel**, where active investigations are managed.

The analyst opens the alert, reviews details, and determines whether the
activity is harmful or benign.

### 9.4 Create a case and follow the playbook

The analyst clicks **Create Case**, follows the assigned playbook,
reviews evidence, records observations, and completes the investigation
questions.

The playbook is guidance, not a substitute for understanding why each
check matters.

### 9.5 Make a final decision

After investigation, classify the alert as True Positive or False
Positive according to the evidence and the platform's available options.

Review: - What triggered the alert. - What the underlying event
represents. - User, host, IP, process, or URL context. - Correlated
events. - Whether the activity matches the detection's purpose.

Do not classify something as malicious merely because it contains a
suspicious keyword. Do not classify it as benign merely because it is
unfamiliar.

### 9.6 Close and review

The lesson describes selecting the classification, entering an
explanation, and closing the alert. It then moves to **Closed Alerts**.

LetsDefend provides an **Editor Note** and, where available, a
**Community Walkthrough**. These let learners compare their reasoning
with the provided analysis and discover missed steps.

In a real organization, the closed record should preserve evidence,
rationale, actions, and approvals according to policy.

## 10. False-positive analysis and feedback

The lesson emphasizes that analysts spend substantial time reviewing
false positives and should communicate feedback to the team responsible
for SIEM rules.

Common causes: - A keyword-based rule is too broad. - Legitimate
administrator activity resembles suspicious behaviour. - A vulnerability
scanner generates attack-like traffic. - A business application behaves
in an unexpected but legitimate way. - A rule uses incomplete or
outdated indicators.

Useful feedback should record: - Alert name or ID. - Triggering event or
search result. - Why the activity was legitimate. - Which field or
condition caused the match. - Whether the pattern may recur. - A
suggested tuning improvement, if known.

Possible improvements: - Add carefully designed exclusions. - Require
multiple indicators. - Improve field parsing. - Add asset or user
context. - Tune thresholds. - Restrict the rule to relevant sources. -
Clarify validation steps in the playbook.

Do not disable a detection simply because it produced a false positive.
It may still identify genuine attacks in other circumstances.

## 11. Important distinctions

  -----------------------------------------------------------------------
  Concept                             Meaning
  ----------------------------------- -----------------------------------
  Event                               Observable occurrence in a system
                                      or network

  Alert                               Notification generated when a
                                      detection condition is met

  Incident                            Violation or imminent threat of
                                      violation of security policy or
                                      practices

  Case/ticket                         Tracked record used to organize and
                                      document investigation

  True Positive                       Alert correctly identifies the
                                      activity it was designed to detect

  False Positive                      Alert triggers on activity that
                                      does not represent the suspected
                                      behaviour

  IMS                                 Platform for managing cases,
                                      evidence, ownership, and actions

  Playbook                            Documented investigation steps

  Threat Intelligence                 Context about indicators, threats,
                                      and attacker infrastructure

  SOAR                                Platform for coordinating and
                                      automating security workflows
  -----------------------------------------------------------------------

A single incident may involve many events and alerts. A case is the
record used to manage the investigation. These terms are not
interchangeable.

## 12. End-to-end example: possible SQL injection

1.  **Event:** A web server records an HTTP request containing
    suspicious input.
2.  **Detection:** A SIEM rule matches the request and generates an
    alert.
3.  **Case:** The alert is sent to the IMS or an analyst creates a case.
4.  **Ownership:** An analyst takes responsibility.
5.  **Playbook:** The analyst follows the web-attack investigation
    steps.
6.  **Evidence:** The analyst checks the request, target application,
    source, response, and related logs.
7.  **Classification:** The analyst decides whether the request was
    genuinely an SQL injection attempt.
8.  **Incident assessment:** The analyst determines whether there is
    evidence of successful exploitation or wider impact.
9.  **Response:** If required and authorized, the SOC coordinates
    containment or blocking.
10. **Closure:** The analyst records evidence, conclusion, actions, and
    final status.

A true-positive detection of an attack attempt does not automatically
prove that the application was compromised. The investigation must
establish what happened and what impact occurred.

