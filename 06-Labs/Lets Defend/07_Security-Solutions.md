# Introduction to Security Solutions

**Study date:** 17 November 2026\
**Learning platform:** LetsDefend\
**Topic:** Introduction to Security Solutions

## 1. Why Organizations Need Multiple Security Solutions

Organizations use many technologies to protect endpoints, networks,
applications, cloud services, and sensitive information. No single
product can prevent or detect every attack. Each solution has a
different purpose and visibility.

-   IDS detects suspicious network or host activity.
-   IPS detects and can block suspicious activity.
-   Firewalls control network traffic according to rules.
-   EDR monitors endpoint behaviour and supports investigation and
    response.
-   Antivirus detects and blocks malicious files and activity.
-   Sandboxes execute suspicious files in an isolated environment.
-   DLP helps prevent sensitive information from leaving an
    organization.
-   Asset management maintains an inventory of hardware, software,
    mobile, and cloud assets.
-   WAF protects web applications by inspecting application traffic.
-   Load balancers distribute traffic across servers.
-   Proxy servers act as intermediaries between clients and
    destinations.
-   Email security solutions inspect messages, links, and attachments.

People are equally important. SOC analysts, incident responders, system
administrators, and security managers configure, monitor, investigate,
and maintain these technologies.

**Main idea:** Security combines people, processes, and technology.
Products support security teams; they do not replace skilled analysts or
correct configuration.

As a SOC analyst, I should understand what each product protects, what
it monitors, whether it detects or blocks, what logs it produces, where
it is deployed, and how its events can be correlated with other sources.

## 2. Intrusion Detection System (IDS)

### What is an IDS?

An **Intrusion Detection System (IDS)** is hardware or software that
monitors network or host activity to identify possible attacks,
suspicious behaviour, or policy violations. An IDS primarily detects and
reports. It commonly generates an alert for an administrator or forwards
events to a SIEM.

Example: A network sensor sees repeated connection attempts to many
internal devices. A detection rule identifies the pattern as suspicious
and generates an alert. The SOC analyst investigates the source,
destination, timing, and related activity.

### Types of IDS

**Network Intrusion Detection System (NIDS)**\
A NIDS monitors traffic at a selected point in a network. It examines
packets or traffic metadata for patterns associated with attacks. It can
only see traffic that reaches its monitoring interface. Network design,
encryption, and sensor placement affect visibility.

**Host Intrusion Detection System (HIDS)**\
A HIDS monitors an individual host, such as a workstation or server. The
lesson describes it as examining traffic entering and leaving that host.
In practice, host-based systems may also monitor logs, files,
configuration, processes, and integrity changes; exact visibility
depends on the product.

**Protocol-Based Intrusion Detection System (PIDS)**\
A PIDS examines communication associated with a particular protocol
between a client and server. It focuses on suspicious or invalid
protocol behaviour.

**Application Protocol-Based Intrusion Detection System (APIDS)**\
An APIDS monitors communication associated with a particular application
protocol or service. It attempts to identify suspicious
application-level activity.

**Hybrid IDS**\
A hybrid IDS combines two or more detection approaches, such as network
and host monitoring. This can improve coverage because an attack may be
visible in one source but not another.

### IDS functions and importance

-   Monitor activity according to configured rules or detection methods.
-   Identify suspicious patterns or policy violations.
-   Generate alerts and notify administrators.
-   Forward events to a SIEM for central analysis.

Detection quality depends on rules, signatures, configuration, and
visibility. A poorly written rule may miss an attack; an overly broad
rule may alert on normal activity. Rules need tuning and alerts need
investigation.

An IDS is useful as part of layered security, but it generally does not
block the traffic it detects. It is commonly used with firewalls, IPS,
endpoint security, and incident-response processes.

### IDS products mentioned in the lesson

-   Zeek (formerly Bro)
-   Snort
-   Suricata
-   Fail2Ban
-   OSSEC

These do not all operate identically. Zeek is commonly used for network
security monitoring and analysis; Snort and Suricata can operate as IDS
and, in supported configurations, IPS; Fail2Ban responds to repeated
authentication failures by updating firewall rules; OSSEC provides
host-based security monitoring.

