# Structured Logging System

This document describes the structured logging system for the StoryGenerator application.

## Overview

The logging system provides structured, configurable logging with support for multiple output formats, log levels, request tracking, and contextual information. It integrates with the configuration system (`core.config`) for seamless setup.

## Quick Start

```python
from core.logging import setup_logging, get_logger

# Setup logging (usually done once at application startup)
setup_logging()

# Get a logger for your module
logger = get_logger(__name__)

# Log messages
logger.debug("Debugging information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical error")
```

## Features

- **Multiple Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Multiple Handlers**: Console and file output with independent formatting
- **JSON Formatting**: Optional JSON output for production (structured logs)
- **Request ID Tracking**: Track requests across distributed systems
- **Context Managers**: Add contextual information to all logs within a scope
- **Configuration Integration**: Uses settings from `core.config`
- **Auto-configuration**: Automatically configured when you call `get_logger()`

## Configuration

Logging can be configured via environment variables (through `core.config`):

```bash
# Log level
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Log format
LOG_FORMAT=text             # text or json

# File logging
LOG_TO_FILE=true            # Enable/disable file logging

# Logs directory
LOGS_DIR=./logs             # Directory for log files
```

## Setup and Configuration

### Basic Setup

```python
from core.logging import setup_logging

# Use config defaults
setup_logging()

# Or customize
setup_logging(
    level="DEBUG",
    console_output=True,
    file_output=True,
    json_format=False
)
```

### With Request ID

```python
from core.logging import setup_logging

# Add request ID to all logs
setup_logging(request_id="req-12345")

# Logs will include: [req-12345] 2025-10-10 12:00:00 - mymodule - INFO - Message
```

### Custom Log Directory

```python
from pathlib import Path
from core.logging import setup_logging

setup_logging(log_dir=Path("/var/log/myapp"))
```

## Using Loggers

### Getting a Logger

```python
from core.logging import get_logger

logger = get_logger(__name__)  # Use module name
logger = get_logger("myapp.component")  # Use custom name
```

### Logging Messages

```python
logger = get_logger(__name__)

# Basic logging
logger.info("Application started")
logger.warning("Low memory: %d MB", 100)
logger.error("Failed to connect to database")

# With extra context
logger.info("User logged in", extra={"user_id": "user-123", "ip": "192.168.1.1"})

# With exception information
try:
    risky_operation()
except Exception:
    logger.error("Operation failed", exc_info=True)  # Includes stack trace
```

## Context Managers

### Using log_context

```python
from core.logging import get_logger, log_context

logger = get_logger(__name__)

with log_context(request_id="req-123", user_id="user-456"):
    logger.info("Processing request")  # Will include request_id and user_id
    logger.info("Request completed")   # Context applies to all logs in block
```

### Using LoggerContext

```python
from core.logging import get_logger, LoggerContext

logger = get_logger(__name__)

with LoggerContext(logger, transaction_id="tx-789"):
    logger.info("Starting transaction")
    # ... transaction code ...
    logger.info("Transaction completed")
```

### Nested Contexts

```python
with log_context(request_id="req-123"):
    logger.info("Outer context")
    
    with log_context(operation="database_query"):
        logger.info("Inner context")  # Has both request_id and operation
```

## Output Formats

### Console Output (Text Format)

```
2025-10-10 12:00:00 - myapp.module - INFO - Application started
2025-10-10 12:00:01 - myapp.module - WARNING - Low memory: 100 MB
2025-10-10 12:00:02 - myapp.module - ERROR - Connection failed
```

### Console Output with Request ID

```
[req-123] 2025-10-10 12:00:00 - myapp.module - INFO - Processing request
[req-123] 2025-10-10 12:00:01 - myapp.module - INFO - Request completed
```

### File Output (Text Format)

```
2025-10-10 12:00:00 - myapp.module - INFO - module:42 - Application started
2025-10-10 12:00:01 - myapp.module - WARNING - module:56 - Low memory: 100 MB
```

### File Output (JSON Format)

```json
{
  "timestamp": "2025-10-10T12:00:00",
  "level": "INFO",
  "logger": "myapp.module",
  "module": "module",
  "function": "start_app",
  "line": 42,
  "message": "Application started"
}
```

## Log Levels

### Level Hierarchy

From most verbose to least verbose:

1. **DEBUG**: Detailed diagnostic information
2. **INFO**: General informational messages
3. **WARNING**: Warning messages (something unexpected but not critical)
4. **ERROR**: Error messages (something failed but application continues)
5. **CRITICAL**: Critical messages (severe errors, application may stop)

### When to Use Each Level

