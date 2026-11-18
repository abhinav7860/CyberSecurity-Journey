# SIEM Introduction

**LetsDefend study notes \| 18 November 2026**

## 1. What is SIEM?

SIEM means **Security Information and Event Management**. It is a
security solution that collects, processes, stores, searches, and
analyses event data from an organization's technology environment to
help identify potential threats.

A company may generate logs from Windows and Linux systems, servers,
applications, firewalls, routers, switches, IDS/IPS, proxies, WAFs, EDR
products, identity providers, and cloud services. A SIEM brings data
from these sources into a central environment.

A SIEM helps a SOC to: - Centralize logs from different systems. -
Search events using timestamps, users, hosts, IP addresses, and other
fields. - Identify patterns and correlate activity. - Create reports,
alerts, and dashboards. - Support incident investigation and response.

**SIEM is not the SOC.** SIEM is a technology used by the SOC. It can
generate alerts when detection conditions are met, but an alert is not
automatic proof of an attack. Analysts must validate the evidence and
context.

The lesson references a Gartner 2021 image of commercial SIEM products.
That is a historical market snapshot, not a current ranking. The
important point is that many vendors provide SIEM platforms with broadly
similar purposes.

## 2. How SIEM works

A simplified SIEM pipeline is:

**Data sources → Log collection → Aggregation and parsing → Enrichment →
Storage and indexing → Search and detection → Alerts → SOC
investigation**

  -----------------------------------------------------------------------
  Stage                               What happens
  ----------------------------------- -----------------------------------
  Data generation                     Systems and applications create
                                      events

  Collection                          Agents, Syslog, remote collection,
                                      or APIs transfer events

  Aggregation                         Events from multiple sources arrive
                                      at a central processing point

  Parsing                             Raw messages are separated into
                                      useful fields

  Enrichment                          Context such as DNS, geolocation,
                                      or asset information is added

  Storage/indexing                    Events are retained and made
                                      searchable

  Detection                           Searches or rules identify
                                      conditions of interest

  Alerting                            A notification or case is generated

  Investigation                       Analysts validate the activity and
                                      decide what to do
  -----------------------------------------------------------------------

Not every deployment has a separate product for every stage. A single
platform may perform several of these functions.

## 3. Logs and logging

A **log** is a record of an event that occurred in an operating system,
application, network device, or other technology. **Logging** is the
process of recording those events.

A simple log contains: - **Timestamp:** when the event occurred. -
**Source:** which system or application generated it. - **Message:**
what happened. - **Additional fields:** for example, username, IP
address, event ID, process, result, or severity.

The lesson uses Ubuntu's `/var/log/auth.log` as an example. It contains
authentication-related messages, such as login and authentication
activity.

Logs are essential because the SIEM cannot detect activity it never
receives. Missing authentication logs can create a visibility gap for
login investigations; missing firewall logs can make network activity
harder to reconstruct; missing endpoint telemetry can limit process
investigations.

## 4. Log collection methods

The lesson groups collection into **agent-based** and **agentless**
methods, and also describes manual/custom collection.

### 4.1 Agent-based collection

A log agent is software installed on a source system to collect and
forward logs. Depending on the product, it may support: - Parsing and
field extraction. - Log rotation. - Buffering during temporary
connection problems. - Integrity checking. - Encryption. - Data
conversion, filtering, and routing.

Example raw message:

`username: LetsDefend; account: Administrator`

A parser could extract: - `username = LetsDefend` -
`account = Administrator`

**Advantages** - Designed and tested for supported collection tasks. -
Can provide parsing, buffering, encryption, and other capabilities. -
Can support continuous collection.

**Disadvantages** - Must be installed, configured, updated, and
maintained. - Consumes CPU, RAM, and sometimes disk resources. -
Advanced features may increase resource use.

### 4.2 Syslog

**Syslog** is a widely used standard for log message transmission. It is
supported by many network devices and operating systems, directly or
with additional software.

