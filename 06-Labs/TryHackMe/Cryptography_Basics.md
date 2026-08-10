# TryHackMe — Cryptography Basics
**Date Completed:** 10 August 2026
## Room: Cryptography Basics

---

# 1. Introduction to Cryptography

Cryptography is the practice and study of techniques used to protect information and enable secure communication in the presence of adversaries.

Its main goals include:

- **Confidentiality** — preventing unauthorised people from reading data.
- **Integrity** — preventing unauthorised modification of data.
- **Authenticity** — verifying that data or communication comes from the expected source.

Cryptography is used every day, often without the user directly interacting with it.

Examples include:

- Logging in to websites using encrypted connections.
- Connecting to systems using SSH.
- Online banking and certificate verification.
- Verifying downloaded files using hashes.
- Protecting sensitive information such as payment and medical records.

---

# 2. Cryptography in Real-World Security

Cryptography is especially important when sensitive information is stored or transmitted.

For example, organisations handling credit card information must follow security requirements designed to protect payment data.

Medical information is also protected by laws and regulations, depending on the country and environment.

Examples mentioned in the room include:

- PCI DSS
- HIPAA
- HITECH
- GDPR
- DPA

Cryptography therefore forms an important part of modern information security.

---

# 3. Task 1 — Cryptography and Secure Data

Cryptography protects information against attackers and unauthorised third parties.

It can be used to protect:

```text
Confidentiality
Integrity
Authenticity
```

Sensitive information should be protected both when it is stored and when it is transmitted.

### Question

**What is the standard required for handling credit card information?**

### Answer

```text
PCI DSS
```

**PCI DSS** stands for **Payment Card Industry Data Security Standard**.

---

# 4. Task 3 — Plaintext to Ciphertext

Before encryption, data is readable.

After encryption, the data becomes an unreadable form.

The basic process is:

```text
Plaintext
    |
    | Encryption
    | + Cipher + Key
    ↓
Ciphertext
```

To recover the original message:

```text
Ciphertext
    |
    | Decryption
    | + Cipher + Key
    ↓
Plaintext
```

---

## 4.1 Plaintext

**Plaintext** is the original readable message or data before encryption.

It can be:

- Text
- Documents
- Images
- Multimedia
- Credit card information
- Medical records
- Other binary data

Example:

```text
HELLO
```

---

## 4.2 Ciphertext

**Ciphertext** is the scrambled and unreadable version of plaintext after encryption.

Example:

```text
Plaintext  → HELLO
Ciphertext → [encrypted data]
```

The purpose is to prevent unauthorised people from understanding the original information.

### Question

**What do you call the encrypted plaintext?**

### Answer

```text
Ciphertext
```

---

## 4.3 Cipher

A **cipher** is an algorithm or method used to convert plaintext into ciphertext and back again.

The cipher itself can be publicly known.

The security normally depends on keeping the key secret.

---

## 4.4 Key

A **key** is a string of bits used by a cipher to encrypt or decrypt data.

In general:

```text
Cipher = Publicly known
Key    = Secret
```

An exception is the public key used in asymmetric cryptography, which is intentionally shared.

---

## 4.5 Encryption

**Encryption** is the process of converting plaintext into ciphertext using a cipher and a key.

```text
Plaintext + Key + Cipher
            ↓
        Encryption
            ↓
        Ciphertext
```

---

## 4.6 Decryption

**Decryption** is the reverse process.

It converts ciphertext back into the original plaintext using the appropriate cipher and key.

### Question

**What do you call the process that returns the plaintext?**

### Answer

```text
Decryption
```

---

# 5. Task 4 — Historical Ciphers

Cryptography has existed for thousands of years.

One of the most famous historical encryption techniques is the **Caesar Cipher**, associated with Julius Caesar.

The Caesar Cipher works by shifting letters by a fixed number of positions.

---

## 5.1 Caesar Cipher Example

Given:

```text
Plaintext: TRYHACKME
Key:       3
Cipher:    Caesar Cipher
```

Each letter is shifted three positions to the right.

For example:

```text
T → W
R → U
Y → B
```

The resulting ciphertext is:

```text
WUBKDFNPH
```

Because the alphabet wraps around after Z, letters near the end of the alphabet return to the beginning.

---

## 5.2 Caesar Cipher Decryption

To decrypt:

```text
Ciphertext: WUBKDFNPH
Key:        3
```

we shift each letter three positions to the left.

This returns:

```text
TRYHACKME
```

---

## 5.3 Why Caesar Cipher Is Insecure

The English alphabet contains only 26 letters.

A shift of 26 returns every letter to its original position.

