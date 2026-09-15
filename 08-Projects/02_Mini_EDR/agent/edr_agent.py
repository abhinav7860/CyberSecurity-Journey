# agent/edr_agent.py

import os
import sys
import time
import psutil
import hashlib


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORTS
# ============================================================

from monitor.file_monitor import (
    get_files,
    detect_file_changes
)

from monitor.file_integrity import (
    get_file_hashes,
    detect_integrity_changes
)

from monitor.network_monitor import (
    get_network_connections
)

from detection.detection_engine import (
    detect_suspicious_process,
    detect_suspicious_powershell_content,
    detect_suspicious_file,
    detect_suspicious_network,
    detect_suspicious_process_location
)

from detection.mitre_mapping import (
    get_mitre_mapping
)

from utils.event_schema import (
    create_event
)


# ============================================================
# LOG FILES
# ============================================================

LOG_DIRECTORY = os.path.join(
    PROJECT_ROOT,
    "logs"
)

EVENTS_FILE = os.path.join(
    LOG_DIRECTORY,
    "events.json"
)


# ============================================================
# PROCESS FINGERPRINTS
# ============================================================

previous_processes = {}


def get_process_fingerprint(process):
    """
    Create a fingerprint for a process.

    The fingerprint helps prevent the same process
    from being processed repeatedly.
    """

    try:
        pid = process.pid

        create_time = process.create_time()

        return f"{pid}-{create_time}"

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):
        return None


# ============================================================
# PROCESS MONITORING
# ============================================================

