# UltraTech — TryHackMe CTF Walkthrough

**Date:** 24 October 2026  
**Platform:** TryHackMe  
**Room:** UltraTech  
**Target used in this lab:** `10.48.160.193`  
**Focus:** Enumeration, API command injection, credential discovery, SSH access, Docker-based privilege escalation

> **Scope and safety:** This walkthrough documents activity performed against the assigned TryHackMe UltraTech target in an authorized training environment. Do not run these techniques against systems you do not own or have explicit permission to test. The private SSH key shown in the lab should be treated as sensitive; this document records only the task-relevant prefix, not the complete key.

---

## 1. Lab objective and overview

The objective of this room was to move from externally accessible services to privileged access on the target. The route used in this run was:

1. Discover services and identify the API listening on port `8081`.
2. Test the API's `ping` endpoint and identify command injection through the `ip` parameter.
3. Execute commands as the web service account `www`.
4. Locate the SQLite database and identify password hashes.
5. Crack the hashes to recover candidate credentials.
6. Use SSH to access the machine as `r00t`.
7. Notice that `r00t` belongs to the `docker` group.
8. Use Docker to mount the host filesystem and enter it with `chroot`.
9. Confirm root-level access and inspect the root user's SSH key for the final task.

The key lesson is that several weaknesses chained together. The API command injection did not directly grant root; it provided a low-privilege foothold. Credential discovery enabled SSH access, and excessive Docker privileges enabled host-level escalation.

---

## 2. Reconnaissance and service discovery

### 2.1 Identify reachable services

The target used during the lab was:

```text
10.48.160.193
```

A typical initial Nmap scan is:

```bash
nmap -sC -sV -oN nmap-initial.txt 10.48.160.193
```

**What each part means:**

- `nmap` launches the network scanner.
- `-sC` runs Nmap's default set of safe-enough discovery scripts. These can reveal service details and common configuration information.
- `-sV` probes discovered open ports to identify the service and version where possible.
- `-oN nmap-initial.txt` saves the output in normal, readable text format so it can be reviewed later.
- `10.48.160.193` is the target address assigned for this lab.

The purpose of this scan is to create an initial map of the exposed services. It does not prove that a service is vulnerable. Each result needs to be followed up with targeted enumeration.

**Finding from this run:** SSH was available on port `22`, and an API service was available on port `8081`.

If you are repeating the room and your target IP differs, use the current IP assigned by TryHackMe rather than copying the old address.

### 2.2 Inspect the API

The API endpoint used in the lab was:

```text
http://10.48.160.193:8081/ping
```

The endpoint accepted an `ip` parameter. A simple benign request would look like:

```bash
curl 'http://10.48.160.193:8081/ping?ip=127.0.0.1'
```

**Explanation:**

- `curl` sends an HTTP request and prints the server's response.
- The URL identifies the API host, port, and `/ping` route.
- `ip=127.0.0.1` supplies the loopback address as the parameter value.
- The request checks how the endpoint responds to ordinary input before testing its handling of unusual input.

A baseline request is useful because it lets you compare normal behavior with the behavior of later test input. It is good practice to establish what the application is supposed to do before deciding that an input-handling issue exists.

---

## 3. API command injection

### 3.1 What the vulnerability means

Command injection occurs when an application incorporates untrusted input into a system-shell command in a way that lets the input change the command's structure. The API appeared to use the supplied IP value as part of a ping command. If the application passes the resulting string to a shell, shell metacharacters or command separators can cause additional instructions to run.

In this lab, the encoded newline `%0A` was used as a separator in the request. The command-execution test used the endpoint's `ip` parameter:

```text
http://10.48.160.193:8081/ping?ip=127.0.0.1%0Aid
```

This is an example of a lab request showing the separator and a harmless identity command. When sending it, the URL's `%0A` represents a line-feed/newline character.

### 3.2 Why the test was useful

The `id` command prints the effective user and group identity of the process running it. That makes it a useful, low-impact way to verify whether command execution occurred and to learn the privilege level of the process.

