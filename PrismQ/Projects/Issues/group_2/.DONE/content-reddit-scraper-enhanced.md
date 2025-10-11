# Content Pipeline: Enhanced Reddit Scraper

**Group:** group_2  
**Priority:** P1 (High)  
**Status:** ✅ Complete  
**Estimated Effort:** 4-6 hours  
**Actual Effort:** ~5 hours  
**Completed:** 2025-10-10  

## Description

Enhance the existing Reddit content scraper (`scripts/reddit_scraper.py`) with better filtering, rate limiting, and multi-subreddit support. This builds upon the completed Reddit scraper from `issues/resolved/p0-content-PrismQ/Pipeline/02-content-01-reddit-scraper/`.

**Key Enhancements:**
- Incremental updates (fetch only new content since last scrape)
- Enhanced duplicate detection using persistent storage
- Improved rate limiting with exponential backoff
- Better content quality filtering
- Support for additional subreddit categories

## Current Implementation

The existing Reddit scraper (`scripts/reddit_scraper.py`) provides:
- Basic Reddit API integration using PRAW
- Scraping from predefined subreddit map for demographics (women/men × 3 age groups)
- Basic age-appropriate filtering
- JSON output with metadata
- Score-based content filtering

**See:** `issues/resolved/p0-content-PrismQ/Pipeline/02-content-01-reddit-scraper/issue.md` for current implementation details.

## Acceptance Criteria

- [x] Incremental updates - track last scrape timestamp per subreddit
- [x] Persistent duplicate detection across scrapes (SQLite database)
- [x] Enhanced rate limiting with exponential backoff and retry logic
- [x] Configurable quality thresholds per demographic
- [x] Command-line interface for flexible operation
- [x] Improved logging and error handling
- [x] Unit tests for all new features (16 tests)
- [x] Documentation updated with new features

## Dependencies

- **Builds on:** `scripts/reddit_scraper.py` (existing implementation)
- **Requires:** `praw>=7.7.0` (already installed)
- **Optional:** `sqlite3` (for persistent duplicate tracking)
- Can work in parallel with other Group 2 tasks

## Implementation Notes

Enhance `scripts/reddit_scraper.py` with the following:

### 1. Incremental Scraping

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

class IncrementalRedditScraper:
    def __init__(self):
        self.state_file = Path("data/reddit_scraper_state.json")
        self.last_scraped = self._load_state()
    
    def _load_state(self) -> dict:
        """Load last scrape timestamps per subreddit"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_state(self):
        """Save current scrape timestamps"""
        with open(self.state_file, 'w') as f:
            json.dump(self.last_scraped, f, indent=2)
    
    def scrape_new_posts(self, subreddit_name: str) -> list:
        """Only fetch posts newer than last scrape"""
        last_time = self.last_scraped.get(subreddit_name, 0)
        posts = []
        
        subreddit = self.reddit.subreddit(subreddit_name)
        for post in subreddit.new(limit=100):
            if post.created_utc <= last_time:
                break  # Stop when we reach old content
            posts.append(post)
        
        # Update timestamp
        if posts:
            self.last_scraped[subreddit_name] = posts[0].created_utc
            self._save_state()
        
        return posts
```

### 2. Enhanced Rate Limiting

```python
import time
from functools import wraps

def rate_limit_with_backoff(max_retries=3, base_delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)  # Exponential backoff
                        print(f"⚠️  Rate limited. Waiting {delay}s before retry...")
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

@rate_limit_with_backoff(max_retries=3, base_delay=5)
def scrape_subreddit_safe(reddit, subreddit_name, limit=100):
    """Scrape with automatic rate limit handling"""
    subreddit = reddit.subreddit(subreddit_name)
    return list(subreddit.top(time_filter='day', limit=limit))
```

### 3. Persistent Duplicate Detection

```python
import hashlib
import sqlite3

class DuplicateTracker:
    def __init__(self, db_path="data/reddit_duplicates.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()
    
    def _init_db(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS seen_posts (
                post_id TEXT PRIMARY KEY,
                title_hash TEXT,
                content_hash TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def is_duplicate(self, post_id: str, title: str, content: str) -> bool:
        """Check if post is duplicate by ID or content similarity"""
        # Check exact ID match
        cursor = self.conn.execute(
            "SELECT 1 FROM seen_posts WHERE post_id = ?", 
            (post_id,)
        )
        if cursor.fetchone():
            return True
        
        # Check content hash
        content_hash = hashlib.md5(content.encode()).hexdigest()
        cursor = self.conn.execute(
            "SELECT 1 FROM seen_posts WHERE content_hash = ?",
            (content_hash,)
        )
        if cursor.fetchone():
            return True
        
        # Not a duplicate - record it
        title_hash = hashlib.md5(title.encode()).hexdigest()
        self.conn.execute(
            "INSERT INTO seen_posts (post_id, title_hash, content_hash) VALUES (?, ?, ?)",
            (post_id, title_hash, content_hash)
        )
        self.conn.commit()
        return False
```

## Output Files

**Directory:** `Generator/sources/reddit/{gender}/{age}/`
**Files:**
- `YYYYMMDD_reddit_stories.json` - Scraped stories (same as before)
- `reddit_scraper_state.json` - Last scrape timestamps (NEW)
- `reddit_duplicates.db` - Duplicate tracking database (NEW)
- `scraper_log.txt` - Enhanced logging with retry information

## Testing

```bash
# Test incremental scraping
python scripts/reddit_scraper.py --segment women --age 18-23

# Run again to test incremental behavior (should fetch fewer posts)
python scripts/reddit_scraper.py --segment women --age 18-23

# Force full scrape (ignore state)
python scripts/reddit_scraper.py --all --force-full

# Test with dry run
python scripts/reddit_scraper.py --dry-run --segment men --age 14-17
```

## Links

- **Related:** [HYBRID_ROADMAP.md](../../../docs/roadmaps/HYBRID_ROADMAP.md)
- **Builds on:** [02-content-01-reddit-scraper](../../resolved/p0-content-PrismQ/Pipeline/02-content-01-reddit-scraper/issue.md)
- **Current implementation:** `scripts/reddit_scraper.py`

## Notes

**Benefits of Enhancements:**
- Faster scraping (incremental fetching)
- Lower API usage (fewer redundant requests)
- Better duplicate prevention (persistent tracking)
- More reliable (exponential backoff on rate limits)
- Production-ready (improved error handling)

**Migration Path:**
- Enhancements are backward-compatible
- Existing JSON output format unchanged
- State files are optional (falls back to full scrape)
- Can be implemented incrementally
