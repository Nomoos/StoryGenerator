"""
Trend scoring utilities.

Implements comprehensive scoring algorithms for trend items.
"""

import math
from typing import Dict, Any
from datetime import datetime, timedelta


class TrendScorer:
    """
    Calculate comprehensive trend scores from metrics.
    
    Scoring formula:
    - 40% velocity (24-hour growth rate)
    - 30% volume (absolute views/engagement)
    - 20% engagement (likes, comments, shares)
    - 10% recency (freshness bonus)
    """
    
    @staticmethod
    def compute_velocity_score(current_value: int, previous_value: int) -> float:
        """
        Compute velocity score from value change over time.
        
        Args:
            current_value: Current metric value
            previous_value: Previous metric value (24h ago)
            
        Returns:
            Velocity score (0-100)
        """
        if previous_value == 0:
            # If no previous data, assume high velocity for new trends
            return 80.0 if current_value > 0 else 0.0
        
        # Calculate growth rate
        growth_rate = ((current_value - previous_value) / previous_value) * 100
        
        # Normalize to 0-100 scale
        # 100% growth = 80 points, 500%+ growth = 100 points
        if growth_rate < 0:
            velocity_score = 0.0  # Declining trend
        elif growth_rate <= 100:
            velocity_score = growth_rate * 0.8  # Linear up to 100%
        else:
            # Logarithmic scaling for high growth
            velocity_score = min(100, 80 + (math.log10(growth_rate / 100) * 20))
        
        return velocity_score
    
    @staticmethod
    def compute_volume_score(value: int, scale: str = "views") -> float:
        """
        Compute volume score from absolute value.
        
        Args:
            value: Metric value (views, searches, etc.)
            scale: Type of metric (views, searches, engagement)
            
        Returns:
            Volume score (0-100)
        """
        if value <= 0:
            return 0.0
        
        # Logarithmic scale based on metric type
        if scale == "views":
            # 1M views = ~82 points, 10M views = ~99 points
            log_value = math.log10(value)
            volume_score = min(100, log_value * 16.67)
        elif scale == "searches":
            # Searches typically have lower numbers
            # 10K searches = ~66 points, 100K searches = ~83 points
            log_value = math.log10(value)
            volume_score = min(100, log_value * 20)
        else:
            # Generic engagement
            log_value = math.log10(value)
            volume_score = min(100, log_value * 18)
        
        return volume_score
    
    @staticmethod
    def compute_engagement_score(engagement: int, total: int) -> float:
        """
        Compute engagement rate score.
        
        Args:
            engagement: Total engagement (likes + comments + shares)
            total: Total reach/views
            
        Returns:
            Engagement score (0-100)
        """
        if total == 0:
            return 0.0
        
        # Calculate engagement rate
        engagement_rate = (engagement / total) * 100
        
        # Normalize to 0-100 scale
        # 10% engagement = 100 points (very high for most platforms)
        # 1% engagement = 10 points (average for most content)
        score = min(100, engagement_rate * 10)
        
        return score
    
    @staticmethod
    def compute_recency_score(timestamp: datetime) -> float:
        """
        Compute recency bonus score.
        
        Args:
            timestamp: When content was published/captured
            
        Returns:
            Recency score (0-100)
        """
        now = datetime.utcnow()
        age = now - timestamp
        
        # Score decays over time
        if age < timedelta(hours=6):
            recency_score = 100.0  # Very fresh
        elif age < timedelta(hours=24):
            recency_score = 80.0  # Fresh
        elif age < timedelta(days=3):
            recency_score = 60.0  # Recent
        elif age < timedelta(days=7):
            recency_score = 40.0  # Moderately recent
        elif age < timedelta(days=14):
            recency_score = 20.0  # Older
        else:
            recency_score = 10.0  # Old
        
        return recency_score
    
    @classmethod
    def compute_comprehensive_score(
        cls,
        current_value: int,
        previous_value: int = 0,
        engagement: int = 0,
        total_views: int = 0,
        timestamp: datetime = None,
        scale: str = "views"
    ) -> float:
        """
        Compute comprehensive trend score using weighted formula.
        
        Score = 0.40 * velocity + 0.30 * volume + 0.20 * engagement + 0.10 * recency
        
        Args:
            current_value: Current metric value
            previous_value: Previous metric value (for velocity)
            engagement: Total engagement (likes + comments + shares)
            total_views: Total views/reach (for engagement rate)
            timestamp: When content was published
            scale: Type of metric (views, searches, engagement)
            
        Returns:
            Comprehensive score (0-100)
        """
        # Velocity (40%)
        velocity_score = cls.compute_velocity_score(current_value, previous_value)
        
        # Volume (30%)
        volume_score = cls.compute_volume_score(current_value, scale)
        
        # Engagement (20%)
        if total_views > 0:
            engagement_score = cls.compute_engagement_score(engagement, total_views)
        else:
            engagement_score = 0.0
        
        # Recency (10%)
        if timestamp:
            recency_score = cls.compute_recency_score(timestamp)
        else:
            recency_score = 50.0  # Default neutral score
        
        # Weighted combination
        comprehensive_score = (
            0.40 * velocity_score +
            0.30 * volume_score +
            0.20 * engagement_score +
            0.10 * recency_score
        )
        
        return min(100.0, max(0.0, comprehensive_score))