### IDS logs and SOC investigation

The lesson highlights network-packet information. Useful fields can
include timestamp, source and destination IP addresses and ports,
protocol, alert/signature name, rule identifier, severity, packet or
flow details, and sensor name.

When investigating an IDS alert, I should ask: - What rule generated the
alert, and what does it detect? - Which source and destination are
involved? - Is the traffic expected? - Are there related firewall, EDR,
or SIEM events? - Is the alert a true positive, false positive, or does
it need more evidence?

### IDS placement

A NIDS is placed where it can observe relevant traffic, such as near a
network boundary, between network segments, or near a data centre. It
may receive mirrored traffic through a network TAP or switch SPAN port;
it does not always need to be inline. A HIDS is installed on or
associated with the host it monitors.

## 3. Intrusion Prevention System (IPS)

### What is an IPS?

An **Intrusion Prevention System (IPS)** monitors network or host
activity, detects suspicious behaviour, and can take action to prevent
it.

Example: An IPS detects traffic matching an exploit rule and drops the
packet or blocks the connection according to its configuration. It also
records the event and may notify the security team.

### Types of IPS

**Network-Based IPS (NIPS):** Monitors network traffic and can block
traffic matching configured prevention rules. It is commonly deployed
inline so traffic passes through it.

**Host-Based IPS (HIPS):** Runs on an endpoint or server and monitors
suspicious activity on that host. Depending on the product, it may block
processes, system changes, or other activity.

**Network Behaviour Analysis (NBA):** Focuses on unusual traffic
patterns or flows, including activity associated with DoS attacks,
scanning, or abnormal network behaviour. NBA is often a detection
capability; whether it blocks depends on product and integration.

**Wireless IPS (WIPS):** Monitors wireless network activity to identify
and, where supported, prevent threats such as rogue access points or
suspicious wireless behaviour.

### IPS functions, importance, and products

An IPS monitors, detects, takes configured actions such as dropping
packets or resetting connections, and generates alerts. It can reduce
the time between detection and prevention, but incorrect rules may block
legitimate business traffic. IPS systems need ongoing monitoring,
tuning, updates, and validation.

Products named in the lesson: - Cisco NGIPS - Suricata - Fidelis

### IPS logs

The lesson lists date/time, attack message, source IP and port,
destination IP and port, action, and device name. The action field is
especially important: it may indicate allowed, blocked, dropped, reset,
or another outcome.

An alert does not automatically prove the attack was blocked. I should
inspect the action and correlate with other logs.

### IPS placement

A network IPS is often inline at a network boundary or between important
network segments. A host IPS is installed on the endpoint or server it
protects.

## 4. IDS vs IPS

  -----------------------------------------------------------------------
  Feature                 IDS                     IPS
  ----------------------- ----------------------- -----------------------
  Main purpose            Detect suspicious       Detect and prevent
                          activity                suspicious activity

  Typical response        Alert/report            Alert and take
                                                  configured action

  Network placement       Often out-of-band or    Commonly inline
                          mirrored traffic        

  Blocking risk           Usually lower           Higher if rules are
                                                  incorrect

  SOC use                 Detection and           Prevention monitoring
                          investigation           and investigation
  -----------------------------------------------------------------------

**Memory aid:** IDS tells the team that something suspicious may be
happening. IPS can take action to stop traffic matching its prevention
rules. Modern products may combine both capabilities.

## 5. Firewalls

### What is a firewall?

A **firewall** is hardware or software that monitors incoming and
outgoing network traffic and allows or blocks it according to configured
security rules.

Rules may consider source/destination IP, ports, protocol, traffic
direction, connection state, and, depending on the product, application
or user identity.

Example: An organization may allow employees to access an approved
business service while blocking unnecessary inbound connections to
workstations.

### Types of firewall

**Packet-filtering firewall:** Checks packet information such as IP
addresses, ports, and protocols against rules. It is efficient but basic
packet filtering has limited understanding of application content.

