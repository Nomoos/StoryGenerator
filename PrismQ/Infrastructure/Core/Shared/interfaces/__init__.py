"""
Core interfaces package.

This package contains abstract base classes (interfaces) that define contracts
for various service providers (LLM, Storage, Voice, etc.) and pipeline stages.
"""

from PrismQ.Shared.interfaces.llm_provider import (
    ILLMProvider,
    IAsyncLLMProvider,
    ChatMessage,
)
from PrismQ.Shared.interfaces.storage_provider import (
    IStorageProvider,
    IFileSystemProvider,
)
from PrismQ.Shared.interfaces.voice_provider import (
    IVoiceProvider,
    IVoiceCloningProvider,
)
from PrismQ.Infrastructure.Core.Shared.interfaces.pipeline_stage import (
    IPipelineStage,
    BasePipelineStage,
    StageResult,
    StageMetadata,
    StageStatus,
)
from PrismQ.Infrastructure.Core.Shared.interfaces.stage_contracts import (
    # Stage 01: Idea Generation
    IdeaGenerationInput,
    IdeaGenerationOutput,
    IdeaItem,
    # Stage 02: Text Generation
    TextGenerationInput,
    TextGenerationOutput,
    TextContent,
    # Stage 03: Audio Generation
    AudioGenerationInput,
    AudioGenerationOutput,
    AudioContent,
    SubtitleSegment,
    # Stage 04: Image Generation
    ImageGenerationInput,
    ImageGenerationOutput,
    KeyFrame,
    # Stage 05: Video Generation
    VideoGenerationInput,
    VideoGenerationOutput,
    VideoContent,
)

__all__ = [
    # Provider interfaces
    "ILLMProvider",
    "IAsyncLLMProvider",
    "ChatMessage",
    "IStorageProvider",
    "IFileSystemProvider",
    "IVoiceProvider",
    "IVoiceCloningProvider",
    # Pipeline stage interfaces
    "IPipelineStage",
    "BasePipelineStage",
    "StageResult",
    "StageMetadata",
    "StageStatus",
    # Stage contracts - Idea Generation
    "IdeaGenerationInput",
    "IdeaGenerationOutput",
    "IdeaItem",
    # Stage contracts - Text Generation
    "TextGenerationInput",
    "TextGenerationOutput",
    "TextContent",
    # Stage contracts - Audio Generation
    "AudioGenerationInput",
    "AudioGenerationOutput",
    "AudioContent",
    "SubtitleSegment",
    # Stage contracts - Image Generation
    "ImageGenerationInput",
    "ImageGenerationOutput",
    "KeyFrame",
    # Stage contracts - Video Generation
    "VideoGenerationInput",
    "VideoGenerationOutput",
    "VideoContent",
]
