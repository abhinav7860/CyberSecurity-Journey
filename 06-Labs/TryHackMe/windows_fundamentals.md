# TryHackMe - Windows Basics

**Platform:** TryHackMe  
**Room:** Windows Basics 

---

# Objective

In this room, I learned the fundamentals of the Windows operating system by working through a hands-on lab using **Windows Server 2019**. The room focused on navigating the Windows interface, managing files and applications, exploring system settings, monitoring system performance, and understanding Windows' built-in security features.

Unlike the previous Operating Systems room, which explained OS concepts theoretically, this room allowed me to apply those concepts in a real Windows environment.

---

# What is Microsoft Windows?

Microsoft Windows is the most widely used desktop operating system in the world.

Earlier versions of Windows were built on top of **MS-DOS**, where users interacted with the computer by typing commands.

Windows 1.0 (1985) introduced a Graphical User Interface (GUI), making computers easier to use with windows, icons, menus, and a mouse.

Today, Windows combines both GUI and Command Line tools while providing security, application management, networking, and hardware support.

---

# User Authentication

Before accessing Windows, every user must authenticate themselves.

Authentication verifies the user's identity and determines the permissions they receive after logging in.

### Windows Account Types

### Guest

- Very limited permissions
- Temporary access
- Cannot change system settings

### Standard User

- Everyday user account
- Can run applications
- Cannot make major system changes

### Administrator

- Full control over the computer
- Install software
- Modify system settings
- Create or remove users
- Manage security settings

During this room, I worked with an **Administrator account**, allowing full access to the operating system.

---

# Windows Desktop

After logging in, Windows loads the Desktop, which serves as the main workspace.

The Desktop contains:

- Files
- Folders
- Shortcuts
- Applications

It is the first screen users interact with after authentication.

---

# Taskbar

The Taskbar is located at the bottom of the screen.

It provides quick access to:

- Start Menu
- Search
- Running Applications
- File Explorer
- Notifications
- Network Settings
- Volume Controls
- Date & Time

---

# Start Menu

The Start Menu acts as the central navigation point in Windows.

Using the Start Menu, I can:

- Launch applications
- Search files
- Open Settings
- Shut down or restart the computer
- Access user account options

It is one of the fastest ways to access Windows tools.

---

# Built-in Windows Applications

Windows comes with several useful built-in applications.

Some important ones include:

- File Explorer
- Notepad
- Paint
- Calculator
- Settings
- Task Manager
- Windows Security

These applications are available immediately after installing Windows.

---

# System Information

The **About your PC** section provides information about the computer.

Important information available includes:

- Device Name
- Installed RAM
- Processor
- Windows Version
- Operating System Build
- Device Specifications

Knowing this information helps identify the system during troubleshooting or administration.

---

# File Explorer

File Explorer is Windows' file management application.

It allows users to:

- Browse folders
- Open files
- Create folders
- Copy files
- Move files
- Delete files
- Rename files

Windows stores files using a hierarchical folder structure.

Example:

```
C:\
 └── Users
      └── Administrator
           └── Desktop
                └── TryHatMe Onboarding
```

Understanding file paths is important when navigating the system.

---

# Windows File Paths

Windows uses drive letters.

Example:

```
C:\Users\Administrator\Desktop
```

Components:

- **C:** → Drive
- **Users** → Folder
- **Administrator** → User Folder
- **Desktop** → Desktop Directory

---

# Installing Applications

Applications can be installed in multiple ways.

### Microsoft Store

Used to install trusted applications.

### Installer Files

Downloaded directly from software vendors.

Common installer formats:

```
.exe
.msi
```

During the lab, I installed the **TryHatMeWelcome** application.

---

# Updating Applications

Keeping Windows updated is important for:

- Security patches
- Bug fixes
- Performance improvements
- New features

Updates are managed using:

- Windows Update
- Built-in application updates
- Third-party update mechanisms

---

# Uninstalling Applications

Applications can be removed using:

- Settings
- Control Panel
- Microsoft Store
- Built-in uninstallers

Removing unused software helps reduce attack surface and free disk space.

---

# Windows Settings

Windows Settings is the modern configuration application.

It allows users to configure:

- Display
- Sound
- Personalization
- Accounts
- Network
- Privacy
- Updates
- Accessibility
- Security

Most system configuration tasks can now be performed here.

---

# Control Panel

Control Panel is the older configuration interface.

Although Windows Settings replaces many features, Control Panel is still used for:

- Legacy configurations
- Advanced system settings
- Installed programs
- Network configuration
- Administrative tools

Many enterprise environments still rely on it.

---

# Task Manager

Task Manager helps monitor the system in real time.

Main tabs include:

### Processes

Shows:

- Running applications
- Background processes
- CPU usage
- Memory usage

---

### Performance

Displays:

- CPU utilization
- RAM usage
- Disk activity
- Network activity

---

### Users

Shows:

- Logged-in users
- Resource usage

---

### Details

Displays:

- Process IDs (PID)
- Technical process information

---

### Services

Shows:

- Running Windows services
- Stopped services

Task Manager is one of the first tools used during troubleshooting.

---

# Windows Security

Windows includes built-in security features that help protect the operating system.

Main sections include:

### Virus & Threat Protection

Provides:

- Real-time protection
- Virus scanning
- Malware detection

---

### Firewall & Network Protection

Controls:

- Incoming traffic
- Outgoing traffic
- Network access

---

### App & Browser Control

Protects against:

- Malicious websites
- Unsafe applications
- Harmful downloads

---

### Device Security

Provides hardware-based security protections.

---

# Windows Defender Firewall

Windows Defender Firewall filters network traffic.

It decides whether connections should be:

- Allowed
- Blocked

Firewall Profiles:

### Domain

Used inside organizational networks.

### Private

Used for trusted networks like home.

### Public

Used on public Wi-Fi or unknown networks.

The firewall helps prevent unauthorized access to the system.

---

# Hands-on Activities Completed

During this room I:

- Explored the Windows Desktop
- Opened the Start Menu
- Checked Device Specifications
- Explored File Explorer
- Navigated Windows directories
- Installed an application
- Used Windows Settings
- Opened Control Panel
- Used Task Manager
- Viewed logged-in users
- Performed a custom Windows Security scan
- Explored Windows Defender Firewall

---

# Key Terms Learned

| Term | Description |
|-------|-------------|
| Desktop | Main Windows workspace |
| Taskbar | Quick access bar for applications and notifications |
| Start Menu | Central application launcher |
| File Explorer | File management tool |
| Windows Update | Updates Windows and security features |
| Windows Settings | Modern configuration application |
| Control Panel | Legacy configuration interface |
| Task Manager | Monitors running processes and performance |
| Windows Security | Built-in Windows security dashboard |
| Windows Defender Firewall | Controls network traffic |

---

# Commands / Tools Used

Although this room focused on the GUI, I used several built-in Windows tools:

- About Your PC
- File Explorer
- Windows Settings
- Control Panel
- Task Manager
- Windows Security
- Windows Defender Firewall

---
