<h1 align="center">👁️ EYE OF THE STORM (EOTS)</h1>
<h3 align="center"><em>Automated External Attack Surface Management (EASM) & OSINT Reconnaissance Engine</em></h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/AsyncIO-Powered-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Docker-FCC624?style=for-the-badge&logo=linux&logoColor=black"/>
  <img src="https://img.shields.io/badge/Compliance-ISO27001%20%7C%20NIS2%20%7C%20DORA-8A2BE2?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p align="center">
  <strong>Discover shadow assets, correlate threat intelligence, and audit digital footprints before threat actors do.</strong><br/>
  Built for IT Risk Analysts, Security Auditors, Penetration Testers, and Threat Intelligence Teams.
</p>

---

## 📋 Table of Contents

- [Why Eye of the Storm?](#-why-eye-of-the-storm)
- [Compliance Mapping](#️-governance--compliance-mapping)
- [Installation](#-installation)
- [Usage](#-cli-usage--workflows)
- [Modules Overview](#-modules-overview)
- [API Configuration](#-api-configuration-optional)

---

## ⚡ Why Eye of the Storm?

Modern organizations suffer from **Shadow IT** and sprawling external attack surfaces. Traditional reconnaissance requires chaining dozens of disjointed scripts and manual API queries. 

**Eye of the Storm (EOTS)** unifies **16 specialized reconnaissance and intelligence modules** into a single, asynchronous Python engine:
* **⚡ High-Concurrency Engine:** Powered by `asyncio` and `aiohttp` for rapid non-blocking network and API harvesting.
* **🧠 AI/NLP Entity Extraction:** Automatically parses scraped web content using `spaCy` to identify organizations, personnel, and leaked contact vectors.
* **🛡️ Graceful Degradation:** Operates out-of-the-box using passive sources, while seamlessly scaling up when optional CTI API keys (Shodan, VirusTotal, AbuseIPDB, HIBP) are provided.
* **📊 Executive-Ready Deliverables:** Generates structured **JSON** for SIEM/SOAR ingestion and clean **HTML reports** for risk committees and audit evidence.

---

## 🛡️ Governance & Compliance Mapping

| Framework / Standard | Control / Article | How EOTS Assists Auditors & Security Teams |
| :--- | :--- | :--- |
| **ISO/IEC 27001:2022** | **Control A.5.7** *(Threat Intelligence)* | Automates the collection and correlation of tactical threat intelligence. |
| **ISO/IEC 27001:2022** | **Control A.8.9 & A.5.9** *(Asset Inventory)* | Identifies undocumented internet-facing assets and forgotten subdomains. |
| **DORA (EU Regulation)** | **Art. 8** *(Identification)* & **Art. 28** *(Third-Party)* | Enables rapid external footprint assessment of critical ICT third-party providers. |
| **NIS 2 Directive** | **Art. 21** *(Supply Chain Security)* | Verifies external DNS hygiene, mail security records, and public credential leaks. |

---

## 📦 Installation

### Quick Automated Setup (Linux / Kali / Ubuntu)
```bash
git clone [https://github.com/samyvenom69/eye-of-the-storm.git](https://github.com/samyvenom69/eye-of-the-storm.git)
cd eye-of-the-storm
chmod +x install.sh eots.sh
./install.sh
