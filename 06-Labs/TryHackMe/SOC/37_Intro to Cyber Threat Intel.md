# Intro to Cyber Threat Intel --- TryHackMe

**Date:** 17 September 2026\
**Path:** SOC Level 1 → Cyber Threat Intelligence

## What I learned

This room introduced me to **Cyber Threat Intelligence (CTI)** and
showed me how raw security data can be turned into useful intelligence
for a SOC analyst.

The main idea I took from this room is:

> I should not just see an IP address, hash, domain, or email and call
> it malicious. I should enrich it, add context, correlate it with other
> evidence, and then decide what it means.

I also learned about the CTI lifecycle, intelligence classifications,
TLP, STIX, TAXII, MITRE ATT&CK, the Cyber Kill Chain, and finally used a
small simulated SOC to build a threat profile.

------------------------------------------------------------------------

# Task 2 --- Cyber Threat Intelligence

## Data → Information → Intelligence

### Data

Raw evidence with no extra context.

Example:

``` text
45.155.205.3:443
```

### Information

Data with additional facts, such as registration details or when an
indicator was first seen.

### Intelligence

Information that has been analysed and answers the **"so what?"**
question.

## IOC, IOA and TTP

**IOC --- Indicator of Compromise:** evidence that may show a system has
been compromised.

**IOA --- Indicator of Attack:** an action that shows an attack may be
happening.

**TTP --- Tactics, Techniques and Procedures:** the way an attacker
operates.

## Threat Intelligence classifications

  Classification   What it means
  ---------------- ---------------------------------------------------------
  Strategic        High-level trends and risks used for business decisions
  Tactical         Attacker TTPs and behaviours
  Operational      Campaigns, motives and intent
  Technical        Concrete artefacts such as IPs and hashes

### Answers

**What does CTI stand for?**

``` text
Cyber Threat Intelligence
```

**IP addresses, Hashes and other threat artefacts would be found under
which Threat Intelligence classification?**

``` text
technical intel
```

------------------------------------------------------------------------

# Task 3 --- CTI Lifecycle

The CTI lifecycle has six phases:

``` text
Direction
   ↓
Collection
   ↓
Processing
   ↓
Analysis
   ↓
Dissemination
   ↓
Feedback
   ↺
```

## Direction

This is where the intelligence mission is defined. The analyst decides
what needs protection and what questions need to be answered.

## Collection

The required information is gathered from sources such as internal logs,
EDR, SIEM, commercial feeds and OSINT.

## Processing

Raw information is sorted, organised, normalised, correlated, tagged and
presented in a usable form.

## Analysis

The analyst works out what the information actually means and looks for
attack patterns and useful actions.

## Dissemination

The intelligence is given to the people who need it, such as the
firewall, endpoint, SOC or management teams.

## Feedback

The results are reviewed so the CTI process can be improved.

### Answers

**At which phase is data converted into usable formats through sorting,
organising, correlation and presentation?**

``` text
processing
```

**During which phase do analysts define the questions to investigate
incidents?**

``` text
direction
```

------------------------------------------------------------------------

# Task 4 --- CTI Standards & Frameworks

## MITRE ATT&CK

MITRE ATT&CK gives analysts a common language for describing attacker
behaviour.

Example:

``` text
T1059.001
```

## MITRE D3FEND

I remember this as:

``` text
ATT&CK  → How attackers behave
D3FEND  → How defenders can respond
```

## Cyber Kill Chain

``` text
Reconnaissance
      ↓
Weaponisation
      ↓
Delivery
      ↓
Exploitation
      ↓
Installation
      ↓
Command & Control
      ↓
Actions on Objectives
```

If an attacker has already obtained access and is extracting data, the
phase is:

``` text
actions on objectives
```

## CVE, CVSS and NVD

-   **CVE** --- identifier for a vulnerability.
-   **CVSS** --- severity scoring system.
-   **NVD** --- vulnerability database containing CVE information and
    related details.

## STIX

**Structured Threat Information Expression**

STIX provides a structured way to represent cyber threat information
such as indicators, malware, campaigns, relationships and TTPs.

## TAXII

**Trusted Automated eXchange of Indicator Information**

TAXII is used to exchange threat intelligence.

The two sharing models are:

``` text
Collection
Channel
```

### Collection

Threat intelligence is hosted by a producer and requested by users.

### Channel

Threat intelligence is pushed to users from a central server.

### Answers

**What sharing models are supported by TAXII?**

``` text
Collection and channel
```

**When an adversary has obtained access to a network and is extracting
data, what phase of the kill chain are they on?**

