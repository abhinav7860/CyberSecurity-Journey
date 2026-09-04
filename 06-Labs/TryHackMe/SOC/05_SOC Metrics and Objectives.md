# SOC Metrics and Objectives — TryHackMe

**Date:** September 4, 2026  
**Platform:** TryHackMe  
**Room:** SOC Metrics and Objectives  
**Focus:** SOC metrics, MTTD, MTTA, MTTR, SLA, False Positive Rate, Threat Detection Rate, and improving SOC performance.

---

# Task 1 — Introduction

Today I worked on the **TryHackMe SOC Metrics and Objectives** room.

A SOC can measure its efficiency using different indicators and metrics. These metrics help the team understand its workload, alert quality, detection capability, and response speed.

The main metrics I learned were:

- Alerts Count (AC)
- False Positive Rate (FPR)
- Alert Escalation Rate (AER)
- Threat Detection Rate (TDR)
- Mean Time to Detect (MTTD)
- Mean Time to Acknowledge (MTTA)
- Mean Time to Respond (MTTR)

I also learned how poor metrics can affect both the security of an organisation and the workload of SOC analysts.

---

# Task 2 — Core Metrics

The main goal of a SOC is to protect the **confidentiality, integrity, and availability** of an organisation's digital assets.

The SOC performs this role by developing, receiving, and triaging alerts. L1 analysts are especially important because they need to reliably identify and report True Positives to L2.

## Core Metrics

| Metric | Formula | Measures |
|---|---|---|
| **Alerts Count (AC)** | `AC = Total Count of Alerts Received` | Overall SOC analyst workload |
| **False Positive Rate (FPR)** | `FPR = False Positives / Total Alerts` | Amount of noise in alerts |
| **Alert Escalation Rate (AER)** | `AER = Escalated Alerts / Total Alerts` | Experience/independence of L1 analysts |
| **Threat Detection Rate (TDR)** | `TDR = Detected Threats / Total Threats` | Reliability of the SOC |

## Alerts Count

Alerts Count measures how many alerts the SOC receives.

```text
AC = Total Count of Alerts Received
```

For example, 80 unresolved alerts at the beginning of a shift can be overwhelming and can make it easier to miss a real threat hidden among the noise.

However, **zero alerts is not automatically good**. A very low alert count could indicate:

- SIEM problems
- Missing visibility
- Broken detection rules
- Missing log sources
- Undetected breaches

The room states that **5–30 alerts per day per L1 analyst** is generally a good metric, although the ideal number depends on the organisation.

## False Positive Rate

FPR measures how many alerts turn out to be False Positives.

```text
FPR = False Positives / Total Alerts
```

If 75 out of 80 alerts are False Positives:

```text
FPR = 75 / 80 = 93.75%
```

A high FPR creates alert noise and can lead to **alert fatigue**. When analysts repeatedly see harmless alerts, they can become less vigilant and may miss a genuine attack.

The room explains that **0% is an unrealistic ideal**, while **80% or higher is a serious problem**.

High FPR can be addressed through **False Positive Remediation**, such as tuning detection rules and excluding trusted activity.

## Alert Escalation Rate

AER measures how often L1 analysts escalate alerts to higher-level analysts.

```text
AER = Escalated Alerts / Total Alerts
```

L2 depends on L1 to filter out noise and escalate actionable threats. However, L1 should also ask for help when an alert is not fully understood.

The room says AER is generally aimed to be:

- Below **50%**
- Preferably below **20%**

## Threat Detection Rate

TDR measures how many real threats the SOC successfully detects.

```text
TDR = Detected Threats / Total Threats
```

Example:

```text
6 attacks occurred
4 were detected
2 were missed

TDR = 4 / 6 = 67%
```

This is a bad result. The room states that TDR should ideally be **100%**, because every missed threat can potentially lead to serious consequences such as ransomware or data exfiltration.

---

# Task 2 — Answers

