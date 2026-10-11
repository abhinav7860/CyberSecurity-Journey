**TryHackMe Room: Splunk -- Exploring SPL**

**Completion Date:** October 8, 2026

**Purpose**

I completed the TryHackMe room "Splunk: Exploring SPL" to improve my
understanding of Splunk Search Processing Language (SPL) and how I can
use searches to investigate security events as a SOC analyst.

**What I Worked On**

**1. Practising SPL searches**

I practised searching data in Splunk and narrowing the results using
search conditions. I worked on understanding how SPL commands fit
together in a pipeline and how each command changes the results passed
to the next command.

**2. Filtering and transforming results**

I explored commands used to organise, filter and analyse search results,
including:

-   `sort` to order results.
-   `highlight` to highlight fields in search results.
-   `top` and `rare` to identify frequently and infrequently occurring
    values.
-   `stats` to calculate statistics and aggregate events.
-   `chart` and `timechart` to visualise data and trends over time.
-   `iplocation` to add geographic information based on IP addresses.
-   `lookup` to add information from lookup data.
-   `eval` to create or calculate field values.

I practised choosing commands based on the question I wanted to answer
instead of using commands without understanding their purpose.

**3. Working with log data**

I worked with the room's log datasets, including the `windowslogs` and
`vpnlogs` indexes. I used searches to explore the available events and
fields and to understand how Splunk can help an analyst investigate
Windows and VPN-related activity.

Example search patterns I practised included:

``` spl
index=windowslogs
```

``` spl
index=vpnlogs
```

These searches depend on the indexes being available in the lab
environment. I used them as starting points to inspect the data before
refining my searches.

**4. Analysing patterns and possible anomalies**

I explored how statistical analysis can help identify activity that
differs from a normal pattern. I worked with commands and techniques
such as `eventstats`, `where` and `eval` to compare values and
investigate unusual login behaviour.

I also learned about concepts such as:

-   Comparing login activity across countries.
-   Looking for countries or login patterns that occur unusually rarely.
-   Establishing a typical login hour and comparing activity against
    that baseline.
-   Using standard deviation and a z-score to identify values that are
    far from the expected pattern.
-   Understanding why an unusual login time or location should be
    investigated rather than automatically treated as proof of an
    attack.

During the exercises, I examined an example involving the user `jsmith`
and an unusual login time around 18:30. I also recognised that an
outlier must be checked against the actual search results and
surrounding evidence before drawing a conclusion.

**5. Understanding impossible travel and anomaly detection**

I learned how an analyst can use login locations and timestamps to
identify potentially suspicious activity, including impossible-travel
scenarios. A location change that appears too fast to be physically
plausible can be a useful signal, but VPN use, proxy services, shared
infrastructure, inaccurate geolocation and incomplete logs can affect
the interpretation.

I also explored the idea of using statistical and machine-learning
techniques to detect behaviour that differs from a baseline. These
techniques support investigation; they do not independently prove
malicious activity.

**What I Learned**

By completing this room, I improved my understanding of:

-   How SPL searches are built and how commands are chained together.
-   How to filter, sort, aggregate and visualise events.
-   How to use `stats`, `eval`, `eventstats`, `where` and other commands
    for analysis.
-   How to explore Windows and VPN log data.
-   How to look for unusual patterns in login activity.
-   How statistical outliers can help prioritise investigations.
-   Why an alert or anomaly needs validation and supporting evidence
    before I classify it as malicious.

**How This Helps My SOC Learning**

This room helped me practise a core SOC skill: turning raw log data into
useful evidence. I can apply these techniques when investigating failed
logins, unusual account activity, suspicious locations and other events
that may need further analysis.

I still need regular practice writing SPL independently, validating
results and explaining why a search supports a conclusion. Completing
the room is a milestone in my learning, not a claim that I have mastered
every Splunk feature.

**My Next Steps**

-   Practise writing SPL queries without copying a walkthrough.
-   Review the fields available in Windows and authentication logs.
-   Build and test a failed-login detection.
-   Investigate suspicious PowerShell and network activity.
-   Practise creating alerts and dashboards.
-   Apply my Splunk knowledge to my SIEM-to-firewall automation project.

**Personal Reflection**

I completed the "Splunk: Exploring SPL" room on October 8, 2026. I used
the exercises to practise SPL, analyse log data and explore how
statistical techniques can help identify unusual behaviour. My next goal
is to become more confident investigating unfamiliar datasets and
explaining my findings clearly, as I would in a SOC L1 role.

