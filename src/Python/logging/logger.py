"""
Structured logging system with console and file handlers.

Provides structured logging with support for:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Console output with readable formatting
- File output with JSON formatting for production
- Request ID tracking for distributed tracing
- Contextual information in logs
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter that adds additional context."""
    
    def add_fields(self, log_record, record, message_dict):
        """Add custom fields to log record."""
        super().add_fields(log_record, record, message_dict)
        
        # Add standard fields
        log_record['timestamp'] = self.formatTime(record, self.datefmt)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        
        # Add location info
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno


def setup_logging(
    level: str = "INFO",
    log_dir: Optional[Path] = None,
    console_output: bool = True,
    file_output: bool = True,
    json_format: bool = False,
    request_id: Optional[str] = None
) -> logging.Logger:
    """Set up structured logging with console and file handlers.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (default: ./logs)
        console_output: Enable console output
        file_output: Enable file output
        json_format: Use JSON format for file output (recommended for production)
        request_id: Optional request ID for tracking
        
    Returns:
        logging.Logger: Configured root logger
        
    Example:
        >>> from src.Python.logging import setup_logging, get_logger
        >>> setup_logging(level="DEBUG", json_format=True)
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started", extra={"version": "1.0"})
    """
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(level.upper())
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level.upper())
        
        # Human-readable format for console
        console_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        if request_id:
            console_format = f'[{request_id}] {console_format}'
        
        console_formatter = logging.Formatter(
            console_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if file_output:
        if log_dir is None:
            log_dir = Path("./logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / "app.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level.upper())
        
        if json_format:
            # JSON format for production (easier to parse)
            file_formatter = CustomJsonFormatter(
                '%(timestamp)s %(level)s %(name)s %(message)s'
            )
        else:
            # Human-readable format for development
            file_format = '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
            if request_id:
                file_format = f'[{request_id}] {file_format}'
            
            file_formatter = logging.Formatter(
                file_format,
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.
    
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
    return logging.getLogger(name)


class LoggerContext:
    """Context manager for adding contextual information to logs.
    
    Example:
        >>> with LoggerContext(logger, request_id="req-123"):
        ...     logger.info("Processing request")
    """
    
    def __init__(self, logger: logging.Logger, **context):
        """Initialize context manager.
        
        Args:
            logger: Logger instance
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
