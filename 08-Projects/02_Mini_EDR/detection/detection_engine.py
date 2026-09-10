SUSPICIOUS_POWERSHELL_FLAGS = [
    "-enc",
    "-encodedcommand",
    "-nop",
    "-noprofile",
    "-hidden",
    "-windowstyle hidden"
]


def detect_suspicious_process(event):
    process_name = event["name"].lower()

    if process_name != "powershell.exe":
        return None

    command_line = event["cmdline"]

    if command_line:
        command_line = " ".join(command_line).lower()
    else:
        command_line = ""

    suspicious_flags = []

    for flag in SUSPICIOUS_POWERSHELL_FLAGS:
        if flag in command_line:
            suspicious_flags.append(flag)

    if suspicious_flags:
        return {
            "rule": "DET-001",
            "severity": "HIGH",
            "detection": "Suspicious PowerShell command-line activity",
            "pid": event["pid"],
            "process": event["name"],
            "timestamp": event["timestamp"],
            "indicators": suspicious_flags
        }

    return None