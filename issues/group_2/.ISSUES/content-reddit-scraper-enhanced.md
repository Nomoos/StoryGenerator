# Content Pipeline: Enhanced Reddit Scraper

**Group:** group_2  
**Priority:** P1 (High)  
**Status:** 📋 Not Started  
**Estimated Effort:** 4-6 hours  

## Description

Enhance Reddit content scraping with better filtering, rate limiting, and multi-subreddit support. Implement incremental updates and duplicate detection.

## Acceptance Criteria

- [ ] Multi-subreddit scraping support
- [ ] Incremental updates (fetch only new content)
- [ ] Duplicate detection across scrapes
- [ ] Rate limiting compliance with Reddit API
- [ ] Content quality filtering (score, length, engagement)
- [ ] JSON output with full metadata
- [ ] Unit tests with mocked Reddit API

## Dependencies

- Install: `praw>=7.7.0` (Python Reddit API Wrapper)
- Requires: `infrastructure-configuration` from Group 1 (for API credentials)
- Can work in parallel with other Group 2 tasks

## Implementation Notes

Create `core/pipeline/reddit_scraper.py`:

```python
import praw
from datetime import datetime, timedelta
from typing import List, Dict
from core.config import settings

class EnhancedRedditScraper:
    def __init__(self, subreddits: List[str]):
        self.reddit = praw.Reddit(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent=settings.reddit_user_agent
        )
        self.subreddits = subreddits
        self.seen_ids = set()
    
    def scrape_recent(self, time_filter: str = "day", limit: int = 100) -> List[Dict]:
        """Scrape recent posts from configured subreddits"""
        posts = []
        
        for subreddit_name in self.subreddits:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            for post in subreddit.top(time_filter=time_filter, limit=limit):
                if post.id in self.seen_ids:
                    continue
                
                if self._is_quality_content(post):
                    posts.append(self._extract_post_data(post))
                    self.seen_ids.add(post.id)
        
        return posts
    
    def _is_quality_content(self, post) -> bool:
        """Filter for quality content"""
        return (
            post.score >= 100 and
            len(post.selftext) >= 200 and
            post.num_comments >= 10
        )
```

## Output Files

**Directory:** `data/content/reddit/{date}/`
**File:** `scraped_posts.json`

## Links

- Related: [HYBRID_ROADMAP.md](../../../docs/roadmaps/HYBRID_ROADMAP.md)
- Completed work: [group-1-content-pipeline](../../resolved/phase-3-implementation/group-1-content-pipeline/)
