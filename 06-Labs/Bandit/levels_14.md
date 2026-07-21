# OverTheWire Bandit Level 14 → Level 15

## Objective

The password for the next level can be retrieved by submitting the password of the current level to port 30000 on localhost.
---

# Step 1: Login to Bandit14

The previous level provided an SSH private key instead of a password. I used that private key to log in to the Bandit server.

```bash
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220
```

### Explanation

- `ssh` → Secure Shell client
- `-i sshkey.private` → Uses the private key for authentication
- `bandit14@bandit.labs.overthewire.org` → Username and server
- `-p 2220` → Connects to port **2220**

---

# Step 2: Read the Current Password

The password for the current level is stored in:

```text
/etc/bandit_pass/bandit14
```

Read it using:

```bash
cat /etc/bandit_pass/bandit14
```

This prints the current password to the terminal.

---

# Step 3: Initial Mistake

Initially, I tried:

```bash
cat /etc/bandit_pass/bandit14 | nc localhost -p 30000
```

Result:

```text
usage: nc ...
```

### Why did this fail?

The `-p` option **does not specify the destination port**.

Instead, it specifies the **source port** that Netcat should use.

The challenge requires connecting **to** port **30000**, so the correct syntax is:

```bash
nc <host> <destination_port>
```

---

# Step 4: Connect to the Service

The correct command is:

```bash
cat /etc/bandit_pass/bandit14 | nc localhost 30000
```

Output:

```text
Correct!
Password retrieved successfully.
```

The service validates the password and returns the password for the next level.

---

# Why Was Netcat (`nc`) Used?

The objective of this level was **not just to read the password**, but to **submit it to a service running on localhost port 30000**.

The challenge teaches how to communicate with a network service instead of simply reading files.

The password stored inside `/etc/bandit_pass/bandit14` had to be sent over a **TCP connection** to a program listening on **port 30000**.

Netcat (`nc`) is a lightweight networking utility that can:

- Connect to TCP/UDP services
- Send data
- Receive responses
- Test network services

---

## How the Command Works

```bash
cat /etc/bandit_pass/bandit14 | nc localhost 30000
```

### Workflow

```text
Read password
        │
        ▼
cat /etc/bandit_pass/bandit14
        │
        ▼
Pipe (|)
        │
        ▼
Netcat (nc)
        │
        ▼
Connect to localhost:30000
        │
        ▼
Send password
        │
        ▼
Server verifies password
        │
        ▼
Returns password for Bandit Level 15
```

---

# Understanding the Pipe (`|`)

The pipe operator (`|`) sends the output of one command as the input to another.

Example:

```bash
cat /etc/bandit_pass/bandit14 | nc localhost 30000
```

What happens:

1. `cat` reads the password.
2. The pipe (`|`) forwards that output.
3. Netcat sends it over the TCP connection.
4. The server validates it.
5. The server returns the next password.

---

# Why Not Just Use `cat`?

Using:

```bash
cat /etc/bandit_pass/bandit14
```

only prints the password on the screen.

It **does not send** the password anywhere.

The challenge specifically requires submitting the password to a service.

---

# Why Not Use SSH?

SSH is used to log into a remote machine.

In this level:

- I was already logged into the Bandit server.
- The requirement was to communicate with a **TCP service**, not another machine.

Netcat is the correct tool because it communicates directly with TCP services.

---

# Concepts Learned

## SSH

Used to securely log into remote systems.

Example:

```bash
ssh user@host
```

---

## Netcat (`nc`)

Netcat is a networking utility used to:

- Connect to TCP services
- Connect to UDP services
- Send and receive data
- Test open ports
- Troubleshoot network services

General syntax:

```bash
nc <host> <port>
```

Example:

```bash
nc localhost 30000
```

---

## Localhost

`localhost` refers to the current machine.

Instead of connecting to another computer, the connection is made to a service running on the same system.

---

## TCP Port

A port identifies a specific network service.

Here:

```text
Host : localhost
Port : 30000
```

The service was listening on TCP port **30000**, waiting for the password.

---

# Commands Used

```bash
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220

cat /etc/bandit_pass/bandit14

cat /etc/bandit_pass/bandit14 | nc localhost 30000
```

---

# Mistakes I Made

### Incorrect Command

```bash
nc localhost -p 30000
```

### Why it was wrong

The `-p` option sets the **source port**, not the destination port.

### Correct Command

```bash
nc localhost 30000
```

---
