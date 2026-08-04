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

---

# Authentication Methods

Active Directory stores user credentials on the Domain Controller. Whenever a user attempts to access a resource within the domain, the service contacts the Domain Controller to verify the user's identity.

Windows domains support two authentication protocols:

- **Kerberos** (Default)
- **NetNTLM** (Legacy)

Although Kerberos is the modern authentication protocol, NetNTLM still exists in many environments to maintain compatibility with older systems.

---

# Kerberos Authentication

Kerberos is the default authentication protocol used in modern Windows domains.

Instead of sending passwords every time a user accesses a resource, Kerberos uses **tickets** to prove the user's identity.

These tickets allow users to authenticate securely without repeatedly transmitting their credentials across the network.

---

## Components of Kerberos

### Key Distribution Center (KDC)

The **Key Distribution Center (KDC)** is a service running on the **Domain Controller**.

It is responsible for:

- Authenticating users
- Issuing Kerberos tickets
- Generating session keys
- Verifying ticket requests

---

### Ticket Granting Ticket (TGT)

The first ticket a user receives after successfully authenticating.

Purpose:

- Proves the user has already authenticated
- Allows requesting additional service tickets without re-entering credentials

The TGT is encrypted using the **krbtgt account password hash**, meaning only the Domain Controller can decrypt it.

---

### Ticket Granting Service (TGS)

A **Ticket Granting Service (TGS)** ticket allows access to a specific network service.

Examples:

- Shared folders
- Databases
- Web servers
- File servers
- Network printers

Unlike a TGT, a TGS only grants access to one particular service.

---

### Session Keys

Kerberos also generates temporary **Session Keys**.

These keys are used to:

- Encrypt communication
- Request additional tickets
- Authenticate to network services securely

---

# Kerberos Authentication Process

## Step 1 – Initial Authentication

The user sends:

- Username
- Current timestamp

The timestamp is encrypted using a key derived from the user's password and sent to the **KDC**.

If the credentials are correct, the KDC returns:

- Ticket Granting Ticket (TGT)
- Session Key

---

## Step 2 – Requesting a Service Ticket

When accessing a network resource, the user presents:

- Username
- TGT
- Service Principal Name (SPN)
- Timestamp encrypted using the Session Key

The KDC verifies the TGT and issues:

- Ticket Granting Service (TGS)
- Service Session Key

The TGS is encrypted using the password hash of the account running the requested service.

---

## Step 3 – Accessing the Service

The client presents the TGS to the target service.

The service decrypts the ticket using its own password hash.

If everything is valid:

- The user is authenticated.
- Access to the requested resource is granted.

---

# Kerberos Workflow

```
User
   │
   ▼
KDC (Domain Controller)
   │
   ├── Issues TGT
   │
   ▼
User Requests TGS
   │
   ▼
KDC Issues TGS
   │
   ▼
Target Service
   │
   ▼
Access Granted
```

---

# Important Kerberos Concepts

- Default authentication protocol in Windows domains.
- Uses tickets instead of repeatedly sending passwords.
- Authentication occurs through the KDC.
- Supports Single Sign-On (SSO).
- Passwords are never repeatedly transmitted across the network.

---

# NetNTLM Authentication

NetNTLM is the older Windows authentication protocol.

Unlike Kerberos, NetNTLM uses a **Challenge-Response** authentication mechanism.

It is primarily retained for backward compatibility with legacy applications and systems.

---

# NetNTLM Authentication Process

## Step 1

The client requests authentication from the server.

---

## Step 2

The server generates a random challenge.

---

## Step 3

The client combines:

- NTLM Password Hash
- Challenge
- Additional authentication data

to calculate a response.

The password itself is **never sent**.

---

## Step 4

The server forwards:

- Challenge
- Client Response

to the Domain Controller.

---

## Step 5

The Domain Controller performs the same calculation.

If the generated response matches the client's response:

Authentication succeeds.

Otherwise:

Authentication fails.

---

## Step 6

