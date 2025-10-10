"""
YouTube Platform Provider for video uploads and analytics.

This module implements the YouTube Data API v3 for programmatic video uploads
and the YouTube Analytics API for performance metrics.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

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


class YouTubeUploader(IPlatformUploader):
    """
    YouTube video upload provider using YouTube Data API v3.
    
    Requires OAuth 2.0 credentials with 'youtube.upload' scope.
    Upload quota: 1,600 units per video (out of 10,000 daily units).
    
    Example:
        >>> uploader = YouTubeUploader(credentials_path="client_secret.json")
        >>> metadata = VideoMetadata(
        ...     title="My Video",
        ...     description="Description here",
        ...     tags=["shorts", "viral"],
        ...     privacy_status=PrivacyStatus.PUBLIC
        ... )
        >>> result = uploader.upload_video("video.mp4", metadata)
    """

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
    ):
        """
        Initialize YouTube uploader.
        
        Args:
            credentials_path: Path to OAuth 2.0 client secret JSON file.
            token_path: Path to save/load OAuth tokens.
        """
        self.credentials_path = credentials_path or os.getenv(
            "YOUTUBE_CREDENTIALS_PATH", "credentials/youtube_client_secret.json"
        )
        self.token_path = token_path or os.getenv(
            "YOUTUBE_TOKEN_PATH", "credentials/youtube_token.json"
        )
        self.youtube = None
        self._authenticated = False

    def authenticate(self) -> bool:
        """
        Authenticate with YouTube using OAuth 2.0.
        
        Returns:
            bool: True if authentication successful.
            
        Raises:
            ImportError: If google-auth libraries not installed.
            FileNotFoundError: If credentials file not found.
        """
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
        except ImportError:
            logger.error(
                "Google API libraries not installed. "
                "Install with: pip install google-auth google-auth-oauthlib "
                "google-auth-httplib2 google-api-python-client"
            )
            raise

        SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

        creds = None
        # Load existing token
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # Refresh or obtain new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"YouTube credentials not found at: {self.credentials_path}"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for future use
            os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        self.youtube = build("youtube", "v3", credentials=creds)
        self._authenticated = True
        logger.info("YouTube authentication successful")
        return True

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def upload_video(
        self,
        video_path: str,
        metadata: VideoMetadata,
    ) -> UploadResult:
        """
        Upload a video to YouTube.
        
        Args:
            video_path: Path to the video file.
            metadata: Video metadata including title, description, tags, etc.
            
        Returns:
            UploadResult: Result of the upload operation.
        """
        if not self._authenticated:
            self.authenticate()

        try:
            from googleapiclient.http import MediaFileUpload
        except ImportError:
            logger.error("Google API client library not installed")
            return UploadResult(
                success=False,
                platform=PlatformType.YOUTUBE,
                error_message="Google API client library not installed",
            )

        if not os.path.exists(video_path):
            return UploadResult(
                success=False,
                platform=PlatformType.YOUTUBE,
                error_message=f"Video file not found: {video_path}",
            )

        # Build request body
        body = {
            "snippet": {
                "title": metadata.title,
                "description": metadata.description,
                "tags": metadata.tags or [],
                "categoryId": metadata.category_id or "22",  # People & Blogs
            },
            "status": {
                "privacyStatus": metadata.privacy_status.value,
                "selfDeclaredMadeForKids": metadata.made_for_kids,
            },
        }

        # Add #Shorts tag for YouTube Shorts
        if metadata.hashtags and "#Shorts" not in body["snippet"]["tags"]:
            body["snippet"]["tags"].append("#Shorts")

        logger.info(f"Uploading video to YouTube: {metadata.title}")

        try:
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media,
            )
            response = request.execute()

            video_id = response.get("id")
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            logger.info(f"Video uploaded successfully: {video_url}")

            # Set thumbnail if provided
            if metadata.thumbnail_path and os.path.exists(metadata.thumbnail_path):
                self.set_thumbnail(video_id, metadata.thumbnail_path)

            return UploadResult(
                success=True,
                platform=PlatformType.YOUTUBE,
                video_id=video_id,
                url=video_url,
                upload_time=datetime.now(),
            )

        except Exception as e:
            logger.error(f"YouTube upload failed: {str(e)}")
            return UploadResult(
                success=False,
                platform=PlatformType.YOUTUBE,
                error_message=str(e),
            )

    def set_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """
        Set a custom thumbnail for a YouTube video.
        
        Args:
            video_id: YouTube video ID.
            thumbnail_path: Path to the thumbnail image.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._authenticated:
            self.authenticate()

        try:
            from googleapiclient.http import MediaFileUpload
        except ImportError:
            logger.error("Google API client library not installed")
            return False

        if not os.path.exists(thumbnail_path):
            logger.error(f"Thumbnail file not found: {thumbnail_path}")
            return False

        try:
            media = MediaFileUpload(thumbnail_path)
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=media,
            ).execute()
            logger.info(f"Thumbnail set successfully for video {video_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to set thumbnail: {str(e)}")
            return False


