# Network Services 2 — TryHackMe

**Study date:** 20 November 2026  
**Platform:** TryHackMe  
**Focus:** NFS, SMTP, service enumeration, SSH authentication, MySQL fundamentals and database security

> **Lab scope:** The commands and exploitation concepts below are for the authorised TryHackMe lab only. Do not scan, enumerate, mount shares, brute-force accounts or exploit systems without explicit permission.

---

## 1. Learning objectives

In this room I studied how common network services work and how misconfigurations can expose information or provide unauthorised access.

- Understand Network File System (NFS), exports and mounting.
- Enumerate NFS services and inspect exposed files.
- Understand NFS root squashing and the security implications of SUID files.
- Explain SMTP, POP and IMAP.
- Fingerprint SMTP services and enumerate users using Metasploit.
- Understand how discovered usernames may be abused in password attacks.
- Understand MySQL, relational databases, schemas and password hashes.

---

# Task 2 — Understanding NFS

## 2.1 What is NFS?

**NFS (Network File System)** allows a system to share directories and files with other systems over a network. A client can access files on a remote server almost as though those files were stored locally.

The server makes all or part of its filesystem available for mounting. The access a client receives depends on the permissions and export configuration applied by the server.

## 2.2 How NFS works

The lesson describes the following sequence:

1. An NFS client requests to mount a directory exported by a remote server.
2. The mount service communicates with the relevant mount daemon using RPC (Remote Procedure Call).
3. The server checks whether the client is permitted to mount the requested directory.
4. If permitted, the server returns a **file handle** that uniquely identifies a file or directory on the server.
5. When the client accesses a file, it sends an RPC request to the NFS daemon (**NFSD**) on the server.
6. The request includes information such as the file handle, filename, user ID (UID) and group ID (GID).
7. The server uses this information and its permissions to decide whether the requested operation, such as reading or writing, is allowed.

### Important terms

| Term | Meaning |
|---|---|
| NFS | Network File System; shares remote filesystems over a network |
| Client | System requesting access to a remote NFS share |
| Server | System exporting directories or files |
| Mount | Attaching a remote filesystem to a local directory |
| Export | Directory made available by an NFS server |
| Mount daemon | Service involved in handling mount requests |
| RPC | Remote Procedure Call; allows a program to request an operation from another system |
| NFSD | NFS server daemon that handles NFS requests |
| File handle | Identifier used to refer to an exported file or directory |
| UID/GID | Numeric user and group identities used in permission checks |

## 2.3 Where is NFS used?

NFS can be used across different operating systems. A Windows Server system can act as an NFS file server for non-Windows clients. A Windows-based system can also access files stored on a non-Windows NFS server.

Common administrative uses include centralised file storage, shared home directories and shared application data.

## 2.4 Security relevance

An NFS export may expose files that should not be available to every network client. A poorly restricted export can reveal:

- User home directories.
- Configuration files.
- SSH key material.
- Scripts and application files.
- Sensitive documents or backups.

**SOC perspective:** An unexpected client mounting an NFS export, accessing sensitive directories, or writing to a shared filesystem may deserve investigation. Context matters because NFS activity can also be legitimate.

---

# Task 3 — Enumerating NFS

## 3.1 What is enumeration?

Enumeration is an active information-gathering process used to discover details about a target system and its services. The results help identify possible attack paths and determine what should be investigated next.

A useful workflow is:

**Discover host → Scan ports → Identify services → Enumerate exports → Mount permitted share → Inspect contents → Record evidence**

## 3.2 Prepare the environment

The TryHackMe lesson asks learners to start the AttackBox (if required) and deploy the lab machine. Allow time for the target to boot.

Install NFS client utilities on Debian/Kali-based systems:

```bash
sudo apt update
sudo apt install nfs-common
```

The `nfs-common` package includes utilities such as:

| Utility | Purpose |
|---|---|
| `showmount` | Queries an NFS server for exported directories |
| `mount.nfs` | Supports mounting an NFS filesystem |
| `nfsstat` | Displays NFS statistics |
| `lockd`, `statd` | Support NFS file-locking coordination |
| `idmapd` | Supports mapping between user/group identities |

For this task, the most important tools are `showmount` and `mount.nfs`.

## 3.3 Port scanning

The lesson recommends Nmap with aggressive service detection and a scan of all TCP ports:

