# Social Media Platforms - Trends Data Collection Research

## Overview

This document outlines how to gather trend and popularity data from YouTube, TikTok, and Instagram to complement Google Trends data for viral content generation.

---

## YouTube Data API v3

### Official API ✅ Recommended

**Endpoint:** `https://www.googleapis.com/youtube/v3/videos`

**Authentication:** API Key (free tier: 10,000 quota units/day)

**Key Methods:**

1. **Most Popular Videos:**
```python
GET /youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&maxResults=50

Response:
{
  "items": [{
    "id": "video_id",
    "snippet": {
      "title": "...",
      "tags": ["tag1", "tag2"],
      "categoryId": "10"
    },
    "statistics": {
      "viewCount": "1000000",
      "likeCount": "50000"
    }
  }]
}
```

2. **Trending Searches:**
```python
GET /youtube/v3/search?part=snippet&order=viewCount&publishedAfter=2024-01-01T00:00:00Z&regionCode=US&maxResults=50
```

**Quota Costs:**
- `videos.list`: 1 unit per request
- `search.list`: 100 units per request
- Budget: ~100 search requests/day or 10K video list requests/day

**Python Example:**
```python
from googleapiclient.discovery import build

def get_youtube_trends(api_key, region_code='US', max_results=50):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        chart='mostPopular',
        regionCode=region_code,
        maxResults=max_results,
        videoCategoryId='10'  # Music category
    )
    
    response = request.execute()
    
    trends = []
    for item in response['items']:
        trends.append({
            'keyword': item['snippet']['title'],
            'tags': item['snippet'].get('tags', []),
            'views': int(item['statistics']['viewCount']),
            'likes': int(item['statistics']['likeCount']),
            'source': 'youtube',
            'region': region_code,
            'video_id': item['id']
        })
    
    return trends
```

**Best Practices:**
- Cache results for 1 hour minimum
- Use exponential backoff for rate limiting
- Filter by video duration (<60s for Shorts)
- Track velocity (views change over 24h)

---

## TikTok

### No Official Public API ❌

TikTok Creative Center API is invite-only for advertisers.

### Third-Party Solutions:

**1. Apify TikTok Scrapers** (Paid)
- URL: `https://apify.com/apify/tiktok-scraper`
- Cost: ~$49/month for 100K results
- Features: Hashtag trends, video stats, user profiles
- Legal: Complies with ToS through rotation

**2. RapidAPI TikTok APIs** (Paid)
- URL: `https://rapidapi.com/hub?search=tiktok`
- Options: TikTok API, TikApi, TikTok Data
- Cost: $10-50/month for basic plans
- Rate limits: 500-5000 requests/month

**3. Picodata TikTok Trends** (Paid)
- URL: `https://www.picodata.io/`
- Features: Real-time trending hashtags, sounds, challenges
- Cost: Custom pricing (enterprise)

**4. Custom Scraping** (Not Recommended)
- Violates TikTok ToS
- Requires:
  - Selenium/Playwright for dynamic content
  - Residential proxy rotation
  - CAPTCHA solving service
  - Cookie/session management
- Risk: IP bans, legal issues

**Example Using RapidAPI:**
```python
import requests

def get_tiktok_trends_rapidapi(api_key, region='US'):
    url = "https://tiktok-scraper2.p.rapidapi.com/trending/feed"
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "tiktok-scraper2.p.rapidapi.com"
    }
    
    params = {"region": region, "count": 50}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    trends = []
    for item in data.get('itemList', []):
        trends.append({
            'keyword': item['desc'],
            'hashtags': [tag['hashtagName'] for tag in item.get('textExtra', [])],
            'views': item['stats']['playCount'],
            'likes': item['stats']['diggCount'],
            'source': 'tiktok',
            'region': region
        })
    
    return trends
```

**Recommendation:**
- Start without TikTok if budget constrained
- Add RapidAPI integration if budget allows ($10-20/month)
- Focus on YouTube + Google Trends initially

---

## Instagram

### Official Graph API ❌ No Trends Endpoint

Instagram Graph API does not expose trending content or discovery features.

### Third-Party Solutions:

**1. CrowdTangle (Meta-owned)** (Paid, Invite-only)
- URL: `https://www.crowdtangle.com/`
- Features: Top posts, hashtag tracking, engagement metrics
- Access: Free for academics, journalists (application required)
- API: REST API with historical data

