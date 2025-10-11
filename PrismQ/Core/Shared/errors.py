"""
Custom exception hierarchy for StoryGenerator.

This module defines a comprehensive exception hierarchy for handling
various error scenarios in the StoryGenerator application.
"""

from typing import Any, Dict, Optional


class StoryGeneratorError(Exception):
    """Base exception for all StoryGenerator errors.
    
    All custom exceptions in the application should inherit from this class.
    This allows catching all application-specific errors with a single except clause.
    
    Attributes:
        message: Human-readable error message
        details: Optional dictionary with additional error context
        original_error: Optional original exception that caused this error
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None,
    ):
        """Initialize StoryGeneratorError.
        
        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
            original_error: Optional original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.original_error = original_error

    def __str__(self) -> str:
        """Return string representation of the error."""
        base_msg = self.message
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            base_msg += f" ({details_str})"
        if self.original_error:
            base_msg += f" | Original: {str(self.original_error)}"
        return base_msg

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging/serialization.
        
        Returns:
            Dictionary representation of the error
        """
        result = {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
        }
        if self.original_error:
            result["original_error"] = str(self.original_error)
        return result


class ValidationError(StoryGeneratorError):
    """Input validation failures.
    
    Raised when input data doesn't meet validation requirements.
    Examples: invalid types, out-of-range values, missing required fields.
    """

    pass


class APIError(StoryGeneratorError):
    """API call failures.
    
    Raised when external API calls fail (OpenAI, ElevenLabs, etc.).
    Includes HTTP errors, timeouts, rate limits, and authentication issues.
    
    Attributes:
        status_code: HTTP status code if applicable
        retry_after: Seconds to wait before retrying (for rate limits)
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None,
        status_code: Optional[int] = None,
        retry_after: Optional[int] = None,
    ):
        """Initialize APIError.
        
        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
            original_error: Optional original exception that caused this error
            status_code: HTTP status code if applicable
            retry_after: Seconds to wait before retrying
        """
        super().__init__(message, details, original_error)
        self.status_code = status_code
        self.retry_after = retry_after

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        result = super().to_dict()
        if self.status_code:
            result["status_code"] = self.status_code
        if self.retry_after:
            result["retry_after"] = self.retry_after
        return result


class ProcessingError(StoryGeneratorError):
    """Processing pipeline failures.
    
    Raised when data processing or transformation fails.
    Examples: script generation errors, image processing failures.
    
    Attributes:
        stage: Pipeline stage where error occurred
        item_id: ID of the item being processed
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None,
        stage: Optional[str] = None,
        item_id: Optional[str] = None,
    ):
        """Initialize ProcessingError.
        
        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
            original_error: Optional original exception that caused this error
            stage: Pipeline stage where error occurred
            item_id: ID of the item being processed
        """
        super().__init__(message, details, original_error)
        self.stage = stage
        self.item_id = item_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        result = super().to_dict()
        if self.stage:
            result["stage"] = self.stage
        if self.item_id:
            result["item_id"] = self.item_id
        return result


class ConfigurationError(StoryGeneratorError):
    """Configuration-related errors.
    
    Raised when configuration is invalid or missing.
    Examples: missing API keys, invalid file paths, bad settings.
    """

    pass


class ResourceError(StoryGeneratorError):
    """Resource-related errors.
    
    Raised when resources (files, memory, disk space) are unavailable.
    Examples: file not found, out of disk space, memory exhausted.
    """

    pass


class TimeoutError(StoryGeneratorError):
    """Operation timeout errors.
    
    Raised when an operation exceeds its time limit.
    """

    pass


class RateLimitError(APIError):
    """Rate limit exceeded errors.
    
    Raised when API rate limits are exceeded.
    Should include retry_after if provided by the API.
    """

    pass


class AuthenticationError(APIError):
    """Authentication/authorization errors.
    
    Raised when API authentication fails.
    Examples: invalid API key, expired token, insufficient permissions.
    """

    pass
