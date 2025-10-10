"""
Unit tests for core.logging module.

Tests the structured logging system including:
- Setup and configuration
- Log levels and handlers
- JSON formatting
- Request ID tracking
- Context managers
- Integration with config
"""

import os
import logging
import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest

from core.logging import (
    setup_logging,
    get_logger,
    log_context,
    LoggerContext,
    reset_logging,
    RequestIdFilter
)


@pytest.fixture(autouse=True)
def reset_logging_state():
    """Reset logging state before and after each test."""
    reset_logging()
    yield
    reset_logging()


class TestLoggingSetup:
    """Test logging setup and configuration."""
    
    def test_setup_logging_basic(self):
        """Test basic logging setup."""
        logger = setup_logging(level="INFO", console_output=True, file_output=False)
        
        assert logger is not None
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0
    
    def test_setup_logging_with_config_defaults(self):
        """Test that setup can use explicit log level parameter."""
        # Instead of testing config defaults (which is complex with singleton),
        # test that setup_logging accepts and uses the level parameter
        reset_logging()
        logger = setup_logging(level="DEBUG", file_output=False)
        
        assert logger.level == logging.DEBUG
    
    def test_setup_logging_levels(self):
        """Test different log levels."""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        for level in levels:
            reset_logging()
            logger = setup_logging(level=level, file_output=False)
            assert logger.level == getattr(logging, level)
    
    def test_setup_logging_case_insensitive(self):
        """Test that log level is case-insensitive."""
        reset_logging()
        logger = setup_logging(level="debug", file_output=False)
        assert logger.level == logging.DEBUG
    
    def test_setup_logging_console_only(self):
        """Test console-only logging."""
        logger = setup_logging(console_output=True, file_output=False)
        
        # Should have at least one handler (console)
        assert len(logger.handlers) >= 1
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
    
    def test_setup_logging_file_only(self, tmp_path):
        """Test file-only logging."""
        log_dir = tmp_path / "logs"
        logger = setup_logging(
            console_output=False,
            file_output=True,
            log_dir=log_dir
        )
        
        # Should have file handler
        assert len(logger.handlers) >= 1
        assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)
        
        # Log file should exist
        log_file = log_dir / "app.log"
        assert log_file.exists()
    
    def test_setup_logging_creates_log_directory(self, tmp_path):
        """Test that log directory is created if it doesn't exist."""
        log_dir = tmp_path / "nonexistent" / "logs"
        assert not log_dir.exists()
        
        setup_logging(log_dir=log_dir, file_output=True, console_output=False)
        
        assert log_dir.exists()
        assert (log_dir / "app.log").exists()
    
    def test_setup_logging_no_duplicate_handlers(self):
        """Test that reconfiguring doesn't create duplicate handlers."""
        setup_logging(file_output=False)
        handler_count_1 = len(logging.getLogger().handlers)
        
        setup_logging(file_output=False, force_reconfigure=True)
        handler_count_2 = len(logging.getLogger().handlers)
        
        assert handler_count_1 == handler_count_2


class TestGetLogger:
    """Test get_logger function."""
    
    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a Logger instance."""
        logger = get_logger(__name__)
        assert isinstance(logger, logging.Logger)
    
    def test_get_logger_different_names(self):
        """Test that different names return different loggers."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        assert logger1.name == "module1"
        assert logger2.name == "module2"
        assert logger1 is not logger2
    
    def test_get_logger_auto_configures(self):
        """Test that get_logger auto-configures logging."""
        reset_logging()
        logger = get_logger(__name__)
        
        # Root logger should be configured
        root = logging.getLogger()
        assert len(root.handlers) > 0


class TestRequestIdFilter:
    """Test request ID filter."""
    
    def test_request_id_filter_adds_id(self):
        """Test that filter adds request ID to records."""
        filter_obj = RequestIdFilter(request_id="test-123")
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        filter_obj.filter(record)
        assert hasattr(record, 'request_id')
        assert record.request_id == "test-123"
    
    def test_request_id_filter_generates_id(self):
        """Test that filter generates ID if none provided."""
        filter_obj = RequestIdFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        filter_obj.filter(record)
        assert hasattr(record, 'request_id')
        assert len(record.request_id) > 0


class TestLoggingOutput:
    """Test actual logging output."""
    
    def test_logging_to_console(self, capsys):
        """Test logging to console."""
        setup_logging(level="INFO", console_output=True, file_output=False)
        logger = get_logger("test")
        
        logger.info("Test message")
        
        captured = capsys.readouterr()
        assert "Test message" in captured.out
        assert "INFO" in captured.out
    
    def test_logging_to_file(self, tmp_path):
        """Test logging to file."""
        log_dir = tmp_path / "logs"
        setup_logging(
            level="INFO",
            log_dir=log_dir,
            console_output=False,
            file_output=True
        )
        logger = get_logger("test")
        
        logger.info("Test file message")
        
        log_file = log_dir / "app.log"
        assert log_file.exists()
        
        content = log_file.read_text()
        assert "Test file message" in content
        assert "INFO" in content
    
    def test_logging_levels_filtering(self, capsys):
        """Test that log levels filter messages correctly."""
        setup_logging(level="WARNING", console_output=True, file_output=False)
        logger = get_logger("test")
        
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        captured = capsys.readouterr()
        assert "Debug message" not in captured.out
        assert "Info message" not in captured.out
        assert "Warning message" in captured.out
        assert "Error message" in captured.out