def get_processes():
    """
    Get information about currently running processes.
    """

    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "exe",
            "cmdline",
            "username"
        ]
    ):

        try:

            process_info = process.info

            processes.append({
                "pid": process_info.get("pid"),
                "name": process_info.get("name"),
                "exe": process_info.get("exe"),
                "cmdline": process_info.get("cmdline"),
                "username": process_info.get("username")
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return processes


# ============================================================
# JSON LOGGING
# ============================================================

def load_events():
    """
    Load existing EDR events from events.json.
    """

    import json

    if not os.path.exists(EVENTS_FILE):
        return []

    try:

        with open(
            EVENTS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

    except (
        json.JSONDecodeError,
        OSError
    ):
        pass

    return []


def save_event(event):
    """
    Save a standardized event to events.json.
    """

    import json

    os.makedirs(
        LOG_DIRECTORY,
        exist_ok=True
    )

    events = load_events()

    events.append(event)

    try:

        with open(
            EVENTS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                events,
                file,
                indent=4
            )

    except OSError as error:

        print(
            f"[ERROR] Could not save event: {error}"
        )


# ============================================================
# STANDARDIZED DETECTION LOGGING
# ============================================================

def save_detection_event(alert):
    """
    Create and save a standardized detection event.
    """

    evidence = {}

    for key, value in alert.items():

        if key not in [
            "rule",
            "severity",
            "detection"
        ]:

            evidence[key] = value

    rule_id = alert.get("rule")

    mitre_mapping = get_mitre_mapping(
        rule_id
    )

    mitre = None

    if mitre_mapping:

        technique_id = mitre_mapping.get(
            "technique_id"
        )

        if technique_id:

            mitre = {
                "technique_id": technique_id,
                "technique": mitre_mapping.get(
                    "technique"
                ),
                "tactic": mitre_mapping.get(
                    "tactic"
                )
            }

    details = {
        "evidence": evidence
    }

    if mitre:

        details["mitre"] = mitre

    standardized_event = create_event(
        event_type="detection",
        source="detection_engine",
        details=details,
        severity=alert.get(
            "severity",
            "INFO"
        ),
        rule=rule_id,
        detection=alert.get(
            "detection"
        )
    )

    save_event(
        standardized_event
    )


# ============================================================
# TELEMETRY EVENT
# ============================================================

def save_telemetry_event(
    event_type,
    source,
    details
):
    """
    Create and save a standardized telemetry event.
    """

    standardized_event = create_event(
        event_type=event_type,
        source=source,
        details=details
    )

    save_event(
        standardized_event
    )


# ============================================================
# PROCESS DISPLAY
# ============================================================

def display_process(process):
    """
    Display detailed process information.
    """

    print("\n" + "=" * 70)
    print("                    MINI EDR - PROCESS EVENT")
    print("=" * 70)

    print(
        f"[+] Process Name  : "
        f"{process.get('name')}"
    )

    print(
        f"[+] PID            : "
        f"{process.get('pid')}"
    )

    print(
        f"[+] Executable     : "
        f"{process.get('exe')}"
    )

    print(
        f"[+] Username       : "
        f"{process.get('username')}"
    )

    command_line = process.get(
        "cmdline"
    )

    if isinstance(command_line, list):

        command_line = " ".join(
            str(part)
            for part in command_line
        )

    print(
        f"[+] Command Line   : "
        f"{command_line}"
    )

    print("-" * 70)


# ============================================================
# FILE EVENT DISPLAY
# ============================================================

def display_file_event(event):
    """
    Display detailed file monitoring information.
    """

    print("\n" + "=" * 70)
    print("                     MINI EDR - FILE EVENT")
    print("=" * 70)

    print(
        f"[+] Event Type     : "
        f"{event.get('event_type')}"
    )

    print(
        f"[+] File Name      : "
        f"{event.get('file_name')}"
    )

    print(
        f"[+] Path           : "
        f"{event.get('path')}"
    )

    print("-" * 70)


# ============================================================
# NETWORK EVENT DISPLAY
# ============================================================

def display_network_event(event):
    """
    Display detailed network connection information.
    """

    print("\n" + "=" * 70)
    print("                  MINI EDR - NETWORK EVENT")
    print("=" * 70)

    print(
        f"[+] Process        : "
        f"{event.get('process')}"
    )

    print(
        f"[+] PID            : "
        f"{event.get('pid')}"
    )

    print(
        f"[+] Local Address  : "
        f"{event.get('local_ip')}:"
        f"{event.get('local_port')}"
    )

    print(
        f"[+] Remote Address : "
        f"{event.get('remote_ip')}:"
        f"{event.get('remote_port')}"
    )

    print(
        f"[+] Status         : "
        f"{event.get('status')}"
    )

    print("-" * 70)


# ============================================================
# DETECTION DISPLAY
# ============================================================

def display_detection(alert):
    """
    Display detailed security detection information.
    """

    print("\n" + "=" * 70)
    print("                  !!! SECURITY ALERT !!!")
    print("=" * 70)

    print(
        f"[!] Rule           : "
        f"{alert.get('rule')}"
    )

    print(
        f"[!] Severity       : "
        f"{alert.get('severity')}"
    )

    print(
        f"[!] Detection      : "
        f"{alert.get('detection')}"
    )

    print(
        f"[+] Timestamp      : "
        f"{alert.get('timestamp')}"
    )

    if alert.get("pid") is not None:

        print(
            f"[+] PID            : "
            f"{alert.get('pid')}"
        )

    if alert.get("process"):

        print(
            f"[+] Process        : "
            f"{alert.get('process')}"
        )

    if alert.get("file"):

        print(
            f"[+] File           : "
            f"{alert.get('file')}"
        )

    if alert.get("path"):

        print(
            f"[+] Path           : "
            f"{alert.get('path')}"
        )

    if alert.get("remote_ip"):

        print(
            f"[+] Remote Address : "
            f"{alert.get('remote_ip')}:"
            f"{alert.get('remote_port')}"
        )

    if alert.get("port_service"):

        print(
            f"[+] Service         : "
            f"{alert.get('port_service')}"
        )

    if alert.get("indicator"):

        print(
            f"[+] Indicator       : "
            f"{alert.get('indicator')}"
        )

    indicators = alert.get(
        "indicators"
    )

    if indicators:

        print("[+] Indicators     :")

        for indicator in indicators:

            print(
                f"    - {indicator}"
            )

    if alert.get("command_line"):

        command_line = alert.get(
            "command_line"
        )

        if isinstance(command_line, list):

            command_line = " ".join(
                str(part)
                for part in command_line
            )

        print(
            f"[+] Command Line   : "
            f"{command_line}"
        )

    print(
        "[!] ACTION         : "
        "INVESTIGATION REQUIRED"
    )

    print("=" * 70)


# ============================================================
# PROCESS DETECTION
# ============================================================

def analyze_process(process):
    """
    Run all process-related detection rules.
    """

    # --------------------------------------------------------
    # DET-001
    # Suspicious PowerShell flags
    # --------------------------------------------------------

    alert = detect_suspicious_process(
        process
    )

    if alert:

        display_detection(
            alert
        )

        save_detection_event(
            alert
        )

    # --------------------------------------------------------
    # DET-003
    # Suspicious PowerShell command content
    # --------------------------------------------------------

    alert = detect_suspicious_powershell_content(
        process
    )

    if alert:

        display_detection(
            alert
        )

        save_detection_event(
            alert
        )

    # --------------------------------------------------------
    # PROC-001
    # Suspicious system process location
    # --------------------------------------------------------

    alert = detect_suspicious_process_location(
        process
    )

    if alert:

        display_detection(
            alert
        )

        save_detection_event(
            alert
        )


# ============================================================
# FILE DETECTION
# ============================================================

def analyze_file_event(event):
    """
    Run file-related detection rules.
    """

    alert = detect_suspicious_file(
        event
    )

    if alert:

        display_detection(
            alert
        )

        save_detection_event(
            alert
        )


# ============================================================
# NETWORK DETECTION
# ============================================================

def analyze_network_event(event):
    """
    Run network-related detection rules.
    """

    alert = detect_suspicious_network(
        event
    )

    if alert:

        display_detection(
            alert
        )

        save_detection_event(
            alert
        )


# ============================================================
# FILE INTEGRITY
# ============================================================

def create_integrity_event(
    event
):
    """
    Save a file integrity event.
    """

    save_telemetry_event(
        event_type=event.get(
            "event_type"
        ),
        source="file_integrity",
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


# ============================================================
# MAIN EDR LOOP
# ============================================================

def run_edr():
    """
    Main Mini EDR monitoring loop.
    """

    global previous_processes

    print(
        "============================================"
    )

    print(
        "           MINI EDR STARTED"
    )

    print(
        "============================================"
    )

    print(
        f"[INFO] Project root: {PROJECT_ROOT}"
    )

    print(
        "[INFO] Monitoring processes..."
    )

    print(
        "[INFO] Monitoring files..."
    )

    print(
        "[INFO] Monitoring file integrity..."
    )

    print(
        "[INFO] Monitoring network connections..."
    )

    print(
        "[INFO] Detection Engine active..."
    )

    print(
        "[INFO] Press CTRL+C to stop."
    )

    print(
        "============================================"
    )


    # ========================================================
    # INITIAL PROCESS SNAPSHOT
    # ========================================================

    current_processes = {}

    for process in get_processes():

        fingerprint = (
            get_process_fingerprint(
                psutil.Process(
                    process["pid"]
                )
            )
            if process.get("pid")
            else None
        )

        if fingerprint:

            current_processes[
                fingerprint
            ] = process

    previous_processes = current_processes


    # ========================================================
    # INITIAL FILE SNAPSHOT
    # ========================================================

    previous_files = get_files()


    # ========================================================
    # INITIAL FILE INTEGRITY SNAPSHOT
    # ========================================================

    baseline_hashes = get_file_hashes()


    # ========================================================
    # INITIAL NETWORK SNAPSHOT
    # ========================================================

    previous_network = {}

    for connection in get_network_connections():

        fingerprint = (
            connection.get("pid"),
            connection.get("local_ip"),
            connection.get("local_port"),
            connection.get("remote_ip"),
            connection.get("remote_port"),
            connection.get("status")
        )

        previous_network[
            fingerprint
        ] = connection


    # ========================================================
    # MONITORING LOOP
    # ========================================================

    try:

        while True:

            # ==================================================
            # PROCESS MONITORING
            # ==================================================

            current_processes = {}

            for process in get_processes():

                pid = process.get(
                    "pid"
                )

                if not pid:
                    continue

                try:

                    psutil_process = psutil.Process(
                        pid
                    )

                    fingerprint = get_process_fingerprint(
                        psutil_process
                    )

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess
                ):

                    continue

                if not fingerprint:
                    continue

                current_processes[
                    fingerprint
                ] = process

            new_processes = (
                set(current_processes)
                - set(previous_processes)
            )

            for fingerprint in new_processes:

                process = current_processes[
                    fingerprint
                ]

                display_process(
                    process
                )

                save_telemetry_event(
                    event_type="process_created",
                    source="process_monitor",
                    details=process
                )

                # ----------------------------------------------
                # Run all process detections
                # ----------------------------------------------

                analyze_process(
                    process
                )

            previous_processes = (
                current_processes
            )


            # ==================================================
            # FILE MONITORING
            # ==================================================

            current_files = get_files()

            file_events = detect_file_changes(
                previous_files,
                current_files
            )

            for event in file_events:

                display_file_event(
                    event
                )

                save_telemetry_event(
                    event_type=event.get(
                        "event_type"
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

                analyze_file_event(
                    event
                )

            previous_files = (
                current_files
            )


            # ==================================================
            # FILE INTEGRITY MONITORING
            # ==================================================

            current_hashes = get_file_hashes()

            integrity_events = (
                detect_integrity_changes(
                    baseline_hashes,
                    current_hashes
                )
            )

            for event in integrity_events:

                print(
                    "\n" + "=" * 70
                )

                print(
                    "                MINI EDR - INTEGRITY EVENT"
                )

                print(
                    "=" * 70
                )

                print(
                    f"[+] Event Type     : "
                    f"{event.get('event_type')}"
                )

                print(
                    f"[+] File Name      : "
                    f"{event.get('file_name')}"
                )

                print(
                    f"[+] Path           : "
                    f"{event.get('path')}"
                )

                print(
                    f"[+] Old SHA-256    : "
                    f"{event.get('old_hash')}"
                )

                print(
                    f"[+] New SHA-256    : "
                    f"{event.get('new_hash')}"
                )

                print(
                    "-" * 70
                )

                create_integrity_event(
                    event
                )

            baseline_hashes = (
                current_hashes
            )


            # ==================================================
            # NETWORK MONITORING
            # ==================================================

            current_network = {}

            for connection in get_network_connections():

                fingerprint = (
                    connection.get("pid"),
                    connection.get("local_ip"),
                    connection.get("local_port"),
                    connection.get("remote_ip"),
                    connection.get("remote_port"),
                    connection.get("status")
                )

                current_network[
                    fingerprint
                ] = connection

            new_connections = (
                set(current_network)
                - set(previous_network)
            )

            for fingerprint in new_connections:

                connection = current_network[
                    fingerprint
                ]

                display_network_event(
                    connection
                )

                save_telemetry_event(
                    event_type="network_connection",
                    source="network_monitor",
                    details=connection
                )

                analyze_network_event(
                    connection
                )

            previous_network = (
                current_network
            )


            # ==================================================
            # LOOP DELAY
            # ==================================================

            time.sleep(2)


    except KeyboardInterrupt:

        print(
            "\n[INFO] Mini EDR stopped."
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_edr()