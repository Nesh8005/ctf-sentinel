# CTF Sentinel - Kali Linux Installation Guide

## 🐉 Perfect for Kali Linux

CTF Sentinel is **optimized for Kali Linux** - most external OSINT tools are pre-installed or easily available in Kali's repositories.

## 🚀 Quick Installation (Kali Linux)

### Step 1: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Python Dependencies

```bash
# Navigate to project directory
cd /path/to/OSINT

# Install Python packages
pip3 install -r requirements.txt

# Download spaCy language model
python3 -m spacy download en_core_web_sm
```

### Step 3: Install External OSINT Tools

Most tools are in Kali's default repos or easily installable:

#### Subdomain Enumeration

```bash
# Amass (Recommended - usually pre-installed on Kali)
sudo apt install amass -y

# OR Sublist3r (Alternative)
sudo apt install sublist3r -y
```

#### Username Search

```bash
# Sherlock
pip3 install sherlock-project

# Or install via apt if available
sudo apt install sherlock -y
```

#### Metadata Extraction

```bash
# ExifTool (usually pre-installed)
sudo apt install libimage-exiftool-perl -y
```

#### Network Tools (Usually Pre-installed)

```bash
# Nmap
sudo apt install nmap -y

# DNS utilities (dig, whois)
sudo apt install dnsutils whois -y
```

### Step 4: Verify Installation

```bash
# Test Python
python3 --version

# Run demo
python3 demo.py

# Check tool availability
python3 main.py --help
```

## 🎯 Quick Start Commands (Kali Linux)

### Basic Scans

```bash
# Domain reconnaissance
python3 main.py --target-type domain --value ctfchallenge.com

# Username OSINT
python3 main.py --target-type alias --value hacker_ctf

# IP investigation
python3 main.py --target-type ip --value 192.168.1.1

# Email analysis
python3 main.py --target-type email --value admin@target.com

# Hash lookup
python3 main.py --target-type hash --value 5d41402abc4b2a76b9719d911017c592

# File metadata
python3 main.py --target-type filename --value /path/to/image.jpg
```

### With Output

```bash
# Save to JSON
python3 main.py --target-type domain --value example.com --output ~/results.json

# Verbose mode
python3 main.py --target-type domain --value example.com --verbose
```

## 🔧 Kali-Specific Optimizations

### 1. Create Bash Alias (Optional)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias ctf-sentinel='python3 /path/to/OSINT/main.py'
```

Then use:

```bash
ctf-sentinel --target-type domain --value example.com
```

### 2. Install Additional Kali Tools

CTF Sentinel works great with other Kali tools:

```bash
# TheHarvester (email/subdomain enumeration)
sudo apt install theharvester -y

# Recon-ng (reconnaissance framework)
sudo apt install recon-ng -y

# Maltego (visual link analysis)
sudo apt install maltego -y

# OSINT Framework tools
sudo apt install osrframework -y
```

### 3. Setup Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv ctf-sentinel-env

# Activate it
source ctf-sentinel-env/bin/activate

# Install dependencies
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_sm

# Run tool
python3 main.py --target-type domain --value example.com

# Deactivate when done
deactivate
```

## 🐳 Docker Option (Advanced)

Create a `Dockerfile`:

```dockerfile
FROM kalilinux/kali-rolling

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    amass \
    sublist3r \
    nmap \
    whois \
    dnsutils \
    libimage-exiftool-perl

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm

COPY . .

ENTRYPOINT ["python3", "main.py"]
```

Build and run:

```bash
docker build -t ctf-sentinel .
docker run ctf-sentinel --target-type domain --value example.com
```

## 🎓 Kali Linux Advantages

### Pre-installed Tools

Kali comes with many tools CTF Sentinel can leverage:

- ✅ Nmap (port scanning)
- ✅ Whois (domain info)
- ✅ Dig (DNS queries)
- ✅ ExifTool (metadata)
- ✅ Amass (subdomain enum)
- ✅ Sublist3r (subdomain enum)

### Easy Installation

```bash
# All in one command
sudo apt install amass sublist3r nmap whois dnsutils libimage-exiftool-perl -y
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_sm
```

### CTF-Optimized Environment

