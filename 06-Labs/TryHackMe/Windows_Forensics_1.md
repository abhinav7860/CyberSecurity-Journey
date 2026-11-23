# Windows Forensics 1 — TryHackMe Study Playbook

**Study date:** 23 November 2026  
**Platform:** TryHackMe  
**Focus:** Windows Registry, offline hives, data acquisition, system information, user activity, program execution and USB device forensics.

> **Purpose of these notes:** This README turns the room material into a practical revision playbook. I have grouped registry locations by the question they help answer, added simple memory cues, and explained what each artefact can tell an investigator.
>
> **Forensic reminder:** Registry artefacts provide evidence and investigative leads. A single key or timestamp is rarely enough to prove that a user performed an action. Correlate findings with other artefacts, system logs, file metadata and the wider timeline.

---

# 1. Introduction to Windows Forensics

## 1.1 What is computer forensics?

Computer forensics is the process of collecting, preserving, examining and analysing data from computers to understand what happened on a system.

It is part of the wider field of **digital forensics**, which can involve computers, phones, storage devices, networks and other digital systems.

Investigations may be performed for:

- Criminal or civil cases.
- Internal company investigations.
- Incident response.
- Suspected data theft.
- Malware and intrusion investigations.
- Recovering or examining deleted or modified information.

The room introduces the BTK case as an example of how computer evidence can help an investigation. Investigators recovered a deleted Word document from a floppy disk and used metadata and other evidence to help identify the person who sent it.

The important lesson is that even information that appears unimportant or has been deleted may leave traces that can be examined.

## 1.2 What is a forensic artefact?

A **forensic artefact** is a piece of information left behind by activity on a device.

Examples from a Windows computer include:

- Recently opened files.
- Programs that were executed.
- USB devices that were connected.
- User account information.
- Network configurations.
- Application history.
- Registry entries.
- Browser history and downloads.

Windows creates many of these artefacts to remember user preferences and improve the user experience. For example, Windows remembers recently opened documents and previously connected devices. Investigators can use the same information to reconstruct activity.

**Think of forensic artefacts as digital footprints.** One footprint may not tell the whole story, but several connected footprints can help rebuild a timeline.

---

# 2. Windows Registry — The Main Evidence Store

## 2.1 What is the Windows Registry?

The **Windows Registry** is a collection of databases that stores configuration information about:

- The operating system.
- Hardware.
- Installed software.
- Users and their preferences.
- Recently accessed files.
- Programs that have been used.
- Devices connected to the computer.

Forensic investigators examine registry data to understand how a Windows system was configured and what activity may have taken place.

The built-in Windows tool for viewing the live registry is:

```text
regedit.exe
```

To open it, press `Windows + R`, type `regedit.exe`, and press Enter.

## 2.2 Registry keys, values and hives

Understand these three terms first:

| Term | Simple meaning | Analogy |
|---|---|---|
| Registry key | A folder-like container in the Registry | A folder |
| Registry value | A named item containing data inside a key | A file or setting inside a folder |
| Registry hive | A group of keys and values stored in a file on disk | A saved collection of folders and settings |

The Registry Editor displays keys in a tree on the left and the selected key's values on the right.

## 2.3 The five root keys — remember these first

Windows displays five main root keys:

| Root key | Short name | What it contains | Memory cue |
|---|---|---|---|
| `HKEY_CURRENT_USER` | HKCU | Settings for the currently logged-in user | **Current user** |
| `HKEY_USERS` | HKU | All user profiles currently loaded | **Users loaded** |
| `HKEY_LOCAL_MACHINE` | HKLM | Computer-wide configuration applying to users of the machine | **Local machine** |
| `HKEY_CLASSES_ROOT` | HKCR | File associations and class information, presented as a merged view | **File types/classes** |
| `HKEY_CURRENT_CONFIG` | HKCC | Hardware profile used by the computer at startup | **Current hardware config** |

### Understand each root key

**HKCU — HKEY_CURRENT_USER**

Stores configuration for the currently logged-in user. Examples include desktop preferences, folders, colours and Control Panel settings.

**HKU — HKEY_USERS**

Contains the profiles currently loaded on the computer. HKCU is a view of the currently logged-in user's profile under HKU.

**HKLM — HKEY_LOCAL_MACHINE**

Stores configuration related to the computer itself rather than just one user. This includes operating-system, hardware, software and service configuration.

**HKCR — HKEY_CLASSES_ROOT**

Contains file-association and class information, helping Windows determine which application should open a particular file type. It is a merged view of information from:

```text
HKEY_LOCAL_MACHINE\Software\Classes
HKEY_CURRENT_USER\Software\Classes
```

The current user's settings can override the computer-wide defaults.

**HKCC — HKEY_CURRENT_CONFIG**

Contains information about the hardware profile used by the local computer at system startup.

### Quick memory trick

- **CU** = Current User.
- **U** = Users.
- **LM** = Local Machine.
- **CR** = Classes Root.
- **CC** = Current Config.

When investigating a question about one particular user, I should usually look at that user's hive. When investigating computer-wide configuration, I should usually look at the SYSTEM or SOFTWARE hive.

---

# 3. Offline Registry Hives — Where the Evidence Lives

## 3.1 Live registry vs offline registry

On a running Windows system, `regedit.exe` displays the registry in its live, loaded form.

In a forensic investigation, I may receive only a disk image or a copy of the relevant files. In that situation, I need to know where Windows stores the registry hive files on disk.

