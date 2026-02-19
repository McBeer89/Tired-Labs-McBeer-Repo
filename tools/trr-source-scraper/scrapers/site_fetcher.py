"""
Site metadata fetcher for extracting details from URLs.
"""

from typing import Dict, Optional, List
from bs4 import BeautifulSoup
import requests

from trr_source_scraper.utils import (
    RateLimiter,
    clean_text,
    create_session,
    extract_domain,
    is_valid_url,
    extract_meta_description,
    extract_title,
    extract_date,
)


class SiteFetcher:
    """
    Fetches and extracts metadata from web pages.
    """
    
    def __init__(self, rate_limiter: Optional[RateLimiter] = None, user_agent: str = ""):
        self.rate_limiter = rate_limiter or RateLimiter(delay=2.0)
        self.session = create_session(user_agent or "TRR-Source-Scraper/1.0")
    
    def fetch_page_metadata(self, url: str) -> Optional[Dict]:
        """
        Fetch metadata from a single URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            Dictionary with metadata or None if failed
        """
        if not is_valid_url(url):
            return None
        
        self.rate_limiter.wait()
        
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            return None
        
        # Check content type
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            # Not an HTML page, return basic info
            return {
                'url': url,
                'domain': extract_domain(url),
                'title': url.split('/')[-1] or 'Non-HTML Content',
                'description': f"Non-HTML content: {content_type}",
                'date': None,
                'content_type': content_type,
            }
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        return {
            'url': url,
            'domain': extract_domain(url),
            'title': extract_title(soup),
            'description': clean_text(extract_meta_description(soup), max_length=300),
            'date': extract_date(soup),
            'content_type': content_type,
        }
    
    def fetch_multiple(self, urls: List[str]) -> List[Dict]:
        """
        Fetch metadata from multiple URLs.
        
        Args:
            urls: List of URLs to fetch
            
        Returns:
            List of metadata dictionaries
        """
        results = []
        for url in urls:
            metadata = self.fetch_page_metadata(url)
            if metadata:
                results.append(metadata)
        return results


def enrich_search_results(results: List[Dict], user_agent: str = "") -> List[Dict]:
    """
    Enrich search results with page metadata.
    
    Takes search results that may have basic info and fetches
    additional metadata from each URL.
    
    Args:
        results: List of search result dictionaries
        user_agent: Custom user agent string
        
    Returns:
        Enriched list of results
    """
    fetcher = SiteFetcher(user_agent=user_agent)
    enriched = []
    
    for result in results:
        url = result.get('url', '')
        if not url:
            continue
        
        # Don't re-fetch if we already have good metadata
        if result.get('title') and result.get('description'):
            if len(result.get('description', '')) > 50:
                enriched.append(result)
                continue
        
        metadata = fetcher.fetch_page_metadata(url)
        
        if metadata:
            # Merge metadata with existing result
            enriched_result = {**result, **metadata}
            enriched.append(enriched_result)
        else:
            # Keep original result if fetch failed
            enriched.append(result)
    
    return enriched