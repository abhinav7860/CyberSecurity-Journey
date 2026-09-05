# TryHackMe - Splunk: The Basics

**Name:** Abhinav  
**Date:** 05 September 2026  
**Platform:** TryHackMe  
**Room:** Splunk: The Basics

---

## What I Learned

This room introduced me to **Splunk**, a SIEM platform used to collect, search, analyze and correlate logs.

The basic flow I learned was:

```text
Log Source → Forwarder → Indexer → Search Head → SPL Search → Results
```

---

## Task 1 - Introduction

Splunk can collect and analyze logs from different sources. For a SOC analyst, it can be used to search through large amounts of security data and investigate suspicious activity.

---

## Task 3 - Splunk Components

### Forwarder

The **Forwarder** is installed on the system generating the logs. It collects the data and sends it to Splunk.

Examples include:

- Windows Event Logs
- PowerShell and Sysmon logs
- Linux logs
- Web server logs
- Database logs

### Indexer

The **Indexer** receives the data from the Forwarder. It processes, normalizes and stores the data as events so it can be searched.

### Search Head

The **Search Head** is where I search and analyze the indexed data using **SPL (Search Processing Language)**. It can also turn search results into tables and visualizations.

### Question

**Which component is used to collect and send data over the Splunk instance?**

**Answer:** `forwarder`

---

## Task 4 - Navigating Splunk

I learned about the main parts of the Splunk interface:

- Splunk Bar
- Apps Panel
- Explore Splunk
- Search & Reporting
- Dashboards

The **Search & Reporting** app is mainly used to search and analyze logs.

### Question

**In the Add Data tab, which option is used to collect data from files and ports?**

**Answer:** `monitor`

---

# Task 5 - Adding Data

For the practical part, I worked with the `VPN_logs` file.

The file was **newline-delimited JSON**, so each line represented an individual event.

### What I Did

1. Opened **Add Data** in Splunk.
2. Selected **Upload**.
3. Uploaded the `VPN_logs` file.
4. Created/selected the `VPN_Logs` index.
5. Kept the JSON source type.
6. Opened **Search & Reporting**.
7. Set the time range to **All time**.
8. Searched the logs using SPL.
9. Used `spath` when needed to extract JSON fields.
10. Used `stats count` to count matching events.

---

## SPL Queries I Used

### Count all events

```spl
index=VPN_Logs
| stats count
```

This counts all events in the `VPN_Logs` index.

### Search for Maleena

```spl
index=VPN_Logs
| spath
| search UserName="Maleena"
| stats count
```

This extracts the JSON fields, searches for Maleena and counts the matching events.

### Find the username for an IP

```spl
index=VPN_Logs
| spath
| search Source_ip="107.14.182.38"
| stats values(UserName) as UserName count
```

This searches for the IP and shows the username associated with it.

### Count events excluding France

```spl
index=VPN_Logs
| spath
| search Source_Country!="France"
| stats count
```

This counts events where the source country is not France.

### Count events from a specific IP

```spl
index=VPN_Logs
| spath
| search Source_ip="107.3.206.58"
| stats count
```

This counts VPN events associated with that IP.

---

# Answers

| Question | Answer |
|---|---:|
| Which component collects and sends data to Splunk? | `forwarder` |
| Which Add Data option collects data from files and ports? | `monitor` |
| How many events are present in the log file? | **2862** |
| How many log events are captured by Maleena? | **60** |
| Username associated with `107.14.182.38`? | **Smith** |
| Events from all countries except France? | **2814** |
| VPN events associated with `107.3.206.58`? | **14** |

---

# Important Things to Remember

### Splunk Components

```text
Forwarder
   ↓
Collects and sends logs

Indexer
   ↓
Processes and stores logs

Search Head
   ↓
Searches and analyzes logs
```

### Basic SPL

- `index=VPN_Logs` → searches inside the `VPN_Logs` index.
- `| spath` → extracts fields from JSON data.
- `| search` → filters events.
- `| stats count` → counts matching events.
- `| stats values(UserName)` → shows values of the `UserName` field.

---

# My Takeaway

This was my practical introduction to using Splunk for log investigation. The most useful part for me was actually searching the VPN logs instead of only reading about the components.

I learned the basic Splunk architecture and how to use SPL to filter logs, identify users and IPs, and count events.

For SOC work, I need to be comfortable with this because real environments can contain a huge amount of logs, and being able to search and filter them efficiently is important.
