"""
Username Reconnaissance Module
Phase: INVESTIGATE
Inspired by Sherlock — searches public platforms concurrently (async engine).
"""

import asyncio

import aiohttp
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from modules import BaseModule
from utils.banner import console, print_result

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

RETRY_STATUS = {429, 500, 502, 503, 504}


class UsernameReconModule(BaseModule):
    """Search for a username across public platforms concurrently (asyncio + aiohttp)."""

    CONCURRENCY = 25
    MAX_RETRIES = 2

    def run(self) -> dict:
        username = self.target.lstrip("@")
        results = {"username": username, "found": [], "not_found": [], "errors": []}

        self.info(f"[USERNAME] Checking: {username} across {len(PLATFORMS)} platforms (async engine)")

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

            def on_result(status, platform, info):
                if status == "found":
                    results["found"].append({"platform": platform, "url": info})
                    print_result(f"  ✓ {platform}", info, color="green")
                elif status == "error":
                    results["errors"].append({"platform": platform, "error": info})
                else:
                    results["not_found"].append(platform)
                progress.advance(task)

            asyncio.run(self._scan(username, on_result))

        self.info(f"Found on {len(results['found'])} platforms.")
        return results

    # ------------------------------------------------------------------ #

    async def _scan(self, username: str, on_result):
        timeout = aiohttp.ClientTimeout(total=self.config.REQUEST_TIMEOUT)
        connector = aiohttp.TCPConnector(limit=self.CONCURRENCY)
        semaphore = asyncio.Semaphore(self.CONCURRENCY)

        async with aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers=self.config.REQUEST_HEADERS,
        ) as session:
            checks = [
                self._check(session, semaphore, platform, tpl.format(username))
                for platform, tpl in PLATFORMS.items()
            ]
            for coro in asyncio.as_completed(checks):
                status, platform, info = await coro
                on_result(status, platform, info)

    async def _check(self, session, semaphore, name, url):
        async with semaphore:
            for attempt in range(self.MAX_RETRIES + 1):
                try:
                    async with session.get(url, allow_redirects=True) as resp:
                        if resp.status in RETRY_STATUS and attempt < self.MAX_RETRIES:
                            await asyncio.sleep(0.5 * (attempt + 1))
                            continue
                        if resp.status == 200:
                            return ("found", name, url)
                        return ("not_found", name, url)
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    if attempt < self.MAX_RETRIES:
                        await asyncio.sleep(0.5 * (attempt + 1))
                        continue
                    return ("error", name, str(e))
        return ("error", name, "unreachable")
