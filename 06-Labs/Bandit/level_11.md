# Bandit Level 11 → Level 12

## Objective

Find the password stored in `data.txt`, where the text is encoded using ROT13.

## Commands Used

```bash
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

## What I Learned

- ROT13 is a simple cipher that shifts every letter by **13 positions**.
- After reaching **Z**, it starts again from **A** (the same for lowercase letters).

```
A → N
B → O
...
M → Z
N → A
...
Z → M
```

- Since there are **26 letters** in the alphabet, applying ROT13 twice returns the original text.
- I used `cat` to read the file and piped the output to `tr` to decode the password.