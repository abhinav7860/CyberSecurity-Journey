SOC L1 Alert Triage
What is an alert in a SOC?
What is the main job of an L1 SOC analyst when an alert arrives?
What is the difference between a true positive and a false positive?
What things would you investigate when triaging an alert?
Why is context important during alert triage?
If an alert looks suspicious, what would an L1 analyst generally do next?
What is the difference between triage and a full incident investigation?

SOC L1 Alert Reporting
Why is alert reporting important in a SOC?
What information should a good SOC alert report contain?
What is the difference between observations/evidence and your conclusion?
Why should a SOC analyst avoid making unsupported assumptions in a report?
If you escalate an alert to L2, what information would you want to give them?
Why is maintaining a clear timeline useful when documenting an alert?
What makes a SOC report useful to another analyst who wasn't involved in the original investigation?

SOC Workbooks and Lookups
What did you understand well from Workbooks and Lookups?
What was confusing or difficult?
Did you document the room already, or is documentation still pending?

SOC Metrics and Objectives
What are SOC metrics, and why does a SOC use them?
What is the difference between a KPI and a normal metric?
What is MTTD (Mean Time to Detect)?
What is MTTR (Mean Time to Respond/Remediate)?
Why is reducing MTTD important for a SOC?
Why shouldn't a SOC judge its performance using only the number of alerts closed?
Give one example of a metric that could help determine whether a SOC is performing effectively

SIEM
What a SIEM is
Why SOC analysts use it
How logs/events reach a SIEM
How SIEM helps with detection and investigation
Alerts and correlation
The role of a SIEM in the SOC workflow

EDR
What is EDR, and what problem does it solve?
What kind of endpoints can an EDR monitor? Give a few examples.
What kind of information does EDR collect from an endpoint?
How is EDR different from traditional antivirus?
Suppose EDR detects powershell.exe launching a suspicious command. What would an L1 SOC analyst want to investigate?
What is the difference between detection and response in EDR?
Why is endpoint visibility important for a SOC analyst?
If EDR generates an alert, does that automatically mean the endpoint is compromised? Why or why not?

Splunk
What is Splunk and why is it useful in a SOC?
What is a log/event in the context of Splunk?
What is the purpose of searching/filtering logs in Splunk?
What is SPL (Search Processing Language) used for?
If you wanted to investigate failed login attempts, what information would you look for in the logs?
Why is it useful to correlate multiple events instead of looking at one log entry alone?
What would make a login-related event more suspicious?

Elastic Stack: The Basics
What did you understand well about Elastic Stack?
What was confusing or difficult?
Can you explain the difference between Splunk and Elastic Stack in your own words?

SOAR
What does SOAR stand for?
What problem does SOAR solve in a SOC?
What's the difference between SIEM and SOAR?
What is a playbook in SOAR?
Give one example of an action that could be automated by SOAR after an alert.
Why doesn't SOAR completely replace a SOC analyst?

Windows Logging for SOC
Why are Windows logs important for a SOC analyst?
What is the Windows Event Viewer used for?
What are the three important Windows log categories you learned about?
What is a Windows Event ID, and why is it useful?
What kind of information can an analyst get from a security event?
Why is it important to look at multiple related events instead of investigating only one event?
If you see a suspicious login event, what additional information would you investigate?

Windows Threat Detection 1
What initial-access methods did you learn about in this room?
How can a SOC analyst use Windows logs to detect these activities?
What indicators would make an event look suspicious rather than normal?
Why is understanding the normal behavior of a Windows environment useful when detecting attacks?
When investigating a suspicious event, what context would you look for around it?
If you identify activity that looks like an actual attack, what should an L1 analyst generally do next?

Windows Threat Detection 2
What happens after an attacker successfully breaches a Windows host?
What types of activity did you learn to look for when detecting an attacker's first steps after gaining access?
Which Windows logs/events were useful for identifying the activity you investigated?
Why is it important to build a timeline when investigating post-compromise activity?
What evidence would help you distinguish legitimate administrator activity from attacker activity?
If you identify suspicious post-compromise activity, what would you do as an L1 SOC analyst?