**Stateful inspection firewall:** Tracks connection state and can
distinguish packets belonging to an established session from unexpected
packets. The lesson uses the term Stateful Multi-Layer Inspection (SMLI)
for a firewall combining packet inspection and connection-state
tracking.

**Application-level gateway / proxy firewall:** Acts as an intermediary
and can inspect application-layer communication. It can apply rules
based on application protocol content.

**Circuit-level gateway:** Validates sessions or connections rather than
deeply inspecting all application content. The lesson associates it with
session-layer and TCP session verification.

**Cloud firewall / Firewall as a Service (FWaaS):** Provides firewall
capabilities as a cloud-delivered service. Capacity and configuration
may be adjusted without the organization operating all physical
infrastructure.

**Endpoint firewall:** Runs on an individual device and filters
inbound/outbound traffic. Windows Defender Firewall is an example.

**NAT firewall:** A NAT-enabled gateway translates private internal
addresses to externally routable addresses. NAT can make internal
addressing less directly visible, but NAT alone is not a complete
security control; firewall policy is still needed.

**Next-Generation Firewall (NGFW):** Combines traditional firewall
functions with features such as application awareness, intrusion
prevention, and deep packet inspection (DPI), depending on product and
license.

**Threat-focused NGFW:** The lesson describes this as an NGFW with
additional threat-detection and response capabilities. Exact features
vary by vendor.

**Unified Threat Management (UTM):** Combines several security functions
in one platform, potentially including firewalling, antivirus, IPS, and
web filtering.

### How a firewall works

A firewall evaluates traffic against rules and may allow, deny, reject,
or otherwise handle it. For example, a company may allow approved
devices to access a business application, block unsolicited inbound
connections, permit DNS only through approved resolvers, or restrict
communication between departments.

This supports **network segmentation**: separating systems into zones
and controlling communication between them.

Rule order and default policy matter. A broad allow rule can undermine
restrictions; an overly restrictive rule can interrupt business
operations.

### Importance and products

Firewalls provide network access control and reduce unnecessary
exposure. They cannot stop every threat: permitted encrypted traffic may
still carry malicious activity, and a compromised endpoint or account
may already be inside the network.

Products listed: - Fortinet - Palo Alto Networks - SonicWall - Check
Point - Juniper - pfSense - Sophos

### Firewall logs

The lesson lists date/time, source and destination IPs, source and
destination ports, action, packets sent, and packets received. Other
products may also record protocol, rule name/ID, interface, user,
application, connection state, bytes, and session duration.

SOC example: repeated denied connections from one external IP to many
internal ports may indicate scanning. Correlate with IDS alerts,
endpoint telemetry, and asset information.

### Firewall placement

A network firewall is commonly deployed at the boundary between an
organization and external networks, and between internal security zones.
An endpoint firewall runs on the host. Exact placement of firewall, IDS,
and IPS depends on architecture.

## 6. Endpoint Detection and Response (EDR)

### What is EDR?

**Endpoint Detection and Response (EDR)** monitors endpoint activity,
collects telemetry, detects suspicious behaviour, and supports
investigation and response.

Endpoints include desktops, laptops, servers, virtual machines, and
other supported devices.

### Core components

1.  **Endpoint data collection agents:** Software on a device that
    collects telemetry such as process execution and file activity.
2.  **Automated response:** May isolate a device, stop a process, or
    quarantine a file, depending on permissions and configuration.
3.  **Analysis and forensics:** Helps analysts investigate activity,
    reconstruct events, and collect evidence.

### EDR functions and importance

EDR monitors and collects endpoint activity, analyses it for suspicious
behaviour, alerts analysts, may take configured response actions, and
supports forensic investigation.

Attackers may compromise an endpoint and use it to reach more critical
systems. EDR helps detect suspicious scripts, credential theft, lateral
movement, ransomware behaviour, and other threats. It does not guarantee
that every attack will be detected.

Products named in the lesson: - SentinelOne - CrowdStrike - Carbon
Black - Palo Alto Networks - FireEye HX

### EDR logs and telemetry

The lesson describes process names, file names and paths accessed, file
reads or modifications, sizes, and hashes. Depending on the product,
telemetry may also include parent/child process relationships, command
lines, user/logon details, network connections, Registry changes,
detection severity, and response actions.

