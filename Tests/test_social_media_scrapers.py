#!/usr/bin/env python3
"""
Tests for Instagram and TikTok scrapers.
Tests mock data implementation and BaseScraper interface compliance.
"""

import sys
import json
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "scrapers"))

import instagram_scraper
import tiktok_scraper


def test_instagram_initialization():
    """Test Instagram scraper initialization."""
    print("\n" + "="*60)
    print("Test: Instagram Scraper Initialization")
    print("="*60)
    
    scraper = instagram_scraper.InstagramScraper(use_mock=True)
    
    if scraper.source_name == "instagram":
        print("   ✅ Source name correct")
    else:
        print(f"   ❌ Source name incorrect: {scraper.source_name}")
        return False
    
    if scraper.use_mock:
        print("   ✅ Mock mode enabled")
    else:
        print("   ❌ Mock mode not enabled")
        return False
    
    return True


def test_tiktok_initialization():
    """Test TikTok scraper initialization."""
    print("\n" + "="*60)
    print("Test: TikTok Scraper Initialization")
    print("="*60)
    
    scraper = tiktok_scraper.TikTokScraper(use_mock=True)
    
    if scraper.source_name == "tiktok":
        print("   ✅ Source name correct")
    else:
        print(f"   ❌ Source name incorrect: {scraper.source_name}")
        return False
    
    if scraper.use_mock:
        print("   ✅ Mock mode enabled")
    else:
        print("   ❌ Mock mode not enabled")
        return False
    
    return True


def test_instagram_hashtag_generation():
    """Test Instagram hashtag generation."""
    print("\n" + "="*60)
    print("Test: Instagram Hashtag Generation")
    print("="*60)
    
    scraper = instagram_scraper.InstagramScraper(use_mock=True)
    
    # Test age-specific hashtags
    hashtags_10_13 = scraper._get_hashtags("stories", "women", "10-13")
    hashtags_18_23 = scraper._get_hashtags("stories", "women", "18-23")
    
    if len(hashtags_10_13) > 0 and len(hashtags_18_23) > 0:
        print(f"   ✅ Hashtags generated: 10-13: {hashtags_10_13[:3]}, 18-23: {hashtags_18_23[:3]}")
    else:
        print(f"   ❌ Hashtag generation failed")
        return False
    
    # Check that different age groups have different hashtags
    if hashtags_10_13 != hashtags_18_23:
        print(f"   ✅ Age-specific hashtags different")
    else:
        print(f"   ⚠️  Age-specific hashtags identical")
    
    return True


def test_tiktok_hashtag_generation():
    """Test TikTok hashtag generation."""
    print("\n" + "="*60)
    print("Test: TikTok Hashtag Generation")
    print("="*60)
    
    scraper = tiktok_scraper.TikTokScraper(use_mock=True)
    
    # Test age-specific hashtags
    hashtags_14_17 = scraper._get_hashtags("drama", "men", "14-17")
    hashtags_18_23 = scraper._get_hashtags("drama", "men", "18-23")
    
    if len(hashtags_14_17) > 0 and len(hashtags_18_23) > 0:
        print(f"   ✅ Hashtags generated: 14-17: {hashtags_14_17[:3]}, 18-23: {hashtags_18_23[:3]}")
    else:
        print(f"   ❌ Hashtag generation failed")
        return False
    
    # Check that different age groups have different hashtags
    if hashtags_14_17 != hashtags_18_23:
        print(f"   ✅ Age-specific hashtags different")
    else:
        print(f"   ⚠️  Age-specific hashtags identical")
    
    return True


def test_instagram_mock_data():
    """Test Instagram mock data generation."""
    print("\n" + "="*60)
    print("Test: Instagram Mock Data Generation")
    print("="*60)
    
    scraper = instagram_scraper.InstagramScraper(use_mock=True)
    
    posts = scraper.scrape_content("life stories", "women", "18-23", limit=10)
    
    if len(posts) > 0:
        print(f"   ✅ Generated {len(posts)} mock posts")
    else:
        print(f"   ❌ No mock posts generated")
        return False
    
    # Check post structure
    required_fields = ["id", "title", "text", "url", "author", "likes", "comments", "source"]
    post = posts[0]
    
    for field in required_fields:
        if field not in post:
            print(f"   ❌ Missing field: {field}")
            return False
    
    print(f"   ✅ All required fields present")
    
    if post["source"] == "instagram":
        print(f"   ✅ Source field correct")
    else:
        print(f"   ❌ Source field incorrect: {post['source']}")
        return False
    
    return True


def test_tiktok_mock_data():
    """Test TikTok mock data generation."""
    print("\n" + "="*60)
    print("Test: TikTok Mock Data Generation")
    print("="*60)
    
    scraper = tiktok_scraper.TikTokScraper(use_mock=True)
    
    videos = scraper.scrape_content("storytime", "men", "14-17", limit=15)
    
    if len(videos) > 0:
        print(f"   ✅ Generated {len(videos)} mock videos")
    else:
        print(f"   ❌ No mock videos generated")
        return False
    
    # Check video structure
    required_fields = ["id", "title", "text", "url", "author", "likes", "comments", "shares", "views", "source"]
    video = videos[0]
    
    for field in required_fields:
        if field not in video:
            print(f"   ❌ Missing field: {field}")
            return False
    
    print(f"   ✅ All required fields present")
    
    if video["source"] == "tiktok":
        print(f"   ✅ Source field correct")
    else:
        print(f"   ❌ Source field incorrect: {video['source']}")
        return False
    
    return True


