"""
Example: Database Integration and Cross-Platform Comparison

This script demonstrates:
1. Storing upload results and analytics in database
2. Cross-platform performance comparison
3. Generating optimization insights

This addresses the requirement to use database for text data storage
and enable cross-platform performance analysis.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.database import PlatformDatabase
from core.platform_comparison import PlatformComparator
from core.interfaces.platform_provider import (
    PlatformType,
    UploadResult,
    VideoAnalytics,
)


def demo_database_storage():
    """Demonstrate storing upload results and analytics in database."""
    print("\n" + "="*70)
    print("Database Integration Demo")
    print("="*70 + "\n")
    
    # Initialize database
    db = PlatformDatabase("data/platform_analytics.db")
    db.initialize()
    print("✓ Database initialized\n")
    
    # Simulate upload results for a video across multiple platforms
    title_id = "story_demo_001"
    title = "Amazing AI Story - Cross Platform Test"
    description = "This is a test video uploaded across multiple platforms"
    
    print(f"Storing upload results for: {title}\n")
    
    # YouTube upload
    youtube_result = UploadResult(
        success=True,
        platform=PlatformType.YOUTUBE,
        video_id="YT_VIDEO_123",
        url="https://youtube.com/watch?v=YT_VIDEO_123",
        upload_time=datetime.now() - timedelta(days=1),
    )
    
    db.save_upload_result(
        youtube_result,
        title_id=title_id,
        title=title,
        description=description,
        privacy_status="public",
        tags=["ai", "story", "shorts"],
        hashtags=["Shorts", "AI", "Viral"],
    )
    print(f"✓ Saved YouTube upload: {youtube_result.video_id}")
    
    # TikTok upload
    tiktok_result = UploadResult(
        success=True,
        platform=PlatformType.TIKTOK,
        video_id="TT_VIDEO_456",
        url="https://tiktok.com/@user/video/TT_VIDEO_456",
        upload_time=datetime.now() - timedelta(days=1),
    )
    
    db.save_upload_result(
        tiktok_result,
        title_id=title_id,
        title=title,
        description=description,
        hashtags=["fyp", "ai", "story"],
    )
    print(f"✓ Saved TikTok upload: {tiktok_result.video_id}")
    
    # Instagram upload
    instagram_result = UploadResult(
        success=True,
        platform=PlatformType.INSTAGRAM,
        video_id="IG_MEDIA_789",
        url="https://instagram.com/reel/IG_MEDIA_789",
        upload_time=datetime.now() - timedelta(days=1),
    )
    
    db.save_upload_result(
        instagram_result,
        title_id=title_id,
        title=title,
        description=description,
        hashtags=["reels", "ai", "viral"],
    )
    print(f"✓ Saved Instagram upload: {instagram_result.video_id}")
    
    # Facebook upload
    facebook_result = UploadResult(
        success=True,
        platform=PlatformType.FACEBOOK,
        video_id="FB_VIDEO_101",
        url="https://facebook.com/page/videos/FB_VIDEO_101",
        upload_time=datetime.now() - timedelta(days=1),
    )
    
    db.save_upload_result(
        facebook_result,
        title_id=title_id,
        title=title,
        description=description,
        hashtags=["AI", "Story", "Video"],
    )
    print(f"✓ Saved Facebook upload: {facebook_result.video_id}\n")
    
    # Simulate analytics data collection
    print("Storing analytics data...\n")
    
    # YouTube analytics (good performance)
    youtube_analytics = VideoAnalytics(
        platform=PlatformType.YOUTUBE,
        video_id="YT_VIDEO_123",
        title_id=title_id,
        collected_at=datetime.now(),
        views=15000,
        likes=850,
        comments=125,
        shares=45,
        watch_time_seconds=6000,
        average_view_duration=35.5,
        engagement_rate=6.8,
    )
    db.save_analytics(youtube_analytics)
    print(f"✓ Saved YouTube analytics: {youtube_analytics.views:,} views")
    
    # TikTok analytics (excellent viral performance)
    tiktok_analytics = VideoAnalytics(
        platform=PlatformType.TIKTOK,
        video_id="TT_VIDEO_456",
        title_id=title_id,
        collected_at=datetime.now(),
        views=50000,
        likes=4500,
        comments=380,
        shares=250,
        engagement_rate=10.3,
    )
    db.save_analytics(tiktok_analytics)
    print(f"✓ Saved TikTok analytics: {tiktok_analytics.views:,} views")
    
    # Instagram analytics (moderate performance)
    instagram_analytics = VideoAnalytics(
        platform=PlatformType.INSTAGRAM,
        video_id="IG_MEDIA_789",
        title_id=title_id,
        collected_at=datetime.now(),
        views=8500,
        likes=420,
        comments=55,
        shares=25,
        saves=85,
        engagement_rate=6.9,
    )
    db.save_analytics(instagram_analytics)
    print(f"✓ Saved Instagram analytics: {instagram_analytics.views:,} views")
    
    # Facebook analytics (good performance)
    facebook_analytics = VideoAnalytics(
        platform=PlatformType.FACEBOOK,
        video_id="FB_VIDEO_101",
        title_id=title_id,
        collected_at=datetime.now(),
        views=12000,
        likes=680,
        comments=95,
        shares=55,
        engagement_rate=6.9,
    )
    db.save_analytics(facebook_analytics)
    print(f"✓ Saved Facebook analytics: {facebook_analytics.views:,} views\n")
    
    db.close()
    return title_id


def demo_cross_platform_comparison(title_id):
    """Demonstrate cross-platform performance comparison."""
    print("\n" + "="*70)
    print("Cross-Platform Performance Comparison")
    print("="*70 + "\n")
    
    # Initialize comparator
    comparator = PlatformComparator("data/platform_analytics.db")
    
    # Get comparison
    comparison = comparator.compare_video(title_id)
    
    if not comparison:
        print("✗ No comparison data found")
        return
    
    print(f"Video: {comparison.title}")
    print(f"Title ID: {comparison.title_id}\n")
    
    print("📊 Performance Summary:")
    print(f"  Total Views: {comparison.total_views:,}")
    print(f"  Total Engagement: {comparison.total_engagement:,}")
    print(f"  Average Engagement Rate: {comparison.average_engagement_rate:.2f}%\n")
    
    print("📈 Platform Breakdown:\n")
    for perf in sorted(comparison.platforms, key=lambda p: p.views, reverse=True):
        print(f"  {perf.platform.upper()}")
        print(f"    Views: {perf.views:,}")
        print(f"    Likes: {perf.likes:,}")
        print(f"    Comments: {perf.comments:,}")
        print(f"    Shares: {perf.shares:,}")
        print(f"    Engagement Rate: {perf.engagement_rate:.2f}%")
        print(f"    Virality Score: {perf.virality_score:.2f}")
        print(f"    URL: {perf.url}\n")
    
    # Get rankings by different metrics
    print("🏆 Platform Rankings:\n")
    
    print("  By Views:")
    for rank, (platform, value) in enumerate(comparison.get_platform_ranking("views"), 1):
        print(f"    {rank}. {platform}: {int(value):,} views")
    
    print("\n  By Engagement Rate:")
    for rank, (platform, value) in enumerate(comparison.get_platform_ranking("engagement_rate"), 1):
        print(f"    {rank}. {platform}: {value:.2f}%")
    
    print("\n  By Virality Score:")
    for rank, (platform, value) in enumerate(comparison.get_platform_ranking("virality_score"), 1):
        print(f"    {rank}. {platform}: {value:.2f}")
    
    comparator.close()


def demo_optimization_insights(title_id):
    """Demonstrate generating optimization insights."""
    print("\n" + "="*70)
    print("Optimization Insights & Recommendations")
    print("="*70 + "\n")
    
    # Initialize comparator
    comparator = PlatformComparator("data/platform_analytics.db")
    
    # Generate insights
    insights = comparator.generate_insights(title_id)
    
    if "error" in insights:
        print(f"✗ {insights['error']}")
        return
    
    print(f"Video: {insights['title']}\n")
    
    print("📊 Summary:")
    summary = insights["summary"]
    print(f"  Total Views: {summary['total_views']:,}")
    print(f"  Total Engagement: {summary['total_engagement']:,}")
    print(f"  Average Engagement Rate: {summary['average_engagement_rate']:.2f}%")
    print(f"  Platforms: {summary['platforms_count']}\n")
    
    print("🎯 Best Performers:")
    best = insights["best_performers"]
    print(f"  Most Views: {best.get('views', 'N/A')}")
    print(f"  Best Engagement: {best.get('engagement_rate', 'N/A')}")
    print(f"  Most Viral: {best.get('virality_score', 'N/A')}\n")
    
    print("💡 Recommendations:")
    for i, rec in enumerate(insights["recommendations"], 1):
        print(f"  {i}. {rec}")
    
    comparator.close()


def demo_platform_trends():
    """Demonstrate platform trend analysis."""
    print("\n" + "="*70)
    print("Platform Trends Analysis")
    print("="*70 + "\n")
    
    comparator = PlatformComparator("data/platform_analytics.db")
    
    platforms = ["youtube", "tiktok", "instagram", "facebook"]
    
    for platform in platforms:
        trends = comparator.get_platform_trends(platform, limit=10)
        
        if "error" not in trends:
            print(f"{platform.upper()}:")
            print(f"  Videos: {trends['video_count']}")
            print(f"  Avg Views: {trends['average_views']:,}")
            print(f"  Avg Engagement: {trends['average_engagement']:,}")
            print(f"  Total Views: {trends['total_views']:,}\n")
    
    # Overall comparison
    print("📊 Overall Platform Comparison:")
    overall = comparator.compare_all_platforms()
    print(f"  Total Videos: {overall['total_videos']}")
    print(f"  Total Views: {overall['total_views']:,}\n")
    
    for platform, summary in overall["platform_summaries"].items():
        print(f"  {platform.upper()}:")
        print(f"    Videos: {summary.get('total_videos', 0)}")
        print(f"    Views: {summary.get('total_views', 0):,}")
        print(f"    Avg Engagement: {summary.get('avg_engagement_rate', 0):.2f}%\n")
    
    comparator.close()


def main():
    """Main demo runner."""
    print("\n" + "="*70)
    print("PLATFORM INTEGRATION: DATABASE & CROSS-PLATFORM COMPARISON DEMO")
    print("="*70)
    
    # Demo 1: Store data in database
    title_id = demo_database_storage()
    
    # Demo 2: Cross-platform comparison
    demo_cross_platform_comparison(title_id)
    
    # Demo 3: Optimization insights
    demo_optimization_insights(title_id)
    
    # Demo 4: Platform trends
    demo_platform_trends()
    
    print("\n" + "="*70)
    print("Demo completed!")
    print("="*70)
    print("\nDatabase file: data/platform_analytics.db")
    print("All text data (titles, descriptions, metrics) stored in SQLite database")
    print("Media files (videos, thumbnails) should be stored in file system\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