Most system hives are located here:

```text
C:\Windows\System32\Config\
```

## 3.2 The five important system hives

| Hive file | Normally mounted under | What to remember |
|---|---|---|
| `DEFAULT` | `HKEY_USERS\DEFAULT` | Default user profile settings |
| `SAM` | `HKEY_LOCAL_MACHINE\SAM` | Local accounts and account-related information |
| `SECURITY` | `HKEY_LOCAL_MACHINE\Security` | Local security policy and security-related data |
| `SOFTWARE` | `HKEY_LOCAL_MACHINE\Software` | Installed software, Windows version and system-wide software configuration |
| `SYSTEM` | `HKEY_LOCAL_MACHINE\System` | Services, control sets, hardware and system configuration |

**Memory cue: `D-S-S-S-S`** — Default, SAM, SECURITY, SOFTWARE, SYSTEM.

A quick way to remember their main forensic roles:

- **SAM** → Who are the local users?
- **SYSTEM** → How is the computer configured?
- **SOFTWARE** → What Windows/software information is recorded?
- **SECURITY** → Security configuration.
- **DEFAULT** → Default profile settings.

## 3.3 User-specific registry hives

Each user's profile contains two especially important hives.

For Windows 7 and later, user profiles are commonly stored under:

```text
C:\Users\<username>\
```

| Hive | Location | What it represents |
|---|---|---|
| `NTUSER.DAT` | `C:\Users\<username>\NTUSER.DAT` | User-specific settings; mounted as HKCU when the user logs in |
| `USRCLASS.DAT` | `C:\Users\<username>\AppData\Local\Microsoft\Windows\USRCLASS.DAT` | User-specific class and Shell-related settings; mounted below HKCU\Software\Classes |

Both files are hidden by default.

### Easy memory cue

- **NTUSER.DAT** → Think *user settings*.
- **USRCLASS.DAT** → Think *user shell and classes*.

When the investigation asks what a particular user opened, searched or executed, check that user's profile hives rather than assuming all relevant evidence is in the machine-wide hives.

## 3.4 AmCache hive

Another important registry hive is:

```text
C:\Windows\AppCompat\Programs\Amcache.hve
```

AmCache stores information related to programs and application compatibility. It can contain information such as program paths, installation and execution-related details, deletion-related information and hashes.

This is especially useful when investigating whether a program may have existed or run on the system.

## 3.5 Registry transaction logs

Registry transaction logs record changes associated with a hive. They can contain changes that have not yet been fully written into the main hive file.

They are generally stored alongside the hive and use related filenames, for example:

```text
C:\Windows\System32\Config\SAM.LOG
C:\Windows\System32\Config\SAM.LOG1
C:\Windows\System32\Config\SAM.LOG2
```

There can be more than one transaction log.

**Why should I care?**

If I examine only the main hive and ignore the associated transaction logs, I may miss recent registry changes. A forensic tool that understands the hive and its logs can provide a more complete and up-to-date view.

## 3.6 Registry backups — RegBack

The lesson identifies this location for registry backups:

```text
C:\Windows\System32\Config\RegBack\
```

These files can be useful when investigating whether registry keys were recently changed or removed.

The lesson describes backups being copied to RegBack every ten days. Treat the presence and freshness of these backups as something to verify on the actual Windows version and system being investigated; do not assume a usable backup is always present.

## 3.7 Registry location memory map

