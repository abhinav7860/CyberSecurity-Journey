
import subprocess
import ipaddress

TEST_IP = "192.0.2.1"  # Reserved documentation IP
RULE_NAME = f"SIEM-AutoBlock-TEST-{TEST_IP}"

def run_powershell(command):
    result = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            command,
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()

try:
    # Confirm this is a reserved test address, not a real public IOC.
    address = ipaddress.ip_address(TEST_IP)
    if address.is_global:
        raise RuntimeError("Test safety check failed: IP is globally routable")

    simulated_score = 85
    print(f"Simulated AbuseIPDB score: {simulated_score}")

    if simulated_score < 50:
        print("Decision: MONITOR")
    else:
        print("Decision: BLOCK candidate")

        # Create a narrowly scoped outbound test rule.
        create = (
            "$ErrorActionPreference = 'Stop'; "
            f"New-NetFirewallRule -DisplayName '{RULE_NAME}' "
            f"-Direction Outbound -RemoteAddress '{TEST_IP}' "
            "-Action Block -Profile Any -Enabled True | Out-Null"
        )
        run_powershell(create)

        # Verify that the rule is enabled, blocks, and matches the test IP.
        verify = (
            "$ErrorActionPreference = 'Stop'; "
            f"$r = Get-NetFirewallRule -DisplayName '{RULE_NAME}' "
            "-ErrorAction Stop; "
            "$f = @(Get-NetFirewallAddressFilter "
            "-AssociatedNetFirewallRule $r); "
            f"if ($r.Enabled -eq $true -and $r.Action -eq 'Block' "
            f"-and ($f | Where-Object {{ $_.RemoteAddress -contains '{TEST_IP}' }})) "
            "{ 'VERIFICATION: PASS' } else { exit 1 }"
        )
        print(run_powershell(verify))

finally:
    # Always attempt to remove the temporary test rule.
    cleanup = (
        f"Get-NetFirewallRule -DisplayName '{RULE_NAME}' "
        "-ErrorAction SilentlyContinue | Remove-NetFirewallRule"
    )
    try:
        run_powershell(cleanup)
        print("TEST RULE CLEANUP: completed")
    except Exception as error:
        print(f"WARNING: Check/remove test rule manually: {error}")
