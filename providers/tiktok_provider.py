"""
TikTok Platform Provider for video uploads and analytics.

This module implements TikTok's Content Posting API for direct video uploads
and the TikTok Business API for analytics retrieval.
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

from PrismQ.Shared.interfaces.platform_provider import (
    IPlatformUploader,
    IPlatformAnalytics,
    PlatformType,
    VideoMetadata,
    UploadResult,
    VideoAnalytics,
    PrivacyStatus,
)


logger = logging.getLogger(__name__)


class TikTokUploader(IPlatformUploader):
    """
    TikTok video upload provider using Content Posting API.
    
    Requires TikTok app registration and OAuth bearer token.
    Two-phase upload: initiate upload, then PUT video bytes.
    
    Example:
        >>> uploader = TikTokUploader(access_token="YOUR_TOKEN")
        >>> metadata = VideoMetadata(
        ...     title="My TikTok Video",
        ...     caption="Check this out! #fyp",
        ...     hashtags=["fyp", "viral"],
        ...     privacy_status=PrivacyStatus.PUBLIC
        ... )
        >>> result = uploader.upload_video("video.mp4", metadata)
    """

    API_BASE_URL = "https://open.tiktokapis.com/v2"

    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize TikTok uploader.
        
        Args:
            access_token: OAuth access token for TikTok API.
        """
        self.access_token = access_token or os.getenv("TIKTOK_ACCESS_TOKEN")
        if not self.access_token:
            logger.warning("No TikTok access token provided")
        self._authenticated = bool(self.access_token)

    def authenticate(self) -> bool:
        """
        Verify TikTok authentication.
        
        Returns:
            bool: True if access token is available.
        """
        if not self.access_token:
            logger.error("TikTok access token not set")
            return False
        self._authenticated = True
        return True

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authorization."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

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
        Upload a video to TikTok using Content Posting API.
        
        Args:
            video_path: Path to the video file.
            metadata: Video metadata including caption and hashtags.
            
        Returns:
            UploadResult: Result of the upload operation.
        """
        if not self._authenticated:
            if not self.authenticate():
                return UploadResult(
                    success=False,
                    platform=PlatformType.TIKTOK,
                    error_message="Authentication failed",
                )

        if not os.path.exists(video_path):
            return UploadResult(
                success=False,
                platform=PlatformType.TIKTOK,
                error_message=f"Video file not found: {video_path}",
            )

        # Get video file size
        video_size = os.path.getsize(video_path)

        # Map privacy status
        privacy_level_map = {
            PrivacyStatus.PUBLIC: "PUBLIC_TO_EVERYONE",
            PrivacyStatus.PRIVATE: "SELF_ONLY",
            PrivacyStatus.UNLISTED: "MUTUAL_FOLLOW_FRIENDS",
        }

        # Build caption with hashtags
        caption = metadata.caption or metadata.description or metadata.title
        if metadata.hashtags:
            hashtag_str = " ".join([f"#{tag}" for tag in metadata.hashtags])
            caption = f"{caption} {hashtag_str}".strip()

        # Phase 1: Initiate upload
        logger.info(f"Initiating TikTok upload: {metadata.title}")

        init_payload = {
            "post_info": {
                "title": metadata.title[:150],  # TikTok max title length
                "privacy_level": privacy_level_map[metadata.privacy_status],
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
                "video_cover_timestamp_ms": 1000,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size,
                "chunk_size": video_size,  # Single chunk upload
                "total_chunk_count": 1,
            },
        }

        try:
            # Initiate upload
            response = requests.post(
                f"{self.API_BASE_URL}/post/publish/video/init/",
                headers=self._get_headers(),
                json=init_payload,
            )
            response.raise_for_status()
            init_data = response.json()

            if init_data.get("error"):
                error_msg = init_data["error"].get("message", "Unknown error")
                logger.error(f"TikTok upload init failed: {error_msg}")
                return UploadResult(
                    success=False,
                    platform=PlatformType.TIKTOK,
                    error_message=error_msg,
                )

            publish_id = init_data["data"]["publish_id"]
            upload_url = init_data["data"]["upload_url"]

            # Phase 2: Upload video file
            logger.info(f"Uploading video to TikTok (publish_id: {publish_id})")

            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()

            upload_headers = {
                "Content-Type": "video/mp4",
                "Content-Range": f"bytes 0-{video_size - 1}/{video_size}",
            }

            upload_response = requests.put(
                upload_url,
                headers=upload_headers,
                data=video_bytes,
            )
            upload_response.raise_for_status()

            # Phase 3: Check upload status
            logger.info("Checking TikTok upload status...")
            status_url = f"{self.API_BASE_URL}/post/publish/status/fetch/"
            
            max_attempts = 10
            for attempt in range(max_attempts):
                time.sleep(3)  # Wait before checking status
                
                status_response = requests.post(
                    status_url,
                    headers=self._get_headers(),
                    json={"publish_id": publish_id},
                )
                status_response.raise_for_status()
                status_data = status_response.json()

                status = status_data["data"]["status"]
                
                if status == "PUBLISH_COMPLETE":
                    video_id = status_data["data"].get("video_id")
                    logger.info(f"TikTok upload successful: {video_id}")
                    
                    return UploadResult(
                        success=True,
                        platform=PlatformType.TIKTOK,
                        video_id=video_id,
                        url=f"https://www.tiktok.com/@user/video/{video_id}" if video_id else None,
                        upload_time=datetime.now(),
                    )
                elif status == "FAILED":
                    error_msg = status_data["data"].get("fail_reason", "Upload failed")
                    logger.error(f"TikTok upload failed: {error_msg}")
                    return UploadResult(
                        success=False,
                        platform=PlatformType.TIKTOK,
                        error_message=error_msg,
                    )
                
                # Still processing, continue waiting
                logger.info(f"Upload status: {status} (attempt {attempt + 1}/{max_attempts})")

            # Timeout waiting for completion
            return UploadResult(
                success=False,
                platform=PlatformType.TIKTOK,
                error_message="Upload status check timeout",
            )

        except requests.RequestException as e:
            logger.error(f"TikTok upload request failed: {str(e)}")
            return UploadResult(
                success=False,
                platform=PlatformType.TIKTOK,
                error_message=str(e),
            )

    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """
        Set custom thumbnail (TikTok uses video frame as cover).
        
        Args:
            video_id: TikTok video ID.
            thumbnail_path: Path to thumbnail (not used by TikTok).
            
        Returns:
            bool: Always False (TikTok auto-generates thumbnails).
        """
        logger.warning("TikTok does not support custom thumbnail uploads")
        return False


class TikTokAnalytics(IPlatformAnalytics):
    """
    TikTok analytics provider using Business/Creator API.
    
    Retrieves video and profile metrics like views, likes, shares, etc.
    
    Example:
        >>> analytics = TikTokAnalytics(access_token="YOUR_TOKEN")
        >>> data = analytics.get_video_analytics("VIDEO_ID")
        >>> print(f"Views: {data.views}, Engagement: {data.engagement_rate}%")
    """

    API_BASE_URL = "https://open.tiktokapis.com/v2"

    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize TikTok analytics provider.
        
        Args:
            access_token: OAuth access token for TikTok API.
        """
        self.access_token = access_token or os.getenv("TIKTOK_ACCESS_TOKEN")
        if not self.access_token:
            logger.warning("No TikTok access token provided")
        self._authenticated = bool(self.access_token)

    def authenticate(self) -> bool:
        """
        Verify TikTok authentication.
        
        Returns:
            bool: True if access token is available.
        """
        if not self.access_token:
            logger.error("TikTok access token not set")
            return False
        self._authenticated = True
        return True

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authorization."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

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
        Retrieve analytics for a specific TikTok video.
        
        Args:
            video_id: TikTok video ID.
            start_date: Not used (TikTok returns lifetime metrics).
            end_date: Not used (TikTok returns lifetime metrics).
            
        Returns:
            VideoAnalytics: Analytics data or None if unavailable.
        """
        if not self._authenticated:
            if not self.authenticate():
                return None

        try:
            # TikTok video insights endpoint
            url = f"{self.API_BASE_URL}/video/query/"
            payload = {
                "filters": {
                    "video_ids": [video_id],
                },
                "fields": [
                    "id",
                    "view_count",
                    "like_count",
                    "comment_count",
                    "share_count",
                    "reach",
                    "engagement_rate",
                ],
            }

            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("error"):
                logger.error(f"TikTok API error: {data['error']}")
                return None

            videos = data.get("data", {}).get("videos", [])
            if not videos:
                logger.warning(f"No data found for TikTok video {video_id}")
                return None

            video_data = videos[0]

            return VideoAnalytics(
                platform=PlatformType.TIKTOK,
                video_id=video_id,
                title_id="",  # Set externally
                collected_at=datetime.now(),
                views=video_data.get("view_count", 0),
                likes=video_data.get("like_count", 0),
                comments=video_data.get("comment_count", 0),
                shares=video_data.get("share_count", 0),
                impressions=video_data.get("reach", 0),
                engagement_rate=video_data.get("engagement_rate", 0.0),
            )

        except requests.RequestException as e:
            logger.error(f"Failed to fetch TikTok analytics: {str(e)}")
            return None

    def get_channel_analytics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve user/profile-level analytics.
        
        Args:
            start_date: Start date for analytics.
            end_date: End date for analytics.
            
        Returns:
            Dict[str, Any]: Profile analytics data.
        """
        if not self._authenticated:
            if not self.authenticate():
                return {}

        try:
            url = f"{self.API_BASE_URL}/research/user/info/"
            
            # Format dates for TikTok API
            if not end_date:
                end_date = datetime.now()
            if not start_date:
                from datetime import timedelta
                start_date = end_date - timedelta(days=30)

            payload = {
                "fields": [
                    "follower_count",
                    "following_count",
                    "video_count",
                    "likes_count",
                ],
            }

            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("error"):
                logger.error(f"TikTok API error: {data['error']}")
                return {}

            user_data = data.get("data", {}).get("user", {})
            
            return {
                "follower_count": user_data.get("follower_count", 0),
                "following_count": user_data.get("following_count", 0),
                "video_count": user_data.get("video_count", 0),
                "total_likes": user_data.get("likes_count", 0),
            }

        except requests.RequestException as e:
            logger.error(f"Failed to fetch TikTok profile analytics: {str(e)}")
            return {}
