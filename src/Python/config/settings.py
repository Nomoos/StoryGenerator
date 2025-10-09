"""
Configuration management using pydantic-settings.

Loads configuration from environment variables and .env files.
Provides type-safe access to configuration values with validation.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation and environment variable support.
    
    All settings can be overridden via environment variables.
    Environment variables take precedence over .env file values.
    
    Example:
        >>> settings = get_settings()
        >>> print(settings.openai_api_key)
        >>> print(settings.story_root)
    """
    
    # API Keys
    openai_api_key: str = Field(
        default="",
        description="OpenAI API key for GPT models"
    )
    elevenlabs_api_key: str = Field(
        default="",
        description="ElevenLabs API key for voice synthesis"
    )
    huggingface_token: Optional[str] = Field(
        default=None,
        description="HuggingFace token for private models"
    )
    reddit_client_id: Optional[str] = Field(
        default=None,
        description="Reddit API client ID"
    )
    reddit_client_secret: Optional[str] = Field(
        default=None,
        description="Reddit API client secret"
    )
    
    # Model Settings
    default_model: str = Field(
        default="gpt-4o-mini",
        description="Default OpenAI model to use"
    )
    temperature: float = Field(
        default=0.9,
        ge=0.0,
        le=2.0,
        description="Model temperature for generation"
    )
    max_tokens: int = Field(
        default=4000,
        gt=0,
        description="Maximum tokens for model generation"
    )
    
    # Storage Configuration
    story_root: Path = Field(
        default=Path("./Stories"),
        description="Root directory for story storage"
    )
    log_dir: Path = Field(
        default=Path("./logs"),
        description="Directory for log files"
    )
    cache_dir: Path = Field(
        default=Path("./cache"),
        description="Directory for cache files"
    )
    
    # Voice Settings
    voice_id: str = Field(
        default="BZgkqPqms7Kj9ulSkVzn",
        description="ElevenLabs voice ID"
    )
    voice_model: str = Field(
        default="eleven_v3",
        description="ElevenLabs voice model"
    )
    voice_style: str = Field(
        default="Creative",
        description="ElevenLabs voice style"
    )
    
    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    
    # Performance
    enable_cache: bool = Field(
        default=True,
        description="Enable caching"
    )
    max_retries: int = Field(
        default=3,
        gt=0,
        description="Maximum retry attempts for API calls"
    )
    
    # Optional GPU settings
    cuda_visible_devices: Optional[str] = Field(
        default=None,
        description="GPU device ID(s) to use"
    )
    
    # Debug mode
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )
    
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the allowed values."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}, got '{v}'")
        return v_upper
    
    @field_validator('story_root', 'log_dir', 'cache_dir')
    @classmethod
    def ensure_path_exists(cls, v: Path) -> Path:
        """Ensure directory paths exist, create if they don't."""
        v.mkdir(parents=True, exist_ok=True)
        return v


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the singleton settings instance.
    
    Returns:
        Settings: The application settings instance
        
    Example:
        >>> settings = get_settings()
        >>> print(settings.openai_api_key)
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """Reload settings from environment/files.
    
    Useful for testing or when configuration changes.
    
    Returns:
        Settings: The reloaded settings instance
    """
    global _settings
    _settings = Settings()
    return _settings
