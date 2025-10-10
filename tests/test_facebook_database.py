"""
Tests for Facebook provider, database integration, and cross-platform comparison.

Tests the new functionality requested:
1. Facebook video API integration
2. Database storage for text data
3. Cross-platform performance comparison
"""

import pytest
import tempfile
import os
from datetime import datetime
from unittest.mock import Mock, patch
from pathlib import Path

from core.interfaces.platform_provider import (
    IPlatformUploader,
    IPlatformAnalytics,
    PlatformType,
    PrivacyStatus,
    VideoMetadata,
    UploadResult,
    VideoAnalytics,
)


# Facebook Provider Tests

class TestFacebookUploader:
    """Tests for FacebookUploader."""

    def test_uploader_initialization(self):
        """Test Facebook uploader initialization."""
        from providers.facebook_provider import FacebookUploader

        uploader = FacebookUploader(
            access_token="test_token",
            page_id="test_page_id",
        )
        
        assert uploader.access_token == "test_token"
        assert uploader.page_id == "test_page_id"
        assert uploader._authenticated is True

    def test_uploader_implements_interface(self):
        """Test that FacebookUploader implements IPlatformUploader."""
        from providers.facebook_provider import FacebookUploader

        assert issubclass(FacebookUploader, IPlatformUploader)

    def test_authentication(self):
        """Test Facebook authentication."""
        from providers.facebook_provider import FacebookUploader

        uploader = FacebookUploader(
            access_token="test_token",
            page_id="test_page_id",
        )
        result = uploader.authenticate()

        assert result is True
        assert uploader._authenticated is True

    @patch("requests.post")
    def test_upload_video_from_url_success(self, mock_post):
        """Test successful Facebook upload from URL."""
        from providers.facebook_provider import FacebookUploader

        mock_response = Mock()
        mock_response.json.return_value = {"id": "fb_video_123"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        uploader = FacebookUploader(
            access_token="test_token",
            page_id="test_page_id",
        )
        
        metadata = VideoMetadata(
            title="Test Video",
            description="Test description",
        )
        
        result = uploader.upload_video("https://example.com/video.mp4", metadata)

        assert result.success is True
        assert result.platform == PlatformType.FACEBOOK
        assert result.video_id == "fb_video_123"

    def test_set_thumbnail_not_supported(self):
        """Test that Facebook doesn't support custom thumbnails via API."""
        from providers.facebook_provider import FacebookUploader

        uploader = FacebookUploader(
            access_token="test_token",
            page_id="test_page_id",
        )
        result = uploader.set_thumbnail("video_id", "thumb.jpg")

        assert result is False


class TestFacebookAnalytics:
    """Tests for FacebookAnalytics."""

    def test_analytics_initialization(self):
        """Test Facebook analytics initialization."""
        from providers.facebook_provider import FacebookAnalytics

        analytics = FacebookAnalytics(
            access_token="test_token",
            page_id="test_page_id",
        )
        
        assert analytics.access_token == "test_token"
        assert analytics.page_id == "test_page_id"
        assert analytics._authenticated is True

    def test_analytics_implements_interface(self):
        """Test that FacebookAnalytics implements IPlatformAnalytics."""
        from providers.facebook_provider import FacebookAnalytics

        assert issubclass(FacebookAnalytics, IPlatformAnalytics)

    @patch("requests.get")
    def test_get_video_analytics_success(self, mock_get):
        """Test successful Facebook analytics retrieval."""
        from providers.facebook_provider import FacebookAnalytics

        mock_response = Mock()
        mock_response.json.return_value = {
            "views": 10000,
            "likes": {"summary": {"total_count": 500}},
            "comments": {"summary": {"total_count": 75}},
            "shares": {"count": 50},
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        analytics = FacebookAnalytics(
            access_token="test_token",
            page_id="test_page_id",
        )
        result = analytics.get_video_analytics("fb_video_123")

        assert result is not None
        assert result.platform == PlatformType.FACEBOOK
        assert result.views == 10000
        assert result.likes == 500
        assert result.comments == 75
        assert result.shares == 50


# Database Tests

class TestPlatformDatabase:
    """Tests for PlatformDatabase."""

    def test_database_initialization(self):
        """Test database creation and schema initialization."""
        from core.database import PlatformDatabase

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            db = PlatformDatabase(db_path)
            db.initialize()
            
            # Check that tables exist
            conn = db.connect()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('videos', 'analytics')
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            assert "videos" in tables
            assert "analytics" in tables
            
            db.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)

    def test_save_upload_result(self):
        """Test saving upload result to database."""
        from core.database import PlatformDatabase

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            db = PlatformDatabase(db_path)
            db.initialize()
            
            result = UploadResult(
                success=True,
                platform=PlatformType.YOUTUBE,
                video_id="test_video_123",
                url="https://youtube.com/watch?v=test_video_123",
                upload_time=datetime.now(),
            )
            
            row_id = db.save_upload_result(
                result,
                title_id="test_story",
                title="Test Title",
                description="Test description",
            )
            
            assert row_id > 0
            
            # Verify saved
            video = db.get_video_by_title_id("test_story", "youtube")
            assert video is not None
            assert video["video_id"] == "test_video_123"
            assert video["title"] == "Test Title"
            
            db.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)

    def test_save_analytics(self):
        """Test saving analytics data to database."""
        from core.database import PlatformDatabase

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            db = PlatformDatabase(db_path)
            db.initialize()
            
            # First save upload result
            result = UploadResult(
                success=True,
                platform=PlatformType.YOUTUBE,
                video_id="test_video_123",
                url="https://youtube.com/watch?v=test_video_123",
                upload_time=datetime.now(),
            )
            
            db.save_upload_result(
                result,
                title_id="test_story",
                title="Test Title",
            )
            
            # Then save analytics
            analytics = VideoAnalytics(
                platform=PlatformType.YOUTUBE,
                video_id="test_video_123",
                title_id="test_story",
                collected_at=datetime.now(),
                views=1000,
                likes=50,
                engagement_rate=5.0,
            )
            
            row_id = db.save_analytics(analytics)
            assert row_id > 0
            
            # Verify saved
            saved_analytics = db.get_latest_analytics("test_video_123", "youtube")
            assert saved_analytics is not None
            assert saved_analytics["views"] == 1000
            assert saved_analytics["likes"] == 50
            
            db.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)


