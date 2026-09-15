# TryHackMe - Linux Logging for SOC

**Date:** 15 September 2026\
**Author:** Abhinav

## Overview

In this room I learned how Linux logs can be used during SOC
investigations. I worked with `/var/log/syslog`, `/var/log/auth.log`,
package logs, Bash history and Auditd.

The main workflow I learned was:

**Find the right log → filter it → read the event → build the
timeline.**

------------------------------------------------------------------------

# Task 2 - Working With Text Logs

Most Linux logs are stored in:

``` text
/var/log/
```

Useful commands:

``` bash
cat /var/log/syslog
cat /var/log/syslog | grep CRON
grep -R -E "auth|login|session" /var/log
```

### Time server domain

**Answer:** `ntp.ubuntu.com`

I searched for synchronization events:

``` bash
cat /var/log/syslog | grep "sync"
```

The output showed `ntp.ubuntu.com`.

### Kernel message from Yama

**Answer:** `becoming mindful.`

I searched the syslog for Yama:

``` bash
grep -i "yama" /var/log/syslog
```

------------------------------------------------------------------------

# Task 3 - Authentication Logs

The main authentication log on Ubuntu/Debian is:

``` text
/var/log/auth.log
```

It can contain SSH logins, sudo activity, sessions, user management and
password changes.

Useful searches:

``` bash
cat /var/log/auth.log | grep -E 'session opened|session closed'
cat /var/log/auth.log | grep "sshd" | grep -E 'Accepted|Failed'
cat /var/log/auth.log | grep -E '(passwd|useradd|usermod|userdel)\['
cat /var/log/auth.log | grep -E 'COMMAND='
```

### IP that failed SSH logins against multiple users

**Answer:** `10.14.94.82`

I filtered failed SSH attempts:

``` bash
cat /var/log/auth.log | grep "sshd" | grep -i "Failed"
```

I checked the results and found the same IP attempting multiple
usernames.

### User created and added to sudo

**Answer:** `xeres`

I searched for `usermod` events involving the sudo group:

``` bash
cat /var/log/auth.log | grep -E "usermod" | grep "sudo"
```

This showed that `xeres` was added to the `sudo` group.

------------------------------------------------------------------------

# Task 4 - Common Linux Logs

Some useful Linux logs are:

  Log                   Purpose
  --------------------- ----------------------------------------
  `/var/log/kern.log`   Kernel messages
  `/var/log/syslog`     General system events
  `/var/log/dpkg.log`   Package activity on Debian/Ubuntu
  `/var/log/dnf.log`    Package activity on RHEL-based systems
  `/var/log/yum.log`    Older RHEL/CentOS package activity

## Bash History

Bash stores previous commands in:

``` text
~/.bash_history
```

It can be viewed with:

``` bash
cat ~/.bash_history
history
```

Bash history has limitations because commands can sometimes be hidden by
using another shell, scripts, or other techniques.

### Version of unzip installed

**Answer:** `6.0-28ubuntu4.1`

I searched the package manager log:

``` bash
cat /var/log/dpkg.log | grep "unzip"
```

The installation entry showed the version.

### Flag in Bash history

**Answer:** `THM{note_to_remember}`

I checked the root user's history:

``` bash
sudo cat /root/.bash_history
```

The flag was present there.

------------------------------------------------------------------------

# Task 5 - Runtime Monitoring

Normal Linux logs do not reliably record every runtime event such as
process creation, file activity and network activity.

This is why additional monitoring is needed.

Linux programs interact with the kernel through **system calls**. For
example:

``` text
execve
```

is used to execute a program.

Tools such as Auditd, Sysmon for Linux, Falco, Osquery and EDRs can use
system-call information for runtime monitoring.

------------------------------------------------------------------------

# Task 6 - Using Auditd

Auditd provides auditing of runtime activity.

Important locations:

``` text
/etc/audit/rules.d/
 /var/log/audit/audit.log
```

`ausearch` makes Auditd logs easier to search:

``` bash
ausearch -i -k <key>
```

The `-i` option makes values easier to read and `-k` searches for a
specific audit key.

## Finding the first access to `secret.thm`

The room specified the key:

``` text
file_thmsecret
```

I searched:

``` bash
ausearch -i -k file_thmsecret
```

The first relevant event showed:

``` text
08/13/25 18:36:54
```

## Finding the original file downloaded with wget

Wget activity was logged with:

``` text
proc_wget
```

I searched the key and filtered for GitHub-related output:

``` bash
ausearch -i -k proc_wget | grep "git"
```

The downloaded filename was:

``` text
naabu_2.3.5_linux_amd64.zip
```

## Finding the scanned network range

There was no dedicated key for this event, so I searched all Auditd
events for `naabu`:

``` bash
ausearch -i | grep -E 'naabu'
```

The scanned network was:

``` text
192.168.50.0/24
```

------------------------------------------------------------------------

# Auditd Fields Worth Remembering

When investigating an Auditd event, useful fields include:

-   `pid` - process ID
-   `ppid` - parent process ID
-   `auid` - original authenticated user
-   `uid` - user who actually ran the action
-   `tty` - terminal/session
-   `exe` - executable path
-   `key` - rule label used for searching

These fields help connect commands, users and processes into a timeline.

------------------------------------------------------------------------

# Commands I Used

``` bash
# Syslog
grep "sync" /var/log/syslog
grep -i "yama" /var/log/syslog

# Authentication
grep "sshd" /var/log/auth.log | grep -i "Failed"
grep -E "usermod" /var/log/auth.log | grep "sudo"

# Package logs
grep "unzip" /var/log/dpkg.log

# Bash history
sudo cat /root/.bash_history

# Auditd
ausearch -i -k file_thmsecret
ausearch -i -k proc_wget
ausearch -i -k proc_wget | grep "git"
ausearch -i | grep -E 'naabu'
```

------------------------------------------------------------------------

# My Takeaway

This room helped me understand where to look when investigating a Linux
host as a SOC analyst.

The most important things I learned were:

-   `syslog` is useful for general system activity.
-   `auth.log` is important for authentication and privilege activity.
-   Package logs can reveal installed software.
-   Bash history can provide useful clues but is not a reliable security
    log by itself.
-   Auditd provides much better runtime visibility.
-   `ausearch` and `grep` are useful for filtering large log files.
-   Understanding system calls helps me understand how runtime
    monitoring works.

**Main workflow:**

``` text
Identify the event
      ↓
Find the correct log
      ↓
Filter the data
      ↓
Understand the event
      ↓
Build the timeline
```

## Sanitization

For public documentation, unnecessary internal infrastructure details,
credentials, tokens and sensitive host information should be masked. The
commands and investigation methods are kept for revision.
