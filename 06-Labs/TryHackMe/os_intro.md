# Operating System Basics - Part 2

**Platform:** TryHackMe  
**Module:** OS introduction 
**Date:** 09 July 2026

---

# Objective

In this section, I learned how users interact with an operating system, the different types of operating systems, where they are used, and why different operating systems exist for different environments.

---

# Operating System Interfaces

There are two primary ways to interact with an operating system.

## 1. Graphical User Interface (GUI)

A GUI allows users to interact with the computer using windows, icons, buttons, and menus instead of typing commands.

Examples:

- Windows Desktop
- Ubuntu Desktop
- macOS Finder

Advantages:

- Beginner friendly
- Easy navigation
- No command knowledge required

Example:

Opening the Downloads folder by clicking on the File Manager.

---

## 2. Command Line Interface (CLI)

The CLI allows users to communicate with the operating system by typing commands.

Examples:

```bash
pwd
ls
cd
mkdir
```

Advantages:

- Faster for experienced users
- More powerful
- Used by system administrators and cybersecurity professionals

Example:

```bash
ls
```

Lists all files and folders in the current directory.

---

# GUI vs CLI

GUI

- Uses icons and windows
- Easy for beginners
- Slower for repetitive tasks

CLI

- Uses commands
- Faster and more flexible
- Requires knowledge of commands

---

# Types of Operating Systems

## Desktop Operating System

Designed for personal computers.

Examples:

- Windows 11
- Ubuntu Desktop
- macOS

Common Uses:

- Browsing
- Programming
- Gaming
- Office work

---

## Server Operating System

Designed to provide services over a network.

Examples:

- Ubuntu Server
- Windows Server
- Red Hat Enterprise Linux

Common Uses:

- Web hosting
- Databases
- File servers
- Cloud infrastructure

---

## Mobile Operating System

Used in smartphones and tablets.

Examples:

- Android
- iOS

Features:

- Touchscreen interface
- Battery optimization
- App sandboxing

---

## Embedded Operating System

Runs on devices designed for a specific purpose.

Examples:

- Routers
- Smart TVs
- IoT devices
- Cars

Examples of Embedded Linux:

- OpenWrt
- Ubuntu Core
- Yocto Project

---

## Virtual and Cloud Operating Systems

Used inside cloud platforms and virtual machines.

Examples:

- Ubuntu LTS
- Amazon Linux
- Rocky Linux
- Alpine Linux

Used for:

- AWS
- Azure
- Google Cloud
- Virtual Machines
- Containers

---

# Popular Operating System Families

## Windows

Desktop:

- Windows 10
- Windows 11

Server:

- Windows Server 2019
- Windows Server 2022
- Windows Server 2025

---

## Linux

Desktop:

- Ubuntu
- Fedora
- Debian

Server:

- Ubuntu Server
- Red Hat
- CentOS
- Debian

Linux is widely used in:

- Cybersecurity
- Servers
- Cloud Computing
- Ethical Hacking

---

## macOS

Apple's operating system for Mac computers.

Examples:

- Sonoma
- Sequoia
- Tahoe

---

## Unix

Enterprise operating systems used by large organizations.

Examples:

- IBM AIX
- Oracle Solaris

---

## Android

Most widely used mobile operating system.

Versions:

- Android 14
- Android 15
- Android 16

---

## iOS

Apple's mobile operating system.

Versions:

- iOS 17
- iOS 18
- iOS 26

---

# Why Are There So Many Operating Systems?

Different devices require different operating systems.

Desktop OS

- User friendly
- Supports many applications

Server OS

- Stable
- Reliable
- High uptime

Mobile OS

- Battery efficient
- Optimized for touch devices

Embedded OS

- Lightweight
- Built for dedicated hardware

Cloud OS

- Easy to deploy
- Optimized for virtualization

No single operating system is perfect for every situation.

---

# Practical Activity

Using the Ubuntu virtual machine provided in the lab, I explored the system information using the **About This Computer** application.

Information gathered:

- Ubuntu MATE Version: **1.26.2**
- Allocated Memory: **1.9 GiB**

---

# Questions Completed

✔ Which OS space has unrestricted hardware access?

**Answer:** Kernel Space

---

✔ Which OS responsibility manages user accounts and permissions?

**Answer:** User Management

---

✔ Ubuntu MATE version?

**Answer:** 1.26.2

---

✔ Memory allocated to the machine?

**Answer:** 1.9 GiB

---

# Key Takeaways

- Operating systems provide two interfaces: GUI and CLI.
- GUI is easier for beginners, while CLI provides more control and efficiency.
- Operating systems are designed for different environments such as desktops, servers, mobile devices, embedded systems, and cloud platforms.
- Linux is one of the most widely used operating systems in cybersecurity because of its flexibility, stability, and powerful command-line tools.
- Understanding different operating systems helps in choosing the right platform for different computing tasks.

---