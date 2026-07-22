# Windows Fundamentals 2 

# Part 1 -- System Configuration (MSConfig), Advanced System Settings & User Account Control (UAC)

## What is MSConfig?

System Configuration (MSConfig) is a Windows utility used primarily for
advanced troubleshooting and diagnosing startup problems. It helps
administrators control how Windows starts and provides quick access to
administrative tools.

> Local administrator privileges are required to open MSConfig.

Open: - Win + R - msconfig

## MSConfig Tabs

### General

Controls startup mode: - Normal Startup - Diagnostic Startup - Selective
Startup

### Boot

Configure Windows boot options such as Safe Mode and boot timeout.

### Services

Displays every Windows service, whether running or stopped. A Windows
service is a background application that performs system tasks.

### Startup

On Windows Server this tab is usually empty. To view startup
applications:

Win + R shell:startup

### Tools

Provides shortcuts to Windows administrative utilities. The Selected
Command field shows the exact command used to launch each tool.

## Advanced System Settings

Used to configure:

-   Performance
-   Virtual Memory (Page File)
-   Startup and Recovery

### Virtual Memory

Windows uses a page file when RAM becomes full.

Performance Settings displays: - Page file location - Initial size -
Maximum size - Automatic management

### Startup and Recovery

Windows can generate crash dump files after BSODs.

Dump types: - Automatic Memory Dump - Kernel Memory Dump - Small Memory
Dump - Complete Memory Dump - None

## User Account Control (UAC)

Four security levels:

1.  Always notify
2.  Notify for apps (Default)
3.  Notify without dimming
4.  Never notify (Not recommended)

Open UAC:

UserAccountControlSettings.exe

## Useful Commands

-   msconfig
-   shell:startup
-   UserAccountControlSettings.exe
-   control.exe
-   control.exe /name Microsoft.Troubleshooting

## Key Takeaways

-   MSConfig is a troubleshooting utility.
-   Windows Server stores startup items in the Startup folder.
-   Page files provide virtual memory.
-   Crash dumps assist BSOD analysis.
-   UAC protects the operating system from unauthorized changes.

## Interview Questions

1.  What is MSConfig?
2.  Explain the three startup modes.
3.  What is a Windows service?
4.  What is a page file?
5.  Why are crash dump files useful?
6.  What are the four UAC levels?


# Part 2 -- Computer Management, Task Scheduler, Event Viewer & Storage

------------------------------------------------------------------------

# Computer Management (compmgmt.msc)

Computer Management is a central console that combines multiple Windows
administration tools into one interface.

It is divided into three sections:

-   System Tools
-   Storage
-   Services and Applications

Open using:

``` text
compmgmt.msc
```

------------------------------------------------------------------------

# System Tools

## Task Scheduler

Task Scheduler automates tasks so Windows can run programs or scripts at
a specific time or when an event occurs.

Tasks can run:

-   At system startup
-   At user logon/logoff
-   On a schedule
-   When triggered by an event

To view tasks:

**Task Scheduler Library**

Example from the room:

-   `npcapwatchdog` runs **at system startup**.

You can create your own automated task using **Create Basic Task**.

------------------------------------------------------------------------

## Event Viewer

Event Viewer records activities that occur on Windows.

It is commonly used for:

-   Troubleshooting
-   Security investigations
-   Application debugging
-   Reviewing system events

The interface contains:

-   Left Pane -- Event log tree
-   Middle Pane -- Event details
-   Right Pane -- Available actions

Important Windows Logs:

-   Application
-   Security
-   Setup
-   System
-   Forwarded Events

------------------------------------------------------------------------

## Shared Folders

Displays resources shared across the network.

Common shares include:

-   C\$
-   ADMIN\$

Other sections:

-   Shares
-   Sessions
-   Open Files

Example hidden shared folder from the lab:

`sh4r3dF0Ld3r`

------------------------------------------------------------------------

## Local Users and Groups

Opens:

``` text
lusrmgr.msc
```

Used to manage:

-   Local users
-   Local groups
-   Permissions

------------------------------------------------------------------------

## Performance Monitor

Command:

``` text
perfmon
```

Used for:

-   Monitoring CPU
-   Memory
-   Disk
-   Network performance

Useful for diagnosing performance bottlenecks.

------------------------------------------------------------------------

## Device Manager

Used to:

-   View hardware
-   Update drivers
-   Disable/Enable devices
-   Troubleshoot hardware issues

------------------------------------------------------------------------

# Storage

## Disk Management

Disk Management allows administrators to manage storage devices.

Common tasks:

-   Initialize new disks
-   Create partitions
-   Extend partitions
-   Shrink partitions
-   Assign drive letters

------------------------------------------------------------------------

# Services and Applications

## Services

Windows services are background applications that start automatically,
manually, or remain disabled.

Common startup types:

-   Automatic
-   Manual
-   Disabled

Viewing service properties shows:

-   Service name
-   Display name
-   Executable path
-   Startup type
-   Status

------------------------------------------------------------------------

## WMI Control

Windows Management Instrumentation (WMI) provides information about
Windows systems and allows administrative automation.

WMIC has been deprecated in modern Windows versions and replaced
primarily by PowerShell.

------------------------------------------------------------------------

# Useful Commands

  Purpose                Command
  ---------------------- ----------------
  Computer Management    `compmgmt.msc`
  Local Users & Groups   `lusrmgr.msc`
  Performance Monitor    `perfmon`

------------------------------------------------------------------------

# Key Takeaways

-   Computer Management combines many administrative tools.
-   Task Scheduler automates recurring or event-based tasks.
-   Event Viewer is essential for troubleshooting and investigations.
-   Shared Folders displays network shares and connected users.
-   Disk Management handles partitions and drives.
-   Windows services run in the background and have configurable startup
    types.
-   WMI enables Windows management and automation.

------------------------------------------------------------------------

# Interview Questions

1.  What is Computer Management?
2.  What is Task Scheduler used for?
3.  What information can Event Viewer provide?
4.  What are hidden administrative shares?
5.  What does Disk Management do?
6.  Explain Automatic, Manual, and Disabled services.
7.  What is WMI?


# Part 3 -- System Information (MSInfo32), Environment Variables & Resource Monitor

------------------------------------------------------------------------

# System Information (MSInfo32)

## What is MSInfo32?

Microsoft System Information (`msinfo32`) collects detailed information
about your computer's hardware, system components, and software
environment. It is commonly used to diagnose system issues and verify
system configuration.

Open using:

``` text
msinfo32.exe
```

------------------------------------------------------------------------

# Main Sections

## 1. System Summary

Provides an overview of the system including:

-   Computer name
-   Operating System
-   BIOS version
-   Processor
-   Installed memory (RAM)

Example from the room:

-   System Name: **THM-WINFUN2**

------------------------------------------------------------------------

## 2. Hardware Resources

Shows low-level hardware resource allocation such as:

-   IRQs
-   DMA channels
-   I/O ports
-   Memory addresses

Primarily useful for advanced troubleshooting.

------------------------------------------------------------------------

## 3. Components

Displays information about installed hardware including:

-   Display adapters
-   Storage devices
-   USB devices
-   Input devices
-   Network adapters

------------------------------------------------------------------------

## 4. Software Environment

Shows software-related information such as:

-   Running tasks
-   Drivers
-   Services
-   Network connections
-   Environment Variables

------------------------------------------------------------------------

# Environment Variables

Environment Variables store configuration values used by Windows and
applications.

Examples include:

-   `%SystemRoot%`
-   `%TEMP%`
-   `%PATH%`
-   `%ComSpec%`

Example from the room:

``` text
ComSpec = %SystemRoot%\\system32\\cmd.exe
```

They help programs locate Windows files and determine important system
paths.

------------------------------------------------------------------------

# Searching in MSInfo32

MSInfo32 includes a search bar that allows you to quickly locate
information.

Example:

-   Select **Components**
-   Search for **IP Address**

------------------------------------------------------------------------

# Resource Monitor (resmon)

## What is Resource Monitor?

Resource Monitor provides detailed real-time information about system
resource usage and is mainly used for advanced troubleshooting.

Open using:

``` text
resmon.exe
```

------------------------------------------------------------------------

# Overview Tab

Displays four major resource categories:

-   CPU
-   Memory
-   Disk
-   Network

Each category also has its own dedicated tab with additional details.

------------------------------------------------------------------------

# CPU

Displays:

-   Running processes
-   CPU utilization
-   Threads
-   Services

Useful for identifying high CPU usage.

------------------------------------------------------------------------

# Memory

