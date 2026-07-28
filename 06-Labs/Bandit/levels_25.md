# OverTheWire Bandit Level 25 → 26  
**Level:** 25 → 26   
**Date:** 28 July 2026

---

# Objective

The goal of this level is to obtain the password for **bandit26**.

Unlike previous levels, logging into bandit26 immediately disconnects the session because the user's default shell is **not `/bin/bash`**. The challenge is to identify the shell being used and escape from it to gain access.

---

# Understanding the Challenge

After completing Level 25, I found the following file in the home directory:

```bash
ls
```

Output:

```text
bandit26.sshkey
```

This file contains the **private SSH key** required to authenticate as **bandit26**.

Since I was working from my local Kali machine, I copied the contents of the SSH key into a new file.

---

# Step 1 - Create the SSH Key

Create a new file.

```bash
nano bandit26.sshkey
```

Paste the private RSA key into the file.

Save and exit.

---

# Step 2 - Set Correct Permissions

SSH refuses to use private keys that are accessible by other users.

Set the correct permissions:

```bash
chmod 600 bandit26.sshkey
```

This gives:

- Read
- Write

permissions only to the file owner.

---

# Step 3 - Connect to Bandit26

Use the SSH key for authentication.

```bash
ssh -i bandit26.sshkey bandit26@localhost -p 2220
```

Instead of receiving a shell, the connection immediately closed.

This happens because **bandit26's login shell is not Bash**.

---

# Step 4 - Trigger the `more` Program

I maximized (zoomed) my terminal window before connecting.

When the login banner became long enough, it caused the **more** pager to pause instead of immediately exiting.

At this point, I was inside the **more** program.

---

# Step 5 - Escape into Vim

While inside **more**, I pressed:

```text
v
```

The **v** key opens the current file inside **Vim**.

Now I had access to the Vim editor.

---

# Step 6 - Read the Password File

Inside Vim, I opened the password file using:

```vim
:e /etc/bandit_pass/bandit26
```

Vim displayed the password.

```text
jHdv2ELQhT22BkprMNDjybZDAkw1zeBJ
```

---

# Step 7 - Get a Shell

Instead of exiting Vim, I changed the shell setting.

```vim
:set shell=/bin/bash
```

Then launched a Bash shell directly from Vim.

```vim
:shell
```

I now had an interactive Bash shell running as **bandit26**.

---

# Password Obtained

```text
jHdv2ELQhT22BkprMNDjybZDAkw1zeBJ
```

---

# Commands Used

```bash
ls

nano bandit26.sshkey

chmod 600 bandit26.sshkey

ssh -i bandit26.sshkey bandit26@localhost -p 2220
```

Inside **more**

```text
v
```

Inside **Vim**

```vim
:e /etc/bandit_pass/bandit26

:set shell=/bin/bash

:shell
```

---

# Understanding the Commands

## `chmod 600`

```bash
chmod 600 bandit26.sshkey
```

Sets the permissions to:

```
Owner:
Read
Write

Group:
No permissions

Others:
No permissions
```

SSH requires private keys to be accessible only by their owner.

---

## SSH Using a Private Key

```bash
ssh -i bandit26.sshkey bandit26@localhost -p 2220
```

Options used:

- `-i` → Specifies the private key.
- `localhost` → Connects to the same machine.
- `-p 2220` → Uses the Bandit SSH port.

---

## Why Did the Session Close?

Normally, SSH starts the user's login shell.

Example:

```
/bin/bash
```

However, bandit26 uses a different shell that immediately exits after displaying the banner.

As a result, the SSH session closes before the user can interact with it.

---

## Why Did Zooming the Terminal Help?

The login banner became larger than the visible terminal window.

Linux automatically used the **more** pager to display the overflowing text.

Instead of exiting immediately, the connection paused inside **more**, giving an opportunity to interact with the program.

---

## Escaping from `more`

The **more** pager includes a shortcut:

```text
v
```

Pressing **v** opens the displayed content inside the **Vim** editor.

---

## Opening a File in Vim

Inside Vim:

```vim
:e filename
```

means:

```
Edit another file
```

Example:

```vim
:e /etc/bandit_pass/bandit26
```

This loads the Bandit password file into Vim.

---

## Changing Vim's Shell

Vim normally launches the default shell.

We changed it using:

```vim
:set shell=/bin/bash
```

Now whenever Vim starts a shell, it launches Bash instead.

---

## Starting a Shell

```vim
:shell
```

launches the configured shell.

Since we changed it to Bash, Vim started:

```
/bin/bash
```

giving us an interactive shell running as **bandit26**.

---

# Workflow

```text
Bandit25
      │
      ▼
Find bandit26.sshkey
      │
      ▼
Copy SSH Key
      │
      ▼
chmod 600
      │
      ▼
SSH Login
      │
      ▼
Login banner opens in "more"
      │
      ▼
Press "v"
      │
      ▼
Open Vim
      │
      ▼
:e /etc/bandit_pass/bandit26
      │
      ▼
Read Password
      │
      ▼
:set shell=/bin/bash
      │
      ▼
:shell
      │
      ▼
Interactive Bash Shell
```
