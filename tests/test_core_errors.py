"""
Tests for core.errors module - custom exception hierarchy.
"""

import pytest

from core.errors import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    ProcessingError,
    RateLimitError,
    ResourceError,
    StoryGeneratorError,
    TimeoutError,
    ValidationError,
)


class TestStoryGeneratorError:
    """Test base StoryGeneratorError exception."""

    def test_basic_error(self):
        """Test basic error creation."""
        error = StoryGeneratorError("Test error")
        assert error.message == "Test error"
        assert error.details == {}
        assert error.original_error is None
        assert str(error) == "Test error"

    def test_error_with_details(self):
        """Test error with details dictionary."""
        error = StoryGeneratorError(
            "Test error", details={"key": "value", "count": 42}
        )
        assert error.details == {"key": "value", "count": 42}
        assert "key=value" in str(error)
        assert "count=42" in str(error)

    def test_error_with_original_exception(self):
        """Test error with original exception."""
        original = ValueError("Original error")
        error = StoryGeneratorError("Wrapped error", original_error=original)
        assert error.original_error is original
        assert "Original: Original error" in str(error)

    def test_error_to_dict(self):
        """Test error serialization to dictionary."""
        original = ValueError("Original")
        error = StoryGeneratorError(
            "Test error",
            details={"key": "value"},
            original_error=original,
        )
        result = error.to_dict()
        
        assert result["error_type"] == "StoryGeneratorError"
        assert result["message"] == "Test error"
        assert result["details"] == {"key": "value"}
        assert "Original" in result["original_error"]


class TestValidationError:
    """Test ValidationError exception."""

    def test_validation_error(self):
        """Test validation error."""
        error = ValidationError("Invalid input")
        assert isinstance(error, StoryGeneratorError)
        assert error.message == "Invalid input"

    def test_validation_error_with_details(self):
        """Test validation error with field details."""
        error = ValidationError(
            "Validation failed",
            details={"field": "email", "reason": "invalid format"},
        )
        assert error.details["field"] == "email"
        assert error.details["reason"] == "invalid format"


class TestAPIError:
    """Test APIError exception."""

    def test_basic_api_error(self):
        """Test basic API error."""
        error = APIError("API call failed")
        assert isinstance(error, StoryGeneratorError)
        assert error.message == "API call failed"
        assert error.status_code is None
        assert error.retry_after is None

    def test_api_error_with_status_code(self):
        """Test API error with HTTP status code."""
        error = APIError("Server error", status_code=500)
        assert error.status_code == 500
        result = error.to_dict()
        assert result["status_code"] == 500

    def test_api_error_with_retry_after(self):
        """Test API error with retry_after."""
        error = APIError("Rate limited", retry_after=60)
        assert error.retry_after == 60
        result = error.to_dict()
        assert result["retry_after"] == 60

    def test_api_error_complete(self):
        """Test API error with all fields."""
        original = ConnectionError("Connection failed")
        error = APIError(
            "API unavailable",
            details={"endpoint": "/v1/completions"},
            original_error=original,
            status_code=503,
            retry_after=30,
        )
        
        assert error.status_code == 503
        assert error.retry_after == 30
        result = error.to_dict()
        assert result["status_code"] == 503
        assert result["retry_after"] == 30
        assert "endpoint" in result["details"]


class TestProcessingError:
    """Test ProcessingError exception."""

    def test_basic_processing_error(self):
        """Test basic processing error."""
        error = ProcessingError("Processing failed")
        assert isinstance(error, StoryGeneratorError)
        assert error.message == "Processing failed"
        assert error.stage is None
        assert error.item_id is None

    def test_processing_error_with_stage(self):
        """Test processing error with stage."""
        error = ProcessingError("Failed at stage", stage="script_generation")
        assert error.stage == "script_generation"
        result = error.to_dict()
        assert result["stage"] == "script_generation"

    def test_processing_error_with_item_id(self):
        """Test processing error with item ID."""
        error = ProcessingError("Item failed", item_id="item-123")
        assert error.item_id == "item-123"
        result = error.to_dict()
        assert result["item_id"] == "item-123"

    def test_processing_error_complete(self):
        """Test processing error with all fields."""
        error = ProcessingError(
            "Script generation failed",
            details={"reason": "timeout"},
            stage="script_generation",
            item_id="story-456",
        )
        
        assert error.stage == "script_generation"
        assert error.item_id == "story-456"
        result = error.to_dict()
        assert result["stage"] == "script_generation"
        assert result["item_id"] == "story-456"
        assert result["details"]["reason"] == "timeout"


class TestSpecializedErrors:
    """Test specialized error types."""

    def test_configuration_error(self):
        """Test configuration error."""
        error = ConfigurationError("Missing API key")
        assert isinstance(error, StoryGeneratorError)
        assert error.message == "Missing API key"

    def test_resource_error(self):
        """Test resource error."""
        error = ResourceError("File not found")
        assert isinstance(error, StoryGeneratorError)
        assert error.message == "File not found"

    def test_timeout_error(self):
        """Test timeout error."""
        error = TimeoutError("Operation timed out")
        assert isinstance(error, StoryGeneratorError)
        assert error.message == "Operation timed out"

    def test_rate_limit_error(self):
        """Test rate limit error."""
        error = RateLimitError("Rate limit exceeded", retry_after=120)
        assert isinstance(error, APIError)
        assert error.retry_after == 120

    def test_authentication_error(self):
        """Test authentication error."""
        error = AuthenticationError("Invalid API key", status_code=401)
        assert isinstance(error, APIError)
        assert error.status_code == 401


class TestErrorHierarchy:
    """Test exception hierarchy relationships."""

    def test_all_inherit_from_base(self):
        """Test that all custom errors inherit from StoryGeneratorError."""
        errors = [
            ValidationError("test"),
            APIError("test"),
            ProcessingError("test"),
            ConfigurationError("test"),
            ResourceError("test"),
            TimeoutError("test"),
            RateLimitError("test"),
            AuthenticationError("test"),
        ]
        
        for error in errors:
            assert isinstance(error, StoryGeneratorError)
            assert isinstance(error, Exception)

    def test_specialized_api_errors(self):
        """Test that specialized API errors inherit from APIError."""
        rate_limit = RateLimitError("test")
        auth_error = AuthenticationError("test")
        
        assert isinstance(rate_limit, APIError)
        assert isinstance(auth_error, APIError)

    def test_catch_base_exception(self):
        """Test catching all errors with base exception."""
        try:
            raise ValidationError("test")
        except StoryGeneratorError as e:
            assert e.message == "test"
        
        try:
            raise APIError("test")
        except StoryGeneratorError as e:
            assert e.message == "test"