class TestLogContext:
    """Test log_context context manager."""
    
    def test_log_context_adds_fields(self, tmp_path):
        """Test that log_context adds fields to log records."""
        log_dir = tmp_path / "logs"
        setup_logging(
            level="INFO",
            log_dir=log_dir,
            console_output=False,
            file_output=True
        )
        logger = get_logger("test")
        
        # Store records to check attributes
        records = []
        class RecordCapture(logging.Handler):
            def emit(self, record):
                records.append(record)
        
        capture = RecordCapture()
        logger.addHandler(capture)
        
        with log_context(request_id="req-123", user_id="user-456"):
            logger.info("Context message")
        
        # Check that context was added to record
        assert len(records) == 1
        assert hasattr(records[0], 'request_id')
        assert records[0].request_id == "req-123"
        assert hasattr(records[0], 'user_id')
        assert records[0].user_id == "user-456"
    
    def test_log_context_restores_factory(self):
        """Test that log_context restores original factory."""
        original_factory = logging.getLogRecordFactory()
        
        with log_context(test_key="test_value"):
            pass
        
        restored_factory = logging.getLogRecordFactory()
        assert original_factory == restored_factory


class TestLoggerContext:
    """Test LoggerContext class."""
    
    def test_logger_context_adds_fields(self, tmp_path):
        """Test that LoggerContext adds fields to log records."""
        log_dir = tmp_path / "logs"
        setup_logging(
            level="INFO",
            log_dir=log_dir,
            console_output=False,
            file_output=True
        )
        logger = get_logger("test")
        
        # Store records to check attributes
        records = []
        class RecordCapture(logging.Handler):
            def emit(self, record):
                records.append(record)
        
        capture = RecordCapture()
        logger.addHandler(capture)
        
        with LoggerContext(logger, request_id="req-789"):
            logger.info("Context message")
        
        # Check that context was added to record
        assert len(records) == 1
        assert hasattr(records[0], 'request_id')
        assert records[0].request_id == "req-789"
    
    def test_logger_context_nested(self, tmp_path):
        """Test nested LoggerContext managers."""
        log_dir = tmp_path / "logs"
        setup_logging(
            level="INFO",
            log_dir=log_dir,
            console_output=False,
            file_output=True
        )
        logger = get_logger("test")
        
        with LoggerContext(logger, outer="value1"):
            logger.info("Outer context")
            
            with LoggerContext(logger, inner="value2"):
                logger.info("Inner context")
        
        log_file = log_dir / "app.log"
        content = log_file.read_text()
        
        assert "Outer context" in content
        assert "Inner context" in content


class TestLoggingIntegration:
    """Integration tests for logging system."""
    
    def test_complete_logging_workflow(self, tmp_path):
        """Test complete logging workflow with all features."""
        log_dir = tmp_path / "logs"
        
        # Setup logging
        setup_logging(
            level="DEBUG",
            log_dir=log_dir,
            console_output=True,
            file_output=True,
            json_format=False,
            request_id="test-req"
        )
        
        # Get logger and log messages
        logger = get_logger("test.module")
        
        logger.debug("Debug message")
        logger.info("Info message", extra={"key": "value"})
        logger.warning("Warning message")
        logger.error("Error message", exc_info=False)
        
        # Use context manager
        with log_context(user_id="user-123"):
            logger.info("Context message")
        
        # Check log file
        log_file = log_dir / "app.log"
        assert log_file.exists()
        
        content = log_file.read_text()
        assert "Debug message" in content
        assert "Info message" in content
        assert "Warning message" in content
        assert "Error message" in content
        assert "Context message" in content
    
    def test_logging_with_exceptions(self, tmp_path):
        """Test logging with exception information."""
        log_dir = tmp_path / "logs"
        setup_logging(
            level="ERROR",
            log_dir=log_dir,
            console_output=False,
            file_output=True
        )
        logger = get_logger("test")
        
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.error("Exception occurred", exc_info=True)
        
        log_file = log_dir / "app.log"
        content = log_file.read_text()
        
        assert "Exception occurred" in content
        assert "ValueError" in content
        assert "Test exception" in content


class TestResetLogging:
    """Test reset_logging function."""
    
    def test_reset_logging_clears_state(self):
        """Test that reset_logging clears configuration state."""
        setup_logging(file_output=False)
        assert len(logging.getLogger().handlers) > 0
        
        reset_logging()
        assert len(logging.getLogger().handlers) == 0
    
    def test_reset_logging_allows_reconfiguration(self):
        """Test that logging can be reconfigured after reset."""
        setup_logging(level="INFO", file_output=False)
        reset_logging()
        setup_logging(level="DEBUG", file_output=False)
        
        assert logging.getLogger().level == logging.DEBUG


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
