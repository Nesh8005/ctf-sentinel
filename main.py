#!/usr/bin/env python3
"""
CTF Sentinel - Main CLI Interface

This is the entry point for the CTF OSINT tool. It handles command-line arguments,
orchestrates the data collection and AI analysis pipeline, and displays results.

Author: CTF Sentinel Team
Version: 1.0.0
"""

import argparse
import sys
from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich import print as rprint

from collection_engine import CollectionEngine
from ai_parser import AIParser
from correlation_report import CorrelationEngine, ReportGenerator

# Initialize Rich console for beautiful output
console = Console()

# Supported target types
SUPPORTED_TARGETS = ['domain', 'ip', 'alias', 'hash', 'email', 'filename']


def parse_arguments() -> argparse.Namespace:
    """
    Parse and validate command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments containing target_type and value.
    
    Raises:
        SystemExit: If arguments are invalid or missing.
    """
    parser = argparse.ArgumentParser(
        description='CTF Sentinel - AI-Enhanced OSINT Tool for CTF Competitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --target-type domain --value example.com
  python main.py --target-type alias --value johnny_ctf
  python main.py --target-type email --value suspect@example.com
  python main.py --target-type ip --value 192.168.1.1
  python main.py --target-type hash --value 5d41402abc4b2a76b9719d911017c592
  python main.py --target-type filename --value suspect.jpg
        """
    )
    
    parser.add_argument(
        '--target-type',
        type=str,
        required=True,
        choices=SUPPORTED_TARGETS,
        help=f'Type of target to investigate ({", ".join(SUPPORTED_TARGETS)})'
    )
    
    parser.add_argument(
        '--value',
        type=str,
        required=True,
        help='Target value to investigate (e.g., domain name, IP address, username)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Optional: Save results to file (JSON format)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    
    parser.add_argument(
        '--skip-ai',
        action='store_true',
        help='Skip AI/NER analysis (faster but less intelligent)'
    )
    
    return parser.parse_args()


def display_banner():
    """Display the CTF Sentinel banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🔍 CTF SENTINEL 🔍                           ║
    ║         AI-Enhanced OSINT for CTF Competitions            ║
    ║                                                           ║
    ║  Speed • Intelligence • Correlation • Flag Detection      ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", border_style="bright_blue"))


def main():
    """
    Main execution flow.
    
    Orchestrates the entire OSINT pipeline:
    1. Parse CLI arguments
    2. Collect data from external tools
    3. Apply AI/NER analysis
    4. Correlate findings
    5. Generate and display report
    """
    # Display banner
    display_banner()
    
    # Parse arguments
    args = parse_arguments()
    
    # Display target information
    console.print(f"\n[bold yellow]Target Type:[/bold yellow] {args.target_type}")
    console.print(f"[bold yellow]Target Value:[/bold yellow] {args.value}\n")
    
    try:
        # Initialize engines
        collection_engine = CollectionEngine(verbose=args.verbose)
        correlation_engine = CorrelationEngine()
        report_generator = ReportGenerator()
        
        # Step 1: Data Collection
        console.print("[bold green]═══ Phase 1: Data Collection ═══[/bold green]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            collection_task = progress.add_task(
                "[cyan]Gathering intelligence from external tools...",
                total=100
            )
            
            # Collect data based on target type
            raw_data = collection_engine.collect(
                target_type=args.target_type,
                target_value=args.value,
                progress_callback=lambda p: progress.update(collection_task, completed=p)
            )
            
            progress.update(collection_task, completed=100)
        
        console.print(f"[green]✓[/green] Collected {len(raw_data)} data sources\n")
        
        # Step 2: AI Analysis (if not skipped)
        parsed_entities = {}
        
        if not args.skip_ai:
            console.print("[bold green]═══ Phase 2: AI/NER Analysis ═══[/bold green]\n")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                ai_task = progress.add_task(
                    "[cyan]Applying AI models for entity extraction...",
                    total=None
                )
                
                # Initialize AI parser
                ai_parser = AIParser(verbose=args.verbose)
                
                # Parse all collected data
                for source, content in raw_data.items():
                    entities = ai_parser.extract_entities(content, source)
                    parsed_entities[source] = entities
                
                progress.update(ai_task, completed=100)
            
            # Count total entities found
            total_entities = sum(len(entities) for entities in parsed_entities.values())
            console.print(f"[green]✓[/green] Extracted {total_entities} entities using AI/NER\n")
        
        # Step 3: Correlation
        console.print("[bold green]═══ Phase 3: Correlation & Analysis ═══[/bold green]\n")
        
        with console.status("[cyan]Correlating findings and identifying patterns..."):
            correlation_engine.add_raw_data(raw_data)
            
            if parsed_entities:
                correlation_engine.add_parsed_entities(parsed_entities)
            
            correlation_results = correlation_engine.correlate()
        
        console.print(f"[green]✓[/green] Identified {correlation_results['linked_count']} linked entities\n")
        
        # Step 4: Generate and Display Report
        console.print("[bold green]═══ Phase 4: Intelligence Report ═══[/bold green]\n")
        
        report_generator.display_report(
            target_type=args.target_type,
            target_value=args.value,
            raw_data=raw_data,
            entities=parsed_entities,
            correlation=correlation_results
        )
        
        # Step 5: Save to file (if requested)
        if args.output:
            report_generator.save_to_file(
                filepath=args.output,
                target_type=args.target_type,
                target_value=args.value,
                raw_data=raw_data,
                entities=parsed_entities,
                correlation=correlation_results
            )
            console.print(f"\n[green]✓[/green] Report saved to: {args.output}")
        
        console.print("\n[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
        console.print("[bold green]✓ Analysis Complete![/bold green]")
        console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]\n")
        
    except KeyboardInterrupt:
        console.print("\n\n[bold red]✗ Operation cancelled by user[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n\n[bold red]✗ Error: {str(e)}[/bold red]")
        if args.verbose:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
