# Security Principles
## infoseclab
**Date:** 08 August 2026

1. CIA Triad

The CIA Triad is a fundamental model used to guide information security policies and security controls.

        [ Confidentiality ]
              /     \
             /       \
            /         \
     [ Integrity ]---[ Availability ]

The three pillars are:

Confidentiality
Integrity
Availability
Confidentiality

Confidentiality ensures that sensitive information is accessible only to authorized users, systems, or processes.

Common controls
Encryption
Access Control Lists (ACLs)
Authentication
Example

If an attacker steals customer credit card information from a database, confidentiality has been violated.

Integrity

Integrity ensures that information has not been modified, altered, or deleted without authorization.

Common controls
Hashing
Digital signatures
File checksums
Example

If an attacker changes the destination account in a bank transfer, the integrity of the transaction has been compromised.

Availability

Availability ensures that systems, applications, and data remain accessible to authorized users when required.

Common controls
Redundant servers
Backups
Disaster recovery
Load balancing
DDoS protection
Example

A DDoS attack that prevents customers from accessing an online service primarily affects Availability.

2. Authentication

Authentication is the process of verifying that a user or system is who they claim to be.

There are three main authentication factors.

Factor 1 — Something You Know

Information that the user knows.

Examples:

Passwords
PINs
Security question answers
Weakness

These can potentially be:

Guessed
Cracked
Stolen
Captured through phishing
Factor 2 — Something You Have

Something physically possessed by the user.

Examples:

Smart cards
USB security keys
Hardware tokens
Authenticator applications
Factor 3 — Something You Are

A physical characteristic of the user.

Examples:

Fingerprint
Iris scan
Retina scan
Facial recognition
Voice recognition

3. Multi-Factor Authentication (MFA)

MFA requires two or more different authentication factors.

For example:

Password
   +
Fingerprint
   ↓
MFA

This uses:

Something you know → Password
Something you are → Fingerprint
Important

Two passwords do not count as MFA because both belong to the same authentication factor.

MFA requires different factors.

4. Authentication vs Authorization

These two concepts are closely related but have different purposes.

Authentication

Answers:

"Who are you?"

Examples:

Username and password
Fingerprint
Security key
Authorization

Answers:

"What are you allowed to do?"

Examples:

Read a file
Modify a database
Access an administrator console
Execute a program

The general sequence is:

Authentication
      ↓
Who are you?
      ↓
Authorization
      ↓
What are you allowed to access?

Authentication occurs first.

5. Access Control Models

Different environments use different approaches to authorization.

DAC — Discretionary Access Control

The owner of a resource determines who can access it.

This is commonly used in standard Windows and Linux file systems.

RBAC — Role-Based Access Control

Permissions are assigned according to a user's role.

Example:

Finance Employee
       ↓
Finance Group
       ↓
Finance Resources

Instead of configuring every user individually, permissions can be assigned to the role or group.

MAC — Mandatory Access Control

Access is controlled using security labels and clearances.

Example:

Confidential
Secret
Top Secret

The system enforces the access rules rather than allowing the resource owner to decide.

This model is commonly associated with highly controlled environments such as government and military systems.

ABAC — Attribute-Based Access Control

Access decisions are based on attributes.

These could include:

User identity
Location
Time
Device status
Other environmental conditions

This allows access decisions to be more dynamic.

6. Principle of Least Privilege

Least Privilege means giving a user or system only the minimum permissions required to perform its job.

For example:

Normal Employee
      ↓
Only required permissions

Instead of:

Normal Employee
      ↓
Administrator privileges
Why it matters

If an employee account is compromised, an attacker gets the permissions associated with that account.

If the account only has normal permissions, the potential damage is limited.

If the account has unnecessary administrator privileges, the attacker may gain much greater control.

7. AAA Security Framework

AAA stands for:

Authentication
Authorization
Accounting
1. Authentication

Verifies identity.

"Who are you?"

2. Authorization

Determines permissions.

"What are you allowed to do?"

3. Accounting

Records user activity and system actions.

"What did you do?"

8. Accounting

Accounting provides visibility into what users and systems do after authentication.

Security teams can maintain audit logs containing information such as:

User actions
System configuration changes
Access events
Connection information
Timestamps

These records create an audit trail.

9. Non-Repudiation

Non-repudiation means preventing a user from falsely denying that they performed a particular action.

For example:

User performs transaction
        ↓
Transaction is digitally signed
        ↓
Evidence of who performed it
Methods
Digital Signatures

Cryptographic signatures can provide proof of the origin of a message or transaction.

Tamper-Proof Logs

Logs can include:

Timestamps
Secure hashes
Recorded actions

This helps prevent users from denying actions that were properly recorded.

10. Accounting and Digital Forensics

Accounting logs are extremely valuable during incident investigations.

For example, if an employee account is compromised, investigators can examine audit trails to determine:

Which files were accessed
Which servers were contacted
What actions were performed
When the activity occurred

The general investigation process can look like:

Compromised Account
        ↓
Audit Logs
        ↓
User Activity
        ↓
Timeline
        ↓
Forensic Investigation

Without sufficient logging, reconstructing an incident becomes much more difficult.

11. Hashing vs Encryption

Hashing and encryption are both cryptographic techniques, but they have different purposes.

Feature	Encryption	Hashing
Reversible	Yes, with the correct key	No
Main purpose	Confidentiality	Integrity
Uses keys	Yes	Typically no
Output	Variable length	Fixed length
Examples	AES, RSA, Blowfish	SHA-256, bcrypt, MD5, SHA-1

12. Encryption

Encryption transforms readable information into protected ciphertext.

Plaintext
    ↓
Encryption + Key
    ↓
Ciphertext

With the correct key, the ciphertext can be decrypted.

Ciphertext
    ↓
Decryption + Key
    ↓
Plaintext
Main goal

Confidentiality

Encryption prevents unauthorized people from easily reading protected information.

Examples from the lesson:

AES
RSA
Blowfish

13. Hashing

Hashing converts input data into a fixed-length value called a hash or message digest.

Input
  ↓
Hash Function
  ↓
Hash

For example:

File
 ↓
SHA-256
 ↓
Fixed-length hash

Hashing is designed to be a one-way operation.

The lesson emphasizes that even a small change to the original input can produce a significantly different hash. This is known as the avalanche effect.

14. Uses of Hashing

Password Storage

Instead of storing passwords directly, systems can store password-derived hashes.

During login:

Entered Password
       ↓
Hash
       ↓
Compare with stored value
File Verification

Hashes can be used to verify whether a downloaded file has changed.

For example:

Original File
     ↓
SHA-256
     ↓
Expected Hash

The downloaded file can then be hashed and compared against the expected value.

15. Hashing Algorithms

Not every hashing algorithm is considered secure today.

Older / Vulnerable
MD5
SHA-1

The lesson notes that these algorithms have known collision weaknesses.

Modern Example

SHA-256

SHA-256 is presented in the lesson as a modern cryptographically secure hashing algorithm and is widely used for integrity verification and other security applications.

16. Security Principles Summary

The major concepts from this section can be remembered like this:

CIA
│
├── Confidentiality → Keep information secret
├── Integrity       → Keep information accurate
└── Availability    → Keep systems accessible

Authentication and authorization:

Authentication → Who are you?
Authorization  → What can you access?
Accounting     → What did you do?

Cryptography:

Encryption → Confidentiality
Hashing    → Integrity

Access control:

DAC  → Owner decides
RBAC → Role decides
MAC  → System/security labels decide
ABAC → Attributes decide

Authentication factors:

Something You Know
Something You Have
Something You Are