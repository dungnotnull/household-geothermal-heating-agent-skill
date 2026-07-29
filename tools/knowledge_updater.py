"""
knowledge_updater.py — Skill 248: household-geothermal-heating
Production-grade crawl pipeline for geothermal heat pump knowledge base.

Fetches latest papers + news → scores → appends to SECOND-KNOWLEDGE-BRAIN.md.

Features:
- Robust error handling with exponential backoff
- Rate limiting and respectful crawling
- Comprehensive logging
- Configurable knowledge sources
- SHA256 deduplication
- Composite scoring (recency + relevance + citations)
- Dry-run mode for testing

Dependencies:
    pip install requests feedparser python-dateutil tenacity

Usage:
    python tools/knowledge_updater.py [--dry-run] [--news-only] [--keywords ...]
    python tools/knowledge_updater.py --test-connection

Author: household-geothermal-heating v1.0
License: MIT
"""

import argparse
import hashlib
import json
import logging
import math
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Optional dependencies with graceful fallback
try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    requests = None

try:
    import feedparser
except ImportError:
    feedparser = None

try:
    from dateutil import parser as date_parser
except ImportError:
    date_parser = None

try:
    from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
    TENACITY_AVAILABLE = True
except ImportError:
    TENACITY_AVAILABLE = False
    # Fallback decorators
    def retry(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    def stop_after_attempt(*args, **kwargs):
        return None
    def wait_exponential(*args, **kwargs):
        return None
    def before_sleep_log(*args, **kwargs):
        return None


# =============================================================================
# Configuration
# =============================================================================

KNOWLEDGE_CONFIG = {
    "domain": "Small-Scale Geothermal Heat Pump Engineering",
    "keywords": [
        "ground source heat pump",
        "geothermal heat pump",
        "GSHP design",
        "borehole thermal resistance",
        "ground loop design",
        "geothermal heating load",
        "heat pump COP",
        "thermal conductivity grout",
        "horizontal ground loop",
        "vertical borehole",
        "geothermal maintenance"
    ],
    "arxiv_categories": [
        "physics.flu-dyn",
        "cond-mat",
        "cs.CE"
    ],
    "arxiv_base": "https://export.arxiv.org/api/query",
    "semantic_scholar_base": "https://api.semanticscholar.org/graph/v1/paper/search",
    "rss_feeds": [
        "https://www.igshpa.okstate.edu/rss/news",
        "https://www.ashrae.org/rss/news",
        "https://www.renewableenergyworld.com/rss/"
    ],
    "authoritative_docs": [
        "Geothermics — Elsevier",
        "Energy and Buildings — Elsevier",
        "Applied Thermal Engineering — Elsevier",
        "Renewable Energy — Elsevier",
        "Building and Environment — Elsevier",
        "ASHRAE Handbook",
        "IGSHPA Standards"
    ],
    "scoring_weights": {
        "recency": 0.4,
        "keyword_relevance": 0.4,
        "citation_count": 0.2
    },
    "max_results_per_source": 10,
    "max_new_entries_per_run": 20,
    "min_relevance_score": 5.0,
    "request_timeout": 30,
    "max_retries": 3,
    "retry_delay": 2.0,
    "rate_limit_delay": 1.0
}


# =============================================================================
# Logging Setup
# =============================================================================

def setup_logging(log_dir: Optional[Path] = None, verbose: bool = False) -> logging.Logger:
    """Configure logging with file and console handlers."""
    logger = logging.getLogger("knowledge_updater")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler (optional)
    if log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"knowledge_update_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(f"Logging to file: {log_file}")

    return logger


# Global logger instance
logger = logging.getLogger("knowledge_updater")


# =============================================================================
# Path Configuration
# =============================================================================

def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).resolve().parent.parent


def get_brain_path() -> Path:
    """Get path to SECOND-KNOWLEDGE-BRAIN.md."""
    root = get_project_root()
    return root / "SECOND-KNOWLEDGE-BRAIN.md"


def get_log_dir() -> Path:
    """Get log directory path."""
    root = get_project_root()
    log_dir = root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


