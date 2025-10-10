"""
Instagram Platform Provider for Reels uploads and analytics.

This module implements Instagram Graph API for Business/Creator accounts
to publish Reels and retrieve performance insights.
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


class InstagramUploader(IPlatformUploader):
    """
    Instagram Reels upload provider using Graph API.
    
    Requires Instagram Business/Creator account linked to Facebook page.
    Two-phase upload: create media container, then publish.
    
    Example:
        >>> uploader = InstagramUploader(
        ...     access_token="YOUR_TOKEN",
        ...     instagram_user_id="YOUR_IG_USER_ID"
        ... )
        >>> metadata = VideoMetadata(
        ...     caption="Amazing content! #reels #viral",
        ...     hashtags=["reels", "viral"],
        ... )
        >>> result = uploader.upload_video("video.mp4", metadata)
    """

    API_BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(
        self,
        access_token: Optional[str] = None,
        instagram_user_id: Optional[str] = None,
    ):
        """
        Initialize Instagram uploader.
        
        Args:
            access_token: Facebook Graph API access token.
            instagram_user_id: Instagram Business/Creator account ID.
        """
        self.access_token = access_token or os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.instagram_user_id = instagram_user_id or os.getenv("INSTAGRAM_USER_ID")
        
        if not self.access_token or not self.instagram_user_id:
            logger.warning("Instagram credentials not fully configured")
        
        self._authenticated = bool(self.access_token and self.instagram_user_id)

    def authenticate(self) -> bool:
        """
        Verify Instagram authentication.
        
        Returns:
            bool: True if credentials are available.
        """
        if not self.access_token or not self.instagram_user_id:
            logger.error("Instagram access token or user ID not set")
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
        Upload a Reel to Instagram using Graph API.
        
        Args:
            video_path: Path to the video file (must be publicly accessible URL).
            metadata: Video metadata including caption and hashtags.
            
        Returns:
            UploadResult: Result of the upload operation.
            
        Note:
            Instagram requires video to be hosted at a public URL.
            Local files must be uploaded to temporary hosting first.
        """
        if not self._authenticated:
            if not self.authenticate():
                return UploadResult(
                    success=False,
                    platform=PlatformType.INSTAGRAM,
                    error_message="Authentication failed",
                )

        # Check if video_path is a URL or local file
        is_url = video_path.startswith(("http://", "https://"))
        
        if not is_url:
            # For local files, user must upload to hosting first
            logger.error(
                "Instagram requires video to be at a public URL. "
                "Please upload the video to a hosting service first."
            )
            return UploadResult(
                success=False,
                platform=PlatformType.INSTAGRAM,
                error_message="Video must be at a public URL for Instagram upload",
            )

        video_url = video_path

        # Build caption with hashtags
        caption = metadata.caption or metadata.description or ""
        if metadata.hashtags:
            hashtag_str = " ".join([f"#{tag}" for tag in metadata.hashtags])
            caption = f"{caption}\n\n{hashtag_str}".strip()

        # Phase 1: Create media container
        logger.info(f"Creating Instagram Reel media container")

        container_params = {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption[:2200],  # Instagram caption limit
            "access_token": self.access_token,
            "share_to_feed": True,  # Also share to main feed
        }

        # Add thumbnail if provided and is a URL
        if metadata.thumbnail_path and metadata.thumbnail_path.startswith(("http://", "https://")):
            container_params["thumb_offset"] = 0  # Use frame at 0ms

        try:
            # Create container
            container_url = f"{self.API_BASE_URL}/{self.instagram_user_id}/media"
            container_response = requests.post(container_url, params=container_params)
            container_response.raise_for_status()
            container_data = container_response.json()

            if "error" in container_data:
                error_msg = container_data["error"].get("message", "Unknown error")
                logger.error(f"Instagram container creation failed: {error_msg}")
                return UploadResult(
                    success=False,
                    platform=PlatformType.INSTAGRAM,
                    error_message=error_msg,
                )

            creation_id = container_data.get("id")
            logger.info(f"Media container created: {creation_id}")

            # Phase 2: Wait for container processing (Instagram processes video)
            max_checks = 20
            for check in range(max_checks):
                time.sleep(5)  # Wait 5 seconds between checks

                status_url = f"{self.API_BASE_URL}/{creation_id}"
                status_response = requests.get(
                    status_url,
                    params={
                        "fields": "status_code",
                        "access_token": self.access_token,
                    },
                )
                status_response.raise_for_status()
                status_data = status_response.json()

                status_code = status_data.get("status_code")

                if status_code == "FINISHED":
                    # Ready to publish
                    break
                elif status_code == "ERROR":
                    logger.error("Instagram video processing failed")
                    return UploadResult(
                        success=False,
                        platform=PlatformType.INSTAGRAM,
                        error_message="Video processing failed",
                    )
                elif status_code == "EXPIRED":
                    logger.error("Instagram media container expired")
                    return UploadResult(
                        success=False,
                        platform=PlatformType.INSTAGRAM,
                        error_message="Media container expired",
                    )

                logger.info(f"Container status: {status_code} (check {check + 1}/{max_checks})")

            # Phase 3: Publish the media
            logger.info("Publishing Instagram Reel...")

            publish_url = f"{self.API_BASE_URL}/{self.instagram_user_id}/media_publish"
            publish_params = {
                "creation_id": creation_id,
                "access_token": self.access_token,
            }

            publish_response = requests.post(publish_url, params=publish_params)
            publish_response.raise_for_status()
            publish_data = publish_response.json()

            if "error" in publish_data:
                error_msg = publish_data["error"].get("message", "Unknown error")
                logger.error(f"Instagram publish failed: {error_msg}")
                return UploadResult(
                    success=False,
                    platform=PlatformType.INSTAGRAM,
                    error_message=error_msg,
                )

            media_id = publish_data.get("id")
            logger.info(f"Instagram Reel published successfully: {media_id}")

            return UploadResult(
                success=True,
                platform=PlatformType.INSTAGRAM,
                video_id=media_id,
                url=f"https://www.instagram.com/reel/{media_id}/",
                upload_time=datetime.now(),
            )

        except requests.RequestException as e:
            logger.error(f"Instagram upload request failed: {str(e)}")
            return UploadResult(
                success=False,
                platform=PlatformType.INSTAGRAM,
                error_message=str(e),
            )

    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """
        Set thumbnail for Instagram Reel (limited support).
        
        Args:
            video_id: Instagram media ID.
            thumbnail_path: Path to thumbnail (must be set during upload).
            
        Returns:
            bool: Always False (thumbnails must be set during upload).
        """
        logger.warning(
            "Instagram thumbnails must be set during upload via thumb_offset parameter"
        )
        return False


