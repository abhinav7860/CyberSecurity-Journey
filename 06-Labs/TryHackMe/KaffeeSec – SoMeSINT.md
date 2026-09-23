# TryHackMe – KaffeeSec: SoMeSINT

**Date Completed:** 23 September 2026  
**Category:** OSINT / Social Media Intelligence  
**Difficulty:** Medium

## Overview

I completed the **KaffeeSec – SoMeSINT** room on TryHackMe. This room focused on passive Open-Source Intelligence (OSINT), social-media investigation, Google dorking, reverse-image searching, and website archiving.

The investigation focused on the fictional subject **Thomas Straussman** and his relevant Twitter/X and Reddit accounts. The room emphasizes passive collection and staying within the in-scope accounts.

---

## Investigation Target

**Subject:** Thomas Straussman

**Username:** `tstraussman`

The investigation started from this username and pivoted between Twitter/X, Reddit, Francesca's account, archived Reddit pages, and external paste links.

---

# Task 2 – Story

### Who hired you?

The person who hired me used the moniker:

```text
H
```

**Answer:**

```text
ks{H}
```

### Who are you investigating?

The target was:

```text
Thomas Straussman
```

**Answer:**

```text
ks{thomas straussman}
```

---

# Task 3 – Let's Get Started

## Finding Thomas's Social Accounts

I started with the known username:

```text
tstraussman
```

I used the username to locate the relevant Twitter/X and Reddit accounts. The room specifically says these are the in-scope platforms, so I kept the investigation passive.

## Thomas's Favorite Holiday

I checked Thomas's Twitter/X profile and found that his favorite holiday was:

```text
Christmas
```

**Answer:** `Christmas`

## Thomas's Birth Date

A birthday-related post indicated that Thomas turned 30 in December 2020.

Therefore:

```text
December 20, 1990
```

**Answer:** `12-20-1990`

## Thomas's Fiancée's Twitter Handle

By examining Thomas's Twitter/X account and followers, I identified his fiancée's account:

```text
@FHodgelink
```

**Answer:** `@FHodgelink`

## Thomas's Background Picture

The background/header image on Thomas's profile showed:

```text
Buddha
```

**Answer:** `Buddha`

---

# Task 4 – Account Enumeration and Shadowban API

## Source Module Used to Find the Accounts

The relevant account-enumeration module was:

```text
sfp_accounts
```

This is the Account Finder module.

**Answer:**

```text
sfp_accounts
```

## Shadowban API

The historical API endpoint used by the room was:

```text
https://shadowban.eu/.api/tstraussman
```

The live service is no longer available in the same form, so the original API response had to be treated as historical information.

The value of the `search` field was:

```text
ks{1346173539712380929}
```

**Answer:** `ks{1346173539712380929}`

---

# Task 5 – Connections, Connections

After gathering information from Thomas, I pivoted to his fiancée:

```text
@FHodgelink
```

I investigated her posts, images, and personal information.

## Where Did Thomas and His Fiancée Vacation?

I found a vacation photograph and investigated it using reverse-image searching and visual clues.

I also checked the image for metadata/EXIF information, but the copy available to me did not contain useful GPS/location data.

The location identified for the room was:

```text
Koblenz, Germany
```

**Answer:** `Koblenz, Germany`

### Reverse-image investigation

The process I followed was:

1. Upload the image to a reverse-image search engine.
2. Check visual matches.
3. Compare the landscape, buildings, mountains, and shoreline.
4. Search for the original/source image.
5. Correlate the result with Francesca's post and the context of the investigation.

An important lesson was that reverse-image tools can return visually similar places, so a result should be verified instead of accepted immediately.

## Francesca's Mother's Birthday

I searched Francesca's posts for family-related information.

**Answer:**

```text
December 25th
```

## Name of Their Cat

A post revealed that their cat was named:

```text
Gotank
```

**Answer:** `Gotank`

## What Show Does Francesca Like to Watch?

A post referenced:

```text
90 Day Fiancee
```

**Answer:** `90 Day Fiancee`

---

# Task 6 – Turn Back the Clock

This section moved the investigation to Reddit and introduced historical website analysis.

The main tools/methods were:

- Old Reddit
- Current Reddit
- Wayback Machine
- Archived snapshots
- Historical comments and posts

## Finding Thomas's Coworker

I opened Thomas's birthday Reddit post and checked its historical versions using the Wayback Machine.

The current version did not reveal the useful comment, so I selected the earliest useful archived snapshot.

The archived page contained the comment:

```text
Hey, It's Hans from work. Congrats!!
```

I then inspected the archived HTML and found the Reddit username associated with the commenter:

```text
minikhans
```

This gave me the pivot:

```text
Thomas
    ↓
Birthday Reddit post
    ↓
Archived comment
    ↓
"Hans from work"
    ↓
minikhans
```

The coworker's full name was:

```text
Hans Minik
```

**Answer:**

```text
ks{Hans Minik}
```

## Where Does His Coworker Live?

I pivoted to the Reddit account:

```text
minikhans
```

The account's posts/profile information indicated:

```text
Nuuk, Greenland
```

**Answer:**

```text
ks{Nuuk, Greenland}
```

## Finding the Paste ID

I examined historical versions of Hans's Reddit profile.

An archived post contained a Ghostbin link:

```text
https://ghostbin.com/paste/ww4ju
```

The final part of the URL was the required paste ID:

```text
ww4ju
```

**Answer:**

```text
ks{ww4ju}
```

### Lesson

