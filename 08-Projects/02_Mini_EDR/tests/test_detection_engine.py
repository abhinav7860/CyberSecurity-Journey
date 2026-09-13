# tests/test_detection_engine.py

from detection.detection_engine import (
    detect_suspicious_process,
    detect_suspicious_file,
    detect_suspicious_network,
    detect_suspicious_process_location
)


# ============================================================
# DET-001 — PowerShell Detection
# ============================================================

def test_powershell_encoded_command():

    event = {
        "pid": 1234,
        "name": "powershell.exe",
        "cmdline": [
            "powershell.exe",
            "-enc",
            "ABC123"
        ],
        "timestamp": "2026-09-13 21:00:00"
    }

    result = detect_suspicious_process(
        event
    )

    assert result is not None
    assert result["rule"] == "DET-001"


def test_powershell_noprofile_is_not_alerted():

    event = {
        "pid": 1234,
        "name": "powershell.exe",
        "cmdline": [
            "powershell.exe",
            "-noprofile"
        ],
        "timestamp": "2026-09-13 21:00:00"
    }

    result = detect_suspicious_process(
        event
    )

    assert result is None


def test_powershell_hidden_window():

    event = {
        "pid": 1234,
        "name": "powershell.exe",
        "cmdline": [
            "powershell.exe",
            "-windowstyle",
            "hidden"
        ],
        "timestamp": "2026-09-13 21:00:00"
    }

    result = detect_suspicious_process(
        event
    )

    assert result is not None
    assert result["rule"] == "DET-001"


# ============================================================
# DET-002 — File Detection
# ============================================================

def test_executable_file_creation():

    event = {
        "event_type": "file_created",
        "file_name": "test.exe",
        "path": "C:\\Temp\\test.exe",
        "timestamp": "2026-09-13 21:00:00"
    }

    result = detect_suspicious_file(
        event
    )

    assert result is not None
    assert result["rule"] == "DET-002"


def test_normal_text_file_creation():

    event = {
        "event_type": "file_created",
        "file_name": "notes.txt",
        "path": "C:\\Temp\\notes.txt",
        "timestamp": "2026-09-13 21:00:00"
    }

    result = detect_suspicious_file(
        event
    )

    assert result is None


def test_executable_modification_is_not_file_creation():

    event = {
        "event_type": "file_modified",
        "file_name": "test.exe",
        "path": "C:\\Temp\\test.exe",
        "timestamp": "2026-09-13 21:00:00"
    }

    result = detect_suspicious_file(
        event
    )

    assert result is None


# ============================================================
# NET-001 — Network Detection
# ============================================================

def test_suspicious_network_port():

    event = {
        "pid": 1234,
        "process": "test.exe",
        "remote_ip": "192.168.1.10",
        "remote_port": 4444,
        "status": "ESTABLISHED"
    }

    result = detect_suspicious_network(
        event
    )

    assert result is not None
    assert result["rule"] == "NET-001"


def test_normal_https_connection():

    event = {
        "pid": 1234,
        "process": "chrome.exe",
        "remote_ip": "142.250.1.1",
        "remote_port": 443,
        "status": "ESTABLISHED"
    }

    result = detect_suspicious_network(
        event
    )

    assert result is None


# ============================================================
# PROC-001 — Process Location Detection
# ============================================================

def test_system_process_normal_location():

    event = {
        "pid": 1234,
        "name": "svchost.exe",
        "exe": "C:\\Windows\\System32\\svchost.exe",
        "timestamp": "2026-09-13 21:00:00"
    }

    result = detect_suspicious_process_location(
        event
    )

    assert result is None


def test_system_process_unusual_location():

    event = {
        "pid": 1234,
        "name": "svchost.exe",
        "exe": "C:\\Temp\\svchost.exe",
        "timestamp": "2026-09-13 21:00:00"
    }

    result = detect_suspicious_process_location(
        event
    )

    assert result is not None
    assert result["rule"] == "PROC-001"


def test_normal_application_is_ignored():

    event = {
        "pid": 1234,
        "name": "chrome.exe",
        "exe": (
            "C:\\Program Files\\Google\\"
            "Chrome\\Application\\chrome.exe"
        ),
        "timestamp": "2026-09-13 21:00:00"
    }

    result = detect_suspicious_process_location(
        event
    )

    assert result is None