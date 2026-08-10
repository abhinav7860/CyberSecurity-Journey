# TryHackMe — Sakura Room CTF Write-Up

## Room Overview

**Platform:** TryHackMe  
**Room:** Sakura  
**Category:** OSINT / CTF  
**Focus:** Open-Source Intelligence, GitHub Investigation, PGP, Cryptocurrency OSINT, Social Media OSINT, Wi-Fi Intelligence, and Geolocation

---

# Introduction

The **Sakura** room is an OSINT-focused CTF designed to test the ability to collect and connect information from different public sources.

The investigation covers:

- Username discovery
- Source-code inspection
- Search-engine reconnaissance
- GitHub investigation
- PGP key analysis
- Git commit-history analysis
- Cryptocurrency wallet investigation
- Social-media OSINT
- Wi-Fi SSID/BSSID investigation
- Reverse image searching
- Geolocation
- Airport and travel identification

> **Note:** This write-up documents the supplied Sakura room walkthrough and its answers.

---

# Task 1 — Introduction

Task 1 is an introduction to the room and does not require an investigation.

---

# Task 2 — TIP-OFF

## Objective

Find the attacker's username.

## Investigation

The room provides an SVG image:

```text
sakurapwnedletter.svg
```

Instead of only viewing the image, inspect the underlying SVG source.

SVG files are text-based, so useful information can sometimes be found inside the source that is not visible in the rendered image.

The investigation revealed an operating-system-style path containing:

```text
/home/XXXX
```

The username identified from this clue was:

```text
SakuraSnowAngelAiko
```

## Answer

```text
SakuraSnowAngelAiko
```

---

# Task 3 — RECONNAISSANCE

## Objective

Find:

1. The attacker's email address
2. The attacker's full real name

The username from Task 2 becomes the main OSINT pivot:

```text
SakuraSnowAngelAiko
```

## Step 1 — Search the Username

Searching the username reveals references to the attacker's online presence, including GitHub and LinkedIn.

This demonstrates a useful OSINT technique:

> A username can be used as a pivot across multiple online platforms.

## Step 2 — Investigate GitHub

The GitHub account identified in the source was:

```text
https://github.com/sakurasnowangelaiko
```

One interesting repository was:

```text
PGP
```

A PGP public key can contain identity information associated with the key.

## Step 3 — Inspect the PGP Key

The key was decoded and the relevant identity information was extracted.

The source identified:

```text
Name: Aiko Abe
Email: SakuraSnowAngel83@protonmail.com
```

## Answers

**Full Name**

```text
Aiko Abe
```

**Email**

```text
SakuraSnowAngel83@protonmail.com
```

---

# Task 4 — UNVEIL

## Objective

Find:

1. The attacker's cryptocurrency wallet address
2. Their choice of cryptocurrency
3. The payment pool that paid them on January 23, 2021

The task specifically warns that the GitHub account owner had been editing and deleting information.

This makes Git history important.

## Step 1 — Investigate the GitHub Repositories

The account contained repositories associated with projects such as:

```text
cpuminer
Mailpile
xmrig
ETH
```

The `ETH` repository was particularly interesting because of its connection to Ethereum.

## Step 2 — Check Commit History

Although information had been deleted from the current repository, Git commits can preserve previous versions.

The deleted content contained:

```text
stratum://0xa102397dbeeBeFD8cD2F73A89122fCdB53abB6ef.Aiko:pswd@eu1.ethermine.org:4444
```

The important wallet address was:

```text
0xa102397dbeeBeFD8cD2F73A89122fCdB53abB6ef
```

## Step 3 — Investigate the Wallet

The wallet was investigated using blockchain transaction information.

The source identified activity involving:

```text
Ethereum
Tether
```

The payment pool associated with the January 23, 2021 activity was:

```text
Ethermine
```

## Answers

**Wallet Address**

```text
0xa102397dbeeBeFD8cD2F73A89122fCdB53abB6ef
```

**Choice of Cryptocurrency**

```text
Ethereum
```

The source also identified some:

```text
Tether
```

**Payment Pool — January 23, 2021**

```text
Ethermine
```

---

# Task 5 — TAUNT

## Objective

Find:

1. The attacker's current Twitter handle
2. The URL where the attacker saved Wi-Fi SSIDs and passwords
3. The BSSID of the attacker's home Wi-Fi

