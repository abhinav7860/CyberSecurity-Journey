# Bandit Level 6 → Level 7

## Objective

Find the password stored somewhere on the server. The file should:

- Be owned by user `bandit7`
- Be owned by group `bandit6`
- Be exactly **33 bytes** in size.

## Commands Used

```bash
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
cat <filename>
```

## What I Learned

This level taught me how to search for files using different conditions.

Instead of checking every folder manually, I used the `find` command to search the entire server.

The command searched for a file that:
- Belongs to the user `bandit7`
- Belongs to the group `bandit6`
- Has a size of exactly **33 bytes**

While searching, many folders showed **Permission denied** because I didn't have access to them.

Using `2>/dev/null` hid those error messages and displayed only the correct result.

After finding the file, I used `cat` to read its contents and get the password.