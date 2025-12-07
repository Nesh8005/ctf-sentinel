"""
CTF Sentinel - Correlation and Reporting Engine

This module handles entity correlation, relationship mapping, and report generation
with rich terminal output formatting.

Author: CTF Sentinel Team
Version: 1.0.0
"""

import json
from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich import box
from rich.text import Text

console = Console()


class CorrelationEngine:
    """
    Correlates entities across different sources to find connections.
    
    This engine builds a knowledge graph of entities and their relationships,
    helping to identify patterns and linked information.
    
    Attributes:
        correlation_map (Dict): Central data structure linking all entities.
        relationships (List): List of identified relationships.
    """
    
    def __init__(self):
        """Initialize the correlation engine."""
        self.correlation_map: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'type': None,
            'sources': set(),
            'linked_entities': set(),
            'metadata': {},
            'importance': 0.0
        })
        self.relationships: List[Dict] = []
    
    def add_raw_data(self, raw_data: Dict[str, str]):
        """
        Add raw data from collection sources.
        
        Args:
            raw_data (Dict[str, str]): Raw output from collection tools.
        """
        for source, content in raw_data.items():
            # Store raw data for reference
            if 'raw_data' not in self.correlation_map:
                self.correlation_map['raw_data'] = {
                    'type': 'metadata',
                    'sources': set(),
                    'data': {}
                }
            self.correlation_map['raw_data']['data'][source] = content
    
    def add_parsed_entities(self, parsed_entities: Dict[str, List[Dict]]):
        """
        Add parsed entities from AI analysis.
        
        Args:
            parsed_entities (Dict): Entities extracted by AI parser, grouped by source.
        """
        for source, entities in parsed_entities.items():
            for entity in entities:
                entity_key = self._normalize_key(entity['value'])
                entity_type = entity['type']
                
                # Update correlation map
                if self.correlation_map[entity_key]['type'] is None:
                    self.correlation_map[entity_key]['type'] = entity_type
                
                self.correlation_map[entity_key]['sources'].add(source)
                self.correlation_map[entity_key]['importance'] = max(
                    self.correlation_map[entity_key]['importance'],
                    entity.get('importance_score', 0.5)
                )
                
                # Store original entity data
                if 'occurrences' not in self.correlation_map[entity_key]:
                    self.correlation_map[entity_key]['occurrences'] = []
                self.correlation_map[entity_key]['occurrences'].append(entity)
    
    def _normalize_key(self, value: str) -> str:
        """
        Normalize entity value for consistent keying.
        
        Args:
            value (str): Raw entity value.
        
        Returns:
            str: Normalized key.
        """
        # Convert to lowercase and strip whitespace
        return value.lower().strip()
    
    def _find_entity_links(self):
        """
        Identify links between entities based on co-occurrence and metadata.
        """
        entities = [k for k in self.correlation_map.keys() if k != 'raw_data']
        
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                # Check if entities appear in same sources
                sources1 = self.correlation_map[entity1]['sources']
                sources2 = self.correlation_map[entity2]['sources']
                
                common_sources = sources1 & sources2
                
                if common_sources:
                    # Link entities
                    self.correlation_map[entity1]['linked_entities'].add(entity2)
                    self.correlation_map[entity2]['linked_entities'].add(entity1)
                    
                    # Record relationship
                    self.relationships.append({
                        'entity1': entity1,
                        'entity2': entity2,
                        'relationship': 'co_occurrence',
                        'sources': list(common_sources),
                        'strength': len(common_sources)
                    })
    
    def _calculate_entity_scores(self):
        """
        Calculate final importance scores based on links and sources.
        """
        for entity_key, entity_data in self.correlation_map.items():
            if entity_key == 'raw_data':
                continue
            
            # Base importance
            base_score = entity_data['importance']
            
            # Boost for multiple sources
            source_boost = min(len(entity_data['sources']) * 0.1, 0.3)
            
            # Boost for being linked to other entities
            link_boost = min(len(entity_data['linked_entities']) * 0.05, 0.2)
            
            # Final score
            final_score = min(base_score + source_boost + link_boost, 1.0)
            self.correlation_map[entity_key]['final_score'] = final_score
    
    def correlate(self) -> Dict[str, Any]:
        """
        Perform correlation analysis on all collected data.
        
        Returns:
            Dict: Correlation results including linked entities and statistics.
        """
        # Find entity relationships
        self._find_entity_links()
        
        # Calculate importance scores
        self._calculate_entity_scores()
        
        # Compile statistics
        entities = [k for k in self.correlation_map.keys() if k != 'raw_data']
        
        # Count high-value entities
        high_value = [
            k for k in entities
            if self.correlation_map[k].get('final_score', 0) >= 0.8
        ]
        
        # Count CTF-specific entities
        ctf_flags = [
            k for k in entities
            if self.correlation_map[k]['type'] == 'CTF_FLAG'
        ]
        
        api_keys = [
            k for k in entities
            if self.correlation_map[k]['type'] == 'API_KEY'
        ]
        
        credentials = [
            k for k in entities
            if self.correlation_map[k]['type'] == 'CREDENTIAL'
        ]
        
        # Count linked entities
        linked_count = sum(
            1 for k in entities
            if len(self.correlation_map[k]['linked_entities']) > 0
        )
        
        return {
            'total_entities': len(entities),
            'linked_count': linked_count,
            'high_value_count': len(high_value),
            'ctf_flags': ctf_flags,
            'api_keys': api_keys,
            'credentials': credentials,
            'relationships': self.relationships,
            'high_value_entities': high_value
        }
    
    def get_entity_details(self, entity_key: str) -> Optional[Dict]:
        """
        Get detailed information about a specific entity.
        
        Args:
            entity_key (str): Entity key to lookup.
        
        Returns:
            Optional[Dict]: Entity details or None if not found.
        """
        normalized_key = self._normalize_key(entity_key)
        return self.correlation_map.get(normalized_key)


