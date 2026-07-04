# Bandit Level 4 → Level 5

## Objective

Find the password stored in the only human-readable file inside the `inhere` directory.

## Commands Used

```bash
cd inhere
ls
cat ./-file07
```

## What I Learned

- Some files may contain unreadable (binary) data.
- Human-readable files can be identified by checking their contents.
- `./` is used to access files that start with `-`.