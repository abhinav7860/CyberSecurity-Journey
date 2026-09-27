# The Unified Kill Chain --- Detailed Notes

**Date:** 27 September 2026\
**Room:** TryHackMe --- Unified Kill Chain\
**Focus:** Understanding the 18 phases of the Unified Kill Chain (UKC)

------------------------------------------------------------------------

## 1. Introduction

In this room, I learned about the **Unified Kill Chain (UKC)** and how
it can be used to understand an attack from the very beginning to the
attacker's final objective.

The main idea I took from the room is simple:

> An attack is not just one action. It is a chain of actions that can
> happen in different stages, and attackers can move backward and
> forward between those stages.

The UKC helps me break a complicated attack into smaller pieces. As a
SOC analyst, this is useful because I can look at an alert or an event
and ask:

-   Where does this activity fit in the attack?
-   What happened before it?
-   What happened after it?
-   What evidence should I look for next?
-   At which stage can the attack be detected or disrupted?

The room explains that the UKC contains **18 phases**. These phases are
grouped into three major goals:

1.  **In --- Initial Foothold**
2.  **Through --- Network Propagation**
3.  **Out --- Action on Objectives**

The important thing is that the UKC is not necessarily a straight line.
An attacker may move through several phases, return to an earlier phase,
and repeat phases when moving to another machine.

------------------------------------------------------------------------

# 2. What Is a Kill Chain?

The term **Kill Chain** originally came from the military. It describes
the different stages involved in identifying, engaging, and completing
an attack against a target.

In cybersecurity, a Kill Chain describes the **methodology or path an
attacker uses to approach and compromise a target**.

For example, a simple attack could look like:

``` text
Reconnaissance
      ↓
Find a vulnerable web application
      ↓
Exploit the vulnerability
      ↓
Execute code
      ↓
Escalate privileges
      ↓
Access sensitive data
```

All of these steps together form part of the attacker's Kill Chain.

## Why is the Kill Chain useful?

The objective is not only to understand what the attacker did. It is
also to understand **where defenders can interrupt the attack**.

For example:

-   Reconnaissance can reveal suspicious scanning.
-   Exploitation can generate IDS/WAF alerts.
-   Persistence can create suspicious services or scheduled tasks.
-   Discovery can generate unusual process or command activity.
-   Credential Access can produce credential-dumping indicators.
-   Lateral Movement can generate unusual authentication events.
-   Exfiltration can create abnormal network traffic.

This gives a SOC analyst a structured way to investigate an incident
rather than looking at individual alerts in isolation.

------------------------------------------------------------------------

# 3. What Is Threat Modelling?

**Threat modelling** is a process used to understand the security risks
of a system, application, or environment.

The room breaks the process down into four main ideas.

## Step 1 --- Identify the assets

First, I need to understand what needs protection.

Examples include:

-   Servers
-   Workstations
-   Web applications
-   Databases
-   User accounts
-   Network devices
-   Customer information
-   Payment information

I also need to understand how important each asset is to the
organisation.

For example, losing access to a public test server may be less serious
than losing access to a database containing customer information.

## Step 2 --- Identify vulnerabilities and weaknesses

Next, I look for weaknesses that could potentially be abused.

Examples include:

-   Vulnerable software
-   Weak passwords
-   Misconfigurations
-   Exposed services
-   Missing security controls
-   Insecure application functionality
-   Poor access control

## Step 3 --- Create a security plan

After identifying the weaknesses, I need to decide how they should be
addressed.

For example:

``` text
Weak password policy
        ↓
Improve password requirements
        ↓
Enable MFA where appropriate
        ↓
Monitor authentication events
```

## Step 4 --- Prevent the same problem from happening again

The final step is to introduce policies and processes that reduce the
chance of the same vulnerability returning.

Examples include:

-   Secure development practices
-   Software Development Life Cycle (SDLC)
-   Security awareness training
-   Patch management
-   Access-control policies
-   Monitoring and logging

## Threat modelling frameworks mentioned in the room

The room mentions several frameworks and approaches used in threat
modelling:

-   **STRIDE**
-   **DREAD**
-   **CVSS**

The important point for me is that threat modelling is about
understanding **what needs protection, how it could be attacked, and how
to reduce the risk**.

