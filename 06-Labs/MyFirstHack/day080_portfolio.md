============================================================
 VULNERABILITY TRIAGE REPORT
============================================================

Analyst:   Abhinav Sabu
Date:      26 October 2026
Scope:     Triage of 7 scan findings for a hypothetical
           organisation
Method:    Risk-based prioritisation (severity weighed by
           exposure, value, active exploitation, patchability)


------------------------------------------------------------
 1. SUMMARY
------------------------------------------------------------

Seven vulnerability findings were triaged based on their
real risk to the organisation. Finding 1, the critical
internet-facing web application vulnerability actively
exploited in the wild, is the top priority because of its
immediate exposure and the availability of a patch.

Finding 6, the critical vulnerability affecting the
unsupported internet-facing legacy system, also requires
urgent mitigation through compensating controls because
it cannot be patched. The remaining findings are ranked
according to exposure, business impact, exploitation
activity, and patch availability, with Finding 3 closed
as not applicable after confirming the software is absent.


------------------------------------------------------------
 2. FINDINGS AND REAL-RISK ASSESSMENT
------------------------------------------------------------

  # | Severity | Real Risk | Key factors
 ---+----------+-----------+----------------------------------
  1 | CRITICAL | HIGH      | Public-facing web application;
   |          |           | actively exploited; company
   |          |           | website; patch available.
  2 | HIGH     | HIGH      | Internal customer database;
   |          |           | valuable customer data; behind
   |          |           | defences; no known exploitation;
   |          |           | patch available.
  3 | CRITICAL | LOW       | Software not installed or used;
   |          |           | no confirmed vulnerable asset;
   |          |           | no applicable exposure.
  4 | MEDIUM   | LOW       | Isolated test machine; no
   |          |           | valuable data; no external
   |          |           | access; patch available.
  5 | HIGH     | HIGH      | Finance staff laptops; sensitive
   |          |           | financial files; no known active
   |          |           | exploitation; patch available.
  6 | CRITICAL | HIGH      | Internet-facing legacy system;
   |          |           | unsupported software; no patch;
   |          |           | compensating controls possible.
  7 | LOW      | LOW       | Public-facing website; minor
   |          |           | information disclosure; patch
   |          |           | available.

Real-risk justifications:

Finding 1:
The critical vulnerability is actively exploited and
affects an internet-facing company website, making
immediate patching necessary to prevent potential
compromise.

Finding 2:
The vulnerability affects a valuable customer database
containing sensitive information, and although internal
defences reduce exposure, the potential impact of
compromise remains significant.

Finding 3:
Despite its critical severity, the affected software
is not installed or used in the organisation, so no
vulnerable asset or operational exposure is confirmed;
the finding should be validated before closure.

Finding 4:
The vulnerability has limited real-world impact because
the machine is isolated, contains no valuable data,
has no external access, and can be patched.

Finding 5:
The vulnerability affects finance staff laptops containing
sensitive financial files, creating significant potential
business impact despite the absence of known active
exploitation.

Finding 6:
The critical vulnerability affects an internet-facing
system running unsupported software with no available
patch, creating substantial risk that requires urgent
compensating controls.

Finding 7:
The vulnerability affects a publicly accessible website,
but its impact is limited to minor information disclosure
and a patch is available, making it a lower priority.


------------------------------------------------------------
 3. PRIORITISED FIX-FIRST ORDER
------------------------------------------------------------

 1st  -  Finding 1  -  Critical, internet-facing web
                     application vulnerability actively
                     exploited in the wild; patch available.
                     Immediate remediation is necessary.

 2nd  -  Finding 6  -  Critical, internet-facing legacy
                     system with unsupported software and
                     no patch. Urgent compensating controls
                     are required to reduce exposure.

 3rd  -  Finding 5  -  High-severity vulnerability affecting
                     finance laptops containing sensitive
                     financial files. Endpoint exposure
                     and data sensitivity make it a
                     significant business risk.

 4th  -  Finding 2  -  High-severity vulnerability affecting
                     the internal customer database.
                     Sensitive customer data creates
                     significant impact, but internal
                     defences reduce immediate exposure.

 5th  -  Finding 7  -  Low-severity vulnerability on a
                     public-facing website. Although
                     externally accessible, the impact
                     is limited to minor information
                     disclosure and a patch is available.

 6th  -  Finding 4  -  Medium-severity vulnerability on an
                     isolated test machine with no
                     valuable data or external access.
                     Its limited business impact allows
                     remediation to be deferred.

 Drop -  Finding 3  -  Critical vulnerability in software
                     that is not installed or used.
                     Validate the scanner finding against
                     the asset inventory and close it as
                     not applicable if confirmed.

Close-call reasoning:

Finding 1 ranks above Finding 6 because active exploitation
and patch availability make immediate remediation possible.
Finding 6 remains urgent because it is internet-facing
and cannot be patched.

Finding 5 ranks above Finding 2 because finance endpoints
contain sensitive financial files and have greater endpoint
exposure, while the database has additional internal
defences.

