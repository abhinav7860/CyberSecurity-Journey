# utils/incident_manager.py

import os
import json


# ============================================================
# Incident Storage
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

INCIDENT_FILE = os.path.join(
    PROJECT_ROOT,
    "logs",
    "incidents.json"
)


# ============================================================
# Load Incidents
# ============================================================

def load_incidents():
    """Load incidents from the incident JSON file."""

    if not os.path.exists(
        INCIDENT_FILE
    ):
        return []

    try:

        with open(
            INCIDENT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

            if isinstance(
                data,
                list
            ):
                return data

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []

    return []


# ============================================================
# Save Incidents
# ============================================================

def save_incidents(
    incidents
):
    """Save incidents to the incident JSON file."""

    os.makedirs(
        os.path.dirname(
            INCIDENT_FILE
        ),
        exist_ok=True
    )

    with open(
        INCIDENT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            incidents,
            file,
            indent=4
        )


# ============================================================
# Check Existing Incident
# ============================================================

def is_already_incident(
    detection,
    incidents
):
    """Check whether a detection already has an incident."""

    detection_event_id = detection.get(
        "event_id"
    )

    if not detection_event_id:
        return False

    for incident in incidents:

        if incident.get(
            "detection_event_id"
        ) == detection_event_id:

            return True

    return False


# ============================================================
# Generate Incident ID
# ============================================================

def generate_incident_id(
    incidents
):
    """Generate the next incident ID."""

    number = len(
        incidents
    ) + 1

    return f"INC-{number:04d}"


# ============================================================
# Create Incident
# ============================================================

def create_incident(
    triage,
    detection,
    incidents
):
    """Create an incident from a triage record."""

    incident = {

        "incident_id": generate_incident_id(
            incidents
        ),

        "detection_event_id": detection.get(
            "event_id"
        ),

        "status": "NEW",

        "rule": triage.get(
            "rule"
        ),

        "severity": triage.get(
            "severity"
        ),

        "priority": triage.get(
            "priority"
        ),

        "detection": triage.get(
            "detection"
        ),

        "evidence": triage.get(
            "evidence"
        ),

        "related_process": triage.get(
            "related_process"
        ),

        "mitre": triage.get(
            "mitre"
        ),

        "recommended_action": triage.get(
            "recommended_action"
        )
    }

    return incident


# ============================================================
# Display Incident
# ============================================================

def display_incident(
    incident
):
    """Display an incident."""

    print()

    print(
        "=" * 60
    )

    print(
        "                  EDR INCIDENT"
    )

    print(
        "=" * 60
    )

    print()

    print(
        f"Incident ID : "
        f"{incident.get('incident_id')}"
    )

    print(
        f"Rule        : "
        f"{incident.get('rule')}"
    )

    print(
        f"Severity    : "
        f"{incident.get('severity')}"
    )

    print(
        f"Priority    : "
        f"{incident.get('priority')}"
    )

    print(
        f"Status      : "
        f"{incident.get('status')}"
    )

    print()

    print(
        f"Detection   : "
        f"{incident.get('detection')}"
    )

    print()

    evidence = incident.get(
        "evidence"
    )

    if evidence:

        print(
            "Evidence"
        )

        print(
            "-" * 60
        )

        for key, value in evidence.items():

            if key == "indicators":

                print(
                    "Indicators :"
                )

                for indicator in value:

                    print(
                        f"  - {indicator}"
                    )

            else:

                print(
                    f"{key:<11}: {value}"
                )

    print()

    process = incident.get(
        "related_process"
    )

    if process:

        details = process.get(
            "details",
            {}
        )

        print(
            "Related Process"
        )

        print(
            "-" * 60
        )

        print(
            f"Process     : "
            f"{details.get('process')}"
        )

        print(
            f"PID         : "
            f"{details.get('pid')}"
        )

    print()

    mitre = incident.get(
        "mitre"
    )

    if mitre:

        print(
            "MITRE ATT&CK"
        )

        print(
            "-" * 60
        )

        print(
            f"Technique    : "
            f"{mitre.get('technique_id')}"
        )

        print(
            f"Name         : "
            f"{mitre.get('technique')}"
        )

        print(
            f"Tactic       : "
            f"{mitre.get('tactic')}"
        )

    print()

    print(
        "Recommended Action"
    )

    print(
        "-" * 60
    )

    print(
        incident.get(
            "recommended_action"
        )
    )

    print()

    print(
        "=" * 60
    )


# ============================================================
# Main
# ============================================================

def main():

    from event_correlator import (
        load_events,
        get_detections,
        correlate_detection
    )

    events = load_events()

    if not events:

        print(
            "[INCIDENT] No events found."
        )

        return

    detections = get_detections(
        events
    )

    if not detections:

        print(
            "[INCIDENT] No detections found."
        )

        return

    incidents = load_incidents()

    new_incidents = 0

    for detection in detections:

        if is_already_incident(
            detection,
            incidents
        ):

            print(
                f"[INCIDENT] Detection "
                f"{detection.get('event_id')} "
                f"already has an incident."
            )

            continue

        investigation = correlate_detection(
            detection,
            events
        )

        triage = investigation.get(
            "triage"
        )

        incident = create_incident(
            triage,
            detection,
            incidents
        )

        incidents.append(
            incident
        )

        new_incidents += 1

        display_incident(
            incident
        )

    save_incidents(
        incidents
    )

    print()

    print(
        f"[INCIDENT] New incidents created: "
        f"{new_incidents}"
    )


# ============================================================
# Program Entry Point
# ============================================================

if __name__ == "__main__":

    main()