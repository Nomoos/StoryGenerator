# Content Pipeline: Alternative Social Media Sources (Instagram & TikTok)

**Group:** group_2  
**Priority:** P1 (High)  
**Status:** 📋 Not Started  
**Estimated Effort:** 6-8 hours  

## Description

Expand alternative content sources beyond Quora and Twitter by adding Instagram and TikTok scrapers. This builds upon the completed alternative sources work in `issues/resolved/p0-content-pipeline/02-content-02-alt-sources/`.

**Current Implementation:**
- ✅ Quora scraper (questions and answers)
- ✅ Twitter/X scraper (story threads)
- ✅ Base scraper interface

**New Additions:**
- 📋 Instagram scraper (stories from hashtags/accounts)
- 📋 TikTok scraper (video descriptions and captions)

## Current Implementation

The existing alternative sources system (`scripts/scrapers/`) provides:
- Base scraper interface for consistency
- Quora scraper for questions and answers
- Twitter/X scraper for story threads
- Age-appropriate content filtering
- Unified CLI for batch scraping
- Mock data implementations for testing

**See:** `issues/resolved/p0-content-pipeline/02-content-02-alt-sources/issue.md` for current implementation details.

## Acceptance Criteria

- [ ] Instagram scraper implemented following BaseScraper interface
- [ ] TikTok scraper implemented following BaseScraper interface
- [ ] Content normalization to match existing format
- [ ] Age-appropriate content filtering applied
- [ ] Integration with existing unified CLI (`alt_sources_scraper.py`)
- [ ] Rate limiting for each platform
- [ ] Compliance with platform Terms of Service
- [ ] Mock data implementation for testing (production API optional)
- [ ] Unit tests following existing test patterns
- [ ] Documentation updated in scrapers README

## Dependencies

- **Builds on:** `scripts/scrapers/` (existing alternative sources)
- **Install:** `instagrapi>=1.16.0` (Instagram), `TikTokApi>=5.0.0` (TikTok)
- **Requires:** Platform API credentials (optional for mock implementation)
- Can work in parallel with other Group 2 tasks

## Implementation Notes

### 1. Instagram Scraper

Create `scripts/scrapers/instagram_scraper.py`:

```python
from typing import List, Dict
from scripts.scrapers.base_scraper import BaseScraper
from datetime import datetime

# For production: from instagrapi import Client
# For now: Use mock data like other scrapers

class InstagramScraper(BaseScraper):
    """
    Scrapes Instagram content from public hashtags and accounts.
    Currently uses mock data - can be extended with instagrapi for production.
    """
    
    def __init__(self):
        super().__init__()
        # For production:
        # self.client = Client()
        # self.client.login(username, password)
    
    def scrape(self, topic: str, gender: str, age_bucket: str, limit: int = 50) -> List[Dict]:
        """
        Scrape Instagram posts by hashtag
        
        Production would use:
        - hashtag_medias_recent() for hashtag content
        - user_medias() for specific accounts
        - Filter by caption length and engagement
        """
        hashtags = self._get_hashtags_for_segment(topic, gender, age_bucket)
        
        # Mock implementation (replace with actual API calls in production)
        posts = self._generate_mock_instagram_data(hashtags, gender, age_bucket, limit)
        
        return posts
    
    def _get_hashtags_for_segment(self, topic: str, gender: str, age_bucket: str) -> List[str]:
        """Get relevant hashtags for demographic"""
        hashtag_map = {
            "women/18-23": ["#relationshipstories", "#storytime", "#confessiontime"],
            "women/14-17": ["#teenlife", "#schoolstories", "#teenconfessions"],
            "women/10-13": ["#kidstories", "#middleschool", "#friendshipstories"],
            "men/18-23": ["#brocode", "#gamingstories", "#collegelife"],
            "men/14-17": ["#teenboys", "#sportsstories", "#schoollife"],
            "men/10-13": ["#boystories", "#adventuretime", "#friendstories"]
        }
        segment_key = f"{gender}/{age_bucket}"
        return hashtag_map.get(segment_key, [f"#{topic}"])
    
    def _generate_mock_instagram_data(self, hashtags: List[str], gender: str, 
                                     age_bucket: str, limit: int) -> List[Dict]:
        """Generate mock Instagram data for testing"""
        posts = []
        for i in range(limit):
            posts.append({
                "id": f"instagram_{i+1}",
                "source": "instagram",
                "platform_id": f"ig_{i+1000}",
                "url": f"https://instagram.com/p/ABC{i+100}/",
                "author": f"@user_{i+1}",
                "author_followers": 1000 + (i * 100),
                "caption": self._generate_mock_caption(gender, age_bucket, i),
                "hashtags": hashtags,
                "engagement": {
                    "likes": 500 + (i * 50),
                    "comments": 20 + (i * 2),
                    "shares": 10 + i
                },
                "created_at": datetime.now().isoformat(),
                "media_type": "carousel",  # carousel, photo, video
                "has_story_content": True
            })
        return posts
    
    def _generate_mock_caption(self, gender: str, age_bucket: str, seed: int) -> str:
        """Generate realistic caption for demographic"""
        templates = [
            "Story time! 📖 So this happened last week and I still can't believe it...",
            "You won't BELIEVE what happened today... Thread 🧵👇",
            "Okay so storytime because this is crazy 😱",
            "Real talk: something happened that changed everything...",
        ]
        return templates[seed % len(templates)]
```

