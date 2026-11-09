# LetsDefend – Phishing Email Analysis

**Study date:** 9 November 2026  
**Topic:** Introduction to Phishing, Email Investigation, Static Analysis, and Dynamic Analysis  
**Platform:** LetsDefend

---

## 1. Introduction

In this study session, I learned how phishing works and how a SOC analyst can investigate suspicious emails. I focused on identifying suspicious senders, examining email headers, validating domains and sending infrastructure, inspecting URLs, and safely analysing suspicious files or websites.

A phishing investigation requires more than deciding whether an email looks suspicious. I need to combine multiple pieces of evidence, understand email authentication, and avoid treating one tool's result as a final verdict.

## 2. What Is Phishing?

Phishing is a form of social engineering in which an attacker tricks a person into performing an action that benefits the attacker. The attacker may try to make the recipient:

- Open a malicious attachment.
- Visit a fraudulent website.
- Enter account credentials.
- Share personal or financial information.
- Approve a fraudulent payment or change to payment details.
- Run a malicious file or enable harmful content.

Phishing commonly arrives through email, but similar techniques are also used through text messages, phone calls, social media, collaboration platforms, and other communication channels.

### 2.1 Phishing and the Cyber Kill Chain

Phishing is commonly associated with the **Delivery** stage of the Cyber Kill Chain. During this stage, an attacker attempts to deliver a malicious payload or link to a target.

A phishing email may be the initial delivery mechanism. If the recipient interacts with it, the attack may progress to exploitation, installation, command and control, and actions on objectives. Not every phishing email contains malware; some campaigns simply attempt to steal credentials or persuade a victim to perform a fraudulent action.

### 2.2 Spoofing

Email spoofing occurs when an attacker forges or manipulates sender-related information so that a message appears to come from another person or organisation.

The visible `From` field alone is not enough to establish that a message genuinely came from the displayed organisation. I should compare the sender with the message headers, authentication results, sending infrastructure, links, attachments, and the context of the message.

**Important:** A legitimate account can also be compromised and used to send phishing emails. Therefore, an email that passes authentication checks is not automatically safe.

## 3. Email Authentication: SPF, DKIM, and DMARC

These mechanisms help receiving mail systems assess whether a message is authorised and whether signed parts have been altered.

### 3.1 SPF – Sender Policy Framework

SPF is a DNS-based mechanism that allows a domain owner to publish which mail servers or IP addresses are authorised to send email for that domain.

During an SPF check, the receiving mail server evaluates whether the sending IP address is permitted by the SPF policy of the relevant envelope-sender domain.

**SPF helps answer:** Is this sending IP authorised to send mail for the domain being checked?

SPF does not prove that the message content is safe, and it does not by itself prove that the visible display name or `From` address is trustworthy.

### 3.2 DKIM – DomainKeys Identified Mail

DKIM adds a cryptographic signature to an email. The receiving system can use the public key published in the signing domain's DNS records to verify the signature.

DKIM helps verify that signed parts of the message have not been modified in transit and that the signing domain takes responsibility for the signature.

**DKIM helps answer:** Does the DKIM signature validate for the signing domain, and have the signed parts remained intact?

A valid DKIM signature does not prove that the sender or message is benign. A compromised account can still send a harmful message with a valid signature.

### 3.3 DMARC – Domain-based Message Authentication, Reporting, and Conformance

DMARC builds on SPF and DKIM. It allows a domain owner to publish a policy that tells receiving systems how to handle messages that fail DMARC evaluation. It also introduces alignment requirements between the visible `From` domain and the domains authenticated by SPF or DKIM.

Common DMARC policies include:

- `p=none` – request monitoring and reporting without asking receivers to quarantine or reject based on DMARC policy.
- `p=quarantine` – ask receivers to treat failing messages as suspicious, often by placing them in spam or quarantine.
- `p=reject` – ask receivers to reject messages that fail DMARC evaluation.

**DMARC helps answer:** Do SPF or DKIM authenticate in alignment with the visible `From` domain, and what policy has the domain owner published?

### 3.4 Comparing SPF, DKIM, and DMARC

| Mechanism | Main purpose | What it does not prove |
|---|---|---|
| SPF | Checks whether the sending IP is authorised by the relevant domain's SPF policy | That the message content is safe |
| DKIM | Verifies a cryptographic signature and integrity of signed message parts | That the sender or message is benign |
| DMARC | Applies alignment rules and a domain-published policy using SPF and/or DKIM | That every message passing DMARC is legitimate |

