# TryHackMe - Active Directory Basics

**Platform:** TryHackMe  
**Room:** Active Directory Basics  
**Date Completed:** 04 August 2026

---

# Overview

In this room, I learned the fundamentals of **Microsoft Active Directory (AD)** and why organizations use it to centrally manage users, computers, and security policies across large enterprise networks.

The room introduced the concept of Windows Domains, Domain Controllers, Active Directory Domain Services (AD DS), Organizational Units (OUs), users, machine accounts, and security groups.

This room forms the foundation for understanding Windows enterprise environments and is essential before learning Active Directory attacks, privilege escalation, Kerberos, LDAP, BloodHound, and Active Directory exploitation.

---

# Learning Objectives

After completing this section, I understood:

- Why Active Directory exists
- What a Windows Domain is
- What a Domain Controller (DC) does
- Active Directory Domain Services (AD DS)
- Active Directory Objects
- Users
- Machine Accounts
- Security Groups
- Organizational Units (OUs)
- Difference between OUs and Security Groups
- Default Active Directory Containers

---

# Why Active Directory?

Managing a few computers manually is simple.

For example:

- 5 Computers
- 5 Employees

An administrator could easily:

- Create user accounts
- Configure each computer manually
- Reset passwords
- Troubleshoot systems individually

However, as organizations grow, this approach becomes impossible.

Example:

- 157 Computers
- 320 Users
- Multiple Office Locations

Managing every system individually would consume enormous time and increase administrative overhead.

To solve this problem, Microsoft introduced **Active Directory**, which allows administrators to centrally manage users, computers, groups, and security policies.

---

# Windows Domain

A **Windows Domain** is a collection of users, computers, and network resources managed centrally by an organization.

Instead of configuring every computer individually, all authentication and administration are handled from a central location.

### Benefits of a Windows Domain

- Centralized user management
- Centralized authentication
- Centralized password management
- Group policy deployment
- Easier administration
- Better security management

---

# Domain Controller (DC)

The server responsible for running Active Directory services is called the **Domain Controller (DC).**

The Domain Controller is responsible for:

- Authenticating users
- Authenticating computers
- Managing Active Directory
- Applying Group Policies
- Managing domain resources

### TryHackMe Question

**Question**

What is the server that runs Active Directory services called?

**Answer**

```
Domain Controller
```

---

# Active Directory Domain Services (AD DS)

The core component of Active Directory is **Active Directory Domain Services (AD DS).**

AD DS acts as a centralized database that stores every object inside the domain.

Examples of Active Directory objects include:

- Users
- Computers
- Groups
- Printers
- Shared Folders
- Services

Rather than storing information separately on every machine, all information is maintained inside Active Directory.

---

# Active Directory Objects

Everything inside Active Directory is represented as an object.

Some of the most important object types include:

- User Accounts
- Machine Accounts
- Security Groups
- Organizational Units (OUs)

---

# User Objects

Users are one of the most common Active Directory objects.

They are considered **Security Principals**, meaning they can:

- Authenticate to the domain
- Access resources
- Receive permissions
- Be assigned privileges

User accounts generally represent two entities.

---

## Human Users

Examples:

- Employees
- Students
- Administrators

These users log in to computers and access company resources.

---

## Service Accounts

Some applications require their own accounts to run.

Examples include:

- IIS
- MSSQL
- Other Windows Services

These accounts are granted only the permissions required to run their associated services.

---

# Machine Accounts

Whenever a computer joins an Active Directory domain, a **Machine Account** is automatically created.

Like user accounts, machine accounts are also Security Principals.

Machine accounts:

- Authenticate to the domain
- Have passwords
- Possess limited domain permissions
- Act as local administrators on their own machine

Machine account passwords are automatically generated and rotated by Windows.

Typical characteristics:

- Around 120 random characters
- Automatically managed
- Rarely accessed manually

---

## Machine Naming Convention

Machine accounts always end with:

```
$
```

Example:

Computer Name:

```
ROOTDC
```

Machine Account:

```
ROOTDC$
```

TryHackMe Question

Machine Name:

```
TOM-PC
```

Machine Account:

```
TOM-PC$
```

---

# Security Groups

Managing permissions individually for hundreds of users would be inefficient.

Instead, Active Directory uses **Security Groups**.

Permissions are assigned to groups rather than individual users.

Users inherit permissions simply by joining a group.

