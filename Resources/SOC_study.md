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