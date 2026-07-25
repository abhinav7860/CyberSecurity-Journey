# CompTIA Security+ (SY0-701)

## Domain 1.2 - Deception and Disruption

> 📅 Date: 25 July 2026
> 🎥 Source: Professor Messer - Security+ (SY0-701)

---

# Exam Objective

**CompTIA Security+ SY0-701**

- Domain 1.2: Summarize fundamental security concepts.
- Topic: Deception and Disruption

---

# What is Deception and Disruption?

Instead of blocking attackers immediately, organizations sometimes **trick them into interacting with fake systems**.

The goal is to:

- Detect attackers early
- Waste the attacker's time
- Study attacker behavior
- Collect information about attacks
- Protect the real systems

Think of it like setting a trap for an intruder.

---

# 1. Honeypot

A **Honeypot** is a fake computer or service designed to attract attackers.

It looks like a real system, but it contains no valuable data.

Everything an attacker does inside the honeypot is monitored.

### Purpose

- Attract attackers
- Monitor their activities
- Learn new attack techniques
- Keep attackers away from real systems

### Example

A fake Linux server is placed on the network.

An attacker tries to break into it, believing it's a real production server.

Meanwhile, the security team watches everything the attacker does.

### Easy to Remember

> Honeypot = Fake system used as bait.

---

# 2. Honeynet

A **Honeynet** is a collection of multiple honeypots connected together.

Instead of one fake device, it creates an entire fake network.

It may include:

- Servers
- Workstations
- Routers
- Switches
- Firewalls
- Databases

This gives attackers the impression that they are exploring a real company network.

### Benefits

- Collect more attack information
- Observe attacker movement
- Study advanced attacks
- Improve threat intelligence

### Easy to Remember

> Honeypot = One fake device.

> Honeynet = Many fake devices.

---

# 3. Honeyfiles

Honeyfiles are fake files placed on real systems.

These files look valuable but contain fake information.

Examples:

```
passwords.txt

salary.xlsx

confidential.docx

database_backup.sql
```

If someone opens or copies these files, an alert is generated.

### Purpose

- Detect unauthorized access
- Catch insider threats
- Identify attackers exploring file shares

### Easy to Remember

> Honeyfile = Fake file used as bait.

---

# 4. Honeytokens

Honeytokens are fake pieces of digital information that help track attackers.

Unlike honeypots, they are **not actual systems**.

They can be:

- Fake usernames
- Fake passwords
- Fake API keys
- Fake database records
- Fake email addresses
- Browser cookies
- Web tracking pixels

If someone tries to use a honeytoken, security teams immediately know it has been stolen.

### Example

A fake API key is uploaded to a public GitHub repository.

If someone attempts to use that API key, an alert is sent to the security team.

The API key doesn't provide real access—it only acts as bait.

### Easy to Remember

> Honeytoken = Fake information used to detect attackers.

---

# Comparison

| Technology | Purpose |
|------------|---------|
| Honeypot | Fake computer or service |
| Honeynet | Collection of multiple honeypots |
| Honeyfile | Fake file placed on a system |
| Honeytoken | Fake digital information |

---

# Real-Life Example

Imagine someone breaks into an office.

Instead of finding the real finance cabinet,

they find a cabinet labelled:

```
Employee Salaries
```

Inside, every document is fake.

The moment the cabinet is opened,

an alarm silently alerts the security team.

That's exactly how deception technologies work.

---

# Advantages

✔ Detect attackers early

✔ Collect threat intelligence

✔ Reduce risk to real systems

✔ Learn attacker techniques

✔ Improve incident response

---

# Limitations

- Skilled attackers may recognize fake systems.
- Honeypots must be monitored regularly.
- They don't replace traditional security controls.
- They should be isolated from production systems.

---

# Exam Tips 📝

✅ Honeypot = Fake **system**

✅ Honeynet = Fake **network**

✅ Honeyfile = Fake **file**

✅ Honeytoken = Fake **piece of information**

Remember:

**Pot → Network → File → Token**

Each one gets smaller.


---

# Quick Revision

| Term | Easy Meaning |
|------|--------------|
| Honeypot | Fake computer |
| Honeynet | Fake network |
| Honeyfile | Fake document |
| Honeytoken | Fake digital data |

---
