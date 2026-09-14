# TryHackMe - Phishing Prevention

**Date:** 14 September 2026\
**Room:** Phishing Prevention\
**Author:** Abhinav

------------------------------------------------------------------------

## What I Learned

In this room I learned how organizations can prevent phishing using
email authentication standards, secure email controls, and user
awareness.

The main topics were:

-   SPF (Sender Policy Framework)
-   DKIM (DomainKeys Identified Mail)
-   DMARC (Domain-Based Message Authentication, Reporting, and
    Conformance)
-   S/MIME
-   SMTP traffic analysis
-   Internet Message Format (IMF)
-   Email filtering and Secure Email Gateways
-   Link rewriting
-   Sandboxing
-   User awareness and phishing reporting

I also used Wireshark to investigate SMTP responses and inspect email
messages and attachments inside a PCAP.

------------------------------------------------------------------------

# Task 2 - Sender Policy Framework (SPF)

## What is SPF?

SPF is an email authentication mechanism that uses a DNS TXT record to
specify which mail servers are authorized to send email on behalf of a
domain.

The basic workflow is:

1.  An email is sent claiming to be from a domain.
2.  The receiving mail server checks that domain's SPF record through
    DNS.
3.  It checks whether the sending server is authorized.
4.  The receiving server decides whether to accept, flag, or reject the
    message.

### SPF results from the room

  Result                Intended action
  --------------------- -----------------
  Pass, Neutral, None   Accept
  SoftFail, PermError   Flag
  Fail, TempError       Reject

## SPF Record Example

``` text
v=spf1 ip4:127.0.0.1 include:_spf.google.com -all
```

-   `v=spf1` - identifies the SPF version.
-   `ip4:127.0.0.1` - authorizes this IPv4 address.
-   `include:_spf.google.com` - allows the IPs authorized by that
    domain.
-   `-all` - unauthorized senders should fail SPF.

## Tools

I learned that SPF records can be inspected with tools such as
dmarcian's SPF Surveyor. Google's Messageheader tool can also analyze
full email headers and show authentication results such as SPF.

A **SoftFail** means the sender is not authorized according to the SPF
record, but the receiving server may still accept the email and flag it
as suspicious.

------------------------------------------------------------------------

# Task 3 - DomainKeys Identified Mail (DKIM)

## What is DKIM?

DKIM provides email authentication using a digital signature.

The sending mail server signs the email using a **private key**. The
receiving server retrieves the corresponding **public key** from DNS and
uses it to verify the signature.

``` text
Sending Server
      |
      | Sign with private key
      v
    Email
      |
      v
Receiving Server
      |
      | Get public key from DNS
      v
 Verify DKIM signature
```

If the signature matches, the message can be authenticated with respect
to DKIM. If verification fails, the message may be flagged or rejected
depending on policy.

## DKIM Record Example

``` text
v=DKIM1; k=rsa; p=<public_key>
```

-   `v=DKIM1` - DKIM version.
-   `k=rsa` - key type.
-   `p=` - public key used to verify the signature.

One useful point I learned is that DKIM can survive email forwarding
better than SPF because it is based on a digital signature.

A result such as:

``` text
dkim=permerror
```

indicates a permanent verification problem, such as an invalid
signature, missing key, or configuration problem.

------------------------------------------------------------------------

# Task 4 - DMARC

## What is DMARC?

DMARC builds on SPF and DKIM.

It uses **alignment** to connect the sender domain with the domains
authenticated by SPF and/or DKIM. If authentication or alignment fails,
DMARC applies the policy defined by the domain owner.

## DMARC Record Example

``` text
v=DMARC1; p=quarantine; rua=mailto:postmaster@website.com
```

-   `v=DMARC1` - DMARC version.
-   `p=quarantine` - failing messages should be quarantined.
-   `rua=` - destination for aggregate reports.

Common policies are:

``` text
p=none
p=quarantine
p=reject
```

I remember them as:

-   `none` - monitor/report.
-   `quarantine` - treat failures as suspicious.
-   `reject` - reject failing messages.

------------------------------------------------------------------------

