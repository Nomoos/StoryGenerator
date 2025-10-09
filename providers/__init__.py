"""
Providers package for external service integrations.

This package contains concrete implementations of various service providers
including LLM providers (OpenAI), voice synthesis (ElevenLabs), and storage.
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

__all__ = [
    "MockLLMProvider",
    "AsyncMockLLMProvider",
]

if _has_openai:
    __all__.extend([
        "OpenAIProvider",
        "AsyncOpenAIProvider",
    ])

