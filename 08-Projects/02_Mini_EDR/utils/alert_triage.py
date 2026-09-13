# utils/alert_triage.py


# ============================================================
# Alert Triage
# ============================================================

def determine_priority(severity):
    """Determine investigation priority from alert severity."""

    severity = str(
        severity
    ).upper()

    if severity == "HIGH":
        return "HIGH"

    if severity == "MEDIUM":
        return "MEDIUM"

    return "LOW"


# ============================================================
# Detection Explanation
# ============================================================

def explain_detection(detection):
    """Explain why a detection may require investigation."""

    rule = detection.get(
        "rule"
    )

    explanations = {

        "DET-001": (
            "PowerShell was executed with "
            "suspicious command-line indicators. "
            "This behavior may require investigation."
        ),

        "DET-002": (
            "An executable or script file was created "
            "inside the monitored area. "
            "The file should be reviewed."
        ),

        "NET-001": (
            "A process established a connection to "
            "a port that requires investigation."
        ),

        "PROC-001": (
            "A Windows system process was found running "
            "from an unusual executable location."
        )
    }

    return explanations.get(
        rule,
        "The detection requires further investigation."
    )


# ============================================================
# Recommended Analyst Action
# ============================================================

def get_recommended_action(detection):
    """Provide a basic analyst recommendation."""

    rule = detection.get(
        "rule"
    )

    recommendations = {

        "DET-001": (
            "Review the PowerShell command and "
            "its parent process."
        ),

        "DET-002": (
            "Review the newly created file and "
            "verify whether its creation was expected."
        ),

        "NET-001": (
            "Review the destination, process, and "
            "connection context."
        ),

        "PROC-001": (
            "Verify the executable path and determine "
            "whether the process location is legitimate."
        )
    }

    return recommendations.get(
        rule,
        "Review the available evidence and determine "
        "whether further investigation is required."
    )


# ============================================================
# Create Triage Record
# ============================================================

def create_triage_record(
    detection,
    related_process=None
):
    """Create a structured triage record."""

    severity = detection.get(
        "severity",
        "INFO"
    )

    evidence = detection.get(
        "details",
        {}
    ).get(
        "evidence",
        {}
    )

    mitre = detection.get(
        "details",
        {}
    ).get(
        "mitre"
    )

    return {

        "rule": detection.get(
            "rule"
        ),

        "severity": severity,

        "priority": determine_priority(
            severity
        ),

        "detection": detection.get(
            "detection"
        ),

        "why_it_matters": explain_detection(
            detection
        ),

        "evidence": evidence,

        "related_process": related_process,

        "mitre": mitre,

        "recommended_action": get_recommended_action(
            detection
        )
    }