# Phishing Analysis Fundamentals --- TryHackMe


**Platform:** TryHackMe\
**Room:** Phishing Analysis Fundamentals\
**Date:** 13 September 2026\

------------------------------------------------------------------------

## About This Room

I started the **Phishing Analysis Fundamentals** room to understand how
phishing emails are structured, delivered, and analyzed from a
defensive/SOC perspective.

The main goal is not just to recognize a suspicious email visually. I
want to understand what is happening underneath the email --- especially
the headers, raw message source, HTML body, attachments, and common
phishing techniques.

This README contains my notes from the parts I completed so far. I have
also added how I got the answers to the questions so I can come back
later and understand the reasoning instead of only memorizing the
answers.

------------------------------------------------------------------------

# Task 1 --- Introduction

Phishing and spam are common social-engineering threats.

Spam is generally unsolicited bulk email, while phishing is more
dangerous because it tries to make the victim perform an action that
benefits the attacker.

A phishing email may try to make a user:

-   Enter their username and password
-   Click a malicious link
-   Open a malicious attachment
-   Transfer money
-   Share sensitive information
-   Install malware

From a SOC/defender perspective, the job is to examine the email and
decide whether it is **malicious or legitimate**, while also collecting
useful indicators for further investigation.

### My main takeaway

A phishing email can sometimes be the first step in an attack. If one
employee interacts with a malicious email, an attacker may get an
initial foothold in the organization.

------------------------------------------------------------------------

# Task 2 --- The Email Address

Before analyzing phishing emails, I need to understand the basic
structure of an email address.

An email address is made up of three important parts:

``` text
username@domain
```

For example:

``` text
david@tryhackme.com
```

### 1. Username

The username identifies the mailbox or recipient.

### 2. `@` Symbol

The `@` symbol separates the username from the domain.

### 3. Domain

The domain identifies the destination/mail system responsible for
receiving the email.

### Easy way I remember it

I think of an email address like a physical mailing address:

-   **Domain** → the building/location
-   **Username** → the specific person/mailbox inside that location

### Why this matters for phishing

Attackers can create addresses that look similar to legitimate
addresses.

So when investigating an email, I should not only look at the display
name. I should inspect the **actual email address and domain**.

------------------------------------------------------------------------

# Task 3 --- Email Delivery

Different protocols are involved in sending and receiving email.

## SMTP

**SMTP = Simple Mail Transfer Protocol**

SMTP is responsible for **sending email**.

``` text
Email Client
     |
     | SMTP
     v
Sender Mail Server
```

------------------------------------------------------------------------

## POP3

**POP3 = Post Office Protocol 3**

POP3 is used for retrieving email.

According to the room:

-   Emails are downloaded and stored on a single device
-   Sent messages are stored on the single device from which the email
    was sent
-   Emails are accessed from the device to which they were downloaded
-   Emails are typically removed from the server after download

------------------------------------------------------------------------

## IMAP

**IMAP = Internet Message Access Protocol**

IMAP is used for receiving/retrieving email while keeping messages
synchronized through the mail server.

According to the room:

-   Emails remain stored on the server
-   Emails can be accessed from multiple devices
-   Sent messages are stored on the server
-   Messages are synchronized across multiple devices
-   Emails remain on the server unless explicitly deleted

------------------------------------------------------------------------

## Email Journey

``` text
Sender
  |
  | SMTP
  v
Sender Mail Server
  |
  | DNS lookup
  v
Recipient Mail Server
  |
  | Mail delivered
  v
Recipient Mailbox
  |
  | POP3 / IMAP
  v
Recipient Device
```

### Step-by-step

1.  The sender sends an email using their email client.
2.  The sender's mail server uses DNS to find the recipient domain's
    mail server.
3.  DNS provides the required mail-server information.
4.  The email is transferred to the recipient's mail server.
5.  The recipient's email client connects to the mailbox.
6.  The email is retrieved using POP3 or synchronized using IMAP.

------------------------------------------------------------------------

## Questions and How I Got the Answers

### Question 1

**Which protocol is responsible for sending an email from a client to a
mail server?**

**Answer: `SMTP`**

### How I Got It

SMTP stands for **Simple Mail Transfer Protocol** and the room
identifies it as the protocol responsible for sending email.

``` text
Client -> Mail Server = SMTP
```

------------------------------------------------------------------------

### Question 2

**Which service is used to look up the recipient domain's mail server?**

**Answer: `DNS`**

### How I Got It

The sending mail server needs to find the recipient's mail server. The
room explains that it queries **DNS** for this information.

``` text
Find recipient mail server = DNS
```

------------------------------------------------------------------------

### Question 3

**Bob wants to access his email from multiple devices, including his
phone and laptop. Which protocol should he use?**

**Answer: `IMAP`**

### How I Got It

IMAP keeps email on the server and synchronizes messages across devices.

``` text
Multiple devices + synchronization = IMAP
```

------------------------------------------------------------------------

# Task 4 --- Email Headers