Shows:

-   RAM usage
-   Hard faults
-   Memory consumption per process

Useful for detecting memory bottlenecks.

------------------------------------------------------------------------

# Disk

Displays:

-   Disk activity
-   Read/Write speeds
-   Active processes accessing storage

Useful when troubleshooting slow storage.

------------------------------------------------------------------------

# Network

Displays:

-   Network activity
-   TCP connections
-   Listening ports
-   Bandwidth usage

Useful for identifying applications using the network.

------------------------------------------------------------------------

# Real-Time Graphs

The right-hand pane displays live graphs for CPU, Disk, Memory, and
Network usage.

------------------------------------------------------------------------

# Useful Commands

  Purpose              Command
  -------------------- ----------------
  System Information   `msinfo32.exe`
  Resource Monitor     `resmon.exe`

------------------------------------------------------------------------

# Key Takeaways

-   MSInfo32 provides a complete overview of system hardware and
    software.
-   Environment Variables define important operating system paths.
-   Resource Monitor provides detailed live performance data.
-   The CPU, Memory, Disk, and Network tabs help troubleshoot
    performance issues.

------------------------------------------------------------------------

# Interview Questions

1.  What is MSInfo32 used for?
2.  What information is available in System Summary?
3.  What are Environment Variables?
4.  What does the ComSpec variable represent?
5.  What are the four Resource Monitor sections?
6.  When would you use Resource Monitor?


# Part 4 -- Command Prompt (CMD) & Essential Networking Commands

------------------------------------------------------------------------

# Command Prompt (CMD)

The Command Prompt (`cmd.exe`) is the Windows command-line interface.
Before graphical interfaces became common, it was the primary way to
interact with Windows. Even today it is an essential tool for
troubleshooting and system administration.

Open using:

``` text
cmd
```

------------------------------------------------------------------------

# Basic Commands

## hostname

Displays the computer name.

``` cmd
hostname
```

------------------------------------------------------------------------

## whoami

Displays the currently logged-in user.

``` cmd
whoami
```

Useful for confirming which account is executing commands.

------------------------------------------------------------------------

# IP Configuration (ipconfig)

`ipconfig` displays the TCP/IP configuration of the computer.

``` cmd
ipconfig
```

To display complete network information:

``` cmd
ipconfig /all
```

Common information shown:

-   IPv4 Address
-   IPv6 Address
-   Default Gateway
-   DNS Servers
-   MAC Address
-   DHCP Status

------------------------------------------------------------------------

# Getting Help

Most Windows commands support:

``` cmd
command /?
```

Example:

``` cmd
ipconfig /?
```

This displays syntax, parameters and usage information.

------------------------------------------------------------------------

# Clearing the Screen

``` cmd
cls
```

Clears all text from the Command Prompt window.

------------------------------------------------------------------------

# netstat

`netstat` displays network connections and protocol statistics.

``` cmd
netstat
```

Useful options include:

``` cmd
netstat -a
```

Show all active and listening connections.

``` cmd
netstat -e
```

Display Ethernet statistics.

Different switches change the output depending on the troubleshooting
task.

------------------------------------------------------------------------

# net Command

The `net` command manages Windows networking resources and services.

To view available subcommands:

``` cmd
net
```

Unlike many commands, help is accessed with:

``` cmd
net help
```

Example:

``` cmd
net help user
```

Other useful subcommands include:

-   `net localgroup`
-   `net share`
-   `net use`
-   `net session`

------------------------------------------------------------------------

# Useful Commands

  Purpose               Command
  --------------------- -----------------
  Computer Name         `hostname`
  Current User          `whoami`
  IP Configuration      `ipconfig`
  Detailed IP Info      `ipconfig /all`
  Help                  `command /?`
  Clear Screen          `cls`
  Network Connections   `netstat`
  Net Help              `net help`

------------------------------------------------------------------------

# Troubleshooting Workflow

``` text
Identify Current User
        ↓
Check Computer Name
        ↓
Verify Network Configuration
        ↓
Review Active Connections
        ↓
Use net Commands
        ↓
Resolve Network Issue
```

------------------------------------------------------------------------

# Key Takeaways

-   CMD remains an important Windows administration tool.
-   `hostname` identifies the computer.
-   `whoami` identifies the current user.
-   `ipconfig` displays network configuration.
-   `ipconfig /all` provides detailed adapter information.
-   `netstat` displays current network activity.
-   `net` manages Windows networking resources.