class YouTubeAnalytics(IPlatformAnalytics):
    """
    YouTube analytics provider using YouTube Analytics API.
    
    Retrieves performance metrics like views, watch time, likes, etc.
    
    Example:
        >>> analytics = YouTubeAnalytics(credentials_path="client_secret.json")
        >>> data = analytics.get_video_analytics("VIDEO_ID")
        >>> print(f"Views: {data.views}, Likes: {data.likes}")
    """

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
    ):
        """
        Initialize YouTube analytics provider.
        
        Args:
            credentials_path: Path to OAuth 2.0 client secret JSON file.
            token_path: Path to save/load OAuth tokens.
        """
        self.credentials_path = credentials_path or os.getenv(
            "YOUTUBE_CREDENTIALS_PATH", "credentials/youtube_client_secret.json"
        )
        self.token_path = token_path or os.getenv(
            "YOUTUBE_TOKEN_PATH", "credentials/youtube_token.json"
        )
        self.youtube_analytics = None
        self.youtube_data = None
        self._authenticated = False

    def authenticate(self) -> bool:
        """
        Authenticate with YouTube Analytics API.
        
        Returns:
            bool: True if authentication successful.
        """
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
        except ImportError:
            logger.error("Google API libraries not installed")
            raise

        SCOPES = [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/yt-analytics.readonly",
        ]

        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"YouTube credentials not found at: {self.credentials_path}"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        self.youtube_analytics = build("youtubeAnalytics", "v2", credentials=creds)
        self.youtube_data = build("youtube", "v3", credentials=creds)
        self._authenticated = True
        logger.info("YouTube Analytics authentication successful")
        return True

    @retry(
        retry=retry_if_exception_type(Exception),
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
        Retrieve analytics for a specific YouTube video.
        
        Args:
            video_id: YouTube video ID.
            start_date: Start date for analytics (default: 7 days ago).
            end_date: End date for analytics (default: today).
            
        Returns:
            VideoAnalytics: Analytics data or None if unavailable.
        """
        if not self._authenticated:
            self.authenticate()

        from datetime import timedelta

        if not end_date:
            end_date = datetime.now()
        if not start_date:
            start_date = end_date - timedelta(days=7)

        try:
            # Query analytics
            response = self.youtube_analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics="views,likes,comments,shares,estimatedMinutesWatched,averageViewDuration",
                dimensions="video",
                filters=f"video=={video_id}",
            ).execute()

            if not response.get("rows"):
                logger.warning(f"No analytics data found for video {video_id}")
                return None

            row = response["rows"][0]
            
            # Parse metrics (order matches metrics parameter)
            views = int(row[1]) if len(row) > 1 else 0
            likes = int(row[2]) if len(row) > 2 else 0
            comments = int(row[3]) if len(row) > 3 else 0
            shares = int(row[4]) if len(row) > 4 else 0
            watch_time_minutes = float(row[5]) if len(row) > 5 else 0.0
            avg_view_duration = float(row[6]) if len(row) > 6 else 0.0

            return VideoAnalytics(
                platform=PlatformType.YOUTUBE,
                video_id=video_id,
                title_id="",  # Set externally
                collected_at=datetime.now(),
                views=views,
                likes=likes,
                comments=comments,
                shares=shares,
                watch_time_seconds=watch_time_minutes * 60,
                average_view_duration=avg_view_duration,
                engagement_rate=(likes + comments + shares) / max(views, 1) * 100,
            )

        except Exception as e:
            logger.error(f"Failed to fetch YouTube analytics: {str(e)}")
            return None

    def get_channel_analytics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve channel-level analytics.
        
        Args:
            start_date: Start date for analytics (default: 30 days ago).
            end_date: End date for analytics (default: today).
            
        Returns:
            Dict[str, Any]: Channel analytics data.
        """
        if not self._authenticated:
            self.authenticate()

        from datetime import timedelta

        if not end_date:
            end_date = datetime.now()
        if not start_date:
            start_date = end_date - timedelta(days=30)

        try:
            response = self.youtube_analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date.strftime("%Y-%m-%d"),
                endDate=end_date.strftime("%Y-%m-%d"),
                metrics="views,likes,comments,shares,subscribersGained,subscribersLost,estimatedMinutesWatched",
            ).execute()

            if not response.get("rows"):
                return {}

            row = response["rows"][0]
            
            return {
                "views": int(row[0]) if len(row) > 0 else 0,
                "likes": int(row[1]) if len(row) > 1 else 0,
                "comments": int(row[2]) if len(row) > 2 else 0,
                "shares": int(row[3]) if len(row) > 3 else 0,
                "subscribers_gained": int(row[4]) if len(row) > 4 else 0,
                "subscribers_lost": int(row[5]) if len(row) > 5 else 0,
                "watch_time_minutes": float(row[6]) if len(row) > 6 else 0.0,
            }

        except Exception as e:
            logger.error(f"Failed to fetch channel analytics: {str(e)}")
            return {}
