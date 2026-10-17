"""
IP Geolocation & Abuse Intelligence Module
Phase: RECON
"""

import re
import requests
from modules import BaseModule
from utils.banner import print_result

IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


class IPGeoModule(BaseModule):
    """IP geolocation (ipinfo.io) and abuse score (AbuseIPDB)."""

    def run(self) -> dict:
        results = {
            "target": self.target,
            "geo":    {},
            "abuse":  {},
            "rdns":   None,
        }

        target = self.target
        if not IP_RE.match(target):
            # Resolve hostname to IP
            import socket
            try:
                target = socket.gethostbyname(target)
                self.info(f"Resolved to IP: {target}")
                results["resolved_ip"] = target
            except Exception as e:
                results["error"] = str(e)
                return results

        self.info(f"[IP GEO] Querying: {target}")

        # ipinfo.io
        try:
            token  = self.config.IPINFO_TOKEN
            url    = f"https://ipinfo.io/{target}/json"
            params = {"token": token} if token else {}
            resp   = requests.get(url, params=params, timeout=self.config.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                data = resp.json()
                results["geo"] = {
                    "ip":       data.get("ip"),
                    "hostname": data.get("hostname", "N/A"),
                    "city":     data.get("city"),
                    "region":   data.get("region"),
                    "country":  data.get("country"),
                    "org":      data.get("org"),
                    "timezone": data.get("timezone"),
                    "loc":      data.get("loc"),
                }
                for k, v in results["geo"].items():
                    if v:
                        print_result(k.capitalize(), str(v), color="cyan")
        except Exception as e:
            self.error(f"ipinfo error: {e}")

        # AbuseIPDB
        key = self.config.ABUSEIPDB_KEY
        if key:
            try:
                resp = requests.get(
                    "https://api.abuseipdb.com/api/v2/check",
                    headers={"Key": key, "Accept": "application/json"},
                    params={"ipAddress": target, "maxAgeInDays": 90},
                    timeout=self.config.REQUEST_TIMEOUT,
                )
                if resp.status_code == 200:
                    abuse = resp.json().get("data", {})
                    results["abuse"] = {
                        "score":       abuse.get("abuseConfidenceScore"),
                        "total_reports": abuse.get("totalReports"),
                        "last_reported": abuse.get("lastReportedAt"),
                        "is_whitelisted": abuse.get("isWhitelisted"),
                    }
                    score = results["abuse"]["score"]
                    color = "red" if score > 50 else "yellow" if score > 10 else "green"
                    print_result("Abuse score", f"{score}/100", color=color)
            except Exception as e:
                self.warn(f"AbuseIPDB error: {e}")

        return results
