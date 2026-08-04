# InfoSecLab – Pre-Security Fundamentals
## Module 1: Introduction to Cybersecurity

**Platform:** InfoSecLab  
**Module:** Pre-Security Fundamentals  
**Lesson:** Introduction to Cybersecurity  
**Date Completed:** 04 August 2026

---

# Overview

This introductory module provided a foundation in cybersecurity by explaining the core security principles, common attack methods, cybersecurity career paths, and the relationship between threats, vulnerabilities, and risks.

The module focused on understanding how organizations protect digital assets and the different roles involved in maintaining security.

---

# Learning Objectives

After completing this module, I learned:

- The purpose of cybersecurity
- The CIA Triad
- Common cyber attacks such as phishing
- The relationship between threats, vulnerabilities, and risks
- CVEs and Zero-Day vulnerabilities
- Blue Team vs Red Team
- Common cybersecurity career paths
- Industry certifications

---

# Lesson 1 – What is Cybersecurity?

Cybersecurity is the practice of protecting:

- Computers
- Networks
- Applications
- Data
- Digital infrastructure

from unauthorized access, attacks, damage, and disruption.

Every security control implemented inside an organization aims to protect one or more components of the **CIA Triad**.

---

# The CIA Triad

The CIA Triad forms the foundation of information security.

```
          Confidentiality
             /         \
            /           \
     Integrity ------- Availability
```

---

## 1. Confidentiality

### Objective

Ensure sensitive information is accessible only to authorized users.

### Examples

- Banking information
- Medical records
- Corporate documents

### Security Controls

- Encryption (AES)
- Multi-Factor Authentication (MFA)
- Access Control Lists (ACLs)
- User Permissions

---

## 2. Integrity

### Objective

Ensure information remains accurate and has not been modified without authorization.

### Example

A banking transaction of:

```
$50
```

must never become

```
$5000
```

during transmission.

### Security Controls

- SHA-256 Hashing
- Digital Signatures
- Checksums
- File Integrity Monitoring

---

## 3. Availability

### Objective

Ensure systems remain accessible whenever legitimate users require them.

### Examples

- Banking websites
- E-commerce platforms
- Cloud services

### Security Controls

- Backups
- Redundant Servers
- Disaster Recovery
- DDoS Protection

---

# Common Attack Vector – Phishing

One of the most common cyber attacks is **Phishing**.

### Goal

Trick users into revealing sensitive information.

Examples include:

- Passwords
- Credit Card Details
- Banking Credentials
- Corporate Login Credentials

---

### How Phishing Works

Attackers impersonate trusted organizations such as:

- Banks
- IT Departments
- HR Teams
- Microsoft
- Google

Victims are encouraged to:

- Click malicious links
- Download malware
- Enter login credentials

---

### Why Phishing Works

Rather than exploiting software vulnerabilities,

phishing exploits:

> Human psychology.

Common techniques include:

- Urgency
- Fear
- Curiosity
- Authority
- Rewards

---

# Security Operations Center (SOC)

Organizations monitor cyber threats through a **Security Operations Center (SOC).**

A SOC continuously monitors:

- Networks
- Endpoints
- Security Logs
- Alerts
- Incidents

---

## SOC Analyst

The SOC Analyst serves as the **first line of defense**.

Responsibilities include:

- Monitoring SIEM alerts
- Investigating suspicious activity
- Initial incident triage
- Escalating confirmed threats

---

## Incident Responder

The Incident Response team handles:

- Confirmed security breaches
- Malware outbreaks
- Containment
- Recovery
- Digital Forensics

Often described as the:

> "SWAT Team of Cybersecurity"

---

## Security Engineer

Security Engineers design and maintain security infrastructure.

Examples include:

- Firewalls
- SIEM Platforms
- Endpoint Detection & Response (EDR)
- IDS/IPS Systems

---

# Lesson 2 – Understanding Threats, Vulnerabilities and Risks

