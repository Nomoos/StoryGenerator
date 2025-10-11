"""
Example: YouTube Video Upload and Analytics

This script demonstrates how to upload a video to YouTube and retrieve analytics.
Requires OAuth 2.0 credentials from Google Cloud Console.

Setup:
1. Create a project in Google Cloud Console
2. Enable YouTube Data API v3 and YouTube Analytics API
3. Create OAuth 2.0 credentials (Desktop application)
4. Download credentials JSON as 'credentials/youtube_client_secret.json'
5. Install dependencies: pip install google-auth google-auth-oauthlib google-api-python-client
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from providers import YouTubeUploader, YouTubeAnalytics
from PrismQ.Shared.interfaces.platform_provider import VideoMetadata, PrivacyStatus


def upload_video_example():
    """Example of uploading a video to YouTube."""
    print("=== YouTube Video Upload Example ===\n")
    
    # Initialize uploader
    uploader = YouTubeUploader(
        credentials_path="credentials/youtube_client_secret.json",
        token_path="credentials/youtube_token.json"
    )
    
    # Authenticate (will open browser on first run)
    print("Authenticating with YouTube...")
    uploader.authenticate()
    print("✓ Authentication successful\n")
    
    # Prepare video metadata
    metadata = VideoMetadata(
        title="Amazing AI-Generated Story - #Shorts",
        description=(
            "An incredible AI-generated story that will keep you on the edge of your seat!\n\n"
            "This short-form video was created using our StoryGenerator pipeline.\n\n"
            # Note: Hashtags in description are treated differently from tags.
            # Description hashtags appear as clickable links; tags are for search/categorization.
            "#Shorts #AI #Story #Storytelling #Viral"
        ),
        tags=["shorts", "ai", "story", "viral", "entertainment", "storytelling"],
        category_id="22",  # People & Blogs
        privacy_status=PrivacyStatus.PUBLIC,
        made_for_kids=False,
        thumbnail_path="output/thumbnail.jpg"  # Optional custom thumbnail
    )
    
    # Upload video
    video_path = "output/final_video.mp4"
    print(f"Uploading video: {video_path}")
    
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
    """Example of retrieving YouTube analytics."""
    print("\n=== YouTube Analytics Example ===\n")
    
    if not video_id:
        video_id = input("Enter YouTube video ID: ").strip()
    
    # Initialize analytics
    analytics = YouTubeAnalytics(
        credentials_path="credentials/youtube_client_secret.json",
        token_path="credentials/youtube_token.json"
    )
    
    # Authenticate
    print("Authenticating with YouTube Analytics...")
    analytics.authenticate()
    print("✓ Authentication successful\n")
    
    # Get video analytics (last 7 days)
    print(f"Fetching analytics for video: {video_id}")
    video_data = analytics.get_video_analytics(
        video_id=video_id,
        start_date=datetime.now() - timedelta(days=7),
        end_date=datetime.now()
    )
    
    if video_data:
        print("\n📊 Video Performance (Last 7 Days):")
        print(f"  Views: {video_data.views:,}")
        print(f"  Likes: {video_data.likes:,}")
        print(f"  Comments: {video_data.comments:,}")
        print(f"  Shares: {video_data.shares:,}")
        print(f"  Watch time: {video_data.watch_time_seconds / 60:.1f} minutes")
        print(f"  Avg view duration: {video_data.average_view_duration:.1f} seconds")
        print(f"  Engagement rate: {video_data.engagement_rate:.2f}%")
    else:
        print("✗ No analytics data available (video may be too new)")
    
    # Get channel analytics
    print("\n📈 Channel Performance (Last 30 Days):")
    channel_stats = analytics.get_channel_analytics(
        start_date=datetime.now() - timedelta(days=30)
    )
    
    if channel_stats:
        print(f"  Total views: {channel_stats.get('views', 0):,}")
        print(f"  Total likes: {channel_stats.get('likes', 0):,}")
        print(f"  Subscribers gained: {channel_stats.get('subscribers_gained', 0):,}")
        print(f"  Subscribers lost: {channel_stats.get('subscribers_lost', 0):,}")
        print(f"  Watch time: {channel_stats.get('watch_time_minutes', 0):.1f} minutes")


def main():
    """Main example runner."""
    print("\n" + "="*60)
    print("YouTube Integration Example")
    print("="*60 + "\n")
    
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
