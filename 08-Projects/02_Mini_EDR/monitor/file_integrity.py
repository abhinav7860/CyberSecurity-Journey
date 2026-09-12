# monitor/file_integrity.py

import os
import hashlib


MONITORED_FOLDER = "monitored_files"


# ============================================================
# Calculate SHA-256
# ============================================================

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    try:

        with open(
            file_path,
            "rb"
        ) as file:

            while True:

                data = file.read(4096)

                if not data:
                    break

                sha256.update(data)

        return sha256.hexdigest()

    except (
        FileNotFoundError,
        PermissionError,
        OSError
    ):

        return None


# ============================================================
# Create File Hash Baseline
# ============================================================

def get_file_hashes():
    """Create a snapshot of files and their SHA-256 hashes."""

    hashes = {}

    for root, directories, filenames in os.walk(
        MONITORED_FOLDER
    ):

        for filename in filenames:

            file_path = os.path.join(
                root,
                filename
            )

            file_hash = calculate_hash(
                file_path
            )

            if file_hash:

                hashes[file_path] = file_hash

    return hashes


# ============================================================
# Detect Integrity Changes
# ============================================================

def detect_integrity_changes(
    baseline,
    current_hashes
):
    """Detect modified and deleted files."""

    events = []

    # ========================================================
    # Check Existing Files
    # ========================================================

    for file_path in baseline:

        # File was deleted
        if file_path not in current_hashes:

            events.append({
                "event_type": "file_integrity_deleted",
                "file_name": os.path.basename(file_path),
                "path": os.path.abspath(file_path),
                "old_hash": baseline[file_path],
                "new_hash": None
            })

            continue

        old_hash = baseline[file_path]
        new_hash = current_hashes[file_path]

        # File contents changed
        if old_hash != new_hash:

            events.append({
                "event_type": "file_integrity_changed",
                "file_name": os.path.basename(file_path),
                "path": os.path.abspath(file_path),
                "old_hash": old_hash,
                "new_hash": new_hash
            })


    # ========================================================
    # New Files
    # ========================================================

    # New files are intentionally NOT reported as
    # integrity events.
    #
    # The File Monitor already reports file creation.
    # FIM will simply include the new file in the
    # next baseline.


    return events