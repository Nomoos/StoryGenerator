# Infrastructure: Add Logging System

**ID:** `infrastructure-logging`  
**Priority:** P1 (High)  
**Effort:** 3-4 hours  
**Status:** Not Started

## Overview

Minimal logging with print statements. Implement proper structured logging for debugging and monitoring.

## Acceptance Criteria

- [ ] Structured logging with Python logging module
- [ ] Different log levels (DEBUG, INFO, WARNING, ERROR)
- [ ] Log to file and console
- [ ] JSON log format for production
- [ ] Request ID tracking

## Task Details

### Logging Configuration

```python
import logging
from pythonjsonlogger import jsonlogger

def setup_logging(level: str = "INFO"):
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(console)
    
    # File handler with JSON
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(jsonlogger.JsonFormatter())
    logger.addHandler(file_handler)
```

## Related Documentation

- See `docs/RESEARCH_AND_IMPROVEMENTS.md` Section 10
