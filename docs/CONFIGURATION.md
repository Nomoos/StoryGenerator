# Audience Configuration Guide

## Overview

The StoryGenerator folder structure is now fully configurable through JSON configuration files. This allows you to customize:
- Gender categories with preference percentages
- Country targeting with preference percentages
- Age groups with preference percentages (5-year ranges from 10 to 65+)
- Folder structure organization

## Configuration File Format

### Location
- Default: `config/audience_config.json`
- Test: `config/audience_config.test.json`
- Custom: Specify path as command-line argument

### Structure

```json
{
  "audience": {
    "genders": [
      {
        "name": "men",
        "preference_percentage": 50
      },
      {
        "name": "women",
        "preference_percentage": 50
      }
    ],
    "countries": [
      {
        "name": "US",
        "preference_percentage": 40
      },
      {
        "name": "UK",
        "preference_percentage": 30
      }
    ],
    "age_groups": [
      {
        "range": "10-14",
        "preference_percentage": 10
      },
      {
        "range": "15-19",
        "preference_percentage": 15
      },
      ...
      {
        "range": "65+",
        "preference_percentage": 0.2
      }
    ]
  },
  "folder_structure": {
    "content_folders": ["ideas", "topics", "titles", "scores"],
    "script_folders": ["scripts/raw_local", "scripts/iter_local", "scripts/gpt_improved"],
    ...
  }
}
```

## Audience Configuration

### Genders
- **name**: Gender category name (e.g., "men", "women", "non-binary")
- **preference_percentage**: Target percentage (0-100) for this demographic
- Percentages don't need to sum to 100, they indicate relative preference

### Countries
- **name**: Country code or name (e.g., "US", "UK", "CA", "AU")
- **preference_percentage**: Target percentage (0-100) for this market
- Use to target specific geographical regions

### Age Groups
- **range**: Age range in format "XX-YY" or "XX+" for open-ended
- **preference_percentage**: Target percentage (0-100) for this age group
- Default configuration includes:
  - 10-14 (Pre-teen)
  - 15-19 (Teen)
  - 20-24 (Young adult)
  - 25-29 (Adult)
  - 30-34 (Adult)
  - 35-39 (Mid-adult)
  - 40-44 (Mid-adult)
  - 45-49 (Mature)
  - 50-54 (Mature)
  - 55-59 (Senior)
  - 60-64 (Senior)
  - 65+ (Senior+)

## Folder Structure Configuration

### Content Folders
Folders organized by gender and age group:
- `content_folders`: General content (ideas, topics, titles, scores)
- `script_folders`: Script variants at different stages
- `voice_folders`: Voice selection and configuration
- `audio_folders`: Audio files (TTS, normalized)
- `subtitle_folders`: Subtitle files (SRT, timed)
- `scene_folders`: Scene descriptions
- `image_folders`: Image assets (keyframes)
- `video_folders`: Video files (LTX, interpolated)
- `final_folders`: Final output files

### Research Folders
Technology-specific research folders:
- `research_folders`: e.g., ["research/python", "research/csharp"]

### Simple Folders
Folders without gender/age structure:
- `simple_folders`: e.g., ["config"]

## Usage

### Python

**Default configuration:**
```bash
python setup_folders.py
```

**Custom configuration:**
```bash
python setup_folders.py path/to/config.json
```

**Test configuration:**
```bash
python setup_folders.py config/audience_config.test.json
```

### C#

**Default configuration:**
```bash
csc CSharp/Tools/SetupFolders.cs
./SetupFolders.exe
```

**Custom configuration (run parameter):**
```bash
./SetupFolders.exe path/to/config.json
```

**Test configuration (run parameter):**
```bash
./SetupFolders.exe config/audience_config.test.json
```

## Test Configuration

The test configuration (`audience_config.test.json`) is a minimal setup for testing:
- Limited genders (70% men, 30% women)
- Limited countries (80% US, 20% UK)
- Limited age groups (20-24, 25-29, 30-34)
- Limited folder structure (ideas, topics, scripts/raw_local)

Use this for:
- Quick testing
- Development environments
- CI/CD pipelines
- Minimal setup validation

## Examples

### Example 1: Youth-Focused Content

```json
{
  "audience": {
    "genders": [
      {"name": "all", "preference_percentage": 100}
    ],
    "countries": [
      {"name": "US", "preference_percentage": 100}
    ],
    "age_groups": [
      {"range": "10-14", "preference_percentage": 30},
      {"range": "15-19", "preference_percentage": 70}
    ]
  },
  "folder_structure": {
    "content_folders": ["ideas", "topics"],
    "simple_folders": ["config"]
  }
}
```

### Example 2: Adult Professional Content

```json
{
  "audience": {
    "genders": [
      {"name": "men", "preference_percentage": 60},
      {"name": "women", "preference_percentage": 40}
    ],
    "countries": [
      {"name": "US", "preference_percentage": 50},
      {"name": "UK", "preference_percentage": 30},
      {"name": "EU", "preference_percentage": 20}
    ],
    "age_groups": [
      {"range": "25-29", "preference_percentage": 20},
      {"range": "30-34", "preference_percentage": 30},
      {"range": "35-39", "preference_percentage": 30},
      {"range": "40-44", "preference_percentage": 20}
    ]
  }
}
```

### Example 3: Senior Content

```json
{
  "audience": {
    "genders": [
      {"name": "all", "preference_percentage": 100}
    ],
    "age_groups": [
      {"range": "55-59", "preference_percentage": 20},
      {"range": "60-64", "preference_percentage": 30},
      {"range": "65+", "preference_percentage": 50}
    ]
  }
}
```

## Best Practices

1. **Preference Percentages**: Use percentages to indicate relative importance, not strict quotas
2. **Age Groups**: Keep 5-year ranges for consistency
3. **Testing**: Use test configuration for development
4. **Validation**: Script validates JSON structure automatically
5. **Backup**: Keep a backup of working configurations
6. **Version Control**: Track configurations in git
7. **Documentation**: Document custom configurations

## Troubleshooting

### Config file not found
- Check file path is correct
- Ensure file is in correct location
- Script will create default config if not found

### JSON parsing error
- Validate JSON syntax (use online validator)
- Check for missing commas or brackets
- Verify all field names are correct

### Folder structure issues
- Run verify script after setup
- Check permissions on target directory
- Ensure sufficient disk space

## Migration from Old Structure

Old hardcoded structure (10-13, 14-17, 18-23, 24-30) can be recreated with:

```json
{
  "audience": {
    "age_groups": [
      {"range": "10-13", "preference_percentage": 25},
      {"range": "14-17", "preference_percentage": 25},
      {"range": "18-23", "preference_percentage": 25},
      {"range": "24-30", "preference_percentage": 25}
    ]
  }
}
```

Note: This is not included in default config as the new structure uses standard 5-year ranges.

## See Also

- `FOLDER_STRUCTURE.md` - Overall folder structure documentation
- `TEST_FILES.md` - Test file system documentation
- `audience_config.json` - Default configuration file
- `audience_config.test.json` - Test configuration file
