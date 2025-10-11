# Viral Short Video Requirements Specification

## Overview

This document defines the requirements and specifications for creating viral short-form videos (Reels, Shorts, TikToks) including content discovery, metadata, and technical implementation.

---

## 1. Scope: Videos + Keywords/Hashtags

### Both Are Required ✅

**Videos:**
- Content delivery mechanism
- Visual engagement
- Retention and watch time
- Core product

**Keywords/Hashtags:**
- Discovery mechanism
- Search ranking
- Algorithm signals
- Distribution amplifier

**Why Both?**
```
Keywords → Discovery → Video Views → Engagement → Algorithm Boost → More Discovery
```

**Implementation:**
- Videos stored in `Generator/final/{gender}/{age}/`
- Keywords stored in `Generator/topics/{gender}/{age}/`
- Hashtags generated in `Generator/titles/{gender}/{age}/`
- Unified in final output JSON with both video path and keywords

---

## 2. Regions & Languages

### Initial Support (MVP)

| Region Code | Locale | Language | Priority |
|-------------|--------|----------|----------|
| US | en-US | English (US) | P0 |
| CZ | cs-CZ | Czech | P0 |
| UK | en-GB | English (UK) | P1 |
| CA | en-CA | English (Canada) | P1 |
| AU | en-AU | English (Australia) | P1 |

### Configuration Structure

```json
{
  "regions": [
    {
      "code": "US",
      "locale": "en-US",
      "language": "English",
      "preference_percentage": 40,
      "content_types": ["shorts", "reels", "tiktok"],
      "platforms": ["youtube", "instagram", "tiktok"]
    },
    {
      "code": "CZ",
      "locale": "cs-CZ",
      "language": "Czech",
      "preference_percentage": 20,
      "content_types": ["shorts", "reels"],
      "platforms": ["youtube", "instagram"]
    }
  ]
}
```

### Expansion Plan

**Phase 2 (Months 2-3):**
- DE (de-DE): German
- FR (fr-FR): French
- ES (es-ES): Spanish (Spain)
- MX (es-MX): Spanish (Mexico)

**Phase 3 (Months 4-6):**
- BR (pt-BR): Portuguese (Brazil)
- JP (ja-JP): Japanese
- KR (ko-KR): Korean
- IN (hi-IN): Hindi (India)

---

## 3. Cadence: Refresh Frequency

### Recommended Schedule

| Data Source | Cadence | Reason | Storage Duration |
|-------------|---------|--------|------------------|
| **Google Trends** | Daily | Updated every 24h | 30 days |
| **YouTube Trending** | Daily | Most Popular refreshed daily | 14 days |
| **YouTube Search** | Hourly* | Catch breakout trends early | 7 days |
| **TikTok Trends** | Hourly* | Fast-moving platform | 7 days |
| **Instagram Trends** | Daily | Slower trend cycles | 14 days |

*Only during peak hours (9 AM - 11 PM in target regions)

### Implementation

```python
# trends_scheduler.py

from datetime import datetime, time

class TrendsScheduler:
    def should_refresh(self, source: str) -> bool:
        """Determine if source should be refreshed"""
        now = datetime.utcnow()
        current_hour = now.hour
        
        if source == 'google_trends':
            # Once per day at 3 AM UTC
            return current_hour == 3
        
        elif source == 'youtube_trending':
            # Once per day at 4 AM UTC
            return current_hour == 4
        
        elif source in ['youtube_search', 'tiktok']:
            # Hourly during peak hours (9 AM - 11 PM UTC)
            return 9 <= current_hour <= 23
        
        elif source == 'instagram':
            # Once per day at 5 AM UTC
            return current_hour == 5
        
        return False
    
    def get_storage_duration_days(self, source: str) -> int:
        """Get storage duration for each source"""
        durations = {
            'google_trends': 30,
            'youtube_trending': 14,
            'youtube_search': 7,
            'tiktok': 7,
            'instagram': 14
        }
        return durations.get(source, 7)
```

