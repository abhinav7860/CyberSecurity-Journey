# OverTheWire Bandit Level 30 → 31 
**Level:** 30 → 31    
**Date:** 30 July 2026

---

# Objective

The goal of this level is to learn how to inspect **Git tags** to discover hidden information stored in a Git repository.

This level introduces another important Git feature called **tags**, which are commonly used to mark releases or important points in a project's history.

---

# Understanding the Challenge

After cloning the repository, the README file did not contain any useful information.

There was only one commit and no additional branches, meaning the password was not hidden in the commit history or another branch.

The next step was to inspect other Git objects, eventually leading to the discovery of a Git tag containing the password.

---

# Step 1 - Create a Working Directory

First, I created a directory for this level.

```bash
mkdir bandit30
cd bandit30
```

---

# Step 2 - Clone the Repository

I cloned the Git repository using SSH.

```bash
git clone ssh://bandit30-git@bandit.labs.overthewire.org:2220/home/bandit30-git/repo
```

When prompted, I entered the **Bandit30** password.

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

Only a single README file was present.

---

# Step 5 - Read the README

```bash
cat README.md
```

Output:

```text
just an empty file... muahaha
```

The README intentionally contained no useful information.

---

# Step 6 - Check the Commit History

Since previous levels hid information in older commits, I checked the commit history.

```bash
git log --oneline
```

Output:

```text
929c564 (HEAD -> master, origin/master, origin/HEAD) initial commit of README.md
```

There was only one commit.

So the password was not hidden in the commit history.

---

# Step 7 - Check Available Branches

Next, I checked for other branches.

```bash
git branch -a
```

Output:

```text
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
```

There were no additional branches to inspect.

---

# Step 8 - List Git Tags

Since commits and branches did not reveal anything, I checked whether the repository contained any Git tags.

```bash
git tag
```

Output:

```text
secret
```

A tag named **secret** existed in the repository.

---

# Step 9 - Inspect the Tag

To view the contents of the tag, I used:

```bash
git show secret
```

Output:

```text
82NkymblpGBYmIXG6ZQ8YldBYstHpfUf
```

The tag contained the password for **Bandit31**.

---

# Password Obtained

```text
82NkymblpGBYmIXG6ZQ8YldBYstHpfUf
```

---

# Commands Used

```bash
mkdir bandit30

cd bandit30

git clone ssh://bandit30-git@bandit.labs.overthewire.org:2220/home/bandit30-git/repo

cd repo

ls

cat README.md

git log --oneline

git branch -a

git tag

git show secret
```

---

# Understanding the Commands

## mkdir

```bash
mkdir bandit30
```

Creates a new working directory.

---

## cd

```bash
cd bandit30
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
git clone ssh://bandit30-git@bandit.labs.overthewire.org:2220/home/bandit30-git/repo
```

Downloads the complete Git repository from the remote server.

---

## ls

```bash
ls
```

Lists the files inside the repository.

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

In this level, the README was intentionally empty.

---

## git log --oneline

```bash
git log --oneline
```

Displays the commit history in a compact format.

Example:

```text
929c564 initial commit of README.md
```

Since only one commit existed, there were no previous commits to investigate.

---

## git branch -a

```bash
git branch -a
```

Lists all local and remote branches.

The output confirmed that only the **master** branch existed.

---

## git tag

```bash
git tag
```

Lists every tag in the repository.

Output:

```text
secret
```

This revealed the existence of a hidden Git tag.

---

## git show

```bash
git show secret
```

Displays information about a Git object.

When used with a tag, it shows:

- Tag details
- Referenced object
- Stored message or contents

In this challenge, the tag itself contained the password.

---

# What is a Git Tag?

A **Git tag** is a named reference to a specific point in a repository's history.

Tags are commonly used to:

- Mark software releases
- Identify important versions
- Label milestones
- Reference specific commits

Example:

```text
Commit A
     │
Commit B  ← v1.0
     │
Commit C
     │
Commit D  ← v2.0
```

Unlike branches, tags usually do **not** move after they are created.

---

# Branches vs Tags

| Branch | Tag |
|---------|-----|
| Changes over time | Fixed reference |
| Used for development | Used to mark important versions |
| Can receive new commits | Usually points to an existing commit |
| Frequently updated | Rarely changed |

---

# Why Check Tags?

When performing security assessments, developers and penetration testers should inspect:

- Commits
- Branches
- Tags

Sensitive information can accidentally be stored in any Git object.

Even if the files appear clean, hidden objects like tags may still contain secrets.

---

# Workflow

```text
Create Working Directory
          │
          ▼
Clone Repository
          │
          ▼
Read README
          │
          ▼
Nothing Found
          │
          ▼
Check Commit History
          │
          ▼
Only One Commit
          │
          ▼
Check Branches
          │
          ▼
Only Master Branch
          │
          ▼
List Git Tags
          │
          ▼
Find "secret"
          │
          ▼
Inspect Tag
          │
          ▼
Retrieve Password
          │
          ▼
Login as bandit31
```

---

# What I Learned

This level introduced Git tags and showed that important information can be stored outside the normal file structure. After confirming that there were no useful commits or additional branches, I listed the repository's tags and found one named `secret`. Using `git show`, I viewed the tag's contents and recovered the password for the next level. This level demonstrated that during a Git security assessment, it's important to inspect every Git object—not just the working files, commits, or branches.

---

