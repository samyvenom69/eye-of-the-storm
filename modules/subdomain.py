"""Subdomain Enumeration Module — Phase: RECON"""

import dns.resolver
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from modules import BaseModule
from utils.banner import print_result
from utils.http import make_session


class SubdomainModule(BaseModule):
    """Enumerate subdomains via wordlist brute-force + certificate transparency."""

    WORKERS = 40
    MAX_DISPLAY = 20

    def run(self) -> dict:
        results = {"target": self.target, "found": [], "crt_sh": []}
        self.info(f"[SUBDOMAIN] Enumerating: {self.target}")

        results["crt_sh"] = self._crt_sh()
        for sub in results["crt_sh"][:self.MAX_DISPLAY]:
            print_result("crt.sh", sub, color="cyan")

        results["found"] = self._bruteforce()
        return results

    # ------------------------------------------------------------------ #
    # Certificate Transparency (crt.sh)
    # ------------------------------------------------------------------ #
    def _crt_sh(self) -> list:
        try:
            session = make_session(self.config, pool_size=4)
            resp = session.get(
                f"https://crt.sh/?q=%.{self.target}&output=json",
                timeout=self.config.REQUEST_TIMEOUT,
            )
            if resp.status_code != 200:
                return []
            entries = set()
            for entry in resp.json():
                # name_value may hold several newline-separated names, some wildcarded
                for name in str(entry.get("name_value", "")).splitlines():
                    name = name.strip().lower().lstrip("*.")
                    if name and name.endswith(self.target):
                        entries.add(name)
            return sorted(entries)
        except Exception as e:
            self.warn(f"crt.sh error: {e}")
            return []

    # ------------------------------------------------------------------ #
    # Parallel wordlist brute-force (DNS A-record resolution)
    # ------------------------------------------------------------------ #
    def _bruteforce(self) -> list:
        wordlist = self.config.WORDLIST_PATH
        try:
            with open(wordlist, encoding="utf-8", errors="ignore") as f:
                words = [w.strip() for w in f if w.strip()]
        except FileNotFoundError:
            self.warn(f"Wordlist not found: {wordlist}")
            return []

        found = []

        def resolve(word):
            fqdn = f"{word}.{self.target}"
            try:
                dns.resolver.Resolver().resolve(fqdn, "A")
                return fqdn
            except Exception:
                return None

        with ThreadPoolExecutor(max_workers=self.WORKERS) as executor:
            futures = {executor.submit(resolve, w): w for w in words}
            for future in as_completed(futures):
                fqdn = future.result()
                if fqdn:
                    found.append(fqdn)
                    print_result("Found", fqdn, color="green")

        self.info(f"Brute-force: {len(found)}/{len(words)} subdomains resolved.")
        return sorted(found)