---

## 4. Limits: Items & Pagination

### API Quota Limits

| Source | Daily Quota | Request Cost | Max Requests/Day | Items per Request | Max Items/Day |
|--------|-------------|--------------|------------------|-------------------|---------------|
| YouTube Data API | 10,000 units | 100 units (search) | 100 | 50 | 5,000 |
| YouTube Data API | 10,000 units | 1 unit (videos.list) | 10,000 | 50 | 500,000* |
| Google Trends | Unlimited | N/A | Manual export | Variable | Unlimited |
| RapidAPI TikTok | 500/month | 1 per request | 500/month | 50 | 25,000 |

*Theoretical max, practical limit ~5,000/day

### Per-Run Limits

```python
LIMITS = {
    'max_items_per_source': 100,      # Max trending items per source per run
    'max_requests_per_run': 10,       # Max API requests per execution
    'max_storage_items': 10000,       # Max items stored in database
    'max_age_days': 30,               # Max age of stored trends
    'min_score_threshold': 50,        # Min score to store (0-100)
}
```

### Pagination Strategy

**Cursor-Based Pagination (Preferred):**
```python
def paginate_youtube_trends(api_key, max_items=100):
    """Paginate through YouTube trending videos"""
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    all_items = []
    next_page_token = None
    duplicate_count = 0
    
    while len(all_items) < max_items:
        request = youtube.videos().list(
            part='snippet,statistics',
            chart='mostPopular',
            regionCode='US',
            maxResults=50,
            pageToken=next_page_token
        )
        
        response = request.execute()
        items = response.get('items', [])
        
        # Check for duplicates
        for item in items:
            if item['id'] not in [i['id'] for i in all_items]:
                all_items.append(item)
            else:
                duplicate_count += 1
        
        # Stop if >30% duplicates
        if duplicate_count / max(len(items), 1) > 0.3:
            break
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return all_items[:max_items]
```

---

## 5. Storage: Database Schema

### Recommended: SQLite (Development) → PostgreSQL (Production)

**Why SQLite for Dev?**
- Zero configuration
- File-based (easy backup)
- Fast for <100K rows
- Built into Python

**Why PostgreSQL for Prod?**
- Concurrent writes
- Advanced indexing
- Partitioning by date
- JSON support
- Full-text search

### Schema

```sql
-- trends.sql

CREATE TABLE trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    score REAL NOT NULL CHECK (score >= 0 AND score <= 100),
    source TEXT NOT NULL CHECK (source IN ('google', 'youtube', 'tiktok', 'instagram')),
    region TEXT NOT NULL,
    locale TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metadata JSON,
    
    -- Velocity tracking
    views_current INTEGER DEFAULT 0,
    views_24h_ago INTEGER DEFAULT 0,
    velocity REAL GENERATED ALWAYS AS (
        CASE WHEN views_24h_ago > 0 
        THEN ((views_current - views_24h_ago) * 100.0 / views_24h_ago)
        ELSE 0 END
    ) STORED,
    
    -- De-duplication
    content_hash TEXT,
    
    -- Indexes
    UNIQUE(keyword, source, region, DATE(timestamp)),
    INDEX idx_score (score DESC),
    INDEX idx_timestamp (timestamp DESC),
    INDEX idx_region (region),
    INDEX idx_source (source),
    INDEX idx_content_hash (content_hash)
);

-- Velocity history for trend tracking
CREATE TABLE trend_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trend_id INTEGER REFERENCES trends(id),
    views INTEGER NOT NULL,
    likes INTEGER,
    shares INTEGER,
    comments INTEGER,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_trend_timestamp (trend_id, timestamp DESC)
);

-- Hashtags/keywords association
CREATE TABLE hashtags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trend_id INTEGER REFERENCES trends(id),
    hashtag TEXT NOT NULL,
    frequency INTEGER DEFAULT 1,
    
    INDEX idx_trend_id (trend_id),
    INDEX idx_hashtag (hashtag)
);
```

