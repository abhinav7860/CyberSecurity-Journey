# utils/log_analyzer.py

import os
import json
from collections import Counter


# ============================================================
# Configuration
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
    """Load events from the JSON log."""

    if not os.path.exists(LOG_FILE):
        return []

    try:

        with open(
            LOG_FILE,
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
        return []

    return []


# ============================================================
# Count Event Categories
# ============================================================

def count_event_categories(events):
    """Count events by category."""

    categories = Counter()

    for event in events:

        category = event.get(
            "event_category",
            "unknown"
        )

        categories[category] += 1

    return dict(categories)


# ============================================================
# Count Event Status
# ============================================================

def count_event_status(events):
    """Count events by status."""

    statuses = Counter()

    for event in events:

        status = event.get(
            "status",
            "UNKNOWN"
        )

        statuses[status] += 1

    return dict(statuses)


# ============================================================
# Count Severity
# ============================================================

def count_severity(events):
    """Count events by severity."""

    severities = Counter()

    for event in events:

        severity = event.get(
            "severity",
            "UNKNOWN"
        )

        severities[severity] += 1

    return dict(severities)


# ============================================================
# Count Detection Rules
# ============================================================

def count_detection_rules(events):
    """Count detections by rule."""

    rules = Counter()

    for event in events:

        if event.get(
            "event_category"
        ) != "detection":

            continue

        rule = event.get(
            "rule"
        )

        if rule:
            rules[rule] += 1

    return dict(rules)


# ============================================================
# Generate Summary
# ============================================================

def generate_summary(events):
    """Generate a summary of the EDR events."""

    return {
        "total_events": len(events),
        "event_categories": (
            count_event_categories(
                events
            )
        ),
        "event_status": (
            count_event_status(
                events
            )
        ),
        "severity": (
            count_severity(
                events
            )
        ),
        "detection_rules": (
            count_detection_rules(
                events
            )
        )
    }


# ============================================================
# Display Summary
# ============================================================

def display_summary(summary):
    """Display the event summary."""

    print()
    print("=" * 60)
    print("                  EDR LOG SUMMARY")
    print("=" * 60)

    print(
        f"Total Events : "
        f"{summary['total_events']}"
    )


    # ========================================================
    # Event Categories
    # ========================================================

    print()
    print("Event Categories:")

    for category, count in (
        summary["event_categories"].items()
    ):

        print(
            f"  {category:<15} : {count}"
        )


    # ========================================================
    # Event Status
    # ========================================================

    print()
    print("Event Status:")

    for status, count in (
        summary["event_status"].items()
    ):

        print(
            f"  {status:<15} : {count}"
        )


    # ========================================================
    # Severity
    # ========================================================

    print()
    print("Severity:")

    for severity, count in (
        summary["severity"].items()
    ):

        print(
            f"  {severity:<15} : {count}"
        )


    # ========================================================
    # Detection Rules
    # ========================================================

    print()
    print("Detection Rules:")

    if summary["detection_rules"]:

        for rule, count in (
            summary["detection_rules"].items()
        ):

            print(
                f"  {rule:<15} : {count}"
            )

    else:

        print(
            "  No detections"
        )

    print()
    print("=" * 60)


# ============================================================
# Main
# ============================================================

def main():

    events = load_events()

    if not events:

        print(
            "[LOG] No events found."
        )

        return

    summary = generate_summary(
        events
    )

    display_summary(
        summary
    )


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()