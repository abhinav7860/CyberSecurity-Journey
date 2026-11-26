# Intro to Threat Emulation — TryHackMe Study Notes
**Study date:** 25 November 2026 
> **Study focus:** Understand how an organisation can test its security controls by reproducing adversary behaviour in a controlled, authorised exercise.
>
> **Primary perspective:** SOC / Blue Team, with enough Red Team context to understand how an emulation is planned and executed.

---

---

## 1. Introduction

A company can have a firewall, current patches, antivirus and other security controls and still suffer a breach. The presence of security tools does not automatically prove that they are configured correctly, provide sufficient visibility, or stop an attacker.

The important question is not only **whether security controls are installed**, but also **whether they can detect and respond to realistic adversary behaviour**.

Threat emulation addresses this problem by reproducing real-world adversary tactics, techniques and procedures (TTPs) in a controlled environment. This allows an organisation to find weaknesses before a real attacker exploits them.

### Main idea

Threat emulation tests security using an adversary's perspective. It replaces assumptions such as “our firewall will stop everything” with evidence gathered by carrying out approved tests and observing the results.

---

## 2. Purpose of Threat Emulation

Threat emulation helps an organisation understand the actual effectiveness of its security posture and defensive mechanisms.

Organisations may believe that:

- All systems are patched.
- Multi-factor authentication (MFA) is enabled.
- The network is segmented and traffic passes through a DMZ or proxy.
- Firewalls, antivirus and intrusion detection systems will stop malicious activity.

These statements describe intended security controls. They do not prove that the controls work against the techniques an adversary may use.

Threat emulation challenges these assumptions by testing them and collecting evidence.

### Why organisations use it

1. Identify weaknesses in preventive controls.
2. Check whether security tools generate useful telemetry.
3. Evaluate whether the SOC recognises suspicious behaviour.
4. Test whether response actions are effective.
5. Produce recommendations that can be validated through another test.

---

## 3. What Is Threat Emulation?

**Threat emulation** is an intelligence-driven reproduction of real-world attack scenarios and adversary TTPs in a controlled environment. Its purpose is to test, assess and improve an organisation's security defences and response capabilities.

The emulation team attempts to behave like an adversary described by threat intelligence. The defensive team then evaluates what its controls detect, prevent or miss.

### Blind and non-blind operations

| Type | Meaning |
|---|---|
| **Blind operation** | The exercise is not announced to the wider defensive team. This is commonly associated with a Red Team engagement and tests how defenders respond without advance knowledge of the activity. |
| **Non-blind operation** | The participating security teams know about the exercise. This supports coordination, knowledge sharing and collaborative improvement. |

The choice depends on the exercise objectives. A blind exercise tests response under less predictable conditions; a non-blind exercise can make it easier to investigate techniques and improve detections together.

---

## 4. Emulation vs Simulation

The terms are sometimes used interchangeably, but the room describes an important distinction.

| Threat emulation | Threat simulation |
|---|---|
| Replicates the behaviour of a particular real-world adversary using threat intelligence. | Uses predefined or automated attack patterns representing adversary behaviour. |
| Aims to imitate a specific threat actor or campaign as accurately as practical. | May combine TTPs from multiple threat groups without copying one specific actor. |
| Intelligence-driven and adversary-specific. | Often pattern-driven and predefined. |

**Remember:** Emulation asks, “How would this known adversary behave?” Simulation asks, “What happens when we run this selected set of attack behaviours?”

---

## 5. The Emulation Spectrum

Threat emulation can be performed at different levels of depth.

### 5.1 Atomic testing

- Runs an individual technique in isolation.
- Maps the test to MITRE ATT&CK.
- Produces focused and repeatable telemetry.
- Useful for validating one detection at a time.
- The next room in the module introduces Atomic Red Team.

### 5.2 Adversary emulation

- Chains multiple TTPs together.
- Represents a particular adversary's campaign.
- Can cover a sequence from initial access through later attack stages and impact.
- Tests whether defenders can detect activity across an attack sequence, not just one isolated event.

