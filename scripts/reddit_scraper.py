#!/usr/bin/env python3
"""
Reddit Story Scraper for StoryGenerator

Mines stories from target subreddits filtered by demographics.
Enhanced with incremental scraping, persistent deduplication, and improved rate limiting.
"""

import json
import os
import sqlite3
import sys
import time
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Optional

import praw
from praw.exceptions import PRAWException

# Subreddit mapping by segment and age
SUBREDDIT_MAP: dict[str, list[str]] = {
    "women/10-13": ["r/TrueOffMyChest", "r/relationships", "r/AmItheAsshole"],
    "women/14-17": ["r/teenagers", "r/AmItheAsshole", "r/TrueOffMyChest"],
    "women/18-23": ["r/relationships", "r/dating_advice", "r/confession"],
    "men/10-13": ["r/teenagers", "r/stories", "r/confession"],
    "men/14-17": ["r/teenagers", "r/confession", "r/TrueOffMyChest"],
    "men/18-23": ["r/relationships", "r/AskMen", "r/confession"],
}

# Default quality thresholds by age bucket (can be overridden in config)
QUALITY_THRESHOLDS = {
    "10-13": {"min_upvotes": 300, "min_comments": 20, "min_text_length": 100},
    "14-17": {"min_upvotes": 400, "min_comments": 30, "min_text_length": 150},
    "18-23": {"min_upvotes": 500, "min_comments": 40, "min_text_length": 200},
}


class DuplicateTracker:
    """Persistent duplicate tracking using SQLite."""

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            root_dir = Path(__file__).parent.parent
            data_dir = root_dir / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = data_dir / "reddit_scraper_duplicates.db"
        
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS seen_posts (
                post_id TEXT PRIMARY KEY,
                title TEXT,
                subreddit TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                scrape_count INTEGER DEFAULT 1
            )
        """)
        conn.commit()
        conn.close()

    def is_duplicate(self, post_id: str, title: str, subreddit: str) -> bool:
        """Check if post has been seen before."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT post_id FROM seen_posts WHERE post_id = ?",
            (post_id,)
        )
        exists = cursor.fetchone() is not None
        
        if exists:
            # Update scrape count
            conn.execute(
                "UPDATE seen_posts SET scrape_count = scrape_count + 1 WHERE post_id = ?",
                (post_id,)
            )
        else:
            # Record new post
            conn.execute(
                "INSERT INTO seen_posts (post_id, title, subreddit) VALUES (?, ?, ?)",
                (post_id, title, subreddit)
            )
        
        conn.commit()
        conn.close()
        return exists

    def get_stats(self) -> dict:
        """Get duplicate tracking statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT COUNT(*), AVG(scrape_count) FROM seen_posts")
        total, avg_scrapes = cursor.fetchone()
        conn.close()
        return {
            "total_seen": total or 0,
            "avg_scrapes": round(avg_scrapes or 0, 2)
        }


class ScraperState:
    """Manages incremental scraping state."""

    def __init__(self, state_file: Optional[Path] = None):
        if state_file is None:
            root_dir = Path(__file__).parent.parent
            data_dir = root_dir / "data"
            data_dir.mkdir(exist_ok=True)
            state_file = data_dir / "reddit_scraper_state.json"
        
        self.state_file = state_file
        self.last_scraped = self._load_state()

    def _load_state(self) -> dict:
        """Load last scrape timestamps per subreddit."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_state(self):
        """Save current scrape timestamps."""
        with open(self.state_file, 'w') as f:
            json.dump(self.last_scraped, f, indent=2)

    def get_last_scrape_time(self, subreddit: str) -> float:
        """Get last scrape timestamp for a subreddit."""
        return self.last_scraped.get(subreddit, 0)

    def update_scrape_time(self, subreddit: str, timestamp: float):
        """Update scrape timestamp for a subreddit."""
        self.last_scraped[subreddit] = timestamp
        self._save_state()


def rate_limit_with_backoff(max_retries: int = 3, base_delay: int = 5):
    """Decorator for rate limiting with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except PRAWException as e:
                    error_str = str(e).lower()
                    if "rate limit" in error_str or "429" in error_str:
                        if attempt < max_retries - 1:
                            delay = base_delay * (2 ** attempt)
                            print(f"⚠️  Rate limited. Waiting {delay}s before retry (attempt {attempt + 1}/{max_retries})...")
                            time.sleep(delay)
                        else:
                            print(f"❌ Rate limit exceeded after {max_retries} retries")
                            raise
                    else:
                        raise
            return None
        return wrapper
    return decorator


def init_reddit() -> praw.Reddit:
    """Initialize Reddit API client."""
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("❌ Error: Reddit API credentials not found!")
        print("Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables.")
        print("You can get credentials from: https://www.reddit.com/prefs/apps")
        sys.exit(1)

    return praw.Reddit(
        client_id=client_id, client_secret=client_secret, user_agent="StoryGenerator/2.0 (Enhanced)"
    )


@rate_limit_with_backoff(max_retries=3, base_delay=5)
def scrape_subreddit(
    reddit: praw.Reddit, 
    subreddit_name: str, 
    limit: int = 100, 
    min_upvotes: int = 500,
    duplicate_tracker: Optional[DuplicateTracker] = None,
    use_incremental: bool = False,
    last_scrape_time: float = 0
) -> list[dict[str, str | int]]:
    """Scrape top posts from a subreddit with enhanced filtering."""
    stories = []
    subreddit = reddit.subreddit(subreddit_name.replace("r/", ""))

    # Choose scraping strategy
    if use_incremental and last_scrape_time > 0:
        # Incremental: get new posts only
        post_iterator = subreddit.new(limit=limit)
        print(f"   📥 Fetching new posts since last scrape...")
    else:
        # Full scrape: get top posts from last week
        post_iterator = subreddit.top(time_filter="week", limit=limit)
        print(f"   📥 Fetching top posts from last week...")

    posts_checked = 0
    posts_filtered = 0
    posts_duplicates = 0
    
    for post in post_iterator:
        posts_checked += 1
        
        # Stop if we've reached old content in incremental mode
        if use_incremental and post.created_utc <= last_scrape_time:
            print(f"   ⏹️  Reached previously scraped content")
            break
        
        # Filter by engagement
        if post.score < min_upvotes:
            posts_filtered += 1
            continue

        # Check for duplicates
        if duplicate_tracker and duplicate_tracker.is_duplicate(post.id, post.title, subreddit_name):
            posts_duplicates += 1
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
            "created_utc_timestamp": post.created_utc,
            "subreddit": subreddit_name,
            "author": str(post.author) if post.author else "[deleted]",
            "awards": post.total_awards_received,
            "is_self": post.is_self,
        }

        # Add top 5 comments for context
        try:
            post.comments.replace_more(limit=0)
            story["top_comments"] = [
                {"text": comment.body, "score": comment.score} for comment in list(post.comments)[:5]
            ]
        except Exception as e:
            print(f"   ⚠️  Failed to fetch comments: {e}")
            story["top_comments"] = []

        stories.append(story)

    print(f"   📊 Checked: {posts_checked}, Accepted: {len(stories)}, Filtered: {posts_filtered}, Duplicates: {posts_duplicates}")
    return stories


def filter_age_appropriate(
    stories: list[dict[str, str | int]], 
    age_bucket: str,
    min_text_length: Optional[int] = None,
    apply_quality_threshold: bool = False
) -> list[dict[str, str | int]]:
    """Filter stories for age-appropriateness and quality.
    
    Args:
        stories: List of story dictionaries
        age_bucket: Age bucket string (e.g., "10-13")
        min_text_length: Minimum text length (None = no filtering for backward compatibility)
        apply_quality_threshold: If True and min_text_length is None, use threshold from config
    """
    # Simple keyword filtering (enhance with ML model later)
    inappropriate_keywords: dict[str, list[str]] = {
        "10-13": ["sex", "drugs", "violence", "nsfw", "explicit"],
        "14-17": ["explicit", "nsfw"],
        "18-23": [],  # No filtering for adults
    }

    keywords = inappropriate_keywords.get(age_bucket, [])
    
    # Determine text length threshold
    effective_min_length = 0
    if min_text_length is not None:
        effective_min_length = min_text_length
    elif apply_quality_threshold:
        effective_min_length = QUALITY_THRESHOLDS.get(age_bucket, {}).get("min_text_length", 0)

    filtered: list[dict[str, str | int]] = []
    for story in stories:
        text_lower = (str(story["title"]) + " " + str(story["text"])).lower()
        
        # Check inappropriate keywords
        if keywords and any(kw in text_lower for kw in keywords):
            continue
        
        # Check minimum text length (skip if 0)
        if effective_min_length > 0:
            text_content = str(story.get("text", ""))
            if len(text_content) < effective_min_length:
                continue
        
        filtered.append(story)

    return filtered


def scrape_segment(
    reddit: praw.Reddit, 
    gender: str, 
    age: str,
    use_incremental: bool = True,
    use_duplicate_tracking: bool = True
) -> dict[str, str | list[dict[str, str | int]] | dict]:
    """Scrape all stories for a segment with enhanced features."""
    segment_key = f"{gender}/{age}"
    subreddits = SUBREDDIT_MAP.get(segment_key, [])
    
    # Get quality thresholds for this age bucket
    thresholds = QUALITY_THRESHOLDS.get(age, {})
    min_upvotes = thresholds.get("min_upvotes", 500)
    min_text_length = thresholds.get("min_text_length", 100)
    
    # Initialize trackers
    duplicate_tracker = DuplicateTracker() if use_duplicate_tracking else None
    scraper_state = ScraperState() if use_incremental else None

    all_stories: list[dict[str, str | int]] = []
    scrape_stats = {
        "total_checked": 0,
        "total_accepted": 0,
        "total_filtered": 0,
        "total_duplicates": 0
    }
    
    for subreddit in subreddits:
        print(f"📥 Scraping {subreddit} for {segment_key}...")
        
        last_scrape_time = scraper_state.get_last_scrape_time(subreddit) if scraper_state else 0
        
        try:
            stories = scrape_subreddit(
                reddit, 
                subreddit, 
                min_upvotes=min_upvotes,
                duplicate_tracker=duplicate_tracker,
                use_incremental=use_incremental,
                last_scrape_time=last_scrape_time
            )
            all_stories.extend(stories)
            
            # Update scrape time with newest post
            if scraper_state and stories:
                newest_timestamp = max(s["created_utc_timestamp"] for s in stories)
                scraper_state.update_scrape_time(subreddit, newest_timestamp)
            
            # Respect rate limits
            time.sleep(2)
            
        except Exception as e:
            print(f"⚠️  Error scraping {subreddit}: {e}")
            continue

    # Filter for age-appropriateness and quality
    filtered_stories = filter_age_appropriate(
        all_stories, age, min_text_length=min_text_length, apply_quality_threshold=True
    )

    # Sort by engagement
    filtered_stories.sort(key=lambda x: x["upvotes"] + x["num_comments"], reverse=True)

    # Take top 100
    top_stories = filtered_stories[:100]
    
    # Get duplicate tracker stats
    dup_stats = duplicate_tracker.get_stats() if duplicate_tracker else {"total_seen": 0, "avg_scrapes": 0}

    result = {
        "segment": gender,
        "age_bucket": age,
        "subreddits": subreddits,
        "quality_thresholds": thresholds,
        "total_scraped": len(all_stories),
        "after_filtering": len(filtered_stories),
        "selected": len(top_stories),
        "scraped_at": datetime.now().isoformat(),
        "incremental_mode": use_incremental,
        "duplicate_tracking": use_duplicate_tracking,
        "duplicate_stats": dup_stats,
        "stories": top_stories,
    }

    return result


def main():
    """Main scraper entry point."""
    print("=" * 60)
    print("Reddit Story Scraper for StoryGenerator (Enhanced)")
    print("=" * 60)
    print()
    
    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Enhanced Reddit Story Scraper")
    parser.add_argument("--segment", help="Specific segment (e.g., 'women')")
    parser.add_argument("--age", help="Specific age (e.g., '18-23')")
    parser.add_argument("--no-incremental", action="store_true", help="Disable incremental scraping")
    parser.add_argument("--no-dedup", action="store_true", help="Disable duplicate tracking")
    parser.add_argument("--force-full", action="store_true", help="Force full scrape (alias for --no-incremental)")
    args = parser.parse_args()
    
    use_incremental = not (args.no_incremental or args.force_full)
    use_dedup = not args.no_dedup
    
    print(f"📋 Configuration:")
    print(f"   Incremental scraping: {'✅ Enabled' if use_incremental else '❌ Disabled'}")
    print(f"   Duplicate tracking: {'✅ Enabled' if use_dedup else '❌ Disabled'}")
    print()

    reddit = init_reddit()

    # Determine which segments to process
    if args.segment and args.age:
        genders = [args.segment]
        ages = [args.age]
        print(f"🎯 Processing single segment: {args.segment}/{args.age}")
    else:
        genders = ["women", "men"]
        ages = ["10-13", "14-17", "18-23"]
        print(f"🎯 Processing all segments")
    print()

    # Get root directory (parent of scripts)
    root_dir = Path(__file__).parent.parent

    for gender in genders:
        for age in ages:
            print(f"\n🎯 Processing {gender}/{age}...")

            data = scrape_segment(
                reddit, 
                gender, 
                age,
                use_incremental=use_incremental,
                use_duplicate_tracking=use_dedup
            )

            # Save to file
            output_dir = root_dir / "Generator" / "sources" / "reddit" / gender / age
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d")
            output_file = output_dir / f"{timestamp}_reddit_stories.json"

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Saved {len(data['stories'])} stories to {output_file}")
            if use_dedup:
                dup_stats = data.get("duplicate_stats", {})
                print(f"   📊 Duplicate stats: {dup_stats.get('total_seen', 0)} total seen, {dup_stats.get('avg_scrapes', 0)} avg scrapes")

    print("\n" + "=" * 60)
    print("✨ Reddit scraping complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
