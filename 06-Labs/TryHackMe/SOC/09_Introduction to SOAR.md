# TryHackMe - Introduction to SOAR

**Date:** 2026-09-05\
**Room:** Introduction to SOAR\
**Platform:** TryHackMe

------------------------------------------------------------------------

## What this room was about

In this room, I learned about **SOAR**, which stands for **Security
Orchestration, Automation, and Response**.

SOAR is used in a SOC to connect different security tools and automate
repetitive tasks. The main goal is to reduce the amount of manual work
that SOC analysts have to do when handling alerts and incidents.

The main areas I covered were:

-   SOC challenges
-   How SOAR helps a SOC
-   Orchestration, automation and playbooks
-   Building SOAR playbooks
-   A practical threat intelligence automation lab

------------------------------------------------------------------------

# Task 1 - Introduction

## What is SOAR?

**SOAR = Security Orchestration, Automation, and Response**

SOAR platforms help security teams manage and respond to security
incidents more efficiently.

A SOC can receive a very large number of alerts every day. If analysts
have to manually investigate every alert and perform every action
themselves, it can take a lot of time.

SOAR helps by connecting security tools and automating repetitive steps.

For example, a SOAR workflow could:

1.  Receive a security alert.
2.  Extract an IP address or domain from the alert.
3.  Check the indicator against a threat intelligence service.
4.  Decide whether it looks malicious.
5.  Create or update a case.
6.  Block the malicious indicator if the workflow allows it.

The important thing I understood is that SOAR does not completely
replace the SOC analyst. It helps the analyst by handling repetitive and
predictable tasks.

------------------------------------------------------------------------

# Task 2 - Traditional SOC and Its Challenges

## What does a SOC do?

A Security Operations Center (SOC) is responsible for monitoring and
responding to security threats.

Some important SOC capabilities are:

### 1. Monitoring and Detection

The SOC continuously monitors systems, networks and security tools to
detect suspicious activity.

### 2. Recovery and Remediation

When an incident happens, the SOC works to contain the problem, remove
the threat and recover affected systems.

### 3. Threat Intelligence

Threat intelligence provides information about things such as:

-   Malicious IP addresses
-   Malicious domains
-   Malware hashes
-   Known attackers
-   Known vulnerabilities

### 4. Communication

SOC analysts need to communicate with other teams and keep track of
incidents and their progress.

------------------------------------------------------------------------

## Problems faced by traditional SOCs

### Alert Fatigue

A SOC can receive a huge number of security alerts.

When analysts have to deal with too many alerts, it becomes difficult to
identify the important ones. This is called **alert fatigue**.

### Disconnected Tools

A SOC normally uses many different tools, such as:

-   SIEM
-   EDR
-   Firewall
-   IAM
-   Threat intelligence platforms
-   Ticketing systems

If these tools are not connected, analysts may have to manually move
information between them.

### Manual Processes

Many SOC tasks can be repetitive.

For example, an analyst might repeatedly:

-   Copy an IP address
-   Search it in a threat intelligence platform
-   Create a ticket
-   Update the ticket
-   Block the IP
-   Inform another team

Doing this manually for every alert takes a lot of time.

### Talent Shortage

There are not enough skilled cybersecurity professionals to handle the
growing number of security events.

SOAR can help analysts use their time more effectively.

------------------------------------------------------------------------

## Question

**What is the overload of security events in a SOC called?**

**Answer:** `alert fatigue`

------------------------------------------------------------------------

# Task 3 - Overcoming SOC Challenges

SOAR helps solve many of the problems found in traditional SOC
environments.

## Orchestration

**Orchestration** means connecting different security tools and making
them work together as part of a single workflow.

For example:

**SIEM → SOAR → Threat Intelligence → Firewall → Ticketing System**

Instead of an analyst manually moving information between each tool,
SOAR can connect them.

------------------------------------------------------------------------

## Playbook

A **playbook** is a predefined list of actions that should be performed
for a particular type of security incident.

For example, a phishing playbook could contain steps such as:

