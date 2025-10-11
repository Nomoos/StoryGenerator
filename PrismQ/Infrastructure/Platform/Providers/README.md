# Providers Package

This package contains concrete implementations of service provider interfaces for the StoryGenerator application.

## Overview

The provider architecture pattern decouples the application from specific service implementations, making it easy to:
- Swap between different service providers
- Mock services for testing
- Add retry logic and error handling centrally
- Follow SOLID principles (especially Dependency Inversion)

## Available Providers

### LLM Providers

#### OpenAIProvider
Synchronous OpenAI API implementation using the new SDK (v1.0+).

```python
from PrismQ.Providers import OpenAIProvider

provider = OpenAIProvider(model="gpt-4o-mini")
result = provider.generate_completion("Your prompt here")
```

Features:
- Automatic retry with exponential backoff (3 attempts)
- Comprehensive error handling
- Rate limit management
- Detailed logging

#### AsyncOpenAIProvider
Asynchronous OpenAI API implementation for high-throughput applications.

```python
from PrismQ.Providers import AsyncOpenAIProvider

provider = AsyncOpenAIProvider(model="gpt-4o-mini")
result = await provider.generate_completion("Your prompt here")
```

#### MockLLMProvider
Mock provider for testing without making actual API calls.

```python
from PrismQ.Providers import MockLLMProvider

provider = MockLLMProvider(response="Test response")
result = provider.generate_completion("Any prompt")
# result == "Test response"
```

Features:
- No API calls required
- Tracks call count and last inputs
- Perfect for unit testing

### Platform Integration Providers

#### YouTubeUploader & YouTubeAnalytics
Upload videos to YouTube and retrieve analytics via YouTube Data API v3.

```python
from PrismQ.Providers import YouTubeUploader, YouTubeAnalytics
from core.interfaces.platform_provider import VideoMetadata, PrivacyStatus

# Upload a video
uploader = YouTubeUploader()
uploader.authenticate()
metadata = VideoMetadata(
    title="My Video #Shorts",
    description="Amazing content!",
    tags=["shorts", "viral"],
    privacy_status=PrivacyStatus.PUBLIC
)
result = uploader.upload_video("video.mp4", metadata)

# Get analytics
analytics = YouTubeAnalytics()
analytics.authenticate()
data = analytics.get_video_analytics(result.video_id)
print(f"Views: {data.views}, Likes: {data.likes}")
```

#### TikTokUploader & TikTokAnalytics
Upload videos to TikTok and retrieve analytics via TikTok Content Posting API.

```python
from PrismQ.Providers import TikTokUploader, TikTokAnalytics

# Upload a video
uploader = TikTokUploader(access_token="YOUR_TOKEN")
metadata = VideoMetadata(
    title="Epic Story",
    caption="Check this out! #fyp",
    hashtags=["fyp", "viral"]
)
result = uploader.upload_video("video.mp4", metadata)

# Get analytics
analytics = TikTokAnalytics(access_token="YOUR_TOKEN")
data = analytics.get_video_analytics(result.video_id)
```

#### InstagramUploader & InstagramAnalytics
Upload Reels to Instagram and retrieve analytics via Instagram Graph API.

```python
from PrismQ.Providers import InstagramUploader, InstagramAnalytics

# Upload a Reel (requires public video URL)
uploader = InstagramUploader(
    access_token="YOUR_TOKEN",
    instagram_user_id="YOUR_ID"
)
metadata = VideoMetadata(caption="Amazing Reel! #reels")
result = uploader.upload_video("https://example.com/video.mp4", metadata)

# Get analytics
analytics = InstagramAnalytics(
    access_token="YOUR_TOKEN",
    instagram_user_id="YOUR_ID"
)
data = analytics.get_video_analytics(result.video_id)
```

#### WordPressProvider
Create draft posts in WordPress with story titles and content.