**Is zero alerts for one month a good sign?**  
**Answer: Nay**

**What is the FPR if only 10 out of 50 alerts are real threats?**

```text
Real threats = 10
False Positives = 50 - 10 = 40

FPR = 40 / 50 = 80%
```

**Answer: 80%**

---

# Task 3 — Triage Metrics

An alert by itself does not stop a breach. The SOC needs to detect the threat, receive and acknowledge the alert, investigate it, and respond before attackers achieve their goals.

These timing requirements are commonly defined in a **Service Level Agreement (SLA)**.

An SLA can exist between:

- An internal SOC and company management
- A Managed Security Service Provider (MSSP) and its customers

The main time-based metrics are:

- MTTD
- MTTA
- MTTR

## MTTD — Mean Time to Detect

MTTD is the average time between an attack occurring and the SOC tools detecting it.

```text
Attack occurs
     ↓
   MTTD
     ↓
Threat detected
```

Reference SLA: **5 minutes**

## MTTA — Mean Time to Acknowledge

MTTA is the average time between an alert being generated and an L1 analyst starting the triage.

```text
Alert generated
     ↓
   MTTA
     ↓
L1 starts triage
```

Reference SLA: **10 minutes**

## MTTR — Mean Time to Respond

MTTR is the average time taken by the SOC to actually stop or contain the breach.

Examples include:

- Isolating a device
- Securing a breached account
- Removing malware
- Stopping malicious activity

Reference SLA: **60 minutes**

## Reference Table

| Metric | Common SLA | Description |
|---|---:|---|
| SOC Team Availability | 24/7 | SOC working schedule; some teams may use 8/5 |
| MTTD | 5 minutes | Time from attack to detection |
| MTTA | 10 minutes | Time from alert to L1 starting triage |
| MTTR | 60 minutes | Time taken to stop/contain the breach |

Different SOC teams may define metrics differently, so for this room I used the definitions provided by TryHackMe.

## Saturday Scenario

If the SOC works **8/5** and receives a critical alert on Saturday, the alert will be acknowledged on:

**Monday**

## Redline Stealer Scenario

The room gave this timeline:

1. SOC received the **Connection to Redline Stealer C2** alert after 12 minutes.
2. L1 moved it to In Progress 10 minutes later.
3. It was escalated to L2 after another 6 minutes.
4. L2 spent 35 minutes cleaning the malware.

The accepted answer was:

```text
12,10,51
```

Therefore:

- **MTTD = 12**
- **MTTA = 10**
- **MTTR = 51**

---

# Task 4 — Improving Metrics

Metrics are used to make the SOC more efficient and reduce the chance of successful attacks. They can also be used to evaluate team performance.

## FPR Over 80%

**Problem:** Too much alert noise.

### Recommendations

1. Exclude trusted activities such as system updates from EDR/SIEM detection rules.
2. Automate common alert triage using SOAR or custom scripts.

## MTTD Over 30 Minutes

**Problem:** Threat detection is too slow.

### Recommendations

1. Contact SOC engineers and make detection rules run faster or more frequently.
2. Check whether SIEM logs are being collected in real time instead of arriving with delays such as 10 minutes.

## MTTA Over 30 Minutes

**Problem:** L1 analysts start triage too slowly.

### Recommendations

1. Ensure analysts receive real-time notifications for new alerts.
2. Distribute alerts evenly between analysts on shift.

## MTTR Over 4 Hours

**Problem:** The SOC cannot stop the breach quickly enough.

### Recommendations

1. As L1, quickly escalate threats that require L2 action.
2. Ensure the team has documented procedures for different attack scenarios.

### Question

**What is the highest acceptable False Positive Rate for SOC teams?**

**Answer: 80%**

---

# Task 5 — Practice Scenarios

The practice lab asked me to act like a SOC manager and improve metrics across three scenarios by assigning the correct improvement task to the correct person/team.

The three scenarios were:

