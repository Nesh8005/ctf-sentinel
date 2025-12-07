"""
CTF Sentinel - Data Collection Engine

This module handles the execution and output capture of external OSINT tools.
It runs tools like Amass, Sherlock, ExifTool, and others, capturing their output
for further AI analysis.

Author: CTF Sentinel Team
Version: 1.0.0
"""

import subprocess
import shutil
import tempfile
import os
from typing import Dict, List, Optional, Callable
from pathlib import Path
import requests
from rich.console import Console

console = Console()


class CollectionEngine:
    """
    Manages the execution of external OSINT tools and data collection.
    
    This class provides a unified interface for running various OSINT tools,
    capturing their output, and handling errors gracefully.
    
    Attributes:
        verbose (bool): Enable verbose logging.
        tool_paths (Dict[str, str]): Cached paths to external tools.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the Collection Engine.
        
        Args:
            verbose (bool): Enable verbose output for debugging.
        """
        self.verbose = verbose
        self.tool_paths: Dict[str, str] = {}
        self._detect_tools()
    
    def _detect_tools(self):
        """
        Detect available external OSINT tools in the system PATH.
        
        Searches for common OSINT tools and caches their paths.
        Warns if critical tools are missing.
        """
        tools = ['amass', 'sublist3r', 'sherlock', 'exiftool', 'nmap', 'dig', 'whois']
        
        if self.verbose:
            console.print("[dim]Detecting available OSINT tools...[/dim]")
        
        for tool in tools:
            path = shutil.which(tool)
            if path:
                self.tool_paths[tool] = path
                if self.verbose:
                    console.print(f"[green]✓[/green] Found {tool}: {path}")
            else:
                if self.verbose:
                    console.print(f"[yellow]![/yellow] {tool} not found in PATH")
    
    def _run_command(
        self,
        command: List[str],
        timeout: int = 300,
        capture: bool = True
    ) -> str:
        """
        Execute an external command and capture its output.
        
        Args:
            command (List[str]): Command and arguments to execute.
            timeout (int): Maximum execution time in seconds.
            capture (bool): Whether to capture and return output.
        
        Returns:
            str: Command output (stdout + stderr combined).
        
        Raises:
            subprocess.TimeoutExpired: If command exceeds timeout.
            subprocess.CalledProcessError: If command returns non-zero exit code.
        """
        try:
            if self.verbose:
                console.print(f"[dim]Running: {' '.join(command)}[/dim]")
            
            result = subprocess.run(
                command,
                capture_output=capture,
                text=True,
                timeout=timeout,
                check=False  # Don't raise on non-zero exit
            )
            
            # Combine stdout and stderr
            output = (result.stdout or "") + "\n" + (result.stderr or "")
            
            if self.verbose and result.returncode != 0:
                console.print(f"[yellow]Warning: Command exited with code {result.returncode}[/yellow]")
            
            return output.strip()
        
        except subprocess.TimeoutExpired:
            console.print(f"[red]✗ Command timed out after {timeout}s[/red]")
            return ""
        except Exception as e:
            console.print(f"[red]✗ Error running command: {e}[/red]")
            return ""
    
    def collect_domain(self, domain: str, progress_callback: Optional[Callable] = None) -> Dict[str, str]:
        """
        Collect OSINT data for a domain target.
        
        Args:
            domain (str): Target domain name.
            progress_callback (Optional[Callable]): Callback for progress updates.
        
        Returns:
            Dict[str, str]: Dictionary mapping source names to their output.
        """
        results = {}
        
        # Amass subdomain enumeration
        if 'amass' in self.tool_paths:
            if progress_callback:
                progress_callback(20)
            console.print("[cyan]  → Running Amass subdomain enumeration...[/cyan]")
            amass_output = self._run_command(['amass', 'enum', '-passive', '-d', domain])
            results['amass'] = amass_output
        
        # Sublist3r (alternative)
        elif 'sublist3r' in self.tool_paths:
            if progress_callback:
                progress_callback(20)
            console.print("[cyan]  → Running Sublist3r subdomain enumeration...[/cyan]")
            sublist3r_output = self._run_command(['sublist3r', '-d', domain])
            results['sublist3r'] = sublist3r_output
        
        # DNS records via dig
        if 'dig' in self.tool_paths:
            if progress_callback:
                progress_callback(40)
            console.print("[cyan]  → Querying DNS records...[/cyan]")
            dig_output = self._run_command(['dig', domain, 'ANY'])
            results['dig'] = dig_output
        
        # WHOIS lookup
        if 'whois' in self.tool_paths:
            if progress_callback:
                progress_callback(60)
            console.print("[cyan]  → Running WHOIS lookup...[/cyan]")
            whois_output = self._run_command(['whois', domain])
            results['whois'] = whois_output
        
        # Web scraping (basic)
        if progress_callback:
            progress_callback(80)
        console.print("[cyan]  → Fetching web content...[/cyan]")
        results['web_content'] = self._fetch_web_content(f"https://{domain}")
        
        if progress_callback:
            progress_callback(100)
        
        return results
    
    def collect_ip(self, ip: str, progress_callback: Optional[Callable] = None) -> Dict[str, str]:
        """
        Collect OSINT data for an IP address target.
        
        Args:
            ip (str): Target IP address.
            progress_callback (Optional[Callable]): Callback for progress updates.
        
        Returns:
            Dict[str, str]: Dictionary mapping source names to their output.
        """
        results = {}
        
        # Reverse DNS
        if 'dig' in self.tool_paths:
            if progress_callback:
                progress_callback(30)
            console.print("[cyan]  → Reverse DNS lookup...[/cyan]")
            results['reverse_dns'] = self._run_command(['dig', '-x', ip])
        
        # WHOIS for IP
        if 'whois' in self.tool_paths:
            if progress_callback:
                progress_callback(60)
            console.print("[cyan]  → WHOIS lookup for IP...[/cyan]")
            results['whois'] = self._run_command(['whois', ip])
        
        # Nmap port scan (basic, non-intrusive)
        if 'nmap' in self.tool_paths:
            if progress_callback:
                progress_callback(90)
            console.print("[cyan]  → Running basic port scan...[/cyan]")
            results['nmap'] = self._run_command(['nmap', '-sV', '-F', ip], timeout=120)
        
        if progress_callback:
            progress_callback(100)
        
        return results
    
    def collect_alias(self, alias: str, progress_callback: Optional[Callable] = None) -> Dict[str, str]:
        """
        Collect OSINT data for a username/alias target.
        
        Args:
            alias (str): Target username or alias.
            progress_callback (Optional[Callable]): Callback for progress updates.
        
        Returns:
            Dict[str, str]: Dictionary mapping source names to their output.
        """
        results = {}
        
        # Sherlock username search
        if 'sherlock' in self.tool_paths:
            if progress_callback:
                progress_callback(50)
            console.print("[cyan]  → Running Sherlock username search...[/cyan]")
            results['sherlock'] = self._run_command(['sherlock', alias], timeout=180)
        
        # GitHub user search
        if progress_callback:
            progress_callback(75)
        console.print("[cyan]  → Searching GitHub...[/cyan]")
        results['github'] = self._search_github_user(alias)
        
        # Pastebin search (if API available)
        if progress_callback:
            progress_callback(90)
        console.print("[cyan]  → Searching Pastebin...[/cyan]")
        results['pastebin'] = self._search_pastebin(alias)
        
        if progress_callback:
            progress_callback(100)
        
        return results
    
    def collect_email(self, email: str, progress_callback: Optional[Callable] = None) -> Dict[str, str]:
        """
        Collect OSINT data for an email address target.
        
        Args:
            email (str): Target email address.
            progress_callback (Optional[Callable]): Callback for progress updates.
        
        Returns:
            Dict[str, str]: Dictionary mapping source names to their output.
        """
        results = {}
        
        # Extract domain from email
        domain = email.split('@')[1] if '@' in email else None
        
        if domain:
            if progress_callback:
                progress_callback(30)
            console.print(f"[cyan]  → Analyzing domain: {domain}...[/cyan]")
            
            # WHOIS for domain
            if 'whois' in self.tool_paths:
                results['whois'] = self._run_command(['whois', domain])
        
        # GitHub search
        if progress_callback:
            progress_callback(60)
        console.print("[cyan]  → Searching GitHub for email...[/cyan]")
        results['github'] = self._search_github_email(email)
        
        # Pastebin search
        if progress_callback:
            progress_callback(90)
        console.print("[cyan]  → Searching Pastebin...[/cyan]")
        results['pastebin'] = self._search_pastebin(email)
        
        if progress_callback:
            progress_callback(100)
        
        return results
    
    def collect_hash(self, hash_value: str, progress_callback: Optional[Callable] = None) -> Dict[str, str]:
        """
        Collect OSINT data for a hash target.
        
        Args:
            hash_value (str): Target hash value.
            progress_callback (Optional[Callable]): Callback for progress updates.
        
        Returns:
            Dict[str, str]: Dictionary mapping source names to their output.
        """
        results = {}
        
        if progress_callback:
            progress_callback(50)
        console.print("[cyan]  → Searching for hash in public databases...[/cyan]")
        
        # Search GitHub for hash
        results['github'] = self._search_github_hash(hash_value)
        
        # Search Pastebin
        results['pastebin'] = self._search_pastebin(hash_value)
        
        if progress_callback:
            progress_callback(100)
        
        return results
    
    def collect_filename(self, filename: str, progress_callback: Optional[Callable] = None) -> Dict[str, str]:
        """
        Collect OSINT data for a filename target.
        
        Args:
            filename (str): Target filename (local path).
            progress_callback (Optional[Callable]): Callback for progress updates.
        
        Returns:
            Dict[str, str]: Dictionary mapping source names to their output.
        """
        results = {}
        
        # Check if file exists
        if not os.path.exists(filename):
            console.print(f"[red]✗ File not found: {filename}[/red]")
            return results
        
        # ExifTool metadata extraction
        if 'exiftool' in self.tool_paths:
            if progress_callback:
                progress_callback(50)
            console.print("[cyan]  → Extracting metadata with ExifTool...[/cyan]")
            results['exiftool'] = self._run_command(['exiftool', filename])
        
        # File command (Linux/Unix)
        if progress_callback:
            progress_callback(80)
        console.print("[cyan]  → Analyzing file type...[/cyan]")
        if shutil.which('file'):
            results['file_analysis'] = self._run_command(['file', filename])
        
        if progress_callback:
            progress_callback(100)
        
        return results
    
    def _fetch_web_content(self, url: str) -> str:
        """
        Fetch web content from a URL.
        
        Args:
            url (str): URL to fetch.
        
        Returns:
            str: Response text or error message.
        """
        try:
            response = requests.get(
                url,
                timeout=10,
                headers={'User-Agent': 'CTF-Sentinel/1.0'}
            )
            return response.text[:10000]  # Limit to first 10KB
        except Exception as e:
            return f"Error fetching {url}: {str(e)}"
    
    def _search_github_user(self, username: str) -> str:
        """
        Search for a GitHub user.
        
        Args:
            username (str): GitHub username.
        
        Returns:
            str: User profile information or empty string.
        """
        try:
            response = requests.get(
                f"https://api.github.com/users/{username}",
                timeout=10,
                headers={'User-Agent': 'CTF-Sentinel/1.0'}
            )
            if response.status_code == 200:
                return str(response.json())
            return ""
        except:
            return ""
    
    def _search_github_email(self, email: str) -> str:
        """
        Search GitHub commits by email.
        
        Args:
            email (str): Email address.
        
        Returns:
            str: Search results or empty string.
        """
        try:
            response = requests.get(
                f"https://api.github.com/search/commits?q=author-email:{email}",
                timeout=10,
                headers={
                    'User-Agent': 'CTF-Sentinel/1.0',
                    'Accept': 'application/vnd.github.cloak-preview'
                }
            )
            if response.status_code == 200:
                return str(response.json())
            return ""
        except:
            return ""
    
    def _search_github_hash(self, hash_value: str) -> str:
        """
        Search GitHub for a hash value.
        
        Args:
            hash_value (str): Hash to search for.
        
        Returns:
            str: Search results or empty string.
        """
        try:
            response = requests.get(
                f"https://api.github.com/search/code?q={hash_value}",
                timeout=10,
                headers={'User-Agent': 'CTF-Sentinel/1.0'}
            )
            if response.status_code == 200:
                return str(response.json())
            return ""
        except:
            return ""
    
    def _search_pastebin(self, query: str) -> str:
        """
        Search Pastebin (placeholder - requires API key).
        
        Args:
            query (str): Search query.
        
        Returns:
            str: Search results or placeholder message.
        """
        # Note: Pastebin requires API key for scraping
        # This is a placeholder implementation
        return f"Pastebin search for '{query}' (requires API key configuration)"
    
    def collect(
        self,
        target_type: str,
        target_value: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, str]:
        """
        Main collection dispatcher based on target type.
        
        Args:
            target_type (str): Type of target (domain, ip, alias, etc.).
            target_value (str): Target value.
            progress_callback (Optional[Callable]): Progress update callback.
        
        Returns:
            Dict[str, str]: Collected data from all sources.
        
        Raises:
            ValueError: If target_type is not supported.
        """
        collectors = {
            'domain': self.collect_domain,
            'ip': self.collect_ip,
            'alias': self.collect_alias,
            'email': self.collect_email,
            'hash': self.collect_hash,
            'filename': self.collect_filename
        }
        
        collector = collectors.get(target_type)
        if not collector:
            raise ValueError(f"Unsupported target type: {target_type}")
        
        return collector(target_value, progress_callback)
