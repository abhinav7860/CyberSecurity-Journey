# OverTheWire Bandit Level 15 → Level 16

## Objective

The goal of this level is to retrieve the password for **Bandit Level 16**.

Unlike the previous level, the service listening on **localhost port 30001** only accepts connections using **SSL/TLS encryption**. Therefore, a normal TCP connection is not sufficient.

---

# Step 1: Login to Bandit15

Login using SSH.

```bash
ssh bandit15@bandit.labs.overthewire.org -p 2220
```

---

# Step 2: Read the Current Password

The current level password is stored in:

```text
/etc/bandit_pass/bandit15
```

Read it using:

```bash
cat /etc/bandit_pass/bandit15
```

---

# Step 3: First Attempt Using Netcat

I first tried connecting with Netcat.

```bash
nc localhost 30001
```

Nothing happened.

After typing the password, there was no useful response.

---

# Why Didn't Netcat Work?

Netcat (`nc`) creates a **normal TCP connection**.

However, the service on **port 30001** expects an **SSL/TLS encrypted connection**.

Since Netcat cannot automatically perform the SSL/TLS handshake, the server does not accept normal TCP communication.

---

# What is SSL/TLS?

SSL (Secure Sockets Layer) and TLS (Transport Layer Security) are protocols used to encrypt communication between a client and a server.

Instead of sending plain text over the network, the data is encrypted.

Examples:

- HTTPS
- Secure Email
- Online Banking
- SSH

This challenge requires talking to the server securely.

---

# Why Use OpenSSL?

OpenSSL is a tool used to create encrypted SSL/TLS connections.

It can:

- Connect securely to servers
- Test SSL/TLS services
- View certificates
- Perform SSL/TLS handshakes

Since port **30001** requires encryption, OpenSSL is the correct tool.

---

# Step 4: Connect Using OpenSSL

Use:

```bash
openssl s_client -connect localhost:30001
```

After the SSL connection is established, enter the current password.

```text
Current Password
```

Output:

```text
Correct!
Password retrieved successfully.
```

---

# Understanding the Command

```bash
openssl s_client -connect localhost:30001
```

### Explanation

- `openssl` → OpenSSL program
- `s_client` → Creates an SSL/TLS client
- `-connect` → Specifies the server to connect to
- `localhost:30001` → Target server and port

---

# How It Works

```text
Current Password
        │
        ▼
OpenSSL Client
        │
        ▼
TLS Handshake
        │
        ▼
Encrypted Connection
        │
        ▼
Send Password
        │
        ▼
Server verifies password
        │
        ▼
Returns Bandit Level 16 password
```

---

# What is a TLS Handshake?

Before any encrypted communication begins, both the client and server perform a **TLS Handshake**.

During this process they:

- Agree on the encryption method.
- Exchange certificates.
- Create secure encryption keys.
- Start encrypted communication.

Only after the handshake is complete can the password be safely sent.

---

# Certificate Information

While connecting, OpenSSL displayed information about the server certificate.

Example:

```text
subject=CN=SnakeOil
issuer=CN=SnakeOil
```

The certificate is **self-signed**, which is expected in this Bandit challenge.

---

# Netcat vs OpenSSL

| Netcat (`nc`) | OpenSSL (`openssl s_client`) |
|---------------|------------------------------|
| Normal TCP connection | Encrypted SSL/TLS connection |
| Does not perform TLS handshake | Performs TLS handshake |
| Used for plain TCP/UDP services | Used for secure services |
| Cannot communicate with SSL-only services | Can communicate with SSL-enabled services |

---

# Why Not Use Netcat?

Netcat only sends plain text.

```text
You
   │
   ▼
Plain TCP
   │
   ▼
Server requiring TLS
   │
   ▼
Connection fails
```

The server expects encrypted communication.

---

# Why OpenSSL Works

OpenSSL first creates the secure connection.

```text
You
   │
   ▼
TLS Handshake
   │
   ▼
Encrypted Tunnel
   │
   ▼
Send Password
   │
   ▼
Server accepts password
```

Because the connection is encrypted, the server accepts the password and returns the next one.

---

# Commands Used

```bash
ssh bandit15@bandit.labs.overthewire.org -p 2220

cat /etc/bandit_pass/bandit15

nc localhost 30001

openssl s_client -connect localhost:30001
```

---

# Mistakes I Made

### First Attempt

```bash
nc localhost 30001
```

This did not work because the service expected SSL/TLS encryption.

### Correct Command

```bash
openssl s_client -connect localhost:30001
```

---

