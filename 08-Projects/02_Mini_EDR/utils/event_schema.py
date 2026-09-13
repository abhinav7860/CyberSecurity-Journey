# utils/event_schema.py

from datetime import datetime
import uuid


def get_event_category(event_type):
    """Determine the category of an EDR event."""

    if event_type == "detection":
        return "detection"

    if event_type in [
        "file_integrity_changed",
        "file_integrity_deleted"
    ]:
        return "integrity"

    return "telemetry"


def get_event_status(event_type):
    """Determine the status of an EDR event."""

    if event_type == "detection":
        return "ALERT"

    return "OBSERVED"


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
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "event_type": event_type,
        "event_category": get_event_category(
            event_type
        ),
        "status": get_event_status(
            event_type
        ),
        "source": source,
        "severity": severity,
        "rule": rule,
        "detection": detection,
        "details": details
    }

    return event