```bash
nmap -A -p- <TARGET_IP>
```

| Option | Meaning |
|---|---|
| `-A` | Enables OS detection, version detection, script scanning and traceroute |
| `-p-` | Scans all TCP ports, rather than only Nmap's default top 1,000 ports |

Record the discovered ports and service versions. NFS commonly involves port 2049, but RPC-related services can also be relevant. Use the actual scan output rather than assuming a port is open.

## 3.4 Enumerating NFS exports

Use `showmount` to request the list of exports:

```bash
/usr/sbin/showmount -e <TARGET_IP>
```

The `-e` option requests the server's export list. Record the visible share name and any client restrictions shown.

Example output format (illustrative only):

```text
Export list for <TARGET_IP>:
/home *
```

This is not the result of my lab scan. Replace it with the actual output from the deployed machine.

## 3.5 Mounting an NFS share

Create a local mount point:

```bash
sudo mkdir -p /tmp/mount
```

Mount the exported share:

```bash
sudo mount -t nfs <TARGET_IP>:<SHARE_NAME> /tmp/mount/ -o nolock
```

| Part | Function |
|---|---|
| `sudo` | Runs the command with elevated local privileges |
| `mount` | Attaches a filesystem to a local directory |
| `-t nfs` | Specifies NFS as the filesystem type |
| `<TARGET_IP>:<SHARE_NAME>` | NFS server address and exported directory |
| `/tmp/mount/` | Local mount point |
| `-o nolock` | Mount option that disables NLM locking |

The lesson writes the option as `-nolock`; the conventional mount syntax is `-o nolock`, where `nolock` is a mount option.

After mounting, inspect the contents:

```bash
cd /tmp/mount
pwd
ls -la
find . -maxdepth 3 -type d -print
```

Look carefully at directories and files. In this lab, the share appears to expose a user's home directory. SSH-related directories may contain authentication material.

## 3.6 SSH key discovery

A user's SSH configuration directory is commonly:

```text
~/.ssh/
```

Files that may be present include:

| File | Meaning |
|---|---|
| `id_rsa` | Common name for a private RSA key |
| `id_ed25519` | Common name for a private Ed25519 key |
| `id_ecdsa` | Common name for a private ECDSA key |
| `*.pub` | Public key |
| `authorized_keys` | Public keys permitted to authenticate to the account |
| `known_hosts` | Records host keys for servers previously contacted |
| `config` | Optional per-host SSH client configuration |

A **private key** is sensitive authentication material. A public key is intended to be shared, but a private key must be protected.

Copy a discovered private key to a location outside the mounted share, then restrict its permissions:

```bash
cp /tmp/mount/<PATH_TO_PRIVATE_KEY> ~/private_key
chmod 600 ~/private_key
```

The `600` permission means the file owner can read and write it, while group and other users have no permissions. SSH commonly refuses to use a private key if its permissions are too open.

The lesson's SSH command pattern is:

```bash
ssh -i <KEY_FILE> <USERNAME>@<TARGET_IP>
```

The username may be inferred from the home-directory name or other lab evidence. Confirm it from the actual files and lab context.

## 3.7 NFS enumeration record

I will fill in these values from my own TryHackMe scan and terminal output.

| Question | My lab result |
|---|---|
| Number of open ports | **[Fill in from Nmap]** |
| Port running the NFS-related service | **[Fill in from Nmap]** |
| Visible NFS share | **[Fill in from showmount]** |
| Folder inside the mounted share | **[Fill in from `ls`]** |
| Home-directory name | **[Fill in from directory listing]** |
| Directory that may contain SSH keys | **[Fill in from directory listing]** |
| Most useful key file | **[Fill in from the actual files]** |
| SSH login successful? (Y/N) | **[Record actual result]** |

**Note:** The source material supplied for these NFS questions displayed “Correct Answer” but did not include the answer values. I have deliberately not invented them.

---

# Task 4 — Exploiting NFS: Root Squashing and SUID

This task explains how a poorly configured NFS export can contribute to privilege escalation.

## 4.1 What is root squashing?

NFS commonly uses **root squashing** to prevent a remote client process running as root from automatically receiving root-level privileges on the NFS server.

With root squashing enabled, requests from a remote root user are mapped to an unprivileged identity, commonly `nfsnobody` or an equivalent anonymous account depending on the system.

