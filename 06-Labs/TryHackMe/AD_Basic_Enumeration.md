# Active Directory (AD) Basic Enumeration -- Complete Study Notes

> **Room:** TryHackMe -- Active Directory Basic Enumeration\
> **Purpose:** Personal study notes for revision and GitHub
> documentation.\
> **Goal:** Understand Active Directory Enumeration from scratch and
> learn how to enumerate an AD environment without credentials.

------------------------------------------------------------------------

# Table of Contents

-   Introduction
-   Learning Objectives
-   What is Active Directory?
-   Why Enumeration is Important
-   Active Directory Components
-   Domain Controller
-   Authentication Process
-   Enumeration Methodology
-   Host Discovery
-   Network Discovery Tools
-   Port Scanning
-   Understanding Active Directory Ports
-   Nmap Deep Dive

------------------------------------------------------------------------

# Introduction

When performing an internal penetration test, the attacker normally
starts with almost nothing.

Most organizations provide:

-   VPN access
-   Target subnet
-   Scope

Example:

``` text
10.211.11.0/24
```

But they **do not provide credentials**.

Therefore the first objective is **Enumeration**.

Enumeration means collecting as much information as possible without
attacking the target.

Think of enumeration like gathering intelligence before a military
operation.

The more information collected---users, groups, computers, operating
systems, services, shares, and policies---the easier later attacks
become.

------------------------------------------------------------------------

# Learning Objectives

During this room we learn how to:

-   Discover hosts
-   Identify Domain Controllers
-   Enumerate SMB
-   Enumerate LDAP
-   Enumerate RPC
-   Discover domain users
-   Verify usernames
-   Enumerate password policy
-   Perform password spraying
-   Obtain valid credentials

------------------------------------------------------------------------

# What is Active Directory?

Active Directory (AD) is Microsoft's directory service.

Think of AD as a giant database that stores every object inside an
organization.

Examples:

-   Users
-   Computers
-   Printers
-   Groups
-   Servers
-   Policies
-   Shared folders

Whenever someone logs into Windows inside a company, Active Directory is
usually responsible for authenticating that user.

Without Active Directory, an administrator would have to manage
thousands of computers individually.

Instead, everything is managed from one central location.

------------------------------------------------------------------------

# Real World Example

Suppose a company has:

-   5000 Employees
-   8000 Computers
-   300 Servers
-   100 Printers

Without Active Directory, every computer would have its own users,
passwords, and permissions.

Active Directory stores everything centrally.

------------------------------------------------------------------------

# Active Directory Components

## Domain

A Domain is a logical collection of objects.

Example:

``` text
tryhackme.loc
```

Inside it we may have Users, Groups, Computers, Servers, Printers and
Policies.

## Domain Controller (DC)

The Domain Controller is the most important server inside Active
Directory.

Responsibilities:

-   Authentication
-   Authorization
-   User Management
-   Group Management
-   Password Storage
-   Kerberos
-   LDAP
-   DNS

If the Domain Controller goes down, users cannot log in.

## Organizational Units (OU)

OUs organize objects into departments such as IT, HR, Finance and
Marketing.

## Users

Examples:

-   john.smith
-   administrator
-   guest

## Groups

Examples:

-   Domain Users
-   Domain Admins
-   Enterprise Admins
-   Remote Desktop Users

## Computers

Computer accounts typically end with a `$`, for example:

-   DC\$
-   WRK\$
-   FILESERVER\$

------------------------------------------------------------------------

# Active Directory Authentication

Kerberos is the primary authentication protocol.

Workflow:

``` text
User
 ↓
Username & Password
 ↓
Domain Controller
 ↓
Kerberos Verification
 ↓
Ticket Issued
 ↓
Access Granted
```

------------------------------------------------------------------------

# Why Enumeration Matters

Enumeration is reconnaissance.

The goal is to understand the environment before attempting
exploitation.

The better the information gathered, the more targeted and efficient
later attacks become.

------------------------------------------------------------------------

# Enumeration Methodology