# Task 5 - S/MIME

## What is S/MIME?

S/MIME is used for digitally signing and encrypting email using
public-key cryptography.

### Digital Signature

The sender signs with their **private key** and the recipient verifies
it using the sender's **public key**.

This provides:

-   **Authentication**
-   **Non-repudiation**
-   **Data integrity**

### Encryption

The sender encrypts the message using the **recipient's public key**.
The recipient decrypts it using their **private key**.

This provides:

-   **Confidentiality**

### Easy way I remember it

``` text
Signing    -> Proves the sender and helps detect modification
Encryption -> Keeps the message private
```

------------------------------------------------------------------------

# Task 6 - Analyzing SMTP Responses

For this task I analyzed the provided SMTP PCAP using Wireshark.

## 1. Wireshark filter for SMTP response codes

**Answer:**

``` text
smtp.response.code
```

### How I got it

This is the Wireshark field for SMTP response codes. Using it narrows
the capture to SMTP server responses.

## 2. Packets with `220 Service ready`

**Answer: `19`**

### How I got it

I filtered the SMTP responses and narrowed them to response code `220`.

``` text
smtp.response.code == 220
```

There were **19** matching packets.

## 3. Response code for the Spamhaus-blocked email

**Answer: `553`**

### How I got it

I inspected the SMTP response mentioning `spamhaus.org`. The server
returned code **553**.

## 4. Full response message

**Answer:**

``` text
Requested action not taken: mailbox name not allowed (553)
```

### How I got it

I opened the packet from the previous question and inspected the
complete SMTP response rather than only the numeric code.

## 5. Messages blocked with response code `552`

**Answer: `6`**

### How I got it

I searched for:

``` text
smtp.response.code == 552
```

The capture contained **6** matching messages.

------------------------------------------------------------------------

# Task 7 - Inspecting Emails and Attachments

This task moved from SMTP status codes to the actual email contents
using **Internet Message Format (IMF)**.

I used IMF information to inspect sender/recipient fields, email-client
information, content and attachments.

## 1. SMTP packets available

**Answer: `512`**

### How I got it

I counted the SMTP packets available in the provided capture. There were
**512**.

## 2. Attachment in packet `270`

**Answer:**

``` text
document.zip
```

### How I got it

I opened packet `270` and inspected the IMF/MIME information. The
attachment filename was `document.zip`.

## 3. Host IP that was not responding

**Answer:**

``` text
212.253.25.152
```

### How I got it

The message in packet `270` identified the host that was not responding,
making the message undeliverable.

## 4. Email client used for `attachment.scr`

**Answer:**

``` text
Microsoft Outlook Express 6.00.2600.0000
```

### How I got it

I filtered for IMF traffic and inspected the message metadata associated
with `attachment.scr`. The email client field showed Microsoft Outlook
Express 6.00.2600.0000.

## 5. Encoding used for the potentially malicious attachment

**Answer:**

``` text
base64
```

### How I got it

The MIME/IMF attachment information showed Base64 encoding.

Base64 is **encoding, not encryption**. It represents binary data as
text so it can be transported through email systems.

------------------------------------------------------------------------

# Task 8 - How Organizations Stop Phishing

After learning SPF, DKIM, DMARC and S/MIME, I learned about additional
controls organizations use to prevent phishing.

## Technical Defenses

### Email Filtering

Email filtering can use IP and domain reputation and other indicators to
block or quarantine suspicious messages.

### Secure Email Gateways (SEGs)

SEGs inspect email for:

-   Spoofing
-   Impersonation
-   Malicious attachments
-   Suspicious links
-   Reputation problems
-   Phishing indicators

### Link Rewriting

Link rewriting replaces suspicious or unknown URLs with
protected/redirected links. This gives security systems an opportunity
to inspect the destination when a user clicks it.

### Sandboxing

Sandboxing executes suspicious attachments or links in an isolated
environment so their behavior can be observed safely.

Things that can be monitored include:

-   Process creation
-   Network connections
-   File changes
-   Registry changes
-   Downloads
-   Other suspicious behavior

------------------------------------------------------------------------

