# Step 14: Platform Distribution & Performance Analytics

**Status:** Not Started  
**Priority:** Medium  
**Dependencies:** Step 13 (Final Export)

---

## Overview

This step handles the distribution of final videos to multiple social media platforms (YouTube, TikTok, Instagram, Facebook) and tracks their performance through analytics APIs. It also monitors monetization metrics and provides insights for content optimization.

### Target Platforms

- **YouTube** - Long-form content (Shorts support)
- **TikTok** - Vertical short-form content
- **Instagram** - Reels and Stories
- **Facebook** - Video posts and Reels
- **YouTube Shorts** - Short-form vertical content

---

## Detailed Checklist

### 14.1 Platform Upload Integration

- [ ] **YouTube Upload API**
  - [ ] Set up OAuth 2.0 authentication for YouTube Data API v3
  - [ ] Implement video upload with metadata (title, description, tags, category)
  - [ ] Support for YouTube Shorts designation
  - [ ] Handle privacy settings (public, unlisted, private)
  - [ ] Implement thumbnail upload
  - [ ] Add playlist management
  - [ ] Handle upload quota limits and retry logic
  - [ ] Save: `/distribution/youtube/{segment}/{age}/{title_id}_upload_response.json`

- [ ] **TikTok Upload API**
  - [ ] Set up TikTok Content Posting API authentication
  - [ ] Implement video upload with captions and hashtags
  - [ ] Handle TikTok's video requirements (resolution, duration, format)
  - [ ] Add cover image/thumbnail selection
  - [ ] Implement privacy and comment settings
  - [ ] Save: `/distribution/tiktok/{segment}/{age}/{title_id}_upload_response.json`

- [ ] **Instagram API Integration**
  - [ ] Set up Instagram Graph API authentication
  - [ ] Implement Reels publishing
  - [ ] Add caption and hashtag support
  - [ ] Handle Instagram's aspect ratio requirements
  - [ ] Implement location and tagging features
  - [ ] Save: `/distribution/instagram/{segment}/{age}/{title_id}_upload_response.json`

- [ ] **Facebook Video API**
  - [ ] Set up Facebook Graph API authentication
  - [ ] Implement video upload to Pages
  - [ ] Support for Facebook Reels
  - [ ] Add title, description, and tags
  - [ ] Handle privacy settings and scheduling
  - [ ] Save: `/distribution/facebook/{segment}/{age}/{title_id}_upload_response.json`

### 14.2 Analytics Integration

- [ ] **YouTube Analytics API**
  - [ ] Implement YouTube Analytics API v2 authentication
  - [ ] Collect metrics:
    - Views, watch time, average view duration
    - Engagement (likes, comments, shares, saves)
    - CTR (click-through rate), impressions
    - Audience retention graphs
    - Traffic sources and demographics
    - Revenue (estimated, ad revenue, RPM, CPM)
  - [ ] Schedule periodic data collection (daily, weekly)
  - [ ] Save: `/analytics/youtube/{segment}/{age}/{title_id}_YYYYMMDD_analytics.json`

- [ ] **TikTok Analytics API**
  - [ ] Implement TikTok Research API or Creator API
  - [ ] Collect metrics:
    - Views, likes, comments, shares
    - Watch time and completion rate
    - Follower growth
    - Audience demographics
    - Trending hashtag performance
  - [ ] Save: `/analytics/tiktok/{segment}/{age}/{title_id}_YYYYMMDD_analytics.json`

- [ ] **Instagram Insights API**
  - [ ] Implement Instagram Graph API Insights
  - [ ] Collect metrics:
    - Reach, impressions, engagement
    - Saves, shares, comments, likes
    - Profile visits from content
    - Audience demographics
  - [ ] Save: `/analytics/instagram/{segment}/{age}/{title_id}_YYYYMMDD_analytics.json`

- [ ] **Facebook Insights API**
  - [ ] Implement Facebook Graph API Insights
  - [ ] Collect metrics:
    - Views, reach, engagement
    - Reactions, comments, shares
    - Audience demographics
    - Video retention
  - [ ] Save: `/analytics/facebook/{segment}/{age}/{title_id}_YYYYMMDD_analytics.json`

### 14.3 Third-Party Analytics Integration