------------------------------------------------------------------------

# 4. Introducing the Unified Kill Chain

The Unified Kill Chain was created by **Paul Pols** and was published in
**2017**. The room explains that it is intended to complement other
cybersecurity frameworks, including the Lockheed Martin Cyber Kill Chain
and MITRE ATT&CK, rather than compete with them.

The UKC contains **18 phases** covering an attack from:

``` text
Reconnaissance
      ↓
Initial access / foothold
      ↓
Persistence and control
      ↓
Internal discovery and privilege changes
      ↓
Credential access and lateral movement
      ↓
Collection and exfiltration
      ↓
Impact / attacker objectives
```

One of the important advantages explained in the room is the level of
detail.

The room describes the UKC as:

-   Modern
-   Detailed
-   Covering the entire attack
-   Able to represent realistic attacker behaviour
-   Able to represent attackers returning to earlier phases

For example, after compromising one server, an attacker might perform
**Discovery** again to find another system. They could then **Pivot**,
perform **Privilege Escalation**, and continue the attack.

Therefore, the UKC should not be viewed as a simple one-way checklist.

------------------------------------------------------------------------

# 5. The 18 Unified Kill Chain Phases

The 18 phases covered in the room are:

  \#   Phase                  Goal
  ---- ---------------------- --------------
  1    Reconnaissance         In
  2    Weaponization          In
  3    Delivery               In
  4    Social Engineering     In
  5    Exploitation           In
  6    Persistence            In
  7    Defence Evasion        In
  8    Command & Control      In
  9    Pivoting               In / Through
  10   Discovery              Through
  11   Privilege Escalation   Through
  12   Execution              Through
  13   Credential Access      Through
  14   Lateral Movement       Through
  15   Collection             Out
  16   Exfiltration           Out
  17   Impact                 Out
  18   Objectives             Out

The sections below explain every phase in detail.

------------------------------------------------------------------------

# 6. Goal: IN --- Initial Foothold

The **In** section is mainly about getting into the target environment
and establishing a foothold.

The room explains that attackers can use reconnaissance to discover
potential attack paths, exploit weaknesses, establish persistence, evade
defensive controls, establish command and control, and pivot toward
other systems.

The phases in this section are:

1.  Reconnaissance
2.  Weaponization
3.  Delivery
4.  Social Engineering
5.  Exploitation
6.  Persistence
7.  Defence Evasion
8.  Command & Control
9.  Pivoting

------------------------------------------------------------------------

# 7. Phase 1 --- Reconnaissance

## What is Reconnaissance?

**Reconnaissance** is the process of gathering information about a
target before or during an attack.

The attacker wants to learn as much as possible about the target
environment.

The room explains that reconnaissance can be:

-   **Passive**
-   **Active**

### Passive reconnaissance

The attacker gathers information without directly interacting with the
target in an obvious way.

Examples include researching:

-   Public websites
-   Employee information
-   Public documents
-   Public DNS information
-   Publicly available technology information
-   Information about an organisation's infrastructure

### Active reconnaissance

The attacker directly interacts with the target environment.

Examples include:

-   Port scanning
-   Service enumeration
-   Host discovery
-   Web application enumeration

## What information is useful?

The room specifically highlights information such as:

### Systems and services

Knowing what systems and services are running helps the attacker
identify possible attack paths.

For example:

``` text
Target
  ├── Web Server
  ├── SSH
  ├── RDP
  └── Database
```

The attacker can then investigate which of these may contain weaknesses.

### Employees and contacts

Employee information can be useful for social engineering and phishing
attacks.

### Credentials

Attackers may search for information that could eventually help them
obtain credentials.

### Network topology

Understanding how systems connect to one another helps attackers
identify possible paths for pivoting.

## SOC perspective

As a defender, reconnaissance can sometimes be detected through:

-   Port scans
-   Large numbers of connection attempts
-   Web enumeration
-   DNS queries
-   Repeated requests to many endpoints
-   Unusual external activity against public infrastructure

------------------------------------------------------------------------

# 8. Phase 2 --- Weaponization

## What is Weaponization?

**Weaponization** is the preparation of the infrastructure and resources
needed to conduct the attack.

The attacker has identified a possible target and now prepares the
things needed to carry out the attack.

