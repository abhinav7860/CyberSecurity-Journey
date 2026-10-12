# TryHackMe: Intro to Detection Engineering

**Date added:** 12 October 2026\
**Room:** Intro to Detection Engineering\
**Focus:** SOC, detection logic, alert quality, and the detection
engineering lifecycle\
**Status:** Learning notes based on the room material studied on 12
October 2026

------------------------------------------------------------------------

## 1. What is Detection Engineering?

Detection Engineering (DE) is the systematic process of designing,
building, testing, deploying, and maintaining detections that help a
Security Operations Centre (SOC) identify suspicious or malicious
activity.

A SIEM can collect millions of events and still fail to help analysts if
its detections are poor. For example, a SOC might receive 100 alerts
every hour, most of which are noise, while a real attacker remains
unnoticed. Detection Engineering works to make alerts more useful and to
reduce the chance that important activity is missed.

A detection is not just a query or rule that fires once. It should be
researched, checked against available data, tested, documented, deployed
carefully, and reviewed over time.

### Detection Engineering and a SOC Analyst

  -----------------------------------------------------------------------
  SOC Analyst                         Detection Engineer
  ----------------------------------- -----------------------------------
  Investigates alerts produced by     Builds and improves the detections
  security tools.                     that produce alerts.

  Triages suspicious activity and     Researches attacker techniques and
  decides whether it needs            turns them into detection logic.
  escalation.                         

  Works mainly with the alerts and    Proactively looks for gaps and
  tools already available.            tests detection quality.

  Provides investigation feedback     Uses analyst feedback to tune and
  that can improve detections.        maintain detection rules.
  -----------------------------------------------------------------------

The roles can overlap. In a smaller SOC, L2 or L3 analysts may also be
responsible for detection engineering. In a more mature organisation, a
detection engineer may work inside the SOC or as part of a separate
detection engineering team.

## 2. Where Detection Engineering Fits in a SOC

The room describes three possible team structures:

### Low maturity / limited resources

-   L1 analysts focus on alert triage.
-   L2/L3 analysts handle detection engineering when needed.
-   There may be no dedicated detection engineering role.

### Mid maturity

-   Detection engineering is performed by a person or role embedded in
    the SOC.
-   L1/L2 analysts continue handling alerts.
-   Detection improvements are part of the SOC's regular work.

### High maturity

-   L1/L2 analysts focus on alert triage and investigation.
-   A dedicated Detection Engineering team independently builds and
    maintains detections.
-   The SOC and detection engineering team need to work together and
    share feedback.

The right model depends on the organisation's size, budget, needs, and
maturity.

## 3. Three Core Pillars of Detection Engineering

### 3.1 Detection creation

Research a threat or attacker technique, identify what evidence it
leaves behind, and create logic that can detect that evidence in a SIEM,
EDR, or another security tool.

### 3.2 Detection tuning

Improve a detection so that it produces fewer unnecessary alerts without
creating gaps that allow real threats to go unnoticed.

### 3.3 Detection management

Track, document, version, review, update, and eventually retire
detection rules that are no longer useful or accurate.

Detection Engineering may also include threat intelligence, automation,
threat hunting, and testing. The exact responsibilities differ between
organisations.

## 4. Detection Engineering Life Cycle

The room presents a lifecycle with seven steps. The process is
iterative: failed tests send the detection back for improvement, and
meaningful changes in attacker techniques can require new research.

### Step 0: Detection Backlog Management

**Question:** What should we detect right away in this environment?

A team cannot detect everything at once. It must prioritise the threats
and gaps that matter most to the organisation. Priorities may depend on
important assets, likely threats, business risk, incidents, and
available telemetry.

### Step 1: Threat Research

**Question:** What are the technical details of the attacker's
technique?

Learn how the behaviour works and what an attacker must do to carry it
out. Identify the observable actions, tools, events, or artefacts that
may support a detection. Research should focus on behaviour and
evidence, not just on a vague description of a threat.

### Step 2: Data Review

**Question:** Do we have logs that can show this activity? Are they
sufficient?

Check whether the necessary data sources are collected and forwarded to
the SIEM or other detection platform. Confirm that the logs contain the
fields and details needed by the proposed detection.

A detection can fail silently when the required logs are missing. Data
review also includes checking data quality, parsing, timestamps, and
whether the available telemetry gives enough visibility.

### Step 3: Detection Design

**Question:** What is the best query or rule logic to detect this
threat?

Use the threat research and available data to create detection logic.
The rule must match the intended behaviour while avoiding unnecessary
matches. The logic should be clear enough for someone else to review and
maintain.

### Step 4: Testing and Validation

**Question:** Does the detection work? Does it generate false positives?

