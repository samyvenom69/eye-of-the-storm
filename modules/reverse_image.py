"""Reverse Image Search — Phase: ANALYSE"""
from modules import BaseModule
from utils.banner import print_result

class ReverseImageModule(BaseModule):
    """Generate reverse image search URLs for multiple engines."""
    def run(self) -> dict:
        url = self.target
        results = {"image": url, "search_urls": {}}
        engines = {
            "Google Images": f"https://www.google.com/searchbyimage?image_url={url}",
            "Bing Images":   f"https://www.bing.com/images/search?view=detailv2&iss=sbi&form=SBIHMP&q=imgurl:{url}",
            "TinEye":        f"https://tineye.com/search?url={url}",
            "Yandex Images": f"https://yandex.com/images/search?rpt=imageview&url={url}",
        }
        results["search_urls"] = engines
        for engine, link in engines.items():
            print_result(engine, link, color="cyan")
        return results
