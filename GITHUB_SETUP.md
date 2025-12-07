# How to Push to GitHub and Enable Git Clone

Follow these steps to make your CTF Sentinel available via `git clone`:

## Step 1: Initialize Git Repository (On Your Machine)

```bash
cd ~/Downloads/OSINT

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: CTF Sentinel - AI-Enhanced OSINT for Kali Linux"
```

## Step 2: Create GitHub Repository

1. Go to <https://github.com>
2. Click "New Repository" (+ icon, top right)
3. Fill in:
   - **Repository name**: `ctf-sentinel` (or your choice)
   - **Description**: "AI-Enhanced OSINT Tool for CTF Competitions on Kali Linux"
   - **Visibility**: Public or Private
   - **DO NOT** initialize with README (we already have one)
4. Click "Create repository"

## Step 3: Push to GitHub

GitHub will show you commands. Use these:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/ctf-sentinel.git

# Push code
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 4: Update README

After pushing, update the README.md to replace placeholders:

Find and replace:

```
YOUR_USERNAME
```

With your actual GitHub username in:

- README.md (lines with git clone commands)

Then commit and push:

```bash
git add README.md
git commit -m "Update repository URLs"
git push
```

## Step 5: Users Can Now Clone

Anyone can now install with:

```bash
git clone https://github.com/YOUR_USERNAME/ctf-sentinel.git
cd ctf-sentinel
chmod +x setup.sh && ./setup.sh
```

## Optional: Add GitHub Features

### Add Topics

On your GitHub repository page:

- Click "⚙️ Settings" (or the gear icon near "About")
- Add topics: `ctf`, `osint`, `kali-linux`, `ai`, `security`, `python`, `spacy`, `reconnaissance`

### Add Description

- Edit the "About" section
- Add: "AI-Enhanced OSINT Tool for CTF Competitions on Kali Linux"
- Add website (if you have one)

### Enable Issues

- Go to Settings → Features
- Enable "Issues" for bug reports and feature requests

## File Structure Ready for Git

All files are already configured:

- ✅ `.gitignore` - Excludes venv, cache, outputs
- ✅ `README.md` - Complete documentation
- ✅ `setup.sh` - Automated installation
- ✅ `requirements.txt` - Dependencies
- ✅ All source code and tests
- ✅ Docker configuration

## Bonus: Add GitHub Actions (Optional)

Create `.github/workflows/tests.yml` to auto-run tests on push:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m spacy download en_core_web_sm
      - name: Run tests
        run: pytest
```

---

**You're ready for `git clone`! 🚀**
