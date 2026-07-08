# Day 10 - Client-Server Model & Network Services

# 1. Client and Server

A client is a device or application that requests a service.

A server is a device or application that provides the requested service.

Example:

```
My Browser (Client)
        ↓
Web Server
        ↓
Returns the website
```

Examples:
- Chrome → Client
- Gmail Server → Server
- YouTube Server → Server

---

# 2. Client-Server Communication

A client requests a service.

The server processes the request and sends back the response.

Example:

```
Browser
     ↓ HTTP Request
Web Server
     ↓ HTML Response
Browser displays the website
```

---

# 3. URI, URL and URN

A URI (Uniform Resource Identifier) identifies a resource.

Example:

```
https://www.example.com/author/book.html#page155
```

### URI

The complete address.

```
https://www.example.com/author/book.html#page155
```

### URL

Specifies where the resource is located.

```
https://www.example.com/author/book.html
```

### URN

Identifies the resource without the protocol.

```
www.example.com/author/book.html
```

### Fragment

Points to a specific section.

```
#page155
```

---

# 4. Common Network Services

### DNS

Converts domain names into IP addresses.

Example:

```
google.com
↓

142.250.x.x
```

---

### HTTP

Used to load web pages.

Default Port:

```
80
```

---

### HTTPS

Secure version of HTTP using encryption.

Default Port:

```
443
```

---

### FTP

Transfers files between client and server.

Ports:

```
21 → Control
20 → Data Transfer
```

---

### DHCP

Automatically assigns:

- IP Address
- Subnet Mask
- Default Gateway
- DNS Server

Ports:

```
67 → Server
68 → Client
```

---

### SSH

Provides secure remote login.

Port:

```
22
```

---

### Telnet

Provides remote login without encryption.

Port:

```
23
```

Not recommended because usernames and passwords are sent in plain text.

---

# 5. HTTP Request Flow

When opening a website:

```
Browser

↓

DNS finds the server IP

↓

HTTP Request

↓

Web Server

↓

HTML Page

↓

Browser displays the website
```

HTTPS works the same way but encrypts the communication.

---

# 6. FTP

FTP allows uploading and downloading files.

Uses two connections:

- Control Connection (Port 21)
- Data Connection (Port 20)

Example:

```
FTP Client
      ↓
FTP Server
```

---

# 7. Telnet vs SSH

### Telnet

- Port 23
- No encryption
- Password sent as plain text
- Not secure

### SSH

- Port 22
- Encrypted communication
- Secure authentication
- Recommended for remote access

---

# 8. Email Protocols

### SMTP

Used to send emails.

Port:

```
25
```

---

### POP3

Downloads emails from the server.

By default, emails are removed from the server after downloading.

Port:

```
110
```

---

### IMAP

Keeps emails stored on the server.

Allows access from multiple devices.

Port:

```
143
```

---

# 9. Email Flow

```
Sender

↓

SMTP

↓

Mail Server

↓

Recipient Mail Server

↓

POP3 / IMAP

↓

Recipient
```

SMTP sends emails.

POP3 and IMAP retrieve emails.

---

# 10. Instant Messaging

Applications like:

- WhatsApp
- Microsoft Teams
- Webex
- Messenger

allow users to send messages, files, images, and videos over the internet.

---

# 11. VoIP (Voice over IP)

VoIP converts voice into digital packets and sends them over the internet.

Examples:

- WhatsApp Call
- Microsoft Teams Call
- Zoom
- Google Meet

---

# Commands Practiced

### DNS Lookup

```bash
nslookup google.com
```

Example Output:

```
Server: 8.8.8.8
Address: 142.250.xx.xx
```

Used to find the IP address of a domain.

---

