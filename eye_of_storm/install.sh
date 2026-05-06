#!/usr/bin/env bash
# Eye of the Storm — One-Click Installer
# Tested on Kali Linux / Ubuntu 22.04+

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
cat << 'EOF'
  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
  Eye of the Storm — Installer
EOF
echo -e "${NC}"

echo -e "${YELLOW}[*] Checking Python version...${NC}"
python3 --version || { echo -e "${RED}Python 3.10+ required${NC}"; exit 1; }

echo -e "${YELLOW}[*] Installing system dependencies (requires sudo)...${NC}"
sudo apt-get update -qq
sudo apt-get install -y -qq nmap libimage-exiftool-perl dnsutils curl

echo -e "${YELLOW}[*] Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

echo -e "${YELLOW}[*] Upgrading pip...${NC}"
pip install --upgrade pip --quiet

echo -e "${YELLOW}[*] Installing Python dependencies...${NC}"
pip install -r requirements.txt --quiet

echo -e "${YELLOW}[*] Downloading spaCy NLP model...${NC}"
python3 -m spacy download en_core_web_sm --quiet

echo -e "${YELLOW}[*] Creating output directory...${NC}"
mkdir -p output

echo -e "${YELLOW}[*] Copying .env example...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}    → Edit .env to add your API keys${NC}"
fi

echo -e "${YELLOW}[*] Making launcher executable...${NC}"
chmod +x eots.sh

echo -e "${GREEN}"
echo "  ✓ Installation complete!"
echo "  ✓ Activate venv : source venv/bin/activate"
echo "  ✓ Run           : python3 main.py"
echo "  ✓ Or one-click  : ./eots.sh --target example.com --all"
echo -e "${NC}"
