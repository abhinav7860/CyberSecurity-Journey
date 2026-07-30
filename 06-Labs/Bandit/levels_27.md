# OverTheWire Bandit Level 27 → 28
**Level:** 27 → 28   
**Date:** 30 July 2026

---

# Objective

The goal of this level is to learn how to clone a Git repository over SSH and retrieve the password for **bandit28**.

This level introduces using **Git over SSH** and demonstrates how repositories can store information that can be accessed after authentication.

---


# Step 1 - Create a Working Directory

First, I created a directory to keep the repository organized.

```bash
mkdir bandit27
cd bandit27
```

This creates a new folder named **bandit27** and moves into it.

---

# Step 2 - Clone the Git Repository

I cloned the repository using Git over SSH.

```bash
git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo
```

When prompted, I entered the **bandit27** password.

Git authenticated using SSH and downloaded the repository to my local machine.

Output:

```text
Cloning into 'repo'...
```

---

# Step 3 - Enter the Repository

After cloning completed successfully, I moved into the repository.

```bash
cd repo
```

---

# Step 4 - View Repository Files

To see what files were present, I listed the contents.

```bash
ls
```

Output:

```text
README
```

The repository contained a single file named **README**.

---

# Step 5 - Read the README File

I displayed the contents of the README file.

```bash
cat README
```

Inside the file was the password for the next Bandit level.

Output:

```text
y8Yd2ssKcpHpud7UvOSOxwamRMzIGIeQ
```

---

# Password Obtained

```text
y8Yd2ssKcpHpud7UvOSOxwamRMzIGIeQ
```

---

# Commands Used

```bash
mkdir bandit27

cd bandit27

git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo

cd repo

ls

cat README
```

---

# Understanding the Commands

## mkdir

```bash
mkdir bandit27
```

Creates a new directory named **bandit27**.

---

## cd

```bash
cd bandit27
```

Changes the current working directory.

Later,

```bash
cd repo
```

moves into the cloned Git repository.

---

## git clone

```bash
git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo
```

Downloads a remote Git repository to the local machine.

### Breakdown

```
ssh://
```

Specifies that Git should use the SSH protocol.

```
bandit27-git@
```

The SSH username used to access the repository.

```
bandit.labs.overthewire.org
```

The remote Git server.

```
:2220
```

The SSH port used by OverTheWire.

```
/home/bandit27-git/repo
```

The location of the Git repository on the server.

---

## ls

```bash
ls
```

Lists the files inside the repository.

Output:

```text
README
```

---

## cat

```bash
cat README
```

Displays the contents of the README file.

In this level, the README contained the password for the next Bandit level.

---

# What is Git?

Git is a **Version Control System (VCS)** used to track changes in files and source code over time.

It allows developers to:

- Track file changes
- Collaborate with others
- Restore previous versions
- Manage project history

Popular platforms that use Git include:

- GitHub
- GitLab
- Bitbucket

---

# What is Git Clone?

`git clone` creates a complete copy of a remote repository on your local machine.

It downloads:

- Project files
- Commit history
- Branches
- Repository metadata

General syntax:

```bash
git clone <repository-url>
```

---

# Why SSH?

Git supports multiple protocols, including:

- HTTPS
- SSH

SSH is commonly used because it provides:

- Encrypted communication
- Authentication
- Secure access without exposing passwords repeatedly (using SSH keys)

In this Bandit level, authentication was performed using the **bandit27** password.

---

# Workflow

```text
Create Working Directory
          │
          ▼
Clone Git Repository
          │
          ▼
Authenticate with SSH
          │
          ▼
Repository Downloaded
          │
          ▼
Open Repository
          │
          ▼
Read README
          │
          ▼
Retrieve Password
          │
          ▼
Login as bandit28
```

---