The output in this lab indicated:

```text
uid=1002(www)
```

This finding established that the API was executing commands as the `www` service account. It did **not** mean that root access had been obtained.

### 3.3 What to record

The important evidence was:

- The API accepted a user-controlled parameter intended to contain an IP address.
- A newline separator caused the input to be interpreted as more than an IP address.
- A system command ran in the context of the API process.
- The resulting account was `www` (`uid=1002`).

This is a useful example of why a command-injection finding should include both the vulnerable input and the observed execution identity. The identity indicates the initial impact and helps plan the next authorized enumeration steps.

### 3.4 Defensive lessons

Developers should avoid passing user-controlled strings through a shell. Where a subprocess is necessary, use an argument array and avoid shell interpretation. Validate the input as an IP address using a dedicated parser, apply least privilege to the service account, and log unexpected input and child-process activity.

---

## 4. Finding the SQLite database and password hashes

### 4.1 Database location

Through the command execution available as `www`, the lab database was found at:

```text
/home/www/api/utech.db.sqlite
```

The database was SQLite, a file-based relational database. SQLite databases can be inspected with the `sqlite3` command-line program if it is installed and accessible.

A general way to inspect a database's table names is:

```bash
sqlite3 /home/www/api/utech.db.sqlite '.tables'
```

**Explanation:**

- `sqlite3` starts the SQLite command-line client.
- The path points to the database file.
- `'.tables'` is a SQLite dot-command that lists tables in the database.
- The single quotes keep the dot-command together as one argument for the client.

To inspect a table's schema, a common SQLite command is:

```bash
sqlite3 /home/www/api/utech.db.sqlite '.schema users'
```

This requests the schema for the `users` table. The schema tells you the table's column names and how it is defined; it does not itself reveal plaintext passwords.

### 4.2 Hashes discovered

The `users` table contained these password-hash values:

| Username | Hash |
|---|---|
| `admin` | `0d0ea5111e3c1def594c1684e3b9be84` |
| `r00t` | `f357a0c52799563c7c7b76c1e7543a32` |

The 32-hex-character appearance was consistent with an MD5 digest, though a hash's length alone is not definitive proof of its algorithm. In the room, these were treated as MD5 hashes for the cracking step.

### 4.3 Hash cracking concepts

A password hash is a one-way output generated from a password. Password cracking does not normally “decrypt” the hash. Instead, a cracking tool tests candidate passwords, hashes each candidate with the suspected algorithm, and checks whether the output matches the stored hash.

For example, a wordlist-based approach with Hashcat for a known MD5 hash uses mode `0`:

```bash
hashcat -m 0 hashes.txt wordlist.txt
```

**Explanation:**

- `hashcat` is a password-recovery tool.
- `-m 0` selects Hashcat's MD5 mode.
- `hashes.txt` contains the hashes to test, typically one hash per line.
- `wordlist.txt` contains candidate passwords.

This is a generic example of the method, not a claim that these exact filenames were used during the session. In the lab, the hashes were cracked and the recovered database credentials were:

| Username | Recovered database password |
|---|---|
| `admin` | `n100906` |
| `r00t` | `mrsheafy` |

A recovered password is a candidate credential for a service, not proof that it is valid everywhere. Services may use different credentials, and password reuse should be verified only within the authorized lab.

### 4.4 Defensive lessons

MD5 is fast and unsuitable for modern password storage because it permits high-speed guessing. Applications should use a password-hashing function designed to slow guessing, such as Argon2id, bcrypt, scrypt, or appropriately configured PBKDF2, with unique salts and suitable parameters. Passwords should also be strong and not reused across services.

---

## 5. SSH access as `r00t`

### 5.1 Connect to SSH

SSH was available on port `22`. In this run, the successful login was:

```bash
ssh r00t@10.48.160.193
```

**Explanation:**

- `ssh` starts an encrypted Secure Shell session.
- `r00t` is the remote account name.
- `@` separates the account name from the host.
- `10.48.160.193` is the target's address.
- Because no custom port was specified, SSH uses its default port, `22`.