Groups may contain:

- Users
- Computers
- Other Groups

Unlike Organizational Units, users can belong to multiple Security Groups simultaneously.

---

# Common Default Security Groups

## Domain Admins

Highest privilege group within the domain.

Members can:

- Manage every computer
- Manage every user
- Manage Domain Controllers
- Configure Active Directory

---

## Server Operators

Can administer Domain Controllers but cannot modify administrative group memberships.

---

## Backup Operators

Can access every file regardless of file permissions.

Primarily used for backup operations.

---

## Account Operators

Responsible for:

- Creating users
- Modifying users
- Managing accounts

---

## Domain Users

Contains every standard user account.

---

## Domain Computers

Contains every computer joined to the domain.

---

## Domain Controllers

Contains all Domain Controllers within the domain.

---

### TryHackMe Question

**Question**

Which group normally administers all computers and resources in a domain?

**Answer**

```
Domain Admins
```

---

# Active Directory Users and Computers (ADUC)

The primary management console for Active Directory is:

```
Active Directory Users and Computers
```

Administrators use this tool to:

- Create users
- Delete users
- Reset passwords
- Create groups
- Manage computers
- Organize Organizational Units

This tool displays the entire hierarchy of the domain.

---

# Organizational Units (OUs)

Organizational Units (OUs) are containers used to organize objects within Active Directory.

Typical organizational structure:

```
THM
│
├── IT
├── Management
├── Marketing
├── Research & Development
└── Sales
```

Each department can have different:

- Security Policies
- Login Restrictions
- Desktop Configurations
- Software Deployment

A user can belong to only **one Organizational Unit** at a time.

---

# Default Active Directory Containers

Windows automatically creates several containers.

## Builtin

Contains built-in Windows security groups.

---

## Computers

Stores newly joined computers by default.

---

## Domain Controllers

Contains all Domain Controllers.

---

## Users

Stores default domain users and groups.

---

## Managed Service Accounts

Contains service accounts used by applications.

---

# Organizational Units vs Security Groups

Although they may appear similar, they serve different purposes.

## Organizational Units (OUs)

Purpose:

Administrative organization and policy application.

Characteristics:

- Apply Group Policies
- Organize departments
- One user belongs to one OU

---

## Security Groups

Purpose:

Permission management.

Characteristics:

- Grant access to resources
- Users can belong to multiple groups
- Used for authorization

---

# Real-World Example

Most organizations structure Active Directory according to business departments.

Example:

```
Company
│
├── IT
├── HR
├── Finance
├── Sales
└── Marketing
```

Each department receives its own:

- Password Policies
- Desktop Restrictions
- Software Packages
- Network Permissions

This centralized structure simplifies administration and improves consistency across the organization.

---

# Commands / Tools Used

- Remote Desktop Protocol (RDP)
- Active Directory Users and Computers (ADUC)

RDP Connection:

```bash
xfreerdp /u:Administrator /p:'learningadisfun1!' /d:THM.LOC /v:192.168.10.100 /dynamic-resolution
```

---

# Key Concepts Learned

- Active Directory
- Windows Domain
- Domain Controller (DC)
- Active Directory Domain Services (AD DS)
- Security Principals
- User Objects
- Service Accounts
- Machine Accounts
- Machine Account Naming Convention
- Organizational Units (OUs)
- Security Groups
- Active Directory Users and Computers (ADUC)
- Centralized Authentication
- Centralized Administration

---

# Skills Gained

After completing this section, I can:

- Explain why organizations use Active Directory.
- Identify the role of a Domain Controller.
- Understand how Active Directory stores and manages objects.
- Differentiate between users, computers, and service accounts.
- Recognize machine account naming conventions.
- Explain the purpose of Organizational Units and Security Groups.
- Navigate the Active Directory Users and Computers management console.

---

# Key Takeaways

- Active Directory centralizes user, computer, and security management within a Windows domain.
- The Domain Controller authenticates users, computers, and manages domain resources.
- Active Directory stores all domain objects through Active Directory Domain Services (AD DS).
- Machine accounts are automatically created when computers join the domain and are identified by a trailing `$`.
- Organizational Units are used for organizing objects and applying policies, while Security Groups are used to assign permissions to resources.
- Understanding Active Directory fundamentals is essential before progressing to topics such as Group Policy, Kerberos authentication, LDAP, BloodHound, and Active Directory attacks.

---

