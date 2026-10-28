# PortSwigger Web Security Academy
# Blind SQL Injection with Conditional Responses

## 1. Lab Overview

**Platform:** PortSwigger Web Security Academy  
**Lab:** Blind SQL injection with conditional responses  
**Difficulty:** Practitioner  
**Category:** SQL Injection  
**Vulnerability Type:** Blind SQL Injection  
**Testing Tool:** Burp Suite Community Edition  
**Target:** PortSwigger-provided vulnerable lab  
**Status:** Solved

### Objective

The objective of this lab was to exploit a blind SQL injection vulnerability in the application's `TrackingId` cookie.

The application did not directly display database query results or SQL errors. Instead, it returned different HTTP responses depending on whether the injected SQL condition was true or false.

By observing these differences, I was able to:

1. Identify the SQL injection vulnerability.
2. Confirm that the database contained an administrator account.
3. Determine the administrator password length.
4. Extract the password character by character.
5. Authenticate as the administrator.
6. Successfully complete the lab.

This exercise demonstrated how an attacker can retrieve sensitive database information even when the application does not directly expose query results.

---

## 2. Lab Environment

### Tools

**Burp Suite Community Edition**

Burp Suite was used to intercept and manipulate HTTP requests.

The following components were used:

- Proxy: Intercepting and forwarding HTTP requests.
- Repeater: Manually testing SQL injection conditions.
- Intruder: Automating character-by-character password extraction.

### Target Application

The target was a PortSwigger Web Security Academy lab.

The application used a tracking cookie named:

`TrackingId`

The cookie was included in HTTP requests sent to the application.

The testing was performed exclusively against the authorized Academy lab environment.

---

## 3. Understanding Blind SQL Injection

### What is SQL Injection?

SQL injection occurs when an application incorporates untrusted input into a SQL query without properly separating data from executable SQL instructions.

An attacker may manipulate the input to change the behavior of the database query.

For example, an application might internally execute a query resembling:

```sql
SELECT *
FROM products
WHERE category = 'Gifts';
```

If user-controlled input is inserted directly into the query, an attacker may be able to modify its logic.

The resulting vulnerability can allow unauthorized database access, information disclosure, or authentication bypass.

### What makes SQL injection blind?

In a traditional SQL injection vulnerability, the application may directly display database results or SQL errors.

Blind SQL injection is different.

The application does not directly reveal the information being queried.

Instead, the attacker observes indirect effects of the query.

These effects can include:

- Changes in response content.
- Differences in response length.
- Changes in HTTP status codes.
- Conditional messages.
- Response timing.

In this lab, the application displayed a particular message when an injected SQL condition evaluated to true.

The message was:

`Welcome back`

This message became the indicator used to extract information from the database.

### Conditional responses

The vulnerable application behaved differently depending on the result of the injected condition.

Conceptually:

```sql
IF(condition_is_true)
    RETURN normal_response_with_welcome_message
ELSE
    RETURN normal_response_without_welcome_message
```

The application did not expose the password itself.

However, it exposed enough information to determine whether a particular condition was true.

This made it possible to extract the password through repeated queries.

---

## 4. Initial Reconnaissance

### Step 1: Identify the tracking cookie

I examined the HTTP request in Burp Suite.

The request contained a cookie similar to:

```http
Cookie: TrackingId=ORIGINAL_VALUE; session=SESSION_VALUE
```

The `TrackingId` cookie was the parameter selected for testing.

The original cookie value was preserved as the baseline.

### Step 2: Send the request to Repeater

I intercepted the request and sent it to Burp Repeater.

Repeater allowed me to modify the cookie and observe the application's response without repeatedly navigating through the browser.

The request was sent to the lab's root page.

The response was examined for:

- HTTP status code.
- Response body.
- Application messages.
- Response length.

### Step 3: Establish a baseline

The original request returned the normal application response.

This provided a reference point for subsequent tests.

A baseline is important because the meaning of an injected response depends on how the application behaves without the injection.

---

## 5. Confirming the SQL Injection

