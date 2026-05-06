"""Eye of the Storm — Configuration."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    IPINFO_TOKEN      = os.getenv("IPINFO_TOKEN", "")
    ABUSEIPDB_KEY     = os.getenv("ABUSEIPDB_KEY", "")
    HIBP_API_KEY      = os.getenv("HIBP_API_KEY", "")
    SHODAN_API_KEY    = os.getenv("SHODAN_API_KEY", "")
    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")

    REQUEST_TIMEOUT = 10
    REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (compatible; EOTS-OSINT-Research/1.0)"
    }
    OUTPUT_DIR    = "output"
    WORDLIST_PATH = "wordlists/subdomains.txt"
