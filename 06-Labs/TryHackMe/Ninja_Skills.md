# TryHackMe – Ninja Skills 
**Room:** Ninja Skills  
**Date:** 30 July 2026

---

# Overview

During this room, I practiced using several essential Linux commands that are frequently used in system administration, Capture The Flag (CTF) challenges, and penetration testing.

The tasks required finding files based on:

- Group ownership
- File contents
- SHA1 hashes
- Number of lines
- User IDs (UID)
- File permissions

Rather than opening every file individually, I used commands such as `find`, `grep`, `sha1sum`, `wc`, `ls`, and `awk` to automate the search process.

---

# Machine Deployment

Normally, the room starts by clicking:

```text
Start Machine
```

or by connecting through SSH using:

```text
Username: new-user
Password: new-user
```

---

# Problem Encountered

While attempting this room, the virtual machine failed to deploy.

Error displayed:

```text
Oh no, an error occurred whilst starting your machine.

No available machines in your region right now.

Please try again later.
```

The issue persisted for more than two days.

Other TryHackMe rooms launched successfully, indicating that the problem was specific to the **Ninja Skills** room rather than my local setup. I solved the problem by logging in to my Tryhackme account in another browser and opened Ninja Skills to do this room.

---

# Files Provided

Every answer in the room corresponds to one of the following filenames.

```text
8V2L
bny0
c4ZX
D8B3
FHl1
oiMO
PFbD
rmfX
SRSq
uqyw
v2Vb
X1Uy
```

---

# Linux Commands Used

## 1. find

### Purpose

Searches for files and directories based on different criteria.

Syntax

```bash
find <directory> <condition>
```

Example

```bash
find /home -name notes.txt
```

Searches for a file named **notes.txt** inside `/home`.

---

## 2. grep

### Purpose

Searches inside files for specific text or patterns.

Example

```bash
grep "hello" file.txt
```

Returns every line containing the word **hello**.

---

## 3. sha1sum

### Purpose

Calculates the SHA1 hash of a file.

Example

```bash
sha1sum file.txt
```

Example output:

```text
9d54da7584015647ba052173b84d45e8007eba94 file.txt
```

Useful when searching for a file using its hash.

---

## 4. wc

### Purpose

Counts lines, words, and bytes.

Example

```bash
wc -l file.txt
```

Output:

```text
230 file.txt
```

The `-l` option counts only the number of lines.

---

## 5. ls

### Purpose

Displays file information.

Example

```bash
ls -l
```

Shows:

- Permissions
- Owner
- Group
- File size
- Date
- Filename

---

## 6. ls -ln

### Purpose

Displays numeric User IDs (UID) and Group IDs (GID).

Example

```bash
ls -ln
```

Output:

```text
-rw-r--r-- 1 502 1000 X1Uy
```

Here:

- **502** → User ID
- **1000** → Group ID

---

# Task 1

## Which files are owned by the group **best-group**?

### Command

```bash
find / -group best-group 2>/dev/null
```

### Explanation

`find /`

Searches from the root directory.

`-group best-group`

Finds files owned by the specified group.

`2>/dev/null`

Suppresses permission denied errors to keep the output clean.

### Answer

```text
D8B3
v2Vb
```

---

# Task 2

## Which file contains an IP address?

### Command

```bash
find / -exec grep -lE '([0-9]{1,3}\.){3}[0-9]{1,3}' {} \; 2>/dev/null
```

### Explanation

`-exec`

Runs a command on every file found.

`grep -l`

Prints only the filename.

`-E`

Enables Extended Regular Expressions.

Regular Expression:

```text
([0-9]{1,3}\.){3}[0-9]{1,3}
```

Matches IPv4 addresses such as:

```text
192.168.1.1
10.0.0.5
172.16.100.20
```

### Answer

```text
oiMO
```

---

# Task 3

## Which file has the given SHA1 hash?

Hash:

```text
9d54da7584015647ba052173b84d45e8007eba94
```

### Command

```bash
find / -type f -exec sha1sum {} \; 2>/dev/null | grep 9d54da7584015647ba052173b84d45e8007eba94
```

### Explanation

`-type f`

Searches only files.

`sha1sum`

Calculates the SHA1 hash.

`grep`

Filters the matching hash.

### Answer

```text
c4ZX
```

---

# Task 4

## Which file contains exactly **230 lines**?

### Command

```bash
find / -type f -exec wc -l {} \; 2>/dev/null | grep "^230 "
```

### Explanation

`wc -l`

Counts the number of lines.

`grep "^230 "`

Shows only files containing exactly **230** lines.

### Answer

```text
bny0
```

---

# Task 5

## Which file is owned by UID **502**?

### Command

```bash
find / -type f -exec ls -ln {} \; 2>/dev/null | awk '$3==502'
```

### Explanation

`ls -ln`

Displays numeric owner IDs.

`awk '$3==502'`

Filters entries where the third column (UID) equals **502**.

### Answer

```text
X1Uy
```

---

# Task 6

## Which file is executable by everyone?

### Command

```bash
find / -type f -perm -111 2>/dev/null
```

### Alternative Method

```bash
ls -l
```

Look for permissions similar to:

```text
-rwxr-xr-x
```

### Explanation

Permission breakdown:

```text
Owner  -> rwx
Group  -> r-x
Others -> r-x
```

Each category has execute (`x`) permission.

### Answer

```text
8V2L
```

---

# Final Answers

| Question | Answer |
|----------|--------|
| Files owned by **best-group** | **D8B3**, **v2Vb** |
| File containing an IP address | **oiMO** |
| File matching the given SHA1 hash | **c4ZX** |
| File containing exactly **230 lines** | **bny0** |
| File owned by UID **502** | **X1Uy** |
| Executable by everyone | **8V2L** |

---

# Workflow

```text
Start Machine
      │
      ▼
Understand the Requirement
      │
      ▼
Choose the Appropriate Linux Command
      │
      ▼
Search the Entire Filesystem
      │
      ▼
Filter the Results
      │
      ▼
Identify the Correct File
      │
      ▼
Submit the Answer
```

---

# Key Linux Concepts Learned

- Searching files with `find`
- Suppressing errors using `2>/dev/null`
- Searching file contents using `grep`
- Using regular expressions to identify IPv4 addresses
- Calculating file hashes using `sha1sum`
- Counting lines with `wc -l`
- Viewing numeric UIDs and GIDs with `ls -ln`
- Filtering command output using `awk`
- Understanding Linux file permissions

---
