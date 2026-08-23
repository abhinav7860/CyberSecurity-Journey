# OWASP Top 10

## Web Application Security

**Topic:** OWASP Top 10  
**Version Studied:** OWASP Top 10 - 2021  
**Date Added:** 23 August 2026  
**Status:** Completed

---

## What is OWASP Top 10?

The OWASP Top 10 is a list of the most important web application security risks.

I studied it to get a basic understanding of the common vulnerabilities that can affect web applications and what kind of problems developers and security testers should look for.

The main thing I understood is that these are common security problems caused by things like bad access control, weak authentication, unsafe input handling, poor configuration, and insecure design.

---

# OWASP Top 10 - 2021

## 1. Broken Access Control

This happens when a user can access something they shouldn't be allowed to access.

For example, changing an ID in a URL and getting another user's information.

This connects directly with **IDOR**, which I saw while doing web security labs.

```text
Authentication = Who am I?
Authorization  = What am I allowed to access?
```

Being logged in doesn't mean I should have access to everything.

---

## 2. Cryptographic Failures

This is related to sensitive information not being properly protected.

Examples include:

- Weak encryption
- Sensitive data being sent without encryption
- Poor password storage
- Exposing sensitive information

The main point I took from this is that sensitive data needs proper protection when stored and transmitted.

---

## 3. Injection

Injection happens when untrusted input is interpreted as part of a command or query.

Examples include:

- SQL Injection
- Command Injection
- Other types of injection

A common problem is when an application directly includes user input in a query instead of handling it safely.

```text
Untrusted input + unsafe processing = possible injection
```

---

## 4. Insecure Design

This is more about problems in the way an application is designed rather than just a coding mistake.

If security isn't considered when designing a feature, the final application can have weaknesses even if the code works as intended.

**Main idea:** security should be considered during the design stage, not added only at the end.

---

## 5. Security Misconfiguration

This happens when systems or applications are configured insecurely.

Examples:

- Default passwords
- Unnecessary services enabled
- Debug features left enabled
- Incorrect permissions
- Poorly configured security settings

Small configuration mistakes can create big security problems.

---

## 6. Vulnerable and Outdated Components

Applications depend on libraries, frameworks, servers, and other software.

If these components have known vulnerabilities and aren't updated, the application can become vulnerable even if its own code is fine.

```text
Know what components you use.
Keep them updated.
Remove things you don't need.
```

---

## 7. Identification and Authentication Failures

This category covers weaknesses in login and authentication systems.

Examples include:

- Weak passwords
- Poor session handling
- Weak authentication mechanisms
- Poor account recovery
- Missing protections against attacks on login

Authentication is responsible for establishing who the user actually is.

---

## 8. Software and Data Integrity Failures

This involves trusting software, updates, plugins, dependencies, or data without properly verifying their integrity.

If something the application trusts can be modified, malicious code or data could potentially be introduced.

The main idea I took from this is:

> Don't automatically trust software or data just because it comes from somewhere you normally trust.

---

## 9. Security Logging and Monitoring Failures

If an application isn't logging important security events, detecting and investigating attacks becomes much harder.

Useful logging and monitoring can help identify:

- Failed login attempts
- Suspicious activity
- Access violations
- Unexpected behaviour

This also connects with what I learned about **SIEM, IDS and security monitoring** during the networking part.

---

## 10. Server-Side Request Forgery (SSRF)

SSRF happens when an application can be tricked into making requests to locations that the attacker shouldn't normally be able to reach.

The application becomes a kind of middleman for the attacker's request.

This can be especially dangerous when the server can access internal systems that aren't directly accessible from the internet.

---

# What I learned

The OWASP Top 10 helped me understand that web security isn't just about finding one particular exploit.

There are common patterns behind many vulnerabilities:

```text
Bad access control
Weak authentication
Unsafe input
Poor configuration
Outdated software
Missing security controls
Poor monitoring
```

I also noticed that some things I learned earlier connect directly to OWASP:

```text
IDOR              -> Broken Access Control
SQL Injection     -> Injection
Default settings  -> Security Misconfiguration
Old software      -> Vulnerable Components
Missing logs      -> Logging and Monitoring Failures
```

---