### Alternative: Parquet for Analytics

```python
# For long-term analytics and data science
import pandas as pd

# Export to Parquet daily
df = pd.read_sql('SELECT * FROM trends', conn)
df.to_parquet(
    f'Generator/trends/archives/trends_{datetime.now().strftime("%Y%m%d")}.parquet',
    compression='snappy',
    index=False
)
```

---

## 6. Ethics & Terms of Service

### API Usage Guidelines

✅ **ALWAYS Use Official APIs First:**
1. Google Trends (CSV export - official)
2. YouTube Data API v3 (official)
3. Instagram Graph API (official, limited)
4. TikTok Creative Center API (invite-only)

⚠️ **Third-Party APIs (Proceed with Caution):**
- RapidAPI TikTok scrapers (grey area)
- Apify actors (ToS compliant but expensive)
- Always check current ToS before using

❌ **NEVER Do Custom Scraping:**
- Violates platform ToS
- Risk of IP/account bans
- Legal liability
- Unreliable and fragile

### robots.txt Compliance

```python
from urllib.robotparser import RobotFileParser

def can_fetch(url: str, user_agent: str = 'StoryGeneratorBot/1.0') -> bool:
    """Check if URL can be fetched per robots.txt"""
    rp = RobotFileParser()
    rp.set_url(f"{url.split('/')[0]}//{url.split('/')[2]}/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)
```

### Rate Limiting Best Practices

```python
import time
from functools import wraps

def rate_limit(max_calls_per_minute=60):
    """Decorator to enforce rate limiting"""
    min_interval = 60.0 / max_calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls_per_minute=30)  # 30 calls/min for YouTube
def fetch_youtube_data(api_key, video_id):
    # API call here
    pass
```

### Attribution Requirements

```python
# Add to video metadata
attribution = {
    'data_sources': [
        {
            'platform': 'YouTube',
            'attribution': 'Data provided by YouTube Data API',
            'license': 'YouTube Terms of Service'
        },
        {
            'platform': 'Google Trends',
            'attribution': 'Trending data from Google Trends',
            'license': 'Google Terms of Service'
        }
    ],
    'generated_by': 'StoryGenerator v1.0',
    'timestamp': datetime.utcnow().isoformat()
}
```

---

## 7. Normalization: Common Fields

### Unified Trend Schema

```python
from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class NormalizedTrend:
    """Normalized trend across all sources"""
    
    # Required fields
    keyword: str              # Main keyword/title
    score: float             # Normalized 0-100 score
    source: str              # youtube|google|tiktok|instagram
    region: str              # ISO country code (US, UK, CZ)
    locale: str              # Language locale (en-US, cs-CZ)
    timestamp: datetime      # When collected
    
    # Optional fields
    hashtags: list[str] = None
    category: str = None     # Technology, Entertainment, etc.
    views: int = 0
    likes: int = 0
    shares: int = 0
    comments: int = 0
    
    # Velocity metrics
    views_24h_ago: int = 0
    velocity: float = 0.0    # % change in 24h
    
    # Raw data
    raw_data: Dict = None    # Platform-specific data
    
    # Content hash for deduplication
    content_hash: str = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'keyword': self.keyword,
            'score': self.score,
            'source': self.source,
            'region': self.region,
            'locale': self.locale,
            'timestamp': self.timestamp.isoformat(),
            'hashtags': self.hashtags or [],
            'category': self.category,
            'views': self.views,
            'likes': self.likes,
            'shares': self.shares,
            'comments': self.comments,
            'views_24h_ago': self.views_24h_ago,
            'velocity': self.velocity,
            'raw_data': self.raw_data or {},
            'content_hash': self.content_hash
        }
```

### Normalization Functions

