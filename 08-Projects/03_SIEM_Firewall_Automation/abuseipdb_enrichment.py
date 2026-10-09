import sys
import winreg
import requests


def get_api_key():
    key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    )

    api_key, _ = winreg.QueryValueEx(key, "ABUSEIPDB_API_KEY")
    return api_key


def check_ip(ip):
    api_key = get_api_key()

    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()["data"]

    return {
        "ip": ip,
        "abuse_confidence_score": data.get("abuseConfidenceScore"),
        "total_reports": data.get("totalReports"),
        "country": data.get("countryCode"),
        "isp": data.get("isp"),
        "domain": data.get("domain")
    }


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("ERROR: IP address required")
        sys.exit(1)

    ip = sys.argv[1]

    try:
        result = check_ip(ip)

        print(f"IP: {result['ip']}")
        print(
            f"Abuse Confidence Score: "
            f"{result['abuse_confidence_score']}"
        )
        print(f"Total Reports: {result['total_reports']}")
        print(f"Country: {result['country']}")
        print(f"ISP: {result['isp']}")
        print(f"Domain: {result['domain']}")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)