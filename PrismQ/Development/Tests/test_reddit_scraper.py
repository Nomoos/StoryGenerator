#!/usr/bin/env python3
"""
Test script for Reddit Story Scraper.
Tests the scraper configuration and basic functionality.
"""

import os
import sys
from pathlib import Path
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    import reddit_scraper
except ImportError as e:
    print(f"❌ Failed to import reddit_scraper: {e}")
    sys.exit(1)


def test_imports():
    """Test that all required imports are available."""
    print("\n" + "="*60)
    print("Testing Imports")
    print("="*60)
    
    try:
        import praw
        print("   ✅ PRAW library available")
    except ImportError:
        print("   ❌ PRAW library not installed")
        print("   Run: pip install praw")
        return False
    
    try:
        import json
        print("   ✅ JSON library available")
    except ImportError:
        print("   ❌ JSON library not available")
        return False
    
    return True


def test_subreddit_map():
    """Test that the subreddit map is properly configured."""
    print("\n" + "="*60)
    print("Testing Subreddit Map Configuration")
    print("="*60)
    
    subreddit_map = reddit_scraper.SUBREDDIT_MAP
    
    # Check all expected segments exist
    genders = ["women", "men"]
    ages = ["10-13", "14-17", "18-23"]
    
    all_present = True
    for gender in genders:
        for age in ages:
            segment_key = f"{gender}/{age}"
            if segment_key not in subreddit_map:
                print(f"   ❌ Missing segment: {segment_key}")
                all_present = False
            else:
                subreddits = subreddit_map[segment_key]
                print(f"   ✅ {segment_key}: {len(subreddits)} subreddits")
    
    if all_present:
        total_segments = len(genders) * len(ages)
        print(f"\n   ✅ All {total_segments} segments configured")
    
    return all_present


def test_filter_age_appropriate():
    """Test the age filtering function."""
    print("\n" + "="*60)
    print("Testing Age Filtering")
    print("="*60)
    
    # Test stories with various content
    test_stories = [
        {
            "id": "1",
            "title": "Appropriate story for all ages",
            "text": "This is a nice story about friendship.",
            "upvotes": 1000,
            "num_comments": 100
        },
        {
            "id": "2",
            "title": "Story with NSFW content",
            "text": "This contains nsfw material.",
            "upvotes": 2000,
            "num_comments": 200
        },
        {
            "id": "3",
            "title": "Another appropriate story",
            "text": "A story about overcoming challenges.",
            "upvotes": 1500,
            "num_comments": 150
        }
    ]
    
    # Test for 10-13 age group (should filter NSFW)
    filtered_10_13 = reddit_scraper.filter_age_appropriate(test_stories, "10-13")
    if len(filtered_10_13) == 2:
        print("   ✅ Age 10-13 filtering works (filtered out NSFW)")
    else:
        print(f"   ❌ Age 10-13 filtering failed (expected 2, got {len(filtered_10_13)})")
        return False
    
    # Test for 18-23 age group (should not filter)
    filtered_18_23 = reddit_scraper.filter_age_appropriate(test_stories, "18-23")
    if len(filtered_18_23) == 3:
        print("   ✅ Age 18-23 filtering works (no filtering)")
    else:
        print(f"   ❌ Age 18-23 filtering failed (expected 3, got {len(filtered_18_23)})")
        return False
    
    return True


def test_environment_variables():
    """Test that Reddit API credentials are configured."""
    print("\n" + "="*60)
    print("Testing Environment Variables")
    print("="*60)
    
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    
    if client_id and client_id != "your_reddit_client_id_here":
        print("   ✅ REDDIT_CLIENT_ID is set")
    else:
        print("   ⚠️  REDDIT_CLIENT_ID not set or using default value")
        print("      Set this before running the scraper")
    
    if client_secret and client_secret != "your_reddit_client_secret_here":
        print("   ✅ REDDIT_CLIENT_SECRET is set")
    else:
        print("   ⚠️  REDDIT_CLIENT_SECRET not set or using default value")
        print("      Set this before running the scraper")
    
    return True  # Not a failure, just a warning


def test_output_directory():
    """Test that output directory structure can be created."""
    print("\n" + "="*60)
    print("Testing Output Directory Structure")
    print("="*60)
    
    root_dir = Path(__file__).parent.parent
    test_dir = root_dir / "Generator" / "sources" / "reddit" / "test" / "10-13"
    
    try:
        test_dir.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Can create output directories")
        
        # Cleanup test directory
        test_dir.rmdir()
        test_dir.parent.rmdir()
        
        return True
    except Exception as e:
        print(f"   ❌ Failed to create output directory: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("Reddit Scraper Test Suite")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Subreddit Map", test_subreddit_map),
        ("Age Filtering", test_filter_age_appropriate),
        ("Environment Variables", test_environment_variables),
        ("Output Directory", test_output_directory),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n   ❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {name}")
    
    print("\n" + "="*60)
    print(f"Tests Passed: {passed}/{total}")
    print("="*60)
    
    if passed == total:
        print("\n✨ All tests passed!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
