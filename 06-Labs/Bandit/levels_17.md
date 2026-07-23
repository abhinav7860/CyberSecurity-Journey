# OverTheWire Bandit Level 17 → 18

## Objective

There are two files in the home directory:

- `passwords.old`
- `passwords.new`

Both files contain many passwords, but **only one line has changed**.

The password for the next level is **the only line that differs in `passwords.new`**.

---

# Understanding the Challenge

Manually comparing two files with hundreds of lines is inefficient and error-prone.

Linux provides a utility called **diff** that compares two files line by line and highlights any differences.

This makes it the perfect tool for this challenge.

---

# Step 1 – View the Files

List the files in the home directory.

```bash
ls
```

Output:

```text
passwords.new
passwords.old
```

You can inspect them manually if needed.

```bash
cat passwords.old
cat passwords.new
```

Both files appear almost identical except for one line.

---

# Step 2 – Compare the Files

Use the `diff` command to compare both files.

```bash
diff passwords.new passwords.old
```

Output:

```text
42c42
< OQxXZjELndr90zuhOTDYBEomI0SZITXI
---
> icUh23IUytZLIYhcCaXL18agiSIqymBc
```

---

# Understanding the Output

The `diff` command uses a simple notation to describe differences.

```
42c42
```

Breakdown:

- **42** → Line number in the first file (`passwords.new`)
- **c** → Means **change**
- **42** → Corresponding line number in the second file (`passwords.old`)

In other words:

> Line **42** in `passwords.new` is different from line **42** in `passwords.old`.

---

## Symbols Used by `diff`

### `<`

Represents content from the **first file**.

```text
< OQxXZjELndr90zuhOTDYBEomI0SZITXI
```

Since the first file is `passwords.new`, this line is the **new password**.

---

### `---`

Separator showing where the first file ends and the second file begins.

---

### `>`

Represents content from the **second file**.

```text
> icUh23IUytZLIYhcCaXL18agiSIqymBc
```

This is the old password stored in `passwords.old`.

---

# Step 3 – Obtain the Password

The challenge states:

> The password is the only line that has changed in **passwords.new**.

Therefore, the correct password is the line marked with **`<`**.

Example:

```text
OQxXZjELndr90zuhOTDYBEomI0SZITXI
```

Use this password to log in as **bandit18**.

---

# Commands Used

List files:

```bash
ls
```

View file contents:

```bash
cat passwords.old
cat passwords.new
```

Compare files:

```bash
diff passwords.new passwords.old
```

---

# Understanding the `diff` Command

Syntax:

```bash
diff file1 file2
```

`diff` compares two files line by line and reports:

- Changed lines
- Added lines
- Deleted lines

Common symbols:

| Symbol | Meaning |
|---------|---------|
| `<` | Line from the first file |
| `>` | Line from the second file |
| `c` | Change |
| `a` | Addition |
| `d` | Deletion |

---

# Commands Summary

```bash
# List files
ls

# View files
cat passwords.old
cat passwords.new

# Compare files
diff passwords.new passwords.old
```