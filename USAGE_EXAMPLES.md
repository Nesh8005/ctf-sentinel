# CTF Sentinel - Usage Examples

## Basic Target Types

### 1. Domain Analysis

```bash
python main.py --target-type domain --value ctfchallenge.com
```

**What it does:**

- Subdomain enumeration (if Amass/Sublist3r installed)
- DNS record queries
- WHOIS lookup
- Web content analysis
- AI extraction of IPs, emails, URLs, potential flags

**Example output:**

- Discovered subdomains
- Email addresses found
- IP addresses
- CTF flags in HTML/JS
- Linked entities

### 2. IP Address Investigation

```bash
python main.py --target-type ip --value 104.21.45.78
```

**What it does:**

- Reverse DNS lookup
- WHOIS information
- Port scanning (if Nmap installed)
- Geographic location hints

### 3. Username/Alias Reconnaissance

```bash
python main.py --target-type alias --value h4ck3r_ctf
```

**What it does:**

- Sherlock search across social media (if installed)
- GitHub user/repository search
- Pastebin search
- Username pattern analysis

**Use case:** Finding CTF player's online presence

### 4. Email Address Analysis

```bash
python main.py --target-type email --value admin@target-ctf.com
```

**What it does:**

- Domain analysis
- GitHub commit search
- Breach database correlation
- Associated usernames

### 5. Hash Lookup

```bash
python main.py --target-type hash --value 5d41402abc4b2a76b9719d911017c592
```

**What it does:**

- Search in GitHub code
- Pastebin searches
- Hash type identification
- Potential password cracking hints

### 6. File Metadata Extraction

```bash
python main.py --target-type filename --value challenge_image.jpg
```

**What it does:**

- EXIF metadata extraction (if ExifTool installed)
- GPS coordinates
- Camera/software info
- Hidden flags in metadata
- File type analysis

## Advanced Usage

### Save Results to File

```bash
python main.py --target-type domain --value example.com --output results.json
```

The JSON file contains:

- All extracted entities
- Relationships
- Source data
- Correlation results

### Verbose Mode for Debugging

```bash
python main.py --target-type domain --value example.com --verbose
```

Shows:

- Tool detection status
- Command execution
- Entity extraction details
- Performance metrics

### Quick Scan (Skip AI)

```bash
python main.py --target-type domain --value example.com --skip-ai
```

Faster but:

- No custom NER patterns
- No flag detection
- No entity correlation
- Just raw tool output

## CTF-Specific Examples

### Finding Hidden Flags in Subdomains

```bash
python main.py --target-type domain --value challenge.ctf.com
```

Look for:

- Subdomain names with "flag", "admin", "secret"
- Flags in DNS TXT records
- Hidden content in subdomain pages

### Analyzing Challenge Files

```bash
python main.py --target-type filename --value stego_challenge.png
```

Extracts:

- EXIF data with potential flags
- Hidden metadata
- GPS coordinates (if present)
- Software/creation info

### User Profiling for Social Engineering Challenges

```bash
python main.py --target-type alias --value target_username
```

Discovers:

- Social media accounts
- GitHub repositories (potential leaked keys)
- Personal information
- Activity patterns

### API Key Discovery

```bash
# From a domain
python main.py --target-type domain --value api.example.com

# Look in the output for:
# - Exposed API keys in JavaScript
# - AWS keys in subdomains
# - GitHub tokens in repos
```

## Workflow Examples

### Complete Domain Reconnaissance

```bash
# 1. Start with domain
python main.py --target-type domain --value target.ctf --output domain_report.json

# 2. Extract IPs and analyze them
python main.py --target-type ip --value <discovered_ip>

# 3. Find usernames and profile them
python main.py --target-type alias --value <found_username>
```

### File Analysis Pipeline

```bash
# 1. Extract metadata
python main.py --target-type filename --value challenge.jpg --output metadata.json

# 2. If email found in metadata, analyze it
python main.py --target-type email --value <extracted_email>
```

## Tips for CTF Success

### 1. Always Use Verbose Mode First

```bash
python main.py --target-type domain --value target.com --verbose
```

This shows what tools are available and working.

### 2. Save Everything

```bash
python main.py --target-type domain --value target.com --output $(date +%Y%m%d_%H%M%S)_scan.json
```

### 3. Look for Patterns in Output

- Check the "High-Value Targets" section first
- Review entity relationships
- Cross-reference multiple sources

### 4. Combine with Manual Analysis

Use CTF Sentinel to automate collection, then:

- Review raw data in output files
- Follow up on interesting findings manually
- Use discovered info for further reconnaissance

## Common CTF Flag Patterns Detected

The tool automatically detects:

- `CTF{...}` - Standard CTF format
- `flag{...}` - Common variation
- `FLAG{...}` - Uppercase version
- `ABC{...}` - Any 2-10 uppercase letters followed by {...}
- Custom patterns in metadata

## Performance Tips

### For Large Domains

```bash
# Use skip-ai for initial fast scan
python main.py --target-type domain --value large-domain.com --skip-ai

# Then run AI on specific subdomains
python main.py --target-type domain --value sub.large-domain.com
```

### For Multiple Targets

Create a simple batch script:

```bash
# targets.txt contains one target per line
for target in $(cat targets.txt); do
    python main.py --target-type domain --value $target --output "${target}_report.json"
done
```

## Interpreting Results

### High Importance Score (0.8-1.0)

- CTF flags
- API keys
- Credentials
- Review immediately!

### Medium Importance (0.5-0.7)

- IPs, URLs, emails
- Technical entities
- Useful for correlation

### Low Importance (<0.5)

- Generic text entities
- Common words
- Filtered by default

## Need More Examples?

Check the test files:

- `test_ai_parser.py` - Shows entity patterns
- `test_correlation.py` - Demonstrates correlation logic
