# TryHackMe - The Greenholt Phish

**Date:** 15 September 2026\
**Room:** The Greenholt Phish\
**Author:** Abhinav

------------------------------------------------------------------------

## Overview

In this room I investigated a suspicious email reported by a Greenholt
PLC employee.

The investigation followed a simple SOC phishing-analysis workflow:

``` text
Email -> Headers -> Source IP -> DNS Authentication -> Attachment -> Hash -> VirusTotal
```

I mainly used **Thunderbird**, **WHOIS**, **HostedScan**, the
**terminal**, and **VirusTotal**.

------------------------------------------------------------------------

# Investigation

## 1. Transfer Reference Number

**Answer:**

``` text
09674321
```

### How I got it

I opened the email in Thunderbird and checked the **Subject** line.

The transfer reference number was included directly in the subject.

------------------------------------------------------------------------

## 2. Display Name of Sender

**Answer:**

``` text
Mr. James Jackson
```

### How I got it

I checked the **From** field in Thunderbird.

------------------------------------------------------------------------

## 3. Sender Email Address

**Answer:**

``` text
info@mutawamarine.com
```

### How I got it

I continued inspecting the email headers and checked the address
associated with the sender.

------------------------------------------------------------------------

## 4. Reply-To Address

**Answer:**

``` text
info.mutawamarine@mail.com
```

### How I got it

I inspected the `Reply-To` header in the email source.

This is an important phishing indicator because the sender address and
reply address are different:

``` text
From:     info@mutawamarine.com
Reply-To: info.mutawamarine@mail.com
```

A reply would therefore go to the `mail.com` address instead of the
sender's `mutawamarine.com` address.

------------------------------------------------------------------------

## 5. Originating IP Address

**Answer:**

``` text
192.119.71.157
```

### How I got it

In Thunderbird I opened:

``` text
View -> Message Source
```

I then inspected the `Received` headers and traced the mail path until I
found the originating IP.

------------------------------------------------------------------------

## 6. Owner of the Originating IP

**Answer:**

``` text
HostPapa
```

### How I got it

I copied the originating IP:

``` text
192.119.71.157
```

and searched it using a WHOIS/IP lookup service.

The current WHOIS/network information associates the range with
**HostPapa**, while the hostname/network information also references
Hostwinds infrastructure. For the current room result, I recorded
**HostPapa**.

------------------------------------------------------------------------

## 7. SPF Record

**Answer:**

``` text
v=spf1 include:spf.protection.outlook.com -all
```

### How I got it

First I identified the Return-Path domain from the email headers:

``` text
mutawamarine.com
```

I then entered the domain into **HostedScan** and checked its SPF
information.

The complete SPF record was:

``` text
v=spf1 include:spf.protection.outlook.com -all
```

### What it means

-   `v=spf1` - SPF version.
-   `include:spf.protection.outlook.com` - authorizes Microsoft's mail
    infrastructure.
-   `-all` - unauthorized senders should fail SPF.

This is important because the originating IP was not authorized by this
SPF record.

------------------------------------------------------------------------

## 8. DMARC Record

**Answer:**

``` text
v=DMARC1; p=quarantine; fo=1
```

### How I got it

I used the same Return-Path domain:

``` text
mutawamarine.com
```

and performed a DMARC lookup using HostedScan.

The complete record was:

``` text
v=DMARC1; p=quarantine; fo=1
```

### What it means

-   `v=DMARC1` - DMARC version.
-   `p=quarantine` - messages failing DMARC should be treated as
    suspicious/quarantined.
-   `fo=1` - enables failure reporting when relevant authentication
    checks fail.

------------------------------------------------------------------------

## 9. Attachment Filename

**Answer:**

``` text
SWT_#09674321____PDF__.CAB
```

### How I got it

I checked the attachment shown in the email in Thunderbird.

The filename is suspicious because it contains `PDF` in the name, but
the actual extension is `.CAB`.

------------------------------------------------------------------------

## 10. SHA256 Hash

**Answer:**