# =============================================================================
# HTTP Client with Retry Logic
# =============================================================================

def create_session() -> Optional['requests.Session']:
    """Create a requests session with retry logic."""
    if requests is None:
        return None

    session = requests.Session()

    retry_strategy = Retry(
        total=KNOWLEDGE_CONFIG["max_retries"],
        backoff_factor=KNOWLEDGE_CONFIG["retry_delay"],
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def fetch_with_retry(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    session: Optional['requests.Session'] = None,
    max_retries: int = 3,
    timeout: int = 30
) -> Optional['requests.Response']:
    """Fetch URL with retry logic and exponential backoff."""
    if requests is None:
        logger.error("requests library not available")
        return None

    if session is None:
        session = create_session()
        if session is None:
            return None

    last_error = None
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                wait_time = KNOWLEDGE_CONFIG["retry_delay"] * (2 ** attempt)
                logger.debug(f"Retry attempt {attempt + 1}/{max_retries} after {wait_time:.1f}s wait")
                time.sleep(wait_time)

            response = session.get(
                url,
                params=params or {},
                timeout=timeout,
                headers={'User-Agent': 'household-geothermal-heating/1.0'}
            )

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited. Waiting {retry_after}s before retry.")
                time.sleep(retry_after)
                continue

            # Handle server errors
            if response.status_code >= 500:
                logger.warning(f"Server error {response.status_code} on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    continue

            response.raise_for_status()
            return response

        except requests.exceptions.Timeout:
            last_error = "Timeout"
            logger.warning(f"Request timeout on attempt {attempt + 1}/{max_retries}")
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            logger.warning(f"Request failed on attempt {attempt + 1}/{max_retries}: {e}")
        except Exception as e:
            last_error = str(e)
            logger.error(f"Unexpected error on attempt {attempt + 1}/{max_retries}: {e}")

    logger.error(f"All {max_retries} attempts failed. Last error: {last_error}")
    return None


# =============================================================================
# Hash and Deduplication
# =============================================================================

def compute_hash(identifier: str) -> str:
    """Compute SHA256 hash of identifier (case-insensitive, trimmed)."""
    normalized = identifier.strip().lower()
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def load_existing_hashes() -> Set[str]:
    """Load existing hashes from SECOND-KNOWLEDGE-BRAIN.md."""
    brain_path = get_brain_path()
    if not brain_path.exists():
        logger.warning(f"Knowledge base not found: {brain_path}")
        return set()

    hashes = set()
    try:
        content = brain_path.read_text(encoding='utf-8')
        # Find all DOI/URL entries
        pattern = r"\*\*DOI/URL:\*\*\s*(\S+)"
        for match in re.finditer(pattern, content):
            identifier = match.group(1)
            hashes.add(compute_hash(identifier))
        logger.debug(f"Loaded {len(hashes)} existing hashes")
    except Exception as e:
        logger.error(f"Error loading existing hashes: {e}")

    return hashes


# =============================================================================
# Scoring Algorithm
# =============================================================================

def score_entry(
    entry: Dict[str, Any],
    keywords: List[str],
    now: datetime
) -> float:
    """
    Calculate relevance score for an entry.

    Score = (recency_weight × recency_score) +
            (relevance_weight × keyword_score) +
            (citation_weight × citation_score)

    Returns: float between 0 and 10
    """
    weights = KNOWLEDGE_CONFIG["scoring_weights"]

    # 1. Recency score (0-1)
    recency_score = 0.0
    pub_date = entry.get("published_date")
    if pub_date and isinstance(pub_date, datetime):
        try:
            days_old = (now - pub_date).days
            recency_score = max(0.0, 1.0 - (days_old / 730.0))  # 2-year decay
        except Exception as e:
            logger.debug(f"Error calculating recency: {e}")

    # 2. Keyword relevance score (0-1)
    keyword_score = 0.0
    text = " ".join([
        entry.get("title", ""),
        entry.get("abstract", ""),
        entry.get("venue", "")
    ]).lower()

    matching_keywords = sum(1 for kw in keywords if kw.lower() in text)
    keyword_score = min(matching_keywords / max(len(keywords), 1), 1.0)

    # 3. Citation score (0-1, log-scaled)
    citation_score = 0.0
    citation_count = entry.get("citation_count", 0) or 0
    if citation_count > 0:
        citation_score = min(math.log1p(citation_count) / math.log1p(1000), 1.0)

    # Combine with weights
    total = (
        recency_score * weights["recency"] +
        keyword_score * weights["keyword_relevance"] +
        citation_score * weights["citation_count"]
    )

    # Scale to 0-10
    return round(total * 10.0, 2)


# =============================================================================
# ArXiv Fetcher
# =============================================================================

def fetch_arxiv(
    keywords: List[str],
    session: Optional['requests.Session'] = None
) -> List[Dict[str, Any]]:
    """Fetch papers from ArXiv based on keywords."""
    if requests is None or not KNOWLEDGE_CONFIG["arxiv_categories"]:
        logger.info("ArXiv fetcher disabled (no requests or no categories)")
        return []

    cats = KNOWLEDGE_CONFIG["arxiv_categories"]
    max_results = KNOWLEDGE_CONFIG["max_results_per_source"]

    # Build query: (cat:...) AND (keyword1 OR keyword2 ...)
    cat_query = " OR ".join(f"cat:{c}" for c in cats)
    kw_query = " OR ".join(f'"{kw}"' for kw in keywords[:5])
    query = f"({cat_query}) AND ({kw_query})"

    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results
    }

    logger.info(f"Fetching ArXiv with query: {query[:100]}...")
    response = fetch_with_retry(
        KNOWLEDGE_CONFIG["arxiv_base"],
        params=params,
        session=session,
        timeout=60
    )

    if response is None:
        return []

    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
    except Exception as e:
        logger.error(f"Error parsing ArXiv XML: {e}")
        return []

    entries = []
    for entry in root.findall("atom:entry", ns):
        try:
            title_elem = entry.find("atom:title", ns)
            summary_elem = entry.find("atom:summary", ns)
            id_elem = entry.find("atom:id", ns)
            published_elem = entry.find("atom:published", ns)

            title = (title_elem.text or "").strip().replace("\n", " ") if title_elem is not None else ""
            url = (id_elem.text or "").strip() if id_elem is not None else ""

            if not title or not url:
                continue

            # Parse date
            pub_date = None
            if published_elem is not None and date_parser:
                try:
                    pub_date = date_parser.parse(published_elem.text).replace(tzinfo=None)
                except Exception:
                    pass

            # Extract authors (first 3)
            authors = []
            for author in entry.findall("atom:author", ns)[:3]:
                name_elem = author.find("atom:name", ns)
                if name_elem is not None:
                    authors.append(name_elem.text)

            entries.append({
                "title": title,
                "authors": authors,
                "year": pub_date.year if pub_date else datetime.now().year,
                "venue": "ArXiv",
                "doi_or_url": url,
                "abstract": (summary_elem.text or "")[:300] if summary_elem is not None else "",
                "published_date": pub_date,
                "citation_count": 0,
                "source": "arxiv"
            })
        except Exception as e:
            logger.warning(f"Error parsing ArXiv entry: {e}")

    logger.info(f"ArXiv: Retrieved {len(entries)} entries")
    return entries


# =============================================================================
# Semantic Scholar Fetcher
# =============================================================================

def fetch_semantic_scholar(
    keywords: List[str],
    session: Optional['requests.Session'] = None
) -> List[Dict[str, Any]]:
    """Fetch papers from Semantic Scholar API."""
    if requests is None:
        logger.info("Semantic Scholar fetcher disabled (no requests)")
        return []

    params = {
        "query": " ".join(keywords[:4]),
        "fields": "title,authors,year,venue,externalIds,abstract,citationCount",
        "limit": KNOWLEDGE_CONFIG["max_results_per_source"]
    }

    logger.info("Fetching Semantic Scholar...")
    response = fetch_with_retry(
        KNOWLEDGE_CONFIG["semantic_scholar_base"],
        params=params,
        session=session,
        timeout=30
    )

    if response is None:
        return []

    try:
        data = response.json()
    except Exception as e:
        logger.error(f"Error parsing Semantic Scholar JSON: {e}")
        return []

    entries = []
    for paper in data.get("data", []):
        try:
            title = paper.get("title", "")
            if not title:
                continue

            year = paper.get("year") or datetime.now().year

            # Get DOI or construct URL
            external_ids = paper.get("externalIds", {})
            doi = external_ids.get("DOI", "")

            if not doi:
                arxiv_id = external_ids.get("ArXiv")
                if arxiv_id:
                    doi = f"https://arxiv.org/abs/{arxiv_id}"
                else:
                    paper_id = paper.get("paperId", "")
                    doi = f"https://www.semanticscholar.org/paper/{paper_id}"

            # Extract authors
            authors = [a.get("name", "") for a in paper.get("authors", [])[:3]]

            entries.append({
                "title": title,
                "authors": authors,
                "year": year,
                "venue": paper.get("venue") or "Unknown",
                "doi_or_url": doi,
                "abstract": (paper.get("abstract") or "")[:300],
                "published_date": datetime(year, 1, 1),
                "citation_count": paper.get("citationCount", 0) or 0,
                "source": "semantic_scholar"
            })
        except Exception as e:
            logger.warning(f"Error parsing Semantic Scholar entry: {e}")

    logger.info(f"Semantic Scholar: Retrieved {len(entries)} entries")
    return entries


# =============================================================================
# RSS Feed Fetcher
# =============================================================================

def fetch_rss(
    session: Optional['requests.Session'] = None
) -> List[Dict[str, Any]]:
    """Fetch news from RSS feeds."""
    if feedparser is None or not KNOWLEDGE_CONFIG["rss_feeds"]:
        logger.info("RSS fetcher disabled (no feedparser or no feeds)")
        return []

    entries = []
    feeds = KNOWLEDGE_CONFIG["rss_feeds"]

    for feed_url in feeds:
        logger.info(f"Fetching RSS feed: {feed_url[:50]}...")
        try:
            feed = feedparser.parse(feed_url)

            if feed.get('bozo'):
                logger.warning(f"Feed parsing warning for {feed_url}: {feed['bozo']}")

            for item in feed.entries[:10]:
                try:
                    title = item.get("title", "")
                    link = item.get("link", "")

                    if not title or not link:
                        continue

                    # Parse publication date
                    pub_date = None
                    if item.get("published_parsed"):
                        try:
                            pub_date = datetime(*item["published_parsed"][:6])
                        except Exception:
                            pass

                    if pub_date is None:
                        pub_date = datetime.now()

                    entries.append({
                        "title": title,
                        "authors": ["Editorial"],
                        "year": pub_date.year,
                        "venue": f"RSS ({feed.get('feed', {}).get('title', 'News')})",
                        "doi_or_url": link,
                        "abstract": (item.get("summary", "") or "")[:200],
                        "published_date": pub_date,
                        "citation_count": 0,
                        "source": "rss"
                    })
                except Exception as e:
                    logger.warning(f"Error parsing RSS item: {e}")

        except Exception as e:
            logger.error(f"Error fetching RSS feed {feed_url}: {e}")

    logger.info(f"RSS: Retrieved {len(entries)} total entries")
    return entries


# =============================================================================
# Entry Formatting
# =============================================================================

def format_entry(entry: Dict[str, Any], score: float, tier: int = 4) -> str:
    """Format an entry for appending to SECOND-KNOWLEDGE-BRAIN.md."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    authors = ", ".join(entry.get("authors", [])) or "Unknown"

    return (
        f"\n### {date_str} — {entry.get('title', 'Untitled')}\n"
        f"- **Authors:** {authors}\n"
        f"- **Year:** {entry.get('year', '')}\n"
        f"- **Venue:** {entry.get('venue', 'Unknown')}\n"
        f"- **DOI/URL:** {entry.get('doi_or_url', '')}\n"
        f"- **Relevance Score:** {score:.1f}/10\n"
        f"- **Tier:** {tier}\n"
        f"- **Key Finding:** {entry.get('abstract', 'No abstract available.')}\n"
    )


def determine_tier(entry: Dict[str, Any]) -> int:
    """Determine evidence tier based on entry source and venue."""
    source = entry.get("source", "")
    venue = entry.get("venue", "").lower()

    # Tier 1: Standards and guidelines
    if any(org in venue for org in ["ashrae", "iso", "igshpa", "standard", "guideline"]):
        return 1

    # Tier 2: Peer-reviewed academic
    if source in ["arxiv", "semantic_scholar"]:
        if any(journal in venue for journal in ["geothermics", "energy and buildings",
            "applied thermal", "renewable energy"]):
            return 2
        return 3  # General academic but not top-tier journal

    # Tier 3: Industry reports
    if source == "rss" and any(term in venue for term in ["news", "editorial"]):
        return 3

    # Default Tier 4
    return 4


# =============================================================================
# Append to Knowledge Base
# =============================================================================

def append_to_brain(
    entries: List[Dict[str, Any]],
    dry_run: bool = False
) -> int:
    """Append new entries to SECOND-KNOWLEDGE-BRAIN.md."""
    brain_path = get_brain_path()

    if not brain_path.exists():
        logger.error(f"Knowledge base not found: {brain_path}")
        return 0

    # Load existing hashes
    existing_hashes = load_existing_hashes()
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Filter out duplicates
    new_entries = []
    for entry in entries:
        doi_or_url = entry.get("doi_or_url", "")
        if not doi_or_url:
            continue

        h = compute_hash(doi_or_url)
        if h in existing_hashes:
            logger.debug(f"Duplicate entry skipped: {entry.get('title', '')[:50]}...")
            continue

        existing_hashes.add(h)
        new_entries.append(entry)

    if not new_entries:
        logger.info("No new entries to append (all duplicates)")
        return 0

    # Score all entries
    for entry in new_entries:
        entry["_score"] = score_entry(entry, KNOWLEDGE_CONFIG["keywords"], now)
        entry["_tier"] = determine_tier(entry)

    # Filter by minimum relevance
    min_score = KNOWLEDGE_CONFIG["min_relevance_score"]
    new_entries = [e for e in new_entries if e["_score"] >= min_score]
    logger.info(f"After scoring and filtering (score >= {min_score}): {len(new_entries)} entries")

    # Sort by score and limit
    new_entries.sort(key=lambda x: x["_score"], reverse=True)
    max_entries = KNOWLEDGE_CONFIG["max_new_entries_per_run"]
    new_entries = new_entries[:max_entries]

    # Format entries
    formatted_text = "".join(
        format_entry(e, e["_score"], e["_tier"])
        for e in new_entries
    )

    if dry_run:
        logger.info(f"[DRY RUN] Would append {len(new_entries)} entries:")
        for e in new_entries:
            logger.info(f"  - [{e['_score']:.1f}/10] {e['title'][:60]}...")
        return len(new_entries)

    # Append to file
    try:
        content = brain_path.read_text(encoding='utf-8')

        if "## 7. Knowledge Update Log" in content:
            # Append to existing section
            content += formatted_text
        else:
            # Create new section
            content += "\n## 7. Knowledge Update Log\n" + formatted_text

        brain_path.write_text(content, encoding='utf-8')
        logger.info(f"Successfully appended {len(new_entries)} entries to knowledge base")

        # Log summary
        for e in new_entries:
            logger.info(f"  + [{e['_score']:.1f}/10 T{e['_tier']}] {e['title'][:60]}...")

        return len(new_entries)

    except Exception as e:
        logger.error(f"Error writing to knowledge base: {e}")
        return 0


# =============================================================================
# Connection Testing
# =============================================================================

def test_connection() -> bool:
    """Test connection to all configured sources."""
    logger.info("Testing connections to knowledge sources...")

    all_ok = True
    session = create_session()

    # Test ArXiv
    if KNOWLEDGE_CONFIG["arxiv_categories"]:
        logger.info("Testing ArXiv connection...")
        resp = fetch_with_retry(
            KNOWLEDGE_CONFIG["arxiv_base"],
            params={"search_query": "cat:physics.flu-dyn", "max_results": 1},
            session=session,
            timeout=10
        )
        if resp:
            logger.info("✓ ArXiv connection successful")
        else:
            logger.error("✗ ArXiv connection failed")
            all_ok = False
    else:
        logger.info("⊘ ArXiv not configured")

    # Test Semantic Scholar
    logger.info("Testing Semantic Scholar connection...")
    resp = fetch_with_retry(
        KNOWLEDGE_CONFIG["semantic_scholar_base"],
        params={"query": "heat pump", "limit": 1},
        session=session,
        timeout=10
    )
    if resp:
        logger.info("✓ Semantic Scholar connection successful")
    else:
        logger.error("✗ Semantic Scholar connection failed")
        all_ok = False

    # Test RSS
    if KNOWLEDGE_CONFIG["rss_feeds"] and feedparser:
        logger.info("Testing RSS feeds...")
        for feed_url in KNOWLEDGE_CONFIG["rss_feeds"][:1]:  # Test first feed only
            try:
                feed = feedparser.parse(feed_url)
                logger.info(f"✓ RSS feed parseable: {feed_url[:50]}...")
            except Exception as e:
                logger.error(f"✗ RSS feed failed: {e}")
                all_ok = False
    else:
        logger.info("⊘ RSS not configured or feedparser not available")

    return all_ok


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    """Main entry point for knowledge updater."""
    parser = argparse.ArgumentParser(
        description="Update SECOND-KNOWLEDGE-BRAIN.md with latest research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/knowledge_updater.py                    # Full update
  python tools/knowledge_updater.py --dry-run          # Test without writing
  python tools/knowledge_updater.py --news-only        # News sources only
  python tools/knowledge_updater.py --test-connection # Test connectivity
  python tools/knowledge_updater.py --verbose          # Detailed logging
        """
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without writing to knowledge base"
    )
    parser.add_argument(
        "--news-only",
        action="store_true",
        help="Only fetch news from RSS feeds"
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=KNOWLEDGE_CONFIG["keywords"],
        help="Keywords to search for (default: use config)"
    )
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test connectivity to all sources"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(log_dir=get_log_dir(), verbose=args.verbose)

    logger.info("=" * 60)
    logger.info("Knowledge Updater Started")
    logger.info(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    logger.info(f"News only: {args.news_only}")
    logger.info(f"Keywords: {', '.join(args.keywords[:5])}")
    logger.info("=" * 60)

    # Test connection if requested
    if args.test_connection:
        success = test_connection()
        sys.exit(0 if success else 1)

    # Check dependencies
    if requests is None:
        logger.error("requests library not available. Install with: pip install requests")
        sys.exit(1)

    start_time = time.time()
    all_entries = []
    session = create_session()

    try:
        # Fetch academic sources
        if not args.news_only:
            logger.info("Fetching academic sources...")

            if KNOWLEDGE_CONFIG["arxiv_categories"]:
                arxiv_entries = fetch_arxiv(args.keywords, session)
                all_entries.extend(arxiv_entries)
                time.sleep(KNOWLEDGE_CONFIG["rate_limit_delay"])

            semantic_entries = fetch_semantic_scholar(args.keywords, session)
            all_entries.extend(semantic_entries)
            time.sleep(KNOWLEDGE_CONFIG["rate_limit_delay"])

        # Fetch news
        rss_entries = fetch_rss(session)
        all_entries.extend(rss_entries)

        logger.info(f"Total candidates retrieved: {len(all_entries)}")

        # Append to knowledge base
        appended = append_to_brain(all_entries, dry_run=args.dry_run)

        elapsed = time.time() - start_time
        logger.info("=" * 60)
        logger.info(f"Update completed in {elapsed:.1f}s")
        logger.info(f"Entries appended: {appended}")
        logger.info("=" * 60)

        sys.exit(0)

    except KeyboardInterrupt:
        logger.warning("Update cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error during update: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