1.  Receive a phishing alert.
2.  Extract the URL.
3.  Check the URL reputation.
4.  Check the attachment hash.
5.  Decide whether the email is malicious.
6.  Remove the email if necessary.
7.  Update the incident ticket.

The playbook provides a structured process for handling the incident.

------------------------------------------------------------------------

## Automation

Automation means allowing the SOAR platform to perform predefined
actions automatically.

For example, if a known malicious IP is detected, the SOAR platform
could automatically send it to a firewall and block it.

This saves the analyst from doing repetitive work manually.

------------------------------------------------------------------------

## Response

Response is the actual action taken to deal with the security incident.

Depending on the workflow, this could include:

-   Blocking an IP
-   Blocking a domain
-   Removing a malicious email
-   Disabling an account
-   Creating a ticket
-   Updating an incident

------------------------------------------------------------------------

## Does SOAR replace SOC analysts?

No.

SOAR can automate repetitive and predictable actions, but analysts are
still needed for situations that require human judgement.

An analyst may need to:

-   Investigate unusual behaviour
-   Validate automated results
-   Decide whether an alert is actually malicious
-   Approve potentially dangerous actions
-   Create or modify playbooks

So I understood SOAR more as a tool that **assists SOC analysts**,
rather than replacing them.

------------------------------------------------------------------------

## Questions

### Connecting and integrating security tools into seamless workflows

**Answer:** `orchestration`

### A predefined list of actions

**Answer:** `playbook`

------------------------------------------------------------------------

# Task 4 - Building SOAR Playbooks

In this task, I learned how SOAR playbooks can be used to handle
different types of security incidents.

------------------------------------------------------------------------

## Phishing Playbook

A phishing playbook can automate many of the repetitive investigation
steps involved in handling suspicious emails.

### General workflow

1.  A suspicious email is received.
2.  A case/investigation ticket is created.
3.  The email attachments and URLs are checked.
4.  If there is an attachment, its hash can be calculated.
5.  The hash can be checked against VirusTotal or another threat
    intelligence service.
6.  If there is a URL, the URL can also be checked.
7.  If the automated checks do not provide enough information, manual
    analysis or sandbox analysis can be performed.
8.  If the email is confirmed as malicious, it can be deleted.
9.  The relevant IOCs are added to the investigation ticket.
10. Users can be notified when necessary.

The important idea is that the repetitive investigation steps can be
automated, while uncertain or high-impact decisions can still involve an
analyst.

------------------------------------------------------------------------

## CVE Patching Playbook

A SOAR playbook can also help automate vulnerability management.

### General workflow

1.  Monitor security advisory lists.
2.  Detect a new CVE.
3.  Extract the CVE information.
4.  Query the patch management system.
5.  Check whether the vulnerability has already been addressed.
6.  If it has already been fixed, the workflow can end.
7.  If it has not been fixed, create a CVE ticket.
8.  Assign the ticket to an analyst.
9.  The analyst reviews the vulnerability.
10. Identify affected assets.
11. Check whether a patch is available.
12. Update the patch management database if necessary.
13. Create test machines.
14. Apply the patch to the test machines.
15. Check performance and other metrics.
16. Update the ticket.
17. Deploy the patch.
18. Verify the rollout.
19. Scan the assets again.
20. If assets are still vulnerable, create a mitigation plan.
21. If everything is fixed, close the ticket and update the patch
    management system.

This showed me that SOAR can also be useful outside of just alert
investigation. It can help automate parts of vulnerability management as
well.

------------------------------------------------------------------------

## Questions

### Is manual analysis vital in some situations?

**Answer:** `yay`

### Where does the CVE information come from?

**Answer:** `advisory lists`

### What should be developed if assets remain vulnerable after patching?

**Answer:** `mitigation plan`

------------------------------------------------------------------------

# Task 5 - Threat Intel Workflow Practical

This was the practical SOAR lab where I had to configure different
automation settings and then run the workflow to get the flag.

The main idea was to decide **which tasks should be automated and which
tasks should remain manual for a SOC analyst**.

## Goal

I had to configure these five sections:

