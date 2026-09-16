# TryHackMe - Linux Threat Detection 2

**Date:** 16 September 2026\
**Author:** Abhinav

## Overview

This room continued from Linux Threat Detection 1 and focused on what
attackers do after getting access to a Linux system.

Main topics: - Discovery - Auditd investigation - Ingress Tool
Transfer - Cryptominer infections - Dota3 malware - Process analysis

My main mental model:

``` text
Initial Access → Discovery → Tool Transfer → Malware Execution → Attack Activity
```

------------------------------------------------------------------------

# Task 2 - Discovery Overview

After entering a Linux system, attackers usually perform Discovery to
understand the machine.

Common commands include:

``` bash
pwd
ls /
env
uname -a
hostname
id
whoami
ps aux
ip a
ip r
ss -tnlp
```

`whoami` is particularly useful to watch for because attackers commonly
use it to find the current user.

### Cloud detected by `systemd-detect-virt`

**Answer:** `amazon`

I ran:

``` bash
systemd-detect-virt
```

The output was:

``` text
amazon
```

### Antimalware binary

**Answer:**

``` text
/var/lib/ultrasec/malscan
```

I checked running processes and searched for security-related names:

``` bash
ps aux | grep -Ei "mal|scan|edr|security"
```

From the results I found the full path of the antimalware binary.

### What I learned

A Discovery command is not automatically malicious. I need to look at
the context.

``` text
Command → Parent process → Other commands → Context
```

------------------------------------------------------------------------

# Task 3 - Detecting Discovery

Attackers can perform more focused Discovery, such as searching for
credentials, checking CPU/RAM, or scanning the network.

Examples:

``` bash
history | grep pass
find / -name .env
find /home -name id_rsa
cat /proc/cpuinfo
lscpu
free -m
```

Auditd can record these command executions.

## Script that initiated `hostname`

**Answer:**

``` text
/home/itsupport/debug.sh
```

I investigated the Auditd event:

``` bash
sudo ausearch -p 3771
```

The process information showed that `hostname` was started by:

``` text
/home/itsupport/debug.sh
```

## Last Discovery command

**Answer:**

``` text
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu
```

I looked at the processes launched by the script:

``` bash
sudo ausearch -i --ppid 3771 | grep "proctitle"
```

The `proctitle` field showed the command that was executed. The last
Discovery command was the `ps` command above.

## Email of the script author

**Answer:**

``` text
greg@tryhackme.thm
```

I searched the script for author/email information:

``` bash
sudo grep -Ei "author|email|@" /home/itsupport/debug.sh
```

The author's email was shown in the script.

### Investigation idea

If a SIEM alerts on a Discovery command, I should trace where it came
from:

``` text
Discovery command
      ↓
PID / PPID
      ↓
Parent process
      ↓
Script/application
      ↓
Other activity
```

------------------------------------------------------------------------

# Task 4 - Motivation for Attacks

After Discovery, attackers may install malware or perform actions for
their actual objective.

"**Hack and Forget**" attacks commonly include:

-   Cryptomining
-   Botnet enrollment
-   Proxy use

## Ingress Tool Transfer

Attackers need to transfer tools onto the victim. Common commands are:

``` bash
wget
curl
scp
sftp
```

### Domain used to download the Elastic agent

**Answer:**

``` text
artifacts.elastic.co
```

I searched for `wget` activity:

``` bash
ausearch -i -x wget | grep "elastic"
```

The URL showed the domain `artifacts.elastic.co`.

### Full path to `helper.sh`

**Answer:**

``` text
/var/tmp/helper.sh
```

I investigated `curl`:

``` bash
ausearch -i -x curl
```

The command showed that `helper.sh` was downloaded to
`/var/tmp/helper.sh`.

### Which download was more likely malicious?

**Answer:** `curl`

The room's Auditd evidence showed the suspicious download associated
with `curl`.

### What I learned

For a file transfer investigation I can check:

``` text
Command → URL/domain → Destination → File → Execution
```

------------------------------------------------------------------------

# Task 5 - Dota3: First Actions

This task introduced the Dota3 cryptominer infection chain.

The general flow is:

``` text
SSH brute force
      ↓
SSH access
      ↓
Discovery
      ↓
Security/EDR checks
      ↓
Persistence
      ↓
Malware transfer
```

## IP that brute-forced SSH

**Answer:**

``` text
45.9.148.125
```

I searched the scenario Auditd log for failed SSH activity:

``` bash
ausearch -i -if /home/ubuntu/scenario/audit.log | grep -Ei "sshd|ssh" | grep -Ei "failed|failure|invalid"
```

I checked the source IP in the failed SSH events.

## Command used to list previous logged-in users

**Answer:**

``` text
last
```

I searched Auditd process titles:

``` bash
sudo ausearch -i -if /home/ubuntu/scenario/audit.log | grep -i "proctitle" | grep -i "last"
```

The `proctitle` showed the `last` command.

## EDR processes the attacker searched for

**Answer:**

``` text
ds_agent,falcon,sentinel
```