Therefore, there are only 25 meaningful encryption keys.

An attacker can simply try every possible shift.

This is known as a brute-force approach.

Because of this very small key space, the Caesar Cipher is considered insecure by modern standards.

---

## 5.4 Caesar Cipher Question

Given:

```text
Ciphertext: XRPCTCRGNEI
```

and knowing it was encrypted using a Caesar Cipher, the original plaintext is:

```text
I CAN ENCRYPT
```

The shift used is:

```text
15
```

when decrypting by shifting the ciphertext 15 positions backward.

---

## 5.5 Other Historical Ciphers

Other historical cryptographic systems mentioned in the room include:

- **Vigenère Cipher** — 16th century
- **Enigma Machine** — World War II
- **One-Time Pad** — Cold War era

---

# 6. Task 5 — Types of Encryption

There are two main categories of encryption:

```text
Symmetric Encryption
        +
Asymmetric Encryption
```

They differ mainly in how keys are used.

---

# 7. Symmetric Encryption

Symmetric encryption uses the **same key** for encryption and decryption.

```text
             Same Secret Key
                    |
        ┌───────────┴───────────┐
        ↓                       ↓
   Encryption              Decryption
        ↓                       ↓
    Plaintext              Ciphertext
        ↓                       ↓
    Ciphertext              Plaintext
```

The key must remain secret.

---

## 7.1 The Main Problem with Symmetric Encryption

The major challenge is securely sharing the key.

For example:

```text
Alice
  |
  | Encrypted file
  ↓
Bob
```

Alice cannot safely send the encryption key through the same insecure channel.

If an attacker obtains both the encrypted file and the key, the encryption provides no protection.

This is known as the key-distribution problem.

---

## 7.2 Examples of Symmetric Encryption

Examples mentioned in the room:

- DES
- 3DES
- AES

---

## 7.3 DES

**DES — Data Encryption Standard**

Important points:

- Adopted as a standard in 1977.
- Uses a 56-bit key.
- Became insecure as computing power increased.
- A DES key was successfully broken in less than 24 hours in 1999.
- It was replaced by stronger alternatives.

### Question

**Should you trust DES?**

### Answer

```text
Nay
```

DES should not be trusted for modern secure encryption.

---

## 7.4 3DES

**3DES — Triple DES**

3DES applies DES three times.

Important points:

- Nominal key size: 168 bits.
- Effective security: approximately 112 bits.
- Developed as an interim solution after DES became insecure.
- Deprecated in 2019.
- Modern systems should use stronger alternatives such as AES.

---

## 7.5 AES

**AES — Advanced Encryption Standard**

AES was adopted as an encryption standard in:

```text
2001
```

AES supports:

- 128-bit keys
- 192-bit keys
- 256-bit keys

AES is widely used for modern symmetric encryption.

### Question

**When was AES adopted as an encryption standard?**

### Answer

```text
2001
```

---

# 8. Asymmetric Encryption

Unlike symmetric encryption, asymmetric encryption uses a pair of keys:

```text
Public Key
Private Key
```

The public key can be shared.

The private key must remain secret.

For confidentiality:

```text
Message
   ↓
Encrypt with Public Key
   ↓
Ciphertext
   ↓
Decrypt with Private Key
   ↓
Original Message
```

---

## 8.1 Examples

Examples mentioned in the room include:

- RSA
- Diffie-Hellman
- Elliptic Curve Cryptography (ECC)

---

## 8.2 Public Key

The public key can be shared with other people.

It can be used for operations such as encryption or establishing secure cryptographic communication, depending on the algorithm and protocol.

---

## 8.3 Private Key

The private key must be kept secret.

In public-key encryption, data encrypted with the corresponding public key can be decrypted using the private key.

---

## 8.4 Symmetric vs Asymmetric

| Feature | Symmetric | Asymmetric |
|---|---|---|
| Number of keys | One shared key | Public + private key |
| Encryption speed | Generally faster | Generally slower |
| Key distribution | More difficult | Public key can be shared |
| Examples | AES, DES, 3DES | RSA, Diffie-Hellman, ECC |
| Main challenge | Secure key sharing | More computationally expensive |

---

# 9. Key Sizes Mentioned

The room gives several examples of cryptographic key sizes.

### RSA

Common key sizes mentioned:

```text
2048 bits
3072 bits
4096 bits
```

2048-bit RSA is given as the recommended minimum in the room.

### Diffie-Hellman

The room mentions:

```text
2048 bits minimum
3072 bits
4096 bits
```

### ECC

ECC can provide comparable security using significantly shorter keys.

For example:

```text
256-bit ECC
≈ comparable security to
3072-bit RSA
```

