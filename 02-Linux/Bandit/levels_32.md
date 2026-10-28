# OverTheWire Bandit Level 32 → 33 
**Level:** 32 → 33   
**Date:** 31 July 2026

---

# Objective

The goal of this level is to escape a restricted uppercase shell, understand how shell variables behave, exploit a SUID binary, and obtain the password for the final Bandit level.

This challenge demonstrates how restricted shells can sometimes be bypassed and how SUID binaries can execute programs with elevated privileges.

---

# Understanding the Challenge

After logging into Bandit32, I was greeted by an unusual shell called the **Uppercase Shell**.

Unlike a normal Linux shell, every command entered is automatically converted to uppercase before execution.

For example:

```bash
ls
```

became

```text
LS
```

Since Linux commands are case-sensitive, most commands failed because there is no executable named `LS`.

The challenge was to escape this restricted shell and obtain access to the password for the next level.

---

# Step 1 - Connect to the Machine

I connected to the Bandit32 machine using SSH.

```bash
ssh bandit32@bandit.labs.overthewire.org -p 2220
```

After entering the password, the following message appeared:

```text
WELCOME TO THE UPPERCASE SHELL
```

---

# Step 2 - Observe the Restricted Shell

Testing a simple command:

```bash
ls
```

Result:

```text
LS
```

Since the shell converted everything to uppercase, normal commands no longer worked.

---

# Step 3 - Escape the Uppercase Shell

Instead of running a normal command, I used the special shell variable:

```bash
$0
```

This started another instance of the current shell.

Unlike typed commands, the shell variable itself was not converted into uppercase, allowing me to escape the restriction.

To verify that I had escaped successfully:

```bash
whoami
```

Output:

```text
bandit33
```

---

# Step 4 - Inspect the Directory

I listed the files in the current directory.

```bash
ls -la
```

Among the files was:

```text
-rwsr-x--- 1 bandit33 bandit32 ... uppershell
```

The important part was:

```text
rws
```

The **s** indicates that the executable has the **SUID** bit set.

---

# Step 5 - Execute the SUID Binary

I executed the binary.

```bash
./uppershell
```

This launched another uppercase shell.

However, because the binary is owned by **bandit33**, it executes with **bandit33's privileges**.

---

# Step 6 - Escape the SUID Shell

Inside the SUID uppercase shell, I again used:

```bash
$0
```

This opened a normal shell running with the permissions of **bandit33**.

To verify:

```bash
whoami
```

Output:

```text
bandit33
```

---

# Step 7 - Read the Password

Now that I had the correct privileges, I could read the password file.

```bash
cat /etc/bandit_pass/bandit33
```

Output:

```text
u4P2CyPOwPGLe94RdD9Uo2FxFwvnFswM
```

---

# Password Obtained

```text
u4P2CyPOwPGLe94RdD9Uo2FxFwvnFswM
```

---

# Commands Used

```bash
ssh bandit32@bandit.labs.overthewire.org -p 2220

$0

whoami

ls -la

./uppershell

$0

whoami

cat /etc/bandit_pass/bandit33
```

---

# Understanding the Commands

## ssh

```bash
ssh bandit32@bandit.labs.overthewire.org -p 2220
```

Creates a secure remote connection to the Bandit server.

`-p 2220`

Specifies the custom SSH port used by OverTheWire.

---

## $0

```bash
$0
```

`$0` is a special shell variable that contains the name of the currently running shell or script.

Executing it launches another instance of that shell.

In this challenge, it bypassed the command transformation performed by the uppercase shell and provided access to a normal shell.

---

## whoami

```bash
whoami
```

Displays the username of the current process.

This confirmed which user's privileges the shell was running with.

---

## ls -la

```bash
ls -la
```

Lists all files, including hidden ones, along with detailed information such as:

- Permissions
- Owner
- Group
- File size
- Modification date

This allowed me to identify the `uppershell` executable and its permissions.

---

## ./uppershell

```bash
./uppershell
```

Runs the executable located in the current directory.

Since the binary has the SUID bit set, it executes using the permissions of its owner (**bandit33**) rather than the current user.

---

## cat

```bash
cat /etc/bandit_pass/bandit33
```

Displays the contents of the password file once sufficient privileges are obtained.

---

# What is a Restricted Shell?

A restricted shell limits what a user can do.

Examples include:

- Blocking certain commands
- Restricting directory changes
- Preventing program execution
- Modifying user input

In this challenge, every command entered by the user was automatically converted to uppercase before execution.

---

# What is `$0`?

`$0` is one of Bash's special shell variables.

It represents the name of the currently running shell or script.

Example:

```bash
echo $0
```

Output:

```text
bash
```

Running:

```bash
$0
```

starts another instance of that shell.

Because the shell interpreted `$0` before converting the command to uppercase, it allowed the restricted environment to be bypassed.

---

# What is SUID?

**SUID (Set User ID)** is a special Linux file permission.

Normally:

```
Program
        │
Runs as
        ▼
Current User
```

With SUID:

```
Program
        │
Runs as
        ▼
File Owner
```

This allows ordinary users to execute specific programs with the privileges of the file owner.

---

## Identifying SUID

Example:

```text
-rwsr-x---
```

Breaking it down:

```
Owner   -> rws
Group   -> r-x
Others  -> ---
```

The **s** replaces the owner's execute bit and indicates that the SUID permission is enabled.

---

# Why Did This Work?

The `uppershell` program is owned by **bandit33** and has the SUID bit set.

When executed, it runs with **bandit33's** privileges.

By escaping the restricted uppercase shell using `$0`, I obtained a normal shell that inherited those elevated privileges.

This allowed access to files that were otherwise unreadable.

---

# Workflow

```text
SSH Login
      │
      ▼
Uppercase Shell
      │
      ▼
Use $0
      │
      ▼
Normal Shell
      │
      ▼
Find SUID Binary
      │
      ▼
Execute uppershell
      │
      ▼
Uppercase SUID Shell
      │
      ▼
Use $0 Again
      │
      ▼
Normal Shell as bandit33
      │
      ▼
Read Password
      │
      ▼
Complete Bandit
```

---

# Key Concepts Learned

- Restricted Shell
- Uppercase Shell
- Bash Special Variables
- `$0`
- SSH
- SUID (Set User ID)
- Linux File Permissions
- Privilege Escalation
- `whoami`
- `ls -la`

---
