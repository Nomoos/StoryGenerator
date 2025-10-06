# Repository Reorganization Guide

## 📋 Overview

The StoryGenerator repository has been reorganized to support **two separate implementations**:
- **C# Implementation** (Primary/Preferred) - Located in `CSharp/`
- **Python Implementation** (Legacy/Alternative) - Located in `Python/`

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

1. **Separation of Concerns**: Keep C# and Python implementations separate
2. **C# Preference**: Makes it clear that C# is the preferred implementation
3. **Easier Maintenance**: Changes to one implementation don't affect the other
4. **Better Organization**: Clearer project structure
5. **Future-Proof**: Room for additional implementations if needed

## 🚀 Migration Guide

### For Existing Users (Python)

If you have an existing setup, you need to update your paths:

**Old Commands:**
```bash
cd StoryGenerator
python -m Generators.GStoryIdeas
```

**New Commands:**
```bash
cd StoryGenerator/Python
python -m Generators.GStoryIdeas
```

### Import Path Changes

**Old (root-level imports):**
```python
from Generators.GStoryIdeas import StoryIdeasGenerator
from Models.StoryIdea import StoryIdea
from Tools.Utils import sanitize_filename
```

**New (same imports, but run from Python/ directory):**
```python
# No changes needed if you run from Python/ directory
from Generators.GStoryIdeas import StoryIdeasGenerator
from Models.StoryIdea import StoryIdea
from Tools.Utils import sanitize_filename
```

### Virtual Environment

If you had a virtual environment at the root, you can:

**Option 1: Move it**
```bash
mv venv Python/venv
cd Python
source venv/bin/activate
```

**Option 2: Create a new one**
```bash
cd Python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

The `.env` file location has two options:

**Option 1: Keep at root (recommended)**
```bash
# .env file at: StoryGenerator/.env
# Shared by both implementations
```

**Option 2: Separate .env files**
```bash
# StoryGenerator/Python/.env
# StoryGenerator/CSharp/.env (when available)
```

For Python, if you keep `.env` at root, update your code to load from parent directory:
```python
from pathlib import Path
from dotenv import load_dotenv

# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)
```

## 📁 File Mappings

| Old Location | New Location |
|-------------|--------------|
| `Generators/` | `Python/Generators/` |
| `Models/` | `Python/Models/` |
| `Tools/` | `Python/Tools/` |
| `Generation/` | `Python/Generation/` |
| `requirements.txt` | `Python/requirements.txt` |
| `requirements-dev.txt` | `Python/requirements-dev.txt` |
| `pyproject.toml` | `Python/pyproject.toml` |
| N/A | `CSharp/` (new) |

## 🔧 Development Workflow Changes

### Python Development

**Before:**
```bash
cd StoryGenerator
source venv/bin/activate
pip install -r requirements.txt
python Generation/Manual/MIdea.py
```

**After:**
```bash
cd StoryGenerator/Python
source venv/bin/activate
pip install -r requirements.txt
python Generation/Manual/MIdea.py
```

### C# Development (Coming Soon)

```bash
cd StoryGenerator/CSharp
dotnet build
dotnet run --project StoryGenerator.CLI
```

## 📝 Documentation Updates

All documentation files remain at the root level:
- `README.md` - Updated to reflect new structure
- `QUICKSTART.md` - Updated for Python in subdirectory
- `ARCHITECTURE.md` - Remains valid
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