Windows Threat Detection 3
What did you understand best from Threat Detection 3?
What did you struggle with or find confusing?

Network Traffic Basics
What is network traffic?
What is the difference between incoming and outgoing traffic?
What is a packet?
What information can you typically identify from network traffic, such as source/destination IPs and ports?
Why is network traffic monitoring important for a SOC analyst?
What could make otherwise normal network traffic look suspicious?
Why is understanding normal network behaviour useful when detecting attacks?

Wireshark: The Basics
What is Wireshark used for?
What is a packet capture (PCAP)?
What is the difference between a capture filter and a display filter, if you learned both?
How can you identify the source and destination of network communication in Wireshark?
Why are protocols and ports important when analysing traffic?
What is the purpose of using filters such as http, dns, or tcp?
If you notice unusual traffic in a PCAP, what would you investigate next as an L1 SOC analyst?

Wireshark: Traffic Analysis
What is the main purpose of analysing network traffic in Wireshark?
How can you use filters to reduce a large PCAP to traffic you're interested in?
What information can you learn from examining a TCP connection?
Why is it useful to follow a TCP stream during an investigation?
How could DNS traffic help an analyst investigate suspicious activity?
What signs in network traffic might make you suspect malicious or unusual behaviour?
If you find something suspicious in a PCAP, what additional context would you want before deciding that it's malicious?

Wireshark: Packet Operations && Wireshark: Traffic Analysis
What did you learn from Packet Operations?
What did you learn from Traffic Analysis?
What part of Wireshark/packet analysis was difficult or confusing?
If you were given a suspicious PCAP in a SOC, what would be the first things you'd look at?

NetworkMiner
What is NetworkMiner used for?
What is the difference between using Wireshark and NetworkMiner?
What useful information can NetworkMiner extract from captured network traffic?
What did you find most useful about NetworkMiner?
What was confusing or difficult while working through the Network Traffic Analysis section?

Network Discovery Detection
What did you understand from Network Discovery Detection?
What did you struggle with or find confusing?

Data Exfiltration Detection
What is data exfiltration?
What are some signs that could indicate data is being exfiltrated?
Why can DNS traffic be important when investigating possible exfiltration?
Why is an unusually large amount of outbound traffic potentially suspicious?
How would you distinguish legitimate large data transfers from potentially malicious exfiltration?
If you detected possible exfiltration as an L1 analyst, what would you investigate next?
What part of this room was confusing or difficult for you?

Man-in-the-Middle Detection
What is a Man-in-the-Middle (MITM) attack?
How can an attacker position themselves between two communicating devices?
What signs in network traffic could make you suspect MITM activity?
Why is ARP relevant when investigating certain MITM attacks?
What would you investigate to determine whether suspicious traffic is actually malicious?
If you identify a possible MITM attack as an L1 SOC analyst, what would you do next?
What part of the room was confusing or difficult for you?

IDS Fundamentals
What is an IDS, and what is its main purpose?
What is the difference between a network-based IDS (NIDS) and a host-based IDS (HIDS)?
What is the difference between signature-based detection and anomaly-based detection?
If an IDS generates an alert, does it automatically mean an attack happened? Why?
As an L1 SOC analyst, what would you investigate after receiving an IDS alert?

Snort
What is Snort?
What is a Snort rule, and what does it help detect?
What is the difference between using Snort for real-time traffic monitoring and analysing a PCAP?
If Snort generates an alert, what information would you examine to determine whether it's a true positive?
What did you find confusing or difficult about IDS or Snort?

Phishing Analysis Fundamentals
What is phishing?
Why do attackers use phishing emails?
What are some common indicators that an email may be phishing?
Why should you inspect the sender's email address carefully?
What should you check before clicking a link in a suspicious email?
Why can attachments be dangerous?
What is the importance of checking email headers during an investigation?
If an employee reports a suspicious email, what would you investigate as an L1 SOC analyst?
How would you decide whether the email is likely malicious or legitimate?
What did you find confusing or difficult in this room?