SOC example: EDR reports that an Office application started a script
interpreter, which launched a command shell. I should inspect the
process tree, command line, user, paths, and network activity.

## 7. Antivirus Software (AV)

### What is antivirus?

**Antivirus (AV)** detects malicious files or activity and may block,
quarantine, or remove threats.

Traditional AV focuses heavily on file scanning, while modern endpoint
protection may also use behaviour monitoring and cloud intelligence.

### Signature-based scanning

AV compares a file or its characteristics with known malware signatures
in a database. A match may cause the file to be identified and
quarantined or removed.

**Strength:** Effective for many known threats.\
**Limitation:** New or modified malware may not match an existing
signature. Databases need regular updates.

### Heuristic and behaviour-based detection

The lesson describes heuristic scanning as examining file
characteristics and behaviour rather than relying only on known
signatures. For example, a program attempting suspicious access to
protected system files may be flagged even if its exact signature is
unknown.

This can detect new or modified threats, but legitimate administrative
tools may also perform powerful actions and cause false positives.

### AV functions, products, and logs

Functions include scanning, detecting known or suspicious malware,
blocking execution/access, quarantining or removing files, and recording
findings.

Products listed: - McAfee - Symantec - Bitdefender - ESET - Norton

Logs may contain file name, size, path, signature/detection name,
malware type, scan time, action taken, and quarantine status.

**SOC distinction:** An AV detection tells me that a product identified
a file or behaviour. I still need to determine whether it was blocked,
whether it executed earlier, and whether related activity occurred.

## 8. Sandbox Solutions

### What is a sandbox?

A **sandbox** is an isolated environment used to run or open suspicious
files and observe behaviour without exposing an ordinary production
system directly. Depending on capability, it may analyse executables and
documents such as PDF, DOCX, or XLSX.

A sandbox may report process creation, file access, Registry changes,
network connections, DNS requests, execution duration, behavioural
detections, and hashes.

### Benefits and limitations

The lesson identifies benefits: - Reduces risk to normal hosts when
properly isolated. - Helps identify potentially dangerous files. -
Allows testing of software updates before production. - Can help
investigate threats involving zero-day vulnerabilities.

A sandbox does not guarantee safety. Malware may detect the environment,
delay activity, or require conditions that are absent.

Products listed: - Check Point - McAfee - Symantec - Trend Micro -
Proofpoint

Sandbox reports may include sample hash, name/type, analysis time,
process tree, files accessed/created, network activity, and behavioural
indicators.

**Privacy warning:** Before uploading a sample to an online sandbox,
check whether it contains confidential, personal, customer, or
organizational data. Some services may share samples or reports. Follow
organizational policy.

## 9. Data Loss Prevention (DLP)

### What is DLP?

**Data Loss Prevention (DLP)** helps prevent sensitive or critical
information from being disclosed or transferred outside an
organization's permitted boundaries.

Examples include customer personal information, payment-card data,
employee records, intellectual property, confidential documents, and
credentials.

### Types of DLP

**Network DLP:** Monitors data moving across network channels. It may
detect sensitive content in a transfer and block, audit, or report it.

**Endpoint DLP:** Monitors activity on a particular device. Depending on
the product, it may control copying, printing, removable-media use, or
file transfers. It is useful for remote laptops.

**Cloud DLP:** Helps discover and protect sensitive information stored
in or transferred through cloud services and applications.

### How DLP works

DLP uses policies and detection methods such as data patterns, keywords,
file classification, document fingerprints, and context such as user,
application, destination, or device.

If a policy matches, the product may block the action, alert an analyst,
encrypt or quarantine content, or log the event. A format match alone
does not always prove that data is sensitive; policies need context and
tuning.

Products listed: - Forcepoint - McAfee - Trend Micro - Check Point -
Symantec

### SOC investigation

For a DLP alert, determine what data was detected, which user and device
were involved, which application/channel was used, the destination,
whether the action was blocked or allowed, whether the transfer was
authorized, and whether related endpoint or identity activity exists.

## 10. Asset Management Solutions

