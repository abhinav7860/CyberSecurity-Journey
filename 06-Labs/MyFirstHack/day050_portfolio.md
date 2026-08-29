# Day 50 Mini-Project – Navigate a Linux System

**Day 50 of 90 – How Networks Actually Work**  
**Date Added: 29 August 2026**

## Objective

Today I practised navigating around a Linux system using the commands and shortcuts I learned on Days 48 and 49.

The main commands I used were:

```bash
pwd
ls
ls -la
cd
cd ..
cd ~
cd -
```

The idea was to explore the filesystem, move between different locations, use shortcuts, and find my way back without getting stuck.

---

## Task 1 – Orient Yourself

### Starting location

```text
[Paste your pwd output here]
```

### Home directory

I used:

```bash
ls -la
```

Number of items shown:

```text
[Enter your number here]
```

### Top-level directories

I checked the root directory with:

```bash
ls /
```

Three directories I noticed:

1. `/home` – contains users' home directories.
2. `/etc` – contains system configuration files.
3. `/var` – contains variable data such as logs.

---

## Task 2 – Travel to Known Destinations

### `/etc`

I navigated using:

```bash
cd /etc
pwd
ls
```

Confirmation:

```text
[Paste your pwd output here]
```

Approximate number of items shown by `ls`:

```text
[Enter your number here]
```

### `/var/log`

I then moved to the Linux log directory:

```bash
cd /var/log
pwd
ls -la
```

Two log files/directories I noticed:

```text
1. [Name]
2. [Name]
```

Something I noticed in the detailed listing:

```text
[Write what you noticed about timestamps, permissions, owners, etc.]
```

---

## Task 3 – Using Navigation Shortcuts

From `/var/log`, I used:

```bash
cd ..
```

This took me to:

```text
/var
```

I then used `ls` to see what was there besides `log`.

What I found:

```text
[Write what you saw here]
```

After another:

```bash
cd ..
```

I reached:

```text
/
```

### Testing `cd ~`

I used:

```bash
cd ~
pwd
```

It returned me to my home directory.

### Testing `cd -`

I then used:

```bash
cd -
pwd
```

This took me back to the previous location.

The shortcut I think I will use most:

```text
[cd ~ / cd - / cd .. / Tab – choose one]
```

Reason:

```text
[Write your reason in your own words]
```

---

## Task 4 – Small File-System Hunt

### Temporary files

From my home directory, I navigated to:

```bash
cd /tmp
ls -la
```

The temporary-files directory is:

```text
/tmp
```

What I found there:

```text
[Write whether it was empty or what you noticed]
```

### Route I used

```text
[Example: I used the absolute path /tmp because I already knew the exact location.]
```

### Tab completion

I also practised Tab completion while navigating.

Directory I entered using Tab:

```text
[Directory name]
```

This helped because:

```text
[Write a short reason – faster / avoids typing mistakes / easier]
```

---

## Task 5 – Getting Lost and Finding My Way Back

I started from:

```bash
cd /usr/share
ls
```

Then I went a few levels deeper into one of the directories.

My deepest path was:

```text
[Paste your pwd output here]
```

After that, I used:

```bash
cd ~
pwd
```

My home directory was:

```text
[Paste your pwd output here]
```

So I was able to return home in one command.

---