- [ ] **TubeBuddy API Integration** (if available)
  - [ ] Set up TubeBuddy API access
  - [ ] Collect keyword ranking data
  - [ ] Get SEO scores and recommendations
  - [ ] Track competitor analysis
  - [ ] Save: `/analytics/tubebuddy/{segment}/{age}/{title_id}_YYYYMMDD.json`

- [ ] **VidIQ API Integration** (if available)
  - [ ] Set up VidIQ API access
  - [ ] Collect video SEO metrics
  - [ ] Get trending topic suggestions
  - [ ] Track video performance scores
  - [ ] Competitor comparison data
  - [ ] Save: `/analytics/vidiq/{segment}/{age}/{title_id}_YYYYMMDD.json`

- [ ] **Social Blade API** (optional)
  - [ ] Track channel growth metrics
  - [ ] Collect estimated earnings data
  - [ ] Get rank and subscriber projections
  - [ ] Save: `/analytics/socialblade/{segment}/{age}/YYYYMMDD_channel_stats.json`

### 14.4 Monetization Tracking

- [ ] **YouTube Revenue Tracking**
  - [ ] Collect YouTube Partner Program metrics
  - [ ] Track estimated earnings per video
  - [ ] Calculate RPM (Revenue Per Mille) and CPM (Cost Per Mille)
  - [ ] Monitor monetization status and ad suitability
  - [ ] Track revenue by geography and ad type
  - [ ] Save: `/monetization/youtube/{segment}/{age}/{title_id}_YYYYMMDD_revenue.json`

- [ ] **TikTok Creator Fund** (if applicable)
  - [ ] Track Creator Fund earnings
  - [ ] Monitor eligibility and payout metrics
  - [ ] Save: `/monetization/tiktok/{segment}/{age}/{title_id}_YYYYMMDD_revenue.json`

- [ ] **Instagram/Facebook Monetization**
  - [ ] Track bonus program earnings
  - [ ] Monitor ad revenue sharing (if applicable)
  - [ ] Save: `/monetization/meta/{segment}/{age}/{title_id}_YYYYMMDD_revenue.json`

- [ ] **Cross-Platform Revenue Summary**
  - [ ] Aggregate earnings across all platforms
  - [ ] Calculate total ROI per video
  - [ ] Generate monthly/quarterly revenue reports
  - [ ] Save: `/monetization/summary/{segment}/{age}/YYYYMM_summary.json`

### 14.5 Performance Evaluation

- [ ] **Automated Performance Scoring**
  - [ ] Create scoring algorithm based on:
    - View count vs. expected baseline
    - Engagement rate (likes, comments, shares / views)
    - Retention rate and watch time
    - Revenue per view
    - Growth metrics (subscribers, followers)
  - [ ] Generate performance score (0-100) per video
  - [ ] Save: `/analytics/performance/{segment}/{age}/{title_id}_performance_score.json`

- [ ] **A/B Testing Analysis**
  - [ ] Compare different title variants
  - [ ] Analyze thumbnail effectiveness
  - [ ] Test posting times and days
  - [ ] Evaluate content length performance
  - [ ] Save: `/analytics/ab_tests/{test_id}_results.json`

- [ ] **Content Optimization Recommendations**
  - [ ] Analyze top-performing videos
  - [ ] Identify successful patterns (topics, styles, lengths)
  - [ ] Generate recommendations for future content
  - [ ] Save: `/analytics/recommendations/YYYYMMDD_recommendations.json`

### 14.6 Reporting & Dashboards

- [ ] **Automated Reporting**
  - [ ] Generate daily performance summaries
  - [ ] Create weekly analytics reports
  - [ ] Monthly revenue and growth reports
  - [ ] Save reports: `/reports/{YYYY}/{MM}/YYYYMMDD_report.pdf`

- [ ] **Dashboard Integration** (optional)
  - [ ] Export data to visualization tools (Grafana, Tableau, Power BI)
  - [ ] Create real-time performance dashboards
  - [ ] Set up alerts for viral content or issues
  - [ ] Save dashboard configs: `/dashboards/config.json`

---

## JSON Schemas

### Upload Response Schema

