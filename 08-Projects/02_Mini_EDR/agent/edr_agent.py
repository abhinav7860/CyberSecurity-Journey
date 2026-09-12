# agent/edr_agent.py

import os
import sys
import json
import time
import psutil

from datetime import datetime


# ============================================================
# Add Project Root To Python Path
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


# ============================================================
# Detection Engine
# ============================================================

from detection.detection_engine import (
    detect_suspicious_process,
    detect_suspicious_file,
    detect_suspicious_network,
    detect_suspicious_process_location
)


# ============================================================
# File Monitor
# ============================================================

from monitor.file_monitor import (
    get_files,
    detect_file_changes
)


# ============================================================
# File Integrity Monitoring
# ============================================================

from monitor.file_integrity import (
    get_file_hashes,
    detect_integrity_changes
)


# ============================================================
# Network Monitor
# ============================================================

from monitor.network_monitor import (
    get_network_connections
)


# ============================================================
# Event Schema
# ============================================================

from utils.event_schema import (
    create_event
)


# ============================================================
# Configuration
# ============================================================

LOG_FILE = os.path.join(
    PROJECT_ROOT,
    "logs",
    "events.json"
)


# ============================================================
# Process Monitoring
# ============================================================

def get_process_info(process):
    """Collect information about a process."""

    try:

        return {
            "pid": process.pid,
            "name": process.name(),
            "parent_pid": process.ppid(),
            "username": process.username(),
            "exe": process.exe(),
            "cmdline": process.cmdline(),
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):

        return None


def get_processes():
    """Get a snapshot of currently running processes."""

    processes = {}

    for process in psutil.process_iter():

        info = get_process_info(
            process
        )

        if info:
            processes[info["pid"]] = info

    return processes


# ============================================================
# Logging
# ============================================================

