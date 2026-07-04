# Bandit Level 5 → Level 6

## Objective

Find the password stored in a file that is:
- Human-readable
- 1033 bytes in size
- Not executable

## Commands Used

```bash
cd inhere
du -ab | grep 1033
cat <filename>
```

## What I Learned

- `du -ab` shows the size of files in bytes.
- `grep` filters output based on a keyword or value.
- `|` (pipe) sends the output of one command as the input to another command.