| What am I looking for? | First place to remember |
|---|---|
| System configuration | `C:\Windows\System32\Config\SYSTEM` |
| Installed software and Windows details | `C:\Windows\System32\Config\SOFTWARE` |
| Local account information | `C:\Windows\System32\Config\SAM` |
| User's personal settings | `C:\Users\<user>\NTUSER.DAT` |
| User's Shell/class settings | `C:\Users\<user>\AppData\Local\Microsoft\Windows\USRCLASS.DAT` |
| Program execution-related artefacts | `C:\Windows\AppCompat\Programs\Amcache.hve` |
| Recent registry changes | Hive transaction logs (`.LOG`, `.LOG1`, `.LOG2`) |
| Older registry copies | `C:\Windows\System32\Config\RegBack\` |

---

# 4. Data Acquisition — Collect Before Analysing

## 4.1 What is data acquisition?

**Data acquisition** is the process of collecting data from a live system or a forensic image so that it can be examined.

The room recommends examining a copy of the required data rather than directly changing or analysing the original evidence wherever possible.

Some registry hives are protected system files, so ordinary copying through File Explorer may not work. The lesson introduces three tools for acquiring data.

## 4.2 KAPE

**KAPE (Kroll Artifact Parser and Extractor)** is a forensic collection and processing tool.

It can be used to collect Windows artefacts, including registry data. It is primarily command-line based but also provides a graphical interface.

Remember KAPE as:

**KAPE = Collect forensic artefacts efficiently.**

## 4.3 Autopsy

**Autopsy** is a digital forensics platform that can analyse disk images and other data sources.

The lesson describes a workflow:

1. Add the data source.
2. Browse to the files or folders that need to be collected.
3. Right-click the required items.
4. Select **Extract File(s)**.

Remember Autopsy as:

**Autopsy = Examine a case and extract files from a data source.**

## 4.4 FTK Imager

**FTK Imager** can access live drives or mounted disk images and export files.

The lesson discusses two useful methods:

- Browse the source and use **Export files**.
- On a live system, use **Obtain Protected Files** to acquire protected registry hives.

The lesson notes that the Obtain Protected Files method does not collect `Amcache.hve`, so that file may need to be acquired separately.

Remember FTK Imager as:

**FTK Imager = Image, mount and export evidence.**

## 4.5 Tool comparison

| Tool | Main role in this lesson | Easy memory cue |
|---|---|---|
| KAPE | Collect forensic artefacts, including registry data | Collect |
| Autopsy | Examine data sources and extract files | Analyse |
| FTK Imager | Access images/live drives and export protected files | Image and export |

## 4.6 Evidence-handling checklist

Before analysis:

- Record the source of the evidence.
- Note the system, user and acquisition time.
- Preserve the original evidence.
- Work from a forensic copy where possible.
- Record the tool and method used.
- Calculate and document hashes when appropriate.
- Keep transaction logs and related hive files with the main hive.
- Do not modify the original hive files during analysis.

---

# 5. Tools for Exploring Registry Hives

After acquisition, I need a tool that can read offline registry hive files.

## 5.1 Registry Viewer

Registry Viewer provides a graphical interface similar to Windows Registry Editor.

The lesson notes two limitations:

- It loads only one hive at a time.
- It does not take transaction logs into account.

It can still be useful for basic offline registry viewing.

## 5.2 Registry Explorer

**Registry Explorer**, developed by Eric Zimmerman, is the main tool used in this room.

The lesson highlights that it can:

- Load multiple registry hives simultaneously.
- Incorporate transaction-log data.
- Present a cleaner, more current view of registry data.
- Provide bookmarks to important forensic registry locations.

Remember:

**Registry Explorer = Browse and investigate registry hives.**

## 5.3 RegRipper

**RegRipper** takes a registry hive as input and extracts information from important registry keys and values into a text report.

It is available in command-line and graphical forms.

One limitation mentioned in the lesson is that RegRipper does not process transaction logs itself. The suggested workflow is:

1. Load the hive and its transaction logs in Registry Explorer.
2. Make sure the hive view includes the relevant log data.
3. Use the resulting hive for further analysis with RegRipper.

Remember:

**RegRipper = Extract registry findings into a report.**

## 5.4 Tool comparison

| Tool | What it does | Important point |
|---|---|---|
| Registry Viewer | Opens offline registry hives | One hive at a time; no transaction-log processing according to the lesson |
| Registry Explorer | Examines multiple hives and incorporates transaction logs | Main registry analysis tool in this room |
| RegRipper | Extracts useful registry data into a report | Does not process transaction logs itself |

---

# 6. System Information and System Accounts

This task is about establishing the identity and configuration of the computer before interpreting other artefacts.

**Playbook order:** OS → Control Set → Computer name → Time zone → Network → Autoruns/services → Accounts.

## 6.1 OS version

**Question:** Which Windows version and build is represented by the evidence?

Registry location:

```text
SOFTWARE\Microsoft\Windows NT\CurrentVersion
```

Hive file:

```text
SOFTWARE
```

This key contains Windows version information. In Registry Explorer, inspect the values associated with the current Windows installation.

**Memory cue:** `SOFTWARE → Microsoft → Windows NT → CurrentVersion` = Windows version/build.

The exact OS version value was shown in a TryHackMe screenshot, but the value itself was not included in the pasted lesson text. I have left it for my own lab record.

## 6.2 Control Sets

The SYSTEM hive contains **Control Sets**, which hold machine configuration used during startup.

Common examples are:

```text
SYSTEM\ControlSet001
SYSTEM\ControlSet002
```

The lesson explains that:

- `ControlSet001` will often be the Control Set used for booting.
- `ControlSet002` may represent the Last Known Good configuration.
- The exact relationship should be verified using the `Select` key rather than assumed.

### CurrentControlSet

On a live Windows system, Windows provides a convenient alias:

```text
HKLM\SYSTEM\CurrentControlSet
```

To identify which numbered Control Set is currently selected, examine:

```text
SYSTEM\Select\Current
```

To identify the Last Known Good Control Set, examine:

```text
SYSTEM\Select\LastKnownGood
```

**Memory cue:**

- `Current` = Which Control Set is active?
- `LastKnownGood` = Which Control Set is recorded as the last known good one?

This matters because many other forensic registry paths use `CurrentControlSet`. In an offline hive, I must identify the correct numbered Control Set using `SYSTEM\Select`.

## 6.3 Computer name

To identify the computer name:

```text
SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName
```

This helps confirm that the registry data belongs to the expected workstation.

**Memory cue:** `ComputerName` = Name of the machine.

## 6.4 Time zone

To identify the configured time zone:

```text
SYSTEM\CurrentControlSet\Control\TimeZoneInformation
```

Time zone information is essential when constructing a forensic timeline.

Different artefacts may record timestamps in UTC/GMT or local time. Without knowing the system's time zone, events from different sources may appear out of order.

**Memory cue:** `TimeZoneInformation` = How to interpret local timestamps.

## 6.5 Network interfaces

To identify network interface configuration:

```text
SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces
```

Each network interface is represented by a GUID subkey.

The values can contain information such as:

- IP address.
- DHCP-assigned IP address.
- Subnet mask.
- DNS servers.
- Other TCP/IP configuration.

**Memory cue:** `Tcpip → Parameters → Interfaces` = Network configuration currently represented in the registry.

## 6.6 Past networks

To identify networks the computer has connected to, inspect:

```text
SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged
```

and:

```text
SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Managed
```

These keys can contain information about previously connected networks and when they were last connected. The lesson explains that the registry key's last-write time can help identify the most recent connection time represented by the key.

**Memory cue:** `NetworkList → Signatures` = Networks the computer has remembered.

This can help determine whether a workstation has connected to a network that is unusual for the organisation or relevant to the suspected incident.

## 6.7 Autostart programs — Autoruns

Autorun registry keys contain commands or programs configured to run automatically, commonly at user logon or system startup.

The lesson provides these locations:

### User-specific Run keys

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Run
```

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

