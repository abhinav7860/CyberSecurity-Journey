# OverTheWire Bandit Level 28 → 29
**Level:** 28 → 29  
**Date:** 30 July 2026

---

# Objective

The goal of this level is to learn how to inspect a Git repository's commit history and recover information that was removed from the latest version of a file.

This level demonstrates that Git stores the complete history of a project, allowing previous versions of files to be viewed even after changes have been made.

---

# Understanding the Challenge

After cloning the repository, the `README.md` file appeared to have its password removed.

The repository hinted that an **information leak had been fixed**, suggesting the password might still exist in an earlier commit.

Since Git keeps every commit in its history, I could inspect previous versions of the file to recover the hidden password.

---

# Step 1 - Create a Working Directory

First, I created a directory for this level.

```bash
mkdir bandit28
cd bandit28
```

---

# Step 2 - Clone the Repository

I cloned the repository using Git over SSH.

```bash
git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo
```

When prompted, I entered the **Bandit28** password.

Git downloaded the repository to my local machine.

---

# Step 3 - Navigate into the Repository

```bash
cd repo
```

---

# Step 4 - List the Repository Files

```bash
ls
```

Output:

```text
README.md
```

The repository contained a single README file.

---

# Step 5 - Read the README File

```bash
cat README.md
```

Output:

```text
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx
```

The password had been replaced with **xxxxxxxxxx**, meaning it had been removed from the latest version.

---

# Step 6 - View the Commit History

To investigate earlier versions of the repository, I displayed the commit history.

```bash
git log
```

Output:

```text
commit e2e1de5396037bafb23e9bb37c12ebea9b911cfd
    fix info leak

commit 2678cfadd8f2a347bc23e1ea491f702e5b184709
    add missing data

commit 9530d526c22b9e6e6ae11070ef8ff8ee21eb2e02
    initial commit of README.md
```

The latest commit message:

```text
fix info leak
```

strongly suggested that sensitive information had been removed from the repository.

---

# Step 7 - View the Previous Commit

I inspected the previous version of the repository using:

```bash
git show HEAD~1
```

or

```bash
git show 2678cfadd8f2a347bc23e1ea491f702e5b184709
```

The previous version of **README.md** contained the real password for **bandit29**.

Output:

```text
Em7eGtqaMySwNFjCpwzzHhLhospOcdt0
```

---

# Password Obtained

```text
Em7eGtqaMySwNFjCpwzzHhLhospOcdt0
```

---

# Commands Used

```bash
mkdir bandit28

cd bandit28

git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo

cd repo

ls

cat README.md

git log

git show HEAD~1
```

---

# Understanding the Commands

## mkdir

```bash
mkdir bandit28
```

Creates a new working directory.

---

## cd

```bash
cd bandit28
```

Moves into the newly created directory.

Later,

```bash
cd repo
```

moves into the cloned Git repository.

---

## git clone

```bash
git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo
```

Downloads the remote Git repository to the local machine using SSH.

---

## ls

```bash
ls
```

Lists all files in the current directory.

Output:

```text
README.md
```

---

## cat

```bash
cat README.md
```

Displays the contents of the README file.

The latest version showed the password had been hidden.

---

## git log

```bash
git log
```

Displays the complete commit history of the repository.

Each entry contains:

- Commit hash
- Author
- Date
- Commit message

Example:

```text
fix info leak
```

This commit message suggested that sensitive information had been removed.

---

## git show

```bash
git show HEAD~1
```

Displays the previous commit.

`HEAD`

Represents the latest commit.

`~1`

Means one commit before the latest.

Equivalent command:

```bash
git show <commit-hash>
```

This command displays:

- Commit details
- Files changed
- Exact modifications made

---

# What is Git History?

Git never immediately deletes previous versions of files.

Instead, every change is stored as a **commit**, creating a complete history of the project.

Example:

```text
Commit 1
README created
        │
        ▼
Commit 2
Password added
        │
        ▼
Commit 3
Password removed
```

Even though the latest version hides the password, Git still stores the earlier commits.

---

# Why is This Important?

Developers often assume that deleting sensitive information from a repository removes it permanently.

In reality:

- Previous commits still exist.
- Anyone with access to the repository can inspect older commits.
- Accidentally committed secrets should be removed using Git history rewriting tools, not by simply editing the latest file.

This is why developers should avoid committing passwords, API keys, or tokens to Git repositories.

---

# Workflow

```text
Create Working Directory
          │
          ▼
Clone Repository
          │
          ▼
Open Repository
          │
          ▼
Read README
          │
          ▼
Password Hidden
          │
          ▼
View Commit History
          │
          ▼
Find "fix info leak"
          │
          ▼
Inspect Previous Commit
          │
          ▼
Recover Password
          │
          ▼
Login as bandit29
```

---

