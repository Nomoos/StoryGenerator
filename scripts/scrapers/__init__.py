"""
Alternative Content Source Scrapers Package

This package contains scrapers for alternative content sources:
- Quora: Questions and answers
- Twitter/X: Story threads

Usage:
    from scrapers.quora_scraper import QuoraScraper
    from scrapers.twitter_scraper import TwitterScraper

    scraper = QuoraScraper()
    content = scraper.scrape_content("topic", "women", "18-23", limit=50)
"""

from .base_scraper import BaseScraper
from .quora_scraper import QuoraScraper
from .twitter_scraper import TwitterScraper

__all__ = [
    "BaseScraper",
    "QuoraScraper",
    "TwitterScraper",
]
