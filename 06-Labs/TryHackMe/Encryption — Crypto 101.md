# Encryption — Crypto 101: Detailed Study Notes

**Platform:** TryHackMe  
**Study date:** 12 November 2026  
**Scope:** Tasks 2–12  
**Focus:** Cryptography foundations, CTF understanding, and SOC awareness

> Based on the lesson material supplied. Simplified descriptions are clarified where needed. No task-file outputs or flags were provided, so none are invented.

---

## Task 2 — Key Terms

| Term | Meaning |
|---|---|
| Plaintext | Data before encryption. It may be text, an image, or another file. |
| Ciphertext | The result of encrypting plaintext. |
| Cipher | A method or algorithm used to encrypt or decrypt data. |
| Encryption | Transforming plaintext into ciphertext using a cipher and key. |
| Encoding | Changing how data is represented. Encoding is not encryption and normally requires no secret to reverse. |
| Key | Information required by a cryptographic operation. |
| Passphrase | A password-like value that can protect a cryptographic key. |
| Symmetric encryption | Uses the same secret key to encrypt and decrypt. |
| Asymmetric cryptography | Uses a related public/private key pair. |
| Brute force | Trying possible passwords or keys until a match is found. |
| Cryptanalysis | Studying or exploiting weaknesses in cryptographic algorithms or their use. |
| Alice and Bob | Conventional fictional names for parties communicating securely. |

### Encryption versus encoding

Encryption protects confidentiality and normally requires an appropriate key to decrypt. Encoding changes representation only. Base64, for example, can be reversed by anyone who recognizes the encoding; it does not protect secrets.

### Key versus passphrase

A key is used by the cryptographic operation. A passphrase may protect a stored key. For example, an encrypted SSH private-key file may require a passphrase before the client can use the private key.

---

## Task 3 — Why Is Encryption Important?

Cryptography supports three important security goals:

1. **Confidentiality:** preventing unauthorized people from reading information.
2. **Integrity:** detecting unauthorized or unexpected changes to data.
3. **Authenticity:** helping verify the identity of a party or the origin of data.

### Everyday examples

| Situation | How cryptography helps |
|---|---|
| Logging in to a website | An encrypted connection helps protect credentials in transit. |
| Connecting through SSH | SSH establishes an encrypted session. |
| Visiting a bank website | Certificates and authentication help verify the server's identity. |
| Downloading a file | A cryptographic hash/checksum can help verify that data matches an expected value. |
| Storing sensitive information | Encryption can protect stored data if storage is exposed. |

### Data at rest and data in transit

- **At rest:** information stored on disks, databases, removable media, or other storage.
- **In transit:** information moving across a network.

The lesson highlights protecting sensitive data in both states, including payment-card and medical information.

### Password storage: encryption or hashing?

For routine authentication storage, passwords should not be stored in plaintext or reversibly encrypted. Store password verifiers using a purpose-built password-hashing scheme.

Hashing is preferred because authentication normally needs to verify a submitted password, not recover the original. A salted, deliberately expensive password-hashing function makes large-scale guessing more costly. A password manager is different: it may need to recover stored secrets, so it uses encryption protected by a master secret.

---

## Task 4 — Crucial Cryptography Mathematics: Modulo

The modulo operator returns the remainder after integer division. In many programming languages it is written `%`.

```text
25 % 5 = 0
23 % 6 = 5
```

25 divides evenly by 5. For 23 divided by 6, the remainder is 5.

Modulo arithmetic appears frequently in cryptographic algorithms because it keeps calculations within a defined range.

### Modulo is not generally reversible

For example:

```text
x % 5 = 4
```

Many integer values satisfy this equation:

```text
4, 9, 14, 19, 24, ...
```

Knowing only the remainder does not reveal the original value.

### Python examples

```python
print(25 % 5)  # 0
print(23 % 6)  # 5
print(19 % 5)  # 4
```

Python integers can represent very large values, making Python useful for experimenting with cryptographic arithmetic.

---

## Task 5 — Types of Encryption

### Symmetric encryption

Symmetric encryption uses the **same secret key** to encrypt and decrypt.

Examples from the lesson:
- **AES (Advanced Encryption Standard):** a widely used modern symmetric block cipher.
- **DES (Data Encryption Standard):** an older algorithm considered insecure due to its short effective key length.

