#!/usr/bin/env python3
"""
TikTok Video Scraper

Scrapes TikTok video descriptions and captions on specific topics.
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
    from TikTokApi import TikTokApi
    HAS_TIKTOK_API = True
except ImportError:
    HAS_TIKTOK_API = False
    print("⚠️  TikTokApi not available. Using mock data only. Install with: pip install TikTokApi")


class TikTokScraper(BaseScraper):
    """Scraper for TikTok video descriptions and captions."""

    def __init__(self, use_mock: bool = True):
        """Initialize TikTok scraper.
        
        Args:
            use_mock: If True, uses mock data instead of real API calls
        """
        super().__init__("tiktok")
        self.use_mock = use_mock or not HAS_TIKTOK_API
        
        if not self.use_mock and HAS_TIKTOK_API:
            try:
                self.api = TikTokApi()
            except Exception as e:
                print(f"⚠️  Could not initialize TikTok API: {e}. Using mock data.")
                self.api = None
                self.use_mock = True
        else:
            self.api = None
        
        self.rate_limit_delay = 3  # seconds between requests

    def scrape_content(
        self, topic: str, gender: str, age_bucket: str, limit: int = 50
    ) -> List[Dict]:
        """Scrape TikTok video descriptions and captions.

        Args:
            topic: Topic or hashtag to search for
            gender: Target gender
            age_bucket: Target age bucket
            limit: Maximum number of videos to fetch

        Returns:
            List of dictionaries containing video data
        """
        if self.use_mock:
            return self._scrape_mock_data(topic, gender, age_bucket, limit)
        
        videos = []
        
        # Get relevant hashtags for the demographic
        hashtags = self._get_hashtags(topic, gender, age_bucket)
        
        for hashtag in hashtags[:3]:  # Limit to 3 hashtags
            try:
                videos.extend(self._scrape_hashtag(hashtag, limit // 3))
                time.sleep(self.rate_limit_delay)
            except Exception as e:
                print(f"   ⚠️  Error scraping #{hashtag}: {e}")
                continue
        
        return videos[:limit]

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
            "10-13": ["teentok", "middleschoolstories", "youngteen"],
            "14-17": ["teenlife", "highschoolstories", "teendrama"],
            "18-23": ["collegestories", "youngadult", "adulting"],
        }
        
        hashtags = base_hashtags.get(age_bucket, [])
        
        # Add topic-specific hashtags
        if topic and topic.lower() not in ["general", "all"]:
            clean_topic = topic.replace(" ", "").lower()
            hashtags.insert(0, clean_topic)
        
        # Add story-related hashtags
        hashtags.extend(["storytime", "truestory", "storytelling"])
        
        return hashtags[:5]

    def _scrape_hashtag(self, hashtag: str, limit: int) -> List[Dict]:
        """Scrape videos from a hashtag (real API implementation).

        Args:
            hashtag: Hashtag to search (without #)
            limit: Maximum number of videos

        Returns:
            List of video data dictionaries
        """
        if not self.api:
            return []
        
        try:
            # Use TikTokApi to get videos by hashtag
            videos = self.api.by_hashtag(hashtag, count=limit)
            
            video_list = []
            for video in videos:
                video_data = {
                    "id": f"tiktok_{video.get('id', '')}",
                    "title": video.get('desc', '')[:100] if video.get('desc') else "TikTok Video",
                    "text": video.get('desc', ''),
                    "url": f"https://www.tiktok.com/@{video.get('author', {}).get('uniqueId', '')}/video/{video.get('id', '')}",
                    "author": video.get('author', {}).get('uniqueId', 'unknown'),
                    "likes": video.get('stats', {}).get('diggCount', 0),
                    "comments": video.get('stats', {}).get('commentCount', 0),
                    "shares": video.get('stats', {}).get('shareCount', 0),
                    "views": video.get('stats', {}).get('playCount', 0),
                    "hashtag": hashtag,
                    "created_at": datetime.fromtimestamp(video.get('createTime', 0)).isoformat() if video.get('createTime') else datetime.now().isoformat(),
                    "source": "tiktok",
                }
                video_list.append(video_data)
            
            return video_list
        
        except Exception as e:
            print(f"   ⚠️  Error scraping TikTok hashtag #{hashtag}: {e}")
            return []

    def _scrape_mock_data(self, topic: str, gender: str, age_bucket: str, limit: int) -> List[Dict]:
        """Generate mock TikTok data for testing.

        Args:
            topic: Topic or hashtag
            gender: Target gender
            age_bucket: Target age bucket
            limit: Maximum number of items

        Returns:
            List of mock video data
        """
        hashtags = self._get_hashtags(topic, gender, age_bucket)
        
        mock_stories = [
            "POV: When you realize your best friend has been lying to you this whole time",
            "Story time: My parents caught me sneaking out and what happened next was crazy",
            "My teacher accidentally showed her personal messages on the projector",
            "Found my boyfriend's secret TikTok account and I wish I hadn't",
            "Roommate drama part 3: She stole my stuff and blamed me for it",
            "Failed my exam but the reason why will shock you",
            "Someone recorded me without my permission and posted it online",
            "My pet passed away today and here's what they meant to me",
            "Accidentally confessed my feelings in a group chat",
            "Update on my crush situation: They said yes but there's a twist",
            "My friend group kicked me out and this is what happened",
            "Parents got divorced and I found out through Instagram",
            "That moment when you realize you're the problem",
            "My sibling read my diary and told everyone my secrets",
            "First day of college didn't go as planned",
        ]
        
        mock_videos = []
        for i in range(min(limit, 15)):
            story = mock_stories[i % len(mock_stories)]
            hashtag = hashtags[i % len(hashtags)]
            
            video = {
                "id": f"tiktok_{gender}_{age_bucket}_{i}",
                "title": story[:50] + "...",
                "text": story + "\n\n" + " ".join([f"#{h}" for h in hashtags[:3]]),
                "url": f"https://www.tiktok.com/@user{i}/video/mock{i}",
                "author": f"@user_{i}",
                "likes": 10000 + (i * 1000),
                "comments": 500 + (i * 50),
                "shares": 200 + (i * 20),
                "views": 50000 + (i * 5000),
                "hashtag": hashtag,
                "created_at": datetime.now().isoformat(),
                "source": "tiktok",
            }
            mock_videos.append(video)
        
        return mock_videos


def main():
    """Main entry point for TikTok scraper."""
    scraper = TikTokScraper(use_mock=True)
    
    # Define demographics
    genders = ["women", "men"]
    ages = ["10-13", "14-17", "18-23"]
    
    # Define topics by age group
    topics = {
        "10-13": "teen stories",
        "14-17": "high school drama",
        "18-23": "college life"
    }
    
    results = []
    
    for gender in genders:
        for age in ages:
            topic = topics.get(age, "storytime")
            result = scraper.run(topic, gender, age, limit=50)
            results.append(result)
            
            # Be respectful with rate limiting
            time.sleep(2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TikTok Scraping Summary")
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
