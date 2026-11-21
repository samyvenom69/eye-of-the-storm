<div align="center">

<img src="assets/banner.svg" width="100%" alt="Eye of the Storm Banner">

# 👁️ EYE OF THE STORM (EOTS)
### *Automated External Attack Surface Management & OSINT Reconnaissance Framework*

[![CI](https://github.com/samyvenom69/eye-of-the-storm/actions/workflows/ci.yml/badge.svg)](https://github.com/samyvenom69/eye-of-the-storm/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Compliance: ISO27001 | NIS2 | DORA](https://img.shields.io/badge/Compliance-ISO27001%20%7C%20NIS2%20%7C%20DORA-8A2BE2?style=for-the-badge)]()
<br/>
[![Stars](https://img.shields.io/github/stars/samyvenom69/eye-of-the-storm?style=social)](https://github.com/samyvenom69/eye-of-the-storm/stargazers)
[![Forks](https://img.shields.io/github/forks/samyvenom69/eye-of-the-storm?style=social)](https://github.com/samyvenom69/eye-of-the-storm/network/members)
[![Last commit](https://img.shields.io/github/last-commit/samyvenom69/eye-of-the-storm)](https://github.com/samyvenom69/eye-of-the-storm/commits/main)

</div>

---

Discover shadow assets, correlate threat intelligence, and audit digital footprints before threat actors do. Built for IT Risk Analysts, Security Auditors, Penetration Testers, and Threat Intelligence Teams.

## 📑 Table of Contents
- [Why Eye of the Storm?](#️-why-eye-of-the-storm)
- [Performance](#-performance)
- [Governance & Compliance Mapping](#️-governance--compliance-mapping)
- [Installation](#-installation)
- [Usage & Quick Start](#-usage--quick-start)
- [Modules Overview](#-modules-overview)
- [API Configuration](#-api-configuration-optional)
- [Roadmap](#️-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## ⚡ Why Eye of the Storm?
Modern organizations suffer from Shadow IT and sprawling external attack surfaces. EOTS unifies 16 specialized reconnaissance modules into a single high-performance Python engine:
- **Parallel Execution Engine:** Independent modules run concurrently (thread pool), cutting multi-module scan times dramatically.
- **High-Concurrency Harvesting:** DNS brute-force and username recon run dozens of workers with connection pooling, automatic retries and exponential backoff.
- **AI/NLP Entity Extraction:** Automatically parses scraped web content using `spaCy` to identify organizations, personnel, and leaked contact vectors.
- **Graceful Degradation:** Operates out-of-the-box using passive sources, while seamlessly scaling when CTI API keys (Shodan, VirusTotal, AbuseIPDB, HIBP) are provided.
- **Executive Deliverables:** Generates structured JSON for SIEM ingestion and polished dark-theme HTML reports for risk committees.

---

## 🚀 Performance
| Optimization | Impact |
|---|---|
| Parallel module engine (`--jobs N`) | Modules no longer run one after another — wall-clock time ≈ slowest module |
| Lazy module imports (`importlib`) | Startup stays fast; heavy deps like `spaCy` load only when used |
| Parallel DNS brute-force (40 workers) | Subdomain enumeration no longer resolves names sequentially |
| Shared `requests.Session` + retries/backoff | Fewer dropped requests, resilience to rate limits (HTTP 429/5xx) |
| Live progress bars & spinners (`rich`) | Real-time feedback on long-running scans |

---

## 🛡️ Governance & Compliance Mapping
- **ISO/IEC 27001:2022 (Control A.5.7 - Threat Intelligence):** Automates collection and correlation of tactical threat intelligence.
- **ISO/IEC 27001:2022 (Control A.8.9 & A.5.9 - Asset Inventory):** Identifies undocumented internet-facing assets and forgotten subdomains.
- **DORA Regulation (Art. 8 & 28):** Enables rapid external footprint assessment of critical ICT third-party providers.
- **NIS 2 Directive (Art. 21 - Supply Chain Security):** Verifies external DNS hygiene, mail security records, and public credential leaks.

---

## 📦 Installation
1. Clone the repository: `git clone https://github.com/samyvenom69/eye-of-the-storm.git`
2. Enter directory: `cd eye-of-the-storm`
3. Run the automated installer: `./install.sh` (or set up manually using a Python virtual environment and `pip install -r requirements.txt`).

---

## 🚀 Usage & Quick Start
- Run interactive menu: `python3 main.py`
- Full automated reconnaissance pipeline: `./eots.sh --target example.com --all --report`
- Run a specific module: `./eots.sh --module email --target user@example.com`
- Speed up multi-module runs: `./eots.sh --target example.com --all --jobs 8`
- Sequential (legacy) mode: `--jobs 1`

---

## 🧩 Modules Overview
| Phase | Flag | Capability |
|---|---|---|
| 🟦 RECON | `whois` | WHOIS lookup & DNS records (A, MX, NS, TXT, CNAME) |
| 🟦 RECON | `subdomain` | Subdomain enumeration (crt.sh + parallel wordlist brute-force) |
| 🟦 RECON | `ip` | IP geolocation, ASN, abuse score, reverse DNS |
| 🟦 RECON | `portscan` | TCP/UDP port scanning via Nmap integration |
| 🟦 RECON | `metadata` | Extract metadata from PDF, DOCX, XLSX, images |
| 🟪 INVESTIGATE | `username` | Username lookup across 30+ platforms (concurrent) |
| 🟪 INVESTIGATE | `email` | Breach detection, paste leaks, email validation |
| 🟪 INVESTIGATE | `phone` | Carrier, region, timezone, number validation |
| 🟪 INVESTIGATE | `exif` | Extract GPS coordinates & EXIF from images |
| 🟪 INVESTIGATE | `dork` | Automated Google Dorking query templates |
| 🟨 ANALYSE | `scrape` | Website crawling + `spaCy` NLP entity extraction |
| 🟨 ANALYSE | `wayback` | Wayback Machine historical snapshot analysis |
| 🟨 ANALYSE | `revimg` | Reverse image search correlation |
| 🟨 ANALYSE | `geoint` | GEOINT coordinate analysis & satellite links |
| 🟥 INTELLIGENCE | `threat` | Threat intelligence feeds (VirusTotal, AbuseIPDB) |
| 🟥 INTELLIGENCE | `social` | Reddit & GitHub public data intelligence |
| 🟩 INTELLIGENCE | `report` | HTML / JSON executive report generation |

---

## 🔑 API Configuration (Optional)
Copy `.env.example` to `.env` and configure your optional API keys for Shodan, VirusTotal, AbuseIPDB, HIBP, and Ipinfo.

---

## 🗺️ Roadmap
- [x] Parallel module execution engine
- [x] Retries & exponential backoff on HTTP calls
- [x] Redesigned executive HTML report
- [ ] Async (`aiohttp`) migration of network-heavy modules
- [ ] Result diffing between two scans (attack-surface drift)
- [ ] Docker image & `pipx` installation
- [ ] Optional SQLite history of past scans

---

## 🤝 Contributing
Issues and pull requests are welcome. Please run `ruff check .` before submitting, and make sure the CI workflow stays green.

---

## 📜 License
Distributed under the [MIT License](LICENSE).

> ⚠️ **Legal notice:** EOTS is intended for authorized security assessments and research only. Always obtain written permission before scanning systems you do not own.

---

## 👤 Author
**Samir K.** (`samyvenom69`) — IT Risk & Cybersecurity Specialist | CNAM Paris
