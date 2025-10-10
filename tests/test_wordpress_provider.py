"""
Tests for WordPress provider.

Tests the WordPressProvider implementation for creating draft posts.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

# Skip tests if requests not available
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    skip_reason = "requests library not available"

pytestmark = pytest.mark.skipif(not REQUESTS_AVAILABLE, reason="requests not available")


# Test fixtures

@pytest.fixture
def wordpress_provider():
    """WordPress provider with mock credentials."""
    from providers.wordpress_provider import WordPressProvider
    
    return WordPressProvider(
        site_url="https://example.wordpress.com",
        username="testuser",
        app_password="test pass word here"
    )


@pytest.fixture
def wordpress_selfhosted_provider():
    """WordPress provider for self-hosted site."""
    from providers.wordpress_provider import WordPressProvider
    
    return WordPressProvider(
        site_url="https://mysite.com",
        username="admin",
        app_password="xxxx xxxx xxxx xxxx"
    )


@pytest.fixture
def wordpress_oauth_provider():
    """WordPress provider with OAuth token."""
    from providers.wordpress_provider import WordPressProvider
    
    return WordPressProvider(
        site_url="https://example.wordpress.com",
        oauth_token="test_oauth_token_12345"
    )


# WordPress Provider Tests

class TestWordPressProvider:
    """Tests for WordPressProvider."""

    def test_provider_initialization_with_app_password(self, wordpress_provider):
        """Test WordPress provider initialization with Application Password."""
        assert wordpress_provider.site_url == "https://example.wordpress.com"
        assert wordpress_provider.username == "testuser"
        assert wordpress_provider.app_password == "test pass word here"
        assert wordpress_provider.oauth_token is None
        assert wordpress_provider._authenticated

    def test_provider_initialization_with_oauth(self, wordpress_oauth_provider):
        """Test WordPress provider initialization with OAuth token."""
        assert wordpress_oauth_provider.site_url == "https://example.wordpress.com"
        assert wordpress_oauth_provider.oauth_token == "test_oauth_token_12345"
        assert wordpress_oauth_provider._authenticated

    def test_provider_initialization_selfhosted(self, wordpress_selfhosted_provider):
        """Test WordPress provider for self-hosted site."""
        assert wordpress_selfhosted_provider.site_url == "https://mysite.com"
        assert "wp-json/wp/v2" in wordpress_selfhosted_provider.api_base_url
        
    def test_provider_initialization_wordpress_com(self, wordpress_provider):
        """Test WordPress provider for WordPress.com site."""
        assert "wordpress.com" in wordpress_provider.site_url
        assert "public-api.wordpress.com" in wordpress_provider.api_base_url

    def test_provider_without_credentials(self):
        """Test provider initialization without credentials."""
        from providers.wordpress_provider import WordPressProvider
        
        provider = WordPressProvider()
        assert not provider._authenticated

    @patch('requests.get')
    def test_authenticate_success(self, mock_get, wordpress_provider):
        """Test successful authentication."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 1, 'name': 'Test User'}
        mock_get.return_value = mock_response
        
        result = wordpress_provider.authenticate()
        
        assert result is True
        assert wordpress_provider._authenticated
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_authenticate_failure(self, mock_get, wordpress_provider):
        """Test authentication failure."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        result = wordpress_provider.authenticate()
        
        assert result is False

    @patch('requests.post')
    def test_create_draft_post_success(self, mock_post, wordpress_provider):
        """Test successful draft post creation."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'id': 123,
            'link': 'https://example.wordpress.com/2025/10/10/my-post/',
            'status': 'draft',
            'title': {'rendered': 'Test Post'},
            'content': {'rendered': 'Test content'}
        }
        mock_post.return_value = mock_response
        
        result = wordpress_provider.create_draft_post(
            title="Test Post",
            content="Test content"
        )
        
        assert result['success'] is True
        assert result['post_id'] == 123
        assert result['status'] == 'draft'
        assert result['post_url'] == 'https://example.wordpress.com/2025/10/10/my-post/'
        assert result['error'] is None
        assert 'edit_url' in result
        
        # Verify API call
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args[1]
        assert call_kwargs['json']['title'] == 'Test Post'
        assert call_kwargs['json']['content'] == 'Test content'
        assert call_kwargs['json']['status'] == 'draft'

    @patch('requests.post')
    def test_create_draft_post_with_optional_fields(self, mock_post, wordpress_provider):
        """Test draft post creation with optional fields."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'id': 456,
            'link': 'https://example.wordpress.com/2025/10/10/my-post/',
            'status': 'draft'
        }
        mock_post.return_value = mock_response
        
        result = wordpress_provider.create_draft_post(
            title="Test Post",
            content="Test content",
            excerpt="Test excerpt",
            categories=[1, 2],
            tags=[3, 4],
            featured_media=999
        )
        
        assert result['success'] is True
        
        # Verify optional fields were included
        call_kwargs = mock_post.call_args[1]
        assert call_kwargs['json']['excerpt'] == 'Test excerpt'
        assert call_kwargs['json']['categories'] == [1, 2]
        assert call_kwargs['json']['tags'] == [3, 4]
        assert call_kwargs['json']['featured_media'] == 999

    @patch('requests.post')
    def test_create_draft_post_failure(self, mock_post, wordpress_provider):
        """Test failed draft post creation."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'code': 'rest_invalid_param',
            'message': 'Invalid parameter(s): title'
        }
        mock_response.text = 'Bad Request'
        mock_post.return_value = mock_response
        
        result = wordpress_provider.create_draft_post(
            title="",
            content="Test content"
        )
        
        assert result['success'] is False
        assert result['error'] is not None
        assert result['post_id'] is None

    @patch('requests.post')
    def test_create_draft_post_network_error(self, mock_post, wordpress_provider):
        """Test draft post creation with network error."""
        mock_post.side_effect = requests.RequestException("Network error")
        
        result = wordpress_provider.create_draft_post(
            title="Test Post",
            content="Test content"
        )
        
        assert result['success'] is False
        assert 'Network error' in result['error']

    @patch('requests.post')
    def test_update_post_success(self, mock_post, wordpress_provider):
        """Test successful post update."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 123,
            'link': 'https://example.wordpress.com/2025/10/10/updated-post/',
            'status': 'publish',
            'title': {'rendered': 'Updated Title'}
        }
        mock_post.return_value = mock_response
        
        result = wordpress_provider.update_post(
            post_id=123,
            title="Updated Title",
            status="publish"
        )
        
        assert result['success'] is True
        assert result['post_id'] == 123
        assert result['status'] == 'publish'

    @patch('requests.post')
    def test_update_post_no_fields(self, mock_post, wordpress_provider):
        """Test post update with no fields specified."""
        result = wordpress_provider.update_post(post_id=123)
        
        assert result['success'] is False
        assert 'No fields to update' in result['error']
        mock_post.assert_not_called()

    @patch('requests.get')
    def test_get_post_success(self, mock_get, wordpress_provider):
        """Test successful post retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 123,
            'title': {'rendered': 'Test Post'},
            'content': {'rendered': 'Test content'},
            'status': 'draft'
        }
        mock_get.return_value = mock_response
        
        result = wordpress_provider.get_post(123)
        
        assert result is not None
        assert result['id'] == 123
        assert result['status'] == 'draft'

    @patch('requests.get')
    def test_get_post_not_found(self, mock_get, wordpress_provider):
        """Test post retrieval for non-existent post."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = wordpress_provider.get_post(999)
        
        assert result is None

    def test_auth_headers_with_app_password(self, wordpress_provider):
        """Test authentication headers with Application Password."""
        headers = wordpress_provider._get_auth_headers()
        
        assert 'Authorization' in headers
        assert headers['Authorization'].startswith('Basic ')
        assert 'Content-Type' in headers

    def test_auth_headers_with_oauth(self, wordpress_oauth_provider):
        """Test authentication headers with OAuth token."""
        headers = wordpress_oauth_provider._get_auth_headers()
        
        assert 'Authorization' in headers
        assert headers['Authorization'] == 'Bearer test_oauth_token_12345'
        assert 'Content-Type' in headers


class TestWordPressProviderIntegration:
    """Integration-style tests for complete workflows."""

    @patch('requests.post')
    @patch('requests.get')
    def test_create_and_publish_workflow(self, mock_get, mock_post, wordpress_provider):
        """Test creating a draft and then publishing it."""
        # Mock authentication
        mock_get.return_value = Mock(status_code=200, json=lambda: {'id': 1})
        
        # Mock draft creation
        create_response = Mock()
        create_response.status_code = 201
        create_response.json.return_value = {
            'id': 123,
            'link': 'https://example.wordpress.com/2025/10/10/my-post/',
            'status': 'draft'
        }
        
        # Mock post update (publish)
        update_response = Mock()
        update_response.status_code = 200
        update_response.json.return_value = {
            'id': 123,
            'link': 'https://example.wordpress.com/2025/10/10/my-post/',
            'status': 'publish'
        }
        
        mock_post.side_effect = [create_response, update_response]
        
        # Create draft
        create_result = wordpress_provider.create_draft_post(
            title="Test Post",
            content="Test content"
        )
        
        assert create_result['success'] is True
        assert create_result['status'] == 'draft'
        post_id = create_result['post_id']
        
        # Publish the draft
        update_result = wordpress_provider.update_post(
            post_id=post_id,
            status='publish'
        )
        
        assert update_result['success'] is True
        assert update_result['status'] == 'publish'
