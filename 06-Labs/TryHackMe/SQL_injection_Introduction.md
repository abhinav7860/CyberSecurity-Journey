# SQL Injection Introduction – TryHackMe

**Platform:** TryHackMe  
**Room:** SQL Injection Introduction  
**Part:** 1  
**Date:** 2 September 2026  
**Level:** Beginner

---

## SQL Essentials for Injection

Before learning SQL Injection techniques, I studied some SQL features that are commonly used in injection payloads.

### SQL Comments

Comments tell the database to ignore the remaining SQL.

MySQL comment syntax:

```sql
-- 
#
/* */
```

Example:

```sql
SELECT * FROM users WHERE username='INPUT' AND password='secret';
```

Input such as:

```text
admin'-- 
```

can comment out the remaining part of the query.

### UNION

`UNION` combines the results of two or more `SELECT` statements into one result set.

The `SELECT` statements must return the **same number of columns** with compatible data types.

```sql
SELECT name, age FROM students
UNION
SELECT username, id FROM admins;
```

This is the basis of **Union-Based SQL Injection**.

### LIKE and Wildcards

`LIKE` is used for pattern matching.

- `%` → any sequence of characters
- `_` → exactly one character

```sql
SELECT * FROM users WHERE username LIKE 'adm%';
```

### LIMIT

`LIMIT` controls how many rows are returned.

```sql
SELECT * FROM users LIMIT 1;
SELECT * FROM users LIMIT 2, 1;
```

It can also be useful during injection to control which row is returned.

### String Functions

`group_concat()` combines values from multiple rows into one result.

```sql
SELECT group_concat(username, ':', password SEPARATOR '<br>') FROM users;
```

`CONCAT()` joins values together:

```sql
CONCAT(username, ':', password)
```

### information_schema

`information_schema` contains metadata about databases, tables, columns and data types.

Important tables:

- `information_schema.tables` – information about tables
- `information_schema.columns` – information about columns

It can help reveal the structure of a database during SQL Injection testing.

> SQL syntax can vary between database engines such as MySQL, MSSQL, PostgreSQL, SQLite and Oracle.

---

# What is SQL Injection?

**SQL Injection (SQLi)** occurs when user input is directly included in a SQL query without proper sanitisation or parameterisation.

The input can then be interpreted as part of the SQL query instead of just normal data.

Example:

```sql
SELECT * FROM articles WHERE id = 1 AND public = 1;
```

If input is directly concatenated, an input such as:

```text
1 OR 1=1--
```

could change the query logic:

```sql
SELECT * FROM articles WHERE id = 1 OR 1=1-- AND public = 1;
```

Because `1=1` is always true, the query can return unintended results.

---

## Types of SQL Injection

### In-Band SQL Injection

The results of the injection are returned directly through the web application.

Two common types:

- **Error-Based** – database errors reveal information.
- **Union-Based** – `UNION` is used to retrieve additional data through the page.

### Blind SQL Injection

The application does not directly display useful query results or errors. Information is inferred from behaviour.

Examples:

- **Authentication Bypass**
- **Boolean-Based** – response changes depending on whether a condition is true or false.
- **Time-Based** – delays such as `SLEEP()` are used to infer results.

### Out-of-Band SQL Injection

The database makes an external request, such as a DNS request, allowing information to be transferred through another channel.

---

# Detecting SQL Injection

Common places to test include:

- URL parameters
- Login forms
- Search fields
- Comment fields
- Cookies
- HTTP headers

Basic test inputs include:

```text
'
"
;--
OR 1=1
```

A single quote `'` is a common first test. A database error or change in application behaviour can indicate possible SQL Injection.

If errors are hidden, behavioural or timing differences may help identify Blind SQL Injection.

---

# Questions I Answered

### What SQL statement combines results from two `SELECT` queries into one result set?

**Answer:** `UNION`

### What built-in database contains metadata about databases, tables, and columns in MySQL?

**Answer:** `information_schema`

### What character is commonly used as a first test when probing for SQL Injection?

**Answer:** `'` (single quote)

### What type of SQL Injection returns results directly in the web page?

**Answer:** In-Band SQL Injection

---

# My Takeaway

Today I learned the basic concepts of **SQL Injection** and some SQL features used when understanding injection payloads.

The main things I learned:

- SQL comments can remove the remaining part of a query.
- `UNION` combines results from multiple `SELECT` statements.
- `LIKE` is used for pattern matching.
- `LIMIT` controls returned rows.
- `CONCAT()` and `group_concat()` combine values.
- `information_schema` contains database metadata.
- SQL Injection happens when user input can change SQL query logic.
- SQLi can be **In-Band, Blind, or Out-of-Band**.
- `'` is a common first test for SQL Injection.
- **In-Band SQLi** returns results through the application response.

---

# Part 2

<!-- Space reserved for the next part of the SQL Injection Introduction room. -->

