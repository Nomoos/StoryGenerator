"""
Database module for storing platform analytics and video metadata.

This module provides a SQLite-based storage solution for:
- Video upload records
- Analytics data from all platforms
- Cross-platform performance comparisons

Usage:
    from core.database import PlatformDatabase
    
    db = PlatformDatabase("data/platform_analytics.db")
    db.initialize()
    
    # Store upload result
    db.save_upload_result(result, title_id="story_123")
    
    # Store analytics
    db.save_analytics(analytics_data)
    
    # Query comparisons
    comparison = db.get_cross_platform_comparison(title_id="story_123")
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.interfaces.platform_provider import (
    PlatformType,
    UploadResult,
    VideoAnalytics,
)


class PlatformDatabase:
    """
    SQLite database for platform integration data storage.
    
    Stores:
    - Video upload records with metadata
    - Analytics data from all platforms
    - Cross-platform performance metrics
    """

    def __init__(self, db_path: str = "data/platform_analytics.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file.
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def initialize(self) -> None:
        """Initialize database schema."""
        conn = self.connect()
        cursor = conn.cursor()

        # Videos table - stores upload information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                platform TEXT NOT NULL,
                video_id TEXT NOT NULL,
                url TEXT,
                upload_time TIMESTAMP NOT NULL,
                privacy_status TEXT,
                tags TEXT,
                hashtags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(platform, video_id)
            )
        """)

        # Analytics table - stores performance metrics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER NOT NULL,
                platform TEXT NOT NULL,
                platform_video_id TEXT NOT NULL,
                collected_at TIMESTAMP NOT NULL,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                saves INTEGER DEFAULT 0,
                watch_time_seconds REAL DEFAULT 0,
                average_view_duration REAL DEFAULT 0,
                completion_rate REAL DEFAULT 0,
                impressions INTEGER DEFAULT 0,
                ctr REAL DEFAULT 0,
                engagement_rate REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos(id),
                UNIQUE(platform_video_id, collected_at)
            )
        """)

        # Cross-platform comparisons view
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS cross_platform_comparison AS
            SELECT 
                v.title_id,
                v.title,
                v.platform,
                v.video_id AS platform_video_id,
                v.url,
                a.views,
                a.likes,
                a.comments,
                a.shares,
                a.engagement_rate,
                a.collected_at,
                ROW_NUMBER() OVER (
                    PARTITION BY v.title_id, v.platform 
                    ORDER BY a.collected_at DESC
                ) AS rn
            FROM videos v
            LEFT JOIN analytics a ON v.id = a.video_id
        """)

        # Indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_videos_title_id 
            ON videos(title_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_videos_platform 
            ON videos(platform)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_analytics_video_id 
            ON analytics(video_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_analytics_collected_at 
            ON analytics(collected_at)
        """)

        conn.commit()

    def save_upload_result(
        self,
        result: UploadResult,
        title_id: str,
        title: str,
        description: str = "",
        privacy_status: str = "public",
        tags: Optional[List[str]] = None,
        hashtags: Optional[List[str]] = None,
    ) -> int:
        """
        Save video upload result to database.
        
        Args:
            result: Upload result from platform provider.
            title_id: Internal title/story ID.
            title: Video title.
            description: Video description.
            privacy_status: Privacy status.
            tags: List of tags.
            hashtags: List of hashtags.
            
        Returns:
            int: Database row ID of inserted record.
        """
        if not result.success or not result.video_id:
            raise ValueError("Can only save successful upload results")

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO videos (
                title_id, title, description, platform, video_id, url,
                upload_time, privacy_status, tags, hashtags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title_id,
            title,
            description,
            result.platform.value,
            result.video_id,
            result.url,
            result.upload_time or datetime.now(),
            privacy_status,
            json.dumps(tags or []),
            json.dumps(hashtags or []),
        ))

        conn.commit()
        return cursor.lastrowid

    def save_analytics(self, analytics: VideoAnalytics) -> int:
        """
        Save analytics data to database.
        
        Args:
            analytics: Video analytics from platform provider.
            
        Returns:
            int: Database row ID of inserted record.
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Get video database ID
        cursor.execute("""
            SELECT id FROM videos 
            WHERE platform = ? AND video_id = ?
        """, (analytics.platform.value, analytics.video_id))
        
        row = cursor.fetchone()
        if not row:
            raise ValueError(
                f"Video not found: {analytics.platform.value}/{analytics.video_id}. "
                "Upload result must be saved first."
            )
        
        video_db_id = row[0]

        cursor.execute("""
            INSERT OR REPLACE INTO analytics (
                video_id, platform, platform_video_id, collected_at,
                views, likes, comments, shares, saves,
                watch_time_seconds, average_view_duration, completion_rate,
                impressions, ctr, engagement_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            video_db_id,
            analytics.platform.value,
            analytics.video_id,
            analytics.collected_at,
            analytics.views,
            analytics.likes,
            analytics.comments,
            analytics.shares,
            analytics.saves,
            analytics.watch_time_seconds,
            analytics.average_view_duration,
            analytics.completion_rate,
            analytics.impressions,
            analytics.ctr,
            analytics.engagement_rate,
        ))

        conn.commit()
        return cursor.lastrowid

    def get_video_by_title_id(self, title_id: str, platform: str) -> Optional[Dict[str, Any]]:
        """
        Get video information by title ID and platform.
        
        Args:
            title_id: Internal title/story ID.
            platform: Platform name (youtube, tiktok, instagram, facebook).
            
        Returns:
            Dict with video information or None.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM videos 
            WHERE title_id = ? AND platform = ?
        """, (title_id, platform))

        row = cursor.fetchone()
        return dict(row) if row else None

    def get_latest_analytics(
        self,
        platform_video_id: str,
        platform: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get most recent analytics for a video.
        
        Args:
            platform_video_id: Platform-specific video ID.
            platform: Platform name.
            
        Returns:
            Dict with analytics data or None.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.* FROM analytics a
            JOIN videos v ON a.video_id = v.id
            WHERE v.video_id = ? AND v.platform = ?
            ORDER BY a.collected_at DESC
            LIMIT 1
        """, (platform_video_id, platform))

        row = cursor.fetchone()
        return dict(row) if row else None

    def get_cross_platform_comparison(
        self,
        title_id: str,
        limit_per_platform: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Get cross-platform performance comparison for a title.
        
        Args:
            title_id: Internal title/story ID.
            limit_per_platform: Number of records per platform (default: latest).
            
        Returns:
            List of dicts with comparison data for each platform.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                title_id,
                title,
                platform,
                platform_video_id,
                url,
                views,
                likes,
                comments,
                shares,
                engagement_rate,
                collected_at
            FROM cross_platform_comparison
            WHERE title_id = ? AND rn <= ?
            ORDER BY platform, collected_at DESC
        """, (title_id, limit_per_platform))

        return [dict(row) for row in cursor.fetchall()]

    def get_platform_summary(self, platform: str) -> Dict[str, Any]:
        """
        Get summary statistics for a platform.
        
        Args:
            platform: Platform name.
            
        Returns:
            Dict with summary statistics.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                COUNT(DISTINCT v.id) as total_videos,
                SUM(a.views) as total_views,
                SUM(a.likes) as total_likes,
                SUM(a.comments) as total_comments,
                SUM(a.shares) as total_shares,
                AVG(a.engagement_rate) as avg_engagement_rate,
                MAX(a.collected_at) as last_updated
            FROM videos v
            LEFT JOIN analytics a ON v.id = a.video_id
            WHERE v.platform = ?
            GROUP BY v.platform
        """, (platform,))

        row = cursor.fetchone()
        return dict(row) if row else {}

    def get_all_videos(
        self,
        platform: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get all videos, optionally filtered by platform.
        
        Args:
            platform: Optional platform filter.
            limit: Maximum number of results.
            
        Returns:
            List of video records.
        """
        conn = self.connect()
        cursor = conn.cursor()

        if platform:
            cursor.execute("""
                SELECT * FROM videos 
                WHERE platform = ?
                ORDER BY upload_time DESC
                LIMIT ?
            """, (platform, limit))
        else:
            cursor.execute("""
                SELECT * FROM videos 
                ORDER BY upload_time DESC
                LIMIT ?
            """, (limit,))

        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
