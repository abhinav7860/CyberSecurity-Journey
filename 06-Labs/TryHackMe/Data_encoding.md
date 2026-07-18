# TryHackMe — Data Encoding

**Room:** Data Encoding  
**Platform:** TryHackMe  


---
# Task 1 — Introduction

The room introduced the difference between **representation** and **encoding**.

## Representation

Representation is how computers store information internally using binary.

Everything eventually becomes:

```
0
or
1
```

---

## Encoding

Encoding defines what those binary numbers actually mean.

Example:

```
65

=

A
```

Another number may represent:

```
😊
```

instead.

Without an agreed encoding standard, computers wouldn't know how to display text correctly.

---

# Task 2 — ASCII

## What is ASCII?

ASCII stands for:

> **American Standard Code for Information Interchange**

It was introduced in **1963** and became one of the first character encoding standards.

ASCII assigns a number to every English character.

Example:

| Character | Decimal | Hex |
|-----------|---------|-----|
|A|65|41|
|B|66|42|
|a|97|61|
|0|48|30|
|9|57|39|

---

## ASCII Uses 7 Bits

ASCII originally used:

```
7 Bits
```

Which means it could represent:

```
2⁷

=

128 characters
```

These include:

- Uppercase letters
- Lowercase letters
- Numbers
- Symbols
- Control characters

---

## Example

The word

```
TryHackMe
```

is stored internally as binary.

Example:

```
T

=

01010100
```

When grouped together:

```
54 72 79 48 61 63 6B 4D 65
```

This hexadecimal representation is much easier to read than raw binary.

---

## ASCII Control Characters

ASCII also includes characters that don't appear on screen.

Examples include:

- New Line
- Tab
- Delete
- Bell (BEL)

These control how text is displayed rather than displaying actual symbols.

---

## ASCII Limitations

ASCII only supports English.

It cannot properly represent characters like:

```
ñ
é
ü
ç
あ
ب
龍
😊
```

To support European languages, extended versions such as:

- ISO-8859-1
- ISO-8859-2

were created.

However, these standards were incompatible with each other.

The same numeric value could represent different characters depending on which encoding was used.

This often caused unreadable or incorrect text.

---

## Practical Questions

### ASCII value of

```
@
```

Answer

```
64
```

---

### Character with decimal value

```
35
```

Answer

```
#
```

---

### Character with decimal value

```
7
```

Answer

```
BEL
```

---

# Task 3 — Unicode

ASCII solved English text.

Unicode solved text for the entire world.

---

## What is Unicode?

Unicode is a universal character standard.

Instead of supporting only English, it assigns a unique code point to every character from every writing system.

Examples:

```
A

=

U+0041
```

```
Ω

=

U+03A9
```

```
あ

=

U+3042
```

```
😊

=

U+1F60A
```

Every modern operating system, browser, and programming language relies on Unicode.

---

## Why Unicode Was Needed

Different countries previously used different encoding standards.

This created problems.

For example:

A document saved using one encoding might display completely different characters when opened using another encoding.

Unicode solved this by giving every character a globally unique identifier.

---

# UTF-8

UTF-8 is the most common Unicode encoding today.

It uses:

```
1–4 Bytes
```

depending on the character.

### Advantages

- Backward compatible with ASCII
- Efficient for English
- Supports every language
- Used by almost every website

Examples

```
A

=

1 Byte
```

```
Ω

=

2 Bytes
```

```
😊

=

4 Bytes
```

Most websites today specify:

```
UTF-8
```

as their default encoding.

---

# UTF-16

UTF-16 stores characters using:

```
2 Bytes
```

or

```
4 Bytes
```

Simple characters fit into:

```
2 Bytes
```

Complex characters such as emojis require:

```
4 Bytes
```

---

# UTF-32

UTF-32 is the simplest encoding.

Every character uses:

```
4 Bytes
```

Advantages:

- Very easy to process

Disadvantages:

- Uses much more memory

---

# Unicode Examples

The room showed several interesting examples.

### Dragon

```
龍

=

U+9F8D
```

---

### Smiling Face

```
😊

=

U+1F60A
```

---

### Arabic Letter

```
ت

=

U+062A
```

---

### Japanese Character

```
ツ

=

U+30C4
```

---

### Chess Knight

```
♞

=

U+265E
```

This made me realize that every emoji and symbol is simply another Unicode value stored by the computer.

---

# Why Gibberish Happens

One of the most useful things I learned was why unreadable text sometimes appears.

Example:

```
Ã©

instead of

é
```

This happens when:

- A file is saved using one encoding
- It is opened using another encoding

The computer interprets the bytes incorrectly, resulting in strange characters.

---

# Practical Questions

### UTF-32 of

```
😌
```

Answer

```
U+0001F60C
```

---

### UTF-16 of

```
シ
```

Answer

```
U+30B7
```

---

### Character

```
U+2615
```

Answer

```
☕
```

---

### Character

```
U+2658
```

Answer

```
♘
```

---

# Concepts I Learned

## Character Encoding

A standard that maps numbers to characters.

---

## ASCII

- 7-bit encoding
- 128 characters
- English only

---

## Unicode

A universal standard that assigns every character a unique code point.

---

## UTF-8

- Most common encoding
- Uses 1–4 bytes
- Compatible with ASCII

---

## UTF-16

Uses:

- 2 bytes
- or 4 bytes

---

## UTF-32

Always:

```
4 Bytes
```

per character.

---

## Code Point

Every Unicode character has a unique identifier.

Example:

```
A

=

U+0041
```

---
