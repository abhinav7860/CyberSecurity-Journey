# LazySysAdmin --- Full Walkthrough & Learning Notes
**Date:** 19 September 2026  
> **Lab:** VulnHub LazySysAdmin\
> **Purpose:** Educational penetration-testing lab in an isolated
> environment\
> **Focus:** Enumeration → SMB discovery → credential discovery →
> WordPress access → SSH → sudo privilege escalation\
> **Style:** Step-by-step explanation of what I did, why I did it, what
> I learned, and which paths turned out to be dead ends.

------------------------------------------------------------------------

## 1. Lab Overview

This walkthrough documents my complete path through the LazySysAdmin
machine, starting from host discovery with `netdiscover` and ending with
a root shell using:

``` bash
sudo /bin/bash
```

The important lesson from this machine is that the final privilege
escalation was simple. The difficult part was **enumeration and
connecting clues together**.

The final attack chain was:

``` text
Host Discovery
      ↓
Nmap Enumeration
      ↓
SMB Enumeration
      ↓
Anonymous SMB Access
      ↓
WordPress Files
      ↓
wp-config.php
      ↓
Database Credential
      ↓
WordPress Administrator Access
      ↓
Credential Reuse / Password Clue
      ↓
SSH as togie
      ↓
sudo -l
      ↓
(ALL : ALL) ALL
      ↓
sudo /bin/bash
      ↓
ROOT
```

------------------------------------------------------------------------

# 2. Important Safety / Sanitization Note

This document is written for my **VulnHub lab**.

For a public GitHub repository, I sanitized identifying details such as:

-   attacker-machine IP
-   exact MAC address
-   SSH host fingerprint
-   passwords discovered during the lab
-   other unnecessary environment-specific information

The commands use variables where possible:

``` bash
TARGET_IP="192.168.29.190"
```

The target IP above is a private lab address. If publishing this
publicly, it can also be replaced with:

``` text
TARGET_IP
```

The credentials discovered during the lab are intentionally referred to
as:

``` text
[REDACTED_DB_PASSWORD]
[REDACTED_USER_PASSWORD]
```

This preserves the learning process without publishing reusable
credentials.

------------------------------------------------------------------------

# 3. Step 1 --- Discovering the Target with `netdiscover`

## Command

``` bash
sudo netdiscover
```

### What is `netdiscover`?

`netdiscover` is a tool used to discover devices that are alive on a
local network.

Think of the lab network like a classroom.

There may be several computers connected to the same network, but I do
not initially know which computer is the vulnerable machine.

`netdiscover` helps answer:

> "Which devices are currently on my local network?"

It uses ARP (Address Resolution Protocol) to identify devices.

### Result

The vulnerable machine appeared as:

``` text
192.168.29.190
```

The machine was identified as a VirtualBox system.

I saved this as the target:

``` bash
TARGET_IP=192.168.29.190
```

### Why this matters

Before attacking a machine, I first need to know:

1.  Does the machine exist?
2.  What IP address does it have?
3.  Which machine should I investigate?

This is the first stage of reconnaissance.

------------------------------------------------------------------------

# 4. Step 2 --- Scan the Target with Nmap

Once I knew the target IP, I performed a detailed Nmap scan.

## Command

``` bash
nmap -A -sV 192.168.29.190
```

### What does `nmap` do?

Nmap is a network scanner.

It helps answer questions such as:

-   Which ports are open?
-   What services are running?
-   What versions are running?
-   Can Nmap identify the operating system?
-   Are there useful service-specific details?

### Meaning of the options

``` text
-A
```

Enables aggressive detection features such as:

-   OS detection
-   version detection
-   script scanning
-   traceroute

``` text
-sV
```

Attempts to identify the versions of services running on open ports.

### Important findings

The scan revealed:

  Port   Service       Finding
  ------ ------------- ---------------------------
  22     SSH           OpenSSH
  80     HTTP          Apache + Silex / Backnode
  139    SMB/NetBIOS   Samba
  445    SMB           Samba
  3306   MySQL         MySQL reachable
  6667   IRC           InspIRCd

This was a very important point.