### Step 1: Test a true condition

I modified the `TrackingId` cookie by appending a SQL condition that evaluated to true.

Conceptually, the condition was:

```sql
' AND '1'='1
```

The important part was the logical comparison:

```sql
1 = 1
```

This comparison always evaluates to true.

The application returned its normal response.

The welcome message appeared.

### Why this mattered

The response indicated that the injected condition was being evaluated by the database.

However, a single true condition was not sufficient to prove the vulnerability.

I needed to compare it with a false condition.

### Step 2: Test a false condition

I changed the condition to:

```sql
' AND '1'='2
```

The comparison:

```sql
1 = 2
```

always evaluates to false.

The application returned a different response.

The `Welcome back` message disappeared.

### Observation

| Test | SQL condition | Result |
|---|---|---|
| True condition | `1 = 1` | Welcome message appeared |
| False condition | `1 = 2` | Welcome message disappeared |

### Conclusion

The difference between the two responses confirmed that the injected SQL condition influenced the application's behavior.

The vulnerability was a blind SQL injection with conditional responses.

---

## 6. Confirming the Administrator Account

After confirming the injection, I tested whether the database contained an administrator account.

The following SQL condition was used:

```sql
' AND (SELECT 'a'
FROM users
WHERE username='administrator')='a
```

### Explanation

The query attempted to retrieve a constant value from the `users` table.

The condition was:

```sql
SELECT 'a'
FROM users
WHERE username='administrator'
```

If the administrator account existed, the subquery returned the value:

```text
a
```

The outer condition then compared that result with:

```sql
'a'
```

The comparison evaluated to true.

If the account did not exist, the subquery returned no matching row.

The overall condition did not evaluate to true.

### Observation

The application returned the welcome message.

### Conclusion

The conditional response indicated that the administrator account existed in the database.

This was an important step because it confirmed the database structure and account name required for the next stage.

---

## 7. Determining the Administrator Password Length

The next objective was to determine how many characters were present in the administrator password.

The SQL function used was:

```sql
LENGTH(password)
```

This function returns the length of a string.

### Step 1: Test a password length condition

The following condition was used:

```sql
' AND (
SELECT 'a'
FROM users
WHERE username='administrator'
AND LENGTH(password)>19
)='a
```

### Explanation

The query checked whether the administrator password contained more than 19 characters.

The important expression was:

```sql
LENGTH(password)>19
```

If the password length was greater than 19, the subquery returned the constant value `a`.

The outer comparison then evaluated to true.

The application displayed the welcome message.

### Step 2: Interpret the result

The condition was true.

Therefore:

```text
Password length > 19
```

The next step was to test whether the password length was greater than 20.

The condition was false.

Therefore:

```text
Password length <= 20
```

Combining both observations:

```text
Password length > 19
Password length <= 20
```

The password length was exactly:

```text
20 characters
```

### Why this technique works

Instead of retrieving the password directly, I used a SQL function to ask a yes-or-no question.

The application response revealed the answer.

This reduced the problem to a series of conditional checks.

---

## 8. Extracting the Password Character by Character

After determining the password length, I began extracting its characters.

The SQL function used was:

```sql
SUBSTRING(password,position,1)
```

### Understanding SUBSTRING

The function extracts a specified portion of a string.

For example:

```sql
SUBSTRING('security',1,1)
```

returns:

```text
s
```

The expression:

```sql
SUBSTRING('security',2,1)
```

returns:

```text
e
```

The first argument identifies the string.

The second argument identifies the character position.

The third argument specifies the number of characters to extract.

In this lab, the function was applied to the administrator password.

### Step 1: Extract the first character

The following condition was used:

```sql
' AND (
SELECT SUBSTRING(password,1,1)
FROM users
WHERE username='administrator'
)='a
```

This condition checked whether the first password character was `a`.

The final comparison was:

```sql
SUBSTRING(password,1,1)='a'
```

If the first character matched, the application returned the welcome message.

Otherwise, the welcome message was absent.

### Step 2: Test candidate characters

I used Burp Intruder to automate the testing process.