I should interpret these results together with the rest of the investigation. A failure can be suspicious, but it can also result from legitimate forwarding or configuration problems. A pass is useful evidence, not a guarantee of safety.

## 4. Email Traffic Analysis

Email traffic analysis helps an analyst understand who sent a suspicious message, who received it, when it was sent, and whether other users received similar messages. The aim is not only to investigate one email but also to determine whether it is part of a wider phishing campaign.

### 4.1 Details to Collect

- **Sender address:** The address displayed as the sender.
- **SMTP sending IP:** The IP address of the sending mail server or relevant external hop.
- **Sender domain:** The domain associated with the sender.
- **Subject:** The subject line, including suspicious urgency or payment-related wording.
- **Recipient addresses:** The users or mailboxes that received the message.
- **CC and BCC:** Other recipients, where available from the message data.
- **Date and time:** When the message was sent and received, including timezone considerations.
- **Message identifiers:** Such as Message-ID, which can help correlate copies of a message.
- **Links and attachments:** URLs, files, or embedded content.
- **Authentication results:** SPF, DKIM, and DMARC outcomes.

### 4.2 Determining Campaign Scope

If multiple users received similar messages, compare the subject, sender, sending IP, domain, URLs, attachment names, hashes, timestamps, and Message-ID patterns.

This can help answer:

1. How many users received the message?
2. Which users opened it or interacted with it, if telemetry is available?
3. Did any user click a link or open an attachment?
4. Are there related messages with slightly different subjects or sender addresses?
5. Are the same indicators present in other alerts or endpoint/network logs?

A single suspicious email may be one part of a larger campaign. Identifying the scope helps the SOC team decide whether additional mailboxes, endpoints, or accounts need investigation.

### 4.3 theHarvester

`theHarvester` is an OSINT tool that can collect publicly available information about a domain, including email addresses and subdomains, from supported public sources.

In a phishing investigation, publicly discovered email addresses may help an analyst understand an organisation's exposed information or identify possible targets. Results depend on the sources queried and should be treated as leads, not as a complete list of an organisation's users.

## 5. Email Header Analysis

An email header contains technical information about the message and the path it travelled through mail systems. It is one of the most useful sources of evidence during email investigations.

### 5.1 Important Header Fields

| Header field | Meaning and investigative value |
|---|---|
| `From` | Sender identity displayed in the email client. It can be spoofed. |
| `To` | Intended recipient shown in the message. |
| `Cc` | Recipients copied into the message. |
| `Bcc` | Blind-copy recipients; these may not appear in every recipient's copy. |
| `Date` | Date and time claimed by the sending system. Compare with other timestamps and timezones. |
| `Subject` | Subject line of the email. |
| `Return-Path` | Envelope sender used for bounce handling. It is not the same as `Reply-To`. |
| `Reply-To` | Address to which replies are directed, if specified. A mismatch with `From` may deserve investigation. |
| `DKIM-Signature` | DKIM signature and related parameters used for validation. |
| `Message-ID` | Message identifier that can help correlate messages and copies. |
| `MIME-Version` | Indicates MIME formatting support. |
| `Received` | Routing information added by mail servers as the message moves through the mail system. |
| `X-Spam-Status` | Provider- or system-specific spam assessment header, when present. |
| `Authentication-Results` | Authentication results such as SPF, DKIM, and DMARC, added by a receiving system. |

### 5.2 From, Reply-To, and Return-Path

These fields serve different purposes:

- `From` identifies the sender shown to the recipient.
- `Reply-To` specifies where a reply should be sent, if present.
- `Return-Path` records the envelope sender used for delivery-status notifications and bounces.

For example, an email may display a familiar company address in `From`, while `Reply-To` points to an unrelated external address. That difference is a useful clue, but it should be investigated in context rather than treated as proof by itself.

### 5.3 Received Headers

Mail servers normally add `Received` headers as a message passes through them. Newer hops are generally added above older hops, so the top entries are usually more recent.

When reconstructing the route, I can read the chain from the bottom upward. However, I should place greater trust in entries added by known, trusted mail infrastructure. An attacker may insert forged header text before the message reaches the receiving organisation.

### 5.4 Authentication-Results

`Authentication-Results` may report SPF, DKIM, and DMARC outcomes. I should identify which mail system added the result and whether that system is trusted. A sender can include forged header text, so an arbitrary `Authentication-Results` line should not automatically be trusted.

### 5.5 Viewing Headers

Email clients provide options to view the original message or its full headers.

