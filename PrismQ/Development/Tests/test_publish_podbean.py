"""
Tests for scripts/publish_podbean.py - Podbean episode publishing.
"""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# Add scripts directory to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scripts_dir = os.path.join(project_root, "scripts")
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

# Add project root for core imports
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the module
import publish_podbean

from PrismQ.Shared.errors import APIError, AuthenticationError, ValidationError


class TestGetToken:
    """Test Podbean OAuth authentication."""

    def test_get_token_success(self):
        """Test successful token retrieval."""
        with patch.dict(os.environ, {
            "PODBEAN_CLIENT_ID": "test_client_id",
            "PODBEAN_CLIENT_SECRET": "test_client_secret"
        }):
            mock_response = Mock()
            mock_response.json.return_value = {"access_token": "test_token_123"}
            mock_response.raise_for_status = Mock()

            with patch("requests.post", return_value=mock_response) as mock_post:
                token = publish_podbean.get_token()

                assert token == "test_token_123"
                mock_post.assert_called_once()
                call_args = mock_post.call_args
                assert call_args[0][0] == "https://api.podbean.com/v1/oauth/token"
                assert call_args[1]["data"]["grant_type"] == "client_credentials"
                assert call_args[1]["data"]["client_id"] == "test_client_id"
                assert call_args[1]["data"]["client_secret"] == "test_client_secret"

    def test_get_token_missing_credentials(self):
        """Test authentication with missing credentials."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(AuthenticationError) as exc_info:
                publish_podbean.get_token()

            assert "Missing Podbean credentials" in str(exc_info.value)

    def test_get_token_invalid_response(self):
        """Test authentication with invalid response."""
        with patch.dict(os.environ, {
            "PODBEAN_CLIENT_ID": "test_client_id",
            "PODBEAN_CLIENT_SECRET": "test_client_secret"
        }):
            mock_response = Mock()
            mock_response.json.return_value = {"error": "invalid"}
            mock_response.raise_for_status = Mock()

            with patch("requests.post", return_value=mock_response):
                with pytest.raises(AuthenticationError) as exc_info:
                    publish_podbean.get_token()

                assert "Invalid response from Podbean OAuth" in str(exc_info.value)


class TestUploadAuthorize:
    """Test upload authorization."""

    def test_upload_authorize_success(self):
        """Test successful upload authorization."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "presigned_url": "https://s3.example.com/upload",
            "file_key": "test_file_key_123"
        }
        mock_response.raise_for_status = Mock()

        with patch("requests.get", return_value=mock_response) as mock_get:
            url, key = publish_podbean.upload_authorize("test_token")

            assert url == "https://s3.example.com/upload"
            assert key == "test_file_key_123"
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert "Bearer test_token" in call_args[1]["headers"]["Authorization"]

    def test_upload_authorize_invalid_response(self):
        """Test upload authorization with invalid response."""
        mock_response = Mock()
        mock_response.json.return_value = {"error": "invalid"}
        mock_response.raise_for_status = Mock()

        with patch("requests.get", return_value=mock_response):
            with pytest.raises(APIError) as exc_info:
                publish_podbean.upload_authorize("test_token")

            assert "Invalid upload authorization response" in str(exc_info.value)


class TestUploadFile:
    """Test file upload."""

    def test_upload_file_success(self, tmp_path):
        """Test successful file upload."""
        # Create a temporary test file
        test_file = tmp_path / "test_audio.mp3"
        test_file.write_bytes(b"test audio content")

        mock_response = Mock()
        mock_response.raise_for_status = Mock()

        with patch("requests.put", return_value=mock_response) as mock_put:
            publish_podbean.upload_file("https://s3.example.com/upload", str(test_file))

            mock_put.assert_called_once()
            call_args = mock_put.call_args
            assert call_args[0][0] == "https://s3.example.com/upload"

    def test_upload_file_not_found(self):
        """Test upload with non-existent file."""
        with pytest.raises(ValidationError) as exc_info:
            publish_podbean.upload_file("https://s3.example.com/upload", "/nonexistent/file.mp3")

        assert "File not found" in str(exc_info.value)