```python
from PrismQ.Providers import WordPressProvider

# Initialize provider
provider = WordPressProvider(
    site_url="https://mysite.wordpress.com",
    username="admin",
    app_password="xxxx xxxx xxxx xxxx"
)

# Create draft post
result = provider.create_draft_post(
    title="My Story Title",
    content="This is the story content..."
)

if result['success']:
    print(f"Draft created: {result['edit_url']}")
    print(f"Post ID: {result['post_id']}")
```

**📖 Full Documentation:** 
- [Platform Integration Guide](../docs/guides/integration/PLATFORM_INTEGRATION.md)
- [WordPress Integration Guide](../docs/guides/integration/WORDPRESS_INTEGRATION.md)

## Usage Examples

### Basic Usage

```python
from PrismQ.Providers import OpenAIProvider

# Initialize with environment variable OPENAI_API_KEY
provider = OpenAIProvider(model="gpt-4o-mini")

# Simple completion
response = provider.generate_completion("Write a haiku about coding")

# Chat completion
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]
response = provider.generate_chat(messages, temperature=0.8)
```

### Interface-Based Design

```python
from core.interfaces.llm_provider import ILLMProvider
from PrismQ.Providers import OpenAIProvider, MockLLMProvider

def generate_content(provider: ILLMProvider, topic: str) -> str:
    """Works with any LLM provider."""
    return provider.generate_completion(f"Write about {topic}")

# Production
prod_provider = OpenAIProvider()
result = generate_content(prod_provider, "AI")

# Testing
test_provider = MockLLMProvider(response="Test content")
result = generate_content(test_provider, "AI")
```

### Error Handling

```python
from openai import RateLimitError, APIError
from PrismQ.Providers import OpenAIProvider

provider = OpenAIProvider()

try:
    result = provider.generate_completion("prompt")
except RateLimitError:
    # Rate limit exceeded after retries
    print("Rate limited - try again later")
except APIError as e:
    # API error from OpenAI
    print(f"API error: {e}")
```

## Configuration

### Environment Variables

```bash
# Required for OpenAI providers
OPENAI_API_KEY=sk-your-key-here

# Optional: default model
DEFAULT_MODEL=gpt-4o-mini
```

### Logging

Enable debug logging to see provider operations:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

## Testing

### Unit Tests

Use `MockLLMProvider` for fast, reliable unit tests:

```python
from PrismQ.Providers import MockLLMProvider

def test_story_generation():
    provider = MockLLMProvider(response="A test story")
    
    result = generate_story(provider, "robots")
    
    assert result == "A test story"
    assert provider.call_count == 1
```

### Integration Tests

Mark integration tests that require API keys:

```python
import pytest
from PrismQ.Providers import OpenAIProvider

@pytest.mark.slow
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="OPENAI_API_KEY not set"
)
def test_real_api():
    provider = OpenAIProvider()
    result = provider.generate_completion("test")
    assert isinstance(result, str)
```

## Architecture

```
PrismQ/Providers/
├── __init__.py              # Package exports
├── openai_provider.py       # OpenAI implementation
├── mock_provider.py         # Mock for testing
└── README.md               # This file

core/interfaces/
└── llm_provider.py         # ILLMProvider interface
```

## Adding New Providers

To add a new provider:

1. Create a new file in `PrismQ/Providers/`
2. Implement the `ILLMProvider` or `IAsyncLLMProvider` interface
3. Add error handling and retry logic as needed
4. Export from `__init__.py`
5. Add tests
6. Update documentation

Example:

```python
from core.interfaces.llm_provider import ILLMProvider

class MyProvider(ILLMProvider):
    @property
    def model_name(self) -> str:
        return "my-model"
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        # Implementation here
        pass
    
    def generate_chat(self, messages: List[Dict], **kwargs) -> str:
        # Implementation here
        pass
```

## See Also

- [Migration Guide](../docs/MIGRATION_GUIDE.md) - Full migration documentation
- [Examples](../examples/provider_architecture_example.py) - Working examples
- [Tests](../tests/test_openai_provider.py) - Test examples
- [Interface Definition](../core/interfaces/llm_provider.py) - Interface contracts
