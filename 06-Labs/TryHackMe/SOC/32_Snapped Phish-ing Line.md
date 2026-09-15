# TryHackMe - Snapped Phish-ing Line

**Date:** 15 September 2026\
**Room:** Snapped Phish-ing Line\
**Author:** Abhinav

------------------------------------------------------------------------

## Overview

In this room I investigated a phishing campaign targeting SwiftSpend
Financial.

I used:

-   Thunderbird
-   Browser/source inspection
-   Terminal
-   VirusTotal
-   CyberChef

The investigation went from the original phishing emails to the phishing
page, exposed phishing kit, captured credentials, and finally the hidden
flag.

------------------------------------------------------------------------

# Investigation

## 1. Who received the "Quote for Services Rendered" email?

**Answer:**

``` text
William McClean
```

### How I got it

I reviewed the emails in the `phish-emails` folder using Thunderbird and
checked the recipient of the email with the **Quote for Services
Rendered** subject.

------------------------------------------------------------------------

## 2. What email address did the attacker use?

**Answer:**

``` text
Accounts.Payable@groupmarketingonline.icu
```

### How I got it

I checked the **From** field/header of the phishing emails in
Thunderbird.

------------------------------------------------------------------------

## 3. Root domain of the redirection URL

**Answer:**

``` text
kennaroads.buzz
```

### How I got it

I opened Zoe Duncan's email and inspected its HTML attachment.

The attachment contained the phishing redirection URL. From that URL I
identified the root domain:

``` text
kennaroads.buzz
```

------------------------------------------------------------------------

## 4. Which company was impersonated?

**Answer:**

``` text
Microsoft
```

### How I got it

I opened the HTML attachment in the lab browser. It displayed a fake
login page designed to impersonate Microsoft.

------------------------------------------------------------------------

## 5. Name of the exposed archive

**Answer:**

``` text
Update365.zip
```

### How I got it

I visited the exposed:

``` text
/data
```

directory on the phishing website and found the ZIP archive.

------------------------------------------------------------------------

## 6. SHA256 hash of the phishing kit

**Answer:**

``` text
ba3c15267393419eb08c7b2652b8b6b39b406ef300ae8a18fee4d16b19ac9686
```

### How I got it

I downloaded the ZIP and calculated its SHA256 in the terminal:

``` bash
sha256sum Update365.zip
```

I then used the hash for VirusTotal analysis.

------------------------------------------------------------------------

## 7. Other threat category assigned to the ZIP

**Answer:**

``` text
Trojan
```

### How I got it

I searched the SHA256 hash in VirusTotal and checked the file's
detection/category information.

Apart from **phishing**, the ZIP was also associated with the **Trojan**
category.

------------------------------------------------------------------------

## 8. How many files were inside the archive?

**Answer: `49`**

### How I got it

I opened the VirusTotal **Details** page for the ZIP and checked the
archive contents. It contained **49 files**.

------------------------------------------------------------------------

## 9. User who submitted credentials more than once

**Answer:**

``` text
michael.ascot@swiftspend.finance
```

### How I got it

I visited:

``` text
/data/Update365/
```

and opened:

``` text
log.txt
```

I checked the entries and found that this user had submitted credentials
more than once.

------------------------------------------------------------------------

## 10. Email used by the attacker to collect credentials

**Answer:**

``` text
m3npat@yandex.com
```

### How I got it

I extracted the phishing kit and located the `submit.php` file.

The script contained the email address used to collect the submitted
credentials.

------------------------------------------------------------------------

## 11. Hidden flag

**Answer:**

``` text
THM{pL4y_w1Th_tH3_URL}
```

### How I got it

I returned to the phishing website and checked:

``` text
/data/Update365/office365/flag.txt
```

The file contained an encoded value.

I copied it into CyberChef and used Base64 decoding followed by
reversing the result.

The final value was:

``` text
THM{pL4y_w1Th_tH3_URL}
```

------------------------------------------------------------------------

# Quick Investigation Flow

``` text
Phishing Emails
      |
      v
Thunderbird / Headers
      |
      v
HTML Attachment
      |
      v
Phishing URL -> Fake Microsoft Login
      |
      v
/data -> Update365.zip
      |
      v
sha256sum
      |
      v
VirusTotal -> Trojan / 49 files
      |
      v
/data/Update365/log.txt
      |
      v
Repeated Credentials
      |
      v
Extract ZIP -> submit.php
      |
      v
Credential Collection Email
      |
      v
flag.txt
      |
      v
CyberChef
      |
      v
Final Flag
```

------------------------------------------------------------------------

# Tools Used

  Tool          Purpose
  ------------- -------------------------------------
  Thunderbird   Email and header analysis
  Browser       Inspect phishing/login page
  Terminal      Calculate SHA256
  VirusTotal    Hash, category and archive analysis
  CyberChef     Decode/reverse the flag

------------------------------------------------------------------------

# Final Answers

  --------------------------------------------------------------------------------------------------------
  \#                                  Answer
  ----------------------------------- --------------------------------------------------------------------
  1                                   `William McClean`

  2                                   `Accounts.Payable@groupmarketingonline.icu`

  3                                   `kennaroads.buzz`

  4                                   `Microsoft`

  5                                   `Update365.zip`

  6                                   `ba3c15267393419eb08c7b2652b8b6b39b406ef300ae8a18fee4d16b19ac9686`

  7                                   `Trojan`

  8                                   `49`

  9                                   `michael.ascot@swiftspend.finance`

  10                                  `m3npat@yandex.com`

  11                                  `THM{pL4y_w1Th_tH3_URL}`
  --------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# My Takeaway

This room helped me practice a complete phishing investigation: starting
with email analysis, following the phishing URL, finding an exposed
phishing kit, checking the kit's hash in VirusTotal, investigating
captured credentials, and finally finding and decoding the hidden flag.

The main workflow I took from this room is:

**Email → URL → Phishing Page → Phishing Kit → Hash → Credentials →
IOC/Flag**

## Sanitization

For public documentation, sensitive credentials, tokens, and unnecessary
infrastructure details should be removed or masked. The investigation
steps and learning-relevant indicators are retained.