## Step 1 — Identify the Twitter Account

The provided image contains clues that can be searched to identify the social-media account.

The Twitter handle identified was:

```text
SakuraLoverAiko
```

## Step 2 — Find the Wi-Fi Information

The investigation led to a paste-style `.onion` resource containing Wi-Fi information.

The information included:

- Wi-Fi names
- SSIDs
- Passwords

The source gives the following URL:

```text
depasteon6cqgrykzrgya52xglohg5ovyuyhte3ll7hzix7h5ldfqsyd.onion/show.php?md5=0a5c6e136a98a60b8a21643ce8c15a74
```

## Step 3 — Identify the BSSID

A **BSSID** identifies a Wi-Fi access point and is commonly represented as a MAC address.

The source used WiGLE to correlate the Wi-Fi clue.

One relevant SSID clue was:

```text
DK1F-G
```

The matching BSSID was:

```text
84:AF:EC:34:FC:F8
```

## Answers

**Current Twitter Handle**

```text
SakuraLoverAiko
```

**Wi-Fi Information URL**

```text
depasteon6cqgrykzrgya52xglohg5ovyuyhte3ll7hzix7h5ldfqsyd.onion/show.php?md5=0a5c6e136a98a60b8a21643ce8c15a74
```

**BSSID**

```text
84:AF:EC:34:FC:F8
```

---

# Task 6 — HOMEBOUND

## Objective

Find:

1. The location closest to the photograph posted before the flight
2. The last layover airport
3. The lake visible on the map
4. The attacker's home city

---

## Part 1 — Closest Airport

A Twitter post contains a photograph with a recognizable landmark.

The landmark was identified as the:

```text
Washington Monument
```

in Washington, D.C.

The airport identified as closest to the location was:

```text
Ronald Reagan Washington National Airport
```

Airport code:

```text
DCA
```

## Answer

```text
DCA
```

---

## Part 2 — Layover Airport

Another photograph showed a first-class airport lounge.

Reverse image searching was used to identify the location.

The image matched the:

```text
Japan Airlines Sakura Lounge
```

at:

```text
Haneda Airport
```

Airport code:

```text
HND
```

## Answer

```text
HND
```

---

## Part 3 — Lake on the Map

The map shown in the investigation was identified as being in Japan.

The lake was:

```text
Lake Inawashiro
```

## Answer

```text
Lake Inawashiro
```

---

## Part 4 — Home City

The Wi-Fi information discovered earlier contained an SSID:

```text
HIROSAKI_Free_Wi-Fi
```

This provided the clue for the attacker's home city.

The city identified was:

```text
Hirosaki
```

## Answer

```text
Hirosaki
```

---

# Complete Answer Sheet

| Task | Question | Answer |
|---|---|---|
| Task 2 | Attacker username | `SakuraSnowAngelAiko` |
| Task 3 | Full name | `Aiko Abe` |
| Task 3 | Email | `SakuraSnowAngel83@protonmail.com` |
| Task 4 | Cryptocurrency wallet | `0xa102397dbeeBeFD8cD2F73A89122fCdB53abB6ef` |
| Task 4 | Cryptocurrency | `Ethereum` |
| Task 4 | Additional cryptocurrency observed | `Tether` |
| Task 4 | Payment pool | `Ethermine` |
| Task 5 | Twitter handle | `SakuraLoverAiko` |
| Task 5 | BSSID | `84:AF:EC:34:FC:F8` |
| Task 6 | Closest airport | `DCA` |
| Task 6 | Layover airport | `HND` |
| Task 6 | Lake | `Lake Inawashiro` |
| Task 6 | Home city | `Hirosaki` |

---

# Tools and Techniques

## Browser Developer Tools

Useful when investigating web-based files such as SVGs.

```text
Open file
   ↓
Inspect source
   ↓
Find hidden/non-visible information
   ↓
Extract clue
```

In this room, inspecting the SVG source helped reveal the username.

---

## Search Engines

Search engines can be used to pivot from a username to other public identities.

Useful for:

- Username searches
- Finding social profiles
- Finding GitHub accounts
- Finding location clues
- Correlating information

---

## GitHub

Important GitHub investigation areas include:

```text
Repositories
Commits
Branches
Deleted files
Source code
Repository history
```

A key lesson from this room is:

> Deleted information may still be recoverable from Git history.