class TestCreateEpisode:
    """Test episode creation."""

    def test_create_episode_immediate_publish(self):
        """Test creating episode for immediate publishing."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "episode_id": "123",
            "permalink_url": "https://podcast.example.com/ep123"
        }
        mock_response.raise_for_status = Mock()

        with patch("requests.post", return_value=mock_response) as mock_post:
            result = publish_podbean.create_episode(
                "test_token",
                media_key="media_key_123",
                title="Test Episode",
                description="Test description"
            )

            assert result["episode_id"] == "123"
            assert result["permalink_url"] == "https://podcast.example.com/ep123"

            call_args = mock_post.call_args
            assert call_args[1]["data"]["status"] == "publish"
            assert call_args[1]["data"]["title"] == "Test Episode"
            assert call_args[1]["data"]["media_key"] == "media_key_123"

    def test_create_episode_scheduled(self):
        """Test creating episode with scheduled publish time."""
        mock_response = Mock()
        mock_response.json.return_value = {"episode_id": "124"}
        mock_response.raise_for_status = Mock()

        with patch("requests.post", return_value=mock_response) as mock_post:
            result = publish_podbean.create_episode(
                "test_token",
                media_key="media_key_123",
                title="Scheduled Episode",
                description="Test description",
                publish_at="2025-10-12T15:00:00Z"
            )

            assert result["episode_id"] == "124"

            call_args = mock_post.call_args
            assert call_args[1]["data"]["status"] == "schedule"
            assert "publish_time" in call_args[1]["data"]

    def test_create_episode_with_artwork(self):
        """Test creating episode with artwork."""
        mock_response = Mock()
        mock_response.json.return_value = {"episode_id": "125"}
        mock_response.raise_for_status = Mock()

        with patch("requests.post", return_value=mock_response) as mock_post:
            publish_podbean.create_episode(
                "test_token",
                media_key="media_key_123",
                title="Episode with Art",
                description="Test description",
                logo_key="logo_key_456"
            )

            call_args = mock_post.call_args
            assert call_args[1]["data"]["logo_key"] == "logo_key_456"

    def test_create_episode_invalid_publish_time(self):
        """Test creating episode with invalid publish time format."""
        with pytest.raises(ValidationError) as exc_info:
            publish_podbean.create_episode(
                "test_token",
                media_key="media_key_123",
                title="Test Episode",
                description="Test description",
                publish_at="invalid-date-format"
            )

        assert "Invalid publish_at format" in str(exc_info.value)


class TestUploadArtwork:
    """Test artwork upload."""

    def test_upload_artwork_success(self, tmp_path):
        """Test successful artwork upload."""
        # Create a temporary artwork file
        artwork_file = tmp_path / "artwork.jpg"
        artwork_file.write_bytes(b"fake image data")

        mock_auth_response = Mock()
        mock_auth_response.json.return_value = {
            "presigned_url": "https://s3.example.com/upload",
            "file_key": "artwork_key_789"
        }
        mock_auth_response.raise_for_status = Mock()

        mock_upload_response = Mock()
        mock_upload_response.raise_for_status = Mock()

        with patch("requests.get", return_value=mock_auth_response):
            with patch("requests.put", return_value=mock_upload_response):
                file_key = publish_podbean.upload_artwork("test_token", str(artwork_file))

                assert file_key == "artwork_key_789"

    def test_upload_artwork_not_found(self):
        """Test artwork upload with non-existent file."""
        with pytest.raises(ValidationError) as exc_info:
            publish_podbean.upload_artwork("test_token", "/nonexistent/artwork.jpg")

        assert "Artwork file not found" in str(exc_info.value)


class TestMain:
    """Test main function."""

    def test_main_success(self, tmp_path, monkeypatch):
        """Test successful end-to-end publishing."""
        # Create test audio file
        audio_file = tmp_path / "test_episode.mp3"
        audio_file.write_bytes(b"test audio")

        # Set environment variables
        env_vars = {
            "PODBEAN_CLIENT_ID": "test_client_id",
            "PODBEAN_CLIENT_SECRET": "test_client_secret",
            "AUDIO_PATH": str(audio_file),
            "EP_TITLE": "Test Episode",
            "EP_DESC": "Test description"
        }

        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        # Mock all API calls
        with patch("publish_podbean.get_token", return_value="test_token"):
            with patch("publish_podbean.upload_authorize", return_value=("https://s3.example.com", "media_key")):
                with patch("publish_podbean.upload_file"):
                    with patch("publish_podbean.create_episode", return_value={
                        "episode_id": "123",
                        "permalink_url": "https://podcast.example.com/ep123"
                    }):
                        result = publish_podbean.main()

                        assert result == 0

    def test_main_missing_audio_path(self, monkeypatch):
        """Test main function with missing audio path."""
        # Set only credentials
        monkeypatch.setenv("PODBEAN_CLIENT_ID", "test_client_id")
        monkeypatch.setenv("PODBEAN_CLIENT_SECRET", "test_client_secret")

        result = publish_podbean.main()
        assert result == 1

    def test_main_with_artwork(self, tmp_path, monkeypatch):
        """Test publishing with artwork."""
        # Create test files
        audio_file = tmp_path / "test_episode.mp3"
        audio_file.write_bytes(b"test audio")
        artwork_file = tmp_path / "artwork.jpg"
        artwork_file.write_bytes(b"test image")

        # Set environment variables
        env_vars = {
            "PODBEAN_CLIENT_ID": "test_client_id",
            "PODBEAN_CLIENT_SECRET": "test_client_secret",
            "AUDIO_PATH": str(audio_file),
            "EP_TITLE": "Test Episode",
            "EP_DESC": "Test description",
            "EP_ARTWORK_PATH": str(artwork_file)
        }

        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        # Mock all API calls
        with patch("publish_podbean.get_token", return_value="test_token"):
            with patch("publish_podbean.upload_authorize", return_value=("https://s3.example.com", "key")):
                with patch("publish_podbean.upload_file"):
                    with patch("publish_podbean.upload_artwork", return_value="logo_key"):
                        with patch("publish_podbean.create_episode", return_value={
                            "episode_id": "123",
                            "permalink_url": "https://podcast.example.com/ep123"
                        }) as mock_create:
                            result = publish_podbean.main()

                            assert result == 0
                            # Verify artwork was included in episode creation
                            call_kwargs = mock_create.call_args[1]
                            assert call_kwargs["logo_key"] == "logo_key"