---

# 10. Alice and Bob

Cryptography examples commonly use fictional characters.

```text
Alice ↔ Bob
```

They represent two parties trying to communicate securely.

For example:

- Alice wants to send a message.
- Bob wants to receive it.
- An attacker is trying to intercept the communication.

These names make cryptography concepts easier to explain.

---

# 11. Task 6 — Basic Mathematics

Modern cryptography depends heavily on mathematics.

This task introduces two mathematical operations:

```text
XOR
Modulo
```

---

# 12. XOR Operation

XOR means:

```text
Exclusive OR
```

It is represented by:

```text
⊕
```

or:

```text
^
```

XOR compares two bits.

The result is `1` when the bits are different and `0` when they are the same.

---

## 12.1 XOR Truth Table

| A | B | A XOR B |
|---|---|---------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Therefore:

```text
0 ⊕ 0 = 0
0 ⊕ 1 = 1
1 ⊕ 0 = 1
1 ⊕ 1 = 0
```

---

## 12.2 XOR Example

Consider:

```text
1010
1100
```

Apply XOR bit by bit:

```text
1 ⊕ 1 = 0
0 ⊕ 1 = 1
1 ⊕ 0 = 1
0 ⊕ 0 = 0
```

Therefore:

```text
1010
⊕ 1100
------
0110
```

---

# 13. XOR Properties

Several properties make XOR useful in cryptography.

### Property 1 — XOR With Itself

```text
A ⊕ A = 0
```

### Property 2 — XOR With Zero

```text
A ⊕ 0 = A
```

### Property 3 — Commutative

```text
A ⊕ B = B ⊕ A
```

### Property 4 — Associative

```text
(A ⊕ B) ⊕ C = A ⊕ (B ⊕ C)
```

---

# 14. XOR as Simple Symmetric Encryption

XOR can demonstrate the basic idea behind symmetric encryption.

Let:

```text
P = Plaintext
K = Secret Key
C = Ciphertext
```

Encryption:

```text
C = P ⊕ K
```

To recover the plaintext:

```text
C ⊕ K
```

Substituting:

```text
(P ⊕ K) ⊕ K
```

Because XOR is associative:

```text
P ⊕ (K ⊕ K)
```

And:

```text
K ⊕ K = 0
```

Therefore:

```text
P ⊕ 0 = P
```

So:

```text
(P ⊕ K) ⊕ K = P
```

This demonstrates why XOR can be used as a simple symmetric encryption operation.

In practical cryptographic systems, much more is required than simply XORing data with an arbitrary key.

---

# 15. XOR Question

### Question

**What is `1001 ⊕ 1010`?**

Calculate bit by bit:

```text
1001
1010
----
0011
```

### Answer

```text
0011
```

---

# 16. Modulo Operation

The modulo operator calculates the **remainder** after division.

It is commonly written as:

```text
%
```

or:

```text
mod
```

For:

```text
X % Y
```

the result is the remainder after dividing `X` by `Y`.

---

## 16.1 Modulo Examples

### Example 1

```text
25 % 5 = 0
```

Because:

```text
25 = 5 × 5 + 0
```

### Example 2

```text
23 % 6 = 5
```

Because:

```text
23 = 3 × 6 + 5
```

### Example 3

```text
23 % 7 = 2
```

Because:

```text
23 = 3 × 7 + 2
```

---

# 17. Important Modulo Property

Modulo is not reversible in the normal sense.

For example:

```text
x % 5 = 4
```

can have infinitely many values of `x`.

Examples include:

```text
4
9
14
19
24
29
...
```

For any integer `a` and positive integer `n`:

```text
0 ≤ a % n < n
```

Therefore, the result is always:

- Greater than or equal to `0`
- Less than the divisor

---

# 18. Modulo Questions

### Question 1

```text
118613842 % 9091
```

### Answer

```text
3565
```

### Question 2

```text
60 % 12
```

Since 60 divides evenly by 12:

```text
60 = 12 × 5 + 0
```

### Answer

```text
0
```

---

# 19. TryHackMe Answers — Quick Reference

| Question | Answer |
|---|---|
| Standard required for handling credit card information | `PCI DSS` |
| Encrypted plaintext is called | `Ciphertext` |
| Process that returns plaintext | `Decryption` |
| Original plaintext of `XRPCTCRGNEI` | `I CAN ENCRYPT` |
| Should you trust DES? | `Nay` |
| When was AES adopted as an encryption standard? | `2001` |
| `1001 ⊕ 1010` | `0011` |
| `118613842 % 9091` | `3565` |
| `60 % 12` | `0` |

---
