import psutil
import time
import json
import os
import sys
from datetime import datetime


# Add project root to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from detection.detection_engine import detect_suspicious_process


LOG_FILE = "logs/events.json"


def get_process_info(process):
    """Collect information about a process."""

    try:
        return {
            "pid": process.pid,
            "name": process.name(),
            "parent_pid": process.ppid(),
            "username": process.username(),
            "exe": process.exe(),
            "cmdline": process.cmdline(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):
        return None


def get_processes():
    """Get a snapshot of currently running processes."""

    processes = {}

    for process in psutil.process_iter():

        info = get_process_info(process)

        if info:
            processes[info["pid"]] = info

    return processes


def save_event(event):
    """Save process event to JSON."""

    os.makedirs("logs", exist_ok=True)

    events = []

    if os.path.exists(LOG_FILE):

        try:
            with open(LOG_FILE, "r") as file:
                events = json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            events = []

    events.append(event)

    with open(LOG_FILE, "w") as file:
        json.dump(events, file, indent=4)


def display_process_event(process):
    """Display information about a newly created process."""

    print("\n[PROCESS CREATED]")

    print(f"Time       : {process['timestamp']}")
    print(f"PID        : {process['pid']}")
    print(f"Process    : {process['name']}")
    print(f"Parent PID : {process['parent_pid']}")
    print(f"User       : {process['username']}")
    print(f"Path       : {process['exe']}")
    print(f"Command    : {process['cmdline']}")


def display_alert(alert):
    """Display security alert."""

    print("\n🚨 SECURITY ALERT")

    print(f"Rule       : {alert['rule']}")
    print(f"Severity   : {alert['severity']}")
    print(f"Detection  : {alert['detection']}")
    print(f"Process    : {alert['process']}")
    print(f"PID        : {alert['pid']}")
    print(f"Time       : {alert['timestamp']}")

    if "indicators" in alert:
        print(
            f"Indicators : {', '.join(alert['indicators'])}"
        )


def main():

    print("[EDR] Mini EDR started")
    print("[EDR] Monitoring processes...\n")

    # Take initial process snapshot
    previous_processes = get_processes()

    try:

        while True:

            # Wait before taking another snapshot
            time.sleep(2)

            # Get current processes
            current_processes = get_processes()

            # Find newly created processes
            new_processes = (
                set(current_processes)
                - set(previous_processes)
            )

            for pid in new_processes:

                process = current_processes[pid]

                # Display process event
                display_process_event(process)

                # Save event to JSON
                save_event(process)

                # Run detection engine
                alert = detect_suspicious_process(process)

                # Display alert if detected
                if alert:
                    display_alert(alert)

            # Update previous snapshot
            previous_processes = current_processes

    except KeyboardInterrupt:

        print("\n\n[EDR] Monitoring stopped.")
        print("[EDR] Exiting...")


if __name__ == "__main__":
    main()