``` text
actions on objectives
```

------------------------------------------------------------------------

# Task 5 --- Practical Analysis

This was the most practical part of the room.

I opened the green **View Site** button and entered the Static Site Lab.
The lab contains a small simulated security monitoring tool. My job was
to look at the events, connect them together, and build a threat
profile.

I used a Medium walkthrough as a reference for the intended
investigation flow and to cross-check the final answers. The walkthrough
confirms the practical values and final flag.

## Step 1 --- Open the Static Site Lab

I clicked:

``` text
View Site
```

This opened the simulated security monitoring environment.

The important part was the monitoring tool on the right side.

I needed to investigate the events rather than looking at them
individually.

## Step 2 --- Identify the suspicious network activity

The monitoring dashboard showed suspicious network activity.

The important IP address I identified was:

``` text
91.185.23.222
```

I treated this as an IOC that needed to be correlated with the other
events.

## Step 3 --- Find the suspicious email

I then looked through the monitoring information for the email event.

The source email address was:

``` text
vipivillain@badbank.com
```

Now I had another IOC:

``` text
Suspicious IP
        +
Suspicious email
```

## Step 4 --- Find the downloaded file

The next event showed that the victim downloaded a file.

The filename was:

``` text
flbpfuh.exe
```

The `.exe` extension made it important to investigate because it was an
executable associated with the suspicious activity.

At this point I could connect the events:

``` text
Suspicious IP
     ↓
Suspicious email
     ↓
Email received
     ↓
Executable downloaded
```

## Step 5 --- Correlate the events

This was the main lesson of the practical task.

I did not treat each event as a separate problem.

I connected them into one story:

``` text
91.185.23.222
       ↓
Suspicious activity
       ↓
vipivillain@badbank.com
       ↓
Email received
       ↓
flbpfuh.exe downloaded
```

The walkthrough also describes the simulated timeline as suspicious
network traffic, an email arriving, the executable being downloaded, and
subsequent host changes.

## Step 6 --- Build the threat profile

I entered the relevant information into the monitoring tool.

The main values I had collected were:

  Threat detail     Value
  ----------------- ---------------------------
  Suspicious IP     `91.185.23.222`
  Source email      `vipivillain@badbank.com`
  Downloaded file   `flbpfuh.exe`

The goal was to turn several separate observations into one useful
threat profile.

## Step 7 --- Submit the profile

After entering the threat details, I submitted the completed profile.

The site returned:

``` text
John Doe
```

This confirmed that the profile had been built correctly.

## Step 8 --- Retrieve the final flag

The final flag was:

``` text
THM{NOW_I_CAN_CTI}
```

## Practical Analysis --- Final Answers

  Question                                Answer
  --------------------------------------- ---------------------------
  Source email address                    `vipivillain@badbank.com`
  Downloaded file                         `flbpfuh.exe`
  Message after building threat profile   `John Doe`
  Final flag                              `THM{NOW_I_CAN_CTI}`

------------------------------------------------------------------------

# What I learned from the practical

The biggest thing I learned is that **CTI is not just checking whether
an IP is bad**.

The useful part is connecting different pieces of evidence.

``` text
IP
 ↓
Email
 ↓
Downloaded file
 ↓
Timeline
 ↓
Threat profile
 ↓
Actionable intelligence
```

This is what turns raw security events into a story that a SOC analyst
can understand and act on.

------------------------------------------------------------------------

# Quick Revision Notes

## CTI

``` text
Cyber Threat Intelligence
```

## Intelligence classifications

``` text
Strategic
Tactical
Operational
Technical
```

## CTI lifecycle

``` text
Direction
Collection
Processing
Analysis
Dissemination
Feedback
```

## TAXII

``` text
Collection
Channel
```

## STIX

``` text
Structured Threat Information Expression
```

## Cyber Kill Chain

``` text
Reconnaissance
Weaponisation
Delivery
Exploitation
Installation
Command & Control
Actions on Objectives
```

## Practical IOCs

``` text
IP:    91.185.23.222
Email: vipivillain@badbank.com
File:  flbpfuh.exe
```

## Practical result

``` text
John Doe
```

## Flag

``` text
THM{NOW_I_CAN_CTI}
```

------------------------------------------------------------------------

# My takeaway

This room connected many things I had already been learning in the SOC
path.

I learned that a SOC analyst should move from:

``` text
"I found an indicator."
```

to:

``` text
"I enriched the indicator,
correlated it with other evidence,
understood what happened,
and can explain why it matters."
```

That is the part of CTI that I want to remember going forward.

------------------------------------------------------------------------

