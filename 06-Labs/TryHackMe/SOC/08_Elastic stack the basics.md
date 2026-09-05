# TryHackMe - Elastic Stack: The Basics

**Date:** 05 September 2026\
**Platform:** TryHackMe\
**Room:** Elastic Stack: The Basics

## What I learned

In this room, I learned the basics of the Elastic Stack and how it can
be used for log analysis and investigations in a SOC environment.

The main idea I took from this room is that the different Elastic
components work together to collect, process, search, and visualize log
data.

## 1. Elastic Stack Components

### Elasticsearch

Elasticsearch stores and searches JSON-formatted data. It can also
analyze and correlate the data.

### Logstash

Logstash collects and processes data. It can filter/normalize logs and
send the processed data to another destination.

A Logstash configuration has three main parts:

-   **Input** → where the data comes from
-   **Filter** → processes/normalizes the data
-   **Output** → where the processed data is sent

### Beats

Beats are lightweight agents that ship data from endpoints to
Elasticsearch.

Examples: - Winlogbeat → Windows event logs - Packetbeat → network
traffic data

### Kibana

Kibana is the web interface I used to search, investigate, visualize,
and create dashboards from Elasticsearch data.

### How they work together

**Beats → Logstash → Elasticsearch → Kibana**

Beats collect data, Logstash can process it, Elasticsearch
stores/searches it, and Kibana provides the interface for investigation
and visualization.

## 2. Lab Connection

I connected to the TryHackMe Elastic lab and opened the Kibana
dashboard.

The main interface I used was **Kibana**, especially the **Discover**
section.

## 3. Discover Tab

The Discover tab is where I worked with the VPN logs.

Important things I learned:

-   **Logs:** Each row represents a log/event and contains fields and
    values.
-   **Fields Pane:** Shows fields extracted from the logs. I could use
    these fields for filtering.
-   **Index Pattern / Data View:** Tells Kibana which Elasticsearch data
    I want to explore.
-   **Search Bar:** Used to enter KQL queries.
-   **Time Filter:** Controls which time period is included in the
    results.
-   **Timeline:** Shows event counts over time and can help identify
    spikes.
-   **Add Filter:** Allows filters to be applied without manually
    writing the whole query.

For this lab, the data view was:

``` text
vpn_connections
```

I made sure the time picker included **January 2022** before doing the
investigations.

## 4. KQL - Kibana Query Language

KQL is the query language I used in Kibana to search the logs.

### Free-text search

Example:

``` text
"United States"
```

I also learned about wildcards:

``` text
United*
```

The wildcard can match additional text after the specified term.

### Logical operators

**AND** --- both conditions must match:

``` text
"United States" AND "Virginia"
```

**OR** --- either condition can match:

``` text
"United States" OR "England"
```

**NOT** --- excludes a condition:

``` text
"United States" AND NOT ("Florida")
```

### Field-based search

Instead of searching the whole document, I can search specific fields:

``` text
Source_ip : 238.163.231.224 AND UserName : Suleman
```

This searches for logs where the source IP and username match the given
values.

## 5. Practical Investigation

I used the `vpn_connections` data to investigate VPN activity.

### United States + James/Albert

I searched for logs where the country was United States and the user was
James or Albert.

Query:

``` text
"United States" AND UserName :"James" OR UserName :"Albert"
```

Result:

**161 records**

### Johny Brown

I investigated VPN activity after Johny Brown was terminated on 1
January 2022.

Result:

**1 VPN connection**

## 6. Creating Visualizations

I used Kibana's visualization features to make the log data easier to
understand.

I worked with fields such as:

-   `Source_Country`
-   `Source_ip`
-   `UserName`

I created visualizations including tables and charts and learned how
fields can be combined to show useful relationships in the data.

### Failed VPN attempts

For failed connections, I filtered using:

``` text
action : "failed"
```

I then used `UserName` and `Source_ip` as useful fields.

The user with the highest number of failed attempts was:

**Simon**

Number of failed attempts:

**274**

## 7. Creating a Dashboard

I created a dashboard to bring the saved visualizations together.

Steps I followed:

1.  Open **Dashboard**.
2.  Create a new dashboard.
3.  Select **Add from Library**.
4.  Add the saved visualizations/searches.
5.  Arrange them.
6.  Save the dashboard.

I successfully created the dashboard containing the available
visualizations.

## 8. Important Results

  Investigation                                     Result
  ------------------------------------------------- -----------------
  United States + James/Albert                      **161 records**
  VPN connections after Johny Brown's termination   **1**
  User with most failed attempts                    **Simon**
  Failed VPN attempts in January                    **274**

## 9. What I should remember

-   **Elasticsearch** → stores and searches the data.
-   **Logstash** → collects/processes/normalizes data.
-   **Beats** → lightweight agents that ship data.
-   **Kibana** → interface for searching, investigating, visualizing,
    and dashboards.
-   **Discover** → main place I used for log investigation.
-   **KQL** → used to search/filter Elasticsearch data in Kibana.
-   Always check the **time range** before investigating logs.
-   Fields such as `Source_ip`, `Source_Country`, `UserName`, and
    `action` are useful during investigations.
-   Visualizations and dashboards make large amounts of log data easier
    to understand.

## 10. My Takeaway

This room helped me understand Elastic from a SOC analyst's point of
view. I don't need to know every internal detail of Elasticsearch or
Logstash right now. For me, the important part is understanding how to
use Kibana to search logs, apply filters, investigate events, create
visualizations, and build dashboards.

The workflow I want to remember is:

``` text
Collect data
    ↓
Process / normalize data
    ↓
Store and search data
    ↓
Investigate in Kibana
    ↓
Visualize findings
    ↓
Create dashboards
```
