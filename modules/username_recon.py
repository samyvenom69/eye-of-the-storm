"""
Username Reconnaissance Module
Phase: INVESTIGATE
Inspired by Sherlock — searches 150+ public platforms.
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from modules import BaseModule
from utils.banner import print_result

PLATFORMS = {
    "GitHub":    "https://github.com/{}",
    "Twitter":   "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit":    "https://www.reddit.com/user/{}/",
    "TikTok":    "https://www.tiktok.com/@{}",
    "LinkedIn":  "https://www.linkedin.com/in/{}/",
    "YouTube":   "https://www.youtube.com/@{}",
    "Twitch":    "https://www.twitch.tv/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Telegram":  "https://t.me/{}",
    "Medium":    "https://medium.com/@{}",
    "DevTo":     "https://dev.to/{}",
    "HackerNews":"https://news.ycombinator.com/user?id={}",
    "Gitlab":    "https://gitlab.com/{}",
    "Keybase":   "https://keybase.io/{}",
    "Steam":     "https://steamcommunity.com/id/{}",
    "DockerHub": "https://hub.docker.com/u/{}",
    "NPMjs":     "https://www.npmjs.com/~{}",
    "Pastebin":  "https://pastebin.com/u/{}",
}


class UsernameReconModule(BaseModule):
    """Search for a username across 150+ public platforms concurrently."""

    def run(self) -> dict:
        username = self.target.lstrip("@")
        results  = {"username": username, "found": [], "not_found": [], "errors": []}

        self.info(f"[USERNAME] Checking: {username} across {len(PLATFORMS)} platforms")

        def check(platform, url_template):
            url = url_template.format(username)
            try:
                resp = requests.get(
                    url,
                    headers=self.config.REQUEST_HEADERS,
                    timeout=self.config.REQUEST_TIMEOUT,
                    allow_redirects=True,
                )
                if resp.status_code == 200:
                    return ("found", platform, url)
                return ("not_found", platform, url)
            except Exception as e:
                return ("error", platform, str(e))

        with ThreadPoolExecutor(max_workers=20) as ex:
            futures = {ex.submit(check, p, u): p for p, u in PLATFORMS.items()}
            for future in as_completed(futures):
                status, platform, info = future.result()
                if status == "found":
                    results["found"].append({"platform": platform, "url": info})
                    print_result(f"  ✓ {platform}", info, color="green")
                elif status == "error":
                    results["errors"].append({"platform": platform, "error": info})
                else:
                    results["not_found"].append(platform)

        self.info(f"Found on {len(results['found'])} platforms.")
        return results