The lesson describes Syslog transport over: - UDP - TCP - TLS-protected
transport in supported configurations

Potential Syslog sources include switches, routers, IDS/IPS, firewalls,
Linux, macOS, and Windows systems configured with suitable software.

The lesson presents a simplified message structure containing:

**Timestamp -- Source Device -- Facility -- Severity -- Message Number
-- Message Text**

-   **Facility** identifies the type of process or subsystem that
    generated the message.
-   **Severity** indicates the urgency level.
-   **Message text** contains the event details.

In common Syslog standards, priority is derived from facility and
severity. Exact message syntax depends on the protocol version and
implementation.

**UDP** is connectionless and lightweight, but does not provide
TCP-style delivery guarantees. **TCP** is connection-oriented. **TLS**
can protect supported Syslog traffic in transit.

The lesson gives example packet sizes of 1024 bytes for UDP and 4096
bytes for TCP. Treat these as lesson-specific figures, not universal
limits. Actual message-size limits depend on the protocol, transport,
device, and implementation.

SOC checks for Syslog: - Is the source configured to send logs? - Is the
destination correct? - Is the expected UDP/TCP port reachable? - Is TLS
configured consistently, if used? - Is the receiver accepting
messages? - Are events dropped, truncated, or filtered? - Are clocks and
time zones correct?

Syslog transport alone does not guarantee secure, complete, or correctly
parsed logs.

### 4.3 Vendor and third-party agents

The lesson lists: - **Splunk Universal Forwarder:** collects configured
data and forwards it to Splunk. - **ArcSight Connectors:** collect and
process data for ArcSight environments. - **Elastic Beats:**
https://www.elastic.co/beats/ - **NXLog:** https://nxlog.co/

Agents and connectors can provide source-specific collection, parsing,
buffering, filtering, and forwarding capabilities. Choose a tool based
on supported sources, destination SIEM, deployment model, and
operational requirements.

### 4.4 Agentless collection

Agentless collection retrieves or sends logs without installing a
dedicated agent on the source. The lesson mentions remote connections
using: - SSH - WMI

**Advantages** - No dedicated agent installation on every source. - May
be easier to deploy where software installation is restricted. - Can
reduce agent update and deployment work.

**Disadvantages** - May have fewer collection features than an agent. -
Requires credentials or an authorized remote access method. -
Credentials can be exposed if not properly protected. - Collection can
fail when permissions, remote access, or connectivity changes. - Polling
may be less timely than continuous forwarding.

Protect credentials using secure secret storage, least privilege,
encrypted transport, and suitable authentication controls. Avoid shared,
highly privileged accounts for routine log collection.

### 4.5 Manual or custom collection

If existing agents cannot collect a required source, an organization may
use an application API, export function, or custom script. The lesson
gives a cloud-based application as an example.

Custom collection should handle authentication securely, errors, rate
limits, timestamp preservation, and monitoring of collection failures.

### 4.6 Comparison

  -------------------------------------------------------------------------
  Method            How it works      Benefits            Limitations
  ----------------- ----------------- ------------------- -----------------
  Agent             Software on       Rich features,      Installation,
                    source collects   continuous          maintenance,
                    and forwards      collection,         resource use
                                      parsing/buffering   

  Syslog            Source or agent   Broad device        Delivery,
                    sends Syslog      support             parsing, size,
                    messages                              and security
                                                          depend on
                                                          configuration

  Agentless         Collector         No dedicated agent  Credentials,
                    retrieves data    on every source     permissions,
                    remotely                              polling, feature
                                                          limits

  Manual/custom     Script, API, or   Can cover           Development and
                    export collects   unsupported sources maintenance
                    data                                  required
  -------------------------------------------------------------------------

## 5. Log aggregation and parsing

A **log aggregator** receives logs from multiple sources and provides a
central point for processing and routing them to their destination.

The lesson identifies these operations: 1. Parsing. 2. Filtering. 3.
Enrichment. 4. Log modification or normalization. 5. Routing.

