# Phishing — Merry Clickmas

**Platform:** TryHackMe — Advent of Cyber 2025  
**Study date:** 20 November 2026  
**Focus:** Social engineering, phishing awareness, fake login-page simulations, SET, and SOC investigation.

> These notes are based on the supplied lesson. The exercise is an authorised simulation in the fictional TBFC lab. The techniques must only be used in an explicitly authorised environment.

## Learning objectives

- Understand social engineering and phishing.
- Learn the phishing types described in the room.
- Understand the fake-login-page demonstration.
- Learn how the Social-Engineer Toolkit (SET) is used in the lab email exercise.
- Connect the attack workflow to SOC monitoring and response.

## Task 1 — Introduction

TBFC has faced cybersecurity threats, so its local red team schedules penetration tests. One goal is to assess whether employees recognise phishing messages and whether the company has adequate protections.

The learner joins the fictional TBFC red team alongside Recon McRed, Exploit McRed, and Pivot McRed. The exercise tests employee awareness and helps determine whether further training is required.

The lab asks the learner to start both the AttackBox and target VM. The target VM may take around two minutes to boot.

---

# Task 2 — Phishing Exercise for TBFC

## 1. Social engineering

**Social engineering** means manipulating a person into making a mistake or taking an action that benefits an attacker.

Examples:
- Sharing a password.
- Opening a malicious file.
- Approving a fraudulent payment.
- Clicking a malicious link.
- Revealing confidential information.

The attacker targets human behaviour rather than directly attacking a computer system. Social engineering is sometimes called **human hacking**.

The lesson identifies three psychological factors:

| Factor | How it can influence a target |
|---|---|
| Urgency | Makes the target feel they must act immediately, reducing time to verify. |
| Curiosity | Encourages the target to open a message, attachment, or link to find out more. |
| Authority | Makes the target more likely to comply with someone they believe is trusted or senior. |

## 2. Phishing

**Phishing** is a form of social engineering in which the attacker uses messages to persuade a target to click, open, reply, or otherwise interact. The objective may be to steal information, money, or access.

### Types described in the lesson

| Type | Communication channel |
|---|---|
| Email phishing | Email |
| Smishing | SMS or text messages |
| Vishing | Voice calls |
| Quishing | QR codes |
| Social-media phishing | Social-media direct messages |

The delivery channel changes, but the goal remains similar: persuade a person to take an action that benefits the attacker.

## 3. The two S.T.O.P. anti-phishing mnemonics

The room teaches two S.T.O.P. reminders.

### S.T.O.P. — Questions to ask

This version, attributed in the lesson to All Things Secured, encourages users to question a message:

| Letter | Question |
|---|---|
| S | **Suspicious?** Does anything seem unusual? |
| T | **Telling me to click something?** Is it directing me to a link or action? |
| O | **Offering me an amazing deal?** Is the offer unusually attractive? |
| P | **Pushing me to do something now?** Is it creating pressure or urgency? |

### S.T.O.P. — Actions to take

| Letter | Action |
|---|---|
| S | **Slow down.** Scammers rely on adrenaline and rushed decisions. |
| T | **Type the address yourself.** Do not use the message's link. |
| O | **Open nothing unexpected.** Verify first. |
| P | **Prove the sender.** Check the real From address or number, not just the display name. |

The first mnemonic helps identify warning signs. The second tells me how to respond safely. A display name alone does not prove who sent a message.

## 4. Building the trap

A phishing exercise is designed around a specific objective. The lesson gives two examples of traps:

1. A malicious attachment intended to compromise a target machine.
2. A webpage that imitates a legitimate login page to capture credentials.

### Objective in the TBFC scenario

The objective is to obtain a target user's login credentials through a fake TBFC portal login page.

A fake login page must be hosted, and the lab's supplied script implements the credential-capture behavior. The script is already on the AttackBox at:

```bash
~/Rooms/AoC2025/Day02
```

The lesson says VPN-connected users can download the task files and should keep both files in the same directory.

### Starting the supplied lab server

```bash
cd ~/Rooms/AoC2025/Day02
./server.py
```

Example output:

```text
Starting server on http://0.0.0.0:8000
```

Interpretation:
- The web application is listening on port `8000`.
- `0.0.0.0` means the service is bound to all available network interfaces on that machine.
- The application is ready to serve the demonstration page.

The lesson provides these example addresses for viewing the page from the AttackBox:

```text
http://10.48.182.75:8000
http://127.0.0.1:8000
```

`127.0.0.1` is the loopback address and refers to the local machine. The `10.48.182.75` address is specific to the supplied lab example; the live room may assign a different address.

The supplied script displays credentials entered into the demonstration page in the terminal where the server is running. This is a controlled lab artifact. Never enter real credentials into an untrusted page.

