# 🎓 CTF Sentinel - Mastery Guide

**From Beginner to Advanced OSINT Expert**

---

## 📚 **TABLE OF CONTENTS**

1. [Basic Usage](#basic-usage)
2. [Advanced Techniques](#advanced-techniques)
3. [CTF Workflows](#ctf-workflows)
4. [Maximizing AI Detection](#maximizing-ai-detection)
5. [Output Analysis](#output-analysis)
6. [Automation & Scripting](#automation--scripting)
7. [Pro Tips & Tricks](#pro-tips--tricks)
8. [Real CTF Examples](#real-ctf-examples)

---

# 1. BASIC USAGE

## Always Start Here

```bash
cd ~/ctf-sentinel
source venv/bin/activate
```

## The 6 Target Types

### 1.1 Domain Scanning (Most Powerful!)

```bash
python3 main.py --target-type domain --value example.com
```

**What it finds:**

- 🌐 Subdomains (dev, staging, admin)
- 📧 Email addresses
- 🔑 API keys in HTML/JS
- 🚩 Flags in subdomain names
- 🌍 DNS records
- 📝 WHOIS information
- 🔗 Related domains

**When to use:**

- CTF web challenges
- Bug bounty recon
- Company infrastructure mapping

**Example:**

```bash
# Scan a CTF platform
python3 main.py --target-type domain --value hackthebox.com --output htb.json
```

---

### 1.2 IP Scanning

```bash
sudo python3 main.py --target-type ip --value 192.168.1.1
```

**What it finds:**

- 🔌 Open ports (Nmap)
- 🖥️ Running services
- 🔄 Reverse DNS
- 📡 Network info

**When to use:**

- Network challenges
- After finding IPs from domain scan
- Port enumeration needed

**Example:**

```bash
# Scan local network device
sudo python3 main.py --target-type ip --value 192.168.1.1 --verbose
```

---

### 1.3 Username/Alias Hunting

```bash
python3 main.py --target-type alias --value hacker_123
```

**What it finds:**

- 🐙 GitHub profile & repos
- 🐦 Twitter/X account
- 💬 Reddit posts
- 📱 Other social media
- 📝 Pastebin entries

**When to use:**

- Social engineering CTFs
- Finding developer accounts
- OSINT challenges
- Team reconnaissance

**Example:**

```bash
# Find famous CTF player
python3 main.py --target-type alias --value LiveOverflow --output liveoverflow.json
```

---

### 1.4 Email Intelligence

```bash
python3 main.py --target-type email --value admin@target.com
```

**What it finds:**

- 🌐 Domain analysis
- 💻 GitHub commits
- 📋 Public pastes
- 🔓 Data breach info (if available)
- 📧 Email pattern

**When to use:**

- After finding email in domain scan
- Developer profiling
- Leak detection

**Example:**

```bash
python3 main.py --target-type email --value security@github.com
```

---

### 1.5 Hash Cracking Hints

```bash
python3 main.py --target-type hash --value 5d41402abc4b2a76b9719d911017c592
```

**What it finds:**

- 🔍 Hash in GitHub repos
- 📝 Hash in public databases
- 📋 Hash in pastes
- 💡 Context clues

**When to use:**

- Found hash in CTF
- Password hint needed
- Hash identification

**Example:**

```bash
# MD5 of "hello"
python3 main.py --target-type hash --value 5d41402abc4b2a76b9719d911017c592
```

---

### 1.6 File Metadata Extraction

```bash
python3 main.py --target-type filename --value image.jpg
```

**What it finds:**

- 📸 EXIF data
- 📍 GPS coordinates
- 📅 Creation date/time
- 🖥️ Software used
- 💬 Hidden comments
- 🚩 Flags in metadata

**When to use:**

- Steganography challenges
- Image forensics
- Hidden data detection

**Example:**

```bash
wget https://example.com/challenge.jpg
python3 main.py --target-type filename --value challenge.jpg
```

---

# 2. ADVANCED TECHNIQUES

## 2.1 Verbose Mode (See Everything!)

```bash
python3 main.py --target-type domain --value target.com --verbose
```

**Shows:**

- Raw tool output
- All external command execution
- Detailed AI processing
- Full correlation logs

**Use when:**

- Debugging
- Learning what tools run
- Need all details

---

## 2.2 Save Results for Later

```bash
# Save to JSON
python3 main.py --target-type domain --value target.com --output results.json

# View nicely formatted
python3 -m json.tool results.json

# Search in results
jq '.entities[] | select(.type=="EMAIL")' results.json
```

---

## 2.3 Skip AI for Speed

```bash
# Faster, but less intelligent
python3 main.py --target-type domain --value target.com --skip-ai
```

**Use when:**

- Just need raw data collection
- Speed is critical
- Running many scans

---

## 2.4 Combine with Other Tools

### Extract IPs and Feed to Nmap

```bash
python3 main.py --target-type domain --value target.com --output scan.json

# Extract IPs
jq '.entities[] | select(.type=="IP") | .value' scan.json > ips.txt

# Scan each IP
while read ip; do
    sudo nmap -sV $ip -oN "nmap_$ip.txt"
done < ips.txt
```

### Extract Subdomains for Further Testing

```bash
# Get subdomains
python3 main.py --target-type domain --value target.com --output scan.json
jq -r '.entities[] | select(.type=="SUBDOMAIN") | .value' scan.json > subdomains.txt

# Test each subdomain
while read subdomain; do
    echo "Testing $subdomain"
    curl -I "https://$subdomain"
done < subdomains.txt
```

---

# 3. CTF WORKFLOWS

## 3.1 Complete Web Challenge Workflow

### Step 1: Initial Domain Recon

```bash
python3 main.py --target-type domain --value challenge.ctf.com --output step1.json --verbose
```

**Look for:**

- Subdomains (especially dev, admin, api)
- Email addresses
- Flags in HTML/DNS

### Step 2: Investigate Findings

```bash
# Found email? Scan it
python3 main.py --target-type email --value admin@challenge.ctf.com --output step2.json

# Found subdomain? Scan it
python3 main.py --target-type domain --value dev.challenge.ctf.com --output step3.json
```

### Step 3: Profile Developers

```bash
# Search GitHub
python3 main.py --target-type alias --value ctf_admin --output step4.json
```

### Step 4: Analyze Any Files

```bash
# Download and analyze
wget http://challenge.ctf.com/hint.jpg
python3 main.py --target-type filename --value hint.jpg --output step5.json
```

---

## 3.2 OSINT Challenge Workflow

### Step 1: Start with Username

```bash
python3 main.py --target-type alias --value target_user --output user.json
```

### Step 2: Extract Info

```bash
# Find GitHub
jq '.entities[] | select(.type=="GITHUB")' user.json

# Find email
jq '.entities[] | select(.type=="EMAIL")' user.json
```

### Step 3: Pivot to Email

```bash
# Scan found email
python3 main.py --target-type email --value found@email.com --output email.json
```

### Step 4: Check Related Domains

```bash
# Extract domain from email
python3 main.py --target-type domain --value email-domain.com --output domain.json
```

---

# 4. MAXIMIZING AI DETECTION

## 4.1 What the AI Looks For

The AI automatically detects:

### 🚩 CTF Flags

- `CTF{...}`
- `flag{...}`
- `FLAG{...}`
- `[A-Z]{2,10}{...}` (custom formats)

### 🔑 API Keys

- AWS: `AKIA[0-9A-Z]{16}`
- GitHub: `ghp_[a-zA-Z0-9]{36}`
- Generic: `api_key=...`, `token=...`

### 🔐 Credentials

- `username:password`
- `password=...`
- `user=...`

### 📁 Sensitive Paths

- `/etc/passwd`
- `~/.ssh/`
- `/var/log/`
- `C:\Windows\`

### 📧 Standard Entities

- Emails
- IPs
- URLs
- Hashes (MD5, SHA1, SHA256)
- Subdomains
- Ports

---

## 4.2 Understanding Entity Scores

Entities are scored by importance:

**HIGH Priority (🔴):**

- CTF flags
- API keys
- Credentials
- Sensitive file paths

**MEDIUM Priority (🟡):**

- Emails
- Subdomains
- IPs

**LOW Priority (🟢):**

- Person names
- Organizations
- Dates

---

## 4.3 Reading AI Output

```
🚩 HIGH-VALUE TARGETS (AI-DETECTED)
╔══════════════════════════════════╗
║ CTF Flags Found: 3              ║  ← Most important!
║ API Keys Found: 2               ║  ← Check these!
║ Credentials Found: 1            ║  ← Try logging in!
╚══════════════════════════════════╝
```

**Always check:**

1. CTF Flags first (your goal!)
2. API Keys (might give access)
3. Credentials (test them)
4. File paths (check for LFI/RFI)

---

# 5. OUTPUT ANALYSIS

## 5.1 Understanding the Report

### Executive Summary

```
╭──────────────────────────┬───────╮
│ Metric                   │ Count │
├──────────────────────────┼───────┤
│ Data Sources             │     5 │  ← Tools run
│ Total Entities Extracted │   142 │  ← AI found 142 things
│ Linked Entities          │    23 │  ← 23 appear in multiple places
│ 🚩 CTF Flags Found       │     3 │  ← Your flags!
│ 🔑 API Keys Found        │     2 │  ← Secrets found
│ 🔐 Credentials Found     │     1 │  ← Login info
╰──────────────────────────┴───────╯
```

---

### Entity Breakdown

```
╭─────────────┬───────┬───────────╮
│ Entity Type │ Count │ Priority  │
├─────────────┼───────┼───────────┤
│ CTF_FLAG    │     3 │ 🔴 HIGH   │  ← Focus here!
│ API_KEY     │     2 │ 🔴 HIGH   │
│ EMAIL       │    15 │ 🟡 MEDIUM │
│ SUBDOMAIN   │    45 │ 🟡 MEDIUM │
│ IP          │     8 │ 🟡 MEDIUM │
╰─────────────┴───────┴───────────╯
```

---

### Relationships

```
Entity 1          ↔  Entity 2              Strength
─────────────────────────────────────────────────
admin@site.com    ↔  admin.site.com        5       ← Same entity in 5 places!
api_key_123       ↔  dev.site.com          3       ← API key found in dev subdomain
CTF{flag}         ↔  flag.site.com         2       ← Flag in subdomain name
```

**High strength = More reliable!**

---

## 5.2 Analyzing JSON Output

```bash
# Pretty print
python3 -m json.tool results.json

# Extract all flags
jq '.entities[] | select(.type=="CTF_FLAG")' results.json

# Get high-value entities
jq '.entities[] | select(.importance > 0.7)' results.json

# List all subdomains
jq -r '.entities[] | select(.type=="SUBDOMAIN") | .value' results.json

# Count by type
jq '[.entities[].type] | group_by(.) | map({type: .[0], count: length})' results.json
```

---

# 6. AUTOMATION & SCRIPTING

## 6.1 Batch Domain Scanning

```bash
#!/bin/bash
# scan_domains.sh

# Create targets.txt with domains
cat > targets.txt << EOF
hackthebox.com
tryhackme.com
picoctf.org
EOF

# Scan each
while read domain; do
    echo "[*] Scanning $domain"
    python3 main.py --target-type domain --value $domain \
        --output "results/${domain}_$(date +%s).json"
    sleep 5  # Be nice, don't spam
done < targets.txt

echo "[*] All scans complete! Results in results/"
```

---

## 6.2 Automated CTF Workflow

```bash
#!/bin/bash
# ctf_recon.sh <target_domain>

TARGET=$1
OUTPUT_DIR="recon_$(date +%Y%m%d_%H%M%S)"
mkdir -p $OUTPUT_DIR

echo "[1/5] Scanning main domain"
python3 main.py --target-type domain --value $TARGET \
    --output "$OUTPUT_DIR/1_domain.json"

# Extract subdomains
echo "[2/5] Extracting subdomains"
jq -r '.entities[] | select(.type=="SUBDOMAIN") | .value' \
    "$OUTPUT_DIR/1_domain.json" > "$OUTPUT_DIR/subdomains.txt"

# Scan each subdomain
echo "[3/5] Scanning subdomains"
while read subdomain; do
    python3 main.py --target-type domain --value $subdomain \
        --output "$OUTPUT_DIR/subdomain_$subdomain.json"
done < "$OUTPUT_DIR/subdomains.txt"

# Extract  emails
echo "[4/5] Extracting emails"
jq -r '.entities[] | select(.type=="EMAIL") | .value' \
    "$OUTPUT_DIR/1_domain.json" > "$OUTPUT_DIR/emails.txt"

# Scan emails
echo "[5/5] Scanning emails"
while read email; do
    python3 main.py --target-type email --value $email \
        --output "$OUTPUT_DIR/email_$email.json"
done < "$OUTPUT_DIR/emails.txt"

echo "[*] Complete! Results in $OUTPUT_DIR"
```

---

## 6.3 Continuous Monitoring

```bash
#!/bin/bash
# monitor.sh - Run every hour

TARGET="target.com"
BASELINE="baseline.json"
CURRENT="current_$(date +%s).json"

# Run scan
python3 main.py --target-type domain --value $TARGET --output $CURRENT

# Compare with baseline
if [ -f $BASELINE ]; then
    NEW_SUBDOMAINS=$(comm -13 \
        <(jq -r '.entities[] | select(.type=="SUBDOMAIN") | .value' $BASELINE | sort) \
        <(jq -r '.entities[] | select(.type=="SUBDOMAIN") | .value' $CURRENT | sort))
    
    if [ -n "$NEW_SUBDOMAINS" ]; then
        echo "🚨 New subdomains found!"
        echo "$NEW_SUBDOMAINS"
        # Send alert (email, Slack, etc.)
    fi
else
    cp $CURRENT $BASELINE
fi
```

---

# 7. PRO TIPS & TRICKS

## 7.1 Create Permanent Alias

```bash
# Add to ~/.bashrc
echo 'alias ctf="source ~/ctf-sentinel/venv/bin/activate && python3 ~/ctf-sentinel/main.py"' >> ~/.bashrc
source ~/.bashrc

# Now use:
ctf --target-type domain --value example.com
```

---

## 7.2 Quick Subdomain Enumeration

```bash
# Just get subdomains fast
ctf --target-type domain --value target.com --skip-ai --output temp.json
jq -r '.entities[] | select(.type=="SUBDOMAIN") | .value' temp.json | sort -u
```

---

## 7.3 Find Hidden Flags in Results

```bash
# Scan and extract flags
ctf --target-type domain --value target.com --output scan.json

# Get all flags
jq -r '.entities[] | select(.type=="CTF_FLAG") | .value' scan.json

# Get flags with context
jq '.entities[] | select(.type=="CTF_FLAG") | {flag: .value, source: .source, context: .context}' scan.json
```

---

## 7.4 Combine with Grep

```bash
# Scan and search output
ctf --target-type domain --value target.com --verbose 2>&1 | grep -i "flag\|ctf{"
```

---

## 7.5 Export for Other Tools

```bash
# Export to CSV
jq -r '.entities[] | [.type, .value, .importance, .source] | @csv' scan.json > results.csv

# Import to Excel, Google Sheets, etc.
```

---

# 8. REAL CTF EXAMPLES

## 8.1 Web Exploitation CTF

**Challenge:** Find the flag on challenge.ctf.com

```bash
# Step 1: Initial scan
ctf --target-type domain --value challenge.ctf.com --output scan1.json --verbose

# Found: dev.challenge.ctf.com subdomain

# Step 2: Scan dev subdomain
ctf --target-type domain --value dev.challenge.ctf.com --output scan2.json

# Found: admin@challenge.ctf.com email

# Step 3: Profile admin
ctf --target-type email --value admin@challenge.ctf.com --output scan3.json

# Found: GitHub repo with leaked credentials!

# Step 4: Check repo
git clone <repo_url>
grep -r "flag\|CTF{" .

# Flag found in commit history!
```

---

## 8.2 OSINT Challenge

**Challenge:** Find information about user "mystery_hacker"

```bash
# Step 1: Username scan
ctf --target-type alias --value mystery_hacker --output user.json

# Found: GitHub profile, Twitter, email

# Step 2: Check GitHub repos
# Clone repos and search for flags

# Step 3: Analyze timeline
jq '.entities[] | select(.type=="DATE")' user.json

# Step 4: Find location clues
jq '.entities[] | select(.type contains "LOC")' user.json
```

---

## 8.3 Forensics Challenge

**Challenge:** Analyze suspect.jpg for hidden data

```bash
# Scan the file
ctf --target-type filename --value suspect.jpg --output forensics.json

# Check JSON for interesting metadata
jq '.entities[]' forensics.json

# Found GPS coordinates!
# Found flag in EXIF comment!
```

---

# 9. TROUBLESHOOTING

## Common Issues

### "Permission denied"

```bash
# Use sudo for IP scans
sudo python3 main.py --target-type ip --value 192.168.1.1
```

### "Tool not found" warnings

```bash
# Install missing tools
sudo apt install amass sublist3r sherlock exiftool nmap
```

### "Module not found"

```bash
# Activate venv
source venv/bin/activate
```

### Slow scans

```bash
# Use --skip-ai for speed
ctf --target-type domain --value target.com --skip-ai
```

---

# 10. BEST PRACTICES

✅ **Always use VPN** for anonymity
✅ **Save all results** for later reference
✅ **Use verbose mode** when learning
✅ **Correlate findings** manually too
✅ **Double-check AI detections** (false positives happen)
✅ **Only scan authorized targets**
✅ **Respect rate limits**
✅ **Document your methodology**

---

# 🎯 QUICK REFERENCE CARD

```bash
# Activate environment
source ~/ctf-sentinel/venv/bin/activate

# Basic scans
ctf --target-type domain --value TARGET
ctf --target-type alias --value USERNAME
ctf --target-type email --value EMAIL
ctf --target-type ip --value IP
ctf --target-type hash --value HASH
ctf --target-type filename --value FILE

# With options
ctf --target-type domain --value TARGET --output file.json --verbose

# Extract from JSON
jq '.entities[] | select(.type=="CTF_FLAG")' results.json
jq '.entities[] | select(.importance > 0.7)' results.json
```

---

**You're now a CTF Sentinel master! 🎓🐉**

**Practice on authorized targets and happy hacking! 🔍🚀**
