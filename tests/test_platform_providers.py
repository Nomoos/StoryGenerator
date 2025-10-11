"""
Tests for platform provider interfaces and implementations.

Tests the YouTube, TikTok, and Instagram upload and analytics providers.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock, mock_open
import os
import sys

from PrismQ.Shared.interfaces.platform_provider import (
    IPlatformUploader,
    IPlatformAnalytics,
    PlatformType,
    PrivacyStatus,
    VideoMetadata,
    UploadResult,
    VideoAnalytics,
)

# Skip all tests if platform provider dependencies aren't available
pytest_plugins = []

try:
    import providers.youtube_provider
    import providers.tiktok_provider
    import providers.instagram_provider
    PROVIDERS_AVAILABLE = True
except ImportError as e:
    PROVIDERS_AVAILABLE = False
    skip_reason = f"Platform provider dependencies not available: {e}"

pytestmark = pytest.mark.skipif(not PROVIDERS_AVAILABLE, reason="Platform providers not available")


# Test fixtures

@pytest.fixture
def video_metadata():
    """Sample video metadata."""
    return VideoMetadata(
        title="Test Video",
        description="Test description",
        tags=["test", "shorts"],
        privacy_status=PrivacyStatus.PUBLIC,
        hashtags=["viral", "fyp"],
    )


@pytest.fixture
def mock_video_file(tmp_path):
    """Create a mock video file."""
    video_path = tmp_path / "test_video.mp4"
    video_path.write_bytes(b"fake video content")
    return str(video_path)


# YouTube Provider Tests

class TestYouTubeUploader:
    """Tests for YouTubeUploader."""

    def test_uploader_initialization(self):
        """Test YouTube uploader initialization."""
        from providers.youtube_provider import YouTubeUploader

        uploader = YouTubeUploader(
            credentials_path="test_creds.json",
            token_path="test_token.json",
        )
        
        assert uploader.credentials_path == "test_creds.json"
        assert uploader.token_path == "test_token.json"
        assert not uploader._authenticated

    def test_uploader_implements_interface(self):
        """Test that YouTubeUploader implements IPlatformUploader."""
        from providers.youtube_provider import YouTubeUploader

        assert issubclass(YouTubeUploader, IPlatformUploader)

    def test_authentication_with_existing_token(self):
        """Test authentication with existing valid token."""
        from providers.youtube_provider import YouTubeUploader

        # Skip if Google libraries not available
        try:
            import google.oauth2.credentials
        except ImportError:
            pytest.skip("Google API libraries not installed")

        with patch("os.path.exists", return_value=True), \
             patch("google.oauth2.credentials.Credentials.from_authorized_user_file") as mock_creds:
            
            mock_creds_instance = Mock()
            mock_creds_instance.valid = True
            mock_creds.return_value = mock_creds_instance

            with patch("googleapiclient.discovery.build"):
                uploader = YouTubeUploader()
                result = uploader.authenticate()

                assert result is True
                assert uploader._authenticated is True

    def test_upload_video_success(self, mock_video_file, video_metadata):
        """Test successful video upload."""
        from providers.youtube_provider import YouTubeUploader

        # Skip if Google libraries not available
        try:
            import googleapiclient.http
        except ImportError:
            pytest.skip("Google API libraries not installed")

        with patch("os.path.exists", return_value=True), \
             patch("googleapiclient.http.MediaFileUpload"):
            
            # Mock YouTube API
            mock_youtube = Mock()
            mock_response = {"id": "test_video_id_123"}
            mock_youtube.videos().insert().execute.return_value = mock_response

            uploader = YouTubeUploader()
            uploader.youtube = mock_youtube
            uploader._authenticated = True

            result = uploader.upload_video(mock_video_file, video_metadata)

            assert result.success is True
            assert result.platform == PlatformType.YOUTUBE
            assert result.video_id == "test_video_id_123"
            assert "youtube.com/watch" in result.url

    def test_upload_video_file_not_found(self, video_metadata):
        """Test upload with non-existent file."""
        from providers.youtube_provider import YouTubeUploader

        # Skip if Google libraries not available
        try:
            import googleapiclient.http
        except ImportError:
            pytest.skip("Google API libraries not installed")

        with patch("googleapiclient.http.MediaFileUpload"):
            uploader = YouTubeUploader()
            uploader._authenticated = True

            result = uploader.upload_video("/nonexistent/video.mp4", video_metadata)

            assert result.success is False
            assert "not found" in result.error_message.lower()


class TestYouTubeAnalytics:
    """Tests for YouTubeAnalytics."""

    def test_analytics_initialization(self):
        """Test YouTube analytics initialization."""
        from providers.youtube_provider import YouTubeAnalytics

        analytics = YouTubeAnalytics(
            credentials_path="test_creds.json",
            token_path="test_token.json",
        )
        
        assert analytics.credentials_path == "test_creds.json"
        assert analytics.token_path == "test_token.json"
        assert not analytics._authenticated

    def test_analytics_implements_interface(self):
        """Test that YouTubeAnalytics implements IPlatformAnalytics."""
        from providers.youtube_provider import YouTubeAnalytics

        assert issubclass(YouTubeAnalytics, IPlatformAnalytics)

    def test_get_video_analytics_success(self):
        """Test successful video analytics retrieval."""
        from providers.youtube_provider import YouTubeAnalytics

        # Mock YouTube Analytics API response
        mock_response = {
            "rows": [
                ["video_id", 1000, 50, 10, 5, 500.0, 60.0]
            ]
        }

        mock_youtube_analytics = Mock()
        mock_youtube_analytics.reports().query().execute.return_value = mock_response

        analytics = YouTubeAnalytics()
        analytics.youtube_analytics = mock_youtube_analytics
        analytics._authenticated = True

        result = analytics.get_video_analytics("test_video_id")

        assert result is not None
        assert result.platform == PlatformType.YOUTUBE
        assert result.video_id == "test_video_id"
        assert result.views == 1000
        assert result.likes == 50
        assert result.comments == 10
        assert result.shares == 5

    def test_get_video_analytics_no_data(self):
        """Test analytics retrieval with no data available."""
        from providers.youtube_provider import YouTubeAnalytics

        mock_response = {"rows": []}
        
        mock_youtube_analytics = Mock()
        mock_youtube_analytics.reports().query().execute.return_value = mock_response

        analytics = YouTubeAnalytics()
        analytics.youtube_analytics = mock_youtube_analytics
        analytics._authenticated = True

        result = analytics.get_video_analytics("test_video_id")

        assert result is None


# TikTok Provider Tests

class TestTikTokUploader:
    """Tests for TikTokUploader."""

    def test_uploader_initialization(self):
        """Test TikTok uploader initialization."""
        from providers.tiktok_provider import TikTokUploader

        uploader = TikTokUploader(access_token="test_token")
        
        assert uploader.access_token == "test_token"
        assert uploader._authenticated is True

    def test_uploader_implements_interface(self):
        """Test that TikTokUploader implements IPlatformUploader."""
        from providers.tiktok_provider import TikTokUploader

        assert issubclass(TikTokUploader, IPlatformUploader)

    def test_authentication(self):
        """Test TikTok authentication."""
        from providers.tiktok_provider import TikTokUploader

        uploader = TikTokUploader(access_token="test_token")
        result = uploader.authenticate()

        assert result is True
        assert uploader._authenticated is True

    @patch("requests.post")
    @patch("requests.put")
    @patch("os.path.exists")
    @patch("os.path.getsize")
    def test_upload_video_success(
        self,
        mock_getsize,
        mock_exists,
        mock_put,
        mock_post,
        mock_video_file,
        video_metadata,
    ):
        """Test successful TikTok video upload."""
        from providers.tiktok_provider import TikTokUploader

        mock_exists.return_value = True
        mock_getsize.return_value = 1024

        # Mock API responses
        init_response = Mock()
        init_response.json.return_value = {
            "data": {
                "publish_id": "test_publish_123",
                "upload_url": "https://upload.tiktok.com/test",
            }
        }
        init_response.raise_for_status = Mock()

        status_response = Mock()
        status_response.json.return_value = {
            "data": {
                "status": "PUBLISH_COMPLETE",
                "video_id": "test_video_456",
            }
        }
        status_response.raise_for_status = Mock()

        mock_post.side_effect = [init_response, status_response]
        mock_put.return_value = Mock(raise_for_status=Mock())

        with patch("builtins.open", mock_open(read_data=b"video data")):
            uploader = TikTokUploader(access_token="test_token")
            result = uploader.upload_video(mock_video_file, video_metadata)

        assert result.success is True
        assert result.platform == PlatformType.TIKTOK
        assert result.video_id == "test_video_456"

    def test_set_thumbnail_not_supported(self):
        """Test that TikTok doesn't support custom thumbnails."""
        from providers.tiktok_provider import TikTokUploader

        uploader = TikTokUploader(access_token="test_token")
        result = uploader.set_thumbnail("video_id", "thumb.jpg")

        assert result is False


