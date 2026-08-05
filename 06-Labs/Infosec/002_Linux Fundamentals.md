# InfoSecLab - Linux Fundamentals
**Date:** 05 August 2026

## Module
Linux Fundamentals

---

# Objective

Learn the fundamentals of the Linux operating system, including:

- Linux file system hierarchy
- Basic file and directory operations
- File permissions
- File searching
- Process management
- Package management
- Linux commands commonly used by system administrators and security professionals

---

# 1. Linux File System Hierarchy

Unlike Windows, Linux does not use drive letters like **C:** or **D:**.

Everything starts from a single root directory:

```
/
```

```
                    /
        ├──────────┼──────────┬───────────┐
      /bin       /etc       /var       /home
```

Every file and directory on the system exists somewhere beneath the root directory.

---

## Important Directories

### `/`

The root directory.

Everything in Linux starts here.

---

### `/bin`

Contains essential system binaries and commands.

Examples:

```bash
ls
cp
mv
cat
bash
```

---

### `/etc`

Stores system configuration files.

Examples:

```
/etc/passwd
/etc/shadow
/etc/hosts
```

---

### `/var`

Contains files that constantly change.

Examples:

```
/var/log/
/var/www/
/var/cache/
```

---

### `/home`

Home directories of normal users.

Example:

```
/home/abhinav
```

---

### `/root`

Home directory of the root user.

Unlike `/home`, only the administrator normally has access.

---

# Commands Learned

## Display Current Directory

```bash
pwd
```

Meaning:

```
Print Working Directory
```

Example:

```bash
pwd
```

Output:

```
/home/analyst/investigations
```

---

## List Files

Basic listing:

```bash
ls
```

Shows only visible files.

---

Detailed listing:

```bash
ls -l
```

Displays:

- permissions
- owner
- group
- size
- date

---

Show hidden files:

```bash
ls -a
```

Hidden files begin with:

```
.
```

Example:

```
.bashrc
.profile
```

---

Complete Listing

```bash
ls -la
```

Shows:

- hidden files
- permissions
- owner
- size
- timestamps

Example:

```
-rw-r--r--
.hidden_config
audit.log
```

---

# File Operations

## Create a File

```bash
touch notes.txt
```

Creates an empty file.

If the file already exists, it updates the timestamp.

---

## Copy Files

```bash
cp source.txt destination.txt
```

Example:

```bash
cp raw_events.log /var/backups/events_copy.log
```

---

### Copy Directories

```bash
cp -r folder destination
```

The `-r` flag means **recursive**, allowing entire directories (including all subdirectories and files) to be copied.

Example:

```bash
cp -r /var/log /backup/logs
```

---

## Move Files

```bash
mv file destination
```

Example:

```bash
mv report.txt /home/analyst/
```

---

## Rename Files

```bash
mv old.txt new.txt
```

The `mv` command is also used to rename files.

---

# Deleting Files

Delete a file:

```bash
rm file.txt
```

---

Delete a directory:

```bash
rm -r folder
```

---

Force deletion:

```bash
rm -rf folder
```

Flags:

- `-r` → Recursive
- `-f` → Force

---

## Dangerous Command

```bash
rm -rf /
```

### Why It Is Dangerous

This command recursively deletes the entire Linux file system, including:

- system binaries
- configuration files
- user files
- installed programs

The operating system becomes unusable.

This command should **never** be executed on a production or personal system.

---

# Viewing Files

## View Entire File

```bash
cat file.txt
```

---

## View Beginning of a File

```bash
head file.txt
```

Specify lines:

```bash
head -n 20 file.txt
```

Displays the first 20 lines.

---

## View End of a File

```bash
tail file.txt
```

Specify lines:

```bash
tail -n 50 auth.log
```

Displays the last 50 lines.

---

## Monitor Logs in Real Time

```bash
tail -f /var/log/syslog
```

The `-f` (follow) option continuously displays new lines as they are written to the log file.

### SOC Use Case

A SOC analyst can monitor logs in real time to detect:

- SSH brute-force attacks
- failed login attempts
- service crashes
- suspicious activity

---

# Linux Permissions

Using:

```bash
ls -l
```

Produces output like:

```
-rwxr-xr--
```

---

## Permission Structure

```
-rwxr-xr--
│ │ │ │
│ │ │ └── Others
│ │ └──── Group
│ └────── Owner
└──────── File Type
```

---

## File Types

```
-  File

d  Directory
```

---

## Permission Values

| Permission | Value |
|------------|------:|
| Read | 4 |
| Write | 2 |
| Execute | 1 |

---

### Examples

```
rwx

4+2+1

=

7
```

```
rw-

4+2

=

6
```

```
r-x

4+1

=

5
```