Instead of manually changing the candidate character for every request, I configured a payload list containing possible characters.

The payload list included:

- Lowercase letters.
- Digits.
- Additional characters where necessary.

Intruder substituted each candidate into the SQL condition and sent the resulting request.

### Step 3: Identify the matching character

The results were compared using:

- HTTP status code.
- Response length.
- Welcome message indicator.

The successful result showed:

```text
Payload: h
Status: 200
Response length: 11652
Welcome back: 1
```

The normal responses had a length of approximately:

```text
11591
```

The successful response was different.

Therefore, the first password character was:

```text
h
```

### Step 4: Repeat for subsequent characters

The character position was incremented.

For the second character, the query used:

```sql
SUBSTRING(password,2,1)
```

For the third character:

```sql
SUBSTRING(password,3,1)
```

The same process was repeated until all 20 characters had been recovered.

The position was changed for each extraction.

The candidate character list remained the same.

### Character extraction logic

The extraction process can be represented as:

```text
Position 1:
Test candidate characters
Identify matching character

Position 2:
Test candidate characters
Identify matching character

Position 3:
Test candidate characters
Identify matching character

Repeat until the password length is reached
```

The result was a complete administrator password recovered through conditional responses.

---

## 9. Burp Suite Repeater Configuration

### Purpose

Repeater was used for manually testing SQL conditions.

It provided immediate feedback and helped verify whether the injection syntax was correct.

### Procedure

1. Intercept the original application request.
2. Send the request to Repeater.
3. Locate the `TrackingId` cookie.
4. Preserve the original tracking value.
5. Append the SQL condition.
6. Send the request.
7. Inspect the response.
8. Compare the result with the baseline.

### Important observations

Repeater was useful for:

- Testing true and false conditions.
- Confirming the administrator account.
- Determining password length.
- Testing individual character conditions.

It was also useful for identifying syntax problems before using Intruder.

---

## 10. Burp Suite Intruder Configuration

### Purpose

Intruder automated the repetitive character-testing process.

The password extraction required multiple requests for each character position.

Automating the requests made the process more efficient.

### Step 1: Send the request to Intruder

The working request was sent from Repeater to Intruder.

The `TrackingId` cookie was selected as the injection location.

### Step 2: Configure the payload position

The payload position was placed around the candidate character in the SQL comparison.

Conceptually:

```sql
SUBSTRING(password,1,1)='§PAYLOAD§'
```

The payload marker identified the value Intruder would replace.

### Step 3: Select the payload type

The payload type was configured as:

```text
Simple list
```

This allowed a list of candidate characters to be tested.

### Step 4: Add candidate characters

The payload list contained the candidate characters.

Intruder substituted each character into the request.

Each request tested whether the password character at the selected position matched the candidate.

### Step 5: Start the attack

The attack was started.

Intruder sent the requests and collected the responses.

### Step 6: Analyze the results

The results table included:

- Request number.
- Payload.
- HTTP status code.
- Response length.
- Welcome message indicator.

The welcome message was used as the primary success indicator.

### Important troubleshooting note

During the initial attempt, Intruder requests returned errors.

The attack did not produce usable results.

The problem was not the SQL injection logic itself.

The later successful attack returned HTTP 200 responses and revealed a distinct response for the matching character.

This demonstrated why it is important to verify the request in Repeater before automating it.

---

## 11. Final Authentication

After extracting the complete administrator password, I returned to the lab application.

The administrator account was:

```text
administrator
```

I entered the recovered password into the login form.

The application accepted the credentials.

I successfully authenticated as the administrator.

The lab displayed its completion state.

### Final result

**Lab status: SOLVED**

The administrator password was recovered through blind SQL injection with conditional responses.

The lab demonstrated that an application can disclose sensitive database information even when it does not directly display SQL query results.

---

## 12. Vulnerability Impact

Blind SQL injection can have serious security consequences.

The impact depends on the application's database permissions, query structure, and the information accessible through the vulnerable query.

Potential impacts include:

### Sensitive information disclosure

