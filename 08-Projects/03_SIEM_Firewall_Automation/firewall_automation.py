import sys
import csv
import gzip
import os

print("=== SIEM FIREWALL AUTOMATION ===")
print("Arguments received:", sys.argv)

if len(sys.argv) < 2:
    print("No Splunk result file received.")
    sys.exit(1)

result_file = sys.argv[-1]

print("Result file:", result_file)

if not os.path.exists(result_file):
    print("Result file does not exist.")
    sys.exit(1)

print("Result file found.")

if result_file.endswith(".gz"):
    with gzip.open(result_file, "rt", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print("Splunk result:", row)
else:
    with open(result_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print("Splunk result:", row)

print("=== END ===")