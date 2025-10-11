"""
Configuration management system using Pydantic Settings.

This module provides centralized, type-safe configuration management for the
application. It loads settings from environment variables and .env files with
automatic validation and type conversion.

Example:
    >>> from PrismQ.Shared.config import settings
    >>> print(settings.openai_api_key)
    >>> print(settings.story_root)
"""

import logging
import os
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Application settings with type-safe access and validation.

    Settings are loaded from environment variables and .env files.
    All paths are automatically created if they don't exist.

    Configuration sources (in order of precedence):
    1. Environment variables
    2. .env file in the project root
    3. Default values defined here
    """

    # ============================================
    # API Keys
    # ============================================
    openai_api_key: str = Field(default="", description="OpenAI API key for GPT models")

    elevenlabs_api_key: str = Field(
        default="", description="ElevenLabs API key for voice synthesis"
    )

    reddit_client_id: str = Field(default="", description="Reddit API client ID")

    reddit_client_secret: str = Field(default="", description="Reddit API client secret")

    reddit_user_agent: str = Field(
        default="StoryGenerator/1.0", description="Reddit API user agent"
    )

    huggingface_token: str = Field(default="", description="HuggingFace token for model access")

    # ============================================
    # Paths
    # ============================================
    story_root: Path = Field(
        default=Path("./Stories"), description="Root directory for story storage"
    )

    data_root: Path = Field(default=Path("./data"), description="Root directory for data storage")

    cache_dir: Path = Field(default=Path("./cache"), description="Directory for cached data")

    logs_dir: Path = Field(default=Path("./logs"), description="Directory for log files")

    # ============================================
    # Logging Configuration
    # ============================================
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )

    log_format: Literal["json", "text"] = Field(default="text", description="Log output format")

    log_to_file: bool = Field(default=True, description="Whether to write logs to file")

    # ============================================
    # Performance Settings
    # ============================================
    max_workers: int = Field(default=4, ge=1, le=32, description="Maximum number of worker threads")

    retry_attempts: int = Field(
        default=3, ge=1, le=10, description="Number of retry attempts for failed operations"
    )

    timeout: int = Field(default=30, ge=1, le=300, description="Request timeout in seconds")

    # ============================================
    # Model Settings
    # ============================================
    default_model: str = Field(default="gpt-4o-mini", description="Default OpenAI model to use")

    temperature: float = Field(
        default=0.9, ge=0.0, le=2.0, description="Model temperature for text generation"
    )

    max_tokens: int = Field(
        default=4000, ge=1, le=128000, description="Maximum tokens for model responses"
    )

    # ============================================
    # Voice Settings
    # ============================================
    voice_id: str = Field(default="BZgkqPqms7Kj9ulSkVzn", description="Default ElevenLabs voice ID")

    voice_stability: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Voice stability setting"
    )

    voice_similarity_boost: float = Field(
        default=0.75, ge=0.0, le=1.0, description="Voice similarity boost setting"
    )

    # ============================================
    # Environment
    # ============================================
    environment: Literal["development", "production", "test"] = Field(
        default="development", description="Application environment"
    )

    debug: bool = Field(default=False, description="Enable debug mode")

    # ============================================
    # Pydantic Settings Configuration
    # ============================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra env vars
    )

    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate and normalize log level."""
        if isinstance(v, str):
            v = v.upper()
            if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
                logger.warning(f"Invalid log level '{v}', defaulting to INFO")
                return "INFO"
        return v

    @model_validator(mode="after")
    def create_directories(self) -> "Settings":
        """Create all configured directories if they don't exist."""
        directories = [
            self.story_root,
            self.data_root,
            self.cache_dir,
            self.logs_dir,
        ]

        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Ensured directory exists: {directory}")
            except Exception as e:
                logger.warning(f"Failed to create directory {directory}: {e}")

        return self

    def get_log_level_int(self) -> int:
        """Get numeric log level for Python logging."""
        return getattr(logging, self.log_level)

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"

    def is_test(self) -> bool:
        """Check if running in test environment."""
        return self.environment == "test"


# Singleton instance - import this to access settings throughout the application
settings = Settings()


def get_settings() -> Settings:
    """
    Get the global settings instance.

    This function is useful for dependency injection and testing,
    allowing you to override settings in tests.

    Returns:
        Settings: The global settings instance
    """
    return settings


# Log the configuration on module import (excluding sensitive data)
if __name__ != "__main__":
    logger.info(f"Configuration loaded - Environment: {settings.environment}")
    logger.debug(f"Log level: {settings.log_level}")
    logger.debug(f"Story root: {settings.story_root}")
    logger.debug(f"Data root: {settings.data_root}")