``` text
VPN
 ↓
Host Discovery
 ↓
Find Live Hosts
 ↓
Port Scan
 ↓
Find Domain Controller
 ↓
Enumerate SMB
 ↓
Enumerate LDAP
 ↓
Enumerate RPC
 ↓
Collect Users
 ↓
Verify Users
 ↓
Password Policy
 ↓
Password Spray
 ↓
Valid Credentials
```

------------------------------------------------------------------------

# Host Discovery

Before scanning ports, determine which hosts are online.

## ICMP

Most host discovery relies on ICMP Echo Requests (ping).

## Using fping

``` bash
fping -agq 10.211.11.0/24
```

Options:

-   `-a` Show alive hosts
-   `-g` Generate targets from subnet
-   `-q` Quiet mode

Example output:

``` text
10.211.11.1
10.211.11.10
10.211.11.20
10.211.11.250
```

Store live systems in a file:

``` text
hosts.txt
10.211.11.10
10.211.11.20
```

## Host Discovery with Nmap

``` bash
nmap -sn 10.211.11.0/24
```

`-sn` performs host discovery only and skips port scanning.

------------------------------------------------------------------------

# Port Scanning

After identifying live systems, identify services and the Domain
Controller.

Common AD Ports:

    Port Service                    Purpose
  ------ -------------------------- ------------------------
      88 Kerberos                   Authentication
     135 RPC                        Remote Procedure Calls
     139 NetBIOS                    Legacy SMB
     389 LDAP                       Directory Services
     445 SMB                        File Sharing
     464 Kerberos Password Change   Password Management
     636 LDAPS                      Encrypted LDAP

A Domain Controller commonly exposes ports 88, 389 and 445 together.

## Nmap Service Detection

``` bash
nmap -p 88,135,139,389,445,636 -sV -sC -iL hosts.txt
```

Explanation:

-   `-p` Scan selected ports
-   `-sV` Detect service versions
-   `-sC` Run default NSE scripts
-   `-iL` Read targets from a file

Using `-sV` helps identify exact services and operating systems.

Using `-sC` performs safe default enumeration scripts that often reveal
additional information.

------------------------------------------------------------------------

**========== CONTINUE TO PART 2 (SMB Enumeration) ==========**
# Active Directory (AD) Basic Enumeration -- Complete Study Notes

# Part 2 -- SMB Enumeration

------------------------------------------------------------------------

# SMB (Server Message Block)

## What is SMB?

Server Message Block (SMB) is Microsoft's network file sharing protocol.

It allows systems on a network to:

-   Share files
-   Share folders
-   Share printers
-   Access remote resources
-   Perform remote administration

SMB is one of the most important services to enumerate during an Active
Directory assessment because misconfigured shares often expose sensitive
information.

------------------------------------------------------------------------

# Why SMB Enumeration Matters

SMB shares frequently contain:

-   Configuration files
-   Backup files
-   Passwords
-   Scripts
-   Software installers
-   Internal documentation
-   User data

Even without credentials, some environments expose anonymous shares that
can provide an attacker with an initial foothold.

------------------------------------------------------------------------

# Important SMB Ports

    Port Description
  ------ --------------------------------------
     139 NetBIOS Session Service (legacy SMB)
     445 Direct SMB over TCP (modern SMB)

------------------------------------------------------------------------

# Discovering SMB

Use Nmap to identify SMB services:

``` bash
nmap -p 88,135,139,389,445,636 -sV -sC TARGET_IP
```

Typical output:

``` text
445/tcp open microsoft-ds Windows Server 2019 Datacenter
```

The presence of ports 139 and 445 generally indicates SMB is available.

------------------------------------------------------------------------

# Listing SMB Shares

The first task is to determine which shares are available.

``` bash
smbclient -L //TARGET_IP -N
```

## Command Breakdown

-   `smbclient` -- Samba client for interacting with SMB.
-   `-L` -- List available shares.
-   `//TARGET_IP` -- Target SMB server.
-   `-N` -- Use no password (anonymous/null session).

Example output:

``` text
ADMIN$
AnonShare
C$
IPC$
NETLOGON
SYSVOL
SharedFiles
UserBackups
```