```python
def normalize_youtube_trend(item: Dict, region: str) -> NormalizedTrend:
    """Normalize YouTube API response to common format"""
    import hashlib
    
    keyword = item['snippet']['title']
    views = int(item['statistics']['viewCount'])
    likes = int(item['statistics'].get('likeCount', 0))
    
    return NormalizedTrend(
        keyword=keyword,
        score=calculate_youtube_score(views, likes),
        source='youtube',
        region=region,
        locale=get_locale_from_region(region),
        timestamp=datetime.utcnow(),
        hashtags=item['snippet'].get('tags', []),
        category=item['snippet'].get('categoryId'),
        views=views,
        likes=likes,
        comments=int(item['statistics'].get('commentCount', 0)),
        raw_data=item,
        content_hash=hashlib.md5(keyword.lower().encode()).hexdigest()
    )

def normalize_google_trend(item: Dict, region: str) -> NormalizedTrend:
    """Normalize Google Trends CSV to common format"""
    import hashlib
    
    keyword = item['topic']
    score = float(item['value'])
    
    return NormalizedTrend(
        keyword=keyword,
        score=score,
        source='google',
        region=region,
        locale=get_locale_from_region(region),
        timestamp=datetime.utcnow(),
        hashtags=extract_hashtags(keyword),
        raw_data=item,
        content_hash=hashlib.md5(keyword.lower().encode()).hexdigest()
    )
```

---

## 8. De-duplication Strategy

### Fuzzy Matching Algorithm

```python
from difflib import SequenceMatcher
from typing import List

class TrendDeduplicator:
    def __init__(self, similarity_threshold=0.85):
        self.threshold = similarity_threshold
        self.seen = {}
    
    def deduplicate(self, trends: List[NormalizedTrend]) -> List[NormalizedTrend]:
        """Remove duplicates and merge scores"""
        unique_trends = []
        
        for trend in sorted(trends, key=lambda t: t.score, reverse=True):
            # Find similar existing trends
            similar_trend = self._find_similar(trend, unique_trends)
            
            if similar_trend:
                # Merge with existing
                self._merge_trends(similar_trend, trend)
            else:
                # Add as new unique trend
                unique_trends.append(trend)
        
        return unique_trends
    
    def _find_similar(self, trend: NormalizedTrend, 
                      trends: List[NormalizedTrend]) -> Optional[NormalizedTrend]:
        """Find similar trend using fuzzy matching"""
        keyword_lower = trend.keyword.lower()
        
        for existing in trends:
            # Exact hash match
            if trend.content_hash == existing.content_hash:
                return existing
            
            # Fuzzy string match
            similarity = SequenceMatcher(
                None, 
                keyword_lower, 
                existing.keyword.lower()
            ).ratio()
            
            if similarity >= self.threshold:
                return existing
        
        return None
    
    def _merge_trends(self, existing: NormalizedTrend, new: NormalizedTrend):
        """Merge new trend into existing"""
        # Keep highest score
        if new.score > existing.score:
            existing.score = new.score
        
        # Combine hashtags
        existing.hashtags = list(set(
            (existing.hashtags or []) + (new.hashtags or [])
        ))
        
        # Add source if different
        if new.source != existing.source:
            existing.raw_data['sources'] = list(set(
                existing.raw_data.get('sources', [existing.source]) + [new.source]
            ))
        
        # Aggregate metrics
        existing.views = max(existing.views, new.views)
        existing.likes += new.likes
        existing.shares += new.shares
        existing.comments += new.comments
```

### Cross-Platform Keyword Mapping

```python
# Common themes across platforms
KEYWORD_MAPPINGS = {
    'ai': ['artificial intelligence', 'chatgpt', 'machine learning', 'ai tool'],
    'crypto': ['cryptocurrency', 'bitcoin', 'blockchain', 'nft'],
    'fitness': ['workout', 'exercise', 'gym', 'fitness motivation'],
    'cooking': ['recipe', 'cooking', 'food', 'meal prep'],
}

def normalize_keyword(keyword: str) -> str:
    """Normalize keyword to canonical form"""
    keyword_lower = keyword.lower().strip()
    
    for canonical, variants in KEYWORD_MAPPINGS.items():
        if any(variant in keyword_lower for variant in variants):
            return canonical
    
    return keyword_lower
```

