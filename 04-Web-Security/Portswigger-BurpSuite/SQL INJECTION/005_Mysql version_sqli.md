# PortSwigger Web Security Academy – SQL Injection: Database Version (MySQL & Microsoft)

> **Difficulty:** Practitioner  
> **Topic:** SQL Injection / UNION-based SQL Injection  
> **Database:** MySQL / Microsoft SQL Server   
> **Date:** 01 September 2026  
> **Tool:** Burp Suite Community Edition

---

## 1. Lab Objective

The goal of this lab was to exploit a SQL injection vulnerability in the **product category filter** and retrieve the **database version string**.

The important part was not just solving the lab, but understanding:

- How to identify a SQL injection point
- Why Burp Repeater is useful
- How `UNION SELECT` works
- How to determine the number of columns
- Why `NULL` is used
- What `#` means in MySQL
- What `@@version` does
- How the injected query is reflected in the application response

---

## 2. What is SQL Injection?

SQL Injection happens when user-controlled input is inserted into a SQL query without proper protection.

For example, an application might internally construct something like:

```sql
SELECT name, description
FROM products
WHERE category = '<USER_INPUT>'
```

If the application directly places our input into the query, we may be able to change the meaning of the SQL statement.

Instead of supplying only a normal category such as:

```text
Corporate gifts
```

we can test whether special SQL syntax changes the application's behavior.

---

# 3. Why Burp Repeater?

### What is Burp Repeater?

Burp Repeater allows us to take an HTTP request and **send it repeatedly while changing individual parts of the request**.

This is extremely useful during SQL injection testing.

Instead of repeatedly:

1. Going to the browser
2. Selecting a category
3. Sending the request
4. Looking at the result

we can send the same request directly from Burp and change only the `category` parameter.

### In this lab

The interesting request was:

```http
GET /filter?category=Corporate+gifts
```

We sent this request to **Burp Repeater**.

Then we could test different SQL payloads without constantly interacting with the browser.

### Simple way to remember

> **Proxy = capture the request**  
> **Repeater = modify and test the request**

---

# 4. Finding the Injection Point

The vulnerable parameter was:

```text
category
```

The normal request looked similar to:

```http
GET /filter?category=Corporate+gifts
```

We then modified the value of `category` and observed how the server responded.

This indicated that the parameter was being used in a SQL query.

---

# 5. Testing the Number of Columns

Before using `UNION SELECT`, we need to know how many columns the original SQL query returns.

The lab solution indicates that the query returns **2 columns**.

We tested this using:

```sql
'+UNION+SELECT+'abc','def'#
```

In SQL form, this is:

```sql
' UNION SELECT 'abc','def'#
```

The application response displayed:

```text
abc
```

and:

```text
def
```

This confirmed that:

- The SQL injection worked.
- The `UNION SELECT` was accepted.
- The original query has **2 columns**.
- Both columns can contain text.

---

# 6. Understanding UNION SELECT

`UNION` combines the results of two SQL queries.

For example:

```sql
SELECT column1, column2 FROM products
UNION
SELECT 'abc', 'def'
```

The important rule is that both queries must have a compatible number of columns.

If the original query returns:

```text
2 columns
```

our injected `SELECT` also needs:

```text
2 columns
```

Therefore:

```sql
UNION SELECT @@version, NULL
```

has two columns:

```text
Column 1 → @@version
Column 2 → NULL
```

---

# 7. Why Did We Use NULL?

Our final payload was:

```sql
' UNION SELECT @@version, NULL#
```

The `NULL` is used because we only need useful information from the first column.

Think of it like:

```text
Column 1          Column 2
---------         ---------
@@version         NULL
```

`@@version` gives us the database version.

`NULL` simply fills the second required column.

---

# 8. Final Payload

The final payload used in the lab was:

```text
'+UNION+SELECT+@@version,+NULL#
```

Decoded into normal SQL:

```sql
' UNION SELECT @@version, NULL#
```

### Breaking it down

#### `'`

```sql
'
```

This closes the original string value in the SQL query.

---

#### `UNION`

```sql
UNION
```

Allows us to combine the original query's result with our injected query.

---

#### `SELECT`

```sql
SELECT
```

