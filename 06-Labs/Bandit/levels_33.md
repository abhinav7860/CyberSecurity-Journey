# OverTheWire Bandit – Level 33 (Final Level)

**Platform:** OverTheWire  
**Room:** Bandit  
**Level:** 33 (Final Level)  
**Date:** 31 July 2026

---

# Objective

The objective of this final level was simply to log in using the password obtained from the previous level and verify the completion of the Bandit wargame.

Unlike previous levels, there is no challenge to solve. Instead, this level serves as the official completion point of the Bandit series and congratulates players for successfully finishing all levels.

---

# Overview

After solving **Bandit Level 32 → 33**, I logged into the Bandit33 account using the password obtained from the previous challenge.

Upon logging in, I reached the final level of the Bandit wargame and confirmed that there were no further challenges to complete.

---

# Step 1 - Connect to the Server

I connected to the Bandit server using SSH.

```bash
ssh bandit33@bandit.labs.overthewire.org -p 2220
```

After entering the Bandit33 password, I successfully logged into the final account.

---

# Step 2 - List the Available Files

I listed the files in the home directory.

```bash
ls
```

Output:

```text
README.txt
```

The only file available was **README.txt**.

---

# Step 3 - Read the Final Message

I opened the README file.

```bash
cat README.txt
```

Output:

```text
Congratulations on solving the last level of this game!

At this moment, there are no more levels to play in this game.
However, we are constantly working on new levels and will most likely
expand this game with more levels soon.

Keep an eye out for an announcement on our usual communication channels!

In the meantime, you could play some of our other wargames.

If you have an idea for an awesome new level, please let us know!
```

This confirmed that I had successfully completed the entire Bandit wargame.

---

# Commands Used

```bash
ssh bandit33@bandit.labs.overthewire.org -p 2220

ls

cat README.txt
```

---

# Understanding the Commands

## ssh

```bash
ssh bandit33@bandit.labs.overthewire.org -p 2220
```

Creates a secure remote connection to the Bandit server.

`-p 2220`

Specifies the custom SSH port used by OverTheWire.

---

## ls

```bash
ls
```

Lists the contents of the current directory.

In this level, the directory contained only one file:

```text
README.txt
```

---

## cat

```bash
cat README.txt
```

Displays the contents of the README file, which contains the official completion message for the Bandit wargame.

---

# Workflow

```text
Login as bandit33
          │
          ▼
List Home Directory
          │
          ▼
Open README.txt
          │
          ▼
Read Congratulations Message
          │
          ▼
Bandit Wargame Completed
```

---

# What I Learned

Although this level did not contain a technical challenge, it marked the successful completion of the Bandit wargame. Throughout the journey, I developed a solid foundation in Linux command-line usage, file permissions, shell behavior, networking, Git, cron jobs, encoding and decoding techniques, and basic privilege escalation concepts. More importantly, I learned how to approach unfamiliar problems methodically by exploring the system, reading documentation, and combining Linux utilities to solve challenges.

---

# Skills Gained Throughout Bandit

During the Bandit wargame, I gained practical experience with:

- Linux command-line navigation
- File and directory management
- File permissions and ownership
- Hidden files and symbolic links
- SSH authentication
- Searching and filtering files
- Text processing with Linux utilities
- File compression and extraction
- Base64 and hexadecimal encoding
- Network communication using Netcat
- Cron jobs and scheduled tasks
- Bash shell variables
- Restricted shell bypass techniques
- SUID binaries and privilege escalation
- Git repositories, branches, tags, commits, and remote repositories

---

# Personal Reflection

Bandit was my first complete Linux-based cybersecurity wargame, and it significantly improved my confidence in using the Linux terminal. Each level introduced a new concept while reinforcing skills learned in previous challenges. Instead of memorizing commands, I learned how to investigate systems, interpret command outputs, and think through problems logically. Documenting every level also helped me strengthen my understanding and build a structured cybersecurity knowledge base for future reference.

---

# Summary

Bandit Level 33 marks the successful completion of the OverTheWire Bandit wargame. While this level did not introduce a new technical challenge, it served as the final milestone in a series that covered essential Linux and cybersecurity concepts. Completing Bandit provided hands-on experience with Linux commands, networking, file permissions, Git, shell behavior, and privilege escalation, creating a strong foundation for more advanced cybersecurity labs and wargames.

---

# Next Steps

With Bandit completed , my next learning goals are:

- OverTheWire Natas (Web Security)
- TryHackMe Rooms
- Networking Fundamentals
- Web Application Security
- Active Directory Basics
- Capture The Flag (CTF) Challenges

This marks the end of my Bandit journey and the beginning of more advanced cybersecurity learning.