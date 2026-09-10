import os
import time
from datetime import datetime


MONITORED_FOLDER = "monitored_files"


def get_files():
    """Get files currently present in the monitored folder."""

    files = set()

    for root, directories, filenames in os.walk(MONITORED_FOLDER):

        for filename in filenames:

            full_path = os.path.join(root, filename)

            files.add(full_path)

    return files


def main():

    print("[FILE MONITOR] Started")
    print(f"[FILE MONITOR] Watching: {MONITORED_FOLDER}\n")

    previous_files = get_files()

    try:

        while True:

            time.sleep(2)

            current_files = get_files()

            new_files = current_files - previous_files

            for file_path in new_files:

                print("\n[FILE CREATED]")

                print(
                    f"Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )

                print(f"File : {os.path.basename(file_path)}")
                print(f"Path : {os.path.abspath(file_path)}")

            previous_files = current_files

    except KeyboardInterrupt:

        print("\n\n[FILE MONITOR] Stopped.")


if __name__ == "__main__":
    main()