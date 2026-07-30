# CompTIA Security+ (SY0-701)

## Domain 1.2 - Public Key Infrastructure (PKI)

> 📅 Date: 30 July 2026
> 🎥 Source: Professor Messer - Security+ (SY0-701)

---

# Exam Objective

**CompTIA Security+ SY0-701**

- Domain 1.2: Summarize fundamental security concepts.
- Topic:
  - Public Key Infrastructure (PKI)
  - Symmetric Encryption
  - Asymmetric Encryption
  - Public & Private Keys
  - Key Escrow

---
# What is Public Key Infrastructure (PKI)?

Public Key Infrastructure (PKI) is a framework used to manage digital certificates and public-key encryption.

PKI includes:

- Policies
- Procedures
- Hardware
- Software
- People

Its main job is to create trust between users, devices, and organizations.

PKI manages digital certificates throughout their lifecycle.

It can:

- Create certificates
- Distribute certificates
- Store certificates
- Renew certificates
- Revoke certificates

---

# Why is PKI Needed?

Imagine visiting your bank's website.

How do you know it is really your bank and not a fake website?

PKI solves this problem.

It binds a public key to a person, device, or organization using a digital certificate issued by a trusted Certificate Authority (CA).

Without PKI, secure communication on the Internet would not be possible.

---

# Symmetric Encryption

Symmetric encryption uses **one shared secret key**.

The same key is used to encrypt and decrypt data.

```
Encrypt ---> Secret Key ---> Ciphertext

Ciphertext ---> Same Secret Key ---> Plaintext
```

## Characteristics

- One shared key
- Fast
- Efficient
- Low processing overhead
- Difficult to securely share the key

If someone steals the key, they can both encrypt and decrypt your data.

---

## Advantages

✔ Very fast

✔ Efficient for large files

✔ Low CPU usage

---

## Disadvantages

- Securely sharing the key is difficult.
- Doesn't scale well.
- A different key is needed for every secure communication.

---

## Common Algorithms

- AES
- DES (legacy)
- 3DES (legacy)
- Blowfish
- ChaCha20

---

## Easy to Remember

One key.

Same key locks and unlocks.

---

# Asymmetric Encryption

Asymmetric encryption uses **two mathematically related keys**.

These are called a **key pair**.

- Public Key
- Private Key

Unlike symmetric encryption, both keys are different.

```
Public Key  ---> Encrypt

Private Key ---> Decrypt
```

Only the private key can decrypt information encrypted with its matching public key.

The public key cannot reveal the private key.

---

## Public Key

The public key is designed to be shared.

Anyone can have it.

Examples:

- Websites
- Email encryption
- Digital certificates

Think of it as:

> "Here is my lock."

Anyone can lock the box.

Only you can unlock it.

---

## Private Key

The private key must always remain secret.

Only the owner should possess it.

If someone obtains your private key,

they can decrypt your encrypted messages and impersonate you.

---

## Advantages

✔ More secure key exchange

✔ Supports digital signatures

✔ Used by SSL/TLS

✔ Works well across the Internet

---

## Disadvantages

- Slower than symmetric encryption
- Uses more CPU resources
- More computationally expensive

---

# The Key Pair

Public and private keys are generated together.

During generation:

- Large random numbers are created.
- Mathematical algorithms generate the key pair.
- Large prime numbers are commonly used.
- The keys are mathematically related.

Example:

```
Alice

Public Key  ---> Shared with everyone

Private Key ---> Kept secret
```

Everyone can send encrypted data to Alice using her public key.

Only Alice can decrypt it using her private key.

---

# Why Both Encryption Types Are Used

Modern secure protocols combine both encryption methods.

Example: HTTPS

Step 1

Asymmetric encryption safely exchanges a symmetric key.

Step 2

Symmetric encryption handles the actual communication because it is much faster.

This gives both:

- Strong security
- High performance

---

# Key Escrow

Key escrow means a trusted third party stores copies of encryption keys.

Usually:

- Company security team
- Organization
- Government agency (in some situations)

Instead of only you holding the private key,

another trusted entity also stores it securely.

---

## Why Use Key Escrow?

Suppose an employee leaves the company.

Their encrypted files still need to be accessed.

Without key escrow:

Nobody can decrypt the files.

With key escrow:

The organization retrieves the stored private key and accesses the encrypted data.

---

## Advantages

✔ Business continuity

✔ Disaster recovery

✔ Access to important encrypted information

✔ Employee data recovery

---

## Disadvantages

- Reduces privacy
- Creates another target for attackers
- Must be highly protected
- Can become controversial

---

# Comparison

| Symmetric | Asymmetric |
|------------|------------|
| One key | Two keys |
| Fast | Slower |
| Low CPU usage | High CPU usage |
| Same key encrypts & decrypts | Public encrypts, Private decrypts |
| Best for large data | Best for key exchange |

---

# Real-Life Example

Imagine a mailbox.

Anyone can drop a letter into your mailbox.

That is your **Public Key**.

Only you have the mailbox key.

That is your **Private Key**.

Anyone can send you messages,

but only you can read them.

---

# Exam Tips 📝

✅ Symmetric = One shared secret key

✅ Asymmetric = Public + Private key

✅ Public Key = Share with everyone

✅ Private Key = Never share

✅ PKI = Trust through digital certificates

✅ Key Escrow = Someone else securely stores your private key

---

# Memory Trick 🧠

🔑 Symmetric

```
One Key
```

🌍 Public Key

```
Share It
```

🔒 Private Key

```
Keep It Secret
```

🏛 PKI

```
Creates Trust
```

🗄 Key Escrow

```
Backup of Private Keys
```

---

# Things I Need to Remember

- PKI manages digital certificates.
- Certificates bind public keys to identities.
- Symmetric encryption is faster.
- Asymmetric encryption is more secure for key exchange.
- Public keys are shared.
- Private keys remain secret.
- HTTPS combines both encryption methods.
- Key escrow allows trusted organizations to recover encrypted information.

---