1.  Case Ticket
2.  Threat Intel
3.  Data Extraction
4.  Reputation Checks
5.  Course of Action

After configuring the workflow correctly, I ran it and got the flag.

------------------------------------------------------------------------

## 1. Case Ticket

### Set to automated

-   Create Case Ticket
-   Assign Case Ticket
-   Communicate Case Ticket
-   Update Case Ticket

### Keep manual

-   Delete Case Ticket

### Why?

Creating, assigning, communicating and updating tickets are repetitive
tasks, so they can be automated.

Deleting a case should remain manual because accidentally deleting an
important investigation could cause problems.

------------------------------------------------------------------------

## 2. Threat Intel

### Set to automated

-   Fetch Threat Intelligence
-   Fetch Interval
-   Failed Fetches

### Keep manual

-   Discard Old Alerts

### Why?

Fetching and processing threat intelligence is repetitive and suitable
for automation.

Discarding old alerts should involve analyst review because an alert
should not simply be removed without considering whether it is still
relevant.

------------------------------------------------------------------------

## 3. Data Extraction

### Set to automated

-   Extract Domains
-   Extract IPs
-   Extract URLs

### Keep manual

-   Analyst Extraction

### Why?

Extracting common indicators of compromise (IOCs), such as domains, IP
addresses and URLs, is repetitive work and can be automated.

However, unusual or unknown data may require analyst judgement.

------------------------------------------------------------------------

## 4. Reputation Checks

### Set to automated

-   Reputation Results Output

### Keep manual

-   Reputation Validation
-   Reputation Confirmation
-   Sandbox Testing

### Why?

SOAR can automatically collect and output reputation results from
security services.

However, automated reputation results should not always be blindly
trusted.

Validation, confirmation and sandbox testing can require analyst
judgement, especially when the result could lead to a blocking or
containment action.

------------------------------------------------------------------------

## 5. Course of Action

### Set to automated

-   Block Domains
-   Block IPs
-   Block URLs
-   Update Case Ticket

### Keep manual

-   Analyst Approval COA

### Why?

Blocking known malicious indicators and updating the case are repetitive
actions that can be automated.

However, the final approval should remain with the SOC analyst because
blocking something incorrectly could affect legitimate users or systems.

------------------------------------------------------------------------

# Running the Workflow

After configuring all five sections, I ran the workflow.

### Steps I followed

1.  Checked the automation/manual settings.
2.  Started the workflow.
3.  Followed the workflow flowchart.
4.  Made sure the different stages transitioned correctly.
5.  If a stage did not progress, I checked the automation settings.
6.  Once the workflow completed successfully, the flag was displayed.

------------------------------------------------------------------------

## Flag

``` text
THM{AUT0M@T1N6_S3CUR1T¥}
```

------------------------------------------------------------------------

# What I learned from this room

The main thing I understood from this room is that **SOAR is not about
automating absolutely everything**.

The repetitive and predictable tasks can be automated, while actions
involving things such as:

-   Deletion
-   Validation
-   Confirmation
-   Unknown threats
-   Final approval

can still require a SOC analyst.

This helps reduce **alert fatigue** and gives analysts more time to
focus on actual investigation and decision-making.

I also understood the difference between the main SOAR concepts:

  -----------------------------------------------------------------------
  Concept                             What I understood
  ----------------------------------- -----------------------------------
  **Orchestration**                   Connecting different security tools
                                      and workflows

  **Playbook**                        A predefined sequence of actions

  **Automation**                      Automatically executing repetitive
                                      actions

  **Response**                        Taking action against the security
                                      incident
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Final Takeaway

SOAR acts like a bridge between the different tools used by a SOC.

A simple example of a SOAR workflow could look like:

``` text
Security Alert
      ↓
Create Case
      ↓
Extract IOC
      ↓
Threat Intelligence Check
      ↓
Reputation Check
      ↓
Analyst Decision / Approval
      ↓
Block Malicious IOC
      ↓
Update Case
```

The biggest takeaway for me was that **automation should reduce
repetitive work, not remove human judgement from important security
decisions.**