1. Unhappy Customer
2. Delayed Alert
3. Tired Analysts

---

# Scenario 1 — Unhappy Customer

## Situation

OpenDoor Inc., a major customer, was unhappy with how the SOC handled a breach.

The customer's CFO's email and Entra ID account were breached.

It took the SOC almost **5 hours** to kick the attacker out of the mailbox and clean the account. The attacker had enough time to dump emails and leak them on the Darknet.

## Problematic Metric

**MTTR was too high.**

The SOC spent too much time containing the attack.

## Improvement Task

Create a **workbook explaining credential rotation steps** and present it to the team.

A documented procedure can make credential-related response faster and more consistent.

## Assign the Task To

**The L2 that handled the incident**

The L2 already handled the incident and is therefore in a good position to document the procedure and lessons learned.

## Flag

```text
THM{mttr:quick_start_but_slow_response}
```

---

# Scenario 2 — Delayed Alert

## Situation

The SOC successfully stopped a ransomware simulation in 40 minutes, but during the first **20 minutes** everyone was waiting for an alert to appear.

This created a detection delay.

## Problematic Metric

**MTTD was too high.**

The scenario specifically identified:

> Time to Detect of 20 minutes led to a delayed alert triage.

## Improvement Task

**Tune the SIEM and detection rules to run more often, every 5 minutes.**

More frequent detection can reduce the delay between an attack occurring and the SOC receiving an alert.

## Assign the Task To

**SOC Engineer**

The SOC engineer is responsible for detection-rule and SIEM-related technical improvements.

## Flag

```text
THM{mttd:time_between_attack_and_alert}
```

---

# Scenario 3 — Tired Analysts

## Situation

The L1 analysts reported that their workload was becoming too high.

During an 8-hour shift:

- L1 analysts close around **760 alerts**
- **95%** are system noise from IT teams or automation scripts
- The workload makes vigilant triage difficult
- Analysts are becoming exhausted
- The company is growing and the number of alerts is expected to increase

## Problematic Metric

**False Positive Rate was the core problem.**

If 95% of alerts are noise, analysts spend most of their time investigating activity that is not actually threatening.

This can cause:

```text
High FPR
   ↓
Alert noise
   ↓
Too much manual investigation
   ↓
Analyst fatigue
   ↓
Reduced vigilance
   ↓
Higher chance of missing a real threat
```

## Improvement Task

**Exclude system and IT noise from the detection rules.**

The goal is to reduce unnecessary alerts and therefore reduce the FPR.

## Assign the Task To

**SOC Engineers**

SOC engineers can tune the detection rules to exclude trusted system and IT activity.

## Flag

```text
THM{fpr:the_main_cause_of_l1_burnout}
```

---

# Practice Scenario Summary

| Scenario | Problem | Metric | Improvement | Assigned To | Flag |
|---|---|---|---|---|---|
| Unhappy Customer | Breach took too long to contain | MTTR | Credential-rotation workbook | L2 that handled incident | `THM{mttr:quick_start_but_slow_response}` |
| Delayed Alert | Threat detected after 20 minutes | MTTD | Run SIEM/detection rules every 5 minutes | SOC Engineer | `THM{mttd:time_between_attack_and_alert}` |
| Tired Analysts | 95% of alerts were noise | FPR | Exclude system/IT noise | SOC Engineers | `THM{fpr:the_main_cause_of_l1_burnout}` |

---

# How the Metrics Connect

## FPR → Analyst Fatigue

```text
High FPR
 ↓
More noisy alerts
 ↓
More work
 ↓
Analyst fatigue
 ↓
Less vigilance
 ↓
Possible missed threat
```

## MTTD → Detection Speed

```text
Attack
 ↓
Detection
 ↓
MTTD
```

A high MTTD means attackers have more time before the SOC even knows something is wrong.

## MTTA → L1 Response

```text
Alert generated
 ↓
MTTA
 ↓
L1 starts triage
```

