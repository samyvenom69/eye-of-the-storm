"""
Username Reconnaissance Module
Phase: INVESTIGATE
Inspired by Sherlock — searches public platforms concurrently.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from modules import BaseModule
from utils.banner import console, print_result
from utils.http import make_session

PLATFORMS = {
    "GitHub":     "https://github.com/{}",
    "Gitlab":     "https://gitlab.com/{}",
    "Twitter":    "https://twitter.com/{}",
    "Instagram":  "https://www.instagram.com/{}/",
    "Reddit":     "https://www.reddit.com/user/{}/",
    "TikTok":     "https://www.tiktok.com/@{}",
    "LinkedIn":   "https://www.linkedin.com/in/{}/",
    "YouTube":    "https://www.youtube.com/@{}",
    "Twitch":     "https://www.twitch.tv/{}",
    "Pinterest":  "https://www.pinterest.com/{}/",
    "Telegram":   "https://t.me/{}",
    "Medium":     "https://medium.com/@{}",
    "DevTo":      "https://dev.to/{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Keybase":    "https://keybase.io/{}",
    "Steam":      "https://steamcommunity.com/id/{}",
    "DockerHub":  "https://hub.docker.com/u/{}",
    "NPMjs":      "https://www.npmjs.com/~{}",
    "Pastebin":   "https://pastebin.com/u/{}",
    "Bitbucket":  "https://bitbucket.org/{}/",
    "Flickr":     "https://www.flickr.com/people/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Spotify":    "https://open.spotify.com/user/{}",
    "Vimeo":      "https://vimeo.com/{}",
    "Behance":    "https://www.behance.net/{}",
    "Dribbble":   "https://dribbble.com/{}",
    "Replit":     "https://replit.com/@{}",
    "Kaggle":     "https://www.kaggle.com/{}",
    "Disqus":     "https://disqus.com/by/{}/",
    "Gravatar":   "https://en.gravatar.com/{}",
    "AboutMe":    "https://about.me/{}",
    "Patreon":    "https://www.patreon.com/{}",
    "Kickstarter": "https://www.kickstarter.com/profile/{}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "Wikipedia":  "https://en.wikipedia.org/wiki/User:{}",
}


class UsernameReconModule(BaseModule):
    """Search for a username across public platforms concurrently."""

    WORKERS = 20

    def run(self) -> dict:
        username = self.target.lstrip("@")
        results = {"username": username, "found": [], "not_found": [], "errors": []}

        self.info(f"[USERNAME] Checking: {username} across {len(PLATFORMS)} platforms")

        session = make_session(self.config, pool_size=self.WORKERS)

        def check(platform, url_template):
            url = url_template.format(username)
            try:
                resp = session.get(url, timeout=self.config.REQUEST_TIMEOUT)
                if resp.status_code == 200:
                    return ("found", platform, url)
                return ("not_found", platform, url)
            except Exception as e:
                return ("error", platform, str(e))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task(
                f"[blue]Scanning {len(PLATFORMS)} platforms…[/blue]",
                total=len(PLATFORMS),
            )
            with ThreadPoolExecutor(max_workers=self.WORKERS) as ex:
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
                    progress.advance(task)

        self.info(f"Found on {len(results['found'])} platforms.")
        return results
