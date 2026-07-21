============================================================
 PHISHING EMAIL ANALYSIS REPORT
============================================================

Analyst:        Abhinav Sabu
Analysis Date:  21 July 2026
Engagement:     Suspected Phishing Email Triage
Methodology:    Headers > Sender > Content > Links > Verdict


------------------------------------------------------------
 1. EMAIL METADATA
------------------------------------------------------------

Subject:        More ways to create with Seedance 2.0
From (display): Hannah from DomoAI
From (actual):  hannah@domoai.app
Reply-To:       Same as sender (no different Reply-To observed)
Date received:  Tue, 14 Jul 2026, 7:34 PM
Recipient:      ab******@gmail.com


------------------------------------------------------------
 2. EXECUTIVE SUMMARY
------------------------------------------------------------

The email was initially treated as suspicious because it was delivered to the Gmail Spam folder. Technical analysis of the sender, email headers, and embedded URLs found no evidence of phishing or malicious activity. The email was determined to be a legitimate marketing communication from DomoAI introducing its new Text-to-Video and Frames-to-Video features.


------------------------------------------------------------
 3. HEADER ANALYSIS
------------------------------------------------------------

SPF:            PASS — Sender IP was authorised to send email
                for the domoai.app domain.

DKIM:           PASS — Valid digital signature confirmed the
                integrity of the message.

DMARC:          PASS — Authentication checks passed and domain
                alignment was successful.

Originating IP: 119.28.120.101
IP Geolocation: San Francisco, California,  USA
Reverse DNS:    DNS Record not found


------------------------------------------------------------
 4. SENDER DOMAIN ANALYSIS
------------------------------------------------------------

Domain:           domoai.app
Registered on:     Not publicly available
Registrar:         Not publicly available
Privacy enabled:   Yes 
Domain age:        3 Years
Lookalike of:     No. The sender domain matches the official
                  DomoAI domain and no evidence of
                  typosquatting was observed.


------------------------------------------------------------
 5. CONTENT INDICATORS
------------------------------------------------------------

  [ ] Urgency
  [x] Generic marketing message introducing new features
  [ ] Spelling/grammar errors
  [ ] Mismatched branding
  [ ] Authority impersonation
  [ ] Threat
  [ ] Reward bait


------------------------------------------------------------
 6. LINK ANALYSIS
------------------------------------------------------------

Visible link text:  Text to Video, Frames to Video
Actual URL:         https://mail-track.domoai.app/...
Destination domain: www.domoai.app
URL shortener:      No
HTTPS:              Yes
Landing page:       Official DomoAI website promoting AI
                    video generation features.

VirusTotal Result:  0/92 security vendors detected the URL
                    as malicious.

URLScan.io Result:  URL redirected to the official
                    www.domoai.app website. No malicious
                    behaviour observed during analysis.


------------------------------------------------------------
 7. VERDICT
------------------------------------------------------------

Classification:   LEGITIMATE MARKETING EMAIL
Confidence:       MEDIUM
Severity:         LOW

Reasoning:

Although the email was delivered to the Gmail Spam folder, the investigation found no technical indicators of phishing. SPF, DKIM, and DMARC authentication all passed successfully, confirming the authenticity of the sender. VirusTotal reported no malicious detections, and URLScan.io confirmed that the embedded tracking link redirected to the official DomoAI website. Based on the available evidence, the email is classified as a legitimate marketing communication rather than a phishing attempt.


------------------------------------------------------------
 8. RECOMMENDED ACTIONS
------------------------------------------------------------

If you received this email:

  [x] Verify the sender's domain before interacting with links.
  [x] Analyze embedded URLs using VirusTotal or URLScan.io.
  [x] Check email authentication (SPF, DKIM, and DMARC) when possible.
  [x] Delete or archive the email if it is not relevant.

If you clicked the link:

  [x] No immediate action required, as no malicious activity
      was identified during the investigation.
  [ ] Continue monitoring for unusual account activity if
      sensitive information was entered.


============================================================
 END OF REPORT
============================================================