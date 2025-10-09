"""
Providers package for external service integrations.

This package contains concrete implementations of various service providers
including LLM providers (OpenAI), voice synthesis (ElevenLabs), and storage.
"""

from .openai_provider import OpenAIProvider

__all__ = ["OpenAIProvider"]
