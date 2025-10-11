"""
Example: Facebook Video Upload and Analytics

This script demonstrates how to upload a video to Facebook and retrieve analytics.
Requires Facebook Page access token.

Setup:
1. Create Facebook Page
2. Create Facebook App and get Page access token
3. Set FACEBOOK_ACCESS_TOKEN and FACEBOOK_PAGE_ID environment variables
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PrismQ.Providers import FacebookUploader, FacebookAnalytics
from PrismQ.Shared.interfaces.platform_provider import VideoMetadata, PrivacyStatus


def upload_video_example():
    """Example of uploading a video to Facebook."""
    print("=== Facebook Video Upload Example ===\n")
    
    # Get credentials from environment
    access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")
    
    if not access_token:
        access_token = input("Enter your Facebook Page access token: ").strip()
    if not page_id:
        page_id = input("Enter your Facebook Page ID: ").strip()
    
    # Initialize uploader
    uploader = FacebookUploader(
        access_token=access_token,
        page_id=page_id
    )
    
    # Authenticate
    print("Authenticating with Facebook...")
    if uploader.authenticate():
        print("✓ Authentication successful\n")
    else:
        print("✗ Authentication failed")
        return None
    
    # Prepare video metadata
    metadata = VideoMetadata(
        title="AI-Generated Story",
        description="An amazing story created with AI technology!",
        hashtags=["AI", "Story", "Video", "Entertainment"],
        privacy_status=PrivacyStatus.PUBLIC
    )
    
    # Choose upload method
    print("Facebook supports two upload methods:")
    print("  1. Local file upload")
    print("  2. Public URL upload")
    method = input("\nChoose method (1 or 2): ").strip()
    
    if method == "1":
        video_path = input("Enter path to video file: ").strip()
    else:
        video_path = input("Enter public video URL: ").strip()
    
    print(f"\nUploading video: {metadata.title}")
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
    """Example of retrieving Facebook analytics."""
    print("\n=== Facebook Analytics Example ===\n")
    
    # Get credentials
    access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")
    
    if not access_token:
        access_token = input("Enter your Facebook Page access token: ").strip()
    if not page_id:
        page_id = input("Enter your Facebook Page ID: ").strip()
    
    if not video_id:
        video_id = input("Enter Facebook video ID: ").strip()
    
    # Initialize analytics
    analytics = FacebookAnalytics(
        access_token=access_token,
        page_id=page_id
    )
    
    # Authenticate
    print("Authenticating with Facebook...")
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
        print(f"  Engagement rate: {video_data.engagement_rate:.2f}%")
    else:
        print("✗ No analytics data available")
    
    # Get page analytics
    print("\n📈 Page Stats:")
    page_stats = analytics.get_channel_analytics()
    
    if page_stats:
        print(f"  Fans: {page_stats.get('fan_count', 0):,}")
        print(f"  Followers: {page_stats.get('followers_count', 0):,}")


def main():
    """Main example runner."""
    print("\n" + "="*60)
    print("Facebook Integration Example")
    print("="*60 + "\n")
    
    print("⚠️  Note: Requires Facebook Page and access token.")
    print("   Get token from: https://developers.facebook.com/\n")
    
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