# User-Facing Defenses

Technical controls are important, but users are still part of the
security boundary.

## Trust and Warning Indicators

Email platforms can show warnings such as:

-   External Sender
-   Suspicious Link
-   Untrusted Sender

These warnings encourage users to stop and inspect a message before
interacting with it.

## Phishing Reporting

Organizations should provide an easy way for users to report suspicious
emails so the SOC/security team can investigate and protect other users.

## User Awareness Training

Training should cover:

-   Urgent requests
-   Social engineering
-   Suspicious links
-   Unexpected attachments
-   Sender impersonation
-   Credential/payment requests

## Phishing Simulations

Controlled phishing simulations can test whether employees recognize
phishing and help improve security awareness.

------------------------------------------------------------------------

# My Phishing Defense Mental Model

The main thing I took from this room is that phishing defense is not
based on one tool. It works best as a layered approach.

``` text
Incoming Email
      |
      v
Email Filtering
      |
      v
SPF / DKIM / DMARC
      |
      v
Secure Email Gateway
      |
      v
URL / Attachment Inspection
      |
      v
User Mailbox
      |
      v
User Awareness + Reporting
      |
      v
SOC Investigation
```

If one layer misses a malicious email, another layer may still detect or
stop it.

------------------------------------------------------------------------

# SMTP Investigation Cheatsheet

## SMTP response codes

``` text
smtp.response.code
```

## Specific codes

``` text
smtp.response.code == 220
smtp.response.code == 552
smtp.response.code == 553
```

## IMF traffic

``` text
imf
```

## Investigation workflow

``` text
1. Filter the protocol
2. Identify interesting response codes
3. Open the relevant packet
4. Inspect the SMTP response
5. Follow the TCP stream if necessary
6. Inspect IMF headers
7. Identify sender/recipient/client
8. Inspect MIME/attachment information
9. Identify the encoding
10. Treat suspicious attachments and URLs carefully
```

------------------------------------------------------------------------

# Email Authentication Comparison

  -----------------------------------------------------------------------
  Technology              Main Purpose            Easy way to remember
  ----------------------- ----------------------- -----------------------
  SPF                     Sender authorization    Who is allowed to send?

  DKIM                    Authentication and      Was the message signed
                          integrity               correctly?

  DMARC                   Policy and alignment    What should happen when
                                                  authentication fails?

  S/MIME                  Signing and encryption  Prove identity and/or
                                                  keep content private
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Final Answers

## Task 6

  --------------------------------------------------------------------------------------------------
  Question                            Answer
  ----------------------------------- --------------------------------------------------------------
  Wireshark filter                    `smtp.response.code`

  `220 Service ready` packets         `19`

  Spamhaus response code              `553`

  Full response                       `Requested action not taken: mailbox name not allowed (553)`

  `552` blocked messages              `6`
  --------------------------------------------------------------------------------------------------

## Task 7

  Question                 Answer
  ------------------------ --------------------------------------------
  SMTP packets             `512`
  Packet 270 attachment    `document.zip`
  Host IP not responding   `212.253.25.152`
  Email client             `Microsoft Outlook Express 6.00.2600.0000`
  Attachment encoding      `base64`

------------------------------------------------------------------------

# What I Learned

This room connected the phishing-analysis skills I learned earlier with
the prevention side.

I now understand that:

-   SPF checks whether a sending server is authorized for a domain.
-   DKIM uses a digital signature to authenticate email.
-   DMARC uses SPF/DKIM alignment and a domain policy.
-   S/MIME can provide digital signatures and encryption.
-   SMTP response codes can reveal why email delivery failed.
-   Wireshark can inspect SMTP and IMF traffic.
-   IMF/MIME information can reveal email clients and attachments.
-   Base64 is encoding, not encryption.
-   Secure Email Gateways, filtering, link rewriting and sandboxing
    provide additional protection.
-   User awareness and phishing reporting remain important.

My biggest takeaway is that phishing defense works best as **defense in
depth**, combining email authentication, filtering, analysis, sandboxing
and user awareness.

------------------------------------------------------------------------
