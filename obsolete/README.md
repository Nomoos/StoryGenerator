# Obsolete Code Archive

This folder contains code and documentation that is no longer actively maintained or used in the project.

## Contents

### ✅ Python Implementation - Removed (2025-01-09)

The original Python implementation of StoryGenerator has been removed after successful migration to C#.

**Status:** Removed - Migration complete

**Why removed:**
- All core generators migrated to C# implementation
- Unique features documented as issues for future implementation
- Code preserved in git history for reference
- Aligns with project's hybrid architecture (C# + Python)

**Migration Details:**
- See `MIGRATION_STATUS.md` for complete migration tracking
- Issues created for valuable features not yet re-implemented
- Active Python scripts (hybrid mode) remain in `research/python/`, `src/scripts/`, `src/Python/`

**For reference:**
- Git history: `git show HEAD~1:obsolete/Python/` to view removed code
- Migration status: See `obsolete/MIGRATION_STATUS.md`

### Python Documentation (`docs/`)

Documentation specific to the Python implementation, including:
- `PYTHON_OBSOLETE_NOTICE.md` - Official deprecation notice
- `python-code-removal/` - Issue tracking for Python code removal

### Python Issues (`issues/`)

Issue tracking files for the obsolete Python-based implementation plan, including:
- **Sequential step issues** (`step-00` through `step-14`) - Comprehensive Python implementation plans
- **Python-specific atomic tasks** - Research prototypes for Python implementations

See `issues/README.md` for details on archived issues.

**Current Issues:** Active C# implementation issues are in the main `issues/` directory.

### Python Research (`research/`)

**Status:** Mostly archived - Some files moved to active `research/python/`

Research prototypes and scripts created for the obsolete Python implementation. Most files have been archived here, but some actively-used Python scripts remain in the main `research/python/` directory as they are part of the hybrid architecture.

**Archived Python Research Files:**
- See `research/README.md` for details on archived research files
- LLM integration prototypes
- Image generation experiments  
- Video generation experiments
- Audio processing utilities
- Subtitle tools
- Frame interpolation research

**Active Python Files (NOT obsolete):**
The following Python files are **NOT obsolete** and remain active in the hybrid architecture:
- `research/python/whisper_subprocess.py` - Used by C# WhisperClient
- `research/python/test_whisper_integration.py` - Integration tests
- `src/scripts/whisper_asr.py` - ASR processing
- `src/scripts/sdxl_generation.py` - Image generation  
- `src/scripts/ltx_synthesis.py` - Video synthesis
- `src/Python/` - Various utility modules for hybrid integration

**Current Research:** Active research (including C#-compatible Python scripts) is in the main `research/` directory.

## Migration Guide

If you were using the Python version:

1. **Switch to C# implementation** in `src/CSharp/`
2. **Review the main README.md** for C# setup instructions
3. **Check docs/QUICKSTART.md** for getting started with C#

## Why Keep This?

This code is kept for:
- Historical reference
- Understanding the project evolution
- Reference for anyone who needs to understand the original implementation
- Potential future porting or learning purposes

## Related Documentation

- See main `README.md` for current project documentation
- See `MIGRATION_STATUS.md` for Python to C# migration tracking
- See `docs/RESEARCH_SUMMARY.md` for hybrid architecture research
- See `docs/HYBRID_ARCHITECTURE_QUICKREF.md` for C# + Python integration patterns

---

**Last Updated:** 2025-01-09  
**Status:** Python implementation removed after successful C# migration  
**Archived From:** 
- `obsolete/Python/` - Removed 2025-01-09 (see MIGRATION_STATUS.md)
- `docs/` - Python-specific documentation
- `issues/step-XX/` - Python-based sequential issues
- `research/python/` - Python research prototypes (partial - some remain active)
