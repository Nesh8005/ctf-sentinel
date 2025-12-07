#!/bin/bash
# CTF Sentinel - Post-Clone Setup Script
# Run this after: git clone <your-repo-url>

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║              🔍 CTF SENTINEL 🔍                           ║
║         AI-Enhanced OSINT for Kali Linux                  ║
║                                                           ║
║              Post-Clone Setup                             ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${GREEN}Setting up CTF Sentinel...${NC}\n"

# Check if running on Kali or Linux
if [ ! -f /etc/os-release ]; then
    echo -e "${RED}Cannot detect OS. This script is for Linux/Kali.${NC}"
    exit 1
fi

# Step 1: Create virtual environment
echo -e "${CYAN}[1/6] Creating virtual environment...${NC}"
python3 -m venv venv
echo -e "${GREEN}✓ Virtual environment created${NC}\n"

# Step 2: Activate venv
echo -e "${CYAN}[2/6] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}\n"

# Step 3: Install Python packages
echo -e "${CYAN}[3/6] Installing Python packages...${NC}"
pip3 install --upgrade pip
pip3 install -r requirements.txt
echo -e "${GREEN}✓ Python packages installed${NC}\n"

# Step 4: Download spaCy model
echo -e "${CYAN}[4/6] Downloading spaCy NLP model...${NC}"
python3 -m spacy download en_core_web_sm
echo -e "${GREEN}✓ spaCy model downloaded${NC}\n"

# Step 5: Install external tools
echo -e "${CYAN}[5/6] Installing external OSINT tools...${NC}"
echo -e "${YELLOW}This requires sudo privileges...${NC}"

sudo apt update -qq

echo -e "  → Installing Amass..."
sudo apt install -y amass 2>/dev/null && echo -e "${GREEN}  ✓ Amass installed${NC}" || echo -e "${YELLOW}  ! Amass skipped${NC}"

echo -e "  → Installing Sublist3r..."
sudo apt install -y sublist3r 2>/dev/null && echo -e "${GREEN}  ✓ Sublist3r installed${NC}" || echo -e "${YELLOW}  ! Sublist3r skipped${NC}"

echo -e "  → Installing Nmap..."
sudo apt install -y nmap 2>/dev/null && echo -e "${GREEN}  ✓ Nmap installed${NC}" || echo -e "${YELLOW}  ! Nmap skipped${NC}"

echo -e "  → Installing DNS tools..."
sudo apt install -y dnsutils whois 2>/dev/null && echo -e "${GREEN}  ✓ DNS tools installed${NC}" || echo -e "${YELLOW}  ! DNS tools skipped${NC}"

echo -e "  → Installing ExifTool..."
sudo apt install -y libimage-exiftool-perl 2>/dev/null && echo -e "${GREEN}  ✓ ExifTool installed${NC}" || echo -e "${YELLOW}  ! ExifTool skipped${NC}"

echo -e "  → Installing Sherlock..."
pip3 install sherlock-project && echo -e "${GREEN}  ✓ Sherlock installed${NC}" || echo -e "${YELLOW}  ! Sherlock skipped${NC}"

echo -e "${GREEN}✓ External tools setup complete${NC}\n"

# Step 6: Verify installation
echo -e "${CYAN}[6/6] Verifying installation...${NC}"
python3 demo.py

echo -e "\n${GREEN}════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓✓✓ Setup Complete! ✓✓✓${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════${NC}\n"

echo -e "${CYAN}Quick Start:${NC}"
echo -e "  ${YELLOW}source venv/bin/activate${NC}  # Activate environment"
echo -e "  ${YELLOW}python3 main.py --target-type domain --value example.com${NC}"
echo -e ""
echo -e "${CYAN}Create alias (optional):${NC}"
echo -e "  ${YELLOW}echo \"alias ctf-sentinel='source $(pwd)/venv/bin/activate && python3 $(pwd)/main.py'\" >> ~/.bashrc${NC}"
echo -e ""
echo -e "${GREEN}🐉 Happy Hunting! 🔍${NC}\n"
