# TryHackMe - Linux Threat Detection 1

**Date:** 16 September 2026\
**Author:** Abhinav

## Overview

In this room I learned how to detect Linux **Initial Access** techniques
using logs and process trees.

Main topics:

-   SSH brute force
-   Exposed/public services
-   Web application exploitation
-   Auditd
-   Process tree analysis
-   Supply Chain Compromise

The main idea I want to remember is:

``` text
Suspicious activity
      ↓
Find the log
      ↓
Find the process/PID
      ↓
Trace the PPID
      ↓
Build the process tree
      ↓
Understand how the attack started
```

------------------------------------------------------------------------

# Task 2 - Initial Access via SSH

SSH is a common remote access service on Linux. If it is exposed and
uses weak passwords, attackers can perform brute-force attacks.

I started the investigation with:

``` bash
cat /var/log/auth.log | grep "sshd"
```

### First SSH login of the ubuntu user

**Answer:** `2024-10-22`

I filtered successful SSH logins:

``` bash
cat /var/log/auth.log | grep "sshd" | grep "Accepted"
```

Then I looked for the first `Accepted` entry for the `ubuntu` user.

------------------------------------------------------------------------

# Task 3 - Detecting SSH Attacks

A brute-force attack usually creates many `Failed` login events. I
looked at both failed and successful attempts:

``` bash
cat /var/log/auth.log | grep "sshd" | grep -E "Accepted|Failed"
```

### When did the SSH brute force start?

**Answer:** `2025-08-21`

I looked for the earliest date where the repeated failed SSH attempts
started.

### Which four users were targeted?

**Answer:**

``` text
root, roy, sol, user
```

I used the same command and checked the usernames appearing in the
failed attempts:

``` bash
cat /var/log/auth.log | grep "sshd" | grep -E "Accepted|Failed"
```

The four targeted usernames were then written in alphabetical order.

### Which IP breached the root user?

**Answer:** `91.224.92.79`

I searched the same SSH results for the successful `root` login and
checked the source IP from the `Accepted` entry.

### Simple SSH attack pattern

``` text
Many Failed logins
       ↓
Several usernames targeted
       ↓
Successful login
       ↓
Possible compromise
```

------------------------------------------------------------------------

# Task 4 - Initial Access via Services

Linux servers commonly expose services such as web servers, databases,
VPNs and applications. A vulnerable public service can become the
attacker's entry point.

The room used a vulnerable web application called **TryPingMe**. Its
input was passed to a system command without proper filtering, allowing
command injection.

For example:

``` text
/ping?host=;whoami
/ping?host=;ls
```

The web logs therefore became useful evidence.

### Python file the attacker attempted to open

**Answer:**

``` text
/opt/trypingme/main.py
```

I searched the Nginx access log for Python files:

``` bash
cat /var/log/nginx/access.log | grep ".py"
```

### Flag inside the Python file

**Answer:**

``` text
THM{i_am_vulnerable!}
```

After finding the path, I opened the file:

``` bash
cat /opt/trypingme/main.py
```

The flag was inside the application source.

### What I learned

A web log can reveal command injection when normal-looking parameters
suddenly contain Linux commands.

``` text
Web request
    ↓
Suspicious parameter
    ↓
Linux command
    ↓
Command execution
    ↓
Possible service breach
```

------------------------------------------------------------------------

# Task 5 - Detecting Service Breach

Sometimes application logs are not enough. A useful SOC technique is
**process tree analysis**.

A process tree shows which process started another process:

``` text
Python Web App
      ↓
/bin/sh
      ↓
whoami
```

If I find a suspicious command, I can trace its parent processes
backwards.

## PPID of the suspicious `whoami`

**Answer:** `1018`

I searched Auditd for the command:

``` bash
ausearch -i -x whoami
```

Here:

-   `-i` makes the output easier to read.
-   `-x whoami` searches for execution of `whoami`.

In the output I checked the `ppid` field:

``` text
ppid=1018
```

PPID means **Parent Process ID**, so `1018` is the process that started
`whoami`.

## PID of the TryPingMe application

**Answer:** `577`

I moved up the process tree by investigating the parent PID:

``` bash
ausearch -i --pid 1018
```

The output showed the parent process, leading me to PID `577`, which
belonged to the TryPingMe application.

## Program used to open the reverse shell

**Answer:** `python`

I then looked at the child processes of PID `577`:

``` bash
sudo ausearch -i --ppid 577 | grep "proctitle"
```

I checked the `proctitle` values to see what commands the application
launched. This showed that **python** was used to open the reverse
shell.

------------------------------------------------------------------------

# Task 6 - Advanced Initial Access

Linux can also be compromised through:

-   Malicious scripts
-   Malicious packages
-   Compromised dependencies
-   Supply chain attacks

## Supply Chain Compromise

A supply chain compromise happens when a trusted software component,
dependency, or supplier is compromised and becomes a path for malicious
activity.

### If a trusted app suddenly runs malicious commands

**Answer:**

``` text
Supply Chain Compromise
```

This is the answer used by the room for the scenario.

### Detection method for different Initial Access techniques

**Answer:**

``` text
Process Tree Analysis
```

The reason this is useful is that I can start with a suspicious command
and trace backwards:

``` text
Suspicious command
       ↓
PID
       ↓
PPID
       ↓
Parent process
       ↓
Application/user
       ↓
How the activity started
```

This can help investigate SSH compromises, web-service breaches and
activity originating from trusted applications.

------------------------------------------------------------------------

# Commands I Used

## SSH

``` bash
cat /var/log/auth.log | grep "sshd"
cat /var/log/auth.log | grep "sshd" | grep -E "Accepted|Failed"
```

## Web logs

``` bash
cat /var/log/nginx/access.log | grep ".py"
```

## Application source

``` bash
cat /opt/trypingme/main.py
```

## Auditd / Process Tree

``` bash
ausearch -i -x whoami
ausearch -i --pid 1018
sudo ausearch -i --ppid 577 | grep "proctitle"
```

------------------------------------------------------------------------

# Important Terms

### PID

**Process ID** --- the number identifying a process.

### PPID

**Parent Process ID** --- the PID of the process that started another
process.

### Process Tree

Shows the parent/child relationship between processes.

### Initial Access

The technique an attacker uses to enter a system.

------------------------------------------------------------------------

# Final Answers

  Task   Question                      Answer
  ------ ----------------------------- ---------------------------
  2      First SSH login of `ubuntu`   `2024-10-22`
  3      SSH brute force started       `2025-08-21`
  3      Four targeted users           `root, roy, sol, user`
  3      IP that breached `root`       `91.224.92.79`
  4      Python file                   `/opt/trypingme/main.py`
  4      Flag                          `THM{i_am_vulnerable!}`
  5      PPID of `whoami`              `1018`
  5      TryPingMe PID                 `577`
  5      Reverse shell program         `python`
  6      Initial Access technique      `Supply Chain Compromise`
  6      Detection method              `Process Tree Analysis`

------------------------------------------------------------------------

# My Takeaway

The biggest thing I learned is that I should not stop after finding a
suspicious command.

For example:

``` text
whoami
  ↓
Find PID/PPID
  ↓
Find parent
  ↓
Trace the process tree
  ↓
Find the application/user
  ↓
Understand the Initial Access
```

This makes process-tree analysis a very useful SOC investigation
technique.

## Sanitization

For public documentation, unnecessary internal IPs, hostnames,
credentials, tokens and sensitive infrastructure details should be
masked. The commands, concepts and lab answers are kept for revision.
