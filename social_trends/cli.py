"""
Command-line interface for the social trends pipeline.

Usage:
    python -m social_trends.cli --sources youtube,google_trends --region US --limit 50 --out data/trends.csv
"""

import asyncio
import argparse
import sys
from typing import List

from social_trends.pipeline import TrendsPipeline
from social_trends.sources import (
    YouTubeSource,
    GoogleTrendsSource,
    TikTokSource,
    InstagramSource,
    ExplodingTopicsSource
)


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Social Trends Pipeline - Aggregate trending content from multiple sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch YouTube trends for US
  python -m social_trends.cli --sources youtube --region US --limit 50

  # Fetch from multiple sources and regions
  python -m social_trends.cli --sources youtube,google_trends --region US,UK,CZ --limit 100

  # Export to JSON
  python -m social_trends.cli --sources youtube --region US --out trends.json --format json

  # Use SQLite with velocity tracking
  python -m social_trends.cli --sources youtube --region US --storage sqlite --enable-velocity

  # Use custom root directory (e.g., for tests)
  python -m social_trends.cli --sources youtube --region US --root-dir TestInstance

Sources:
  - youtube: YouTube Data API v3 (requires YOUTUBE_API_KEY env var)
  - google_trends: Google Trends via pytrends
  - tiktok: TikTok (not yet implemented)
  - instagram: Instagram (not yet implemented)
  - exploding_topics: Exploding Topics (not yet implemented)
        """
    )
    
    parser.add_argument(
        "--sources",
        type=str,
        default="youtube,google_trends",
        help="Comma-separated list of sources to query (default: youtube,google_trends)"
    )
    
    parser.add_argument(
        "--region",
        type=str,
        default="US",
        help="Comma-separated list of region codes (default: US)"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum items to fetch per source (default: 50)"
    )
    
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.0,
        help="Minimum score threshold (default: 0.0)"
    )
    
    parser.add_argument(
        "--out",
        type=str,
        default="trends",
        help="Output file path without extension (default: trends)"
    )
    
    parser.add_argument(
        "--root-dir",
        type=str,
        default="data",
        help="Root directory for all processing (default: data, use TestInstance for tests)"
    )
    
    parser.add_argument(
        "--format",
        type=str,
        choices=["csv", "json"],
        default="csv",
        help="Output format (default: csv)"
    )
    
    parser.add_argument(
        "--storage",
        type=str,
        choices=["csv", "sqlite"],
        default="csv",
        help="Storage backend (default: csv)"
    )
    
    parser.add_argument(
        "--enable-velocity",
        action="store_true",
        help="Enable velocity tracking (requires sqlite storage)"
    )
    
    return parser.parse_args()


def init_sources(source_names: List[str]) -> List:
    """Initialize source instances"""
    sources = []
    
    for name in source_names:
        name = name.strip().lower()
        
        try:
            if name == "youtube":
                sources.append(YouTubeSource())
                print(f"✅ Initialized YouTube source")
            elif name == "google_trends":
                sources.append(GoogleTrendsSource())
                print(f"✅ Initialized Google Trends source")
            elif name == "tiktok":
                sources.append(TikTokSource())
                print(f"⚠️  TikTok source is a stub (not yet implemented)")
            elif name == "instagram":
                sources.append(InstagramSource())
                print(f"⚠️  Instagram source is a stub (not yet implemented)")
            elif name == "exploding_topics":
                sources.append(ExplodingTopicsSource())
                print(f"⚠️  Exploding Topics source is a stub (not yet implemented)")
            else:
                print(f"❌ Unknown source: {name}")
        except Exception as e:
            print(f"❌ Failed to initialize {name}: {e}")
    
    return sources


async def main():
    """Main entry point"""
    args = parse_args()
    
    # Parse sources and regions
    source_names = [s.strip() for s in args.sources.split(",")]
    regions = [r.strip().upper() for r in args.region.split(",")]
    
    print("=" * 60)
    print("🌐 Social Trends Pipeline")
    print("=" * 60)
    print(f"Sources: {', '.join(source_names)}")
    print(f"Regions: {', '.join(regions)}")
    print(f"Limit per source: {args.limit}")
    print(f"Min score: {args.min_score}")
    print(f"Root directory: {args.root_dir}")
    print(f"Storage: {args.storage}")
    if args.enable_velocity:
        print(f"Velocity tracking: ENABLED")
    print("=" * 60)
    
    # Initialize sources
    sources = init_sources(source_names)
    
    if not sources:
        print("❌ No sources initialized. Exiting.")
        sys.exit(1)
    
    # Validate velocity tracking
    if args.enable_velocity and args.storage != "sqlite":
        print("⚠️  Velocity tracking requires SQLite storage. Disabling velocity tracking.")
        args.enable_velocity = False
    
    # Initialize pipeline
    pipeline = TrendsPipeline(
        sources=sources,
        storage_backend=args.storage,
        storage_path=args.out,
        enable_velocity=args.enable_velocity,
        root_dir=args.root_dir
    )
    
    try:
        # Run pipeline
        items = await pipeline.run(
            regions=regions,
            limit_per_source=args.limit,
            min_score=args.min_score
        )
        
        # Export if JSON format requested
        if args.format == "json":
            json_path = f"{args.root_dir}/{args.out}.json"
            pipeline.export_json(items, json_path)
        
        # Print summary
        print("=" * 60)
        print("📊 Summary")
        print("=" * 60)
        print(f"Total items collected: {len(items)}")
        
        if items:
            print(f"Top 5 trends:")
            for i, item in enumerate(items[:5], 1):
                print(f"  {i}. [{item.source}] {item.title_or_keyword} (score: {item.score:.2f})")
        
        print("=" * 60)
        print("✅ Pipeline complete!")
        
    finally:
        # Clean up
        await pipeline.close()


if __name__ == "__main__":
    asyncio.run(main())