AES supports 128-, 192-, and 256-bit keys. DES has a 56-bit effective key. Symmetric algorithms are generally faster than asymmetric operations, but parties need a secure way to share or establish their key.

### Asymmetric cryptography

Asymmetric cryptography uses a mathematically related pair:

- **Public key:** can be shared.
- **Private key:** must be kept secret.

The lesson introduces RSA and Elliptic Curve Cryptography (ECC). The key pair can be used for different operations depending on the scheme, including signatures, key agreement, and certain encryption constructions.

Asymmetric operations are generally more computationally expensive than symmetric encryption. The lesson gives RSA sizes of 2048 to 4096 bits as examples.

| Feature | Symmetric | Asymmetric |
|---|---|---|
| Keys | One shared secret | Related public/private pair |
| Typical speed | Faster | Generally slower |
| Common role | Bulk data encryption | Key establishment and signatures; some encryption schemes |
| Examples | AES, DES (obsolete) | RSA, ECC |

**Remember:** Symmetric cryptography efficiently protects large amounts of data. Asymmetric cryptography helps solve problems such as establishing keys and authenticating parties.

---

## Task 6 — RSA: Rivest–Shamir–Adleman

RSA is an asymmetric algorithm whose security is associated with the difficulty of factoring a large composite integer into its prime factors.

### The factoring idea

Multiplying two primes is straightforward:

```text
17 × 23 = 391
113 × 127 = 14351
```

Given a sufficiently large product of suitable primes, finding the original factors is computationally difficult using classical methods.

### Important RSA variables

| Symbol | Meaning |
|---|---|
| `p` | One prime number |
| `q` | The other prime number |
| `n` | Modulus, calculated as `p × q` |
| `e` | Public exponent |
| `d` | Private exponent |
| `m` | Plaintext message represented as an integer |
| `c` | Ciphertext represented as an integer |

The public key is `(n, e)` and the private key is `(n, d)`. The factors `p` and `q` are used during key generation and must be protected.

### RSA in CTF challenges

A cryptography challenge may provide some RSA variables and ask you to recover the plaintext or flag.

A useful approach:
1. Identify which values are provided.
2. Determine which values are missing.
3. Check for weak parameters or implementation mistakes.
4. Determine whether factoring `n` or another weakness applies.
5. Recover the relevant private-key information if the challenge permits.
6. Decrypt and interpret the result.

Do not assume every RSA challenge is solved by factoring `n`; different weaknesses can be deliberately introduced.

### Tools and resources mentioned

