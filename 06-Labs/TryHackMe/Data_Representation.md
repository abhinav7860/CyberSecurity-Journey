# TryHackMe — Data Representation

**Room:** Data Representation  
**Platform:** TryHackMe  


---

# Task 1 — Introduction

The room introduced the concept that computers only understand two states:

- 0 (Off / Low)
- 1 (On / High)

Everything inside a computer—from colors to files, images, text, and numbers—is ultimately represented using these two values.

### Learning Objectives

- Representing colors
- Binary numbers
- Hexadecimal numbers
- Octal numbers
- Understanding bits and bytes

---

# Task 2 — Representing Colors

## RGB Color Model

Computers create colors by combining three primary colors:

- 🔴 Red
- 🟢 Green
- 🔵 Blue

This is known as the **RGB color model**.

---

## Representing 8 Colors

Initially, each color can only have two states:

- ON
- OFF

Since there are three colors:

```
2 × 2 × 2 = 8 Colors
```

Each color is represented by **1 bit**.

Example:

| Binary | Color |
|---------|-------|
|000|Black|
|001|Blue|
|010|Green|
|100|Red|
|011|Cyan|
|101|Magenta|
|110|Yellow|
|111|White|

This helped me understand why binary is enough to represent multiple combinations.

---

## From 8 Colors to 16 Million Colors

Modern computers don't just use ON or OFF.

Instead, each RGB component uses:

```
8 bits = 256 levels
```

Since there are three colors:

```
256 × 256 × 256
=
16,777,216 colors
```

This is why modern displays can show over **16 million colors**.

---

## Bits and Bytes

I learned:

```
1 Bit
=
0 or 1
```

```
8 Bits
=
1 Byte
```

Since every RGB value uses one byte:

```
Red   → 8 bits
Green → 8 bits
Blue  → 8 bits

Total = 24 bits
```

This explains why color codes are called **24-bit colors**.

---

## Hexadecimal Color Codes

Instead of writing long binary values:

```
101000111110101000101010
```

we use hexadecimal:

```
A3EA2A
```

Hexadecimal makes binary much easier to read.

Example:

```
#FFFFFF
```

means

```
White
```

```
#000000
```

means

```
Black
```

---

## Binary to Hex Mapping

Every:

```
4 Bits
```

becomes

```
1 Hex Digit
```

Example:

```
1010 = A
1111 = F
0011 = 3
```

---

## Practical Questions

### Preview color

```
#3BC81E
```

Answer:

```
Green
```

---

### Binary of

```
#EB0037
```

Answer:

```
11101011 00000000 00110111
```

---

### Decimal of

```
#D4D8DF
```

Answer:

```
212 216 223
```

---

# Task 3 — Decimal, Binary and Hexadecimal

The room then explained how computers represent numbers.

---

## Decimal System (Base 10)

Humans use:

```
0–9
```

Example:

```
213

=
2×100
+
1×10
+
3×1
```

or mathematically

```
2×10²
+
1×10¹
+
3×10⁰
```

---

## Binary System (Base 2)

Computers only use:

```
0
1
```

Each position is a power of two.

Example:

```
1001
```

equals

```
1×8
+
0×4
+
0×2
+
1×1

=
9
```

Another example:

```
1111

=
8+4+2+1

=
15
```

This helped me understand how binary numbers are converted into decimal values.

---

## Hexadecimal System (Base 16)

Hexadecimal uses:

```
0-9
A-F
```

Where:

```
A = 10
B = 11
C = 12
D = 13
E = 14
F = 15
```

Each hexadecimal digit represents:

```
4 Bits
```

Example:

```
1111

=

F
```

---

## Why Hexadecimal is Useful

Instead of writing

```
111111111111111111111111
```

we can simply write

```
FFFFFF
```

Hexadecimal is much shorter and is widely used in:

- Memory addresses
- Packet analysis
- Wireshark
- Hex editors
- Malware analysis
- Programming
- Color codes

---

## Octal Numbers

The room also introduced **Octal (Base 8)**.

Octal groups:

```
3 Bits
```

Example:

```
111

=

7
```

Although octal is less common today, I learned that older Unix systems still use it in some places, such as file permissions.

---

# Practical Questions

### FF in Binary

Answer

```
1111 1111
```

---

### AB in Decimal

```
A = 10

B = 11

AB

=

10×16

+

11

=

171
```

Answer

```
171
```

---

### FFFFFF in Decimal

The room asked to round the value to the nearest million.

```
FFFFFF

=

16,777,215
```

Rounded:

```
17 Million
```

Answer

```
17
```

---

# Concepts I Learned

## Bit

Smallest unit of data.

```
0 or 1
```

---

## Byte

```
8 Bits
```

---

## Binary

Base 2

```
0
1
```

---

## Decimal

Base 10

```
0–9
```

---

## Hexadecimal

Base 16

```
0–9
A–F
```

---

## Octal

Base 8

```
0–7
```

---

## RGB

Every digital color is made from:

- Red
- Green
- Blue

using

```
24 bits
```

---