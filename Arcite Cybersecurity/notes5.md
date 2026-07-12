# Arcite Cybersecurity Internship Notes
# Reconnaissance

**Date:** July 11, 2026

---

# What is Reconnaissance?

Reconnaissance is the process of collecting information about a target before attempting any attack or security assessment.

The goal is to understand the target's environment, technologies, services, domains, employees, and any publicly available information.

Some of the questions reconnaissance tries to answer are:

- What domains does the organization own?
- What IP addresses belong to them?
- Which services are exposed?
- What operating systems or technologies are being used?
- Are there any potential weaknesses?

Reconnaissance is often called **Footprinting** because we are building a footprint of the target.

---

# Why is Reconnaissance Important?

Reconnaissance is considered one of the most important phases in cybersecurity because it helps both attackers and defenders.

### From an Attacker's Perspective

Attackers perform reconnaissance to:

- Identify exposed systems
- Discover open services
- Find employee information
- Learn about the target's infrastructure
- Plan attacks more effectively

Without reconnaissance, an attacker would mostly be guessing.

---

### From a Defender's Perspective

Security teams perform reconnaissance on their own organization to:

- Find exposed assets
- Detect forgotten servers or domains
- Identify security weaknesses
- Reduce the attack surface
- Fix problems before attackers discover them

---

# Types of Reconnaissance

Reconnaissance is mainly divided into two categories:

```
Reconnaissance
      │
 ┌────┴────┐
 │         │
Passive   Active
```

---

# Passive Reconnaissance

Passive reconnaissance means gathering information **without directly interacting with the target**.

Since there is no communication with the target system, it is very difficult to detect.

It mainly relies on publicly available information.

### Examples

### Open Source Intelligence (OSINT)

Collecting publicly available information from sources like:

- Google
- LinkedIn
- GitHub
- Company websites
- News articles
- Public documents

Example:

Finding employee names and job roles from LinkedIn.

---

### WHOIS Lookup

WHOIS provides information about domain registration.

Example:

```bash
whois example.com
```

It can reveal:

- Domain registrar
- Registration date
- Expiration date
- Name servers
- Contact details (if public)

---

### DNS Lookup

DNS records provide information such as:

- IP addresses
- Mail servers
- Name servers
- TXT records
- Subdomains

Example:

```bash
dig example.com
```

or

```bash
nslookup example.com
```

---

### Search Engine Dorking

Using advanced Google search operators to find hidden or exposed resources.

Examples:

```
site:example.com

filetype:pdf

inurl:admin

intitle:"index of"
```

Google Dorks can reveal:

- Login pages
- Configuration files
- Backup files
- Public documents

---

# Advantages of Passive Recon

- Difficult to detect
- Safe to perform
- Uses publicly available information
- Great starting point before active testing

---

# Disadvantages of Passive Recon

- Limited information
- Cannot confirm live systems
- Cannot directly identify vulnerabilities

---

# Active Reconnaissance

Active reconnaissance involves directly communicating with the target.

Packets are sent to the target, making this method much more detailed but also easier for security systems to detect.

---

# Examples

### Port Scanning

Port scanning is used to identify open ports and running services.

Common tools:

- Nmap
- Masscan

Example:

```bash
nmap example.com
```

Information gathered:

- Open ports
- Running services
- Service versions

---

### Banner Grabbing

Banner grabbing helps identify the software running on a service.

Example:

```bash
nc example.com 80
```

or

```bash
telnet example.com 80
```

This may reveal:

- Apache version
- Nginx version
- FTP server
- SSH version

---

### Vulnerability Scanning

Vulnerability scanners check systems for known security issues.

Examples:

- Nikto
- Nuclei

These tools compare discovered services against known vulnerabilities.

---

# Passive vs Active Reconnaissance

| Passive Recon | Active Recon |
|---------------|--------------|
| No direct interaction | Direct interaction |
| Difficult to detect | Easier to detect |
| Uses public information | Sends packets to target |
| Low risk | Higher risk |
| Less detailed | More detailed |

---

# Tools Mentioned

### Passive Recon

- Google
- LinkedIn
- GitHub
- WHOIS
- DNS Lookup
- Google Dorks

### Active Recon

- Nmap
- Masscan
- Netcat (nc)
- Telnet
- Vulnerability Scanners

---
