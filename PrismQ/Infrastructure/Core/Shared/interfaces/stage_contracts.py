"""
Pipeline Stage Contracts.

This module defines the input/output contracts for each pipeline stage.
These contracts enable independent development and testing of stages.
"""

from dataclasses import dataclass, field
from typing import Any
from datetime import datetime


# ============================================================================
# Stage 01: Idea Generation
# ============================================================================

@dataclass
class IdeaGenerationInput:
    """
    Input contract for Idea Generation stage.
    
    Attributes:
        target_gender: Target audience gender (e.g., 'women', 'men', 'all')
        target_age: Target age bucket (e.g., '18-23', '24-29', '30-39')
        idea_count: Number of ideas to generate
        source_stories: Optional list of source stories to adapt
        additional_params: Additional parameters for idea generation
    """
    target_gender: str
    target_age: str
    idea_count: int = 20
    source_stories: list[dict[str, Any]] | None = None
    additional_params: dict[str, Any] = field(default_factory=dict)


@dataclass
class IdeaItem:
    """
    A single generated idea.
    
    Attributes:
        id: Unique identifier for the idea
        content: The idea content/description
        source: Source of the idea (e.g., 'reddit_adapted', 'llm_generated')
        target_gender: Target gender for this idea
        target_age: Target age bucket for this idea
        created_at: When the idea was created
        metadata: Additional metadata about the idea
    """
    id: str
    content: str
    source: str
    target_gender: str
    target_age: str
    created_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class IdeaGenerationOutput:
    """
    Output contract for Idea Generation stage.
    
    Attributes:
        ideas: List of generated ideas
        total_count: Total number of ideas generated
        adapted_count: Number of ideas adapted from sources
        generated_count: Number of LLM-generated ideas
        metadata: Stage execution metadata
    """
    ideas: list[IdeaItem]
    total_count: int
    adapted_count: int
    generated_count: int
    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Stage 02: Text Generation
# ============================================================================

@dataclass
class TextGenerationInput:
    """
    Input contract for Text Generation stage.
    
    Attributes:
        idea: The idea to develop into text content
        generate_title: Whether to generate a title
        generate_description: Whether to generate a description
        generate_tags: Whether to generate tags
        generate_scenes: Whether to generate scene descriptions
        additional_params: Additional parameters for text generation
    """
    idea: IdeaItem
    generate_title: bool = True
    generate_description: bool = True
    generate_tags: bool = True
    generate_scenes: bool = True
    additional_params: dict[str, Any] = field(default_factory=dict)


@dataclass
class TextContent:
    """
    Generated text content.
    
    Attributes:
        story_script: Main story script/narrative
        title: Generated title (if requested)
        description: Generated description (if requested)
        tags: Generated tags (if requested)
        scenes: Scene descriptions (if requested)
        metadata: Additional metadata
    """
    story_script: str
    title: str | None = None
    description: str | None = None
    tags: list[str] = field(default_factory=list)
    scenes: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TextGenerationOutput:
    """
    Output contract for Text Generation stage.
    
    Attributes:
        content: Generated text content
        quality_score: Quality score of the generated content (0-100)
        metadata: Stage execution metadata
    """
    content: TextContent
    quality_score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Stage 03: Audio Generation
# ============================================================================

@dataclass
class AudioGenerationInput:
    """
    Input contract for Audio Generation stage.
    
    Attributes:
        text_content: Text content to convert to audio
        voice_id: Voice identifier to use
        generate_subtitles: Whether to generate subtitles
        audio_format: Desired audio format (e.g., 'mp3', 'wav')
        additional_params: Additional parameters for audio generation
    """
    text_content: TextContent
    voice_id: str | None = None
    generate_subtitles: bool = True
    audio_format: str = "mp3"
    additional_params: dict[str, Any] = field(default_factory=dict)


@dataclass
class SubtitleSegment:
    """
    A subtitle segment.
    
    Attributes:
        start_time: Start time in seconds
        end_time: End time in seconds
        text: Subtitle text
    """
    start_time: float
    end_time: float
    text: str


@dataclass
class AudioContent:
    """
    Generated audio content.
    
    Attributes:
        audio_file_path: Path to the generated audio file
        duration_seconds: Duration of the audio in seconds
        subtitles: Generated subtitles (if requested)
        voice_id: Voice ID used for generation
        metadata: Additional metadata
    """
    audio_file_path: str
    duration_seconds: float
    subtitles: list[SubtitleSegment] = field(default_factory=list)
    voice_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AudioGenerationOutput:
    """
    Output contract for Audio Generation stage.
    
    Attributes:
        audio: Generated audio content
        metadata: Stage execution metadata
    """
    audio: AudioContent
    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Stage 04: Image Generation
# ============================================================================

@dataclass
class ImageGenerationInput:
    """
    Input contract for Image Generation stage.
    
    Attributes:
        text_content: Text content to generate images for
        audio_content: Audio content for timing synchronization
        keyframe_count: Number of keyframes to generate
        image_style: Style for image generation
        additional_params: Additional parameters for image generation
    """
    text_content: TextContent
    audio_content: AudioContent | None = None
    keyframe_count: int = 5
    image_style: str | None = None
    additional_params: dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyFrame:
    """
    A generated keyframe.
    
    Attributes:
        id: Unique identifier for the keyframe
        image_path: Path to the generated image
        timestamp: Timestamp in the video (seconds)
        description: Description of the keyframe
        metadata: Additional metadata
    """
    id: str
    image_path: str
    timestamp: float
    description: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageGenerationOutput:
    """
    Output contract for Image Generation stage.
    
    Attributes:
        keyframes: List of generated keyframes
        metadata: Stage execution metadata
    """
    keyframes: list[KeyFrame]
    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Stage 05: Video Generation
# ============================================================================

@dataclass
class VideoGenerationInput:
    """
    Input contract for Video Generation stage.
    
    Attributes:
        text_content: Text content for the video
        audio_content: Audio content for the video
        keyframes: Generated keyframes/images
        video_format: Desired video format (e.g., 'mp4', 'webm')
        resolution: Video resolution (e.g., '1920x1080', '1080x1920')
        fps: Frames per second
        additional_params: Additional parameters for video generation
    """
    text_content: TextContent
    audio_content: AudioContent
    keyframes: list[KeyFrame]
    video_format: str = "mp4"
    resolution: str = "1080x1920"
    fps: int = 30
    additional_params: dict[str, Any] = field(default_factory=dict)


@dataclass
class VideoContent:
    """
    Generated video content.
    
    Attributes:
        video_file_path: Path to the generated video file
        duration_seconds: Duration of the video in seconds
        resolution: Video resolution
        fps: Frames per second
        file_size_bytes: File size in bytes
        metadata: Additional metadata
    """
    video_file_path: str
    duration_seconds: float
    resolution: str
    fps: int
    file_size_bytes: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VideoGenerationOutput:
    """
    Output contract for Video Generation stage.
    
    Attributes:
        video: Generated video content
        metadata: Stage execution metadata
    """
    video: VideoContent
    metadata: dict[str, Any] = field(default_factory=dict)