An attacker may extract:

- Usernames.
- Password hashes.
- Account information.
- Personal information.
- Application configuration data.

### Credential compromise

If password data can be extracted, attackers may attempt to authenticate using recovered credentials.

This can lead to account compromise.

### Privilege escalation

If an administrator account is exposed, an attacker may gain access to privileged application functionality.

### Wider database compromise

Depending on the database permissions and vulnerable query, SQL injection may expose additional tables or sensitive records.

---

## 13. Root Cause

The root cause was the application's unsafe handling of the tracking cookie.

The application incorporated the cookie value into a SQL query without adequately separating user-controlled data from SQL instructions.

This allowed the injected SQL condition to influence database execution.

The application then exposed the result indirectly through its response behavior.

The vulnerability was therefore caused by unsafe SQL query construction and insufficient input handling.

---

## 14. Remediation

### 1. Use parameterized queries

The primary remediation is to use prepared statements or parameterized queries.

User-controlled values should be passed as parameters rather than concatenated into SQL statements.

Example using Python and SQLite:

```python
cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
)
```

The parameter is treated as data rather than executable SQL.

This prevents the username from changing the query structure.

### 2. Avoid string concatenation

Unsafe query construction should be avoided.

Example of unsafe code:

```python
query = (
    "SELECT * FROM users WHERE username = '"
    + username
    + "'"
)
```

This approach allows user-controlled input to become part of the SQL statement.

Parameterized queries should be used instead.

### 3. Apply least privilege

The application's database account should have only the permissions required for its functionality.

It should not have unnecessary administrative privileges.

This reduces the impact of a successful SQL injection attack.

### 4. Avoid exposing sensitive authentication information

Applications should not expose password data through database queries or application responses.

Passwords should be stored using an appropriate password hashing algorithm with unique salts.

The application should use secure authentication mechanisms and avoid retrieving plaintext passwords from the database.

### 5. Implement safe error handling

Applications should not expose detailed database errors to users.

Errors should be logged securely for developers and administrators.

The user-facing response should not reveal database structure, query details, or sensitive internal information.

### 6. Perform security testing

Applications should be tested for SQL injection during development and security assessments.

Testing should include:

- Authentication endpoints.
- Tracking cookies.
- Query parameters.
- Form inputs.
- Search functionality.
- Other database-backed inputs.

Automated security testing should be combined with manual validation.

---

## 15. Lessons Learned

This lab improved my understanding of blind SQL injection and practical web application testing.

### Key lessons

**1. SQL injection does not require direct database output.**

Even when query results are not displayed, application behavior may reveal information about database conditions.

**2. True and false conditions are fundamental.**

Comparing the responses to true and false SQL conditions helped confirm the vulnerability.

**3. Database functions can support information extraction.**

`LENGTH()` helped determine the password length.

`SUBSTRING()` helped extract individual characters.

**4. Burp Repeater is useful for manual validation.**

It helped establish the correct request structure before automation.

**5. Burp Intruder can automate repetitive testing.**

It reduced the manual effort required to test candidate characters.

**6. Response differences are important evidence.**

The HTTP response length and application message helped identify successful conditions.

**7. SQL injection can lead to account compromise.**

The vulnerability ultimately allowed administrator authentication.

**8. Parameterized queries are the primary defense.**

Input validation alone is not an adequate replacement for safe SQL query construction.

---

## 16. Conclusion

In this lab, I successfully exploited a blind SQL injection vulnerability in the `TrackingId` cookie of a PortSwigger Web Security Academy application.

The application did not directly reveal database query results.

Instead, I used conditional SQL statements and observed differences in application responses.

I confirmed the existence of the administrator account, determined the password length, and extracted the password character by character using Burp Suite Repeater and Intruder.

After recovering the password, I authenticated as the administrator and successfully solved the lab.

This exercise demonstrated how blind SQL injection can lead to sensitive information disclosure and account compromise.

The most important defensive lesson is to use parameterized SQL queries, enforce least-privilege database permissions, and avoid exposing sensitive information through application responses.

