"""Reddit & GitHub Public Intelligence Module — Phase: INTELLIGENCE"""
import requests
from modules import BaseModule
from utils.banner import print_result

class SocialIntelModule(BaseModule):
    """Query Reddit and GitHub public APIs for mentions."""
    def run(self) -> dict:
        results = {"target": self.target, "reddit": [], "github": []}
        self.info(f"[SOCIAL] Searching: {self.target}")
        # Reddit public search
        try:
            resp = requests.get(
                f"https://www.reddit.com/search.json?q={self.target}&limit=10",
                headers={"User-Agent": "EOTS-OSINT-Research/1.0"},
                timeout=self.config.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                posts = resp.json().get("data", {}).get("children", [])
                for p in posts:
                    d = p["data"]
                    results["reddit"].append({
                        "title": d.get("title"), "url": d.get("url"),
                        "subreddit": d.get("subreddit"),
                    })
                    print_result(f"r/{d.get('subreddit')}", d.get("title","")[:60], color="yellow")
        except Exception as e:
            self.warn(f"Reddit error: {e}")
        # GitHub public search
        try:
            resp = requests.get(
                f"https://api.github.com/search/repositories?q={self.target}&per_page=5",
                headers=self.config.REQUEST_HEADERS,
                timeout=self.config.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                items = resp.json().get("items", [])
                for repo in items:
                    results["github"].append({
                        "name": repo["full_name"], "url": repo["html_url"],
                        "stars": repo["stargazers_count"],
                    })
                    print_result("GitHub", repo["full_name"], color="cyan")
        except Exception as e:
            self.warn(f"GitHub error: {e}")
        return results
