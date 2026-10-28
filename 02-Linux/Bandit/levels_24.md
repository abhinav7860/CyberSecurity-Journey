# OverTheWire Bandit Level 24 → 25
**Level:** 24 → 25    
**Date:** 26 July 2026

---

# Objective

The goal of this level is to retrieve the password for **bandit25**.

A daemon is listening on **localhost port 30002**. It expects:

1. The current password for **bandit24**
2. A **4-digit numeric PIN**

If both are correct, it returns the password for the next level.

---

# Understanding the Challenge

Unlike previous Bandit levels, this challenge requires brute-forcing a **4-digit PIN** while using the already known password.

Since a 4-digit PIN ranges from **0000** to **9999**, there are only **10,000 possible combinations**. Instead of trying each PIN manually, we can automate the process using a Bash script.

---

# Step 1: Create a Working Directory

The Bandit home directory is read-only, so it's recommended to work inside `/tmp`.

```bash
mkdir /tmp/bar
cd /tmp/bar
```

---

# Step 2: Create the Bash Script

Create a new file.

```bash
nano script.sh
```

Add the following script:

```bash
#!/bin/bash

for i in {0..9}{0..9}{0..9}{0..9}
do
    echo "hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv $i" >> list.txt
done
```

Save and exit.

---

# Step 3: Make the Script Executable

```bash
chmod +x script.sh
```

Execute it.

```bash
./script.sh
```

This generates a file named **list.txt** containing every possible password + PIN combination.

Example:

```text
hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv 0000
hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv 0001
hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv 0002
...
hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv 9999
```

---

# Step 4: Send Every Combination to the Server

Use **Netcat (nc)** to send the contents of the file to the daemon.

```bash
cat list.txt | nc localhost 30002
```

The server checks every line until it finds the correct PIN.

Output:

```text
Wrong!
Wrong!
Wrong!
...
Correct!
The password of user bandit25 is
SoHfqMOEqIX2IYKVciZxvgpR9a2Djx4P
```

---

# Password Obtained

```text
SoHfqMOEqIX2IYKVciZxvgpR9a2Djx4P
```

---

# Explanation of the Script

### Shebang

```bash
#!/bin/bash
```

The first line tells Linux to execute the script using the Bash shell.

> **Note:** I initially wrote `!#/bin/bash`, which caused the following error:

```text
./script.sh: line 1: !#/bin/bash: No such file or directory
```

Correcting it to `#!/bin/bash` fixed the issue.

---

## The For Loop

```bash
for i in {0..9}{0..9}{0..9}{0..9}
```

Brace expansion generates every four-digit number:

```text
0000
0001
0002
...
9999
```

This creates exactly **10,000** possible PIN combinations.

---

## Echo Command

```bash
echo "password $i"
```

Each iteration prints:

```text
password 0000
password 0001
password 0002
...
```

For this level, the server expects:

```text
current_password PIN
```

Therefore each generated line follows that format.

---

## Output Redirection

```bash
>>
```

The append operator (`>>`) adds each new line to the existing file.

Example:

```bash
echo hello >> file.txt
echo world >> file.txt
```

Result:

```text
hello
world
```

Using `>` instead would overwrite the file every iteration, leaving only the last line.

---

# Understanding Netcat

The command

```bash
cat list.txt | nc localhost 30002
```

works as follows:

### Step 1

```bash
cat list.txt
```

Prints the contents of the file.

---

### Step 2

```bash
|
```

The pipe (`|`) sends the output of one command as the input to another.

---

### Step 3

```bash
nc localhost 30002
```

Netcat connects to:

- Host: `localhost`
- Port: `30002`

The daemon reads each line until the correct password and PIN combination is received.

---

# Workflow

```text
Create Bash Script
        │
        ▼
Generate 10,000 PIN combinations
        │
        ▼
Store them in list.txt
        │
        ▼
cat list.txt
        │
        ▼
Pipe (|)
        │
        ▼
Netcat connects to localhost:30002
        │
        ▼
Server validates each PIN
        │
        ├── Wrong
        ├── Wrong
        ├── Wrong
        │
        ▼
Correct PIN Found
        │
        ▼
Returns Bandit25 Password
```

---

# Commands Used

```bash
mkdir /tmp/bar
cd /tmp/bar

nano script.sh

chmod +x script.sh

./script.sh

cat list.txt | nc localhost 30002
```

---

# Key Concepts Learned

- Working in temporary directories (`/tmp`)
- Writing executable Bash scripts
- Understanding the shebang (`#!/bin/bash`)
- Using `chmod +x` to make scripts executable
- Automating repetitive tasks with `for` loops
- Using brace expansion to generate combinations
- Difference between `>` and `>>`
- File redirection
- Pipes (`|`)
- Using Netcat (`nc`) to communicate with network services
- Automating a brute-force attack against a service

---
