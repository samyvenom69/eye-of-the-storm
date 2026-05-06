"""Subdomain Enumeration Module — Phase: RECON"""
import requests, dns.resolver
from modules import BaseModule
from utils.banner import print_result

class SubdomainModule(BaseModule):
    """Enumerate subdomains via wordlist brute-force + certificate transparency."""
    def run(self) -> dict:
        results = {"target": self.target, "found": [], "crt_sh": []}
        self.info(f"[SUBDOMAIN] Enumerating: {self.target}")
        # Certificate Transparency (crt.sh)
        try:
            resp = requests.get(f"https://crt.sh/?q=%.{self.target}&output=json",
                                timeout=self.config.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                entries = {e["name_value"] for e in resp.json()}
                results["crt_sh"] = sorted(entries)
                for sub in results["crt_sh"][:20]:
                    print_result("crt.sh", sub, color="cyan")
        except Exception as e:
            self.warn(f"crt.sh error: {e}")
        # Wordlist brute-force
        wordlist = self.config.WORDLIST_PATH
        try:
            with open(wordlist) as f:
                words = [w.strip() for w in f if w.strip()]
            resolver = dns.resolver.Resolver()
            for word in words:
                fqdn = f"{word}.{self.target}"
                try:
                    resolver.resolve(fqdn, "A")
                    results["found"].append(fqdn)
                    print_result("Found", fqdn, color="green")
                except Exception:
                    pass
        except FileNotFoundError:
            self.warn(f"Wordlist not found: {wordlist}")
        return results