I searched for `egrep` activity:

``` bash
sudo ausearch -i -if /home/ubuntu/scenario/audit.log | grep -i "egrep"
```

The attacker searched for the three EDR/security process names. I
entered them alphabetically as required.

------------------------------------------------------------------------

# Task 6 - Dota3: Miner Setup

After gaining access, the attacker transferred the malware and prepared
the cryptominer.

The attack chain looked like:

``` text
Transfer archive
      ↓
Extract into hidden /tmp location
      ↓
Run malware
      ↓
Scan internal network
      ↓
Start cryptominer
```

`nohup` is important because it allows a process to continue running
after the terminal/session closes.

## Malicious archive transferred via SCP

**Answer:**

``` text
kernupd.tar.gz
```

I searched the Auditd scenario log for archive and SCP activity:

``` bash
sudo ausearch -i -if /home/ubuntu/scenario/audit.log | grep -Ei "dota3|tar\.gz|scp "
```

The transferred archive was `kernupd.tar.gz`.

## Full cryptominer launch command

**Answer:**

``` text
nohup /tmp/.apt/kernupd/kernupd
```

I searched for `nohup` executions:

``` bash
sudo ausearch -i -if /home/ubuntu/scenario/audit.log | grep -Ei "nohup" | grep proctitle
```

The `proctitle` showed the complete launch command.

## IP range scanned for exposed SSH

**Answer:**

``` text
10.10.12.1-10.10.12.10
```

I searched the `nohup` commands for IP information:

``` bash
sudo ausearch -i -if /home/ubuntu/scenario/audit.log | grep -i "nohup" | grep ip
```

The output showed the range scanned for exposed SSH services.

------------------------------------------------------------------------

# Commands I Used

## Discovery

``` bash
systemd-detect-virt
ps aux | grep -Ei "mal|scan|edr|security"
```

## Discovery investigation

``` bash
sudo ausearch -p 3771
sudo ausearch -i --ppid 3771 | grep "proctitle"
sudo grep -Ei "author|email|@" /home/itsupport/debug.sh
```

## Ingress Tool Transfer

``` bash
ausearch -i -x wget | grep "elastic"
ausearch -i -x curl
```

## Dota3 investigation

``` bash
ausearch -i -if /home/ubuntu/scenario/audit.log | grep -Ei "sshd|ssh" | grep -Ei "failed|failure|invalid"

sudo ausearch -i -if /home/ubuntu/scenario/audit.log | grep -i "proctitle" | grep -i "last"

sudo ausearch -i -if /home/ubuntu/scenario/audit.log | grep -i "egrep"
```

## Miner setup

``` bash
sudo ausearch -i -if /home/ubuntu/scenario/audit.log | grep -Ei "dota3|tar\.gz|scp "

sudo ausearch -i -if /home/ubuntu/scenario/audit.log | grep -Ei "nohup" | grep proctitle

sudo ausearch -i -if /home/ubuntu/scenario/audit.log | grep -i "nohup" | grep ip
```

------------------------------------------------------------------------

# Important Terms

### Discovery

Finding information about the compromised system, users, processes,
security tools and network.

### Ingress Tool Transfer

Bringing a tool or file onto the compromised system.

### Auditd

Linux auditing system that can record process and other system activity.

### PID

Process ID.

### PPID

Parent Process ID --- the process that started another process.

### `proctitle`

Auditd field showing the command/process title that was executed.

### `nohup`

Allows a process to continue running after the terminal/session closes.

------------------------------------------------------------------------

# Final Answers

  ----------------------------------------------------------------------------------------------
  Task                    Question                Answer
  ----------------------- ----------------------- ----------------------------------------------
  2                       Cloud detected          `amazon`

  2                       Antimalware binary      `/var/lib/ultrasec/malscan`

  3                       Script that initiated   `/home/itsupport/debug.sh`
                          `hostname`              

  3                       Last Discovery command  `ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu`

  3                       Script author's email   `greg@tryhackme.thm`

  4                       Elastic download domain `artifacts.elastic.co`

  4                       `helper.sh` path        `/var/tmp/helper.sh`

  4                       More likely malicious   `curl`
                          download                

  5                       SSH brute-force IP      `45.9.148.125`

  5                       Last-login command      `last`

  5                       EDR processes           `ds_agent,falcon,sentinel`

  6                       Malicious archive       `kernupd.tar.gz`

  6                       Cryptominer command     `nohup /tmp/.apt/kernupd/kernupd`

  6                       SSH scan range          `10.10.12.1-10.10.12.10`
  ----------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# My Takeaway

The main thing I learned is that attackers usually do not jump straight
to their final objective.

``` text
Get access
   ↓
Discover the system
   ↓
Check security controls
   ↓
Transfer tools
   ↓
Execute malware
   ↓
Achieve the objective
```

When I investigate Linux activity, I should connect the commands
together instead of looking at one event by itself.

## Sanitization

For public documentation, unnecessary credentials, tokens, hostnames and
sensitive infrastructure details should be masked. The commands and lab
answers are retained because they are useful for revision.