------------------------------------------------------------------------

# Understanding Common Shares

## ADMIN\$

Administrative share used for remote administration.

Normally accessible only to administrators.

------------------------------------------------------------------------

## C\$

Administrative share exposing the C: drive.

Should never allow anonymous access.

------------------------------------------------------------------------

## IPC\$

Inter-Process Communication share.

Often used together with RPC.

Can sometimes allow anonymous enumeration.

------------------------------------------------------------------------

## NETLOGON

Stores logon scripts and authentication resources.

Usually accessible to authenticated domain users.

------------------------------------------------------------------------

## SYSVOL

Contains:

-   Group Policy Objects (GPOs)
-   Logon scripts
-   Domain-wide configuration

It is one of the most important shares during Active Directory
assessments.

------------------------------------------------------------------------

## Non-standard Shares

Example:

-   AnonShare
-   SharedFiles
-   UserBackups

These deserve immediate attention because administrators often store
sensitive files inside them.

------------------------------------------------------------------------

# Enumerating Permissions with smbmap

``` bash
smbmap -H TARGET_IP
```

Why use smbmap?

-   Quickly lists shares
-   Displays permissions
-   Avoids manually connecting to every share

Permission meanings:

-   READ -- Download files
-   WRITE -- Upload files
-   NO ACCESS -- Permission denied

------------------------------------------------------------------------

# Accessing a Share

``` bash
smbclient //TARGET_IP/SharedFiles -N
```

Useful interactive commands:

``` text
help        Show commands
ls          List files
cd          Change directory
pwd         Print working directory
get file    Download a file
put file    Upload a file
exit        Exit smbclient
```

Example:

``` bash
get Mouse_and_Malware.txt
```

This downloads the file to the local machine.

------------------------------------------------------------------------

# Why Search Every Share?

SMB shares may contain:

-   Passwords in configuration files
-   Backup archives
-   SSH keys
-   Scripts with credentials
-   Database exports
-   Network diagrams

Always inspect every readable share.

------------------------------------------------------------------------

# Nmap SMB Script

Nmap can also enumerate shares:

``` bash
nmap -p445 --script smb-enum-shares TARGET_IP
```

This identifies accessible shares and permissions without manually
connecting.

------------------------------------------------------------------------

# Other Useful Tools

## enum4linux-ng

``` bash
enum4linux-ng -A TARGET_IP
```

Performs extensive SMB and RPC enumeration including:

-   Users
-   Groups
-   Shares
-   Password policy
-   RID cycling
-   OS information

------------------------------------------------------------------------

## CrackMapExec

CrackMapExec supports SMB enumeration, credential testing and many
post-exploitation features.

It is commonly used during Active Directory assessments.

------------------------------------------------------------------------

## Impacket smbclient

The Impacket toolkit includes a Python implementation of smbclient that
provides additional flexibility during penetration tests.

------------------------------------------------------------------------

# SMB Enumeration Workflow

``` text
Discover SMB
      ↓
List Shares
      ↓
Identify Anonymous Access
      ↓
Enumerate Permissions
      ↓
Access Readable Shares
      ↓
Download Interesting Files
      ↓
Search for Credentials
      ↓
Use Findings in Later Attacks
```

------------------------------------------------------------------------

# Common Mistakes

-   Ignoring non-standard shares
-   Downloading only one file and stopping
-   Forgetting SYSVOL and NETLOGON
-   Not checking write permissions
-   Assuming ADMIN\$ is always inaccessible

------------------------------------------------------------------------

# Key Takeaways

-   SMB is one of the most valuable enumeration services.
-   Anonymous shares frequently leak sensitive information.
-   Always enumerate permissions before accessing shares.
-   Inspect every readable file for credentials and configuration data.
-   SMB findings often provide the information needed for the next stage
    of an assessment.

------------------------------------------------------------------------

**========== CONTINUE TO PART 3 (LDAP & RPC Enumeration) ==========**
# Active Directory (AD) Basic Enumeration -- Complete Study Notes

# Part 3 -- LDAP Enumeration, RPC Enumeration & RID Cycling