- **Gmail:** Open the message, use the message's More menu, and choose **Show original**.
- **Outlook:** Open the message and locate the message-details or internet-headers option. Exact steps depend on the Outlook version.
- **EML files:** An `.eml` file stores an email message, including headers and body, and can be opened with a compatible mail client or inspected with a text editor.

When sharing headers for analysis, sensitive information such as personal email addresses, internal hostnames, tokens, and message contents should be protected.

## 6. Static Analysis of Phishing Emails

Static analysis means examining an email, URL, or file without executing it. It is a safer first step because it allows an analyst to collect clues before interacting with suspicious content.

### 6.1 Inspecting Links in HTML Emails

An HTML email can display one URL while the actual hyperlink points somewhere else. For example, the visible text may say `https://www.example.com`, while the underlying hyperlink destination is a completely different domain.

I should inspect the actual `href` destination rather than trusting the visible text. I should also look for:

- Misspelled or lookalike domains.
- Unusual subdomains.
- URL shorteners.
- IP addresses used instead of normal domain names.
- Unexpected file extensions or download paths.
- URL parameters containing encoded or personal information.
- Links that redirect through multiple websites.

I should not open a suspicious link directly on my normal workstation.

### 6.2 Understanding the Actual Domain

A URL can contain several subdomains. The important step is identifying the registered domain rather than judging the URL by the first familiar-looking word.

Example:

`company.com.attacker.net`

The registered domain in this example is `attacker.net`, not `company.com`.

Attackers may use familiar brand names as subdomains or in URL paths to make a link appear trustworthy.

### 6.3 Domain Registration and Age

A newly registered domain may be suspicious, especially when it is used in an unexpected email or imitates a known organisation.

WHOIS and domain-registration information can provide details such as registration dates, registrar information, and name servers, depending on what is publicly available.

However, domain age is only one clue:

- New domains can be legitimate.
- Old domains can be compromised or repurposed.
- Privacy-protected registration is not proof of malicious activity.

I should combine registration information with DNS records, reputation, website content, email context, and other indicators.

### 6.4 MX Records and SMTP Information

MX records identify the mail servers that receive email for a domain. They do not, by themselves, prove that a particular IP address is authorised to send email for that domain.

SPF records are more directly relevant to identifying authorised sending infrastructure. During an investigation, I should avoid confusing inbound mail routing (MX) with outbound sender authorisation (SPF).

### 6.5 Reputation and Threat-Intelligence Services

The lesson introduced several services that can provide useful context:

- **VirusTotal:** Aggregates results from multiple security vendors and other analysis sources for files, URLs, domains, and IP addresses.
- **Cisco Talos Intelligence:** Provides reputation and threat-intelligence information for IP addresses, domains, and other indicators.
- **AbuseIPDB:** Provides reports and reputation information related to IP addresses.
- **MXToolbox:** Offers email and DNS-related diagnostic tools, including checks for mail records and blocklist status.
- **WHOIS services:** Provide available domain-registration information.

These tools support an investigation, but their results are not final verdicts. I should record what was checked, when it was checked, and what the result actually means.

### 6.6 VirusTotal: Cached Results and Scan Time

A VirusTotal result may come from an earlier submission. The scan date matters. A URL scanned several months ago may have changed since then. A domain may have been clean at the time of the old scan and become malicious later.

When using VirusTotal, I should:

1. Check the last analysis or submission time.
2. Review detection names and the number of engines detecting the item.
3. Inspect available relationships and historical information.
4. Correlate the result with other sources.
5. Avoid interpreting zero detections as proof that the item is safe.

**Privacy warning:** Submitting a URL to a public analysis service may expose it to other users or researchers. URLs can contain personal information, access tokens, password-reset tokens, or other sensitive query parameters. I should follow organisational policy and avoid submitting confidential URLs or files to public services without authorisation.

## 7. Dynamic Analysis

Dynamic analysis involves observing a suspicious file or website while it is running or being accessed in a controlled environment.

It can reveal behaviours that static inspection cannot easily show, such as redirects, scripts, network connections, file creation, process activity, or attempts to download additional payloads.

### 7.1 Sandboxes

A sandbox is an isolated environment used to execute or inspect suspicious content while monitoring its behaviour.

Services and tools introduced in the lesson include:

- VMRay
- Joe Sandbox
- ANY.RUN
- Hybrid Analysis
- Browserling

The capabilities differ between platforms. Some focus on malware execution and system behaviour; others provide isolated browser sessions for examining suspicious websites.

### 7.2 What to Observe

During dynamic analysis, I should look for:

- Unexpected redirects.
- Requests to suspicious domains or IP addresses.
- Downloads of additional files.
- JavaScript or browser behaviour that attempts to hide the real destination.
- Credential-harvesting pages.
- Unexpected pop-ups or prompts.
- Process creation or suspicious child processes.
- Changes to files, registry locations, or system settings.
- Connections to command-and-control infrastructure.
- Behaviour that appears only after a delay or user interaction.

I should record the time, environment, actions performed, observed behaviour, and any indicators produced by the analysis.

### 7.3 Sandbox Limitations and Evasion

A clean sandbox result does not guarantee that a file or website is safe.

Malware may try to avoid analysis by:

- Waiting before performing malicious actions.
- Detecting virtual machines or sandbox environments.
- Requiring a particular user interaction.
- Checking the system's language, location, or configuration.
- Activating only at a particular time.
- Requiring a connection to infrastructure that is temporarily unavailable.

Some suspicious content may not produce obvious behaviour during a short analysis. I should consider the sandbox result alongside static analysis, reputation information, endpoint telemetry, and network logs.

### 7.4 Browser Isolation

Browser isolation runs website activity in a separate environment rather than directly on the analyst's normal workstation. This can reduce the risk of exposing the local device to malicious web content. It does not eliminate every risk, and I should still follow the organisation's approved procedures.

### 7.5 URL Parameters and Tracking

A URL may contain query parameters after a question mark (`?`). These parameters can be used for tracking, campaign identification, redirection, or passing data to a website.

A phishing link may contain an encoded recipient email address or a unique identifier. This can allow an attacker to identify which recipient clicked the link, even if the recipient did not enter a password.

I should inspect URL parameters carefully and avoid sharing them publicly because they may contain personal or sensitive information.

## 8. Additional Phishing Techniques

Phishing campaigns do not always use newly created malicious websites. Attackers may abuse legitimate platforms and services to make their content appear trustworthy.

### 8.1 Abuse of Cloud Storage

Attackers may host malicious files or phishing content on legitimate cloud-storage platforms such as Google Drive or Microsoft OneDrive. The domain may belong to a genuine service, but the file or content hosted there may still be malicious.

### 8.2 Abuse of Free Subdomains and Website Platforms

Attackers may create pages using free website-hosting or publishing services, such as WordPress, Blogger, or Wix.

The hosting platform may be legitimate while a particular page or account is controlled by an attacker. I should investigate the complete URL, page content, account context, redirects, and reputation rather than trusting the platform's brand.

### 8.3 Abuse of Online Forms

Attackers may use legitimate online form services, including Google Forms, to collect information or direct victims to another stage of a phishing campaign.

The fact that a form is hosted on a trusted service does not make the form's purpose trustworthy. I should assess what information it requests, who created or distributed it, and how it is being used.

## 9. Practical SOC Phishing Investigation Workflow

Based on the topics in this lesson, I can organise a phishing investigation into the following workflow.

### Step 1 – Preserve the Evidence

- Obtain the original email or an approved `.eml` export.
- Preserve the full headers and message body.
- Record when and where the email was reported.
- Avoid forwarding the message in a way that changes or removes important evidence.

### Step 2 – Review the Message

- Examine the sender, recipient, subject, timestamp, and message content.
- Look for urgency, unusual requests, impersonation, or unexpected attachments.
- Compare the visible sender with `Reply-To` and `Return-Path`.
- Identify suspicious links and attachments without opening them.

### Step 3 – Analyse the Headers

- Review the `Received` chain.
- Identify relevant sending IP addresses and mail infrastructure.
- Check SPF, DKIM, and DMARC results.
- Verify that authentication results came from trusted receiving infrastructure.
- Note unusual sender or reply-routing differences.

### Step 4 – Analyse the Indicators

- Extract domains, URLs, IP addresses, file names, and hashes.
- Inspect the actual hyperlink destination and URL parameters.
- Check domain-registration and DNS information where relevant.
- Use approved reputation and threat-intelligence services.
- Record scan timestamps and the limitations of each result.

### Step 5 – Perform Controlled Dynamic Analysis

- Use an approved sandbox or isolated browser environment.
- Observe redirects, downloads, scripts, network activity, and other behaviour.
- Record indicators and timestamps.
- Do not use a personal workstation to open suspicious content.

### Step 6 – Determine Campaign Scope

- Search for similar messages across mailboxes.
- Compare sender details, subjects, URLs, hashes, and timestamps.
- Identify recipients and users who interacted with the content.
- Correlate with endpoint, DNS, proxy, firewall, and authentication logs where available.