``` text
2e91c533615a9bb8929ac4bb76707b2444597ce063d84a4b33525e25074fff3f
```

### How I got it

I downloaded the attachment into the lab environment and used:

``` bash
sha256sum SWT_#09674321____PDF__.CAB
```

The command returned the SHA256 hash above.

I then used this hash for further investigation rather than
opening/executing the suspicious file.

------------------------------------------------------------------------

## 11. Attachment File Size

**Answer:**

``` text
400.26 KB
```

### How I got it

I copied the SHA256 hash into **VirusTotal** and checked the file's
details.

VirusTotal showed the file size as:

``` text
400.26 KB
```

Using the hash is useful because it lets me investigate the sample
without having to execute it.

------------------------------------------------------------------------

## 12. Actual File Type

**Answer:**

``` text
RAR
```

### How I got it

In VirusTotal's file details, the actual detected file type was shown as
**RAR**.

This is different from the misleading `.CAB` filename.

``` text
Filename: SWT_#09674321____PDF__.CAB
Actual type: RAR
```

This mismatch is a strong indicator that the attachment should be
treated as suspicious.

------------------------------------------------------------------------

# Key Phishing Indicators I Found

The investigation revealed several red flags:

1.  **Unexpected financial request**
2.  **Generic greeting**
3.  **Mismatched Reply-To address**
4.  **Originating IP not aligned with the sender's domain**
5.  **SPF authentication issue**
6.  **Suspicious attachment filename**
7.  **Misleading `.CAB` extension**
8.  **Actual file type was RAR**

The combination of these indicators makes the email highly suspicious
and consistent with a phishing/BEC attempt.

------------------------------------------------------------------------

# Tools I Used

  Tool                Purpose
  ------------------- -----------------------------------
  Thunderbird         Email and header/source analysis
  WHOIS / IP lookup   Identify IP ownership
  HostedScan          SPF and DMARC lookup
  `sha256sum`         Calculate attachment hash
  VirusTotal          Hash reputation and file metadata

------------------------------------------------------------------------

# Quick SOC Workflow

``` text
1. Open suspicious email safely
2. Check sender and subject
3. Compare From and Reply-To
4. View full message source
5. Identify originating IP
6. Check IP ownership/reputation
7. Identify Return-Path domain
8. Check SPF and DMARC
9. Extract attachment safely
10. Calculate SHA256
11. Search hash in VirusTotal
12. Compare filename with actual file type
13. Record IOCs and determine verdict
```

------------------------------------------------------------------------

# Final Answer Sheet

  --------------------------------------------------------------------------------------------------------
  Question                            Answer
  ----------------------------------- --------------------------------------------------------------------
  Transfer Reference Number           `09674321`

  Sender display name                 `Mr. James Jackson`

  Sender email                        `info@mutawamarine.com`

  Reply-To                            `info.mutawamarine@mail.com`

  Originating IP                      `192.119.71.157`

  IP owner                            `HostPapa`

  SPF                                 `v=spf1 include:spf.protection.outlook.com -all`

  DMARC                               `v=DMARC1; p=quarantine; fo=1`

  Attachment                          `SWT_#09674321____PDF__.CAB`

  SHA256                              `2e91c533615a9bb8929ac4bb76707b2444597ce063d84a4b33525e25074fff3f`

  File size                           `400.26 KB`

  Actual file type                    `RAR`
  --------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# My Takeaway

This was a good example of how a SOC analyst should not trust an email
just because the sender appears familiar.

The biggest things I learned were to **inspect the raw headers, compare
the From and Reply-To addresses, trace the originating IP, check
SPF/DMARC, hash suspicious attachments, and verify the real file type**.

I also learned that a misleading filename can hide what the file
actually is, so the extension shown by the email should never be treated
as proof of the file's true format.

## Sanitization

For public documentation, I would avoid exposing unnecessary personal
information, credentials, tokens, or internal lab details. The technical
investigation steps and relevant IOCs are retained because they
demonstrate the analysis process.
