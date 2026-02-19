# TRR Source Scraper

A Python tool for scraping the web to find potential research sources for MITRE ATT&CK techniques when creating Technique Research Reports (TRRs).

## Purpose

When creating a Technique Research Report, researchers need to gather information from multiple sources to understand an attack technique thoroughly. This tool automates the discovery of relevant sources, including:

- **MITRE ATT&CK** - Official technique documentation
- **Security Research Blogs** - SpecterOps, Red Canary, CrowdStrike, Elastic, etc.
- **Microsoft Documentation** - Official Windows/Azure docs
- **Conference Presentations** - Black Hat, DEF CON, BSides
- **GitHub Resources** - POC code, detection rules, Atomic tests
- **Academic Papers** - Research publications

## Installation

```bash
# Navigate to the tool directory
cd tools/trr-source-scraper

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Search for sources on a technique
python trr_scraper.py T1003.006

# With technique name for better search results
python trr_scraper.py T1003.006 --name "DCSync"
```

### Advanced Options

```bash
# Specify output directory
python trr_scraper.py T1003.006 --output ./my-research/

# Limit results per category
python trr_scraper.py T1003.006 --max-per-category 5

# Skip metadata enrichment (faster but less detail)
python trr_scraper.py T1003.006 --no-enrich

# Verbose mode for debugging
python trr_scraper.py T1003.006 --verbose
```

### Command-Line Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `technique_id` | - | MITRE ATT&CK technique ID (required) |
| `--name` | `-n` | Technique name for better search results |
| `--output` | `-o` | Output directory for the markdown report |
| `--max-per-category` | `-m` | Maximum number of results per category |
| `--no-enrich` | - | Skip fetching page metadata |
| `--verbose` | `-v` | Print detailed progress information |

## Output

The tool generates a markdown report containing:

1. **MITRE ATT&CK Reference** - Technique summary, tactics, platforms, data sources
2. **Existing TRRs** - Any existing reports in the repository that match the technique
3. **Existing DDMs** - Detection Data Models related to the technique
4. **Categorized Sources** - Research sources organized by type:
   - Security Research Blogs (High Priority)
   - Microsoft Documentation (High Priority)
   - Conference Presentations (Medium Priority)
   - GitHub Resources (Medium Priority)
   - Academic Papers (Low Priority)
5. **Search Queries** - Suggested queries for manual additional research

### Example Output

```markdown
# Research Sources for T1003.006 - DCSync

**Generated:** 2026-02-18 14:30:00
**Technique:** T1003.006
**Tactics:** Credential Access
**Platforms:** Windows, SaaS

---

## MITRE ATT&CK Reference

### [T1003.006 - OS Credential Dumping: DCSync](https://attack.mitre.org/techniques/T1003/006/)

> **Summary:** Adversaries may attempt to access credentials and other sensitive material...

**Data Sources:** Active Directory, Windows Event Log

---

## Security Research Blogs (High Priority)

### 1. [DCSync: What It Is and How to Detect It](https://specterops.io/...)

> **Source:** specterops.io
> **Published:** 2023-05-15

**Excerpt:** DCSync is a technique that simulates the behavior of a Domain Controller...

**Relevance:** High

---

...
```

## Configuration

The tool's behavior can be customized via `config/sources.json`:

### Source Categories

Add or modify trusted sources in the `trusted_sources` section:

```json
{
  "trusted_sources": {
    "security_research": {
      "priority": "high",
      "domains": ["specterops.io", "redcanary.com", ...],
      "search_suffix": "security research analysis detection"
    }
  }
}
```

### Search Settings

```json
{
  "search_settings": {
    "max_results_per_category": 10,
    "delay_between_requests": 2,
    "timeout": 15,
    "max_retries": 3,
    "user_agent": "TRR-Source-Scraper/1.0 (Educational Research Tool)"
  }
}
```

### Output Settings

```json
{
  "output_settings": {
    "default_output_dir": "output",
    "include_excerpts": true,
    "excerpt_length": 200,
    "include_dates": true
  }
}
```

## Project Structure

```
trr-source-scraper/
├── trr_scraper.py           # Main entry point
├── scrapers/
│   ├── __init__.py
│   ├── duckduckgo.py        # DuckDuckGo HTML search scraper
│   ├── mitre_attack.py      # MITRE ATT&CK page scraper
│   ├── existing_trr.py      # Check existing TRRs in repo
│   └── site_fetcher.py      # Individual site metadata fetcher
├── utils/
│   ├── __init__.py
│   └── helpers.py           # Rate limiting, URL validation, etc.
├── config/
│   └── sources.json         # Trusted sources list with categories
├── output/                  # Generated markdown reports
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Ethical Scraping

This tool follows ethical scraping practices:

- **Rate Limiting**: Built-in delays between requests (configurable)
- **User-Agent**: Identifies the scraper in requests
- **Respect for Robots.txt**: Checks when possible
- **Conservative Limits**: Caps results per category to avoid overwhelming sources

## Extending the Tool

### Adding New Source Categories

1. Edit `config/sources.json`
2. Add a new category with domains and search settings:

```json
{
  "my_new_category": {
    "priority": "medium",
    "domains": ["example-security-blog.com"],
    "search_suffix": "analysis"
  }
}
```

### Adding New Scrapers

1. Create a new scraper in `scrapers/`
2. Import and use the `RateLimiter` and helper utilities
3. Register in `scrapers/__init__.py`
4. Call from `trr_scraper.py` main function

## Troubleshooting

### "Could not fetch MITRE ATT&CK page"

- Check your internet connection
- The MITRE ATT&CK site may be temporarily unavailable
- The tool will continue with limited information

### No search results found

- Try adding the `--name` parameter with the technique name
- Some techniques may have limited public research
- Check if DuckDuckGo is accessible from your network

### Slow performance

- Use `--no-enrich` to skip metadata fetching
- Reduce `--max-per-category` to fewer results
- The tool includes rate limiting for ethical scraping

## License

This tool is part of the Tired Labs project. See the main repository for license information.