#!/usr/bin/env python3
"""
Twitter/X Thread Scraper

Scrapes viral story threads from Twitter/X using tweepy and Twitter API v2.
Focuses on narrative threads that tell compelling stories.
"""

import os
from typing import List, Dict, Optional
import time
from datetime import datetime, timedelta

# Support both relative and absolute imports
try:
    from .base_scraper import BaseScraper
except ImportError:
    from base_scraper import BaseScraper

# Note: tweepy would be imported here in a real implementation
# import tweepy


class TwitterScraper(BaseScraper):
    """Scraper for Twitter/X story threads."""
    
    def __init__(self, bearer_token: Optional[str] = None):
        """Initialize Twitter scraper.
        
        Args:
            bearer_token: Twitter API bearer token. If not provided, 
                         will try to get from environment variable.
        """
        super().__init__("twitter")
        self.bearer_token = bearer_token or os.getenv("TWITTER_BEARER_TOKEN")
        self.client = None
        
        # Initialize Twitter API client (mock for now)
        # In production: self.client = tweepy.Client(bearer_token=self.bearer_token)
        
    def scrape_content(self, 
                      topic: str, 
                      gender: str, 
                      age_bucket: str, 
                      limit: int = 50) -> List[Dict]:
        """Scrape Twitter threads.
        
        Args:
            topic: Topic or keywords to search for
            gender: Target gender
            age_bucket: Target age bucket
            limit: Maximum number of threads to fetch
            
        Returns:
            List of dictionaries containing thread data
        """
        threads = []
        
        # Get search queries based on demographics
        search_queries = self._get_search_queries(topic, gender, age_bucket)
        
        for query in search_queries[:3]:  # Limit to 3 queries
            try:
                threads.extend(self._search_threads(query, limit // 3))
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"   ⚠️  Error searching '{query}': {e}")
                continue
        
        return threads[:limit]
    
    def _get_search_queries(self, topic: str, gender: str, age_bucket: str) -> List[str]:
        """Generate Twitter search queries based on demographics.
        
        Args:
            topic: Base topic
            gender: Target gender
            age_bucket: Target age bucket
            
        Returns:
            List of optimized search queries
        """
        # Twitter search queries that find story threads
        base_queries = {
            "10-13": [
                "thread about school life",
                "teenage story thread",
                "friendship thread"
            ],
            "14-17": [
                "high school story thread",
                "teenage experience thread",
                "life lesson thread"
            ],
            "18-23": [
                "college story thread",
                "relationship thread",
                "life advice thread"
            ]
        }
        
        queries = base_queries.get(age_bucket, [])
        
        # Add topic if provided
        if topic and topic.lower() not in ["general", "all"]:
            queries = [f"{topic} {q}" for q in queries]
        
        # Add filters for engagement (threads with multiple tweets)
        # In real implementation: queries = [f"{q} min_replies:10" for q in queries]
        
        return queries if queries else [topic]
    
    def _search_threads(self, query: str, limit: int) -> List[Dict]:
        """Search for story threads on Twitter (mock implementation).
        
        Note: This is a MOCK implementation. Real implementation would use
        Twitter API v2 with proper authentication and endpoint calls.
        
        Args:
            query: Search query
            limit: Maximum number of threads
            
        Returns:
            List of thread data
        """
        # MOCK DATA - In production, this would use Twitter API v2
        # This demonstrates the expected data structure
        
        # Validate query
        if not query or not query.strip():
            return []
        
        # Safe extraction for hashtag
        query_parts = query.split()
        first_term = query_parts[0] if query_parts else "story"
        
        mock_threads = [
            {
                "id": f"twitter_{hash(query)}_{i}",
                "thread_id": f"thread_{i}_{int(time.time())}",
                "title": f"A thread about {first_term}",
                "url": f"https://twitter.com/user/status/{1234567890 + i}",
                "author": f"@storyteller{i}",
                "author_followers": 10000 + (i * 1000),
                "created_at": (datetime.now() - timedelta(days=i)).isoformat(),
                "tweets_count": 8 + i,
                "first_tweet": f"🧵 THREAD: Let me tell you about {query}... (1/{8+i})",
                "full_thread": [
                    f"Tweet {j+1}: This is part of the story about {query}..."
                    for j in range(min(8 + i, 15))
                ],
                "engagement": {
                    "likes": 1000 + (i * 200),
                    "retweets": 200 + (i * 50),
                    "replies": 100 + (i * 20),
                    "views": 50000 + (i * 5000)
                },
                "hashtags": ["#thread", "#story", first_term],
                "source": "twitter"
            }
            for i in range(min(limit, 10))
        ]
        
        return mock_threads
    
    def _get_thread_tweets(self, thread_id: str) -> List[Dict]:
        """Retrieve all tweets in a thread (placeholder for real implementation).
        
        Args:
            thread_id: ID of the thread
            
        Returns:
            List of tweets in the thread
        """
        # In production, this would use Twitter API v2 to get conversation thread
        # Using the conversation_id field to retrieve all related tweets
        pass
    
    def _is_story_thread(self, thread: Dict) -> bool:
        """Determine if a thread is a story thread vs. other content.
        
        Args:
            thread: Thread data
            
        Returns:
            True if it's a story thread, False otherwise
        """
        # Check for story indicators
        story_indicators = [
            "thread",
            "story",
            "let me tell you",
            "🧵",
            "here's what happened"
        ]
        
        first_tweet = thread.get("first_tweet", "").lower()
        return any(indicator in first_tweet for indicator in story_indicators)


def main():
    """Main entry point for Twitter scraper."""
    # Check for API credentials
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        print("⚠️  Warning: TWITTER_BEARER_TOKEN not set. Using mock data.")
    
    scraper = TwitterScraper(bearer_token)
    
    # Define demographics
    genders = ["women", "men"]
    ages = ["10-13", "14-17", "18-23"]
    
    # Define topics by age group
    topics = {
        "10-13": "teenage experiences",
        "14-17": "high school life",
        "18-23": "young adult"
    }
    
    results = []
    
    for gender in genders:
        for age in ages:
            topic = topics.get(age, "life stories")
            result = scraper.run(topic, gender, age, limit=50)
            results.append(result)
            
            # Rate limiting
            time.sleep(2)
    
    # Print summary
    print("\n" + "="*60)
    print("Twitter Scraping Summary")
    print("="*60)
    for result in results:
        print(f"{result['gender']:6} / {result['age_bucket']:6} - "
              f"Scraped: {result['scraped']:3} | "
              f"Filtered: {result['filtered']:3} | "
              f"File: {result['output_file']}")
    
    print("\n✨ Twitter scraping complete!")


if __name__ == "__main__":
    main()
