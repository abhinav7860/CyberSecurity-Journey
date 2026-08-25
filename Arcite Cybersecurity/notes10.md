# Gobuster

## Basic Notes

**Topic:** Gobuster  
**Date Added:** 25 August 2026  
**Status:** Studied - Basic Level

---

## What is Gobuster?

Gobuster is a command-line tool used for discovering hidden or interesting resources on web servers.

I studied it mainly for web reconnaissance, especially finding directories and files that are not directly visible from a website's normal navigation.

---

## Why Gobuster is Used

When testing a web application, we might only see a few pages from the website.

Gobuster can help discover additional paths such as:

- Directories
- Files
- PHP pages
- Other web resources

For example:

```text
/index.php
/login.php
/admin/
/uploads/
```

Some of these might not be linked from the main page.

---

## Basic Directory Enumeration

The basic command I learned is:

```bash
gobuster dir -u http://TARGET_IP -w wordlist.txt
```

Where:

- `dir` = directory/file enumeration mode
- `-u` = target URL
- `-w` = wordlist
- `TARGET_IP` = target web server

Example:

```bash
gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt
```

---

## Using File Extensions

Gobuster can also check for specific file extensions.

```bash
gobuster dir -u http://10.10.10.10 -w wordlist.txt -x php
```

The `-x` option tells Gobuster to check for files with that extension.

For example:

```text
login.php
admin.php
test.php
```

---

## Wordlists

Gobuster uses wordlists containing possible directory or file names.

Example:

```text
admin
login
uploads
backup
test
dashboard
```

The wordlist affects what Gobuster is able to discover.

---

## Understanding the Results

Gobuster can show the HTTP status code for discovered resources.

Some common ones are:

```text
200 -> OK / resource found
301 -> Redirect
302 -> Temporary redirect
403 -> Forbidden
404 -> Not found
```

These codes help me understand what happened when Gobuster requested a path.

Finding something like `/admin` does not automatically mean it is vulnerable. It just means it is worth investigating.

---

## Basic Options I Learned

### `-u`

Specifies the target URL.

```bash
-u http://TARGET_IP
```

### `-w`

Specifies the wordlist.

```bash
-w wordlist.txt
```

### `-x`

Checks specific file extensions.

```bash
-x php
```

### `-t`

Controls the number of concurrent threads.

```bash
-t 10
```

---

## Basic Recon Workflow

My basic understanding is:

```text
1. Identify the web server
        ↓
2. Choose a suitable wordlist
        ↓
3. Run Gobuster
        ↓
4. Look at interesting results
        ↓
5. Investigate the discovered resources
```

Gobuster is mainly a discovery tool. It helps me understand what is exposed by a web server.

---

## Gobuster vs Nmap

I understood the basic difference as:

```text
Nmap     -> Finds hosts, ports and services
Gobuster -> Finds web directories and files
```

They can be used together during reconnaissance.

Example:

```text
Nmap
  ↓
Find port 80/443
  ↓
Identify web service
  ↓
Gobuster
  ↓
Find hidden web resources
```

---

## What I Learned

The main thing I understood about Gobuster is that it helps with web enumeration.

Instead of manually guessing whether a website has an `/admin`, `/backup`, or `/uploads` directory, Gobuster can test many possible paths using a wordlist.

It is useful during the reconnaissance stage because it helps build a better picture of what is exposed by the web server.

---

## Important Note

I should only use Gobuster against:

- My own systems
- TryHackMe/CTF machines
- Lab environments
- Targets where I have explicit permission

---

## My Takeaway

Gobuster is a simple but useful reconnaissance tool.

For now, I only studied the basic stuff: what Gobuster does, directory enumeration, wordlists, file extensions, common HTTP status codes, and options like `-u`, `-w`, `-x`, and `-t`.

I don't need to know every option yet. The important part is understanding where Gobuster fits into a penetration testing workflow and how it helps discover web resources.

---

## Progress

```text
[✓] What Gobuster is
[✓] Directory enumeration
[✓] Wordlists
[✓] File extensions
[✓] HTTP status codes
[✓] Basic options
[✓] Recon workflow
[✓] Gobuster vs Nmap
```

**Status: Completed - Basic Level**
