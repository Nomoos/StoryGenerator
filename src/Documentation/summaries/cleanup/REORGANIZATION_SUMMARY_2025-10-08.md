# Repository Reorganization - October 2025

This document describes the final repository reorganization completed on 2025-10-08.

## Overview

The repository has been reorganized to have a cleaner top-level structure with better separation of concerns. This reorganization follows the guidelines in `CLEANUP_REPO.md`.

## Changes Made

### 1. Issues Moved to Top Level

**Before:** `docs/issues/`  
**After:** `issues/` (at repository root)

All issue tracking files have been moved to a top-level `issues/` folder for better visibility and organization. This includes:
- Sequential step-by-step issues
- Atomic parallelizable task breakdown
- C# roadmap and phase tracking

### 2. Python Code Archived to Obsolete Folder

**Before:** `src/Python/`  
**After:** `obsolete/Python/`

The Python implementation has been moved to an `obsolete/` folder since:
- C# implementation is now the primary codebase
- Python code is no longer actively maintained
- Keeping it for historical reference and learning purposes

### 3. Python Documentation Archived

**Before:**
- `docs/PYTHON_OBSOLETE_NOTICE.md`
- `docs/issues/python-code-removal/`

**After:**
- `obsolete/docs/PYTHON_OBSOLETE_NOTICE.md`
- `obsolete/docs/python-code-removal/`

Python-specific documentation has been moved alongside the Python code in the obsolete folder.

### 4. Research Moved to Top Level

**Before:** `src/research/`  
**After:** `research/` (at repository root)

Research and prototype code has been moved to the top level for better visibility and separation from production source code. This includes:
- C# research implementations
- Python research scripts
- Research documentation

### 5. Updated Root Guard

The root guard script (`scripts/check-clean-root.sh`) has been updated to allow the new folder structure:
- `issues/` - Issue tracking and task breakdown
- `obsolete/` - Archived code and documentation
- `research/` - Research and prototypes

### 6. Updated Documentation

- `CLEANUP_REPO.md` - Updated with new allowed top-level items
- `issues/README.md` - Updated path references
- `obsolete/README.md` - Created to explain the obsolete folder purpose
- `.gitignore` - Added section for obsolete folder artifacts

### 7. Python Issues and Research Further Archived (2025-10-08 Update)

**Additional Python-specific items moved to obsolete:**

**Issues:**
- **Before:** `issues/step-00-research/` through `issues/step-14-distribution-analytics/`
- **After:** `obsolete/issues/step-XX/`

All sequential Python-based implementation issues have been archived to `obsolete/issues/` as they represented the Python implementation plan which is no longer maintained. Active C# implementation tracking remains in `issues/atomic/` and `issues/csharp-*/`.

**Research:**
- **Before:** Multiple Python research scripts in `research/python/`
- **After:** Most moved to `obsolete/research/python/`

Python research files created for the obsolete Python implementation have been archived:
- `llm_call.py`, `asr_whisper.py`, `sdxl_keyframe.py`, `ltx_generate.py`
- `lufs_normalize.py`, `srt_tools.py`, `interpolation.py`

**Active files kept in `research/python/`:**
- `whisper_subprocess.py` - Used by C# WhisperClient via subprocess
- `test_whisper_integration.py` - Tests for whisper integration

## Current Top-Level Structure

```
StoryGenerator/
├── .github/          # GitHub configuration and workflows
├── .idea/            # IDE configuration
├── assets/           # Static assets (images, fonts, etc.)
├── data/             # Generated content and data files
├── docs/             # Project documentation
├── examples/         # Example files and starting work directory
├── issues/           # Issue tracking and task breakdown
├── obsolete/         # Archived Python code and docs
├── research/         # Research and prototypes
├── scripts/          # Utility scripts
├── src/              # Source code
│   ├── CSharp/       # C# implementation (active)
│   └── Generator/    # Generator modules
├── tests/            # Test files
├── .editorconfig     # Editor configuration
├── .env.example      # Environment variables template
├── .gitattributes    # Git attributes
├── .gitignore        # Git ignore patterns
├── CLEANUP_REPO.md   # Cleanup and reorganization guide
├── QUICKSTART.md     # Quick start guide
├── README.md         # Main documentation
└── requirements.txt  # Python dependencies (for tools)
```

## Why This Structure?

### Issues at Top Level
- **Visibility:** Issues are first-class citizens in project management
- **Accessibility:** Easier to find and navigate issue tracking
- **Convention:** Follows common patterns in open-source projects

### Obsolete Folder
- **Clarity:** Makes it obvious that Python code is no longer maintained
- **Preservation:** Keeps historical implementation for reference
- **Clean Separation:** Active code in `src/`, archived code in `obsolete/`

### Research at Top Level
- **Visibility:** Research code is distinct from production code
- **Accessibility:** Easier to find experimental and prototype implementations
- **Separation of Concerns:** Production code in `src/`, research in `research/`

### Clean Top Level
- **Maintainability:** Easier to navigate the project
- **Standards:** Follows industry best practices
- **Automation:** Root guard prevents clutter from accumulating

## Migration Guide

### For Developers

If you were working with the old structure:

1. **Python code:** Now in `obsolete/Python/` (read-only reference)
2. **Issues:** Now in `issues/` instead of `docs/issues/`
3. **Research code:** Now in `research/` instead of `src/research/`
4. **C# code:** Still in `src/CSharp/` (no change)

### For Documentation Links

Update any documentation that references:
- `docs/issues/` → `issues/`
- `src/Python/` → `obsolete/Python/` (note: obsolete, use C# instead)

## Testing

✅ Root guard script passes with new structure  
✅ All files properly moved with `git mv` (preserving history)  
✅ .gitignore updated to handle obsolete folder  
✅ Documentation updated with correct paths

## Related Documentation

- `CLEANUP_REPO.md` - Comprehensive cleanup and reorganization guide
- `docs/summaries/REORGANIZATION_SUMMARY_2025-10-07.md` - Previous reorganization summary
- `obsolete/README.md` - Information about archived code

---

**Date:** 2025-10-08  
**Branch:** copilot/chorereorg-repository-structure  
**Files Changed:** ~172 files (mostly moves/renames)  
**Status:** ✅ Complete