Test the rule using suitable lab activity, test data, or known examples.
Confirm that the expected activity triggers an alert and that benign
activity does not create too much noise. If the detection fails, return
to design and improve it rather than deploying it untested.

### Step 5: Deployment

**Question:** Is the rule ready for production? Is it documented?

After successful testing and review, deploy the detection through the
organisation's process. Document what it detects, what data it needs,
its limitations, and how analysts should investigate an alert.

### Step 6: Maintenance

**Question:** Is the detection still useful? Is it generating false
positives? Does it need to change or be retired?

Environments and attacker techniques change. Review detections
regularly, tune noisy rules, check for missing telemetry, and retire
rules that no longer serve a useful purpose. If attacker behaviour
changes significantly, the lifecycle may need to restart from threat
research.

### Important lifecycle lesson

Detection Engineering is continuous. Deployment is not the finish line.
A detection should be treated as something that needs testing,
documentation, monitoring, and maintenance.

## 5. Detection Engineering Frameworks

Frameworks provide structure so that detection work is repeatable and
easier to review. The room introduces CREDO and ADS.

### CREDO

CREDO stands for: - **Creation** - **Review** - **Evaluation** -
**Deployment** - **Operations**

It emphasises that detections need review and evaluation and that
operational maintenance continues after deployment.

### ADS --- Alerting and Detection Strategy

ADS is a framework for documenting the purpose and design of a
detection. It helps ensure that another analyst can understand what the
alert is intended to identify, what data it needs, what its limitations
are, and how to validate and investigate it.

The ADS stages are explained in Section 8 below.

## 6. The Mentality of a Detection Engineer

### 6.1 The detection gap

Attackers continuously develop and change techniques. Defenders often
learn about new techniques after they have appeared in the real world.
By the time a detection is widely used, an attacker may have changed
their approach.

The detection gap is the difference between an attacker's ability to
evade detection and the defender's ability to detect the activity. The
goal is to reduce this gap as much as possible, not to assume that it
can be eliminated completely.

### 6.2 You do not need to detect everything

An attack usually involves multiple actions or techniques. Detecting one
important stage can be enough to start an investigation or disrupt the
attack. Coverage should be prioritised based on risk and useful evidence
rather than by trying to create a rule for every imaginable action.

### 6.3 Focus on durable behaviour

Detections based only on a single IP address, domain, or file hash may
become ineffective when an attacker changes that indicator.
Behaviour-based detections can be more durable when they identify
actions the attacker needs to perform. The room connects this idea to
the Pyramid of Pain.

This does not mean indicators are useless. It means detection engineers
should understand the strengths and limitations of each detection
approach.

## 7. Precision, Recall, False Positives, and False Negatives

Detection quality is about more than whether a rule fires.

### Precision

Precision asks: **Of all the alerts this detection generates, how many
are genuine threats?**

Formula:

`Precision = True Positives / (True Positives + False Positives)`

Example: A rule generates 100 alerts. After investigation, 20 are
genuine threats and 80 are false positives.

`Precision = 20 / 100 = 20%`

Low precision means analysts may spend too much time investigating
benign activity.

### Recall

Recall asks: **Of all the real attacks that occurred, how many did the
detection identify?**

Formula:

`Recall = True Positives / (True Positives + False Negatives)`

Example: There were 100 real attack events and the detection caught 70
of them.

`Recall = 70 / 100 = 70%`

Low recall means real threats are being missed.

### False positive

A detection alerts on activity that is not actually a threat. False
positives can contribute to alert fatigue.

### False negative

A real threat occurs, but the detection does not alert. False negatives
are dangerous because the gap may be invisible to analysts.

### The trade-off

A rule that alerts on everything can overwhelm the SOC. A rule that is
too restrictive can miss attacks. Good research and testing help improve
both precision and recall, but the right balance depends on the use case
and risk.

## 8. Detection Engineering Challenges

The room highlights the following practical problems:

  -----------------------------------------------------------------------
  Challenge               What it means           Lifecycle stage
  ----------------------- ----------------------- -----------------------
  Missing log sources     Required events are not Step 2: Data Review
                          collected or forwarded, 
                          so a detection may      
                          never trigger.          

  Parsing problems        Events arrive, but      Step 3: Detection
                          fields, timestamps, or  Design
                          event structure are     
                          incorrect.              

  Data volume decisions   High-volume, low-value  Step 2: Data Review
                          logs can increase costs 
                          and slow searches.      

  No testing environment  Rules reach production  Step 4: Testing &
                          without being validated Validation
                          in a realistic setting. 

  Detection library decay Old or irrelevant rules Step 6: Maintenance
                          remain active and       
                          generate noise.         

  Alert fatigue           Too many low-quality    Often Step 4: Testing &
                          alerts cause analysts   Validation
                          to lose trust in        
                          alerts.                 

  TTP drift               Attacker techniques     Step 1: Threat Research
                          change, so existing     
                          rules may no longer     
                          detect them.            

  Adjacent                Documentation,          All stages
  responsibilities        automation, and other   
                          duties compete for      
                          limited time.           
  -----------------------------------------------------------------------

### Practical ways to address these challenges

-   Maintain an inventory of log sources and document which detections
    depend on them.
-   Check that events are parsed correctly before relying on their
    fields.
-   Use a suitable lab or test data before deployment.
-   Give detections an owner and review date.
-   Monitor alert quality and investigate rules that produce too much
    noise.
-   Revisit detection logic when the environment or attacker techniques
    change.

## 9. Tools Used in Detection Engineering

The room identifies several tool categories:

  -----------------------------------------------------------------------
  Tool category           Examples from the room  Purpose
  ----------------------- ----------------------- -----------------------
  SIEM                    Splunk, Microsoft       Search logs and run
                          Sentinel, Elastic       detection rules.

  EDR                     CrowdStrike,            Collect endpoint
                          SentinelOne, Microsoft  telemetry and detect
                          Defender                host activity.

  Threat intelligence     MISP, OpenCTI, The DFIR Research attacker
                          Report                  techniques and identify
                                                  detection
                                                  opportunities.

  Automation              Python scripts, SOAR    Automate testing,
                          platforms               enrichment, and
                                                  workflows.

  Version control         Git, GitHub             Track changes and
                                                  support review of
                                                  detection logic.

  Lab/testing             Atomic Red Team, custom Simulate activity and
  environments            VMs, BAS solutions      validate detections
                                                  before production.
  -----------------------------------------------------------------------

The tool alone does not make a detection effective. The quality of the
research, available data, logic, testing, and maintenance also matters.

## 10. Applying the Concepts to a Simple SOC Example

Suppose a SOC wants to detect suspicious PowerShell execution.

1.  **Prioritise:** Decide why suspicious PowerShell activity matters in
    this environment.
2.  **Research:** Learn what suspicious execution looks like and what
    evidence it may leave.
3.  **Review data:** Confirm that the relevant Windows and PowerShell
    logs are collected and parsed.
4.  **Design:** Write detection logic that identifies the selected
    behaviour.
5.  **Test:** Generate safe test activity in a controlled lab and check
    that the rule fires. Also test benign activity to identify false
    positives.
6.  **Deploy:** Publish the reviewed rule and document how to
    investigate the alert.
7.  **Maintain:** Review alert quality and update the rule when
    telemetry or attacker techniques change.

If the rule never fires, do not immediately increase its severity or
deploy it anyway. First check whether the necessary logs exist, whether
the events contain the expected fields, and whether the detection logic
matches the available data.

## 11. Quick Revision Notes

-   Detection Engineering creates, tests, and maintains effective
    detections.
-   SOC analysts investigate alerts; detection engineers improve the
    logic that generates them. In some organisations, responsibilities
    overlap.
-   The lifecycle is: backlog management, threat research, data review,
    detection design, testing and validation, deployment, and
    maintenance.
-   Failed tests should lead to redesign and retesting.
-   Missing telemetry can cause a detection to fail silently.
-   Precision measures how many generated alerts are genuine threats.
-   Recall measures how many real attacks are detected.
-   False positives create noise; false negatives represent missed
    threats.
-   Attackers change their techniques, so detections need maintenance.
-   Detection Engineering is an ongoing process, not a one-time
    rule-writing task.

## 12. Personal Learning Log

On 12 October 2026, I studied the concepts in the TryHackMe Intro to
Detection Engineering room and reviewed how detection engineering fits
into a SOC.

I learned that detection engineering is not only about writing a rule. A
reliable detection needs threat research, the right telemetry, careful
design, testing, documentation, deployment, and maintenance.

I reviewed the difference between a SOC analyst and a detection
engineer, the detection engineering lifecycle, CREDO and ADS, the
detection gap, precision and recall, and common challenges such as
missing logs, parsing problems, alert fatigue, and outdated rules.

I also practised checking my understanding with knowledge-check
questions. I answered four review questions correctly: - The purpose of
detection engineering is to design, test, and maintain effective
detections. - A detection with only 20 genuine threats among 100 alerts
has low precision. - Missing Windows process-creation logs should be
identified during data review. - A detection that fails validation
should return to design for improvement.

These notes cover the room material reviewed so far. They are a learning
summary, not a claim that every interactive task or room question has
been completed.

------------------------------------------------------------------------
