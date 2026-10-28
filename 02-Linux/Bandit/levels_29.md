# OverTheWire Bandit Level 29 → 30
**Level:** 29 → 30    
**Date:** 30 July 2026

---

# Objective

The goal of this level is to learn how to explore Git branches and retrieve information stored in a development branch.

This level demonstrates that not all information is stored in the default branch. Developers often use multiple branches to work on new features or test changes before merging them into production.

---

# Understanding the Challenge

After cloning the repository, the `README.md` file on the default branch did not contain the password.

Instead, it displayed:

```text
password: <no passwords in production!>
```

This suggested that the password might exist in another branch.

Git repositories can have multiple branches, so the next step was to inspect all available branches.

---

# Step 1 - Create a Working Directory

First, I created a directory for this level.

```bash
mkdir bandit29
cd bandit29
```

---

# Step 2 - Clone the Repository

I cloned the remote Git repository using SSH.

```bash
git clone ssh://bandit29-git@bandit.labs.overthewire.org:2220/home/bandit29-git/repo
```

When prompted, I entered the **Bandit29** password.

After authentication, Git downloaded the repository to my local machine.

---

# Step 3 - Navigate into the Repository

```bash
cd repo
```

---

# Step 4 - Read the README File

```bash
cat README.md
```

Output:

```text
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: <no passwords in production!>
```

The password was intentionally removed from the production branch.

---

# Step 5 - List All Branches

To check whether other branches existed, I ran:

```bash
git branch -a
```

Output:

```text
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
  remotes/origin/sploits-dev
```

Besides the default **master** branch, the repository also contained:

- origin/dev
- origin/sploits-dev

The **dev** branch looked like the most likely place to continue.

---

# Step 6 - Switch to the Development Branch

I created a local branch that tracks the remote **origin/dev** branch.

```bash
git checkout -b dev origin/dev
```

Output:

```text
Branch 'dev' set up to track remote branch 'dev' from 'origin'.
Switched to a new branch 'dev'
```

Now I was working inside the development branch.

---

# Step 7 - Read the README Again

```bash
cat README.md
```

This time the README contained the actual password for **bandit30**.

Output:

```text
jq9Dfg2rXsfYsWMgFuKlXhphjdH7USgX
```

---

# Password Obtained

```text
jq9Dfg2rXsfYsWMgFuKlXhphjdH7USgX
```

---

# Commands Used

```bash
mkdir bandit29

cd bandit29

git clone ssh://bandit29-git@bandit.labs.overthewire.org:2220/home/bandit29-git/repo

cd repo

cat README.md

git branch -a

git checkout -b dev origin/dev

cat README.md
```

---

# Understanding the Commands

## mkdir

```bash
mkdir bandit29
```

Creates a new directory for the challenge.

---

## cd

```bash
cd bandit29
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
git clone ssh://bandit29-git@bandit.labs.overthewire.org:2220/home/bandit29-git/repo
```

Downloads a complete copy of the remote Git repository using SSH.

---

## cat

```bash
cat README.md
```

Displays the contents of the README file.

On the **master** branch, the password had been removed.

On the **dev** branch, the password was available.

---

## git branch -a

```bash
git branch -a
```

Lists every branch in the repository.

### Local Branches

Example:

```text
master
```

These exist only on your computer.

### Remote Branches

Example:

```text
origin/dev
origin/master
```

These exist on the remote Git server.

The `-a` option means:

```
All Branches
```

---

## git checkout

```bash
git checkout -b dev origin/dev
```

This command performs two actions:

### `-b`

Creates a new local branch.

### `origin/dev`

Uses the remote **dev** branch as the starting point.

The result is a local **dev** branch that tracks the remote branch.

---

# What is a Git Branch?

A Git branch is an independent line of development.

Developers use branches to:

- Develop new features
- Fix bugs
- Test changes
- Experiment safely

without affecting the main project.

Example:

```text
                master
                   │
                   │
        -------------------
        │                 │
      dev          sploits-dev
```

Each branch can contain different files or different versions of the same files.

---

# Why Use Multiple Branches?

Using branches allows developers to:

- Keep production stable
- Develop new features safely
- Test experimental code
- Merge completed work later

The **master** branch usually contains production-ready code, while development branches may contain unfinished work or additional information.

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
Password Missing
          │
          ▼
List All Branches
          │
          ▼
Discover dev Branch
          │
          ▼
Switch to dev
          │
          ▼
Read README Again
          │
          ▼
Retrieve Password
          │
          ▼
Login as bandit30
```

---


# What I Learned

This level taught me that a Git repository can contain multiple branches, each representing a different version of the project. I learned how to list both local and remote branches using `git branch -a` and how to switch to a remote development branch using `git checkout -b`. By exploring the `dev` branch, I found information that was intentionally removed from the production branch. This demonstrated why security reviews should include every branch in a repository, not just the default branch.

---

