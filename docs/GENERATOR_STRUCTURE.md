# Generator Folder Structure

## Overview

All generation-related files and artifacts are organized under the `Generator/` folder. This structure provides a clean separation between source code and generated content, making the repository easier to navigate and maintain.

## Folder Organization

```
Generator/
├── config/                  # Configuration files
│   └── *.json              # Audience and pipeline configurations
│
├── trends/                  # Google Trends processing (Step 1)
│   ├── raw/                # Raw CSV exports from Google Trends
│   ├── processed/          # Processed trends and content suggestions
│   ├── samples/            # Sample CSV files for reference
│   └── {gender}/{age}/     # Organized trends by audience
│
├── ideas/                   # Story ideas generation (Step 2)
│   └── {gender}/{age}/     # Ideas organized by target audience
│
├── topics/                  # Topic classification (Step 3)
│   └── {gender}/{age}/     # Topics organized by target audience
│
├── titles/                  # Video titles generation (Step 4)
│   └── {gender}/{age}/     # Titles organized by target audience
│
├── scores/                  # Quality scores and metrics (Step 5)
│   └── {gender}/{age}/     # Scores organized by target audience
│
├── scripts/                 # Script generation and refinement
│   ├── raw_local/          # Initial scripts (Step 6)
│   │   └── {gender}/{age}/
│   ├── iter_local/         # Iteratively refined scripts (Step 7)
│   │   └── {gender}/{age}/
│   └── gpt_improved/       # GPT-improved scripts (Step 8)
│       └── {gender}/{age}/
│
├── voices/                  # Voice configuration
│   └── choice/             # Voice selection (Step 9)
│       └── {gender}/{age}/
│
├── audio/                   # Audio generation
│   ├── tts/                # Text-to-speech audio (Step 10)
│   │   └── {gender}/{age}/
│   └── normalized/         # Normalized audio (Step 11)
│       └── {gender}/{age}/
│
├── subtitles/               # Subtitle generation
│   ├── srt/                # SRT subtitle files (Step 12)
│   │   └── {gender}/{age}/
│   └── timed/              # Timed subtitle data (Step 13)
│       └── {gender}/{age}/
│
├── scenes/                  # Scene descriptions
│   └── json/               # Scene JSON files (Step 14)
│       └── {gender}/{age}/
│
├── images/                  # Image assets
│   ├── keyframes_v1/       # Keyframe images v1 (Step 15)
│   │   └── {gender}/{age}/
│   └── keyframes_v2/       # Keyframe images v2 (Step 16)
│       └── {gender}/{age}/
│
├── videos/                  # Video generation
│   ├── ltx/                # LTX video files (Step 17)
│   │   └── {gender}/{age}/
│   └── interp/             # Interpolated videos (Step 18)
│       └── {gender}/{age}/
│
├── final/                   # Final output (Step 19)
│   └── {gender}/{age}/     # Ready for distribution
│
└── research/                # Research and experiments
    ├── python/             # Python research scripts
    └── csharp/             # C# research scripts
```

## Audience Organization

All content folders follow the pattern:
```
{folder}/
└── {gender}/               # men, women, etc.
    └── {age}/              # 10-14, 15-19, 20-24, etc.
        └── content files
```

This allows for precise demographic targeting and organization.

## Pipeline Stages

### Content Generation Pipeline

1. **Trends** - Process Google Trends data for trending topics
2. **Ideas** - Generate story ideas from trends
3. **Topics** - Classify and organize topics
4. **Titles** - Create engaging video titles
5. **Scores** - Quality scoring and metrics
6. **Scripts (Raw)** - Initial script generation
7. **Scripts (Iterative)** - Refined through iteration
8. **Scripts (GPT Improved)** - Enhanced with GPT
9. **Voice Choice** - Select appropriate voices
10. **Audio (TTS)** - Generate text-to-speech audio
11. **Audio (Normalized)** - Normalize audio levels
12. **Subtitles (SRT)** - Generate SRT subtitle files
13. **Subtitles (Timed)** - Create timed subtitle data
14. **Scenes** - Define scene descriptions
15. **Images (Keyframes v1)** - Generate keyframe images
16. **Images (Keyframes v2)** - Refined keyframes
17. **Videos (LTX)** - Generate LTX videos
18. **Videos (Interpolated)** - Create interpolated videos
19. **Final** - Complete videos ready for distribution

## Iterative Quality Control

Files with low quality scores are handled iteratively:

### Scoring Thresholds

- **Minimum Score (70+)**: Content passes to next stage
- **Reprocess Score (50-69)**: Content marked with underscore prefix (`_filename`) for reprocessing
- **Below Reprocess (<50)**: Content moved back to previous pipeline stage with underscore prefix

### Underscore Naming Convention

Files prefixed with `_` indicate they need reprocessing:
- `_idea_001.json` - Idea that needs improvement
- `_script_002.txt` - Script that needs revision
- `_video_003.mp4` - Video that needs regeneration

### Processing Commands

```bash
# Process quality for all content
python process_quality.py

# Process specific folder
python process_quality.py Generator/topics/men/20-24 topics ideas

# Check scores
python process_quality.py Generator/scripts/raw_local/women/15-19 scripts/raw_local topics
```

## Configuration

All configuration is managed through `Generator/config/audience_config.json`:

```json
{
  "audience": {
    "genders": [...],
    "countries": [...],
    "age_groups": [...]
  },
  "folder_structure": {
    "base_path": "Generator",
    ...
  },
  "quality_thresholds": {
    "min_score": 70,
    "reprocess_score": 50,
    "underscore_prefix": "_"
  }
}
```

## Setup

### Initial Setup

```bash
# Create the complete folder structure
python setup_folders.py

# This creates Generator/ and all subdirectories
```

### Verify Structure

```bash
# Verify all required folders exist
python verify_folders.py
```

## Git Tracking

The Generator folder uses smart git tracking:

- **Tracked**: Directory structure (`.gitkeep` files), configuration, samples
- **Ignored**: All generated content (audio, images, videos, JSON data)
- **Test Files**: Files with `.test` or `.test.*` extensions are tracked as examples

This keeps the repository clean while preserving the organizational structure.

## Migration from Old Structure

If you have content in the old root-level folders (ideas/, topics/, etc.), you can move them:

```bash
# Example: Move ideas to Generator
mv ideas/* Generator/ideas/

# Or use a script
python migrate_to_generator.py
```

## Benefits

1. **Clear Organization** - All generated content in one place
2. **Easy Navigation** - Logical folder hierarchy
3. **Git-Friendly** - Structure tracked, content ignored
4. **Scalable** - Easy to add new stages or demographics
5. **Quality Control** - Iterative refinement with underscore naming
6. **Demographic Targeting** - Organized by gender and age
7. **Pipeline Clarity** - Each stage has its own folder

## See Also

- [CONFIGURATION.md](../CONFIGURATION.md) - Configuration guide
- [FOLDER_STRUCTURE.md](../FOLDER_STRUCTURE.md) - Overall structure documentation
- [process_quality.py](../process_quality.py) - Quality processing script
- [setup_folders.py](../setup_folders.py) - Folder setup script