```json
{
  "upload_response": {
    "platform": "youtube|tiktok|instagram|facebook",
    "video_id": "platform_specific_id",
    "title_id": "uuid",
    "segment": "women|men",
    "age_bucket": "10-13|14-17|18-23",
    "upload_date": "ISO-8601",
    "url": "public_url",
    "status": "processing|published|failed",
    "metadata": {
      "title": "string",
      "description": "string",
      "tags": ["tag1", "tag2"],
      "category": "string",
      "privacy": "public|unlisted|private"
    },
    "error": "error_message_if_failed"
  }
}
```

### Analytics Schema

```json
{
  "analytics": {
    "platform": "youtube|tiktok|instagram|facebook",
    "video_id": "platform_specific_id",
    "title_id": "uuid",
    "collected_at": "ISO-8601",
    "metrics": {
      "views": 0,
      "likes": 0,
      "comments": 0,
      "shares": 0,
      "saves": 0,
      "watch_time_seconds": 0,
      "average_view_duration": 0,
      "completion_rate": 0.0,
      "ctr": 0.0,
      "impressions": 0
    },
    "engagement": {
      "engagement_rate": 0.0,
      "like_rate": 0.0,
      "comment_rate": 0.0,
      "share_rate": 0.0
    },
    "audience": {
      "age_ranges": {"18-24": 0.45, "25-34": 0.35},
      "gender": {"male": 0.52, "female": 0.48},
      "top_countries": ["US", "UK", "CA"],
      "devices": {"mobile": 0.85, "desktop": 0.15}
    },
    "traffic_sources": {
      "search": 0.25,
      "suggested": 0.45,
      "external": 0.10,
      "direct": 0.20
    }
  }
}
```

### Revenue Schema

```json
{
  "revenue": {
    "platform": "youtube|tiktok|instagram|facebook",
    "video_id": "platform_specific_id",
    "title_id": "uuid",
    "period_start": "ISO-8601",
    "period_end": "ISO-8601",
    "currency": "USD",
    "earnings": {
      "total": 0.00,
      "ad_revenue": 0.00,
      "creator_fund": 0.00,
      "bonus_programs": 0.00
    },
    "metrics": {
      "rpm": 0.00,
      "cpm": 0.00,
      "monetized_views": 0,
      "ad_impressions": 0
    },
    "by_country": {
      "US": {"earnings": 0.00, "views": 0},
      "UK": {"earnings": 0.00, "views": 0}
    }
  }
}
```

### Performance Score Schema

```json
{
  "performance_score": {
    "title_id": "uuid",
    "video_id": "platform_specific_id",
    "platform": "youtube|tiktok|instagram|facebook",
    "scored_at": "ISO-8601",
    "overall_score": 85,
    "breakdown": {
      "views_score": 90,
      "engagement_score": 85,
      "retention_score": 80,
      "revenue_score": 75,
      "growth_score": 88
    },
    "performance_tier": "excellent|good|average|poor",
    "recommendations": [
      "Posting time optimization: Post 2 hours earlier",
      "Consider shorter duration for this audience segment",
      "Strong engagement - replicate this content style"
    ],
    "comparison": {
      "vs_channel_average": "+15%",
      "vs_segment_average": "+8%",
      "vs_previous_video": "+22%"
    }
  }
}
```

---

## API Integration Notes

### YouTube Data API v3

- **Authentication:** OAuth 2.0
- **Key APIs:**
  - `youtube.videos.insert` - Upload videos
  - `youtube.thumbnails.set` - Set custom thumbnail
  - `youtubeAnalytics.reports.query` - Get analytics
  - `youtube.videos.list` - Get video details
- **Rate Limits:** 10,000 quota units/day (uploads cost 1600 units each)
- **Documentation:** https://developers.google.com/youtube/v3

### TikTok API

- **Options:**
  - Content Posting API (for uploads)
  - Research API (for analytics - limited access)
  - Creator API (for creator metrics)
- **Rate Limits:** Varies by API tier
- **Documentation:** https://developers.tiktok.com/

### Instagram Graph API

- **Authentication:** Facebook OAuth
- **Key APIs:**
  - `POST /{ig-user-id}/media` - Create media container
  - `POST /{ig-user-id}/media_publish` - Publish media
  - `GET /{ig-media-id}/insights` - Get insights
- **Limitations:** Business/Creator accounts only
- **Documentation:** https://developers.facebook.com/docs/instagram-api

### Facebook Graph API

- **Authentication:** Facebook OAuth
- **Key APIs:**
  - `POST /{page-id}/videos` - Upload video
  - `GET /{video-id}/video_insights` - Get insights
