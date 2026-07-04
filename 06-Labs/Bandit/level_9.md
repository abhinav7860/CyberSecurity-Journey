# Bandit Level 9 → Level 10

## Objective

Find the password stored in `data.txt` among the few human-readable strings that begin with several `=` characters.

## Commands Used

```bash
strings data.txt | grep "==="
```

## What I Learned

- `strings` extracts readable text from a binary file.
- `grep` searches for a specific pattern.
- `|` passes the output of one command to another.