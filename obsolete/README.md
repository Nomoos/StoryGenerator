# Obsolete Code Archive

This folder contains code and documentation that is no longer actively maintained or used in the project.

## Contents

### Python Implementation (`Python/`)

The original Python implementation of StoryGenerator has been deprecated in favor of the C# implementation.

**Status:** ⚠️ Obsolete - No longer maintained

**Why deprecated:**
- The C# implementation provides better performance
- Better integration with .NET ecosystem
- More maintainable codebase
- Improved error handling and type safety

**For users:**
- If you need the Python version, it is preserved here for reference
- We strongly recommend using the C# implementation in `src/CSharp/`
- No bug fixes or feature updates will be made to the Python code

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

### Python Research (`research/python/`)

Research prototypes and scripts created for the Python implementation:
- LLM integration scripts (llm_call.py)
- Image generation (sdxl_keyframe.py)
- Video generation (ltx_generate.py)
- Audio processing (lufs_normalize.py)
- Subtitle tools (srt_tools.py)
- Frame interpolation (interpolation.py)

See `research/README.md` for details on archived research files.

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
- See `docs/CSHARP_IMPLEMENTATION_COMPLETE.md` for C# implementation details
- See `CLEANUP.md` for repository reorganization history

---

**Last Updated:** 2025-10-08  
**Archived From:** 
- `src/Python/` - Python implementation
- `docs/` - Python-specific documentation
- `issues/step-XX/` - Python-based sequential issues
- `research/python/` - Python research prototypes (partial)
