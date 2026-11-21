"""Subdomain Enumeration Module — Phase: RECON (async engine)"""

import asyncio

import aiohttp
import dns.asyncresolver
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from modules import BaseModule
from utils.banner import console, print_result


class SubdomainModule(BaseModule):
    """Enumerate subdomains via wordlist brute-force + certificate transparency."""

    CONCURRENCY = 60
    MAX_DISPLAY = 20

    def run(self) -> dict:
        self.info(f"[SUBDOMAIN] Enumerating: {self.target} (async engine)")
        return asyncio.run(self._run_async())

    # ------------------------------------------------------------------ #

    async def _run_async(self) -> dict:
        results = {"target": self.target, "found": [], "crt_sh": []}

        # crt.sh and DNS brute-force are independent: run them concurrently.
        results["crt_sh"], results["found"] = await asyncio.gather(
            self._crt_sh(), self._bruteforce()
        )
        for sub in results["crt_sh"][:self.MAX_DISPLAY]:
            print_result("crt.sh", sub, color="cyan")

        return results

    # ------------------------------------------------------------------ #
    # Certificate Transparency (crt.sh) — aiohttp with retry
    # ------------------------------------------------------------------ #
    async def _crt_sh(self) -> list:
        timeout = aiohttp.ClientTimeout(total=self.config.REQUEST_TIMEOUT)
        try:
            async with aiohttp.ClientSession(
                timeout=timeout, headers=self.config.REQUEST_HEADERS
            ) as session:
                for attempt in range(3):
                    try:
                        async with session.get(
                            f"https://crt.sh/?q=%.{self.target}&output=json"
                        ) as resp:
                            if resp.status in {429, 500, 502, 503, 504} and attempt < 2:
                                await asyncio.sleep(0.5 * (attempt + 1))
                                continue
                            if resp.status != 200:
                                return []
                            payload = await resp.json(content_type=None)
                            break
                    except (aiohttp.ClientError, asyncio.TimeoutError):
                        if attempt == 2:
                            raise
                        await asyncio.sleep(0.5 * (attempt + 1))
                else:
                    return []
        except Exception as e:
            self.warn(f"crt.sh error: {e}")
            return []

        entries = set()
        for entry in payload:
            # name_value may hold several newline-separated names, some wildcarded
            for name in str(entry.get("name_value", "")).splitlines():
                name = name.strip().lower().lstrip("*.")
                if name and name.endswith(self.target):
                    entries.add(name)
        return sorted(entries)

    # ------------------------------------------------------------------ #
    # Async wordlist brute-force (DNS A-record resolution)
    # ------------------------------------------------------------------ #
    async def _bruteforce(self) -> list:
        wordlist = self.config.WORDLIST_PATH
        try:
            with open(wordlist, encoding="utf-8", errors="ignore") as f:
                words = [w.strip() for w in f if w.strip()]
        except FileNotFoundError:
            self.warn(f"Wordlist not found: {wordlist}")
            return []

        resolver = dns.asyncresolver.Resolver()
        resolver.timeout = 2.0
        resolver.lifetime = 5.0
        semaphore = asyncio.Semaphore(self.CONCURRENCY)
        found = []

        async def resolve(word):
            fqdn = f"{word}.{self.target}"
            try:
                async with semaphore:
                    await resolver.resolve(fqdn, "A")
                return fqdn
            except Exception:
                return None

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task(
                f"[cyan]Brute-forcing {len(words)} subdomains…[/cyan]",
                total=len(words),
            )
            for coro in asyncio.as_completed([resolve(w) for w in words]):
                fqdn = await coro
                if fqdn:
                    found.append(fqdn)
                    print_result("Found", fqdn, color="green")
                progress.advance(task)

        self.info(f"Brute-force: {len(found)}/{len(words)} subdomains resolved.")
        return sorted(found)
