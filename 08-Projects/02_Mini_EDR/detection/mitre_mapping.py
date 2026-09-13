# detection/mitre_mapping.py


# ============================================================
# MITRE ATT&CK Mapping
# ============================================================

MITRE_MAPPINGS = {

    "DET-001": {
        "technique_id": "T1059.001",
        "technique": "PowerShell",
        "tactic": "Execution",
        "description": (
            "Detects suspicious PowerShell "
            "command-line activity."
        )
    },

    "DET-002": {
        "technique_id": None,
        "technique": None,
        "tactic": None,
        "description": (
            "Executable or script file creation "
            "is monitored, but no ATT&CK technique "
            "is assigned by this rule alone."
        )
    },

    "NET-001": {
        "technique_id": None,
        "technique": None,
        "tactic": None,
        "description": (
            "A connection to an investigation-worthy "
            "port alone does not provide enough "
            "behavioral context for a specific "
            "ATT&CK technique."
        )
    },

    "PROC-001": {
        "technique_id": None,
        "technique": None,
        "tactic": None,
        "description": (
            "An unusual system-process location "
            "may indicate masquerading, but this "
            "rule alone does not confirm a specific "
            "ATT&CK technique."
        )
    }
}


# ============================================================
# Get MITRE Mapping
# ============================================================

def get_mitre_mapping(rule_id):
    """Return the MITRE ATT&CK mapping for a detection rule."""

    return MITRE_MAPPINGS.get(
        rule_id
    )