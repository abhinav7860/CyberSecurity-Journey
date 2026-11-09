# DFIR: An Introduction --- Detailed Walkthrough Notes

**Platform:** TryHackMe\
**Scope:** Tasks 2--5 (The Need for DFIR, Basic Concepts, Tools,
Incident Response)\
**Study date:** 9 November 2026\
**Focus:** SOC / Blue Team

> These notes explain the supplied lesson. Practical scenarios are
> illustrative, not evidence from a completed lab.

## Task 2 --- The Need for DFIR

### What is DFIR?

**Digital Forensics and Incident Response (DFIR)** combines the
collection and examination of evidence from digital devices with the
operational process of investigating and responding to security
incidents.

-   **Digital forensics** identifies and interprets artifacts of
    activity on computers, smartphones, storage media, and other
    devices.
-   **Incident response (IR)** uses investigative findings to determine
    the scope of an incident, contain the attacker, eradicate their
    foothold, and restore the environment.
-   The two disciplines depend on each other: IR defines the questions
    and scope of the investigation; forensics provides evidence that
    guides IR decisions.

### Why organizations need DFIR

1.  **Confirm incidents:** distinguish real malicious activity from
    false alarms.
2.  **Remove attacker footholds:** discover persistence and ensure the
    threat is removed.
3.  **Establish scope and timeframe:** identify affected hosts,
    accounts, systems, and relevant times.
4.  **Find root causes:** understand weaknesses that enabled the
    compromise.
5.  **Understand attacker behavior:** use observed techniques to improve
    defenses.
6.  **Share threat knowledge:** communicate useful attacker indicators
    and techniques with stakeholders or the wider community.

**Illustrative SOC scenario:** An alert flags suspicious account
activity. The SOC analyst initially triages the alert; DFIR examines
logs, system artifacts, and other evidence to determine whether
compromise occurred and what must be contained.

### Who performs DFIR?

  -----------------------------------------------------------------------
  Discipline              Main expertise          Investigation
                                                  contribution
  ----------------------- ----------------------- -----------------------
  Digital Forensics       Locating, preserving,   Evidence about what
                          and interpreting        occurred
                          digital artifacts       

  Incident Response       Cybersecurity           Scope, containment,
                          investigation and       eradication, and
                          operational response    recovery

  DFIR                    Both domains            Evidence-led incident
                                                  handling
  -----------------------------------------------------------------------

**Remember:** Forensics asks what the evidence shows; incident response
asks what action should follow from those findings.

------------------------------------------------------------------------

## Task 3 --- Basic Concepts of DFIR

### 1. Forensic artifacts

An **artifact** is a piece of digital evidence that indicates activity
on a system. Artifacts can originate from filesystems, memory, or
network activity.

Examples: - A Windows Registry entry associated with application
execution or persistence. - An event log showing a logon or
process-related event. - A file or filesystem timestamp. - Network
activity connecting an endpoint to an external address.

**Hypothesis versus evidence:** "An attacker used a Registry Run key for
persistence" is a hypothesis until relevant evidence supports it. The
key itself is an artifact; investigators should correlate it with other
evidence rather than relying on one artifact alone.

### 2. Evidence preservation

The goal is to protect evidence integrity during investigation.

General workflow: 1. Identify the potential evidence source. 2. Collect
and document it using an appropriate forensic process. 3. Preserve the
original evidence and protect it against unintended modification. 4.
Analyze a verified working copy where possible. 5. Retain the preserved
original so another working copy can be produced if needed.

**Why this matters:** Investigation activities can alter a live system.
Appropriate acquisition, write protection, and working copies reduce
contamination risk. The lesson emphasizes write-protected evidence and
analysis of a copy.

### 3. Chain of custody

**Chain of custody** is the documented record of who controlled or
handled evidence and when.

A custody record commonly documents: - Evidence identifier and
description. - Collector and collection time. - Transfers between
custodians. - Storage and access history. - Purpose of handling and
relevant integrity checks.

**Example:** A disk image is acquired by Analyst A and transferred to
Analyst B. The transfer should be authorized and documented. An
unexplained transfer or access raises questions about integrity and
reliability.

### 4. Order of volatility

**Volatility** describes how easily data may be lost or changed.

  Evidence source   Lesson's key point
  ----------------- ---------------------------------------------------
  RAM               Volatile: contents can disappear after power loss
  Hard drive        More persistent: retains data without power

