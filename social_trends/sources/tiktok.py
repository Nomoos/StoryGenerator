"""
TikTok source stub implementation.

TODO: Implement using official TikTok Business API or third-party services.

Options:
1. TikTok Business API (official, requires business account)
   - https://developers.tiktok.com/
   - Provides trending content, hashtags, and video metrics
   
2. RapidAPI TikTok API ($10-50/month)
   - https://rapidapi.com/yi005/api/tiktok-api23
   - Access trending videos, hashtags, user data
   
3. Apify TikTok Scraper ($49+/month)
   - https://apify.com/apify/tiktok-scraper
   - Extract trending content, videos, hashtags
"""

from typing import List, Dict, Any

from social_trends.interfaces import TrendSource, TrendItem


class TikTokSource(TrendSource):
    """
    TikTok trend source - STUB IMPLEMENTATION.
    
    To implement:
    1. Choose API provider (official TikTok Business API, RapidAPI, or Apify)
    2. Add API credentials to environment variables
    3. Implement fetch_items() to call API and parse response
    4. Map TikTok metrics (views, likes, shares, comments) to TrendItem
    5. Implement compute_score() based on TikTok engagement metrics
    
    TikTok-specific metrics to consider:
    - Video views
    - Likes (hearts)
    - Shares
    - Comments
    - Video completion rate
    - Sound/music usage (trending sounds)
    - Hashtag performance
    """
    
    @property
    def name(self) -> str:
        return "tiktok"
    
    def supports_regions(self) -> List[str]:
        """TikTok supports most countries"""
        return ["US", "GB", "CZ", "CA", "AU", "DE", "FR", "ES", "IT", "JP", "KR", "BR", "MX", "IN"]
    
    async def fetch_items(self, region: str, limit: int = 50) -> List[TrendItem]:
        """
        Fetch trending TikTok videos/hashtags.
        
        TODO: Implement API integration
        
        Args:
            region: Region code (e.g., 'US', 'UK', 'CZ')
            limit: Maximum number of items to return
            
        Returns:
            List of TrendItem objects
            
        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError(
            "TikTok source is not yet implemented. "
            "To implement, choose an API provider:\n"
            "1. TikTok Business API (official, free with business account)\n"
            "2. RapidAPI TikTok API ($10-50/month)\n"
            "3. Apify TikTok Scraper ($49+/month)\n"
            "\nSee documentation in this file for details."
        )
    
    async def compute_score(self, metrics: Dict[str, Any]) -> float:
        """
        Compute score from TikTok metrics.
        
        TODO: Implement scoring based on:
        - Views (40%)
        - Engagement rate: (likes + comments + shares) / views (40%)
        - Velocity: growth rate over 24h (20%)
        
        Args:
            metrics: Dict with views, likes, comments, shares
            
        Returns:
            Score between 0 and 100
        """
        raise NotImplementedError("TikTok scoring not yet implemented")


# Example implementation structure (commented out):
"""
class TikTokSourceImpl(TrendSource):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tiktok.com/v1"  # or RapidAPI URL
    
    async def fetch_items(self, region: str, limit: int = 50) -> List[TrendItem]:
        async with aiohttp.ClientSession() as session:
            # Example for trending videos
            url = f"{self.base_url}/trending/videos"
            params = {"country": region, "count": limit}
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            async with session.get(url, params=params, headers=headers) as response:
                data = await response.json()
                
                items = []
                for video in data.get("videos", []):
                    item = TrendItem(
                        id=f"tiktok_{video['id']}",
                        title_or_keyword=video.get("desc", ""),
                        type=TrendType.VIDEO,
                        source="tiktok",
                        score=await self.compute_score(video["stats"]),
                        metrics={
                            "views": video["stats"]["playCount"],
                            "likes": video["stats"]["diggCount"],
                            "shares": video["stats"]["shareCount"],
                            "comments": video["stats"]["commentCount"],
                        },
                        url=f"https://www.tiktok.com/@{video['author']}/video/{video['id']}",
                        region=region,
                        ...
                    )
                    items.append(item)
                
                return items
"""
