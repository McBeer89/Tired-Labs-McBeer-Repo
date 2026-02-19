"""
Atomic Red Team emulation test fetcher.

Queries the redcanaryco/atomic-red-team GitHub repository for emulation
tests that match a given MITRE ATT&CK technique ID.
"""

from typing import Dict, List, Optional
import requests

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from utils import RateLimiter, create_session

ART_BASE_URL = "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics"
ART_GITHUB_URL = "https://github.com/redcanaryco/atomic-red-team/blob/master/atomics"


def fetch_atomic_tests(technique_id: str, user_agent: str = "") -> List[Dict]:
    """
    Fetch Atomic Red Team emulation tests for a given technique.

    Directly retrieves the YAML file for the technique from the
    redcanaryco/atomic-red-team repository. Returns an empty list
    if no tests exist for this technique.

    Args:
        technique_id: MITRE ATT&CK technique ID (e.g., T1003.006)
        user_agent: Custom user agent string

    Returns:
        List of test dictionaries, each with keys:
        - name: test name
        - description: what the test does
        - platforms: list of supported OS platforms
        - executor: execution method (command_prompt, powershell, bash, etc.)
        - github_url: direct link to the test file on GitHub
        - auto_generated_guid: unique test identifier
    """
    if not YAML_AVAILABLE:
        print("Warning: pyyaml not installed. Run: pip install pyyaml")
        print("         Atomic Red Team tests will not be fetched.")
        return []

    tid = technique_id.upper().strip()
    rate_limiter = RateLimiter(delay=1.0)
    session = create_session(user_agent or "TRR-Source-Scraper/1.0")

    yaml_url = f"{ART_BASE_URL}/{tid}/{tid}.yaml"
    github_url = f"{ART_GITHUB_URL}/{tid}/{tid}.yaml"

    rate_limiter.wait()
    try:
        response = session.get(yaml_url, timeout=15)
        if response.status_code == 404:
            return []
        response.raise_for_status()
    except requests.RequestException:
        return []

    try:
        data = yaml.safe_load(response.text)
    except yaml.YAMLError:
        return []

    if not data or 'atomic_tests' not in data:
        return []

    results = []
    for test in data.get('atomic_tests', []):
        platforms = test.get('supported_platforms', [])
        executor = test.get('executor', {})
        executor_name = executor.get('name', 'unknown') if isinstance(executor, dict) else str(executor)

        results.append({
            'name': test.get('name', 'Unnamed Test'),
            'description': test.get('description', '').strip(),
            'platforms': platforms,
            'executor': executor_name,
            'auto_generated_guid': test.get('auto_generated_guid', ''),
            'github_url': github_url,
        })

    return results
