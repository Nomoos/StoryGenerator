# WordPress Integration Guide

This guide shows how to integrate WordPress with StoryGenerator to automatically create draft posts with your generated stories.

## Overview

The WordPress integration allows you to:
- Create draft posts with story titles and content
- Update existing posts
- Publish drafts programmatically
- Support both WordPress.com and self-hosted WordPress sites

## Quick Start

### 1. Setup WordPress Authentication

#### For WordPress.com Sites

Generate an OAuth token or use Application Passwords:

1. Go to https://wordpress.com/me/security/application-passwords
2. Click "Create New Application Password"
3. Name it "StoryGenerator"
4. Copy the generated password

#### For Self-Hosted WordPress

WordPress 5.6+ includes Application Passwords:

1. Log in to WordPress admin
2. Go to: **Users → Profile → Application Passwords**
3. Enter application name: "StoryGenerator"
4. Click **Add New Application Password**
5. Copy the generated password (format: `xxxx xxxx xxxx xxxx`)

### 2. Configure Environment Variables

```bash
export WORDPRESS_SITE_URL="https://mysite.wordpress.com"
export WORDPRESS_USERNAME="your_username"
export WORDPRESS_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

Or create a `.env` file:

```
WORDPRESS_SITE_URL=https://mysite.wordpress.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

### 3. Basic Usage

```python
from providers.wordpress_provider import WordPressProvider

# Initialize provider (uses environment variables)
provider = WordPressProvider()

# Create a draft post
result = provider.create_draft_post(
    title="My Story Title",
    content="This is my story content..."
)

if result['success']:
    print(f"Draft created: {result['edit_url']}")
    print(f"Post ID: {result['post_id']}")
else:
    print(f"Error: {result['error']}")
```

## Integration with StoryGenerator Pipeline

### Method 1: Manual Script Publishing

After generating scripts, manually create WordPress drafts:

```python
from core.script_development import develop_script
from providers import WordPressProvider

# Generate script
script_result = develop_script(
    idea={'content': 'A story about...', 'target_gender': 'women', 'target_age': '18-23'},
    llm_provider=provider
)

# Create WordPress draft
wp = WordPressProvider()
result = wp.create_draft_post(
    title=script_result['best_script'].title,
    content=script_result['best_script'].content,
    excerpt=f"Story for {script_result['best_script'].target_gender}"
)
```

### Method 2: Automated Publishing Stage

Add WordPress publishing to your pipeline:

```python
class WordPressPublishingStage:
    """Pipeline stage for publishing scripts to WordPress."""
    
    def __init__(self):
        self.wp = WordPressProvider()
    
    def process(self, script_data):
        """Publish script as WordPress draft."""
        result = self.wp.create_draft_post(
            title=script_data['title'],
            content=script_data['content']
        )
        
        return {
            'script': script_data,
            'wordpress': result
        }
```

## API Reference

### WordPressProvider

Main class for WordPress integration.

#### `__init__(site_url, username, app_password, oauth_token)`

Initialize WordPress provider.

