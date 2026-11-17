# Introduction to Splunk

**LetsDefend study notes \| 17 November 2026**

## 1. What is Splunk?

Splunk is a platform for collecting, indexing, searching, analysing,
monitoring, and visualizing machine-generated data. In cybersecurity, it
is widely used as a Security Information and Event Management (SIEM)
platform.

Organizations generate logs from Windows and Linux systems, firewalls,
routers, IDS/IPS, EDR, antivirus, DNS, web servers, cloud services, and
identity providers. Splunk brings this information into a searchable
platform so analysts can investigate activity across different systems.

### Why SOC teams use Splunk

-   Centralize logs from different systems.
-   Search events using timestamps, users, hosts, IP addresses, and
    other fields.
-   Identify unusual patterns and correlate activity.
-   Create reports, scheduled searches, alerts, and dashboards.
-   Support incident investigation, monitoring, and documentation.

**Important:** Splunk does not automatically know that an event is
malicious. It stores and processes data. Detection logic and analyst
investigation give the events security meaning.

### Basic SIEM workflow

1.  **Generate:** A system creates an event.
2.  **Collect:** A forwarder or another input method collects it.
3.  **Ingest and index:** Splunk processes and stores the event.
4.  **Search:** An analyst uses Search Processing Language (SPL).
5.  **Detect:** A saved search or detection identifies a condition.
6.  **Investigate:** The analyst reviews related evidence.
7.  **Respond:** The SOC follows its incident-response process.

## 2. Main Splunk components

### Splunk Enterprise

The core platform installed on a server or computer. In a small lab, one
installation can receive data, index it, run searches, and provide
Splunk Web.

### Universal Forwarder (UF)

A lightweight agent installed on an endpoint. It monitors configured
data sources and forwards selected events to a Splunk receiving
endpoint.

Example: A Windows computer creates Security Event Log records →
Universal Forwarder collects selected records → sends them to Splunk →
Splunk indexes them → an analyst searches them.

### Indexer

Receives incoming data, processes it, and stores indexed events.
Analysts search the indexed data.

### Search Head

Provides the search environment and user interface for running searches
and presenting reports, alerts, and dashboards. In a single-instance
lab, the same Splunk Enterprise server may perform both search-head and
indexer functions.

### Deployment Server

Centrally distributes configuration files and apps to groups of
forwarders. It is a management component, not the destination for event
data simply because it manages forwarders.

Remember: - **Indexer/receiving endpoint:** receives event data. -
**Deployment server:** distributes forwarder configuration.

A small lab does not necessarily need a separate deployment server.

## 3. Planning, sizing, requirements, and ports

### Sizing

Splunk sizing depends on: - Data ingestion volume per day. - Number of
endpoints and data sources. - Number of concurrent users and searches. -
Search complexity and frequency. - Data retention period. -
Single-instance versus distributed architecture. - CPU, RAM, storage
capacity, and disk performance.