------------------------------------------------------------------------

# LDAP (Lightweight Directory Access Protocol)

## What is LDAP?

LDAP is the protocol Active Directory uses to store and retrieve
information about directory objects.

Think of LDAP as the **database query language** for Active Directory.

LDAP can return information about:

-   Users
-   Groups
-   Computers
-   Organizational Units (OUs)
-   Password policies
-   Domain information

------------------------------------------------------------------------

# Why LDAP Enumeration Matters

If anonymous LDAP bind is enabled, an attacker may gather valuable
information **without valid credentials**.

Possible information includes:

-   Domain name
-   Domain Controller hostname
-   User accounts
-   Group memberships
-   Organizational structure

------------------------------------------------------------------------

# Testing Anonymous LDAP Bind

``` bash
ldapsearch -x -H ldap://10.211.11.10 -s base
```

## Command Breakdown

-   `ldapsearch` -- LDAP query tool.
-   `-x` -- Simple (anonymous) authentication.
-   `-H` -- LDAP server URI.
-   `-s base` -- Query only the base object.

Example output may reveal:

-   Domain name
-   Forest information
-   Default naming context
-   DNS hostname
-   LDAP service name

These values help identify the AD environment.

------------------------------------------------------------------------

# Enumerating Users

``` bash
ldapsearch -x -H ldap://10.211.11.10 -b "dc=tryhackme,dc=loc" "(objectClass=person)"
```

## Option Breakdown

-   `-b` -- Base distinguished name to search.
-   `(objectClass=person)` -- Filter for user objects.

This query attempts to return user objects stored in the directory.

------------------------------------------------------------------------

# enum4linux-ng

`enum4linux-ng` automates common SMB and RPC enumeration tasks.

``` bash
enum4linux-ng -A 10.211.11.10 -oA results
```

## Options

-   `-A` -- Run all supported enumeration modules.
-   `-oA` -- Save output in multiple formats.

It can gather:

-   Users
-   Groups
-   Shares
-   NetBIOS information
-   Password policy
-   RID information
-   Operating system details

------------------------------------------------------------------------

# RPC (Remote Procedure Call)

## What is RPC?

RPC allows one computer to request services from another across the
network.

Windows uses RPC extensively for administration and management.

If SMB null sessions are enabled, RPC may allow anonymous enumeration.

------------------------------------------------------------------------

# Connecting with rpcclient

``` bash
rpcclient -U "" 10.211.11.10 -N
```

## Command Breakdown

-   `rpcclient` -- RPC client.
-   `-U ""` -- Empty username.
-   `-N` -- Do not ask for a password.

If successful, an `rpcclient>` prompt is displayed.

------------------------------------------------------------------------

# Useful rpcclient Commands

``` text
help
enumdomusers
enumdomgroups
queryuser RID
queryusergroups RID
lookupnames USERNAME
lsaquery
getdompwinfo
```

## enumdomusers

Lists domain user accounts and their Relative Identifiers (RIDs).

Example:

``` text
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[gerald.burgess] rid:[0x650]
```

## enumdomgroups

Lists domain groups.

Useful for translating group RIDs into readable names.

## queryuser RID

Displays detailed information about a specific RID.

## queryusergroups RID

Shows which groups a user belongs to.

## getdompwinfo

Retrieves password policy information if permitted.

------------------------------------------------------------------------

# RID and SID

## SID (Security Identifier)

Every Active Directory object has a unique SID.

Example:

``` text
S-1-5-21-XXXXXXXX-XXXXXXXX-XXXXXXXX-1001
```

The last number is the RID.

## RID (Relative Identifier)

The RID uniquely identifies an object within the domain.

Common RIDs:

    RID Meaning
  ----- ---------------
    500 Administrator
    501 Guest
    512 Domain Admins
    513 Domain Users
    514 Domain Guests

Normal user accounts usually begin around RID 1000.

------------------------------------------------------------------------

# RID Cycling

If `enumdomusers` is blocked, individual RIDs can still be queried.

``` bash
for i in $(seq 500 2000); do
echo "queryuser $i" | rpcclient -U "" -N 10.211.11.10 2>/dev/null | grep -i "User Name"
done
```

