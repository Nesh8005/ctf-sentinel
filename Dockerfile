# CTF Sentinel - Docker Container
# Based on Kali Linux Rolling for maximum tool availability

FROM kalilinux/kali-rolling

# Set metadata
LABEL maintainer="CTF Sentinel Team"
LABEL description="AI-Enhanced OSINT Tool for CTF Competitions"
LABEL version="1.0.0"

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Update and install system dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install external OSINT tools
RUN apt-get update && apt-get install -y \
    amass \
    sublist3r \
    nmap \
    whois \
    dnsutils \
    libimage-exiftool-perl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python3 -m spacy download en_core_web_sm

# Install Sherlock (from pip)
RUN pip3 install --no-cache-dir sherlock-project

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p /output

# Set volume for output
VOLUME ["/output"]

# Make script executable (if needed)
RUN chmod +x demo.py 2>/dev/null || true

# Set entrypoint
ENTRYPOINT ["python3", "main.py"]

# Default command (shows help)
CMD ["--help"]

# Usage examples:
# Build: docker build -t ctf-sentinel .
# Run: docker run --rm ctf-sentinel --target-type domain --value example.com
# With output: docker run --rm -v $(pwd)/output:/output ctf-sentinel --target-type domain --value example.com --output /output/report.json
# Interactive: docker run --rm -it ctf-sentinel /bin/bash