def test_instagram_age_filtering():
    """Test Instagram age-appropriate filtering."""
    print("\n" + "="*60)
    print("Test: Instagram Age-Appropriate Filtering")
    print("="*60)
    
    scraper = instagram_scraper.InstagramScraper(use_mock=True)
    
    # Create test posts with inappropriate content
    test_posts = [
        {"id": "1", "title": "Good story", "text": "A nice story about friendship"},
        {"id": "2", "title": "Bad story", "text": "This contains nsfw explicit content"},
        {"id": "3", "title": "Another good", "text": "A story about school"},
    ]
    
    # Filter for 10-13 age group
    filtered = scraper.filter_age_appropriate(test_posts, "10-13")
    
    if len(filtered) == 2:
        print(f"   ✅ Correctly filtered out inappropriate content (2/3 items kept)")
    else:
        print(f"   ❌ Filtering failed: expected 2, got {len(filtered)}")
        return False
    
    # Filter for 18-23 age group (no filtering)
    filtered_adult = scraper.filter_age_appropriate(test_posts, "18-23")
    
    if len(filtered_adult) == 3:
        print(f"   ✅ Adult filtering works (all 3 items kept)")
    else:
        print(f"   ❌ Adult filtering failed: expected 3, got {len(filtered_adult)}")
        return False
    
    return True


def test_tiktok_age_filtering():
    """Test TikTok age-appropriate filtering."""
    print("\n" + "="*60)
    print("Test: TikTok Age-Appropriate Filtering")
    print("="*60)
    
    scraper = tiktok_scraper.TikTokScraper(use_mock=True)
    
    # Create test videos with inappropriate content
    test_videos = [
        {"id": "1", "title": "Good video", "text": "A nice story about friendship"},
        {"id": "2", "title": "Bad video", "text": "This contains explicit adult content"},
        {"id": "3", "title": "Another good", "text": "A story about school"},
    ]
    
    # Filter for 14-17 age group
    filtered = scraper.filter_age_appropriate(test_videos, "14-17")
    
    if len(filtered) == 2:
        print(f"   ✅ Correctly filtered out inappropriate content (2/3 items kept)")
    else:
        print(f"   ❌ Filtering failed: expected 2, got {len(filtered)}")
        return False
    
    return True


def test_instagram_data_saving():
    """Test Instagram data saving functionality."""
    print("\n" + "="*60)
    print("Test: Instagram Data Saving")
    print("="*60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        scraper = instagram_scraper.InstagramScraper(use_mock=True)
        # Override base output dir for testing
        scraper.base_output_dir = Path(tmpdir) / "instagram"
        
        # Generate and save mock data
        posts = scraper.scrape_content("test", "women", "18-23", limit=5)
        output_file = scraper.save_content(posts, "women", "18-23")
        
        if output_file.exists():
            print(f"   ✅ Output file created: {output_file.name}")
        else:
            print(f"   ❌ Output file not created")
            return False
        
        # Verify JSON structure
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        required_keys = ["source", "gender", "age_bucket", "total_items", "content"]
        for key in required_keys:
            if key not in data:
                print(f"   ❌ Missing key in JSON: {key}")
                return False
        
        print(f"   ✅ JSON structure correct")
        
        if data["source"] == "instagram" and data["total_items"] == len(posts):
            print(f"   ✅ Data integrity verified")
        else:
            print(f"   ❌ Data integrity check failed")
            return False
    
    return True


def test_tiktok_data_saving():
    """Test TikTok data saving functionality."""
    print("\n" + "="*60)
    print("Test: TikTok Data Saving")
    print("="*60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        scraper = tiktok_scraper.TikTokScraper(use_mock=True)
        # Override base output dir for testing
        scraper.base_output_dir = Path(tmpdir) / "tiktok"
        
        # Generate and save mock data
        videos = scraper.scrape_content("test", "men", "14-17", limit=5)
        output_file = scraper.save_content(videos, "men", "14-17")
        
        if output_file.exists():
            print(f"   ✅ Output file created: {output_file.name}")
        else:
            print(f"   ❌ Output file not created")
            return False
        
        # Verify JSON structure
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        required_keys = ["source", "gender", "age_bucket", "total_items", "content"]
        for key in required_keys:
            if key not in data:
                print(f"   ❌ Missing key in JSON: {key}")
                return False
        
        print(f"   ✅ JSON structure correct")
        
        if data["source"] == "tiktok" and data["total_items"] == len(videos):
            print(f"   ✅ Data integrity verified")
        else:
            print(f"   ❌ Data integrity check failed")
            return False
    
    return True


def run_all_tests():
    """Run all social media scraper tests."""
    print("\n" + "="*80)
    print("SOCIAL MEDIA SCRAPERS TESTS (Instagram & TikTok)")
    print("="*80)
    
    tests = [
        ("Instagram Initialization", test_instagram_initialization),
        ("TikTok Initialization", test_tiktok_initialization),
        ("Instagram Hashtag Generation", test_instagram_hashtag_generation),
        ("TikTok Hashtag Generation", test_tiktok_hashtag_generation),
        ("Instagram Mock Data", test_instagram_mock_data),
        ("TikTok Mock Data", test_tiktok_mock_data),
        ("Instagram Age Filtering", test_instagram_age_filtering),
        ("TikTok Age Filtering", test_tiktok_age_filtering),
        ("Instagram Data Saving", test_instagram_data_saving),
        ("TikTok Data Saving", test_tiktok_data_saving),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n   ❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "="*80)
    print(f"Tests Passed: {passed}/{total}")
    if passed == total:
        print("✨ All tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
    print("="*80 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