The room gives examples such as preparing:

-   Command-and-control infrastructure
-   A system capable of receiving reverse shells
-   Payload-delivery infrastructure
-   Malicious files or other attack resources

A simple way to understand this is:

``` text
Reconnaissance = "Who/what can I attack?"

Weaponization = "What do I need to attack it?"
```

## SOC perspective

Defenders may look for:

-   Newly registered or suspicious domains
-   Suspicious infrastructure
-   Malware hosting
-   Unusual external servers
-   Threat-intelligence indicators

------------------------------------------------------------------------

# 9. Phase 3 --- Delivery

## What is Delivery?

**Delivery** is the stage where the weaponized object or payload is
transmitted to the target environment.

The key idea is that the attacker has prepared something and now needs
to get it to the victim or target.

Possible delivery methods include:

-   Malicious email attachments
-   Malicious links
-   Drive-by downloads
-   Exploit traffic
-   Removable media
-   Malicious documents

For example:

``` text
Attacker infrastructure
        ↓
Malicious document
        ↓
Email
        ↓
Victim
```

## SOC perspective

Useful evidence can include:

-   Email logs
-   Proxy logs
-   Web logs
-   Attachment hashes
-   Download events
-   Endpoint telemetry

------------------------------------------------------------------------

# 10. Phase 4 --- Social Engineering

## What is Social Engineering?

**Social Engineering** involves manipulating people into performing
actions that help the attacker.

Instead of attacking only the technology, the attacker attacks the
**human decision-making process**.

Examples from the room include:

### Phishing attachment

The attacker sends a malicious attachment and tries to convince the user
to open it.

### Fake login page

The attacker creates a page that looks legitimate and attempts to
convince the user to enter credentials.

### Impersonation

The attacker may pretend to be:

-   IT support
-   A manager
-   A service provider
-   Another employee

The goal is to convince the target to perform an unsafe action.

## SOC perspective

I can investigate:

-   Suspicious email senders
-   Spoofed domains
-   Malicious attachments
-   Phishing URLs
-   Credential submissions
-   Unusual authentication events

------------------------------------------------------------------------

# 11. Phase 5 --- Exploitation

## What is Exploitation?

**Exploitation** is where the attacker takes advantage of a weakness or
vulnerability in order to perform an action such as code execution.

The room gives examples including:

-   Uploading and executing a reverse shell through a web application
-   Abusing an automated script
-   Exploiting a web application vulnerability to execute code

A simple example is:

``` text
Vulnerable application
        ↓
Attacker sends malicious input
        ↓
Vulnerability is triggered
        ↓
Code executes
```

## Important distinction

Finding a vulnerability is not necessarily the same as exploiting it.

For example:

``` text
Vulnerability discovered → Reconnaissance / analysis
Vulnerability abused → Exploitation
```

## SOC perspective

Evidence may include:

-   WAF alerts
-   IDS alerts
-   Suspicious HTTP requests
-   Exploit payloads
-   Unexpected process creation
-   Web shell creation
-   Reverse-shell activity

------------------------------------------------------------------------

# 12. Phase 6 --- Persistence

## What is Persistence?

**Persistence** is the attacker's ability to maintain access after
gaining a foothold.

Without persistence, the attacker may lose access when:

-   A session ends
-   A machine reboots
-   A password changes
-   A process stops
-   The original vulnerability is fixed

The attacker therefore creates another way to return.

The room gives examples such as:

-   Creating a service
-   Establishing command-and-control access
-   Leaving a backdoor
-   Creating something that executes when a specific event occurs

Examples of persistence mechanisms an analyst might investigate include:

-   Scheduled tasks
-   Services
-   Startup items
-   SSH authorized keys
-   Registry run keys
-   Web shells
-   Backdoor accounts

## SOC perspective

Persistence is especially important because it explains how the attacker
can return later.

Useful logs include:

-   Windows Security logs
-   Sysmon
-   Linux auth logs
-   Auditd
-   Service logs
-   Scheduled-task events
-   Endpoint detection logs

------------------------------------------------------------------------

# 13. Phase 7 --- Defence Evasion

## What is Defence Evasion?

**Defence Evasion** covers techniques used to avoid or bypass security
controls.

The room specifically mentions defensive technologies such as:

