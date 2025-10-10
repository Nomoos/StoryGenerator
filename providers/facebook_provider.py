"""
Facebook Platform Provider for video uploads and analytics.

This module implements the Facebook Graph API for video publishing
and performance insights retrieval.
"""

import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, Optional

import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from core.interfaces.platform_provider import (
    IPlatformUploader,
    IPlatformAnalytics,
    PlatformType,
    VideoMetadata,
    UploadResult,
    VideoAnalytics,
    PrivacyStatus,
)


logger = logging.getLogger(__name__)


class FacebookUploader(IPlatformUploader):
    """
    Facebook video upload provider using Graph API.
    
    Requires Facebook Page access token with appropriate permissions.
    Supports both standard videos and Facebook Reels.
    
    Example:
        >>> uploader = FacebookUploader(
        ...     access_token="YOUR_TOKEN",
        ...     page_id="YOUR_PAGE_ID"
        ... )
        >>> metadata = VideoMetadata(
        ...     title="My Video",
        ...     description="Amazing content!",
        ...     privacy_status=PrivacyStatus.PUBLIC
        ... )
        >>> result = uploader.upload_video("video.mp4", metadata)
    """

    API_BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(
        self,
        access_token: Optional[str] = None,
        page_id: Optional[str] = None,
    ):
        """
        Initialize Facebook uploader.
        
        Args:
            access_token: Facebook Page access token.
            page_id: Facebook Page ID.
        """
        self.access_token = access_token or os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.page_id = page_id or os.getenv("FACEBOOK_PAGE_ID")
        
        if not self.access_token or not self.page_id:
            logger.warning("Facebook credentials not fully configured")
        
        self._authenticated = bool(self.access_token and self.page_id)

    def authenticate(self) -> bool:
        """
        Verify Facebook authentication.
        
        Returns:
            bool: True if credentials are available.
        """
        if not self.access_token or not self.page_id:
            logger.error("Facebook access token or page ID not set")
            return False
        self._authenticated = True
        return True

    @retry(
        retry=retry_if_exception_type((requests.RequestException, ConnectionError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def upload_video(
        self,
        video_path: str,
        metadata: VideoMetadata,
    ) -> UploadResult:
        """
        Upload a video to Facebook Page.
        
        Args:
            video_path: Path to the video file (must be publicly accessible URL or local file).
            metadata: Video metadata including title, description.
            
        Returns:
            UploadResult: Result of the upload operation.
        """
        if not self._authenticated:
            if not self.authenticate():
                return UploadResult(
                    success=False,
                    platform=PlatformType.FACEBOOK,
                    error_message="Authentication failed",
                )

        # Check if video_path is a URL or local file
        is_url = video_path.startswith(("http://", "https://"))
        
        try:
            # Build caption with title and description
            caption = f"{metadata.title}\n\n{metadata.description or ''}"
            if metadata.hashtags:
                hashtag_str = " ".join([f"#{tag}" for tag in metadata.hashtags])
                caption = f"{caption}\n\n{hashtag_str}".strip()

            # Map privacy status
            published = metadata.privacy_status == PrivacyStatus.PUBLIC

            if is_url:
                # Upload from URL
                logger.info(f"Uploading Facebook video from URL: {metadata.title}")
                
                upload_url = f"{self.API_BASE_URL}/{self.page_id}/videos"
                upload_params = {
                    "access_token": self.access_token,
                    "file_url": video_path,
                    "title": metadata.title[:65],  # Facebook title limit
                    "description": caption[:5000],  # Facebook description limit
                    "published": published,
                }

                response = requests.post(upload_url, data=upload_params)
                response.raise_for_status()
                
            else:
                # Upload local file
                if not os.path.exists(video_path):
                    return UploadResult(
                        success=False,
                        platform=PlatformType.FACEBOOK,
                        error_message=f"Video file not found: {video_path}",
                    )

                logger.info(f"Uploading Facebook video from file: {metadata.title}")
                
                upload_url = f"{self.API_BASE_URL}/{self.page_id}/videos"
                
                with open(video_path, "rb") as video_file:
                    files = {"source": video_file}
                    data = {
                        "access_token": self.access_token,
                        "title": metadata.title[:65],
                        "description": caption[:5000],
                        "published": published,
                    }
                    
                    response = requests.post(upload_url, data=data, files=files)
                    response.raise_for_status()

            result_data = response.json()
            
            if "error" in result_data:
                error_msg = result_data["error"].get("message", "Unknown error")
                logger.error(f"Facebook upload failed: {error_msg}")
                return UploadResult(
                    success=False,
                    platform=PlatformType.FACEBOOK,
                    error_message=error_msg,
                )

            video_id = result_data.get("id")
            logger.info(f"Facebook video uploaded successfully: {video_id}")

            return UploadResult(
                success=True,
                platform=PlatformType.FACEBOOK,
                video_id=video_id,
                url=f"https://www.facebook.com/{self.page_id}/videos/{video_id}/",
                upload_time=datetime.now(),
            )

        except requests.RequestException as e:
            logger.error(f"Facebook upload request failed: {str(e)}")
            return UploadResult(
                success=False,
                platform=PlatformType.FACEBOOK,
                error_message=str(e),
            )

    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """
        Set thumbnail for Facebook video.
        
        Args:
            video_id: Facebook video ID.
            thumbnail_path: Path to thumbnail (must be set during upload).
            
        Returns:
            bool: Always False (thumbnails auto-generated by Facebook).
        """
        logger.warning(
            "Facebook auto-generates thumbnails. Custom thumbnails not supported via API."
        )
        return False


class FacebookAnalytics(IPlatformAnalytics):
    """
    Facebook analytics provider using Graph API.
    
    Retrieves video performance metrics like views, reactions, shares, etc.
    
    Example:
        >>> analytics = FacebookAnalytics(
        ...     access_token="YOUR_TOKEN",
        ...     page_id="YOUR_PAGE_ID"
        ... )
        >>> data = analytics.get_video_analytics("VIDEO_ID")
        >>> print(f"Views: {data.views}, Engagement: {data.engagement_rate}%")
    """

    API_BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(
        self,
        access_token: Optional[str] = None,
        page_id: Optional[str] = None,
    ):
        """
        Initialize Facebook analytics provider.
        
        Args:
            access_token: Facebook Page access token.
            page_id: Facebook Page ID.
        """
        self.access_token = access_token or os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.page_id = page_id or os.getenv("FACEBOOK_PAGE_ID")
        
        if not self.access_token or not self.page_id:
            logger.warning("Facebook credentials not fully configured")
        
        self._authenticated = bool(self.access_token and self.page_id)

    def authenticate(self) -> bool:
        """
        Verify Facebook authentication.
        
        Returns:
            bool: True if credentials are available.
        """
        if not self.access_token or not self.page_id:
            logger.error("Facebook access token or page ID not set")
            return False
        self._authenticated = True
        return True

    @retry(
        retry=retry_if_exception_type((requests.RequestException, ConnectionError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def get_video_analytics(
        self,
        video_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Optional[VideoAnalytics]:
        """
        Retrieve analytics for a specific Facebook video.
        
        Args:
            video_id: Facebook video ID.
            start_date: Not used (Facebook returns lifetime metrics).
            end_date: Not used (Facebook returns lifetime metrics).
            
        Returns:
            VideoAnalytics: Analytics data or None if unavailable.
        """
        if not self._authenticated:
            if not self.authenticate():
                return None

        try:
            # Get video insights
            url = f"{self.API_BASE_URL}/{video_id}"
            params = {
                "fields": "views,likes.summary(true),comments.summary(true),shares",
                "access_token": self.access_token,
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                logger.error(f"Facebook API error: {data['error']}")
                return None

            # Parse metrics
            views = data.get("views", 0)
            
            likes_data = data.get("likes", {})
            likes = likes_data.get("summary", {}).get("total_count", 0) if isinstance(likes_data, dict) else 0
            
            comments_data = data.get("comments", {})
            comments = comments_data.get("summary", {}).get("total_count", 0) if isinstance(comments_data, dict) else 0
            
            shares = data.get("shares", {}).get("count", 0) if isinstance(data.get("shares"), dict) else 0

            # Calculate engagement rate
            total_engagement = likes + comments + shares
            engagement_rate = (total_engagement / max(views, 1)) * 100 if views > 0 else 0.0

            return VideoAnalytics(
                platform=PlatformType.FACEBOOK,
                video_id=video_id,
                title_id="",  # Set externally
                collected_at=datetime.now(),
                views=views,
                likes=likes,
                comments=comments,
                shares=shares,
                engagement_rate=engagement_rate,
            )

        except requests.RequestException as e:
            logger.error(f"Failed to fetch Facebook analytics: {str(e)}")
            return None

    def get_channel_analytics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve Facebook Page-level analytics.
        
        Args:
            start_date: Start date for analytics.
            end_date: End date for analytics.
            
        Returns:
            Dict[str, Any]: Page analytics data.
        """
        if not self._authenticated:
            if not self.authenticate():
                return {}

        try:
            # Get page insights
            url = f"{self.API_BASE_URL}/{self.page_id}"
            params = {
                "fields": "fan_count,followers_count,engagement",
                "access_token": self.access_token,
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                logger.error(f"Facebook API error: {data['error']}")
                return {}

            return {
                "fan_count": data.get("fan_count", 0),
                "followers_count": data.get("followers_count", 0),
                "engagement": data.get("engagement", {}),
            }

        except requests.RequestException as e:
            logger.error(f"Failed to fetch Facebook page analytics: {str(e)}")
            return {}
