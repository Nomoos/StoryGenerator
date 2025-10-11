"""
Example: Instagram Reels Upload and Analytics

This script demonstrates how to upload a Reel to Instagram and retrieve analytics.
Requires Instagram Professional account linked to Facebook Business.

Setup:
1. Create Facebook Business account
2. Link Instagram Professional account (Business or Creator)
3. Create Facebook app and get access token with required scopes:
   - instagram_basic
   - instagram_content_publish
   - pages_read_engagement
4. Get your Instagram Business account ID
5. Set INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_USER_ID environment variables
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from providers import InstagramUploader, InstagramAnalytics
from PrismQ.Shared.interfaces.platform_provider import VideoMetadata


def upload_reel_example():
    """Example of uploading a Reel to Instagram."""
    print("=== Instagram Reels Upload Example ===\n")
    
    # Get credentials from environment
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    user_id = os.getenv("INSTAGRAM_USER_ID")
    
    if not access_token:
        access_token = input("Enter your Instagram access token: ").strip()
    if not user_id:
        user_id = input("Enter your Instagram Business User ID: ").strip()
    
    # Initialize uploader
    uploader = InstagramUploader(
        access_token=access_token,
        instagram_user_id=user_id
    )
    
    # Authenticate
    print("Authenticating with Instagram...")
    if uploader.authenticate():
        print("✓ Authentication successful\n")
    else:
        print("✗ Authentication failed")
        return None
    
    # Prepare video metadata
    metadata = VideoMetadata(
        caption=(
            "Mind-blowing AI-generated story! 🤯\n"
            "What would you do in this situation?\n\n"
            "#reels #viral #story #ai #entertainment"
        ),
        hashtags=["reels", "viral", "story", "ai", "entertainment"],
    )
    
    # Note: Instagram requires video at public URL
    print("⚠️  Instagram requires video to be at a public URL.")
    print("   You need to upload your video to a hosting service first.\n")
    
    video_url = input("Enter public video URL (or press Enter to skip): ").strip()
    
    if not video_url:
        print("Skipping upload (no URL provided)")
        return None
    
    print(f"\nUploading Reel from: {video_url}")
    print("(This may take a few minutes...)\n")
    
    result = uploader.upload_video(video_url, metadata)
    
    if result.success:
        print(f"\n✓ Upload successful!")
        print(f"  Media ID: {result.video_id}")
        print(f"  URL: {result.url}")
        print(f"  Upload time: {result.upload_time}")
        return result.video_id
    else:
        print(f"\n✗ Upload failed: {result.error_message}")
        return None


def get_analytics_example(media_id=None):
    """Example of retrieving Instagram analytics."""
    print("\n=== Instagram Analytics Example ===\n")
    
    # Get credentials
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    user_id = os.getenv("INSTAGRAM_USER_ID")
    
    if not access_token:
        access_token = input("Enter your Instagram access token: ").strip()
    if not user_id:
        user_id = input("Enter your Instagram Business User ID: ").strip()
    
    if not media_id:
        media_id = input("Enter Instagram media ID: ").strip()
    
    # Initialize analytics
    analytics = InstagramAnalytics(
        access_token=access_token,
        instagram_user_id=user_id
    )
    
    # Authenticate
    print("Authenticating with Instagram...")
    if analytics.authenticate():
        print("✓ Authentication successful\n")
    else:
        print("✗ Authentication failed")
        return
    
    # Get Reel analytics
    print(f"Fetching analytics for media: {media_id}")
    reel_data = analytics.get_video_analytics(media_id)
    
    if reel_data:
        print("\n📊 Reel Performance:")
        print(f"  Plays: {reel_data.views:,}")
        print(f"  Likes: {reel_data.likes:,}")
        print(f"  Comments: {reel_data.comments:,}")
        print(f"  Shares: {reel_data.shares:,}")
        print(f"  Saves: {reel_data.saves:,}")
        print(f"  Reach: {reel_data.impressions:,}")
        print(f"  Engagement rate: {reel_data.engagement_rate:.2f}%")
    else:
        print("✗ No analytics data available")
    
    # Get account analytics
    print("\n📈 Account Stats (Last 30 Days):")
    account_stats = analytics.get_channel_analytics()
    
    if account_stats:
        print(f"  Impressions: {account_stats.get('impressions', 0):,}")
        print(f"  Reach: {account_stats.get('reach', 0):,}")
        print(f"  Follower count: {account_stats.get('follower_count', 0):,}")
        print(f"  Profile views: {account_stats.get('profile_views', 0):,}")


def main():
    """Main example runner."""
    print("\n" + "="*60)
    print("Instagram Integration Example")
    print("="*60 + "\n")
    
    print("⚠️  Note: Requires Instagram Professional account (Business/Creator)")
    print("   and Facebook Business integration.\n")
    
    # Check if we should upload or just get analytics
    mode = input("Choose mode:\n  1. Upload Reel\n  2. Get analytics\n  3. Both\n\nEnter choice (1-3): ").strip()
    
    media_id = None
    
    if mode in ["1", "3"]:
        media_id = upload_reel_example()
    
    if mode in ["2", "3"]:
        get_analytics_example(media_id)
    
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
