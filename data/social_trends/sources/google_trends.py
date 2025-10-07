"""
Google Trends source implementation using pytrends.

Fetches trending searches and keyword interest from Google Trends.
No API key required - uses public Google Trends data.
"""

from typing import List, Dict, Any
from datetime import datetime
import asyncio

try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except ImportError:
    PYTRENDS_AVAILABLE = False

from social_trends.interfaces import TrendSource, TrendItem, TrendType


class GoogleTrendsSource(TrendSource):
    """
    Fetch trending searches from Google Trends using pytrends library.
    
    Note: Google Trends has rate limiting. Use with caution and respect delays.
    Ref: https://github.com/GeneralMills/pytrends
    """
    
    def __init__(self, hl: str = "en-US", tz: int = 360):
        """
        Initialize Google Trends source.
        
        Args:
            hl: Language parameter (e.g., 'en-US', 'cs-CZ')
            tz: Timezone offset in minutes
        """
        if not PYTRENDS_AVAILABLE:
            raise ImportError(
                "pytrends is required for GoogleTrendsSource. "
                "Install with: pip install pytrends"
            )
        
        self.hl = hl
        self.tz = tz
        self._pytrends = None
    
    def _get_pytrends(self) -> TrendReq:
        """Lazy initialization of TrendReq"""
        if self._pytrends is None:
            self._pytrends = TrendReq(hl=self.hl, tz=self.tz)
        return self._pytrends
    
    @property
    def name(self) -> str:
        return "google_trends"
    
    def supports_regions(self) -> List[str]:
        """Google Trends supports most countries"""
        return ["US", "GB", "CZ", "CA", "AU", "DE", "FR", "ES", "IT", "JP", "KR", "BR", "MX", "IN", "worldwide"]
    
    async def fetch_items(self, region: str, limit: int = 50) -> List[TrendItem]:
        """
        Fetch trending searches from Google Trends.
        
        Args:
            region: Region code (e.g., 'US', 'UK', 'CZ') or 'worldwide'
            limit: Maximum number of trends to return
            
        Returns:
            List of TrendItem objects representing trending keywords
        """
        self.validate_region(region)
        
        # Run in thread pool since pytrends is synchronous
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._fetch_trends_sync, region, limit)
    
    def _fetch_trends_sync(self, region: str, limit: int) -> List[TrendItem]:
        """Synchronous fetch to run in executor"""
        pytrends = self._get_pytrends()
        items = []
        
        try:
            # Get trending searches for the region
            # Note: trending_searches only works for certain regions (US, IN, JP, etc.)
            if region in ["US", "IN", "JP", "SG", "TH", "TW", "HK", "PH", "VN", "MY", "ID"]:
                trending_df = pytrends.trending_searches(pn=region.lower())
                
                for idx, keyword in enumerate(trending_df[0].head(limit)):
                    score = 100 - (idx * 2)  # Decreasing score based on rank
                    
                    item = TrendItem(
                        id=f"google_trends_{region}_{idx}",
                        title_or_keyword=keyword,
                        type=TrendType.KEYWORD,
                        source=self.name,
                        score=max(0, score),
                        metrics={"rank": idx + 1},
                        region=region,
                        locale=self._get_locale(region),
                        captured_at=datetime.utcnow(),
                        keywords=[keyword],
                        metadata={"source_type": "trending_searches"}
                    )
                    items.append(item)
            
            # Also try today's searches (realtime trends)
            try:
                today_df = pytrends.today_searches(pn=region)
                for idx, keyword in enumerate(today_df[0].head(limit - len(items))):
                    score = 95 - (idx * 2)  # Slightly lower than trending
                    
                    item = TrendItem(
                        id=f"google_trends_today_{region}_{idx}",
                        title_or_keyword=keyword,
                        type=TrendType.KEYWORD,
                        source=self.name,
                        score=max(0, score),
                        metrics={"rank": idx + 1},
                        region=region,
                        locale=self._get_locale(region),
                        captured_at=datetime.utcnow(),
                        keywords=[keyword],
                        metadata={"source_type": "today_searches"}
                    )
                    items.append(item)
            except Exception:
                # today_searches might not be available for all regions
                pass
                
        except Exception as e:
            # If API fails, return empty list (don't crash the pipeline)
            print(f"Warning: Google Trends API error for region {region}: {e}")
            return []
        
        return items[:limit]
    
    def _get_locale(self, region: str) -> str:
        """Map region code to locale"""
        locale_map = {
            "US": "en-US", "GB": "en-GB", "CZ": "cs-CZ",
            "CA": "en-CA", "AU": "en-AU", "DE": "de-DE",
            "FR": "fr-FR", "ES": "es-ES", "IT": "it-IT",
            "JP": "ja-JP", "KR": "ko-KR", "BR": "pt-BR",
            "MX": "es-MX", "IN": "hi-IN", "SG": "en-SG",
            "TH": "th-TH", "TW": "zh-TW", "HK": "zh-HK",
            "PH": "en-PH", "VN": "vi-VN", "MY": "ms-MY",
            "ID": "id-ID", "worldwide": "en-US"
        }
        return locale_map.get(region, "en-US")
    
    async def compute_score(self, metrics: Dict[str, Any]) -> float:
        """
        Compute score for Google Trends items.
        
        Score is primarily based on rank (position in trending list).
        
        Args:
            metrics: Dict with 'rank' key
            
        Returns:
            Score between 0 and 100
        """
        rank = metrics.get("rank", 50)
        
        # Linear decay: rank 1 = 100, rank 50 = 0
        score = max(0, 100 - (rank * 2))
        
        return float(score)