### 5.3 Purple teaming

- Red Team and Blue Team work together.
- The Red Team performs selected techniques.
- The Blue Team checks telemetry and detections as the activity occurs.
- Both teams collaborate to improve detection and response.

| Activity | Main focus |
|---|---|
| Atomic testing | One technique at a time |
| Adversary emulation | A connected adversary campaign |
| Purple teaming | Collaborative execution and detection improvement |

---

## 6. Key Characteristics

| Characteristic | Explanation |
|---|---|
| **Real-world threats** | TTPs are based on real incidents, campaigns and threat intelligence, including knowledge bases such as MITRE ATT&CK. |
| **Behaviour-focused** | Tests adversary behaviour rather than relying only on known malware signatures. |
| **Transparent** | In a collaborative exercise, relevant teams share information so the organisation can improve its overall security posture. |
| **Collaborative** | Red and Blue Teams work towards improving security, rather than treating the exercise only as a competition. |
| **Repeatable** | Tests can be run again to establish a baseline and verify whether defensive improvements work. |

Repeatability is especially important: after a detection rule or security configuration is improved, the same technique can be tested again to check whether the gap has been closed.

---

## 7. Frameworks, Resources and Methodologies

These three categories have different roles in an emulation exercise.

| Category | What it provides | Example from the room |
|---|---|---|
| **Framework** | Knowledge base and structure for understanding adversary behaviour. | MITRE ATT&CK |
| **Resource** | Libraries, test cases or plans that help teams perform emulation. | Atomic Red Team; CTID Adversary Emulation Library |
| **Methodology** | A structured process for planning and carrying out an exercise. | TIBER-EU |

### 7.1 MITRE ATT&CK — Framework