### Parsing

Parsing breaks a raw message into meaningful fields. A web-server log
might contain a timestamp, client IP, HTTP method, URI, status code, and
response size. Parsing extracts those values so analysts can search and
group events by field.

**Preserve the original raw event where possible.** Parsing should not
destroy evidence needed for later investigation.

### Filtering

Filtering decides which events or fields continue through the pipeline.
For example, an organization may exclude repetitive debug messages or
route authentication logs separately.

Filtering can reduce storage and processing requirements, but careless
filtering can remove evidence needed for incident response or
compliance.

### Modification and normalization

Different sources may represent the same information differently.

The lesson examples: - Most sources use `dd-mm-yyyy`, but one uses
`mm-dd-yyyy`. - Some sources use UTC+2 while another component expects
UTC+1.

The aggregator may normalize formats and timestamps so that events can
be compared correctly.

Time handling is essential for incident timelines. Preserve original
timestamp and time-zone information when possible, while also
maintaining a normalized timestamp. Do not shift time without knowing
the source time zone and whether the source has already converted it.

### Enrichment

Enrichment adds contextual information to an event. The lesson lists
geolocation, DNS, and add/remove operations.

**Geolocation:** A source IP can be looked up to add approximate
country, region, or city information. This can help an analyst assess
whether a connection's apparent location is unusual.

Limitations: IP geolocation is approximate. VPNs, proxies, mobile
networks, cloud providers, and NAT can affect apparent location. A
location mismatch is a clue, not proof of malicious activity.

**DNS:** Forward DNS lookup maps a domain to an IP address. Reverse DNS
lookup attempts to map an IP address to a hostname through a PTR record.
DNS data may be missing, stale, or misleading, so treat it as context
rather than definitive identity.

**Add/remove:** Enrichment may add asset owner, business unit, device
criticality, or threat-intelligence context. It may also remove
duplicate or unnecessary fields. Do not remove original evidence that
could be important later.

## 6. EPS and aggregator scaling

**EPS means Events Per Second.** It measures the rate at which events
are received or processed.

\[ EPS = `\frac{\text{Number of events}}{\text{Time in seconds}}`{=tex}
\]

Example: 1,000 events in 5 seconds = 1,000 ÷ 5 = **200 EPS**.

EPS is not the same as the number of devices, average event size, or
daily storage volume.

Capacity planning should consider: - Average and peak EPS. - Average
event size. - Parsing and enrichment complexity. - Network bandwidth. -
Buffering requirements. - Storage throughput. - Indexing and search
workload.

Two environments with the same EPS may need different resources if one
generates much larger events or performs more complex processing.

### Scaling aggregators

The lesson explains that multiple aggregators can distribute incoming
logs instead of sending all traffic to one system. Distribution may use
round-robin/sequential, load-balanced, random, or source-based routing.

When scaling, consider: - Whether event order from a source must be
preserved. - Duplicate event risks. - What happens if an aggregator
fails. - Buffering and retry behaviour. - Whether downstream SIEM
storage can handle the increased rate.

Adding aggregators does not fix a bottleneck if the indexing or storage
layer is still overloaded.

## 7. Log storage

After collection and processing, logs must be stored so that analysts
can search and investigate them.

The lesson emphasizes two requirements: 1. **Capacity:** how much data
can be retained. 2. **Performance:** how quickly data can be retrieved.

A system may have enough disk space but still be unsuitable if a search
takes 15 minutes. During an incident, slow retrieval delays scoping,
timeline construction, correlation, and response.

### SIEM storage versus transactional databases

A transactional database commonly supports frequent inserts, updates,
and deletes. SIEM log storage is often designed around high-volume
ingestion, indexing, searching, time-based retrieval, and retention.

Security logs should not be casually edited after ingestion. The goal is
to preserve records and make them searchable.

### WORM

