"""
Structured logging system for the StoryGenerator application.

This module provides enhanced logging with:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Console and file output with configurable formats
- JSON formatting for production
- Request ID tracking for distributed tracing
- Context managers for contextual logging
- Integration with core.config for configuration

Example:
    >>> from core.logging import setup_logging, get_logger
    >>> setup_logging()
    >>> logger = get_logger(__name__)
    >>> logger.info("Application started")
    >>> logger.warning("Low memory", extra={"memory_mb": 100})
"""

import logging
import sys
import uuid
from pathlib import Path
from typing import Optional, Dict, Any
from contextlib import contextmanager

try:
    from pythonjsonlogger import jsonlogger
    JSON_LOGGER_AVAILABLE = True
except ImportError:
    JSON_LOGGER_AVAILABLE = False
    jsonlogger = None

from core.config import settings


# Global logger instance tracking
_logging_configured = False


class CustomJsonFormatter(jsonlogger.JsonFormatter if JSON_LOGGER_AVAILABLE else object):
    """Custom JSON formatter with additional context fields."""
    
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        """
        Add custom fields to log record.
        
        Args:
            log_record: Dictionary to add fields to
            record: LogRecord instance
            message_dict: Message dictionary
        """
        if not JSON_LOGGER_AVAILABLE:
            return
            
        super().add_fields(log_record, record, message_dict)
        
        # Add standard fields
        log_record['timestamp'] = self.formatTime(record, self.datefmt)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        
        # Add location info
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno
        
        # Add request ID if present
        if hasattr(record, 'request_id'):
            log_record['request_id'] = record.request_id


class RequestIdFilter(logging.Filter):
    """Filter to add request ID to log records."""
    
    def __init__(self, request_id: Optional[str] = None):
        """
        Initialize filter with optional request ID.
        
        Args:
            request_id: Optional request ID to add to all log records
        """
        super().__init__()
        self.request_id = request_id or str(uuid.uuid4())[:8]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add request ID to record.
        
        Args:
            record: Log record to filter
            
        Returns:
            bool: Always True (don't filter out records)
        """
        if not hasattr(record, 'request_id'):
            record.request_id = self.request_id
        return True


def setup_logging(
    level: Optional[str] = None,
    log_dir: Optional[Path] = None,
    console_output: bool = True,
    file_output: Optional[bool] = None,
    json_format: Optional[bool] = None,
    request_id: Optional[str] = None,
    force_reconfigure: bool = False
) -> logging.Logger:
    """
    Set up structured logging with console and file handlers.
    
    Uses configuration from core.config.settings by default, but allows
    overrides for all parameters.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               Defaults to settings.log_level
        log_dir: Directory for log files. Defaults to settings.logs_dir
        console_output: Enable console output (default: True)
        file_output: Enable file output. Defaults to settings.log_to_file
        json_format: Use JSON format for file output. Defaults to
                    True if settings.log_format == "json"
        request_id: Optional request ID for tracking
        force_reconfigure: Force reconfiguration even if already configured
        
    Returns:
        logging.Logger: Configured root logger
        
    Example:
        >>> from core.logging import setup_logging, get_logger
        >>> setup_logging(level="DEBUG")
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started", extra={"version": "1.0"})
    """
    global _logging_configured
    
    # Skip if already configured unless forced
    if _logging_configured and not force_reconfigure:
        return logging.getLogger()
    
    # Use settings defaults if not provided
    if level is None:
        level = settings.log_level
    if log_dir is None:
        log_dir = settings.logs_dir
    if file_output is None:
        file_output = settings.log_to_file
    if json_format is None:
        json_format = (settings.log_format == "json")
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level.upper())
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers = []
    
    # Create request ID filter if provided
    request_id_filter = RequestIdFilter(request_id) if request_id else None
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level.upper())
        
        # Add request ID filter to handler if provided
        if request_id_filter:
            console_handler.addFilter(request_id_filter)
        
        # Human-readable format for console
        console_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        if request_id:
            console_format = f'[%(request_id)s] {console_format}'
        
        console_formatter = logging.Formatter(
            console_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # File handler
    if file_output:
        # Ensure log directory exists
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / "app.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level.upper())
        
        # Add request ID filter to handler if provided
        if request_id_filter:
            file_handler.addFilter(request_id_filter)
        
        if json_format and JSON_LOGGER_AVAILABLE:
            # JSON format for production (easier to parse)
            file_formatter = CustomJsonFormatter(
                '%(timestamp)s %(level)s %(name)s %(message)s'
            )
        else:
            # Human-readable format for development
            file_format = '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
            if request_id:
                file_format = f'[%(request_id)s] {file_format}'
            
            file_formatter = logging.Formatter(
                file_format,
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    _logging_configured = True
    root_logger.info(f"Logging configured - Level: {level}, Format: {'JSON' if json_format else 'TEXT'}")
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Automatically sets up logging if not already configured.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        logging.Logger: Logger instance
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
        >>> logger.warning("Low memory", extra={"memory_mb": 100})
        >>> logger.error("Failed to process", exc_info=True)
    """
    global _logging_configured
    
    # Auto-configure if not already done
    if not _logging_configured:
        setup_logging()
    
    return logging.getLogger(name)


@contextmanager
def log_context(**context):
    """
    Context manager for adding contextual information to all logs.
    
    Args:
        **context: Context key-value pairs to add to all logs
        
    Yields:
        None
        
    Example:
        >>> logger = get_logger(__name__)
        >>> with log_context(request_id="req-123", user_id="user-456"):
        ...     logger.info("Processing request")
        ...     logger.info("Request completed")
    """
    old_factory = logging.getLogRecordFactory()
    
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        for key, value in context.items():
            setattr(record, key, value)
        return record
    
    logging.setLogRecordFactory(record_factory)
    try:
        yield
    finally:
        logging.setLogRecordFactory(old_factory)


class LoggerContext:
    """
    Context manager for adding contextual information to logs.
    
    This is an alternative to the log_context function that can be used
    when you need more control over the logger instance.
    
    Example:
        >>> logger = get_logger(__name__)
        >>> with LoggerContext(logger, request_id="req-123"):
        ...     logger.info("Processing request")
    """
    
    def __init__(self, logger: logging.Logger, **context):
        """
        Initialize context manager.
        
        Args:
            logger: Logger instance (not actually used, kept for compatibility)
            **context: Context key-value pairs to add to all logs
        """
        self.logger = logger
        self.context = context
        self.old_factory = None
    
    def __enter__(self):
        """Enter context and set up context injection."""
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and restore original factory."""
        if self.old_factory:
            logging.setLogRecordFactory(self.old_factory)


def reset_logging():
    """
    Reset logging configuration.
    
    Useful for testing or when you need to reconfigure logging.
    """
    global _logging_configured
    _logging_configured = False
    
    # Clear all handlers
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.filters = []


# Auto-configure logging on module import if not in test mode
if not settings.is_test():
    setup_logging()
