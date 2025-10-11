"""
Core interfaces package.

This package contains abstract base classes (interfaces) that define contracts
for various service providers (LLM, Storage, Voice, etc.).
"""

from core.interfaces.llm_provider import (
    ILLMProvider,
    IAsyncLLMProvider,
    ChatMessage,
)
from core.interfaces.storage_provider import (
    IStorageProvider,
    IFileSystemProvider,
)
from core.interfaces.voice_provider import (
    IVoiceProvider,
    IVoiceCloningProvider,
)

__all__ = [
    "ILLMProvider",
    "IAsyncLLMProvider",
    "ChatMessage",
    "IStorageProvider",
    "IFileSystemProvider",
    "IVoiceProvider",
    "IVoiceCloningProvider",
]