### Step 7 – Assess Impact and Escalate

- Determine whether a user clicked a link, opened an attachment, submitted credentials, or executed a file.
- Identify affected accounts and endpoints.
- Follow the organisation's incident-response procedures.
- Escalate confirmed or high-confidence malicious activity to the appropriate team.
- Document evidence, conclusions, uncertainty, and actions taken.

## 10. Important Investigation Principles

1. **Do not trust the display name alone.** Verify the sender using headers and supporting evidence.
2. **Do not treat authentication passes as proof of safety.** Compromised legitimate accounts can send malicious messages.
3. **Do not confuse header fields.** `From`, `Reply-To`, and `Return-Path` have different purposes.
4. **Do not trust every header line.** Give more weight to information added by known, trusted mail systems.
5. **Do not trust visible link text.** Inspect the actual destination.
6. **Do not judge a domain only by its age.** Use multiple sources of evidence.
7. **Do not confuse MX and SPF.** MX identifies inbound mail servers; SPF describes authorised sending hosts for a domain.
8. **Do not assume zero detections means safe.** New or evasive threats may not be detected.
9. **Check the timestamp of reputation results.** Old scans may not represent current behaviour.
10. **Use public analysis services carefully.** Submissions may expose sensitive data.
11. **Do not assume a legitimate hosting platform means legitimate content.** Cloud storage, free hosting, and online forms can be abused.
12. **Treat sandbox results as one source of evidence.** Malware may delay or hide its behaviour.

## 11. Key Terms

| Term | Meaning |
|---|---|
| Phishing | Social engineering intended to trick a person into taking an action beneficial to an attacker |
| Spoofing | Forging or manipulating identity information to appear as another sender or entity |
| SPF | DNS-based check of authorised sending IP addresses |
| DKIM | Cryptographic email signature used to verify signed message parts |
| DMARC | Policy and alignment framework built on SPF and DKIM |
| SMTP | Simple Mail Transfer Protocol, used to transfer email |
| MX record | DNS record identifying mail servers that receive email for a domain |
| Email header | Technical metadata describing a message and its delivery path |
| Message-ID | Identifier associated with an email message |
| OSINT | Open-source intelligence gathered from publicly available information |
| Static analysis | Examining an item without executing it |
| Dynamic analysis | Observing an item while it runs or is accessed in a controlled environment |
| Sandbox | Isolated environment for analysing suspicious files or content |
| IOC | Indicator of Compromise, such as a malicious IP, domain, URL, or file hash |
| URL parameter | Data included in a URL, often after `?`, that may control or identify a request |
| Campaign scope | The set of users, systems, or messages potentially associated with the same attack |

## 12. My Learning Reflection

In this session, I learned that phishing analysis is not simply about identifying spelling mistakes or suspicious-looking email addresses. A proper investigation combines message context, email authentication, header analysis, infrastructure checks, URL inspection, reputation data, and controlled dynamic analysis.

I also understood that security tools provide evidence rather than absolute answers. A clean VirusTotal result or sandbox run does not prove that a suspicious item is harmless. Likewise, a legitimate cloud-service domain can host attacker-controlled content.

The most important lesson for me is to follow an evidence-based process. I should preserve the original email, inspect its headers, identify and analyse indicators, determine whether other users were targeted, and assess whether anyone interacted with the message.

## 13. Practical Lab Progress

The following progress reflects the status I recorded while studying this lesson:

| Lab area | Recorded progress |
|---|---|
| Email header analysis | 100% – questions completed correctly |
| Static analysis | 0% at the time of recording; section marked complete in the lesson interface |
| Dynamic analysis | Reviewed as part of the study material; completion status not confirmed |

I will update this section after verifying the remaining practical exercises in LetsDefend.

## 14. Quick Review Questions

1. What is the difference between `From`, `Reply-To`, and `Return-Path`?
2. What does SPF check, and why does an SPF pass not prove that an email is safe?
3. What is the difference between static analysis and dynamic analysis?
4. Why should I check the timestamp of a VirusTotal result?
5. Why can a URL hosted on a legitimate cloud platform still be part of a phishing attack?
6. Why should I inspect the actual hyperlink destination instead of trusting the visible text?
7. What is the difference between an MX record and an SPF record?
8. Why might a malicious file behave differently in a sandbox than on a real endpoint?
9. How can URL parameters help an attacker identify which recipient clicked a link?
10. Why is identifying all recipients important when investigating a phishing campaign?