Instead of blindly trying exploits, I now had a map of the machine's
exposed services.

------------------------------------------------------------------------

# 5. Step 3 --- Investigating HTTP

The web server was running on:

``` text
http://192.168.29.190/
```

The page showed a Silex/Backnode-based site.

I then investigated `robots.txt`.

## Command

``` bash
curl -i http://192.168.29.190/robots.txt
```

The file revealed directories such as:

``` text
/old/
/test/
/TR2/
/Backnode_files/
```

### Why check `robots.txt`?

`robots.txt` tells search-engine crawlers which paths a website owner
does not want indexed.

It is **not a security mechanism**.

In CTFs and labs, developers sometimes accidentally reveal interesting
directories there.

I investigated:

``` text
/old/
/test/
/TR2/
/Backnode_files/
```

The first three did not give me a useful foothold.

------------------------------------------------------------------------

# 6. Step 4 --- Investigating `Backnode_files`

I checked:

``` bash
curl -i http://192.168.29.190/Backnode_files/
```

The server returned a directory listing.

It contained files such as:

``` text
styles.css
front-end.css
jquery-ui.js
front-end.js
jquery.js
script.json
logo.png
normalize.css
```

I also checked:

``` bash
curl http://192.168.29.190/Backnode_files/script.json
```

The response indicated that the requested file/data was not found.

At this point, `Backnode_files` appeared to be mostly frontend resources
rather than an immediate attack path.

------------------------------------------------------------------------

# 7. Step 5 --- Discovering SMB

Nmap showed SMB on ports 139 and 445.

SMB is important because it can provide access to:

-   shared files
-   directories
-   printers
-   Windows/Linux file shares
-   sometimes sensitive configuration files

I enumerated the SMB shares anonymously.

## Command

``` bash
smbclient -L //192.168.29.190 -N
```

### Meaning

``` text
-L
```

List available shares.

``` text
-N
```

Do not ask for a password.

### Result

The important share was:

``` text
share$
```

There were also:

``` text
print$
IPC$
```

The `share$` share was the interesting one.

------------------------------------------------------------------------

# 8. Step 6 --- Anonymous SMB Access

I connected without credentials:

``` bash
smbclient //192.168.29.190/share$ -N
```

The server allowed anonymous access.

This was a major security misconfiguration.

Inside the share, I found:

``` text
wordpress/
Backnode_files/
wp/
deets.txt
robots.txt
todolist.txt
apache/
index.html
info.php
test/
old/
```

This was much more interesting than the original web page.

------------------------------------------------------------------------

# 9. Step 7 --- Discovering `deets.txt`

One of the files was:

``` text
deets.txt
```

I opened it with the SMB client.

It contained a warning about remembering passwords and an old password.

For the sanitized version of this README, the actual password is
omitted:

``` text
CBF Remembering all these passwords.
Remember to remove this file and update your password after we push out the server.

Password: [REDACTED_USER_PASSWORD]
```

### Why was this important?

A file containing passwords should never be exposed through an anonymous
network share.

It also gave me a possible credential-reuse clue.

At this point I did **not** yet know which account the password belonged
to.

That distinction is important.

Finding a password does not automatically mean:

> "This must be the SSH password."

I needed more evidence.

------------------------------------------------------------------------

# 10. Step 8 --- Discovering `todolist.txt`

Another useful file was:

``` text
todolist.txt
```

It contained a task referring to preventing users from viewing the web
root through the local file browser.

This was a useful clue because it explained why the SMB share exposed so
much of the web directory.

In other words:

> The server configuration itself was insecure, and the administrator
> had apparently intended to fix it but had not done so.

This helped explain why anonymous SMB access was possible.

------------------------------------------------------------------------

# 11. Step 9 --- Investigating `info.php`

The SMB share also contained:

``` text
info.php
```

The page contained PHP information generated by:

``` php
phpinfo();
```

I requested it with:

``` bash
curl -i http://192.168.29.190/info.php
```

Important information included:

``` text
Apache 2.4.7
PHP 5.5.9
Ubuntu 14.04
Document Root: /var/www/html
Server user: www-data
MySQL support enabled
```