[MITRE ATT&CK](https://attack.mitre.org/) is a knowledge base of adversary tactics, techniques and sub-techniques observed in real-world activity.

It gives emulation teams a shared language for:

- Identifying techniques used by a threat actor.
- Understanding how those techniques work.
- Mapping techniques to defensive detections and mitigations.
- Selecting behaviours to test in an environment.

The room describes the ATT&CK matrix as organising **14 tactics**, from reconnaissance to impact, with techniques and sub-techniques under them.

**ATT&CK Navigator** allows teams to create colour-coded layers. A layer can highlight techniques associated with a particular adversary or relevant to a platform. This helps teams visualise and prioritise what they plan to test.

Resources:
- [MITRE ATT&CK](https://attack.mitre.org/)
- [TryHackMe MITRE room](https://tryhackme.com/room/mitre)
- [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)

### 7.2 Atomic Red Team — Resource

[Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) is a library of focused emulation tests maintained by Red Canary.

Each test is called an **atomic**. An atomic is a small, focused test that executes one technique and generates telemetry that can be examined by defenders.

Important points:

- Atomics map to MITRE ATT&CK techniques.
- They help validate whether a detection works.
- They can be repeated after a detection or configuration change.
- The library supports multiple platforms, including Windows, Linux, macOS and cloud environments.

**Example workflow:** Select an ATT&CK technique → identify a matching atomic → run it in an authorised test environment → inspect generated telemetry → evaluate the detection.

### 7.3 CTID Adversary Emulation Library — Resource

The [Center for Threat-Informed Defense (CTID)](https://mitre-engenuity.org/cybersecurity/center-for-threat-informed-defense/) is a research and development organisation operated by MITRE Engenuity.

Its [Adversary Emulation Library](https://github.com/center-for-threat-informed-defense/adversary_emulation_library) provides open-source plans that organisations can use to evaluate their security capabilities against known threats.

The room describes two approaches:

| Approach | Explanation |
|---|---|
| **Full emulation** | A more comprehensive emulation of a particular adversary, potentially covering the campaign from initial access to exfiltration. The room gives the APT29 plan as an example. |
| **Micro emulation** | A focused emulation of selected behaviours, such as file access or process injection, across relevant adversary techniques. |

**Important distinction:** CTID provides emulation plans as a resource. A plan is not itself an organisational methodology; the team still needs a process for safely executing and documenting it.

Example: [CTID APT29 emulation plan](https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/6a5b0413dbe2761d2cb08afe2729d6cf9d021ab6/apt29)

### 7.4 TIBER-EU — Methodology

[TIBER-EU](https://www.ecb.europa.eu/paym/cyber-resilience/tiber-eu/html/index.en.html) stands for **Threat Intelligence-based Ethical Red Teaming**. The room presents it as a formal methodology developed for the European financial sector.

It provides a structured three-phase approach for intelligence-led testing against critical live production systems.

#### Phase 1 — Preparation

- Establish the security teams.
- Define and approve the scope.
- Complete planning and procurement.
- Obtain the necessary organisational approval before testing.

#### Phase 2 — Testing

- The threat intelligence team prepares a report describing relevant threat areas and attack scenarios.
- The Red Team conducts the agreed emulation against critical systems.
- The Blue Team observes and assesses defensive performance.

#### Phase 3 — Closure

- Teams prepare analysis reports.
- Document what was tested and what was found.
- Provide recommendations for technical controls, policies and awareness training.

**Memory aid:** Preparation → Testing → Closure.

---

## 8. Threat Emulation Process

The room presents a five-step process. The later tasks break observation and reporting out as additional activities, so the complete learning sequence below is shown in six practical steps.

| Step | Activity | Main question |
|---|---|---|
| 1 | Define objectives | What are we trying to test? |
| 2 | Research adversary TTPs | Which adversary behaviours are relevant? |
| 3 | Plan the engagement | How will we perform the test safely and with approval? |
| 4 | Conduct the emulation | How will the selected TTPs be carried out? |
| 5 | Observe results | What did the security controls detect or miss? |
| 6 | Document and report findings | What should be improved and retested? |

### Step 1 — Define Objectives

An emulation exercise should have clear, specific and measurable objectives.

The scenario in the room involves **VASEPY Corp**, a large U.S. retail company concerned about threats following a competitor's breach.

The objective selected for VASEPY Corp is to identify gaps in protection against:

- Credit card fraud.
- Ransomware attacks.

The scope must also identify which systems and data are included in the exercise.

**Why this matters:** Without objectives and scope, a team may run tests that do not answer the organisation's actual security questions or may affect systems that were never approved for testing.

### Step 2 — Research Adversary TTPs

The purpose of this step is to model the target adversary's behaviour using relevant threat intelligence.

The room divides the research into four activities.

#### 2.1 Information Gathering

Collect information from internal and external sources.

Internal sources may include:

- Cyber Threat Intelligence (CTI) analysts.
- Cyber defence or SOC teams.
- System administrators.

For VASEPY Corp, the concern is financially motivated threat actors targeting retail organisations. A search of MITRE ATT&CK identifies three candidate groups in the room:

- [FIN6 (G0037)](https://attack.mitre.org/groups/G0037/)
- [FIN7 (G0046)](https://attack.mitre.org/groups/G0046/)
- [FIN8 (G0061)](https://attack.mitre.org/groups/G0061/)

#### 2.2 Select the Adversary

The shortlist is narrowed using four factors:

| Factor | Question to ask |
|---|---|
| **Relevance** | Does the adversary match the organisation's industry, goals and geography? |
| **Available CTI** | Is there enough reliable information about the adversary's TTPs? |
| **TTP complexity** | Can existing tools perform the tests, or would custom tools be required? |
| **Available resources** | Are enough budget, time and personnel available? |

For the VASEPY Corp scenario, **FIN7** is selected because the room identifies it as a group that specifically targets U.S.-based retail entities.

#### 2.3 Select the TTPs

Use ATT&CK and ATT&CK Navigator to visualise the selected adversary's techniques.

The team should prioritise techniques based on their relevance to the organisation and its environment. The objective is not to execute every technique indiscriminately; it is to select meaningful behaviours that answer the exercise objectives.

#### 2.4 Construct the TTP Outline

Create an outline describing:

- Planned activities.
- Scope of the activity.
- Rules of engagement.
- How each selected TTP will be implemented.

Adversary behaviour can change as threat intelligence develops. Therefore, the outline should be kept current rather than treated as a permanent description of the adversary.

### Step 3 — Plan the Engagement

Threat emulation imitates cyberattack behaviour. Poor planning can lead to data loss, unexpected downtime or exposure of private information.

The engagement plan keeps the exercise controlled and aligned with the organisation's approval.

#### Components of an emulation plan

| Component | What it should define |
|---|---|
| **Engagement objectives** | What the exercise is intended to achieve and why. |
| **Scope** | The departments, users, devices and systems on which testing is permitted. |
| **Schedule** | Dates and times for activities and deliverables, avoiding conflicts with business operations. |
| **Rules of engagement** | Which adversary behaviours are permitted and what mitigation actions apply to high-risk TTPs. |
| **Permission to execute** | Explicit written approval from an appropriate organisational authority. |
| **Communication plan** | How and when the emulation team and stakeholders communicate. |

**Remember:** A technically correct attack plan is not sufficient. The activity also needs scope, written permission, timing, safety boundaries and communication arrangements.

### Step 4 — Conduct the Emulation

The team carries out the selected TTPs in a controlled environment. The room describes three typical lab components:

| Component | Purpose |
|---|---|
| **Attack platform** | The system from which the emulation activity is executed. |
| **Analysis platform** | The system used to collect forensic details and analyse artefacts. |
| **Test systems** | The target systems on which the selected TTPs are deployed and observed. |

#### 4.1 Plan the Deployment

Before execution:

1. Revisit the selected FIN7 TTPs.
2. Map the techniques using ATT&CK and ATT&CK Navigator.
3. Review CTI reports to understand how the techniques appeared in actual campaigns.
4. Prepare the lab environment.
5. Confirm that every team member understands their responsibilities.

The room references:

- [Mandiant research on FIN7](https://www.fireeye.com/blog/threat-research/2017/04/fin7-phishing-lnk.html)
- [eSentire FIN7 report](https://www.esentire.com/security-advisories/notorious-cybercrime-gang-fin7-lands-malware-in-law-firm-using-fake-legal-complaint-against-jack-daniels-owner-brown-forman-inc)
- [CTID FIN7 emulation plan](https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Emulation_Plan/Scenario_1)

#### 4.2 Implement the TTP

The room uses FIN7 initial access as an example. It describes an emulation involving an RTF document delivered through a spear-phishing scenario. FIN7 has been associated in the room's explanation with DOCX and RTF files containing embedded Windows Shortcut (`.LNK`) files.

The technique referenced is:

**MITRE ATT&CK T1204.002 — Malicious File Execution**

The room provides the following command fragment from the CTID FIN7 emulation plan:

```shell-session
# Copy 2-list.rtf to Desktop on hotelmanager.
sudo smbclient -U '\\' ///C$ -c "put fin7/Resources/Step1/SQLRat/2-list.rtf Users\\.\\Desktop\\2-list.rtf"

# Provide password when prompted.

# Log in to the victim workstation as the authorised lab user.
xfreerdp +clipboard /u:"<username>" /p:"<password>" /v:"<target-host>"
```

**Important lab note:** The source text supplied for this room contains incomplete connection and account details. The command above is therefore a learning reference, not a ready-to-run command. Do not guess the missing values. Only perform this activity in the explicitly authorised TryHackMe or isolated lab environment, using the lab's actual instructions and approved test files. Do not send malicious documents to real users or systems.

What the example is illustrating:

- `smbclient` is used to interact with an SMB share and transfer the file to the test workstation.
- The `C$` share is an administrative Windows share in the example.
- `xfreerdp` is used to establish an RDP session to the test workstation.
- The exercise represents delivery and user execution of a file, which is the behaviour defenders are expected to monitor.

#### 4.3 Detections and Mitigations

The Blue Team must determine how to detect and mitigate the emulated technique.

The SOC uses security tools to collect, correlate and analyse the activity and related logs. MITRE ATT&CK provides detection and mitigation information for individual techniques.

For this example, consult the ATT&CK page for [T1204.002 — Malicious File](https://attack.mitre.org/techniques/T1204/002/).

The room also points to [YARA](https://tryhackme.com/room/yara) as a useful detection-rule resource and gives the [FIN7 pillowMint.exe YARA rule](https://github.com/center-for-threat-informed-defense/adversary_emulation_library/blob/master/fin7/yara-rules/pillowmint.txt) as an example.

**Key distinction:** Emulation is not complete just because the Red Team successfully performed a technique. The defensive team must also determine what telemetry was generated, whether it was detected, and whether an appropriate response occurred.

### Step 5 — Observe Results

While the emulation is running, the Blue Team actively searches for artefacts associated with the executed TTPs.

The room identifies three observation channels:

| Observation channel | What the team examines |
|---|---|
| **Log analysis** | System and application logs generated by the activity. |
| **Event log evaluation** | Relevant Windows Event IDs and Sysmon events. |
| **Network traffic monitoring** | Network connections, DNS queries and data flows. |

#### Classifying the result of each TTP

Each tested technique should be assigned one of three outcomes:

| Result | Meaning | What it tells the team |
|---|---|---|
| **Detected and blocked** | The activity was identified and prevented. | The relevant defensive control worked as expected for this test. |
| **Detected but not blocked** | The activity was visible, but it was not prevented. | Visibility exists, but response or prevention needs improvement. |
| **Not detected** | The activity was not identified by the defensive controls. | A detection or visibility gap exists. |

The FIN7 example highlights detection rules and references the YARA rule for `pillowMint.exe`. This illustrates how detection logic can be used to identify known malware artefacts. Behavioural telemetry remains important as well, because threat emulation aims to assess adversary behaviour rather than relying only on file signatures.

### Step 6 — Document and Report Findings

After observation, the teams document what happened and what should change.

A useful report includes:

| Section | What to record |
|---|---|
| **Exercise summary** | A high-level overview of the exercise, adversary emulated and TTPs tested. |
| **Findings** | For every TTP, state whether it was detected, blocked or missed, and include supporting log evidence. |
| **Gaps identified** | Detection and visibility weaknesses discovered during the exercise. |
| **Recommendations** | Specific actions such as adding detection rules, changing configurations or tuning existing controls. |
| **Re-validation plan** | Which TTPs should be executed again after improvements to confirm that the gaps are closed. |

A strong finding answers three questions:

1. **What was executed?** — Identify the TTP and the activity performed.
2. **What was observed?** — Record the telemetry, alert, response or absence of detection.
3. **What needs to change?** — Explain the recommended improvement.

The report should be evidence-based. “The test failed” is not enough; the team should describe which activity was tested, what evidence supports the result and what action is required.

---

## 9. VASEPY Corp and FIN7 Case Study

This scenario connects the process steps.

| Area | Decision in the room |
|---|---|
| Organisation | VASEPY Corp, a large U.S. retail company |
| Business concerns | Credit card fraud and ransomware |
| Candidate adversaries | FIN6, FIN7 and FIN8 |
| Selected adversary | FIN7 |
| Reason for selection | The scenario identifies FIN7 as relevant to U.S.-based retail entities. |
| Technique example | T1204.002 — Malicious File Execution |
| Delivery example | RTF document in a spear-phishing scenario |
| Defensive evaluation | Logs, Windows events, Sysmon and network traffic |
| Example detection resource | YARA rule for `pillowMint.exe` |
| Final output | Findings, identified gaps, recommendations and re-validation plan |

### Process in one view

```text
Business objective
      |
      v
Research relevant adversaries and their TTPs
      |
      v
Select techniques and build the TTP outline
      |
      v
Approve scope, schedule and rules of engagement
      |
      v
Execute the techniques in the controlled lab
      |
      v
Blue Team observes logs, events and network traffic
      |
      v
Classify each result: detected/blocked, detected/not blocked, or missed
      |
      v
Report gaps and recommendations
      |
      v
Re-run the relevant techniques to validate improvements
```

---

## 10. Important Terms

| Term | Meaning in this room |
|---|---|
| **Threat emulation** | Intelligence-driven reproduction of real adversary behaviour to evaluate security controls. |
| **Threat simulation** | Use of predefined or automated attack patterns representing adversary behaviour. |
| **TTP** | Tactics, techniques and procedures used by adversaries. |
| **CTI** | Cyber Threat Intelligence: information about threats that supports adversary research and decisions. |
| **Atomic** | A focused test of one technique, commonly mapped to ATT&CK. |
| **Adversary emulation** | Chaining TTPs to represent a particular adversary's campaign. |
| **Purple Teaming** | Red and Blue Teams working together to perform tests and improve detections. |
| **ATT&CK Navigator** | A tool for visualising and prioritising ATT&CK techniques in layers. |
| **Rules of engagement** | Agreed boundaries describing what the emulation team is permitted to do. |
| **YARA** | A rule-based tool referenced in the room for identifying patterns associated with files or malware. |
| **Re-validation** | Repeating relevant tests after a change to check whether the defensive gap has been addressed. |

---

## 11. SOC Analyst Perspective

Threat emulation is useful to a SOC because it tests the entire defensive workflow, not just whether a security product is installed.

When a technique is executed, a SOC analyst should think through the following questions:

### Before the exercise

- Which adversary and ATT&CK technique are being tested?
- What is the expected activity and which systems are in scope?
- Which log sources should provide visibility?
- What does the organisation expect the control to detect or prevent?

### During the exercise

- Did the endpoint or server create relevant logs?
- Did Windows Event Logs or Sysmon record the activity?
- Did network monitoring show related connections or DNS activity?
- Did the SIEM receive the relevant events?
- Was an alert generated?
- Was the activity blocked, or did it continue?

### After the exercise

- What evidence supports the outcome?
- Was the technique detected but not blocked, or was it completely missed?
- Does the detection rule need to be created or tuned?
- Does the control configuration need to change?
- Has the same technique been re-tested after the fix?

### Connection to normal SOC work

| Threat emulation activity | Related SOC work |
|---|---|
| Map an adversary technique to ATT&CK | Understand and classify attacker behaviour. |
| Identify relevant logs and events | Log-source onboarding and telemetry validation. |
| Execute a controlled test | Detection validation and security control testing. |
| Review alerts and event data | Alert triage and investigation. |
| Identify a missed technique | Detection-gap analysis. |
| Recommend a rule or configuration change | Detection engineering and security improvement. |
| Re-run the test | Detection validation and regression testing. |

**Main SOC lesson:** An alert is not the only measure of success. The team must know whether the relevant telemetry was collected, whether the alert was meaningful, whether the response was appropriate and whether the improvement works when tested again.

---

## 12. Revision Checklist

Use this checklist to check whether the main ideas are clear.

- [ ] Explain why having a firewall, antivirus and patches does not prove that an organisation is secure.
- [ ] Define threat emulation in your own words.
- [ ] Explain blind and non-blind operations.
- [ ] Distinguish threat emulation from threat simulation.
- [ ] Explain atomic testing, adversary emulation and purple teaming.
- [ ] Distinguish a framework, a resource and a methodology.
- [ ] Explain the role of MITRE ATT&CK and ATT&CK Navigator.
- [ ] Explain what an Atomic Red Team atomic test is.
- [ ] Describe the purpose of the CTID Adversary Emulation Library.
- [ ] Recall the three TIBER-EU phases.
- [ ] List the stages of the threat emulation process.
- [ ] Explain the four activities involved in researching adversary TTPs.
- [ ] List the key components of an emulation plan.
- [ ] Explain the three components of an emulation lab.
- [ ] Describe the three ways the Blue Team observes results.
- [ ] Classify an outcome as detected and blocked, detected but not blocked, or not detected.
- [ ] Explain what should be included in an emulation report.

---