Phishing Emails in Action
What was the main goal of the phishing emails you investigated?
What clues helped you identify an email as phishing/malicious?
What did you learn about checking sender addresses and domains?
How can a malicious link be identified without simply clicking it?
What role can email headers play in an investigation?
What kinds of attachments or attachment behaviour should make an analyst suspicious?
If an employee receives a suspicious email, what evidence would you collect before deciding whether it's malicious?
What part of this room was confusing or difficult for you?

Phishing Analysis Tools
What was the purpose of the phishing analysis tools you learned?
Which tools/techniques did you use to investigate a suspicious email?
What information were you looking for from the email, links, domains, or attachments?
How do these tools help an analyst validate an indicator instead of simply assuming it's malicious?
What would make you classify something as suspicious after using these tools?
What was confusing or difficult for you in this room?

Phishing Prevention
What is the main goal of phishing prevention?
What are some practices that can help users avoid falling for phishing attacks?
Why is user awareness important even when an organization has security tools in place?
What should a user do if they receive a suspicious email?
How can organizations reduce the risk of successful phishing attacks?
As an L1 SOC analyst, why is understanding phishing prevention useful even though your main role is detection/investigation?
What did you find confusing or difficult in this room?

The Greenholt Phish
What was the main phishing scenario in The Greenholt Phish?
What indicators did you investigate to determine whether the email was malicious?
What did you learn from examining the sender, links, domains, or other email details?
How did you use the available analysis information to reach your conclusion?
As an L1 SOC analyst, what would you document when reporting this phishing incident?
What was the most difficult or confusing part of this room for you?

Snapped Phish-ing Line
What was the main investigation scenario in Snapped Phish-ing Line?
What indicators did you use to determine whether the emails were legitimate or malicious?
How did you investigate the links/domains involved?
What role did email headers or metadata play in your analysis?
What would you include in an L1 SOC report after confirming a phishing email?
What is the biggest thing you learned from the entire phishing section?
What was confusing or difficult for you?

Linux Logging for SOC
Why are Linux logs important for a SOC analyst?
Where are Linux logs commonly stored?
What is the purpose of /var/log?
What kinds of information can an analyst learn from authentication-related logs?
Why is it useful to correlate multiple Linux log entries during an investigation?
If you see repeated failed authentication attempts, what additional information would you investigate?
How can Linux logs help an analyst build an incident timeline?
What was confusing or difficult about Linux Logging for SOC?

Linux Threat Detection 1
What type of Linux activity were you investigating in this room?
What logs or evidence did you use to identify the suspicious activity?
What indicators made the activity suspicious?
How did you establish what happened and when?
What would you investigate next if you encountered similar activity in a real SOC?
What was confusing or difficult for you in Linux Threat Detection 1?

Linux Threat Detection 2
What was the overall attack/infection chain you investigated in this room?
How did the attacker initially gain access to the Linux system?
What evidence showed that the exposed SSH service was being brute-forced?
Why did the attacker use the last command?
The attacker searched for processes using grep. Why would an attacker look for EDR/security-agent processes?
What was the purpose of transferring the malicious archive through SCP?
How did the logs help you reconstruct the attacker's actions and create a timeline?
If you encountered a similar investigation in a real SOC and didn't know which command or log to look at, what would be your investigation approach?
Which part of Task 5 or Task 6 was difficult for you, and what did you understand after getting help?

Linux Threat Detection 3
What was the main attack activity investigated in Threat Detection 3?
What evidence/logs helped you identify the attacker's actions?
What persistence or access-maintaining technique did you learn to detect?
What commands or Linux artifacts were useful during the investigation?
How did you determine which activity was suspicious rather than normal administrative activity?
How would you build a timeline of the attack using the available Linux evidence?
If you saw similar activity in a real SOC, what would you investigate first?
What was the most confusing or difficult part of Threat Detection 3?

