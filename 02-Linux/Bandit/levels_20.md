# OverTheWire Bandit: Level 20 → Level 21 
**Date:** 24 July 2026

---

# Objective

There is a setuid binary in the homedirectory that does the following: it makes a connection to localhost on the port you specify as a commandline argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).


The binary:

- Connects to **localhost** on a port that we specify.
- Reads one line of text from that connection.
- Compares the received text with the **Bandit20 password**.
- If the password matches, it returns the password for **Bandit21**.

---

# Understanding the Concept

This level introduces **network communication between processes** using **Netcat (nc)**.

Instead of reading a password from a file, we need to:

1. Start our own TCP server (listener).
2. Make the provided binary connect to our listener.
3. Send the correct Bandit20 password.
4. Receive the Bandit21 password.

---

# Important Commands

| Command | Purpose |
|----------|---------|
| `nc` (Netcat) | Creates TCP/UDP connections and listeners |
| `jobs` | Shows background jobs |
| `&` | Runs a process in the background |
| `./suconnect` | Connects to a localhost port and validates the password |

---

# Step 1 - Check the Home Directory

List the available files.

```bash
ls
```

Output

```text
suconnect
```

The executable provided for this level is **suconnect**.

---

# Step 2 - Create a Local Listener

We need a TCP server that returns the **Bandit20 password** whenever a client connects.

Command

```bash
echo "4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA" | nc -l -p 1244 &
```

Output

```text
[1] 47
```

### Command Breakdown

```bash
echo "password"
```

Prints the Bandit20 password.

---

```bash
|
```

The pipe (`|`) sends the password directly into Netcat.

---

```bash
nc
```

Starts Netcat.

---

```bash
-l
```

Listen mode.

Instead of connecting to another system, Netcat waits for incoming connections.

---

```bash
-p 1244
```

Tells Netcat to listen on port **1244**.

Any unused port can be chosen.

---

```bash
&
```

Runs the listener in the **background**.

Without it, the terminal would remain occupied by Netcat.

---

# Step 3 - Verify the Background Job

Check that the listener is running.

```bash
jobs
```

Output

```text
[1]+ Running echo "4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA" | nc -l -p 1244 &
```

The listener is now waiting for incoming connections.

---

# Step 4 - Run the suconnect Binary

Now make the binary connect to the listener.

```bash
./suconnect 1244
```

Output

```text
Read: 4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA
Password matches, sending next password

bW9kBv5WC3P4yoDyf12LSdGuNz5ka6hY
```

The binary connected to our Netcat listener, received the password, verified it, and returned the password for **Bandit21**.

---

# Step 5 - Background Job Ends

After the connection is complete, the Netcat listener exits automatically.

Output

```text
[1]+ Done
```

This happens because Netcat handled one connection and then terminated.

---

# Commands Used

```bash
ls

echo "4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA" | nc -l -p 1244 &

jobs

./suconnect 1244
```

---

# How the Communication Works

```
                Bandit20 Shell

                       │
                       │
                       ▼

      echo "Bandit20 Password"

                       │
                       ▼

      Netcat Listener (Port 1244)

                       ▲
                       │
                       │
                suconnect Binary
              (Connects to localhost)

                       │
             Reads one line of text
                       │
                       ▼

      Compares with Bandit20 Password

               If Password Matches

                       ▼

        Sends Bandit21 Password
```

---

# Key Concepts Learned

## Netcat (nc)

Netcat is often called the **Swiss Army Knife of Networking**.

It can:

- Listen on ports
- Connect to remote systems
- Transfer files
- Test services
- Debug network connections

Example

```bash
nc -l -p 1234
```

Creates a TCP listener on port **1234**.

---

## Localhost

The binary connects to:

```
localhost
```

or

```
127.0.0.1
```

This is the local machine itself.

No external network communication occurs.

---

## Background Processes

Adding

```bash
&
```

runs the command in the background.

This allows the same terminal to execute additional commands.

Example

```bash
python3 -m http.server &
```

---

## Job Control

Linux keeps track of background processes.

Useful command

```bash
jobs
```

Example output

```text
[1]+ Running
```

This shows that the Netcat listener is still active.

---

## Pipes (`|`)

The pipe operator sends the output of one command as the input to another.

Example

```bash
echo "Hello" | wc
```

Instead of saving output to a file, it is directly passed to the next command.

In this level:

```bash
echo "password" | nc -l -p 1244
```

The password is sent directly to the client when it connects.

---

