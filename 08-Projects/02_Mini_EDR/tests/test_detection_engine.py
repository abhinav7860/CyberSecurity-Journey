# tests/test_detection_engine.py

from detection.detection_engine import (
    detect_suspicious_process,
    detect_suspicious_file,
    detect_suspicious_powershell_content,
    detect_suspicious_network,
    detect_suspicious_process_location,
)


# ============================================================
# DET-001 TESTS
# Suspicious PowerShell Flags
# ============================================================

def test_detect_encoded_powershell():

    event = {
        "name": "powershell.exe",
        "cmdline": [
            "powershell.exe",
            "-EncodedCommand",
            "TEST"
        ],
        "pid": 1000,
        "timestamp": "2026-09-15 10:00:00"
    }

    result = detect_suspicious_process(event)

    assert result is not None
    assert result["rule"] == "DET-001"
    assert result["severity"] == "HIGH"


def test_detect_hidden_powershell():

    event = {
        "name": "powershell.exe",
        "cmdline": [
            "powershell.exe",
            "-WindowStyle",
            "Hidden"
        ],
        "pid": 1001,
        "timestamp": "2026-09-15 10:01:00"
    }

    result = detect_suspicious_process(event)

    assert result is not None
    assert result["rule"] == "DET-001"


def test_normal_powershell():

    event = {
        "name": "powershell.exe",
        "cmdline": [
            "powershell.exe",
            "-Command",
            "Get-Process"
        ],
        "pid": 1002,
        "timestamp": "2026-09-15 10:02:00"
    }

    result = detect_suspicious_process(event)

    assert result is None


# ============================================================
# DET-002 TESTS
# Suspicious File Creation
# ============================================================

def test_detect_executable_creation():

    event = {
        "event_type": "file_created",
        "file_name": "test.exe",
        "path": "monitored_files/test.exe",
        "timestamp": "2026-09-15 10:03:00"
    }

    result = detect_suspicious_file(event)

    assert result is not None
    assert result["rule"] == "DET-002"
    assert result["severity"] == "MEDIUM"


def test_normal_text_file():

    event = {
        "event_type": "file_created",
        "file_name": "normal.txt",
        "path": "monitored_files/normal.txt",
        "timestamp": "2026-09-15 10:04:00"
    }

    result = detect_suspicious_file(event)

    assert result is None


# ============================================================
# DET-003 TESTS
# Suspicious PowerShell Command Content
# ============================================================

def test_detect_invoke_expression():

    event = {
        "name": "powershell.exe",
        "cmdline": [
            "powershell.exe",
            "-Command",
            "Invoke-Expression",
            "Get-Process"
        ],
        "pid": 2000,
        "timestamp": "2026-09-15 10:05:00"
    }

    result = detect_suspicious_powershell_content(
        event
    )

    assert result is not None
    assert result["rule"] == "DET-003"
    assert result["severity"] == "HIGH"
    assert "invoke-expression" in result["indicators"]


def test_detect_download_string():

    event = {
        "name": "powershell.exe",
        "cmdline": [
            "powershell.exe",
            "-Command",
            "DownloadString"
        ],
        "pid": 2001,
        "timestamp": "2026-09-15 10:06:00"
    }

    result = detect_suspicious_powershell_content(
        event
    )

    assert result is not None
    assert result["rule"] == "DET-003"
    assert "downloadstring" in result["indicators"]


def test_detect_base64_conversion():

    event = {
        "name": "powershell.exe",
        "cmdline": [
            "powershell.exe",
            "-Command",
            "FromBase64String"
        ],
        "pid": 2002,
        "timestamp": "2026-09-15 10:07:00"
    }

    result = detect_suspicious_powershell_content(
        event
    )

    assert result is not None
    assert result["rule"] == "DET-003"
    assert "frombase64string" in result["indicators"]


def test_normal_powershell_content():

    event = {
        "name": "powershell.exe",
        "cmdline": [
            "powershell.exe",
            "-Command",
            "Get-Process"
        ],
        "pid": 2003,
        "timestamp": "2026-09-15 10:08:00"
    }

    result = detect_suspicious_powershell_content(
        event
    )

    assert result is None


def test_non_powershell_process():

    event = {
        "name": "cmd.exe",
        "cmdline": [
            "cmd.exe",
            "Invoke-Expression"
        ],
        "pid": 2004,
        "timestamp": "2026-09-15 10:09:00"
    }

    result = detect_suspicious_powershell_content(
        event
    )

    assert result is None


# ============================================================
# NET-001 TESTS
# Suspicious Network Connection
# ============================================================

def test_detect_suspicious_network_port():

    event = {
        "remote_ip": "127.0.0.1",
        "remote_port": 4444,
        "process": "test.exe",
        "pid": 3000,
        "status": "ESTABLISHED"
    }

    result = detect_suspicious_network(event)

    assert result is not None
    assert result["rule"] == "NET-001"
    assert result["severity"] == "MEDIUM"


def test_normal_https_connection():

    event = {
        "remote_ip": "127.0.0.1",
        "remote_port": 443,
        "process": "chrome.exe",
        "pid": 3001,
        "status": "ESTABLISHED"
    }

    result = detect_suspicious_network(event)

    assert result is None


# ============================================================
# PROC-001 TESTS
# Unusual System Process Location
# ============================================================

def test_detect_unusual_system_process_location():

    event = {
        "name": "svchost.exe",
        "exe": "C:\\Users\\Test\\Downloads\\svchost.exe",
        "pid": 4000,
        "timestamp": "2026-09-15 10:10:00"
    }

    result = detect_suspicious_process_location(
        event
    )

    assert result is not None
    assert result["rule"] == "PROC-001"
    assert result["severity"] == "HIGH"


def test_normal_system_process_location():

    event = {
        "name": "svchost.exe",
        "exe": "C:\\Windows\\System32\\svchost.exe",
        "pid": 4001,
        "timestamp": "2026-09-15 10:11:00"
    }

    result = detect_suspicious_process_location(
        event
    )

    assert result is None