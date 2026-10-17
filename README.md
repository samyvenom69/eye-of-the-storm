<p align="center">
  <img src="assets/banner.svg" alt="Eye of the Storm" width="100%"/>
</p>

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

<p align="center">
  <a href="#-architecture--workflow">Architecture</a> •
  <a href="#-governance--compliance-mapping">Compliance Mapping</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-cli-usage--workflows">Usage</a> •
  <a href="#-modules-ecosystem">Modules</a>
</p>

---

## ⚡ Why Eye of the Storm?

Modern organizations suffer from **Shadow IT** and sprawling external attack surfaces. Traditional reconnaissance requires chaining dozens of disjointed scripts and manual API queries. 

**Eye of the Storm (EOTS)** unifies **16 specialized reconnaissance and intelligence modules** into a single, asynchronous Python engine:
* **⚡ High-Concurrency Engine:** Powered by `asyncio` and `aiohttp` for rapid non-blocking network and API harvesting.
* **🧠 AI/NLP Entity Extraction:** Automatically parses scraped web content using `spaCy` to identify organizations, personnel, and leaked contact vectors.
* **🛡️ Graceful Degradation:** Operates out-of-the-box using passive sources, while seamlessly scaling up when optional CTI API keys (Shodan, VirusTotal, AbuseIPDB, HIBP) are provided.
* **📊 Executive-Ready Deliverables:** Generates structured **JSON** for SIEM/SOAR ingestion and clean **HTML/PDF reports** for risk committees and audit evidence.

---

## 🏗️ Architecture & Workflow

EOTS structures reconnaissance into a standardized 4-stage intelligence lifecycle:

```mermaid
graph LR
    A[🎯 Target Input<br/>Domain / IP / Email / User] --> B(🔎 1. RECON<br/>Passive & Active Discovery)
    B --> C(🔬 2. INVESTIGATE<br/>Identity & Breach Correlation)
    C --> D(📊 3. ANALYSE<br/>NLP, EXIF & Historical Snapshots)
    D --> E(🧠 4. INTELLIGENCE<br/>CTI Feeds & Risk Scoring)
    E --> F[📄 Output Engine<br/>Rich CLI / JSON / HTML Report]

    style A fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#fff
    style B fill:#0f172a,stroke:#64748b,stroke-width:1px,color:#e2e8f0
    style C fill:#0f172a,stroke:#64748b,stroke-width:1px,color:#e2e8f0
    style D fill:#0f172a,stroke:#64748b,stroke-width:1px,color:#e2e8f0
    style E fill:#0f172a,stroke:#64748b,stroke-width:1px,color:#e2e8f0
    style F fill:#065f46,stroke:#34d399,stroke-width:2px,color:#fff