"""
DuckDuckGo HTML search scraper for finding research sources.
"""

import re
import urllib.parse
from typing import Dict, Optional, List
from bs4 import BeautifulSoup
import requests

from trr_source_scraper.utils import (
    RateLimiter,
    clean_text,
    create_session,
    is_valid_url,
)


class DuckDuckGoScraper:
    """
    Scrapes DuckDuckGo HTML search results.
    
    Uses the html.duckduckgo.com interface which doesn't require
    JavaScript and is more scraper-friendly.
    """
    
    SEARCH_URL = "https://html.duckduckgo.com/html/"
    
    def __init__(self, rate_limiter: Optional[RateLimiter] = None, user_agent: str = ""):
        self.rate_limiter = rate_limiter or RateLimiter(delay=2.0)
        self.session = create_session(user_agent or "TRR-Source-Scraper/1.0")
    
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Perform a search and return results.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries with 'title', 'url', 'description' keys
        """
        self.rate_limiter.wait()
        
        params = {
            'q': query,
            'kl': 'wt-wt',  # No region bias
        }
        
        try:
            response = self.session.get(
                self.SEARCH_URL,
                params=params,
                timeout=15
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error performing search: {e}")
            return []
        
        results = self._parse_results(response.text, max_results)
        return results
    
    def _parse_results(self, html: str, max_results: int) -> List[Dict]:
        """Parse HTML search results."""
        soup = BeautifulSoup(html, 'lxml')
        results = []
        
        # Find all result containers
        for result_div in soup.find_all('div', class_='result'):
            if len(results) >= max_results:
                break
            
            result = self._parse_single_result(result_div)
            if result and is_valid_url(result['url']):
                results.append(result)
        
        return results
    
    def _parse_single_result(self, result_div) -> Optional[Dict]:
        """Parse a single search result div."""
        try:
            # Find the main link
            link = result_div.find('a', class_='result__a')
            if not link:
                return None
            
            title = clean_text(link.get_text())
            
            # Extract URL (DuckDuckGo uses redirect URLs)
            raw_url = link.get('href', '')
            url = self._extract_real_url(raw_url)
            
            if not url:
                return None
            
            # Extract description
            snippet = result_div.find('a', class_='result__snippet')
            if snippet:
                description = clean_text(snippet.get_text())
            else:
                # Try to find description in other elements
                desc_elem = result_div.find('td', class_='result__snippet')
                if desc_elem:
                    description = clean_text(desc_elem.get_text())
                else:
                    description = ""
            
            # Extract display URL
            display_url_elem = result_div.find('span', class_='result__url')
            display_url = clean_text(display_url_elem.get_text()) if display_url_elem else ""
            
            return {
                'title': title,
                'url': url,
                'description': description,
                'display_url': display_url,
            }
            
        except Exception as e:
            return None
    
    def _extract_real_url(self, duckduckgo_url: str) -> Optional[str]:
        """
        Extract the real URL from a DuckDuckGo redirect URL.
        
        DuckDuckGo URLs look like:
        //duckduckgo.com/l/?uddg=<encoded_url>&rut=...
        """
        if not duckduckgo_url:
            return None
        
        # If it's already a direct URL
        if duckduckgo_url.startswith('http'):
            return duckduckgo_url
        
        # Parse redirect URL
        if 'uddg=' in duckduckgo_url:
            try:
                # Extract the uddg parameter
                parsed = urllib.parse.urlparse(duckduckgo_url, scheme='https')
                query_params = urllib.parse.parse_qs(parsed.query)
                
                if 'uddg' in query_params:
                    real_url = query_params['uddg'][0]
                    # URL decode
                    real_url = urllib.parse.unquote(real_url)
                    return real_url
            except:
                pass
        
        # Try to extract from the URL directly
        match = re.search(r'uddg=([^&]+)', duckduckgo_url)
        if match:
            encoded_url = match.group(1)
            try:
                return urllib.parse.unquote(encoded_url)
            except:
                pass
        
        return None
    
    def search_with_site_filter(self, query: str, sites: List[str], max_results: int = 10) -> List[Dict]:
        """
        Search with a site: filter for specific domains.
        
        Args:
            query: Base search query
            sites: List of domains to search (e.g., ['specterops.io', 'redcanary.com'])
            max_results: Maximum results per site query
            
        Returns:
            Combined list of results
        """
        all_results = []
        seen_urls = set()
        
        if sites:
            # Build site filter
            site_filter = ' OR '.join(f'site:{site}' for site in sites[:5])  # Limit to 5 sites
            full_query = f"{query} ({site_filter})"
        else:
            full_query = query
        
        results = self.search(full_query, max_results)
        
        for result in results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                all_results.append(result)
        
        return all_results


def search_technique_sources(
    technique_id: str,
    technique_name: str,
    categories: Dict,
    max_per_category: int = 10,
    user_agent: str = ""
) -> Dict[str, List[Dict]]:
    """
    Search for sources across multiple categories.
    
    Args:
        technique_id: MITRE ATT&CK technique ID
        technique_name: Human-readable technique name
        categories: Dictionary of category configs from sources.json
        max_per_category: Maximum results per category
        user_agent: Custom user agent string
        
    Returns:
        Dictionary mapping category names to lists of results
    """
    scraper = DuckDuckGoScraper(user_agent=user_agent)
    results = {}
    
    # Build search queries
    base_queries = [
        f"{technique_id} {technique_name}",
        f"{technique_id} attack technique",
        f"{technique_name} detection",
    ]
    
    for category_name, category_config in categories.items():
        category_results = []
        domains = category_config.get('domains', [])
        search_suffix = category_config.get('search_suffix', '')
        
        for base_query in base_queries[:1]:  # Use just the primary query per category
            full_query = f"{base_query} {search_suffix}".strip()
            
            # Search with site filter
            search_results = scraper.search_with_site_filter(
                full_query,
                domains,
                max_per_category
            )
            
            category_results.extend(search_results)
        
        # Deduplicate and limit
        seen = set()
        unique_results = []
        for r in category_results:
            if r['url'] not in seen:
                seen.add(r['url'])
                unique_results.append(r)
        
        results[category_name] = unique_results[:max_per_category]
    
    return results