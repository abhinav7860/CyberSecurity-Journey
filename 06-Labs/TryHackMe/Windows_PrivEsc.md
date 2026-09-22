# Windows Privilege Escalation --- TryHackMe

**Date Completed:** 22 September 2026\
**Platform:** TryHackMe\
**Room:** Windows PrivEsc\
**Focus:** Windows Privilege Escalation

## Overview

I completed the **Windows Privilege Escalation** room on TryHackMe to
practice identifying and exploiting common Windows privilege-escalation
misconfigurations.

The room provided an intentionally vulnerable Windows machine with
multiple paths from a low-privileged user to **Administrator** or
**SYSTEM**.

The main lesson from this room was that Windows privilege escalation is
often caused by insecure permissions, weak service configurations,
exposed credentials, writable scripts, and dangerous user privileges.

> **Lab note:** All techniques documented here were performed in the
> authorized TryHackMe lab environment.

------------------------------------------------------------------------

## Initial Access

I connected to the Windows machine through RDP using the credentials
provided by the room.

The initial session was running as a normal low-privileged user.

I also created a Windows reverse shell using `msfvenom`, transferred it
to the Windows machine through SMB, and used Netcat on Kali to receive
the connection.

The reverse shell provided command-line access, but **it did not provide
administrator or SYSTEM privileges by itself**.

------------------------------------------------------------------------

# Privilege Escalation Techniques

## 1. Weak Service Permissions --- `daclsvc`

I used `accesschk.exe` to inspect the permissions of the `daclsvc`
service.

The low-privileged user had:

``` text
SERVICE_CHANGE_CONFIG
```

I then checked the service configuration with:

``` cmd
sc qc daclsvc
```

The service was configured to run with SYSTEM privileges.

Because the user could modify the service configuration, I changed its
executable path to the reverse shell and started the service.

### Vulnerability

A low-privileged user could modify the configuration of a service that
executes with SYSTEM privileges.

### Result

The reverse shell ran as:

``` text
NT AUTHORITY\SYSTEM
```

------------------------------------------------------------------------

## 2. Unquoted Service Path --- `unquotedsvc`

I inspected the service using:

``` cmd
sc qc unquotedsvc
```

The executable path contained spaces and was not properly quoted.

I then used `accesschk.exe` to check whether the relevant directory was
writable.

The directory was writable by the `BUILTIN\Users` group.

I placed the reverse shell in the expected executable location and
started the service.

### Vulnerability

The dangerous combination was:

``` text
Unquoted service path
        +
Writable directory
        +
Privileged service
```

This can allow an attacker-controlled executable to be executed with the
service's privileges.

------------------------------------------------------------------------

## 3. Writable Service Registry Configuration --- `regsvc`

I inspected the service:

``` cmd
sc qc regsvc
```

The service was running with SYSTEM privileges.

I then checked its registry permissions using `accesschk.exe`.

The service configuration was writable by the `NT AUTHORITY\INTERACTIVE`
group.

I modified the service's `ImagePath` registry value to point to the
reverse shell and started the service.

### Vulnerability

A low-privileged logged-in user could modify the registry configuration
of a service running as SYSTEM.

------------------------------------------------------------------------

## 4. Writable Service Executable --- `filepermsvc`

I inspected:

``` cmd
sc qc filepermsvc
```

The service ran with SYSTEM privileges.

I then checked the permissions of its executable using `accesschk.exe`.

The executable itself was writable.

I replaced the service executable with the reverse shell and started the
service.

### Vulnerability

A low-privileged user could modify or replace the executable used by a
SYSTEM-level service.

------------------------------------------------------------------------

## 5. AutoRun Registry Configuration

I searched the Windows registry for AutoRun entries:

``` cmd
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```

The executable configured for AutoRun was writable.

I replaced it with the reverse shell.

When a privileged user logged in, Windows automatically executed the
program in that user's security context.

### Vulnerability

The problem was not AutoRun itself. The weakness was that a program
configured to run automatically during login was writable by a
low-privileged user.

------------------------------------------------------------------------

## 6. AlwaysInstallElevated

I checked the following registry locations:

``` cmd
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

``` cmd
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

Both were enabled.

I created an MSI reverse-shell payload and used Windows Installer to
execute it.

### Vulnerability

`AlwaysInstallElevated` was enabled in both the current-user and
machine-wide registry locations, allowing MSI packages to be installed
with elevated privileges.

### Key concept

-   `HKCU` = HKEY_CURRENT_USER --- settings for the current user
-   `HKLM` = HKEY_LOCAL_MACHINE --- system-wide settings

------------------------------------------------------------------------

## 7. Windows AutoLogon Credentials

I searched the registry for stored password-related information:

``` cmd
reg query HKLM /f password /t REG_SZ /s
```

I also inspected the Winlogon configuration:

``` cmd
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon"
```

The room demonstrated how AutoLogon configuration can expose
administrative credentials.

### Vulnerability

Sensitive administrative credentials may be stored in accessible
registry locations and could potentially be recovered by a
lower-privileged user.

------------------------------------------------------------------------

## 8. Saved Credentials --- `cmdkey`

I checked for stored Windows credentials:

``` cmd
cmdkey /list
```

The lab contained saved administrator credentials.

I used `runas` with the saved credentials:

``` cmd
runas /savecred /user:admin C:\PrivEsc\reverse.exe
```

### Vulnerability

Privileged credentials had been saved on the machine in a way that a
lower-privileged user could leverage.

The weakness was the insecure availability of saved privileged
credentials, not the `runas` command itself.

------------------------------------------------------------------------

## 9. SAM and SYSTEM Files

Windows stores local account information in the **SAM (Security Account
Manager)** database.

The lab contained insecurely stored backup copies of the SAM and SYSTEM
files.

I transferred the files to Kali and used `creddump7` to extract the
local account password hashes.

The extracted data included NTLM hashes for local accounts.

### Vulnerability

Sensitive SAM and SYSTEM backup files were stored in a location
accessible to the low-privileged user.

### Security lesson

Protecting these files is important because access to them can expose
password hashes and potentially lead to further account compromise.

------------------------------------------------------------------------

## 10. Pass-the-Hash

After obtaining the administrator's NTLM hash, I learned that the
plaintext password does not always need to be recovered.

Instead, the NTLM hash can sometimes be used directly for
authentication.

This technique is known as:

**Pass-the-Hash (PtH)**

### Concept

``` text
Password
   ↓
NTLM authentication
   ↓
Access
```

versus:

``` text
NTLM hash
   ↓
NTLM authentication
   ↓
Access
```

### Security lesson

A password hash should be treated as sensitive authentication material.
Obtaining the hash can be dangerous even if the original password cannot
be cracked.

------------------------------------------------------------------------

## 11. Writable Scheduled Task Script

The room contained a PowerShell script:

``` text
C:\DevTools\CleanUp.ps1
```

The script was executed by a Scheduled Task running as SYSTEM.

I checked the file permissions using `accesschk.exe` and found that my
user could write to the script.

I appended a command that executed the reverse shell.

When the Scheduled Task executed again, the modified script ran with
SYSTEM privileges.

### Vulnerability

The Scheduled Task itself was not necessarily the problem. The weakness
was that a low-privileged user could modify a script executed by a
privileged task.

### Attack chain

``` text
Writable script
      ↓
SYSTEM Scheduled Task
      ↓
Attacker-controlled code
      ↓
SYSTEM
```

------------------------------------------------------------------------

## 12. Elevated Application --- AdminPaint

The room provided an `AdminPaint` shortcut that launched Paint with
administrative privileges.

I verified the process using:

``` cmd
tasklist /V | findstr mspaint.exe
```

The lab demonstrated that functionality inside the elevated Paint
process could be used to launch `cmd.exe`.

### Security lesson

A privileged application should not expose functionality that allows an
untrusted user to launch another process while inheriting its elevated
security context.

------------------------------------------------------------------------

## 13. Writable Startup Directory

I checked the permissions of the Windows Startup directory:

``` cmd
C:\PrivEsc\accesschk.exe /accepteula -d "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
```

The `BUILTIN\Users` group could write to the directory.

The lab provided a script to create a shortcut pointing to the reverse
shell.

When an administrator logged in, Windows automatically executed the
shortcut.

### Vulnerability

A low-privileged user could place an attacker-controlled program in a
Startup directory used by a privileged user.

### Attack chain

``` text
Writable Startup directory
          ↓
Privileged user logs in
          ↓
Shortcut executes
          ↓
Code runs in privileged context
```

------------------------------------------------------------------------

## 14. RoguePotato --- `SeImpersonatePrivilege`

The final section introduced Windows impersonation privileges.

I first obtained a shell running as:

``` text
NT AUTHORITY\LOCAL SERVICE
```

I checked the account's privileges:

``` cmd
whoami /priv
```

The important privilege was:

``` text
SeImpersonatePrivilege
```

RoguePotato was then used to demonstrate how this privilege can be
abused to obtain a SYSTEM token.

### Concept

``` text
Local Service
      ↓
SeImpersonatePrivilege
      ↓
RoguePotato
      ↓
SYSTEM token
      ↓
SYSTEM process
```

During my lab attempt, RoguePotato successfully obtained a SYSTEM token,
although the final token-duplication stage produced an access-denied
error in the lab environment.

### Security lesson

Powerful impersonation privileges assigned to service accounts can
become privilege-escalation paths.

------------------------------------------------------------------------

## 15. PrintSpoofer --- `SeImpersonatePrivilege`