## 5. Delivery using Social-Engineer Toolkit (SET)

**SET (Social-Engineer Toolkit)** is an open-source tool designed for social-engineering security testing. The lesson identifies David Kennedy as its primary designer.

In this task, SET is used to compose and send a phishing email to the lab recipient.

Start SET:

```bash
setoolkit
```

The initial menu includes:

| Option | Function |
|---|---|
| 1 | Social-Engineering Attacks |
| 2 | Penetration Testing (Fast-Track) |
| 3 | Third Party Modules |
| 4 | Update SET |
| 5 | Update SET configuration |
| 6 | Help, Credits, and About |
| 99 | Exit |

The room's menu path is:
1. `1` — Social-Engineering Attacks
2. `5` — Mass Mailer Attack
3. `1` — E-Mail Attack Single Email Address

The Mass Mailer menu also offers sending to a list of recipients. This room uses the single-recipient option.

The lesson notes:
- Option `99` returns to the main menu at the relevant menu stage.
- `Ctrl + C` can return to the main menu if a mistake is made while composing the message.

## 6. Understanding the email configuration

SET asks for information about the recipient, delivery method, sender, SMTP server, and message content.

| Field | Purpose |
|---|---|
| Recipient | Intended lab user |
| Delivery method | How the email is sent |
| From address | Sender email address displayed in the message |
| From name | Sender display name |
| SMTP username/password | Authentication details if required by the mail server |
| SMTP server | Mail server used for delivery |
| SMTP port | Port used to connect to the mail server |
| High priority | Whether the message is marked high priority |
| Attachment / inline attachment | Whether files are included |
| Subject | Email subject |
| Format | Plain text or HTML |
| Body | Message content |

### Values in the written lesson instructions

| Field | Value |
|---|---|
| Recipient | `factory@wareville.thm` |
| Delivery method | Own server or open relay |
| From address | `updates@flyingdeer.thm` |
| From name | `Flying Deer` |
| SMTP username/password | Blank |
| SMTP server | `10.48.177.254` |
| SMTP port | Default `25` |
| High priority | No |
| Attachment | No |
| Inline attachment | No |
| Subject | `Shipping Schedule Changes` |
| Format | Plain text |

### Discrepancy in the supplied lesson

The later worked terminal example shows a different sender:
- From address: `updates@deershipping.thm`
- From name: `Deer Shipping`

This differs from the earlier written instructions (`updates@flyingdeer.thm` and `Flying Deer`). I have preserved both versions rather than silently choosing one. Follow the live room's current instructions when completing the lab.

### Message example

The lesson's example uses a shipping-schedule theme:

```text
Dear elves,

Kindly note that there have been significant changes to the shipping schedules due to increased shipping orders.
Please confirm the new schedule by visiting [the lab-provided URL]

Best regards,
Flying Deer
```

The message uses a business context the target might expect: a shipping company communicating with the toy factory.

The lesson says to type `END` in capital letters on a new line to finish the message body. SET then reports that it has finished sending the email.

For a real organisation, any phishing simulation must be formally approved, scoped, and coordinated with the appropriate security and business stakeholders.

## 7. Observing the simulation result

After sending the email, the lesson instructs the learner to return to the terminal running `server.py` and observe it for approximately one to two minutes.

If the target enters credentials into the demonstration page, the supplied script displays the entered values in that terminal.

The room reports that the red team receives at least one set of working credentials.

### Why this matters

A successful simulation means at least one user interacted with the page and submitted credentials. The lesson warns that an adversary with those credentials could potentially disrupt TBFC's gift-delivery operation.

A successful phishing simulation should lead to defensive action, not simply a count of users who clicked.

Possible organisational responses:
- Reset credentials exposed during the exercise.
- Check whether the same password was reused elsewhere.
- Review authentication activity for suspicious logins.
- Enforce multi-factor authentication where appropriate.
- Improve awareness training.
- Review email filtering and reporting procedures.
- Make it easy for employees to report suspicious messages.

## 8. Lab answers included in the supplied lesson

The source text explicitly provides these answers:

| Question | Answer shown |
|---|---|
| Password used to access the TBFC portal | `unranked-wisdom-anthem` |
| Total number of toys expected for delivery, found by accessing the factory user's mailbox at `10.48.177.254` | `1984000` |

These are lab artifacts from the fictional scenario, not real-world credentials.

The lesson recommends the TryHackMe **Phishing Prevention** room for further practice.

---

# SOC Analyst Perspective

This room is presented as a red-team phishing exercise, but the same workflow connects directly to SOC responsibilities: recognise phishing, investigate reported messages, determine whether users interacted with them, and assess whether credentials or systems were compromised.

## 9. Email analysis