## How It Works

1.  Loop through RID values.
2.  Execute `queryuser`.
3.  Ignore errors with `2>/dev/null`.
4.  Display only successful matches using `grep`.

This technique discovers valid users even when bulk enumeration is
restricted.

------------------------------------------------------------------------

# Enumeration Workflow

``` text
LDAP
 ↓
Discover Domain Information
 ↓
Discover Users

RPC
 ↓
List Users
 ↓
List Groups
 ↓
Query Individual Users

RID Cycling
 ↓
Recover Hidden Users
```

------------------------------------------------------------------------

# Common Mistakes

-   Assuming LDAP always allows anonymous access.
-   Forgetting to save enumeration output.
-   Ignoring group membership information.
-   Stopping after `enumdomusers` without using `queryuser`.
-   Not attempting RID cycling when enumeration is blocked.

------------------------------------------------------------------------

# Key Takeaways

-   LDAP stores Active Directory directory information.
-   Anonymous LDAP access can leak valuable data.
-   RPC is a powerful enumeration interface.
-   RID cycling is an excellent fallback technique.
-   Combining LDAP and RPC provides a much clearer understanding of the
    domain.

------------------------------------------------------------------------

**========== CONTINUE TO PART 4 (Kerberos, Kerbrute & User Validation)
==========**
# Active Directory (AD) Basic Enumeration -- Complete Study Notes

# Part 4 -- Kerberos, Kerbrute & Password Policy Enumeration

------------------------------------------------------------------------

# Kerberos

## What is Kerberos?

Kerberos is the default authentication protocol used by Active
Directory.

Instead of repeatedly sending passwords across the network, Kerberos
uses **tickets** issued by a trusted server called the **Key
Distribution Center (KDC)**.

Benefits:

-   Mutual authentication
-   Strong encryption
-   Reduced password exposure
-   Single Sign-On (SSO)

------------------------------------------------------------------------

# Kerberos Authentication Workflow

``` text
User
  │
  ▼
Enters Username & Password
  │
  ▼
Domain Controller (KDC)
  │
  ├── Authentication Service (AS)
  ├── Ticket Granting Service (TGS)
  ▼
Ticket Issued
  │
  ▼
Access Network Resources
```

The KDC is hosted on the Domain Controller and normally listens on
**TCP/UDP 88**.

------------------------------------------------------------------------

# Why Enumerate Kerberos?

Kerberos can reveal whether usernames are valid even when passwords are
unknown.

Valid usernames become valuable targets for:

-   Password spraying
-   AS-REP roasting
-   Kerberoasting
-   Further credential attacks

------------------------------------------------------------------------

# Kerbrute

Kerbrute is a tool used to enumerate Active Directory usernames through
Kerberos.

Unlike brute forcing passwords, it checks whether usernames exist.

------------------------------------------------------------------------

# Installing Kerbrute

1.  Download the correct binary from the official Kerbrute releases.
2.  Rename it:

``` bash
mv kerbrute_linux_amd64 kerbrute
```

3.  Make it executable:

``` bash
chmod +x kerbrute
```

`chmod +x` adds execute permission so Linux can run the binary as a
program.

------------------------------------------------------------------------

# Creating a User List

Collect usernames from:

-   LDAP
-   RPC
-   enum4linux-ng
-   RID Cycling

Save them into:

``` text
users.txt
```

Example:

``` text
Administrator
Guest
gerald.burgess
guy.smith
rduke
```

------------------------------------------------------------------------

# Username Enumeration

``` bash
./kerbrute userenum --dc 10.211.11.10 -d tryhackme.loc users.txt
```

## Command Breakdown

-   `./kerbrute` -- Run the Kerbrute executable.
-   `userenum` -- Username enumeration mode.
-   `--dc` -- Domain Controller IP.
-   `-d` -- Domain name.
-   `users.txt` -- File containing usernames.

------------------------------------------------------------------------

# Understanding the Output

Example:

``` text
[+] VALID USERNAME: rduke@tryhackme.loc
```

