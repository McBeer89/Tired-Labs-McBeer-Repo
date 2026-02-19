#!/usr/bin/env python3
"""
TRR Source Scraper - Main Entry Point

A tool for scraping the web to find potential research sources
for MITRE ATT&CK techniques when creating Technique Research Reports.

Usage:
    python -m trr_source_scraper T1003.006
    python -m trr_source_scraper T1003.006 --name "DCSync"
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Use absolute imports when running as module
from trr_source_scraper.scrapers import (
    fetch_mitre_technique,
    search_technique_sources,
    scan_for_existing_trrs,
    enrich_search_results,
)
from trr_source_scraper.utils import (
    ConfigManager,
    RateLimiter,
    validate_technique_id,
    normalize_technique_id,
    clean_text,
    format_date,
    get_category_for_domain,
)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Scrape the web for research sources on MITRE ATT&CK techniques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m trr_source_scraper T1003.006
    python -m trr_source_scraper T1003.006 --name "DCSync"
    python -m trr_source_scraper T1003.006 --output ./research/ --max-per-category 5
        """
    )
    
    parser.add_argument(
        "technique_id",
        help="MITRE ATT&CK technique ID (e.g., T1003.006 or T1003)"
    )
    
    parser.add_argument(
        "--name", "-n",
        help="Technique name for better search results (e.g., 'DCSync')"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output directory for the markdown report (default: ./output/)"
    )
    
    parser.add_argument(
        "--max-per-category", "-m",
        type=int,
        help="Maximum number of results per category (default: from config)"
    )
    
    parser.add_argument(
        "--no-enrich",
        action="store_true",
        help="Skip fetching page metadata (faster but less detail)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print detailed progress information"
    )
    
    return parser.parse_args()


def print_progress(message: str, verbose: bool = False):
    """Print progress message if verbose mode is enabled."""
    if verbose:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")


