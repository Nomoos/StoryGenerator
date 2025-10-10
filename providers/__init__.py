"""
Providers package for external service integrations.

This package contains concrete implementations of various service providers
including LLM providers (OpenAI), voice synthesis (ElevenLabs), platform
integrations (YouTube, TikTok, Instagram), and storage.
"""

from .mock_provider import MockLLMProvider, AsyncMockLLMProvider

# Conditionally import OpenAI provider to avoid hard dependency
try:
    from .openai_provider import OpenAIProvider, AsyncOpenAIProvider
    _has_openai = True
except ImportError:
    _has_openai = False
    OpenAIProvider = None
    AsyncOpenAIProvider = None

# Conditionally import platform providers
try:
    from .youtube_provider import YouTubeUploader, YouTubeAnalytics
    _has_youtube = True
except ImportError:
    _has_youtube = False
    YouTubeUploader = None
    YouTubeAnalytics = None

try:
    from .tiktok_provider import TikTokUploader, TikTokAnalytics
    _has_tiktok = True
except ImportError:
    _has_tiktok = False
    TikTokUploader = None
    TikTokAnalytics = None

try:
    from .instagram_provider import InstagramUploader, InstagramAnalytics
    _has_instagram = True
except ImportError:
    _has_instagram = False
    InstagramUploader = None
    InstagramAnalytics = None

__all__ = [
    "MockLLMProvider",
    "AsyncMockLLMProvider",
]

if _has_openai:
    __all__.extend([
        "OpenAIProvider",
        "AsyncOpenAIProvider",
    ])

if _has_youtube:
    __all__.extend([
        "YouTubeUploader",
        "YouTubeAnalytics",
    ])

if _has_tiktok:
    __all__.extend([
        "TikTokUploader",
        "TikTokAnalytics",
    ])

if _has_instagram:
    __all__.extend([
        "InstagramUploader",
        "InstagramAnalytics",
    ])