-   Web Application Firewalls
-   Network firewalls
-   Antivirus
-   Intrusion Detection Systems

The attacker may attempt to make malicious activity look normal, hide
files, bypass security controls, or otherwise reduce the chance of
detection.

## Why is this important to a SOC analyst?

If I see evidence that an attacker is attempting to evade security
controls, that can tell me that the attacker is actively trying to
remain undetected.

For example:

``` text
Malicious process
      ↓
Attempts to disable or bypass security control
      ↓
Continues attack
```

## Evidence I may investigate

-   Security-tool configuration changes
-   Disabled services
-   Suspicious exclusions
-   Obfuscated commands
-   Renamed tools
-   Deleted logs
-   Processes designed to hide activity

------------------------------------------------------------------------

# 14. Phase 8 --- Command & Control

## What is Command & Control?

**Command & Control (C2)** is the communication channel between an
attacker and a compromised system.

Once a machine is under the attacker's control, the attacker needs some
way to communicate with it.

The room explains that C2 can allow an attacker to:

-   Execute commands
-   Steal credentials
-   Steal information
-   Control the compromised system
-   Pivot to other systems

A simplified model is:

``` text
Attacker
   ↕
 C2 Server
   ↕
Compromised Host
```

## SOC evidence

I can investigate:

-   Suspicious outbound connections
-   Repeated beaconing
-   Unknown domains
-   Suspicious IP addresses
-   DNS activity
-   Unusual ports
-   Long-lived connections
-   Network traffic patterns

This is where network telemetry becomes very valuable.

------------------------------------------------------------------------

# 15. Phase 9 --- Pivoting

## What is Pivoting?

**Pivoting** means using a compromised system as a route to reach other
systems that the attacker cannot directly access.

For example:

``` text
Internet
   ↓
Compromised Web Server
   ↓
Internal Network
   ├── Database
   ├── File Server
   └── Domain Controller
```

The compromised web server becomes the attacker's starting point inside
the network.

The room explains that the compromised system can be used as:

-   A staging location
-   A tunnel
-   A route into the internal network
-   A distribution point for malware or backdoors

## SOC perspective

I should look for signs that a compromised host is suddenly
communicating with systems it normally would not contact.

Examples:

-   New internal connections
-   SSH/RDP/SMB connections from an unusual host
-   Port forwarding
-   Proxying
-   Tunnelling
-   Authentication to multiple internal systems

------------------------------------------------------------------------

# 16. Goal: THROUGH --- Network Propagation

After the attacker establishes a foothold, the attack moves into the
**Through** goal.

The room describes this as the stage where the attacker attempts to
expand their access and move through the network.

The attacker may establish a base on one system and then use it to:

-   Discover other systems
-   Find credentials
-   Increase privileges
-   Execute malicious code
-   Move laterally

The phases are:

9.  Pivoting
10. Discovery
11. Privilege Escalation
12. Execution
13. Credential Access
14. Lateral Movement

------------------------------------------------------------------------

# 17. Phase 10 --- Discovery

## What is Discovery?

**Discovery** is the process of learning about the compromised system
and its surrounding environment.

After gaining access, the attacker does not necessarily know everything
about the machine.

They may ask questions such as:

``` text
Who am I?
What privileges do I have?
What operating system is this?
What users exist?
What software is installed?
What files are available?
What systems are nearby?
What network shares exist?
```

The room specifically mentions discovering:

-   Active user accounts
-   Permissions
-   Applications and software
-   Web browser activity
-   Files and directories
-   Network shares
-   System configuration

## Common discovery examples

Commands such as these may appear during an investigation:

``` text
whoami
whoami /priv
hostname
ipconfig
systeminfo
net user
net localgroup
```

The important SOC lesson is that a single discovery command is not
automatically malicious. Context matters.

For example:

``` text
Administrator runs systeminfo during normal maintenance
```

may be legitimate.

But:

``` text
Newly compromised account
        ↓
whoami
        ↓
whoami /priv
        ↓
net user
        ↓
network enumeration
```

is much more interesting and should be correlated with the rest of the
timeline.

------------------------------------------------------------------------

# 18. Phase 11 --- Privilege Escalation

## What is Privilege Escalation?

