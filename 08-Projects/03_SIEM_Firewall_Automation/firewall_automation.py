import csv

import ipaddress

import json

import os

import subprocess

import tempfile

import winreg

from datetime import datetime, timedelta, timezone



import requests





# ============================================================

# CONFIGURATION

# ============================================================



LOOKUP_FILE = (

    r"C:\Program Files\Splunk\etc\apps\search"

    r"\lookups\suspicious_firewall_iocs.csv"

)



LOG_FILE = (

    r"C:\Program Files\Splunk\var\log\splunk"

    r"\firewall_automation.log"

)



STATE_FILE = (

    r"C:\Program Files\Splunk\var\log\splunk"

    r"\firewall_automation_state.json"

)



ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"

ABUSE_SCORE_THRESHOLD = 50

REQUEST_TIMEOUT = 15



# Re-check an IOC previously classified as MONITOR after this interval.

MONITOR_RECHECK_HOURS = 24





# ============================================================

# LOGGING

# ============================================================



def log(message):

    """Write a timestamped message to the automation log."""

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    try:

        with open(LOG_FILE, "a", encoding="utf-8") as file:

            file.write(f"{timestamp} | {message}\n")

    except OSError as error:

        # Keep a logging failure visible to the task's captured output.

        print(f"LOGGING ERROR: {error} | Original message: {message}")





# ============================================================

# API KEY

# ============================================================



def get_api_key():

    """Read the machine-level AbuseIPDB key from the registry."""

    registry_path = (

        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"

    )



    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:

        api_key, _ = winreg.QueryValueEx(key, "ABUSEIPDB_API_KEY")



    if not api_key or not api_key.strip():

        raise ValueError("ABUSEIPDB_API_KEY is empty")



    return api_key.strip()





# ============================================================

# IP VALIDATION

# ============================================================



def validate_ip(value):

    """Accept valid, globally routable IP addresses only."""

    try:

        address = ipaddress.ip_address(value.strip())

    except (ValueError, AttributeError):

        log(f"SAFETY: Invalid IP skipped: {value!r}")

        return None



    if not address.is_global:

        log(f"SAFETY: Non-global IP skipped: {address}")

        return None



    return str(address)





# ============================================================

# PERSISTENT STATE / DEDUPLICATION

# ============================================================



def load_state():

    """Load previously completed IOC decisions."""

    if not os.path.exists(STATE_FILE):

        return {}



    with open(STATE_FILE, "r", encoding="utf-8") as file:

        state = json.load(file)



    if not isinstance(state, dict):

        raise ValueError("State file must contain a JSON object")



    return state





def save_state(state):

    """Atomically save the state file."""

    state_dir = os.path.dirname(STATE_FILE)

    fd, temporary_path = tempfile.mkstemp(

        prefix="firewall_state_",

        suffix=".tmp",

        dir=state_dir,

        text=True,

    )



    try:

        with os.fdopen(fd, "w", encoding="utf-8") as file:

            json.dump(state, file, indent=2)

            file.write("\n")



        os.replace(temporary_path, STATE_FILE)

    finally:

        if os.path.exists(temporary_path):

            os.remove(temporary_path)





def should_process_ip(ip, state, now=None):

    """

    Return True for new IOCs and MONITOR IOCs whose recheck interval elapsed.

    Previously blocked IOCs remain deduplicated.

    """

    entry = state.get(ip)

    if not isinstance(entry, dict):

        return True



    if entry.get("decision") != "monitor":

        log(f"Previously processed IOC skipped: {ip}")

        return False



    processed_at = entry.get("processed_at")

    try:

        last_checked = datetime.fromisoformat(processed_at)

        if last_checked.tzinfo is None:

            last_checked = last_checked.replace(tzinfo=timezone.utc)

    except (TypeError, ValueError):

        # If a legacy/corrupt monitor timestamp cannot be parsed, recheck it.

        log(f"MONITOR state timestamp invalid; rechecking IOC: {ip}")

        return True



    now = now or datetime.now(timezone.utc)

    if now - last_checked.astimezone(timezone.utc) >= timedelta(

        hours=MONITOR_RECHECK_HOURS

    ):

        log(f"MONITOR recheck interval elapsed; rechecking IOC: {ip}")

        return True



    log(f"MONITOR IOC not due for recheck: {ip}")

    return False





# ============================================================

# ABUSEIPDB ENRICHMENT

# ============================================================



def enrich_ip(ip, api_key):

    """Return the AbuseIPDB abuse confidence score, or None."""

    log(f"Starting IOC enrichment: {ip}")



    headers = {"Key": api_key, "Accept": "application/json"}

    params = {"ipAddress": ip, "maxAgeInDays": 90}



    try:

        response = requests.get(

            ABUSEIPDB_URL,

            headers=headers,

            params=params,

            timeout=REQUEST_TIMEOUT,

        )

        response.raise_for_status()



        data = response.json()["data"]

        score = int(data["abuseConfidenceScore"])



        if not 0 <= score <= 100:

            raise ValueError("Unexpected abuse confidence score")



        log(f"AbuseIPDB score: {score}")

        log(f"Total reports: {data.get('totalReports')}")

        log(f"Country: {data.get('countryCode')}")

        log(f"ISP: {data.get('isp')}")

        log(f"Domain: {data.get('domain')}")

        return score



    except Exception as error:

        log(f"ENRICHMENT FAILED for {ip}: {error}")

        return None





# ============================================================

# WINDOWS FIREWALL

# ============================================================