class TestTikTokAnalytics:
    """Tests for TikTokAnalytics."""

    def test_analytics_initialization(self):
        """Test TikTok analytics initialization."""
        from providers.tiktok_provider import TikTokAnalytics

        analytics = TikTokAnalytics(access_token="test_token")
        
        assert analytics.access_token == "test_token"
        assert analytics._authenticated is True

    def test_analytics_implements_interface(self):
        """Test that TikTokAnalytics implements IPlatformAnalytics."""
        from providers.tiktok_provider import TikTokAnalytics

        assert issubclass(TikTokAnalytics, IPlatformAnalytics)

    @patch("requests.post")
    def test_get_video_analytics_success(self, mock_post):
        """Test successful TikTok video analytics retrieval."""
        from providers.tiktok_provider import TikTokAnalytics

        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {
                "videos": [
                    {
                        "id": "test_video_id",
                        "view_count": 5000,
                        "like_count": 200,
                        "comment_count": 50,
                        "share_count": 30,
                        "reach": 10000,
                        "engagement_rate": 5.6,
                    }
                ]
            }
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        analytics = TikTokAnalytics(access_token="test_token")
        result = analytics.get_video_analytics("test_video_id")

        assert result is not None
        assert result.platform == PlatformType.TIKTOK
        assert result.views == 5000
        assert result.likes == 200
        assert result.comments == 50


