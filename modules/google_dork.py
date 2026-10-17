"""Google Dorking Automation — Phase: INVESTIGATE"""
from modules import BaseModule
from utils.banner import print_result

DORK_TEMPLATES = [
    'site:{target} filetype:pdf',
    'site:{target} filetype:xls OR filetype:xlsx',
    'site:{target} inurl:admin',
    'site:{target} inurl:login',
    'site:{target} "index of"',
    'site:{target} ext:sql',
    '"@{target}" email',
    'intext:"{target}" site:pastebin.com',
    'intext:"{target}" site:github.com',
]

class GoogleDorkModule(BaseModule):
    """Generate Google Dork query templates for OSINT research."""
    def run(self) -> dict:
        results = {"target": self.target, "dorks": []}
        self.info(f"[DORK] Generating dork templates for: {self.target}")
        for tpl in DORK_TEMPLATES:
            query = tpl.format(target=self.target)
            url   = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            results["dorks"].append({"query": query, "url": url})
            print_result("Dork", query, color="yellow")
        self.info("Open URLs manually in browser for results (anti-scraping).")
        return results