def block_ip(ip):

    """

    Create an outbound block rule and verify its enabled status, action,

    and associated remote address.

    """

    validated_ip = validate_ip(ip)

    if validated_ip is None:

        log(f"BLOCK REFUSED: Invalid or non-global IP: {ip}")

        return False



    rule_name = f"SIEM-AutoBlock-{validated_ip}"

    # The name and address have already been validated/constructed from an IP.

    rule_name_ps = rule_name.replace("'", "''")



    verify_command = (

        "$ErrorActionPreference = 'Stop'; "

        f"$rules = @(Get-NetFirewallRule -DisplayName '{rule_name_ps}' "

        "-ErrorAction SilentlyContinue); "

        "foreach ($r in $rules) { "

        "$filters = @(Get-NetFirewallAddressFilter "

        "-AssociatedNetFirewallRule $r -ErrorAction SilentlyContinue); "

        "foreach ($f in $filters) { "

        f"if ($r.Enabled -eq $true -and $r.Action -eq 'Block' "

        f"-and $f.RemoteAddress -contains '{validated_ip}') "

        "{ exit 0 } } }; exit 1"

    )



    try:

        existing = subprocess.run(

            [

                "powershell.exe",

                "-NoProfile",

                "-NonInteractive",

                "-Command",

                verify_command,

            ],

            capture_output=True,

            text=True,

            timeout=20,

        )



        if existing.returncode == 0:

            log(f"VERIFIED: Existing matching block rule is enabled: {validated_ip}")

            return True



        create_command = (

            "$ErrorActionPreference = 'Stop'; "

            "New-NetFirewallRule "

            f"-DisplayName '{rule_name_ps}' "

            "-Direction Outbound "

            f"-RemoteAddress '{validated_ip}' "

            "-Action Block "

            "-Profile Any "

            "-Enabled True | Out-Null; "

            f"$r = Get-NetFirewallRule -DisplayName '{rule_name_ps}' "

            "-ErrorAction Stop; "

            "$filters = @(Get-NetFirewallAddressFilter "

            "-AssociatedNetFirewallRule $r -ErrorAction Stop); "

            "if ($r.Enabled -eq $true -and $r.Action -eq 'Block' "

            f"-and ($filters | Where-Object {{ $_.RemoteAddress -contains '{validated_ip}' }})) "

            "{ exit 0 } else { exit 1 }"

        )



        result = subprocess.run(

            [

                "powershell.exe",

                "-NoProfile",

                "-NonInteractive",

                "-Command",

                create_command,

            ],

            capture_output=True,

            text=True,

            timeout=30,

        )



        if result.returncode == 0:

            log(f"FIREWALL BLOCK CREATED AND VERIFIED: {validated_ip}")

            return True



        log(f"FIREWALL BLOCK FAILED: {validated_ip}")

        if result.stderr.strip():

            log(f"PowerShell error: {result.stderr.strip()}")

        return False



    except Exception as error:

        log(f"FIREWALL BLOCK ERROR for {validated_ip}: {error}")

        return False





# ============================================================

# MAIN AUTOMATION

# ============================================================



def main():

    log("=== SIEM FIREWALL AUTOMATION STARTED ===")



    if not os.path.isfile(LOOKUP_FILE):

        log(f"ERROR: Lookup file not found: {LOOKUP_FILE}")

        return 1



    try:

        state = load_state()

    except Exception as error:

        # Fail closed: do not process IOCs if state is unreadable.

        log(f"ERROR: Could not load state; stopping safely: {error}")

        return 1



    try:

        api_key = get_api_key()

    except Exception as error:

        log(f"ERROR: Cannot retrieve AbuseIPDB API key: {error}")

        return 1



    seen_this_run = set()



    try:

        with open(

            LOOKUP_FILE,

            "r",

            encoding="utf-8-sig",

            newline="",

        ) as file:

            reader = csv.DictReader(file)

            # Splunk outputlookup may leave a zero-byte file when there are
            # no matching IOCs. Treat this as a normal no-work run.
            if not reader.fieldnames:
                log("LOOKUP EMPTY: No IOC rows available; waiting for next Splunk refresh")
                log("=== SIEM FIREWALL AUTOMATION FINISHED ===")
                return 0

            if "dst_ip" not in reader.fieldnames:
                log(f"ERROR: Invalid CSV headers: {reader.fieldnames!r}")
                return 1

            for row in reader:

                raw_ip = (row.get("dst_ip") or "").strip()

                log(f"Splunk detection: {row}")



                ip = validate_ip(raw_ip)

                if ip is None:

                    continue



                if ip in seen_this_run:

                    log(f"Duplicate IOC skipped this run: {ip}")

                    continue

                seen_this_run.add(ip)



                if not should_process_ip(ip, state):

                    continue



                score = enrich_ip(ip, api_key)



                # Failed enrichment is not saved; a later scheduled run retries.

                if score is None:

                    log(f"ACTION: MONITOR {ip}; enrichment unavailable; will retry")

                    continue



                if score >= ABUSE_SCORE_THRESHOLD:

                    log(f"DECISION: BLOCK CANDIDATE {ip}; AbuseIPDB score={score}")



                    # Record completion only if the firewall action succeeds.

                    if not block_ip(ip):

                        log(

                            f"NOT MARKED PROCESSED: Firewall action failed for {ip}; "

                            "will retry"

                        )

                        continue



                    decision = "blocked"

                else:

                    log(f"DECISION: MONITOR {ip}; AbuseIPDB score={score}")

                    decision = "monitor"



                state[ip] = {

                    "processed_at": datetime.now(timezone.utc).isoformat(),

                    "abuse_score": score,

                    "decision": decision,

                }



                try:

                    save_state(state)

                except Exception as error:

                    log(f"CRITICAL: Could not save state for {ip}: {error}")

                    return 1



    except Exception as error:

        log(f"ERROR while processing lookup: {error}")

        return 1



    log("=== SIEM FIREWALL AUTOMATION FINISHED ===")

    return 0





if __name__ == "__main__":

    raise SystemExit(main())
