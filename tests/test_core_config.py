"""
Unit tests for core.config module.

Tests the centralized configuration management system including:
- Default value loading
- Environment variable loading
- Validation logic
- Path creation
- Helper methods
"""

import os
import pytest
import logging
from pathlib import Path
from unittest.mock import patch
from core.config import Settings, get_settings


class TestSettingsDefaults:
    """Test default configuration values."""
    
    def test_default_api_keys(self):
        """Test default API key values."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.openai_api_key == ""
            assert settings.elevenlabs_api_key == ""
            assert settings.reddit_client_id == ""
            assert settings.huggingface_token == ""
    
    def test_default_paths(self):
        """Test default path configuration."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.story_root == Path("./Stories")
            assert settings.data_root == Path("./data")
            assert settings.cache_dir == Path("./cache")
            assert settings.logs_dir == Path("./logs")
    
    def test_default_logging(self):
        """Test default logging configuration."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.log_level == "INFO"
            assert settings.log_format == "text"
            assert settings.log_to_file is True
    
    def test_default_performance(self):
        """Test default performance settings."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.max_workers == 4
            assert settings.retry_attempts == 3
            assert settings.timeout == 30
    
    def test_default_model_settings(self):
        """Test default model configuration."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.default_model == "gpt-4o-mini"
            assert settings.temperature == 0.9
            assert settings.max_tokens == 4000
    
    def test_default_voice_settings(self):
        """Test default voice configuration."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.voice_id == "BZgkqPqms7Kj9ulSkVzn"
            assert settings.voice_stability == 0.5
            assert settings.voice_similarity_boost == 0.75
    
    def test_default_environment(self):
        """Test default environment settings."""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.environment == "development"
            assert settings.debug is False