This reduces the impact of a client attempting to use root privileges against a shared filesystem.

If root squashing is disabled on an export, remote root access can be dangerously powerful. In a vulnerable configuration, a client may be able to create files on the share with ownership and permissions that have security consequences on the server.

## 4.2 What is SUID?

**SUID (Set User ID)** is a special permission bit on executable files. When a SUID executable is run, the process uses the file owner's effective user ID rather than simply the ID of the user who launched it.

For example, if an executable is owned by root and has SUID enabled, executing it may cause the process to run with an effective UID of root. This is why an unexpected root-owned SUID executable is security-sensitive.

Useful permission inspection commands:

```bash
ls -l <FILE>
stat <FILE>
find <DIRECTORY> -type f -perm -4000 -ls 2>/dev/null
```

In a normal permission listing, SUID is represented by an `s` in the owner's execute position, for example:

```text
-rwsr-xr-x
```

## 4.3 The lab's exploitation chain

The lesson describes this sequence:

1. Obtain access to an NFS export.
2. Obtain a low-privilege shell on the target.
3. Retrieve a compatible Bash executable from the lab machine.
4. Place the executable in the writable NFS share.
5. Use the misconfigured export's permissions to set SUID on the file.
6. Connect to the target through SSH.
7. Execute the SUID Bash file in the lab to demonstrate the privilege-escalation condition.

The lesson provides this SCP pattern for retrieving Bash from the target:

```bash
scp -i <KEY_FILE> <USERNAME>@<TARGET_IP>:/bin/bash ~/Downloads/bash
```

It also provides an alternative download source for a compatible Bash binary:

```bash
wget https://github.com/polo-sec/writing/raw/master/Security%20Challenge%20Walkthroughs/Networks%202/bash
```

The downloaded binary must be compatible with the target operating system and architecture. The lesson specifically mentions a standard Ubuntu Server 18.04 Bash executable as an alternative.

> **Security note:** SUID shell exploitation is a privilege-escalation technique. Keep it inside the authorised lab. From a defensive perspective, the key lesson is that unsafe NFS export options combined with writable shares and SUID-capable files can create a path to elevated privileges.

## 4.4 Defensive checks

Administrators should:

- Keep root squashing enabled unless a well-justified exception exists.
- Restrict exports to trusted client hosts and networks.
- Avoid exporting sensitive directories unnecessarily.
- Use least privilege and read-only exports where possible.
- Review ownership and SUID permissions on files stored in shared directories.
- Monitor unexpected file creation, ownership changes and permission changes.
- Review NFS configuration and access logs as part of routine hardening.

## 4.5 SOC investigation clues

Potentially suspicious activity includes:

- A new or unusual client accessing an NFS server.
- Mount requests from an unexpected subnet.
- Enumeration of export lists followed by access to user directories.
- Reads of private SSH key files from a shared filesystem.
- Unexpected writes to a share that should be read-only.
- Creation of executable files or changes to SUID permissions.
- Subsequent SSH authentication from an unusual source.

Correlate network, authentication and endpoint evidence before deciding whether activity is malicious. A mount or SSH login by itself is not proof of compromise.

---

# Task 5 — Understanding SMTP

## 5.1 What is SMTP?

**SMTP (Simple Mail Transfer Protocol)** is used to send outgoing email.

An email system commonly uses SMTP for sending and POP3 or IMAP for retrieving or synchronising incoming messages.

The lesson describes three basic SMTP server functions:

1. Verify who is sending email through the SMTP server.
2. Send outgoing email.
3. Return the message to the sender when delivery cannot be completed.

## 5.2 SMTP, POP3 and IMAP

| Protocol | Main purpose | Typical use |
|---|---|---|
| SMTP | Sending and relaying email | Client-to-mail-server or mail-server-to-mail-server delivery |
| POP3 | Retrieving email | Downloads messages from the mail server to a client |
| IMAP | Accessing and synchronising email | Keeps messages and mailbox state synchronised with the server |

The main difference described in the lesson is that POP takes a simpler download-oriented approach, while IMAP synchronises mailbox state with the server. Modern POP clients can also be configured to leave messages on the server, so exact behaviour depends on client settings.

## 5.3 How SMTP delivery works

The lesson presents this simplified flow:

1. The mail user agent (email client or external program) connects to the sender's SMTP server. This begins the SMTP handshake.
2. The client submits sender and recipient addresses, the message body and attachments.
3. The sender's SMTP server checks whether the sender and recipient domains are the same.
4. The sender's server connects to the recipient's SMTP server and attempts to relay the email.
5. If the recipient's server cannot be reached, the message is placed in an SMTP queue for later delivery attempts.
6. The recipient's SMTP server validates the incoming message and passes it to the recipient's POP or IMAP service.
7. The email becomes available in the recipient's inbox.

### SMTP default port

The lesson identifies **TCP port 25** as the usual SMTP port, particularly for server-to-server mail transfer.

Other commonly encountered email ports include:

| Port | Common use |
|---|---|
| 25/TCP | SMTP relay |
| 587/TCP | Message submission, commonly with STARTTLS |
| 465/TCP | Message submission over implicit TLS |

## 5.4 What runs SMTP?

SMTP server software is available for both Windows Server and Linux. The lesson explicitly states that both operating systems can run SMTP server software.

## 5.5 Task 5 knowledge check — supplied answers

| Question | Answer |
|---|---|
| What does SMTP stand for? | Simple Mail Transfer Protocol |
| What does SMTP handle the sending of? | Emails |
| What is the first step in the SMTP process? | The mail user agent connects to the sender's SMTP server and initiates the SMTP handshake |
| What is the default SMTP port? | 25 |
| Where does SMTP send the email if the recipient's server is unavailable? | An SMTP queue |
| On what server does the email ultimately end up? | The recipient's POP/IMAP server |
| Can a Linux machine run an SMTP server? | Y |
| Can a Windows machine run an SMTP server? | Y |

---

# Task 6 — Enumerating SMTP

## 6.1 Why enumerate an SMTP server?

A poorly configured mail server can reveal useful information about a target. Before attempting further activity, fingerprinting helps identify the mail software and gather information about valid users.

The lesson uses Metasploit modules for two purposes:

- `smtp_version`: identify SMTP service details and version information.
- `smtp_enum`: attempt to identify valid usernames using SMTP responses.

## 6.2 SMTP VRFY and EXPN

SMTP includes commands that can disclose account information:

| Command | Purpose |
|---|---|
| `VRFY` | Requests confirmation that a mailbox or user is valid |
| `EXPN` | Requests expansion of a mailing-list or alias address |

Whether these commands reveal information depends on the SMTP server's configuration. Many administrators restrict or disable them to reduce user enumeration.

The lesson also mentions `RCPT TO` responses as another source of information used by tools such as `smtp-user-enum`.

## 6.3 Start Metasploit

Update package metadata first when appropriate:

```bash
sudo apt update
```

Start the Metasploit Framework console:

```bash
msfconsole
```

Search for the SMTP version scanner:

```text
search smtp_version
```

The full module name supplied by the lesson is:

```text
auxiliary/scanner/smtp/smtp_version
```

Select it:

```text
use auxiliary/scanner/smtp/smtp_version
```

View module options:

```text
options
```

Set the target address:

```text
set RHOSTS <TARGET_IP>
```

Run the module:

```text
run
```

### Key option

| Option | Purpose |
|---|---|
| `RHOSTS` | Specifies the remote host or hosts to scan |

## 6.4 Results from the supplied lesson

The source material included the following answers from its worked lab:

| Item | Supplied result |
|---|---|
| SMTP port | `25` |
| Metasploit launch command | `msfconsole` |
| SMTP version module | `auxiliary/scanner/smtp/smtp_version` |
| Command to view options | `options` |
| Essential target option | `RHOSTS` |
| System mail name | `polosmtp.home` |
| Mail Transfer Agent (MTA) | `Postfix` |

**MTA (Mail Transfer Agent):** Software responsible for transferring email between mail systems. Postfix is an example of an MTA.

## 6.5 Enumerating SMTP users

Search for the enumeration module:

```text
search smtp_enum
```

The full module name supplied by the lesson is:

```text
auxiliary/scanner/smtp/smtp_enum
```

Select it and view its options:

```text
use auxiliary/scanner/smtp/smtp_enum
options
```

The lesson uses the SecLists username shortlist:

```text
/usr/share/wordlists/SecLists/Usernames/top-usernames-shortlist.txt
```

