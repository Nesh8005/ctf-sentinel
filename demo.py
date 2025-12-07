#!/usr/bin/env python3
"""
CTF Sentinel - Demo Script

This script demonstrates the basic functionality of CTF Sentinel
with example targets that don't require external tools.

Run this to verify your installation works correctly.
"""

import sys
from rich.console import Console
from rich.panel import Panel

console = Console()


def main():
    """Run demo scenarios."""
    
    console.print(Panel.fit(
        "[bold cyan]CTF Sentinel - Demo Script[/bold cyan]\n\n"
        "This demo will test basic functionality without requiring\n"
        "external OSINT tools to be installed.",
        border_style="cyan"
    ))
    
    console.print("\n[yellow]Demo 1: Email Entity Extraction[/yellow]")
    console.print("[dim]Testing AI/NER on sample text with CTF-relevant entities...[/dim]\n")
    
    sample_text = """
    Admin contact: admin@ctfchallenge.com
    Server IP: 192.168.1.100
    Flag location: CTF{test_flag_demo_123}
    API Key: AKIAIOSFODNN7EXAMPLE
    Backup at /etc/backup/data.tar.gz
    """
    
    try:
        from ai_parser import AIParser
        
        parser = AIParser(verbose=True)
        entities = parser.extract_entities(sample_text, source="demo")
        
        console.print(f"[green]✓[/green] Extracted {len(entities)} entities:\n")
        
        for entity in entities:
            console.print(f"  • [{entity['type']}] {entity['value']}")
        
        console.print("\n[green]✓ Demo 1 Complete![/green]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Demo failed: {e}[/red]")
        console.print("\n[yellow]Make sure you've installed dependencies:[/yellow]")
        console.print("  pip install -r requirements.txt")
        console.print("  python -m spacy download en_core_web_sm")
        return 1
    
    console.print("\n[yellow]Demo 2: Correlation Engine[/yellow]")
    console.print("[dim]Testing entity correlation and linking...[/dim]\n")
    
    try:
        from correlation_report import CorrelationEngine
        
        engine = CorrelationEngine()
        
        # Add sample entities
        sample_entities = {
            'source1': [
                {'value': 'admin@example.com', 'type': 'EMAIL', 'source': 'source1', 'importance_score': 0.8},
                {'value': '192.168.1.1', 'type': 'IP_ADDRESS', 'source': 'source1', 'importance_score': 0.8},
            ],
            'source2': [
                {'value': 'admin@example.com', 'type': 'EMAIL', 'source': 'source2', 'importance_score': 0.8},
                {'value': 'CTF{demo_flag}', 'type': 'CTF_FLAG', 'source': 'source2', 'importance_score': 1.0},
            ]
        }
        
        engine.add_parsed_entities(sample_entities)
        results = engine.correlate()
        
        console.print(f"[green]✓[/green] Correlation results:")
        console.print(f"  • Total entities: {results['total_entities']}")
        console.print(f"  • Linked entities: {results['linked_count']}")
        console.print(f"  • CTF flags: {len(results['ctf_flags'])}")
        console.print(f"  • Relationships: {len(results['relationships'])}")
        
        console.print("\n[green]✓ Demo 2 Complete![/green]\n")
        
    except Exception as e:
        console.print(f"[red]✗ Demo failed: {e}[/red]")
        return 1
    
    console.print("\n" + "="*60)
    console.print("[bold green]✓ All Demos Completed Successfully![/bold green]")
    console.print("="*60)
    console.print("\n[cyan]Your CTF Sentinel installation is working correctly![/cyan]")
    console.print("\n[yellow]Next steps:[/yellow]")
    console.print("  1. Read README.md for full documentation")
    console.print("  2. Check USAGE_EXAMPLES.md for CTF scenarios")
    console.print("  3. Try: python main.py --target-type domain --value example.com")
    console.print("  4. Install external tools (see INSTALL.md) for full functionality\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