WORM means **Write Once, Read Many**. A WORM storage model is designed
to prevent data from being modified or deleted for a defined period or
under defined controls.

It can support: - Log integrity. - Audit and retention requirements. -
Evidence preservation. - Protection against tampering.

The lesson links to: https://en.wikipedia.org/wiki/Write_once_read_many

**Clarification:** WORM is a storage and retention concept, not a
requirement that every SIEM use one particular WORM technology. SIEM
platforms commonly use indexed stores optimized for searching.
Organizations may use immutable or WORM-capable storage for protected
retention or archival. Immutability and search performance are separate
design considerations.

Other storage considerations include ingestion rate, indexing
throughput, search latency, retention, compression, storage tiers,
replication, backup/recovery, access control, and integrity.

## 8. Alerting

After logs are collected, processed, and stored, the SIEM searches for
activity matching detection conditions and generates alerts.

An **alert** is a notification that a defined rule or search condition
has been met. It is not automatically a confirmed incident.

### Why timely alerting matters

If a suspicious event occurs today but the SIEM identifies it two days
later, the organization loses response time. Detection speed depends
on: - How quickly logs are collected. - Whether parsing is correct. -
How quickly data is indexed. - Search frequency and efficiency. -
Storage performance. - Alert delivery reliability.

### Two approaches in the lesson

1.  **Search stored data:** Run searches against data already collected
    and stored.
2.  **Evaluate incoming logs:** Generate detections while data is being
    collected or processed.

The exact implementation depends on the SIEM. Products may use scheduled
searches, real-time searches, streaming rules, or correlation engines.

### Example alerts

**New user added to Global Administrator:** Detect a privileged role
assignment or addition to a privileged group. Review who made the
change, which account was added, when it happened, and whether it was
authorized.

**15 failed logins in 3 minutes from the same IP:** This may indicate
brute-force activity or an authentication problem. Review targeted
accounts, source IP context, successful logons afterwards, VPN/proxy
use, and related activity.

These are examples, not universal thresholds. Tune detections to the
organization's normal behaviour.

### Alert quality and alert fatigue

Too many low-value alerts can cause alert fatigue, delayed triage,
overlooked important events, wasted analyst time, and reduced trust in
detections.

A useful alert should have: - A clear detection purpose. - Reliable data
sources. - A sensible condition or threshold. - Enough context to begin
investigation. - An owner and response process. - Regular tuning and
validation.

Do not suppress alerts merely to reduce their count if that removes
important visibility.

## 9. Alert-tuning techniques

The lesson introduces blacklisting, whitelisting, and long-tail log
analysis.

### 9.1 Blacklist

A blacklist contains known prohibited or suspicious items, such as
process names, IP addresses, domains, or applications.

The lesson uses `mimikatz.exe` as an example. If a log records that
process name, a detection can generate an alert.

**Advantages** - Easy to understand and implement. - Can identify known
prohibited indicators. - Lists can be updated as new indicators are
discovered.

**Limitations** - Attackers can change filenames, paths, domains, or
infrastructure. - A process can be renamed (the lesson example is
`mimikatz2.exe`). - IPs and domains can change ownership or be
reassigned. - A matching name does not always prove malicious
execution. - A blacklist only detects items already listed.

Use blacklists as one detection layer. Where possible, combine names
with hashes, paths, signatures, process ancestry, and behaviour.

### 9.2 Whitelist

A whitelist contains known or approved items. Activity outside the
approved set may be flagged.

The lesson example is a list of IP addresses with normal communication.
Communication with an address outside the list can generate an alert.

**Advantages** - Useful in tightly controlled environments. - Highlights
activity outside an expected set. - Can reduce noise when the approved
baseline is accurate.

**Limitations** - Requires continuous maintenance. - Legitimate business
activity changes. - New services, cloud providers, remote workers, and
software updates may introduce new activity. - A compromised approved
system can still be used maliciously. - An overly broad whitelist can
hide suspicious behaviour.

