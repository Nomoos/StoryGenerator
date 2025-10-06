"""
YouTube Data API v3 source implementation.

Uses the official YouTube Data API to fetch trending videos and extract keywords.
Requires YOUTUBE_API_KEY environment variable.
"""

import os
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
from collections import Counter

from social_trends.interfaces import TrendSource, TrendItem, TrendType
from social_trends.utils.keywords import KeywordExtractor


class YouTubeSource(TrendSource):
    """
    Fetch trending videos from YouTube using the official Data API v3.
    
    API Quota: 10,000 units/day (videos.list costs 1 unit per request)
    Ref: https://developers.google.com/youtube/v3/docs/videos/list
    """
    
    API_BASE_URL = "https://www.googleapis.com/youtube/v3"
    MAX_RESULTS_PER_REQUEST = 50
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize YouTube source.
        
        Args:
            api_key: YouTube Data API key. If None, reads from YOUTUBE_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "YouTube API key required. Set YOUTUBE_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.keyword_extractor = KeywordExtractor()
        self._session: Optional[aiohttp.ClientSession] = None
    
    @property
    def name(self) -> str:
        return "youtube"
    
    def supports_regions(self) -> List[str]:
        """YouTube supports 100+ regions. Listing key ones."""
        return ["US", "GB", "CZ", "CA", "AU", "DE", "FR", "ES", "IT", "JP", "KR", "BR", "MX", "IN"]
    
    async def _ensure_session(self):
        """Lazy initialization of aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
    
    async def _close_session(self):
        """Close aiohttp session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def fetch_items(self, region: str, limit: int = 50) -> List[TrendItem]:
        """
        Fetch trending videos from YouTube.
        
        Args:
            region: Region code (e.g., 'US', 'UK', 'CZ')
            limit: Maximum number of videos to return (max 50 per API request)
            
        Returns:
            List of TrendItem objects representing trending videos
        """
        self.validate_region(region)
        await self._ensure_session()
        
        # YouTube API limits to 50 results per request
        max_results = min(limit, self.MAX_RESULTS_PER_REQUEST)
        
        params = {
            "part": "snippet,statistics,contentDetails",
            "chart": "mostPopular",
            "regionCode": region,
            "maxResults": max_results,
            "key": self.api_key
        }
        
        url = f"{self.API_BASE_URL}/videos"
        
        try:
            async with self._session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                
                items = []
                for video in data.get("items", []):
                    item = await self._parse_video(video, region)
                    items.append(item)
                
                return items
                
        except aiohttp.ClientError as e:
            raise Exception(f"YouTube API error: {e}")
    
    async def _parse_video(self, video: Dict[str, Any], region: str) -> TrendItem:
        """Parse YouTube video data into TrendItem"""
        video_id = video["id"]
        snippet = video["snippet"]
        statistics = video.get("statistics", {})
        
        # Extract metrics
        view_count = int(statistics.get("viewCount", 0))
        like_count = int(statistics.get("likeCount", 0))
        comment_count = int(statistics.get("commentCount", 0))
        
        # Calculate score based on engagement
        metrics = {
            "viewCount": view_count,
            "likeCount": like_count,
            "commentCount": comment_count,
            "favoriteCount": int(statistics.get("favoriteCount", 0))
        }
        
        score = await self.compute_score(metrics)
        
        # Extract keywords from title, description, and tags
        title = snippet.get("title", "")
        description = snippet.get("description", "")
        tags = snippet.get("tags", [])
        
        text_for_keywords = f"{title} {description} {' '.join(tags)}"
        keywords = self.keyword_extractor.extract_keywords(text_for_keywords, top_n=10)
        
        # Determine locale from region
        locale_map = {
            "US": "en-US", "GB": "en-GB", "CZ": "cs-CZ", 
            "CA": "en-CA", "AU": "en-AU", "DE": "de-DE",
            "FR": "fr-FR", "ES": "es-ES", "IT": "it-IT",
            "JP": "ja-JP", "KR": "ko-KR", "BR": "pt-BR",
            "MX": "es-MX", "IN": "hi-IN"
        }
        locale = locale_map.get(region, "en-US")
        
        return TrendItem(
            id=f"youtube_{video_id}",
            title_or_keyword=title,
            type=TrendType.VIDEO,
            source=self.name,
            score=score,
            metrics=metrics,
            url=f"https://www.youtube.com/watch?v={video_id}",
            region=region,
            locale=locale,
            captured_at=datetime.utcnow(),
            keywords=keywords,
            metadata={
                "channel": snippet.get("channelTitle", ""),
                "publishedAt": snippet.get("publishedAt", ""),
                "categoryId": snippet.get("categoryId", ""),
                "duration": video.get("contentDetails", {}).get("duration", ""),
            }
        )
    
    async def compute_score(self, metrics: Dict[str, Any]) -> float:
        """
        Compute trend score from YouTube metrics.
        
        Score formula:
        - 60% views (logarithmic scale)
        - 25% engagement rate (likes + comments / views)
        - 15% recency bonus (applied elsewhere based on publishedAt)
        
        Args:
            metrics: Dict with viewCount, likeCount, commentCount
            
        Returns:
            Score between 0 and 100
        """
        import math
        
        views = metrics.get("viewCount", 0)
        likes = metrics.get("likeCount", 0)
        comments = metrics.get("commentCount", 0)
        
        # Logarithmic scale for views (1M views = ~82 points)
        if views > 0:
            view_score = min(100, math.log10(views) * 16.67)  # log10(1M) * 16.67 ≈ 100
        else:
            view_score = 0
        
        # Engagement rate
        if views > 0:
            engagement_rate = (likes + comments) / views
            engagement_score = min(100, engagement_rate * 1000)  # 10% engagement = 100 points
        else:
            engagement_score = 0
        
        # Weighted combination
        score = (0.60 * view_score) + (0.25 * engagement_score)
        
        return min(100.0, max(0.0, score))
    
    async def __aenter__(self):
        """Async context manager support"""
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up session on exit"""
        await self._close_session()
