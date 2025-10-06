"""
Core interfaces and data structures for the social trends system.

Defines the contract that all trend sources must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class TrendType(Enum):
    """Type of trending item"""
    VIDEO = "video"
    KEYWORD = "keyword"
    HASHTAG = "hashtag"
    TOPIC = "topic"


@dataclass
class TrendItem:
    """
    Normalized representation of a trending item from any source.
    
    Attributes:
        id: Unique identifier (source-specific)
        title_or_keyword: The trending title, keyword, or hashtag
        type: Type of trend (video, keyword, hashtag, topic)
        source: Platform name (youtube, google_trends, tiktok, instagram)
        score: Normalized trend score (0-100)
        metrics: Source-specific metrics (views, likes, shares, etc.)
        url: Optional URL to the content
        region: Region code (US, UK, CZ, etc.)
        locale: Language locale (en-US, cs-CZ, etc.)
        captured_at: UTC timestamp when data was captured
        keywords: Extracted keywords from title/description
        metadata: Additional source-specific data
    """
    id: str
    title_or_keyword: str
    type: TrendType
    source: str
    score: float
    metrics: Dict[str, Any] = field(default_factory=dict)
    url: Optional[str] = None
    region: str = "US"
    locale: str = "en-US"
    captured_at: datetime = field(default_factory=datetime.utcnow)
    keywords: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate and normalize fields"""
        # Ensure score is between 0 and 100
        self.score = max(0.0, min(100.0, self.score))
        
        # Convert type to enum if it's a string
        if isinstance(self.type, str):
            self.type = TrendType(self.type)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "title_or_keyword": self.title_or_keyword,
            "type": self.type.value,
            "source": self.source,
            "score": self.score,
            "metrics": self.metrics,
            "url": self.url,
            "region": self.region,
            "locale": self.locale,
            "captured_at": self.captured_at.isoformat(),
            "keywords": self.keywords,
            "metadata": self.metadata
        }


class TrendSource(ABC):
    """
    Abstract base class for all trend sources.
    
    Each source (YouTube, TikTok, Google Trends, etc.) implements this interface
    to provide a consistent way to fetch and normalize trending data.
    
    Design: Open/Closed Principle - extend by adding new sources without modifying existing code.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the source name (e.g., 'youtube', 'google_trends')"""
        pass
    
    @abstractmethod
    def supports_regions(self) -> List[str]:
        """Return list of supported region codes (e.g., ['US', 'UK', 'CZ'])"""
        pass
    
    @abstractmethod
    async def fetch_items(self, region: str, limit: int = 50) -> List[TrendItem]:
        """
        Fetch trending items from this source.
        
        Args:
            region: Region code (e.g., 'US', 'UK', 'CZ')
            limit: Maximum number of items to return
            
        Returns:
            List of normalized TrendItem objects
            
        Raises:
            NotImplementedError: If source is not yet implemented
            ValueError: If region is not supported
            Exception: For API errors or network issues
        """
        pass
    
    @abstractmethod
    async def compute_score(self, metrics: Dict[str, Any]) -> float:
        """
        Compute normalized trend score (0-100) from raw metrics.
        
        Args:
            metrics: Source-specific metrics (views, likes, velocity, etc.)
            
        Returns:
            Normalized score between 0 and 100
        """
        pass
    
    def validate_region(self, region: str) -> None:
        """Validate that region is supported"""
        if region not in self.supports_regions():
            raise ValueError(
                f"Region '{region}' not supported by {self.name}. "
                f"Supported regions: {', '.join(self.supports_regions())}"
            )