### What is asset management?

IT Asset Management (ITAM) software helps identify, inventory, track,
maintain, and manage technology assets through their lifecycle.

The lesson identifies four broad categories: 1. Software. 2. Hardware.
3. Mobile devices. 4. Cloud resources.

### Benefits and security importance

Asset management supports standards, documentation, inventory control,
maintenance, and strategic decisions.

A security team cannot protect assets it does not know exist. An
accurate inventory helps identify: - Which servers and endpoints
exist. - Which operating systems and software versions are installed. -
Who owns each asset. - Which devices are internet-facing. - Which assets
are unsupported or unpatched. - Which devices contain sensitive data.

When a critical vulnerability is announced, asset inventory helps
identify affected systems and prioritize patching.

Products listed: - AssetExplorer - Ivanti - Armis - Asset Panda

For SOC investigations, asset owner, purpose, criticality, operating
system, and exposure provide context. An alert involving a domain
controller may have a different risk from one involving a test
workstation.

## 11. Web Application Firewall (WAF)

### What is a WAF?

A **Web Application Firewall (WAF)** monitors HTTP/HTTPS traffic to and
from a web application and applies rules to allow, block, or otherwise
handle requests.

It helps protect web applications from attack patterns such as SQL
injection attempts, XSS attempts, malicious request patterns, protocol
violations, and automated abusive traffic, depending on the product.

A WAF does not replace secure application code, authentication,
authorization, or patching.

### Types of WAF

**Network-based WAF:** Often a dedicated hardware appliance or network
service. It can provide performance but may require infrastructure and
maintenance.

**Host-based WAF:** Software installed on or alongside a web server. It
can be customizable but uses server resources and requires maintenance
and hardening.

**Cloud-based WAF:** Delivered as a service. It can be easier to scale
and maintain, but policies still need correct configuration.

### How a WAF works

A WAF commonly sits in front of a web application. Incoming HTTP
requests pass through its inspection and policy engine. It may allow,
block, log, alert, or challenge a request, depending on capability.

A request containing a pattern associated with SQL injection may be
blocked by a rule. But broad rules can block legitimate requests, while
narrow rules may miss attacks. Tuning matters.

Products listed: - AWS - Cloudflare - F5 - Citrix - FortiWeb

WAF logs may include timestamp, source IP, host, URL, HTTP method,
matching rule, request details, action, response status, and request ID.

For an alert, determine whether the request was blocked, whether it
reached the application, and whether application logs show evidence of
successful exploitation. A WAF alert does not automatically prove
compromise.

## 12. Load Balancer

### What is a load balancer?

A **load balancer** is hardware or software placed in front of multiple
servers to distribute incoming traffic among them.

It helps prevent one server from receiving too much traffic while others
are underused.

### How it works

A load balancer selects a backend server using an algorithm or policy.
Examples include: - Round robin. - Least connections. - Weighted
distribution. - Health-based routing.

If one server becomes unhealthy, the load balancer may stop sending it
new requests.

### Benefits and security relevance

Load balancing improves workload distribution, availability, scaling,
and resilience. It can route around failed servers.

It is not by itself a complete DoS/DDoS defence. A large attack may
overwhelm the load balancer, network links, or backend capacity.
Additional DDoS protection, rate limiting, upstream filtering, and
capacity planning may be required.

Products listed: - Nginx - F5 - HAProxy - Citrix - Azure Traffic
Manager - AWS load-balancing services

A **DoS (Denial of Service)** attack attempts to make a service
unavailable by exhausting resources or disrupting operation. A **DDoS**
attack uses multiple sources or systems to generate attack traffic.

## 13. Proxy Servers

### What is a proxy?

A **proxy server** is an intermediary between a client and another
server. The client sends a request to the proxy, which forwards it
according to its configuration.

Proxies may provide access control, monitoring, filtering, caching,
privacy/address masking, security inspection, and routing.

### Forward proxy

A **forward proxy** acts on behalf of clients. For example, employees
may access the internet through an organization's proxy. It can apply
web-access policies, log requests, and filter destinations.

### Reverse proxy

