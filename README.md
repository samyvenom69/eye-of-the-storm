# 👁️ EYE OF THE STORM (EOTS)
**Automated External Attack Surface Management (EASM) & OSINT Reconnaissance Engine**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Compliance: ISO27001 | NIS2 | DORA](https://img.shields.io/badge/Compliance-ISO27001%20%7C%20NIS2%20%7C%20DORA-8A2BE2?style=for-the-badge)]()

Discover shadow assets, correlate threat intelligence, and audit digital footprints before threat actors do. Built for IT Risk Analysts, Security Auditors, Penetration Testers, and Threat Intelligence Teams.

---

## ⚡ Why Eye of the Storm?
Modern organizations suffer from Shadow IT and sprawling external attack surfaces. EOTS unifies 16 specialized reconnaissance modules into a single asynchronous Python engine:
- **High-Concurrency Engine:** Powered by `asyncio` and `aiohttp` for rapid non-blocking harvesting.
- **AI/NLP Entity Extraction:** Automatically parses scraped web content using `spaCy` to identify organizations, personnel, and leaked contact vectors.
- **Graceful Degradation:** Operates out-of-the-box using passive sources, while seamlessly scaling when CTI API keys (Shodan, VirusTotal, AbuseIPDB, HIBP) are provided.
- **Executive Deliverables:** Generates structured JSON for SIEM ingestion and clean HTML reports for risk committees.

---

## 🛡️ Governance & Compliance Mapping
- **ISO/IEC 27001:2022 (Control A.5.7 - Threat Intelligence):** Automates collection and correlation of tactical threat intelligence.
- **ISO/IEC 27001:2022 (Control A.8.9 & A.5.9 - Asset Inventory):** Identifies undocumented internet-facing assets and forgotten subdomains.
- **DORA Regulation (Art. 8 & 28):** Enables rapid external footprint assessment of critical ICT third-party providers.
- **NIS 2 Directive (Art. 21 - Supply Chain Security):** Verifies external DNS hygiene, mail security records, and public credential leaks.

---

## 📦 Installation
1. Clone the repository: `git clone [https://github.com/samyvenom69/eye-of-the-storm.git](https://github.com/samyvenom69/eye-of-the-storm.git)`
2. Enter directory: `cd eye-of-the-storm`
3. Run the automated installer: `./install.sh` (or set up manually using a Python virtual environment and `pip install -r requirements.txt`).

---

## 🚀 Usage & Quick Start
- Run interactive menu: `python3 main.py`
- Full automated reconnaissance pipeline: `./eots.sh --target example.com --all --report`
- Run a specific module: `./eots.sh --module email --target user@example.com`

---

## 🧩 Modules Overview
- **RECON (Phase 1):** WHOIS, DNS records, Subdomain enumeration, IP Geolocation/ASN, Nmap port scanning, and file metadata extraction (`PDF`, `DOCX`, `XLSX`).
- **INVESTIGATE (Phase 2):** Username search across 150+ platforms, email breach checks (HIBP), phone carrier intelligence, EXIF GPS coordinates, and Google Dorking.
- **ANALYSE (Phase 3):** Web scraping with `spaCy` NLP entity extraction, Wayback Machine historical snapshots, and reverse image intelligence.
- **INTELLIGENCE (Phase 4):** IOC reputation cross-checking via VirusTotal & AbuseIPDB, public data mining, and automated HTML/JSON report generation.

---

## 🔑 API Configuration (Optional)
Copy `.env.example` to `.env` and configure your optional API keys for Shodan, VirusTotal, AbuseIPDB, HIBP, and Ipinfo.

---

## 👤 Author
**Samir K.** (`samyvenom69`) — IT Risk & Cybersecurity Specialist | CNAM Paris
