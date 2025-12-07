#!/bin/bash
# CTF Sentinel - Kali Linux Automated Setup Script
# This script automates the installation of CTF Sentinel and all dependencies on Kali Linux

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              🔍 CTF SENTINEL 🔍                           ║
║         AI-Enhanced OSINT for CTF Competitions            ║
║                                                           ║
║            Kali Linux Automated Setup                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running on Kali Linux
if [ ! -f /etc/os-release ] || ! grep -q "Kali" /etc/os-release; then
    echo -e "${YELLOW}Warning: This doesn't appear to be Kali Linux${NC}"
    echo -e "${YELLOW}The script will continue, but some tools may not be available${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for root privileges for apt operations
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}Note: Some operations require sudo privileges${NC}"
    echo -e "${YELLOW}You may be prompted for your password${NC}"
    echo
fi

# Update package lists
echo -e "${CYAN}[1/6] Updating package lists...${NC}"
sudo apt update

# Install Python3 and pip if not installed
echo -e "${CYAN}[2/6] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Installing Python3...${NC}"
    sudo apt install -y python3 python3-pip
else
    echo -e "${GREEN}✓ Python3 already installed: $(python3 --version)${NC}"
fi

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}Installing pip3...${NC}"
    sudo apt install -y python3-pip
fi

# Install Python dependencies
echo -e "${CYAN}[3/6] Installing Python packages...${NC}"
pip3 install -r requirements.txt

# Download spaCy language model
echo -e "${CYAN}[4/6] Downloading spaCy NLP model...${NC}"
python3 -m spacy download en_core_web_sm

# Install external OSINT tools
echo -e "${CYAN}[5/6] Installing external OSINT tools...${NC}"

echo -e "${YELLOW}  → Installing Amass (subdomain enumeration)...${NC}"
sudo apt install -y amass 2>/dev/null || echo -e "${RED}  ✗ Amass not available in repos${NC}"

echo -e "${YELLOW}  → Installing Sublist3r (subdomain enumeration)...${NC}"
sudo apt install -y sublist3r 2>/dev/null || echo -e "${RED}  ✗ Sublist3r not available in repos${NC}"

echo -e "${YELLOW}  → Installing Nmap (port scanning)...${NC}"
sudo apt install -y nmap 2>/dev/null || echo -e "${RED}  ✗ Nmap installation failed${NC}"

echo -e "${YELLOW}  → Installing DNS utilities (dig, whois)...${NC}"
sudo apt install -y dnsutils whois 2>/dev/null || echo -e "${RED}  ✗ DNS utils installation failed${NC}"

echo -e "${YELLOW}  → Installing ExifTool (metadata extraction)...${NC}"
sudo apt install -y libimage-exiftool-perl 2>/dev/null || echo -e "${RED}  ✗ ExifTool installation failed${NC}"

echo -e "${YELLOW}  → Installing Sherlock (username search)...${NC}"
pip3 install sherlock-project 2>/dev/null || echo -e "${RED}  ✗ Sherlock installation failed${NC}"

# Verify installation
echo -e "${CYAN}[6/6] Verifying installation...${NC}"
echo

# Check Python packages
if python3 -c "import spacy, rich, requests" 2>/dev/null; then
    echo -e "${GREEN}✓ Python packages installed successfully${NC}"
else
    echo -e "${RED}✗ Some Python packages failed to install${NC}"
fi

# Check spaCy model
if python3 -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
    echo -e "${GREEN}✓ spaCy model downloaded successfully${NC}"
else
    echo -e "${RED}✗ spaCy model download failed${NC}"
fi

# Check external tools
tools_found=0
tools_total=6

command -v amass &> /dev/null && echo -e "${GREEN}✓ Amass found${NC}" && ((tools_found++)) || echo -e "${YELLOW}! Amass not found (optional)${NC}"
command -v sublist3r &> /dev/null && echo -e "${GREEN}✓ Sublist3r found${NC}" && ((tools_found++)) || echo -e "${YELLOW}! Sublist3r not found (optional)${NC}"
command -v sherlock &> /dev/null && echo -e "${GREEN}✓ Sherlock found${NC}" && ((tools_found++)) || echo -e "${YELLOW}! Sherlock not found (optional)${NC}"
command -v exiftool &> /dev/null && echo -e "${GREEN}✓ ExifTool found${NC}" && ((tools_found++)) || echo -e "${YELLOW}! ExifTool not found (optional)${NC}"
command -v nmap &> /dev/null && echo -e "${GREEN}✓ Nmap found${NC}" && ((tools_found++)) || echo -e "${YELLOW}! Nmap not found (optional)${NC}"
command -v dig &> /dev/null && echo -e "${GREEN}✓ dig found${NC}" && ((tools_found++)) || echo -e "${YELLOW}! dig not found (optional)${NC}"

echo
echo -e "${CYAN}External tools: ${tools_found}/${tools_total} found${NC}"
echo

# Run demo
echo -e "${CYAN}Running demo to verify installation...${NC}"
echo
if python3 demo.py; then
    echo
    echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓✓✓ Installation Complete! ✓✓✓${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
else
    echo
    echo -e "${YELLOW}════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}⚠ Installation complete with warnings${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════${NC}"
fi

echo
echo -e "${CYAN}Next Steps:${NC}"
echo -e "  1. Read README.md for full documentation"
echo -e "  2. Check USAGE_EXAMPLES.md for CTF scenarios"
echo -e "  3. Try your first scan:"
echo -e "     ${YELLOW}python3 main.py --target-type domain --value example.com${NC}"
echo

# Offer to create alias
echo -e "${CYAN}Would you like to create a 'ctf-sentinel' alias? (y/n)${NC}"
read -p "" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SHELL_RC=""
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi
    
    if [ -n "$SHELL_RC" ]; then
        echo "alias ctf-sentinel='python3 $(pwd)/main.py'" >> "$SHELL_RC"
        echo -e "${GREEN}✓ Alias added to $SHELL_RC${NC}"
        echo -e "  Run: ${YELLOW}source $SHELL_RC${NC}"
        echo -e "  Then use: ${YELLOW}ctf-sentinel --target-type domain --value example.com${NC}"
    fi
fi

echo
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎯 CTF Sentinel is ready! Happy hunting! 🔍${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo
