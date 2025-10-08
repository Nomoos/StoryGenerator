# Setup: Repository Folder Structure

**ID:** `00-setup-01`  
**Priority:** P0 (Critical Path)  
**Effort:** 1-2 hours  
**Status:** Not Started

## Overview

Create the complete folder structure for the StoryGenerator pipeline according to specifications. This is a foundational task that must complete before any content generation can begin.

## Dependencies

**Requires:**
- None (first task)

**Blocks:**
- All other tasks (they need folders to save output)

## Acceptance Criteria

- [ ] All folders created under `/Generator/` directory
- [ ] Folder structure matches specification exactly
- [ ] Age buckets: `10-13`, `14-17`, `18-23`
- [ ] Gender segments: `women`, `men`
- [ ] Verification script runs successfully
- [ ] README.md created in root Generator folder

## Task Details

### Folders to Create

#### Content Generation
```
Generator/
├── config/
├── ideas/{women|men}/{10-13|14-17|18-23}/
├── topics/{women|men}/{10-13|14-17|18-23}/
├── titles/{women|men}/{10-13|14-17|18-23}/
├── scores/{women|men}/{10-13|14-17|18-23}/
├── sources/
│   ├── reddit/{women|men}/{10-13|14-17|18-23}/
│   ├── quora/{women|men}/{10-13|14-17|18-23}/
│   ├── twitter/{women|men}/{10-13|14-17|18-23}/
│   ├── medium/{women|men}/{10-13|14-17|18-23}/
│   ├── tumblr/{women|men}/{10-13|14-17|18-23}/
│   ├── youtube/{women|men}/{10-13|14-17|18-23}/
│   └── ranked/{women|men}/{10-13|14-17|18-23}/
```

#### Script Processing
```
├── scripts/
│   ├── raw_local/{women|men}/{10-13|14-17|18-23}/
│   ├── iter_local/{women|men}/{10-13|14-17|18-23}/
│   └── gpt_improved/{women|men}/{10-13|14-17|18-23}/
```

#### Audio/Video Pipeline
```
├── voices/choice/{women|men}/{10-13|14-17|18-23}/
├── audio/
│   ├── tts/{women|men}/{10-13|14-17|18-23}/
│   └── normalized/{women|men}/{10-13|14-17|18-23}/
├── subtitles/
│   ├── srt/{women|men}/{10-13|14-17|18-23}/
│   └── timed/{women|men}/{10-13|14-17|18-23}/
├── scenes/json/{women|men}/{10-13|14-17|18-23}/
├── images/
│   ├── keyframes_v1/{women|men}/{10-13|14-17|18-23}/
│   └── keyframes_v2/{women|men}/{10-13|14-17|18-23}/
├── videos/
│   ├── ltx/{women|men}/{10-13|14-17|18-23}/
│   └── interp/{women|men}/{10-13|14-17|18-23}/
```

#### Output & Research
```
├── final/{women|men}/{10-13|14-17|18-23}/
└── research/
    ├── python/
    └── csharp/
```

### Implementation

Use existing verification script or create new one:

```python
#!/usr/bin/env python3
"""Create complete Generator folder structure."""

from pathlib import Path

GENDERS = ["women", "men"]
AGE_BUCKETS = ["10-13", "14-17", "18-23"]
RESEARCH_CATS = ["python", "csharp"]

FOLDERS_WITH_GENDER_AGE = [
    "ideas", "topics", "titles", "scores",
    "scripts/raw_local", "scripts/iter_local", "scripts/gpt_improved",
    "voices/choice",
    "audio/tts", "audio/normalized",
    "subtitles/srt", "subtitles/timed",
    "scenes/json",
    "images/keyframes_v1", "images/keyframes_v2",
    "videos/ltx", "videos/interp",
    "final",
    "sources/reddit", "sources/quora", "sources/twitter",
    "sources/medium", "sources/tumblr", "sources/youtube",
    "sources/ranked"
]

def create_structure(base_path="Generator"):
    base = Path(base_path)
    
    # Config folder
    (base / "config").mkdir(parents=True, exist_ok=True)
    
    # Gender/Age folders
    for folder in FOLDERS_WITH_GENDER_AGE:
        for gender in GENDERS:
            for age in AGE_BUCKETS:
                path = base / folder / gender / age
                path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created: {path}")
    
    # Research folders
    for cat in RESEARCH_CATS:
        path = base / "research" / cat
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {path}")
    
    print(f"\n✨ Folder structure created successfully!")

if __name__ == "__main__":
    create_structure()
```

### Verification

Run existing verification:
```bash
cd src/CSharp/Tools
dotnet run VerifyFolders.cs
```

Or use Python verification:
```bash
python scripts/setup_folders.py
```

## Output Files

- `Generator/` - Complete folder structure
- `Generator/README.md` - Documentation of structure
- `Generator/config/.gitkeep` - Ensure config folder is tracked

## Related Files

- `src/CSharp/Tools/VerifyFolders.cs` - C# verification script
- `docs/GENERATOR_STRUCTURE.md` - Documentation

## Validation

```bash
# Verify structure
find Generator -type d | wc -l  # Should be 300+ directories

# Check one segment completely
ls -R Generator/ideas/women/18-23
ls -R Generator/scripts/raw_local/women/18-23
ls -R Generator/final/women/18-23
```

## Notes

- All folders follow pattern: `{base}/{women|men}/{age}/`
- Age buckets are consistent across all folders
- Research folders don't use gender/age segmentation
- Config folder is flat (no subdirectories)

## Next Steps

After completion:
- Proceed to `00-setup-02-config-files`
- Teams can start on research prototypes in parallel