class ReportGenerator:
    """
    Generates formatted intelligence reports using rich terminal output.
    
    Creates visually appealing, structured reports highlighting critical findings.
    """
    
    def __init__(self):
        """Initialize the report generator."""
        self.console = Console()
    
    def display_report(
        self,
        target_type: str,
        target_value: str,
        raw_data: Dict[str, str],
        entities: Dict[str, List[Dict]],
        correlation: Dict[str, Any]
    ):
        """
        Display a comprehensive intelligence report.
        
        Args:
            target_type (str): Type of target analyzed.
            target_value (str): Target value.
            raw_data (Dict): Raw collected data.
            entities (Dict): Parsed entities.
            correlation (Dict): Correlation results.
        """
        # Header
        self._display_header(target_type, target_value)
        
        # Executive Summary
        self._display_summary(raw_data, entities, correlation)
        
        # High-Value Targets (CTF Flags, Keys, etc.)
        self._display_high_value_targets(correlation)
        
        # Entity Breakdown
        self._display_entity_breakdown(entities, correlation)
        
        # Relationships
        self._display_relationships(correlation)
        
        # Sources Summary
        self._display_sources(raw_data)
    
    def _display_header(self, target_type: str, target_value: str):
        """Display report header."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        header_text = f"""
[bold cyan]INTELLIGENCE REPORT[/bold cyan]
[dim]{timestamp}[/dim]