---

## 9. Trend Score Metrics

### Comprehensive Scoring Formula

```python
def calculate_trend_score(trend: Dict) -> float:
    """
    Calculate comprehensive trend score (0-100)
    
    Formula:
        score = (0.4 * velocity) + (0.3 * volume) + (0.2 * engagement) + (0.1 * recency)
    
    Where:
        velocity   = % change in views over 24h (normalized to 0-100)
        volume     = Absolute views/impressions (normalized to 0-100)
        engagement = Likes + shares + comments rate (normalized to 0-100)
        recency    = How recent the trend is (0-100, fresher = higher)
    """
    
    # 1. Velocity Score (40%)
    velocity = calculate_velocity(trend)
    
    # 2. Volume Score (30%)
    volume = calculate_volume(trend)
    
    # 3. Engagement Score (20%)
    engagement = calculate_engagement(trend)
    
    # 4. Recency Score (10%)
    recency = calculate_recency(trend)
    
    # Weighted sum
    total_score = (
        velocity * 0.4 +
        volume * 0.3 +
        engagement * 0.2 +
        recency * 0.1
    )
    
    return min(max(total_score, 0), 100)  # Clamp to 0-100

def calculate_velocity(trend: Dict) -> float:
    """Calculate velocity score (0-100)"""
    views_current = trend.get('views', 0)
    views_24h_ago = trend.get('views_24h_ago', views_current * 0.8)  # Estimate if missing
    
    if views_24h_ago == 0:
        return 50.0  # Default mid-score for new trends
    
    # Calculate % change
    velocity_percent = ((views_current - views_24h_ago) / views_24h_ago) * 100
    
    # Normalize: 100% growth = 100 score, 0% = 50 score, negative = <50
    if velocity_percent >= 100:
        return 100.0
    elif velocity_percent >= 0:
        return 50 + (velocity_percent / 2)
    else:
        # Negative growth
        return max(50 + velocity_percent, 0)

def calculate_volume(trend: Dict) -> float:
    """Calculate volume score based on absolute views"""
    source = trend.get('source', '')
    views = trend.get('views', 0)
    
    # Platform-specific normalization
    if source == 'youtube':
        # 10M views = 100 score
        max_views = 10_000_000
    elif source == 'tiktok':
        # 50M plays = 100 score (TikTok gets more views)
        max_views = 50_000_000
    elif source == 'instagram':
        # 5M views = 100 score
        max_views = 5_000_000
    else:
        # Default
        max_views = 10_000_000
    
    # Logarithmic scale (1M = 60, 10M = 100)
    if views == 0:
        return 0
    
    import math
    score = (math.log10(views) / math.log10(max_views)) * 100
    return min(score, 100)

def calculate_engagement(trend: Dict) -> float:
    """Calculate engagement score"""
    views = trend.get('views', 1)  # Avoid division by zero
    likes = trend.get('likes', 0)
    shares = trend.get('shares', 0)
    comments = trend.get('comments', 0)
    
    # Engagement rate = (likes + 2*shares + 3*comments) / views
    # Shares and comments weighted more as they indicate stronger engagement
    engagement_points = likes + (shares * 2) + (comments * 3)
    engagement_rate = (engagement_points / views) * 100
    
    # Normalize: 10% engagement rate = 100 score
    score = min(engagement_rate / 0.1, 100)
    return score

def calculate_recency(trend: Dict) -> float:
    """Calculate recency score (fresher = higher)"""
    from datetime import datetime, timedelta
    
    timestamp = trend.get('timestamp')
    if not timestamp:
        return 50.0  # Default mid-score
    
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    
    age_hours = (datetime.utcnow() - timestamp).total_seconds() / 3600
    
    # Score decreases over time
    # 0-6 hours: 100 score
    # 24 hours: 75 score
    # 48 hours: 50 score
    # 72+ hours: <50 score
    
    if age_hours <= 6:
        return 100.0
    elif age_hours <= 24:
        return 100 - ((age_hours - 6) / 18) * 25
    elif age_hours <= 48:
        return 75 - ((age_hours - 24) / 24) * 25
    else:
        return max(50 - ((age_hours - 48) / 24) * 10, 0)
```

