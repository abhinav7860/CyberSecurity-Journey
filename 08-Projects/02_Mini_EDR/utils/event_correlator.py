# utils/event_correlator.py

import os
import json

from alert_triage import create_triage_record


# ============================================================
# Log File
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

LOG_FILE = os.path.join(
    PROJECT_ROOT,
    "logs",
    "events.json"
)


# ============================================================
# Load Events
# ============================================================

def load_events():
    """Load events from the EDR JSON log."""

    if not os.path.exists(
        LOG_FILE
    ):
        return []

    try:

        with open(
            LOG_FILE,
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
# Find Related Process
# ============================================================

def find_related_process(
    detection,
    events
):
    """Find the process event related to a detection."""

    evidence = detection.get(
        "details",
        {}
    ).get(
        "evidence",
        {}
    )

    pid = evidence.get(
        "pid"
    )

    if pid is None:
        return None

    for event in events:

        if event.get(
            "event_type"
        ) != "process_created":

            continue

        details = event.get(
            "details",
            {}
        )

        if details.get(
            "pid"
        ) == pid:

            return event

    return None


# ============================================================
# Correlate Detection
# ============================================================

def correlate_detection(
    detection,
    events
):
    """Correlate a detection with related telemetry."""

    related_process = find_related_process(
        detection,
        events
    )

    triage = create_triage_record(
        detection,
        related_process
    )

    investigation = {

        "detection": detection,

        "related_process": related_process,

        "triage": triage
    }

    return investigation


# ============================================================
# Get Detection Events
# ============================================================

def get_detections(
    events
):
    """Return all detection events."""

    detections = []

    for event in events:

        if event.get(
            "event_category"
        ) == "detection":

            detections.append(
                event
            )

    return detections


# ============================================================
# Display Investigation
# ============================================================

def display_investigation(
    investigation
):
    """Display detection, correlation and triage information."""

    detection = investigation.get(
        "detection"
    )

    process = investigation.get(
        "related_process"
    )

    triage = investigation.get(
        "triage"
    )


    # ========================================================
    # Header
    # ========================================================

    print()

    print(
        "=" * 60
    )

    print(
        "              EDR ALERT TRIAGE"
    )

    print(
        "=" * 60
    )


    # ========================================================
    # Detection
    # ========================================================

    print()

    print(
        "Detection"
    )

    print(
        "-" * 60
    )

    print(
        f"Rule       : "
        f"{detection.get('rule')}"
    )

    print(
        f"Severity   : "
        f"{detection.get('severity')}"
    )

    print(
        f"Priority   : "
        f"{triage.get('priority')}"
    )

    print(
        f"Detection  : "
        f"{detection.get('detection')}"
    )


    # ========================================================
    # Why It Matters
    # ========================================================

    print()

    print(
        "Why This Matters"
    )

    print(
        "-" * 60
    )

    print(
        triage.get(
            "why_it_matters"
        )
    )


    # ========================================================
    # Related Process
    # ========================================================

    print()

    print(
        "Related Process"
    )

    print(
        "-" * 60
    )

    if process:

        details = process.get(
            "details",
            {}
        )

        print(
            f"Process    : "
            f"{details.get('process')}"
        )

        print(
            f"PID        : "
            f"{details.get('pid')}"
        )

        print(
            f"Parent PID : "
            f"{details.get('parent_pid')}"
        )

        print(
            f"Executable : "
            f"{details.get('exe')}"
        )

        print(
            f"Command    : "
            f"{details.get('cmdline')}"
        )

        print(
            f"Time       : "
            f"{process.get('timestamp')}"
        )

    else:

        print(
            "No related process event found."
        )


    # ========================================================
    # Evidence
    # ========================================================

    print()

    print(
        "Evidence"
    )

    print(
        "-" * 60
    )

    evidence = triage.get(
        "evidence"
    )

    if evidence:

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

    else:

        print(
            "No additional evidence."
        )


    # ========================================================
    # MITRE ATT&CK
    # ========================================================

    print()

    print(
        "MITRE ATT&CK"
    )

    print(
        "-" * 60
    )

    mitre = triage.get(
        "mitre"
    )

    if mitre:

        print(
            f"Technique  : "
            f"{mitre.get('technique_id')}"
        )

        print(
            f"Name       : "
            f"{mitre.get('technique')}"
        )

        print(
            f"Tactic     : "
            f"{mitre.get('tactic')}"
        )

    else:

        print(
            "No MITRE ATT&CK mapping."
        )


    # ========================================================
    # Recommended Action
    # ========================================================

    print()

    print(
        "Recommended Action"
    )

    print(
        "-" * 60
    )

    print(
        triage.get(
            "recommended_action"
        )
    )


    # ========================================================
    # Footer
    # ========================================================

    print()

    print(
        "=" * 60
    )


# ============================================================
# Main
# ============================================================

def main():

    events = load_events()

    if not events:

        print(
            "[INVESTIGATION] No events found."
        )

        return

    detections = get_detections(
        events
    )

    if not detections:

        print(
            "[INVESTIGATION] No detections found."
        )

        return

    for detection in detections:

        investigation = correlate_detection(
            detection,
            events
        )

        display_investigation(
            investigation
        )


# ============================================================
# Program Entry Point
# ============================================================

if __name__ == "__main__":

    main()