#!/usr/bin/env python3
"""
Test script for alternative content source scrapers.

Tests Quora and Twitter scrapers functionality without requiring actual API access.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add scripts/scrapers directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts', 'scrapers'))

from quora_scraper import QuoraScraper
from twitter_scraper import TwitterScraper
from base_scraper import BaseScraper


def test_base_scraper():
    """Test base scraper functionality."""
    print("\n" + "="*60)
    print("Testing BaseScraper - Abstract Base Class")
    print("="*60)
    
    # Test that we can't instantiate abstract class
    try:
        scraper = BaseScraper("test")
        print("   ❌ Should not be able to instantiate abstract class")
        return False
    except TypeError:
        print("   ✅ Correctly prevents instantiation of abstract class")
    
    return True


def test_quora_scraper_basic():
    """Test basic Quora scraper functionality."""
    print("\n" + "="*60)
    print("Testing QuoraScraper - Basic Functionality")
    print("="*60)
    
    scraper = QuoraScraper()
    
    # Test 1: Check initialization
    print("\n1. Testing initialization...")
    if scraper.source_name == "quora":
        print("   ✅ Scraper initialized with correct source name")
    else:
        print("   ❌ Incorrect source name")
        return False
    
    # Test 2: Scrape content (mock data)
    print("\n2. Testing content scraping...")
    content = scraper.scrape_content("test topic", "women", "18-23", limit=10)
    
    if len(content) > 0:
        print(f"   ✅ Scraped {len(content)} items")
    else:
        print("   ❌ No content scraped")
        return False
    
    # Test 3: Validate content structure
    print("\n3. Testing content structure...")
    required_fields = ["id", "title", "url", "source"]
    first_item = content[0]
    missing_fields = [f for f in required_fields if f not in first_item]
    
    if not missing_fields:
        print(f"   ✅ Content has all required fields: {', '.join(required_fields)}")
    else:
        print(f"   ❌ Missing fields: {', '.join(missing_fields)}")
        return False
    
    # Test 4: Filter age-appropriate content
    print("\n4. Testing age-appropriate filtering...")
    
    # Create test data with inappropriate content
    test_content = [
        {"title": "Clean content", "text": "This is appropriate"},
        {"title": "Inappropriate content", "text": "Contains explicit material"},
        {"title": "Another clean one", "text": "Safe for all ages"}
    ]
    
    filtered = scraper.filter_age_appropriate(test_content, "10-13")
    
    if len(filtered) == 2:
        print(f"   ✅ Correctly filtered content (2 out of 3 items kept)")
    else:
        print(f"   ❌ Filter returned {len(filtered)} items, expected 2")
        return False
    
    return True


def test_twitter_scraper_basic():
    """Test basic Twitter scraper functionality."""
    print("\n" + "="*60)
    print("Testing TwitterScraper - Basic Functionality")
    print("="*60)
    
    scraper = TwitterScraper()
    
    # Test 1: Check initialization
    print("\n1. Testing initialization...")
    if scraper.source_name == "twitter":
        print("   ✅ Scraper initialized with correct source name")
    else:
        print("   ❌ Incorrect source name")
        return False
    
    # Test 2: Scrape content (mock data)
    print("\n2. Testing content scraping...")
    content = scraper.scrape_content("test topic", "men", "14-17", limit=10)
    
    if len(content) > 0:
        print(f"   ✅ Scraped {len(content)} items")
    else:
        print("   ❌ No content scraped")
        return False
    
    # Test 3: Validate content structure
    print("\n3. Testing content structure...")
    required_fields = ["id", "thread_id", "url", "author", "source"]
    first_item = content[0]
    missing_fields = [f for f in required_fields if f not in first_item]
    
    if not missing_fields:
        print(f"   ✅ Content has all required fields: {', '.join(required_fields)}")
    else:
        print(f"   ❌ Missing fields: {', '.join(missing_fields)}")
        return False
    
    # Test 4: Check engagement data
    print("\n4. Testing engagement data...")
    if "engagement" in first_item and "likes" in first_item["engagement"]:
        print(f"   ✅ Engagement data present")
    else:
        print(f"   ❌ Missing engagement data")
        return False
    
    return True


def test_scraper_save_functionality():
    """Test scraper save functionality with temp directory."""
    print("\n" + "="*60)
    print("Testing Scraper Save Functionality")
    print("="*60)
    
    # Use a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        scraper = QuoraScraper()
        
        # Override base output directory to temp dir
        scraper.base_output_dir = Path(temp_dir) / "quora"
        
        # Create mock content
        mock_content = [
            {
                "id": "test_1",
                "title": "Test Question",
                "text": "Test content",
                "source": "quora"
            }
        ]
        
        # Save content
        print("\n1. Testing save_content()...")
        output_file = scraper.save_content(mock_content, "women", "18-23")
        
        if output_file.exists():
            print(f"   ✅ File created: {output_file.name}")
        else:
            print(f"   ❌ File not created")
            return False
        
        # Validate JSON structure
        print("\n2. Validating saved JSON structure...")
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        required_fields = ["source", "gender", "age_bucket", "total_items", "scraped_at", "content"]
        missing_fields = [f for f in required_fields if f not in data]
        
        if not missing_fields:
            print(f"   ✅ JSON has all required fields")
        else:
            print(f"   ❌ Missing fields: {', '.join(missing_fields)}")
            return False
        
        # Check content array
        if data["total_items"] == len(mock_content):
            print(f"   ✅ Content count matches ({data['total_items']} items)")
        else:
            print(f"   ❌ Content count mismatch")
            return False
    
    return True


def test_demographic_variations():
    """Test scraping with different demographic combinations."""
    print("\n" + "="*60)
    print("Testing Demographic Variations")
    print("="*60)
    
    scraper = QuoraScraper()
    demographics = [
        ("women", "10-13"),
        ("women", "14-17"),
        ("women", "18-23"),
        ("men", "10-13"),
        ("men", "14-17"),
        ("men", "18-23"),
    ]
    
    for gender, age in demographics:
        content = scraper.scrape_content("test", gender, age, limit=5)
        if len(content) > 0:
            print(f"   ✅ {gender:6}/{age:6} - {len(content)} items scraped")
        else:
            print(f"   ❌ {gender:6}/{age:6} - No content")
            return False
    
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("ALTERNATIVE CONTENT SOURCES - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Base Scraper", test_base_scraper),
        ("Quora Scraper Basic", test_quora_scraper_basic),
        ("Twitter Scraper Basic", test_twitter_scraper_basic),
        ("Save Functionality", test_scraper_save_functionality),
        ("Demographic Variations", test_demographic_variations),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' raised exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