### Why is `phpinfo()` useful?

`phpinfo()` can expose a large amount of server configuration
information.

For a real production server, exposing it publicly can leak information
useful to attackers.

------------------------------------------------------------------------

# 12. Step 10 --- Investigating the WordPress Directory

The SMB share contained:

``` text
wordpress/
```

I entered it:

``` text
cd wordpress
ls
```

It contained a complete WordPress installation.

Important files included:

``` text
wp-config.php
wp-config-sample.php
wp-login.php
wp-admin/
wp-content/
wp-includes/
```

The most interesting file was:

``` text
wp-config.php
```

because WordPress stores its database connection information there.

------------------------------------------------------------------------

# 13. Step 11 --- Reading `wp-config.php`

I downloaded the file from SMB and inspected it.

The important configuration was:

``` php
define('DB_NAME', 'wordpress');
define('DB_USER', 'Admin');
define('DB_PASSWORD', '[REDACTED_DB_PASSWORD]');
define('DB_HOST', 'localhost');
```

### Why was this important?

WordPress needs database credentials to communicate with MySQL.

So `wp-config.php` effectively told me:

``` text
Database:
    wordpress

Database user:
    Admin

Database password:
    [REDACTED_DB_PASSWORD]

Database host:
    localhost
```

The most important detail was:

``` text
DB_HOST = localhost
```

That would become relevant shortly.

------------------------------------------------------------------------

# 14. Step 12 --- Attempting Remote MySQL Access

Since Nmap showed MySQL on port 3306, I initially tested whether the
credentials could be used remotely.

## Command

``` bash
mysql -h 192.168.29.190 -u Admin -p
```

I supplied the password discovered in `wp-config.php`.

The server returned an error indicating:

``` text
Host '192.168.29.163' is not allowed to connect to this MySQL server
```

### What does this mean?

This was **not necessarily a bad-password error**.

The MySQL server was reachable, but the account was not permitted to
connect from my Kali machine.

This made sense because:

``` text
DB_HOST = localhost
```

The WordPress configuration expected the database to be accessed locally
from the target server.

### Lesson

A credential can be:

``` text
correct
```

but still unusable remotely because of access-control restrictions.

------------------------------------------------------------------------

# 15. Step 13 --- Testing SSH Credential Reuse

At one point, I tested whether the database username/password had been
reused for SSH:

``` bash
ssh Admin@192.168.29.190
```

The authentication failed.

This was useful because it told me:

> Do not assume that a database credential is automatically an SSH
> credential.

This branch was abandoned.

------------------------------------------------------------------------

# 16. Step 14 --- Investigating Other SMB Directories

I checked:

``` text
wp/
apache/
```

Both were empty.

I also checked:

``` text
Backnode_files/
```

through SMB.

It contained mostly the same frontend assets seen through HTTP:

``` text
styles.css
front-end.css
jquery-ui.js
front-end.js
jquery.js
script.json
images
```

No obvious credential or server-side file was discovered there.

This was another example of enumeration helping me eliminate dead ends.

------------------------------------------------------------------------

# 17. Step 15 --- Investigating IRC

Nmap had also found IRC on port 6667.

The server identified itself as:

``` text
Admin.local
```

I initially connected with:

``` bash
nc -nv 192.168.29.190 6667
```

The server responded with a hostname lookup message and then:

``` text
Registration timeout
```

This happened because raw `nc` does not automatically perform the IRC
registration protocol.

I considered registering manually with IRC commands, but this branch did
not produce a useful path for the lab.

### Lesson

Not every open port is an intended exploitation route.

Nmap gives me possibilities.

It does not mean:

> "Every open port must be exploited."

Good enumeration means knowing when to stop chasing a branch.

------------------------------------------------------------------------

# 18. Step 16 --- WordPress Login

The strongest clue from the WordPress configuration was the password
discovered in `wp-config.php`.

The password was reused by the WordPress administrator account.

The WordPress login page was:

``` text
/wordpress/wp-login.php
```

I logged in using the discovered WordPress credentials.

The WordPress administrator identity was:

``` text
togie
```

This was the clue that connected the application to the Linux user we
eventually needed.

------------------------------------------------------------------------

# 19. Step 17 --- Connecting the Password Clues

We now had two important pieces of information:

### From `wp-config.php`

``` text
WordPress database password:
[REDACTED_DB_PASSWORD]
```

### From `deets.txt`

``` text
Password:
[REDACTED_USER_PASSWORD]
```

The WordPress administrator was:

``` text
togie
```

This suggested that the weak password from `deets.txt` belonged to the
Linux `togie` account.

Instead of blindly assuming this, I tested the hypothesis through SSH.

------------------------------------------------------------------------

# 20. Step 18 --- SSH as `togie`

## Command

``` bash
ssh togie@192.168.29.190
```

I supplied the password discovered in `deets.txt`.

This time the login succeeded.

The shell showed:

``` text
togie@LazySysAdmin:~$
```

This was our first actual shell access to the Linux machine.

------------------------------------------------------------------------

# 21. Step 19 --- Understanding the `togie` Shell

I checked the home directory:

``` bash
ls
```

and:

``` bash
ls -la
```

The home directory was:

``` text
/home/togie
```

I also checked:

``` bash
pwd
```

which confirmed:

``` text
/home/togie
```

------------------------------------------------------------------------

# 22. Step 20 --- Checking the Operating System

I ran:

``` bash
uname -a
```

The result showed:

``` text
Linux LazySysAdmin
Ubuntu 14.04
Linux kernel 4.4.0-31-generic
i686
```

This confirmed the older Ubuntu-based lab environment.

------------------------------------------------------------------------

# 23. Step 21 --- Understanding the Restricted Shell

I inspected `/etc/passwd`:

``` bash
cat /etc/passwd
```

The important entry was:

``` text
togie:x:1000:1000:togie,,,:/home/togie:/bin/rbash
```

The final field was:

``` text
/bin/rbash
```

### What is `rbash`?

`rbash` means **restricted Bash**.

It is a restricted version of the Bash shell.

This explains why a command such as:

``` bash
unam -a
```

produced a restricted-shell-related error.

The important point was:

> The shell itself was restricted, but that did not necessarily mean the
> account lacked powerful privileges.

So I needed to inspect the user's sudo permissions.

------------------------------------------------------------------------

# 24. Step 22 --- The Critical Privilege Escalation Discovery

I ran:

``` bash
sudo -l
```

This asks:

> "Which commands is my current user allowed to run with sudo?"

The important result was:

``` text
User togie may run the following commands on LazySysAdmin:
    (ALL : ALL) ALL
```

This is the critical finding of the entire privilege-escalation phase.

------------------------------------------------------------------------

# 25. What `(ALL : ALL) ALL` Means

Break it down:

``` text
(ALL : ALL) ALL
```

The first `ALL` means the command can be run as **any user**.

The second `ALL` means it can be run with **any group**.

The final `ALL` means **any command** is allowed.

Because `root` is one of the users, this effectively gives `togie` the
ability to execute arbitrary commands as root.

This is an extremely dangerous sudo configuration.

------------------------------------------------------------------------

# 26. Step 23 --- Confirming Root Privileges

At this point, I did not need a kernel exploit, SUID exploit, or
complicated privilege-escalation technique.

I simply used the permission that `sudo -l` had already revealed.

## Command

``` bash
sudo /bin/bash
```

After entering the `togie` password, the prompt changed to:

``` text
root@LazySysAdmin:~#
```

I verified it with:

``` bash
whoami
```

Output:

``` text
root
```

### Why did this work?

`sudo` executes a command with elevated privileges.

The command I asked it to execute was:

``` text
/bin/bash
```

Bash is a shell.

Because `togie` was allowed to run **any command as any user**, Bash was
launched with root privileges.

So:

``` text
togie
  |
  | sudo /bin/bash
  ↓
root Bash shell
```

------------------------------------------------------------------------

# 27. Why `pwd` Still Showed `/home/togie`

After becoming root, I ran:

``` bash
pwd
```

and saw:

``` text
/home/togie
```