If SecLists is not installed on Kali or Parrot:

```bash
sudo apt install seclists
```

Set the wordlist path and target:

```text
set USER_FILE /usr/share/wordlists/SecLists/Usernames/top-usernames-shortlist.txt
set RHOSTS <TARGET_IP>
```

Run the module in the authorised lab:

```text
run
```

### Important options

| Option | Purpose |
|---|---|
| `USER_FILE` | Path to the username wordlist |
| `RHOSTS` | Target SMTP server address |

The alternative tool mentioned in the lesson is `smtp-user-enum`. It can inspect responses to VRFY, EXPN and RCPT TO when configured and supported by the server.

## 6.6 Task 6 supplied answers

| Question | Answer |
|---|---|
| SMTP port | 25 |
| Command to start Metasploit | `msfconsole` |
| Full SMTP version module name | `auxiliary/scanner/smtp/smtp_version` |
| Command to list module options | `options` |
| Option that specifies the target | `RHOSTS` |
| System mail name | `polosmtp.home` |
| MTA | Postfix |
| Full SMTP enumeration module name | `auxiliary/scanner/smtp/smtp_enum` |
| Option for the username wordlist | `USER_FILE` |
| Other essential option | `RHOSTS` |
| Username returned by the lab | `administrator` |

---

# Task 7 — Exploiting SMTP

## 7.1 What information was discovered?

At the end of SMTP enumeration, the lesson has gathered:

1. A potentially valid user account name.
2. The SMTP server type and operating-system information from enumeration.
3. The SSH service as another exposed service on the target.

The lesson then demonstrates why exposed account names can matter: an attacker may try to authenticate to another service using that username.

**Important distinction:** Discovering a valid username does not mean that the account is compromised. It is an information disclosure that may make later password attacks more targeted.

## 7.2 What is Hydra?

**THC Hydra** is a network login testing tool that supports password authentication checks against multiple services, including SSH.

The lesson describes using a dictionary of candidate passwords. Kali and Parrot commonly provide wordlists under:

```text
/usr/share/wordlists/
```

The lesson's example command is:

```bash
hydra -t 16 -l <USERNAME> -P /usr/share/wordlists/rockyou.txt -vV <TARGET_IP> ssh
```

This is a password-guessing command. Use it only against the explicitly authorised TryHackMe target and within the room's rules.

### Command breakdown

| Option / component | Meaning |
|---|---|
| `hydra` | Starts THC Hydra |
| `-t 16` | Uses 16 parallel task connections |
| `-l <USERNAME>` | Specifies one login name |
| `-P <WORDLIST>` | Specifies a file containing candidate passwords |
| `-vV` | Enables verbose output, including each login attempt |
| `<TARGET_IP>` | Lab target address |
| `ssh` | Selects SSH as the authentication service |

## 7.3 Online password guessing vs offline password cracking

| Online guessing | Offline cracking |
|---|---|
| Attempts authentication against a live service | Tests guesses against a captured password hash |
| Generates network and authentication events | Can occur without contacting the original service |
| May trigger lockouts, rate limits and alerts | Does not directly generate login attempts on the original service |
| Can be detected through server logs | Detection depends on how the hash was obtained and where cracking occurs |

## 7.4 Defensive and SOC perspective

Repeated SSH failures followed by a successful login can indicate password guessing or account compromise. A SOC analyst should correlate:

- Source IP address and geolocation context.
- Target username.
- Number and frequency of failed logins.
- Whether a successful login followed the failures.
- Authentication method used (password or public key).
- Time of login and whether it matches normal user behaviour.
- Activity performed after authentication.

Do not treat every burst of failures as malicious without considering legitimate causes such as a misconfigured service or a user entering an incorrect password.

---

# Task 8 — Understanding MySQL

## 8.1 What is MySQL?

**MySQL** is a relational database management system (RDBMS) that uses Structured Query Language (SQL).

### Database

A database is a persistent, organised collection of structured information.

### RDBMS

A **Relational Database Management System** is software used to create and manage databases whose data is organised into tables. Tables can be related through keys, such as primary keys and foreign keys.

### SQL

**Structured Query Language (SQL)** is the language used to interact with relational databases. It is used to create, read, update and delete data, as well as to manage database structures and permissions.

MySQL is one implementation of an RDBMS. Other examples include PostgreSQL and Microsoft SQL Server.

