# TryHackMe — OhSINT Walkthrough
**Date Completed:** 11 August 2026
## Room Overview

---

# Introduction

**OhSINT** is a TryHackMe challenge based on **Open-Source Intelligence (OSINT)**.

The main objective is to gather information about a target using publicly available information and passive reconnaissance techniques.

The investigation covers:

- Careful image observation
- Metadata extraction
- Search engines
- Social media
- GitHub
- Wi-Fi intelligence
- Website investigation
- Web-page source inspection

In this challenge, we are given an image and need to use OSINT techniques to answer questions about the target.

---

# Step 1 — Extract Image Metadata

The first step is to inspect the image metadata.

A useful tool for this is:

```text
ExifTool
```

The metadata contains an important clue in the copyright/author information.

This reveals the target's online handle:

```text
OWoodflint
```

This username becomes the main OSINT pivot.

```text
Image
  ↓
Metadata
  ↓
OWoodflint
  ↓
Search public sources
```

---

# Step 2 — Investigate Twitter / X

Searching for:

```text
OWoodflint
```

leads to a Twitter/X profile.

The profile picture shows a:

```text
Cat
```

## Q1. What is this user's avatar of?

**Answer:**

```text
Cat
```

The target's social-media presence also provides a Wi-Fi BSSID that can be investigated later.

---

# Step 3 — Investigate GitHub

The same target can be found on GitHub.

The GitHub information provides answers to several questions.

## Q2. What city is this person in?

**Answer:**

```text
London
```

## Q4. What is his personal email address?

**Answer:**

```text
OWoodflint@gmail.com
```

## Q5. What site did you find his email address on?

**Answer:**

```text
GitHub
```

---

# Step 4 — Investigate the Wi-Fi BSSID

The target has exposed a Wi-Fi **BSSID** on Twitter/X.

A BSSID identifies a wireless access point and is commonly represented as a MAC address.

The walkthrough uses:

```text
WiGLE
```

The investigation process is:

```text
Find BSSID
   ↓
Open WiGLE
   ↓
Use Advanced Search
   ↓
Enter BSSID under Network Characteristics
   ↓
Query
   ↓
Identify the associated Wi-Fi network
```

The SSID identified in the walkthrough was:

```text
UnileverWifi
```

## Q3. What is the SSID of the WAP he connected to?

**Answer:**

```text
UnileverWifi
```

---

# Step 5 — Investigate the Target's Blog

Further investigation leads to the target's blog.

A blog post reveals that the target went to:

```text
New York
```

on holiday.

## Q6. Where has he gone on holiday?

**Answer:**

```text
New York
```

---

# Step 6 — Inspect Website Source Code

The blog contains another important clue.

The walkthrough shows that sensitive information was exposed in the webpage's source code.

The source can be inspected using:

```text
View Page Source
```

or browser developer tools.

The exposed password was:

```text
pennYDr0pper.!
```

## Q7. What is the person's password?

**Answer:**

```text
pennYDr0pper.!
```

---

# Complete Answer Sheet

| Question | Answer |
|---|---|
| Q1. What is this user's avatar of? | `Cat` |
| Q2. What city is this person in? | `London` |
| Q3. What is the SSID of the WAP he connected to? | `UnileverWifi` |
| Q4. What is his personal email address? | `OWoodflint@gmail.com` |
| Q5. What site did you find his email address on? | `GitHub` |
| Q6. Where has he gone on holiday? | `New York` |
| Q7. What is the person's password? | `pennYDr0pper.!` |

---

# Investigation Chain

```text
Initial Image
      ↓
ExifTool
      ↓
Image Metadata
      ↓
OWoodflint
      ↓
Twitter / X
      ├── Cat avatar
      └── Wi-Fi BSSID
      ↓
GitHub
      ├── London
      └── OWoodflint@gmail.com
      ↓
WiGLE
      ↓
UnileverWifi
      ↓
Target Blog
      ├── New York holiday
      └── Password in webpage source
```

---

# Tools Used

## ExifTool

Used to extract metadata from the provided image.

Important clue:

```text
OWoodflint
```

## Search Engines

Used to search for the username and locate the target's public online presence.

## Twitter / X

Used to investigate the target's public profile and identify the avatar and Wi-Fi BSSID clue.

## GitHub

Used to find the target's city and personal email address.

## WiGLE

Used to investigate the Wi-Fi BSSID and identify the associated wireless network.

Result:

```text
UnileverWifi
```

## Website Source Inspection

Used to inspect the target's blog source code and identify the exposed password:

```text
pennYDr0pper.!
```

---

# Key Lessons Learned

## 1. Always Check Image Metadata

An image may contain useful information that is not visible when viewing it normally.

```text
Image
 ↓
Metadata
 ↓
Username / author clue
 ↓
Further OSINT
```

## 2. Usernames Are Powerful OSINT Pivots

Once a username is found, search for it across different public platforms.

```text
OWoodflint
   ↓
Twitter / X
GitHub
Blog
```

## 3. Social Media Can Expose Network Information

A publicly shared Wi-Fi BSSID can potentially be correlated with wireless databases such as WiGLE.

## 4. GitHub Can Expose Personal Information

Public GitHub profiles can contain information such as:

```text
Location
Email
Projects
Usernames
```

## 5. Inspect Website Source Code

Information can sometimes be present in HTML or JavaScript even when it is not visible on the rendered page.

Useful places to inspect include:

```text
View Source
Developer Tools
HTML
Comments
JavaScript
Metadata
```

## 6. Connect Information From Multiple Sources

The main OSINT skill in this room is connecting information:

```text
Metadata
   ↓
Username
   ↓
Social Media
   ↓
GitHub
   ↓
Wi-Fi Information
   ↓
WiGLE
   ↓
Blog
   ↓
Source Code
```
---