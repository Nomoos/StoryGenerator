# Repository Reorganization Guide

## 📋 Overview

The StoryGenerator repository has been reorganized with the Python implementation marked as **OBSOLETE**:
- **C# Implementation** (Primary/Active) - Located in `src/CSharp/` - **Actively developed**
- **Python Implementation** (⚠️ OBSOLETE) - Located in `src/Python/` - **Historic reference only**

**IMPORTANT**: The Python implementation is no longer maintained and should not be used for new development. All active development has moved to C#.

## 🔄 What Changed

### Before (Old Structure)
```
StoryGenerator/
├── Generators/           # Python generators
├── Models/              # Python models
├── Tools/               # Python utilities
├── Generation/          # Python manual scripts
├── requirements.txt     # At root
├── pyproject.toml      # At root
└── requirements-dev.txt # At root
```

### After (New Structure)
```
StoryGenerator/
├── CSharp/              # C# implementation (primary)
│   ├── Generators/      # C# generators (coming soon)
│   ├── Models/          # C# models (coming soon)
│   ├── Tools/           # C# utilities (coming soon)
│   └── README.md        # C# setup guide
│
├── Python/              # Python implementation
│   ├── Generators/      # Python generators (moved)
│   ├── Models/          # Python models (moved)
│   ├── Tools/           # Python utilities (moved)
│   ├── Generation/      # Python manual scripts (moved)
│   ├── requirements.txt # Python deps (moved)
│   ├── requirements-dev.txt
│   ├── pyproject.toml
│   └── README.md        # Python setup guide
│
├── Documentation files (unchanged)
├── .env.example (shared)
└── Stories/ (shared)
```

## 🎯 Why This Change?

1. **Python Obsolescence**: Python implementation is no longer maintained - C# is the only active version
2. **Performance & Type Safety**: C# provides better performance, compile-time error detection, and maintainability
3. **Single Implementation Focus**: Consolidating development efforts on C# implementation
4. **Historic Preservation**: Python code preserved for reference while C# implementation completes
5. **Clear Direction**: Makes it unambiguous that C# is the path forward

## 🚀 Migration Guide

### ⚠️ IMPORTANT: Python is OBSOLETE

The Python implementation is no longer recommended for any use:

**DO NOT USE Python for:**
- ❌ New projects
- ❌ Production deployments
- ❌ Active development
- ❌ Feature additions

**Python code is only for:**
- ✅ Historic reference
- ✅ Understanding original architecture
- ✅ Comparing implementations during C# development

### For New Users

**Start with C#:**
```bash
cd StoryGenerator/src/CSharp
# Follow setup in src/CSharp/MIGRATION_GUIDE.md
```

### For Existing Python Users

**Migrate to C#:**
1. Review [src/CSharp/MIGRATION_GUIDE.md](../src/CSharp/MIGRATION_GUIDE.md)
2. Check current C# implementation status
3. Plan migration based on features you need
4. Stop using Python implementation

**If you must reference old Python code:**
```bash
# Python code remains at src/Python/ for reference only
cd StoryGenerator/src/Python
# DO NOT use for new development
```

## 🔧 Development Workflow Changes

### C# Development (Active - Recommended)

```bash
cd StoryGenerator/src/CSharp
# Follow setup instructions in MIGRATION_GUIDE.md
dotnet build
dotnet run --project StoryGenerator.CLI
```

### Python Development (⚠️ OBSOLETE - Reference Only)

**DO NOT use Python for active development.** The workflow below is documented for historic reference only:

```bash
# OBSOLETE - For reference only
cd StoryGenerator/src/Python
source venv/bin/activate
python Generation/Manual/MIdea.py  # DO NOT USE
```

## 📁 File Mappings

| Old Location | New Location |
|-------------|--------------|
| `Generators/` | `Python/Generators/` |
| `Models/` | `Python/Models/` |
| `Tools/` | `src/Python/Tools/` (OBSOLETE) |
| `Generation/` | `src/Python/Generation/` (OBSOLETE) |
| `requirements.txt` | `src/Python/requirements.txt` (OBSOLETE) |
| `requirements-dev.txt` | `src/Python/requirements-dev.txt` (OBSOLETE) |
| `pyproject.toml` | `src/Python/pyproject.toml` (OBSOLETE) |
| N/A | `src/CSharp/` (ACTIVE) |

## 🔧 Development Workflow Changes

### C# Development (Active - Recommended)

```bash
cd StoryGenerator/src/CSharp
# Follow setup instructions in MIGRATION_GUIDE.md
dotnet build
dotnet run --project StoryGenerator.CLI
```

### Python Development (⚠️ OBSOLETE - Reference Only)

**DO NOT use Python for active development.** The workflow below is documented for historic reference only:

```bash
# OBSOLETE - For reference only
cd StoryGenerator/src/Python
source venv/bin/activate
python Generation/Manual/MIdea.py  # DO NOT USE
```

## 📝 Documentation Updates

All documentation files remain at the root level:
- `README.md` - Updated to mark Python as OBSOLETE
- `docs/REORGANIZATION_GUIDE.md` - Updated with obsolescence notice
- `src/CSharp/MIGRATION_GUIDE.md` - C# implementation guide
- `SECURITY_CHECKLIST.md` - Unchanged
- Other docs - Mostly unchanged

## 🐛 Troubleshooting

### Issue: Module not found errors

**Solution**: Make sure you're running from the correct directory

```bash
# Should be in: StoryGenerator/Python/
pwd  # Check your location
cd Python  # If needed
```

### Issue: Can't find .env file

**Solution 1**: Copy .env.example to Python directory
```bash
cp ../.env.example .env
# Edit with your API keys
```

**Solution 2**: Update code to load from parent directory
```python
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)
```

### Issue: Stories directory not found

**Solution**: The Stories directory is shared and remains at root
```bash
# Make sure it exists
mkdir -p ../Stories/{0_Ideas,1_Scripts,2_Revised,3_VoiceOver}
```

Or update `Tools/Utils.py` to point to the correct location:
```python
import os
from pathlib import Path

# Point to root Stories directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
STORY_ROOT = os.getenv('STORY_ROOT', PROJECT_ROOT / "Stories")
```

## ✅ Checklist for Migration

- [ ] Back up your existing work
- [ ] Pull latest changes
- [ ] Update directory paths in scripts
- [ ] Move/recreate virtual environment
- [ ] Copy or create .env file in correct location
- [ ] Update import statements if needed
- [ ] Test basic functionality
- [ ] Update any CI/CD configurations
- [ ] Update documentation references

## 🎯 Best Practices

1. **Always specify full paths**: Avoid relative path issues
2. **Use environment variables**: For Stories directory location
3. **Keep .env at root**: Shared configuration
4. **Test both implementations**: Ensure compatibility
5. **Follow language-specific conventions**: Python in Python/, C# in CSharp/

## 📞 Support

If you encounter issues after reorganization:

1. Check this guide for common issues
2. Review updated README.md
3. Check Python/README.md for Python-specific help
4. Open a GitHub issue with:
   - Your directory structure (`tree -L 2`)
   - Error messages
   - What you've tried

## 🔮 Future Considerations

- **C# Implementation**: Will follow .NET conventions
- **Shared Resources**: Stories/ and .env remain shared
- **Additional Languages**: Structure allows for easy addition
- **Package Management**: Each implementation has its own deps

---

**Last Updated**: January 2025  
**Reorganization Version**: 1.0  
**Breaking Changes**: Path updates required for Python users

For questions or clarification, please open a GitHub issue.
