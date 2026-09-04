# Metasploit: Introduction

**Platform:** TryHackMe  
**Room:** Metasploit: Introduction  
**Topic:** Metasploit Framework, msfconsole and Modules  
**Completion Date:** 4 September 2026

---

## Overview

This room introduced me to **Metasploit**, one of the most widely used exploitation frameworks.

The **Metasploit Framework** is an open-source command-line framework used for tasks such as information gathering, scanning, exploitation, exploit development, vulnerability research, and post-exploitation.

The main focus of this room was learning how to navigate and use `msfconsole`, understand Metasploit modules, configure module options, search for relevant modules, run modules, and manage sessions.

---

# 1. Metasploit Versions

Metasploit has two main versions:

| Version | Description |
|---|---|
| **Metasploit Pro** | Commercial version with a GUI that helps automate and manage tasks |
| **Metasploit Framework** | Open-source version that works mainly from the command line |

This room focuses on the **Metasploit Framework**.

---

# 2. Vulnerability, Exploit and Payload

These three concepts are fundamental.

### Vulnerability

A vulnerability is a design, coding, or logic flaw affecting a target system.

### Exploit

An exploit is code that takes advantage of a vulnerability.

```text
Vulnerability
      ↓
    Exploit
      ↓
Takes advantage of the flaw
```

**Question:** What is the name of the code taking advantage of a flaw on the target system?

**Answer:**
```text
exploit
```

### Payload

A payload is the code that runs on the target system to achieve the attacker's desired result.

```text
Exploit
   ↓
Uses vulnerability
   ↓
Payload
   ↓
Runs on target
```

**Question:** What is the name of the code that runs on the target system to achieve the attacker's goal?

**Answer:**
```text
payload
```

---

# 3. Main Metasploit Module Categories

The main categories covered were:

- **Auxiliary** — supporting modules such as scanners, crawlers and fuzzers
- **Encoders** — encode exploits or payloads; this may sometimes help against signature-based detection
- **Evasion** — modules that attempt to evade security software
- **Exploits** — exploit modules organized by target systems
- **NOPs** — No Operation modules
- **Payloads** — code that runs on the target
- **Post** — modules used during post-exploitation

---

# 4. Payload Types

Metasploit payloads are organized into:

```text
payloads/
├── adapters
├── singles
├── stagers
└── stages
```

### Adapters

Wrap single payloads to convert them into different formats.

### Singles

Self-contained payloads that do not need to download an additional component.

**Question:** What are self-contained payloads called?

**Answer:**
```text
singles
```

### Stagers

Set up a connection channel between Metasploit and the target and can download the remaining stage.

### Stages

The larger payload component downloaded by the stager.

---

# 5. Single vs Staged Payloads

The lesson showed this distinction:

```text
generic/shell_reverse_tcp
```

is an inline/single payload, while:

```text
windows/x64/shell/reverse_tcp
```

is a staged payload.

The naming pattern shown was:

```text
shell_reverse_tcp
      ↓
 underscore
      ↓
    single
```

versus:

```text
shell/reverse_tcp
      ↓
    slash
      ↓
   staged
```

**Question:** Is `windows/x64/pingback_reverse_tcp` among singles or staged payloads?

**Answer:**
```text
singles
```

---

# 6. msfconsole

`msfconsole` is the main command-line interface for Metasploit.

Start it with:

```bash
msfconsole
```

The prompt will look similar to:

```text
msf6 >
```

The version number depends on the installed Metasploit version.

---

# 7. Commands Inside msfconsole

Metasploit supports many Linux commands.

Example:

```text
msf6 > ls
[*] exec: ls
```

A Linux command such as:

```bash
ping -c 1 8.8.8.8
```

can also be executed.

However, `msfconsole` is not exactly the same as a normal shell. For example, normal output redirection does not work in the shown example:

```text
msf6 > help > help.txt
[-] No such command
```

---

# 8. Useful msfconsole Commands

### `help`

Displays help for commands.

```bash
help
```

For a specific command:

```bash
help set
```

### `history`

Shows previously entered commands:

```bash
history
```

### Tab completion

`msfconsole` supports tab completion, which is useful for long commands and module names.

---

# 9. Metasploit Context

Metasploit is managed by **context**.

The normal prompt is:

```text
msf6 >
```

After selecting a module:

```bash
use exploit/windows/smb/ms17_010_eternalblue
```

the prompt changes to:

```text
msf6 exploit(windows/smb/ms17_010_eternalblue) >
```

This tells me which module context I am currently working in.

Settings made with `set` normally belong to the current module context. If I switch modules, those settings do not automatically follow.

---

# 10. Prompt Types

The room introduced five important prompts:

| Prompt | Meaning |
|---|---|
| `root@...:~#` | Regular system command prompt |
| `msf6 >` | Main Metasploit console |
| `msf6 exploit(...) >` | Module context |
| `meterpreter >` | Meterpreter session |
| `C:\Windows\system32>` | Shell on the target system |

---

# 11. Selecting Modules

Use:

```bash
use MODULE
```

Example:

```bash
use exploit/windows/smb/ms17_010_eternalblue
```

The prompt then shows the selected module context.

---

# 12. `show options`

After selecting a module, use:

```bash
show options
```

This displays the parameters available for the module.

Common parameters include:

| Parameter | Meaning |
|---|---|
| `RHOSTS` | Remote host(s), target IP/range |
| `RPORT` | Remote port where the target service runs |
| `PAYLOAD` | Payload used with the exploit |
| `LHOST` | IP address of the attacking/listening machine |
| `LPORT` | Local port used for the connection back |
| `SESSION` | Existing Metasploit session |

Always check `show options` before running a module because some values may be pre-populated and may not match the target.

---

# 13. Setting Parameters

The general syntax is:

```bash
set PARAMETER_NAME VALUE
```

Example:

```bash
set rhosts 10.10.165.39
```

Then verify with:

```bash
show options
```

**Question:** How would you set the LPORT value to 6666?

**Answer:**
```bash
set lport 6666
```

---

# 14. Clearing Parameters

Use:

```bash
unset PARAMETER
```

To clear a payload:

```bash
unset payload
```

To clear all current parameters:

```bash
unset all
```

**Question:** What command would you use to clear a set payload?

**Answer:**
```bash
unset payload
```

---

# 15. Global Parameters

`setg` sets a value globally so it can be used across modules.

Example:

```bash
setg rhosts 10.10.19.23
```

A global value can be cleared with:

```bash
unsetg rhosts
```

**Question:** How would you set the global value for RHOSTS to `10.10.19.23`?

**Answer:**
```bash
setg rhosts 10.10.19.23
```

### `set` vs `setg`

| Command | Scope |
|---|---|
| `set` | Current module |
| `setg` | Global |
| `unset` | Clear current module value |
| `unsetg` | Clear global value |

---

# 16. Leaving a Module

Use:

```bash
back
```

Example:

```text
msf6 exploit(...) > back
msf6 >
```

---

# 17. Module Information

Use:

```bash
info
```

inside a module.

You can also specify the module:

```bash
info exploit/windows/smb/ms17_010_eternalblue
```

`info` can show:

- Module name
- Module path
- Platform
- Architecture
- Privileges
- Rank
- Disclosure date
- Authors
- Targets
- Options
- Description
- References

`help` explains commands, while `info` provides detailed information about a module.

---

# 18. Searching for Modules

The `search` command searches the Metasploit Framework database.

Example:

```bash
search ms17-010
```

You can search using:

- CVE numbers
- Exploit names
- Target systems
- Other keywords

**Question:** How would you search for a module related to Apache?

**Answer:**
```bash
search apache
```

Searches can also use filters.

Example:

```bash
search type:auxiliary telnet
```

This limits results to auxiliary modules related to Telnet.

---

# 19. Exploit Rankings

Metasploit ranks exploits based on reliability.

| Ranking | Description |
|---|---|
| **Excellent** | Very reliable; generally does not crash the service |
| **Great** | Has a default target and can detect the appropriate target or use a version-specific return address after checking |
| **Good** | Has a default target representing the common case |
| **Normal** | Generally reliable but depends on a specific version and cannot reliably auto-detect |
| **Average** | Generally unreliable or difficult to exploit |
| **Low** | Nearly impossible to exploit or below 50% success for common platforms |
| **Manual** | Unstable/difficult to exploit or effectively a DoS; may require specific configuration |

