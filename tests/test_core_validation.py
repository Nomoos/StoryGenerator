"""Tests for core.validation module."""

import pytest
from pydantic import ValidationError

from core.models import APIResponse, ScriptConfig, StoryIdea
from core.validation import (get_validation_errors, is_valid, validate_call,
                             validate_dict, validate_input, validate_output)


class TestValidateInput:
    """Tests for validate_input decorator."""

    def test_validate_input_with_valid_data(self):
        """Test validate_input with valid input data."""

        @validate_input(idea=StoryIdea)
        def process_idea(idea):
            return idea.content

        data = {
            "id": "test-123",
            "content": "This is valid story content",
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        result = process_idea(data)
        assert result == "This is valid story content"

    def test_validate_input_with_model_instance(self):
        """Test validate_input when input is already a model instance."""

        @validate_input(idea=StoryIdea)
        def process_idea(idea):
            return idea.content

        idea = StoryIdea(
            id="test",
            content="Story content",
            target_gender="women",
            target_age="18-23",
            source="reddit",
        )
        result = process_idea(idea)
        assert result == "Story content"

    def test_validate_input_with_invalid_data(self):
        """Test validate_input with invalid input data."""

        @validate_input(idea=StoryIdea)
        def process_idea(idea):
            return idea.content

        data = {
            "id": "test",
            "content": "Short",  # Too short
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        with pytest.raises(ValidationError):
            process_idea(data)

    def test_validate_input_multiple_parameters(self):
        """Test validate_input with multiple parameters."""

        @validate_input(idea=StoryIdea, config=ScriptConfig)
        def generate_script(idea, config):
            return f"{idea.content[:20]}... ({config.min_words}-{config.max_words} words)"

        idea_data = {
            "id": "test",
            "content": "This is the story content for testing",
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        config_data = {"min_words": 300, "max_words": 400}

        result = generate_script(idea_data, config_data)
        assert "300-400 words" in result

    def test_validate_input_with_kwargs(self):
        """Test validate_input with keyword arguments."""

        @validate_input(config=ScriptConfig)
        def create_script(title, config):
            return f"{title}: {config.min_words}-{config.max_words}"

        result = create_script(title="Test Title", config={"min_words": 350, "max_words": 370})
        assert "350-370" in result

    def test_validate_input_invalid_parameter_name(self):
        """Test validate_input with invalid parameter name."""
        with pytest.raises(ValueError) as exc_info:

            @validate_input(nonexistent=StoryIdea)
            def process_idea(idea):
                return idea

        assert "not found in function signature" in str(exc_info.value)

    def test_validate_input_with_wrong_type(self):
        """Test validate_input with wrong input type."""

        @validate_input(idea=StoryIdea)
        def process_idea(idea):
            return idea

        with pytest.raises(ValueError) as exc_info:
            process_idea("not a dict or model")
        assert "must be a dict or" in str(exc_info.value)


class TestValidateOutput:
    """Tests for validate_output decorator."""

    def test_validate_output_with_valid_dict(self):
        """Test validate_output with valid output dictionary."""

        @validate_output(APIResponse)
        def get_response():
            return {"success": True, "data": {"key": "value"}}

        result = get_response()
        assert isinstance(result, APIResponse)
        assert result.success is True

    def test_validate_output_with_model_instance(self):
        """Test validate_output when output is already a model instance."""

        @validate_output(APIResponse)
        def get_response():
            return APIResponse(success=True, data={"key": "value"})

        result = get_response()
        assert isinstance(result, APIResponse)
        assert result.success is True

    def test_validate_output_with_invalid_dict(self):
        """Test validate_output with invalid output dictionary."""

        @validate_output(APIResponse)
        def get_response():
            return {"success": False}  # Missing required error message

        with pytest.raises(ValidationError):
            get_response()

    def test_validate_output_with_wrong_type(self):
        """Test validate_output with wrong output type."""

        @validate_output(APIResponse)
        def get_response():
            return "not a dict or model"

        with pytest.raises(ValueError) as exc_info:
            get_response()
        assert "must return a dict or" in str(exc_info.value)


class TestValidateCall:
    """Tests for validate_call decorator."""

    def test_validate_call_with_parameters(self):
        """Test validate_call with input validation."""

        @validate_call(idea=StoryIdea)
        def process_idea(idea):
            return {"success": True, "data": {"content": idea.content}}

        data = {
            "id": "test",
            "content": "Story content here",
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        result = process_idea(data)
        assert result["success"] is True

    def test_validate_call_without_parameters(self):
        """Test validate_call without parameters."""

        @validate_call
        def simple_function(x, y):
            return x + y

        result = simple_function(2, 3)
        assert result == 5


class TestValidateDict:
    """Tests for validate_dict function."""

    def test_validate_dict_with_valid_data(self):
        """Test validate_dict with valid data."""
        data = {
            "id": "test",
            "content": "Valid story content",
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        result = validate_dict(data, StoryIdea)
        assert isinstance(result, StoryIdea)
        assert result.content == "Valid story content"

    def test_validate_dict_with_invalid_data(self):
        """Test validate_dict with invalid data."""
        data = {
            "id": "test",
            "content": "Short",
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        with pytest.raises(ValidationError):
            validate_dict(data, StoryIdea)


class TestGetValidationErrors:
    """Tests for get_validation_errors function."""

    def test_get_validation_errors_with_valid_data(self):
        """Test get_validation_errors with valid data returns None."""
        data = {
            "id": "test",
            "content": "Valid story content",
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        errors = get_validation_errors(data, StoryIdea)
        assert errors is None

    def test_get_validation_errors_with_invalid_data(self):
        """Test get_validation_errors with invalid data returns formatted string."""
        data = {
            "id": "test",
            "content": "Short",  # Too short
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        errors = get_validation_errors(data, StoryIdea)
        assert errors is not None
        assert "Validation error" in errors
        assert "content" in errors

    def test_get_validation_errors_multiple_errors(self):
        """Test get_validation_errors with multiple validation errors."""
        data = {
            "id": "",  # Empty
            "content": "Short",  # Too short
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        errors = get_validation_errors(data, StoryIdea)
        assert errors is not None
        assert "id" in errors or "content" in errors


class TestIsValid:
    """Tests for is_valid function."""

    def test_is_valid_with_valid_data(self):
        """Test is_valid returns True for valid data."""
        data = {
            "id": "test",
            "content": "Valid story content",
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        assert is_valid(data, StoryIdea) is True

    def test_is_valid_with_invalid_data(self):
        """Test is_valid returns False for invalid data."""
        data = {
            "id": "test",
            "content": "Short",  # Too short
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        assert is_valid(data, StoryIdea) is False

    def test_is_valid_with_missing_required_field(self):
        """Test is_valid returns False when required field is missing."""
        data = {
            "id": "test",
            # Missing content
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }
        assert is_valid(data, StoryIdea) is False


class TestComplexValidationScenarios:
    """Tests for complex validation scenarios."""

    def test_nested_validation(self):
        """Test validation with nested function calls."""

        @validate_input(config=ScriptConfig)
        def create_config(config):
            return config

        @validate_input(idea=StoryIdea)
        def generate_with_config(idea, script_config):
            return f"{idea.content} | {script_config.min_words}"

        config_data = {"min_words": 300, "max_words": 400}
        idea_data = {
            "id": "test",
            "content": "Story content here",
            "target_gender": "women",
            "target_age": "18-23",
            "source": "reddit",
        }

        config = create_config(config_data)
        result = generate_with_config(idea_data, config)
        assert "Story content here | 300" in result

    def test_validation_with_defaults(self):
        """Test validation preserves default values."""

        @validate_input(config=ScriptConfig)
        def process_config(config, multiplier=2):
            return config.min_words * multiplier

        result = process_config({})  # Uses all defaults
        assert result == 350 * 2

    def test_validation_error_messages(self):
        """Test that validation errors have clear messages."""

        @validate_input(idea=StoryIdea)
        def process_idea(idea):
            return idea

        invalid_data = {
            "id": "test@invalid",
            "content": "Short",
            "target_gender": "invalid_gender",
            "target_age": "18-23",
            "source": "reddit",
        }

        with pytest.raises(ValidationError) as exc_info:
            process_idea(invalid_data)

        error_str = str(exc_info.value)
        # Should contain information about multiple validation errors
        assert "validation" in error_str.lower()
