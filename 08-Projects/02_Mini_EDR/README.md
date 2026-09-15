# 🛡️ Mini EDR — Endpoint Detection & Response

A lightweight Endpoint Detection and Response (EDR) system built with Python for learning and practicing endpoint security monitoring, detection engineering, alert triage, incident handling, and SOC workflows.

The project collects endpoint telemetry from a Windows system, analyzes the activity using detection rules, generates structured security events, correlates alerts with process information, performs basic triage, creates incidents, and presents the collected data through a web dashboard.

> **Project Focus:** Defensive Security / SOC / Endpoint Monitoring  
> **Environment:** Windows  
> **Purpose:** Educational and controlled lab environment

---

## 📌 Overview

Traditional endpoint security solutions can be complex enterprise systems. This project was created to understand the fundamental concepts behind an EDR by building a smaller system from the ground up.

The Mini EDR focuses on the following workflow:

```text
Endpoint Activity
       │
       ▼
Telemetry Collection
       │
       ▼
Detection Engine
       │
       ▼
Security Alert
       │
       ▼
Event Logging
       │
       ▼
Alert Correlation
       │
       ▼
Alert Triage
       │
       ▼
Incident Management
       │
       ▼
Reporting & Dashboard
```

The goal was not to create a production-grade EDR, but to understand how endpoint telemetry can be transformed into actionable security information.

---

# 🎯 Objectives

- Monitor running processes
- Monitor file activity
- Monitor file integrity
- Monitor network connections
- Detect suspicious endpoint activity
- Generate structured security events
- Map applicable detections to MITRE ATT&CK
- Analyze collected events
- Correlate alerts with process information
- Perform basic alert triage
- Create and manage security incidents
- Generate security reports
- Visualize endpoint activity through a dashboard
- Test the complete EDR workflow

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      Windows        │
                         │      Endpoint       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      EDR Agent      │
                         └──────────┬──────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │ Process        │ │ File           │ │ Network        │
        │ Monitoring     │ │ Monitoring     │ │ Monitoring     │
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │  Detection Engine   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Event Schema      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     JSON Logs       │
                         └──────────┬──────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │ Correlation    │ │ Alert Triage   │ │   Reporting    │
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │ Incident Management │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Dashboard      │
                         └─────────────────────┘