The login succeeded with the password `n100906`. This is worth documenting carefully: the database entry for `r00t` had the recovered password `mrsheafy`, but the SSH login that worked in this lab used `n100906`. A credential discovered in one place must be tested against the intended service; it should not be assumed to work universally.

### 5.2 Confirm the account and group memberships

After logging in, the identity was checked:

```bash
id
```

The observed output was:

```text
uid=1001(r00t) gid=1001(r00t) groups=1001(r00t),116(docker)
```

**What `id` tells you:**

- `uid=1001(r00t)` identifies the current user and numeric user ID.
- `gid=1001(r00t)` identifies the user's primary group.
- `groups=...` lists the groups the account belongs to.
- `116(docker)` showed membership in the Docker group.

The username `r00t` can look like “root,” but its numeric UID was `1001`, not `0`. On Linux, UID `0` is the root superuser identity. Therefore, this account was not root yet.

The Docker group membership was the important clue for the next stage.

---

## 6. Docker privilege escalation

### 6.1 Inspect Docker

The local Docker images were listed with:

```bash
docker images
```

This command lists images stored locally in the Docker engine. An image is a template used to create a container; it is not the same thing as a running container.

The lab showed a local image:

```text
bash:latest
```

The running-container list was checked with:

```bash
docker ps
```

`docker ps` displays running containers by default. An empty list means there were no currently running containers; it does not mean Docker is unavailable or that local images are absent.

### 6.2 The escalation command

The command used in the lab was:

```bash
docker run -it --rm -v /:/host bash chroot /host
```

This command is important to understand fully because the privilege escalation came from the Docker configuration and the host filesystem mount—not from a software exploit against Bash.

**Token-by-token explanation:**

- `docker` invokes the Docker command-line client, which communicates with the Docker daemon.
- `run` asks Docker to create and start a new container from an image.
- `-i` keeps standard input open, allowing interactive input.
- `-t` allocates a terminal, which makes an interactive shell usable. Together, `-it` provide an interactive terminal session.
- `--rm` tells Docker to remove the container after it exits. This is convenient for a temporary lab container; it does not undo changes made to mounted host files.
- `-v /:/host` bind-mounts the host's `/` directory into the container at `/host`. The first `/` refers to the host filesystem root; `/host` is the mount location inside the container.
- `bash` names the local image used to create the container. In this room, the `bash:latest` image was available.
- `chroot /host` runs the image's `chroot` command with `/host` as the new apparent root directory. Since `/host` was the host's root filesystem, the process was placed inside that filesystem tree.

### 6.3 Why it gave root-level access

The Docker daemon was accessible to the `r00t` account through its Docker group membership. Docker daemon access is highly privileged. The container was started with the host's entire root filesystem bind-mounted into it.

The container process could therefore access host files through that mount with the permissions provided by the Docker setup. `chroot /host` changed the process's filesystem root to the mounted host root. This produced a shell in the host's filesystem environment.

The resulting prompt was:

```text
root@c8f36cfcfab0:/#
```

The prompt is a visual clue, but the reliable way to verify effective privileges is:

```bash
id
```

A root shell should report UID `0`.

**Important distinction:** `chroot` by itself is not a complete security boundary and does not independently grant privileges. In this case, the critical condition was the privileged Docker access combined with the bind mount of the host root filesystem.

### 6.4 A harmless Docker warning

During the session, a message similar to this appeared:

```text
groups: cannot find name for group ID 11
```

This warning means that the container environment did not have a matching group name for the numeric group ID. It was not the reason the escalation succeeded and did not invalidate the host filesystem access.

### 6.5 Defensive lessons

- Restrict access to the Docker daemon and membership in the `docker` group.
- Treat Docker control as a root-equivalent capability on many conventional installations.
- Consider rootless Docker or other least-privilege container configurations where appropriate.
- Avoid mounting the host's root filesystem into containers unless there is a well-understood, tightly controlled need.
- Monitor for unexpected container creation, sensitive host bind mounts, and Docker daemon activity.
- Review container privileges and mounted paths as part of host hardening.