Tells the database that we want to retrieve values.

---

#### `@@version`

```sql
@@version
```

MySQL's system variable that returns the database/server version information.

---

#### `NULL`

```sql
NULL
```

Provides the second column required by the original query.

---

#### `#`

```sql
#
```

This is a **MySQL comment marker**.

Everything after `#` on that line is treated as a comment.

This is useful because the original application may append additional SQL after our input.

So instead of allowing the rest of the original query to interfere with our injection, we comment it out.

---

# 9. Why is `#` Different From the Oracle Lab?

In the previous Oracle SQL injection lab, the comment syntax was:

```sql
--
```

For this MySQL lab we used:

```sql
#
```

Different database systems support different SQL syntax.

### MySQL

```sql
#
```

is a single-line comment.

### Oracle

A common single-line comment is:

```sql
--
```

This is one reason it is important to identify the database type before choosing payload syntax.

---

# 10. Why Are There `+` Signs?

The request is being sent through a URL.

Spaces in URL query parameters are commonly encoded as:

```text
+
```

Therefore:

```text
'+UNION+SELECT+@@version,+NULL#
```

represents:

```sql
' UNION SELECT @@version, NULL#
```

So the `+` signs are not part of the SQL logic itself.

They represent spaces in the URL-encoded request.

---

# 11. What Happened in Burp?

In Burp Repeater, the request looked like:

```http
GET /filter?category='+UNION+SELECT+@@version,+NULL# HTTP/2
```

The server returned:

```text
HTTP/2 200 OK
```

This showed that the request was accepted.

The response contained information associated with the MySQL database, confirming that our injected query was executed.

---

# 12. Attack Flow

The whole process can be remembered as:

```text
Normal category request
        ↓
Identify category parameter
        ↓
Send request to Burp Repeater
        ↓
Test SQL injection
        ↓
Determine number of columns
        ↓
Confirm 2 columns
        ↓
Use UNION SELECT
        ↓
Place @@version in column 1
        ↓
Use NULL for column 2
        ↓
Use # to comment out remaining SQL
        ↓
Receive database version
        ↓
Lab solved ✅
```

---

# 13. Important Payloads From This Lab

### Column-count / text-column test

```sql
' UNION SELECT 'abc','def'#
```

URL-style:

```text
'+UNION+SELECT+'abc','def'#
```

Purpose:

> Confirm that the query accepts 2 returned columns and that both can contain text.

---

### Final version query

```sql
' UNION SELECT @@version, NULL#
```

URL-style:

```text
'+UNION+SELECT+@@version,+NULL#
```

Purpose:

> Retrieve the MySQL database version.

---

# 14. What I Learned

### SQL Injection

User-controlled parameters can become dangerous when they are directly included in SQL queries.

### UNION-based SQL Injection

`UNION SELECT` can be used to retrieve additional data when the injected query matches the original query's column structure.

### Column Count

The number of columns in the injected `SELECT` must match the original query.

### NULL

`NULL` is useful for filling columns when we don't need meaningful data from them.

### Database-specific syntax

SQL syntax is not identical across database systems.

For example:

```text
MySQL → @@version
MySQL comment → #
Oracle version → v$version
Oracle comment → --
```

### Burp Repeater

Repeater makes manual testing much easier because we can repeatedly modify and resend the same HTTP request.

---

# 15. Key Concepts to Remember

| Concept | Meaning |
|---|---|
| SQL Injection | Manipulating a SQL query through user input |
| UNION | Combines results from SQL queries |
| UNION SELECT | Allows an attacker to retrieve additional query results |
| Column count | Number of columns returned by the original query |
| NULL | Placeholder value for an unused column |
| `@@version` | MySQL version information |
| `#` | MySQL single-line comment |
| Burp Repeater | Tool for modifying and repeatedly sending HTTP requests |
| Payload | Input crafted to test or exploit a vulnerability |

---

# 16. My Notes

This lab helped me understand that SQL injection is not simply about trying random strings.

The important process is:

> **Find the injection point → understand the query → determine the column count → construct a compatible UNION query → retrieve useful information.**

The biggest thing I understood from this lab was how the individual pieces of a payload work together instead of just copying a payload from the solution.

---

