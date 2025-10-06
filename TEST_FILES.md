# Test Files and Git Tracking Policy

## Overview

This document explains how test files and content are managed in the StoryGenerator repository.

## File Tracking Policy

### Ignored Files (Not Tracked in Git)

The following file types are **completely ignored** and will never be committed to git:

#### Media Files
- **Audio files**: `*.mp3`, `*.wav`, `*.flac`, `*.aac`, `*.ogg`, `*.m4a`, `*.wma`
- **Image files**: `*.jpg`, `*.jpeg`, `*.png`, `*.gif`, `*.bmp`, `*.svg`, `*.webp`, `*.ico`, `*.tiff`, `*.tif`
- **Video files**: `*.mp4`, `*.avi`, `*.mov`, `*.wmv`, `*.flv`, `*.mkv`, `*.webm`, `*.m4v`, `*.mpg`, `*.mpeg`

#### Content Files
- All regular content files in the following directories are ignored:
  - `ideas/`
  - `topics/`
  - `titles/`
  - `scores/`
  - `scripts/`
  - `voices/`
  - `audio/`
  - `subtitles/`
  - `scenes/`
  - `images/`
  - `videos/`
  - `final/`

### Tracked Files (Committed to Git)

The following files **are tracked** in git:

1. **`.gitkeep` files**: Preserve directory structure
2. **`.test` files**: Flag files indicating test/example folders
3. **Test/Sample files with `.test` extension**:
   - `.test.json` - Sample JSON files
   - `.test.txt` - Sample text files
   - `.test.srt` - Sample subtitle files

## Test Folder Structure

Folders containing test/example data include a `.test` flag file. This indicates:
- The folder contains sample/demonstration data
- Files with `.test.*` extensions are example files
- These files are safe to commit to git for documentation purposes

### Example Test Folders

```
topics/
├── women/
│   └── 10-13/
│       ├── .gitkeep          # Preserves folder in git
│       ├── .test              # Flags this as a test folder
│       ├── .test.json         # Sample topic (JSON format)
│       ├── .test.txt          # Sample topic (text format)
│       └── actual_topic.json  # IGNORED by git
└── men/
    └── 14-17/
        ├── .gitkeep
        ├── .test
        ├── .test.json
        └── real_topic.json    # IGNORED by git
```

## Usage Guidelines

### For Developers

1. **Adding Test Examples**: Create files with `.test` extension (e.g., `example.test.json`)
2. **Working with Real Content**: Create regular files (e.g., `my_topic.json`) - these are auto-ignored
3. **Marking Test Folders**: Add a `.test` file to indicate the folder contains examples

### For Contributors

When adding new test examples:

```bash
# Create a test folder flag
echo "Test folder" > ideas/women/18-23/.test

# Add sample files
cp your_example.json ideas/women/18-23/.test.json
cp your_example.txt ideas/women/18-23/.test.txt
```

### Checking What Gets Committed

```bash
# See what files will be tracked
git status

# Test that media files are ignored
touch audio/tts/women/10-13/test.mp3
git status  # Should not show test.mp3

# Test that .test files are tracked
touch topics/women/10-13/example.test.json
git status  # Should show example.test.json
```

## Benefits

1. **Clean Repository**: No large media files in git history
2. **Example Files**: Developers can see sample data format
3. **Structure Preservation**: Empty folders are maintained
4. **Easy Testing**: Clear indication of what folders contain test data

## Current Test Folders

The repository includes test examples in:
- `topics/women/10-13/` - AI technology topic for pre-teen girls
- `topics/men/14-17/` - Space exploration topic for teenage boys
- `ideas/women/18-23/` - Mystery story idea for young adult women
- `scripts/raw_local/men/24-30/` - Quantum computing script for adult men
- `subtitles/srt/women/14-17/` - Sample SRT subtitle file

## See Also

- `.gitignore` - Complete list of ignored file patterns
- `FOLDER_STRUCTURE.md` - Detailed folder structure documentation
- `setup_folders.py` - Script to create folder structure