The room also demonstrated PrintSpoofer as another technique involving
`SeImpersonatePrivilege`.

From the Local Service context, PrintSpoofer was used to attempt to
launch the reverse shell with SYSTEM privileges.

The general concept was:

``` text
Local Service
      ↓
SeImpersonatePrivilege
      ↓
PrintSpoofer
      ↓
SYSTEM
```

### Key takeaway

RoguePotato and PrintSpoofer are different tools, but both demonstrate
why `SeImpersonatePrivilege` deserves attention when enumerating Windows
service accounts.

------------------------------------------------------------------------

# Privilege Escalation Enumeration Tools

The room also introduced several tools that can automate Windows
privilege-escalation enumeration.

## winPEAS

A broad Windows privilege-escalation enumeration tool that checks many
areas of the system for potential weaknesses.

## Seatbelt

A Windows security enumeration tool that gathers information about
users, processes, services, credentials, applications, and other
security-relevant configuration.

## PowerUp

A PowerShell-based tool focused on identifying common Windows
privilege-escalation opportunities.

## SharpUp

A C# tool that performs many PowerUp-style privilege-escalation checks.

### General purpose

These tools help answer:

> **What misconfigurations on this Windows machine could potentially
> allow a low-privileged user to escalate their privileges?**

------------------------------------------------------------------------

# Key Lessons

This room helped me understand that Windows privilege escalation is not
always about finding a single software vulnerability.

A lot of the escalation paths came from **misconfigurations and
excessive permissions**.

The main things I learned were:

-   How Windows service permissions can lead to SYSTEM
-   Why service executable permissions matter
-   How unquoted service paths can become dangerous when combined with
    writable locations
-   How registry permissions can affect service security
-   Why writable scripts used by privileged Scheduled Tasks are
    dangerous
-   How AutoRun and Startup directories can become privilege-escalation
    paths
-   How `AlwaysInstallElevated` can create an insecure MSI installation
    configuration
-   How stored credentials can be abused
-   How SAM and SYSTEM files can expose NTLM hashes
-   Why password hashes can sometimes be used directly through
    Pass-the-Hash
-   Why `SeImpersonatePrivilege` is important during Windows enumeration
-   How tools such as winPEAS, Seatbelt, PowerUp, and SharpUp can
    automate enumeration

------------------------------------------------------------------------

# My Windows Privilege Escalation Checklist

After completing this room, my basic enumeration mindset is:

``` text
Who am I?
   ↓
What privileges do I have?
   ↓
What services are running?
   ↓
Who runs those services?
   ↓
Can I modify their configuration?
   ↓
Can I modify their executable?
   ↓
Are service paths quoted?
   ↓
What Scheduled Tasks exist?
   ↓
Can I modify their scripts/executables?
   ↓
What registry entries are writable?
   ↓
Are credentials exposed?
   ↓
Are SAM/SYSTEM backups accessible?
   ↓
Are privileged Startup/AutoRun locations writable?
   ↓
Do service accounts have dangerous privileges?
```

------------------------------------------------------------------------

# Defensive Perspective

From a defensive and SOC perspective, the same techniques can be viewed
as detection and hardening opportunities.

  -----------------------------------------------------------------------
  Privilege Escalation Path           Defensive Focus
  ----------------------------------- -----------------------------------
  Weak service permissions            Review service ACLs

  Writable service executable         Restrict write access to service
                                      binaries

  Unquoted service path               Properly quote service executable
                                      paths

  Writable service registry           Review registry permissions
  configuration                       

  AutoRun abuse                       Monitor and restrict writable
                                      AutoRun locations

  AlwaysInstallElevated               Disable unnecessary elevated MSI
                                      installation

  Stored credentials                  Avoid unnecessary storage of
                                      privileged credentials

  SAM/SYSTEM exposure                 Protect sensitive registry hives
                                      and backups

  Pass-the-Hash                       Monitor suspicious NTLM
                                      authentication

  Scheduled Task abuse                Audit task permissions and
                                      execution paths

  Startup folder abuse                Restrict write access to privileged
                                      Startup locations

  Potato attacks                      Monitor unusual service-account
                                      process creation
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Conclusion

Completing this room gave me a much better understanding of how Windows
privilege escalation works in practice.

The biggest lesson I took away is that privilege escalation often comes
from **small security weaknesses combining together**:

``` text
Low-privileged user
        ↓
Weak permission / misconfiguration
        ↓
Modify privileged component
        ↓
Privileged process executes attacker-controlled code
        ↓
Administrator / SYSTEM
```

Instead of simply memorizing exploitation commands, I now have a better
process for investigating a Windows system and asking **why a particular
configuration can lead to privilege escalation**.

**Room: Windows PrivEsc --- Completed**

------------------------------------------------------------------------

