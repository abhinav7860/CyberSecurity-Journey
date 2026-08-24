# Hydra
**Topic:** Hydra  
**Date Added:** 24 August 2026  

---

## What is Hydra?

Hydra is a password-cracking and login-testing tool commonly used in cybersecurity.

It can automate login attempts against different network services using usernames and password lists.

I studied Hydra mainly to understand how automated password guessing works and why weak passwords can be a security problem.

---

## Why Hydra is Used

Hydra can be used during an authorised penetration test to check whether accounts are protected against weak or commonly guessed passwords.

It supports services such as:

- SSH
- FTP
- HTTP/HTTPS login forms
- SMB
- Telnet
- Other network services

The exact command depends on the service being tested.

---

## Basic Syntax

A basic Hydra command looks like:

```bash
hydra [options] <target> <service>
```

For example, in an authorised lab:

```bash
hydra -l username -P passwords.txt ssh://TARGET_IP
```

Where:

- `-l` = single username
- `-P` = password wordlist
- `ssh://` = service being tested
- `TARGET_IP` = target machine

---

## Basic Options I Learned

### `-l`

Specifies one username.

```bash
-l username
```

### `-L`

Uses a username list.

```bash
-L users.txt
```

### `-p`

Tests one password.

```bash
-p password
```

### `-P`

Uses a password wordlist.

```bash
-P passwords.txt
```

### `-t`

Controls the number of parallel tasks/connections.

```bash
-t 4
```

---

## Simple Example

For an authorised lab:

```bash
hydra -l testuser -P passwords.txt ssh://10.10.10.10
```

Hydra goes through the passwords in the wordlist and reports valid credentials if it finds them.

I should only use this against systems I own or have explicit permission to test.

---

## Wordlists

A wordlist is a file containing possible usernames or passwords.

Example:

```text
password
123456
admin
qwerty
letmein
Password123
```

Hydra uses these values during its login attempts.

This also shows why strong passwords are important.

---

## What I Learned

The main thing I understood is that Hydra can automate login attempts instead of manually trying passwords one by one.

This helped me understand why authentication protections are important:

- Strong passwords
- Account lockout or rate limiting
- Multi-factor authentication
- Monitoring failed login attempts
- Restricting unnecessary remote services

---

## Hydra vs Nmap

I also understood that Hydra and Nmap have different purposes:

```text
Nmap  -> Discover and identify services
Hydra -> Test authentication/password strength
```

For example, in an authorised lab, Nmap can help identify that SSH is running, and Hydra can then be used to test SSH authentication.

---

## Basic Workflow

```text
1. Identify the target/service
        ↓
2. Confirm permission to test it
        ↓
3. Identify a username or username list
        ↓
4. Choose a password wordlist
        ↓
5. Run Hydra against the authorised service
        ↓
6. Review the result
        ↓
7. Report weak credentials and recommend fixes
```

---

## Defensive Perspective

Hydra also helped me understand the defensive side of password attacks.

Useful protections include:

- Strong, unique passwords
- MFA
- Rate limiting / account lockout
- Disabling unnecessary services
- Restricting remote access
- Monitoring failed logins
- Using SSH keys instead of passwords where appropriate

---