class InstagramAnalytics(IPlatformAnalytics):
    """
    Instagram analytics provider using Graph API Insights.
    
    Retrieves Reel performance metrics like plays, likes, reach, etc.
    
    Example:
        >>> analytics = InstagramAnalytics(
        ...     access_token="YOUR_TOKEN",
        ...     instagram_user_id="YOUR_IG_USER_ID"
        ... )
        >>> data = analytics.get_video_analytics("MEDIA_ID")
        >>> print(f"Plays: {data.views}, Reach: {data.impressions}")
    """

    API_BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(
        self,
        access_token: Optional[str] = None,
        instagram_user_id: Optional[str] = None,
    ):
        """
        Initialize Instagram analytics provider.
        
        Args:
            access_token: Facebook Graph API access token.
            instagram_user_id: Instagram Business/Creator account ID.
        """
        self.access_token = access_token or os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.instagram_user_id = instagram_user_id or os.getenv("INSTAGRAM_USER_ID")
        
        if not self.access_token or not self.instagram_user_id:
            logger.warning("Instagram credentials not fully configured")
        
        self._authenticated = bool(self.access_token and self.instagram_user_id)

    def authenticate(self) -> bool:
        """
        Verify Instagram authentication.
        
        Returns:
            bool: True if credentials are available.
        """
        if not self.access_token or not self.instagram_user_id:
            logger.error("Instagram access token or user ID not set")
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
        Retrieve analytics for a specific Instagram Reel.
        
        Args:
            video_id: Instagram media ID.
            start_date: Not used (Instagram returns lifetime metrics).
            end_date: Not used (Instagram returns lifetime metrics).
            
        Returns:
            VideoAnalytics: Analytics data or None if unavailable.
        """
        if not self._authenticated:
            if not self.authenticate():
                return None

        try:
            # Get insights for the media
            url = f"{self.API_BASE_URL}/{video_id}/insights"
            params = {
                "metric": "plays,likes,comments,shares,saves,reach,total_interactions",
                "access_token": self.access_token,
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                logger.error(f"Instagram API error: {data['error']}")
                return None

            # Parse metrics
            metrics = {}
            for item in data.get("data", []):
                metric_name = item.get("name")
                metric_value = item.get("values", [{}])[0].get("value", 0)
                metrics[metric_name] = metric_value

            views = metrics.get("plays", 0)
            likes = metrics.get("likes", 0)
            comments = metrics.get("comments", 0)
            shares = metrics.get("shares", 0)
            saves = metrics.get("saves", 0)
            reach = metrics.get("reach", 0)
            interactions = metrics.get("total_interactions", 0)

            engagement_rate = (interactions / max(reach, 1)) * 100 if reach > 0 else 0.0

            return VideoAnalytics(
                platform=PlatformType.INSTAGRAM,
                video_id=video_id,
                title_id="",  # Set externally
                collected_at=datetime.now(),
                views=views,
                likes=likes,
                comments=comments,
                shares=shares,
                saves=saves,
                impressions=reach,
                engagement_rate=engagement_rate,
            )

        except requests.RequestException as e:
            logger.error(f"Failed to fetch Instagram analytics: {str(e)}")
            return None

    def get_channel_analytics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve Instagram account-level analytics.
        
        Args:
            start_date: Start date for analytics.
            end_date: End date for analytics.
            
        Returns:
            Dict[str, Any]: Account analytics data.
        """
        if not self._authenticated:
            if not self.authenticate():
                return {}

        try:
            # Get account insights
            url = f"{self.API_BASE_URL}/{self.instagram_user_id}/insights"
            
            # Format dates for Instagram API
            if not end_date:
                end_date = datetime.now()
            if not start_date:
                from datetime import timedelta
                start_date = end_date - timedelta(days=30)

            params = {
                "metric": "impressions,reach,follower_count,profile_views",
                "period": "day",
                "since": int(start_date.timestamp()),
                "until": int(end_date.timestamp()),
                "access_token": self.access_token,
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                logger.error(f"Instagram API error: {data['error']}")
                return {}

            # Parse metrics
            result = {}
            for item in data.get("data", []):
                metric_name = item.get("name")
                values = item.get("values", [])
                # Sum up daily values
                total = sum(v.get("value", 0) for v in values)
                result[metric_name] = total

            return result

        except requests.RequestException as e:
            logger.error(f"Failed to fetch Instagram account analytics: {str(e)}")
            return {}