**Privilege Escalation** is the process of gaining higher permissions
than the attacker originally had.

For example:

``` text
Normal User
    ↓
Privilege Escalation
    ↓
Administrator
    ↓
SYSTEM / Root
```

The room explains that attackers may use vulnerabilities, compromised
accounts, or misconfigurations to gain higher privileges.

Possible levels include:

-   SYSTEM
-   Root
-   Local Administrator
-   Admin-like accounts
-   Accounts with special privileges

## Why does this matter?

Higher privileges usually give an attacker greater control over the
environment.

For example, an attacker with normal user access may not be able to:

-   Modify security settings
-   Access protected files
-   Create system services
-   Change other users
-   Access sensitive systems

After privilege escalation, these actions may become possible.

## SOC evidence

I can look for:

-   Suspicious administrator logons
-   `sudo` activity
-   UAC bypass indicators
-   New privileged accounts
-   Group membership changes
-   Exploitation of local vulnerabilities

------------------------------------------------------------------------

# 19. Phase 12 --- Execution

## What is Execution?

**Execution** is when attacker-controlled code or commands actually run
on a system.

The room explains that attackers may use the compromised system as a
host for:

-   Malware
-   C2 scripts
-   Malicious links
-   Scheduled tasks
-   Other attacker-controlled code

Examples of execution evidence include:

``` text
PowerShell
cmd.exe
bash
python
wscript
rundll32
```

Again, the executable alone does not prove malicious activity.

The important question is:

> Who launched it, what launched it, what command was executed, and what
> happened afterward?

That is why **process-tree analysis** is important for a SOC analyst.

------------------------------------------------------------------------

# 20. Phase 13 --- Credential Access

## What is Credential Access?

**Credential Access** is the stage where the attacker attempts to obtain
account names, passwords, tokens, keys, or other authentication
material.

The room mentions methods such as:

-   Keylogging
-   Credential dumping
-   Other credential theft techniques

The main goal is to obtain legitimate credentials that can be used to
access additional systems.

For example:

``` text
Compromised workstation
        ↓
Credential theft
        ↓
Administrator credentials
        ↓
Remote access to another system
```

## Why stolen credentials are dangerous

If an attacker uses valid credentials, their activity may initially look
like normal user activity.

This is one reason authentication monitoring is important.

A SOC analyst can investigate:

-   Unusual login locations
-   Unusual login times
-   Failed login bursts
-   New authentication sources
-   Privileged account usage
-   RDP/SMB/SSH authentication
-   Credential-dumping indicators

------------------------------------------------------------------------

# 21. Phase 14 --- Lateral Movement

## What is Lateral Movement?

**Lateral Movement** is the process of moving from one compromised
system to another system inside the environment.

The attacker has already gained access to one machine and now wants to
reach additional targets.

For example:

``` text
Compromised Workstation
        ↓
Compromised Server
        ↓
Database Server
        ↓
Critical System
```

The attacker may use credentials obtained earlier to authenticate to
another system.

## Why attackers move laterally

The first machine they compromise may not contain the information they
want.

They may need to reach:

-   File servers
-   Database servers
-   Domain controllers
-   Application servers
-   Backup systems
-   High-value workstations

## SOC evidence

I can look for:

-   RDP connections
-   SMB connections
-   SSH sessions
-   Remote service creation
-   Unusual administrator authentication
-   One host accessing many internal systems

------------------------------------------------------------------------

# 22. Goal: OUT --- Action on Objectives

The **Out** goal represents the later part of the attack, where the
attacker has gained enough access to pursue the final objective.

The room groups this into four phases:

15. Collection
16. Exfiltration
17. Impact
18. Objectives

The objective could involve compromising:

-   Confidentiality
-   Integrity
-   Availability

------------------------------------------------------------------------

# 23. Phase 15 --- Collection

## What is Collection?

**Collection** is the process of gathering information that is valuable
to the attacker.

After gaining access to systems and discovering where useful data
exists, the attacker collects it.

The room lists possible data sources such as:

-   Drives
-   Browsers
-   Audio
-   Video
-   Email

Other examples could include business documents, databases, credentials,
source code, or customer information.

A simplified chain is:

``` text
Discover valuable data
        ↓
Locate the data
        ↓
Gather the data
        ↓
Prepare for the next stage
```

