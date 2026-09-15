import json
import os
from collections import Counter


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

LOG_DIRECTORY = os.path.join(
    PROJECT_ROOT,
    "logs"
)

EVENTS_FILE = os.path.join(
    LOG_DIRECTORY,
    "events.json"
)

INCIDENTS_FILE = os.path.join(
    LOG_DIRECTORY,
    "incidents.json"
)


# ============================================================
# LOAD JSON
# ============================================================

def load_json_file(file_path):
    """
    Load a JSON file and return its contents.
    """

    if not os.path.exists(file_path):
        return []

    try:

        with open(
            file_path,
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


# ============================================================
# REPORT GENERATOR
# ============================================================

def generate_report():
    """
    Generate a summary report from EDR logs.
    """

    events = load_json_file(
        EVENTS_FILE
    )

    incidents = load_json_file(
        INCIDENTS_FILE
    )


    # ========================================================
    # EVENT STATISTICS
    # ========================================================

    total_events = len(events)

    detection_events = [
        event
        for event in events
        if event.get("event_type") == "detection"
    ]

    total_alerts = len(
        detection_events
    )


    severity_counts = Counter(
        event.get(
            "severity",
            "UNKNOWN"
        )
        for event in detection_events
    )


    rule_counts = Counter(
        event.get(
            "rule",
            "UNKNOWN"
        )
        for event in detection_events
    )


    event_type_counts = Counter(
        event.get(
            "event_type",
            "UNKNOWN"
        )
        for event in events
    )


    # ========================================================
    # REPORT
    # ========================================================

    print()
    print("=" * 70)
    print("                    MINI EDR REPORT")
    print("=" * 70)

    print()
    print("[+] EVENT SUMMARY")
    print("-" * 70)

    print(
        f"Total Events       : {total_events}"
    )

    print(
        f"Total Alerts       : {total_alerts}"
    )

    print(
        f"Total Incidents    : {len(incidents)}"
    )


    # ========================================================
    # SEVERITY
    # ========================================================

    print()
    print("[+] ALERT SEVERITY")
    print("-" * 70)

    if severity_counts:

        for severity, count in sorted(
            severity_counts.items()
        ):

            print(
                f"{severity:<18}: {count}"
            )

    else:

        print("No detection alerts found.")


    # ========================================================
    # DETECTION RULES
    # ========================================================

    print()
    print("[+] DETECTION RULES")
    print("-" * 70)

    if rule_counts:

        for rule, count in sorted(
            rule_counts.items()
        ):

            print(
                f"{rule:<18}: {count}"
            )

    else:

        print("No detection rules triggered.")


    # ========================================================
    # EVENT TYPES
    # ========================================================

    print()
    print("[+] EVENT TYPES")
    print("-" * 70)

    for event_type, count in sorted(
        event_type_counts.items()
    ):

        print(
            f"{event_type:<25}: {count}"
        )


    # ========================================================
    # INCIDENTS
    # ========================================================

    print()
    print("[+] INCIDENTS")
    print("-" * 70)

    if incidents:

        for incident in incidents:

            print(
                f"Incident ID       : "
                f"{incident.get('incident_id')}"
            )

            print(
                f"Rule              : "
                f"{incident.get('rule')}"
            )

            print(
                f"Severity          : "
                f"{incident.get('severity')}"
            )

            print(
                f"Priority          : "
                f"{incident.get('priority')}"
            )

            print(
                f"Status            : "
                f"{incident.get('status')}"
            )

            print(
                f"Detection         : "
                f"{incident.get('detection')}"
            )

            print("-" * 70)

    else:

        print("No incidents recorded.")


    # ========================================================
    # RECENT ALERTS
    # ========================================================

    print()
    print("[+] RECENT ALERTS")
    print("-" * 70)

    if detection_events:

        recent_alerts = detection_events[-5:]

        for alert in recent_alerts:

            print(
                f"Time      : "
                f"{alert.get('timestamp')}"
            )

            print(
                f"Rule      : "
                f"{alert.get('rule')}"
            )

            print(
                f"Severity  : "
                f"{alert.get('severity')}"
            )

            print(
                f"Detection : "
                f"{alert.get('detection')}"
            )

            print("-" * 70)

    else:

        print("No recent alerts.")


    print()
    print("=" * 70)
    print("                    END OF REPORT")
    print("=" * 70)
    print()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    generate_report()