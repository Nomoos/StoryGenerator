# Content Pipeline: Alternative Social Media Sources

**Group:** group_2  
**Priority:** P1 (High)  
**Status:** 📋 Not Started  
**Estimated Effort:** 6-8 hours  

## Description

Implement content collection from alternative social media sources (Instagram, TikTok) using official APIs and web scraping where appropriate. Diversify content sources beyond Reddit.

## Acceptance Criteria

- [ ] Instagram story scraping (public accounts)
- [ ] TikTok video description scraping
- [ ] Content normalization to common format
- [ ] Deduplication across all sources
- [ ] Rate limiting for each platform
- [ ] Compliance with platform ToS
- [ ] Unit tests with mocked API responses

## Dependencies

- Install: `instagrapi>=1.16.0 TikTokApi>=5.0.0`
- Requires: `infrastructure-configuration` from Group 1
- Can work in parallel with other Group 2 tasks

## Implementation Notes

Create `core/pipeline/social_scraper.py`:

```python
from instagrapi import Client
from TikTokApi import TikTokApi
from typing import List, Dict

class SocialMediaScraper:
    def __init__(self):
        self.instagram = Client()
        self.tiktok = TikTokApi()
    
    async def scrape_instagram(self, hashtags: List[str]) -> List[Dict]:
        """Scrape Instagram content by hashtags"""
        posts = []
        
        for hashtag in hashtags:
            medias = self.instagram.hashtag_medias_recent(hashtag, amount=50)
            
            for media in medias:
                if media.caption_text and len(media.caption_text) >= 100:
                    posts.append({
                        "source": "instagram",
                        "id": media.id,
                        "content": media.caption_text,
                        "engagement": media.like_count + media.comment_count,
                        "url": f"https://instagram.com/p/{media.code}/"
                    })
        
        return posts
    
    async def scrape_tiktok(self, keywords: List[str]) -> List[Dict]:
        """Scrape TikTok content by keywords"""
        videos = []
        
        async with self.tiktok:
            for keyword in keywords:
                results = await self.tiktok.search.videos(keyword, count=50)
                
                for video in results:
                    if video.desc and len(video.desc) >= 50:
                        videos.append({
                            "source": "tiktok",
                            "id": video.id,
                            "content": video.desc,
                            "engagement": video.stats.digg_count + video.stats.comment_count,
                            "url": f"https://tiktok.com/@{video.author.unique_id}/video/{video.id}"
                        })
        
        return videos
    
    def normalize_content(self, posts: List[Dict]) -> List[Dict]:
        """Normalize content from different sources"""
        # Standardize format across all sources
        pass
```

## Output Files

**Directory:** `data/content/social/{date}/`
**Files:**
- `instagram_posts.json`
- `tiktok_posts.json`
- `normalized_content.json`

## Links

- Related: [HYBRID_ROADMAP.md](../../../docs/roadmaps/HYBRID_ROADMAP.md)
- Related: [PHASE_ORGANIZATION.md](../../atomic/PHASE_ORGANIZATION.md)