A whitelist match does not guarantee safety.

### 9.3 Long-tail log analysis

The lesson describes long-tail analysis as the idea that frequently
occurring behaviour is often normal, while rare or unusual events
deserve attention.

For example, Windows Event ID 4624 (successful logon) may occur
frequently on a workstation. A rare event or unusual pattern may stand
out from the baseline.

**Strengths** - Can find unusual events not represented in a
blacklist. - Helps identify rare behaviour. - Supports anomaly-focused
monitoring.

**Limitations** - Rare does not automatically mean malicious. - Common
activity can still be malicious. - New legitimate activity may appear
unusual. - Baselines can become outdated or be manipulated. - Small
environments may not have enough data for reliable statistical
conclusions.

Treat rarity as a reason to investigate, not proof of an attack. Add
context such as user role, asset criticality, time, source, process
behaviour, and related events.

### Comparison

  -----------------------------------------------------------------------
  Technique         Focus             Strength          Weakness
  ----------------- ----------------- ----------------- -----------------
  Blacklist         Known prohibited  Detects known bad Can be evaded by
                    indicators        items simply      changing
                                                        indicators

  Whitelist         Known approved    Highlights        Maintenance
                    items             activity outside  burden; approved
                                      the approved set  systems can be
                                                        compromised

  Long-tail         Rare or unusual   Can identify      Rare events are
  analysis          activity          previously        not necessarily
                                      unknown anomalies malicious
  -----------------------------------------------------------------------

A mature detection strategy can combine these methods with correlation
rules, behavioural analytics, threat intelligence, and analyst feedback.

## 10. Full SIEM pipeline example: repeated failed logins

Imagine an organization wants to detect repeated failed logins.

1.  **Event generation:** A Windows server or identity service records
    failed authentication attempts.
2.  **Collection:** An agent, Syslog integration, agentless collector,
    or API integration collects the events.
3.  **Aggregation:** Events arrive at a central aggregator or SIEM
    ingestion layer.
4.  **Parsing:** Fields such as timestamp, username, source IP, target
    host, authentication result, and event ID are extracted.
5.  **Enrichment:** Geolocation, reverse DNS, asset owner, or identity
    context may be added.
6.  **Storage:** Events are indexed and retained.
7.  **Detection:** A rule searches for a pattern, such as 15 failures in
    3 minutes from one IP.
8.  **Alert:** The SIEM creates an alert with matching evidence.
9.  **Investigation:** The analyst checks targeted accounts, source
    context, successful logons, and related activity.
10. **Response and documentation:** The analyst classifies the activity
    and follows the organization's response process.

Every stage matters. Missing collection prevents detection; incorrect
parsing can make a search miss events; slow storage delays
investigation; noisy alerts can overwhelm analysts.

## 11. Glossary

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  SIEM                                Security Information and Event
                                      Management

  Log                                 A recorded event or message

  Logging                             Recording events

  Log source                          Device, application, or service
                                      generating logs

  Log agent                           Software that collects and forwards
                                      logs

  Agentless collection                Remote retrieval without installing
                                      a dedicated source agent

  Syslog                              Standard for log message
                                      transmission

  UDP                                 Connectionless transport protocol

  TCP                                 Connection-oriented transport
                                      protocol

  TLS                                 Protocol used to protect data in
                                      transit

  Facility                            Syslog classification for the
                                      generating process/subsystem

  Severity                            Syslog indication of message
                                      urgency

  Aggregator                          Component that receives and
                                      processes logs from multiple
                                      sources

  Parsing                             Extracting structured fields from
                                      raw messages

  Filtering                           Selecting which events or fields
                                      continue

  Normalization                       Converting formats into a
                                      consistent representation

  Enrichment                          Adding context to an event

  EPS                                 Events per second

  WORM                                Write Once, Read Many

  Alert                               Notification generated when a
                                      detection condition is met

  Blacklist                           List of known prohibited or
                                      suspicious items

  Whitelist                           List of known approved items

  Long-tail analysis                  Looking for rare or unusual
                                      activity compared with a baseline
  -----------------------------------------------------------------------