- [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool)
- [rsatool](https://github.com/ius/rsatool)
- [MuirlandOracle — RSA Encryption](https://muirlandoracle.co.uk/2020/01/29/rsa-encryption/)

These resources are for authorized CTF challenges and cryptographic experiments.

---

## Task 7 — Establishing Keys Using Asymmetric Cryptography

### The key-establishment problem

Symmetric encryption is efficient, but both parties need the same secret key. Sending it in plaintext would expose it to anyone observing the communication.

Asymmetric cryptography can help establish or protect key material.

### The locked-box metaphor

Imagine:
- You want to send secret instructions to a friend.
- Your friend gives you a lock that anyone can use to lock a box.
- Only your friend has the key that opens the lock.
- You put the instructions in the box, lock it, and send it.
- Your friend opens it with their private key.

In the metaphor:
- Secret instructions represent the symmetric session key.
- The lock represents the recipient's public key.
- The physical key represents the recipient's private key.

The teaching point is that public-key cryptography can help protect key material, after which faster symmetric encryption can protect the session.

### Hybrid encryption in practice

Real secure connections use hybrid cryptographic designs:
- Asymmetric cryptography and/or authenticated key agreement establish shared secrets.
- A key-derivation process derives symmetric traffic keys.
- Symmetric authenticated encryption protects bulk data.

**Clarification:** Modern TLS commonly uses ephemeral Diffie–Hellman key agreement (such as ECDHE), rather than simply encrypting a symmetric session key with the server's RSA public key. The lesson's metaphor explains the general public-key idea, but is not a complete description of modern HTTPS.

Further reading:
[How does HTTPS actually work? — Robert Heaton](https://robertheaton.com/2014/03/27/how-does-https-actually-work/)

---

## Task 8 — Digital Signatures and Certificates

### Digital signatures

A digital signature helps verify:
- **Authenticity:** the signature was produced using the private key corresponding to a public key.
- **Integrity:** the signed data has not changed since it was signed.

At a high level, a signer uses a private key with a signature algorithm to create a signature over the data (usually through a hash-based process). A verifier uses the corresponding public key to validate it.

### Important clarification: signatures are not ordinary encryption

The lesson describes a simplified analogy where a document is encrypted with a private key and decrypted with a public key. This is not how modern digital-signature schemes should be understood or implemented.

Digital signatures use dedicated signature algorithms. They do not provide confidentiality: anyone with the document and public key may be able to verify the signature.

### Certificates

A digital certificate binds an identity (such as a domain name) to a public key. It is digitally signed by a Certificate Authority (CA), allowing a verifier to evaluate whether the certificate should be trusted.

### Certificate chain of trust

```text
Trusted Root CA
      |
      v
Intermediate CA
      |
      v
Website Certificate (e.g., example.com)
      |
      v
Browser validates certificate for the website
```

- **Root CA:** a trust anchor included in a browser or operating-system trust store.
- **Intermediate CA:** certified by a higher-level CA.
- **Website certificate:** issued for a domain and links that identity to a public key.

The browser validates the chain and checks details such as hostname matching, validity period, and certificate constraints.

### Let's Encrypt

The lesson mentions [Let's Encrypt](https://letsencrypt.org/) as a free Certificate Authority option for obtaining HTTPS certificates for domains you control.

---

## Task 9 — SSH Authentication

### SSH authentication methods

SSH may use:
- Username and password.
- Public/private key authentication.

With key authentication:
- The client holds the private key.
- The server stores an authorized copy of the corresponding public key.
- The client proves possession of the private key through the SSH authentication protocol.

### Generating keys

The lesson identifies `ssh-keygen` as the common utility:

```bash
ssh-keygen
```

Generate the key pair on the client machine and copy the public key to the server. This avoids unnecessarily placing the private key on the remote machine.

### Private key protection

Treat a private SSH key like a password:
- Do not share it.
- Store it securely.
- Consider protecting it with a strong passphrase.
- Restrict its filesystem permissions.

**Important:** The private-key passphrase protects the key file locally. It is not sent to the SSH server as the user's authentication credential.

### SSH key locations

OpenSSH commonly stores user keys in:

```text
~/.ssh/
```

The server-side file:

```text
~/.ssh/authorized_keys
```

contains public keys authorized to authenticate as that account.

### Private-key permissions

The lesson notes that SSH clients may ignore private keys with overly permissive filesystem permissions.

A common restrictive setting:

```bash
chmod 600 ~/.ssh/id_rsa
```

This gives the owner read/write permission and denies access to other users. The actual key filename may differ.

### Connecting with a key

```bash
ssh -i keyNameGoesHere user@host
```

- `-i` specifies the private-key identity file.
- `user` is the remote account.
- `host` is the server.

### SSH keys and reverse-shell stabilization

The lesson notes that SSH can sometimes provide a more capable interactive session when the account is permitted to log in over SSH. Service accounts such as `www-data` often do not have interactive SSH login enabled.

An unexpected key inserted into `authorized_keys` can provide persistence or backdoor access. From a defensive perspective, unexpected changes to this file deserve investigation.

---

## Task 10 — Diffie–Hellman Key Exchange

### What is key exchange?

Key exchange allows two parties to establish common secret material over a channel that may be observed. The shared secret can then be used to derive symmetric encryption keys.

### Alice and Bob explanation

The lesson uses:
- Alice's private secret: `A`.
- Bob's private secret: `B`.
- Common public material: `C`.

They combine their private secrets with the public material, exchange the resulting values, and combine the received values with their own secrets. Under Diffie–Hellman mathematics, both obtain the same shared secret without transmitting their private values.

### Mathematical idea

The lesson's `AC`, `BC`, and `ABC` notation is a metaphor for a one-way mathematical operation. Real finite-field Diffie–Hellman is commonly described using modular exponentiation:

- Public parameters include a prime modulus `p` and generator `g`.
- Alice chooses private value `a` and sends `A = g^a mod p`.
- Bob chooses private value `b` and sends `B = g^b mod p`.
- Alice computes `B^a mod p`.
- Bob computes `A^b mod p`.
- Both obtain the same shared value: `g^(ab) mod p`.

An observer can see public parameters and exchanged values, but recovering the shared secret should be computationally infeasible with appropriate parameters and current classical methods.

### Diffie–Hellman and man-in-the-middle attacks

Unauthenticated Diffie–Hellman does not prove the identity of the other party. An attacker may attempt to establish separate keys with Alice and Bob and relay traffic.

The lesson explains that DH is commonly combined with authentication, such as digital signatures and certificates. This helps prevent an attacker from impersonating the communicating party.

**Remember:** Key agreement creates shared secret material; authentication helps prove who you are sharing it with.

Further reading:
[Diffie–Hellman Key Exchange visual explanation](https://www.youtube.com/watch?v=NmM9HA2MQGI)

---

## Task 11 — PGP, GPG and AES

### PGP

**PGP** stands for Pretty Good Privacy. It is a system/software family used for:
- Encrypting files and messages.
- Digitally signing data.
- Protecting communications.

### GPG / GnuPG

**GnuPG (GPG)** is an open-source implementation of the OpenPGP standard.

In CTFs, a file or message may be encrypted with GPG and require the correct private key to decrypt.

The lesson notes:
- A private key may be protected with a passphrase.
- The key provided in this task is not passphrase-protected.
- For a passphrase-protected key, tools such as `gpg2john` can convert supported key material into a format that John the Ripper can audit.

Resources:
- [GnuPG official website](https://gnupg.org/)
- [GPG manual](https://www.gnupg.org/gph/de/manual/r1023.html)

### AES

**AES** stands for Advanced Encryption Standard. It is a symmetric block cipher selected to replace DES.

Key points:
- AES operates on fixed-size blocks of data.
- AES supports 128-, 192-, and 256-bit keys.
- DES is obsolete for modern security because of its short key length and other limitations.

Lesson video:
[AES explained — Computerphile](https://www.youtube.com/watch?v=O4xNJsjtN6E)

---

## Task 12 — The Future: Quantum Computers and Encryption

The lesson introduces the possible impact of sufficiently capable quantum computers on today's cryptographic algorithms.

### Asymmetric cryptography

RSA and elliptic-curve cryptography rely on mathematical problems that are difficult for classical computers. A sufficiently powerful, fault-tolerant quantum computer running Shor's algorithm could solve the relevant factoring and discrete-logarithm problems much more efficiently, threatening common RSA and ECC deployments.

### Symmetric cryptography

Quantum attacks affect symmetric algorithms differently:
- Grover's algorithm gives a theoretical quadratic speed-up for unstructured key search.
- Larger symmetric keys help maintain security margins.
- The lesson's broad recommendation is to prefer AES-256 for a stronger margin against quantum search than AES-128.

### Post-quantum cryptography

**Post-quantum cryptography (PQC)** refers to algorithms designed to resist attacks from both classical and quantum computers.

Migration to quantum-resistant algorithms requires planning and implementation; it is not simply a matter of waiting for a future computer.

Resources supplied by the lesson:
- [NIST IR 8105 — Report on Post-Quantum Cryptography](https://doi.org/10.6028/NIST.IR.8105)
- *Cryptography Apocalypse* by Roger A. Grimes

**Scope note:** The lesson's estimate of when sufficiently powerful quantum computers might be available is a forecast, not a guaranteed date.

---

## Quick Comparison Tables

### Encryption, hashing, encoding, and signatures

| Concept | Main purpose | Reversible? |
|---|---|---|
| Encryption | Confidentiality | Yes, with the appropriate key |
| Hashing | Integrity checks and password verification | Designed to be one-way |
| Encoding | Data representation | Normally yes, without a secret |
| Digital signature | Authenticity and integrity verification | Verification is possible with the public key; it is not decryption |

### Key types and common uses

| Mechanism | Key arrangement | Main role |
|---|---|---|
| AES | Shared secret key | Efficient data encryption |
| RSA | Public/private pair | Encryption in some schemes, signatures, and key-related operations |
| ECC | Public/private pair | Signatures and key agreement, depending on scheme |
| Diffie–Hellman | Private ephemeral values and public parameters | Establish shared secret material |
| SSH public-key authentication | Client private key and server-authorized public key | Authenticate the SSH client |

### Common misunderstandings

| Confusion | Correct understanding |
|---|---|
| Base64 is encryption | Base64 is encoding, not secrecy. |
| A hash is encryption | Hashing is designed to be one-way. |
| A signature encrypts a document | A signature proves authenticity/integrity; it does not provide confidentiality. |
| An SSH key passphrase authenticates to the server | It protects the private key locally. |
| Diffie–Hellman authenticates a person | DH establishes shared secret material; authentication is separate. |
| A certificate is just a public key | A certificate binds an identity to a public key and is signed by a CA. |

---

## SOC Analyst Perspective

Cryptography appears in network monitoring, endpoint investigations, incident response, and secure system administration.

As a SOC analyst, I should understand:

1. **Encrypted traffic:** Encryption protects users, but can make malicious activity harder to inspect. Detection may rely on metadata, endpoint telemetry, DNS, certificates, and behavior.
2. **Certificate warnings:** Unexpected or invalid certificates may result from configuration errors, expiry, interception, or other suspicious activity. They require investigation rather than automatic conclusions.
3. **SSH key exposure:** A stolen private key may allow access to systems that trust it. Unexpected SSH key changes and unusual key-based logins deserve attention.
4. **Weak cryptography:** Legacy algorithms and weak configurations can expose sensitive information.
5. **Data protection:** Sensitive information should be protected in storage and during transmission.
6. **Integrity verification:** Hashes can help verify file changes, provided the expected hash comes from a trusted source.

---

## Important Definitions — Quick Revision

| Term | Meaning |
|---|---|
| Plaintext | Original unencrypted data |
| Ciphertext | Encrypted data |
| Cipher | Encryption/decryption algorithm |
| Key | Value used by a cryptographic operation |
| Passphrase | Secret used to protect a key |
| Symmetric encryption | Same secret key for encryption and decryption |
| Asymmetric cryptography | Public/private key pair |
| Modulo | Remainder operation |
| RSA | Public-key algorithm based on difficulty of factoring large composites |
| Public key | Key that can be shared |
| Private key | Key that must be protected |
| Digital signature | Cryptographic proof of authenticity and integrity |
| Certificate | Signed binding between an identity and a public key |
| CA | Certificate Authority |
| Diffie–Hellman | Key agreement method for deriving shared secret material |
| PGP | Pretty Good Privacy |
| GPG | GNU implementation of OpenPGP |
| AES | Advanced Encryption Standard |
| PQC | Post-quantum cryptography |

## Self-Test Questions

1. What is the difference between plaintext and ciphertext?
2. Why is Base64 not encryption?
3. What is the difference between a cryptographic key and a passphrase?
4. What three security goals does cryptography help support?
5. Why should passwords generally be hashed rather than reversibly encrypted for authentication storage?
6. What does the modulo operator return?
7. Why is modulo not generally reversible?
8. How does symmetric encryption differ from asymmetric cryptography?
9. What are the RSA variables `p`, `q`, `n`, `e`, `d`, `m`, and `c`?
10. Why is factoring the RSA modulus relevant to RSA security?
11. Why do secure network protocols use hybrid cryptography?
12. What is a digital signature intended to prove?
13. What is the purpose of a certificate chain?
14. What is the difference between an SSH private-key passphrase and SSH server authentication?
15. What does `authorized_keys` contain?
16. What is the purpose of Diffie–Hellman key exchange?
17. Why does unauthenticated key exchange remain vulnerable to a man-in-the-middle attack?
18. What are PGP and GPG?
19. What is AES, and how does it differ from DES?
20. Why are RSA and ECC vulnerable to sufficiently powerful quantum computers?
21. What is post-quantum cryptography?

## My Key Takeaways

- I learned the difference between plaintext, ciphertext, encryption, encoding, keys, and passphrases.
- I understood why cryptography supports confidentiality, integrity, and authenticity.
- I learned why password storage normally relies on secure password hashing rather than reversible encryption.
- I practised understanding modulo arithmetic and why it appears in cryptographic algorithms.
- I compared symmetric encryption such as AES with asymmetric cryptography such as RSA and ECC.
- I learned the purpose of RSA variables and how RSA challenge questions use them.
- I understood the general role of public-key cryptography in establishing symmetric session keys.
- I learned how digital signatures and certificate chains help establish authenticity and trust.
- I understood SSH key authentication, private-key protection, passphrases, and `authorized_keys`.
- I learned how Diffie–Hellman lets two parties establish shared secret material over an observable channel.
- I became familiar with PGP, GPG, and AES.
- I learned why quantum computing creates a future challenge for RSA and ECC, and why post-quantum cryptography matters.