def save_event(event):
    """Save a standardized event to the JSON log."""

    try:

        os.makedirs(
            os.path.dirname(LOG_FILE),
            exist_ok=True
        )

        existing_events = []

        if os.path.exists(LOG_FILE):

            try:

                with open(
                    LOG_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                    if isinstance(data, list):
                        existing_events = data

            except (
                json.JSONDecodeError,
                OSError
            ):

                existing_events = []

        existing_events.append(
            event
        )

        with open(
            LOG_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                existing_events,
                file,
                indent=4
            )

    except OSError as error:

        print(
            f"[LOG ERROR] {error}"
        )


# ============================================================
# Event Creation Helpers
# ============================================================

def save_process_event(event):
    """Create and save a standardized process event."""

    standardized_event = create_event(
        event_type="process_created",
        source="process_monitor",
        details={
            "pid": event.get("pid"),
            "process": event.get("name"),
            "parent_pid": event.get("parent_pid"),
            "username": event.get("username"),
            "exe": event.get("exe"),
            "cmdline": event.get("cmdline")
        }
    )

    save_event(
        standardized_event
    )


def save_file_event(event):
    """Create and save a standardized file event."""

    standardized_event = create_event(
        event_type=event.get(
            "event_type",
            "file_event"
        ),
        source="file_monitor",
        details={
            "file_name": event.get(
                "file_name"
            ),
            "path": event.get(
                "path"
            )
        }
    )

    save_event(
        standardized_event
    )


def save_fim_event(event):
    """Create and save a standardized FIM event."""

    standardized_event = create_event(
        event_type=event.get(
            "event_type",
            "file_integrity_event"
        ),
        source="file_integrity_monitor",
        details={
            "file_name": event.get(
                "file_name"
            ),
            "path": event.get(
                "path"
            ),
            "old_hash": event.get(
                "old_hash"
            ),
            "new_hash": event.get(
                "new_hash"
            )
        }
    )

    save_event(
        standardized_event
    )


def save_network_event(event):
    """Create and save a standardized network event."""

    standardized_event = create_event(
        event_type="network_connection",
        source="network_monitor",
        details={
            "pid": event.get(
                "pid"
            ),
            "process": event.get(
                "process"
            ),
            "local_ip": event.get(
                "local_ip"
            ),
            "local_port": event.get(
                "local_port"
            ),
            "remote_ip": event.get(
                "remote_ip"
            ),
            "remote_port": event.get(
                "remote_port"
            ),
            "status": event.get(
                "status"
            )
        }
    )

    save_event(
        standardized_event
    )


def save_detection_event(alert):
    """Create and save a standardized detection event."""

    details = {}

    for key, value in alert.items():

        if key not in [
            "rule",
            "severity",
            "detection"
        ]:

            details[key] = value

    standardized_event = create_event(
        event_type="detection",
        source="detection_engine",
        details=details,
        severity=alert.get(
            "severity",
            "INFO"
        ),
        rule=alert.get(
            "rule"
        ),
        detection=alert.get(
            "detection"
        )
    )

    save_event(
        standardized_event
    )


# ============================================================
# Display Functions
# ============================================================

def display_process_event(event):
    """Display a new process event."""

    print()
    print("=" * 60)
    print("                    NEW PROCESS")
    print("=" * 60)

    print(
        f"Process : {event.get('name', 'Unknown')}"
    )

    print(
        f"PID     : {event.get('pid', 'Unknown')}"
    )

    print(
        f"Parent  : {event.get('parent_pid', 'Unknown')}"
    )

    print(
        f"User    : {event.get('username', 'Unknown')}"
    )

    print(
        f"EXE     : {event.get('exe', 'Unknown')}"
    )

    print(
        f"Command : {event.get('cmdline', 'Unknown')}"
    )

    print(
        f"Time    : {event.get('timestamp', '')}"
    )

    print("=" * 60)


def display_file_event(event):
    """Display a file monitoring event."""

    print()
    print("=" * 60)
    print("                     FILE EVENT")
    print("=" * 60)

    print(
        f"Type : {event.get('event_type', 'Unknown')}"
    )

    print(
        f"File : {event.get('file_name', 'Unknown')}"
    )

    print(
        f"Path : {event.get('path', 'Unknown')}"
    )

    print(
        f"Time : {event.get('timestamp', '')}"
    )

    print("=" * 60)


def display_fim_event(event):
    """Display a file integrity event."""

    print()
    print("=" * 60)
    print("               FILE INTEGRITY EVENT")
    print("=" * 60)

    print(
        f"Type : {event.get('event_type', 'Unknown')}"
    )

    print(
        f"File : {event.get('file_name', 'Unknown')}"
    )

    print(
        f"Path : {event.get('path', 'Unknown')}"
    )

    print(
        f"Old Hash : {event.get('old_hash', 'None')}"
    )

    print(
        f"New Hash : {event.get('new_hash', 'None')}"
    )

    print("=" * 60)


def display_network_event(event):
    """Display a new network connection."""

    print()
    print("=" * 60)
    print("                  NETWORK CONNECTION")
    print("=" * 60)

    print(
        f"Process : {event.get('process', 'Unknown')}"
    )

    print(
        f"PID     : {event.get('pid', 'Unknown')}"
    )

    print(
        f"Local   : "
        f"{event.get('local_ip', '')}:"
        f"{event.get('local_port', '')}"
    )

    print(
        f"Remote  : "
        f"{event.get('remote_ip', '')}:"
        f"{event.get('remote_port', '')}"
    )

    print(
        f"Status  : {event.get('status', 'Unknown')}"
    )

    print(
        f"Time    : {event.get('timestamp', '')}"
    )

    print("=" * 60)


def display_alert(alert):
    """Display a security alert."""

    print()
    print("!" * 60)
    print("                    SECURITY ALERT")
    print("!" * 60)

    print(
        f"Rule       : "
        f"{alert.get('rule', 'Unknown')}"
    )

    print(
        f"Severity   : "
        f"{alert.get('severity', 'Unknown')}"
    )

    print(
        f"Detection  : "
        f"{alert.get('detection', 'Unknown')}"
    )

    if "pid" in alert:

        print(
            f"PID        : "
            f"{alert.get('pid')}"
        )

    if "process" in alert:

        print(
            f"Process    : "
            f"{alert.get('process')}"
        )

    if "exe" in alert:

        print(
            f"EXE        : "
            f"{alert.get('exe')}"
        )

    if "file" in alert:

        print(
            f"File       : "
            f"{alert.get('file')}"
        )

    if "path" in alert:

        print(
            f"Path       : "
            f"{alert.get('path')}"
        )

    if "remote_ip" in alert:

        print(
            f"Remote IP  : "
            f"{alert.get('remote_ip')}"
        )

    if "remote_port" in alert:

        print(
            f"Remote Port: "
            f"{alert.get('remote_port')}"
        )

    if "indicators" in alert:

        print(
            f"Indicators : "
            f"{alert.get('indicators')}"
        )

    print("!" * 60)


# ============================================================
# Network Fingerprint
# ============================================================

def get_connection_fingerprint(connection):
    """Create a unique identifier for a network connection."""

    return (
        connection.get("pid"),
        connection.get("process"),
        connection.get("local_ip"),
        connection.get("local_port"),
        connection.get("remote_ip"),
        connection.get("remote_port")
    )


# ============================================================
# Main EDR
# ============================================================

def main():

    print()
    print("=" * 60)
    print("                    MINI EDR")
    print("=" * 60)

    print(
        "[EDR] Mini EDR started"
    )

    print(
        "[EDR] Monitoring processes..."
    )

    print(
        "[EDR] Monitoring files..."
    )

    print(
        "[EDR] File Integrity Monitoring enabled"
    )

    print(
        "[EDR] Network monitoring enabled"
    )

    print("=" * 60)


    # ========================================================
    # Initial Snapshots
    # ========================================================

    previous_processes = get_processes()

    previous_files = get_files()

    baseline_hashes = get_file_hashes()

    previous_connections = (
        get_network_connections()
    )

    previous_connection_fingerprints = set()

    for connection in previous_connections:

        fingerprint = (
            get_connection_fingerprint(
                connection
            )
        )

        previous_connection_fingerprints.add(
            fingerprint
        )


    print()
    print(
        f"[FIM] Baseline created for "
        f"{len(baseline_hashes)} file(s)."
    )


    # ========================================================
    # Monitoring Loop
    # ========================================================

    try:

        while True:

            # ==================================================
            # Process Monitoring
            # ==================================================

            current_processes = get_processes()

            new_pids = (
                set(current_processes)
                - set(previous_processes)
            )

            for pid in new_pids:

                process_event = (
                    current_processes[pid]
                )

                display_process_event(
                    process_event
                )

                save_process_event(
                    process_event
                )


                # ==============================================
                # DET-001
                # Suspicious PowerShell
                # ==============================================

                alert = (
                    detect_suspicious_process(
                        process_event
                    )
                )

                if alert:

                    display_alert(
                        alert
                    )

                    save_detection_event(
                        alert
                    )


                # ==============================================
                # PROC-001
                # Suspicious Process Location
                # ==============================================

                location_alert = (
                    detect_suspicious_process_location(
                        process_event
                    )
                )

                if location_alert:

                    display_alert(
                        location_alert
                    )

                    save_detection_event(
                        location_alert
                    )


            previous_processes = (
                current_processes
            )


            # ==================================================
            # File Monitoring
            # ==================================================

            current_files = get_files()

            file_events = (
                detect_file_changes(
                    previous_files,
                    current_files
                )
            )

            for event in file_events:

                event["timestamp"] = (
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

                display_file_event(
                    event
                )

                save_file_event(
                    event
                )


                # ==============================================
                # DET-002
                # Suspicious File
                # ==============================================

                alert = (
                    detect_suspicious_file(
                        event
                    )
                )

                if alert:

                    display_alert(
                        alert
                    )

                    save_detection_event(
                        alert
                    )


            previous_files = (
                current_files
            )


            # ==================================================
            # File Integrity Monitoring
            # ==================================================

            current_hashes = (
                get_file_hashes()
            )

            integrity_events = (
                detect_integrity_changes(
                    baseline_hashes,
                    current_hashes
                )
            )

            for event in integrity_events:

                event["timestamp"] = (
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

                display_fim_event(
                    event
                )

                save_fim_event(
                    event
                )


            # Update FIM baseline
            baseline_hashes = (
                current_hashes
            )


            # ==================================================
            # Network Monitoring
            # ==================================================

            current_connections = (
                get_network_connections()
            )

            current_connection_fingerprints = set()


            for connection in current_connections:

                fingerprint = (
                    get_connection_fingerprint(
                        connection
                    )
                )

                current_connection_fingerprints.add(
                    fingerprint
                )


                # Only process genuinely new connections
                if (
                    fingerprint
                    in previous_connection_fingerprints
                ):
                    continue


                network_event = {
                    "pid": connection.get(
                        "pid"
                    ),
                    "process": connection.get(
                        "process",
                        "Unknown"
                    ),
                    "local_ip": connection.get(
                        "local_ip"
                    ),
                    "local_port": connection.get(
                        "local_port"
                    ),
                    "remote_ip": connection.get(
                        "remote_ip"
                    ),
                    "remote_port": connection.get(
                        "remote_port"
                    ),
                    "status": connection.get(
                        "status"
                    ),
                    "timestamp": (
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    )
                }


                display_network_event(
                    network_event
                )

                save_network_event(
                    network_event
                )


                # ==============================================
                # NET-001
                # Suspicious Network Connection
                # ==============================================

                alert = (
                    detect_suspicious_network(
                        network_event
                    )
                )

                if alert:

                    alert["timestamp"] = (
                        network_event["timestamp"]
                    )

                    display_alert(
                        alert
                    )

                    save_detection_event(
                        alert
                    )


            previous_connection_fingerprints = (
                current_connection_fingerprints
            )


            # ==================================================
            # Wait Before Next Scan
            # ==================================================

            time.sleep(2)


    except KeyboardInterrupt:

        print()
        print(
            "[EDR] Monitoring stopped."
        )

        print(
            "[EDR] Mini EDR shutdown complete."
        )


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()