A **reverse proxy** acts on behalf of servers. Clients connect to the
reverse proxy, which forwards requests to backend servers. It may
provide routing, TLS termination, caching, access control, and load
distribution.

The lesson names Varnish and Squid in its reverse-proxy discussion.
Product roles vary by configuration; Nginx, HAProxy, and dedicated
application-delivery products are also commonly used as reverse proxies.

### Other proxy categories in the lesson

These labels describe different characteristics and are not all mutually
exclusive.

  -----------------------------------------------------------------------
  Type                                Explanation
  ----------------------------------- -----------------------------------
  Transparent proxy                   Forwards requests without requiring
                                      explicit client proxy
                                      configuration; may still inspect or
                                      modify traffic

  Anonymous proxy                     Attempts to conceal the client's
                                      original IP from the destination

  High-anonymity proxy                Attempts not to reveal proxy use or
                                      the client's original IP to the
                                      destination

  Distorting proxy                    Presents misleading
                                      client-identification information

  Datacenter proxy                    Hosted in a data centre rather than
                                      on a residential ISP connection

  Residential proxy                   Uses an IP associated with a
                                      residential ISP network

  Public proxy                        Openly available to many users; may
                                      be unreliable or unsafe

  Shared proxy                        Used by multiple clients; one
                                      user's activity or reputation may
                                      affect others

  SSL proxy                           Handles SSL/TLS-related
                                      connections; exact inspection
                                      capability depends on the product

  Rotating proxy                      Changes egress IP across requests
                                      or sessions

  Split proxy                         Uses two cooperating proxy
                                      components on separate systems, as
                                      described by the lesson

  Non-transparent proxy               Explicitly configured or otherwise
                                      apparent to the client

  Hostile proxy                       Malicious intermediary that may
                                      eavesdrop on or manipulate traffic

  Intercepting proxy                  Intercepts traffic as a network
                                      intermediary

  Forced proxy                        Network policy directs traffic
                                      through the proxy

  Caching proxy                       Stores eligible responses to serve
                                      later requests more efficiently

  Web proxy                           Focuses on web traffic

  SOCKS proxy                         Forwards traffic using SOCKS and
                                      can support multiple application
                                      protocols

  HTTP proxy                          Designed to handle HTTP traffic
  -----------------------------------------------------------------------

A proxy category does not automatically mean that the service is secure
or anonymous. Privacy depends on configuration, encryption, operator
trust, and logging.

### Benefits and SOC importance

Proxies can manage traffic, filter destinations, cache content, and mask
a client's IP from a destination. They do not guarantee anonymity; the
proxy operator may see activity.

When a server receives a request through a proxy, the visible source IP
may be the proxy rather than the original client. SOC analysts should
use trusted proxy logs and correctly configured forwarding headers to
identify the original source.

Important cautions: - Do not blindly trust a client-supplied
`X-Forwarded-For` header. - Trust forwarding information only from
known, controlled proxies. - Correlate proxy, firewall, DNS, identity,
and application logs. - Preserve timestamps and request IDs.

Proxy-related services listed: - Smartproxy - Bright Data - SOAX -
Oxylabs

## 14. Email Security Solutions

### What is email security?

Email security solutions are hardware or software products designed to
protect users and organizations from threats delivered through email.

### Common functions

-   Inspect attachments.
-   Check URLs in messages.
-   Detect spoofed or impersonated messages.
-   Block known malicious emails.
-   Block messages from known malicious senders or sources.
-   Alert administrators or other security products.

Modern systems may also use spam filtering, sender authentication
checks, sandbox analysis, URL rewriting, impersonation detection, and
attachment analysis.

### Importance

Phishing manipulates users into revealing information, opening malicious
files, visiting harmful websites, or performing actions that benefit an
attacker.

Email security can inspect messages before delivery, but no gateway
guarantees that every malicious message will be detected. Attackers may
use compromised legitimate accounts, newly registered domains, or
trusted cloud services. User awareness, identity protection, endpoint
controls, and SOC investigation remain important.

Products listed: - FireEye EX - IronPort - Trend Micro Email Security -
Proofpoint - Symantec

