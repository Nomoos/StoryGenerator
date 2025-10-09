"""
Tests for configuration management system.

Tests the pydantic-settings based configuration system including:
- Loading from environment variables
- Validation of configuration values
- Type safety
- Default values
- Path creation
"""

import os
from pathlib import Path

import pytest

from src.Python.config import Settings, get_settings, reload_settings


class TestSettingsDefaults:
    """Test default configuration values."""
    
    def test_default_model_settings(self):
        """Test default model configuration."""
        settings = Settings()
        assert settings.default_model == "gpt-4o-mini"
        assert settings.temperature == 0.9
        assert settings.max_tokens == 4000
    
    def test_default_paths(self):
        """Test default path configuration."""
        settings = Settings()
        assert settings.story_root == Path("./Stories")
        assert settings.log_dir == Path("./logs")
        assert settings.cache_dir == Path("./cache")
    
    def test_default_log_level(self):
        """Test default log level."""
        settings = Settings()
        assert settings.log_level == "INFO"
    
    def test_default_performance_settings(self):
        """Test default performance settings."""
        settings = Settings()
        assert settings.enable_cache is True
        assert settings.max_retries == 3


class TestSettingsValidation:
    """Test configuration validation."""
    
    def test_log_level_validation_valid(self):
        """Test valid log level values."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        for level in valid_levels:
            settings = Settings(log_level=level)
            assert settings.log_level == level
    
    def test_log_level_validation_case_insensitive(self):
        """Test log level is case insensitive."""
        settings = Settings(log_level='debug')
        assert settings.log_level == 'DEBUG'
        
        settings = Settings(log_level='Info')
        assert settings.log_level == 'INFO'
    
    def test_log_level_validation_invalid(self):
        """Test invalid log level raises error."""
        with pytest.raises(ValueError, match="log_level must be one of"):
            Settings(log_level='INVALID')
    
    def test_temperature_validation(self):
        """Test temperature must be between 0 and 2."""
        # Valid values
        Settings(temperature=0.0)
        Settings(temperature=1.0)
        Settings(temperature=2.0)
        
        # Invalid values
        with pytest.raises(ValueError):
            Settings(temperature=-0.1)
        
        with pytest.raises(ValueError):
            Settings(temperature=2.1)
    
    def test_max_tokens_validation(self):
        """Test max_tokens must be positive."""
        Settings(max_tokens=1)
        Settings(max_tokens=1000)
        
        with pytest.raises(ValueError):
            Settings(max_tokens=0)
        
        with pytest.raises(ValueError):
            Settings(max_tokens=-1)
    
    def test_max_retries_validation(self):
        """Test max_retries must be positive."""
        Settings(max_retries=1)
        Settings(max_retries=10)
        
        with pytest.raises(ValueError):
            Settings(max_retries=0)


class TestSettingsEnvironmentVariables:
    """Test configuration from environment variables."""
    
    def test_env_var_override(self, monkeypatch, tmp_path):
        """Test environment variables override defaults."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-123")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("TEMPERATURE", "0.5")
        monkeypatch.setenv("STORY_ROOT", str(tmp_path / "stories"))
        
        settings = Settings()
        
        assert settings.openai_api_key == "test-key-123"
        assert settings.log_level == "DEBUG"
        assert settings.temperature == 0.5
        assert settings.story_root == tmp_path / "stories"
    
    def test_optional_env_vars(self, monkeypatch):
        """Test optional environment variables."""
        monkeypatch.setenv("HUGGINGFACE_TOKEN", "hf_token")
        monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0,1")
        
        settings = Settings()
        
        assert settings.huggingface_token == "hf_token"
        assert settings.cuda_visible_devices == "0,1"
    
    def test_boolean_env_vars(self, monkeypatch):
        """Test boolean environment variables."""
        monkeypatch.setenv("ENABLE_CACHE", "false")
        monkeypatch.setenv("DEBUG", "true")
        
        settings = Settings()
        
        assert settings.enable_cache is False
        assert settings.debug is True


class TestSettingsPathCreation:
    """Test that paths are created automatically."""
    
    def test_paths_are_created(self, tmp_path, monkeypatch):
        """Test that directories are created on initialization."""
        story_dir = tmp_path / "test_stories"
        log_dir = tmp_path / "test_logs"
        cache_dir = tmp_path / "test_cache"
        
        # Ensure they don't exist yet
        assert not story_dir.exists()
        assert not log_dir.exists()
        assert not cache_dir.exists()
        
        monkeypatch.setenv("STORY_ROOT", str(story_dir))
        monkeypatch.setenv("LOG_DIR", str(log_dir))
        monkeypatch.setenv("CACHE_DIR", str(cache_dir))
        
        settings = Settings()
        
        # They should be created now
        assert settings.story_root.exists()
        assert settings.log_dir.exists()
        assert settings.cache_dir.exists()


class TestSettingsSingleton:
    """Test singleton pattern for settings."""
    
    def test_get_settings_returns_same_instance(self):
        """Test get_settings returns singleton."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2
    
    def test_reload_settings_creates_new_instance(self, monkeypatch):
        """Test reload_settings creates new instance."""
        settings1 = get_settings()
        
        # Change environment and reload
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        settings2 = reload_settings()
        
        assert settings1 is not settings2
        assert settings2.log_level == "DEBUG"


class TestSettingsIntegration:
    """Integration tests for settings system."""
    
    def test_complete_configuration(self, monkeypatch, tmp_path):
        """Test complete configuration with all settings."""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        monkeypatch.setenv("ELEVENLABS_API_KEY", "el-test")
        monkeypatch.setenv("DEFAULT_MODEL", "gpt-4")
        monkeypatch.setenv("TEMPERATURE", "0.7")
        monkeypatch.setenv("MAX_TOKENS", "2000")
        monkeypatch.setenv("STORY_ROOT", str(tmp_path / "stories"))
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("ENABLE_CACHE", "true")
        monkeypatch.setenv("MAX_RETRIES", "5")
        
        settings = Settings()
        
        assert settings.openai_api_key == "sk-test"
        assert settings.elevenlabs_api_key == "el-test"
        assert settings.default_model == "gpt-4"
        assert settings.temperature == 0.7
        assert settings.max_tokens == 2000
        assert settings.story_root == tmp_path / "stories"
        assert settings.log_level == "DEBUG"
        assert settings.enable_cache is True
        assert settings.max_retries == 5
