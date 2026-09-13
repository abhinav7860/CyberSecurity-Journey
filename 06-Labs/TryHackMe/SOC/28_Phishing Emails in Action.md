# Phishing Emails in Action --- TryHackMe

**Platform:** TryHackMe\
**Room:** Phishing Emails in Action\
**Date:** 13 September 2026\

------------------------------------------------------------------------

## About This Room

I worked through **Phishing Emails in Action** to practice identifying
phishing techniques from realistic email samples.

This room is more practical than just learning definitions. I looked at
sender addresses, display names, subjects, recipient fields, links,
redirects, HTML, tracking pixels, attachments, fake login pages,
suspicious file types, brand impersonation, and social-engineering
techniques.

I documented both **what made each sample suspicious** and **how I
identified it**, so I can revisit the investigation later.

------------------------------------------------------------------------

# Task 2 --- Cancel Your Order

This sample is designed to look like an official PayPal transaction
receipt.

### Phishing techniques

-   Spoofed email address
-   URL shortening
-   Branded HTML

## First observations

### Subject

The subject uses a fake transaction to create urgency.

``` text
Fake transaction
      ↓
Victim becomes worried
      ↓
Victim reacts quickly
      ↓
Victim clicks "Cancel"
```

### From address

The displayed sender is shown as:

``` text
service@paypal.com
```

but the actual sender in the sample is:

``` text
gibberish@sultanbogor.com
```

For public documentation, suspicious real-world indicators should be
defanged or masked.

### How I identified it

I compared the claimed identity with the actual sender domain:

``` text
Claimed identity  -> PayPal
Actual domain     -> Different domain
```

That mismatch is a strong phishing indicator.

### To address

The recipient address also looks unusual and does not match the expected
Yahoo-style address described by the room.

------------------------------------------------------------------------

## Email Body

The body imitates a PayPal receipt for a gift-card purchase and contains
a:

``` text
Cancel the order
```

button.

There are no attachments. The main interactive element is the button.

The attack flow is:

``` text
Fake PayPal receipt
        ↓
Fake purchase
        ↓
Victim gets worried
        ↓
"Cancel the order"
        ↓
Malicious redirect
```

## Button investigation

The important part is the link behind the button.

The raw email source reveals that the button points to a **shortened
URL**.

A shortened URL hides the final destination, so I should not trust it
just because the button looks legitimate.

### Safe investigation

The room recommends using a redirect-analysis service such as
**WhereGoes** to inspect shortened URLs without directly visiting the
destination.

**Rule:** Never click a suspicious link just to find out where it goes.

------------------------------------------------------------------------

# Task 3 --- Track Your Package

This sample pretends to be a shipping notification.

### Phishing techniques

-   Spoofed email address
-   Pixel tracking
-   Link manipulation

## First observations

### Subject

A fake tracking number is used to create curiosity and urgency.

``` text
Fake tracking number
        ↓
"What is my package?"
        ↓
Victim clicks
```

### From address

The display name is:

``` text
Distribution Center
```

while the actual sender shown in the sample is:

``` text
contact@beginpro.club
```

The display name and actual sender do not match.

### How I identified it

I compared:

``` text
Display name  -> Distribution Center
Actual sender -> Different domain
```

### Hyperlink

The hyperlink matches the tracking number in the subject, but that does
not prove it is safe.

The important question is:

``` text
Where does the hyperlink actually go?
```

------------------------------------------------------------------------

## Tracking Pixel

The room shows an image file named:

``` text
Tracking.png
```

The email contains a **tracking pixel**, which is a very small or
invisible remote image.

When an email client loads it, information can be sent back to the
sender's server. This can indicate that the message was opened and may
provide other tracking information depending on the implementation.

### Why Yahoo blocked the images

Yahoo blocked the images from automatically loading. Many email
providers do this because remote images can be used for tracking and can
expose information about the recipient.

### Lesson

Blocking remote images can reduce email tracking and improve privacy.

------------------------------------------------------------------------

# Task 4 --- Download Document Here

This sample demonstrates a multi-stage phishing campaign designed to
harvest credentials.

### Phishing techniques

-   Artificial urgency
-   Brand impersonation
-   Link redirection
-   Credential harvesting

## First observations

### Send date

The sample was sent on:

``` text
Thursday, July 15th, 2021
```

### Expiration date

The document link expires on the same day, creating artificial urgency.

``` text
Link expires today
       ↓
Victim feels pressure
       ↓
Victim skips verification
       ↓
Victim clicks
```

### Download button

The email contains:

``` text
Download Document Here
```

This starts the attack chain.

------------------------------------------------------------------------

## Redirection chain

The general flow is:

``` text
Phishing Email
      |
      v
Fake document-sharing page
      |
      v
Fake branded page
      |
      v
Fake login portal
      |
      v
Credential harvesting
```

The first landing page imitates a legitimate OneDrive share.

Buttons on that page lead to another page impersonating Adobe. The
suspicious URL and nonsensical instructions are additional red flags.