Email security logs may include sender, recipient, subject, timestamp,
sending IP/domain, authentication results, attachment names and hashes,
URLs, verdict, delivery/quarantine/block action, and message ID.

For a phishing alert, determine whether the message was delivered, who
received it, whether a user clicked a link or opened an attachment, and
whether endpoint or identity activity followed.

## 15. Comparing the Security Solutions

  ---------------------------------------------------------------------------------------------------
  Solution       Main focus                  Detects?         Can block or act? Useful SOC evidence
  -------------- --------------------------- ---------------- ----------------- ---------------------
  IDS            Network/host intrusion      Yes              Usually           Signatures, packets,
                 indicators                                   alert-only        flows,
                                                                                source/destination

  IPS            Preventing suspicious       Yes              Yes, by           Alert,
                 activity                                     configuration     source/destination,
                                                                                action

  Firewall       Network access control      Policy/traffic   Yes               Allow/deny, IPs,
                                             events                             ports, protocol,
                                                                                bytes

  EDR            Endpoint activity and       Yes              Often supports    Process tree, files,
                 threats                                      response          user, network,
                                                                                response

  Antivirus      Malware and suspicious      Yes              Yes,              File path, hash,
                 files                                        e.g. quarantine   detection, action

  Sandbox        Behaviour of suspicious     Yes, through     Isolates          Process, file,
                 files                       analysis         execution         Registry, network
                                                                                events

  DLP            Sensitive data movement     Yes              Often yes         User, data type,
                                                                                channel, destination

  Asset          Inventory and lifecycle     Not primarily a  Supports          Owner, software,
  management                                 detection tool   management        version, criticality

  WAF            Web application traffic     Yes              Yes, by rules     URL, method, rule,
                                                                                source, action

  Load balancer  Traffic                     Health and       Routes traffic    Backend health,
                 distribution/availability   traffic                            volume, errors
                                             conditions                         

  Proxy          Client/server intermediary  Depends on       Can               User, destination,
                 traffic                     product          filter/restrict   URL, time, source

  Email security Email-borne threats         Yes              Yes,              Sender, recipient,
                                                              e.g. quarantine   URL, attachment,
                                                                                verdict
  ---------------------------------------------------------------------------------------------------

## 16. How the Products Work Together: SOC Example

Imagine an employee receives a phishing email with a malicious
attachment.

1.  **Email security:** Inspects the message and attachment; may block
    or quarantine it.
2.  **Sandbox:** Runs the suspicious attachment in isolation and
    observes behaviour.
3.  **Antivirus:** May detect a known signature or suspicious behaviour
    on the endpoint.
4.  **EDR:** Records process trees, file activity, Registry changes, and
    network connections.
5.  **Firewall:** Records or blocks network connections according to
    policy.
6.  **IDS:** Detects suspicious network patterns and generates an alert.
7.  **IPS:** May block traffic matching a prevention rule.
8.  **Proxy:** Records the user's web requests and may block a malicious
    destination.
9.  **SIEM:** Collects and correlates logs and alerts from multiple
    products.
10. **SOC analyst:** Builds a timeline, identifies affected
    users/devices, assesses impact, and follows incident-response
    procedures.
11. **DLP:** May detect or block an attempt to send sensitive
    information outside the organization.
12. **Asset management:** Provides the endpoint owner, role, software,
    and business criticality.

Not every organization has every product, and not every product sees
every stage. The value comes from combining the visibility that is
available.

## 17. How a SOC Analyst Should Read Security Logs

An alert is a starting point, not a complete conclusion. For each event,
try to establish:

-   **When:** Exact timestamp and timezone.
-   **Where:** Host, network segment, application, or cloud service.
-   **Who:** User, account, device, or service identity.
-   **What:** Process, file, URL, IP, domain, protocol, or action.
-   **How:** Detection rule, behaviour, or policy that triggered the
    event.
-   **Outcome:** Allowed, blocked, quarantined, failed, or unknown.
-   **Context:** Related events before and after the alert.

