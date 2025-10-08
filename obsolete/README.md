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
**Archived From:** `src/Python/` and `docs/` (Python-specific)