A line beginning with `[+]` indicates that the username exists in Active
Directory.

Invalid usernames are ignored or reported as failures.

------------------------------------------------------------------------

# Why Validate Users?

Enumeration tools may return:

-   Disabled accounts
-   Service accounts
-   Stale accounts
-   False positives

Kerbrute helps produce a cleaner list for later password attacks.

------------------------------------------------------------------------

# Password Policy Enumeration

Before attempting password spraying, determine the domain password
policy.

This helps avoid account lockouts and guides password selection.

------------------------------------------------------------------------

# Using rpcclient

Connect anonymously:

``` bash
rpcclient -U "" 10.211.11.10 -N
```

Then run:

``` text
getdompwinfo
```

Possible output:

``` text
min_password_length: 12
password_properties: DOMAIN_PASSWORD_COMPLEX
```

Important fields:

-   Minimum password length
-   Password complexity requirement

------------------------------------------------------------------------

# Using CrackMapExec

``` bash
crackmapexec smb 10.211.11.10 --pass-pol
```

This retrieves additional policy information when anonymous access is
permitted.

Typical values include:

-   Minimum password length
-   Password history
-   Maximum password age
-   Minimum password age
-   Account lockout threshold
-   Lockout duration
-   Password complexity

------------------------------------------------------------------------

# Understanding Password Complexity

Complex passwords usually require a combination of:

-   Uppercase letters
-   Lowercase letters
-   Numbers
-   Special characters

Passwords should also avoid containing the user's name.

------------------------------------------------------------------------

# Why Password Policy Matters

Knowing the policy allows an attacker or tester to:

-   Build realistic password lists
-   Avoid immediate account lockouts
-   Respect password length requirements
-   Reduce unnecessary login failures

------------------------------------------------------------------------

# Workflow

``` text
Enumerate Users
      ↓
Validate Users with Kerbrute
      ↓
Retrieve Password Policy
      ↓
Prepare Password List
      ↓
Ready for Password Spraying
```

------------------------------------------------------------------------

# Common Mistakes

-   Skipping username validation.
-   Spraying passwords before checking lockout thresholds.
-   Using passwords shorter than the minimum length.
-   Ignoring complexity requirements.
-   Forgetting to remove invalid users from the target list.

------------------------------------------------------------------------

# Key Takeaways

-   Kerberos is the primary AD authentication protocol.
-   Kerbrute validates usernames without knowing passwords.
-   Password policy enumeration reduces the risk of account lockouts.
-   A validated user list combined with password policy information
    prepares the environment for password spraying.

------------------------------------------------------------------------

**========== CONTINUE TO PART 5 (Password Spraying, CrackMapExec
Workflow & Cheat Sheet) ==========**
# Active Directory (AD) Basic Enumeration -- Complete Study Notes

# Part 5 -- Password Spraying, CrackMapExec, Workflow & Revision

------------------------------------------------------------------------

# Password Spraying

## What is Password Spraying?

Password spraying is an authentication attack where **one password** is
tested against **many user accounts**.

Unlike brute-force attacks, password spraying minimizes the chance of
triggering account lockouts.

## Password Spraying vs Brute Force

### Brute Force

``` text
User1
 ├── Password1
 ├── Password2
 ├── Password3
 └── ...
```

High risk of locking a single account.

### Password Spraying

``` text
Password1!
 ├── User1
 ├── User2
 ├── User3
 └── User4
```

Lower risk because only one password is attempted per user.

------------------------------------------------------------------------

# Why Password Spraying Works

Many organizations:

-   Reuse common passwords.
-   Choose predictable seasonal passwords.
-   Follow weak password patterns.
-   Fail to educate users about password security.

Examples:

``` text
Password1!
Summer2025!
Winter2025!
Welcome123!
CompanyName2025!
```

------------------------------------------------------------------------

# Building a Password List

Use information gathered during enumeration:

-   Password policy
-   Company naming conventions
-   OSINT
-   Previous data breaches
-   Seasonal passwords

Ensure passwords satisfy the domain's complexity requirements.

------------------------------------------------------------------------