### Score Examples

```
Example 1: Viral Breakout
- Views: 5M (current), 500K (24h ago) → Velocity: 100
- Volume: 5M → Volume: 84
- Engagement: 500K likes, 50K shares → Engagement: 95
- Age: 3 hours → Recency: 100
- **Total Score: 94.5**

Example 2: Steady Popular
- Views: 20M (current), 19M (24h ago) → Velocity: 52.6
- Volume: 20M → Volume: 100
- Engagement: 1M likes → Engagement: 50
- Age: 48 hours → Recency: 50
- **Total Score: 68.0**

Example 3: Declining Trend
- Views: 1M (current), 1.5M (24h ago) → Velocity: 16.7
- Volume: 1M → Volume: 60
- Engagement: 50K likes → Engagement: 50
- Age: 72 hours → Recency: 40
- **Total Score: 45.7**
```

---

## 10. Implementation Roadmap

### Week 1: Foundation
- [x] Google Trends processor (already implemented)
- [ ] SQLite database schema
- [ ] YouTube Data API integration
- [ ] Basic normalization

### Week 2: Aggregation
- [ ] Trend aggregator class
- [ ] De-duplication logic
- [ ] Scoring system implementation
- [ ] Storage layer

### Week 3: Optimization
- [ ] Velocity tracking
- [ ] Historical data retention
- [ ] Rate limiting
- [ ] Error handling

### Week 4: Integration
- [ ] Connect to ideas generator
- [ ] Content suggestion pipeline
- [ ] Testing with real data
- [ ] Documentation

### Optional: TikTok (Week 5+)
- [ ] Evaluate RapidAPI options
- [ ] Budget approval
- [ ] Implementation if approved

---

## Configuration File

```json
{
  "viral_video_config": {
    "scope": {
      "generate_videos": true,
      "generate_keywords": true,
      "generate_hashtags": true
    },
    "regions": [
      {"code": "US", "locale": "en-US", "preference": 40},
      {"code": "CZ", "locale": "cs-CZ", "preference": 20},
      {"code": "UK", "locale": "en-GB", "preference": 15},
      {"code": "CA", "locale": "en-CA", "preference": 15},
      {"code": "AU", "locale": "en-AU", "preference": 10}
    ],
    "cadence": {
      "google_trends": {"frequency": "daily", "hour": 3},
      "youtube_trending": {"frequency": "daily", "hour": 4},
      "youtube_search": {"frequency": "hourly", "peak_hours": [9, 23]},
      "tiktok": {"frequency": "hourly", "peak_hours": [9, 23]}
    },
    "limits": {
      "max_items_per_source": 100,
      "max_requests_per_run": 10,
      "max_storage_items": 10000,
      "pagination_duplicate_threshold": 0.3
    },
    "storage": {
      "type": "sqlite",
      "path": "Generator/trends/data/trends.db",
      "retention_days": 30,
      "archive_to_parquet": true
    },
    "scoring": {
      "velocity_weight": 0.4,
      "volume_weight": 0.3,
      "engagement_weight": 0.2,
      "recency_weight": 0.1,
      "min_score_threshold": 50
    },
    "deduplication": {
      "similarity_threshold": 0.85,
      "merge_strategy": "highest_score"
    }
  }
}
```

---

**Last Updated:** 2025-01-06  
**Status:** Specification Complete - Ready for Implementation  
**Next Step:** Implement YouTube Data API integration