------------------------------------------------------------------------

# Interview Questions

1.  What is Command Prompt?
2.  What does `hostname` display?
3.  What is the difference between `ipconfig` and `ipconfig /all`?
4.  How do you display help for a command?
5.  What does `netstat` show?
6.  Why is the `net` command important?
7.  What command clears the Command Prompt screen?


# Part 5 -- Windows Registry, Cheat Sheet & Final Revision

------------------------------------------------------------------------

# Windows Registry

## What is the Windows Registry?

The **Windows Registry** is a hierarchical database that stores
configuration settings used by Windows, installed applications, hardware
devices, and user profiles.

Windows continuously reads information from the Registry while the
operating system is running.

------------------------------------------------------------------------

# What Information Does the Registry Store?

The Registry contains information such as:

-   User profiles
-   Installed applications
-   File associations
-   Folder settings
-   Hardware configuration
-   Device information
-   Network configuration
-   System ports

Because Windows depends heavily on the Registry, incorrect modifications
can cause applications or even Windows itself to stop functioning
properly.

------------------------------------------------------------------------

# Registry Editor

The Registry can be viewed and modified using **Registry Editor**.

Open using:

``` text
regedt32.exe
```

> **Warning:** Only experienced users or administrators should modify
> Registry values. Incorrect changes may make Windows unstable or
> unbootable.

------------------------------------------------------------------------

# Why is the Registry Important?

System administrators and security professionals use the Registry to:

-   Troubleshoot Windows issues
-   Modify system behavior
-   Configure applications
-   Analyze malware persistence
-   Perform digital forensics

Many malware families create Registry entries to automatically execute
whenever Windows starts.

------------------------------------------------------------------------

# Registry Structure

The Registry is organized into hierarchical keys, similar to folders.

Examples of major Registry hives include:

-   HKEY_LOCAL_MACHINE (HKLM)
-   HKEY_CURRENT_USER (HKCU)
-   HKEY_USERS (HKU)
-   HKEY_CLASSES_ROOT (HKCR)
-   HKEY_CURRENT_CONFIG (HKCC)

Each key can contain:

-   Subkeys
-   Values
-   Configuration data

------------------------------------------------------------------------

# Windows Fundamentals 2 Workflow

``` text
MSConfig
      ↓
Advanced System Settings
      ↓
User Account Control
      ↓
Computer Management
      ↓
Task Scheduler
      ↓
Event Viewer
      ↓
Shared Folders
      ↓
Disk Management
      ↓
Services
      ↓
System Information
      ↓
Resource Monitor
      ↓
Command Prompt
      ↓
Windows Registry
```

------------------------------------------------------------------------

# Quick Cheat Sheet

  Utility                Command
  ---------------------- ----------------------------------
  System Configuration   `msconfig`
  Startup Folder         `shell:startup`
  UAC Settings           `UserAccountControlSettings.exe`
  Computer Management    `compmgmt.msc`
  Local Users & Groups   `lusrmgr.msc`
  Performance Monitor    `perfmon`
  System Information     `msinfo32.exe`
  Resource Monitor       `resmon.exe`
  Command Prompt         `cmd`
  Registry Editor        `regedt32.exe`

Useful CMD commands:

``` cmd
hostname
whoami
ipconfig
ipconfig /all
ipconfig /?
netstat
net help
cls
```

------------------------------------------------------------------------

# Common Mistakes

-   Editing the Registry without creating a backup.
-   Disabling important Windows services.
-   Ignoring Event Viewer logs while troubleshooting.
-   Using MSConfig as a startup manager instead of a troubleshooting
    tool.
-   Disabling UAC completely.
-   Forgetting to check Resource Monitor when investigating performance
    issues.

------------------------------------------------------------------------

# Interview Questions

1.  What is the Windows Registry?
2.  Why is the Registry considered critical to Windows?
3.  Which utility opens the Registry Editor?
4.  What are Registry hives?
5.  Why should Registry modifications be made carefully?
6.  Name five Windows administrative tools covered in this room.
7.  What is the purpose of Resource Monitor?
8.  What information does MSInfo32 provide?
9.  What is the purpose of Event Viewer?
10. Why is UAC important?

------------------------------------------------------------------------