## SOC perspective

Useful indicators can include:

-   Large file access
-   Unusual archive creation
-   Access to sensitive directories
-   Browser-data access
-   Database queries
-   Large amounts of file movement

------------------------------------------------------------------------

# 24. Phase 16 --- Exfiltration

## What is Exfiltration?

**Exfiltration** is the process of removing stolen data from the target
environment.

The attacker may package or compress data before sending it out.

The room specifically explains that encryption and compression can be
used to reduce the chance of detection.

A simplified example is:

``` text
Sensitive files
      ↓
Collection
      ↓
Archive / compress
      ↓
Transfer outside network
      ↓
Attacker-controlled system
```

The attacker may use infrastructure created during earlier stages, such
as a C2 channel or tunnel.

## SOC evidence

I can investigate:

-   Large outbound transfers
-   Unusual destinations
-   DNS tunnelling
-   HTTP/HTTPS uploads
-   FTP transfers
-   Cloud-storage uploads
-   Unusual archive files
-   Abnormal encrypted traffic

------------------------------------------------------------------------

# 25. Phase 17 --- Impact

## What is Impact?

**Impact** is where the attacker attempts to manipulate, interrupt, or
destroy systems or data.

The room connects Impact with the **integrity and availability** of
assets.

Examples mentioned include:

-   Removing account access
-   Disk wiping
-   Data encryption
-   Ransomware
-   Defacement
-   Denial of Service (DoS)

For example:

``` text
Initial Access
      ↓
Privilege Escalation
      ↓
Lateral Movement
      ↓
Access critical server
      ↓
Encrypt files
      ↓
Business disruption
```

## SOC perspective

Indicators may include:

-   Large-scale file modifications
-   Ransom notes
-   Encryption activity
-   Service stoppage
-   Account deletion
-   Disk-wiping commands
-   Website defacement
-   Denial-of-service traffic

------------------------------------------------------------------------

# 26. Phase 18 --- Objectives

## What are Objectives?

**Objectives** represent the strategic goal the attacker ultimately
wants to achieve.

This is important because the technical actions are usually means to an
end.

For example:

``` text
Reconnaissance
      ↓
Exploitation
      ↓
Persistence
      ↓
Credential Access
      ↓
Lateral Movement
      ↓
Collection
      ↓
Exfiltration
      ↓
Financial objective
```

The room gives a financially motivated attack as an example. An attacker
may encrypt files using ransomware and demand payment.

Other objectives may involve:

-   Financial gain
-   Theft of sensitive information
-   Espionage
-   Disruption
-   Reputational damage
-   Destruction

The important point is that the **Objective explains why the attack
happened**.

------------------------------------------------------------------------

# 27. The Three Major Goals --- Easy Revision

The entire UKC can be remembered using three words:

``` text
IN → THROUGH → OUT
```

## IN --- Get inside

``` text
1. Reconnaissance
2. Weaponization
3. Delivery
4. Social Engineering
5. Exploitation
6. Persistence
7. Defence Evasion
8. Command & Control
9. Pivoting
```

Think:

> **How did the attacker get into the environment and establish
> control?**

## THROUGH --- Move around

``` text
10. Discovery
11. Privilege Escalation
12. Execution
13. Credential Access
14. Lateral Movement
```

Think:

> **How did the attacker expand their control?**

## OUT --- Achieve the goal

``` text
15. Collection
16. Exfiltration
17. Impact
18. Objectives
```

Think:

> **What did the attacker do with the access they gained?**

------------------------------------------------------------------------

# 28. One Simple Attack Example Using All 18 Phases

I can understand the UKC much more easily when I imagine one complete
attack.

### 1. Reconnaissance

The attacker researches a company's public infrastructure and discovers
a web server.

### 2. Weaponization

The attacker prepares infrastructure and a payload for the attack.

### 3. Delivery

The malicious content or exploit traffic is delivered to the target.

### 4. Social Engineering

If the attack involves a human, the attacker tricks an employee into
opening a malicious document or visiting a fake page.

### 5. Exploitation

A vulnerability is abused and code execution is achieved.

### 6. Persistence

The attacker creates a mechanism that allows them to return later.

### 7. Defence Evasion

The attacker attempts to avoid security controls and detection.

