# TryHackMe: SOC Workbooks and Lookups - Notes & Writeup
**Date:** September 3, 2026  

## Overview
This room covers the core methodologies and tools SOC analysts use during alert triage. It explains how to build context around alerts using identity lookups, asset inventories, and network diagrams, as well as how to systematically investigate threats using SOC workbooks (playbooks).

---

## Key Concepts & Summaries

### 1. Identity & Asset Inventories
Alert triage requires contextual information about the involved users and endpoints to determine if an action is authorized or suspicious.

* **Identity Inventory:** A centralized catalog of employee accounts, service accounts, roles, access levels, and locations.
  * **Sources:** On-premise Active Directory / Entra ID, Okta, Google Workspace, HR tools (BambooHR, SAP), or custom spreadsheets.
* **Asset Inventory:** A database listing all managed compute resources (servers, workstations, virtual machines) with IP mappings, OS details, assigned owners, and business functions.
  * **Sources:** Active Directory, SIEM/EDR solutions (Elastic, CrowdStrike), MDM platforms (Intune, Jamf), or custom asset tracking lists.

### 2. Network Diagrams in Investigations
Network diagrams map out physical/logical locations, subnets, open ports, and routing boundaries to help trace lateral movement and verify external connections.

* **Scenario Analysis:**
  1. External IP `103.61.240.174` connected via TCP/10443 (`vpn.tryhatme.thm`).
  2. The external connection received internal translation to `10.10.0.53` (VPN Subnet: `10.10.0.0/16`).
  3. The attacker performed reconnaissance on the Database Subnet (`172.16.15.0/24`) but was blocked.
  4. The attacker pivoted to scan the Office Subnet (`172.16.23.0/24`).

### 3. SOC Workbooks (Playbooks / Runbooks)
A SOC workbook is a standard operating procedure (SOP) guiding analysts through structured triage steps to eliminate guesswork and standardize verdicts.

* **Primary Users:** SOC L1 Analysts.
* **Core Workflow Stages:**
  1. **Enrichment:** Gather contextual data using Threat Intelligence (TI) feeds, identity catalogs, and IP reputation lookups.
  2. **Investigation:** Query SIEM logs (e.g., Splunk timeline dashboards) to verify historical user baseline activity and correlate suspicious events.
  3. **Escalation:** Hand off valid threats to L2/incident responders or verify benign activity directly with the user.

---

## Lab Answers & Solutions

### Task 3: Network Diagrams
* **Question:** According to the network diagram, which service is exposed on the TCP/10443 port?  
  **Answer:** `VPN`
* **Question:** Now, which subnet would the server behind 172.16.15.99 IP belong to?  
  **Answer:** `DATABASE SUBNET`
* **Question:** Finally, does the scenario look like a True Positive (TP) or False Positive (FP)?  
  **Answer:** `TP`

### Task 4: Workbooks Theory
* **Question:** Which SOC role would use workbooks the most (e.g. SOC Manager)?  
  **Answer:** `soc L1 analyst`
* **Question:** What is the process of gathering user, host, or IP context using TI and lookups?  
  **Answer:** `enrichment`
* **Question:** Looking at the workbook example, what platform is used as an identity inventory source?  
  **Answer:** `bambooohr`