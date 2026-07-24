# OverTheWire Bandit Level 18 → 19

## Objective

The goal of this level is to retrieve the password stored in the **readme** file located in the home directory.

However, there is a catch:

- The `.bashrc` file has been modified.
- As soon as you log in, the shell executes the modified `.bashrc`.
- The modified script immediately logs you out before you can type any commands.

The challenge is to execute a command **without starting an interactive shell**.

---

# Understanding the Problem

Normally, when you connect through SSH:

```bash
ssh user@host
```

SSH starts a login shell.

The shell then loads configuration files such as:

- `.profile`
- `.bash_profile`
- `.bashrc`

In this level, `.bashrc` has been modified to execute:

```text
Byebye !
```

and immediately terminate the session.

As a result, you cannot run commands after logging in.

---

# Step 1 – Login Normally

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220
```

Output:

```text
Byebye !
Connection to bandit.labs.overthewire.org closed.
```

This confirms that the login shell is exiting immediately.

---

# Step 2 – Execute a Command During Login

SSH allows you to execute a command directly on the remote machine without opening an interactive shell.

Syntax:

```bash
ssh user@host "command"
```

The command is executed immediately after authentication, allowing us to bypass the modified shell.

---

# Step 3 – Verify the Files

Run:

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 "ls -al"
```

Output:

```text
.bashrc
.profile
readme
```

The output confirms that the `readme` file exists.

---

# Step 4 – Read the Password

Now display the contents of the file directly.

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 "cat readme"
```

Output:

```text
KpsOfPkcP7i1FlIExk2QEjyt6dw8dxZI
```

This is the password for **Bandit Level 19**.

---

# Mistake I Made

Initially, I typed:

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 "ls-al"
```

Output:

```text
bash: line 1: ls-al: command not found
```

I forgot the space between `ls` and `-al`.

The correct command is:

```bash
ls -al
```

---

# Why This Works

Normally:

```text
SSH Login
      │
      ▼
Interactive Shell Starts
      │
      ▼
.bashrc Executes
      │
      ▼
Logout
```

Using a remote command:

```text
SSH Login
      │
      ▼
Execute Command
      │
      ▼
Return Output
      │
      ▼
Disconnect
```

Since the command is executed directly, we don't need to interact with the modified shell.

---

# Understanding SSH Remote Commands

General syntax:

```bash
ssh username@host "command"
```

Examples:

Display current directory:

```bash
ssh user@host "pwd"
```

List files:

```bash
ssh user@host "ls -al"
```

Read a file:

```bash
ssh user@host "cat file.txt"
```

Check the current user:

```bash
ssh user@host "whoami"
```

This feature is commonly used by system administrators to execute commands remotely without opening a full interactive session.

---

# Commands Used

Login normally:

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220
```

List files remotely:

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 "ls -al"
```

Read the password:

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 "cat readme"
```

---

# Key Concepts Learned

- SSH remote command execution
- Interactive vs non-interactive shells
- Purpose of `.bashrc`
- Running commands directly through SSH
- Using `ls -al`
- Reading files with `cat`
- Bypassing login shell restrictions

---

# Lessons Learned

- SSH can execute commands directly on a remote system without opening an interactive shell.
- Login scripts like `.bashrc` can modify or restrict shell behavior.
- Remote command execution is useful when interactive logins are restricted or unavailable.
- Always double-check command syntax. A small typo like `ls-al` instead of `ls -al` results in a "command not found" error.
- Knowing how SSH handles remote commands is valuable for both Linux administration and cybersecurity tasks.

---

# Commands Summary

```bash
# Normal login (fails because of modified .bashrc)
ssh bandit18@bandit.labs.overthewire.org -p 2220

# Execute a remote command
ssh bandit18@bandit.labs.overthewire.org -p 2220 "ls -al"

# Read the password
ssh bandit18@bandit.labs.overthewire.org -p 2220 "cat readme"
```