# CrackMapExec (CME)

## What is CrackMapExec?

CrackMapExec (CME) is a post-exploitation and network assessment
framework widely used during Active Directory engagements.

Supported protocols include:

-   SMB
-   LDAP
-   RDP
-   WinRM
-   SSH
-   MSSQL

It can:

-   Validate credentials
-   Enumerate systems
-   Retrieve password policies
-   Execute commands (with sufficient privileges)

------------------------------------------------------------------------

# Password Spraying with CME

``` bash
crackmapexec smb 10.211.11.20 -u users.txt -p passwords.txt
```

## Command Breakdown

-   `crackmapexec` -- Start CME.
-   `smb` -- Use the SMB protocol.
-   `10.211.11.20` -- Target host.
-   `-u users.txt` -- File containing usernames.
-   `-p passwords.txt` -- File containing candidate passwords.

------------------------------------------------------------------------

# Understanding the Output

Example:

``` text
[-] tryhackme.loc\Administrator:Password! STATUS_LOGON_FAILURE
[+] tryhackme.loc\rduke:Password1!
```

-   `[-]` indicates authentication failed.
-   `[+]` indicates valid credentials.

Record successful credentials immediately for later use.

------------------------------------------------------------------------

# Complete Enumeration Workflow

``` text
VPN Access
      ↓
Host Discovery
      ↓
Identify Live Hosts
      ↓
Port Scanning
      ↓
Locate Domain Controller
      ↓
Enumerate SMB Shares
      ↓
Enumerate LDAP
      ↓
Enumerate RPC
      ↓
RID Cycling (if needed)
      ↓
Validate Users with Kerbrute
      ↓
Enumerate Password Policy
      ↓
Create Password List
      ↓
Password Spray with CME
      ↓
Obtain Valid Credentials
```

------------------------------------------------------------------------

# Common Mistakes

-   Spraying passwords without checking the lockout policy.
-   Using an excessive number of passwords.
-   Ignoring successful logins.
-   Forgetting to save enumeration results.
-   Failing to revisit SMB shares after obtaining credentials.

------------------------------------------------------------------------

# Quick Revision Cheat Sheet

``` bash
# Host Discovery
fping -agq 10.211.11.0/24
nmap -sn 10.211.11.0/24

# Port Scan
nmap -p 88,135,139,389,445,636 -sV -sC -iL hosts.txt

# SMB
smbclient -L //TARGET -N
smbclient //TARGET/SHARE -N
smbmap -H TARGET

# LDAP
ldapsearch -x -H ldap://TARGET -s base
ldapsearch -x -H ldap://TARGET -b "dc=domain,dc=local" "(objectClass=person)"

# RPC
rpcclient -U "" TARGET -N
enumdomusers
enumdomgroups
queryuser RID
queryusergroups RID
getdompwinfo

# enum4linux-ng
enum4linux-ng -A TARGET

# Kerbrute
./kerbrute userenum --dc TARGET -d DOMAIN users.txt

# Password Policy
crackmapexec smb TARGET --pass-pol

# Password Spraying
crackmapexec smb TARGET -u users.txt -p passwords.txt
```

------------------------------------------------------------------------

# Interview Questions

1.  What is Active Directory?
2.  What is the role of a Domain Controller?
3.  What are SMB, LDAP and RPC used for?
4.  What is anonymous LDAP bind?
5.  What is a null session?
6.  What is the difference between SID and RID?
7.  Why is Kerbrute used?
8.  Why should password policy be checked before password spraying?
9.  What is the difference between brute force and password spraying?
10. Which ports usually identify a Domain Controller?

------------------------------------------------------------------------

# Final Revision Notes

-   Enumeration is the foundation of every internal penetration test.
-   Always collect as much information as possible before exploitation.
-   Combine results from SMB, LDAP, RPC and Kerberos to build an
    accurate picture of the environment.
-   Save outputs from every tool for later analysis.
-   Respect password lockout policies during testing.
-   Good enumeration often leads directly to valid credentials without
    exploiting software vulnerabilities.

------------------------------------------------------------------------

**End of Documentation**
