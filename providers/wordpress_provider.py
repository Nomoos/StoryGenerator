"""
WordPress Platform Provider for creating draft posts.

This module implements the WordPress REST API v2 for creating draft posts
with story content and titles.

WordPress REST API Documentation:
https://developer.wordpress.com/docs/api/rest-api-reference/#2-posts
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


logger = logging.getLogger(__name__)


class WordPressProvider:
    """
    WordPress post creation provider using WordPress REST API v2.
    
    Creates draft posts with title and content. Supports both WordPress.com
    and self-hosted WordPress sites with REST API enabled.
    
    Authentication:
        - WordPress.com: OAuth token or Application Password
        - Self-hosted: Application Password (WP 5.6+)
    
    Example:
        >>> provider = WordPressProvider(
        ...     site_url="https://example.wordpress.com",
        ...     username="admin",
        ...     app_password="xxxx xxxx xxxx xxxx"
        ... )
        >>> result = provider.create_draft_post(
        ...     title="My Story Title",
        ...     content="This is the story content..."
        ... )
    """

    def __init__(
        self,
        site_url: Optional[str] = None,
        username: Optional[str] = None,
        app_password: Optional[str] = None,
        oauth_token: Optional[str] = None,
    ):
        """
        Initialize WordPress provider.
        
        Args:
            site_url: WordPress site URL (e.g., https://example.com)
            username: WordPress username (for Application Password auth)
            app_password: WordPress Application Password
            oauth_token: OAuth token (alternative to username/password)
        """
        self.site_url = (site_url or os.getenv("WORDPRESS_SITE_URL", "")).rstrip("/")
        self.username = username or os.getenv("WORDPRESS_USERNAME")
        self.app_password = app_password or os.getenv("WORDPRESS_APP_PASSWORD")
        self.oauth_token = oauth_token or os.getenv("WORDPRESS_OAUTH_TOKEN")
        
        if not self.site_url:
            logger.warning("WordPress site URL not configured")
        
        if not (self.oauth_token or (self.username and self.app_password)):
            logger.warning("WordPress authentication not fully configured")
        
        self._authenticated = bool(
            self.site_url and (self.oauth_token or (self.username and self.app_password))
        )
        
        # Build API base URL
        if self.site_url:
            # Check if it's WordPress.com or self-hosted
            if "wordpress.com" in self.site_url:
                # WordPress.com API
                site_slug = self.site_url.replace("https://", "").replace("http://", "").replace(".wordpress.com", "")
                self.api_base_url = f"https://public-api.wordpress.com/rest/v1.1/sites/{site_slug}"
            else:
                # Self-hosted WordPress with REST API
                self.api_base_url = f"{self.site_url}/wp-json/wp/v2"
        else:
            self.api_base_url = None

    def authenticate(self) -> bool:
        """
        Verify WordPress authentication by checking API access.
        
        Returns:
            bool: True if authentication successful.
        """
        if not self.api_base_url:
            logger.error("WordPress site URL not configured")
            return False
        
        if not (self.oauth_token or (self.username and self.app_password)):
            logger.error("WordPress authentication credentials not set")
            return False
        
        try:
            # Test authentication with a simple request
            headers = self._get_auth_headers()
            response = requests.get(
                f"{self.api_base_url}/users/me" if "wordpress.com" in self.site_url 
                else f"{self.api_base_url}/users/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("WordPress authentication successful")
                self._authenticated = True
                return True
            else:
                logger.error(f"WordPress authentication failed: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"WordPress authentication error: {e}")
            return False

    def _get_auth_headers(self) -> Dict[str, str]:
        """
        Build authentication headers.
        
        Returns:
            Dict with Authorization header.
        """
        headers = {
            "Content-Type": "application/json",
        }
        
        if self.oauth_token:
            # OAuth token authentication
            headers["Authorization"] = f"Bearer {self.oauth_token}"
        elif self.username and self.app_password:
            # Application Password authentication (Basic Auth)
            import base64
            credentials = f"{self.username}:{self.app_password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
        
        return headers

    @retry(
        retry=retry_if_exception_type((requests.RequestException, ConnectionError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def create_draft_post(
        self,
        title: str,
        content: str,
        excerpt: Optional[str] = None,
        categories: Optional[list] = None,
        tags: Optional[list] = None,
        featured_media: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Create a draft post in WordPress.
        
        Args:
            title: Post title
            content: Post content (HTML or plain text)
            excerpt: Optional post excerpt
            categories: Optional list of category IDs
            tags: Optional list of tag IDs
            featured_media: Optional featured image ID
            
        Returns:
            Dict with post creation result:
                {
                    'success': bool,
                    'post_id': int,
                    'post_url': str,
                    'edit_url': str,
                    'status': str,
                    'error': Optional[str]
                }
        """
        if not self._authenticated:
            if not self.authenticate():
                return {
                    'success': False,
                    'error': 'Authentication failed',
                    'post_id': None,
                    'post_url': None,
                    'edit_url': None,
                    'status': None
                }
        
        try:
            # Prepare post data
            post_data = {
                'title': title,
                'content': content,
                'status': 'draft',  # Create as draft
            }
            
            # Add optional fields
            if excerpt:
                post_data['excerpt'] = excerpt
            if categories:
                post_data['categories'] = categories
            if tags:
                post_data['tags'] = tags
            if featured_media:
                post_data['featured_media'] = featured_media
            
            # Make API request
            headers = self._get_auth_headers()
            endpoint = f"{self.api_base_url}/posts"
            
            logger.info(f"Creating WordPress draft post: {title}")
            
            response = requests.post(
                endpoint,
                json=post_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in (200, 201):
                data = response.json()
                post_id = data.get('id')
                post_url = data.get('link', '')
                
                # Build edit URL
                if "wordpress.com" in self.site_url:
                    edit_url = f"{self.site_url}/wp-admin/post.php?post={post_id}&action=edit"
                else:
                    edit_url = f"{self.site_url}/wp-admin/post.php?post={post_id}&action=edit"
                
                logger.info(f"Draft post created successfully: ID={post_id}")
                
                return {
                    'success': True,
                    'post_id': post_id,
                    'post_url': post_url,
                    'edit_url': edit_url,
                    'status': 'draft',
                    'error': None
                }
            else:
                error_msg = f"Failed to create post: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('message', '')}"
                except:
                    error_msg += f" - {response.text}"
                
                logger.error(error_msg)
                
                return {
                    'success': False,
                    'error': error_msg,
                    'post_id': None,
                    'post_url': None,
                    'edit_url': None,
                    'status': None
                }
                
        except requests.RequestException as e:
            error_msg = f"Request error creating post: {e}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'post_id': None,
                'post_url': None,
                'edit_url': None,
                'status': None
            }
        except Exception as e:
            error_msg = f"Unexpected error creating post: {e}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'post_id': None,
                'post_url': None,
                'edit_url': None,
                'status': None
            }

    def update_post(
        self,
        post_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        status: Optional[str] = None,
        excerpt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing post.
        
        Args:
            post_id: WordPress post ID
            title: Optional new title
            content: Optional new content
            status: Optional new status (draft, publish, pending, private)
            excerpt: Optional new excerpt
            
        Returns:
            Dict with update result.
        """
        if not self._authenticated:
            if not self.authenticate():
                return {
                    'success': False,
                    'error': 'Authentication failed'
                }
        
        try:
            # Prepare update data
            update_data = {}
            if title is not None:
                update_data['title'] = title
            if content is not None:
                update_data['content'] = content
            if status is not None:
                update_data['status'] = status
            if excerpt is not None:
                update_data['excerpt'] = excerpt
            
            if not update_data:
                return {
                    'success': False,
                    'error': 'No fields to update'
                }
            
            # Make API request
            headers = self._get_auth_headers()
            endpoint = f"{self.api_base_url}/posts/{post_id}"
            
            logger.info(f"Updating WordPress post: {post_id}")
            
            response = requests.post(
                endpoint,
                json=update_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Post updated successfully: ID={post_id}")
                
                return {
                    'success': True,
                    'post_id': post_id,
                    'post_url': data.get('link', ''),
                    'status': data.get('status', ''),
                    'error': None
                }
            else:
                error_msg = f"Failed to update post: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('message', '')}"
                except:
                    error_msg += f" - {response.text}"
                
                logger.error(error_msg)
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except Exception as e:
            error_msg = f"Error updating post: {e}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }

    def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a post by ID.
        
        Args:
            post_id: WordPress post ID
            
        Returns:
            Dict with post data or None if not found.
        """
        try:
            headers = self._get_auth_headers()
            endpoint = f"{self.api_base_url}/posts/{post_id}"
            
            response = requests.get(
                endpoint,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to retrieve post {post_id}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving post: {e}")
            return None
