#!/usr/bin/env python3
"""
Alternative Content Sources Scraper (Enhanced v2.0)

Unified script to scrape content from multiple alternative sources:
- Quora: Questions and answers
- Twitter/X: Story threads
- Instagram: Stories from hashtags and accounts (NEW)
- TikTok: Video descriptions and captions (NEW)

Usage:
    python alt_sources_scraper.py --sources quora,twitter,instagram,tiktok --gender women --age 18-23
    python alt_sources_scraper.py --sources all --all-demographics
    python alt_sources_scraper.py --help
"""

import argparse
import sys
import time
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Add scrapers directory to path
sys.path.insert(0, str(Path(__file__).parent))

from quora_scraper import QuoraScraper
from twitter_scraper import TwitterScraper
from instagram_scraper import InstagramScraper
from tiktok_scraper import TikTokScraper


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Scrape alternative content sources (Quora, Twitter) for story generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape Quora and Twitter for women aged 18-23
  python alt_sources_scraper.py --sources quora,twitter --gender women --age 18-23
  
  # Scrape all sources for all demographics
  python alt_sources_scraper.py --sources all --all-demographics
  
  # Scrape only Instagram and TikTok for men aged 14-17
  python alt_sources_scraper.py --sources instagram,tiktok --gender men --age 14-17
  
  # Scrape with custom topic
  python alt_sources_scraper.py --sources instagram --gender women --age 18-23 --topic "college life"
        """,
    )

    parser.add_argument(
        "--sources",
        type=str,
        default="quora,twitter,instagram,tiktok",
        help="Comma-separated list of sources (quora, twitter, instagram, tiktok, or 'all')",
    )

    parser.add_argument(
        "--gender",
        type=str,
        choices=["men", "women"],
        help="Target gender (required unless --all-demographics)",
    )

    parser.add_argument(
        "--age",
        type=str,
        choices=["10-13", "14-17", "18-23"],
        help="Target age bucket (required unless --all-demographics)",
    )

    parser.add_argument(
        "--all-demographics", action="store_true", help="Scrape all gender/age combinations"
    )

    parser.add_argument(
        "--topic",
        type=str,
        default="life stories",
        help="Topic or keywords to search for (default: 'life stories')",
    )

    parser.add_argument(
        "--limit", type=int, default=50, help="Maximum items to fetch per source (default: 50)"
    )

    parser.add_argument(
        "--delay", type=float, default=2.0, help="Delay in seconds between requests (default: 2.0)"
    )

    return parser.parse_args()


def init_scrapers(source_names: List[str]) -> Dict:
    """Initialize scraper instances.

    Args:
        source_names: List of source names to initialize

    Returns:
        Dictionary mapping source names to scraper instances
    """
    scrapers = {}

    for name in source_names:
        name = name.strip().lower()

        try:
            if name == "quora":
                scrapers["quora"] = QuoraScraper()
                print(f"✅ Initialized Quora scraper")
            elif name == "twitter":
                scrapers["twitter"] = TwitterScraper()
                print(f"✅ Initialized Twitter scraper")
            elif name == "instagram":
                scrapers["instagram"] = InstagramScraper(use_mock=True)
                print(f"✅ Initialized Instagram scraper (mock mode)")
            elif name == "tiktok":
                scrapers["tiktok"] = TikTokScraper(use_mock=True)
                print(f"✅ Initialized TikTok scraper (mock mode)")
            else:
                print(f"⚠️  Unknown source: {name}")
        except Exception as e:
            print(f"❌ Failed to initialize {name}: {e}")

    return scrapers


def run_scraping(
    scrapers: Dict, demographics: List[tuple], topic: str, limit: int, delay: float
) -> List[Dict]:
    """Run scraping for all specified sources and demographics.

    Args:
        scrapers: Dictionary of initialized scrapers
        demographics: List of (gender, age) tuples
        topic: Topic to search for
        limit: Maximum items per source
        delay: Delay between requests

    Returns:
        List of result dictionaries
    """
    results = []
    total = len(scrapers) * len(demographics)
    current = 0

    print(f"\n{'='*60}")
    print(
        f"Starting scraping: {len(scrapers)} sources × {len(demographics)} demographics = {total} tasks"
    )
    print(f"{'='*60}\n")

    for source_name, scraper in scrapers.items():
        for gender, age in demographics:
            current += 1
            print(f"\n[{current}/{total}] {source_name.upper()} - {gender}/{age}")
            print("-" * 60)

            try:
                result = scraper.run(topic, gender, age, limit)
                results.append(result)

                # Rate limiting
                if current < total:
                    time.sleep(delay)

            except Exception as e:
                print(f"❌ Error: {e}")
                results.append(
                    {
                        "source": source_name,
                        "gender": gender,
                        "age_bucket": age,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat(),
                    }
                )

    return results


def print_summary(results: List[Dict]):
    """Print summary of scraping results.

    Args:
        results: List of result dictionaries
    """
    print("\n" + "=" * 60)
    print("SCRAPING SUMMARY")
    print("=" * 60)

    successful = [r for r in results if "error" not in r]
    failed = [r for r in results if "error" in r]

    print(f"\nTotal tasks: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if successful:
        print("\n" + "-" * 60)
        print("Successful scrapes:")
        print("-" * 60)
        for result in successful:
            print(
                f"  {result['source']:8} | {result['gender']:6}/{result['age_bucket']:6} | "
                f"Scraped: {result['scraped']:3} → Filtered: {result['filtered']:3}"
            )
            print(f"           Output: {result['output_file']}")

    if failed:
        print("\n" + "-" * 60)
        print("Failed scrapes:")
        print("-" * 60)
        for result in failed:
            print(f"  {result['source']:8} | {result['gender']:6}/{result['age_bucket']:6}")
            print(f"           Error: {result['error']}")

    print("\n" + "=" * 60)


def main():
    """Main entry point."""
    args = parse_args()

    # Validate arguments
    if not args.all_demographics and (not args.gender or not args.age):
        print("❌ Error: Either --all-demographics or both --gender and --age must be specified")
        sys.exit(1)

    # Parse sources
    source_list = args.sources.lower().split(",")
    if "all" in source_list:
        source_list = ["quora", "twitter", "instagram", "tiktok"]

    # Initialize scrapers
    print("Initializing scrapers...")
    scrapers = init_scrapers(source_list)

    if not scrapers:
        print("❌ No scrapers initialized. Exiting.")
        sys.exit(1)

    # Determine demographics
    if args.all_demographics:
        demographics = [
            (gender, age) for gender in ["women", "men"] for age in ["10-13", "14-17", "18-23"]
        ]
    else:
        demographics = [(args.gender, args.age)]

    print(f"\nConfiguration:")
    print(f"  Sources: {', '.join(scrapers.keys())}")
    print(f"  Demographics: {len(demographics)}")
    print(f"  Topic: {args.topic}")
    print(f"  Limit per source: {args.limit}")
    print(f"  Delay: {args.delay}s")

    # Run scraping
    results = run_scraping(scrapers, demographics, args.topic, args.limit, args.delay)

    # Print summary
    print_summary(results)

    print("\n✨ Alternative sources scraping complete!")


if __name__ == "__main__":
    main()