### 8. Command & Control

The compromised host communicates with attacker-controlled
infrastructure.

### 9. Pivoting

The compromised system becomes a route into the internal network.

### 10. Discovery

The attacker identifies users, systems, applications, files, and network
resources.

### 11. Privilege Escalation

The attacker gains higher privileges.

### 12. Execution

The attacker runs commands and malicious code using the newly obtained
access.

### 13. Credential Access

The attacker obtains additional credentials.

### 14. Lateral Movement

The attacker uses those credentials to access another internal system.

### 15. Collection

The attacker gathers sensitive documents and other valuable information.

### 16. Exfiltration

The collected data is transferred outside the environment.

### 17. Impact

The attacker may encrypt, delete, modify, or otherwise disrupt systems
or data.

### 18. Objectives

The attacker achieves the strategic goal, such as financial gain,
information theft, espionage, or disruption.

------------------------------------------------------------------------

# 29. Why the UKC Is Useful for a SOC Analyst

For me, the biggest value of the Unified Kill Chain is that it gives me
a **story** for an incident.

Instead of looking at alerts separately:

``` text
Alert 1
Alert 2
Alert 3
Alert 4
```

I can ask:

``` text
What happened first?
        ↓
How did the attacker get access?
        ↓
How did they maintain access?
        ↓
What did they discover?
        ↓
How did they increase privileges?
        ↓
Did they steal credentials?
        ↓
Did they move to another system?
        ↓
What data did they access?
        ↓
Did they exfiltrate anything?
        ↓
What was the final objective?
```

This is especially useful during alert triage and incident response.

------------------------------------------------------------------------

# 30. UKC and Log Analysis

The phases can also guide me toward the logs I should investigate.

  -----------------------------------------------------------------------
  UKC Phase                           Useful evidence / logs
  ----------------------------------- -----------------------------------
  Reconnaissance                      Firewall, IDS, DNS, web logs

  Weaponization                       Threat intelligence, network
                                      telemetry

  Delivery                            Email, proxy, web, endpoint logs

  Social Engineering                  Email, authentication, web logs

  Exploitation                        WAF, IDS, web, endpoint logs

  Persistence                         Windows Security, Sysmon, Auditd,
                                      services, scheduled tasks

  Defence Evasion                     AV/EDR, configuration and process
                                      logs

  Command & Control                   DNS, firewall, proxy, network
                                      telemetry

  Pivoting                            Firewall, network flows,
                                      authentication logs

  Discovery                           Process logs, command-line logs,
                                      PowerShell, audit logs

  Privilege Escalation                Security logs, sudo, process
                                      creation, group changes

  Execution                           Sysmon, process creation,
                                      PowerShell, shell logs

  Credential Access                   Authentication, EDR, security logs

  Lateral Movement                    RDP, SSH, SMB, authentication logs

  Collection                          File access, process, endpoint and
                                      network logs

  Exfiltration                        Firewall, proxy, DNS, network
                                      traffic

  Impact                              Endpoint, file, service and
                                      security logs

  Objectives                          Correlated evidence across the
                                      entire environment
  -----------------------------------------------------------------------

This table is not a replacement for investigation. It is a starting
point for deciding where to look.

------------------------------------------------------------------------

# 31. UKC vs a Simple Attack Timeline

A normal incident timeline may look like:

``` text
04:00 — Scan
04:15 — Exploit
04:20 — Shell
04:40 — New account
05:00 — Discovery
05:15 — Lateral movement
06:00 — Data collection
06:30 — Exfiltration
```

The UKC gives meaning to those events:

``` text
04:00 — Reconnaissance
04:15 — Exploitation
04:20 — Command & Control / Execution
04:40 — Persistence
05:00 — Discovery
05:15 — Lateral Movement
06:00 — Collection
06:30 — Exfiltration
```

This makes the attack easier to explain to another analyst or during
incident reporting.

------------------------------------------------------------------------

# 32. Important Lesson --- The Attack Is Not Always Linear

One of the most important things I learned from this room is that
attackers do not always follow the phases in a perfect order.

For example:

``` text
Reconnaissance
      ↓
Exploitation
      ↓
Discovery
      ↓
Pivoting
      ↓
Reconnaissance AGAIN
      ↓
Exploitation of another system
      ↓
Privilege Escalation
```

