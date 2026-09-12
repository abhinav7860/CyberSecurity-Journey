# detection/detection_engine.py


# ============================================================
# Suspicious PowerShell Indicators
# ============================================================

SUSPICIOUS_POWERSHELL_FLAGS = [
    "-enc",
    "-encodedcommand",
    "-nop",
    "-hidden",
    "-windowstyle",
    "-executionpolicy",
    "-bypass"
]


SUSPICIOUS_POWERSHELL_COMBINATIONS = [
    ["-windowstyle", "hidden"],
    ["-executionpolicy", "bypass"]
]


# ============================================================
# Suspicious File Extensions
# ============================================================

SUSPICIOUS_FILE_EXTENSIONS = [
    ".exe",
    ".dll",
    ".scr",
    ".bat",
    ".cmd",
    ".ps1",
    ".vbs",
    ".js"
]


# ============================================================
# Process Detection
# ============================================================

def detect_suspicious_process(event):
    """Detect suspicious PowerShell command-line activity."""

    process_name = event.get(
        "name",
        ""
    ).lower()

    # Only inspect PowerShell
    if process_name != "powershell.exe":
        return None

    command_line = event.get(
        "cmdline"
    )

    if not command_line:
        return None

    # Convert command line into a list
    if isinstance(command_line, list):

        command_parts = [
            str(part).lower()
            for part in command_line
        ]

    else:

        command_parts = (
            str(command_line)
            .lower()
            .split()
        )


    suspicious_flags = []


    # ========================================================
    # Check Individual Indicators
    # ========================================================

    for flag in SUSPICIOUS_POWERSHELL_FLAGS:

        if flag in command_parts:

            suspicious_flags.append(
                flag
            )


    # ========================================================
    # Check Suspicious Combinations
    # ========================================================

    for combination in SUSPICIOUS_POWERSHELL_COMBINATIONS:

        combination_length = len(
            combination
        )

        for index in range(
            len(command_parts)
            - combination_length
            + 1
        ):

            if (
                command_parts[
                    index:index + combination_length
                ]
                == combination
            ):

                suspicious_flags.append(
                    " ".join(combination)
                )

                break


    # ========================================================
    # Generate Detection
    # ========================================================

    if suspicious_flags:

        return {
            "rule": "DET-001",
            "severity": "HIGH",
            "detection": (
                "Suspicious PowerShell "
                "command-line activity"
            ),
            "pid": event.get("pid"),
            "process": event.get("name"),
            "timestamp": event.get("timestamp"),
            "indicators": suspicious_flags
        }

    return None


# ============================================================
# File Detection
# ============================================================

def detect_suspicious_file(event):
    """Detect suspicious executable or script file creation."""

    event_type = event.get(
        "event_type",
        ""
    )

    # Only inspect newly created files
    if event_type != "file_created":
        return None

    file_name = event.get(
        "file_name",
        ""
    ).lower()

    for extension in SUSPICIOUS_FILE_EXTENSIONS:

        if file_name.endswith(extension):

            return {
                "rule": "DET-002",
                "severity": "MEDIUM",
                "detection": (
                    "Executable or script "
                    "file created"
                ),
                "file": event.get(
                    "file_name"
                ),
                "path": event.get(
                    "path"
                ),
                "timestamp": event.get(
                    "timestamp"
                ),
                "indicator": extension
            }

    return None


# ============================================================
# Network Detection
# ============================================================

def detect_suspicious_network(event):
    """Detect suspicious network activity."""

    remote_ip = event.get(
        "remote_ip"
    )

    remote_port = event.get(
        "remote_port"
    )

    process_name = event.get(
        "process",
        "Unknown"
    )

    # Ignore connections without a remote endpoint
    if not remote_ip:
        return None

    # Ports that may deserve investigation
    suspicious_ports = [
        21,      # FTP
        23,      # Telnet
        445,     # SMB
        3389,    # RDP
        4444,    # Common lab/test port
        5555     # Common Android/debug port
    ]

    if remote_port in suspicious_ports:

        return {
            "rule": "NET-001",
            "severity": "MEDIUM",
            "detection": (
                "Connection to suspicious "
                "remote port"
            ),
            "process": process_name,
            "pid": event.get(
                "pid"
            ),
            "remote_ip": remote_ip,
            "remote_port": remote_port,
            "status": event.get(
                "status"
            )
        }

    return None


# ============================================================
# Process Location Detection
# ============================================================

def detect_suspicious_process_location(event):
    """Detect Windows system processes running from unusual locations."""

    process_name = event.get(
        "name",
        ""
    ).lower()

    executable = event.get(
        "exe"
    )

    # Cannot analyze a process without
    # an executable path
    if not executable:
        return None

    executable = executable.lower()

    # Windows system processes
    system_processes = [
        "svchost.exe",
        "lsass.exe",
        "wininit.exe",
        "services.exe",
        "explorer.exe"
    ]

    # Only inspect known Windows system processes
    if process_name not in system_processes:
        return None

    # Expected Windows locations
    expected_locations = [
        r"\windows\system32",
        r"\windows\syswow64"
    ]

    for location in expected_locations:

        if location in executable:
            return None

    # Known Windows system process
    # running outside an expected location
    return {
        "rule": "PROC-001",
        "severity": "HIGH",
        "detection": (
            "Windows system process "
            "running from unusual location"
        ),
        "pid": event.get(
            "pid"
        ),
        "process": event.get(
            "name"
        ),
        "exe": event.get(
            "exe"
        ),
        "timestamp": event.get(
            "timestamp"
        )
    }