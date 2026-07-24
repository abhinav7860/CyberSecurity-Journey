# OverTheWire Bandit: Level 22 → Level 23 
**Date:** 24 July 2026

---

# Objective

A program is running automatically at regular intervals from cron, the time-based job scheduler. Look in /etc/cron.d/ for the configuration and see what command is being executed.

The goal of this level is to inspect another **cron job** running on the system and determine how it stores the password for **Bandit23**.

Unlike the previous level, the password is **not stored in a fixed filename**. Instead, the script dynamically generates a filename using an **MD5 hash**.

---

# Understanding the Concept

This level builds upon the previous cron challenge and introduces:

- Reading shell scripts written by others
- Shell variables
- Command substitution
- MD5 hashing
- Using pipes to combine commands

Instead of guessing where the password is stored, we must understand how the script calculates the filename.

---

# Step 1 - List the Cron Jobs

View the available cron jobs.

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

Since we need the password for **Bandit23**, inspect:

```text
cronjob_bandit23
```

---

# Step 2 - View the Cron Configuration

```bash
cat /etc/cron.d/cronjob_bandit23
```

Output

```text
@reboot bandit23 /usr/bin/cronjob_bandit23.sh &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh &> /dev/null
```

This tells us that every minute the following script is executed:

```text
/usr/bin/cronjob_bandit23.sh
```

---

# Step 3 - Read the Script

```bash
cat /usr/bin/cronjob_bandit23.sh
```

Output

```bash
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

---

# Step 4 - Analyze the Script

Let's understand the script line by line.

---

## Line 1

```bash
myname=$(whoami)
```

`whoami` returns the current user.

Since the cron job runs as **bandit23**, the variable becomes:

```text
myname=bandit23
```

---

## Line 2

```bash
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)
```

This line generates the filename.

Breaking it down:

### Step 1

```bash
echo "I am user bandit23"
```

Produces:

```text
I am user bandit23
```

---

### Step 2

```bash
md5sum
```

Calculates the MD5 hash of that text.

---

### Step 3

```bash
cut -d ' ' -f 1
```

The output of `md5sum` looks like:

```text
8ca319486bfbbc3663ea0fbe81326349  -
```

The `cut` command extracts only the first field:

```text
8ca319486bfbbc3663ea0fbe81326349
```

This value is stored in the variable:

```text
mytarget
```

---

## Final Line

```bash
cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

After variable substitution, the command becomes:

```bash
cat /etc/bandit_pass/bandit23 > /tmp/8ca319486bfbbc3663ea0fbe81326349
```

The password is copied into a file inside `/tmp`.

---

# Step 5 - Generate the Filename

Since we know the value of `myname`, we can calculate the filename ourselves.

```bash
echo "I am user bandit23" | md5sum | cut -d ' ' -f 1
```

Output

```text
8ca319486bfbbc3663ea0fbe81326349
```

This is the filename created by the cron script.

---

# Step 6 - Read the Password

Now simply read the generated file.

```bash
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```

Output

```text
gKXDTAXnIz3OBxiPjRZ2uqutUlPZrBsw
```

This is the password for **Bandit23**.

---

# Commands Used

```bash
ls /etc/cron.d/

cat /etc/cron.d/cronjob_bandit23

cat /usr/bin/cronjob_bandit23.sh

echo "I am user bandit23" | md5sum | cut -d ' ' -f 1

cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```

---

# How the Script Works

```
Cron Scheduler
       │
       ▼
Runs cronjob_bandit23.sh
       │
       ▼
whoami
       │
       ▼
bandit23
       │
       ▼
"I am user bandit23"
       │
       ▼
md5sum
       │
       ▼
8ca319486bfbbc3663ea0fbe81326349
       │
       ▼
Copies

/etc/bandit_pass/bandit23

       │
       ▼

/tmp/8ca319486bfbbc3663ea0fbe81326349
       │
       ▼
Password Retrieved
```

---

# Key Concepts Learned

## Shell Variables

Variables store values that can be reused later.

Example

```bash
name="Bandit"
```

Access the variable using:

```bash
echo $name
```

---

## Command Substitution

The syntax:

```bash
$(command)
```

stores the output of a command inside a variable.

Example

```bash
current=$(whoami)
```

---

## MD5 Hashing

MD5 generates a fixed-length hash from any input.

Example

```bash
echo "hello" | md5sum
```

Output

```text
5d41402abc4b2a76b9719d911017c592
```

In this challenge, MD5 is **not used for security**, but to create a predictable filename.

---

## cut Command

The `cut` command extracts specific fields from text.

Example

```bash
echo "apple banana orange" | cut -d " " -f 2
```

Output

```text
banana
```

---

## Pipes (`|`)

The pipe operator sends the output of one command directly to another.

Example

```bash
echo "hello" | md5sum
```

The output of `echo` becomes the input of `md5sum`.

---