This is not a contradiction.

There are two separate concepts:

### Identity

``` bash
whoami
```

returned:

``` text
root
```

### Current directory

``` bash
pwd
```

returned:

``` text
/home/togie
```

Becoming root changes **who I am running as**. It does not automatically
change my current working directory.

I could move to root's home directory with:

``` bash
cd /root
```

------------------------------------------------------------------------

# 28. Final Attack Chain

The complete chain was:

``` text
1. sudo netdiscover
        ↓
2. Discover target IP
        ↓
3. nmap -A -sV TARGET_IP
        ↓
4. Discover SMB
        ↓
5. smbclient -L //TARGET_IP -N
        ↓
6. Anonymous access to share$
        ↓
7. Find deets.txt
        ↓
8. Find WordPress directory
        ↓
9. Read wp-config.php
        ↓
10. Discover database credentials
        ↓
11. Understand DB_HOST = localhost
        ↓
12. Remote MySQL attempt fails because remote host is not allowed
        ↓
13. SSH as Admin fails
        ↓
14. Investigate WordPress
        ↓
15. Log into WordPress as togie
        ↓
16. Connect the password clue to togie
        ↓
17. SSH as togie
        ↓
18. sudo -l
        ↓
19. Discover (ALL : ALL) ALL
        ↓
20. sudo /bin/bash
        ↓
21. whoami → root
```

------------------------------------------------------------------------

# 29. Commands Used

For reference, these were the important commands used throughout the
lab.

## Host discovery

``` bash
sudo netdiscover
```

## Port and service enumeration

``` bash
nmap -A -sV TARGET_IP
```

## Web enumeration

``` bash
curl -i http://TARGET_IP/robots.txt
curl -i http://TARGET_IP/Backnode_files/
curl http://TARGET_IP/Backnode_files/script.json
curl -i http://TARGET_IP/info.php
```

## SMB enumeration

``` bash
smbclient -L //TARGET_IP -N
```

## Anonymous SMB connection

``` bash
smbclient //TARGET_IP/share$ -N
```

Inside SMB:

``` text
ls
cd wordpress
ls
cd ..
cd wp
ls
cd ..
cd apache
ls
cd ..
cd Backnode_files
ls
```

## Remote MySQL test

``` bash
mysql -h TARGET_IP -u Admin -p
```

## SSH credential-reuse test

``` bash
ssh Admin@TARGET_IP
```

## IRC enumeration attempt

``` bash
nc -nv TARGET_IP 6667
```

## SSH as the discovered Linux user

``` bash
ssh togie@TARGET_IP
```

## Basic Linux enumeration

``` bash
ls
ls -la
pwd
uname -a
cat /etc/passwd
```

## Sudo enumeration

``` bash
sudo -l
```

## Final privilege escalation

``` bash
sudo /bin/bash
```

## Root verification

``` bash
whoami
```

------------------------------------------------------------------------

# 30. What Each Important Tool Taught Me

## `netdiscover`

**Purpose:** Find devices on the local network.

**Lesson:** Start by identifying the target.

------------------------------------------------------------------------

## `nmap`

**Purpose:** Discover open ports and services.

**Lesson:** Build a map of the attack surface before choosing a path.

------------------------------------------------------------------------

## `smbclient`

**Purpose:** Interact with SMB shares.

**Lesson:** Anonymous file shares can expose extremely sensitive files.

------------------------------------------------------------------------

## `curl`

**Purpose:** Send HTTP requests and inspect web responses.

**Lesson:** Web servers can expose useful files, directories, and
configuration information.

------------------------------------------------------------------------

## `mysql`

**Purpose:** Connect to MySQL.

**Lesson:** A valid credential can still be blocked by database access
controls.

------------------------------------------------------------------------

## `ssh`

**Purpose:** Obtain a remote shell.

**Lesson:** Credential reuse can sometimes turn an application clue into
operating-system access.

------------------------------------------------------------------------

## `sudo -l`

**Purpose:** Show what the current user is allowed to execute with sudo.

**Lesson:** Always check sudo permissions after obtaining a shell.

------------------------------------------------------------------------

