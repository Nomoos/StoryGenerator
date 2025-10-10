#!/usr/bin/env python3
"""
Reddit Story Scraper for StoryGenerator

Mines stories from target subreddits filtered by demographics.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import praw

# Subreddit mapping by segment and age
SUBREDDIT_MAP: dict[str, list[str]] = {
    "women/10-13": ["r/TrueOffMyChest", "r/relationships", "r/AmItheAsshole"],
    "women/14-17": ["r/teenagers", "r/AmItheAsshole", "r/TrueOffMyChest"],
    "women/18-23": ["r/relationships", "r/dating_advice", "r/confession"],
    "men/10-13": ["r/teenagers", "r/stories", "r/confession"],
    "men/14-17": ["r/teenagers", "r/confession", "r/TrueOffMyChest"],
    "men/18-23": ["r/relationships", "r/AskMen", "r/confession"],
}


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
        client_id=client_id, client_secret=client_secret, user_agent="StoryGenerator/1.0"
    )


def scrape_subreddit(
    reddit: praw.Reddit, subreddit_name: str, limit: int = 100, min_upvotes: int = 500
) -> list[dict[str, str | int]]:
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
            {"text": comment.body, "score": comment.score} for comment in list(post.comments)[:5]
        ]

        stories.append(story)

    return stories


def filter_age_appropriate(stories: list[dict[str, str | int]], age_bucket: str) -> list[dict[str, str | int]]:
    """Filter stories for age-appropriateness."""
    # Simple keyword filtering (enhance with ML model later)
    inappropriate_keywords: dict[str, list[str]] = {
        "10-13": ["sex", "drugs", "violence", "nsfw", "explicit"],
        "14-17": ["explicit", "nsfw"],
        "18-23": [],  # No filtering for adults
    }

    keywords = inappropriate_keywords.get(age_bucket, [])
    if not keywords:
        return stories

    filtered: list[dict[str, str | int]] = []
    for story in stories:
        text_lower = (str(story["title"]) + " " + str(story["text"])).lower()
        if not any(kw in text_lower for kw in keywords):
            filtered.append(story)

    return filtered


def scrape_segment(reddit: praw.Reddit, gender: str, age: str) -> dict[str, str | list[dict[str, str | int]]]:
    """Scrape all stories for a segment."""
    segment_key = f"{gender}/{age}"
    subreddits = SUBREDDIT_MAP.get(segment_key, [])

    all_stories: list[dict[str, str | int]] = []
    for subreddit in subreddits:
        print(f"📥 Scraping {subreddit} for {segment_key}...")
        try:
            stories = scrape_subreddit(reddit, subreddit)
            all_stories.extend(stories)
            # Respect rate limits
            time.sleep(2)
        except Exception as e:
            print(f"⚠️  Error scraping {subreddit}: {e}")
            continue

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
        "stories": top_stories,
    }

    return result


def main():
    """Main scraper entry point."""
    print("=" * 60)
    print("Reddit Story Scraper for StoryGenerator")
    print("=" * 60)
    print()

    reddit = init_reddit()

    genders = ["women", "men"]
    ages = ["10-13", "14-17", "18-23"]

    # Get root directory (parent of scripts)
    root_dir = Path(__file__).parent.parent

    for gender in genders:
        for age in ages:
            print(f"\n🎯 Processing {gender}/{age}...")

            data = scrape_segment(reddit, gender, age)

            # Save to file
            output_dir = root_dir / "Generator" / "sources" / "reddit" / gender / age
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d")
            output_file = output_dir / f"{timestamp}_reddit_stories.json"

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Saved {len(data['stories'])} stories to {output_file}")

    print("\n" + "=" * 60)
    print("✨ Reddit scraping complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