**2. Iconosquare** (Paid)
- URL: `https://www.iconosquare.com/`
- Cost: $49-79/month
- Features: Hashtag analytics, trending content, engagement
- No API (web dashboard only)

**3. Sprout Social** (Paid)
- URL: `https://sproutsocial.com/`
- Cost: $249-499/month (enterprise)
- Features: Comprehensive social listening
- API: Available on higher tiers

**4. Hashtag Tracking via Graph API** (Limited)
```python
# Only works for business accounts you manage
GET /ig_hashtag_search?user_id={user_id}&q=travel

# Get recent media for hashtag
GET /{ig_hashtag_id}/recent_media
```

**5. Custom Scraping** (Not Recommended)
- Violates Instagram ToS
- High risk of account bans
- Requires complex anti-detection measures

**Recommendation:**
- Skip Instagram for initial MVP
- Consider CrowdTangle if academic/journalism access
- Focus resources on YouTube + Google Trends

---

## Implementation Recommendations

### Phase 1: MVP (Weeks 1-2)
1. ✅ Google Trends (already implemented)
2. ✅ YouTube Data API (official, free)
3. ✅ Local SQLite storage

### Phase 2: Enhancement (Weeks 3-4)
1. Add TikTok via RapidAPI ($10-20/month)
2. Implement trend score normalization
3. Add PostgreSQL for production

### Phase 3: Scale (Months 2-3)
1. Instagram via CrowdTangle (if access granted)
2. Multi-region support (US, UK, CA, AU, CZ)
3. Real-time WebSocket updates

### Phase 4: Advanced (Months 3+)
1. Machine learning for trend prediction
2. Cross-platform deduplication
3. Automated content generation pipeline

---

## Cost Analysis

| Platform | Method | Cost/Month | Requests/Month | Pros | Cons |
|----------|--------|------------|----------------|------|------|
| YouTube | Official API | Free | 300K quota | Official, reliable | Quota limits |
| Google Trends | CSV Export | Free | Unlimited | Already implemented | Manual export |
| TikTok | RapidAPI | $10-50 | 500-5K | Easy integration | Limited data |
| TikTok | Apify | $49+ | 100K results | Comprehensive | Expensive |
| Instagram | CrowdTangle | Free* | Varies | Official (Meta) | Invite-only |
| Instagram | Iconosquare | $49-79 | N/A (dashboard) | Full analytics | No API |

*Requires application and approval

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Trends Aggregator                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Google Trends│  │  YouTube API │  │ TikTok API   │     │
│  │   (CSV)      │  │  (Official)  │  │ (RapidAPI)   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                  ┌─────────▼─────────┐                      │
│                  │  Normalization    │                      │
│                  │  - Keyword        │                      │
│                  │  - Score          │                      │
│                  │  - Region         │                      │
│                  │  - Timestamp      │                      │
│                  └─────────┬─────────┘                      │
│                            │                                 │
│                  ┌─────────▼─────────┐                      │
│                  │  De-duplication   │                      │
│                  │  - Fuzzy match    │                      │
│                  │  - Merge scores   │                      │
│                  └─────────┬─────────┘                      │
│                            │                                 │
│                  ┌─────────▼─────────┐                      │
│                  │  Trend Scoring    │                      │
│                  │  - Velocity       │                      │
│                  │  - Volume         │                      │
│                  │  - Engagement     │                      │
│                  └─────────┬─────────┘                      │
│                            │                                 │
│                  ┌─────────▼─────────┐                      │
│                  │  Storage          │                      │
│                  │  - SQLite/        │                      │
│                  │    PostgreSQL     │                      │
│                  └───────────────────┘                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Code Examples

### Multi-Platform Aggregator