A high MTTA means the alert is waiting too long before an analyst starts investigating.

## MTTR → Containment

```text
Threat detected
 ↓
Investigation
 ↓
Escalation / Response
 ↓
MTTR
 ↓
Breach contained
```

A high MTTR means the SOC takes too long to stop the breach.

---

# Metric Cheat Sheet

| Metric | Full Name | What I remember |
|---|---|---|
| **AC** | Alerts Count | How many alerts are received |
| **FPR** | False Positive Rate | How much alert noise exists |
| **AER** | Alert Escalation Rate | How often L1 escalates |
| **TDR** | Threat Detection Rate | How many real threats are detected |
| **MTTD** | Mean Time to Detect | Attack → detection |
| **MTTA** | Mean Time to Acknowledge | Alert → L1 starts triage |
| **MTTR** | Mean Time to Respond | Response time until breach is stopped/contained |

---

# Important Thresholds From the Room

```text
Good alert count:
5–30 alerts/day/L1 analyst

Serious FPR problem:
80% or higher

Preferred AER:
Below 50%
Better: below 20%

Target TDR:
100%

Reference MTTD:
5 minutes

Reference MTTA:
10 minutes

Reference MTTR:
60 minutes

MTTD problem:
Over 30 minutes

MTTA problem:
Over 30 minutes

MTTR problem:
Over 4 hours
```

---

# My Takeaway

Today I learned that SOC metrics are not just numbers that management looks at. They describe how effectively the SOC is detecting, triaging, and responding to threats.

The three time-based metrics are especially important:

- **MTTD** → How quickly the threat was detected.
- **MTTA** → How quickly L1 started working on the alert.
- **MTTR** → How quickly the SOC stopped or contained the breach.

I also learned that a large number of alerts does not automatically mean a SOC is performing well. If most alerts are False Positives, analysts can become exhausted and may miss a genuine attack.

At the same time, zero alerts can also be a warning sign because the SOC might have broken detection, missing logs, or poor visibility.

Another important lesson is that metrics should lead to action.

```text
High FPR
 ↓
Tune detection rules
 ↓
Less noise
 ↓
Less analyst fatigue
```

```text
High MTTD
 ↓
Improve log collection / detection frequency
 ↓
Threat detected earlier
```

```text
High MTTA
 ↓
Improve notifications / alert distribution
 ↓
L1 starts sooner
```

```text
High MTTR
 ↓
Improve escalation / response procedures
 ↓
Breach contained faster
```

The biggest thing I understood from this room is that **SOC performance is a complete process**. Detection, triage, reporting, escalation, communication, and response are connected. A weakness in one part can affect the entire security operation.

---

# Quick Revision

```text
                         ATTACK
                           ↓
                  MTTD — Detection
                           ↓
                      ALERT
                           ↓
                  MTTA — L1 starts
                           ↓
                       TRIAGE
                           ↓
                   ESCALATION
                           ↓
                    L2 / RESPONSE
                           ↓
                  MTTR — Containment
                           ↓
                  BREACH STOPPED
```

At the same time:

```text
AC  → How many alerts?

FPR → How much noise?

AER → How often does L1 escalate?

TDR → How many real threats are detected?
```

---

# Final Answers

| Task | Question | Answer |
|---|---|---|
| Task 2 | Zero alerts for one month is good? | **Nay** |
| Task 2 | FPR when 10/50 are real threats | **80%** |
| Task 3 | Saturday alert with 8/5 SOC | **Monday** |
| Task 3 | Redline Stealer MTTD, MTTA, MTTR | **12,10,51** |
| Task 4 | Highest acceptable FPR | **80%** |

---

# Flags

### Scenario 1

```text
THM{mttr:quick_start_but_slow_response}
```

### Scenario 2

```text
THM{mttd:time_between_attack_and_alert}
```

### Scenario 3

```text
THM{fpr:the_main_cause_of_l1_burnout}
```

---
