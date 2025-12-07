# CTF Sentinel 🐉

**AI-Enhanced OSINT Tool for Kali Linux**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Kali Linux](https://img.shields.io/badge/Kali%20Linux-Optimized-blueviolet.svg)](https://www.kali.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🎯 **Built for Kali Linux** - Automate CTF reconnaissance with AI-powered intelligence!

---

## 🚀 Quick Start

### One-Command Installation

```bash
git clone https://github.com/YOUR_USERNAME/ctf-sentinel.git
cd ctf-sentinel
chmod +x setup.sh && ./setup.sh
```

That's it! The script handles everything:

- ✅ Creates virtual environment
- ✅ Installs all Python dependencies
- ✅ Downloads AI models
- ✅ Installs external OSINT tools
- ✅ Verifies installation

### First Scan

```bash
source venv/bin/activate
python3 main.py --target-type domain --value example.com
```

---

## 🎯 Overview

CTF Sentinel is a powerful, AI-enhanced OSINT tool designed specifically for CTF competitions on Kali Linux. It automates intelligence collection from external OSINT tools, applies AI/NLP for entity recognition, and intelligently correlates findings to uncover flags and hidden clues.

### Key Features

- **🚀 Speed**: Automated execution of multiple OSINT tools in parallel
- **🤖 AI-Powered**: Advanced NER using spaCy with custom CTF-specific patterns
- **🔗 Correlation**: Intelligent linking of disparate facts across sources
- **🎯 Flag Detection**: Custom patterns for CTF flags, API keys, and credentials
- **📊 Rich Reports**: Beautiful, color-coded terminal output
- **🔍 Multi-Target**: Supports domains, IPs, usernames, emails, hashes, and files

---

## 📋 Requirements

- **Kali Linux** (2021.1+)
- **Python 3.10+** (pre-installed on modern Kali)
- **Root/sudo access** (for external tools)

---

## 🛠️ Installation

### Method 1: Automated Setup (Recommended)

```bash
git clone https://github.com/YOUR_USERNAME/ctf-sentinel.git
cd ctf-sentinel
chmod +x setup.sh && ./setup.sh
```

### Method 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ctf-sentinel.git
cd ctf-sentinel

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_sm

# Install external tools
sudo apt install -y amass sublist3r nmap whois dnsutils libimage-exiftool-perl
pip3 install sherlock-project

# Verify
python3 demo.py
```

### Method 3: Docker

```bash
git clone https://github.com/YOUR_USERNAME/ctf-sentinel.git
cd ctf-sentinel

# Build container
docker build -t ctf-sentinel .

# Run scan
docker run --rm ctf-sentinel --target-type domain --value example.com
```

---

## 🎯 Usage

### Basic Scans

```bash
# Activate virtual environment first
source venv/bin/activate

# Domain reconnaissance
python3 main.py --target-type domain --value ctfchallenge.com

# Username OSINT  
python3 main.py --target-type alias --value hacker_ctf

# IP investigation (may need sudo for Nmap)
sudo python3 main.py --target-type ip --value 192.168.1.1

# Email analysis
python3 main.py --target-type email --value admin@target.com

# Hash lookup
python3 main.py --target-type hash --value 5d41402abc4b2a76b9719d911017c592

# File metadata extraction
python3 main.py --target-type filename --value /path/to/image.jpg
```

### Advanced Options

```bash
# Save results to JSON
python3 main.py --target-type domain --value target.com --output results.json

# Verbose mode
python3 main.py --target-type domain --value target.com --verbose

# Skip AI analysis (faster, less intelligent)
python3 main.py --target-type domain --value target.com --skip-ai
```

### Create Bash Alias

```bash
echo "alias ctf-sentinel='source $(pwd)/venv/bin/activate && python3 $(pwd)/main.py'" >> ~/.bashrc
source ~/.bashrc

# Now use anywhere:
ctf-sentinel --target-type domain --value example.com
```

---

## 📊 Example Output

```
╔═══════════════════════════════════════════════════════════╗
║              🔍 CTF SENTINEL 🔍                           ║
║         AI-Enhanced OSINT for CTF Competitions            ║
╚═══════════════════════════════════════════════════════════╝

Target Type: DOMAIN
Target Value: ctfchallenge.com

═══ Phase 1: Data Collection ═══
  → Running Amass subdomain enumeration...
  → Querying DNS records...
✓ Collected 5 data sources

═══ Phase 2: AI/NER Analysis ═══
✓ Extracted 142 entities using AI/NER

═══ Phase 3: Correlation & Analysis ═══
✓ Identified 23 linked entities

🚩 HIGH-VALUE TARGETS (AI-DETECTED)
╔══════════════════════════════════╗
║ CTF Flags Found: 3              ║
║ API Keys Found: 2               ║
║ Credentials Found: 1            ║
╚══════════════════════════════════╝
```

---

## 🧠 AI Features

### Custom NER Patterns Detect

- **CTF Flags**: `CTF{...}`, `flag{...}`, `FLAG{...}`
- **API Keys**: AWS keys, GitHub tokens, generic API keys
- **Credentials**: username:password patterns
- **File Paths**: `/etc/passwd`, `~/.ssh/`, sensitive directories
- **Standard Entities**: Emails, IPs, URLs, hashes

### Intelligent Correlation

- Links entities across multiple sources
- Identifies relationships and patterns
- Calculates importance scores
- Filters noise automatically

---

## 🎓 CTF Use Cases

1. **Subdomain Enumeration** - Auto-detect flags in subdomain names or content
2. **Username OSINT** - Profile targets across social media and GitHub
3. **Steganography** - Extract EXIF metadata from images
4. **API Key Discovery** - Find exposed keys in repositories and subdomains
5. **Email Intelligence** - Correlate breach data and domain information
6. **Hash Lookup** - Search public databases for hash references

---

## 🏗️ Project Structure

```
ctf-sentinel/
├── main.py                 # CLI entry point
├── collection_engine.py    # External tool execution
├── ai_parser.py           # AI/NLP processing
├── correlation_report.py  # Correlation & reporting
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
├── setup.sh              # Automated setup script
├── demo.py               # Installation verification
├── Dockerfile            # Container deployment
├── docker-compose.yml    # Docker orchestration
├── test_*.py             # Unit tests
└── README.md             # This file
```

---

## 🔧 Advanced Usage

### Batch Scanning

```bash
# Create targets.txt with one domain per line
for target in $(cat targets.txt); do
  python3 main.py --target-type domain --value $target \
    --output "results/${target}_$(date +%s).json"
done
```

### With VPN

```bash
# Start VPN first
sudo openvpn ~/vpn/config.ovpn

# In another terminal
source venv/bin/activate
python3 main.py --target-type domain --value target.com
```

### Integration Example

```bash
# Extract IPs and feed to Nmap
python3 main.py --target-type domain --value target.com --output results.json
jq '.entities.*.value' results.json | grep -E '^[0-9.]+$' | xargs -I {} nmap -sV {}
```

---

## 🧪 Testing

```bash
source venv/bin/activate

# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# View coverage
firefox htmlcov/index.html
```

---

## 🐛 Troubleshooting

### "Permission denied" for Nmap

```bash
sudo python3 main.py --target-type ip --value 192.168.1.1
```

### "Module not found"

```bash
source venv/bin/activate  # Make sure venv is active
pip3 install -r requirements.txt
```

### "Tool not found" warnings

External tools are optional. Install them:

```bash
sudo apt install amass sublist3r nmap whois dnsutils libimage-exiftool-perl
```

---

## 📚 Documentation

- **Installation Guide**: [`KALI_INSTALL.md`](KALI_INSTALL.md)
- **Usage Examples**: [`USAGE_EXAMPLES.md`](USAGE_EXAMPLES.md)
- **Project Summary**: [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## ⚠️ Disclaimer

This tool is intended for **educational purposes and authorized security research only**. Always obtain proper authorization before conducting reconnaissance on systems you do not own.

---

## 🙏 Acknowledgments

- OWASP Amass team
- Kali Linux project  
- spaCy development team
- CTF community
- All OSINT tool creators

---

**🐉 Built for Kali Linux | Made for CTF Players | Powered by AI**

**Happy Hunting! 🔍🚀**
