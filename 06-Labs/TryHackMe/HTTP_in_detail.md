# TryHackMe — HTTP in Detail

**Platform:** TryHackMe  
**Room:** HTTP in Detail  
**Date:** July 19, 2026

---

# What is HTTP?

**HTTP (HyperText Transfer Protocol)** is the protocol used by browsers and web servers to communicate.

Whenever I visit a website, my browser sends an HTTP request to the server, and the server responds with the requested content such as HTML, CSS, JavaScript, images, or videos.

---

# What is HTTPS?

**HTTPS (HyperText Transfer Protocol Secure)** is the secure version of HTTP.

It encrypts the communication between the browser and the server, which helps:

- Protect data from being intercepted.
- Verify that I'm communicating with the real server.

Default ports:

- HTTP → **80**
- HTTPS → **443**

---

# URL Structure

Example:

```
https://user:password@tryhackme.com:443/view-room?id=1#task3
```

| Part | Purpose |
|------|---------|
| Scheme | Protocol (HTTP, HTTPS, FTP) |
| User | Username for authentication |
| Host | Domain name or IP address |
| Port | Communication port (80, 443, etc.) |
| Path | Resource or file being requested |
| Query String | Extra data sent to the server |
| Fragment | Specific location on the page |

---

# HTTP Request

A browser sends a request like:

```http
GET / HTTP/1.1

Host: tryhackme.com
User-Agent: Firefox
```

Important parts:

- **GET** → Request method
- **Host** → Website being requested
- **User-Agent** → Browser information

---

# HTTP Response

Example:

```http
HTTP/1.1 200 OK

Content-Type: text/html
Content-Length: 98
```

Important headers:

- **200 OK** → Request succeeded
- **Content-Type** → Type of returned data
- **Content-Length** → Size of response

---

# HTTP Methods

## GET

Retrieves information from the server.

Example:

- Opening a webpage
- Viewing a profile

---

## POST

Sends data to create something new.

Example:

- Registering a new account
- Posting a comment

---

## PUT

Updates existing data.

Example:

- Changing my email address
- Editing profile information

---

## DELETE

Removes existing data.

Example:

- Deleting a photo
- Removing a post

---

# HTTP Status Codes

Every HTTP response starts with a **status code** that tells me whether my request was successful or if something went wrong.

I remember them by looking at the **first digit**:

| Range | Meaning |
|--------|---------|
| 1xx | Information |
| 2xx | Success |
| 3xx | Redirection |
| 4xx | Client Error |
| 5xx | Server Error |

### 2xx — Success

The request worked successfully.

Common examples:

- **200 OK** → Request completed successfully.
- **201 Created** → A new resource was created (new account, new blog post).

---

### 3xx — Redirection

The server tells the browser to go somewhere else.

Examples:

- **301 Moved Permanently** → Page has permanently moved.
- **302 Found** → Temporary redirect.

---

### 4xx — Client Errors

These usually mean **I made a mistake** in my request.

Examples:

- **400 Bad Request** → Invalid request.
- **401 Unauthorized** → Need to log in first.
- **403 Forbidden** → Logged in, but no permission.
- **404 Not Found** → Requested page doesn't exist.
- **405 Method Not Allowed** → Wrong HTTP method used.

**Easy way to remember:**  
**4xx = Something is wrong on the client (my side).**

---

### 5xx — Server Errors

These mean the request reached the server, but **the server failed to process it**.

Examples:

- **500 Internal Server Error** → Unexpected server problem.
- **503 Service Unavailable** → Server is overloaded or under maintenance.

**Easy way to remember:**  
**5xx = Problem on the server's side, not mine.**

---

# Common HTTP Headers

## Request Headers

Headers sent from the browser to the server.

| Header | Purpose |
|---------|----------|
| Host | Website being requested |
| User-Agent | Browser information |
| Content-Length | Size of data being sent |
| Accept-Encoding | Compression methods supported |
| Cookie | Sends stored cookies to the server |

---

## Response Headers

Headers sent from the server to the browser.

| Header | Purpose |
|---------|----------|
| Set-Cookie | Creates or updates cookies |
| Content-Type | Type of returned data |
| Cache-Control | How long content should be cached |
| Content-Encoding | Compression used |

---

# Cookies in HTTP

The server creates cookies using the **Set-Cookie** response header.

Example:

```http
Set-Cookie: name=adam
```

The browser stores this cookie.

On future requests, the browser automatically sends it back using:

```http
Cookie: name=adam
```

This is how websites remember logged-in users and other preferences.

---

