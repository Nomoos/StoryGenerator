# Content: Reddit Story Scraper

**ID:** `02-content-01`  
**Priority:** P0 (Critical Path)  
**Effort:** 4-6 hours  
**Status:** Not Started

## Overview

Implement Reddit story scraper using PRAW (Python Reddit API Wrapper) to mine stories from target subreddits filtered by segment and age demographics.

## Dependencies

**Requires:**
- `00-setup-01`: Folder structure (need `/sources/reddit/` folders)
- `00-setup-02`: Config files (need Reddit API credentials)

**Blocks:**
- `03-ideas-01`: Reddit story adaptation (needs scraped stories)
- `02-content-03`: Quality scorer (needs stories to score)

## Acceptance Criteria

- [ ] PRAW library installed and configured
- [ ] Reddit API authentication working
- [ ] 18 target subreddits defined (6 segments × 3 age buckets)
- [ ] Scraper fetches top 50-100 posts per subreddit
- [ ] Content filtered by upvotes (500+), engagement, age-appropriateness
- [ ] Output JSON saved to `/sources/reddit/{segment}/{age}/`
- [ ] Script runs successfully for all 6 segments
- [ ] Documentation and usage examples provided

## Task Details

### Target Subreddits by Segment/Age

```python
SUBREDDIT_MAP = {
    "women/10-13": ["r/TrueOffMyChest", "r/relationships", "r/AmItheAsshole"],
    "women/14-17": ["r/teenagers", "r/AmItheAsshole", "r/TrueOffMyChest"],
    "women/18-23": ["r/relationships", "r/dating_advice", "r/confession"],
    "men/10-13": ["r/teenagers", "r/stories", "r/confession"],
    "men/14-17": ["r/teenagers", "r/confession", "r/TrueOffMyChest"],
    "men/18-23": ["r/relationships", "r/AskMen", "r/confession"],
}
```

### Implementation