```python
logger = get_logger(__name__)

# DEBUG - Development and troubleshooting
logger.debug("Variable value: %s", my_var)
logger.debug("Entering function with args: %s", args)

# INFO - Normal operations
logger.info("Application started")
logger.info("Request processed successfully")
logger.info("File saved to %s", path)

# WARNING - Unexpected but recoverable
logger.warning("API rate limit approaching")
logger.warning("Cache miss for key: %s", key)
logger.warning("Deprecated function called")

# ERROR - Failures that need attention
logger.error("Failed to save file: %s", filename)
logger.error("Database connection lost")
logger.error("Invalid input received", exc_info=True)

# CRITICAL - Severe failures
logger.critical("Database unavailable - shutting down")
logger.critical("Out of memory")
logger.critical("Security violation detected")
```

## Advanced Usage

### Filtering Logs by Level

```python
# Set up logging with WARNING level
setup_logging(level="WARNING")

logger = get_logger(__name__)

logger.debug("Not logged")   # Filtered out
logger.info("Not logged")    # Filtered out
logger.warning("Logged!")    # Appears in logs
logger.error("Logged!")      # Appears in logs
```

### Separate Console and File Levels

```python
# Console: INFO, File: DEBUG
setup_logging(level="DEBUG", console_output=True, file_output=True)

# Then configure handlers separately if needed
import logging
root = logging.getLogger()
for handler in root.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setLevel(logging.INFO)
```

### Logging Exceptions

```python
logger = get_logger(__name__)

try:
    result = divide(10, 0)
except ZeroDivisionError:
    # Include full exception traceback
    logger.error("Division failed", exc_info=True)
    
    # Or just the exception message
    logger.error("Division failed: %s", str(e))
```

### Performance Considerations

```python
# Inefficient - string formatting always happens
logger.debug("Processing item: " + str(expensive_operation()))

# Efficient - only evaluated if DEBUG is enabled
logger.debug("Processing item: %s", expensive_operation())

# Most efficient for complex formatting
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("Complex message: %s", complex_computation())
```

## Testing

### Resetting Logging in Tests

```python
from core.logging import reset_logging

def test_my_feature():
    reset_logging()  # Clear any previous configuration
    # ... your test code ...
```

### Capturing Log Output in Tests

```python
import logging
from core.logging import setup_logging, get_logger

def test_logging_output(caplog):
    setup_logging(level="INFO", console_output=False, file_output=False)
    logger = get_logger("test")
    
    with caplog.at_level(logging.INFO):
        logger.info("Test message")
    
    assert "Test message" in caplog.text
```

## Integration with Other Systems

### Flask/FastAPI

```python
from flask import Flask, request
from core.logging import setup_logging, log_context, get_logger

app = Flask(__name__)
setup_logging()
logger = get_logger(__name__)

@app.before_request
def log_request():
    request_id = request.headers.get('X-Request-ID', generate_request_id())
    with log_context(request_id=request_id):
        logger.info("Request started", extra={
            "method": request.method,
            "path": request.path
        })
```

### Django

```python
# settings.py
from core.logging import setup_logging

setup_logging(level="INFO", json_format=True)

# views.py
from core.logging import get_logger

logger = get_logger(__name__)

def my_view(request):
    logger.info("View accessed", extra={"user": request.user.username})
    # ... view logic ...
```

## Troubleshooting

### Logs Not Appearing

1. Check log level is appropriate
2. Verify handlers are configured
3. Check file permissions for log directory

```python
# Debug logging setup
import logging
logging.getLogger().setLevel(logging.DEBUG)
for handler in logging.getLogger().handlers:
    print(f"Handler: {handler}, Level: {handler.level}")
```

### Duplicate Log Messages

If you see duplicate messages, logging may be configured multiple times:

```python
from core.logging import reset_logging

reset_logging()  # Clear and reconfigure
setup_logging()
```

### JSON Logger Not Available

If JSON logging isn't working, install the required package:

```bash
pip install python-json-logger
```

## Best Practices

1. **Use module loggers**: `logger = get_logger(__name__)`
2. **Use appropriate log levels**: INFO for normal ops, WARNING for issues
3. **Include context**: Use `extra={}` or `log_context()` for additional information
4. **Use lazy formatting**: `logger.info("Value: %s", value)` not `f"Value: {value}"`
5. **Log exceptions properly**: Use `exc_info=True` to include tracebacks
6. **Don't log sensitive data**: Passwords, tokens, personal information
7. **Use structured logging**: In production, enable JSON format for parsing

## See Also

- [Configuration System](CONFIG_README.md) - Logging configuration
- [core.config Settings](../core/config.py) - Configuration options
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Structured Logging Best Practices](https://www.structlog.org/en/stable/why.html)
