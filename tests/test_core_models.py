"""Tests for core.models module."""

import pytest
from pydantic import ValidationError

from core.models import (APIResponse, AudioConfig, BatchRequest, ContentSource,
                         ImageConfig, ScriptConfig, StoryIdea, TargetAge,
                         TargetGender, TitleConfig, VideoConfig)


class TestStoryIdea:
    """Tests for StoryIdea model."""

    def test_valid_story_idea(self):
        """Test creating a valid StoryIdea."""
        idea = StoryIdea(
            id="test-id-123",
            content="This is a valid story content with enough characters",
            target_gender=TargetGender.WOMEN,
            target_age=TargetAge.AGE_18_23,
            source=ContentSource.REDDIT,
        )
        assert idea.id == "test-id-123"
        assert idea.target_gender == TargetGender.WOMEN
        assert idea.score == 0.0

    def test_story_idea_with_score(self):
        """Test StoryIdea with custom score."""
        idea = StoryIdea(
            id="test-id",
            content="Story content here",
            target_gender="women",
            target_age="18-23",
            source="reddit",
            score=85.5,
        )
        assert idea.score == 85.5

    def test_story_idea_content_too_short(self):
        """Test that content must be at least 10 characters."""
        with pytest.raises(ValidationError) as exc_info:
            StoryIdea(
                id="test",
                content="Short",
                target_gender="women",
                target_age="18-23",
                source="reddit",
            )
        assert "at least 10 characters" in str(exc_info.value)

    def test_story_idea_empty_content(self):
        """Test that content cannot be empty or whitespace."""
        with pytest.raises(ValidationError) as exc_info:
            StoryIdea(
                id="test",
                content="          ",
                target_gender="women",
                target_age="18-23",
                source="reddit",
            )
        assert "cannot be empty" in str(exc_info.value).lower()

    def test_story_idea_invalid_id_characters(self):
        """Test that ID must contain only valid characters."""
        with pytest.raises(ValidationError) as exc_info:
            StoryIdea(
                id="test@#$%",
                content="Valid content here",
                target_gender="women",
                target_age="18-23",
                source="reddit",
            )
        assert "alphanumeric" in str(exc_info.value).lower()

    def test_story_idea_score_range(self):
        """Test that score must be between 0 and 100."""
        with pytest.raises(ValidationError):
            StoryIdea(
                id="test",
                content="Valid content",
                target_gender="women",
                target_age="18-23",
                source="reddit",
                score=-10,
            )

        with pytest.raises(ValidationError):
            StoryIdea(
                id="test",
                content="Valid content",
                target_gender="women",
                target_age="18-23",
                source="reddit",
                score=150,
            )

    def test_story_idea_with_metadata(self):
        """Test StoryIdea with metadata."""
        idea = StoryIdea(
            id="test",
            content="Story content",
            target_gender="women",
            target_age="18-23",
            source="reddit",
            metadata={"author": "test_user", "upvotes": 100},
        )
        assert idea.metadata["author"] == "test_user"
        assert idea.metadata["upvotes"] == 100


class TestScriptConfig:
    """Tests for ScriptConfig model."""

    def test_valid_script_config(self):
        """Test creating a valid ScriptConfig."""
        config = ScriptConfig()
        assert config.min_words == 350
        assert config.max_words == 370
        assert config.temperature == 0.7

    def test_script_config_custom_values(self):
        """Test ScriptConfig with custom values."""
        config = ScriptConfig(min_words=300, max_words=400, temperature=0.9, model="gpt-3.5-turbo")
        assert config.min_words == 300
        assert config.max_words == 400
        assert config.model == "gpt-3.5-turbo"

    def test_script_config_invalid_word_range(self):
        """Test that max_words must be greater than min_words."""
        with pytest.raises(ValidationError) as exc_info:
            ScriptConfig(min_words=400, max_words=300)
        assert "greater than min_words" in str(exc_info.value)

    def test_script_config_equal_words(self):
        """Test that max_words cannot equal min_words."""
        with pytest.raises(ValidationError):
            ScriptConfig(min_words=350, max_words=350)

    def test_script_config_temperature_range(self):
        """Test that temperature must be between 0 and 1."""
        with pytest.raises(ValidationError):
            ScriptConfig(temperature=-0.1)

        with pytest.raises(ValidationError):
            ScriptConfig(temperature=1.5)


class TestTitleConfig:
    """Tests for TitleConfig model."""

    def test_valid_title_config(self):
        """Test creating a valid TitleConfig."""
        config = TitleConfig()
        assert config.count == 10
        assert config.min_length == 20
        assert config.max_length == 100

    def test_title_config_invalid_length_range(self):
        """Test that max_length must be greater than min_length."""
        with pytest.raises(ValidationError) as exc_info:
            TitleConfig(min_length=100, max_length=50)
        assert "greater than min_length" in str(exc_info.value)

    def test_title_config_count_range(self):
        """Test that count must be within valid range."""
        with pytest.raises(ValidationError):
            TitleConfig(count=0)

        with pytest.raises(ValidationError):
            TitleConfig(count=150)


class TestAudioConfig:
    """Tests for AudioConfig model."""

    def test_valid_audio_config(self):
        """Test creating a valid AudioConfig."""
        config = AudioConfig(voice_id="test-voice-123")
        assert config.voice_id == "test-voice-123"
        assert config.stability == 0.5
        assert config.similarity_boost == 0.75

    def test_audio_config_parameter_ranges(self):
        """Test that audio parameters are within valid ranges."""
        with pytest.raises(ValidationError):
            AudioConfig(voice_id="test", stability=-0.1)

        with pytest.raises(ValidationError):
            AudioConfig(voice_id="test", similarity_boost=1.5)

        with pytest.raises(ValidationError):
            AudioConfig(voice_id="test", style=-0.1)


