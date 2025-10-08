"""
Export Registry System - Track all exported videos with publish status and performance metrics.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from Tools.Utils import FINAL_PATH, PROJECT_ROOT


class ExportRegistry:
    """
    Manages a registry of all exported videos with tracking for publish status,
    performance metrics, and metadata.
    """
    
    def __init__(self, registry_path: Optional[str] = None):
        """
        Initialize the export registry.
        
        Args:
            registry_path: Path to registry JSON file (default: data/final/export_registry.json)
        """
        if registry_path is None:
            registry_path = os.path.join(FINAL_PATH, "export_registry.json")
        
        self.registry_path = registry_path
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load registry from JSON file or create new one."""
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading registry: {e}")
                return self._create_empty_registry()
        else:
            return self._create_empty_registry()
    
    def _create_empty_registry(self) -> Dict[str, Any]:
        """Create an empty registry structure."""
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_exports": 0,
            "videos": {}
        }
    
    def _save_registry(self):
        """Save registry to JSON file."""
        self.registry["last_updated"] = datetime.now().isoformat()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        
        try:
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving registry: {e}")
    
    def register_export(
        self,
        title_id: str,
        title: str,
        segment: str,
        age_group: str,
        video_path: str,
        thumbnail_path: Optional[str] = None,
        metadata_path: Optional[str] = None,
        additional_info: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Register a newly exported video.
        
        Args:
            title_id: Unique title identifier
            title: Story title
            segment: Target segment (women/men)
            age_group: Target age group
            video_path: Path to exported video
            thumbnail_path: Path to thumbnail
            metadata_path: Path to metadata JSON
            additional_info: Additional information to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            export_info = {
                "title": title,
                "title_id": title_id,
                "segment": segment,
                "age_group": age_group,
                "video_path": video_path,
                "thumbnail_path": thumbnail_path,
                "metadata_path": metadata_path,
                "export_date": datetime.now().isoformat(),
                "publish_status": "exported",  # exported, published, archived
                "platforms": {},  # Platform-specific publish info
                "performance": {
                    "views": 0,
                    "likes": 0,
                    "shares": 0,
                    "comments": 0,
                    "engagement_rate": 0.0
                },
                "analytics": {
                    "export_count": 1,
                    "last_export": datetime.now().isoformat(),
                    "re_exports": []
                }
            }
            
            # Add additional info if provided
            if additional_info:
                export_info.update(additional_info)
            
            # Add to registry
            self.registry["videos"][title_id] = export_info
            self.registry["total_exports"] = len(self.registry["videos"])
            
            # Save registry
            self._save_registry()
            
            print(f"✅ Registered export: {title_id} - {title}")
            return True
            
        except Exception as e:
            print(f"❌ Error registering export: {e}")
            return False
    
    def update_publish_status(
        self,
        title_id: str,
        platform: str,
        status: str = "published",
        url: Optional[str] = None,
        published_date: Optional[str] = None
    ) -> bool:
        """
        Update the publish status for a video on a specific platform.
        
        Args:
            title_id: Unique title identifier
            platform: Platform name (youtube, tiktok, instagram)
            status: Publish status (published, scheduled, failed)
            url: URL to published video
            published_date: Date of publication (ISO format)
            
        Returns:
            True if successful, False otherwise
        """
        if title_id not in self.registry["videos"]:
            print(f"⚠️ Video {title_id} not found in registry")
            return False
        
        try:
            video_info = self.registry["videos"][title_id]
            
            # Update platform info
            if "platforms" not in video_info:
                video_info["platforms"] = {}
            
            video_info["platforms"][platform] = {
                "status": status,
                "url": url,
                "published_date": published_date or datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Update overall publish status
            if status == "published":
                video_info["publish_status"] = "published"
            
            self._save_registry()
            print(f"✅ Updated publish status for {title_id} on {platform}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating publish status: {e}")
            return False
    
    def update_performance(
        self,
        title_id: str,
        views: Optional[int] = None,
        likes: Optional[int] = None,
        shares: Optional[int] = None,
        comments: Optional[int] = None
    ) -> bool:
        """
        Update performance metrics for a video.
        
        Args:
            title_id: Unique title identifier
            views: Number of views
            likes: Number of likes
            shares: Number of shares
            comments: Number of comments
            
        Returns:
            True if successful, False otherwise
        """
        if title_id not in self.registry["videos"]:
            print(f"⚠️ Video {title_id} not found in registry")
            return False
        
        try:
            performance = self.registry["videos"][title_id]["performance"]
            
            # Update metrics
            if views is not None:
                performance["views"] = views
            if likes is not None:
                performance["likes"] = likes
            if shares is not None:
                performance["shares"] = shares
            if comments is not None:
                performance["comments"] = comments
            
            # Calculate engagement rate
            total_views = performance.get("views", 0)
            if total_views > 0:
                total_engagement = (
                    performance.get("likes", 0) +
                    performance.get("shares", 0) +
                    performance.get("comments", 0)
                )
                performance["engagement_rate"] = round(
                    (total_engagement / total_views) * 100, 2
                )
            
            performance["last_updated"] = datetime.now().isoformat()
            
            self._save_registry()
            print(f"✅ Updated performance for {title_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating performance: {e}")
            return False
    
    def get_video_info(self, title_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific video."""
        return self.registry["videos"].get(title_id)
    
    def list_videos(
        self,
        segment: Optional[str] = None,
        age_group: Optional[str] = None,
        publish_status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List videos with optional filtering.
        
        Args:
            segment: Filter by segment (women/men)
            age_group: Filter by age group
            publish_status: Filter by publish status
            
        Returns:
            List of video information dictionaries
        """
        videos = []
        
        for title_id, info in self.registry["videos"].items():
            # Apply filters
            if segment and info.get("segment") != segment:
                continue
            if age_group and info.get("age_group") != age_group:
                continue
            if publish_status and info.get("publish_status") != publish_status:
                continue
            
            videos.append(info)
        
        return videos
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics from the registry."""
        total_videos = len(self.registry["videos"])
        
        if total_videos == 0:
            return {
                "total_videos": 0,
                "by_status": {},
                "by_segment": {},
                "by_age_group": {},
                "total_views": 0,
                "total_likes": 0,
                "total_engagement": 0,
                "avg_engagement_rate": 0.0
            }
        
        stats = {
            "total_videos": total_videos,
            "by_status": {},
            "by_segment": {},
            "by_age_group": {},
            "total_views": 0,
            "total_likes": 0,
            "total_shares": 0,
            "total_comments": 0,
            "avg_engagement_rate": 0.0
        }
        
        total_engagement_rate = 0.0
        
        for video_info in self.registry["videos"].values():
            # Count by status
            status = video_info.get("publish_status", "unknown")
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            
            # Count by segment
            segment = video_info.get("segment", "unknown")
            stats["by_segment"][segment] = stats["by_segment"].get(segment, 0) + 1
            
            # Count by age group
            age_group = video_info.get("age_group", "unknown")
            stats["by_age_group"][age_group] = stats["by_age_group"].get(age_group, 0) + 1
            
            # Sum performance metrics
            perf = video_info.get("performance", {})
            stats["total_views"] += perf.get("views", 0)
            stats["total_likes"] += perf.get("likes", 0)
            stats["total_shares"] += perf.get("shares", 0)
            stats["total_comments"] += perf.get("comments", 0)
            total_engagement_rate += perf.get("engagement_rate", 0.0)
        
        # Calculate averages
        stats["avg_engagement_rate"] = round(total_engagement_rate / total_videos, 2)
        
        return stats
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate a human-readable report of the registry.
        
        Args:
            output_path: Path to save report (optional)
            
        Returns:
            Report text
        """
        stats = self.get_statistics()
        
        report = f"""
Export Registry Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

Total Videos: {stats['total_videos']}

By Status:
{self._format_dict(stats['by_status'])}

By Segment:
{self._format_dict(stats['by_segment'])}

By Age Group:
{self._format_dict(stats['by_age_group'])}

Performance Summary:
  Total Views: {stats['total_views']:,}
  Total Likes: {stats['total_likes']:,}
  Total Shares: {stats['total_shares']:,}
  Total Comments: {stats['total_comments']:,}
  Avg Engagement Rate: {stats['avg_engagement_rate']}%

{'='*60}
"""
        
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"✅ Report saved to: {output_path}")
            except Exception as e:
                print(f"❌ Error saving report: {e}")
        
        return report
    
    def _format_dict(self, d: Dict[str, int], indent: int = 2) -> str:
        """Format a dictionary for display."""
        if not d:
            return " " * indent + "(none)"
        
        lines = []
        for key, value in sorted(d.items()):
            lines.append(f"{' ' * indent}{key}: {value}")
        return "\n".join(lines)