### Machine-wide Run keys

```text
SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
```

```text
SOFTWARE\Microsoft\Windows\CurrentVersion\policies\Explorer\Run
```

```text
SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```

**Memory cue:** `Run` = Something may execute automatically.

When investigating these keys, record the value name, command/path, user or machine scope, timestamp and whether the referenced file exists.

## 6.8 Services

Service configuration is recorded under:

```text
SYSTEM\CurrentControlSet\Services
```

The lesson highlights the `Start` value.

If `Start` is set to:

```text
0x02
```

the service is configured to start automatically at boot.

**Memory cue:** `Services → Start` = When the service starts.

A service's existence does not automatically mean it is malicious. Look at the service name, image path, account, start type, timestamps and other supporting evidence.

## 6.9 SAM — User accounts

The Security Account Manager (SAM) hive contains local user account information.

Registry location:

```text
SAM\Domains\Account\Users
```

The lesson lists information that may be found here, including:

- Relative Identifier (RID).
- Login count.
- Last login time.
- Last failed login.
- Last password change.
- Password expiry information.
- Password policy-related information.
- Password hint.
- Group membership information.

**Memory cue:** `SAM → Account → Users` = Who has a local account on this Windows machine?

The exact interpretation of some values may require specialised tools and knowledge of the SAM data structures.

## 6.10 System information quick-reference table

| Question | Registry location | Hive |
|---|---|---|
| What Windows version/build is this? | `Microsoft\Windows NT\CurrentVersion` | SOFTWARE |
| Which Control Set is active? | `Select\Current` | SYSTEM |
| What is Last Known Good? | `Select\LastKnownGood` | SYSTEM |
| What is the computer name? | `ControlSet...\Control\ComputerName\ComputerName` | SYSTEM |
| What is the time zone? | `ControlSet...\Control\TimeZoneInformation` | SYSTEM |
| What network interfaces are configured? | `ControlSet...\Services\Tcpip\Parameters\Interfaces` | SYSTEM |
| Which networks were remembered? | `Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures` | SOFTWARE |
| What runs automatically? | `...\CurrentVersion\Run` and `RunOnce` paths | NTUSER.DAT / SOFTWARE |
| What services are configured? | `ControlSet...\Services` | SYSTEM |
| What local accounts exist? | `Domains\Account\Users` | SAM |

---

# 7. Usage or Knowledge of Files and Folders

This task focuses on proving that a user may have known about, opened or interacted with files and folders.

**Playbook order:** Recent files → Office files → ShellBags → Open/Save dialogs → Typed paths and searches.

## 7.1 Recent Files — RecentDocs

Windows maintains a list of recently opened files for each user.

Registry location:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
```

This can show recently accessed documents and other files.

Registry Explorer can arrange the entries by Most Recently Used (MRU) order, with the newest entries near the top.

The key can also contain subkeys by file extension, for example:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.pdf
```

This is useful when the investigation is focused on a particular file type, such as PDF documents.

**Memory cue:** `RecentDocs` = Files recently opened by the user.

## 7.2 Microsoft Office Recent Files

Microsoft Office also maintains information about recently opened documents.

General location:

```text
NTUSER.DAT\Software\Microsoft\Office\<VERSION>\
```

The lesson gives this example:

```text
NTUSER.DAT\Software\Microsoft\Office\15.0\Word
```

Here, `15.0` refers to Office 2013.

For Office 365, the lesson describes a location associated with the user's Live ID:

```text
NTUSER.DAT\Software\Microsoft\Office\<VERSION>\UserMRU\LiveID_####\FileMRU
```

The `FileMRU` data can include the full paths of recently used files.

**Memory cue:** `Office → UserMRU → FileMRU` = Office documents the user recently accessed.

## 7.3 ShellBags

When a user opens a folder, Windows remembers aspects of how that folder was displayed, such as its layout and view preferences.

This information is known as **ShellBags**.

The lesson gives these locations:

```text
USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\Bags
```

```text
USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\BagMRU
```

```text
NTUSER.DAT\Software\Microsoft\Windows\Shell\BagMRU
```

```text
NTUSER.DAT\Software\Microsoft\Windows\Shell\Bags
```

### Bags vs BagMRU

A simple way to remember them:

- **Bags** = Folder view settings.
- **BagMRU** = The order/history structure that helps relate folder entries.

ShellBags can be useful because they may show that a user browsed a folder, even if the folder or its contents are no longer present in the same location.

The lesson introduces **ShellBag Explorer**, another Eric Zimmerman's tool, because it presents ShellBag information in a more understandable format than manually browsing the registry.

**Memory cue:** `ShellBags` = Folders the user has browsed and how Windows remembered their views.

## 7.4 Open/Save and LastVisited Dialog MRUs

When a user opens or saves a file, Windows may remember the locations used in those dialogs.

The lesson identifies two registry locations:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDlMRU
```

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU
```

These can help identify files or locations that appeared in Open and Save dialog activity.