```python
# trends_aggregator.py

import time
from typing import List, Dict
from datetime import datetime

class TrendsAggregator:
    def __init__(self, youtube_api_key=None, rapidapi_key=None):
        self.youtube_key = youtube_api_key
        self.rapidapi_key = rapidapi_key
        
    def collect_all_trends(self, region='US') -> List[Dict]:
        """Collect trends from all available sources"""
        all_trends = []
        
        # Google Trends (from CSV)
        if google_trends := self.get_google_trends(region):
            all_trends.extend(google_trends)
        
        # YouTube
        if self.youtube_key and (youtube_trends := self.get_youtube_trends(region)):
            all_trends.extend(youtube_trends)
        
        # TikTok (if API key available)
        if self.rapidapi_key and (tiktok_trends := self.get_tiktok_trends(region)):
            all_trends.extend(tiktok_trends)
        
        return all_trends
    
    def normalize_trends(self, trends: List[Dict]) -> List[Dict]:
        """Normalize trends to common format"""
        normalized = []
        
        for trend in trends:
            normalized.append({
                'keyword': trend.get('keyword', '').strip(),
                'score': self.calculate_score(trend),
                'source': trend.get('source', 'unknown'),
                'region': trend.get('region', 'US'),
                'locale': trend.get('locale', 'en-US'),
                'timestamp': datetime.utcnow().isoformat(),
                'raw_metrics': trend
            })
        
        return normalized
    
    def deduplicate_trends(self, trends: List[Dict]) -> List[Dict]:
        """Remove duplicate trends using fuzzy matching"""
        from difflib import SequenceMatcher
        
        unique_trends = []
        seen_keywords = []
        
        for trend in trends:
            keyword = trend['keyword'].lower()
            
            # Check for fuzzy match
            is_duplicate = False
            for seen in seen_keywords:
                similarity = SequenceMatcher(None, keyword, seen).ratio()
                if similarity > 0.85:  # 85% similarity threshold
                    is_duplicate = True
                    # Merge scores
                    for unique_trend in unique_trends:
                        if unique_trend['keyword'].lower() == seen:
                            unique_trend['score'] = max(
                                unique_trend['score'],
                                trend['score']
                            )
                            unique_trend['sources'] = list(set(
                                unique_trend.get('sources', [unique_trend['source']]) +
                                [trend['source']]
                            ))
                            break
                    break
            
            if not is_duplicate:
                seen_keywords.append(keyword)
                trend['sources'] = [trend['source']]
                unique_trends.append(trend)
        
        return unique_trends
    
    def calculate_score(self, trend: Dict) -> float:
        """Calculate normalized trend score (0-100)"""
        source = trend.get('source', '')
        
        if source == 'google':
            # Google Trends value is already 0-100
            return float(trend.get('value', 0))
        
        elif source == 'youtube':
            # Score based on views and likes
            views = float(trend.get('views', 0))
            likes = float(trend.get('likes', 0))
            
            # Normalize (assuming 10M views = 100 score)
            view_score = min((views / 10_000_000) * 100, 100)
            engagement_rate = (likes / views * 100) if views > 0 else 0
            
            return (view_score * 0.7) + (engagement_rate * 0.3)
        
        elif source == 'tiktok':
            # Score based on plays and likes
            plays = float(trend.get('views', 0))
            likes = float(trend.get('likes', 0))
            
            # Normalize (assuming 50M plays = 100 score)
            play_score = min((plays / 50_000_000) * 100, 100)
            engagement_rate = (likes / plays * 100) if plays > 0 else 0
            
            return (play_score * 0.7) + (engagement_rate * 0.3)
        
        return 50.0  # Default mid-range score
```

---

## Next Steps

1. **Implement YouTube Data API integration** (Priority 1)
   - Create `youtube_trends.py` module
   - Add to `process_trends.py` pipeline
   - Update `config/audience_config.json` with API keys

2. **Set up SQLite database** (Priority 2)
   - Create schema for trends storage
   - Add historical tracking for velocity calculation
   - Implement cleanup for old trends (7-day retention)

3. **Add trend aggregation** (Priority 3)
   - Implement `TrendsAggregator` class
   - Add deduplication logic
   - Create unified scoring system

4. **Optional: Add TikTok** (Priority 4)
   - Evaluate RapidAPI vs Apify
   - Budget approval required
   - Implement if budget allows

5. **Documentation** (Priority 5)
   - Update `Generator/trends/README.md`
   - Add API key setup instructions
   - Document rate limits and quotas

---

## References

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [RapidAPI TikTok APIs](https://rapidapi.com/hub?search=tiktok)
- [CrowdTangle Documentation](https://help.crowdtangle.com/en/articles/3443476-api-cheat-sheet)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)

---

**Last Updated:** 2025-01-06  
**Status:** Research Complete - Ready for Implementation  
**Recommended Approach:** YouTube API + Google Trends (MVP)
