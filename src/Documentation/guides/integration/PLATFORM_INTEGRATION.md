# Platform Integration Guide (Milestone 6 + Updates)

This guide covers the implementation of platform integration for YouTube, TikTok, Instagram, and Facebook, including video uploads, analytics collection, database storage, and cross-platform performance comparison.

## Overview

The platform integration module provides:
- **Video Upload**: Automated video publishing to YouTube, TikTok, Instagram, and **Facebook**
- **Analytics Collection**: Performance metrics retrieval from platform APIs
- **Database Storage**: SQLite-based storage for all text data and analytics
- **Cross-Platform Comparison**: Performance analysis and optimization insights
- **Error Handling**: Robust retry logic and error recovery
- **OAuth Support**: Secure authentication for all platforms

## Architecture

### Components

```
PrismQ/Providers/
├── youtube_provider.py     # YouTube Data API v3 & Analytics
├── tiktok_provider.py      # TikTok Content Posting API
├── instagram_provider.py   # Instagram Graph API
├── facebook_provider.py    # Facebook Graph API (NEW)
└── __init__.py            # Provider exports

core/
├── interfaces/
│   └── platform_provider.py    # Provider interfaces
├── database.py                 # SQLite database for text data (NEW)
└── platform_comparison.py      # Cross-platform analysis (NEW)

examples/
├── platform_youtube_example.py
├── platform_tiktok_example.py
├── platform_instagram_example.py
├── platform_facebook_example.py          # NEW
├── platform_batch_analytics.py
└── platform_database_comparison.py       # NEW
```

### Data Storage Strategy

**Text Data → Database (SQLite)**:
- Video titles and descriptions
- Tags and hashtags
- Analytics metrics (views, likes, engagement rates)
- Upload metadata and timestamps

**Media Files → File System**:
- Video files (MP4, etc.)
- Thumbnail images (JPG, PNG)
- Stored in organized directory structure

### Interfaces

All platform providers implement standard interfaces:

- **IPlatformUploader**: Video upload capabilities
- **IPlatformAnalytics**: Metrics retrieval capabilities

## Platform-Specific Implementation

### YouTube Integration

#### Setup


1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable YouTube Data API v3 and YouTube Analytics API

2. **OAuth 2.0 Credentials**:
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the JSON file as `credentials/youtube_client_secret.json`
   - Add scopes:
     - `https://www.googleapis.com/auth/youtube.upload`
     - `https://www.googleapis.com/auth/youtube.readonly`
     - `https://www.googleapis.com/auth/yt-analytics.readonly`

3. **Install Dependencies**:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

#### Usage

**Upload a Video:**

```python
from PrismQ.Providers import YouTubeUploader
from core.interfaces.platform_provider import VideoMetadata, PrivacyStatus

# Initialize uploader
uploader = YouTubeUploader(
    credentials_path="credentials/youtube_client_secret.json",
    token_path="credentials/youtube_token.json"
)

# Authenticate (opens browser for OAuth flow on first run)
uploader.authenticate()

# Prepare metadata
metadata = VideoMetadata(
    title="Amazing Story - #Shorts",
    description="An incredible story that will blow your mind!\\n\\n#Shorts #Viral #Storytelling",
    tags=["shorts", "story", "viral", "entertainment"],
    category_id="22",  # People & Blogs
    privacy_status=PrivacyStatus.PUBLIC,
    made_for_kids=False,
    thumbnail_path="output/thumbnail.jpg"
)

# Upload video
result = uploader.upload_video("output/final_video.mp4", metadata)

if result.success:
    print(f"Video uploaded: {result.url}")
    print(f"Video ID: {result.video_id}")
else:
    print(f"Upload failed: {result.error_message}")
```

**Retrieve Analytics:**

```python
from PrismQ.Providers import YouTubeAnalytics
from datetime import datetime, timedelta

# Initialize analytics
analytics = YouTubeAnalytics(
    credentials_path="credentials/youtube_client_secret.json",
    token_path="credentials/youtube_token.json"
)

# Authenticate
analytics.authenticate()

# Get video analytics (last 7 days)
video_data = analytics.get_video_analytics(
    video_id="VIDEO_ID_HERE",
    start_date=datetime.now() - timedelta(days=7),
    end_date=datetime.now()
)

if video_data:
    print(f"Views: {video_data.views}")
    print(f"Likes: {video_data.likes}")
    print(f"Comments: {video_data.comments}")
    print(f"Watch time: {video_data.watch_time_seconds / 60:.1f} minutes")
    print(f"Engagement rate: {video_data.engagement_rate:.2f}%")

# Get channel analytics
channel_stats = analytics.get_channel_analytics(
    start_date=datetime.now() - timedelta(days=30)
)
print(f"Total views: {channel_stats['views']}")
print(f"Subscribers gained: {channel_stats['subscribers_gained']}")
```

