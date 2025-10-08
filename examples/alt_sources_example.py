#!/usr/bin/env python3
"""
Example: Using Alternative Content Source Scrapers

This example demonstrates how to use the Quora and Twitter scrapers
to gather story content for different demographics.
"""

import sys
from pathlib import Path

# Add scrapers to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "scrapers"))

from quora_scraper import QuoraScraper
from twitter_scraper import TwitterScraper


def example_single_scraper():
    """Example 1: Using a single scraper."""
    print("\n" + "="*60)
    print("Example 1: Single Scraper Usage")
    print("="*60)
    
    # Initialize Quora scraper
    scraper = QuoraScraper()
    
    # Scrape content for women aged 18-23
    result = scraper.run(
        topic="relationships",
        gender="women",
        age_bucket="18-23",
        limit=20
    )
    
    print(f"\n✅ Scraping complete!")
    print(f"   Source: {result['source']}")
    print(f"   Demographic: {result['gender']}/{result['age_bucket']}")
    print(f"   Items scraped: {result['scraped']}")
    print(f"   Items after filtering: {result['filtered']}")
    print(f"   Output file: {result['output_file']}")


def example_multiple_demographics():
    """Example 2: Scraping multiple demographics."""
    print("\n" + "="*60)
    print("Example 2: Multiple Demographics")
    print("="*60)
    
    scraper = TwitterScraper()
    
    demographics = [
        ("women", "14-17"),
        ("women", "18-23"),
        ("men", "14-17"),
    ]
    
    results = []
    for gender, age in demographics:
        print(f"\nScraping {gender}/{age}...")
        result = scraper.run("life stories", gender, age, limit=10)
        results.append(result)
    
    print("\n" + "="*60)
    print("Results Summary:")
    print("="*60)
    for r in results:
        print(f"{r['gender']:6}/{r['age_bucket']:6} - {r['filtered']} items → {r['output_file']}")


def example_both_sources():
    """Example 3: Using both Quora and Twitter."""
    print("\n" + "="*60)
    print("Example 3: Both Sources")
    print("="*60)
    
    scrapers = {
        "quora": QuoraScraper(),
        "twitter": TwitterScraper()
    }
    
    gender = "women"
    age = "18-23"
    
    for source_name, scraper in scrapers.items():
        print(f"\n📥 Scraping {source_name.upper()}...")
        result = scraper.run("college life", gender, age, limit=15)
        print(f"   ✓ {result['filtered']} items saved")


def example_age_filtering():
    """Example 4: Age-appropriate filtering."""
    print("\n" + "="*60)
    print("Example 4: Age-Appropriate Filtering")
    print("="*60)
    
    scraper = QuoraScraper()
    
    # Mock content with varying appropriateness
    test_content = [
        {"title": "Wholesome friendship story", "text": "A story about friends"},
        {"title": "Mature content", "text": "Contains explicit material here"},
        {"title": "School experience", "text": "A day at school"},
        {"title": "Adult topic", "text": "This discusses adult themes and sex"},
        {"title": "General advice", "text": "Life advice for everyone"},
    ]
    
    print(f"\nOriginal content: {len(test_content)} items")
    
    for age_bucket in ["10-13", "14-17", "18-23"]:
        filtered = scraper.filter_age_appropriate(test_content, age_bucket)
        print(f"\nAge {age_bucket}: {len(filtered)} items passed filter")
        for item in filtered:
            print(f"   ✓ {item['title']}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("ALTERNATIVE CONTENT SOURCES - EXAMPLES")
    print("="*60)
    print("\nThese examples demonstrate mock data usage.")
    print("For production, implement actual API calls.")
    
    # Run examples
    example_single_scraper()
    example_multiple_demographics()
    example_both_sources()
    example_age_filtering()
    
    print("\n" + "="*60)
    print("✨ All examples complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review generated JSON files in src/Generator/sources/")
    print("2. Integrate with quality scoring pipeline")
    print("3. Use content for story idea generation")
    print()


if __name__ == "__main__":
    main()
