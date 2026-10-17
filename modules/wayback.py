"""Wayback Machine Historical Analysis — Phase: ANALYSE"""
import requests
from modules import BaseModule
from utils.banner import print_result

class WaybackModule(BaseModule):
    """Query the Wayback Machine CDX API for historical snapshots."""
    CDX_URL = "http://web.archive.org/cdx/search/cdx"
    def run(self) -> dict:
        results = {"target": self.target, "snapshots": [], "total": 0}
        self.info(f"[WAYBACK] Querying: {self.target}")
        try:
            resp = requests.get(self.CDX_URL, params={
                "url": self.target, "output": "json", "limit": 20,
                "fl": "timestamp,statuscode,mimetype,length", "collapse": "timestamp:8",
            }, timeout=self.config.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                rows = resp.json()[1:]  # skip header
                results["total"] = len(rows)
                for row in rows:
                    snap = {"timestamp": row[0], "status": row[1],
                            "mime": row[2], "length": row[3]}
                    snap["url"] = f"https://web.archive.org/web/{row[0]}/{self.target}"
                    results["snapshots"].append(snap)
                    print_result(row[0], snap["url"], color="cyan")
        except Exception as e:
            self.error(str(e)); results["error"] = str(e)
        return results