The lesson links to the [Splunk Sizing
calculator](https://splunk-sizing.soclib.net/). A lab configuration
should not be assumed to be suitable for production.

### System requirements

The lesson references [Splunk Enterprise 9.0.1 system
requirements](https://docs.splunk.com/Documentation/Splunk/9.0.1/Installation/Systemrequirements).
Requirements are version-specific. For a current installation, check the
documentation for the exact Splunk release and operating system.

### Common ports in the lesson

  -----------------------------------------------------------------------
  Port                                Common purpose
  ----------------------------------- -----------------------------------
  TCP 9997                            Forwarder-to-indexer data receiving
                                      (when configured)

  TCP 8000                            Splunk Web interface in the
                                      lesson's configuration

  TCP 8089                            Splunk management/REST interface;
                                      also used for management
                                      communication
  -----------------------------------------------------------------------

These are common defaults, not guarantees. Ports can be changed. The
receiving port must be enabled on the receiving Splunk instance before a
forwarder can send data.

Restrict Splunk Web and management access to trusted networks. Do not
expose management interfaces unnecessarily.

The lesson also references a [Splunk common network ports
chart](http://downloads.jordan2000.com/splunk/Splunk-Common-Network-Ports-v2.0.3.png).

### Licensing

The lesson says that after 60 days an installation can be converted to a
perpetual free license. Licensing terms, limits, and features can
change. Check current Splunk licensing documentation before relying on a
trial period or a particular feature set.

## 4. Installing Splunk Enterprise on Windows

The lesson demonstrates installation on a Windows Server 2022 virtual
machine.

1.  Open the [Splunk Enterprise download
    page](https://www.splunk.com/en_us/download/splunk-enterprise.html?locale=en_us).
2.  Create or sign in to a Splunk account.
3.  Download the Windows MSI installer.
4.  Launch the installer.
5.  Read the license agreement and understand the terms.
6.  Accept it only if you agree.
7.  Choose **Customize Options** to review installation settings.
8.  Select the installation directory.
9.  Choose the account under which Splunk will run. The lesson uses
    Local System.
10. Configure the requested credentials.
11. Start installation and wait for it to complete.
12. Open the Splunk Web interface at the lesson's example address:
    `https://127.0.0.1:8000`.

A local installation may use a certificate that the browser does not
already trust. A certificate warning does not by itself mean the
installation failed. Confirm that the service is running and that you
are connecting to the expected local instance.

### Verify the Windows service

1.  Press `Windows + R`.
2.  Run `services.msc`.
3.  Find the Splunk service (the lesson calls it **Splunkd Service**).
4.  Confirm that it is running.
5.  Review its startup type.

`splunkd` is the main Splunk service/daemon. If it is stopped, the
instance may not receive data or provide searches normally. Exact
service display names and startup settings can vary by version and
installation choices.

## 5. Installing Splunk Enterprise on Linux

The lesson demonstrates Ubuntu 22.04 Desktop and provides GUI and CLI
methods.

### GUI installation using DEB

1.  Visit the Splunk download page and sign in.
2.  Download the Linux `.deb` package.
3.  Open the Downloads folder.
4.  Right-click the package and choose **Open with Other Applications**.
5.  Select **Software Install**.
6.  Click **Install** and wait.

A DEB package is intended for Debian-based distributions such as Ubuntu.
Confirm that the package architecture and OS are supported.

### CLI installation using TGZ

1.  Download the Linux TGZ package.
2.  Use the download page's **Command Linux Wget** option to obtain the
    correct download command.
3.  Open a terminal.
4.  Move to the installation directory; the lesson uses `/opt`.
5.  Download the package, using `sudo` if required.
6.  Extract it with suitable permissions.
7.  Start Splunk and accept the license.
8.  Answer the setup prompts and create the requested credentials.
9.  Open the address displayed by the installer.

The lesson's example extraction command is:

`tar xvzf splunk-9.0.1-82c987350fde-Linux-x86_64.tgz`

Its example start command is:

`/opt/splunk/bin/splunk start --accept-license`

The archive filename is from an older release. Use the exact filename
you downloaded rather than copying an old version string.

### Enable startup at boot

The lesson says that a TGZ installation does not automatically configure
startup at boot. Its example command is:

`sudo /opt/splunk/bin/splunk enable boot-start`

Follow the instructions printed by your installed Splunk version and use
the permissions required by your installation.

### Check status

`/opt/splunk/bin/splunk status`

Other basic commands:

  Command                            Purpose
  ---------------------------------- ----------------
  `/opt/splunk/bin/splunk start`     Start Splunk
  `/opt/splunk/bin/splunk stop`      Stop Splunk
  `/opt/splunk/bin/splunk restart`   Restart Splunk
  `/opt/splunk/bin/splunk status`    Check status

## 6. Installing the Windows Universal Forwarder

The lesson's goal is to collect Windows logs and send them to Splunk
Enterprise.

### Download and verify

1.  Open the [Universal Forwarder download
    page](https://www.splunk.com/en_us/download/universal-forwarder.html).
2.  Sign in if required and download the Windows installer.
3.  Review the license terms.
4.  Obtain the checksum published for that exact installer.
5.  Calculate the local checksum and compare it.

The lesson demonstrates this PowerShell command:

`Get-FileHash .\splunkforwarder-9.0.0.1-9e907cedecb1-x64-release.msi -Algorithm md5`

The lesson's historical example MD5 is
`83a09c64537832701320609e665e3e7`. Do not use that value for a different
installer. Use the checksum supplied for the exact file you downloaded;
prefer a stronger published checksum such as SHA-256 when available. A
matching checksum helps detect corruption or alteration, but does not by
itself prove the download source is trustworthy.

### Install and configure

1.  Launch the installer.
2.  Read and accept the license if you agree.
3.  Select **An on-premises Splunk Enterprise instance** for this lab.
4.  Review the default configuration.
5.  Configure the account used to run the forwarder.
6.  Enter the receiving indexer's IP address or hostname.
7.  Enter the receiving port; the lesson uses `9997`.
8.  Complete the installation.

In production, a dedicated service account may be used, with only the
permissions needed to collect the configured data sources.

### Why enter the indexer address?

The forwarder needs to know where to send its events. The deployment
server is a separate management component that distributes
configuration. Since the lesson does not configure a deployment server,
it enters the receiving indexer's address.

### Verify the forwarder service

1.  Open `services.msc`.
2.  Find **SplunkForwarder Service**.
3.  Confirm that it is running.

### Test network connectivity

The lesson uses:

`Test-NetConnection -ComputerName Splunk_IP -Port 9997`

Replace `Splunk_IP` with the actual server address. A successful TCP
test only shows that a connection to that port could be established. It
does not prove that the forwarder is monitoring the intended logs, that
events are indexed, or that they are routed to the correct index.

### Check forwarder management

On the Splunk server, open **Settings → Forwarder management**. The
endpoint should appear after it connects and reports as expected.

If it does not appear: - Check that the forwarder service is running. -
Verify the receiving address and port. - Verify network connectivity and
firewall rules. - Confirm that receiving is enabled on Splunk. - Review
forwarder and Splunk internal logs. - Allow time for the forwarder to
connect.

Forwarder visibility and successful event ingestion are separate checks.
A connected forwarder may not yet be collecting the intended source.

## 7. Enable receiving on Splunk

The receiving Splunk instance must listen on the port configured in the
forwarder.

The lesson's workflow: 1. Open Splunk Web. 2. Go to **Settings →
Forwarding and receiving**. 3. Open the receiving configuration. 4.
Choose to add a receiving port. 5. Enter `9997`. 6. Save. 7. Wait for
the forwarder to connect and send events. 8. Check the index and search
for incoming events.

The receiving port is often called the Splunk-to-Splunk (S2S) receiving
port.

### Why might an index show no events?

Possible causes: - No input or data source is configured. - The
forwarder is stopped. - The receiving port is not enabled. - A firewall
blocks the connection. - The forwarder points to the wrong server or
port. - Events are routed to a different index. - The source
configuration has not been applied.

An empty index does not automatically mean the index is broken.
Troubleshoot each stage of the data path.

## 8. Add data to Splunk

The lesson demonstrates two methods: collecting from a forwarder and
uploading a log file.

### Add data from a forwarder

1.  Go to **Settings → Add Data**.
2.  Select **Forward**.
3.  Select the endpoint/forwarder.
4.  Assign a server class name if requested by the workflow.
5.  Select the data source to monitor.
6.  Choose the Windows Event Log channel(s) required.
7.  Select the destination index.
8.  Create an index if required; the lesson uses `WinLog_clients`.
9.  Review the configuration and submit.
10. Start searching and confirm events arrive.

### Important data concepts

**Index:** A logical storage location for indexed events. Indexes help
organize data and can support access controls and retention policies.

**Host:** Identifies the system associated with an event, depending on
input configuration.

**Source:** Identifies the origin/input of the data, often a file path
or data-source identifier.

**Sourcetype:** Describes the type/format of incoming data and helps
Splunk interpret it and extract fields.

The exact values depend on input configuration, add-ons, and field
extractions. Inspect real events instead of assuming every data source
uses identical field names.

### Upload a log file

1.  Go to **Settings → Add Data**.
2.  Select **Upload**.
3.  Choose the log file.
4.  Review the data preview.
5.  Check event breaking and timestamp recognition where relevant.
6.  Set a host value if needed.
7.  Select the destination index.
8.  Complete the upload and search the events.

### Forwarder versus upload

  -----------------------------------------------------------------------
  Forwarder                           Upload
  ----------------------------------- -----------------------------------
  Collects from a configured          Imports a selected file
  endpoint/source                     

  Can continuously monitor data       Usually imports a particular file
                                      or batch

  Useful for ongoing endpoint         Useful for labs and offline sample
  telemetry                           logs

  Requires forwarder and receiver     Requires access to the file and
  configuration                       upload permissions
  -----------------------------------------------------------------------

## 9. Searching in Splunk

Splunk Search Processing Language (SPL) is used to retrieve, filter,
transform, aggregate, and analyse indexed data.

### Time range

The lesson introduces: - **Presets:** Today, last week, last year, last
24 hours, etc. - **Relative:** Periods such as a number of minutes or
weeks ago. - **Real-time:** Events as they arrive, depending on search
configuration. - **Date range:** Between selected dates. - **Date and
time range:** Specific start and end dates/times.

Always check the time range before deciding that an event does not
exist. A search limited to the last 15 minutes will not show an event
from yesterday.

Real-time searches can consume resources. Use them when the detection
requirement justifies them.

### Timeline

The timeline visualizes the distribution of events across the selected
time range. It can help reveal: - A sudden spike. - Repeated activity. -
A burst of failed logons. - Activity before or after a suspicious event.

A spike does not explain its own cause. Inspect the underlying events.

### Search modes

The lesson introduces three modes: - **Fast:** Prioritizes search
performance and may omit some field discovery or event-related
processing. - **Smart:** Balances performance and field discovery
depending on the search context. - **Verbose:** Performs more detailed
field discovery and processing, potentially using more resources.

The lesson recommends Smart Mode for typical use. Behaviour can vary by
version and search features.

### Search bar: syntax and examples

The lesson highlights: - Field names are case-sensitive. - Field values
are generally not case-sensitive in ordinary field-value matching. - `*`
is a wildcard. - `AND`, `OR`, and `NOT` combine conditions. - Search
History helps retrieve previous searches.

Use actual field names from your events.

**Username begins with Je:**

`Username=Je*`

This may match values such as Jeanne or Jean if the field is actually
named `Username`.

**Successful logons on computer1:**

`EventID=4624 AND ComputerName=computer1`

**Successful logons excluding the domain controller:**

`EventID=4624 NOT ComputerName=domaincontroller`

These are lesson examples. Confirm the exact field names and values in
your own data.

### Fields panel

The Fields panel shows fields available in the search results. Examples
may include `host`, `source`, `sourcetype`, `user`, `src_ip`, `dest_ip`,
`EventCode`, and `ComputerName`.

The exact fields depend on the data source, sourcetype, add-ons, and
extraction configuration. Selecting a field can show its values and help
narrow an investigation.

**SOC tip:** Inspect raw events before relying on a field. It may be
absent, named differently, or extracted incorrectly.

## 10. Windows Event IDs used in the lesson

  -----------------------------------------------------------------------
  Event ID                Common meaning          SOC relevance
  ----------------------- ----------------------- -----------------------
  4624                    Successful logon        Investigate account
                                                  access and logon
                                                  patterns

  4625                    Failed logon            Investigate incorrect
                                                  credentials, brute
                                                  force, password
                                                  spraying, or user error
  -----------------------------------------------------------------------

### Event ID 4624

A 4624 event records a successful Windows logon. It does not
automatically prove the activity was legitimate. Review the account,
logon type, source workstation/IP if available, target computer,
timestamp, authentication package, and related activity.

### Event ID 4625

A 4625 event records a failed logon. A single failure may be a typo or
an outdated saved password. Repeated failures may indicate brute force,
password spraying, a misconfigured service, or a user entering the wrong
password.

Look for patterns and context instead of classifying every failure as an
attack.

### Failed-logon search from the lesson

The lesson uses:

`source="WinEventLog:*" index="winlog_clients" EventCode=4625 AND Nom_du_compte=Admin`

It notes that the account field may instead be `accountname`.

This is a lesson-specific example. Your data may use fields such as
`Account_Name`, `TargetUserName`, or another extracted field. Inspect
the events and use the exact field names present.

An illustrative partial-match search might be:

`index="WinLog_clients" EventCode=4625 accountname=*admin*`

Confirm the real index and field names before using it.

## 11. Reports

A report is a saved search that can be run when needed or scheduled.

Examples: - Daily failed-logon summary. - Weekly firewall deny
activity. - VPN login report. - Endpoints with repeated authentication
failures.

### Create a report

1.  Run the failed-logon search.
2.  Select **Save As → Report**.
3.  Enter a clear title and description.
4.  Save.
5.  Open/view the report.

A useful title explains its purpose, such as
`Daily Failed Logons - Admin Accounts`.

### Edit or delete a report

Open the Search app's Reports section, find the report, open it, and use
the Edit option. Before deleting a shared report, check whether other
analysts or dashboards depend on it.

### Schedule a report

The lesson schedules the failed-logon report every day at 08:00 to
review the previous day.

1.  Open the saved report.
2.  Select **Edit Schedule**.
3.  Enable **Schedule Report**.
4.  Configure the frequency and time.
5.  Ensure the search time range covers the previous day.
6.  Review available trigger actions.
7.  Save.

**Important:** Scheduling a report for 08:00 does not automatically make
it search yesterday's events. Configure the search time range and
schedule consistently. Consider the Splunk server's time zone and the
SOC's reporting time zone.

### Trigger actions

The lesson mentions actions such as sending an email or launching a
script after report generation. Available actions depend on
configuration, permissions, and installed apps. Do not enable scripts or
external actions without understanding and testing their effects.

## 12. Alerts

An alert is based on a saved search and is configured to trigger when a
defined condition is met.

For example, an alert might trigger when more than 35 failed logons are
found during a specified time window.

### Alert configuration considerations

1.  **Search:** Which events should be examined?
2.  **Schedule or real-time mode:** When should it run?
3.  **Trigger condition:** What result should cause it to fire?
4.  **Trigger actions:** What should happen?
5.  **Throttling/suppression:** Should repeated matching results be
    grouped or temporarily suppressed?
6.  **Permissions:** Who can manage the alert?

Exact options depend on the Splunk version and alert type.

### Threshold example

A detection could search for Event ID 4625, group by account or source,
count failures, and trigger when the count exceeds a threshold.

A threshold alone does not prove brute force. Tune it to normal activity
and consider the source, number of targeted accounts, time window, and
behaviour.

### Scheduled versus real-time alerts

  -----------------------------------------------------------------------
  Scheduled                           Real-time
  ----------------------------------- -----------------------------------
  Runs at defined intervals           Evaluates incoming events
                                      continuously or near-continuously,
                                      depending on configuration

  Useful for periodic checks          Useful when low detection latency
                                      is needed

  Can detect activity after the       Can consume more system resources
  scheduled run                       

  Often easier to control at scale    Requires careful design to avoid
                                      excess load and alert noise
  -----------------------------------------------------------------------

The lesson warns that real-time searches can overload a Splunk server.

**An alert is not incident confirmation.** It means a configured
condition was met. Review the events, identify the account/host/source,
check for successful logons after failures, correlate other logs, and
determine whether the activity is benign, suspicious, or malicious.

## 13. Dashboards

A dashboard is a visual page containing panels. Panels can show search
results, tables, charts, and metrics.

Dashboards help analysts monitor important information without manually
running every search.

### Create the SOC L1 dashboard

The lesson reuses the failed-logon search:

1.  Run the search.
2.  Select **Save As** and choose the dashboard option.
3.  Create a new dashboard named `SOC L1`.
4.  Add the search as a panel.
5.  Configure sharing so the intended SOC users can access it.
6.  Save and open the dashboard.

### Example SOC L1 panels

-   Failed logons over time.
-   Successful logons over time.
-   Accounts with the most failed logons.
-   Source hosts/IPs generating failures.
-   Events by Windows endpoint.
-   High-volume authentication activity.
-   Recent security alerts.

Each panel should answer a clear operational question. Avoid adding
panels merely for appearance.

### Sharing and permissions

Users who only need to view a dashboard should not automatically receive
edit permissions. Restrict access to sensitive operational data and
allow changes only to appropriate users.

## 14. User and role management

Splunk user management controls who can access the platform and what
actions they can perform.

### Roles

The lesson points to **Settings → Roles**.

A role can define permissions such as: - Which Splunk features a user
can access. - Which administrative actions they can perform. - Which
indexes/events they can search. - Whether they can create or manage
reports, alerts, and dashboards. - Whether they can change platform
settings.

Different SOC members need different permissions. An L1 analyst may need
search and alert-review access; a Splunk administrator may need platform
configuration privileges.

Apply the principle of **least privilege**: give each user only the
access required for their responsibilities.

### Users

The lesson points to **Settings → Users** and notes that a new
installation initially provides an administrator account.

The lesson recommends creating another administrator account and
reserving the original `admin` account for emergencies. Treat this as
the lesson's recommendation; follow current Splunk guidance and the
organization's identity and access-management policy.

Good practices: - Use individual accounts rather than shared analyst
accounts. - Avoid routine work with highly privileged accounts. - Assign
roles based on job responsibilities. - Remove access when it is no
longer needed. - Review privileged access periodically. - Monitor
administrative logins and configuration changes.

### Password management

The lesson points to **Settings → Password Management** and states that
the installation asks for a password with an eight-character minimum.
Exact requirements depend on Splunk version and authentication
configuration.

Use long, unique passwords or an approved enterprise authentication
method. Do not reuse passwords. Protect credentials, use multi-factor
authentication where supported and required, and restrict administrative
access. Meeting a setup wizard's minimum length is not necessarily
sufficient security.

## 15. Practical SOC investigation: repeated failed logons

Imagine a Windows endpoint generates repeated Event ID 4625 records.

1.  **Identify:** Search for Event ID 4625.
2.  **Time:** Confirm when the failures began and the selected time
    range.
3.  **Account:** Determine whether one account or many accounts are
    targeted.
4.  **Source:** Review source host, IP, workstation, and target computer
    fields.
5.  **Successful access:** Search for Event ID 4624 involving the same
    account and relevant source/host after the failures.
6.  **Correlate:** Review VPN, domain controller, EDR, firewall, and
    identity-provider logs where available.
7.  **Assess:** Consider whether the pattern is consistent with user
    error, a misconfigured service, brute force, or password spraying.
8.  **Document:** Record what happened, when, affected account/host,
    source, event pattern, evidence, related activity, assessment, and
    actions.

A successful logon after failures can increase concern, but it still
needs context; it could be the legitimate user finally entering the
correct password.

## 16. Troubleshooting: no data arriving

### Endpoint / forwarder

-   Is the SplunkForwarder service running?
-   Is the correct receiving address configured?
-   Is the receiving port correct?
-   Is the intended Windows Event Log channel configured?
-   Does the forwarder have permission to read the source?
-   Are there errors in forwarder internal logs?

### Network

-   Can the endpoint reach the Splunk server?
-   Is TCP 9997 allowed through firewalls?
-   Is the destination address correct?
-   Is routing working?
-   Is the receiving server listening on the expected port?

Test with:

`Test-NetConnection -ComputerName Splunk_IP -Port 9997`

### Receiver

-   Is Splunk Enterprise running?
-   Is receiving enabled on the intended port?
-   Does the port match the forwarder's destination?
-   Are there errors in Splunk internal logs?

### Index and search

-   Is the index name correct?
-   Is data being routed to another index?
-   Is the time range appropriate?
-   Are the field names correct?
-   Are host/source filters excluding events?
-   Has enough time passed for events to arrive and be indexed?

**Troubleshooting principle:** A successful TCP test does not prove
successful ingestion. A visible forwarder does not prove the desired
input is configured. An existing index does not prove that data is being
sent to it. Verify each stage separately.

## 17. Key terms glossary

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  Splunk Enterprise                   Platform for ingesting, indexing,
                                      searching, and analysing machine
                                      data

  SIEM                                Security Information and Event
                                      Management

  Universal Forwarder                 Lightweight endpoint agent that
                                      collects and forwards data

  Indexer                             Component that processes and stores
                                      indexed events

  Search Head                         Component/interface for running
                                      searches and presenting results

  Deployment Server                   Distributes configuration and apps
                                      to forwarders

  `splunkd`                           Main Splunk service/daemon

  Index                               Logical storage location for
                                      indexed events

  Host                                Field identifying the system
                                      associated with an event

  Source                              Field identifying the data
                                      origin/input

  Sourcetype                          Classification describing the event
                                      format/type

  SPL                                 Search Processing Language

  Report                              Saved search that can be run or
                                      scheduled

  Alert                               Saved search configured to trigger
                                      on a condition

  Dashboard                           Collection of panels showing
                                      results and visualizations

  Event ID 4624                       Windows successful-logon event

  Event ID 4625                       Windows failed-logon event

  Receiving port                      Port on which Splunk accepts
                                      forwarded data
  -----------------------------------------------------------------------

## 18. Key takeaways

1.  Splunk is a data platform; it does not automatically decide whether
    every event is malicious.
2.  A Universal Forwarder collects and forwards data; the receiving
    instance must be configured to accept it.
3.  The indexer receives/stores data; the deployment server distributes
    forwarder configurations.
4.  TCP 9997 is a common receiving port, but it must be enabled and can
    be changed.
5.  TCP 8000 is commonly used for Splunk Web; TCP 8089 is commonly used
    for management.
6.  A successful network test does not prove events are indexed.
7.  An index can exist without receiving events.
8.  Always check the time range before deciding an event is missing.
9.  Use field names that actually exist in your data.
10. Event ID 4625 is a failed logon, not automatic proof of brute force.
11. A report is a saved search; an alert triggers on a condition; a
    dashboard visualizes information.
12. Real-time searches should be designed carefully to avoid unnecessary
    resource consumption.
13. Use roles and least privilege to manage access.
14. Protect administrator credentials and restrict access to management
    interfaces.
15. Old package names, checksums, licensing terms, and version-specific
    settings may not apply to a current release.

## 19. My learning reflection

In this lesson, I learned how Splunk is installed and how data travels
from an endpoint into a central SIEM platform. Installing Splunk
Enterprise alone is not enough to monitor a Windows computer. I also
need a Universal Forwarder, a correctly configured receiving port, and
an input configuration that tells the forwarder which logs to collect.

I understood the difference between an indexer and a deployment server.
The indexer receives and stores event data, while the deployment server
distributes configurations to forwarders. I also learned how to check
the forwarder service, test connectivity to port 9997, enable receiving,
create an index, and verify incoming events.

The search section introduced time ranges, fields, wildcards, Boolean
operators, and Windows Event IDs 4624 and 4625. I also learned how to
save searches as reports, schedule reports, create alerts, and build
dashboards for SOC monitoring.

Finally, I learned that Splunk access must be managed through users and
roles. A SOC analyst should have the permissions required for
investigation without automatically receiving administrator privileges.

My main takeaway is that a SIEM is useful only when the right data is
collected, correctly indexed, searchable, and interpreted in context. An
alert or event is evidence to investigate, not automatic proof of an
attack.

## 20. Suggested GitHub location and practice

Suggested path:

`CyberSecurity-Journey/LetsDefend/Splunk/01-Introduction-to-Splunk.md`

Suggested practical exercises: 1. Verify Splunk Enterprise is running.
2. Verify the Universal Forwarder service is running. 3. Confirm that
the forwarder can reach the receiving port. 4. Confirm that receiving is
enabled. 5. Ingest Windows Security Event Logs into a dedicated index.
6. Search for Event IDs 4624 and 4625. 7. Inspect raw events and
identify the actual field names. 8. Create a saved report for failed
logons. 9. Schedule the report to run daily. 10. Create an alert with a
carefully selected threshold. 11. Build a small SOC L1 dashboard with
authentication panels. 12. Review users, roles, and permissions.

Practice only on systems and logs you own or are authorized to monitor.
Keep Splunk Web and management interfaces restricted to trusted lab or
administrative networks.