## 8.2 How MySQL works

MySQL uses a client-server model:

1. The database server stores and manages databases and their tables.
2. A client sends a request using SQL statements.
3. The MySQL server processes the request.
4. The server returns the requested result or an error to the client.

The server handles operations such as creating databases, modifying tables, inserting data and retrieving records.

## 8.3 Where is MySQL used?

MySQL can run on Linux and Windows. It is commonly used as a backend database for websites and applications.

The lesson identifies MySQL as part of the **LAMP stack**:

| Letter | Component |
|---|---|
| L | Linux |
| A | Apache |
| M | MySQL |
| P | PHP |

## 8.4 Security relevance

A database may contain sensitive information such as user records, application data, credentials and business information. Poor access controls or exposed database services can allow unauthorised users to enumerate databases or access data.

For a SOC analyst, useful questions include:

- Is the database service exposed to networks where it is not needed?
- Which accounts are connecting to it?
- Are there unexpected authentication failures?
- Are accounts accessing tables they do not normally use?
- Are there unusual database exports or large data transfers?
- Are database credentials stored insecurely in application files?

---

# Task 10 — Exploiting MySQL: Concepts

The supplied lesson begins Task 10 by stating that the learner already has:

1. MySQL server credentials.
2. The version of MySQL running.
3. The number and names of databases.

The supplied source stops at the introductory terminology on schemas and hashes. It does not include the remaining exploitation procedure or the lab's later questions, so I have documented only the material provided.

## 10.1 Schema

In MySQL, a **schema** is synonymous with a **database**. In MySQL syntax, `SCHEMA` can be used in place of `DATABASE` in statements such as `CREATE SCHEMA` and `CREATE DATABASE`.

This terminology differs across database products. For example, Oracle uses the term schema for objects owned by a particular database user, which is not exactly the same concept as a whole database.

## 10.2 Hashes

A **hash** is the fixed-length output of a cryptographic hash function applied to input data of variable length.

The lesson notes that hashes can be used for indexing, but the focus here is **password hashes**.

A password hash is a stored representation derived from a password. It is not the original plaintext password. A secure password-storage design uses a password-hashing scheme with a unique salt and a deliberately expensive hashing function.

### Hashing vs encryption

| Hashing | Encryption |
|---|---|
| One-way transformation in normal use | Reversible with the correct key |
| Produces a digest | Produces ciphertext |
| Used for integrity checks and password verification | Used to protect confidentiality |
| A password should not be recoverable from its stored hash | Encrypted data can be decrypted with the key |

### Why password hashes matter

If an attacker obtains password hashes from a database, they may attempt offline password guessing. This is why database permissions, credential storage and strong password-hashing configurations are important.

**SOC perspective:** Investigate unusual database queries, access to credential tables, bulk exports and suspicious connections from application or user hosts. A database read event needs context before it can be classified as data theft.

---

# 11. Service comparison and quick revision

| Service | Primary purpose | Common port(s) | Enumeration focus |
|---|---|---|---|
| NFS | Network file sharing | 2049 (commonly) | Export list, client restrictions, mounted contents and file permissions |
| SMTP | Sending and relaying email | 25; 587 and 465 also used | Server banner/version, MTA and user-enumeration exposure |
| SSH | Secure remote administration | 22 (commonly) | Authentication behaviour, user access and exposed keys |
| MySQL | Relational database service | 3306 (commonly) | Version, authentication, database names, privileges and query activity |

Port numbers are common defaults, not proof that a service is running there. Always validate with scan results and service identification.

---

# 12. My Key Takeaways

- I learned that NFS allows a client to mount and access directories shared by a remote server.
- I understood how RPC, the NFS daemon, file handles, UID and GID are involved in file access.
- I practised the NFS enumeration workflow: scan, query exports, mount a share and inspect its contents.
- I learned why private SSH keys must be protected and why file permissions such as `600` matter.
- I understood how root squashing protects NFS exports and why disabling it can create serious privilege-escalation risks when combined with writable shares and SUID files.
- I learned the difference between SMTP, POP3 and IMAP.
- I understood how SMTP relays messages and queues them when a recipient server is unavailable.
- I learned the concepts behind Metasploit's SMTP version and user-enumeration modules.
- I learned how SMTP VRFY and EXPN responses can disclose valid user information when exposed.
- I understood how a discovered username may become useful in a later authentication attack.
- I revised how Hydra uses wordlists for online login testing and how this differs from offline hash cracking.
- I learned the client-server model of MySQL, relational tables, schemas and password hashes.
- I connected these services to SOC monitoring: unexpected mounts, file access, authentication failures, database queries and data transfers can all provide investigation leads.

