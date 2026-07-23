# CompTIA Security+ (SY0-701)

## Domain 1.2 - The CIA Triad & Non-Repudiation

> 📅 Date: 23 July 2026
> 🎥 Source: Professor Messer - Security+ SY0-701

---

# What is the CIA Triad?

The **CIA Triad** is the foundation of Information Security.

It consists of three important security principles:

- Confidentiality
- Integrity
- Availability

Almost every security solution is designed to protect one or more of these three principles.

---

# 1. Confidentiality

Confidentiality means only authorized people should be able to access the information.

The goal is to prevent unauthorized users from viewing sensitive data.

### Examples

- Passwords
- Multi-Factor Authentication (MFA)
- Encryption
- Access Control Lists (ACLs)

### Real-world Example

Only employees in the HR department should be able to access employee salary details.

If another employee tries to open the file, access should be denied.

### Easy to Remember

> **Confidentiality = Keep data secret.**

---

# 2. Integrity

Integrity means data should remain accurate and unchanged.

If someone modifies the data, the change should be detected.

### Used Technologies

- Hashing
- Digital Signatures
- Certificates

### Examples

A downloaded software file should be exactly the same as the original.

If even one bit changes, the hash value changes completely.

### Easy to Remember

> **Integrity = Data should stay accurate.**

---

# 3. Availability

Availability means authorized users should be able to access data whenever they need it.

A secure system is useless if nobody can access it.

### Availability is improved by

- Redundancy
- Backup systems
- Fault Tolerance
- Regular Patching

### Examples

- RAID storage
- Backup servers
- UPS
- Load balancing

### Easy to Remember

> **Availability = Data should always be accessible.**

---

# Non-Repudiation

Non-repudiation means a person cannot deny performing an action.

If someone sends a message or signs a document, they cannot later claim,

> "I never sent it."

Non-repudiation provides proof that the action actually happened.

It mainly relies on:

- Digital Signatures
- Certificates
- Public Key Cryptography

---

# Proof of Integrity

Proof of Integrity confirms that the data has **not been modified**.

If the data changes, the hash value changes as well.

### Uses

- Hashing algorithms
- Digital Signatures

Example:

Download a Linux ISO.

Compare its SHA-256 hash with the value on the official website.

If both hashes match, the file has not been modified.

---

# Proof of Origin

Proof of Origin confirms **who actually sent the data.**

It proves the sender's identity.

This is achieved using **Digital Signatures**.

The sender signs the data using their **private key**, and the receiver verifies it using the sender's **public key**.

Example:

When your bank sends a digitally signed document, you can verify that it actually came from the bank.

---

# Quick Comparison

| Security Principle | Purpose |
|-------------------|---------|
| Confidentiality | Prevent unauthorized access |
| Integrity | Ensure data is not modified |
| Availability | Keep systems accessible |

---

# Non-Repudiation Summary

| Feature | Meaning |
|----------|---------|
| Proof of Integrity | Confirms the data wasn't changed |
| Proof of Origin | Confirms who sent the data |

---

# Quick Revision

### CIA Triad

- Confidentiality → Keep data secret
- Integrity → Keep data accurate
- Availability → Keep systems running

### Non-Repudiation

- Cannot deny sending data
- Uses Digital Signatures
- Uses Certificates
- Uses Public Key Cryptography

---

# Things I Need to Remember

- CIA Triad is one of the most important Security+ concepts.
- Encryption protects Confidentiality.
- Hashing verifies Integrity.
- Redundancy improves Availability.
- Non-repudiation means the sender cannot deny sending the message.
- Digital Signatures provide both Proof of Integrity and Proof of Origin.

---