The final page asks the victim to sign in using their email provider.

------------------------------------------------------------------------

## Credential harvesting

In the sample, the victim attempts to log in using Outlook.

The important point is that the page is not actually authenticating the
user with the real mail service. It is a fake front intended to send
credentials to the attacker.

A generic error can then be displayed so the victim thinks the login
simply failed.

### How I identified the attack

``` text
Urgency
   +
Trusted-brand impersonation
   +
Multiple redirects
   +
Suspicious URLs
   +
Fake login page
   =
Credential phishing
```

### Important lesson about grammar

The sample contains formatting and grammar problems, but I should not
rely on grammar alone. Attackers can use AI to create polished phishing
emails.

Technical indicators and behavior are more reliable.

------------------------------------------------------------------------

# Task 5 --- Your Account Is on Hold

This sample pretends to be a Netflix billing notification.

The main malicious element is an attachment.

### Phishing techniques

-   Spoofed email address
-   Sense of urgency
-   Brand impersonation
-   Poor grammar/typos
-   Malicious attachment

## First observations

### Subject

The message says the account has been suspended and the victim must act
quickly.

This creates fear and urgency.

### From address

The display name is:

``` text
Netllx billing
```

The misspelling is suspicious, and the displayed sender does not match
the expected sender/domain.

### How I identified it

I checked:

``` text
Display name
Actual sender address
Domain
```

The inconsistencies are red flags.

### Brand impersonation

The HTML is designed to look like Netflix billing.

Attackers can copy logos, colors, layouts, and wording. Visual
appearance alone is not proof of legitimacy.

------------------------------------------------------------------------

## Attachment analysis

The victim is told to open a PDF to update billing information.

The PDF contains an embedded link titled:

``` text
Update Payment Account
```

The destination is not associated with a legitimate Netflix domain.

### Other red flags

The room also highlights:

-   An atypical phone-number format
-   Use of a legitimate Netflix help-center domain to create false trust

A legitimate domain appearing somewhere in an email does not make the
entire email legitimate.

### Attack flow

``` text
Fake billing warning
        ↓
Victim opens PDF
        ↓
"Update Payment Account"
        ↓
Embedded link
        ↓
Non-legitimate destination
        ↓
Potential credential/payment theft
```

The room notes that this sample is investigated further in the next
room, **Phishing Analysis Tools**.

------------------------------------------------------------------------

# Task 6 --- Your Recent Purchase

This sample pretends to be an Apple Support billing notification.

The email body is completely blank and the main malicious content is in
the attachment.

### Phishing techniques

-   Spoofed email address
-   BCC recipient
-   Urgency
-   Poor grammar/typos
-   Suspicious attachment

## First observations

### Subject

The victim is told there is an unauthorized purchase and must act
quickly.

This creates a false sense of urgency.

### From address

The display name is:

``` text
Apple Support
```

but the sender address does not match the claimed identity.

The sample also contains spelling problems in the From and To addresses.

### How I identified it

I compared:

``` text
Display name
+
Actual sender address
+
Domain
```

The inconsistencies indicate that the email should be treated as
suspicious.

------------------------------------------------------------------------

## BCC analysis

The victim is **BCCed** rather than directly listed as the recipient.

BCC means:

``` text
Blind Carbon Copy
```

BCC hides recipients from other recipients.

BCC alone does not prove that an email is malicious, but together with
the other indicators it contributes to the overall suspicion.

------------------------------------------------------------------------

## Attachment analysis

The email body is completely blank.

The main content is an attachment:

``` text
.dot
```

A `.dot` file is a Microsoft Word template format. The room considers
this unusual for a purchase receipt.

The document contains a large image. Interacting with it redirects the
user to a phishing site.

The URL contains familiar-looking terms such as:

``` text
apps
ios
```

However, the URL is excessively long and complex.

### Lesson

Familiar words inside a URL do not make the destination trustworthy.

I need to inspect the actual domain and full URL.

------------------------------------------------------------------------

# Task 7 --- Scheduled Shipment

This sample impersonates DHL and uses an Excel attachment to move the
attack to the next stage.

### Phishing techniques

-   Spoofed email address
-   Brand impersonation
-   Malicious attachment

## First observations

### Subject

The subject makes the message look like a normal DHL shipping
notification.

### From address

The display name is:

``` text
DHL Express
```

but the actual sender/domain does not match the claimed organization.

### Brand impersonation

The HTML body uses DHL-style branding to appear legitimate.

------------------------------------------------------------------------

## Attachment analysis

The important part of this phishing attempt is the:

``` text
.xlsx
```

attachment.

The document contains a clickable link.

There are several inconsistencies:

-   Sender uses a German domain
-   Invoice is addressed to a city in India
-   Document content contains Mandarin

These conflicting details are strong reasons to investigate the message.

### Geographic mismatch

A single geographic inconsistency does not automatically prove phishing,
but several unrelated locations and languages together are suspicious.

``` text
Sender domain
      +
Invoice location
      +
Document language
      =
Suspicious inconsistency
```

