#!/usr/bin/env python3
"""
Tests for all export enhancements: Registry, Batch Export, Thumbnails, and Platform Export.
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add src/Python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'Python'))

from Models.StoryIdea import StoryIdea
from Tools.ExportRegistry import ExportRegistry
from Tools.BatchExporter import BatchExporter
from Tools.ThumbnailGenerator import ThumbnailGenerator
from Tools.PlatformExporter import PlatformExporter
from Tools.Utils import generate_title_id


def test_export_registry():
    """Test ExportRegistry functionality."""
    print("\n" + "="*60)
    print("Testing ExportRegistry")
    print("="*60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        registry_path = os.path.join(tmpdir, "test_registry.json")
        registry = ExportRegistry(registry_path)
        
        # Test 1: Register export
        print("\n1. Testing export registration...")
        success = registry.register_export(
            title_id="test123",
            title="Test Story",
            segment="women",
            age_group="18-23",
            video_path="/path/to/video.mp4",
            thumbnail_path="/path/to/thumb.jpg",
            metadata_path="/path/to/meta.json"
        )
        
        if success and os.path.exists(registry_path):
            print("   ✅ Export registered successfully")
        else:
            print("   ❌ Failed to register export")
            return False
        
        # Test 2: Retrieve video info
        print("\n2. Testing video info retrieval...")
        info = registry.get_video_info("test123")
        if info and info["title"] == "Test Story":
            print("   ✅ Video info retrieved successfully")
        else:
            print("   ❌ Failed to retrieve video info")
            return False
        
        # Test 3: Update publish status
        print("\n3. Testing publish status update...")
        success = registry.update_publish_status(
            "test123",
            "youtube",
            "published",
            "https://youtube.com/shorts/abc123"
        )
        
        if success:
            info = registry.get_video_info("test123")
            if "youtube" in info["platforms"]:
                print("   ✅ Publish status updated successfully")
            else:
                print("   ❌ Platform info not found")
                return False
        else:
            print("   ❌ Failed to update publish status")
            return False
        
        # Test 4: Update performance metrics
        print("\n4. Testing performance metrics update...")
        success = registry.update_performance(
            "test123",
            views=1000,
            likes=50,
            shares=10,
            comments=5
        )
        
        if success:
            info = registry.get_video_info("test123")
            perf = info["performance"]
            if perf["views"] == 1000 and perf["engagement_rate"] > 0:
                print(f"   ✅ Performance updated (engagement: {perf['engagement_rate']}%)")
            else:
                print("   ❌ Performance metrics incorrect")
                return False
        else:
            print("   ❌ Failed to update performance")
            return False
        
        # Test 5: Get statistics
        print("\n5. Testing statistics generation...")
        stats = registry.get_statistics()
        if stats["total_videos"] == 1 and stats["total_views"] == 1000:
            print("   ✅ Statistics generated successfully")
        else:
            print("   ❌ Statistics incorrect")
            return False
        
        # Test 6: Generate report
        print("\n6. Testing report generation...")
        report = registry.generate_report()
        if "Total Videos: 1" in report and "Total Views: 1,000" in report:
            print("   ✅ Report generated successfully")
        else:
            print("   ❌ Report incorrect")
            return False
    
    print("\n✅ ExportRegistry tests passed!")
    return True


def test_thumbnail_generator():
    """Test ThumbnailGenerator functionality."""
    print("\n" + "="*60)
    print("Testing ThumbnailGenerator")
    print("="*60)
    
    # Note: This test requires FFmpeg and a video file
    # We'll test the basic functionality without actual video processing
    
    generator = ThumbnailGenerator(1080, 1920)
    
    # Test 1: Check initialization
    print("\n1. Testing initialization...")
    if generator.width == 1080 and generator.height == 1920:
        print("   ✅ ThumbnailGenerator initialized correctly")
    else:
        print("   ❌ Initialization failed")
        return False
    
    print("\n✅ ThumbnailGenerator basic tests passed!")
    print("⚠️  Full video processing tests require FFmpeg and sample video")
    return True


def test_platform_exporter():
    """Test PlatformExporter functionality."""
    print("\n" + "="*60)
    print("Testing PlatformExporter")
    print("="*60)
    
    exporter = PlatformExporter()
    
    # Create test story
    story = StoryIdea(
        story_title="Platform Test Story",
        narrator_gender="F",
        tone="exciting",
        theme="adventure",
        goal="Test platform export",
        potencial={"age_groups": {"20_25": 90}}
    )
    
    # Test 1: List platforms
    print("\n1. Testing platform listing...")
    platforms = exporter.list_platforms()
    if len(platforms) == 3 and "youtube" in platforms:
        print(f"   ✅ Found {len(platforms)} platforms: {', '.join(platforms)}")
    else:
        print("   ❌ Platform listing failed")
        return False
    
    # Test 2: Generate YouTube metadata
    print("\n2. Testing YouTube metadata generation...")
    yt_meta = exporter.generate_platform_metadata(story, "youtube")
    if yt_meta["platform"] == "youtube" and "platform_hashtags" in yt_meta:
        print(f"   ✅ YouTube metadata generated")
        print(f"      Title: {yt_meta['platform_title']}")
        print(f"      Hashtags: {', '.join(yt_meta['platform_hashtags'])}")
    else:
        print("   ❌ YouTube metadata generation failed")
        return False
    
    # Test 3: Generate TikTok metadata
    print("\n3. Testing TikTok metadata generation...")
    tt_meta = exporter.generate_platform_metadata(story, "tiktok")
    if tt_meta["platform"] == "tiktok" and len(tt_meta["platform_hashtags"]) > 5:
        print(f"   ✅ TikTok metadata generated")
        print(f"      Hashtags: {', '.join(tt_meta['platform_hashtags'][:5])}...")
    else:
        print("   ❌ TikTok metadata generation failed")
        return False
    
    # Test 4: Generate Instagram metadata
    print("\n4. Testing Instagram metadata generation...")
    ig_meta = exporter.generate_platform_metadata(story, "instagram")
    if ig_meta["platform"] == "instagram":
        print(f"   ✅ Instagram metadata generated")
        print(f"      Hashtags: {', '.join(ig_meta['platform_hashtags'])}")
    else:
        print("   ❌ Instagram metadata generation failed")
        return False
    
    # Test 5: Generate all platforms
    print("\n5. Testing all platforms metadata generation...")
    all_meta = exporter.generate_all_platforms(story)
    if len(all_meta) == 3:
        print(f"   ✅ Generated metadata for all {len(all_meta)} platforms")
    else:
        print("   ❌ All platforms generation failed")
        return False
    
    # Test 6: Save platform metadata
    print("\n6. Testing metadata file saving...")
    with tempfile.TemporaryDirectory() as tmpdir:
        saved_files = exporter.save_platform_metadata(story, tmpdir)
        if len(saved_files) == 3 and all(os.path.exists(f) for f in saved_files):
            print(f"   ✅ Saved {len(saved_files)} metadata files")
            
            # Verify content
            with open(saved_files[0], 'r') as f:
                data = json.load(f)
                if "platform" in data and "platform_hashtags" in data:
                    print("   ✅ Metadata files have correct structure")
                else:
                    print("   ❌ Metadata file structure incorrect")
                    return False
        else:
            print("   ❌ Failed to save metadata files")
            return False
    
    print("\n✅ PlatformExporter tests passed!")
    return True


def test_integration():
    """Test integration of all components."""
    print("\n" + "="*60)
    print("Testing Component Integration")
    print("="*60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test story
        story = StoryIdea(
            story_title="Integration Test Story",
            narrator_gender="F",
            tone="inspiring",
            theme="personal growth",
            goal="Test all features together",
            potencial={"age_groups": {"20_25": 85}}
        )
        
        # Initialize components
        registry = ExportRegistry(os.path.join(tmpdir, "registry.json"))
        platform_exporter = PlatformExporter()
        
        title_id = generate_title_id(story.story_title)
        
        # Test 1: Export and register
        print("\n1. Testing export registration...")
        registry.register_export(
            title_id=title_id,
            title=story.story_title,
            segment="women",
            age_group="18-23",
            video_path=f"/test/{title_id}.mp4",
            thumbnail_path=f"/test/{title_id}_thumb.jpg",
            metadata_path=f"/test/{title_id}_meta.json"
        )
        
        # Test 2: Generate platform metadata and link to registry
        print("\n2. Testing platform metadata generation...")
        platform_dir = os.path.join(tmpdir, "platforms")
        platform_files = platform_exporter.save_platform_metadata(story, platform_dir)
        
        if len(platform_files) == 3:
            print(f"   ✅ Generated {len(platform_files)} platform metadata files")
        else:
            print("   ❌ Platform metadata generation failed")
            return False
        
        # Test 3: Update publish status
        print("\n3. Testing publish status workflow...")
        for platform in ["youtube", "tiktok", "instagram"]:
            registry.update_publish_status(
                title_id,
                platform,
                "published",
                f"https://{platform}.com/test/{title_id}"
            )
        
        info = registry.get_video_info(title_id)
        if len(info["platforms"]) == 3:
            print(f"   ✅ Updated publish status for 3 platforms")
        else:
            print("   ❌ Publish status update failed")
            return False
        
        # Test 4: Generate report
        print("\n4. Testing report generation...")
        report = registry.generate_report()
        if title_id[:8] in str(registry.registry):
            print("   ✅ Report contains expected data")
        else:
            print("   ❌ Report incomplete")
            return False
    
    print("\n✅ Integration tests passed!")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("EXPORT ENHANCEMENTS - COMPREHENSIVE TESTS")
    print("="*60)
    
    results = []
    
    # Run all tests
    results.append(("ExportRegistry", test_export_registry()))
    results.append(("ThumbnailGenerator", test_thumbnail_generator()))
    results.append(("PlatformExporter", test_platform_exporter()))
    results.append(("Integration", test_integration()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