**Memory cue:**

- `OpenSavePIDlMRU` = Places/files shown in Open or Save dialogs.
- `LastVisitedPidlMRU` = Locations last visited through those dialogs.

## 7.5 Windows Explorer address bar and search history

Windows Explorer can remember paths typed into its address bar and search terms entered into its search field.

### Typed paths

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
```

This can show paths manually typed into the Explorer address bar.

### Search terms

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery
```

This can show terms entered into Windows Explorer's search box.

**Memory cue:**

- `TypedPaths` = Where the user typed to navigate.
- `WordWheelQuery` = What the user searched for.

## 7.6 File and folder activity quick-reference

| Investigative question | Registry location | Hive |
|---|---|---|
| What files did the user recently open? | `...\Explorer\RecentDocs` | NTUSER.DAT |
| Which recent PDFs were opened? | `...\Explorer\RecentDocs\.pdf` | NTUSER.DAT |
| What Office files were recently used? | `...\Office\<VERSION>\UserMRU\...\FileMRU` | NTUSER.DAT |
| Which folders may the user have browsed? | `...\Windows\Shell\BagMRU` and `...\Shell\Bags` | USRCLASS.DAT / NTUSER.DAT |
| What files/locations appeared in Open or Save dialogs? | `...\Explorer\ComDlg32\OpenSavePIDlMRU` | NTUSER.DAT |
| Which locations were last visited in dialogs? | `...\Explorer\ComDlg32\LastVisitedPidlMRU` | NTUSER.DAT |
| Which paths were typed in Explorer? | `...\Explorer\TypedPaths` | NTUSER.DAT |
| What did the user search for in Explorer? | `...\Explorer\WordWheelQuery` | NTUSER.DAT |

---

# 8. Evidence of Execution

This task focuses on artefacts that can indicate whether a program was executed.

**Playbook order:** UserAssist → ShimCache → AmCache → BAM/DAM.

## 8.1 UserAssist

Windows tracks certain programs launched through Windows Explorer for user-experience and usage-statistics purposes.

UserAssist can contain information such as:

- Programs launched through the Windows Explorer interface.
- Number of times a program was launched.
- Time-related information associated with execution.

Registry location:

```text
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{GUID}\Count
```

The key is located in the user's NTUSER.DAT hive and is organised under GUID subkeys.

**Important limitation from the lesson:** Programs run through the command line will not appear in UserAssist in the way Explorer-launched applications do.

**Memory cue:** UserAssist = Programs launched by the user through the Windows interface.

## 8.2 ShimCache — Application Compatibility Cache

ShimCache is also known as **AppCompatCache**.

Windows uses application compatibility information to help applications work correctly with the operating system. The cache can also provide forensic information about executable files.

Registry location:

```text
SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache
```

The lesson identifies information such as:

- Executable filename.
- File size.
- Last modified time.

The room uses **AppCompatCache Parser**, an Eric Zimmerman utility, because the raw registry data is not conveniently presented in a human-readable format by Registry Explorer.

Command format from the lesson:

```text
AppCompatCacheParser.exe --csv <OUTPUT_DIRECTORY> -f <SYSTEM_HIVE> -c <CONTROL_SET>
```

| Parameter | Purpose |
|---|---|
| `--csv` | Output location for CSV results |
| `-f` | Path to the SYSTEM hive |
| `-c` | Control Set to parse |

The output can be viewed using EZViewer.

**Important forensic caution:** ShimCache is an application-compatibility artefact. Its presence should not automatically be treated as proof that a program was successfully executed. Interpret it with other execution artefacts and system context.

**Memory cue:** ShimCache = Application compatibility records that can reveal executable traces.

## 8.3 AmCache

AmCache is related to application compatibility and stores additional information about programs.

The hive is located at:

```text
C:\Windows\AppCompat\Programs\Amcache.hve
```

The lesson lists information that may be available, including:

- Program execution path.
- Installation-related information.
- Execution-related information.
- Deletion-related information.
- SHA1 hashes of programs.

The lesson identifies this part of the hive as useful for information about recently executed programs:

```text
Amcache.hve\Root\File\{Volume GUID}\
```

**Memory cue:** AmCache = Application records, paths and hashes.

## 8.4 BAM and DAM

The lesson introduces two Windows components:

- **BAM** — Background Activity Monitor.
- **DAM** — Desktop Activity Moderator.

They are associated with background application activity and power management.

The following SYSTEM hive locations may contain information about programs, their full paths and last execution times:

```text
SYSTEM\CurrentControlSet\Services\bam\UserSettings\{SID}
```

```text
SYSTEM\CurrentControlSet\Services\dam\UserSettings\{SID}
```

`{SID}` represents the relevant user's Security Identifier.

**Memory cue:**

- BAM = Background activity.
- DAM = Desktop activity and power management.

## 8.5 Execution artefact comparison

| Artefact | Hive/location | What the lesson says it can show |
|---|---|---|
| UserAssist | NTUSER.DAT → `Explorer\UserAssist\{GUID}\Count` | Programs launched through Windows Explorer, launch counts and time-related data |
| ShimCache | SYSTEM → `Session Manager\AppCompatCache` | Executable names, sizes and last modified times |
| AmCache | `C:\Windows\AppCompat\Programs\Amcache.hve` | Program paths, installation/execution/deletion-related information and SHA1 hashes |
| BAM | SYSTEM → `Services\bam\UserSettings\{SID}` | Background program activity, paths and last execution information |
| DAM | SYSTEM → `Services\dam\UserSettings\{SID}` | Desktop activity information and last execution details described in the lesson |

