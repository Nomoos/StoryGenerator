"""
Instagram source stub implementation.

TODO: Implement using official Instagram Graph API or third-party services.

Options:
1. Instagram Graph API (official, requires Facebook Business account)
   - https://developers.facebook.com/docs/instagram-api
   - Access to media insights, hashtags, mentions
   - Requires business/creator account
   
2. CrowdTangle API (free with approval, Meta-owned)
   - https://www.crowdtangle.com/
   - Track trending posts, hashtags, and influencers
   - Requires application approval
   
3. Iconosquare ($49-79/month, no API)
   - https://pro.iconosquare.com/
   - Analytics platform without public API
"""

from typing import List, Dict, Any

from social_trends.interfaces import TrendSource, TrendItem


class InstagramSource(TrendSource):
    """
    Instagram trend source - STUB IMPLEMENTATION.
    
    To implement:
    1. Apply for Instagram Graph API or CrowdTangle access
    2. Obtain access token and add to environment variables
    3. Implement fetch_items() to fetch trending hashtags and posts
    4. Map Instagram metrics (likes, comments, saves, reach) to TrendItem
    5. Implement compute_score() based on Instagram engagement metrics
    
    Instagram-specific metrics to consider:
    - Likes
    - Comments
    - Saves (important for algorithm)
    - Shares (sends)
    - Reach (unique views)
    - Impressions (total views)
    - Hashtag performance
    - Reel views and engagement
    
    Limitations:
    - Instagram API is heavily restricted
    - Requires business account for most endpoints
    - CrowdTangle requires approval
    - No public "trending" endpoint like YouTube
    """
    
    @property
    def name(self) -> str:
        return "instagram"
    
    def supports_regions(self) -> List[str]:
        """
        Instagram doesn't have explicit region filtering in API.
        Trending is more global, but can filter by location hashtags.
        """
        return ["US", "GB", "CZ", "CA", "AU", "DE", "FR", "ES", "IT", "JP", "KR", "BR", "MX", "IN", "worldwide"]
    
    async def fetch_items(self, region: str, limit: int = 50) -> List[TrendItem]:
        """
        Fetch trending Instagram posts/hashtags.
        
        TODO: Implement API integration
        
        Args:
            region: Region code (note: Instagram API has limited region support)
            limit: Maximum number of items to return
            
        Returns:
            List of TrendItem objects
            
        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError(
            "Instagram source is not yet implemented. "
            "Instagram API is heavily restricted. Options:\n"
            "1. Instagram Graph API (requires business account)\n"
            "2. CrowdTangle API (requires approval, best option)\n"
            "3. Manual hashtag analysis via Instagram Search\n"
            "\nRecommendation: Apply for CrowdTangle access first."
        )
    
    async def compute_score(self, metrics: Dict[str, Any]) -> float:
        """
        Compute score from Instagram metrics.
        
        TODO: Implement scoring based on:
        - Engagement rate: (likes + comments + saves) / reach (50%)
        - Reach (30%)
        - Saves (20% - important for Instagram algorithm)
        
        Args:
            metrics: Dict with likes, comments, saves, reach
            
        Returns:
            Score between 0 and 100
        """
        raise NotImplementedError("Instagram scoring not yet implemented")


# Example implementation structure (commented out):
"""
class InstagramSourceImpl(TrendSource):
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://graph.instagram.com/v12.0"
    
    async def fetch_items(self, region: str, limit: int = 50) -> List[TrendItem]:
        # Instagram doesn't have a direct "trending" endpoint
        # Strategy: Fetch top hashtags and their recent media
        
        async with aiohttp.ClientSession() as session:
            # Step 1: Get trending hashtags (would need CrowdTangle or manual list)
            trending_hashtags = await self._get_trending_hashtags(session, region)
            
            items = []
            for hashtag in trending_hashtags[:limit]:
                # Step 2: Get top posts for each hashtag
                url = f"{self.base_url}/ig_hashtag_search"
                params = {
                    "user_id": "your_business_id",
                    "q": hashtag,
                    "access_token": self.access_token
                }
                
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    # Parse and create TrendItem...
            
            return items
"""