### 2. TikTok Scraper

Create `scripts/scrapers/tiktok_scraper.py`:

```python
from typing import List, Dict
from scripts.scrapers.base_scraper import BaseScraper
from datetime import datetime

# For production: from TikTokApi import TikTokApi
# For now: Use mock data

class TikTokScraper(BaseScraper):
    """
    Scrapes TikTok video descriptions and captions.
    Currently uses mock data - can be extended with TikTokApi for production.
    """
    
    def __init__(self):
        super().__init__()
        # For production:
        # self.api = TikTokApi()
    
    def scrape(self, topic: str, gender: str, age_bucket: str, limit: int = 50) -> List[Dict]:
        """
        Scrape TikTok videos by keywords
        
        Production would use:
        - search.videos() for keyword search
        - user.videos() for specific creators
        - trending() for viral content
        """
        keywords = self._get_keywords_for_segment(topic, gender, age_bucket)
        
        # Mock implementation
        videos = self._generate_mock_tiktok_data(keywords, gender, age_bucket, limit)
        
        return videos
    
    def _get_keywords_for_segment(self, topic: str, gender: str, age_bucket: str) -> List[str]:
        """Get relevant keywords for demographic"""
        keyword_map = {
            "women/18-23": ["relationship story", "storytime", "confession"],
            "women/14-17": ["teen life", "school story", "teen drama"],
            "women/10-13": ["friend story", "school life", "tween life"],
            "men/18-23": ["bro story", "college life", "relationship advice"],
            "men/14-17": ["teen boys", "school life", "sports story"],
            "men/10-13": ["kid adventure", "friend story", "school day"]
        }
        segment_key = f"{gender}/{age_bucket}"
        return keyword_map.get(segment_key, [topic])
    
    def _generate_mock_tiktok_data(self, keywords: List[str], gender: str,
                                   age_bucket: str, limit: int) -> List[Dict]:
        """Generate mock TikTok data for testing"""
        videos = []
        for i in range(limit):
            videos.append({
                "id": f"tiktok_{i+1}",
                "source": "tiktok",
                "platform_id": f"tt_{i+5000}",
                "url": f"https://tiktok.com/@user{i+1}/video/{i+1234567890}",
                "author": f"@tiktoker_{i+1}",
                "author_followers": 10000 + (i * 500),
                "description": self._generate_mock_description(gender, age_bucket, i),
                "hashtags": [f"#{kw.replace(' ', '')}" for kw in keywords],
                "sound_name": f"Original Sound - tiktoker_{i+1}",
                "engagement": {
                    "likes": 5000 + (i * 200),
                    "comments": 200 + (i * 10),
                    "shares": 100 + (i * 5),
                    "views": 50000 + (i * 2000)
                },
                "created_at": datetime.now().isoformat(),
                "duration_seconds": 30 + (i % 30),
                "has_story_content": True
            })
        return videos
    
    def _generate_mock_description(self, gender: str, age_bucket: str, seed: int) -> str:
        """Generate realistic TikTok description"""
        templates = [
            "Storytime 📖✨ part 1/3 #storytime #viral",
            "You won't believe what happened 😱 #story #fyp",
            "Real story that changed everything 💯 #truth #real",
            "This actually happened to me 😭 #storytime #real",
        ]
        return templates[seed % len(templates)]
```

### 3. Update Unified CLI

Modify `scripts/scrapers/alt_sources_scraper.py` to include new scrapers:

```python
from scripts.scrapers.quora_scraper import QuoraScraper
from scripts.scrapers.twitter_scraper import TwitterScraper
from scripts.scrapers.instagram_scraper import InstagramScraper  # NEW
from scripts.scrapers.tiktok_scraper import TikTokScraper  # NEW

SCRAPERS = {
    'quora': QuoraScraper,
    'twitter': TwitterScraper,
    'instagram': InstagramScraper,  # NEW
    'tiktok': TikTokScraper,  # NEW
}

# Update help text to include new sources
# Update batch processing to handle new scrapers
```

