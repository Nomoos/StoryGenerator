"""
Tests for Pipeline Stage Contracts and Interfaces.

These tests demonstrate how pipeline stages can be tested independently
without dependencies on other stages or their implementations.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    # Base interfaces
    IPipelineStage,
    BasePipelineStage,
    StageResult,
    StageMetadata,
    StageStatus,
    # Stage 01 contracts
    IdeaGenerationInput,
    IdeaGenerationOutput,
    IdeaItem,
    # Stage 02 contracts
    TextGenerationInput,
    TextGenerationOutput,
    TextContent,
    # Stage 03 contracts
    AudioGenerationInput,
    AudioGenerationOutput,
    AudioContent,
    SubtitleSegment,
    # Stage 04 contracts
    ImageGenerationInput,
    ImageGenerationOutput,
    KeyFrame,
    # Stage 05 contracts
    VideoGenerationInput,
    VideoGenerationOutput,
    VideoContent,
)


# ============================================================================
# Test Base Pipeline Stage Interface
# ============================================================================

class MockPipelineStage(BasePipelineStage[dict, dict]):
    """Mock pipeline stage for testing."""
    
    async def _execute_impl(self, input_data: dict) -> dict:
        """Simple implementation for testing."""
        return {"result": "success", "input": input_data}
    
    async def validate_input(self, input_data: dict) -> bool:
        """Validate that input is a non-empty dict."""
        return isinstance(input_data, dict) and len(input_data) > 0


class TestBasePipelineStage:
    """Test the base pipeline stage implementation."""
    
    @pytest.mark.asyncio
    async def test_stage_initialization(self):
        """Test stage initialization with metadata."""
        stage = MockPipelineStage(
            stage_name="TestStage",
            stage_id="test_stage",
            version="1.0.0"
        )
        
        assert stage.stage_name == "TestStage"
        assert stage.stage_id == "test_stage"
        assert stage.stage_version == "1.0.0"
    
    @pytest.mark.asyncio
    async def test_stage_execute_success(self):
        """Test successful stage execution."""
        stage = MockPipelineStage(
            stage_name="TestStage",
            stage_id="test_stage",
            version="1.0.0"
        )
        
        input_data = {"key": "value"}
        result = await stage.execute(input_data)
        
        assert isinstance(result, StageResult)
        assert result.data["result"] == "success"
        assert result.data["input"] == input_data
        assert result.metadata.status == StageStatus.COMPLETED
        assert result.metadata.stage_name == "TestStage"
        assert result.metadata.execution_time_ms > 0
    
    @pytest.mark.asyncio
    async def test_stage_execute_with_invalid_input(self):
        """Test stage execution with invalid input."""
        stage = MockPipelineStage(
            stage_name="TestStage",
            stage_id="test_stage",
            version="1.0.0"
        )
        
        # Empty dict should fail validation
        with pytest.raises(ValueError, match="Invalid input"):
            await stage.execute({})
    
    @pytest.mark.asyncio
    async def test_stage_metadata_on_success(self):
        """Test metadata is populated correctly on success."""
        stage = MockPipelineStage(
            stage_name="TestStage",
            stage_id="test_stage",
            version="2.0.0"
        )
        
        result = await stage.execute({"test": "data"})
        metadata = result.metadata
        
        assert metadata.stage_name == "TestStage"
        assert metadata.stage_id == "test_stage"
        assert metadata.version == "2.0.0"
        assert metadata.status == StageStatus.COMPLETED
        assert metadata.error_message is None
        assert isinstance(metadata.executed_at, datetime)


# ============================================================================
# Test Stage 01: Idea Generation Contracts
# ============================================================================

class TestIdeaGenerationContracts:
    """Test Idea Generation stage contracts."""
    
    def test_idea_generation_input_creation(self):
        """Test creating IdeaGenerationInput."""
        input_data = IdeaGenerationInput(
            target_gender="women",
            target_age="18-23",
            idea_count=20
        )
        
        assert input_data.target_gender == "women"
        assert input_data.target_age == "18-23"
        assert input_data.idea_count == 20
        assert input_data.source_stories is None
    
    def test_idea_generation_output_creation(self):
        """Test creating IdeaGenerationOutput."""
        idea = IdeaItem(
            id="test_001",
            content="Test idea content",
            source="test",
            target_gender="women",
            target_age="18-23",
            created_at=datetime.now()
        )
        
        output = IdeaGenerationOutput(
            ideas=[idea],
            total_count=1,
            adapted_count=0,
            generated_count=1
        )
        
        assert len(output.ideas) == 1
        assert output.total_count == 1
        assert output.ideas[0].id == "test_001"
    
    def test_idea_item_structure(self):
        """Test IdeaItem data structure."""
        now = datetime.now()
        idea = IdeaItem(
            id="llm_001",
            content="A story about personal growth",
            source="llm_generated",
            target_gender="men",
            target_age="24-29",
            created_at=now,
            metadata={"score": 95}
        )
        
        assert idea.id == "llm_001"
        assert idea.content == "A story about personal growth"
        assert idea.source == "llm_generated"
        assert idea.target_gender == "men"
        assert idea.target_age == "24-29"
        assert idea.created_at == now
        assert idea.metadata["score"] == 95


# ============================================================================
# Test Stage 02: Text Generation Contracts
# ============================================================================

class TestTextGenerationContracts:
    """Test Text Generation stage contracts."""
    
    def test_text_generation_input_creation(self):
        """Test creating TextGenerationInput."""
        idea = IdeaItem(
            id="test_001",
            content="Test content",
            source="test",
            target_gender="women",
            target_age="18-23",
            created_at=datetime.now()
        )
        
        input_data = TextGenerationInput(
            idea=idea,
            generate_title=True,
            generate_description=True,
            generate_tags=True
        )
        
        assert input_data.idea.id == "test_001"
        assert input_data.generate_title is True
        assert input_data.generate_description is True
    
    def test_text_content_structure(self):
        """Test TextContent data structure."""
        content = TextContent(
            story_script="Once upon a time...",
            title="The Journey",
            description="An epic tale",
            tags=["adventure", "inspiration"],
            scenes=[
                {"timestamp": 0, "description": "Opening scene"}
            ]
        )
        
        assert content.story_script == "Once upon a time..."
        assert content.title == "The Journey"
        assert len(content.tags) == 2
        assert len(content.scenes) == 1


# ============================================================================
# Test Stage 03: Audio Generation Contracts
# ============================================================================

class TestAudioGenerationContracts:
    """Test Audio Generation stage contracts."""
    
    def test_audio_generation_input_creation(self):
        """Test creating AudioGenerationInput."""
        text_content = TextContent(
            story_script="Test script",
            title="Test"
        )
        
        input_data = AudioGenerationInput(
            text_content=text_content,
            voice_id="female_1",
            generate_subtitles=True,
            audio_format="mp3"
        )
        
        assert input_data.text_content.story_script == "Test script"
        assert input_data.voice_id == "female_1"
        assert input_data.audio_format == "mp3"
    
    def test_subtitle_segment_structure(self):
        """Test SubtitleSegment data structure."""
        segment = SubtitleSegment(
            start_time=0.0,
            end_time=3.5,
            text="Hello world"
        )
        
        assert segment.start_time == 0.0
        assert segment.end_time == 3.5
        assert segment.text == "Hello world"
    
    def test_audio_content_structure(self):
        """Test AudioContent data structure."""
        audio = AudioContent(
            audio_file_path="/path/to/audio.mp3",
            duration_seconds=45.5,
            subtitles=[
                SubtitleSegment(0.0, 3.5, "First line"),
                SubtitleSegment(3.5, 7.0, "Second line")
            ],
            voice_id="female_1"
        )
        
        assert audio.audio_file_path == "/path/to/audio.mp3"
        assert audio.duration_seconds == 45.5
        assert len(audio.subtitles) == 2
        assert audio.voice_id == "female_1"


# ============================================================================
# Test Stage 04: Image Generation Contracts
# ============================================================================

class TestImageGenerationContracts:
    """Test Image Generation stage contracts."""
    
    def test_keyframe_structure(self):
        """Test KeyFrame data structure."""
        keyframe = KeyFrame(
            id="kf_001",
            image_path="/path/to/image.png",
            timestamp=5.5,
            description="Main character in action",
            metadata={"style": "cinematic"}
        )
        
        assert keyframe.id == "kf_001"
        assert keyframe.image_path == "/path/to/image.png"
        assert keyframe.timestamp == 5.5
        assert keyframe.metadata["style"] == "cinematic"
    
    def test_image_generation_output_creation(self):
        """Test creating ImageGenerationOutput."""
        keyframes = [
            KeyFrame("kf_001", "/img1.png", 0.0, "Scene 1"),
            KeyFrame("kf_002", "/img2.png", 10.0, "Scene 2")
        ]
        
        output = ImageGenerationOutput(
            keyframes=keyframes,
            metadata={"total_generation_time": 120}
        )
        
        assert len(output.keyframes) == 2
        assert output.metadata["total_generation_time"] == 120


# ============================================================================
# Test Stage 05: Video Generation Contracts
# ============================================================================

class TestVideoGenerationContracts:
    """Test Video Generation stage contracts."""
    
    def test_video_content_structure(self):
        """Test VideoContent data structure."""
        video = VideoContent(
            video_file_path="/path/to/video.mp4",
            duration_seconds=45.5,
            resolution="1080x1920",
            fps=30,
            file_size_bytes=15728640,
            metadata={"codec": "h264"}
        )
        
        assert video.video_file_path == "/path/to/video.mp4"
        assert video.duration_seconds == 45.5
        assert video.resolution == "1080x1920"
        assert video.fps == 30
        assert video.file_size_bytes == 15728640
    
    def test_video_generation_input_creation(self):
        """Test creating VideoGenerationInput with all components."""
        text_content = TextContent(story_script="Test", title="Test")
        audio_content = AudioContent(
            audio_file_path="/audio.mp3",
            duration_seconds=30.0
        )
        keyframes = [KeyFrame("kf_001", "/img.png", 0.0, "Test")]
        
        input_data = VideoGenerationInput(
            text_content=text_content,
            audio_content=audio_content,
            keyframes=keyframes,
            video_format="mp4",
            resolution="1080x1920",
            fps=30
        )
        
        assert input_data.text_content.title == "Test"
        assert input_data.audio_content.duration_seconds == 30.0
        assert len(input_data.keyframes) == 1
        assert input_data.video_format == "mp4"
        assert input_data.fps == 30


# ============================================================================
# Test Pipeline Integration (without implementations)
# ============================================================================

class TestPipelineContractChaining:
    """Test that stage contracts can be chained together."""
    
    def test_stage_output_to_input_chaining(self):
        """Test passing output from one stage as input to next."""
        # Stage 01 output
        idea = IdeaItem(
            id="test_001",
            content="Test idea",
            source="test",
            target_gender="women",
            target_age="18-23",
            created_at=datetime.now()
        )
        
        idea_output = IdeaGenerationOutput(
            ideas=[idea],
            total_count=1,
            adapted_count=0,
            generated_count=1
        )
        
        # Use Stage 01 output as Stage 02 input
        text_input = TextGenerationInput(idea=idea_output.ideas[0])
        assert text_input.idea.id == "test_001"
        
        # Stage 02 output
        text_output = TextGenerationOutput(
            content=TextContent(
                story_script="Script",
                title="Title"
            )
        )
        
        # Use Stage 02 output as Stage 03 input
        audio_input = AudioGenerationInput(
            text_content=text_output.content
        )
        assert audio_input.text_content.title == "Title"
        
        # This demonstrates contracts enable stage chaining
        # without any cross-stage implementation dependencies
