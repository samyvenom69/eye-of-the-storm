"""
Email Breach & Validation Module
Phase: INVESTIGATE
"""

import re
import requests
from modules import BaseModule
from utils.banner import print_result


class EmailBreachModule(BaseModule):
    """Email breach detection via HaveIBeenPwned + basic OSINT validation."""

    HIBP_URL   = "https://haveibeenpwned.com/api/v3/breachedaccount/{}"
    PASTE_URL  = "https://haveibeenpwned.com/api/v3/pasteaccount/{}"
    MX_CHECK   = "https://api.hunter.io/v2/email-verifier"

    EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$", re.IGNORECASE)

    def run(self) -> dict:
        results = {
            "target":   self.target,
            "valid":    False,
            "breaches": [],
            "pastes":   [],
            "domain":   None,
        }

        if not self.EMAIL_RE.match(self.target):
            self.warn("Target does not appear to be a valid email address.")
            results["error"] = "Invalid email format"
            return results

        results["valid"]  = True
        results["domain"] = self.target.split("@")[1]
        self.info(f"[EMAIL] Checking: {self.target}")
        print_result("Email",  self.target)
        print_result("Domain", results["domain"], color="cyan")

        # Breach lookup (requires HIBP API key)
        api_key = self.config.HIBP_API_KEY
        if api_key:
            results["breaches"] = self._check_breaches(api_key)
            results["pastes"]   = self._check_pastes(api_key)
        else:
            self.warn("HIBP_API_KEY not set — breach check skipped.")
            results["breaches"] = "API key required (set HIBP_API_KEY)"
            results["pastes"]   = "API key required"

        return results

    def _check_breaches(self, api_key: str) -> list:
        try:
            url  = self.HIBP_URL.format(self.target)
            resp = requests.get(
                url,
                headers={
                    "hibp-api-key":  api_key,
                    "user-agent":    "EOTS-OSINT-Research",
                },
                timeout=self.config.REQUEST_TIMEOUT,
            )
            if resp.status_code == 200:
                breaches = resp.json()
                for b in breaches:
                    print_result(
                        f"  Breach [{b.get('BreachDate','?')}]",
                        b.get("Name", "unknown"),
                        color="red",
                    )
                return [
                    {
                        "name":         b.get("Name"),
                        "date":         b.get("BreachDate"),
                        "data_classes": b.get("DataClasses", []),
                        "description":  b.get("Description", ""),
                    }
                    for b in breaches
                ]
            elif resp.status_code == 404:
                print_result("Breaches", "No breaches found", color="green")
                return []
            else:
                self.warn(f"HIBP returned {resp.status_code}")
                return []
        except Exception as e:
            self.error(f"Breach check error: {e}")
            return []

    def _check_pastes(self, api_key: str) -> list:
        try:
            url  = self.PASTE_URL.format(self.target)
            resp = requests.get(
                url,
                headers={"hibp-api-key": api_key, "user-agent": "EOTS-OSINT-Research"},
                timeout=self.config.REQUEST_TIMEOUT,
            )
            if resp.status_code == 200:
                pastes = resp.json()
                print_result("Paste leaks", str(len(pastes)), color="yellow")
                return pastes
            return []
        except Exception as e:
            self.error(f"Paste check error: {e}")
            return []
