# OverTheWire Bandit Level 16 → 17

## Objective

Obtain the credentials for **bandit17** by finding the correct SSL/TLS service running on localhost between ports **31000–32000**.

---

# Step 1 – Scan for Open Ports

First, scan the required port range using **Nmap**.

```bash
nmap -p 31000-32000 localhost
```

Output showed the following open ports:

```
31046
31518
31691
31790
31960
```

Not every open port uses SSL/TLS, so each one must be tested.

---

# Step 2 – Test SSL/TLS Services

Use OpenSSL to connect to each port.

```bash
openssl s_client -connect localhost:<port>
```

---

## Port 31046

```bash
openssl s_client -connect localhost:31046
```

Result:

```
No peer certificate available
```

This indicates the service is **not using SSL/TLS**.

---

## Port 31518

```bash
openssl s_client -connect localhost:31518
```

After entering the Bandit16 password, OpenSSL returned a **KEY UPDATE** message instead of the expected response.

### Why?

By default, `openssl s_client` runs in **interactive mode**.

Certain characters are interpreted as OpenSSL commands instead of normal input.

Our Bandit password starts with:

```
k
```

According to the OpenSSL manual:

```
k
```

requests a TLS Key Update instead of sending the character to the server.

---

## Fix

Disable interactive mode using the **-quiet** option.

```bash
openssl s_client -quiet -connect localhost:31518
```

This sends the password correctly.

However, this port simply echoed the password back and was **not the correct service**.

---

## Port 31691

```bash
openssl s_client -quiet -connect localhost:31691
```

Result:

Connection failed or produced an error.

Move on to the next port.

---

## Port 31790

```bash
openssl s_client -quiet -connect localhost:31790
```

Enter the Bandit16 password.

This time the server replied:

```
Correct!
```

followed by an **OpenSSH Private Key**.

This is the SSH key required to log into **bandit17**.

---

# Step 3 – Save the Private Key

Copy the private key into a file.

Example:

```bash
nano banditpass.private
```

Paste:

```
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

Save the file.

---

# Step 4 – Change File Permissions

SSH refuses to use private keys that are accessible by other users.

Restrict the permissions:

```bash
chmod 600 banditpass.private
```

Verify:

```bash
ls -l banditpass.private
```

Expected:

```text
-rw------- banditpass.private
```

Only the file owner can read and write it.

---

# Step 5 – Login Using the Private Key

Use SSH with the private key.

```bash
ssh -i banditpass.private bandit17@bandit.labs.overthewire.org -p 2220
```

SSH authenticates using the private key instead of a password.

---

# Step 6 – Retrieve the Password

Display the password for Bandit17.

```bash
cat /etc/bandit_pass/bandit17
```

Example output:

```text
pWXMAZoxGC8JmDMfmT5MGEsobMM3vnj2
```

---

# Commands Used

Scan ports:

```bash
nmap -p 31000-32000 localhost
```

Connect with SSL:

```bash
openssl s_client -connect localhost:31518
```

Disable interactive mode:

```bash
openssl s_client -quiet -connect localhost:31518
```

Retrieve SSH key:

```bash
openssl s_client -quiet -connect localhost:31790
```

Restrict key permissions:

```bash
chmod 600 banditpass.private
```

Login using the SSH key:

```bash
ssh -i banditpass.private bandit17@bandit.labs.overthewire.org -p 2220
```

Display password:

```bash
cat /etc/bandit_pass/bandit17
```

---
# Lessons Learned

- Open ports do not necessarily provide the required service.
- `openssl s_client` defaults to interactive mode, which can interfere with passwords beginning with certain characters.
- SSH private keys must have restrictive permissions before they can be used.
- SSH supports both password-based and key-based authentication.
- Always test each service systematically rather than assuming the first SSL-enabled port is the correct one.