## 12. Key takeaways

1.  SIEM collects and analyses organizational data to help identify
    potential threats.
2.  SOC analysts investigate SIEM alerts; an alert is not proof of
    compromise.
3.  Logs provide evidence about what happened, when, and which system
    recorded it.
4.  Log collection is foundational; missing logs create visibility gaps.
5.  Agents provide useful features but consume resources and need
    maintenance.
6.  Agentless collection avoids installing agents but has credential,
    permission, and capability limitations.
7.  Syslog is widely supported, but delivery and security depend on
    configuration.
8.  Aggregators can parse, filter, enrich, normalize, and route events.
9.  Timestamp normalization is essential for accurate incident
    timelines.
10. Geolocation and DNS enrichment provide context, not certainty.
11. EPS measures event rate, not storage size by itself.
12. Storage must provide both retention capacity and useful search
    performance.
13. WORM is an immutability/retention concept, not the same thing as an
    indexed search engine.
14. Alerts may be generated from stored data or evaluated as data
    arrives.
15. Thresholds must be tuned to the environment.
16. Blacklists, whitelists, and long-tail analysis all have limitations.
17. Rare activity is not automatically malicious; common activity is not
    automatically safe.
18. Detection quality depends on reliable collection, correct parsing,
    useful context, fast retrieval, and analyst validation.

## 13. My learning reflection

In this lesson, I learned how a SIEM works behind the scenes and why log
collection is one of its most important parts. A SIEM cannot detect
activity it never receives, so an organization must collect useful logs
from endpoints, servers, network devices, applications, and cloud
services.

I learned that logs can be collected through agents or agentless
methods. Agents can provide parsing, buffering, encryption, and other
features, but they consume resources and require maintenance. Agentless
collection can be easier to deploy in some environments, but it may
require remote credentials and can have fewer capabilities. I also
learned about Syslog, Splunk Universal Forwarder, ArcSight Connectors,
Beats, and NXLog.

I understood the role of a log aggregator. It receives events from
different sources and can parse, filter, normalize, enrich, and route
them. Enrichment can add geolocation, DNS, or other context. I also
learned why timestamps must be handled carefully so events from
different systems can be placed in the correct order.

The lesson introduced EPS, which measures how many events arrive per
second. This helps with capacity planning and scaling aggregators. I
also learned that storage planning is not only about disk size. Analysts
need to retrieve logs quickly during an investigation. WORM storage can
help protect records from modification, although it is a storage and
retention concept rather than a complete SIEM architecture.

Finally, I learned how SIEM alerts are created and why they need tuning.
Blacklists detect known prohibited indicators, whitelists identify
activity outside approved sets, and long-tail analysis looks for rare
behaviour. None of these methods is perfect by itself. An unusual event
needs investigation, and a common event can still be malicious.

My main takeaway is that SIEM detection quality depends on the complete
pipeline: collecting the right logs, processing them correctly,
enriching them with useful context, storing them efficiently, and
creating alerts that SOC analysts can investigate.

## 14. Suggested GitHub location and practice

Suggested path:

`CyberSecurity-Journey/LetsDefend/SIEM/01-SIEM-Introduction.md`

Practice: 1. Identify five possible log sources in a small organization.
2. Choose an appropriate collection method for each source. 3. Inspect
`/var/log/auth.log` on a system you are authorized to access. 4.
Identify timestamp, source, and message in several events. 5. Take a raw
log example and list fields a parser should extract. 6. Calculate EPS
for a sample event rate. 7. Explain how incorrect time-zone handling can
distort an incident timeline. 8. Compare blacklist, whitelist, and
long-tail analysis. 9. Design a repeated-failed-login alert and list the
evidence an analyst needs to validate it.

Practice only with systems and data you own or are authorized to
monitor.
