# OverTheWire Bandit: Level 21 → Level 22
**Date:** 24 July 2026

---

# Objective

A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

The goal of this level is to investigate a **cron job** that runs automatically on the system and discover how it reveals the password for **Bandit22**.

The challenge hints that the configuration can be found inside:

```text
/etc/cron.d/
```

---

# Understanding the Concept

This level introduces **Cron**, the Linux job scheduler.

Cron automatically executes commands or scripts at scheduled times.

Instead of exploiting a program directly, we inspect the scheduled task to understand **what it does** and **where it stores sensitive information**.

---

# What is Cron?

Cron is a background service that automatically executes scheduled tasks.

Examples of cron jobs:

- Daily backups
- Log cleanup
- Running scripts every minute
- System maintenance

Cron jobs are usually configured in:

```text
/etc/cron.d/
```

or through a user's personal crontab.

---

# Step 1 - List the Cron Jobs

View all available cron jobs.

```bash
ls /etc/cron.d/
```

Output

```text
behemoth4_cleanup
clean_tmp
cronjob_bandit22
cronjob_bandit23
cronjob_bandit24
...
```

Since we need the password for **Bandit22**, the relevant job is:

```text
cronjob_bandit22
```

---

# Step 2 - View the Cron Configuration

Read the cron configuration file.

```bash
cat /etc/cron.d/cronjob_bandit22
```

Output

```text
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
```

### What does this mean?

The script runs:

- Once every time the system boots (`@reboot`)
- Every minute (`* * * * *`)

It executes the script:

```text
/usr/bin/cronjob_bandit22.sh
```

The output is redirected to:

```text
/dev/null
```

meaning any output is discarded.

---

# Step 3 - Read the Script

Initially, I mistakenly tried to read the script from:

```bash
cat /etc/cron.d/cronjob_bandit22.sh
```

Output

```text
cat: /etc/cron.d/cronjob_bandit22.sh: No such file or directory
```

After checking the cron configuration carefully, I realized the script is actually stored in:

```text
/usr/bin/cronjob_bandit22.sh
```

Read it using:

```bash
cat /usr/bin/cronjob_bandit22.sh
```

Output

```bash
#!/bin/bash

chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

---

# Step 4 - Analyze the Script

The script performs two actions.

### Change File Permissions

```bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

Permission **644** means:

| Permission | Meaning |
|------------|---------|
| Owner | Read + Write |
| Group | Read |
| Others | Read |

This makes the file readable by everyone.

---

### Copy the Password

```bash
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

The script copies the Bandit22 password into a file located in:

```text
/tmp
```

Since the permissions are set to **644**, we can read it.

---

# Step 5 - Read the Password

At first I accidentally missed the leading `/` in the path.

Incorrect command:

```bash
cat tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

Output

```text
No such file or directory
```

Using the correct absolute path:

```bash
cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

Output

```text
RYVux2rHEm9tiXHmLFzuR7Vhx6AZQMEz
```

This is the password for **Bandit22**.

---

# Commands Used

```bash
ls /etc/cron.d/

cat /etc/cron.d/cronjob_bandit22

cat /usr/bin/cronjob_bandit22.sh

cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

---

# How the Cron Job Works

```
Cron Scheduler
      │
      ▼
Runs every minute
      │
      ▼
cronjob_bandit22.sh
      │
      ├───────────────► chmod 644
      │
      ▼
Copies password from

/etc/bandit_pass/bandit22

      │
      ▼

/tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv

      │
      ▼
Anyone can read the file
```

---

# Key Concepts Learned

## Cron

Cron is a Linux scheduler that automatically runs commands or scripts at specified intervals.

Common uses include:

- Backups
- Cleanup tasks
- Scheduled maintenance
- Automated scripts

---

## Cron Syntax

Example:

```text
* * * * *
```

The five fields represent:

```
Minute
Hour
Day of Month
Month
Day of Week
```

So:

```text
* * * * *
```

means:

```
Run every minute.
```

---

## @reboot

Special cron keyword:

```text
@reboot
```

Runs a command every time the system starts.

---

## /dev/null

```text
&> /dev/null
```

Redirects both standard output and error output to the null device.

This prevents the script from displaying any messages.

---

## chmod 644

```
Owner : Read + Write
Group : Read
Others: Read
```

This makes the password file readable by everyone on the system.

---

## Absolute vs Relative Paths

Incorrect:

```bash
cat tmp/file
```

Correct:

```bash
cat /tmp/file
```

The leading `/` refers to the filesystem root.

---