[yellow]Target Type:[/yellow] {target_type.upper()}
[yellow]Target Value:[/yellow] {target_value}
        """
        
        console.print(Panel(header_text, box=box.DOUBLE, border_style="cyan"))
    
    def _display_summary(
        self,
        raw_data: Dict,
        entities: Dict,
        correlation: Dict
    ):
        """Display executive summary."""
        total_entities = correlation['total_entities']
        linked = correlation['linked_count']
        flags = len(correlation['ctf_flags'])
        keys = len(correlation['api_keys'])
        creds = len(correlation['credentials'])
        
        summary_table = Table(title="Executive Summary", box=box.ROUNDED)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Count", style="green", justify="right")
        
        summary_table.add_row("Data Sources", str(len(raw_data)))
        summary_table.add_row("Total Entities Extracted", str(total_entities))
        summary_table.add_row("Linked Entities", str(linked))
        summary_table.add_row("🚩 CTF Flags Found", str(flags), style="bold red")
        summary_table.add_row("🔑 API Keys Found", str(keys), style="bold yellow")
        summary_table.add_row("🔐 Credentials Found", str(creds), style="bold magenta")
        
        console.print(summary_table)
        console.print()
    
    def _display_high_value_targets(self, correlation: Dict):
        """Display high-value targets (flags, keys, credentials)."""
        flags = correlation['ctf_flags']
        keys = correlation['api_keys']
        creds = correlation['credentials']
        
        if not (flags or keys or creds):
            return
        
        console.print("[bold red]🚩 HIGH-VALUE TARGETS (AI-DETECTED)[/bold red]\n")
        
        # CTF Flags
        if flags:
            flag_table = Table(title="CTF Flags", box=box.HEAVY, border_style="red")
            flag_table.add_column("Flag", style="bold red")
            flag_table.add_column("Sources", style="cyan")
            flag_table.add_column("Linked To", style="yellow")
            
            for flag in flags:
                # Get from correlation engine (would need access)
                # Placeholder display
                flag_table.add_row(
                    flag,
                    "Multiple Sources",
                    "See correlations"
                )
            
            console.print(flag_table)
            console.print()
        
        # API Keys
        if keys:
            key_table = Table(title="API Keys & Tokens", box=box.HEAVY, border_style="yellow")
            key_table.add_column("Key/Token", style="bold yellow")
            key_table.add_column("Type", style="cyan")
            key_table.add_column("Sources", style="white")
            
            for key in keys:
                key_table.add_row(
                    key[:40] + "..." if len(key) > 40 else key,
                    "API_KEY",
                    "Multiple Sources"
                )
            
            console.print(key_table)
            console.print()
        
        # Credentials
        if creds:
            cred_table = Table(title="Credentials", box=box.HEAVY, border_style="magenta")
            cred_table.add_column("Credential", style="bold magenta")
            cred_table.add_column("Sources", style="cyan")
            
            for cred in creds:
                # Mask sensitive parts
                masked = cred[:20] + "***" if len(cred) > 20 else cred
                cred_table.add_row(masked, "Multiple Sources")
            
            console.print(cred_table)
            console.print()
    
    def _display_entity_breakdown(self, entities: Dict, correlation: Dict):
        """Display entity breakdown by type."""
        # Count entities by type
        entity_counts = defaultdict(int)
        
        for source_entities in entities.values():
            for entity in source_entities:
                entity_counts[entity['type']] += 1
        
        if not entity_counts:
            return
        
        breakdown_table = Table(title="Entity Breakdown by Type", box=box.ROUNDED)
        breakdown_table.add_column("Entity Type", style="cyan")
        breakdown_table.add_column("Count", style="green", justify="right")
        breakdown_table.add_column("Priority", style="yellow")
        
        # Sort by count
        sorted_types = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)
        
        for entity_type, count in sorted_types:
            # Determine priority
            if entity_type in ['CTF_FLAG', 'API_KEY', 'CREDENTIAL']:
                priority = "🔴 CRITICAL"
            elif entity_type in ['IP_ADDRESS', 'URL', 'EMAIL', 'FILE_PATH']:
                priority = "🟡 HIGH"
            else:
                priority = "🟢 MEDIUM"
            
            breakdown_table.add_row(entity_type, str(count), priority)
        
        console.print(breakdown_table)
        console.print()
    
    def _display_relationships(self, correlation: Dict):
        """Display entity relationships."""
        relationships = correlation.get('relationships', [])
        
        if not relationships:
            console.print("[dim]No entity relationships identified.[/dim]\n")
            return
        
        console.print(f"[bold cyan]🔗 Entity Relationships ({len(relationships)} found)[/bold cyan]\n")
        
        # Show top 10 strongest relationships
        sorted_rels = sorted(
            relationships,
            key=lambda x: x.get('strength', 0),
            reverse=True
        )[:10]
        
        rel_table = Table(box=box.SIMPLE)
        rel_table.add_column("Entity 1", style="yellow")
        rel_table.add_column("↔", style="dim")
        rel_table.add_column("Entity 2", style="yellow")
        rel_table.add_column("Type", style="cyan")
        rel_table.add_column("Strength", style="green")
        
        for rel in sorted_rels:
            rel_table.add_row(
                rel['entity1'][:30],
                "↔",
                rel['entity2'][:30],
                rel['relationship'],
                str(rel.get('strength', 0))
            )
        
        console.print(rel_table)
        console.print()
    
    def _display_sources(self, raw_data: Dict):
        """Display data sources summary."""
        source_table = Table(title="Data Sources", box=box.ROUNDED)
        source_table.add_column("Source", style="cyan")
        source_table.add_column("Data Size", style="green", justify="right")
        source_table.add_column("Status", style="yellow")
        
        for source, content in raw_data.items():
            size = len(content)
            status = "✓ SUCCESS" if size > 0 else "✗ NO DATA"
            
            source_table.add_row(
                source.upper(),
                f"{size:,} bytes",
                status
            )
        
        console.print(source_table)
        console.print()
    
    def save_to_file(
        self,
        filepath: str,
        target_type: str,
        target_value: str,
        raw_data: Dict,
        entities: Dict,
        correlation: Dict
    ):
        """
        Save report to JSON file.
        
        Args:
            filepath (str): Output file path.
            target_type (str): Target type.
            target_value (str): Target value.
            raw_data (Dict): Raw data.
            entities (Dict): Parsed entities.
            correlation (Dict): Correlation results.
        """
        report_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'target_type': target_type,
                'target_value': target_value,
                'tool': 'CTF Sentinel',
                'version': '1.0.0'
            },
            'summary': {
                'total_sources': len(raw_data),
                'total_entities': correlation['total_entities'],
                'linked_entities': correlation['linked_count'],
                'ctf_flags': len(correlation['ctf_flags']),
                'api_keys': len(correlation['api_keys']),
                'credentials': len(correlation['credentials'])
            },
            'high_value_targets': {
                'ctf_flags': correlation['ctf_flags'],
                'api_keys': correlation['api_keys'],
                'credentials': correlation['credentials']
            },
            'entities': {
                source: [
                    {k: v for k, v in ent.items() if k not in ['start', 'end']}
                    for ent in ents
                ]
                for source, ents in entities.items()
            },
            'relationships': correlation['relationships'],
            'sources': {
                source: {
                    'size': len(content),
                    'preview': content[:500] if content else None
                }
                for source, content in raw_data.items()
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]✓[/green] Report saved to JSON: {filepath}")