### Important interpretation point

No single execution artefact should be treated as perfect proof that a program was run. Each artefact has its own purpose and limitations. Correlate multiple sources, including Prefetch, event logs or other evidence if those are available in the investigation.

---

# 9. External Devices and USB Forensics

This task focuses on identifying removable storage devices connected to the Windows computer.

**Playbook order:** Identify device → Establish first/last/removal time → Match device to volume name.

## 9.1 Why investigate USB devices?

A USB device can be relevant to investigations involving:

- Possible data theft.
- Copying files to removable storage.
- Introduction of malware.
- Unauthorised access to company data.
- Identifying devices used during a suspected incident.

The Registry can preserve information about USB storage devices that have been connected to a Windows machine.

## 9.2 Identify USB devices

The lesson identifies two registry locations:

```text
SYSTEM\CurrentControlSet\Enum\USBSTOR
```

```text
SYSTEM\CurrentControlSet\Enum\USB
```

These keys can contain device-identification information such as:

- Vendor ID.
- Product ID.
- Device version.
- Device-specific information.
- Device serial-related information.

The USBSTOR key is particularly important for USB mass-storage devices.

**Memory cue:** `Enum\USBSTOR` = Which USB storage devices were recognised?

## 9.3 First connection, last connection and removal times

The lesson provides this detailed registry path:

```text
SYSTEM\CurrentControlSet\Enum\USBSTOR\Ven_Prod_Version\USBSerial#\Properties\{83da6326-97a6-4088-9453-a19231573b29}\####
```

The final four-digit value determines which timestamp is represented:

| Value | Meaning |
|---|---|
| `0064` | First connection time |
| `0066` | Last connection time |
| `0067` | Last removal time |

The placeholders in the path represent the device's vendor/product/version information and serial-specific subkey.

**Memory cue:**

- `0064` = First.
- `0066` = Last connected.
- `0067` = Removed.

Registry Explorer can parse and display these timestamps so that I do not have to interpret every value manually.

## 9.4 Identify the USB volume name

To identify the name associated with a connected USB device, the lesson gives:

```text
SOFTWARE\Microsoft\Windows Portable Devices\Devices
```

This information can be correlated with the device identifier/GUID shown in the USB device records.

The aim is to connect:

**Device identity → Device connection times → Volume/device name**

This provides a clearer picture of which removable storage device was connected and when.

## 9.5 USB investigation quick-reference

| Investigative question | Registry location | Hive |
|---|---|---|
| Which USB storage devices were connected? | `...\Enum\USBSTOR` | SYSTEM |
| Which USB devices were enumerated? | `...\Enum\USB` | SYSTEM |
| When was a device first connected? | USBSTOR device path → `0064` | SYSTEM |
| When was it last connected? | USBSTOR device path → `0066` | SYSTEM |
| When was it last removed? | USBSTOR device path → `0067` | SYSTEM |
| What is the device/volume name? | `Microsoft\Windows Portable Devices\Devices` | SOFTWARE |

## 9.6 Building a USB timeline

For each device, record:

1. Vendor and product information.
2. Serial number or unique device identifier, if available.
3. First connection time.
4. Last connection time.
5. Last removal time.
6. Volume or device name.
7. Related user activity and file-access evidence, if available.

A USB connection alone does not prove that data was copied. To support a data-theft conclusion, correlate device timestamps with file-access artefacts, user activity, endpoint telemetry and other evidence.

---

# 10. Windows Forensics — Master Playbook

When I receive a Windows forensic image or registry collection, I can follow this order.

## Step 1 — Identify the system

Start by establishing the system's identity and time context.

| Question | Registry location |
|---|---|
| Windows version/build? | `SOFTWARE\Microsoft\Windows NT\CurrentVersion` |
| Active Control Set? | `SYSTEM\Select\Current` |
| Computer name? | `SYSTEM\ControlSet...\Control\ComputerName\ComputerName` |
| Time zone? | `SYSTEM\ControlSet...\Control\TimeZoneInformation` |
| Network interfaces? | `SYSTEM\ControlSet...\Services\Tcpip\Parameters\Interfaces` |
| Previously connected networks? | `SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures` |

## Step 2 — Identify users and persistence

| Question | Registry location |
|---|---|
| Which local accounts exist? | `SAM\Domains\Account\Users` |
| What programs run at logon? | `NTUSER.DAT\...\Run` and `SOFTWARE\...\Run` |
| What services are configured? | `SYSTEM\ControlSet...\Services` |
| Which services start automatically? | Service subkey's `Start` value |

## Step 3 — Investigate user file and folder activity

| Question | Artefact |
|---|---|
| Recently opened files? | `RecentDocs` |
| Recently used Office documents? | `Office\...\UserMRU\...\FileMRU` |
| Folders browsed? | ShellBags (`BagMRU`, `Bags`) |
| Files/locations shown in dialogs? | `OpenSavePIDlMRU`, `LastVisitedPidlMRU` |
| Paths manually typed? | `TypedPaths` |
| Explorer search terms? | `WordWheelQuery` |

## Step 4 — Investigate program execution

| Question | Artefact |
|---|---|
| Programs launched through Explorer? | UserAssist |
| Application compatibility/executable traces? | ShimCache |
| Program paths and hashes? | AmCache |
| Background application activity? | BAM |
| Desktop activity? | DAM |