Useful evidence:
- Sender display name.
- Actual sender email address.
- Reply-To address.
- Subject and message body.
- URLs and domains.
- Attachments and file types.
- Email authentication results, where available.
- Mail delivery and filtering logs.

Questions:
- Does the visible sender name match the actual sender address?
- Is the domain expected?
- Does the message create urgency?
- Does the link lead to the expected organisation?
- Is the message consistent with normal business communication?
- Did the email gateway flag or quarantine it?

## 10. URL and website investigation

Useful evidence:
- URL in the message.
- Actual destination after redirects.
- Domain reputation and registration information, where available.
- TLS certificate and hostname details.
- Web proxy or DNS logs.
- Browser telemetry, where available.

Questions:
- Did the user click the link?
- Which host accessed the destination?
- Was it a legitimate company portal?
- Did the user submit credentials?
- Were there redirects to other suspicious destinations?

## 11. Credential compromise investigation

If credentials may have been submitted:
- Identify the affected account.
- Reset the exposed password through the approved process.
- Check whether the password may have been reused.
- Review successful and failed authentication events.
- Look for unfamiliar IP addresses, devices, or locations.
- Review access to email and other sensitive services.
- Revoke active sessions or tokens where appropriate.
- Check for suspicious mailbox rules or forwarding changes.

## 12. Endpoint investigation

If a user opened an attachment or downloaded a file:
- Review process-creation telemetry.
- Check downloaded files and their hashes.
- Examine browser and email-client activity.
- Review persistence indicators.
- Look for unusual network connections.
- Preserve relevant evidence before remediation.

## 13. Phishing incident workflow

```text
User reports suspicious email
            |
            v
Collect the original email and headers
            |
            v
Analyse sender, links, attachments, and context
            |
            v
Search mail logs for other recipients
            |
            v
Determine who clicked or submitted information
            |
            v
Assess account and endpoint impact
            |
            v
Contain: remove/quarantine message and protect accounts
            |
            v
Eradicate and recover affected systems/accounts
            |
            v
Document findings and improve awareness controls
```

## 14. Detection opportunities

| Activity | Potential evidence source |
|---|---|
| Phishing email delivered | Email gateway or mail server logs |
| User clicks suspicious URL | Secure web gateway, proxy, DNS, browser telemetry |
| Credentials submitted to fake page | Identity-provider logs, proxy logs, incident reports, simulation logs |
| Password guessing after credential theft | Authentication logs showing repeated failures |
| Unusual successful login | Identity-provider or VPN authentication logs |
| Mailbox abuse | Mailbox audit logs, forwarding rules, inbox rules |
| Malicious attachment execution | Endpoint detection and response telemetry |

A single indicator is not proof of compromise. Correlate email, user, endpoint, network, and identity evidence into a timeline.

---

# Key Terms

| Term | Meaning |
|---|---|
| Social engineering | Manipulating a person into taking an action that benefits an attacker |
| Phishing | Social engineering delivered through messages |
| Smishing | Phishing through SMS/text messages |
| Vishing | Phishing through voice calls |
| Quishing | Phishing using QR codes |
| S.T.O.P. | Two anti-phishing mnemonics taught in the lesson |
| Red team | Team authorised to simulate attacks and assess security |
| Phishing simulation | Authorised exercise that tests an organisation's resilience to phishing |
| Credential harvesting | Capturing usernames/passwords entered by a user |
| SET | Social-Engineer Toolkit |
| SMTP | Simple Mail Transfer Protocol, used to send email |
| Open relay | Mail-server configuration that relays messages without appropriate restrictions; it can be abused |
| AttackBox | TryHackMe's browser-based attacker environment |
| Loopback address | Address such as `127.0.0.1` that refers to the local machine |

---

# My Key Takeaways

- I learned that social engineering targets human behaviour and can use urgency, curiosity, and authority.
- I understood that phishing can be delivered through email, SMS, voice calls, QR codes, and social-media messages.
- I learned both S.T.O.P. mnemonics: one helps identify suspicious messages, and the other gives actions to take before responding.
- I understood that a phishing simulation measures an organisation's resilience and identifies where further awareness training may be needed.
- I learned that the TBFC exercise uses a fake portal page hosted by a supplied lab script.
- I understood what it means for a web server to listen on `0.0.0.0:8000` and why the AttackBox can access it through a lab address or loopback address.
- I became familiar with SET's menu structure and its Mass Mailer feature as presented in the room.
- I learned the role of SMTP server details, sender fields, recipient, subject, and message body in email delivery.
- I understood why the real sender address must be checked rather than trusting the display name.
- I learned that a successful phishing simulation can expose credential reuse and create broader business risk.
- I connected the attack workflow to SOC tasks such as email analysis, URL investigation, authentication review, endpoint investigation, containment, and awareness training.

---
