# OverTheWire Bandit Level 26 → 27
**Level:** 26 → 27   
**Date:** 28 July 2026

---

# Objective

The goal of this level is to retrieve the password for **bandit27**.

After escaping the restricted shell in the previous level, we now have an interactive Bash shell as **bandit26**. The task is to identify how to execute commands with the permissions of **bandit27** and read its password.

---

# Understanding the Challenge

After escaping the restricted shell using Vim, I obtained a Bash shell.

The first step was to inspect the home directory.

```bash
ls
```

Output:

```text
bandit27-do
text.txt
```

The interesting file is **bandit27-do**, which is an executable binary.

---

# Step 1 - Check the File Permissions

Run:

```bash
ls -l
```

Output:

```text
-rwsr-x--- 1 bandit27 bandit26 14880 Jun 24 14:59 bandit27-do
-rw-r----- 1 bandit26 bandit26   258 Jun 24 14:59 text.txt
```

Notice the permissions of **bandit27-do**.

```
-rwsr-x---
```

The **s** in place of the owner's execute permission indicates that the **SUID (Set User ID)** bit is enabled.

---

# What is SUID?

SUID (Set User ID) is a special Linux permission.

Normally:

```
User
↓

Runs Program

↓

Program executes with the user's permissions
```

With SUID enabled:

```
User
↓

Runs Program

↓

Program executes with the OWNER'S permissions
```

Since the binary is owned by:

```
bandit27
```

any command executed through it runs with **bandit27's permissions**.

---

# Step 2 - Use the SUID Binary

Execute:

```bash
./bandit27-do cat /etc/bandit_pass/bandit27
```

Output:

```text
STJLJBRRphMxKB392CT4iOr5CbzPU9ER
```

The binary executed the **cat** command using the permissions of **bandit27**, allowing access to the password file.

---

# Password Obtained

```text
STJLJBRRphMxKB392CT4iOr5CbzPU9ER
```

---

# Commands Used

```bash
ls

ls -l

./bandit27-do cat /etc/bandit_pass/bandit27
```

---

# Understanding the Commands

## ls

```bash
ls
```

Lists the files in the current directory.

Output:

```text
bandit27-do
text.txt
```

---

## ls -l

```bash
ls -l
```

Displays detailed information about files.

Example:

```text
-rwsr-x---
```

Breakdown:

```
-
Regular file

rwx
Owner permissions

r-x
Group permissions

---
Other users
```

The important part is:

```
rws
```

The **s** indicates that the **SUID bit** is enabled.

---

## bandit27-do

```bash
./bandit27-do
```

Runs the SUID binary.

Anything written after it becomes the command that the binary executes.

Example:

```bash
./bandit27-do id
```

would execute **id** as **bandit27**.

In this level we executed:

```bash
./bandit27-do cat /etc/bandit_pass/bandit27
```

---

## cat

```bash
cat filename
```

Displays the contents of a file.

Normally,

```bash
cat /etc/bandit_pass/bandit27
```

would return:

```text
Permission denied
```

because **bandit26** cannot read that file.

However,

```bash
./bandit27-do cat /etc/bandit_pass/bandit27
```

runs **cat** as **bandit27**, which has permission to read its own password file.

---

# Where is the Password File?

You asked a very good question.

The command was:

```bash
./bandit27-do cat /etc/bandit_pass/bandit27
```

Notice the last part:

```text
/etc/bandit_pass/bandit27
```

This is an **absolute path**.

```
/
│
├── etc
│     │
│     └── bandit_pass
│             │
│             ├── bandit0
│             ├── bandit1
│             ├── bandit2
│             ├── ...
│             └── bandit27
```

Every Bandit user's password is stored in:

```text
/\
└── etc
     └── bandit_pass
```

Each file contains the password for one Bandit user.

Normally:

```
bandit26
```

cannot read

```
/etc/bandit_pass/bandit27
```

because Linux file permissions prevent it.

The SUID binary temporarily gives the necessary permissions.

---

# Why Didn't We Change Directory?

Because the password file is **not** inside your home directory.

It is located in:

```text
/etc/bandit_pass/
```

Linux allows you to access any file directly if you know its absolute path and have permission.

That's why we simply wrote:

```bash
cat /etc/bandit_pass/bandit27
```

instead of changing directories first.

---

# Workflow

```text
Escape Restricted Shell
          │
          ▼
Obtain Bash Shell
          │
          ▼
List Files
          │
          ▼
Find SUID Binary
          │
          ▼
Check Permissions
          │
          ▼
Notice SUID Bit
          │
          ▼
Run:

./bandit27-do cat /etc/bandit_pass/bandit27

          │
          ▼
Read Password
          │
          ▼
Login as bandit27
```