A rank is not a guarantee. A low-ranked exploit may work, while an excellent-ranked exploit may still fail or crash the target.

---

# 20. `show payloads`

Inside a compatible exploit module:

```bash
show payloads
```

lists payloads that can be used with that exploit.

Example:

```text
Compatible Payloads
===================

#   Name
0   generic/custom
1   generic/shell_bind_tcp
2   generic/shell_reverse_tcp
3   windows/x64/exec
```

---

# 21. `check`

Some modules support:

```bash
check
```

This checks whether the target system is vulnerable without exploiting it.

---

# 22. Running Modules

Once the required parameters are set, a module can be launched with:

```bash
exploit
```

Metasploit also supports:

```bash
run
```

`run` is an alias for `exploit`.

The `-z` option can background the session as soon as it opens:

```bash
exploit -z
```

**Question:** What command do you use to proceed with the exploitation phase?

**Answer:**
```bash
exploit
```

---

# 23. Sessions

After successful exploitation, a **session** may be created.

A session is the communication channel established between Metasploit and the target.

```text
Successful exploitation
          ↓
       Session
          ↓
Communication with target
```

### Backgrounding a session

From Meterpreter:

```bash
background
```

`CTRL+Z` can also be used.

### List sessions

```bash
sessions
```

### Interact with a session

```bash
sessions -i 2
```

where `2` is the session ID.

---

# 24. Complete Metasploit Workflow

```text
Start
  ↓
msfconsole
  ↓
Search
  ↓
search <keyword>
  ↓
Select module
  ↓
use <module>
  ↓
Inspect
  ├── info
  └── show options
  ↓
Configure
  ├── set
  └── setg
  ↓
Verify
  ↓
check (if supported)
  ↓
Run
  ├── exploit
  └── run
  ↓
Session
  ↓
sessions
  ↓
sessions -i <ID>
```

---

# 25. Questions & Answers

### What is the name of the code taking advantage of a flaw on the target system?

```text
exploit
```

### What is the name of the code that runs on the target system to achieve the attacker's goal?

```text
payload
```

### What are self-contained payloads called?

```text
singles
```

### Is `windows/x64/pingback_reverse_tcp` among singles or staged payloads?

```text
singles
```

### How would you search for a module related to Apache?

```bash
search apache
```

### Who provided the `auxiliary/scanner/ssh/ssh_login` module?

```text
todb
```

The module information also lists `RageLtMan` as a provider.

### How would you set the LPORT value to 6666?

```bash
set lport 6666
```

### How would you set the global value for RHOSTS to `10.10.19.23`?

```bash
setg rhosts 10.10.19.23
```

### What command would you use to clear a set payload?

```bash
unset payload
```

### What command do you use to proceed with the exploitation phase?

```bash
exploit
```

---

# What I Learned

This room gave me a foundation in the Metasploit Framework and its command-line workflow.

I learned that:

- `msfconsole` is the main Metasploit command-line interface.
- A vulnerability is a flaw in a target.
- An exploit takes advantage of that flaw.
- A payload runs on the target to achieve the desired result.
- Metasploit contains auxiliary, exploit, payload, encoder, evasion, NOP and post modules.
- Self-contained payloads are called **singles**.
- Stagers establish a connection and stages provide the larger payload component.
- `use` selects a module.
- `show options` displays module parameters.
- `set` configures values for the current module.
- `setg` configures global values.
- `unset` and `unset all` clear module settings.
- `back` leaves a module context.
- `info` provides detailed module information.
- `search` finds relevant modules.
- Exploit rankings describe reliability but do not guarantee success.
- `show payloads` displays compatible payloads.
- `check` can test whether a target is vulnerable when supported.
- `exploit` and `run` can execute a module.
- Successful exploitation can create a session.
- `sessions` lists sessions and `sessions -i <ID>` interacts with one.

The basic workflow I want to remember is:

```text
Search → Select → Inspect → Configure → Verify → Run → Session
```

---

# Summary

This room introduced the structure of Metasploit and taught me how to work with its command-line interface.

The most important relationship is:

```text
Vulnerability
      ↓
    Exploit
      ↓
    Payload
      ↓
     Target
      ↓
    Session
```

I now have a basic understanding of how Metasploit modules are searched for, selected, configured and executed in a controlled penetration-testing environment.

---