def generate_markdown_report(
    technique_id: str,
    technique_info: Optional[Dict],
    existing_trrs: List[Dict],
    existing_ddms: List[Dict],
    search_results: Dict[str, List[Dict]],
    config: ConfigManager
) -> str:
    """
    Generate a markdown report with all gathered information.
    """
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Header
    technique_name = technique_info.get('name', 'Unknown') if technique_info else 'Unknown'
    lines.append(f"# Research Sources for {technique_id} - {technique_name}")
    lines.append("")
    lines.append(f"**Generated:** {timestamp}")
    lines.append(f"**Technique:** {technique_id}")
    if technique_info:
        lines.append(f"**Tactics:** {', '.join(technique_info.get('tactics', []))}")
        lines.append(f"**Platforms:** {', '.join(technique_info.get('platforms', []))}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # MITRE ATT&CK Reference
    if technique_info:
        lines.append("## MITRE ATT&CK Reference")
        lines.append("")
        lines.append(f"### [{technique_id} - {technique_info.get('name', 'Unknown')}]({technique_info.get('url', '')})")
        lines.append("")
        description = technique_info.get('description', '')
        if description:
            lines.append(f"> **Summary:** {clean_text(description, 300)}")
            lines.append("")
        
        if technique_info.get('data_sources'):
            lines.append(f"**Data Sources:** {', '.join(technique_info['data_sources'])}")
            lines.append("")
        
        if technique_info.get('permissions_required'):
            lines.append(f"**Permissions Required:** {', '.join(technique_info['permissions_required'])}")
            lines.append("")
        
        if technique_info.get('references'):
            lines.append("**MITRE References:**")
            lines.append("")
            for ref in technique_info['references'][:5]:
                lines.append(f"- [{ref.get('name', 'Reference')}]({ref.get('url', '')})")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Existing TRRs
    if existing_trrs:
        lines.append("## Existing TRRs in Repository")
        lines.append("")
        lines.append("The following existing TRRs were found that may contain relevant information:")
        lines.append("")
        
        for trr in sorted(existing_trrs, key=lambda x: x.get('match_score', 0), reverse=True):
            match_label = {
                'exact': 'Exact Match',
                'parent': 'Parent Technique',
                'name': 'Name Match'
            }.get(trr.get('match_type', ''), 'Related')
            
            lines.append(f"### {trr.get('file_name', 'Unknown')}")
            lines.append("")
            if trr.get('trr_id'):
                lines.append(f"**TRR ID:** {trr['trr_id']}")
            lines.append(f"**Match Type:** {match_label}")
            if trr.get('title'):
                lines.append(f"**Title:** {trr['title']}")
            if trr.get('techniques'):
                lines.append(f"**Techniques:** {', '.join(trr['techniques'])}")
            lines.append("")
            
            if trr.get('references'):
                lines.append("**References from TRR:**")
                for ref in trr['references'][:5]:
                    lines.append(f"- [{ref.get('name', 'Reference')}]({ref.get('url', '')})")
                lines.append("")
            
            lines.append(f"**File:** `{trr.get('file_path', '')}`")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Existing DDMs
    if existing_ddms:
        lines.append("## Existing DDMs in Repository")
        lines.append("")
        for ddm in existing_ddms:
            lines.append(f"- `{ddm.get('file_name', '')}`")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Search Results by Category
    category_labels = {
        'security_research': 'Security Research Blogs',
        'microsoft_docs': 'Microsoft Documentation',
        'conferences': 'Conference Presentations',
        'github': 'GitHub Resources',
        'academic': 'Academic Papers',
    }
    
    priority_order = ['security_research', 'microsoft_docs', 'conferences', 'github', 'academic']
    
    total_sources = 0
    high_priority_count = 0
    
    for category in priority_order:
        results = search_results.get(category, [])
        if not results:
            continue
        
        total_sources += len(results)
        priority = config.trusted_sources.get(category, {}).get('priority', 'medium')
        if priority == 'high':
            high_priority_count += len(results)
        
        label = category_labels.get(category, category.replace('_', '').title())
        lines.append(f"## {label}")
        lines.append("")
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'Untitled')
            url = result.get('url', '')
            description = result.get('description', '')
            date = result.get('date')
            domain = result.get('domain', '')
            
            lines.append(f"### {i}. [{title}]({url})")
            lines.append("")
            
            if domain:
                lines.append(f"> **Source:** {domain}")
            if date:
                lines.append(f"> **Published:** {format_date(date)}")
            lines.append("")
            
            if description:
                excerpt_len = config.output_settings.get('excerpt_length', 200)
                lines.append(f"**Excerpt:** {clean_text(description, excerpt_len)}")
                lines.append("")
            
            lines.append(f"**Relevance:** {priority.title()}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Search Queries Used
    lines.append("## Search Queries Used")
    lines.append("")
    lines.append("To find additional sources, you can manually run these searches:")
    lines.append("")
    lines.append(f"- `{technique_id} {technique_name} detection`")
    lines.append(f"- `{technique_id} {technique_name} site:specterops.io`")
    lines.append(f"- `{technique_name} attack technique analysis`")
    lines.append(f"- `{technique_id} site:github.com`")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Summary
    lines.append(f"*Total sources found: {total_sources}*")
    lines.append(f"*High priority sources: {high_priority_count}*")
    
    return '\n'.join(lines)


def main():
    """Main entry point for the TRR Source Scraper."""
    args = parse_args()
    
    # Validate technique ID
    technique_id = normalize_technique_id(args.technique_id)
    if not validate_technique_id(technique_id):
        print(f"Error: Invalid technique ID format: {args.technique_id}")
        print("Expected format: T1003 or T1003.006")
        sys.exit(1)
    
    print(f"TRR Source Scraper - Researching {technique_id}")
    print("=" * 50)
    
    # Load configuration
    config = ConfigManager()
    max_per_category = args.max_per_category or config.search_settings.get('max_results_per_category', 10)
    user_agent = config.search_settings.get('user_agent', 'TRR-Source-Scraper/1.0')
    
    # Step 1: Fetch MITRE ATT&CK information
    print_progress("Fetching MITRE ATT&CK information...", args.verbose)
    technique_info = fetch_mitre_technique(technique_id, user_agent)
    
    if technique_info:
        print(f"Found: {technique_info.get('name', 'Unknown')}")
    else:
        print("Warning: Could not fetch MITRE ATT&CK page. Continuing with limited info.")
    
    # Get technique name
    technique_name = args.name
    if not technique_name and technique_info:
        technique_name = technique_info.get('name', '')
    
    if not technique_name:
        technique_name = technique_id
    
    # Step 2: Check for existing TRRs
    print_progress("Checking for existing TRRs...", args.verbose)
    existing_trrs, existing_ddms = scan_for_existing_trrs(technique_id, technique_name)
    
    if existing_trrs:
        print(f"Found {len(existing_trrs)} existing TRR(s)")
    if existing_ddms:
        print(f"Found {len(existing_ddms)} existing DDM(s)")
    
    # Step 3: Search for sources
    print_progress("Searching for sources...", args.verbose)
    print(f"Searching across {len(config.trusted_sources)} categories...")
    
    search_results = search_technique_sources(
        technique_id=technique_id,
        technique_name=technique_name,
        categories=config.trusted_sources,
        max_per_category=max_per_category,
        user_agent=user_agent
    )
    
    # Count total results
    total_results = sum(len(results) for results in search_results.values())
    print(f"Found {total_results} potential sources")
    
    # Step 4: Enrich results with metadata (optional)
    if not args.no_enrich and total_results > 0:
        print_progress("Enriching results with page metadata...", args.verbose)
        print("Fetching page details (this may take a moment)...")
        
        for category, results in search_results.items():
            if results:
                search_results[category] = enrich_search_results(results, user_agent)
                print_progress(f"  Enriched {category}: {len(search_results[category])} results", args.verbose)
    
    # Step 5: Generate report
    print_progress("Generating markdown report...", args.verbose)
    report = generate_markdown_report(
        technique_id=technique_id,
        technique_info=technique_info,
        existing_trrs=existing_trrs,
        existing_ddms=existing_ddms,
        search_results=search_results,
        config=config
    )
    
    # Determine output path
    output_dir = args.output or Path(config.output_settings.get('default_output_dir', 'output'))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{technique_id}_sources.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("=" * 50)
    print(f"Report saved to: {output_file}")
    print(f"Total sources found: {total_results}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())