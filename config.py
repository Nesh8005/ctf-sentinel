"""
CTF Sentinel - Configuration and Constants

Configuration settings and constants for the CTF Sentinel tool.

Author: CTF Sentinel Team
Version: 1.0.0
"""

# Application Metadata
APP_NAME = "CTF Sentinel"
APP_VERSION = "1.0.0"
APP_AUTHOR = "CTF Sentinel Team"
APP_DESCRIPTION = "AI-Enhanced OSINT Tool for CTF Competitions"

# Supported Target Types
SUPPORTED_TARGET_TYPES = [
    'domain',
    'ip',
    'alias',
    'email',
    'hash',
    'filename'
]

# External Tool Configuration
EXTERNAL_TOOLS = {
    'amass': {
        'name': 'Amass',
        'purpose': 'Subdomain Enumeration',
        'timeout': 300,
        'required': False
    },
    'sublist3r': {
        'name': 'Sublist3r',
        'purpose': 'Subdomain Enumeration (Alternative)',
        'timeout': 300,
        'required': False
    },
    'sherlock': {
        'name': 'Sherlock',
        'purpose': 'Username Search',
        'timeout': 180,
        'required': False
    },
    'exiftool': {
        'name': 'ExifTool',
        'purpose': 'Metadata Extraction',
        'timeout': 60,
        'required': False
    },
    'nmap': {
        'name': 'Nmap',
        'purpose': 'Port Scanning',
        'timeout': 120,
        'required': False
    },
    'dig': {
        'name': 'dig',
        'purpose': 'DNS Queries',
        'timeout': 30,
        'required': False
    },
    'whois': {
        'name': 'WHOIS',
        'purpose': 'Domain/IP Registration Info',
        'timeout': 30,
        'required': False
    }
}

# AI/NLP Configuration
SPACY_MODEL = "en_core_web_sm"
MIN_ENTITY_IMPORTANCE = 0.3  # Minimum score to keep entities
MAX_TEXT_LENGTH = 1000000    # Maximum text length to process (1MB)

# Entity Type Priority (for scoring)
ENTITY_PRIORITIES = {
    'CTF_FLAG': 1.0,
    'API_KEY': 1.0,
    'CREDENTIAL': 1.0,
    'FILE_PATH': 0.8,
    'IP_ADDRESS': 0.8,
    'URL': 0.8,
    'EMAIL': 0.8,
    'MD5_HASH': 0.75,
    'SHA1_HASH': 0.75,
    'SHA256_HASH': 0.75,
    'PERSON': 0.6,
    'ORG': 0.6,
    'GPE': 0.6,
    'SUBDOMAIN': 0.7,
    'PORT': 0.5
}

# API Configuration (for future expansion)
GITHUB_API_BASE = "https://api.github.com"
PASTEBIN_API_BASE = "https://pastebin.com/api"

# Request Configuration
REQUEST_TIMEOUT = 10
REQUEST_HEADERS = {
    'User-Agent': f'{APP_NAME}/{APP_VERSION}'
}

# Report Configuration
REPORT_MAX_RELATIONSHIPS = 10  # Max relationships to display
REPORT_HIGH_VALUE_THRESHOLD = 0.8  # Score threshold for high-value entities

# Color Scheme for Rich Output
COLOR_SCHEME = {
    'banner': 'cyan',
    'success': 'green',
    'warning': 'yellow',
    'error': 'red',
    'info': 'blue',
    'highlight': 'bold yellow',
    'critical': 'bold red'
}