------------------------------------------------------------------------

# The Executable

The Excel document contains a link that attempts to download and
execute:

``` text
regasms.exe
```

The sample produced a system error when execution was attempted in the
provided environment.

Even though execution failed, the behavior is important because it shows
the intended attack chain:

``` text
Email
  ↓
Excel attachment
  ↓
Embedded link
  ↓
Executable payload
  ↓
Code execution
```

## Possible impact

If successfully executed, the attacker could potentially:

### Establish persistence

Create backdoors or scheduled tasks so access survives a reboot.

### Exfiltrate data

Steal sensitive files, credentials, browser-stored passwords, or other
information.

### Deploy ransomware

Encrypt files and demand payment for recovery.

------------------------------------------------------------------------

# Overall Phishing Investigation Workflow

After these samples, my basic workflow is:

``` text
Suspicious Email
      |
      v
Check Sender Address
      |
      v
Check Display Name
      |
      v
Check Subject
      |
      v
Look for Urgency / Fear
      |
      v
Inspect Recipient Fields
      |
      v
Inspect Raw Source
      |
      +-------------------+
      |                   |
      v                   v
    Links             Attachments
      |                   |
      v                   v
Inspect URL          Identify Type
/ Redirects               |
      |                   v
      |             Inspect Content
      |                   |
      +---------+---------+
                |
                v
        Collect Indicators
                |
                v
          Determine Intent
                |
                v
         Document Findings
```

------------------------------------------------------------------------

# Phishing Red Flags I Practiced

  -----------------------------------------------------------------------
  Red Flag                            What I Look For
  ----------------------------------- -----------------------------------
  Sender mismatch                     Display name and real address do
                                      not match

  Lookalike domain                    Domain resembles a trusted
                                      organization

  Urgency                             Account suspension, expiration,
                                      "act now"

  Fake transaction                    Unauthorized purchase/payment

  Brand impersonation                 Copied logos, colors, HTML

  Suspicious link                     Destination does not match visible
                                      text

  URL shortening                      Final destination is hidden

  Multiple redirects                  Several pages before final
                                      destination

  Tracking pixel                      Remote image used for tracking

  Fake login page                     Credentials requested by an
                                      untrusted page

  Suspicious attachment               Unexpected or unusual file

  Embedded link                       Document contains another URL

  Geographic mismatch                 Sender/document details do not make
                                      sense together

  Typos                               Spelling/grammar inconsistencies

  BCC                                 Hidden recipient list that is
                                      unusual in context

  Executable payload                  Document attempts to
                                      download/execute a program
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# My Key Lessons

## 1. Never trust the display name

Names such as:

``` text
Apple Support
DHL Express
Distribution Center
```

do not prove who actually sent the message.

I need to inspect the real sender address and domain.

## 2. Never trust a button because it looks legitimate

A button can have legitimate-looking text while pointing somewhere
completely different.

I should inspect the underlying HTML or URL before interacting with it.

## 3. Shortened URLs hide information

URL shortening can hide the final destination, so I should inspect the
redirect chain safely.

## 4. HTML can be used for impersonation

Attackers can reproduce the appearance of legitimate companies.

``` text
Looks legitimate != Is legitimate
```

## 5. Attachments can contain the real attack

The malicious element may be hidden inside a PDF, Word template, Excel
document, or another attachment.

## 6. Tracking pixels matter

A tiny remote image can be used to track email opens, which is one
reason email clients may block remote images.

## 7. Multiple redirects can hide the final destination

A phishing campaign may use several branded-looking pages before
reaching the actual credential-harvesting page.

## 8. Grammar is not enough

Typos can be useful clues, but polished grammar does not mean an email
is safe. Modern attackers can use AI to create convincing text.

------------------------------------------------------------------------

# Safe Analysis Rules

### Do

-   Inspect raw email source
-   Check sender and domain
-   Inspect Reply-To when present
-   Examine hyperlinks
-   Analyze redirect chains safely
-   Inspect attachment metadata
-   Use isolated lab environments
-   Defang indicators in documentation
-   Preserve useful evidence

### Do not

-   Click suspicious links on my normal machine
-   Enter real credentials into suspicious pages
-   Open unknown attachments outside an isolated environment
-   Upload sensitive company emails to random online services
-   Put live malicious URLs into public documentation without defanging
    them

------------------------------------------------------------------------

# Quick Revision

``` text
SMTP       -> Sends email
IMAP       -> Synchronizes email across devices
POP3       -> Downloads/retrieves email
DNS        -> Helps locate mail servers

From       -> Sender
To         -> Recipient
BCC        -> Hidden recipient list
Reply-To   -> Reply destination
Subject    -> Message subject

HTML       -> Can contain hidden/modified links
Attachment -> Can contain malicious content or links
Tracking pixel -> Can notify sender when email is opened

Phishing   -> Deceptive attempt to trick a victim
Smishing   -> SMS phishing
Vishing    -> Voice phishing
Whaling    -> Phishing targeting executives
```

------------------------------------------------------------------------

