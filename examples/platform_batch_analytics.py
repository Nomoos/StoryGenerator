"""
Example: Batch Analytics Collection

This script demonstrates how to collect analytics from multiple platforms
and save them to JSON files for analysis.

This is useful for:
- Regular analytics collection (e.g., daily cron job)
- Performance tracking over time
- Cross-platform comparison
- Data-driven content optimization
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from providers import (
    YouTubeAnalytics,
    TikTokAnalytics,
    InstagramAnalytics,
)
from core.interfaces.platform_provider import VideoAnalytics


# Configuration
OUTPUT_DIR = Path("data/analytics")
VIDEO_REGISTRY_FILE = Path("data/video_registry.json")


def load_video_registry() -> List[Dict]:
    """
    Load registry of uploaded videos.
    
    Expected format:
    [
        {
            "title_id": "story_123",
            "title": "Amazing Story",
            "platforms": {
                "youtube": "VIDEO_ID_HERE",
                "tiktok": "VIDEO_ID_HERE",
                "instagram": "MEDIA_ID_HERE"
            },
            "upload_date": "2025-10-10T12:00:00"
        },
        ...
    ]
    """
    if not VIDEO_REGISTRY_FILE.exists():
        print(f"⚠️  Video registry not found at: {VIDEO_REGISTRY_FILE}")
        print("   Create this file to track your uploaded videos.")
        return []
    
    with open(VIDEO_REGISTRY_FILE, "r") as f:
        return json.load(f)


def save_analytics(analytics: VideoAnalytics, platform: str, title_id: str) -> None:
    """Save analytics data to JSON file."""
    # Create platform directory
    platform_dir = OUTPUT_DIR / platform
    platform_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with date
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{title_id}_{date_str}.json"
    output_path = platform_dir / filename
    
    # Save data
    data = {
        "video_id": analytics.video_id,
        "title_id": analytics.title_id,
        "platform": analytics.platform.value,
        "collected_at": analytics.collected_at.isoformat(),
        "metrics": {
            "views": analytics.views,
            "likes": analytics.likes,
            "comments": analytics.comments,
            "shares": analytics.shares,
            "saves": analytics.saves,
            "watch_time_seconds": analytics.watch_time_seconds,
            "average_view_duration": analytics.average_view_duration,
            "completion_rate": analytics.completion_rate,
            "impressions": analytics.impressions,
            "ctr": analytics.ctr,
            "engagement_rate": analytics.engagement_rate,
        }
    }
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"  ✓ Saved to: {output_path}")


def collect_youtube_analytics(video_id: str, title_id: str) -> Optional[VideoAnalytics]:
    """Collect YouTube analytics."""
    try:
        analytics = YouTubeAnalytics(
            credentials_path="credentials/youtube_client_secret.json",
            token_path="credentials/youtube_token.json"
        )
        analytics.authenticate()
        
        data = analytics.get_video_analytics(video_id)
        if data:
            # Create a new instance with title_id set (preserves immutability)
            from dataclasses import replace
            data = replace(data, title_id=title_id)
            save_analytics(data, "youtube", title_id)
        return data
    except Exception as e:
        print(f"  ✗ YouTube error: {e}")
        return None


def collect_tiktok_analytics(video_id: str, title_id: str) -> Optional[VideoAnalytics]:
    """Collect TikTok analytics."""
    try:
        access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
        if not access_token:
            print("  ⚠️  TIKTOK_ACCESS_TOKEN not set, skipping")
            return None
        
        analytics = TikTokAnalytics(access_token=access_token)
        analytics.authenticate()
        
        data = analytics.get_video_analytics(video_id)
        if data:
            # Create a new instance with title_id set (preserves immutability)
            from dataclasses import replace
            data = replace(data, title_id=title_id)
            save_analytics(data, "tiktok", title_id)
        return data
    except Exception as e:
        print(f"  ✗ TikTok error: {e}")
        return None


def collect_instagram_analytics(media_id: str, title_id: str) -> Optional[VideoAnalytics]:
    """Collect Instagram analytics."""
    try:
        access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        user_id = os.getenv("INSTAGRAM_USER_ID")
        
        if not access_token or not user_id:
            print("  ⚠️  Instagram credentials not set, skipping")
            return None
        
        analytics = InstagramAnalytics(
            access_token=access_token,
            instagram_user_id=user_id
        )
        analytics.authenticate()
        
        data = analytics.get_video_analytics(media_id)
        if data:
            # Create a new instance with title_id set (preserves immutability)
            from dataclasses import replace
            data = replace(data, title_id=title_id)
            save_analytics(data, "instagram", title_id)
        return data
    except Exception as e:
        print(f"  ✗ Instagram error: {e}")
        return None


def collect_all_analytics() -> None:
    """Collect analytics for all videos in registry."""
    print("\n" + "="*60)
    print("Batch Analytics Collection")
    print("="*60 + "\n")
    
    # Load video registry
    videos = load_video_registry()
    if not videos:
        print("No videos to process.")
        return
    
    print(f"Found {len(videos)} videos in registry\n")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Collect analytics for each video
    total_collected = 0
    
    for i, video in enumerate(videos, 1):
        title_id = video.get("title_id", f"video_{i}")
        title = video.get("title", "Untitled")
        platforms = video.get("platforms", {})
        
        print(f"[{i}/{len(videos)}] {title} (ID: {title_id})")
        
        # YouTube
        if "youtube" in platforms:
            print("  YouTube...", end=" ")
            data = collect_youtube_analytics(platforms["youtube"], title_id)
            if data:
                print(f"Views: {data.views:,}, Engagement: {data.engagement_rate:.1f}%")
                total_collected += 1
            else:
                print("No data")
        
        # TikTok
        if "tiktok" in platforms:
            print("  TikTok...", end=" ")
            data = collect_tiktok_analytics(platforms["tiktok"], title_id)
            if data:
                print(f"Views: {data.views:,}, Engagement: {data.engagement_rate:.1f}%")
                total_collected += 1
            else:
                print("No data")
        
        # Instagram
        if "instagram" in platforms:
            print("  Instagram...", end=" ")
            data = collect_instagram_analytics(platforms["instagram"], title_id)
            if data:
                print(f"Plays: {data.views:,}, Engagement: {data.engagement_rate:.1f}%")
                total_collected += 1
            else:
                print("No data")
        
        print()  # Blank line between videos
    
    print("="*60)
    print(f"Collection complete! {total_collected} analytics collected.")
    print(f"Data saved to: {OUTPUT_DIR}")
    print("="*60 + "\n")


def create_sample_registry() -> None:
    """Create a sample video registry file."""
    print("Creating sample video registry...\n")
    
    sample_data = [
        {
            "title_id": "story_001",
            "title": "Amazing Adventure Story",
            "platforms": {
                "youtube": "YOUR_YOUTUBE_VIDEO_ID",
                "tiktok": "YOUR_TIKTOK_VIDEO_ID",
                "instagram": "YOUR_INSTAGRAM_MEDIA_ID"
            },
            "upload_date": "2025-10-01T12:00:00"
        },
        {
            "title_id": "story_002",
            "title": "Heartwarming Tale",
            "platforms": {
                "youtube": "YOUR_YOUTUBE_VIDEO_ID_2",
                "tiktok": "YOUR_TIKTOK_VIDEO_ID_2"
            },
            "upload_date": "2025-10-05T15:30:00"
        }
    ]
    
    VIDEO_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VIDEO_REGISTRY_FILE, "w") as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"✓ Sample registry created at: {VIDEO_REGISTRY_FILE}")
    print("  Edit this file with your actual video IDs.\n")


def main():
    """Main runner."""
    if not VIDEO_REGISTRY_FILE.exists():
        print(f"Video registry not found at: {VIDEO_REGISTRY_FILE}\n")
        create_sample = input("Create sample registry? (y/n): ").strip().lower()
        
        if create_sample == "y":
            create_sample_registry()
        else:
            print("\nPlease create a video registry file manually.")
            print("See the example format in this script's docstring.\n")
            return
    
    print("\n⚠️  Make sure you have configured your credentials:")
    print("  - YouTube: credentials/youtube_client_secret.json")
    print("  - TikTok: TIKTOK_ACCESS_TOKEN environment variable")
    print("  - Instagram: INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_USER_ID\n")
    
    proceed = input("Proceed with analytics collection? (y/n): ").strip().lower()
    
    if proceed == "y":
        collect_all_analytics()
    else:
        print("Collection cancelled.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCollection cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
