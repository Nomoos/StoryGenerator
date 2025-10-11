#!/usr/bin/env python3
"""
Test script for YouTube Channel Scraper download feature.
Tests that the download functionality is properly integrated.
"""

import sys
from pathlib import Path
from youtube_channel_scraper import YouTubeChannelScraper, VideoMetadata


def test_initialization_with_download_params():
    """Test that scraper initializes with download parameters."""
    print("\n" + "="*60)
    print("Testing Initialization with Download Parameters")
    print("="*60)
    
    # Test with download enabled
    scraper = YouTubeChannelScraper(
        output_dir="/tmp/test_scraper",
        download_high_views=True,
        view_threshold=5000000
    )
    
    if scraper.download_high_views and scraper.view_threshold == 5000000:
        print("   ✅ Download parameters initialized correctly")
        print(f"   ✅ Download enabled: {scraper.download_high_views}")
        print(f"   ✅ View threshold: {scraper.view_threshold:,}")
        return True
    else:
        print("   ❌ Download parameters not set correctly")
        return False


def test_download_video_method_exists():
    """Test that download_video method exists and has correct signature."""
    print("\n" + "="*60)
    print("Testing Download Video Method")
    print("="*60)
    
    scraper = YouTubeChannelScraper(
        output_dir="/tmp/test_scraper",
        download_high_views=True
    )
    
    # Check if method exists
    if hasattr(scraper, 'download_video'):
        print("   ✅ download_video method exists")
        
        # Check if downloaded_videos list is initialized
        if hasattr(scraper, 'downloaded_videos'):
            print("   ✅ downloaded_videos list initialized")
            return True
        else:
            print("   ❌ downloaded_videos list not found")
            return False
    else:
        print("   ❌ download_video method not found")
        return False


def test_download_decision_logic():
    """Test that download decision logic works correctly."""
    print("\n" + "="*60)
    print("Testing Download Decision Logic")
    print("="*60)
    
    # Create a mock video metadata with high views
    mock_video = VideoMetadata(
        video_id="test123",
        title="Test Video",
        description="Test description",
        tags=["test"],
        duration="01:00",
        duration_seconds=60,
        view_count=15000000,  # 15 million views
        like_count=100000,
        comment_count=5000,
        upload_date="20240101",
        url="https://www.youtube.com/watch?v=test123",
        thumbnail_url="https://example.com/thumb.jpg",
        subtitles_available=False,
        subtitle_text=None
    )
    
    # Test with download disabled
    scraper_disabled = YouTubeChannelScraper(
        output_dir="/tmp/test_scraper",
        download_high_views=False,
        view_threshold=10000000
    )
    
    result = scraper_disabled.download_video("test123", mock_video)
    if not result:
        print("   ✅ Download correctly skipped when disabled")
    else:
        print("   ❌ Download should be skipped when disabled")
        return False
    
    # Test with views below threshold
    scraper_below = YouTubeChannelScraper(
        output_dir="/tmp/test_scraper",
        download_high_views=True,
        view_threshold=20000000  # 20 million
    )
    
    result = scraper_below.download_video("test123", mock_video)
    if not result:
        print("   ✅ Download correctly skipped when below threshold")
    else:
        print("   ❌ Download should be skipped when below threshold")
        return False
    
    print("   ✅ All download decision logic tests passed")
    return True


def test_command_line_args():
    """Test that command line arguments are properly defined."""
    print("\n" + "="*60)
    print("Testing Command Line Arguments")
    print("="*60)
    
    import subprocess
    
    # Check help output for new arguments
    result = subprocess.run(
        [sys.executable, "youtube_channel_scraper.py", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    checks = []
    
    if "--download-high-views" in result.stdout:
        print("   ✅ --download-high-views argument present")
        checks.append(True)
    else:
        print("   ❌ --download-high-views argument missing")
        checks.append(False)
    
    if "--view-threshold" in result.stdout:
        print("   ✅ --view-threshold argument present")
        checks.append(True)
    else:
        print("   ❌ --view-threshold argument missing")
        checks.append(False)
    
    if "10 million" in result.stdout:
        print("   ✅ Help text mentions 10 million views")
        checks.append(True)
    else:
        print("   ❌ Help text should mention 10 million views")
        checks.append(False)
    
    return all(checks)


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("YouTube Channel Scraper - Download Feature Tests")
    print("="*70)
    
    tests = [
        test_initialization_with_download_params,
        test_download_video_method_exists,
        test_download_decision_logic,
        test_command_line_args,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "="*70)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("="*70)
    
    if all(results):
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
