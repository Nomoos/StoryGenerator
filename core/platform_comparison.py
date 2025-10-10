"""
Cross-Platform Performance Comparison Module.

This module provides tools for comparing video performance across different platforms
and generating insights for content optimization.

Usage:
    from core.platform_comparison import PlatformComparator
    
    comparator = PlatformComparator()
    
    # Get comparison for a specific video
    comparison = comparator.compare_video("story_123")
    
    # Get best performing platform
    best = comparator.get_best_platform("story_123")
    
    # Generate optimization recommendations
    insights = comparator.generate_insights("story_123")
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from core.database import PlatformDatabase
from core.interfaces.platform_provider import PlatformType


@dataclass
class PlatformPerformance:
    """Performance metrics for a single platform."""
    platform: str
    video_id: str
    url: Optional[str]
    views: int
    likes: int
    comments: int
    shares: int
    engagement_rate: float
    collected_at: datetime
    
    @property
    def total_engagement(self) -> int:
        """Calculate total engagement actions."""
        return self.likes + self.comments + self.shares
    
    @property
    def virality_score(self) -> float:
        """
        Calculate virality score based on shares and engagement.
        Higher share rate indicates more viral content.
        """
        if self.views == 0:
            return 0.0
        share_rate = (self.shares / self.views) * 100
        return share_rate * (1 + (self.engagement_rate / 100))


@dataclass
class CrossPlatformComparison:
    """Comparison of video performance across platforms."""
    title_id: str
    title: str
    platforms: List[PlatformPerformance]
    collected_at: datetime
    
    @property
    def total_views(self) -> int:
        """Total views across all platforms."""
        return sum(p.views for p in self.platforms)
    
    @property
    def total_engagement(self) -> int:
        """Total engagement across all platforms."""
        return sum(p.total_engagement for p in self.platforms)
    
    @property
    def average_engagement_rate(self) -> float:
        """Average engagement rate across platforms."""
        if not self.platforms:
            return 0.0
        return sum(p.engagement_rate for p in self.platforms) / len(self.platforms)
    
    def get_best_platform(self, metric: str = "engagement_rate") -> Optional[PlatformPerformance]:
        """
        Get best performing platform by specified metric.
        
        Args:
            metric: Metric to compare ('views', 'engagement_rate', 'virality_score').
            
        Returns:
            PlatformPerformance for best platform or None.
        """
        if not self.platforms:
            return None
        
        if metric == "views":
            return max(self.platforms, key=lambda p: p.views)
        elif metric == "engagement_rate":
            return max(self.platforms, key=lambda p: p.engagement_rate)
        elif metric == "virality_score":
            return max(self.platforms, key=lambda p: p.virality_score)
        else:
            return max(self.platforms, key=lambda p: p.total_engagement)
    
    def get_platform_ranking(self, metric: str = "engagement_rate") -> List[Tuple[str, float]]:
        """
        Get platforms ranked by specified metric.
        
        Args:
            metric: Metric to rank by.
            
        Returns:
            List of (platform_name, metric_value) tuples, sorted descending.
        """
        if not self.platforms:
            return []
        
        rankings = []
        for p in self.platforms:
            if metric == "views":
                value = float(p.views)
            elif metric == "engagement_rate":
                value = p.engagement_rate
            elif metric == "virality_score":
                value = p.virality_score
            else:
                value = float(p.total_engagement)
            rankings.append((p.platform, value))
        
        return sorted(rankings, key=lambda x: x[1], reverse=True)


class PlatformComparator:
    """
    Analyzes and compares video performance across platforms.
    """

    def __init__(self, db_path: str = "data/platform_analytics.db"):
        """
        Initialize comparator with database.
        
        Args:
            db_path: Path to platform analytics database.
        """
        self.db = PlatformDatabase(db_path)
        self.db.initialize()

    def compare_video(self, title_id: str) -> Optional[CrossPlatformComparison]:
        """
        Compare performance of a video across all platforms.
        
        Args:
            title_id: Internal title/story ID.
            
        Returns:
            CrossPlatformComparison object or None if not found.
        """
        data = self.db.get_cross_platform_comparison(title_id)
        
        if not data:
            return None
        
        # Group by platform (get latest for each)
        platform_map: Dict[str, Dict[str, Any]] = {}
        for row in data:
            platform = row["platform"]
            if platform not in platform_map or row["collected_at"] > platform_map[platform]["collected_at"]:
                platform_map[platform] = row
        
        # Convert to PlatformPerformance objects
        platforms = []
        title = ""
        for platform, row in platform_map.items():
            if not title:
                title = row["title"]
            
            # Handle None values gracefully
            platforms.append(PlatformPerformance(
                platform=row["platform"],
                video_id=row["platform_video_id"] or "",
                url=row["url"],
                views=row["views"] or 0,
                likes=row["likes"] or 0,
                comments=row["comments"] or 0,
                shares=row["shares"] or 0,
                engagement_rate=row["engagement_rate"] or 0.0,
                collected_at=datetime.fromisoformat(row["collected_at"]) if row["collected_at"] else datetime.now(),
            ))
        
        return CrossPlatformComparison(
            title_id=title_id,
            title=title,
            platforms=platforms,
            collected_at=datetime.now(),
        )

    def get_best_platform_for_title(
        self,
        title_id: str,
        metric: str = "engagement_rate"
    ) -> Optional[str]:
        """
        Get the best performing platform for a specific video.
        
        Args:
            title_id: Internal title/story ID.
            metric: Metric to compare by.
            
        Returns:
            Platform name or None.
        """
        comparison = self.compare_video(title_id)
        if not comparison:
            return None
        
        best = comparison.get_best_platform(metric)
        return best.platform if best else None

    def generate_insights(self, title_id: str) -> Dict[str, Any]:
        """
        Generate optimization insights for a video.
        
        Args:
            title_id: Internal title/story ID.
            
        Returns:
            Dict with insights and recommendations.
        """
        comparison = self.compare_video(title_id)
        
        if not comparison:
            return {
                "error": "No data found for this video",
                "title_id": title_id,
            }
        
        insights = {
            "title_id": title_id,
            "title": comparison.title,
            "summary": {
                "total_views": comparison.total_views,
                "total_engagement": comparison.total_engagement,
                "average_engagement_rate": round(comparison.average_engagement_rate, 2),
                "platforms_count": len(comparison.platforms),
            },
            "platform_ranking": {},
            "best_performers": {},
            "recommendations": [],
        }
        
        # Rank by different metrics
        for metric in ["views", "engagement_rate", "virality_score"]:
            ranking = comparison.get_platform_ranking(metric)
            insights["platform_ranking"][metric] = ranking
            if ranking:
                insights["best_performers"][metric] = ranking[0][0]
        
        # Generate recommendations
        best_engagement = comparison.get_best_platform("engagement_rate")
        if best_engagement:
            insights["recommendations"].append(
                f"Best engagement on {best_engagement.platform} "
                f"({best_engagement.engagement_rate:.2f}%). "
                f"Consider focusing on this platform."
            )
        
        best_virality = comparison.get_best_platform("virality_score")
        if best_virality and best_virality.virality_score > 1.0:
            insights["recommendations"].append(
                f"{best_virality.platform} shows high virality (score: {best_virality.virality_score:.2f}). "
                f"Content style resonates well here."
            )
        
        # Check for underperforming platforms
        for perf in comparison.platforms:
            if perf.engagement_rate < comparison.average_engagement_rate * 0.5:
                insights["recommendations"].append(
                    f"{perf.platform} underperforming (engagement: {perf.engagement_rate:.2f}%). "
                    f"Consider adjusting content strategy or posting time."
                )
        
        return insights

    def get_platform_trends(
        self,
        platform: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get performance trends for a specific platform.
        
        Args:
            platform: Platform name.
            limit: Number of recent videos to analyze.
            
        Returns:
            Dict with trend analysis.
        """
        videos = self.db.get_all_videos(platform=platform, limit=limit)
        
        if not videos:
            return {
                "error": "No videos found for this platform",
                "platform": platform,
            }
        
        # Calculate averages
        total_views = 0
        total_engagement = 0
        video_count = 0
        
        for video in videos:
            analytics = self.db.get_latest_analytics(video["video_id"], platform)
            if analytics:
                total_views += analytics.get("views", 0)
                total_engagement += (
                    analytics.get("likes", 0) +
                    analytics.get("comments", 0) +
                    analytics.get("shares", 0)
                )
                video_count += 1
        
        avg_views = total_views / video_count if video_count > 0 else 0
        avg_engagement = total_engagement / video_count if video_count > 0 else 0
        
        return {
            "platform": platform,
            "video_count": video_count,
            "average_views": int(avg_views),
            "average_engagement": int(avg_engagement),
            "total_views": total_views,
            "total_engagement": total_engagement,
        }

    def compare_all_platforms(self) -> Dict[str, Any]:
        """
        Get overall comparison across all platforms.
        
        Returns:
            Dict with platform summaries.
        """
        platforms = ["youtube", "tiktok", "instagram", "facebook"]
        summaries = {}
        
        for platform in platforms:
            summary = self.db.get_platform_summary(platform)
            if summary and summary.get("total_videos", 0) > 0:
                summaries[platform] = summary
        
        return {
            "platform_summaries": summaries,
            "total_videos": sum(s.get("total_videos", 0) for s in summaries.values()),
            "total_views": sum(s.get("total_views", 0) or 0 for s in summaries.values()),
        }

    def close(self) -> None:
        """Close database connection."""
        self.db.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