class TestSettingsEnvironmentVariables:
    """Test loading from environment variables."""
    
    def test_env_var_override(self):
        """Test environment variables override defaults."""
        test_env = {
            "OPENAI_API_KEY": "test-key-123",
            "LOG_LEVEL": "DEBUG",
            "MAX_WORKERS": "8",
            "TEMPERATURE": "0.7",
            "ENVIRONMENT": "production",
            "DEBUG": "true",
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.openai_api_key == "test-key-123"
            assert settings.log_level == "DEBUG"
            assert settings.max_workers == 8
            assert settings.temperature == 0.7
            assert settings.environment == "production"
            assert settings.debug is True
    
    def test_case_insensitive_env_vars(self):
        """Test environment variables are case-insensitive."""
        test_env = {
            "openai_api_key": "lowercase-key",
            "LOG_LEVEL": "warning",
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.openai_api_key == "lowercase-key"
            assert settings.log_level == "WARNING"
    
    def test_all_api_keys(self):
        """Test all API key environment variables."""
        test_env = {
            "OPENAI_API_KEY": "sk-openai-test",
            "ELEVENLABS_API_KEY": "el-test",
            "REDDIT_CLIENT_ID": "reddit-id",
            "REDDIT_CLIENT_SECRET": "reddit-secret",
            "REDDIT_USER_AGENT": "TestAgent/1.0",
            "HUGGINGFACE_TOKEN": "hf-token",
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.openai_api_key == "sk-openai-test"
            assert settings.elevenlabs_api_key == "el-test"
            assert settings.reddit_client_id == "reddit-id"
            assert settings.reddit_client_secret == "reddit-secret"
            assert settings.reddit_user_agent == "TestAgent/1.0"
            assert settings.huggingface_token == "hf-token"


class TestSettingsValidation:
    """Test configuration validation."""
    
    def test_log_level_validation(self):
        """Test log level validation and normalization."""
        # Valid log levels
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            test_env = {"LOG_LEVEL": level}
            with patch.dict(os.environ, test_env, clear=True):
                settings = Settings()
                assert settings.log_level == level
        
        # Lowercase should be normalized to uppercase
        test_env = {"LOG_LEVEL": "debug"}
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            assert settings.log_level == "DEBUG"
        
        # Invalid log level should default to INFO with warning
        with patch.dict(os.environ, {"LOG_LEVEL": "INVALID"}, clear=True):
            settings = Settings()
            assert settings.log_level == "INFO"
    
    def test_numeric_range_validation(self):
        """Test validation of numeric fields with ranges."""
        # Valid values
        test_env = {
            "MAX_WORKERS": "16",
            "RETRY_ATTEMPTS": "5",
            "TIMEOUT": "60",
            "TEMPERATURE": "1.5",
            "VOICE_STABILITY": "0.8",
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            assert settings.max_workers == 16
            assert settings.retry_attempts == 5
            assert settings.timeout == 60
            assert settings.temperature == 1.5
            assert settings.voice_stability == 0.8
        
        # Out of range values should raise validation error
        with pytest.raises(Exception):  # Pydantic ValidationError
            with patch.dict(os.environ, {"MAX_WORKERS": "0"}, clear=True):
                Settings()
        
        with pytest.raises(Exception):
            with patch.dict(os.environ, {"TEMPERATURE": "3.0"}, clear=True):
                Settings()
        
        with pytest.raises(Exception):
            with patch.dict(os.environ, {"MAX_WORKERS": "100"}, clear=True):
                Settings()
        
        with pytest.raises(Exception):
            with patch.dict(os.environ, {"VOICE_STABILITY": "1.5"}, clear=True):
                Settings()
    
    def test_path_handling(self):
        """Test path field handling."""
        test_env = {
            "STORY_ROOT": "/tmp/test_stories",
            "DATA_ROOT": "/tmp/test_data",
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.story_root == Path("/tmp/test_stories")
            assert settings.data_root == Path("/tmp/test_data")
            assert isinstance(settings.story_root, Path)
            assert isinstance(settings.data_root, Path)


class TestSettingsPathCreation:
    """Test that directories are created automatically."""
    
    def test_directory_creation(self, tmp_path):
        """Test that configured directories are created."""
        test_story_root = tmp_path / "stories"
        test_data_root = tmp_path / "data"
        test_cache_dir = tmp_path / "cache"
        test_logs_dir = tmp_path / "logs"
        
        test_env = {
            "STORY_ROOT": str(test_story_root),
            "DATA_ROOT": str(test_data_root),
            "CACHE_DIR": str(test_cache_dir),
            "LOGS_DIR": str(test_logs_dir),
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            # Directories should be created automatically
            assert test_story_root.exists()
            assert test_data_root.exists()
            assert test_cache_dir.exists()
            assert test_logs_dir.exists()


class TestSettingsHelperMethods:
    """Test helper methods."""
    
    def test_get_log_level_int(self):
        """Test get_log_level_int method."""
        test_cases = [
            ("DEBUG", logging.DEBUG),
            ("INFO", logging.INFO),
            ("WARNING", logging.WARNING),
            ("ERROR", logging.ERROR),
            ("CRITICAL", logging.CRITICAL),
        ]
        
        for level_str, expected_int in test_cases:
            with patch.dict(os.environ, {"LOG_LEVEL": level_str}, clear=True):
                settings = Settings()
                assert settings.get_log_level_int() == expected_int
    
    def test_environment_check_methods(self):
        """Test environment check methods."""
        # Production
        with patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=True):
            settings = Settings()
            assert settings.is_production() is True
            assert settings.is_development() is False
            assert settings.is_test() is False
        
        # Development
        with patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True):
            settings = Settings()
            assert settings.is_production() is False
            assert settings.is_development() is True
            assert settings.is_test() is False
        
        # Test
        with patch.dict(os.environ, {"ENVIRONMENT": "test"}, clear=True):
            settings = Settings()
            assert settings.is_production() is False
            assert settings.is_development() is False
            assert settings.is_test() is True


class TestSettingsSingleton:
    """Test singleton pattern."""
    
    def test_get_settings_function(self):
        """Test the get_settings function."""
        settings = get_settings()
        assert isinstance(settings, Settings)
        
        # Should return the same instance (singleton)
        settings2 = get_settings()
        assert settings is settings2


class TestSettingsIntegration:
    """Integration tests for full configuration."""
    
    def test_complete_configuration(self, tmp_path):
        """Test complete configuration with all settings."""
        test_env = {
            "OPENAI_API_KEY": "sk-test",
            "ELEVENLABS_API_KEY": "el-test",
            "REDDIT_CLIENT_ID": "reddit-id",
            "REDDIT_CLIENT_SECRET": "reddit-secret",
            "HUGGINGFACE_TOKEN": "hf-test",
            "DEFAULT_MODEL": "gpt-4",
            "TEMPERATURE": "0.7",
            "MAX_TOKENS": "2000",
            "STORY_ROOT": str(tmp_path / "stories"),
            "DATA_ROOT": str(tmp_path / "data"),
            "CACHE_DIR": str(tmp_path / "cache"),
            "LOGS_DIR": str(tmp_path / "logs"),
            "LOG_LEVEL": "DEBUG",
            "LOG_FORMAT": "json",
            "LOG_TO_FILE": "true",
            "MAX_WORKERS": "8",
            "RETRY_ATTEMPTS": "5",
            "TIMEOUT": "60",
            "VOICE_ID": "custom-voice",
            "VOICE_STABILITY": "0.8",
            "VOICE_SIMILARITY_BOOST": "0.9",
            "ENVIRONMENT": "production",
            "DEBUG": "true",
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            # API Keys
            assert settings.openai_api_key == "sk-test"
            assert settings.elevenlabs_api_key == "el-test"
            assert settings.reddit_client_id == "reddit-id"
            assert settings.reddit_client_secret == "reddit-secret"
            assert settings.huggingface_token == "hf-test"
            
            # Model settings
            assert settings.default_model == "gpt-4"
            assert settings.temperature == 0.7
            assert settings.max_tokens == 2000
            
            # Paths
            assert settings.story_root == tmp_path / "stories"
            assert settings.data_root == tmp_path / "data"
            assert settings.cache_dir == tmp_path / "cache"
            assert settings.logs_dir == tmp_path / "logs"
            
            # Logging
            assert settings.log_level == "DEBUG"
            assert settings.log_format == "json"
            assert settings.log_to_file is True
            
            # Performance
            assert settings.max_workers == 8
            assert settings.retry_attempts == 5
            assert settings.timeout == 60
            
            # Voice
            assert settings.voice_id == "custom-voice"
            assert settings.voice_stability == 0.8
            assert settings.voice_similarity_boost == 0.9
            
            # Environment
            assert settings.environment == "production"
            assert settings.debug is True
            
            # Directories should exist
            assert (tmp_path / "stories").exists()
            assert (tmp_path / "data").exists()
            assert (tmp_path / "cache").exists()
            assert (tmp_path / "logs").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
