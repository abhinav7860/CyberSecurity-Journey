# Bandit Level 8 → Level 9

## Objective

Find the password stored in `data.txt` that appears only once.

## Commands Used

```bash
ls
cat data.txt | wc -l
cat data.txt | sort | uniq | wc -l
cat data.txt | sort | uniq -u | wc -l
cat data.txt | sort | uniq -u
```

## What I Learned

- `wc -l` counts the number of lines.
- `sort` arranges the lines before using `uniq`.
- `uniq` removes duplicate adjacent lines.
- `uniq -u` displays only the line that appears once.