**Practical lesson:** Collect evidence at risk of disappearing before
less volatile evidence when appropriate. In the example provided, RAM
should be preserved before the hard drive. Real investigations must also
account for operational risk and the effect of collection on the system.

### 5. Timeline creation

**Timeline creation** organizes artifacts and events chronologically so
analysts can reconstruct an incident.

Illustrative timeline: \| Time \| Example observation \| Investigative
question \| \|---\|---\|---\| \| 09:10 \| Suspicious authentication \|
Who accessed the system? \| \| 09:14 \| Unexpected process execution \|
What program ran? \| \| 09:16 \| Unusual network connection \| Was there
external communication? \| \| 09:22 \| Persistence-related change \| Was
a foothold established? \|

These times are fictional. A real timeline should be built from
collected artifacts, with time zones and clock accuracy considered.

**Key takeaway:** A timeline turns scattered evidence into a coherent,
testable sequence of events.

------------------------------------------------------------------------

## Task 4 --- DFIR Tools

  -----------------------------------------------------------------------
  Tool                    Primary use from the    Where it fits
                          lesson                  
  ----------------------- ----------------------- -----------------------
  Eric Zimmerman's tools  Windows Registry,       Windows forensics
                          filesystem, timeline,   
                          and other artifact      
                          analysis                

  KAPE (Kroll Artifact    Automated forensic      Rapid artifact
  Parser and Extractor)   artifact collection and acquisition and
                          parsing; timeline       processing
                          support                 

  Autopsy                 Open-source             Disk, removable-media,
                          digital-media forensic  and supported device
                          analysis with plugins   evidence

  Volatility              Memory analysis of      RAM forensics
                          captured Windows and    
                          Linux memory            

  Redline                 Endpoint forensic data  Incident investigation
                          collection and          
                          examination             

  Velociraptor            Open-source endpoint    Endpoint investigation
                          monitoring, forensics,  and response
                          and response            
  -----------------------------------------------------------------------

### How to choose a tool

-   Need to examine **memory**? The lesson introduces **Volatility**.
-   Need to automate collection of **Windows artifacts**? Consider
    **KAPE**.
-   Need to examine a **disk image**? The lesson introduces **Autopsy**.
-   Need **endpoint investigation and response** capabilities? The
    lesson introduces **Velociraptor** and **Redline**.

**Important:** Tools assist investigations, but they do not replace a
defensible collection process, accurate interpretation, and
documentation.

### TryHackMe follow-up rooms from the lesson