- **Documentation:** https://developers.facebook.com/docs/graph-api

### Third-Party Tools

- **TubeBuddy:** May require browser automation or unofficial API
- **VidIQ:** Similar limitations, may need scraping or partnership
- **Social Blade:** Offers public API for channel statistics

---

## Implementation Considerations

### Upload Automation

```python
# Example: YouTube upload automation
class YouTubeUploader:
    def upload_video(self, video_path, metadata):
        # OAuth 2.0 authentication
        credentials = self.get_credentials()
        youtube = build('youtube', 'v3', credentials=credentials)
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': metadata['title'],
                'description': metadata['description'],
                'tags': metadata['tags'],
                'categoryId': metadata['category']
            },
            'status': {
                'privacyStatus': metadata['privacy'],
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Upload video
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
        )
        
        response = request.execute()
        return response
```

### Analytics Collection

```python
# Example: Periodic analytics collection
class AnalyticsCollector:
    def collect_daily_analytics(self, video_ids):
        for video_id in video_ids:
            # YouTube Analytics
            yt_data = self.youtube_analytics_api.query(
                ids=f'channel=={channel_id}',
                start_date='7daysAgo',
                end_date='today',
                metrics='views,likes,comments,shares,estimatedMinutesWatched',
                dimensions='video',
                filters=f'video=={video_id}'
            )
            
            # Save analytics
            self.save_analytics(video_id, yt_data, 'youtube')
```

### Rate Limiting & Error Handling

- Implement exponential backoff for API rate limits
- Use queue systems for bulk uploads
- Cache analytics data to minimize API calls
- Handle platform-specific errors gracefully
- Log all API interactions for debugging

---

## Acceptance Criteria

- [ ] Successfully upload videos to at least 2 platforms (YouTube + one other)
- [ ] Automated analytics collection working for all integrated platforms
- [ ] Revenue tracking implemented for monetized platforms
- [ ] Performance scoring algorithm generating meaningful scores
- [ ] Weekly reports generated automatically
- [ ] All uploads and analytics logged with proper metadata
- [ ] Error handling and retry logic working correctly
- [ ] API rate limits respected with appropriate throttling

---

## Related Files

### Input
- `/final/{segment}/{age}/{title_id}.mp4` (from Step 13)
- `/final/{segment}/{age}/{title_id}_metadata.json` (from Step 13)
- `/final/{segment}/{age}/{title_id}_thumbnail.png` (from Step 13)

### Output
- `/distribution/{platform}/{segment}/{age}/{title_id}_upload_response.json`
- `/analytics/{platform}/{segment}/{age}/{title_id}_YYYYMMDD_analytics.json`
- `/monetization/{platform}/{segment}/{age}/{title_id}_YYYYMMDD_revenue.json`
- `/analytics/performance/{segment}/{age}/{title_id}_performance_score.json`
- `/reports/{YYYY}/{MM}/YYYYMMDD_report.pdf`

### Configuration
- `/config/distribution.yaml` - Platform credentials and settings
- `/config/analytics.yaml` - Collection schedules and thresholds
- `/config/monetization.yaml` - Revenue tracking settings

---

## Validation

Use MicrostepValidator to track progress:

```python
from Tools.MicrostepValidator import (
    create_microstep_artifact,
    update_microstep_progress,
    copilot_check_microstep
)

# Log upload
create_microstep_artifact(
    step_number=14,
    artifact_name=f"{title_id}_youtube_upload.json",
    content=upload_response,
    gender=gender,
    age=age
)

# Update progress
update_microstep_progress(
    step_number=14,
    status="in_progress",
    details=f"Uploaded to YouTube, collecting analytics",
    gender=gender,
    age=age
)

# Validate completion
copilot_check_microstep(14, gender, age)
```

**Command:** `@copilot check` when uploads and initial analytics collection are complete

---

## Notes

- **Privacy & Compliance:** Ensure all uploads comply with platform policies and copyright laws
- **Automation:** Consider using scheduling tools (cron, celery) for periodic analytics collection
- **Costs:** Monitor API usage costs, especially for third-party analytics tools
- **Backup:** Keep local copies of all uploaded videos and metadata
- **Multi-Account:** May need separate accounts for different content segments
- **Testing:** Use test accounts and private uploads for initial integration testing
