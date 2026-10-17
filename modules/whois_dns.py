"""
WHOIS & DNS Reconnaissance Module
Phase: RECON
"""

import dns.resolver
import whois
from modules import BaseModule
from utils.banner import print_result


class WhoisDNSModule(BaseModule):
    """WHOIS lookup + DNS record enumeration (A, MX, NS, TXT, CNAME)."""

    RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]

    def run(self) -> dict:
        results = {"target": self.target, "whois": {}, "dns": {}}

        self.info(f"[WHOIS/DNS] Querying: {self.target}")

        # WHOIS
        try:
            w = whois.whois(self.target)
            results["whois"] = {
                "registrar":      str(w.registrar or "N/A"),
                "creation_date":  str(w.creation_date or "N/A"),
                "expiration_date": str(w.expiration_date or "N/A"),
                "name_servers":   w.name_servers or [],
                "status":         w.status or [],
                "emails":         w.emails or [],
                "org":            str(w.org or "N/A"),
                "country":        str(w.country or "N/A"),
            }
            print_result("Registrar",       results["whois"]["registrar"])
            print_result("Creation",        results["whois"]["creation_date"])
            print_result("Expiration",      results["whois"]["expiration_date"])
            print_result("Org",             results["whois"]["org"])
        except Exception as e:
            self.warn(f"WHOIS failed: {e}")
            results["whois"]["error"] = str(e)

        # DNS
        resolver = dns.resolver.Resolver()
        resolver.timeout = self.config.REQUEST_TIMEOUT

        for rtype in self.RECORD_TYPES:
            try:
                answers = resolver.resolve(self.target, rtype)
                values  = [str(r) for r in answers]
                results["dns"][rtype] = values
                print_result(f"DNS {rtype}", ", ".join(values), color="green")
            except dns.resolver.NoAnswer:
                results["dns"][rtype] = []
            except dns.resolver.NXDOMAIN:
                self.warn("Domain does not exist (NXDOMAIN).")
                results["dns"]["error"] = "NXDOMAIN"
                break
            except Exception as e:
                results["dns"][rtype] = {"error": str(e)}

        return results
