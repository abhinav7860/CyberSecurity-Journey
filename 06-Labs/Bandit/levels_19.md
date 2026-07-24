# OverTheWire Bandit: Level 19 → Level 20
**Date:** 24 July 2026

---
## Objective

The goal of this level is to use the **setuid binary** located in the home directory to retrieve the password for **bandit20**.

The password is stored in the usual location:

```text
/etc/bandit_pass/bandit20
```

However, the current user (**bandit19**) does not have permission to read it directly.

---

# Understanding the Concept

## What is SUID (Set User ID)?

SUID (Set User ID) is a special Linux file permission.

When an executable has the **SUID** bit set, it runs with the permissions of the **file owner** instead of the user executing it.

Normally:

```
User executes program
        │
        ▼
Program runs as that same user
```

With SUID:

```
User executes program
        │
        ▼
Program temporarily runs as the file owner
```

This allows specific programs to perform privileged tasks without giving users full access to another account.

---

# Step 1 - List the Files

First, check what exists in the home directory.

```bash
ls
```

Output

```text
bandit20-do
```

There is a single executable called **bandit20-do**.

---

# Step 2 - Check File Permissions

Display detailed information about the file.

```bash
ls -l
```

Output

```text
-rwsr-x--- 1 bandit20 bandit19 14880 Jun 24 14:58 bandit20-do
```

### Breaking Down the Permissions

```text
-rwsr-x---
```

| Permission | Meaning |
|------------|---------|
| `-` | Regular file |
| `rwx` | Owner (bandit20) has full permissions |
| `s` | **SUID bit is set** |
| `r-x` | Group can read and execute |
| `---` | Others have no permissions |

Notice the **`s`** instead of **`x`**.

This indicates the executable runs with the privileges of **bandit20**.

---

# Step 3 - Execute the Binary

Run the binary without any arguments.

```bash
./bandit20-do
```

Output

```text
Run a command as another user.
Example: ./bandit20-do whoami
```

The program tells us it can execute commands as another user.

---

# Step 4 - Verify the Effective User

Use the suggested `whoami` command.

```bash
./bandit20-do whoami
```

Output

```text
bandit20
```

This confirms that commands executed through the binary run as **bandit20** instead of **bandit19**.

---

# Step 5 - Read the Password

Since the binary executes commands with **bandit20's** privileges, use it to read the password file.

```bash
./bandit20-do cat /etc/bandit_pass/bandit20
```

Output

```text
4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA
```

This is the password for **Bandit Level 20**.

---

# Commands Used

```bash
ls

ls -l

./bandit20-do

./bandit20-do whoami

./bandit20-do cat /etc/bandit_pass/bandit20
```

---

# Key Concepts Learned

## SUID (Set User ID)

- Allows an executable to run with the permissions of its owner.
- Commonly used for system utilities that require elevated privileges.
- Indicated by an **`s`** in the owner's execute permission.

Example

```text
-rwsr-x---
```

---

## Effective User ID (EUID)

A process has two user IDs:

- **Real User ID (RUID)** → The user who started the process.
- **Effective User ID (EUID)** → The permissions the process currently uses.

Because of SUID:

```
Real User:
bandit19

Effective User:
bandit20
```

The binary temporarily gains **bandit20's** privileges while it executes.

---