- Low-level network access (no permission issues)
- Built-in VPN support for anonymity
- Seamless integration with other pentest tools

## 🔥 Advanced Kali Workflows

### 1. Automated Reconnaissance Script

```bash
#!/bin/bash
# ctf-recon.sh

TARGET=$1
OUTPUT_DIR="./recon_$(date +%Y%m%d_%H%M%S)"

mkdir -p $OUTPUT_DIR

echo "[*] Running CTF Sentinel on $TARGET"
python3 main.py --target-type domain --value $TARGET --output $OUTPUT_DIR/sentinel.json

echo "[*] Running Amass"
amass enum -d $TARGET -o $OUTPUT_DIR/amass.txt

echo "[*] Running TheHarvester"
theharvester -d $TARGET -b all -f $OUTPUT_DIR/harvester

echo "[*] Reconnaissance complete! Results in $OUTPUT_DIR"
```

### 2. Integration with Metasploit

After finding targets with CTF Sentinel, feed them into Metasploit:

```bash
# Find IPs with CTF Sentinel
python3 main.py --target-type domain --value target.com --output results.json

# Extract IPs and scan with Metasploit
# (Parse JSON and use in msf)
```

### 3. Combine with Burp Suite

Use CTF Sentinel for reconnaissance, then test discovered endpoints with Burp Suite.

## 🛡️ Security Best Practices

### Use VPN

```bash
# Start VPN before reconnaissance
sudo openvpn ~/vpn/config.ovpn

# Then run CTF Sentinel
python3 main.py --target-type domain --value target.com
```

### Rate Limiting

Some tools can be aggressive. Use with caution:

```bash
# For authorized testing only
python3 main.py --target-type domain --value authorized-target.com
```

## 🧪 Testing on Kali

```bash
# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# View coverage
firefox htmlcov/index.html
```

## 🚨 Troubleshooting (Kali Linux)

### "Permission denied" errors

```bash
# Use sudo for network tools
sudo python3 main.py --target-type ip --value 192.168.1.1
```

### "Module not found"

```bash
# Ensure you're using pip3 (Python 3)
pip3 install -r requirements.txt

# Check Python version
python3 --version  # Should be 3.10+
```

### "Tool not found" warnings

```bash
# Install missing tools
sudo apt install <tool-name>

# Check if tool is in PATH
which amass
which sherlock
```

### Virtual environment issues

```bash
# Recreate venv
rm -rf ctf-sentinel-env
python3 -m venv ctf-sentinel-env
source ctf-sentinel-env/bin/activate
pip3 install -r requirements.txt
```

## 📦 Complete Setup Script

Save this as `kali-setup.sh`:

```bash
#!/bin/bash
# CTF Sentinel - Kali Linux Setup Script

echo "╔═══════════════════════════════════════╗"
echo "║  CTF Sentinel - Kali Linux Setup     ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Update system
echo "[*] Updating system..."
sudo apt update

# Install Python dependencies
echo "[*] Installing Python packages..."
pip3 install -r requirements.txt

# Download spaCy model
echo "[*] Downloading spaCy model..."
python3 -m spacy download en_core_web_sm

# Install external tools
echo "[*] Installing external OSINT tools..."
sudo apt install -y amass sublist3r nmap whois dnsutils libimage-exiftool-perl

# Install Sherlock
echo "[*] Installing Sherlock..."
pip3 install sherlock-project

# Verify installation
echo "[*] Verifying installation..."
python3 demo.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Try: python3 main.py --target-type domain --value example.com"
```

Make it executable and run:

```bash
chmod +x kali-setup.sh
./kali-setup.sh
```

## 🎯 Ready for CTF

CTF Sentinel on Kali Linux gives you:

- ✅ All tools pre-installed or easily available
- ✅ Root access for network tools
- ✅ Built-in VPN support
- ✅ Integration with other Kali tools
- ✅ Optimized for penetration testing

**Your Kali Linux machine is now a CTF powerhouse! 🚀**

## 📚 Next Steps

1. ✅ Run `kali-setup.sh` or install manually
2. ✅ Test with `python3 demo.py`
3. ✅ Read `USAGE_EXAMPLES.md` for CTF scenarios
4. ✅ Start your first reconnaissance!

---

**Happy Hunting on Kali! 🐉🔍**
