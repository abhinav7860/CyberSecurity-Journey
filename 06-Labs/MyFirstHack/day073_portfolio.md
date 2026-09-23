============================================================
KILL CHAIN BREACH ANALYSIS
==========================

Analyst:     Abhinav Sabu
Date:        23 September 2026
Subject:     Mid-Sized Company Customer Database Breach
Source:      Lesson scenario – myfirsthack.com, Day 73

---

1. BREACH SUMMARY

---

A mid-sized company was targeted through a phishing email sent
to finance employees. The attacker used a malicious attachment
to exploit outdated software, establish persistence, and
maintain command and control access to the environment.

The attacker's goal was to steal the company's customer
database. The attacker successfully accessed and exfiltrated
the customer data from the organization's network.

---

2. KILL CHAIN MAPPING

---

RECONNAISSANCE:
The attacker researched the company, including its website,
employees, and email format. This information helped them
identify suitable targets and prepare a convincing phishing
campaign.

WEAPONIZATION:
The attacker prepared a phishing email containing a malicious
attachment. The attachment was designed to exploit outdated
software on the victim's system when opened.

DELIVERY:
The attacker sent the phishing email and malicious attachment
to finance employees.

EXPLOITATION:
When the victim opened the malicious attachment, it exploited
a vulnerability in outdated software. This allowed malicious
code to execute and gave the attacker an initial foothold.

INSTALLATION:
The attacker installed a backdoor and created a hidden
scheduled task to establish persistence and maintain access
to the compromised system.

COMMAND AND CONTROL:
The compromised machine established an outbound connection
to the attacker's server. This provided a communication
channel that allowed the attacker to operate remotely.
The communication can be described as beaconing.

ACTIONS ON OBJECTIVES:
The attacker explored the environment, reached the customer
database, and copied the database outside the organization's
network. The attacker's objective of stealing customer data
was successfully achieved.

---

3. TECHNIQUES USED (ATT&CK thinking)

---

Stage: Delivery
-> Technique: Spearphishing Attachment
Tactic: Initial Access

Stage: Exploitation
-> Technique: Exploitation of Vulnerability
Tactic: Initial Access

Stage: Installation
-> Technique: Scheduled Task/Job
Tactic: Persistence

Stage: Command and Control
-> Technique: Beaconing / C2 Communication
Tactic: Command and Control

Stage: Actions on Objectives
-> Technique: Data Exfiltration
Tactic: Exfiltration

---

4. WHERE THE CHAIN COULD HAVE BROKEN

---

Stage: Delivery
-> Defence: Email security filtering and employee
security awareness could have detected, blocked,
or reported the phishing email before the attachment
was opened.

Stage: Exploitation
-> Defence: Regular patch management could have removed
the vulnerability in the outdated software, causing
the exploit to fail even if the attachment was opened.

Stage: Installation
-> Defence: Monitoring for unexpected scheduled tasks
and other persistence mechanisms could have detected
the attacker's backdoor and persistence activity.

Stage: Command and Control
-> Defence: Network monitoring and beaconing detection
could have identified the unusual outbound connection
to the attacker's infrastructure and allowed it to
be investigated or blocked.

Stage: Actions on Objectives
-> Defence: Data-loss prevention and monitoring of
unusual outbound data transfers could have detected
or blocked the customer database being transferred
outside the network.

MOST EFFECTIVE DEFENCE:

Patch management would have been the most effective single
defence for this specific scenario.

The attack relied on outdated software being vulnerable to
exploitation. If the software had been patched, the attacker
could still have researched the company and delivered the
phishing email, but the exploitation stage would have failed.

The attack chain would therefore have been broken at:

Reconnaissance -> Weaponization -> Delivery
-> X EXPLOITATION

---

5. LESSONS THAT GENERALISE

---

This breach demonstrates that successful attacks are often
the result of multiple defensive gaps rather than a single
failure.

Organisations should maintain effective patch management to
reduce exploitable vulnerabilities and use email security
controls to detect malicious phishing messages and
attachments.

Security teams should also monitor endpoints for persistence
mechanisms such as unexpected scheduled tasks and monitor
network traffic for suspicious outbound connections and
command-and-control activity.

Finally, organisations should monitor sensitive data movement
and use appropriate data-loss controls to detect or prevent
unauthorized data exfiltration.

The main defensive lesson is the importance of defence in
depth. If one security control fails, another control should
still provide an opportunity to detect or stop the attack.

---

6. KEY TAKEAWAY

---

The attacker had to successfully progress through multiple
stages to achieve the final objective, while the defenders
had multiple opportunities to break the chain.

The major missed opportunities in this scenario included
the phishing delivery, the unpatched software, the lack of
persistence monitoring, the undetected command-and-control
communication, and the absence of effective detection of
data exfiltration.

The key lesson for me is that a SOC analyst should not only
ask what happened, but also identify how the attacker
progressed, which techniques were used, and where a defensive
control could have broken the attack chain.

============================================================
END OF ANALYSIS
===============