# Cross-Platform Comparison Tests

class TestPlatformComparator:
    """Tests for PlatformComparator."""

    def test_compare_video(self):
        """Test cross-platform comparison."""
        from core.database import PlatformDatabase
        from core.platform_comparison import PlatformComparator

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            db = PlatformDatabase(db_path)
            db.initialize()
            
            # Add data for multiple platforms
            title_id = "test_story"
            
            for platform, video_id, views in [
                (PlatformType.YOUTUBE, "yt_123", 1000),
                (PlatformType.TIKTOK, "tt_456", 5000),
            ]:
                result = UploadResult(
                    success=True,
                    platform=platform,
                    video_id=video_id,
                    url=f"https://{platform.value}.com/{video_id}",
                    upload_time=datetime.now(),
                )
                
                db.save_upload_result(result, title_id, "Test Title")
                
                analytics = VideoAnalytics(
                    platform=platform,
                    video_id=video_id,
                    title_id=title_id,
                    collected_at=datetime.now(),
                    views=views,
                    likes=int(views * 0.05),
                    engagement_rate=5.0,
                )
                
                db.save_analytics(analytics)
            
            db.close()
            
            # Test comparison
            comparator = PlatformComparator(db_path)
            comparison = comparator.compare_video(title_id)
            
            assert comparison is not None
            assert comparison.title_id == title_id
            assert len(comparison.platforms) == 2
            assert comparison.total_views == 6000
            
            # Test best platform
            best = comparison.get_best_platform("views")
            assert best.platform == "tiktok"
            assert best.views == 5000
            
            comparator.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)

    def test_generate_insights(self):
        """Test insight generation."""
        from core.database import PlatformDatabase
        from core.platform_comparison import PlatformComparator

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            db = PlatformDatabase(db_path)
            db.initialize()
            
            # Add data
            title_id = "test_story"
            result = UploadResult(
                success=True,
                platform=PlatformType.YOUTUBE,
                video_id="yt_123",
                url="https://youtube.com/watch?v=yt_123",
                upload_time=datetime.now(),
            )
            
            db.save_upload_result(result, title_id, "Test Title")
            
            analytics = VideoAnalytics(
                platform=PlatformType.YOUTUBE,
                video_id="yt_123",
                title_id=title_id,
                collected_at=datetime.now(),
                views=1000,
                likes=50,
                engagement_rate=5.0,
            )
            
            db.save_analytics(analytics)
            db.close()
            
            # Test insights
            comparator = PlatformComparator(db_path)
            insights = comparator.generate_insights(title_id)
            
            assert insights is not None
            assert "error" not in insights
            assert insights["title_id"] == title_id
            assert "summary" in insights
            assert "recommendations" in insights
            assert insights["summary"]["total_views"] == 1000
            
            comparator.close()
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)


# Integration Tests

class TestPlatformIntegration:
    """Integration tests for new features."""

    def test_facebook_in_platform_type(self):
        """Verify Facebook is added to PlatformType enum."""
        assert hasattr(PlatformType, "FACEBOOK")
        assert PlatformType.FACEBOOK.value == "facebook"

    def test_all_uploaders_implement_interface(self):
        """Verify all uploader classes implement the interface."""
        from providers.youtube_provider import YouTubeUploader
        from providers.tiktok_provider import TikTokUploader
        from providers.instagram_provider import InstagramUploader
        from providers.facebook_provider import FacebookUploader

        uploaders = [YouTubeUploader, TikTokUploader, InstagramUploader, FacebookUploader]
        
        for uploader_class in uploaders:
            assert issubclass(uploader_class, IPlatformUploader)

    def test_all_analytics_implement_interface(self):
        """Verify all analytics classes implement the interface."""
        from providers.youtube_provider import YouTubeAnalytics
        from providers.tiktok_provider import TikTokAnalytics
        from providers.instagram_provider import InstagramAnalytics
        from providers.facebook_provider import FacebookAnalytics

        analytics_classes = [YouTubeAnalytics, TikTokAnalytics, InstagramAnalytics, FacebookAnalytics]
        
        for analytics_class in analytics_classes:
            assert issubclass(analytics_class, IPlatformAnalytics)