**Parameters:**
- `site_url` (str, optional): WordPress site URL (e.g., https://mysite.com)
- `username` (str, optional): WordPress username
- `app_password` (str, optional): Application password
- `oauth_token` (str, optional): OAuth token (alternative to username/password)

**Environment Variables:**
- `WORDPRESS_SITE_URL`: Site URL
- `WORDPRESS_USERNAME`: Username
- `WORDPRESS_APP_PASSWORD`: Application password
- `WORDPRESS_OAUTH_TOKEN`: OAuth token

#### `authenticate()` → bool

Verify WordPress authentication.

**Returns:** `True` if authenticated, `False` otherwise

#### `create_draft_post(title, content, excerpt, categories, tags, featured_media)` → dict

Create a draft post in WordPress.

**Parameters:**
- `title` (str): Post title
- `content` (str): Post content (HTML or plain text)
- `excerpt` (str, optional): Post excerpt
- `categories` (list, optional): List of category IDs
- `tags` (list, optional): List of tag IDs
- `featured_media` (int, optional): Featured image ID

**Returns:**
```python
{
    'success': bool,
    'post_id': int,
    'post_url': str,
    'edit_url': str,
    'status': str,
    'error': str  # if success is False
}
```

#### `update_post(post_id, title, content, status, excerpt)` → dict

Update an existing post.

**Parameters:**
- `post_id` (int): WordPress post ID
- `title` (str, optional): New title
- `content` (str, optional): New content
- `status` (str, optional): New status ('draft', 'publish', 'pending', 'private')
- `excerpt` (str, optional): New excerpt

**Returns:**
```python
{
    'success': bool,
    'post_id': int,
    'post_url': str,
    'status': str,
    'error': str  # if success is False
}
```

#### `get_post(post_id)` → dict

Retrieve a post by ID.

**Parameters:**
- `post_id` (int): WordPress post ID

**Returns:** Post data dict or `None` if not found

## Usage Examples

### Example 1: Create Simple Draft

```python
from providers import WordPressProvider

wp = WordPressProvider(
    site_url="https://mysite.wordpress.com",
    username="admin",
    app_password="xxxx xxxx xxxx xxxx"
)

result = wp.create_draft_post(
    title="The Last Message",
    content="In 2095, archaeologists found an old smartphone..."
)

print(f"Draft created: {result['edit_url']}")
```

### Example 2: Create Draft with Metadata

```python
result = wp.create_draft_post(
    title="My Story",
    content="Story content here...",
    excerpt="A brief summary",
    categories=[1, 5],  # Category IDs
    tags=[10, 15, 20]   # Tag IDs
)
```

### Example 3: Publish a Draft

```python
# Create draft
draft_result = wp.create_draft_post(
    title="Initial Title",
    content="Initial content"
)

post_id = draft_result['post_id']

# Update and publish
wp.update_post(
    post_id=post_id,
    title="Final Title",
    content="Final content",
    status='publish'
)
```

### Example 4: Batch Create Drafts

```python
stories = [
    {'title': 'Story 1', 'content': 'Content 1...'},
    {'title': 'Story 2', 'content': 'Content 2...'},
    {'title': 'Story 3', 'content': 'Content 3...'},
]

for story in stories:
    result = wp.create_draft_post(**story)
    print(f"Created: {result['post_id']}")
```

## Troubleshooting

### Authentication Failed

**Error:** "Authentication failed" or 401 Unauthorized

**Solutions:**
1. Verify WordPress site URL is correct
2. Check username is correct
3. Regenerate Application Password
4. For self-hosted: Ensure REST API is enabled
5. For WordPress.com: Verify account has posting permissions

### Invalid Credentials

**Error:** "WordPress authentication credentials not set"

**Solution:** Set environment variables or pass credentials to constructor:

```python
wp = WordPressProvider(
    site_url="https://mysite.com",
    username="admin",
    app_password="xxxx xxxx xxxx xxxx"
)
```

### SSL Certificate Errors

**Error:** SSL verification failed

**Solution:** Ensure your WordPress site has a valid SSL certificate. For development, you can disable SSL verification (not recommended for production):

```python
# Not recommended for production
import requests
requests.packages.urllib3.disable_warnings()
```

### API Not Found (404)

**Error:** 404 when calling WordPress API

**Solutions:**
1. **Self-hosted:** Ensure WordPress is updated to 5.6+
2. **Self-hosted:** Check permalink settings (must not be "Plain")
3. Verify REST API is accessible: `https://yoursite.com/wp-json/`
4. Check for security plugins blocking REST API

## Security Best Practices

1. **Use Application Passwords**: Never use your main WordPress password
2. **Limit Permissions**: Create a dedicated user account with only posting permissions
3. **Rotate Passwords**: Regularly regenerate application passwords
4. **Use Environment Variables**: Never hardcode credentials in source code
5. **HTTPS Only**: Always use HTTPS for WordPress sites
6. **Audit Logs**: Monitor WordPress admin logs for API usage

## API Rate Limits

- **WordPress.com**: Approximately 60 requests per minute per IP
- **Self-hosted**: Depends on server configuration and hosting provider

If you hit rate limits, implement exponential backoff (already included via `tenacity` retry decorator).

## Comparison with Other Platforms

| Feature | WordPress | YouTube | TikTok | Instagram |
|---------|-----------|---------|--------|-----------|
| Draft Creation | ✅ Yes | ❌ No | ❌ No | ❌ No |
| API Approval | ✅ No approval needed | ⚠️ OAuth required | ⚠️ Business account | ⚠️ Facebook Business |
| Text Content | ✅ Primary | ❌ No | ⚠️ Limited | ⚠️ Limited |
| Manual Review | ✅ Easy | ⚠️ Video review | ⚠️ Video review | ⚠️ Video review |

WordPress is ideal for:
- Text-based story publishing
- Manual review workflows
- No API approval requirements
- Full content control before publishing

## Related Documentation

- [WordPress REST API Reference](https://developer.wordpress.com/docs/api/)
- [Application Passwords Documentation](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/)
- [StoryGenerator Integration Guide](./INTEGRATION_GUIDE.md)
- [Platform Integration Summary](../PLATFORM_INTEGRATION_SUMMARY.md)

## Support

For issues specific to:
- **WordPress setup**: See [WordPress Support](https://wordpress.org/support/)
- **StoryGenerator**: Open an issue on GitHub
- **API errors**: Check WordPress REST API logs in admin dashboard