An email has two major parts:

1.  **Email Header**
2.  **Email Body**

The header contains metadata about the email, while the body contains
the actual message.

## Important Email Header Fields

### From

Shows the sender's email address.

``` text
From: <sender@example.com>
```

When investigating phishing, I should check whether the sender address
actually belongs to the organization it claims to represent.

### To

Shows the intended recipient.

``` text
To: <recipient@example.com>
```

### Reply-To

Specifies the address where replies should be sent.

This is useful during phishing analysis because the visible sender and
the reply destination can potentially be different.

### Subject

Contains the email subject.

The subject can provide an initial clue about the purpose of the email.
Phishing messages may use urgent wording, account warnings, payment
requests, or fake security alerts.

### Date

Shows when the email was sent. This can be useful when building an
investigation timeline.

------------------------------------------------------------------------

## Viewing the Raw Message Source

A normal email client does not always show everything contained in an
email.

The **Message Source** shows the raw email data, including:

-   Header fields
-   Email body
-   Technical information
-   HTML content
-   Attachment information

In the TryHackMe VM, the room instructs me to open:

``` text
email1.eml
```

inside the **Email Samples** folder using Thunderbird.

Then:

``` text
View -> Message Source
```

or:

``` text
Ctrl + U
```

### Why this matters

The normal inbox view is designed mainly for users. The raw message
source is much more useful for an analyst because it exposes technical
details that may not be visible in the rendered email.

------------------------------------------------------------------------

# Task 5 --- Email Body

The email body contains the actual message.

Emails can be:

-   Plain text
-   HTML formatted

HTML email can contain:

-   Images
-   Links
-   Formatting
-   Embedded elements

This matters during phishing analysis because the visible content may
not tell me where a link actually goes.

------------------------------------------------------------------------

## Viewing HTML Source

Instead of only looking at the rendered email, I can inspect the
underlying HTML source.

This can reveal:

-   Actual hyperlinks
-   HTML elements
-   Embedded content
-   Image references
-   Suspicious destinations
-   Content hidden from the normal view

A phishing email may display something legitimate while the underlying
HTML points somewhere completely different.

### Important mindset

I should never trust only what the email visually shows me.

``` text
Visible text:
"Verify your account"

Actual destination:
hxxp[://]suspicious[.]example/...
```

The visible text and actual destination can be different.

------------------------------------------------------------------------

# Reconstructing Email Attachments

Attachments are also stored inside the email.

When looking at the raw message source, I can identify headers related
to an attachment.

## Content-Type

This tells me the type of content.

Example from the room:

``` text
Content-Type: application/pdf
```

This indicates that the attachment is a PDF.

## Content-Disposition

This indicates that the content is an attachment and can include the
filename.

``` text
Content-Disposition: attachment; filename="document.pdf"
```

## Content-Transfer-Encoding

This tells me how the attachment data is encoded for transmission.

The room demonstrates:

``` text
Content-Transfer-Encoding: base64
```

The Base64 data that follows represents the encoded file content.

------------------------------------------------------------------------

## Reconstructing the Attachment

``` text
Email Source
     |
     v
Find attachment headers
     |
     v
Identify Base64 data
     |
     v
Decode Base64
     |
     v
Recover original attachment
```

The room mentions using CyberChef or a Base64-to-PDF converter to decode
the data.

For safe analysis, I should work with a copy of the attachment and avoid
opening suspicious files directly on my normal system.

------------------------------------------------------------------------

# Task 6 --- Types of Phishing

The room discusses several forms of malicious or unwanted messaging.

## Spam

Spam is unsolicited bulk email sent to many recipients.

A more malicious version is often called **malspam**.

## Phishing

Phishing impersonates a trusted entity to trick the recipient into
revealing sensitive information or performing an action.

Common goals include:

-   Stealing credentials
-   Delivering malware
-   Stealing financial information
-   Gaining unauthorized access

## Spear Phishing

Spear phishing is a **targeted** form of phishing.

The attacker targets a particular person or organization and may
personalize the message.

## Whaling

Whaling is a type of spear phishing aimed at high-level targets such as
executives.

The goal may involve stealing sensitive information or gaining financial
access.

## Smishing

Smishing is phishing conducted through **SMS/text messages**.

``` text
SMS + Phishing = Smishing
```

## Vishing

Vishing is phishing conducted through **voice calls**.

``` text
Voice + Phishing = Vishing
```

------------------------------------------------------------------------

# Anatomy of a Phishing Email

Attackers often use similar techniques even when their final goals are
different.

## 1. Spoofed From Address

The sender may be made to look like a trusted organization.

For example, an attacker might register a lookalike domain. I should
inspect the actual domain rather than trusting the display name.

## 2. Urgent Subject or Message

Attackers may create pressure with messages such as:

``` text
Your account will be locked soon.
```

The goal is to make the victim act quickly instead of thinking
carefully.

## 3. Brand Impersonation

The email may copy:

-   Logos
-   Colors
-   Layout
-   Writing style