The Domain Controller informs the server.

The server then grants or denies access.

---

# NetNTLM Workflow

```
Client
   │
Authentication Request
   ▼
Server
   │
Random Challenge
   ▼
Client
   │
Challenge Response
   ▼
Server
   │
Forward Response
   ▼
Domain Controller
   │
Verification
   ▼
Server
   │
Authentication Result
   ▼
Client
```

---

# Important NetNTLM Concepts

- Legacy authentication protocol.
- Uses Challenge-Response authentication.
- Passwords are never transmitted over the network.
- Still enabled in many environments for compatibility.

---

## TryHackMe Questions

### Question

When referring to Kerberos, what ticket allows users to request additional TGS tickets?

**Answer**

```
Ticket Granting Ticket (TGT)
```

---

### Question

During NetNTLM authentication, is the user's password transmitted over the network?

**Answer**

```
No (nay)
```

---

# Trees, Forests and Trusts

As organizations grow, a single Active Directory domain often becomes difficult to manage.

Active Directory allows multiple domains to be organized into larger logical structures.

The main structures are:

- Trees
- Forests
- Trust Relationships

---

# Trees

A **Tree** is a collection of Windows domains that share the same namespace.

Example:

```
thm.loc
│
├── tbm.thm.loc
│
├── us.tbm.thm.loc
│
└── uk.tbm.thm.loc
```

Each domain has:

- Its own users
- Computers
- Domain Controller
- Domain Admins

This separation allows departments or business units to be managed independently.

---

## Enterprise Admins

When multiple domains exist within a tree, Active Directory introduces another administrative group.

### Enterprise Admins

Members of this group have administrative privileges across every domain in the tree.

Comparison:

**Domain Admins**

- Manage one domain

**Enterprise Admins**

- Manage every domain within the enterprise

---

# Forests

A **Forest** connects multiple Active Directory Trees that use different namespaces.

Example:

```
thm.loc

tvm.loc
```

Although the namespaces differ, they can still share resources by becoming part of the same forest.

Forests allow organizations resulting from mergers, acquisitions, or partnerships to maintain separate domains while sharing resources securely.

---

# Trust Relationships

Trust Relationships allow users from one domain to access resources located in another domain.

Without a trust relationship:

```
Domain A
      ❌
Domain B
```

Users cannot access resources across domains.

After establishing trust:

```
Domain A
      ⇄
Domain B
```

Users can be granted access across domains.

---

## One-Way Trust

Example:

```
AAA trusts BBB
```

Meaning:

Users from **BBB** may access resources in **AAA** if authorized.

Remember:

The **trust direction** is opposite to the **access direction**.

---

## Two-Way Trust

Both domains trust each other.

```
AAA  ⇄  BBB
```

Users from both domains may be authorized to access resources in the other domain.

By default:

Domains joined within the same tree or forest automatically establish two-way trust relationships.

---

# Important Note

Trust relationships **do not automatically grant access**.

They only make cross-domain authentication possible.

Administrators must still assign permissions manually to determine which users can access which resources.

---

## TryHackMe Question

### Question

What is a group of Windows domains that share the same namespace called?

**Answer**

```
Tree
```

---

# Key Concepts Learned

- Kerberos Authentication
- NetNTLM Authentication
- Key Distribution Center (KDC)
- Ticket Granting Ticket (TGT)
- Ticket Granting Service (TGS)
- Session Keys
- Challenge-Response Authentication
- Service Principal Name (SPN)
- Trees
- Forests
- Trust Relationships
- Enterprise Admins
- Domain Admins

---

# Skills Gained

After completing this section, I can:

- Explain how Kerberos authentication works.
- Understand the purpose of TGT and TGS tickets.
- Describe how NetNTLM Challenge-Response authentication functions.
- Differentiate between Kerberos and NetNTLM.
- Explain Active Directory Trees and Forests.
- Understand one-way and two-way trust relationships.
- Identify Enterprise Admin and Domain Admin responsibilities.

---

