# Bandit Level 12 → Level 13

## Objective

The password for the next level is stored in `data.txt`. Unlike previous levels, the file is not plain text. It contains a **hexdump** of a file that has been compressed multiple times using different compression formats.

The goal was to restore the original file by identifying each layer and extracting it until the password was revealed.

---

## Solution

### Step 1 - Create a Temporary Directory

```bash
mkdir /tmp/inigo12
```

I created a temporary workspace so I could work on a copy of the challenge file without modifying the original.

---

### Step 2 - Copy the Challenge File

```bash
cp data.txt /tmp/inigo12
cd /tmp/inigo12
```

---

### Step 3 - Inspect the File

```bash
file data.txt
```

Output

```
ASCII text
```

Viewing the file showed hexadecimal values instead of readable text.

```bash
cat data.txt
```

```
00000000: 1f8b0808...
```

This indicated that the file was actually a **hexdump**.

---

### Step 4 - Convert the Hexdump

```bash
xxd -r data.txt > data01
```

`xxd -r` converts a hexadecimal dump back into its original binary form.

---

### Step 5 - Identify Every Layer

Instead of guessing, I used the `file` command after every extraction.

```bash
file data01
```

```
gzip compressed data
```

Then continued extracting layer by layer.

---

## Compression Chain

| File | Type | Command Used |
|------|------|--------------|
| data01 | gzip | `gunzip -c data01 > data02` |
| data02 | bzip2 | `bunzip2 -c data02 > data03` |
| data03 | gzip | `gunzip -c data03 > data04` |
| data04 | tar | `tar -xf data04` |
| data5.bin | tar | `tar -xf data5.bin` |
| data6.bin | bzip2 | `bunzip2 -c data6.bin > data07` |
| data07 | tar | `tar -xf data07` |
| data8.bin | gzip | `gunzip -c data8.bin > data09` |
| data09 | ASCII Text | `cat data09` |

---

## Compression Flow

```
data.txt
    │
    ▼
Hexdump
    │
xxd -r
    ▼
gzip
    │
gunzip
    ▼
bzip2
    │
bunzip2
    ▼
gzip
    │
gunzip
    ▼
tar
    │
tar -xf
    ▼
tar
    │
tar -xf
    ▼
bzip2
    │
bunzip2
    ▼
tar
    │
tar -xf
    ▼
gzip
    │
gunzip
    ▼
ASCII Text
    │
cat
    ▼
Password
```

---

## Commands Used

| Command | Purpose |
|----------|---------|
| `mkdir` | Create working directory |
| `cp` | Copy challenge file |
| `cd` | Change directory |
| `file` | Identify actual file type |
| `xxd -r` | Convert hexdump back to binary |
| `gunzip -c` | Extract gzip while keeping original |
| `bunzip2 -c` | Extract bzip2 while keeping original |
| `tar -xf` | Extract tar archive |
| `cat` | Display final password |

---

## Mistake I Made

After reaching `data8.bin`, I checked the file type.

```bash
file data8.bin
```

Output

```
gzip compressed data
```

Instead of extracting it, I accidentally ran:

```bash
gzip -c data8.bin > data09
```

This compressed the file again instead of decompressing it.

As a result:

- `data09` became another gzip file.
- Running `gzip` repeatedly created additional compressed files.
- I had to restart from a clean working directory.

The correct command was:

```bash
gunzip -c data8.bin > data09
```

This reminded me that the **`file` command should always decide my next step**.

---

## Key Takeaways

- Never trust a file extension—always verify it with `file`.
- A hexdump is simply a hexadecimal representation of binary data.
- Different compression formats require different extraction tools.
- `gunzip` extracts gzip files.
- `bunzip2` extracts bzip2 files.
- `tar -xf` extracts tar archives.
- Always inspect the file again after every extraction.

---
