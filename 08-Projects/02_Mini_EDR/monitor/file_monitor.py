import os


MONITORED_FOLDER = "monitored_files"


def get_files():
    """Get information about files in the monitored folder."""

    files = {}

    for root, directories, filenames in os.walk(
        MONITORED_FOLDER
    ):

        for filename in filenames:

            file_path = os.path.join(
                root,
                filename
            )

            try:

                files[file_path] = {
                    "path": file_path,
                    "size": os.path.getsize(file_path),
                    "modified": os.path.getmtime(file_path)
                }

            except OSError:
                continue

    return files


def create_file_event(file_path, event_type):
    """Create a file monitoring event."""

    return {
        "event_type": event_type,
        "file_name": os.path.basename(file_path),
        "path": os.path.abspath(file_path)
    }


def detect_file_changes(previous_files, current_files):
    """Detect created, modified and deleted files."""

    events = []

    # =====================================
    # Detect created files
    # =====================================

    new_files = (
        set(current_files)
        - set(previous_files)
    )

    for file_path in new_files:

        events.append(
            create_file_event(
                file_path,
                "file_created"
            )
        )

    # =====================================
    # Detect modified files
    # =====================================

    common_files = (
        set(current_files)
        & set(previous_files)
    )

    for file_path in common_files:

        old_file = previous_files[file_path]
        new_file = current_files[file_path]

        if (
            old_file["size"] != new_file["size"]
            or
            old_file["modified"] != new_file["modified"]
        ):

            events.append(
                create_file_event(
                    file_path,
                    "file_modified"
                )
            )

    # =====================================
    # Detect deleted files
    # =====================================

    deleted_files = (
        set(previous_files)
        - set(current_files)
    )

    for file_path in deleted_files:

        events.append(
            create_file_event(
                file_path,
                "file_deleted"
            )
        )

    return events