## `sudo /bin/bash`

**Purpose:** Start Bash with sudo privileges.

**Lesson:** If a user is allowed to run arbitrary commands as root, a
root shell may require only a single command.

------------------------------------------------------------------------

# 31. Biggest Lessons From This Lab

### 1. Enumeration is more important than immediately exploiting everything

The box exposed several services:

``` text
SSH
HTTP
SMB
MySQL
IRC
```

But not every service was the intended path.

The successful route came from carefully examining what SMB exposed.

------------------------------------------------------------------------

### 2. Sensitive files are often more valuable than software vulnerabilities

The major breakthroughs came from:

``` text
deets.txt
wp-config.php
```

These were configuration/administrative files, not sophisticated
exploits.

------------------------------------------------------------------------

### 3. Credentials should always be treated in context

The database credentials were not automatically SSH credentials.

I tested the hypothesis, received a denial, and moved on.

Later, the separate password clue combined with the `togie` identity
produced successful SSH access.

------------------------------------------------------------------------

### 4. `DB_HOST=localhost` mattered

The MySQL connection failed remotely because the database account was
not allowed to connect from my Kali machine.

This was not necessarily evidence that the password was incorrect.

It demonstrated the difference between:

``` text
Authentication
```

and:

``` text
Authorization / host-based access control
```

------------------------------------------------------------------------

### 5. `sudo -l` is extremely important after getting a shell

Once I had:

``` text
togie@LazySysAdmin
```

the next logical question was:

> "What can this user do?"

`sudo -l` answered that immediately.

------------------------------------------------------------------------

### 6. Privilege escalation does not always require an exploit

The final escalation was caused by an overly permissive sudo rule:

``` text
(ALL : ALL) ALL
```

There was no need for a kernel exploit.

The machine had already given the user the ability to execute arbitrary
commands as root.

------------------------------------------------------------------------

# 32. Defender / SOC Perspective

From a defensive perspective, this machine demonstrates several things
that should raise alerts or security findings.

## Anonymous SMB access

A user should not normally be able to anonymously browse sensitive
server files.

Potential controls:

-   Disable unnecessary guest access.
-   Restrict SMB shares.
-   Apply least privilege.
-   Monitor anonymous SMB activity.

------------------------------------------------------------------------

## Passwords stored in accessible files

A file containing passwords should never be exposed through a network
share.

Potential controls:

-   Remove plaintext credentials.
-   Use a secrets-management solution.
-   Apply correct file permissions.
-   Scan repositories and shares for secrets.

------------------------------------------------------------------------

## Password reuse

The same or related credentials were used across
application/database/user contexts.

Potential controls:

-   Unique passwords per service.
-   Strong password policies.
-   Credential rotation.
-   MFA where possible.

------------------------------------------------------------------------

## Exposed `phpinfo()`

A publicly accessible `phpinfo()` page can disclose:

-   PHP version
-   modules
-   paths
-   server configuration
-   environment information

Potential control:

Remove it from production systems or restrict access.

------------------------------------------------------------------------

## Overly permissive sudo

The most serious privilege-escalation issue was:

``` text
(ALL : ALL) ALL
```

A least-privilege configuration would grant only the specific commands
required for the user's job.

------------------------------------------------------------------------

# 33. Final Takeaway

The most important thing I learned from LazySysAdmin is that a
successful penetration test is not always about finding a complicated
exploit.

The machine had multiple clues spread across different services.

I had to connect them:

``` text
SMB
 ↓
Sensitive files
 ↓
WordPress configuration
 ↓
Credentials
 ↓
WordPress user
 ↓
Linux user
 ↓
SSH
 ↓
sudo permissions
 ↓
root
```

The final command was simple:

``` bash
sudo /bin/bash
```

But that command only worked because the earlier enumeration revealed:

``` text
togie → (ALL : ALL) ALL
```

So the real skill demonstrated by this lab was **enumeration,
evidence-based decision making, credential analysis, and privilege
discovery**.

------------------------------------------------------------------------

## Final Root Verification

The final verification was:

``` bash
whoami
```

Result:

``` text
root
```