---

## PGP / GPG

PGP keys can contain identity information.

In this investigation, the PGP repository helped identify:

```text
Aiko Abe
SakuraSnowAngel83@protonmail.com
```

---

## Blockchain Investigation

Public blockchain data can be used to investigate cryptocurrency addresses.

The wallet investigation revealed activity involving:

```text
Ethereum
Tether
Ethermine
```

---

## Social Media OSINT

Social media posts can contain clues such as:

- Usernames
- Images
- Landmarks
- Travel information
- Locations
- Background details

The account identified in this room was:

```text
SakuraLoverAiko
```

---

## Wi-Fi Intelligence

Wireless information can contain:

```text
SSID
BSSID
Access-point information
Location clues
```

The BSSID identified in this room was:

```text
84:AF:EC:34:FC:F8
```

---

## WiGLE

WiGLE can be used to investigate publicly mapped wireless networks.

The source used it to correlate the Wi-Fi clue:

```text
DK1F-G
```

with the relevant BSSID.

---

## Reverse Image Search

Reverse image searching can help identify:

- Airports
- Buildings
- Landmarks
- Lounges
- Travel destinations
- Geographic locations

The airport lounge was identified as:

```text
Japan Airlines Sakura Lounge
Haneda Airport (HND)
```

---

# Investigation Chain

The entire investigation can be viewed as one OSINT chain:

```text
SVG Image
   ↓
Source Inspection
   ↓
Username
   ↓
Search Engine Pivot
   ↓
GitHub
   ↓
PGP Key
   ↓
Name + Email
   ↓
Git Commit History
   ↓
Cryptocurrency Wallet
   ↓
Blockchain Transactions
   ↓
Twitter
   ↓
Wi-Fi Information
   ↓
BSSID
   ↓
Geolocation
   ↓
Airport + Lake
   ↓
Home City
```

The important idea is that each clue becomes a pivot for the next investigation.

---

# Key Lessons Learned

## 1. Inspect the Source, Not Only the Image

Images can contain information that is not visible when simply viewing them.

SVG files are particularly useful to inspect because they are text-based.

---

## 2. Usernames Are Powerful OSINT Pivots

A single username can lead to multiple platforms.

```text
Username
   ↓
GitHub
Twitter
LinkedIn
Forums
Other platforms
```

---

## 3. Always Check Git History

If a task says information was deleted, don't only inspect the current repository.

Check:

```text
Commits
Branches
Previous versions
Deleted files
```

---

## 4. Public Keys Can Contain Identity Information

PGP is not only about encryption.

Public keys can contain identity information such as:

```text
Name
Email
Key information
```

---

## 5. Cryptocurrency Addresses Can Be Investigated

Public blockchains provide transaction information that can be used as an OSINT pivot.

A wallet address can lead to:

```text
Transactions
Dates
Assets
Related services
Payment pools
```

---

## 6. Social Media Images Can Reveal Locations

Images can contain useful geolocation clues:

```text
Landmarks
Buildings
Signs
Airports
Maps
Architecture
Geography
```

---

## 7. Wi-Fi Data Can Provide Location Clues

SSID and BSSID information can be combined with wireless databases and other OSINT sources to identify locations.

---

## 8. OSINT Is About Connecting Small Clues

The room demonstrates that one clue rarely gives the entire answer.

Instead:

```text
Username
   ↓
GitHub
   ↓
PGP
   ↓
Email
   ↓
Git history
   ↓
Wallet
   ↓
Social media
   ↓
Wi-Fi
   ↓
Geolocation
```

Each discovery becomes the starting point for the next step.

---

# Final Takeaway

The Sakura room demonstrates how an investigation can start with a very small clue and eventually build a much larger picture.

The room covered:

- Username discovery
- GitHub reconnaissance
- PGP investigation
- Git history analysis
- Cryptocurrency investigation
- Social media OSINT
- Wi-Fi intelligence
- Reverse image searching
- Geolocation
- Travel OSINT

The biggest lesson for me is that **OSINT is about connecting information from different sources**.

A username can lead to a GitHub account.

A GitHub account can lead to a PGP key.

A PGP key can lead to an email address.

Git history can reveal deleted information.

A wallet address can lead to blockchain transactions.

Social media can provide travel and location clues.

Wi-Fi information can provide another location pivot.

---