of a legitimate organization.

## 4. Grammar and Spelling Problems

Some phishing emails contain:

-   Spelling mistakes
-   Grammar mistakes
-   Strange wording
-   Unnatural sentences

However, this is not a reliable indicator by itself anymore because
modern AI can help attackers create polished messages.

## 5. Generic Content

A phishing email may use generic greetings such as:

``` text
Dear Customer
```

instead of using the recipient's actual name.

## 6. Hidden or Shortened Links

A link may look harmless but redirect to a different destination.

Example:

``` text
bit.ly/secure-login
```

The visible text does not automatically tell me where the link will
really lead.

## 7. Malicious Attachments

Attackers may disguise malicious files as legitimate documents.

Example:

``` text
invoice.pdf.exe
```

The final extension is important when determining what type of file it
actually is.

------------------------------------------------------------------------

# Safe Analysis --- Defanging

One of the most important practical habits I learned here is
**defanging**.

When documenting or sharing malicious indicators, I should make them
non-clickable.

### Original

``` text
http://www.suspiciousdomain.com
```

### Defanged

``` text
hxxp[://]www[.]suspiciousdomain[.]com
```

IP addresses can also be defanged:

``` text
192.0.2.10
```

becomes:

``` text
192[.]0[.]2[.]10
```

This reduces the chance of accidentally clicking or interacting with a
malicious resource.

------------------------------------------------------------------------

# My Phishing Analysis Workflow

Based on what I learned in the completed tasks, my basic workflow is:

``` text
1. Check sender address
        |
        v
2. Check domain
        |
        v
3. Check Subject / urgency
        |
        v
4. Inspect Reply-To
        |
        v
5. View raw message source
        |
        v
6. Inspect HTML and links
        |
        v
7. Inspect attachments
        |
        v
8. Extract useful indicators
        |
        v
9. Defang indicators
        |
        v
10. Decide whether the email is suspicious
```

I should avoid clicking suspicious links or opening unknown attachments
during analysis.

------------------------------------------------------------------------

# Quick Revision Notes

  -----------------------------------------------------------------------
  Topic                               What I Need to Remember
  ----------------------------------- -----------------------------------
  SMTP                                Sends email

  POP3                                Retrieves/downloads email

  IMAP                                Keeps email on server and
                                      synchronizes across devices

  DNS                                 Finds the recipient domain's mail
                                      server

  Header                              Email metadata

  Body                                Actual email content

  From                                Sender address

  To                                  Recipient

  Reply-To                            Address used for replies

  Subject                             Email subject

  Date                                Message date/time

  Message Source                      Raw email data

  HTML source                         Helps reveal actual links and
                                      embedded content

  Content-Type                        Identifies content/file type

  Content-Disposition                 Identifies attachment/disposition
                                      and can contain filename

  Base64                              Encoding used in the attachment
                                      example

  Spam                                Unsolicited bulk messages

  Phishing                            Deceptive message to trick a victim

  Spear Phishing                      Targeted phishing

  Whaling                             Phishing targeting executives

  Smishing                            SMS phishing

  Vishing                             Voice phishing

  Defanging                           Makes indicators harder to
                                      accidentally click
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# SOC Analyst Mindset

The biggest thing I took from this section is that **I should not trust
the appearance of an email**.

A professional analysis should look underneath the visible message.

Instead of only asking:

> "Does this email look real?"

I should ask:

``` text
Who actually sent it?
        ↓
What domain was used?
        ↓
Where does the link really go?
        ↓
What does the raw source contain?
        ↓
Is there an attachment?
        ↓
How is the attachment encoded?
        ↓
Are there suspicious indicators?
```

This is much closer to how I would approach a phishing alert as a SOC
analyst.

------------------------------------------------------------------------

# Sanitization Notes

For public documentation, I should avoid exposing unnecessary sensitive
information.

In this README:

-   Real personal email addresses are not included.
-   Credentials, passwords, tokens, and API keys are not included.
-   Suspicious URLs/domains are shown in defanged or example form where
    appropriate.
-   Lab-specific identifiers are avoided when they are not needed to
    explain the technique.
-   The focus is on the analysis methodology rather than exposing
    unnecessary infrastructure details.

> **Note:** Defanging reduces accidental interaction with an indicator;
> it is not a replacement for proper security controls.

------------------------------------------------------------------------

# Final Takeaway

The important concepts I want to remember are:

1.  Understand the structure of an email address.
2.  Know the difference between SMTP, POP3, IMAP, and DNS.
3.  Learn to inspect email headers.
4.  Use the raw message source when investigating suspicious emails.
5.  Inspect HTML instead of trusting only the rendered message.
6.  Understand how attachments are represented and encoded.
7.  Recognize common phishing techniques.
8.  Always defang suspicious indicators when documenting them.
9.  Never click suspicious links or open unknown attachments during
    analysis.

These basics will be useful later when I start doing more realistic
phishing investigations as part of SOC analysis.