Finding 7 ranks above Finding 4 because it is publicly
accessible, even though its impact is minor. Finding 4
is isolated and contains no valuable data.

Finding 3 is excluded from the active remediation queue
only after confirming that the affected software is absent.


------------------------------------------------------------
 4. TRADE-OFFS AND DEFERRED RISK
------------------------------------------------------------

Consciously deferred:

Finding 2:
The internal customer database vulnerability is deferred
briefly while the actively exploited web vulnerability
and the unpatchable legacy system receive immediate
attention.

The accepted risk is that an attacker who gains internal
access or bypasses existing defences could exploit the
vulnerability and compromise sensitive customer data.

Finding 5:
The finance laptop vulnerability is scheduled after
the two most urgent findings.

The accepted risk is potential compromise of sensitive
financial files. This is a significant risk, so the
deferral should be short, documented, and approved by
the appropriate risk owner.

Finding 7:
The low-severity information disclosure vulnerability
is deferred until higher-priority findings are resolved.

The accepted risk is limited information disclosure from
the public-facing website while the available patch is
scheduled for deployment.

Finding 4:
The isolated test machine vulnerability is deferred
because of its limited exposure and low business impact.

The accepted risk is potential exploitation within the
isolated test environment. The machine must remain
isolated and must not contain sensitive production data.

Finding 3:
The finding is closed as not applicable only after
validating that the affected software is not installed
or used.

The remaining concern is inaccurate asset inventory
or scanner data. If the software is discovered later,
the finding must be reassessed.

Finding 6:
The underlying vulnerability cannot be patched, so the
organisation consciously accepts residual risk while
compensating controls are implemented.

The risk acceptance must be documented and approved
by the appropriate business or risk owner.


Compensating controls (for what can't be patched now):

Finding 6 — Unsupported internet-facing legacy system:

 - Isolation and segmentation:
   Place the system in a dedicated network segment and
   restrict communication with other internal systems.

 - Firewall restrictions:
   Block unnecessary inbound and outbound connections.
   Allow only essential and explicitly authorised traffic.

 - Access restrictions:
   Enforce least privilege, restrict administrative
   access, and allow access only from approved systems.

 - Virtual patching:
   Use a web application firewall, intrusion prevention
   system, or other suitable security control to block
   known exploit traffic where technically feasible.

 - Enhanced monitoring:
   Monitor system logs, network traffic, authentication
   attempts, and suspicious activity for signs of
   exploitation.

 - Backup and recovery:
   Maintain tested backups and a recovery plan to reduce
   the impact of a successful compromise.

 - Replacement planning:
   Develop a migration, upgrade, or decommissioning
   plan to eliminate the unsupported software.

These controls reduce exposure and potential impact but
do not eliminate the underlying vulnerability.

Additional controls for deferred findings:

Finding 2 — Internal database:
Restrict database access, enforce least privilege,
segment the database network, and monitor authentication
and access logs.

Finding 5 — Finance laptops:
Enforce endpoint protection, restrict local administrator
privileges, monitor suspicious activity, and prioritise
patch deployment.

Finding 7 — Public-facing website:
Use appropriate web application firewall rules, minimise
information disclosure, monitor web logs, and schedule
the available patch.

Finding 4 — Isolated test machine:
Maintain network isolation, restrict administrative
access, and ensure no sensitive production data is stored
on the machine.


Would re-prioritise if:

If Finding 5, the finance laptop vulnerability, begins
to be actively exploited in the wild, I would immediately
reassess its priority.

Confirmed exploitation would increase the likelihood
of compromise, while the sensitive financial files
increase the potential business impact.

The finding could move ahead of Finding 2 and become
the second remediation priority after Finding 1,
depending on the scope and severity of exploitation.

Actions would include:

 - Expedite patch deployment across affected laptops.
 - Investigate whether any finance endpoints have
   already been compromised.
 - Isolate affected devices if compromise is suspected.
 - Review access to sensitive financial files and
   relevant authentication logs.

The triage order is dynamic and must be reassessed
whenever exposure, exploitation activity, business
impact, or patch availability changes.


------------------------------------------------------------
 5. REASONING APPROACH
------------------------------------------------------------

Severity was used as the starting point for assessing
each vulnerability, but it was not treated as the sole
indicator of real risk.

The assessment considered whether attackers could reach
the affected system, the value and sensitivity of the
data or services it supported, whether exploitation was
occurring in the wild, and whether a patch was available.

Internet-facing vulnerabilities and actively exploited
findings received greater urgency, while isolated systems
and vulnerabilities affecting software that was not
installed received lower priority after validation.

The unpatchable legacy system required compensating
controls because the underlying vulnerability could not
be eliminated through normal patching.

The final order reflects the organisation's actual
exposure and business impact rather than simply sorting
the findings by their CVSS severity.

The key insight is that severity is not the same as
real risk. Effective vulnerability triage requires
context, defensible decisions, documented risk acceptance,
and continuous reassessment.


============================================================
 END OF TRIAGE REPORT
============================================================

