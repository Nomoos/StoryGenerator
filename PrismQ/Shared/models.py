"""Data models and validation schemas for StoryGenerator.

This module provides Pydantic models for type-safe data validation throughout
the application. All models include comprehensive validation rules and clear
error messages.
"""

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class TargetGender(str, Enum):
    """Target gender for content."""

    WOMEN = "women"
    MEN = "men"


class TargetAge(str, Enum):
    """Target age range for content."""

    AGE_10_13 = "10-13"
    AGE_14_17 = "14-17"
    AGE_18_23 = "18-23"


class ContentSource(str, Enum):
    """Source of content."""

    REDDIT = "reddit"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    MANUAL = "manual"
    GENERATED = "generated"


class StoryIdea(BaseModel):
    """A story idea for video generation.

    Attributes:
        id: Unique identifier for the idea
        content: The actual story content
        target_gender: Target gender audience
        target_age: Target age range
        source: Source of the content
        score: Quality score (0-100)
        metadata: Additional metadata
    """

    id: str = Field(..., min_length=1, max_length=100, description="Unique identifier")
    content: str = Field(..., min_length=10, max_length=5000, description="Story content text")
    target_gender: TargetGender = Field(..., description="Target gender audience")
    target_age: TargetAge = Field(..., description="Target age range")
    source: ContentSource = Field(..., description="Source of the content")
    score: float = Field(default=0.0, ge=0.0, le=100.0, description="Quality score (0-100)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate content is not empty after stripping whitespace."""
        if not v.strip():
            raise ValueError("Content cannot be empty or only whitespace")
        return v.strip()

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate ID format."""
        if not v.strip():
            raise ValueError("ID cannot be empty or only whitespace")
        # ID should be alphanumeric with hyphens and underscores
        if not all(c.isalnum() or c in "-_" for c in v):
            raise ValueError(
                "ID must contain only alphanumeric characters, hyphens, and underscores"
            )
        return v


class ScriptConfig(BaseModel):
    """Configuration for script generation.

    Attributes:
        min_words: Minimum word count
        max_words: Maximum word count
        temperature: LLM temperature (0.0-1.0)
        max_tokens: Maximum tokens to generate
        model: LLM model to use
    """

    min_words: int = Field(default=350, ge=100, le=1000, description="Minimum word count")
    max_words: int = Field(default=370, ge=100, le=1000, description="Maximum word count")
    temperature: float = Field(
        default=0.7, ge=0.0, le=1.0, description="LLM temperature for creativity"
    )
    max_tokens: int = Field(
        default=2000, ge=100, le=10000, description="Maximum tokens to generate"
    )
    model: str = Field(default="gpt-4", min_length=1, max_length=100, description="LLM model name")

    @model_validator(mode="after")
    def validate_word_range(self) -> "ScriptConfig":
        """Validate that max_words is greater than min_words."""
        if self.max_words <= self.min_words:
            raise ValueError("max_words must be greater than min_words")
        return self


class TitleConfig(BaseModel):
    """Configuration for title generation.

    Attributes:
        count: Number of titles to generate
        min_length: Minimum character length
        max_length: Maximum character length
        require_emoji: Whether to require emojis
        temperature: LLM temperature
    """

    count: int = Field(default=10, ge=1, le=100, description="Number of titles to generate")
    min_length: int = Field(
        default=20, ge=10, le=200, description="Minimum title length in characters"
    )
    max_length: int = Field(
        default=100, ge=10, le=200, description="Maximum title length in characters"
    )
    require_emoji: bool = Field(default=False, description="Whether titles must contain emojis")
    temperature: float = Field(
        default=0.8, ge=0.0, le=1.0, description="LLM temperature for creativity"
    )

    @model_validator(mode="after")
    def validate_length_range(self) -> "TitleConfig":
        """Validate that max_length is greater than min_length."""
        if self.max_length <= self.min_length:
            raise ValueError("max_length must be greater than min_length")
        return self


class AudioConfig(BaseModel):
    """Configuration for audio generation.

    Attributes:
        voice_id: ElevenLabs voice ID
        stability: Voice stability (0.0-1.0)
        similarity_boost: Similarity boost (0.0-1.0)
        style: Voice style value (0.0-1.0)
        use_speaker_boost: Whether to use speaker boost
    """

    voice_id: str = Field(..., min_length=1, max_length=100, description="Voice ID")
    stability: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Voice stability (0=varied, 1=stable)"
    )
    similarity_boost: float = Field(
        default=0.75,
        ge=0.0,
        le=1.0,
        description="Similarity to training voice (0=creative, 1=similar)",
    )
    style: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Style exaggeration (0=none, 1=exaggerated)"
    )
    use_speaker_boost: bool = Field(
        default=True, description="Whether to enhance clarity and similarity"
    )


class ImageConfig(BaseModel):
    """Configuration for image generation.

    Attributes:
        width: Image width in pixels
        height: Image height in pixels
        steps: Number of diffusion steps
        guidance_scale: Guidance scale for prompt adherence
        negative_prompt: Negative prompt to avoid certain features
        seed: Random seed for reproducibility
    """

    width: int = Field(
        default=1024, ge=256, le=2048, multiple_of=8, description="Image width in pixels"
    )
    height: int = Field(
        default=1024, ge=256, le=2048, multiple_of=8, description="Image height in pixels"
    )
    steps: int = Field(
        default=30, ge=10, le=100, description="Number of diffusion steps (higher=better)"
    )
    guidance_scale: float = Field(
        default=7.5,
        ge=1.0,
        le=20.0,
        description="Guidance scale (lower=creative, higher=accurate)",
    )
    negative_prompt: Optional[str] = Field(
        default=None, max_length=1000, description="What to avoid in the image"
    )
    seed: Optional[int] = Field(
        default=None, ge=0, le=2**32 - 1, description="Random seed for reproducibility"
    )


class VideoConfig(BaseModel):
    """Configuration for video generation.

    Attributes:
        fps: Frames per second
        duration: Duration in seconds
        resolution: Video resolution
        codec: Video codec
        bitrate: Video bitrate
    """

    fps: int = Field(default=30, ge=1, le=60, description="Frames per second")
    duration: float = Field(default=60.0, ge=1.0, le=300.0, description="Duration in seconds")
    resolution: Literal["720p", "1080p", "4k"] = Field(
        default="1080p", description="Video resolution"
    )
    codec: str = Field(default="libx264", min_length=1, max_length=50, description="Video codec")
    bitrate: str = Field(
        default="5M", min_length=1, max_length=20, description="Video bitrate (e.g., '5M')"
    )


class APIResponse(BaseModel):
    """Generic API response wrapper.

    Attributes:
        success: Whether the operation succeeded
        data: Response data
        error: Error message if failed
        metadata: Additional metadata
    """

    success: bool = Field(..., description="Whether the operation succeeded")
    data: Optional[Any] = Field(default=None, description="Response data")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @model_validator(mode="after")
    def validate_response(self) -> "APIResponse":
        """Validate that error is set if success is False."""
        if not self.success and not self.error:
            raise ValueError("error message must be provided when success is False")
        if self.success and self.error:
            raise ValueError("error message should not be provided when success is True")
        return self


class BatchRequest(BaseModel):
    """Request for batch processing.

    Attributes:
        items: List of items to process
        batch_size: Size of each batch
        parallel: Whether to process in parallel
        max_workers: Maximum number of parallel workers
    """

    items: List[Any] = Field(..., min_length=1, description="Items to process")
    batch_size: int = Field(default=10, ge=1, le=100, description="Size of each processing batch")
    parallel: bool = Field(default=True, description="Whether to process in parallel")
    max_workers: int = Field(
        default=4, ge=1, le=32, description="Maximum number of parallel workers"
    )

    @model_validator(mode="after")
    def validate_workers(self) -> "BatchRequest":
        """Validate max_workers is reasonable for batch_size."""
        if not self.parallel and self.max_workers > 1:
            raise ValueError("max_workers should be 1 when parallel is False")
        return self