## Output Files

**Directory:** `src/Generator/sources/{platform}/{gender}/{age_bucket}/`

**New Files:**
- `instagram/{gender}/{age}/YYYYMMDD_instagram_content.json` - Instagram posts (6 files)
- `tiktok/{gender}/{age}/YYYYMMDD_tiktok_content.json` - TikTok videos (6 files)

**Total:** 12 new files (2 platforms × 2 genders × 3 age buckets)

### JSON Output Schema

**Instagram Posts:**
```json
{
  "source": "instagram",
  "gender": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "total_items": 50,
  "scraped_at": "2025-10-10T...",
  "content": [
    {
      "id": "instagram_1",
      "platform_id": "ig_1000",
      "url": "https://instagram.com/p/...",
      "author": "@username",
      "author_followers": 5000,
      "caption": "Story text...",
      "hashtags": ["#storytime", "#viral"],
      "engagement": {
        "likes": 500,
        "comments": 20,
        "shares": 10
      },
      "created_at": "2025-10-10T...",
      "source": "instagram"
    }
  ]
}
```

**TikTok Videos:**
```json
{
  "source": "tiktok",
  "gender": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "total_items": 50,
  "scraped_at": "2025-10-10T...",
  "content": [
    {
      "id": "tiktok_1",
      "platform_id": "tt_5000",
      "url": "https://tiktok.com/@user/video/...",
      "author": "@tiktoker",
      "author_followers": 10000,
      "description": "Storytime 📖✨...",
      "hashtags": ["#storytime", "#viral"],
      "engagement": {
        "likes": 5000,
        "comments": 200,
        "shares": 100,
        "views": 50000
      },
      "created_at": "2025-10-10T...",
      "duration_seconds": 45,
      "source": "tiktok"
    }
  ]
}
```

## Testing

```bash
# Test Instagram scraper
python scripts/scrapers/alt_sources_scraper.py --sources instagram --gender women --age 18-23

# Test TikTok scraper
python scripts/scrapers/alt_sources_scraper.py --sources tiktok --gender men --age 14-17

# Test all sources including new ones
python scripts/scrapers/alt_sources_scraper.py --sources all --all-demographics

# Test just the new platforms
python scripts/scrapers/alt_sources_scraper.py --sources instagram,tiktok --all-demographics
```

## Related Files

- `scripts/scrapers/base_scraper.py` - Base interface (extend this)
- `scripts/scrapers/instagram_scraper.py` - NEW Instagram implementation
- `scripts/scrapers/tiktok_scraper.py` - NEW TikTok implementation
- `scripts/scrapers/alt_sources_scraper.py` - Update to include new scrapers
- `tests/test_alt_sources.py` - Add tests for new scrapers
- `scripts/scrapers/README.md` - Update documentation

## Links

- **Related:** [HYBRID_ROADMAP.md](../../../docs/roadmaps/HYBRID_ROADMAP.md)
- **Builds on:** [02-content-02-alt-sources](../../resolved/p0-content-pipeline/02-content-02-alt-sources/issue.md)
- **Current implementation:** `scripts/scrapers/`

## Notes

### Platform API Considerations

**Instagram:**
- **Library:** `instagrapi` - Unofficial Instagram API
- **Auth:** Requires Instagram account credentials
- **Rate Limits:** ~200 requests/hour (unofficial, varies)
- **ToS Compliance:** Use cautiously, Instagram may block scrapers
- **Alternative:** Instagram Basic Display API (official but limited)

**TikTok:**
- **Library:** `TikTokApi` - Unofficial TikTok API
- **Auth:** No login required for public content
- **Rate Limits:** Varies, implement delays between requests
- **ToS Compliance:** Web scraping, may violate ToS
- **Alternative:** TikTok Content Posting API (official but requires partnership)

### Implementation Strategy

**Phase 1 (Current Task):** Mock data implementation
- Follows existing pattern (Quora, Twitter also use mocks)
- Allows development without API credentials
- Enables testing of downstream pipeline components

**Phase 2 (Future):** Production API integration
- Add actual API calls when credentials available
- Implement proper rate limiting
- Add retry logic and error handling
- Consider proxy rotation if needed

### Content Quality

Both platforms are rich sources of story content:
- **Instagram:** Story-format captions, hashtag discovery
- **TikTok:** High engagement, trending content, younger demographics

### Migration Path

- Mock implementations are sufficient for pipeline development
- Production integration can be added later without breaking changes
- Output format remains consistent regardless of data source