```python
#!/usr/bin/env python3
"""
Reddit Story Scraper for StoryGenerator

Mines stories from target subreddits filtered by demographics.
"""

import praw
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import os

def init_reddit() -> praw.Reddit:
    """Initialize Reddit API client."""
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="StoryGenerator/1.0"
    )

def scrape_subreddit(reddit: praw.Reddit, subreddit_name: str, 
                     limit: int = 100, min_upvotes: int = 500) -> List[Dict]:
    """Scrape top posts from a subreddit."""
    stories = []
    subreddit = reddit.subreddit(subreddit_name.replace("r/", ""))
    
    # Get top posts from last week
    for post in subreddit.top(time_filter="week", limit=limit):
        # Filter by engagement
        if post.score < min_upvotes:
            continue
        
        # Extract story data
        story = {
            "id": post.id,
            "title": post.title,
            "text": post.selftext,
            "url": f"https://reddit.com{post.permalink}",
            "upvotes": post.score,
            "num_comments": post.num_comments,
            "created_utc": datetime.fromtimestamp(post.created_utc).isoformat(),
            "subreddit": subreddit_name,
            "author": str(post.author) if post.author else "[deleted]",
            "awards": post.total_awards_received,
            "is_self": post.is_self,
        }
        
        # Add top 5 comments for context
        post.comments.replace_more(limit=0)
        story["top_comments"] = [
            {
                "text": comment.body,
                "score": comment.score
            }
            for comment in list(post.comments)[:5]
        ]
        
        stories.append(story)
    
    return stories

def filter_age_appropriate(stories: List[Dict], age_bucket: str) -> List[Dict]:
    """Filter stories for age-appropriateness."""
    # Simple keyword filtering (enhance with ML model later)
    inappropriate_keywords = {
        "10-13": ["sex", "drugs", "violence", "nsfw", "explicit"],
        "14-17": ["explicit", "nsfw"],
        "18-23": []  # No filtering for adults
    }
    
    keywords = inappropriate_keywords.get(age_bucket, [])
    if not keywords:
        return stories
    
    filtered = []
    for story in stories:
        text_lower = (story["title"] + " " + story["text"]).lower()
        if not any(kw in text_lower for kw in keywords):
            filtered.append(story)
    
    return filtered

def scrape_segment(reddit: praw.Reddit, gender: str, age: str) -> Dict:
    """Scrape all stories for a segment."""
    segment_key = f"{gender}/{age}"
    subreddits = SUBREDDIT_MAP.get(segment_key, [])
    
    all_stories = []
    for subreddit in subreddits:
        print(f"📥 Scraping {subreddit} for {segment_key}...")
        stories = scrape_subreddit(reddit, subreddit)
        all_stories.extend(stories)
    
    # Filter for age-appropriateness
    filtered_stories = filter_age_appropriate(all_stories, age)
    
    # Sort by engagement
    filtered_stories.sort(key=lambda x: x["upvotes"] + x["num_comments"], reverse=True)
    
    # Take top 100
    top_stories = filtered_stories[:100]
    
    result = {
        "segment": gender,
        "age_bucket": age,
        "subreddits": subreddits,
        "total_scraped": len(all_stories),
        "after_filtering": len(filtered_stories),
        "selected": len(top_stories),
        "scraped_at": datetime.now().isoformat(),
        "stories": top_stories
    }
    
    return result

def main():
    """Main scraper entry point."""
    reddit = init_reddit()
    
    genders = ["women", "men"]
    ages = ["10-13", "14-17", "18-23"]
    
    for gender in genders:
        for age in ages:
            print(f"\n🎯 Processing {gender}/{age}...")
            
            data = scrape_segment(reddit, gender, age)
            
            # Save to file
            output_dir = Path(f"Generator/sources/reddit/{gender}/{age}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d")
            output_file = output_dir / f"{timestamp}_reddit_stories.json"
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved {len(data['stories'])} stories to {output_file}")
    
    print("\n✨ Reddit scraping complete!")

if __name__ == "__main__":
    main()
```

### Setup

```bash
# Install PRAW
pip install praw

# Set environment variables
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_secret"

# Or use config file
```

### JSON Output Schema

```json
{
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "subreddits": ["r/subreddit1", "r/subreddit2"],
  "total_scraped": 250,
  "after_filtering": 180,
  "selected": 100,
  "scraped_at": "2024-01-15T10:30:00",
  "stories": [
    {
      "id": "abc123",
      "title": "Story title",
      "text": "Full story text...",
      "url": "https://reddit.com/r/...",
      "upvotes": 1250,
      "num_comments": 340,
      "created_utc": "2024-01-10T15:20:00",
      "subreddit": "r/relationships",
      "author": "username",
      "awards": 5,
      "is_self": true,
      "top_comments": [
        {"text": "Comment text", "score": 450}
      ]
    }
  ]
}
```

## Output Files

- `/sources/reddit/{gender}/{age}/YYYYMMDD_reddit_stories.json` - Scraped stories (18 files total)
- `/sources/reddit/scraper_log.txt` - Execution log

## Testing

```bash
# Test single segment
python scripts/reddit_scraper.py --segment women --age 18-23

# Test all segments
python scripts/reddit_scraper.py --all

# Dry run
python scripts/reddit_scraper.py --dry-run
```

## Related Files

- `/config/pipeline.yaml` - Reddit API credentials
- `docs/REDDIT_SCRAPING.md` - Documentation

## Notes

- Respect Reddit API rate limits (60 requests/minute)
- Use time.sleep() between subreddit scrapes
- Handle [deleted] and [removed] posts
- Store raw data for later reprocessing
- Consider GDPR/privacy when storing user data

## Next Steps

After completion:
- Stories available for adaptation (`03-ideas-01`)
- Quality scoring can begin (`02-content-03`)
- Alternative sources can be added in parallel (`02-content-02`)
