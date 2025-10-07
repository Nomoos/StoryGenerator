"""
Exploding Topics source stub implementation.

Exploding Topics tracks emerging trends before they become mainstream.
Website: https://explodingtopics.com/

Options:
1. Exploding Topics API (paid plans starting ~$99/month)
   - Access to trending topics database
   - Historical trend data
   - Category filtering
   
2. Web scraping (not recommended due to TOS)
   - Would violate terms of service
   - Rate limiting and blocking likely
   
3. Manual integration via exports
   - Export trending topics from dashboard
   - Process CSV/JSON files
"""

from typing import List, Dict, Any

from social_trends.interfaces import TrendSource, TrendItem


class ExplodingTopicsSource(TrendSource):
    """
    Exploding Topics source - STUB IMPLEMENTATION.
    
    Exploding Topics identifies trends in their early growth phase before
    they hit mainstream platforms like YouTube or Google Trends.
    
    To implement:
    1. Subscribe to Exploding Topics API plan
    2. Obtain API key
    3. Implement fetch_items() to query trending topics
    4. Filter by category (tech, finance, lifestyle, etc.)
    5. Map growth metrics to TrendItem score
    
    Exploding Topics metrics:
    - Search volume growth rate
    - Current search volume
    - Trend status (new, peaked, declining)
    - Category
    - Related topics
    """
    
    @property
    def name(self) -> str:
        return "exploding_topics"
    
    def supports_regions(self) -> List[str]:
        """
        Exploding Topics primarily focuses on US/global trends.
        Region filtering may be limited.
        """
        return ["US", "worldwide"]
    
    async def fetch_items(self, region: str, limit: int = 50) -> List[TrendItem]:
        """
        Fetch emerging trends from Exploding Topics.
        
        TODO: Implement API integration
        
        Args:
            region: Region code (limited to US/worldwide)
            limit: Maximum number of topics to return
            
        Returns:
            List of TrendItem objects
            
        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError(
            "Exploding Topics source is not yet implemented. "
            "Options:\n"
            "1. Subscribe to Exploding Topics API ($99+/month)\n"
            "2. Manual export from dashboard (free tier available)\n"
            "\nExploding Topics focuses on early-stage trends before they hit mainstream."
        )
    
    async def compute_score(self, metrics: Dict[str, Any]) -> float:
        """
        Compute score from Exploding Topics metrics.
        
        TODO: Implement scoring based on:
        - Growth rate (60% - this is the key metric)
        - Current volume (30%)
        - Trend status (10% - bonus for "new" trends)
        
        Args:
            metrics: Dict with growth_rate, volume, status
            
        Returns:
            Score between 0 and 100
        """
        raise NotImplementedError("Exploding Topics scoring not yet implemented")


# Example implementation structure (commented out):
"""
class ExplodingTopicsSourceImpl(TrendSource):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.explodingtopics.com/v1"  # hypothetical
    
    async def fetch_items(self, region: str, limit: int = 50) -> List[TrendItem]:
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/trends"
            params = {
                "status": "growing",  # Filter for actively growing trends
                "limit": limit,
                "api_key": self.api_key
            }
            
            async with session.get(url, params=params) as response:
                data = await response.json()
                
                items = []
                for trend in data.get("trends", []):
                    score = self._compute_score_from_growth(trend["growth_rate"])
                    
                    item = TrendItem(
                        id=f"exploding_{trend['id']}",
                        title_or_keyword=trend["topic"],
                        type=TrendType.TOPIC,
                        source="exploding_topics",
                        score=score,
                        metrics={
                            "growth_rate": trend["growth_rate"],
                            "current_volume": trend["volume"],
                            "status": trend["status"],
                        },
                        region=region,
                        keywords=[trend["topic"]],
                        metadata={
                            "category": trend.get("category", ""),
                            "related_topics": trend.get("related", []),
                        }
                    )
                    items.append(item)
                
                return items
"""
