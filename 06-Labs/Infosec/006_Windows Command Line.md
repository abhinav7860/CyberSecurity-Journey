# Windows Command Line
**Date:** 09 August 2026
## InfosecLab – Windows Fundamentals

The Windows Command Line provides a set of built-in tools that can be used for file management, system administration, network troubleshooting, process management, and cybersecurity investigations.

For cybersecurity, knowing the Windows command line is important because many enumeration and investigation tasks can be performed directly from `cmd.exe`.

This lesson covers:

- Directory navigation
- Reading files
- Searching text
- Output redirection
- Pipes
- System identification
- User and privilege enumeration
- System information
- Network configuration
- Network connections
- Process enumeration
- Process termination
- Windows service investigation

---

# 1. Listing Directory Contents — `dir`

When Command Prompt is opened, it starts in a default working directory, usually the current user's profile directory.

The `dir` command is used to list files and subdirectories in the current directory.

### Command

```cmd
dir
Example
C:\Users\analyst> dir

 Volume in drive C has no label.
 Directory of C:\Users\analyst

12/25/2025  09:30 PM    <DIR>          .
12/25/2025  09:30 PM    <DIR>          ..
12/25/2025  09:35 PM    <DIR>          Documents
12/25/2025  09:36 PM    <DIR>          Downloads
               0 File(s)              0 bytes

The output provides information such as:

Directory names
File names
File sizes
Modification dates
<DIR> to indicate directories
Linux Comparison

The closest commonly used Linux command is:

ls
2. Changing Directories — cd

The cd command means Change Directory.

It is used to move around the Windows filesystem.

Entering a Directory
cd Documents

Example:

C:\Users\analyst> cd Documents
C:\Users\analyst\Documents>
Moving Up One Directory

Use:

cd ..

Example:

C:\Users\analyst\Documents> cd ..
C:\Users\analyst>

.. represents the parent directory.

Going to the Root of the Current Drive
cd \

Example:

C:\Users\analyst> cd \
C:\>
3. Switching Drive Volumes

Windows organizes storage using drive letters such as:

C:
D:
E:

The cd command alone cannot switch from one drive to another.

To switch drives, enter the drive letter followed by :.

Example
C:\Users\analyst> D:
D:\>

This changes the active drive from C: to D:.

4. Useful Command Prompt Shortcuts
Tab Completion

The Tab key can automatically complete directory and file names.

For example:

cd Doc

Pressing Tab can autocomplete it to:

cd Documents

This saves time and reduces typing mistakes.

Clear the Screen

Use:

cls

This clears the Command Prompt screen.

5. Reading File Contents — type

The type command is used to display the contents of a text file directly in Command Prompt.

Example
type note.txt

Output:

CONFIDENTIAL: Do not share password hashes with unauthorized personnel.

This is useful when quickly checking the contents of text files during administration or investigation.

6. Windows vs Linux File Reading

Linux commonly uses:

cat file.txt

However, cat is not a standard Windows Command Prompt command.

If you run:

cat note.txt

inside normal cmd.exe, Windows will report that the command is not recognized.

PowerShell is different.

PowerShell provides cat as an alias for:

Get-Content

So:

cat note.txt

works in PowerShell because it maps to Get-Content.

7. Searching Text — findstr

Windows Command Prompt provides findstr for searching text.

It is commonly compared to the Linux grep command.

Basic Search
findstr "failed" C:\xampp\apache\logs\error.log

This searches the specified log file for the word:

failed
Recursive Search

The /S option searches the current directory and all subdirectories.

findstr /S "password" *.txt
Case-Insensitive Search

The /I option ignores character case.

findstr /S /I "password" *.txt

This can match:

password
Password
PASSWORD
Important Options
Option	Meaning
/S	Searches the current directory and all subdirectories
/I	Ignores character case
8. Output Redirection

Windows Command Prompt supports output redirection.

This allows command output to be saved into files.

> — Overwrite

The > operator redirects output into a file.

If the file already exists, its contents are overwritten.

Example:

echo hello > note.txt

The resulting file contains:

hello
>> — Append

The >> operator adds output to the end of an existing file instead of overwriting it.

Example:

echo world >> note.txt

The file will now contain:

hello
world
9. Pipes — |

A pipe connects two commands.

The output of the first command becomes the input of the second command.

Example
type error.log | findstr "404"

This does two things:

type error.log displays the log.
findstr "404" searches that output for 404.

Pipes are extremely useful for filtering large amounts of command output.

10. Finding the Machine Name — hostname

The hostname command displays the name of the Windows computer.

Command
hostname
Example
C:\> hostname
DESKTOP-SEC-ANALYST

Knowing the hostname is useful during system identification and network enumeration.

11. Finding the Logged-On User — whoami

The whoami command displays the currently logged-on account.

Command
whoami
Example
C:\> whoami
DESKTOP-SEC-ANALYST\analyst

The result normally follows the format:

ComputerOrDomain\Username
12. Checking Group Memberships — whoami /groups

To display the groups associated with the current account:

whoami /groups

This is important during security enumeration because group membership determines what resources and permissions the account may have.

One important group to look for is:

BUILTIN\Administrators

Membership in administrative groups can provide significantly greater privileges.

13. Checking User Privileges — whoami /priv

Use:

whoami /priv

This displays the security privileges associated with the current account.

Examples include:

SeShutdownPrivilege
SeDebugPrivilege

These privileges can be important during security investigations because they help determine what the current user is allowed to do.

14. Why whoami Is Important in Cybersecurity

When an attacker compromises a Windows account, one of the first things they need to determine is:

Who am I?

The answer affects what they can access.

A basic enumeration sequence could therefore be:

whoami
whoami /groups
whoami /priv

This helps determine:

Current username
Domain or computer context
Group membership
Security privileges
15. Advanced System Enumeration — systeminfo

The systeminfo command displays detailed information about the Windows operating system and hardware.

Command
systeminfo

It can provide information about:

Operating system
OS version
OS build
Processor
Memory
Installed hotfixes
Security patches
System configuration

The output can be very large.

Therefore, findstr can be used to filter it.

Example
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"

Example output:

OS Name:                   Microsoft Windows 11 Pro
OS Version:                10.0.22631 N/A Build 22631

Here, the pipe sends the output of systeminfo into findstr.

16. Checking Network Configuration — ipconfig

The ipconfig command displays the network configuration of Windows network adapters.

Command
ipconfig

Example:

Windows IP Configuration

Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . : localdomain
   Link-local IPv6 Address . . . . . : fe80::d9f:224c:4a08:521f%4
   IPv4 Address. . . . . . . . . . . : 192.168.1.100
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.1.1

Important fields include:

IPv4 Address

Example:

192.168.1.100

This is the local IPv4 address assigned to the machine.

Subnet Mask

Example:

255.255.255.0

This determines the network and host portions of the IPv4 address.

Default Gateway

Example:

192.168.1.1

The default gateway is typically the local router or firewall responsible for forwarding traffic to external networks.

17. Private IP Addresses

Common private IPv4 ranges include:

10.0.0.0/8
172.16.0.0/12
192.168.0.0/16

Examples:

10.10.10.5
172.16.1.20
192.168.1.100

These addresses are commonly used inside home, business, and laboratory networks.

18. Advanced ipconfig — /all

For more detailed network information:

ipconfig /all

This can provide:

Physical MAC address
DHCP information
DNS servers
DHCP lease information
Network adapter information
IP configuration

This is useful when performing network troubleshooting or system enumeration.

19. DHCP — /release and /renew

Windows can release its current DHCP configuration:

ipconfig /release

A new DHCP configuration can then be requested:

ipconfig /renew

This is useful when troubleshooting IP configuration problems.

20. Flushing the DNS Cache

Windows maintains a local DNS resolver cache.

To clear it:

ipconfig /flushdns

This forces Windows to perform new DNS lookups when required instead of relying on existing cached entries.

21. Network Connections — netstat

The netstat command can display network connections and listening ports.

Basic command
netstat

For security investigations, the following command is especially useful:

netstat -ano
Options
Option	Meaning
-a	Displays all active connections and listening ports
-n	Displays addresses and ports numerically
-o	Displays the Process ID (PID) owning each connection
22. Why netstat -ano Is Useful for Security

Suppose a machine is suspected of running malware.

The analyst can run:

netstat -ano

This can reveal:

Local ports
Remote IP addresses
Remote ports
Connection states
Process IDs

The PID can then be matched against running processes using:

tasklist

This creates a useful relationship:

Network Connection
       ↓
      PID
       ↓
Running Process

For example:

External IP
    ↓
TCP Connection
    ↓
PID 4320
    ↓
notepad.exe

This helps investigate which process is responsible for a network connection.

23. Listing Running Processes — tasklist

The tasklist command displays currently running processes.

Command
tasklist

Example:

Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
System Idle Process              0 Services                   0          8 K
System                           4 Services                   0        136 K
svchost.exe                    840 Services                   0     15,340 K
notepad.exe                   4320 Console                    1      8,220 K
24. Process IDs — PID

Every running process has a unique Process ID, commonly called a PID.

Example:

notepad.exe    4320

Here:

Process = notepad.exe
PID     = 4320

The PID is useful because multiple instances of the same application can have different PIDs.

For example:

chrome.exe    2000
chrome.exe    2450
chrome.exe    3100

The process name is the same, but the PIDs are different.

25. Terminating Processes — taskkill

Windows provides taskkill for terminating processes.

Terminate by PID
taskkill /PID 4320

Example:

SUCCESS: Sent termination signal to the process with PID 4320.
Terminate by Process Name

Use /IM, which means Image Name.

taskkill /IM notepad.exe

This can terminate processes matching that executable name.

26. Forcefully Terminating a Process

The /F option forces termination.

taskkill /F /PID 4320

This forces the selected process to close immediately.

The concept is similar to Linux:

kill -9 4320

However, forcefully terminating processes can cause:

Unsaved data loss
Application instability
System problems if a critical process is terminated

Therefore, it should be used carefully.

27. Windows Services and svchost.exe

Windows uses background services for many operating-system functions.

A common process associated with Windows services is:

svchost.exe

svchost.exe is a generic Service Host process.

Multiple Windows services can run inside different instances of svchost.exe.

Because of this, simply seeing:

svchost.exe

does not tell us which service is actually running inside that process.

28. Investigating Services — tasklist /svc

The following command displays services associated with running processes:

tasklist /svc

The output can be filtered using findstr.

tasklist /svc | findstr svchost.exe

Example:

svchost.exe                  840 DcomLaunch, LSM, PlugPlay

This tells us that PID 840 is hosting services such as:

DcomLaunch
LSM
PlugPlay

This is useful when investigating suspicious processes and determining what services they are responsible for.

29. Windows Command-Line Security Enumeration

When performing basic enumeration of a Windows system, the following sequence can provide useful information.

Step 1 — Identify the machine
hostname
Step 2 — Identify the current user
whoami
Step 3 — Check group memberships
whoami /groups
Step 4 — Check privileges
whoami /priv
Step 5 — Identify the operating system
systeminfo
Step 6 — Check network configuration
ipconfig /all
Step 7 — Check network connections
netstat -ano
Step 8 — List running processes
tasklist
Step 9 — Investigate services
tasklist /svc

This provides an initial picture of:

Who am I?
    ↓
What machine am I on?
    ↓
What privileges do I have?
    ↓
What operating system is running?
    ↓
What network am I connected to?
    ↓
What connections are active?
    ↓
What processes are running?
    ↓
What services are running?
30. Windows CMD vs Linux
Task	Windows CMD	Linux
List files	dir	ls
Change directory	cd	cd
Move up directory	cd ..	cd ..
Read file	type	cat
Search text	findstr	grep
Clear terminal	cls	clear
Current user	whoami	whoami
Running processes	tasklist	ps
Terminate process	taskkill	kill
Network configuration	ipconfig	ip
Network connections	netstat -ano	ss / netstat
System information	systeminfo	uname and other tools