class TestImageConfig:
    """Tests for ImageConfig model."""

    def test_valid_image_config(self):
        """Test creating a valid ImageConfig."""
        config = ImageConfig()
        assert config.width == 1024
        assert config.height == 1024
        assert config.steps == 30

    def test_image_config_dimensions_multiple_of_8(self):
        """Test that dimensions must be multiples of 8."""
        # Valid: multiple of 8
        config = ImageConfig(width=512, height=768)
        assert config.width == 512

        # Invalid: not multiple of 8
        with pytest.raises(ValidationError):
            ImageConfig(width=513)

    def test_image_config_with_seed(self):
        """Test ImageConfig with seed."""
        config = ImageConfig(seed=12345)
        assert config.seed == 12345

    def test_image_config_seed_range(self):
        """Test that seed must be within valid range."""
        with pytest.raises(ValidationError):
            ImageConfig(seed=-1)

        with pytest.raises(ValidationError):
            ImageConfig(seed=2**32)


class TestVideoConfig:
    """Tests for VideoConfig model."""

    def test_valid_video_config(self):
        """Test creating a valid VideoConfig."""
        config = VideoConfig()
        assert config.fps == 30
        assert config.duration == 60.0
        assert config.resolution == "1080p"

    def test_video_config_resolutions(self):
        """Test valid video resolutions."""
        config = VideoConfig(resolution="720p")
        assert config.resolution == "720p"

        config = VideoConfig(resolution="4k")
        assert config.resolution == "4k"

    def test_video_config_invalid_resolution(self):
        """Test that invalid resolutions are rejected."""
        with pytest.raises(ValidationError):
            VideoConfig(resolution="480p")

    def test_video_config_fps_range(self):
        """Test that FPS must be within valid range."""
        with pytest.raises(ValidationError):
            VideoConfig(fps=0)

        with pytest.raises(ValidationError):
            VideoConfig(fps=120)


class TestAPIResponse:
    """Tests for APIResponse model."""

    def test_valid_success_response(self):
        """Test creating a valid success response."""
        response = APIResponse(success=True, data={"key": "value"})
        assert response.success is True
        assert response.data == {"key": "value"}
        assert response.error is None

    def test_valid_error_response(self):
        """Test creating a valid error response."""
        response = APIResponse(success=False, error="Something went wrong")
        assert response.success is False
        assert response.error == "Something went wrong"
        assert response.data is None

    def test_error_response_requires_error_message(self):
        """Test that error message is required when success is False."""
        with pytest.raises(ValidationError) as exc_info:
            APIResponse(success=False)
        assert "error message must be provided" in str(exc_info.value)

    def test_success_response_cannot_have_error(self):
        """Test that success response cannot have error message."""
        with pytest.raises(ValidationError) as exc_info:
            APIResponse(success=True, error="Error message")
        assert "should not be provided" in str(exc_info.value)

    def test_api_response_with_metadata(self):
        """Test APIResponse with metadata."""
        response = APIResponse(
            success=True, data={"result": "ok"}, metadata={"timestamp": "2025-10-10"}
        )
        assert response.metadata["timestamp"] == "2025-10-10"


class TestBatchRequest:
    """Tests for BatchRequest model."""

    def test_valid_batch_request(self):
        """Test creating a valid BatchRequest."""
        request = BatchRequest(items=[1, 2, 3, 4, 5])
        assert len(request.items) == 5
        assert request.batch_size == 10
        assert request.parallel is True

    def test_batch_request_empty_items(self):
        """Test that items list cannot be empty."""
        with pytest.raises(ValidationError):
            BatchRequest(items=[])

    def test_batch_request_serial_processing(self):
        """Test BatchRequest for serial processing."""
        request = BatchRequest(items=[1, 2, 3], parallel=False, max_workers=1)
        assert request.parallel is False
        assert request.max_workers == 1

    def test_batch_request_max_workers_validation(self):
        """Test that max_workers is validated with parallel flag."""
        with pytest.raises(ValidationError) as exc_info:
            BatchRequest(items=[1, 2, 3], parallel=False, max_workers=4)
        assert "max_workers should be 1 when parallel is False" in str(exc_info.value)

    def test_batch_request_custom_batch_size(self):
        """Test BatchRequest with custom batch size."""
        request = BatchRequest(items=list(range(100)), batch_size=25)
        assert request.batch_size == 25


class TestEnums:
    """Tests for enum types."""

    def test_target_gender_values(self):
        """Test TargetGender enum values."""
        assert TargetGender.WOMEN.value == "women"
        assert TargetGender.MEN.value == "men"

    def test_target_age_values(self):
        """Test TargetAge enum values."""
        assert TargetAge.AGE_10_13.value == "10-13"
        assert TargetAge.AGE_14_17.value == "14-17"
        assert TargetAge.AGE_18_23.value == "18-23"

    def test_content_source_values(self):
        """Test ContentSource enum values."""
        assert ContentSource.REDDIT.value == "reddit"
        assert ContentSource.INSTAGRAM.value == "instagram"
        assert ContentSource.TIKTOK.value == "tiktok"
        assert ContentSource.MANUAL.value == "manual"
        assert ContentSource.GENERATED.value == "generated"