Example: An IDS alert reports suspicious outbound traffic. Firewall logs
may show whether the connection was allowed; proxy logs may identify a
user and requested destination; DNS logs may show domain resolution; EDR
may identify the process; asset inventory may show the device's business
role; SIEM events can help build a timeline.

## 18. Important Concepts and Common Misunderstandings

1.  **IDS and IPS are not identical:** IDS primarily detects and alerts;
    IPS can take configured preventive action.
2.  **A firewall is not a complete security solution:** It controls
    traffic according to policy but cannot stop every threat.
3.  **EDR is not simply antivirus:** EDR focuses on endpoint telemetry,
    detection, investigation, and response. Products may include or
    integrate AV capabilities.
4.  **A sandbox may not reveal all behaviour:** Samples can evade or
    delay execution.
5.  **DLP protects information:** It focuses on sensitive data movement
    and policy enforcement.
6.  **Asset management supports security:** Teams need to know what
    assets exist and which are exposed or vulnerable.
7.  **A WAF does not replace secure coding:** It adds a protective layer
    in front of web applications.
8.  **A load balancer is not a complete DDoS solution:** It distributes
    workload but may itself be overwhelmed.
9.  **A proxy does not guarantee anonymity:** The proxy operator may log
    traffic, and forwarding information must be handled carefully.
10. **An alert does not prove compromise:** Confirm the event's action
    and correlate it with other evidence.

## 19. Key Terms

  -----------------------------------------------------------------------
  Term                                Simple explanation
  ----------------------------------- -----------------------------------
  IDS                                 Detects suspicious activity and
                                      reports it

  NIDS                                IDS monitoring network traffic

  HIDS                                IDS monitoring a host

  PIDS                                Protocol-focused intrusion
                                      detection

  APIDS                               Application-protocol-focused
                                      intrusion detection

  IPS                                 Detects and can prevent suspicious
                                      activity

  NIPS                                Network-based intrusion prevention

  HIPS                                Host-based intrusion prevention

  WIPS                                Wireless intrusion prevention

  NBA                                 Network behaviour analysis

  Firewall                            Controls network traffic using
                                      security rules

  Stateful inspection                 Tracks the state of network
                                      connections

  DPI                                 Deep Packet Inspection

  NGFW                                Next-Generation Firewall

  UTM                                 Unified Threat Management

  EDR                                 Endpoint Detection and Response

  AV                                  Antivirus

  Signature detection                 Matching files/content against
                                      known signatures

  Heuristic detection                 Identifying suspicious
                                      characteristics or behaviour

  Sandbox                             Isolated environment for examining
                                      suspicious files

  DLP                                 Data Loss Prevention

  ITAM                                Information Technology Asset
                                      Management

  WAF                                 Web Application Firewall

  Load balancer                       Distributes traffic across backend
                                      servers

  Forward proxy                       Intermediary acting on behalf of
                                      clients

  Reverse proxy                       Intermediary acting on behalf of
                                      servers

  SIEM                                Security Information and Event
                                      Management

  DoS                                 Denial of Service

  DDoS                                Distributed Denial of Service

  C2                                  Command and Control
  -----------------------------------------------------------------------

## 20. My Learning Reflection

In this lesson, I learned that organizations need multiple security
solutions because each product has a different responsibility and
visibility.

I studied IDS and IPS and understood the difference between detecting an
event and actively preventing it. I learned how firewalls control
network traffic using rules and how EDR and antivirus provide endpoint
protection from different perspectives.

I also learned the purpose of sandboxes, DLP, asset management, WAFs,
load balancers, proxy servers, and email security solutions. Each
product contributes to a different part of the security architecture.

The most important lesson for my SOC preparation is that I must
understand the logs produced by these tools. A product name alone is not
enough. I should know what it monitors, what its alerts mean, what
action it took, and how to correlate its events with other sources.

For example, if an IDS detects suspicious traffic, I can use firewall
logs to determine whether the connection was allowed, EDR logs to
identify the responsible process, proxy logs to identify the user or
request, and asset information to understand the affected device's
importance.

My main takeaway is that effective SOC analysis depends on combining
evidence from multiple security solutions and understanding the role and
limitations of each one.

------------------------------------------------------------------------
