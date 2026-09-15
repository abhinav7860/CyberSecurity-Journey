# detection/detection_engine.py


# ============================================================
# DET-001
# Suspicious PowerShell Flags
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
# DET-002
# Suspicious File Creation
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
# DET-003
# Suspicious PowerShell Command Content
# ============================================================

SUSPICIOUS_POWERSHELL_COMMANDS = [
    "invoke-expression",
    "iex",
    "invoke-webrequest",
    "downloadstring",
    "downloadfile",
    "net.webclient",
    "frombase64string",
    "start-bitstransfer"
]


# ============================================================
# NET-001
# Suspicious Network Connection
# ============================================================

SUSPICIOUS_NETWORK_PORTS = {
    21: "FTP",
    23: "Telnet",
    445: "SMB",
    3389: "RDP",
    4444: "Common test/lab port",
    5555: "Common debug/test port"
}


# ============================================================
# DET-001
# ============================================================

def detect_suspicious_process(event):
    """
    Detect suspicious PowerShell command-line activity.

    DET-001 focuses on suspicious PowerShell flags/options.
    """

    process_name = event.get(
        "name",
        ""
    ).lower()

    if process_name != "powershell.exe":
        return None

    command_line = event.get("cmdline")

    if not command_line:
        return None

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

    # Check individual flags
    for flag in SUSPICIOUS_POWERSHELL_FLAGS:

        if flag in command_parts:

            suspicious_flags.append(
                flag
            )

    # Check suspicious flag combinations
    for combination in SUSPICIOUS_POWERSHELL_COMBINATIONS:

        combination_length = len(combination)

        for index in range(
            len(command_parts)
            - combination_length
            + 1
        ):

            if (
                command_parts[
                    index:
                    index + combination_length
                ]
                == combination
            ):

                suspicious_flags.append(
                    " ".join(combination)
                )

                break

    if suspicious_flags:

        return {
            "rule": "DET-001",
            "severity": "HIGH",
            "detection":
                "Suspicious PowerShell command-line activity",
            "pid": event.get("pid"),
            "process": event.get("name"),
            "timestamp": event.get("timestamp"),
            "indicators": suspicious_flags
        }

    return None


# ============================================================
# DET-002
# ============================================================

def detect_suspicious_file(event):
    """
    Detect suspicious executable or script file creation.
    """

    event_type = event.get(
        "event_type",
        ""
    )

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
                "detection":
                    "Executable or script file created",
                "file": event.get("file_name"),
                "path": event.get("path"),
                "timestamp": event.get("timestamp"),
                "indicator": extension
            }

    return None


# ============================================================
# DET-003
# ============================================================

def detect_suspicious_powershell_content(event):
    """
    Detect suspicious PowerShell command content.

    This rule looks for command patterns that may require
    investigation. It does not determine whether the command
    is malicious by itself.
    """

    process_name = event.get(
        "name",
        ""
    ).lower()

    if process_name != "powershell.exe":
        return None

    command_line = event.get("cmdline")

    if not command_line:
        return None

    if isinstance(command_line, list):

        command_text = " ".join(
            str(part)
            for part in command_line
        ).lower()

    else:

        command_text = str(
            command_line
        ).lower()

    matched_indicators = []

    for indicator in SUSPICIOUS_POWERSHELL_COMMANDS:

        if indicator in command_text:

            matched_indicators.append(
                indicator
            )

    if not matched_indicators:
        return None

    return {
        "rule": "DET-003",
        "severity": "HIGH",
        "detection":
            "Suspicious PowerShell command content",
        "pid": event.get("pid"),
        "process": event.get("name"),
        "timestamp": event.get("timestamp"),
        "indicators": matched_indicators,
        "command_line": event.get("cmdline")
    }


# ============================================================
# NET-001
# ============================================================

def detect_suspicious_network(event):
    """
    Detect network connections that use ports
    requiring investigation.
    """

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

    if not remote_ip:
        return None

    if remote_port is None:
        return None

    if remote_port in SUSPICIOUS_NETWORK_PORTS:

        return {
            "rule": "NET-001",
            "severity": "MEDIUM",
            "detection":
                "Network connection to a port requiring investigation",
            "process": process_name,
            "pid": event.get("pid"),
            "remote_ip": remote_ip,
            "remote_port": remote_port,
            "port_service":
                SUSPICIOUS_NETWORK_PORTS[
                    remote_port
                ],
            "status": event.get("status")
        }

    return None


# ============================================================
# PROC-001
# ============================================================

def detect_suspicious_process_location(event):
    """
    Detect Windows system processes running
    from unusual locations.
    """

    process_name = event.get(
        "name",
        ""
    ).lower()

    executable = event.get(
        "exe"
    )

    if not executable:
        return None

    executable = executable.lower()

    system_processes = {
        "svchost.exe",
        "lsass.exe",
        "wininit.exe",
        "services.exe",
        "explorer.exe"
    }

    if process_name not in system_processes:
        return None

    expected_locations = [
        r"\windows\system32",
        r"\windows\syswow64"
    ]

    for location in expected_locations:

        if location in executable:
            return None

    return {
        "rule": "PROC-001",
        "severity": "HIGH",
        "detection":
            "Windows system process running from an unusual location",
        "pid": event.get("pid"),
        "process": event.get("name"),
        "exe": event.get("exe"),
        "timestamp": event.get("timestamp")
    }