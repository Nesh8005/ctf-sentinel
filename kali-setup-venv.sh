#!/bin/bash
# CTF Sentinel - Quick Setup for Modern Kali (with venv)
# Handles externally-managed-environment error

echo "╔═══════════════════════════════════════╗"
echo "║  CTF Sentinel - Kali Setup (venv)    ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Create virtual environment
echo "[1/5] Creating virtual environment..."
python3 -m venv venv

# Activate venv
echo "[2/5] Activating virtual environment..."
source venv/bin/activate

# Install Python packages
echo "[3/5] Installing Python packages..."
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_sm

# Install external tools
echo "[4/5] Installing external OSINT tools..."
sudo apt update
sudo apt install -y amass sublist3r nmap whois dnsutils libimage-exiftool-perl
pip3 install sherlock-project

# Verify
echo "[5/5] Verifying installation..."
python3 demo.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use CTF Sentinel:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run tool: python3 main.py --target-type domain --value example.com"
echo "  3. Deactivate when done: deactivate"
echo ""
echo "NOTE: venv is now active in this terminal session!"
echo ""
