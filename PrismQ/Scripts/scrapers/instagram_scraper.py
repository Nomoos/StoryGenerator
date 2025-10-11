#!/usr/bin/env python3
"""
Instagram Story Scraper

Scrapes Instagram stories/posts from hashtags and accounts on specific topics.
Uses mock data implementation for testing (production API optional).
"""

from typing import List, Dict, Optional
import time
from datetime import datetime
import re

# Support both relative and absolute imports
try:
    from .base_scraper import BaseScraper
except ImportError:
    from base_scraper import BaseScraper

# Optional dependencies - only needed for actual scraping
try:
    from instagrapi import Client
    HAS_INSTAGRAPI = True
except ImportError:
    HAS_INSTAGRAPI = False
    print("⚠️  instagrapi not available. Using mock data only. Install with: pip install instagrapi")


class InstagramScraper(BaseScraper):
    """Scraper for Instagram stories and posts."""

    def __init__(self, use_mock: bool = True):
        """Initialize Instagram scraper.
        
        Args:
            use_mock: If True, uses mock data instead of real API calls
        """
        super().__init__("instagram")
        self.use_mock = use_mock or not HAS_INSTAGRAPI
        
        if not self.use_mock and HAS_INSTAGRAPI:
            self.client = Client()
            # In production, you would login here:
            # self.client.login(username, password)
        else:
            self.client = None
        
        self.rate_limit_delay = 3  # seconds between requests

    def scrape_content(
        self, topic: str, gender: str, age_bucket: str, limit: int = 50
    ) -> List[Dict]:
        """Scrape Instagram posts and captions.

        Args:
            topic: Topic or hashtag to search for
            gender: Target gender
            age_bucket: Target age bucket
            limit: Maximum number of posts to fetch

        Returns:
            List of dictionaries containing post data
        """
        if self.use_mock:
            return self._scrape_mock_data(topic, gender, age_bucket, limit)
        
        posts = []
        
        # Get relevant hashtags for the demographic
        hashtags = self._get_hashtags(topic, gender, age_bucket)
        
        for hashtag in hashtags[:3]:  # Limit to 3 hashtags
            try:
                posts.extend(self._scrape_hashtag(hashtag, limit // 3))
                time.sleep(self.rate_limit_delay)
            except Exception as e:
                print(f"   ⚠️  Error scraping #{hashtag}: {e}")
                continue
        
        return posts[:limit]

    def _get_hashtags(self, topic: str, gender: str, age_bucket: str) -> List[str]:
        """Get relevant hashtags based on demographics.

        Args:
            topic: Base topic
            gender: Target gender
            age_bucket: Target age bucket

        Returns:
            List of hashtags optimized for the demographic
        """
        # Base hashtags by age group
        base_hashtags = {
            "10-13": ["teenlife", "middleschool", "youngteens"],
            "14-17": ["teenlife", "highschool", "teenproblems"],
            "18-23": ["collegelife", "youngadult", "adulting"],
        }
        
        hashtags = base_hashtags.get(age_bucket, [])
        
        # Add topic-specific hashtags
        if topic and topic.lower() not in ["general", "all"]:
            clean_topic = topic.replace(" ", "").lower()
            hashtags.insert(0, clean_topic)
        
        # Add story-related hashtags
        hashtags.extend(["storytime", "mystory", "truestory"])
        
        return hashtags[:5]

    def _scrape_hashtag(self, hashtag: str, limit: int) -> List[Dict]:
        """Scrape posts from a hashtag (real API implementation).

        Args:
            hashtag: Hashtag to search (without #)
            limit: Maximum number of posts

        Returns:
            List of post data dictionaries
        """
        if not self.client:
            return []
        
        try:
            # Use instagrapi to get posts by hashtag
            medias = self.client.hashtag_medias_recent(hashtag, limit)
            
            posts = []
            for media in medias:
                post = {
                    "id": f"instagram_{media.pk}",
                    "title": media.caption_text[:100] if media.caption_text else "Instagram Post",
                    "text": media.caption_text or "",
                    "url": f"https://www.instagram.com/p/{media.code}/",
                    "author": media.user.username if media.user else "unknown",
                    "likes": media.like_count,
                    "comments": media.comment_count,
                    "views": media.view_count if hasattr(media, 'view_count') else 0,
                    "hashtag": hashtag,
                    "created_at": media.taken_at.isoformat() if media.taken_at else datetime.now().isoformat(),
                    "source": "instagram",
                }
                posts.append(post)
            
            return posts
        
        except Exception as e:
            print(f"   ⚠️  Error scraping Instagram hashtag #{hashtag}: {e}")
            return []

    def _scrape_mock_data(self, topic: str, gender: str, age_bucket: str, limit: int) -> List[Dict]:
        """Generate mock Instagram data for testing.

        Args:
            topic: Topic or hashtag
            gender: Target gender
            age_bucket: Target age bucket
            limit: Maximum number of items

        Returns:
            List of mock post data
        """
        hashtags = self._get_hashtags(topic, gender, age_bucket)
        
        mock_stories = [
            "Finally got the courage to tell my best friend how I really feel",
            "My parents just told me we're moving across the country",
            "I overheard my teacher talking about me and I wish I hadn't",
            "Found out my boyfriend was cheating through his Instagram story",
            "My roommate is driving me crazy and I don't know what to do",
            "I failed my driving test for the third time today",
            "Someone started a rumor about me and now everyone believes it",
            "My dog just passed away and I can't stop crying",
            "I accidentally sent a text to the wrong person and it was bad",
            "My crush just asked me out and I said no by accident",
        ]
        
        mock_posts = []
        for i in range(min(limit, 10)):
            story = mock_stories[i % len(mock_stories)]
            hashtag = hashtags[i % len(hashtags)]
            
            post = {
                "id": f"instagram_{gender}_{age_bucket}_{i}",
                "title": story[:50] + "...",
                "text": story + "\n\n" + " ".join([f"#{h}" for h in hashtags[:3]]),
                "url": f"https://www.instagram.com/p/mock{i}/",
                "author": f"user_{i}",
                "likes": 500 + (i * 100),
                "comments": 20 + (i * 5),
                "views": 2000 + (i * 200),
                "hashtag": hashtag,
                "created_at": datetime.now().isoformat(),
                "source": "instagram",
            }
            mock_posts.append(post)
        
        return mock_posts


def main():
    """Main entry point for Instagram scraper."""
    scraper = InstagramScraper(use_mock=True)
    
    # Define demographics
    genders = ["women", "men"]
    ages = ["10-13", "14-17", "18-23"]
    
    # Define topics by age group
    topics = {
        "10-13": "teenage life",
        "14-17": "high school stories",
        "18-23": "college life"
    }
    
    results = []
    
    for gender in genders:
        for age in ages:
            topic = topics.get(age, "life stories")
            result = scraper.run(topic, gender, age, limit=50)
            results.append(result)
            
            # Be respectful with rate limiting
            time.sleep(2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Instagram Scraping Summary")
    print("=" * 60)
    for result in results:
        print(
            f"{result['gender']:6} / {result['age_bucket']:6} - "
            f"Scraped: {result['scraped']:3} | "
            f"Filtered: {result['filtered']:3} | "
            f"Saved to {result['output_file']}"
        )
    
    print("=" * 60)


if __name__ == "__main__":
    main()