#### Best Practices

1. **SEO Optimization**:
   - Use keyword-rich titles (60 characters max)
   - Write detailed descriptions with timestamps
   - Include relevant hashtags (#Shorts is required for Shorts)
   - Add target keywords in first 150 characters

2. **Quota Management**:
   - Daily quota: 10,000 units
   - Upload cost: 1,600 units per video
   - Plan uploads accordingly (max ~6 videos/day)

3. **Video Requirements**:
   - Format: MP4 (H.264 video, AAC audio)
   - Resolution: 1080x1920 (9:16 for Shorts)
   - Duration: Up to 60 seconds for Shorts
   - File size: Up to 256GB

### TikTok Integration

#### Setup

1. **Register TikTok Developer Account**:
   - Go to [TikTok for Developers](https://developers.tiktok.com/)
   - Create an app and request Content Posting API access
   - Get app credentials and OAuth token

2. **Environment Variables**:
   ```bash
   export TIKTOK_ACCESS_TOKEN="your_access_token_here"
   ```

#### Usage

**Upload a Video:**

```python
from PrismQ.Providers import TikTokUploader
from core.interfaces.platform_provider import VideoMetadata, PrivacyStatus

# Initialize uploader
uploader = TikTokUploader(access_token="YOUR_ACCESS_TOKEN")

# Prepare metadata with hashtags
metadata = VideoMetadata(
    title="Epic Story Time",
    caption="You won't believe what happened next! 😱",
    hashtags=["fyp", "viral", "story", "storytime"],
    privacy_status=PrivacyStatus.PUBLIC
)

# Upload video
result = uploader.upload_video("output/final_video.mp4", metadata)

if result.success:
    print(f"Video published: {result.url}")
    print(f"Publish ID: {result.video_id}")
else:
    print(f"Upload failed: {result.error_message}")
```

**Retrieve Analytics:**

```python
from PrismQ.Providers import TikTokAnalytics

# Initialize analytics
analytics = TikTokAnalytics(access_token="YOUR_ACCESS_TOKEN")

# Get video analytics
video_data = analytics.get_video_analytics("VIDEO_ID")

if video_data:
    print(f"Views: {video_data.views}")
    print(f"Likes: {video_data.likes}")
    print(f"Shares: {video_data.shares}")
    print(f"Engagement rate: {video_data.engagement_rate:.2f}%")

# Get profile analytics
profile_stats = analytics.get_channel_analytics()
print(f"Followers: {profile_stats['follower_count']}")
print(f"Total videos: {profile_stats['video_count']}")
```

#### Best Practices

1. **Content Optimization**:
   - Use natural language with relevant keywords in captions
   - Include 3-5 trending hashtags (mix of trending + niche)
   - Add text overlays for better accessibility
   - Strong hook in first 3 seconds

2. **Video Requirements**:
   - Format: MP4 or WebM
   - Resolution: 1080x1920 (9:16 preferred)
   - Duration: 15-60 seconds
   - File size: Up to 287MB

3. **Algorithm Tips**:
   - Post during peak hours (6-10 PM user timezone)
   - High completion rate is critical
   - Early engagement signals (first hour) matter most

### Instagram Integration

#### Setup

1. **Facebook Business Account**:
   - Create Facebook Business account
   - Link Instagram Professional account (Business or Creator)
   - Create Facebook app and get access token

2. **Graph API Setup**:
   - Enable Instagram Graph API permissions
   - Get access token with required scopes:
     - `instagram_basic`
     - `instagram_content_publish`
     - `pages_read_engagement`

3. **Environment Variables**:
   ```bash
   export INSTAGRAM_ACCESS_TOKEN="your_access_token_here"
   export INSTAGRAM_USER_ID="your_instagram_business_id"
   ```

#### Usage

**Upload a Reel:**

```python
from PrismQ.Providers import InstagramUploader
from core.interfaces.platform_provider import VideoMetadata

# Initialize uploader
uploader = InstagramUploader(
    access_token="YOUR_ACCESS_TOKEN",
    instagram_user_id="YOUR_INSTAGRAM_USER_ID"
)

# Prepare metadata
metadata = VideoMetadata(
    caption="Mind-blowing story! What would you do? 🤔\\n\\n#reels #viral #story",
    hashtags=["reels", "viral", "story", "entertainment"],
)

# Upload video (must be at public URL)
# Note: Upload video to hosting first, then use URL
result = uploader.upload_video("https://example.com/video.mp4", metadata)

if result.success:
    print(f"Reel published: {result.url}")
    print(f"Media ID: {result.video_id}")
else:
    print(f"Upload failed: {result.error_message}")
```

**Retrieve Analytics:**

```python
from PrismQ.Providers import InstagramAnalytics

# Initialize analytics
analytics = InstagramAnalytics(
    access_token="YOUR_ACCESS_TOKEN",
    instagram_user_id="YOUR_INSTAGRAM_USER_ID"
)

# Get Reel analytics
reel_data = analytics.get_video_analytics("MEDIA_ID")

if reel_data:
    print(f"Plays: {reel_data.views}")
    print(f"Likes: {reel_data.likes}")
    print(f"Saves: {reel_data.saves}")
    print(f"Reach: {reel_data.impressions}")
    print(f"Engagement rate: {reel_data.engagement_rate:.2f}%")

# Get account analytics
account_stats = analytics.get_channel_analytics()
print(f"Impressions: {account_stats['impressions']}")
print(f"Reach: {account_stats['reach']}")
```

#### Best Practices

1. **Content Strategy**:
   - Use 3-5 relevant hashtags (avoid hashtag spam)
   - Include keywords in caption naturally
   - Add location tags when relevant
   - Create shareable, entertaining content

2. **Video Requirements**:
   - Format: MP4 or MOV
   - Resolution: 1080x1920 (9:16)
   - Duration: Up to 90 seconds
   - File size: Up to 100MB
   - Video must be hosted at public URL

3. **Engagement Tips**:
   - Ask questions to encourage comments
   - Use trending audio when appropriate
   - Post consistently (1-2 Reels per day)
   - Monitor insights to optimize posting times

### Facebook Integration

#### Setup

1. **Facebook Page**:
   - Create a Facebook Business Page
   - Get Page access token from Facebook Developers

2. **Graph API Setup**:
   - Create Facebook App at developers.facebook.com
   - Enable required permissions:
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `pages_show_list`
   - Get Page access token

3. **Environment Variables**:
   ```bash
   export FACEBOOK_ACCESS_TOKEN="your_page_access_token_here"
   export FACEBOOK_PAGE_ID="your_page_id"
   ```

#### Usage

**Upload a Video:**

```python
from PrismQ.Providers import FacebookUploader
from core.interfaces.platform_provider import VideoMetadata

# Initialize uploader
uploader = FacebookUploader(
    access_token="YOUR_ACCESS_TOKEN",
    page_id="YOUR_PAGE_ID"
)

# Prepare metadata
metadata = VideoMetadata(
    title="Amazing Story",
    description="Check out this incredible AI-generated story!",
    hashtags=["AI", "Story", "Video"],
)

# Upload video (local file or URL)
result = uploader.upload_video("output/video.mp4", metadata)
# Or from URL: result = uploader.upload_video("https://cdn.example.com/video.mp4", metadata)

if result.success:
    print(f"Video published: {result.url}")
    print(f"Video ID: {result.video_id}")
else:
    print(f"Upload failed: {result.error_message}")
```

**Retrieve Analytics:**

```python
from PrismQ.Providers import FacebookAnalytics

# Initialize analytics
analytics = FacebookAnalytics(
    access_token="YOUR_ACCESS_TOKEN",
    page_id="YOUR_PAGE_ID"
)

# Get video analytics
video_data = analytics.get_video_analytics("VIDEO_ID")

if video_data:
    print(f"Views: {video_data.views:,}")
    print(f"Likes: {video_data.likes:,}")
    print(f"Comments: {video_data.comments:,}")
    print(f"Shares: {video_data.shares:,}")
    print(f"Engagement rate: {video_data.engagement_rate:.2f}%")

# Get page analytics
page_stats = analytics.get_channel_analytics()
print(f"Fans: {page_stats.get('fan_count', 0):,}")
```

#### Best Practices

1. **Content Strategy**:
   - Use engaging titles (max 65 characters)
   - Write descriptive captions
   - Include relevant hashtags
   - Post during peak engagement times

2. **Video Requirements**:
   - Format: MP4 (recommended)
   - Resolution: 720p or higher
   - Duration: 1 second to 240 minutes
   - File size: Up to 4GB (or use URL)

3. **Engagement Tips**:
   - Create shareable content
   - Use Facebook's native upload (better reach than YouTube links)
   - Respond to comments quickly
   - Monitor Page Insights for optimal posting times

## Database Integration

The platform integration includes SQLite database storage for all text data and analytics.

### Setting Up the Database

```python
from core.database import PlatformDatabase

# Initialize database
db = PlatformDatabase("data/platform_analytics.db")
db.initialize()
```

### Storing Upload Results

```python
from core.interfaces.platform_provider import UploadResult, PlatformType
from datetime import datetime

# After successful upload
result = uploader.upload_video("video.mp4", metadata)

if result.success:
    # Save to database
    db.save_upload_result(
        result,
        title_id="story_123",
        title="Amazing Story",
        description="An incredible AI-generated story",
        tags=["ai", "story", "shorts"],
        hashtags=["Shorts", "AI", "Viral"],
    )
```

### Storing Analytics

```python
# Collect analytics
analytics_data = analytics.get_video_analytics(video_id)

if analytics_data:
    # Save to database
    db.save_analytics(analytics_data)
```

### Querying Data

```python
# Get video by title ID and platform
video = db.get_video_by_title_id("story_123", "youtube")

# Get latest analytics
latest = db.get_latest_analytics("VIDEO_ID", "youtube")

# Get all videos for a platform
videos = db.get_all_videos(platform="youtube", limit=50)
```

## Cross-Platform Performance Comparison

Analyze and compare video performance across all platforms.

### Basic Comparison

```python
from core.platform_comparison import PlatformComparator

# Initialize comparator
comparator = PlatformComparator("data/platform_analytics.db")

# Compare performance for a specific video
comparison = comparator.compare_video("story_123")

if comparison:
    print(f"Title: {comparison.title}")
    print(f"Total Views: {comparison.total_views:,}")
    print(f"Total Engagement: {comparison.total_engagement:,}")
    print(f"Average Engagement Rate: {comparison.average_engagement_rate:.2f}%")
    
    # Get best platform
    best = comparison.get_best_platform("engagement_rate")
    print(f"Best Platform: {best.platform} ({best.engagement_rate:.2f}%)")
    
    # Get rankings
    rankings = comparison.get_platform_ranking("views")
    for rank, (platform, views) in enumerate(rankings, 1):
        print(f"{rank}. {platform}: {int(views):,} views")
```

### Generating Insights

```python
# Get optimization insights
insights = comparator.generate_insights("story_123")

print(f"Summary:")
print(f"  Total Views: {insights['summary']['total_views']:,}")
print(f"  Average Engagement: {insights['summary']['average_engagement_rate']:.2f}%")

print(f"\nBest Performers:")
for metric, platform in insights['best_performers'].items():
    print(f"  {metric}: {platform}")

print(f"\nRecommendations:")
for rec in insights['recommendations']:
    print(f"  • {rec}")
```

### Platform Trends

```python
# Analyze trends for a specific platform
trends = comparator.get_platform_trends("youtube", limit=10)

print(f"YouTube Trends:")
print(f"  Videos Analyzed: {trends['video_count']}")
print(f"  Average Views: {trends['average_views']:,}")
print(f"  Average Engagement: {trends['average_engagement']:,}")

# Compare all platforms
overall = comparator.compare_all_platforms()
print(f"\nOverall: {overall['total_videos']} videos, {overall['total_views']:,} total views")
```

### Example Output

```
📊 Performance Summary:
  Total Views: 85,500
  Total Engagement: 7,480
  Average Engagement Rate: 7.73%

🏆 Platform Rankings:
  By Views:
    1. tiktok: 50,000 views
    2. youtube: 15,000 views
    3. facebook: 12,000 views
    4. instagram: 8,500 views

  By Engagement Rate:
    1. tiktok: 10.30%
    2. facebook: 6.90%
    3. instagram: 6.90%
    4. youtube: 6.80%

💡 Recommendations:
  1. Best engagement on tiktok (10.30%). Consider focusing on this platform.
  2. tiktok shows high virality (score: 0.55). Content style resonates well here.
  3. instagram underperforming (engagement: 6.90%). Consider adjusting content strategy.
```

## Error Handling

All providers implement automatic retry logic with exponential backoff:

```python
@retry(
    retry=retry_if_exception_type(Exception),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
)
```

**Retry Strategy:**
- Attempt 1: Immediate
- Attempt 2: Wait 4 seconds
- Attempt 3: Wait 8 seconds
- Failed: Raise exception

## Testing

Run the platform provider tests:

```bash
# Run all platform tests
pytest tests/test_platform_providers.py -v

# Run specific platform tests
pytest tests/test_platform_providers.py::TestYouTubeUploader -v
pytest tests/test_platform_providers.py::TestTikTokAnalytics -v

# Run with coverage
pytest tests/test_platform_providers.py --cov=providers --cov-report=html
```

## Resources

### Documentation
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [YouTube Analytics API](https://developers.google.com/youtube/analytics)
- [TikTok for Developers](https://developers.tiktok.com/)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)

### Support
- Check provider logs for detailed error messages
- Review platform API status pages for outages
- Consult platform developer forums for issues

## Next Steps

After implementing platform integration:

1. **Monitor Performance**: Track analytics regularly
2. **Optimize Content**: Use data to improve future videos
3. **Scale Production**: Increase upload frequency gradually
4. **Experiment**: Test different content styles and formats
5. **Automate Workflows**: Build pipelines for end-to-end automation

For questions or issues, refer to the main [StoryGenerator documentation](../../README.md).