## Step 5 — Investigate removable devices

| Question | Artefact |
|---|---|
| Which USB storage devices? | `USBSTOR` |
| First connected? | `0064` |
| Last connected? | `0066` |
| Last removed? | `0067` |
| Volume/device name? | `Windows Portable Devices\Devices` |

## Step 6 — Correlate and report

For every finding:

- Record the source hive and full registry path.
- Record the value name and its data.
- Record relevant key last-write times and interpreted timestamps.
- Record which user or system component the artefact relates to.
- Normalize timestamps to a common time zone.
- Correlate with other artefacts.
- Preserve screenshots or exported results where appropriate.
- Explain what the evidence supports and what it does not prove.

---

# 11. Registry Location Memory Sheet

This is the fast-revision section. Learn the short labels first, then remember the path.

## System identity — SYSTEM and SOFTWARE

| Short label | Full path |
|---|---|
| OS version | `SOFTWARE\Microsoft\Windows NT\CurrentVersion` |
| Active Control Set | `SYSTEM\Select\Current` |
| Last Known Good | `SYSTEM\Select\LastKnownGood` |
| Computer name | `SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName` |
| Time zone | `SYSTEM\CurrentControlSet\Control\TimeZoneInformation` |
| Network interfaces | `SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces` |
| Past networks | `SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged` |
| Past managed networks | `SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Managed` |

## Persistence — Run and Services

| Short label | Full path |
|---|---|
| User Run | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Run` |
| User RunOnce | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\RunOnce` |
| Machine Run | `SOFTWARE\Microsoft\Windows\CurrentVersion\Run` |
| Machine RunOnce | `SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce` |
| Explorer policy Run | `SOFTWARE\Microsoft\Windows\CurrentVersion\policies\Explorer\Run` |
| Services | `SYSTEM\CurrentControlSet\Services` |

## User activity — NTUSER.DAT and USRCLASS.DAT

| Short label | Full path |
|---|---|
| Recent files | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs` |
| Recent PDFs | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.pdf` |
| Office recent files | `NTUSER.DAT\Software\Microsoft\Office\<VERSION>\UserMRU\LiveID_####\FileMRU` |
| ShellBag folders | `USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\BagMRU` |
| ShellBag views | `USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\Bags` |
| Open/Save MRU | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDlMRU` |
| Last visited dialog | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU` |
| Typed Explorer paths | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths` |
| Explorer search history | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery` |
| UserAssist execution | `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{GUID}\Count` |

## Execution — SYSTEM and AmCache

