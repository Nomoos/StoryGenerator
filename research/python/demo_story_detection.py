#!/usr/bin/env python3
"""
Demo script showing story video detection in action.
Creates sample outputs to demonstrate the feature without needing yt-dlp.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from youtube_channel_scraper import YouTubeChannelScraper, VideoMetadata


def create_sample_videos():
    """Create sample videos for demonstration."""
    return [
        # Story videos
        VideoMetadata(
            video_id="story1",
            title="My Crazy Story Time - AITA for Refusing to Pay?",
            description="This is my story about what happened last week. It's a true story about standing up for myself.",
            tags=["story", "aita", "reddit story", "personal story"],
            duration="8:45",
            duration_seconds=525,
            view_count=125000,
            like_count=8500,
            comment_count=432,
            upload_date="20241015",
            url="https://youtube.com/watch?v=story1",
            thumbnail_url="",
            subtitles_available=True,
            subtitle_text="I was sitting at home when my ex called me. I had no idea what was about to happen...",
            title_length=48,
            description_length=95,
            tag_count=4,
            has_chapters=False,
            video_format="short"
        ),
        VideoMetadata(
            video_id="story2",
            title="I Caught My Roommate Stealing - Revenge Story",
            description="You won't believe what happened when I found out my roommate was stealing from me.",
            tags=["revenge", "roommate drama", "story"],
            duration="5:30",
            duration_seconds=330,
            view_count=89000,
            like_count=6200,
            comment_count=318,
            upload_date="20241010",
            url="https://youtube.com/watch?v=story2",
            thumbnail_url="",
            subtitles_available=True,
            subtitle_text="My story begins three months ago when I got a new roommate...",
            title_length=46,
            description_length=82,
            tag_count=3,
            has_chapters=False,
            video_format="short"
        ),
        # Non-story videos
        VideoMetadata(
            video_id="tutorial1",
            title="How to Edit Videos in DaVinci Resolve - Complete Tutorial",
            description="Learn video editing with this comprehensive tutorial for beginners.",
            tags=["tutorial", "video editing", "davinci resolve", "how to"],
            duration="15:22",
            duration_seconds=922,
            view_count=45000,
            like_count=2100,
            comment_count=89,
            upload_date="20241012",
            url="https://youtube.com/watch?v=tutorial1",
            thumbnail_url="",
            subtitles_available=True,
            subtitle_text="In this tutorial, we'll learn how to edit videos...",
            title_length=58,
            description_length=65,
            tag_count=4,
            has_chapters=True,
            chapter_count=8,
            video_format="long"
        ),
        VideoMetadata(
            video_id="review1",
            title="iPhone 15 Pro Review - Is It Worth The Upgrade?",
            description="Complete review of the iPhone 15 Pro with pros and cons.",
            tags=["review", "iphone 15", "tech review", "unboxing"],
            duration="12:45",
            duration_seconds=765,
            view_count=234000,
            like_count=12300,
            comment_count=567,
            upload_date="20241008",
            url="https://youtube.com/watch?v=review1",
            thumbnail_url="",
            subtitles_available=False,
            subtitle_text=None,
            title_length=48,
            description_length=56,
            tag_count=4,
            has_chapters=True,
            chapter_count=6,
            video_format="long"
        ),
        VideoMetadata(
            video_id="vlog1",
            title="My Daily Vlog - Day 45 in Tokyo",
            description="Join me for another day exploring Tokyo! Today we visit Shibuya.",
            tags=["vlog", "daily vlog", "tokyo", "travel"],
            duration="18:30",
            duration_seconds=1110,
            view_count=67000,
            like_count=4500,
            comment_count=234,
            upload_date="20241014",
            url="https://youtube.com/watch?v=vlog1",
            thumbnail_url="",
            subtitles_available=False,
            subtitle_text=None,
            title_length=32,
            description_length=68,
            tag_count=4,
            has_chapters=False,
            video_format="long"
        ),
    ]


def demonstrate_detection():
    """Demonstrate story detection on sample videos."""
    print("\n" + "=" * 80)
    print("YouTube Channel Scraper - Story Video Detection Demo")
    print("=" * 80)
    
    scraper = YouTubeChannelScraper()
    videos = create_sample_videos()
    
    print("\nAnalyzing sample videos...\n")
    
    story_count = 0
    non_story_count = 0
    
    for i, video in enumerate(videos, 1):
        is_story, confidence, indicators = scraper.detect_story_video(video)
        
        if is_story:
            story_count += 1
            emoji = "📖"
            category = "STORY"
        else:
            non_story_count += 1
            emoji = "❌"
            category = "NON-STORY"
        
        print(f"{i}. {emoji} {category} (Confidence: {confidence:.2f})")
        print(f"   Title: \"{video.title}\"")
        print(f"   Format: {video.video_format.upper()}")
        print(f"   Views: {video.view_count:,} | Likes: {video.like_count:,}")
        
        if indicators:
            print(f"   Indicators: {', '.join(indicators[:3])}")
        
        print()
    
    print("=" * 80)
    print(f"Summary: {story_count} story videos, {non_story_count} non-story videos")
    print("=" * 80)
    
    # Demonstrate filtering
    print("\n" + "=" * 80)
    print("Story-Only Mode Demonstration")
    print("=" * 80)
    
    print("\nIf --story-only flag was used, only these videos would be included:\n")
    
    filtered_count = 0
    for video in videos:
        is_story, confidence, _ = scraper.detect_story_video(video)
        if is_story:
            print(f"✅ INCLUDED: \"{video.title}\" (confidence: {confidence:.2f})")
        else:
            filtered_count += 1
            print(f"⏭️  FILTERED: \"{video.title}\" (not a story)")
    
    print(f"\n{filtered_count} non-story videos would be filtered out")
    print("=" * 80)
    
    print("\n💡 Benefits of Story-Only Mode:")
    print("   • Focus analysis on story content only")
    print("   • More relevant insights for story generation pipeline")
    print("   • Cleaner data without non-story noise")
    print("   • Better pattern extraction from actual stories")
    print()


if __name__ == "__main__":
    demonstrate_detection()