URLs themselves can contain useful intelligence. In this case, the paste ID was directly visible in the URL structure.

## Password for the Next Link

Another historical post contained a Pastebin link and the password required for the next stage.

The password was:

```text
1qaz2wsx
```

**Answer:**

```text
ks{1qaz2wsx}
```

## Finding Thomas's Mistress

Using the information recovered from the previous stage, I accessed the relevant paste.

The email contained the recipient:

```text
Emilia Moller
```

This identified Thomas's mistress.

**Answer:**

```text
ks{Emilia Moller}
```

## Finding Thomas's Email Address

The same email revealed Thomas's email address:

```text
straussmanthom@mail.com
```

**Answer:**

```text
ks{straussmanthom@mail.com}
```

---

# Complete Answer List

| Task | Question | Answer |
|---|---|---|
| Story | Who hired you? | `ks{H}` |
| Story | Who are you investigating? | `ks{thomas straussman}` |
| Social OSINT | Thomas's favorite holiday | `Christmas` |
| Social OSINT | Thomas's birth date | `12-20-1990` |
| Social OSINT | Fiancée's Twitter handle | `@FHodgelink` |
| Social OSINT | Background picture | `Buddha` |
| Account Enumeration | Source module | `sfp_accounts` |
| Shadowban API | `search` value | `ks{1346173539712380929}` |
| Social Pivot | Vacation location | `Koblenz, Germany` |
| Social Pivot | Francesca's mother's birthday | `December 25th` |
| Social Pivot | Cat's name | `Gotank` |
| Social Pivot | Favorite show | `90 Day Fiancee` |
| Wayback / Reddit | Coworker's name | `ks{Hans Minik}` |
| Wayback / Reddit | Coworker's location | `ks{Nuuk, Greenland}` |
| Wayback / Reddit | Paste ID | `ks{ww4ju}` |
| Wayback / Reddit | Password | `ks{1qaz2wsx}` |
| Investigation Pivot | Thomas's mistress | `ks{Emilia Moller}` |
| Investigation Pivot | Thomas's email | `ks{straussmanthom@mail.com}` |

---

# Tools and Techniques Used

## Google / Search Engines

Used for:

- Username discovery
- Social-profile discovery
- Google dorking
- Finding indexed information

Example searches:

```text
"tstraussman"
site:twitter.com "tstraussman"
site:reddit.com "tstraussman"
```

## Twitter/X

Used to:

- Locate Thomas's account
- Review profile information
- Identify his fiancée
- Gather personal information
- Pivot to another account

## Reddit

Used to:

- Locate Thomas's Reddit account
- Investigate posts
- Identify connections
- Pivot to Hans's account

## Wayback Machine

Used to:

- Recover deleted/changed Reddit information
- Compare historical versions
- Find old comments
- Recover old posts and links
- Investigate historical versions of external pages

The most important discovery was the archived birthday-post comment from Hans.

## Reverse Image Search

Used to investigate the vacation photograph.

The process involved:

1. Uploading the image.
2. Checking visual matches.
3. Comparing candidate locations.
4. Looking for the original image/source.
5. Checking metadata.

## EXIF / Metadata

I checked the available image for:

```text
GPS Latitude
GPS Longitude
GPS Position
Location
City
Country
Date/Time
```

No useful GPS/location metadata was present in the copy I examined.

---

# Investigation Methodology

The overall workflow was:

```text
Known Username
      ↓
Social Media Accounts
      ↓
Profile Information
      ↓
Fiancée
      ↓
Images / Personal Information
      ↓
Reddit
      ↓
Archived Reddit Post
      ↓
Coworker
      ↓
Coworker's Reddit Account
      ↓
Historical Posts
      ↓
External Paste
      ↓
Password
      ↓
Email Conversation
      ↓
Mistress + Email Address
```

This demonstrated that OSINT investigations are often about **connecting small pieces of information** rather than finding everything in one place.

---

# Key Lessons Learned

### 1. Usernames are powerful pivots

A username such as `tstraussman` can lead to multiple platforms and provide the starting point for an investigation.

### 2. Social profiles contain many different types of intelligence

Useful information can exist in:

- Bios
- Profile/header images
- Posts
- Replies
- Followers
- Dates
- Photos
- External links

### 3. Deleted information may still exist

The Wayback Machine showed that information removed from a current page may still exist in an older archived snapshot.

### 4. Pivoting is a core OSINT skill

Finding Hans was not the end of the investigation. His username became the starting point for another investigation:

```text
Hans
 ↓
minikhans
 ↓
Reddit profile
 ↓
Historical posts
 ↓
External links
 ↓
More information
```

### 5. URLs can contain intelligence

The Ghostbin URL directly exposed the paste ID:

```text
/paste/ww4ju
```

### 6. Historical external pages are valuable

The investigation continued beyond Reddit. Archived Pastebin/Ghostbin content provided the final information about Thomas.

### 7. Reverse-image results must be verified

A visual-search engine can return similar locations rather than the exact source. Images should be verified using multiple clues whenever possible.

---

# What I Learned

This room gave me practical experience with **social-media OSINT and digital investigation methodology**.

The biggest lesson for me was that OSINT is not simply searching for a name and reading the first result.

A structured investigation involves:

```text
Collect
   ↓
Verify
   ↓
Pivot
   ↓
Archive
   ↓
Correlate
   ↓
Verify again
```

Small clues such as a username, comment, image, or external link can connect together and reveal much more information.

I also learned how useful historical web archives can be when information has been deleted or changed.

---
