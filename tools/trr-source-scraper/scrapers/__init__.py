"""
Scraper modules for the TRR Source Scraper.
"""

from trr_source_scraper.scrapers.mitre_attack import MitreAttackScraper, fetch_mitre_technique
from trr_source_scraper.scrapers.duckduckgo import DuckDuckGoScraper, search_technique_sources
from trr_source_scraper.scrapers.existing_trr import ExistingTRRScanner, scan_for_existing_trrs
from trr_source_scraper.scrapers.site_fetcher import SiteFetcher, enrich_search_results

__all__ = [
    'MitreAttackScraper',
    'fetch_mitre_technique',
    'DuckDuckGoScraper',
    'search_technique_sources',
    'ExistingTRRScanner',
    'scan_for_existing_trrs',
    'SiteFetcher',
    'enrich_search_results',
]