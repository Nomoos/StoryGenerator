#!/usr/bin/env python3
"""
Example: Using the Export Registry System to track and manage exported videos.
"""

import os
import sys

# Add src/Python directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'Python'))

from Tools.ExportRegistry import ExportRegistry
from Tools.Utils import FINAL_PATH


def example_basic_usage():
    """Basic registry usage example."""
    print("\n" + "="*60)
    print("Example 1: Basic Registry Usage")
    print("="*60 + "\n")
    
    # Initialize registry
    registry = ExportRegistry()
    
    # Register a new export
    registry.register_export(
        title_id="abc12345",
        title="My Amazing Story",
        segment="women",
        age_group="18-23",
        video_path=f"{FINAL_PATH}/women/18-23/abc12345.mp4",
        thumbnail_path=f"{FINAL_PATH}/women/18-23/abc12345_thumbnail.jpg",
        metadata_path=f"{FINAL_PATH}/women/18-23/abc12345_metadata.json",
        additional_info={
            "theme": "adventure",
            "tone": "exciting"
        }
    )
    
    print("\n📋 Video registered in export registry!")


def example_update_status():
    """Update publish status example."""
    print("\n" + "="*60)
    print("Example 2: Update Publish Status")
    print("="*60 + "\n")
    
    registry = ExportRegistry()
    
    # Update status for YouTube
    registry.update_publish_status(
        title_id="abc12345",
        platform="youtube",
        status="published",
        url="https://youtube.com/shorts/xyz123"
    )
    
    print("✅ Updated YouTube publish status")
    
    # Update status for TikTok
    registry.update_publish_status(
        title_id="abc12345",
        platform="tiktok",
        status="published",
        url="https://tiktok.com/@user/video/456789"
    )
    
    print("✅ Updated TikTok publish status")


def example_track_performance():
    """Track video performance example."""
    print("\n" + "="*60)
    print("Example 3: Track Performance Metrics")
    print("="*60 + "\n")
    
    registry = ExportRegistry()
    
    # Update performance metrics
    registry.update_performance(
        title_id="abc12345",
        views=50000,
        likes=2500,
        shares=150,
        comments=300
    )
    
    print("📊 Performance metrics updated!")
    
    # Get video info
    info = registry.get_video_info("abc12345")
    if info:
        perf = info["performance"]
        print(f"\nCurrent Performance:")
        print(f"  Views: {perf['views']:,}")
        print(f"  Likes: {perf['likes']:,}")
        print(f"  Engagement Rate: {perf['engagement_rate']}%")


def example_generate_report():
    """Generate registry report example."""
    print("\n" + "="*60)
    print("Example 4: Generate Registry Report")
    print("="*60 + "\n")
    
    registry = ExportRegistry()
    
    # Generate and display report
    report = registry.generate_report()
    print(report)
    
    # Save report to file
    report_path = os.path.join(FINAL_PATH, "export_report.txt")
    registry.generate_report(report_path)
    print(f"\n📄 Report saved to: {report_path}")


def example_filter_videos():
    """Filter videos example."""
    print("\n" + "="*60)
    print("Example 5: Filter and List Videos")
    print("="*60 + "\n")
    
    registry = ExportRegistry()
    
    # List all videos for women 18-23
    videos = registry.list_videos(segment="women", age_group="18-23")
    print(f"Found {len(videos)} videos for women 18-23")
    
    # List only exported (not published) videos
    exported_only = registry.list_videos(publish_status="exported")
    print(f"Found {len(exported_only)} videos waiting to be published")
    
    # List published videos
    published = registry.list_videos(publish_status="published")
    print(f"Found {len(published)} published videos")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("EXPORT REGISTRY - USAGE EXAMPLES")
    print("="*60)
    
    # Note: These examples assume you have already exported some videos
    print("\n⚠️  Note: These examples work best after you've exported some videos.")
    print("    Run the video pipeline first, then use these examples to manage exports.\n")
    
    try:
        example_basic_usage()
        example_update_status()
        example_track_performance()
        example_generate_report()
        example_filter_videos()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have exported at least one video first.\n")


if __name__ == "__main__":
    main()
