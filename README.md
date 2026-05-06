
<p align="center">
  <img src="assets/banner.svg" alt="Eye of the Storm" width="100%"/>
</p>

<h1 align="center">👁️ EYE OF THE STORM</h1>
<h3 align="center"><em>Stay vigilant. Follow the trace of everything.</em></h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=for-the-badge&logo=linux&logoColor=white"/>
  <img src="https://img.shields.io/badge/Purpose-Educational-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
</p>

<p align="center">
  <strong>Advanced OSINT Reconnaissance Framework</strong><br/>
  A modular, educational open-source intelligence (OSINT) platform built in Python.<br/>
  Designed for security researchers, students, and ethical investigators.
</p>

---

```
  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
  [ 1-RECON ] → [ 2-INVESTIGATE ] → [ 3-ANALYSE ] → [ 4-INTELLIGENCE ]
```

---

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [API Keys](#api-keys-optional-modules)
- [Modules Overview](#modules-overview)
- [Ethical Use](#ethical-use)
- [Disclaimer](#disclaimer)
- [Author](#author)
- [Support](#support)

---

## 🔍 Overview

**Eye of the Storm** is an educational OSINT (Open Source Intelligence) framework that aggregates multiple reconnaissance techniques into a single, modular Python tool. It is designed for cybersecurity students and ethical investigators who need to gather publicly available information during authorized assessments.

The framework follows a 4-phase methodology:

| Phase | Description |
|-------|-------------|
| 🔎 **RECON** | Passive data collection – DNS, WHOIS, subdomains, IP, metadata |
| 🔬 **INVESTIGATE** | Active correlation – emails, usernames, social, breach data |
| 📊 **ANALYSE** | Data processing – NLP entity extraction, geolocation, image analysis |
| 🧠 **INTELLIGENCE** | Synthesis – threat feeds, network scanning, reporting |

---

## 📦 Installation

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/samyvenom69/eye-of-the-storm.git
cd eye-of-the-storm

# Run the one-click installer
chmod +x install.sh
./install.sh
```

### Manual Setup

```bash
# 1. Ensure Python 3.10+ is installed
python3 --version

# 2. Clone the project
git clone https://github.com/samyvenom69/eye-of-the-storm.git
cd eye-of-the-storm

# 3. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate       # Linux / macOS
# venv\Scripts\activate        # Windows

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Install NLP model (for entity extraction module)
python3 -m spacy download en_core_web_sm

# 6. (Optional) Install system tools for extended modules
sudo apt-get update
sudo apt-get install -y nmap exiftool dnsutils curl
```

---

## 🚀 Usage

### Standard Run (Recommended)

```bash
# Activate your virtual environment first
source venv/bin/activate

# Launch interactive menu
python3 main.py

# Run a specific module
python3 main.py --module whois --target example.com

# Run full recon pipeline on a domain
python3 main.py --target example.com --full-recon

# Export results to JSON
python3 main.py --target example.com --full-recon --output json

# Export results to HTML report
python3 main.py --target example.com --full-recon --output html
```

### Advanced Run (No activation required)

```bash
# Using the wrapper script (manages venv automatically)
./eots.sh --module email --target user@example.com

# Run with verbose output
./eots.sh --target example.com --module dns --verbose

# Chain multiple modules
./eots.sh --target example.com --modules whois,dns,subdomain,ip

# Run with custom wordlist
./eots.sh --target example.com --module subdomain --wordlist wordlists/custom.txt
```

### One-Click Execution (Best)

```bash
# Full automated pipeline — all modules, HTML report generated
./eots.sh --target example.com --all --report
```

### `requirements.txt`

```
# Core Network & Speed
aiohttp
asyncio
requests

# CLI Interface (The "Wow" Factor)
rich
python-dotenv
argparse

# Data Processing
beautifulsoup4
lxml
phonenumbers

# Metadata & DNS
Pillow
exifread
dnspython
python-whois
```

---

## 🔑 API Keys (Optional Modules)

Some features require external APIs. All are **optional** — the framework degrades gracefully without them.

| Module | Service | Free Tier | Get Key |
|--------|---------|-----------|---------|
| IP Geolocation | ipinfo.io | 50k req/month | [ipinfo.io/account](https://ipinfo.io/account) |
| Threat Intelligence | AbuseIPDB | 1000 req/day | [abuseipdb.com](https://www.abuseipdb.com) |
| Email Breach | HaveIBeenPwned | Paid API | [haveibeenpwned.com/API](https://haveibeenpwned.com/API) |
| Network Scan | Shodan | Free (limited) | [shodan.io](https://shodan.io) |
| Threat Feeds | VirusTotal | 4 req/min | [virustotal.com](https://www.virustotal.com) |

### Set environment variables

```bash
# Copy the example file
cp .env.example .env

# Edit and add your keys
nano .env
```

**.env.example**

```env
# Eye of the Storm — API Configuration

IPINFO_TOKEN=your_ipinfo_token_here
ABUSEIPDB_KEY=your_abuseipdb_key_here
HIBP_API_KEY=your_hibp_api_key_here
SHODAN_API_KEY=your_shodan_api_key_here
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
```

---

## 🧩 Modules Overview

### 📍 Phase 1 — RECON

| Module | Flag | Description |
|--------|------|-------------|
| `whois_dns` | `--module whois` | WHOIS lookup, DNS records (A, MX, NS, TXT, CNAME) |
| `subdomain` | `--module subdomain` | Subdomain enumeration via wordlist + certificate transparency |
| `ip_geo` | `--module ip` | IP geolocation, ASN, abuse score, reverse DNS |
| `port_scan` | `--module portscan` | TCP/UDP port scanning via Nmap integration |
| `file_metadata` | `--module metadata` | Extract metadata from PDF, DOCX, XLSX, images |

### 🔬 Phase 2 — INVESTIGATE

| Module | Flag | Description |
|--------|------|-------------|
| `username_recon` | `--module username` | Username lookup across 150+ platforms |
| `email_breach` | `--module email` | Breach detection, paste leaks, email validation |
| `phone_intel` | `--module phone` | Carrier, region, line type, number validation |
| `exif_gps` | `--module exif` | Extract GPS coordinates and metadata from images |
| `google_dork` | `--module dork` | Automated Google Dorking with curated query templates |

### 📊 Phase 3 — ANALYSE

| Module | Flag | Description |
|--------|------|-------------|
| `web_scraper` | `--module scrape` | Website crawling + NLP entity extraction (names, orgs, emails) |
| `wayback` | `--module wayback` | Wayback Machine historical snapshot analysis |
| `reverse_image` | `--module revimg` | Reverse image search via multiple engines |
| `geoint` | `--module geoint` | GEOINT – coordinate analysis, satellite imagery links |

### 🧠 Phase 4 — INTELLIGENCE

| Module | Flag | Description |
|--------|------|-------------|
| `threat_intel` | `--module threat` | Threat intelligence feeds (VirusTotal, AbuseIPDB) |
| `social_intel` | `--module social` | Reddit & GitHub public data intelligence |
| `report` | `--module report` | HTML/JSON/PDF report generation |

---

## ⚖️ Ethical Use

Eye of the Storm is built for **legal, ethical, and authorized** use only.

**Acceptable use cases:**
- Academic research and cybersecurity coursework
- Authorized penetration testing engagements
- Investigating your own digital footprint
- Journalism and open-source investigations on public figures
- CTF (Capture The Flag) competitions
- Bug bounty programs within defined scope

**Unacceptable use:**
- Unauthorized investigation of private individuals
- Stalking, harassment, or doxing
- Corporate espionage
- Any activity that violates local or international law

> **Always obtain written permission before performing reconnaissance on systems or individuals you do not own.**

This tool is designed to promote education in the field of open-source intelligence and cybersecurity. Misuse of this framework is solely the responsibility of the user.

---

## ⚠️ Disclaimer

> **This tool is provided for educational and research purposes only.**
>
> The author assumes **no liability** for any misuse of this software. By using Eye of the Storm, you agree that you are solely responsible for your actions and that you will use this tool only in compliance with applicable laws and regulations.
>
> Some modules query third-party services. Respect their terms of service and rate limits.
>
> **The author does not condone, encourage, or support any form of unauthorized access or illegal activity.**

---

## 👤 Author

```
  Name    : samyvenom69
  GitHub  : github.com/samyvenom69
  Focus   : Cybersecurity | OSINT | Ethical Hacking | AI
  Studies : CNAM Of Paris / Cyber
```

---

## 💬 Support

Found a bug? Have a feature request?

- 🐛 Open an [Issue](https://github.com/samyvenom69/eye-of-the-storm/issues)
- 💡 Submit a [Pull Request](https://github.com/samyvenom69/eye-of-the-storm/pulls)
- ⭐ Star the repo if you find it useful!

---

<p align="center">
  Made with 🔍 for educational purposes &nbsp;|&nbsp; <em>Stay vigilant. Follow the trace of everything.</em>
</p>