---

## 7. Root SSH key and final task detail

After reaching the host's root filesystem, the root SSH directory was inspected:

```bash
ls -la /root/.ssh
```

**Explanation:**

- `ls` lists directory entries.
- `-l` uses a detailed listing with permissions, ownership, sizes, and timestamps.
- `-a` includes hidden entries, such as files whose names begin with a dot.
- `/root/.ssh` is the root user's SSH configuration and key directory.

The directory included:

```text
authorized_keys
id_rsa
id_rsa.pub
```

The private key was viewed during the task. The PEM header was:

```text
-----BEGIN RSA PRIVATE KEY-----
```

The Base64-encoded key data began with:

```text
MIIEogIBAA
```

The task asked for the first nine characters of the encoded key data. The answer was:

```text
MIIEogIBA
```

The header and encoded key data are distinct. The header begins with `-----BEGIN`, while the encoded payload begins with `MIIE...`. That distinction explained why the header-based answer was not accepted.

### RSA in brief

RSA is an asymmetric cryptographic algorithm. A key pair has a private key that must remain secret and a public key that can be distributed. SSH can use a public/private key pair for authentication: the server has a public key configured for an account, and the client proves possession of the corresponding private key.

A private key should never be published or copied into an untrusted location. In a real incident, exposure of a root private key should trigger investigation and key rotation. This README intentionally does not include the full private key.

---

## 8. Complete attack chain and lessons

```text
Reconnaissance
    |
    v
API discovered on port 8081
    |
    v
Command injection through /ping?ip=
    |
    v
Command execution as www (UID 1002)
    |
    v
SQLite database discovered
    |
    v
Password hashes recovered and cracked
    |
    v
SSH access as r00t (UID 1001)
    |
    v
Docker group membership identified
    |
    v
Docker container created with host / mounted at /host
    |
    v
chroot /host
    |
    v
Root-level access to the host filesystem
    |
    v
Root SSH key inspected for the final task
```

The room demonstrated a chain of weaknesses rather than one single flaw. The API command injection provided a foothold, weak password storage enabled credential recovery, and Docker daemon access made it possible to cross the privilege boundary from a regular account to root.

---

## 9. Findings summary

| Finding | Evidence | Security impact |
|---|---|---|
| API command injection | Newline separator in the `ip` parameter led to command execution | Remote command execution as the web account |
| Weak password storage | MD5-like hashes in the SQLite `users` table were crackable | Password recovery and possible credential reuse |
| Credential exposure | Database credentials could be tested against SSH | Remote access as `r00t` |
| Excessive Docker privileges | `r00t` belonged to the `docker` group | Potential root-equivalent control of the host |
| Sensitive SSH key exposure | Root private key present under `/root/.ssh` | Potential persistent or future authentication risk if the key is trusted elsewhere |

---

## 10. Review questions

Use these questions to check that the underlying ideas are clear:

1. Why was `%0A` significant in the API request?
2. What did the `id` output tell you about the command-execution context?
3. Why is password cracking different from decrypting a hash?
4. Why did a recovered database password not automatically prove it was the SSH password?
5. What does UID `1001` tell you about the `r00t` account?
6. Why is Docker group membership sensitive?
7. What did `-v /:/host` make available inside the container?
8. Why was `chroot /host` effective in this particular setup?
9. What is the difference between the PEM header and the Base64 key data?
10. Which defensive control would have broken each stage of the attack chain?

---

## 11. Completion

**UltraTech completed on 24 October 2026.**

The main skills practiced were service enumeration, API testing, command-injection validation, SQLite inspection, password-hash analysis, SSH authentication, Linux identity and group enumeration, and Docker-based privilege escalation.

The most important takeaway is to follow evidence at each stage: identify the service, prove the behavior with a low-impact command, record the account context, enumerate only what that context can access, and understand why the next privilege boundary was crossed.
