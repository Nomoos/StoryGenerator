"""
Example: TikTok Video Upload and Analytics

This script demonstrates how to upload a video to TikTok and retrieve analytics.
Requires TikTok Developer account and Content Posting API access.

Setup:
1. Register at https://developers.tiktok.com/
2. Create an app and request Content Posting API access
3. Get OAuth access token
4. Set TIKTOK_ACCESS_TOKEN environment variable or update this script
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from providers import TikTokUploader, TikTokAnalytics
from core.interfaces.platform_provider import VideoMetadata, PrivacyStatus


def upload_video_example():
    """Example of uploading a video to TikTok."""
    print("=== TikTok Video Upload Example ===\n")
    
    # Get access token from environment
    access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
    if not access_token:
        access_token = input("Enter your TikTok access token: ").strip()
    
    # Initialize uploader
    uploader = TikTokUploader(access_token=access_token)
    
    # Authenticate
    print("Authenticating with TikTok...")
    if uploader.authenticate():
        print("✓ Authentication successful\n")
    else:
        print("✗ Authentication failed")
        return None
    
    # Prepare video metadata
    # Note: This example uses engaging, attention-grabbing style common on TikTok.
    # Adjust tone and emoji usage based on your content strategy and audience.
    metadata = VideoMetadata(
        title="Epic AI Story",
        caption="You won't believe what happened next! 😱 This story is WILD!",
        hashtags=["fyp", "viral", "story", "storytime", "ai"],
        privacy_status=PrivacyStatus.PUBLIC
    )
    
    # Upload video
    video_path = "output/final_video.mp4"
    print(f"Uploading video: {video_path}")
    print("(This may take a few minutes...)\n")
    
    result = uploader.upload_video(video_path, metadata)
    
    if result.success:
        print(f"\n✓ Upload successful!")
        print(f"  Video ID: {result.video_id}")
        print(f"  URL: {result.url}")
        print(f"  Upload time: {result.upload_time}")
        return result.video_id
    else:
        print(f"\n✗ Upload failed: {result.error_message}")
        return None


def get_analytics_example(video_id=None):
    """Example of retrieving TikTok analytics."""
    print("\n=== TikTok Analytics Example ===\n")
    
    # Get access token
    access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
    if not access_token:
        access_token = input("Enter your TikTok access token: ").strip()
    
    if not video_id:
        video_id = input("Enter TikTok video ID: ").strip()
    
    # Initialize analytics
    analytics = TikTokAnalytics(access_token=access_token)
    
    # Authenticate
    print("Authenticating with TikTok...")
    if analytics.authenticate():
        print("✓ Authentication successful\n")
    else:
        print("✗ Authentication failed")
        return
    
    # Get video analytics
    print(f"Fetching analytics for video: {video_id}")
    video_data = analytics.get_video_analytics(video_id)
    
    if video_data:
        print("\n📊 Video Performance:")
        print(f"  Views: {video_data.views:,}")
        print(f"  Likes: {video_data.likes:,}")
        print(f"  Comments: {video_data.comments:,}")
        print(f"  Shares: {video_data.shares:,}")
        print(f"  Reach: {video_data.impressions:,}")
        print(f"  Engagement rate: {video_data.engagement_rate:.2f}%")
    else:
        print("✗ No analytics data available")
    
    # Get profile analytics
    print("\n📈 Profile Stats:")
    profile_stats = analytics.get_channel_analytics()
    
    if profile_stats:
        print(f"  Followers: {profile_stats.get('follower_count', 0):,}")
        print(f"  Following: {profile_stats.get('following_count', 0):,}")
        print(f"  Total videos: {profile_stats.get('video_count', 0):,}")
        print(f"  Total likes: {profile_stats.get('total_likes', 0):,}")


def main():
    """Main example runner."""
    print("\n" + "="*60)
    print("TikTok Integration Example")
    print("="*60 + "\n")
    
    print("⚠️  Note: TikTok Content Posting API requires approval.")
    print("   Apply at: https://developers.tiktok.com/\n")
    
    # Check if we should upload or just get analytics
    mode = input("Choose mode:\n  1. Upload video\n  2. Get analytics\n  3. Both\n\nEnter choice (1-3): ").strip()
    
    video_id = None
    
    if mode in ["1", "3"]:
        video_id = upload_video_example()
    
    if mode in ["2", "3"]:
        get_analytics_example(video_id)
    
    print("\n" + "="*60)
    print("Example completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExample cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
