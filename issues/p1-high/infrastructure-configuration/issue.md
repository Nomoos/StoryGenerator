# Infrastructure: Implement Configuration Management

**ID:** `infrastructure-configuration`  
**Priority:** P1 (High)  
**Effort:** 4-6 hours  
**Status:** Not Started

## Overview

No centralized configuration management. Implement a proper configuration system using environment variables and config files.

## Acceptance Criteria

- [ ] Configuration loaded from files and environment
- [ ] Validation of configuration values
- [ ] Different configs for dev/prod
- [ ] Type-safe configuration access
- [ ] Configuration documentation

## Task Details

### Install

```bash
pip install pydantic-settings>=2.0.0
```

### Configuration Class

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    elevenlabs_api_key: str
    story_root: Path = Path("./Stories")
    log_level: str = "INFO"
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
```

## Related Documentation

- See `docs/RESEARCH_AND_IMPROVEMENTS.md` Section 9