```

---

# 🔍 Features

## 1. Process Monitoring

The EDR monitors newly observed processes and collects:

- Process name
- Process ID (PID)
- Parent PID
- Executable path
- Username
- Command line

---

## 2. File Monitoring

The file monitor watches the configured `monitored_files` directory and detects:

- File creation
- File modification
- File deletion

---

## 3. File Integrity Monitoring

The EDR uses SHA-256 hashing to establish and compare file integrity.

It can identify:

- File content modification
- File deletion

---

## 4. Network Monitoring

The network monitor collects:

- Process
- PID
- Local IP
- Local port
- Remote IP
- Remote port
- Connection status

Network activity is treated as telemetry unless it matches an existing detection rule.

---

# 🚨 Detection Engine

The detection engine contains a small set of focused detection rules.

## DET-001 — Suspicious PowerShell Command-Line Activity

Detects suspicious PowerShell command-line indicators such as:

```text
-enc
-encodedcommand
-nop
-hidden
-windowstyle
-windowstyle hidden
-executionpolicy
-executionpolicy bypass
```

**Severity:** HIGH

### MITRE ATT&CK

```text
Technique : T1059.001
Name      : PowerShell
Tactic    : Execution
```

---

## DET-002 — Executable or Script File Created

Detects creation of files with executable or script-related extensions:

```text
.exe
.dll
.scr
.bat
.cmd
.ps1
.vbs
.js
```

**Severity:** MEDIUM

---

## DET-003 — Suspicious PowerShell Command Content

Detects suspicious PowerShell command content including:

```text
Invoke-Expression
IEX
Invoke-WebRequest
DownloadString
DownloadFile
Net.WebClient
FromBase64String
Start-BitsTransfer
```

**Severity:** HIGH

---

## NET-001 — Investigation-Worthy Network Port

Detects connections involving selected ports that may require investigation:

| Port | Service / Description |
|------|----------------------|
| 21 | FTP |
| 23 | Telnet |
| 445 | SMB |
| 3389 | RDP |
| 4444 | Common test/lab port |
| 5555 | Common debug/test port |

**Severity:** MEDIUM

> A connection to one of these ports is treated as an investigation indicator, not automatic proof of malicious activity.

---

## PROC-001 — Unusual System Process Location

Checks selected Windows system processes and identifies cases where they appear to execute from an unexpected location.

**Severity:** HIGH

---

# 📊 Event Schema

Events are stored using a consistent JSON structure.

Example:

```json
{
    "event_id": "unique-event-id",
    "timestamp": "2026-09-15 22:07:19",
    "event_type": "detection",
    "event_category": "detection",
    "status": "ALERT",
    "source": "detection_engine",
    "severity": "HIGH",
    "rule": "DET-001",
    "detection": "Suspicious PowerShell command-line activity",
    "details": {}
}
```

Important fields include:

| Field | Purpose |
|------|---------|
| `event_id` | Unique identifier |
| `timestamp` | Event time |
| `event_type` | Type of event |
| `event_category` | Telemetry, detection, or integrity |
| `status` | Current event status |
| `source` | Component that generated the event |
| `severity` | Event severity |
| `rule` | Detection rule |
| `detection` | Detection description |
| `details` | Event-specific information |

---

# 📝 Logging

Events are stored in:

```text
logs/events.json
```

Security incidents are stored in:

```text
logs/incidents.json
```

JSON keeps the logging system lightweight and easy to inspect, analyze, and consume through the dashboard API.

---

# 🧠 Alert Correlation

When a security detection is generated, the correlation component attempts to associate the detection with relevant process telemetry.

This provides additional investigation context such as:

- Process name
- PID
- Parent PID
- Executable path
- Command line
- Timestamp

---

# 🔎 Alert Triage

The triage component converts a detection into basic investigation information.

It provides:

- Detection
- Severity
- Priority
- Related process
- Evidence
- MITRE ATT&CK information
- Recommended investigation action

Example:

```text
Review the PowerShell command and its parent process.
```

---

# 🚨 Incident Management

Security detections can be converted into incidents.

Each incident receives a unique identifier such as:

```text
INC-0001
INC-0002
```

An incident contains:

- Incident ID
- Detection rule
- Severity
- Priority
- Status
- Detection description
- Evidence
- Related process
- MITRE ATT&CK information
- Recommended action

The incident manager also performs basic deduplication so the same detection event does not repeatedly create the same incident.

---

# 📈 Reporting

The reporting component summarizes the collected EDR data.

It includes:

- Total events
- Total alerts
- Total incidents
- Alert severity
- Detection rule statistics
- Event type statistics
- Incident information
- Recent alerts

Generate a report with:

```powershell
python utils\report_generator.py
```

---

# 🖥️ Dashboard

The project includes a React-based security monitoring dashboard.

### Overview

- Total events
- Total alerts
- High severity alerts
- Incident count
- System status

### Security Monitoring

- Recent alerts
- Incidents
- Recent event activity
- MITRE ATT&CK information

### Analytics

- Severity Distribution
- Events by Type
- Events Over Time
- Detection Rules
- Top Processes

### Event Investigation

- Event filtering
- Event searching
- Expandable event details
- Detection information

The dashboard receives data from the Python API.

---

# 🔌 API

A lightweight Python HTTP API provides the dashboard with EDR data.

Available endpoints:

```text
/api/events
/api/incidents
/api/status
```

Start the API:

```powershell
python api\server.py
```

The API runs locally on:

```text
http://localhost:8000
```

---

# 🧪 Testing

The detection engine includes automated tests using `pytest`.

Latest test result:

```text
14 passed in 0.02s
```

Run the tests:

```powershell
pytest
```

---

# 🔬 End-to-End Testing

The complete EDR workflow was tested using controlled PowerShell activity.

A PowerShell process was executed with:

```text
-WindowStyle Hidden
```

The EDR successfully detected the activity using:

```text
DET-001
```

The alert was classified as:

```text
Severity : HIGH
```

The detection was then processed through:

```text
PowerShell Activity
        ↓
Process Monitoring
        ↓
DET-001 Detection
        ↓
Security Event
        ↓
Event Correlation
        ↓
Alert Triage
        ↓
Incident Management
        ↓
INC-0002
        ↓
Security Report
        ↓
