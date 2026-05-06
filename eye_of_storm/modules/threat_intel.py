"""Threat Intelligence Feeds Module — Phase: INTELLIGENCE"""
import requests
from modules import BaseModule
from utils.banner import print_result

class ThreatIntelModule(BaseModule):
    """Query VirusTotal and AbuseIPDB threat intelligence APIs."""
    VT_URL = "https://www.virustotal.com/api/v3/domains/{}"
    def run(self) -> dict:
        results = {"target": self.target, "virustotal": {}, "reputation": "unknown"}
        vt_key = self.config.VIRUSTOTAL_API_KEY
        if not vt_key:
            self.warn("VIRUSTOTAL_API_KEY not set."); return results
        self.info(f"[THREAT] Querying VirusTotal: {self.target}")
        try:
            resp = requests.get(self.VT_URL.format(self.target),
                                headers={"x-apikey": vt_key},
                                timeout=self.config.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                data  = resp.json().get("data", {}).get("attributes", {})
                stats = data.get("last_analysis_stats", {})
                results["virustotal"] = {
                    "malicious":   stats.get("malicious", 0),
                    "suspicious":  stats.get("suspicious", 0),
                    "harmless":    stats.get("harmless", 0),
                    "reputation":  data.get("reputation", 0),
                    "categories":  data.get("categories", {}),
                }
                mal = results["virustotal"]["malicious"]
                color = "red" if mal > 0 else "green"
                print_result("Malicious detections", str(mal), color=color)
        except Exception as e:
            self.error(str(e)); results["error"] = str(e)
        return results