-   [Windows Forensics 1](https://tryhackme.com/room/windowsforensics1)
-   [Windows Forensics 2](https://tryhackme.com/room/windowsforensics2)
-   [Linux Forensics](https://tryhackme.com/room/linuxforensics)
-   [KAPE](https://tryhackme.com/room/kape)
-   [Autopsy](https://tryhackme.com/room/btautopsye0)
-   [Volatility](https://tryhackme.com/room/volatility)
-   [Redline](https://tryhackme.com/room/btredlinejoxr3d)
-   [Velociraptor](https://tryhackme.com/room/velociraptorhp)

------------------------------------------------------------------------

## Task 5 --- The Incident Response Process

The supplied lesson compares two incident-response models.

### NIST SP 800-61 Rev. 2 model (as presented in this room)

1.  Preparation
2.  Detection and Analysis
3.  Containment, Eradication, and Recovery
4.  Post-incident Activity

### SANS PICERL model

**P --- Preparation**\
**I --- Identification**\
**C --- Containment**\
**E --- Eradication**\
**R --- Recovery**\
**L --- Lessons Learned**

  -----------------------------------------------------------------------
  PICERL phase            Meaning                 Example
  ----------------------- ----------------------- -----------------------
  Preparation             Establish people,       Response procedures and
                          processes, and          assigned
                          technology before       responsibilities
                          incidents               

  Identification          Detect, analyze,        Determine whether a SOC
                          validate, document, and alert is a true
                          communicate incidents   incident

  Containment             Limit incident effects  Isolate an affected
                          using short- or         endpoint
                          long-term measures      

  Eradication             Remove the threat and   Remove malicious
                          address its entry point persistence and close
                          or foothold             the exploited weakness

  Recovery                Restore disrupted       Bring verified-clean
                          services to normal      services back online
                          operation               

  Lessons Learned         Document the incident   Update detection logic
                          and improve future      and response procedures
                          readiness               
  -----------------------------------------------------------------------

### Mapping the models

  -----------------------------------------------------------------------
  NIST four-phase model               Closely corresponding SANS phases
  ----------------------------------- -----------------------------------
  Preparation                         Preparation

  Detection and Analysis              Identification

  Containment, Eradication, and       Containment + Eradication +
  Recovery                            Recovery

  Post-incident Activity              Lessons Learned
  -----------------------------------------------------------------------

The lesson presents these models as substantially equivalent in purpose,
with different grouping of phases.

### How forensics supports each phase

-   **Identification:** Examine logs and artifacts to confirm an
    incident.
-   **Containment:** Identify affected assets and attacker footholds to
    guide containment.
-   **Eradication:** Check that malicious activity and persistence
    mechanisms are addressed.
-   **Recovery:** Use investigative findings to reduce the risk of
    restoring compromised systems.
-   **Lessons Learned:** Build an evidence-supported account of the
    incident and identify improvements.

### Illustrative end-to-end scenario

1.  **Preparation:** A SOC has response contacts, logging, and an
    escalation procedure.
2.  **Identification:** An alert shows suspicious behavior; analysts
    review supporting evidence.
3.  **Containment:** The affected endpoint is isolated to limit spread.
4.  **Eradication:** Investigators identify and remove the threat and
    its persistence, then address the entry point.
5.  **Recovery:** The endpoint or service is restored and monitored.
6.  **Lessons Learned:** The team documents the incident and improves
    controls and detection.

This is an example to connect the phases, not a lab solution from the
provided lesson.

------------------------------------------------------------------------

## Important Definitions --- Quick Revision

  -----------------------------------------------------------------------
  Term                                Definition
  ----------------------------------- -----------------------------------
  DFIR                                Digital Forensics and Incident
                                      Response

  Artifact                            Digital evidence indicating
                                      activity

  Evidence preservation               Protecting collected evidence
                                      against unintended changes

  Chain of custody                    Documented control and handling
                                      history of evidence

  Volatility                          Likelihood of evidence disappearing
                                      or changing

  Timeline                            Chronological reconstruction from
                                      collected artifacts

  Containment                         Limiting the impact or spread of an
                                      incident

  Eradication                         Removing the threat and its
                                      foothold

  Recovery                            Returning affected services to
                                      normal operation

  PICERL                              Preparation, Identification,
                                      Containment, Eradication, Recovery,
                                      Lessons Learned
  -----------------------------------------------------------------------

## Self-Test Questions

1.  What does DFIR stand for?
2.  Why are digital forensics and incident response interdependent?
3.  How does DFIR help distinguish a false positive from an incident?
4.  What is a forensic artifact? Give two examples.
5.  Why is evidence preservation important?
6.  What could weaken a chain of custody?
7.  Why might RAM be collected before a hard drive?
8.  What is the purpose of a forensic timeline?
9.  Which tool in this lesson specializes in memory analysis?
10. What does KAPE automate?
11. What is Autopsy used for?
12. What are the six PICERL phases?
13. Which three phases does the NIST model group together?
14. Why must eradication address the attacker's entry point?
15. What is the purpose of lessons learned?

## My Key Takeaways

-   I learned that DFIR is the combination of **evidence-led
    investigation** and **incident response**.
-   I understood why forensic artifacts, evidence preservation, and
    chain of custody are central to a reliable investigation.
-   I learned that volatile evidence, especially RAM, may need priority
    during collection.
-   I understood how a timeline helps connect isolated artifacts into an
    incident narrative.
-   I became familiar with tools such as KAPE, Autopsy, Volatility,
    Redline, and Velociraptor.
-   I can explain the SANS **PICERL** lifecycle and map it to the four
    phases of the NIST model presented in the lesson.
-   As I continue studying SOC operations, I want to connect alert
    triage with forensic evidence and incident-response decisions.

## Practice Checklist

-   [ ] Explain DFIR without looking at the notes.
-   [ ] Give three examples of forensic artifacts.
-   [ ] Explain evidence preservation and chain of custody.
-   [ ] Compare RAM and disk volatility.
-   [ ] Build a small fictional event timeline.
-   [ ] Match each DFIR tool to its primary purpose.
-   [ ] Recite PICERL in order.
-   [ ] Explain why containment should precede eradication.
-   [ ] Explain how forensics supports SOC incident response.

## Source and Scope

Based on the user's supplied TryHackMe **DFIR: An Introduction**, Tasks
**2--5**. The lesson's reference to NIST SP 800-61 Rev. 2 is retained as
presented; these notes do not independently verify current framework
revisions. No actual forensic artifact, memory image, or lab output was
provided, so no investigation findings or task answers are fabricated.
