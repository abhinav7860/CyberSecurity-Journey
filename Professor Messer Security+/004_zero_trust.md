# CompTIA Security+ (SY0-701)

## Domain 1.2 - Gap Analysis & Zero Trust

> 📅 Date: 24 July 2026
> 🎥 Source: Professor Messer - Security+ (SY0-701)

---

# What is Gap Analysis?

Gap Analysis is the process of comparing an organization's **current security posture** with its **desired security posture**.

Simply put,

> **Current State ➜ Desired State**

The difference between these two is called the **Gap**.

The goal is to identify what is missing and what needs to be improved.

---

# Why is Gap Analysis Important?

Organizations use Gap Analysis to:

- Find weaknesses in their security
- Meet compliance requirements
- Improve existing security controls
- Plan future security improvements

Gap Analysis often involves:

- Research
- Security assessments
- Interviews
- Collecting technical information
- Reviewing existing policies

Large organizations may spend weeks or even months completing a Gap Analysis.

---

# Choosing a Security Framework

Before improving security, an organization needs a standard to compare against.

This standard is called a **Baseline**.

A baseline can be:

- Internal company policies
- Industry standards
- Government standards

Some common security frameworks are:

### NIST SP 800-171

Focuses on protecting **Controlled Unclassified Information (CUI)** in non-federal organizations.

---

### ISO/IEC 27001

An international standard for building and maintaining an **Information Security Management System (ISMS).**

---

# Easy to Remember

> Gap Analysis = "Where are we now?" vs "Where do we want to be?"

---

# What is Zero Trust?

Traditional networks assumed that users inside the network could be trusted.

Zero Trust changes this idea.

> **Never Trust, Always Verify.**

Every user, device, application, and request must be verified before access is granted.

No one is trusted automatically—even if they are already inside the organization's network.

---

# Principles of Zero Trust

- Verify every request.
- Assume every network is untrusted.
- Use the least privilege principle.
- Continuously monitor users and devices.
- Authenticate and authorize every access request.

---

# Zero Trust Uses

Some common security technologies used in Zero Trust include:

- Multi-Factor Authentication (MFA)
- Encryption
- Identity Verification
- Device Validation
- Network Segmentation
- Monitoring & Logging
- Access Policies

---

# Zero Trust Planes

Zero Trust separates the network into two main planes.

## 1. Control Plane

The Control Plane makes security decisions.

It decides:

- Who can access resources
- Whether access should be allowed
- Which policies should be applied

Think of it as the **brain** of Zero Trust.

---

## Components of the Control Plane

### Policy Decision Point (PDP)

The PDP is responsible for making access decisions.

It checks policies and decides whether access should be:

- Allowed
- Denied
- Revoked

---

### Policy Engine (PE)

The Policy Engine evaluates every access request.

It considers:

- User identity
- Device health
- Security policies
- Risk level
- Other security information

Then it decides whether access should be granted.

---

### Policy Administrator (PA)

The Policy Administrator communicates with the Policy Enforcement Point.

It:

- Creates access tokens
- Issues credentials
- Applies the decision made by the Policy Engine

Think of it as the component that carries out the decision.

---

## 2. Data Plane

The Data Plane handles the actual network traffic.

Its responsibilities include:

- Forwarding packets
- Encrypting traffic
- Network Address Translation (NAT)
- Trunking
- Processing frames and packets

Think of it as the part that actually moves the data.

---

# Policy Enforcement Point (PEP)

The Policy Enforcement Point sits between the user and the protected resource.

Its job is to enforce the decision received from the Control Plane.

If access is approved,

✔ Allow the request.

If access is denied,

❌ Block the request.

The PEP never makes its own decisions.

It simply follows the instructions from the Policy Decision Point.

---

# Security Zones

Zero Trust divides networks into different security zones.

Examples include:

- Trusted Zone
- Untrusted Zone
- Internal Network
- External Network
- Department-based Zones (HR, IT, Finance)

Instead of giving every user access to everything,

users are only allowed into the specific zones they need.

This limits the damage if an account is compromised.

---

# How Zero Trust Works

```
User
   │
Requests Access
   │
Policy Enforcement Point (PEP)
   │
Policy Decision Point (PDP)
      │
      ├── Policy Engine
      └── Policy Administrator
   │
Decision Returned
   │
Allow / Deny
   │
Protected Resource
```

---

# Real-Life Example

Imagine entering an airport.

Traditional Security:

Once you enter the airport, you can move almost anywhere.

Zero Trust:

You show your passport.

↓

Your boarding pass is checked.

↓

Your baggage is scanned.

↓

You go through security.

↓

Your identity is checked again before boarding.

Every step requires verification.

That's exactly how Zero Trust works.

---

# Quick Comparison

| Traditional Security | Zero Trust |
|----------------------|------------|
| Trust internal users | Trust nobody by default |
| Verify once | Verify every request |
| Broad access | Least privilege access |
| Large trusted network | Small protected zones |

---

# Quick Revision

| Term | Easy Meaning |
|------|--------------|
| Gap Analysis | Compare current security with the desired security |
| Baseline | Security standard to work towards |
| Zero Trust | Never Trust, Always Verify |
| Control Plane | Makes decisions |
| Data Plane | Transfers data |
| Policy Engine | Evaluates access requests |
| Policy Administrator | Applies the decision |
| Policy Enforcement Point | Allows or blocks access |

