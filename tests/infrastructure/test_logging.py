"""
Tests for logging system.

Tests the structured logging system including:
- Console and file handlers
- JSON formatting
- Log levels
- Context managers
- Request ID tracking
"""

import json
import logging
from pathlib import Path

import pytest

from src.Python.logging import get_logger, setup_logging
from src.Python.logging.logger import LoggerContext


class TestLoggingSetup:
    """Test logging setup function."""
    
    def test_setup_logging_default(self, tmp_path):
        """Test default logging setup."""
        logger = setup_logging(log_dir=tmp_path)
        assert logger.level == logging.INFO
        assert len(logger.handlers) >= 1
    
    def test_setup_logging_with_level(self, tmp_path):
        """Test logging setup with custom level."""
        logger = setup_logging(level="DEBUG", log_dir=tmp_path)
        assert logger.level == logging.DEBUG
    
    def test_setup_logging_console_only(self, tmp_path):
        """Test logging with console output only."""
        logger = setup_logging(
            log_dir=tmp_path,
            console_output=True,
            file_output=False
        )
        # Should have at least console handler
        assert len(logger.handlers) >= 1
    
    def test_setup_logging_file_only(self, tmp_path):
        """Test logging with file output only."""
        logger = setup_logging(
            log_dir=tmp_path,
            console_output=False,
            file_output=True
        )
        # Should have at least file handler
        assert len(logger.handlers) >= 1
    
    def test_setup_logging_creates_log_dir(self, tmp_path):
        """Test that log directory is created."""
        log_dir = tmp_path / "test_logs"
        assert not log_dir.exists()
        
        setup_logging(log_dir=log_dir, console_output=False)
        
        assert log_dir.exists()
        assert (log_dir / "app.log").exists()


class TestLoggingOutput:
    """Test logging output to files and console."""
    
    def test_log_to_file(self, tmp_path):
        """Test that logs are written to file."""
        log_dir = tmp_path / "logs"
        setup_logging(level="INFO", log_dir=log_dir, console_output=False)
        
        logger = get_logger(__name__)
        logger.info("Test message")
        
        log_file = log_dir / "app.log"
        assert log_file.exists()
        
        content = log_file.read_text()
        assert "Test message" in content
        assert "INFO" in content
    
    def test_log_levels(self, tmp_path):
        """Test different log levels."""
        log_dir = tmp_path / "logs"
        setup_logging(level="DEBUG", log_dir=log_dir, console_output=False)
        
        logger = get_logger(__name__)
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        content = (log_dir / "app.log").read_text()
        assert "Debug message" in content
        assert "Info message" in content
        assert "Warning message" in content
        assert "Error message" in content
        assert "Critical message" in content
    
    def test_log_level_filtering(self, tmp_path):
        """Test that log level filters messages."""
        log_dir = tmp_path / "logs"
        setup_logging(level="WARNING", log_dir=log_dir, console_output=False)
        
        logger = get_logger(__name__)
        logger.debug("Should not appear")
        logger.info("Should not appear")
        logger.warning("Should appear")
        logger.error("Should appear")
        
        content = (log_dir / "app.log").read_text()
        assert "Should not appear" not in content
        assert "Should appear" in content


class TestLoggingJSON:
    """Test JSON logging format."""
    
    def test_json_format(self, tmp_path):
        """Test JSON formatted logs."""
        log_dir = tmp_path / "logs"
        setup_logging(
            level="INFO",
            log_dir=log_dir,
            json_format=True,
            console_output=False
        )
        
        logger = get_logger(__name__)
        logger.info("Test JSON message")
        
        log_file = log_dir / "app.log"
        content = log_file.read_text()
        
        # Parse the JSON log line
        log_lines = [line for line in content.strip().split('\n') if line]
        if log_lines:
            log_data = json.loads(log_lines[0])
            assert log_data['message'] == "Test JSON message"
            assert log_data['level'] == "INFO"
            assert 'timestamp' in log_data


class TestGetLogger:
    """Test get_logger function."""
    
    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger instance."""
        logger = get_logger(__name__)
        assert isinstance(logger, logging.Logger)
    
    def test_get_logger_with_name(self):
        """Test logger has correct name."""
        logger = get_logger("test.module")
        assert logger.name == "test.module"
    
    def test_multiple_loggers(self):
        """Test getting multiple loggers."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        assert logger1.name == "module1"
        assert logger2.name == "module2"
        assert logger1 is not logger2


class TestLoggerContext:
    """Test LoggerContext for contextual logging."""
    
    def test_logger_context_basic(self, tmp_path):
        """Test basic logger context usage."""
        log_dir = tmp_path / "logs"
        setup_logging(level="INFO", log_dir=log_dir, console_output=False)
        
        logger = get_logger(__name__)
        
        with LoggerContext(logger, request_id="req-123"):
            logger.info("Test message")
        
        # Context manager should complete without error
        assert True
    
    def test_logger_context_restores_factory(self):
        """Test that context manager restores log record factory."""
        logger = get_logger(__name__)
        old_factory = logging.getLogRecordFactory()
        
        with LoggerContext(logger, test_key="test_value"):
            pass
        
        # Factory should be restored
        assert logging.getLogRecordFactory() == old_factory


class TestLoggingIntegration:
    """Integration tests for logging system."""
    
    def test_complete_logging_workflow(self, tmp_path):
        """Test complete logging workflow."""
        log_dir = tmp_path / "logs"
        
        # Setup logging
        setup_logging(
            level="DEBUG",
            log_dir=log_dir,
            console_output=True,
            file_output=True,
            json_format=False
        )
        
        # Get logger and log messages
        logger = get_logger("test.integration")
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        # Verify log file
        log_file = log_dir / "app.log"
        assert log_file.exists()
        
        content = log_file.read_text()
        assert "Debug message" in content
        assert "Info message" in content
        assert "Warning message" in content
        assert "Error message" in content
        assert "test.integration" in content
    
    def test_logging_with_request_id(self, tmp_path):
        """Test logging with request ID tracking."""
        log_dir = tmp_path / "logs"
        
        setup_logging(
            level="INFO",
            log_dir=log_dir,
            request_id="req-456",
            console_output=False
        )
        
        logger = get_logger(__name__)
        logger.info("Request message")
        
        content = (log_dir / "app.log").read_text()
        assert "req-456" in content
        assert "Request message" in content