---

# 13. Self-Assessment Questions

Try answering these without looking back at the notes.

1. What problem does NFS solve?
2. What is an NFS export?
3. What role does RPC play during NFS operations?
4. What information is used by the NFS server when checking file access?
5. Why do we install `nfs-common`?
6. What does `showmount -e` reveal?
7. What is a mount point?
8. Why should private SSH keys have restrictive permissions?
9. What is root squashing?
10. What does the SUID permission bit do?
11. Why can a writable NFS export with unsafe root-mapping settings be dangerous?
12. What is the primary purpose of SMTP?
13. What is the difference between POP3 and IMAP?
14. What happens when a recipient SMTP server is unavailable?
15. What information can an SMTP banner reveal?
16. What do VRFY and EXPN do?
17. What is the difference between `smtp_version` and `smtp_enum`?
18. What do `RHOSTS` and `USER_FILE` specify in the SMTP enumeration module?
19. Why is username enumeration useful to an attacker?
20. How does online password guessing differ from offline password cracking?
21. What is a relational database?
22. What is SQL used for?
23. How does a MySQL client communicate with the server?
24. In MySQL, how are schema and database related?
25. Why are password hashes safer to store than plaintext passwords, and what risks remain if hashes are exposed?

---

# 14. Practical Completion Checklist

- [ ] Started the TryHackMe lab environment.
- [ ] Installed or verified `nfs-common`.
- [ ] Scanned the target with Nmap.
- [ ] Identified the NFS-related service.
- [ ] Enumerated NFS exports using `showmount`.
- [ ] Created a local mount point.
- [ ] Mounted the authorised lab share.
- [ ] Inspected directories and files.
- [ ] Identified and handled SSH key material safely.
- [ ] Understood root squashing and SUID.
- [ ] Reviewed the SMTP delivery process.
- [ ] Identified the SMTP service and MTA.
- [ ] Understood VRFY and EXPN enumeration.
- [ ] Reviewed the Hydra command structure and online guessing risks.
- [ ] Revised MySQL, relational databases, schemas and hashes.
- [ ] Recorded actual lab outputs and unanswered values.

---

# 15. Lab Evidence and Notes

Use this section to retain evidence from my own run. Do not put private keys, real passwords, tokens or other secrets in a public repository.

## NFS

**Nmap command used:**

```text
[Paste command]
```

**Relevant Nmap output:**

```text
[Paste relevant output; redact sensitive details]
```

**showmount output:**

```text
[Paste output]
```

**Share contents:**

```text
[Paste directory listing; do not paste private key contents]
```

**SSH test result:**

```text
[Record success/failure and any non-sensitive observations]
```

## SMTP

**SMTP version module output:**

```text
[Paste relevant output]
```

**SMTP enumeration output:**

```text
[Paste relevant output; redact credentials]
```

## MySQL

**Notes / commands / observations from the remaining task:**

```text
[Continue after completing the remaining room material]
```

---

## 16. References

- TryHackMe — Network Services 2 room (lesson material used for these notes).
- Oracle — [NFS technical overview](https://docs.oracle.com/cd/E19683-01/816-4882/6mb2ipq7l/index.html)
- Ubuntu Packages — [nfs-common](https://packages.ubuntu.com/jammy/nfs-common)
- Arch Linux Wiki — [NFS](https://wiki.archlinux.org/title/NFS)
- TryHackMe — [Further Nmap](https://tryhackme.com/room/furthernmap)
- TryHackMe — [Metasploit module](https://tryhackme.com/module/metasploit)
- SecLists — [GitHub repository](https://github.com/danielmiessler/SecLists)
- THC Hydra — [GitHub repository](https://github.com/vanhauser-thc/thc-hydra)
- MySQL — [SQL execution documentation](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_SQL_EXECUTION.html)

---

**Status:** Study notes prepared from the supplied lesson material. NFS task outputs and the continuation of Task 10 remain to be added from my own lab work.
