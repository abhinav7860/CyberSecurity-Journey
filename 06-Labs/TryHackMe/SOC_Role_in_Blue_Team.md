# TryHackMe — SOC Role in Blue Team

**Platform:** TryHackMe  
**Room:** SOC Role in Blue Team  
**Date:** July 20, 2026

---

# Overview

This room explained how a Blue Team is organized inside a company, the different security roles, and how they work together during security incidents. I also learned the difference between an Internal SOC and an MSSP, along with the typical career path of a SOC analyst.

---

# Security Hierarchy

Large organizations usually follow this structure:

```
CEO
   │
CISO
   │
Security Managers
   │
Technical Teams
```

### CEO

- Focuses on business goals.
- Doesn't handle technical security work.

### CISO (Chief Information Security Officer)

- Leads the organization's cyber security.
- Makes important security decisions.
- Manages different security departments.

---

# Main Security Teams

## Red Team

Focuses on **offensive security**.

Responsibilities:

- Penetration Testing
- Ethical Hacking
- Finding vulnerabilities before attackers do

---

## Blue Team

Focuses on **defensive security**.

Responsibilities:

- Monitor alerts
- Detect attacks
- Investigate incidents
- Respond to threats
- Protect company assets

This is where a SOC Analyst works.

---

## GRC Team

GRC stands for **Governance, Risk, and Compliance**.

Responsibilities:

- Security policies
- Risk management
- Compliance (PCI DSS, ISO 27001, etc.)

---

# Blue Team Departments

## Security Operations Center (SOC)

The SOC is the company's first line of defense.

Main roles:

### SOC L1 Analyst

- Monitors alerts.
- Performs initial investigation.
- Escalates complex cases.

### SOC L2 Analyst

- Investigates advanced attacks.
- Handles escalated incidents.

### SOC Engineer

- Maintains SIEM, EDR, and security tools.
- Creates detection rules.
- Keeps monitoring systems running.

### SOC Manager

- Manages the SOC team.
- Coordinates investigations.
- Reports security status.

---

## Cyber Incident Response Team (CIRT)

CIRT responds to **major security incidents**.

Examples:

- Ransomware
- Large data breaches
- Critical attacks

Typical members include:

- Incident Responders
- Malware Analysts
- Threat Hunters
- Digital Forensics Analysts
- Threat Intelligence Analysts

Think of CIRT as the **firefighters** of cyber security.

---

# Specialized Blue Team Roles

Some organizations also have dedicated specialists.

### Threat Intelligence Analyst

Researches new attackers, malware, and threat groups.

### Digital Forensics Analyst

Investigates compromised systems and collects evidence.

### AppSec Engineer

Helps developers build secure applications.

### DevSecOps

Integrates security into the software development process.

### AI Researcher

Studies AI-related threats and defenses.

---

# SOC Career Path

A common career progression is:

```
SOC L1 Analyst
        │
SOC L2 Analyst
        │
SOC Engineer / CIRT / Threat Hunter
        │
SOC Manager
        │
CISO
```

Starting as an L1 analyst helps build practical experience before moving into specialized roles.

---

# Internal SOC vs MSSP

## Internal SOC

- Protects only one organization.
- Fewer security tools.
- Better understanding of the company's environment.
- Usually less pressure.

## MSSP (Managed Security Services Provider)

Provides security services for multiple companies.

Characteristics:

- Faster work environment.
- Handles many customer environments.
- Uses different security tools.
- Great place to gain experience quickly.

---

# Final Challenge

I matched each incident with the correct security role.

| Scenario | Correct Role |
|----------|--------------|
| SIEM alert needs initial triage | SOC L1 Analyst |
| Phishing malware requires deeper investigation | SOC L2 Analyst |
| Ransomware incident | CERT Lead |
| PCI DSS audit | GRC Auditor |
| Check website for vulnerabilities | Penetration Tester |
| SIEM storage issue | SOC Engineer |
| Analyze FIN7 threat group tactics | Threat Researcher |

Successfully completed the challenge and obtained the flag:

```
THM{trysecureme_is_secured!}
```

---
