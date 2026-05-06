"""Web Scraper + NLP Entity Extraction — Phase: ANALYSE"""
import requests
from bs4 import BeautifulSoup
import spacy
from modules import BaseModule
from utils.banner import print_result

class WebScraperModule(BaseModule):
    """Scrape a public webpage and extract named entities (NLP)."""
    def run(self) -> dict:
        results = {"url": self.target, "entities": {}, "links": [], "emails": []}
        self.info(f"[SCRAPER] Crawling: {self.target}")
        try:
            resp = requests.get(self.target, headers=self.config.REQUEST_HEADERS,
                                timeout=self.config.REQUEST_TIMEOUT)
            soup = BeautifulSoup(resp.text, "lxml")
            text = soup.get_text(separator=" ", strip=True)
            results["links"] = list({a["href"] for a in soup.find_all("a", href=True)}[:30])
            import re
            results["emails"] = re.findall(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", text)
            try:
                nlp  = spacy.load("en_core_web_sm")
                doc  = nlp(text[:50000])
                for ent in doc.ents:
                    results["entities"].setdefault(ent.label_, [])
                    if ent.text not in results["entities"][ent.label_]:
                        results["entities"][ent.label_].append(ent.text)
                for label, items in results["entities"].items():
                    print_result(label, ", ".join(items[:5]), color="yellow")
            except OSError:
                self.warn("spaCy model not installed. Run: python -m spacy download en_core_web_sm")
        except Exception as e:
            self.error(str(e)); results["error"] = str(e)
        return results
