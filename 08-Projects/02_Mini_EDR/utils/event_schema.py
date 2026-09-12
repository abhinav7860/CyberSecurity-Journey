# utils/event_schema.py

from datetime import datetime


def create_event(
    event_type,
    source,
    details,
    severity="INFO",
    rule=None,
    detection=None
):
    """Create a standardized EDR event."""

    event = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "event_type": event_type,
        "source": source,
        "severity": severity,
        "rule": rule,
        "detection": detection,
        "details": details
    }

    return event