# Instagram Provider Tests

class TestInstagramUploader:
    """Tests for InstagramUploader."""

    def test_uploader_initialization(self):
        """Test Instagram uploader initialization."""
        from providers.instagram_provider import InstagramUploader

        uploader = InstagramUploader(
            access_token="test_token",
            instagram_user_id="test_user_id",
        )
        
        assert uploader.access_token == "test_token"
        assert uploader.instagram_user_id == "test_user_id"
        assert uploader._authenticated is True

    def test_uploader_implements_interface(self):
        """Test that InstagramUploader implements IPlatformUploader."""
        from providers.instagram_provider import InstagramUploader

        assert issubclass(InstagramUploader, IPlatformUploader)

    def test_authentication(self):
        """Test Instagram authentication."""
        from providers.instagram_provider import InstagramUploader

        uploader = InstagramUploader(
            access_token="test_token",
            instagram_user_id="test_user_id",
        )
        result = uploader.authenticate()

        assert result is True
        assert uploader._authenticated is True

    def test_upload_local_file_rejected(self, mock_video_file, video_metadata):
        """Test that local files are rejected (Instagram requires URLs)."""
        from providers.instagram_provider import InstagramUploader

        uploader = InstagramUploader(
            access_token="test_token",
            instagram_user_id="test_user_id",
        )
        
        result = uploader.upload_video(mock_video_file, video_metadata)

        assert result.success is False
        assert "public URL" in result.error_message

    @patch("requests.post")
    @patch("requests.get")
    def test_upload_video_from_url_success(
        self, mock_get, mock_post, video_metadata
    ):
        """Test successful Instagram upload from URL."""
        from providers.instagram_provider import InstagramUploader

        # Mock container creation
        container_response = Mock()
        container_response.json.return_value = {"id": "container_123"}
        container_response.raise_for_status = Mock()

        # Mock status check
        status_response = Mock()
        status_response.json.return_value = {"status_code": "FINISHED"}
        status_response.raise_for_status = Mock()

        # Mock publish
        publish_response = Mock()
        publish_response.json.return_value = {"id": "media_456"}
        publish_response.raise_for_status = Mock()

        mock_post.side_effect = [container_response, publish_response]
        mock_get.return_value = status_response

        uploader = InstagramUploader(
            access_token="test_token",
            instagram_user_id="test_user_id",
        )
        
        result = uploader.upload_video(
            "https://example.com/video.mp4", video_metadata
        )

        assert result.success is True
        assert result.platform == PlatformType.INSTAGRAM
        assert result.video_id == "media_456"