| Short label | Full path |
|---|---|
| ShimCache | `SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache` |
| AmCache file | `C:\Windows\AppCompat\Programs\Amcache.hve` |
| AmCache program records | `Amcache.hve\Root\File\{Volume GUID}\` |
| BAM | `SYSTEM\CurrentControlSet\Services\bam\UserSettings\{SID}` |
| DAM | `SYSTEM\CurrentControlSet\Services\dam\UserSettings\{SID}` |

## USB — SYSTEM and SOFTWARE

| Short label | Full path |
|---|---|
| USB storage devices | `SYSTEM\CurrentControlSet\Enum\USBSTOR` |
| USB devices | `SYSTEM\CurrentControlSet\Enum\USB` |
| First connection | USBSTOR device path → `0064` |
| Last connection | USBSTOR device path → `0066` |
| Last removal | USBSTOR device path → `0067` |
| USB volume/device names | `SOFTWARE\Microsoft\Windows Portable Devices\Devices` |

---

# 12. My Key Takeaways

- I learned that Windows stores many configuration details and user activity records in the Registry.
- I understood the difference between registry keys, values and hives.
- I learned the purpose of the five root keys: HKCU, HKU, HKLM, HKCR and HKCC.
- I identified the main system hives: DEFAULT, SAM, SECURITY, SOFTWARE and SYSTEM.
- I learned where user hives NTUSER.DAT and USRCLASS.DAT are stored.
- I understood why transaction logs and registry backups should be considered during offline hive analysis.
- I learned the role of KAPE, Autopsy and FTK Imager in data acquisition.
- I compared Registry Viewer, Registry Explorer and RegRipper.
- I learned how to locate OS version, Control Set, computer name, time zone and network information.
- I learned where Windows stores Autorun and service configuration.
- I studied RecentDocs, Office FileMRU, ShellBags, Open/Save MRUs, TypedPaths and WordWheelQuery.
- I learned about UserAssist, ShimCache, AmCache, BAM and DAM as execution-related artefacts.
- I learned how USBSTOR and USB registry keys can identify removable devices and their connection times.
- I understood that registry evidence must be correlated with other sources before drawing conclusions.

---

# 13. Self-Assessment Questions

Try answering these without looking back at the notes.

1. What is computer forensics?
2. What is a forensic artefact?
3. What is the difference between a registry key, registry value and registry hive?
4. What information is stored in HKCU?
5. What is the difference between HKCU and HKU?
6. What does HKLM contain?
7. What is the purpose of HKCR?
8. Where are the main system registry hives stored?
9. Which hive contains local account information?
10. What is the purpose of NTUSER.DAT?
11. Where is USRCLASS.DAT stored?
12. What is AmCache?
13. Why should registry transaction logs be collected with the hive?
14. What is the purpose of KAPE?
15. What is the difference between Registry Explorer and RegRipper?
16. Which registry path identifies the Windows version?
17. How do we identify the active Control Set in an offline hive?
18. Where is the computer name stored?
19. Which key contains time zone information?
20. Where can we find previous network signatures?
21. Which registry paths contain Run and RunOnce entries?
22. What does a service `Start` value of `0x02` indicate in the lesson?
23. Where are local user account records found in SAM?
24. What does RecentDocs show?
25. What are ShellBags used for?
26. What is the difference between TypedPaths and WordWheelQuery?
27. What does UserAssist track, and what is its limitation?
28. What is ShimCache designed to support?
29. What additional information can AmCache provide?
30. What are BAM and DAM?
31. Which USB registry values represent first connection, last connection and removal?
32. How can the USB volume name be correlated with device identification?
33. Why is one registry artefact not always sufficient to prove user activity?

---

# 14. Practical Lab Checklist

- [ ] Reviewed the introduction to computer forensics and forensic artefacts.
- [ ] Understood the five Windows Registry root keys.
- [ ] Identified the main system hives.
- [ ] Identified NTUSER.DAT and USRCLASS.DAT.
- [ ] Located AmCache.
- [ ] Understood registry transaction logs and RegBack.
- [ ] Reviewed KAPE, Autopsy and FTK Imager.
- [ ] Compared Registry Viewer, Registry Explorer and RegRipper.
- [ ] Located OS version information.
- [ ] Identified the active Control Set and Last Known Good Control Set.
- [ ] Located the computer name and time zone.
- [ ] Reviewed network interface and past network keys.
- [ ] Reviewed Autorun and service registry keys.
- [ ] Examined SAM user information.
- [ ] Reviewed RecentDocs and Office MRU locations.
- [ ] Examined ShellBags.
- [ ] Reviewed Open/Save MRUs and LastVisited MRUs.
- [ ] Examined TypedPaths and WordWheelQuery.
- [ ] Reviewed UserAssist, ShimCache, AmCache, BAM and DAM.
- [ ] Identified USB devices and connection timestamps.
- [ ] Correlated findings and recorded evidence.

---

# 15. Lab Answer Record

The supplied lesson text refers to screenshots and says to answer questions from Registry Explorer, but it does not include the actual values shown in those screenshots. I have left those fields blank rather than guessing.

| Task | Question / value to identify | My result |
|---|---|---|
| Task 6 | Windows OS version/build | **[Read from CurrentVersion screenshot]** |
| Task 6 | Current Control Set number | **[Read from SYSTEM\Select\Current]** |
| Task 6 | Computer name | **[Read from ComputerName key]** |
| Task 6 | Time zone | **[Read from TimeZoneInformation]** |
| Task 6 | Network interface details requested by the room | **[Read from Interfaces key]** |
| Task 6 | Local account detail requested by the room | **[Read from SAM screenshot]** |
| Task 7 | Most recently used file shown in RecentDocs | **[Read from screenshot]** |
| Task 7 | Folder/activity identified through ShellBags | **[Read from ShellBag Explorer screenshot]** |
| Task 7 | Open/Save MRU answers | **[Read from screenshot]** |
| Task 7 | LastVisited MRU answer | **[Read from screenshot]** |
| Task 8 | Program identified in UserAssist | **[Read from screenshot]** |
| Task 9 | USB vendor/product/device details | **[Read from USBSTOR screenshot]** |
| Task 9 | USB first/last connection and removal details | **[Read from timestamp values]** |
| Task 9 | USB volume name | **[Correlate Portable Devices key with device ID]** |

---

# 16. Quick Revision: If I Only Have One Minute

Remember these five groups:

1. **SYSTEM = Machine configuration.** Computer name, time zone, Control Sets, network interfaces, services and USB device enumeration.
2. **SOFTWARE = Windows and installed-software configuration.** OS version, remembered networks and portable-device names.
3. **SAM = Local accounts.** User and group-related information.
4. **NTUSER.DAT / USRCLASS.DAT = User activity.** Recent files, searches, typed paths, ShellBags, UserAssist and Office MRUs.
5. **AmCache / ShimCache / BAM / DAM = Program activity clues.** Use them together and do not treat any one artefact as conclusive proof of execution.

### The easy playbook

**IDENTIFY → ACQUIRE → EXAMINE → TRACE → CORRELATE**

- **Identify** the system, users, time zone and network.
- **Acquire** the hives and related logs safely.
- **Examine** user activity, execution and device artefacts.
- **Trace** persistence and activity across the relevant locations.
- **Correlate** evidence and build a timeline before reaching a conclusion.

---

## 17. References

- TryHackMe — Windows Forensics 1 (lesson material used for these notes).
- Microsoft — [Windows Registry for advanced users](https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/windows-registry-advanced-users)
- Microsoft — [Registry Hives](https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-hives)
- KAPE — [Kroll Artifact Parser and Extractor](https://www.kroll.com/en/services/cyber-risk/incident-response-litigation-support/kroll-artifact-parser-extractor-kape)
- Autopsy — [Digital Forensics Platform](https://www.autopsy.com/)
- FTK Imager — [Exterro FTK Imager](https://www.exterro.com/ftk-imager)
- Eric Zimmerman — [Forensic tools](https://ericzimmerman.github.io/#!index.md)
- RegRipper — [GitHub repository](https://github.com/keydet89/RegRipper3.0)

---

**Status:** Study playbook prepared from the supplied Windows Forensics 1 lesson text. Screenshot-dependent lab answers are left as fields to complete from my own Registry Explorer and ShellBag Explorer results.