```
r--

4
```

---

## chmod 700

```bash
chmod 700 sensitive.conf
```

Permission:

```
Owner

rwx

=

7

Group

---

0

Others

---

0
```

Only the owner has full access.

---

# SSH Key Protection

Private SSH keys should be protected.

Example:

```bash
chmod 700 id_rsa
```

If permissions are too open, SSH refuses to use the key and displays:

```
WARNING: UNPROTECTED PRIVATE KEY FILE!
```

This prevents unauthorized users from accessing private keys.

---

# Searching for Files

## find

```bash
find /home -name "file.txt"
```

Searches the live filesystem in real time.

### Characteristics

- Accurate
- Searches every directory
- Slower on large systems

---

## locate

```bash
locate file.txt
```

Searches an indexed database.

### Characteristics

- Very fast
- May not find recently created files because the database is updated periodically using `updatedb`

---

# Hiding Permission Errors

Searching the entire filesystem as a normal user often generates many "Permission denied" messages.

Example:

```bash
find / -name "malware.exe"
```

Clean the output by redirecting errors:

```bash
find / -name "malware.exe" 2>/dev/null
```

### Explanation

```
2

↓

stderr

>

↓

Redirect

/dev/null

↓

Discard the errors
```

Only successful matches are displayed.

---

# Finding SUID Binaries

Command:

```bash
find / -perm -4000 -type f 2>/dev/null
```

### Explanation

- `-perm -4000` → Find SUID files
- `-type f` → Only regular files
- `2>/dev/null` → Hide permission errors

---

## Why SUID Matters

A SUID binary runs with the permissions of its owner instead of the user executing it.

If owned by `root`, it executes with root privileges.

Misconfigured SUID binaries can lead to local privilege escalation.

---

# grep

Search inside files.

Example:

```bash
grep "error" logfile.txt
```

---

## Recursive Search

```bash
grep -r "password" /etc
```

Searches all files and subdirectories.

---

# Pipes

The pipe operator:

```bash
|
```

passes the output of one command as the input to another.

Example:

```bash
cat access.log | grep "404" | wc -l
```

### Breakdown

1. `cat access.log` → Displays the file.
2. `grep "404"` → Filters only lines containing `404`.
3. `wc -l` → Counts the number of matching lines.

Result: Total number of HTTP 404 errors.

---

# Process Management

## View Running Processes

```bash
ps aux
```

Flags:

- `a` → All users
- `u` → User-oriented format
- `x` → Include processes without a terminal

---

## Stop a Process Gracefully

```bash
kill PID
```

Sends the `SIGTERM` signal, allowing the process to exit cleanly.

---

## Force Kill a Process

```bash
kill -9 PID
```

Sends the `SIGKILL` signal, immediately terminating the process without cleanup.

---

# Background Processes

Pause a running process:

```
Ctrl + Z
```

Resume it in the background:

```bash
bg
```

Useful for continuing long-running tasks while keeping the terminal available.

---

# Package Management

Debian-based systems use the `apt` package manager.

---

## Update Package Lists

```bash
sudo apt update
```

Downloads the latest package information from configured repositories.

---

## Upgrade Installed Packages

```bash
sudo apt upgrade
```

Installs the latest available versions of installed packages.

---

## Package Not Found?

If `apt` cannot locate a package, verify that the appropriate repository is listed in:

```text
/etc/apt/sources.list
```

---

# Commands Learned

```bash
pwd

ls
ls -l
ls -a
ls -la

touch

cp
cp -r

mv

rm
rm -r
rm -rf

cat

head
head -n

tail
tail -n
tail -f

chmod

find

locate

grep
grep -r

ps aux

kill
kill -9

bg

apt update
apt upgrade
```

---

# Key Concepts Learned

- Linux File System Hierarchy
- Root Directory
- System Configuration Files
- User Home Directories
- File Creation
- File Copying
- File Moving
- File Deletion
- Linux Permissions
- Numeric Permissions
- chmod
- SSH Key Protection
- Real-Time Log Monitoring
- find vs locate
- Standard Error Redirection
- SUID Binaries
- grep
- Pipes
- Process Management
- Signals (SIGTERM & SIGKILL)
- Background Jobs
- Debian Package Management

---

# Security Notes

- Never execute `rm -rf /` on a production system.
- Restrict sensitive files using appropriate permissions such as `chmod 700`.
- Audit SUID binaries regularly, as misconfigured SUID programs can be exploited for privilege escalation.
- Use `tail -f` to monitor logs during security investigations and incident response.
- Redirect permission errors with `2>/dev/null` to produce cleaner search results.
- Keep systems updated with `apt update` and `apt upgrade` to reduce exposure to known vulnerabilities.