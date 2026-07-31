# OverTheWire Bandit Level 31 → 32  
**Level:** 31 → 32   
**Date:** 31 July 2026

---

# Objective

The goal of this level is to learn how to create a file, bypass `.gitignore`, commit changes, and push them to a remote Git repository.

This level demonstrates how Git ignores files, how ignored files can still be staged intentionally, and how remote Git servers can validate commits using server-side hooks before accepting a push.

---

# Understanding the Challenge

Unlike the previous Git levels, this challenge required making changes to the repository rather than simply reading its contents.

The instructions inside the repository required:

- Create a file named **key.txt**
- Add the text:

```text
May I come in?
```

- Commit the changes
- Push them to the remote repository

However, the repository also contained a `.gitignore` file that prevented Git from tracking `.txt` files.

---

# Step 1 - Create a Working Directory

First, I created a directory for this level.

```bash
mkdir bandit31
cd bandit31
```

---

# Step 2 - Clone the Repository

I cloned the repository using SSH.

```bash
git clone ssh://bandit31-git@bandit.labs.overthewire.org:2220/home/bandit31-git/repo
```

When prompted, I entered the **Bandit31** password.

---

# Step 3 - Navigate into the Repository

```bash
cd repo
```

---

# Step 4 - Read the Challenge Instructions

I opened the README file.

```bash
cat README.md
```

Output:

```text
This time your task is to push a file to the remote repository.

Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master
```

The repository instructed me to create a file named **key.txt** containing the required message.

---

# Step 5 - Check the `.gitignore` File

Before creating the file, I checked the repository's ignore rules.

```bash
cat .gitignore
```

Output:

```text
*.txt
```

This rule tells Git to ignore every file ending in `.txt`.

That means the required `key.txt` file would **not** be tracked by default.

---

# Step 6 - Create the Required File

I created the file using:

```bash
echo "May I come in?" > key.txt
```

The `>` operator creates the file if it does not exist and writes the specified text into it.

---

# Step 7 - Force Git to Stage the File

Since `.gitignore` ignored `key.txt`, I forced Git to add it.

```bash
git add -f key.txt
```

The `-f` (force) option overrides `.gitignore` and stages the file.

---

# Step 8 - Configure Git Identity

Before creating a commit, Git required a username and email.

I configured them locally.

```bash
git config user.name "Abhinav"

git config user.email "abhinav@example.com"
```

These settings identify the author of the commit.

---

# Step 9 - Commit the Changes

I created a commit containing the new file.

```bash
git commit -m "Add key.txt"
```

The commit records the staged changes in the repository history.

---

# Step 10 - Push the Commit

Finally, I pushed the commit to the remote repository.

```bash
git push origin master
```

The remote Git server verified the submission using a **pre-receive hook**.

After validation, it returned the password for the next Bandit level.

---

# Password Obtained

```text
pWuj5jBQ6IgV0NXwiH6g1pXRF8S1YvbT
```

---

# Commands Used

```bash
mkdir bandit31

cd bandit31

git clone ssh://bandit31-git@bandit.labs.overthewire.org:2220/home/bandit31-git/repo

cd repo

cat README.md

cat .gitignore

echo "May I come in?" > key.txt

git add -f key.txt

git config user.name "Abhinav"

git config user.email "abhinav@example.com"

git commit -m "Add key.txt"

git push origin master
```

---

# Understanding the Commands

## mkdir

```bash
mkdir bandit31
```

Creates a new directory for the challenge.

---

## cd

```bash
cd bandit31
```

Moves into the working directory.

Later,

```bash
cd repo
```

moves into the cloned Git repository.

---

## git clone

```bash
git clone ssh://bandit31-git@bandit.labs.overthewire.org:2220/home/bandit31-git/repo
```

Downloads the remote Git repository to the local machine using SSH.

---

## cat

```bash
cat README.md
```

Displays the challenge instructions.

```bash
cat .gitignore
```

Displays the repository's ignore rules.

---

## echo

```bash
echo "May I come in?" > key.txt
```

Creates a new file named `key.txt` and writes the specified text into it.

The `>` operator redirects the output into a file.

---

## git add -f

```bash
git add -f key.txt
```

Stages a file even if it matches a rule inside `.gitignore`.

Normally Git would refuse to stage ignored files.

The `-f` option forces Git to include the file.

---

## git config

```bash
git config user.name "Abhinav"

git config user.email "abhinav@example.com"
```

Configures the author's identity for commits.

Git stores this information inside every commit.

---

## git commit

```bash
git commit -m "Add key.txt"
```

Creates a new commit containing the staged changes.

`-m`

Allows the commit message to be specified directly.

---

## git push

```bash
git push origin master
```

Uploads the local commits to the remote repository.

### Breakdown

```
origin
```

The remote repository.

```
master
```

The branch being pushed.

---

# What is `.gitignore`?

`.gitignore` is a special Git file that specifies files Git should ignore.

Example:

```text
*.txt
```

This tells Git:

> Ignore every file ending with `.txt`.

Commonly ignored files include:

- Log files
- Temporary files
- Build artifacts
- Environment files
- IDE configuration files

Ignored files are not tracked unless they are explicitly forced.

---

# What is `git add -f`?

Normally:

```bash
git add key.txt
```

would fail because `key.txt` matches the `.gitignore` rule.

Using:

```bash
git add -f key.txt
```

forces Git to stage the file anyway.

This is useful when a specific ignored file must still be committed.

---

# What is a Git Commit?

A commit is a snapshot of the repository at a particular point in time.

Each commit records:

- Files changed
- Author
- Date and time
- Commit message

Every commit has a unique SHA-1 hash that identifies it.

---

# What is a Pre-Receive Hook?

A **pre-receive hook** is a server-side script that runs **before** Git accepts a push.

It can:

- Validate commits
- Reject invalid pushes
- Enforce repository policies
- Run automated checks

In this challenge, the hook checked whether:

- `key.txt` existed
- It contained the required text
- The push met the challenge requirements

Only after successful validation did the server reveal the next password.

---

# Workflow

```text
Create Working Directory
          │
          ▼
Clone Repository
          │
          ▼
Read Instructions
          │
          ▼
Check .gitignore
          │
          ▼
Create key.txt
          │
          ▼
Force Stage File
          │
          ▼
Configure Git Identity
          │
          ▼
Commit Changes
          │
          ▼
Push to Remote
          │
          ▼
Pre-Receive Hook Validation
          │
          ▼
Retrieve Password
          │
          ▼
Login as bandit32
```

---

# Key Concepts Learned

- Git Repository
- `.gitignore`
- Git Staging
- `git add -f`
- Git Commit
- Git Push
- Git Configuration
- Server-side Hooks
- Pre-Receive Hooks
- Repository Validation

---