Dashboard
```

During the final end-to-end test:

```text
Total Events       : 253
Total Alerts       : 2
Total Incidents    : 2
HIGH Alerts        : 2
DET-001            : 2
```

This confirmed that the major components of the Mini EDR work together as an integrated workflow.

---

# 📁 Project Structure

```text
02_Mini_EDR/
│
├── agent/
│   └── edr_agent.py
│
├── api/
│   └── server.py
│
├── detection/
│   ├── detection_engine.py
│   └── mitre_mapping.py
│
├── logs/
│   ├── events.json
│   └── incidents.json
│
├── monitor/
│   ├── file_monitor.py
│   ├── file_integrity.py
│   └── network_monitor.py
│
├── monitored_files/
│
├── tests/
│   └── test_detection_engine.py
│
├── utils/
│   ├── event_schema.py
│   ├── log_analyzer.py
│   ├── event_correlator.py
│   ├── alert_triage.py
│   ├── incident_manager.py
│   └── report_generator.py
│
├── dashboard/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── venv/
├── pytest.ini
└── README.md
```

---

# ⚙️ Installation

## Requirements

- Windows
- Python 3.x
- Node.js and npm
- Git

## Python Environment

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the required Python packages used by the project:

```powershell
pip install psutil pytest
```

---

# ▶️ Usage

## Start the EDR Agent

From the project root:

```powershell
.\venv\Scripts\Activate.ps1
python agent\edr_agent.py
```

Press `CTRL+C` to stop the agent.

## Analyze Logs

```powershell
python utils\log_analyzer.py
```

## Correlate Alerts

```powershell
python utils\event_correlator.py
```

## Create Incidents

```powershell
python utils\incident_manager.py
```

## Generate Report

```powershell
python utils\report_generator.py
```

## Run Tests

```powershell
pytest
```

## Start API

```powershell
python api\server.py
```

## Start Dashboard

Open another terminal:

```powershell
cd dashboard
npm install
npm run dev
```

---

# 🛠️ Technologies

| Technology | Purpose |
|------------|---------|
| Python | EDR agent and security processing |
| psutil | Process and network monitoring |
| JSON | Event and incident storage |
| React | Dashboard |
| Vite | Frontend development |
| Recharts | Security analytics |
| REST API | Dashboard data access |
| PowerShell | Controlled detection testing |
| pytest | Automated testing |
| MITRE ATT&CK | Detection classification |

---

# 📚 Learning Outcomes

Building this project provided practical experience with:

- Endpoint telemetry collection
- Windows process monitoring
- File monitoring
- File integrity monitoring
- Network monitoring
- Detection engineering
- Security event schemas
- JSON-based logging
- MITRE ATT&CK mapping
- Alert correlation
- SOC alert triage
- Incident management
- Security reporting
- Security dashboards
- REST APIs
- Automated testing
- End-to-end security workflows

The main learning outcome was understanding how raw endpoint activity can be transformed into a structured SOC investigation workflow.

---

# 🚧 Current Limitations

This is an educational Mini EDR and is **not intended to replace a production EDR platform**.

Current limitations include:

- Local JSON-based storage
- Limited detection rules
- No centralized log infrastructure
- No authentication for the local API
- No distributed endpoint management
- No cloud deployment
- No advanced behavioral analytics
- Limited incident-response automation

These limitations are intentional to keep the project focused on understanding EDR and SOC fundamentals.

---

# 🔐 Security & Ethical Use

This project is intended for:

- Educational purposes
- Defensive security research
- SOC learning
- Controlled laboratory environments
- Personal cybersecurity experimentation

All detection testing should be performed on systems and environments where you have authorization.

---

# 📌 Project Status

| Component | Status |
|-----------|--------|
| Process Monitoring | ✅ Complete |
| File Monitoring | ✅ Complete |
| File Integrity Monitoring | ✅ Complete |
| Network Monitoring | ✅ Complete |
| Detection Engine | ✅ Complete |
| Event Schema | ✅ Complete |
| JSON Logging | ✅ Complete |
| MITRE ATT&CK Mapping | ✅ Complete |
| Log Analyzer | ✅ Complete |
| Automated Tests | ✅ Complete |
| Event Correlation | ✅ Complete |
| Alert Triage | ✅ Complete |
| Incident Management | ✅ Complete |
| Dashboard | ✅ Complete |
| Detection Improvements | ✅ Complete |
| Reporting | ✅ Complete |
| End-to-End Testing | ✅ Complete |
| Documentation | ✅ Complete |
| GitHub Cleanup | ⏳ Next |

---

# 👨‍💻 Author

**Abhinav Sabu**

B.Tech Computer Science & Engineering

Interested in:

- SOC Operations
- Blue Team Security
- Detection Engineering
- Incident Response
- Cybersecurity

---

## ⭐ Project Purpose

This project was built as part of my practical cybersecurity learning journey to gain hands-on experience with endpoint monitoring and SOC workflows.

The focus throughout development was on understanding **how detections are generated, investigated, correlated, and converted into actionable security incidents**, rather than simply building a collection of security tools.
