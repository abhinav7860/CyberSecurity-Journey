# OverTheWire Bandit — Level 13 → Level 14

**Platform:** OverTheWire  
**Game:** Bandit  
**Date:** July 20, 2026

---

# Objective

The password for the next level is stored in /etc/bandit_pass/bandit14 and can only be read by user bandit14. For this level, you don’t get the next password, but you get a private SSH key that can be used to log into the next level. Note: localhost is a hostname that refers to the machine you are working on.

This level teaches how SSH key authentication works.

---

# What I Learned

- SSH can authenticate using a **private key** instead of a password.
- `localhost` always refers to the machine you are currently using.
- SSH private keys must have secure file permissions.
- File permissions are very important when working with SSH.

---

# Step 1 - Login to Bandit13

Login using the password from the previous level.

```bash
ssh -p 2220 bandit13@bandit.labs.overthewire.org
```

After logging in, list the files.

```bash
ls
```

Output:

```text
HINT
sshkey.private
```

I noticed a file called `sshkey.private`.

---

# Step 2 - First Attempt (Mistake)

I tried logging into bandit14 from inside the Bandit server.

```bash
ssh -i sshkey.private bandit14@localhost -p 2200
```

Output:

```text
Connection refused
```

I then tried:

```bash
ssh -i sshkey.private bandit14@localhost -p 2220
```

Output:

```text
Connecting from localhost is blocked.
```

---

## Mistake #1

I assumed I should SSH into **localhost**.

This is wrong.

### Why?

`localhost` means **the machine you are currently on**.

Since I was already inside the Bandit server,

```text
localhost
```

actually meant

```text
Bandit Server
```

So I was trying to SSH **from Bandit back into Bandit**.

OverTheWire blocks this to reduce unnecessary SSH connections.

**Lesson:**

Always think about **which machine you are currently on** before using `localhost`.

---

# Step 3 - Copy the Private Key

Display the private key.

```bash
cat sshkey.private
```

Copy everything including:

```text
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

Exit Bandit.

```bash
exit
```

---

# Step 4 - Save the Key on Kali

Back on my Kali machine, I created a new file.

```bash
nano sshkey.private
```

Then I pasted the entire private key and saved it.

---

# Step 5 - Check File Permissions

I checked the permissions.

```bash
ll
```

Output:

```text
-rw-rw-r--
```

Meaning:

```
Owner
    Read ✔
    Write ✔

Group
    Read ✔
    Write ✔

Others
    Read ✔
```

This is **not secure** for a private SSH key.

---

# Mistake #2

I tried:

```bash
chmod +x sshkey.private
```

Permissions became:

```text
-rwxrwxr-x
```

### Why this was wrong

`+x` means

> Give execute permission.

SSH keys are **not executable files**.

They are simply secret text files.

Adding execute permission does nothing useful.

Even worse, the key was still readable by other users.

SSH does not like insecure private keys.

**Lesson:**

`chmod +x` is used for:

- Shell scripts
- Python scripts
- Programs

NOT for SSH keys.

---

# Step 6 - Correct the Permissions

I changed the permissions.

```bash
chmod 700 sshkey.private
```

Now only I can access the file.

Permissions became:

```text
rwx------
```

This means:

```
Owner
Read ✔
Write ✔
Execute ✔

Group
No access

Others
No access
```

The more common permission is:

```bash
chmod 600 sshkey.private
```

which gives:

```
rw-------
```

Both work because other users cannot access the file.

---

## Why does SSH care?

A private key is like your password.

If anyone else can read it, they can log in as you.

So SSH checks the permissions before using the key.

If the permissions are too open, SSH refuses to use it.

---

# Step 7 - Login Using the Private Key

Instead of using localhost, I connected directly to the Bandit server.

```bash
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220
```

Explanation:

```
-i
```

Use this private key.

```
bandit14
```

User I want to log in as.

```
-p 2220
```

SSH port.

This successfully logged me into **bandit14**.

---

# Step 8 - Read the Password

Now I can read the password.

```bash
cat /etc/bandit_pass/bandit14
```

Output:

```text
aaWecNkG4FhxJQxz07uiwzVP6bJiYS65
```

This is the password for **Bandit Level 14**.

---

# Commands Used

```bash
ssh -p 2220 bandit13@bandit.labs.overthewire.org

ls

cat sshkey.private

exit

nano sshkey.private

ll

chmod +x sshkey.private      # Wrong

chmod 700 sshkey.private

ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220

cat /etc/bandit_pass/bandit14
```

---

# Mistakes I Made

### Mistake 1

Tried:

```bash
ssh -i sshkey.private bandit14@localhost -p 2220
```

Why it failed:

I was already inside the Bandit server.

`localhost` referred to the Bandit server itself, so I was trying to SSH back into the same machine.

The server blocks localhost SSH connections.

---

### Mistake 2

Used:

```bash
chmod +x sshkey.private
```

This only adds execute permission.

SSH keys don't need execute permission.

The correct approach is to make the file private.

```bash
chmod 600 sshkey.private
```

or

```bash
chmod 700 sshkey.private
```

---

### Mistake 3

I kept trying to connect to:

```bash
localhost
```

even after copying the key to Kali.

Since the key was now on my own machine, I needed to connect to the actual server.

Correct command:

```bash
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220
```

---

# Revision Notes

## SSH Login with Password

```bash
ssh username@host
```

Example:

```bash
ssh bandit13@bandit.labs.overthewire.org -p 2220
```

---

## SSH Login with Private Key

```bash
ssh -i private_key username@host
```

Example:

```bash
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220
```

---

## What is localhost?

`localhost` always points to the computer you are currently using.

Examples:

If I'm on Kali:

```
localhost
↓

My Kali machine
```

If I'm inside Bandit:

```
localhost
↓

Bandit server
```

Always remember where you are before using `localhost`.

---


# Password for the next level was -

```text
aaWecNkG4FhxJQxz07uiwzVP6bJiYS65
```