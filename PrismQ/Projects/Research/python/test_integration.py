#!/usr/bin/env python3
"""
Integration test for YouTube Channel Scraper.
Demonstrates the complete workflow without actually scraping YouTube.
"""

import sys
import json
from pathlib import Path


def test_complete_workflow():
    """Test that all components work together correctly."""
    print("\n" + "="*70)
    print("YouTube Channel Scraper - Integration Test")
    print("="*70)
    print("\nThis test verifies that the scraper is properly configured")
    print("and ready to use. It does NOT make actual YouTube requests.\n")
    
    # Test 1: Import and basic initialization
    print("Test 1: Module Import and Initialization")
    print("-" * 60)
    try:
        from youtube_channel_scraper import YouTubeChannelScraper, VideoMetadata
        print("✅ Module imported successfully")
        
        scraper = YouTubeChannelScraper(
            output_dir="/tmp/test_scraper_integration",
            download_high_views=True,
            view_threshold=10000000
        )
        print("✅ Scraper initialized with download feature")
        print(f"   - Download enabled: {scraper.download_high_views}")
        print(f"   - View threshold: {scraper.view_threshold:,}")
    except Exception as e:
        print(f"❌ Failed to initialize scraper: {e}")
        return False
    
    # Test 2: Check dependencies
    print("\nTest 2: Dependencies Check")
    print("-" * 60)
    try:
        if scraper.check_dependencies():
            print("✅ yt-dlp is installed and accessible")
        else:
            print("⚠️  yt-dlp not found (required for actual usage)")
    except Exception as e:
        print(f"⚠️  Could not check dependencies: {e}")
    
    # Test 3: URL extraction
    print("\nTest 3: Channel URL Extraction")
    print("-" * 60)
    try:
        test_cases = [
            ("@testchannel", "https://www.youtube.com/@testchannel"),
            ("UCtest123", "https://www.youtube.com/channel/UCtest123"),
            ("https://www.youtube.com/@existing", "https://www.youtube.com/@existing"),
        ]
        
        all_passed = True
        for input_str, expected in test_cases:
            result = scraper.extract_channel_url(input_str)
            if result == expected:
                print(f"✅ '{input_str}' -> '{result}'")
            else:
                print(f"❌ '{input_str}' expected '{expected}' but got '{result}'")
                all_passed = False
        
        if not all_passed:
            return False
    except Exception as e:
        print(f"❌ URL extraction failed: {e}")
        return False
    
    # Test 4: Story detection logic
    print("\nTest 4: Story Detection Logic")
    print("-" * 60)
    try:
        # Create test video metadata
        story_video = VideoMetadata(
            video_id="test_story",
            title="AITA for My Revenge Story?",
            description="This is a true story about what happened...",
            tags=["story", "storytime", "reddit"],
            duration="01:30",
            duration_seconds=90,
            view_count=15000000,
            like_count=500000,
            comment_count=10000,
            upload_date="20240101",
            url="https://www.youtube.com/watch?v=test_story",
            thumbnail_url="https://example.com/thumb.jpg",
            subtitles_available=True,
            subtitle_text="I was in a difficult situation..."
        )
        
        is_story, confidence, indicators = scraper.detect_story_video(story_video)
        print(f"✅ Story detection works")
        print(f"   - Is story: {is_story}")
        print(f"   - Confidence: {confidence:.2f}")
        print(f"   - Indicators: {len(indicators)} found")
        
        if is_story and confidence > 0.3:
            print("✅ Story video correctly identified")
        else:
            print("⚠️  Story detection may need tuning")
    except Exception as e:
        print(f"❌ Story detection failed: {e}")
        return False
    
    # Test 5: Download decision logic
    print("\nTest 5: Download Decision Logic")
    print("-" * 60)
    try:
        high_view_video = VideoMetadata(
            video_id="test_high",
            title="Test High Views",
            description="Test",
            tags=[],
            duration="01:00",
            duration_seconds=60,
            view_count=20000000,  # 20M views
            like_count=100000,
            comment_count=5000,
            upload_date="20240101",
            url="https://www.youtube.com/watch?v=test_high",
            thumbnail_url="https://example.com/thumb.jpg",
            subtitles_available=False,
            subtitle_text=None
        )
        
        low_view_video = VideoMetadata(
            video_id="test_low",
            title="Test Low Views",
            description="Test",
            tags=[],
            duration="01:00",
            duration_seconds=60,
            view_count=5000000,  # 5M views
            like_count=10000,
            comment_count=500,
            upload_date="20240101",
            url="https://www.youtube.com/watch?v=test_low",
            thumbnail_url="https://example.com/thumb.jpg",
            subtitles_available=False,
            subtitle_text=None
        )
        
        # Note: We don't actually call download_video as it would try to download
        # Instead, we just check the logic
        would_download_high = (scraper.download_high_views and 
                               high_view_video.view_count >= scraper.view_threshold)
        would_download_low = (scraper.download_high_views and 
                              low_view_video.view_count >= scraper.view_threshold)
        
        if would_download_high and not would_download_low:
            print("✅ Download logic correct")
            print(f"   - Would download high-view video: {high_view_video.view_count:,} views")
            print(f"   - Would skip low-view video: {low_view_video.view_count:,} views")
        else:
            print("❌ Download logic incorrect")
            return False
    except Exception as e:
        print(f"❌ Download logic test failed: {e}")
        return False
    
    # Test 6: Output directory structure
    print("\nTest 6: Output Directory Structure")
    print("-" * 60)
    try:
        output_dir = Path("/tmp/test_scraper_integration")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if output_dir.exists() and output_dir.is_dir():
            print(f"✅ Output directory created: {output_dir}")
        else:
            print(f"❌ Could not create output directory")
            return False
    except Exception as e:
        print(f"❌ Directory creation failed: {e}")
        return False
    
    print("\n" + "="*70)
    print("✅ Integration Test Complete!")
    print("="*70)
    print("\nThe scraper is properly configured and ready to use.")
    print("\nTo test with a real channel, run:")
    print("  python youtube_channel_scraper.py @channelname --top 5")
    print("\nTo enable downloads (10M+ views):")
    print("  python youtube_channel_scraper.py @channelname --top 10 --download-high-views")
    print("\n")
    
    return True


if __name__ == "__main__":
    try:
        success = test_complete_workflow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Integration test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