After compromising a new system, the attacker may need to perform
discovery again.

This is why the UKC can represent a more realistic attack than a simple
one-way chain.

------------------------------------------------------------------------

# 33. Important Terms to Remember

### Kill Chain

A model describing the stages of an attack.

### Threat Modelling

A structured process for identifying assets, weaknesses, risks, and
security controls.

### Initial Foothold

The attacker's first successful access to the environment.

### Persistence

A method that allows the attacker to maintain or regain access.

### Defence Evasion

Actions used to avoid security controls or detection.

### Command & Control

Communication between an attacker and a compromised system.

### Pivoting

Using one compromised system to reach another system.

### Discovery

Learning about the compromised host and network.

### Privilege Escalation

Obtaining higher permissions.

### Credential Access

Obtaining credentials or authentication material.

### Lateral Movement

Moving from one system to another.

### Collection

Gathering valuable information.

### Exfiltration

Removing stolen data from the target environment.

### Impact

Manipulating, disrupting, or destroying systems/data.

### Objectives

The attacker's ultimate strategic goal.

------------------------------------------------------------------------

# 34. Quick 18-Phase Memory Trick

I can remember the sequence as:

``` text
RECON
WEAPONIZE
DELIVER
SOCIAL ENGINEER
EXPLOIT
PERSIST
EVADE
C2
PIVOT
DISCOVER
ESCALATE
EXECUTE
STEAL CREDENTIALS
MOVE
COLLECT
EXFILTRATE
IMPACT
OBJECTIVE
```

Or simply group it into three questions:

### IN

**How did they get in and establish control?**

### THROUGH

**How did they expand their control?**

### OUT

**What did they take, damage, or achieve?**

------------------------------------------------------------------------

# 35. SOC Investigation Workflow Based on the UKC

When investigating a real alert, I can use this workflow:

### Step 1 --- Start with the alert

Identify:

-   Time
-   Host
-   User
-   Source IP
-   Destination
-   Process
-   Alert type

### Step 2 --- Determine the UKC phase

Ask:

> Which phase could this activity belong to?

For example, a suspicious scheduled task may indicate **Persistence**.

### Step 3 --- Look backward

Ask:

> What happened immediately before this?

This can reveal the initial access method.

### Step 4 --- Look forward

Ask:

> What happened after this event?

This can reveal discovery, credential access, lateral movement,
collection, or impact.

### Step 5 --- Correlate different logs

Do not rely on only one source.

For example:

``` text
Web Logs
   +
Windows Security
   +
Sysmon
   +
Firewall
   +
EDR
   ↓
Attack Timeline
```

### Step 6 --- Build the attack story

Finally, explain the incident as a sequence rather than a collection of
unrelated alerts.

------------------------------------------------------------------------

# 36. Final Takeaways

After completing this room, I understand that the **Unified Kill Chain
is a framework for understanding an entire cyber attack**.

The 18 phases are:

``` text
1.  Reconnaissance
2.  Weaponization
3.  Delivery
4.  Social Engineering
5.  Exploitation
6.  Persistence
7.  Defence Evasion
8.  Command & Control
9.  Pivoting
10. Discovery
11. Privilege Escalation
12. Execution
13. Credential Access
14. Lateral Movement
15. Collection
16. Exfiltration
17. Impact
18. Objectives
```

The easiest way for me to remember the framework is:

``` text
                UNIFIED KILL CHAIN
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
       IN           THROUGH          OUT
   Get inside      Move around    Achieve goal
        │              │              │
   1 → 9           10 → 14        15 → 18
```

The most important SOC lesson is that **an alert is only one piece of
the attack story**. By identifying where an event fits in the UKC and
then looking for the events before and after it, I can reconstruct the
attacker's path and understand what happened across the environment.

------------------------------------------------------------------------

## Room Completion Note

I completed the **Unified Kill Chain** room and focused on understanding
the framework rather than memorising only the phase names. The main
thing I want to retain for future SOC investigations is the relationship
between the phases and the evidence I can find in logs.

**Core idea:**

> **IN → get access and establish control → THROUGH → expand access and
> move through the environment → OUT → collect data, cause impact, and
> achieve the final objective.**
