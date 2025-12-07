"""
CTF Sentinel - AI/NLP Processing Module

This module handles Named Entity Recognition (NER) using spaCy, including custom
pattern matching for CTF-specific entities like flags, API keys, and file paths.

Author: CTF Sentinel Team
Version: 1.0.0
"""

import re
from typing import Dict, List, Tuple, Optional
import spacy
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span
from rich.console import Console

console = Console()


class AIParser:
    """
    AI-powered entity extraction and analysis using spaCy NLP.
    
    This class provides Named Entity Recognition (NER) with custom patterns
    for CTF-specific entities like flags, API keys, credentials, and file paths.
    
    Attributes:
        nlp (Language): spaCy language model.
        matcher (Matcher): spaCy pattern matcher for custom entities.
        verbose (bool): Enable verbose logging.
    """
    
    def __init__(self, model: str = "en_core_web_sm", verbose: bool = False):
        """
        Initialize the AI Parser with spaCy model and custom patterns.
        
        Args:
            model (str): spaCy model to load (default: en_core_web_sm).
            verbose (bool): Enable verbose output.
        
        Raises:
            OSError: If spaCy model is not installed.
        """
        self.verbose = verbose
        
        try:
            if self.verbose:
                console.print(f"[dim]Loading spaCy model: {model}...[/dim]")
            self.nlp = spacy.load(model)
        except OSError:
            console.print(f"[red]✗ spaCy model '{model}' not found.[/red]")
            console.print(f"[yellow]Run: python -m spacy download {model}[/yellow]")
            raise
        
        # Initialize custom matcher
        self.matcher = Matcher(self.nlp.vocab)
        self._setup_custom_patterns()
        
        if self.verbose:
            console.print("[green]✓[/green] AI Parser initialized")
    
    def _setup_custom_patterns(self):
        """
        Set up custom pattern matching rules for CTF-specific entities.
        
        Defines patterns for:
        - CTF flags (various formats)
        - API keys and tokens
        - File paths
        - Credentials
        - IP addresses
        - URLs
        - Hashes
        """
        # CTF Flag patterns
        flag_patterns = [
            # Standard CTF{...} format
            [{"TEXT": {"REGEX": r"CTF\{[^}]+\}"}}],
            [{"TEXT": {"REGEX": r"flag\{[^}]+\}"}}],
            [{"TEXT": {"REGEX": r"FLAG\{[^}]+\}"}}],
            # Other common formats
            [{"TEXT": {"REGEX": r"[A-Z]{2,10}\{[^}]{10,}\}"}}],
        ]
        
        # API Key patterns
        api_key_patterns = [
            # AWS keys
            [{"TEXT": {"REGEX": r"AKIA[0-9A-Z]{16}"}}],
            # Generic API keys
            [{"TEXT": {"REGEX": r"api[_-]?key[=:]\s*['\"]?[a-zA-Z0-9]{20,}['\"]?"}}],
            [{"TEXT": {"REGEX": r"token[=:]\s*['\"]?[a-zA-Z0-9]{20,}['\"]?"}}],
            # GitHub tokens
            [{"TEXT": {"REGEX": r"ghp_[a-zA-Z0-9]{36}"}}],
            [{"TEXT": {"REGEX": r"gho_[a-zA-Z0-9]{36}"}}],
        ]
        
        # File path patterns
        file_path_patterns = [
            # Unix paths
            [{"TEXT": {"REGEX": r"/etc/[a-z]+(/[a-z._-]+)*"}}],
            [{"TEXT": {"REGEX": r"/var/[a-z]+(/[a-z._-]+)*"}}],
            [{"TEXT": {"REGEX": r"/home/[a-z]+(/[a-z._-]+)*"}}],
            [{"TEXT": {"REGEX": r"~/.ssh/[a-z._-]+"}}],
            # Windows paths
            [{"TEXT": {"REGEX": r"[A-Z]:\\[^<>:\"|?*\n]+"}}],
        ]
        
        # Credential patterns
        credential_patterns = [
            # Username:password
            [{"TEXT": {"REGEX": r"[a-zA-Z0-9_-]+:[a-zA-Z0-9!@#$%^&*]{8,}"}}],
            # Password fields
            [{"TEXT": {"REGEX": r"pass(word)?[=:]\s*['\"]?[a-zA-Z0-9!@#$%^&*]{6,}['\"]?"}}],
        ]
        
        # Register patterns with matcher
        self.matcher.add("CTF_FLAG", flag_patterns)
        self.matcher.add("API_KEY", api_key_patterns)
        self.matcher.add("FILE_PATH", file_path_patterns)
        self.matcher.add("CREDENTIAL", credential_patterns)
        
        if self.verbose:
            console.print("[dim]Custom NER patterns loaded[/dim]")
    
    def _extract_regex_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract entities using regex patterns (backup method).
        
        This method provides regex-based extraction for entities that might
        be missed by spaCy's pattern matcher.
        
        Args:
            text (str): Input text to analyze.
        
        Returns:
            List[Dict[str, str]]: List of extracted entities with type and value.
        """
        entities = []
        
        # Regex patterns for various entities
        patterns = {
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'IP_ADDRESS': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'URL': r'https?://[^\s<>"{}|\\^`\[\]]+',
            'MD5_HASH': r'\b[a-fA-F0-9]{32}\b',
            'SHA1_HASH': r'\b[a-fA-F0-9]{40}\b',
            'SHA256_HASH': r'\b[a-fA-F0-9]{64}\b',
            'SUBDOMAIN': r'\b[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)*\.[a-z]{2,}\b',
            'PORT': r'\bport[:\s]+(\d{1,5})\b',
        }
        
        for entity_type, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'type': entity_type,
                    'value': match.group(0),
                    'start': match.start(),
                    'end': match.end()
                })
        
        return entities
    
    def extract_entities(self, text: str, source: str = "unknown") -> List[Dict[str, any]]:
        """
        Extract all entities from text using spaCy NER and custom patterns.
        
        This is the main entity extraction method combining:
        - spaCy's built-in NER
        - Custom pattern matching
        - Regex-based extraction
        
        Args:
            text (str): Input text to analyze.
            source (str): Source identifier for provenance tracking.
        
        Returns:
            List[Dict[str, any]]: List of extracted entities with metadata.
        """
        if not text or len(text.strip()) == 0:
            return []
        
        entities = []
        
        # Limit text length to avoid performance issues
        max_length = 1000000  # 1MB
        if len(text) > max_length:
            text = text[:max_length]
            if self.verbose:
                console.print(f"[yellow]Warning: Text truncated to {max_length} chars[/yellow]")
        
        # Process with spaCy
        doc = self.nlp(text)
        
        # Extract standard NER entities
        for ent in doc.ents:
            entities.append({
                'type': ent.label_,
                'value': ent.text,
                'start': ent.start_char,
                'end': ent.end_char,
                'source': source,
                'method': 'spacy_ner'
            })
        
        # Extract custom pattern matches
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            entities.append({
                'type': label,
                'value': span.text,
                'start': span.start_char,
                'end': span.end_char,
                'source': source,
                'method': 'pattern_match'
            })
        
        # Extract regex-based entities
        regex_entities = self._extract_regex_entities(text)
        for ent in regex_entities:
            ent['source'] = source
            ent['method'] = 'regex'
            entities.append(ent)
        
        # Remove duplicates (same value and type)
        unique_entities = []
        seen = set()
        for ent in entities:
            key = (ent['type'], ent['value'])
            if key not in seen:
                seen.add(key)
                unique_entities.append(ent)
        
        if self.verbose:
            console.print(f"[dim]Extracted {len(unique_entities)} unique entities from {source}[/dim]")
        
        return unique_entities
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Perform basic sentiment analysis on text.
        
        This is a placeholder for sentiment analysis. For production use,
        integrate libraries like VADER, TextBlob, or transformers.
        
        Args:
            text (str): Text to analyze.
        
        Returns:
            Dict[str, float]: Sentiment scores (positive, neutral, negative).
        """
        # Placeholder implementation
        # In production, use VADER or similar
        return {
            'positive': 0.0,
            'neutral': 1.0,
            'negative': 0.0,
            'compound': 0.0
        }
    
    def extract_relationships(
        self,
        entities: List[Dict[str, any]]
    ) -> List[Tuple[Dict, Dict, str]]:
        """
        Extract relationships between entities.
        
        Identifies potential connections between discovered entities
        based on co-occurrence and context.
        
        Args:
            entities (List[Dict]): List of extracted entities.
        
        Returns:
            List[Tuple]: List of (entity1, entity2, relationship_type) tuples.
        """
        relationships = []
        
        # Simple co-occurrence based relationship detection
        # Group entities by source
        by_source = {}
        for ent in entities:
            source = ent.get('source', 'unknown')
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(ent)
        
        # Find relationships within same source
        for source, source_entities in by_source.items():
            for i, ent1 in enumerate(source_entities):
                for ent2 in source_entities[i+1:]:
                    # Check if entities are close in text
                    if abs(ent1.get('start', 0) - ent2.get('start', 0)) < 1000:
                        relationships.append((ent1, ent2, 'co_occurrence'))
        
        return relationships
    
    def score_entity_importance(self, entity: Dict[str, any]) -> float:
        """
        Calculate an importance score for an entity.
        
        Higher scores indicate entities more likely to be relevant for CTF.
        
        Args:
            entity (Dict): Entity to score.
        
        Returns:
            float: Importance score (0.0 to 1.0).
        """
        score = 0.5  # Base score
        
        entity_type = entity.get('type', '')
        
        # CTF-specific entities get highest priority
        if entity_type in ['CTF_FLAG', 'API_KEY', 'CREDENTIAL']:
            score = 1.0
        
        # Technical entities get high priority
        elif entity_type in ['IP_ADDRESS', 'URL', 'FILE_PATH', 'EMAIL']:
            score = 0.8
        
        # Named entities get medium priority
        elif entity_type in ['PERSON', 'ORG', 'GPE']:
            score = 0.6
        
        # Hashes get medium-high priority
        elif 'HASH' in entity_type:
            score = 0.75
        
        return score
    
    def filter_noise(
        self,
        entities: List[Dict[str, any]],
        min_score: float = 0.3
    ) -> List[Dict[str, any]]:
        """
        Filter out low-value entities (noise reduction).
        
        Args:
            entities (List[Dict]): Entities to filter.
            min_score (float): Minimum importance score threshold.
        
        Returns:
            List[Dict]: Filtered entities above threshold.
        """
        filtered = []
        
        for entity in entities:
            score = self.score_entity_importance(entity)
            entity['importance_score'] = score
            
            if score >= min_score:
                filtered.append(entity)
        
        if self.verbose:
            removed = len(entities) - len(filtered)
            console.print(f"[dim]Filtered out {removed} low-value entities[/dim]")
        
        return filtered
