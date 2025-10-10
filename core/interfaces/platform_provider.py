"""
Platform Provider Interfaces for video distribution and analytics.

This module defines the interfaces for integrating with social media platforms
(YouTube, TikTok, Instagram) for video upload and analytics collection.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class PlatformType(Enum):
    """Supported social media platforms."""
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"


class PrivacyStatus(Enum):
    """Video privacy status."""
    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"


@dataclass
class VideoMetadata:
    """Metadata for video upload."""
    title: str
    description: str
    tags: Optional[List[str]] = None
    category_id: Optional[str] = None
    privacy_status: PrivacyStatus = PrivacyStatus.PUBLIC
    made_for_kids: bool = False
    thumbnail_path: Optional[str] = None
    hashtags: Optional[List[str]] = None
    caption: Optional[str] = None


@dataclass
class UploadResult:
    """Result of a video upload operation."""
    success: bool
    platform: PlatformType
    video_id: Optional[str] = None
    url: Optional[str] = None
    error_message: Optional[str] = None
    upload_time: Optional[datetime] = None


@dataclass
class VideoAnalytics:
    """Analytics data for a video."""
    platform: PlatformType
    video_id: str
    title_id: str
    collected_at: datetime
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    watch_time_seconds: float = 0.0
    average_view_duration: float = 0.0
    completion_rate: float = 0.0
    impressions: int = 0
    ctr: float = 0.0
    engagement_rate: float = 0.0


class IPlatformUploader(ABC):
    """
    Interface for platform video upload providers.
    
    Implementations should handle platform-specific authentication,
    video format requirements, and upload processes.
    """

    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the platform.
        
        Returns:
            bool: True if authentication successful, False otherwise.
        """
        pass

    @abstractmethod
    def upload_video(
        self,
        video_path: str,
        metadata: VideoMetadata,
    ) -> UploadResult:
        """
        Upload a video to the platform.
        
        Args:
            video_path: Path to the video file.
            metadata: Video metadata including title, description, tags, etc.
            
        Returns:
            UploadResult: Result of the upload operation.
        """
        pass

    @abstractmethod
    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """
        Set a custom thumbnail for an uploaded video.
        
        Args:
            video_id: Platform-specific video identifier.
            thumbnail_path: Path to the thumbnail image.
            
        Returns:
            bool: True if thumbnail set successfully, False otherwise.
        """
        pass


class IPlatformAnalytics(ABC):
    """
    Interface for platform analytics providers.
    
    Implementations should retrieve performance metrics from the platform API.
    """

    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the platform analytics API.
        
        Returns:
            bool: True if authentication successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_video_analytics(
        self,
        video_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Optional[VideoAnalytics]:
        """
        Retrieve analytics for a specific video.
        
        Args:
            video_id: Platform-specific video identifier.
            start_date: Start date for analytics range (optional).
            end_date: End date for analytics range (optional).
            
        Returns:
            VideoAnalytics: Analytics data for the video, or None if unavailable.
        """
        pass

    @abstractmethod
    def get_channel_analytics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve channel/account-level analytics.
        
        Args:
            start_date: Start date for analytics range (optional).
            end_date: End date for analytics range (optional).
            
        Returns:
            Dict[str, Any]: Channel analytics data.
        """
        pass