class TestInstagramAnalytics:
    """Tests for InstagramAnalytics."""

    def test_analytics_initialization(self):
        """Test Instagram analytics initialization."""
        from providers.instagram_provider import InstagramAnalytics

        analytics = InstagramAnalytics(
            access_token="test_token",
            instagram_user_id="test_user_id",
        )
        
        assert analytics.access_token == "test_token"
        assert analytics.instagram_user_id == "test_user_id"
        assert analytics._authenticated is True

    def test_analytics_implements_interface(self):
        """Test that InstagramAnalytics implements IPlatformAnalytics."""
        from providers.instagram_provider import InstagramAnalytics

        assert issubclass(InstagramAnalytics, IPlatformAnalytics)

    @patch("requests.get")
    def test_get_video_analytics_success(self, mock_get):
        """Test successful Instagram analytics retrieval."""
        from providers.instagram_provider import InstagramAnalytics

        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {"name": "plays", "values": [{"value": 2000}]},
                {"name": "likes", "values": [{"value": 100}]},
                {"name": "comments", "values": [{"value": 25}]},
                {"name": "shares", "values": [{"value": 15}]},
                {"name": "saves", "values": [{"value": 40}]},
                {"name": "reach", "values": [{"value": 5000}]},
                {"name": "total_interactions", "values": [{"value": 180}]},
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        analytics = InstagramAnalytics(
            access_token="test_token",
            instagram_user_id="test_user_id",
        )
        result = analytics.get_video_analytics("test_media_id")

        assert result is not None
        assert result.platform == PlatformType.INSTAGRAM
        assert result.views == 2000
        assert result.likes == 100
        assert result.saves == 40


# Integration Tests

class TestPlatformIntegration:
    """Integration tests for platform providers."""

    def test_all_uploaders_implement_interface(self):
        """Verify all uploader classes implement the interface."""
        from providers.youtube_provider import YouTubeUploader
        from providers.tiktok_provider import TikTokUploader
        from providers.instagram_provider import InstagramUploader

        uploaders = [YouTubeUploader, TikTokUploader, InstagramUploader]
        
        for uploader_class in uploaders:
            assert issubclass(uploader_class, IPlatformUploader)

    def test_all_analytics_implement_interface(self):
        """Verify all analytics classes implement the interface."""
        from providers.youtube_provider import YouTubeAnalytics
        from providers.tiktok_provider import TikTokAnalytics
        from providers.instagram_provider import InstagramAnalytics

        analytics_classes = [YouTubeAnalytics, TikTokAnalytics, InstagramAnalytics]
        
        for analytics_class in analytics_classes:
            assert issubclass(analytics_class, IPlatformAnalytics)

    def test_video_metadata_creation(self):
        """Test VideoMetadata dataclass creation."""
        metadata = VideoMetadata(
            title="Test",
            description="Description",
            tags=["tag1", "tag2"],
            privacy_status=PrivacyStatus.PUBLIC,
        )
        
        assert metadata.title == "Test"
        assert metadata.description == "Description"
        assert len(metadata.tags) == 2
        assert metadata.privacy_status == PrivacyStatus.PUBLIC

    def test_upload_result_creation(self):
        """Test UploadResult dataclass creation."""
        result = UploadResult(
            success=True,
            platform=PlatformType.YOUTUBE,
            video_id="test_id",
            url="https://youtube.com/watch?v=test_id",
            upload_time=datetime.now(),
        )
        
        assert result.success is True
        assert result.platform == PlatformType.YOUTUBE
        assert result.video_id == "test_id"
        assert result.url is not None

    def test_video_analytics_creation(self):
        """Test VideoAnalytics dataclass creation."""
        analytics = VideoAnalytics(
            platform=PlatformType.YOUTUBE,
            video_id="test_id",
            title_id="title_123",
            collected_at=datetime.now(),
            views=1000,
            likes=50,
            engagement_rate=5.0,
        )
        
        assert analytics.platform == PlatformType.YOUTUBE
        assert analytics.views == 1000
        assert analytics.likes == 50
        assert analytics.engagement_rate == 5.0