One of the most important concepts introduced was the security risk model.

---

# Risk Equation

```
Risk = Threat × Vulnerability × Impact
```

---

## Threat

A threat is anything capable of causing damage.

Examples:

- Hackers
- Malware
- Insider Threats
- Natural Disasters

Organizations cannot eliminate threats entirely.

---

## Vulnerability

A vulnerability is a weakness that attackers can exploit.

Examples:

- Weak Passwords
- Unpatched Software
- Misconfigurations
- Coding Bugs

Organizations reduce risk by fixing vulnerabilities.

Common mitigation methods include:

- Patching
- Hardening
- Secure Configuration

---

## Impact

Impact measures the consequences of a successful attack.

Examples:

- Financial Loss
- Data Breach
- Reputation Damage
- Service Downtime

---

# CVE (Common Vulnerabilities and Exposures)

Software vulnerabilities are tracked using standardized identifiers known as **CVEs**.

Example:

```
CVE-2021-44228
```

(Log4Shell)

Benefits of CVEs:

- Standard vulnerability tracking
- Easier patch management
- Industry-wide vulnerability reference

---

# Zero-Day Vulnerabilities

A **Zero-Day** vulnerability is a software flaw unknown to the vendor.

Because no patch exists,

attackers can exploit the vulnerability before defenders can fix it.

These vulnerabilities are highly valuable because:

- No official patch exists
- Detection is difficult
- High success rate

---

# Lesson 3 – Career Paths in Cybersecurity

Cybersecurity careers generally fall into two major categories.

---

# Red Team

Red Teams simulate real-world attacks.

Objective:

Find weaknesses before attackers do.

Common Roles:

- Penetration Tester
- Red Team Operator
- Exploit Developer

---

# Blue Team

Blue Teams defend organizational infrastructure.

According to the lesson,

approximately:

```
80%
```

of cybersecurity jobs belong to the Blue Team.

Common Roles:

- SOC Analyst
- Security Engineer
- Threat Hunter
- Incident Responder

---

## Threat Hunter

Threat Hunters proactively search for hidden attackers inside an organization's environment.

Rather than waiting for alerts,

they actively investigate:

- Logs
- Endpoints
- Network Activity

---

# Cybersecurity Certifications

The lesson introduced several industry certifications.

---

## CompTIA Security+

A vendor-neutral entry-level certification covering general cybersecurity concepts.

Suitable for beginners entering cybersecurity.

---

## Blue Team Level 1 (BTL1)

A practical certification focused on:

- SOC Operations
- Detection
- Incident Response
- Blue Team Skills

---

## CISSP

Certified Information Systems Security Professional

Often considered the industry **Gold Standard** for senior cybersecurity professionals.

Focus areas include:

- Security Management
- Governance
- Risk Management
- Leadership

---

# Knowledge Check

The module concluded with several review questions.

### Question 1

Which component of the CIA Triad ensures that data has not been tampered with?

**Answer**

```
Integrity
```

---

### Question 2

What is the primary goal of phishing?

**Answer**

```
To trick users into revealing sensitive information.
```

---

### Question 3

Who is considered the first line of defense?

**Answer**

```
SOC Analyst
```

---

# Key Concepts Learned

- Cybersecurity Fundamentals
- CIA Triad
- Confidentiality
- Integrity
- Availability
- Security Operations Center (SOC)
- SOC Analyst
- Security Engineer
- Incident Response
- Phishing
- Social Engineering
- Threat
- Vulnerability
- Risk
- Impact
- CVE
- Zero-Day Vulnerabilities
- Blue Team
- Red Team
- Threat Hunting
- Security+
- BTL1
- CISSP

---

# Skills Gained

Throughout this module, I developed an understanding of:

- Core cybersecurity principles
- Information security objectives
- Common attack techniques
- Security operations workflow
- Cybersecurity risk assessment
- Vulnerability management
- Security career paths
- Industry certifications
- Defensive security fundamentals

---

