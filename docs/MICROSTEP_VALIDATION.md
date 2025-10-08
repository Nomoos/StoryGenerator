# Microstep Validation System

## Overview

The Microstep Validation System provides a comprehensive framework for tracking, validating, and documenting the progress of each stage in the StoryGenerator pipeline. This system ensures that every microstep creates proper artifacts, logs its configuration, tracks progress, and can be validated for completeness.

## Features

### 1. **Artifact Creation**
Each microstep can create artifacts in its designated folder:
- JSON files for structured data
- Text files for scripts, descriptions, etc.
- Metadata files for tracking generation parameters

### 2. **Configuration Logging**
Automatically logs the relevant configuration subset used for each microstep:
- Extracts only the relevant config sections for each step
- Timestamps each configuration snapshot
- Saves in YAML format for easy reading

### 3. **Progress Tracking**
Maintains a running `progress.md` file in each microstep folder:
- Timestamps each update
- Tracks status changes (started, in_progress, completed, failed)
- Lists artifacts created
- Records execution details

### 4. **Validation Interface**
Provides a `@copilot check` command to validate microstep completion:
- Verifies folder structure exists
- Confirms artifacts are present
- Checks for configuration logs
- Validates progress tracking
- Generates validation reports

## Pipeline Microsteps

The system supports all 19 pipeline microsteps:

| # | Name | Folder | Description |
|---|------|--------|-------------|
| 1 | trends | trends | Process Google Trends data |
| 2 | ideas | ideas | Generate story ideas |
| 3 | topics | topics | Classify and organize topics |
| 4 | titles | titles | Create engaging video titles |
| 5 | scores | scores | Quality scoring and metrics |
| 6 | scripts_raw | scripts/raw_local | Initial script generation |
| 7 | scripts_iter | scripts/iter_local | Iteratively refined scripts |
| 8 | scripts_gpt | scripts/gpt_improved | GPT-improved scripts |
| 9 | voice_choice | voices/choice | Voice selection |
| 10 | audio_tts | audio/tts | Text-to-speech audio |
| 11 | audio_normalized | audio/normalized | Normalized audio |
| 12 | subtitles_srt | subtitles/srt | SRT subtitle files |
| 13 | subtitles_timed | subtitles/timed | Timed subtitle data |
| 14 | scenes | scenes/json | Scene descriptions |
| 15 | keyframes_v1 | images/keyframes_v1 | Keyframe images v1 |
| 16 | keyframes_v2 | images/keyframes_v2 | Keyframe images v2 |
| 17 | videos_ltx | videos/ltx | LTX video files |
| 18 | videos_interp | videos/interp | Interpolated videos |
| 19 | final | final | Final output |

## Installation

The MicrostepValidator is included in the `src/Python/Tools/` directory. No additional installation is required beyond the standard StoryGenerator dependencies.

```bash
# Ensure you have the required dependencies
pip install pyyaml
```

## Quick Start

### Basic Usage

```python
from Tools.MicrostepValidator import MicrostepValidator

# Initialize the validator
validator = MicrostepValidator()

# List all available microsteps
validator.list_microsteps()
```

### Complete Workflow for a Microstep

```python
from Tools.MicrostepValidator import (
    create_microstep_artifact,
    log_microstep_config,
    update_microstep_progress,
    copilot_check_microstep
)

# Step number and target audience
step = 2  # Ideas generation
gender = "women"
age = "18-23"

# 1. Start the process
update_microstep_progress(
    step_number=step,
    status="started",
    details="Beginning idea generation with GPT-4",
    gender=gender,
    age=age
)

# 2. Log configuration
log_microstep_config(
    step_number=step,
    gender=gender,
    age=age
)

# 3. Create artifacts
idea_data = {
    "id": "idea_001",
    "title": "A mysterious letter arrives",
    "description": "A woman receives a letter that reveals a family secret",
    "viral_potential": 85
}

create_microstep_artifact(
    step_number=step,
    artifact_name="idea_001.json",
    content=idea_data,
    gender=gender,
    age=age
)

# 4. Update progress with completion
update_microstep_progress(
    step_number=step,
    status="completed",
    details="Generated 20 high-quality ideas",
    gender=gender,
    age=age,
    artifacts=["idea_001.json", "idea_002.json", "config_ideas_20240101.yaml"]
)

# 5. Validate the microstep
copilot_check_microstep(step, gender, age)
```

## API Reference

### MicrostepValidator Class

#### Constructor

```python
validator = MicrostepValidator(base_path=None, config_path=None)
```

**Parameters:**
- `base_path` (str, optional): Base path for Generator folder. Default: `src/Generator`
- `config_path` (str, optional): Path to pipeline.yaml. Default: `data/config/pipeline.yaml`

#### Methods

##### create_artifact()

Creates an artifact file for a microstep.

```python
artifact_path = validator.create_artifact(
    step_number=2,
    artifact_name="idea_001.json",
    content={"id": "idea_001", "title": "Sample Idea"},
    gender="women",
    age="18-23"
)
```

**Parameters:**
- `step_number` (int): Microstep number (1-19)
- `artifact_name` (str): Name of the artifact file
- `content` (Any): Content to write (dict/list → JSON, str → text)
- `gender` (str, optional): Target gender
- `age` (str, optional): Target age group

**Returns:** `Path` to the created artifact

##### log_config()

Logs the configuration used for a microstep.

```python
config_path = validator.log_config(
    step_number=2,
    config_subset=None,  # Auto-extracts if None
    gender="women",
    age="18-23"
)
```

**Parameters:**
- `step_number` (int): Microstep number (1-19)
- `config_subset` (dict, optional): Custom config to log
- `gender` (str, optional): Target gender
- `age` (str, optional): Target age group

**Returns:** `Path` to the config log file

##### update_progress()

Updates the progress.md file for a microstep.

```python
progress_path = validator.update_progress(
    step_number=2,
    status="completed",
    details="Successfully generated ideas",
    gender="women",
    age="18-23",
    artifacts=["idea_001.json", "idea_002.json"]
)
```

**Parameters:**
- `step_number` (int): Microstep number (1-19)
- `status` (str): Status (e.g., 'started', 'completed', 'failed')
- `details` (str, optional): Additional details
- `gender` (str, optional): Target gender
- `age` (str, optional): Target age group
- `artifacts` (list, optional): List of artifact filenames

**Returns:** `Path` to the progress.md file

##### validate_step()

Validates a microstep's completion and artifacts.

```python
report = validator.validate_step(
    step_number=2,
    gender="women",
    age="18-23",
    validation_checks=None
)
```

**Parameters:**
- `step_number` (int): Microstep number (1-19)
- `gender` (str, optional): Target gender
- `age` (str, optional): Target age group
- `validation_checks` (dict, optional): Custom validation checks

**Returns:** Validation report as a dictionary

**Report Structure:**
```python
{
    "step_number": 2,
    "step_name": "ideas",
    "description": "Generate story ideas",
    "folder": "/path/to/folder",
    "timestamp": "2024-01-01T12:00:00",
    "checks": {
        "folder_exists": True,
        "has_artifacts": True,
        "has_progress": True,
        "has_config": True
    },
    "artifacts": ["idea_001.json", "config_ideas.yaml", "progress.md"],
    "is_valid": True
}
```

##### copilot_check()

Performs a @copilot check for a microstep.

```python
summary = validator.copilot_check(
    step_number=2,
    gender="women",
    age="18-23"
)
```

**Parameters:**
- `step_number` (int): Microstep number (1-19)
- `gender` (str, optional): Target gender
- `age` (str, optional): Target age group

**Returns:** Formatted validation summary as a string

**Output Example:**
```
============================================================
@copilot CHECK - Step 2: ideas
============================================================

📁 Folder: /path/to/Generator/ideas/women/18-23
📅 Timestamp: 2024-01-01T12:00:00

✅ Validation Checks:
  ✅ Folder Exists: True
  ✅ Has Artifacts: True
  ✅ Has Progress: True
  ✅ Has Config: True

📦 Artifacts (5):
  - idea_001.json
  - idea_002.json
  - config_ideas_20240101_120000.yaml
  - progress.md
  - validation_report_20240101_120000.json

============================================================
Overall Status: ✅ VALID
============================================================
```

##### list_microsteps()

Lists all available microsteps with their descriptions.

```python
validator.list_microsteps()
```

**Returns:** Formatted list as a string (also prints to console)

### Convenience Functions

For quick one-off operations, use these convenience functions:

```python
from Tools.MicrostepValidator import (
    create_microstep_artifact,
    log_microstep_config,
    update_microstep_progress,
    copilot_check_microstep
)

# Create artifact
create_microstep_artifact(2, "idea.json", content_dict, "women", "18-23")

# Log config
log_microstep_config(2, gender="women", age="18-23")

# Update progress
update_microstep_progress(2, "completed", "Done!", "women", "18-23")

# Perform check
copilot_check_microstep(2, "women", "18-23")
```

## Usage Examples

### Example 1: Ideas Generation (Step 2)

```python
from Tools.MicrostepValidator import MicrostepValidator

validator = MicrostepValidator()
step = 2
gender = "women"
age = "18-23"

# Start
validator.update_progress(step, "started", "Generating ideas", gender, age)

# Log config
validator.log_config(step, gender=gender, age=age)

# Create ideas
for i in range(1, 21):
    idea = {
        "id": f"idea_{i:03d}",
        "title": f"Story Idea {i}",
        "viral_potential": 75 + i
    }
    validator.create_artifact(step, f"idea_{i:03d}.json", idea, gender, age)

# Complete
validator.update_progress(
    step, "completed",
    "Generated 20 ideas with avg viral potential of 85",
    gender, age,
    artifacts=[f"idea_{i:03d}.json" for i in range(1, 21)]
)

# Validate
validator.copilot_check(step, gender, age)
```

### Example 2: Audio TTS (Step 10)

```python
from Tools.MicrostepValidator import MicrostepValidator

validator = MicrostepValidator()
step = 10
gender = "men"
age = "24-29"

# Start
validator.update_progress(step, "started", "Initializing ElevenLabs TTS", gender, age)

# Log config with custom subset
custom_config = {
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "model": "eleven_multilingual_v2",
    "stability": 0.5,
    "similarity_boost": 0.75
}
validator.log_config(step, config_subset=custom_config, gender=gender, age=age)

# Create audio metadata
audio_meta = {
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "duration": 45.3,
    "format": "mp3",
    "bitrate": "128kbps"
}
validator.create_artifact(step, "audio_metadata.json", audio_meta, gender, age)

# Complete
validator.update_progress(
    step, "completed",
    "Audio generated successfully",
    gender, age,
    artifacts=["audio.mp3", "audio_metadata.json"]
)

# Validate
validator.copilot_check(step, gender, age)
```

### Example 3: Batch Processing Multiple Audiences

```python
from Tools.MicrostepValidator import MicrostepValidator

validator = MicrostepValidator()
step = 4  # Titles

audiences = [
    ("women", "18-23"),
    ("women", "24-29"),
    ("men", "18-23"),
    ("men", "24-29")
]

for gender, age in audiences:
    # Process each audience
    validator.update_progress(step, "started", f"Generating titles", gender, age)
    validator.log_config(step, gender=gender, age=age)
    
    # Create titles
    title_data = {
        "id": f"title_{gender}_{age}",
        "title": "Amazing Story Title",
        "viral_score": 88
    }
    validator.create_artifact(step, "title.json", title_data, gender, age)
    
    validator.update_progress(
        step, "completed",
        "Generated viral title",
        gender, age,
        artifacts=["title.json"]
    )
    
    # Validate
    report = validator.validate_step(step, gender, age)
    print(f"{gender}/{age}: {'✅' if report['is_valid'] else '❌'}")
```

## File Structure

After using the validation system, your folders will look like this:

```
src/Generator/
├── ideas/
│   └── women/
│       └── 18-23/
│           ├── idea_001.json                    # Artifacts
│           ├── idea_002.json
│           ├── config_ideas_20240101_120000.yaml  # Config log
│           ├── progress.md                      # Progress tracking
│           └── validation_report_20240101.json  # Validation report
│
├── audio/
│   └── tts/
│       └── men/
│           └── 24-29/
│               ├── audio.mp3                    # Audio file
│               ├── audio_metadata.json          # Metadata
│               ├── config_audio_tts_20240101.yaml
│               ├── progress.md
│               └── validation_report_20240101.json
│
└── [other microstep folders...]
```

## Progress.md Format

The `progress.md` file follows this format:

```markdown
# Progress Log - Step 2: ideas

**Folder:** `ideas`
**Target Audience:** women/18-23

---

## 2024-01-01 12:00:00 - Step 2: ideas - STARTED
**Description:** Generate story ideas
**Target:** women/18-23
**Details:** Beginning idea generation with GPT-4

---

## 2024-01-01 12:15:30 - Step 2: ideas - IN_PROGRESS
**Description:** Generate story ideas
**Target:** women/18-23
**Details:** Generated 10 ideas so far
**Artifacts Created:**
- `idea_001.json`
- `idea_002.json`
- `idea_003.json`

---

## 2024-01-01 12:30:00 - Step 2: ideas - COMPLETED
**Description:** Generate story ideas
**Target:** women/18-23
**Details:** Successfully generated 20 ideas with high viral potential
**Artifacts Created:**
- `idea_001.json`
- `idea_002.json`
- ...
- `config_ideas_20240101_120000.yaml`

---
```

## Integration with Existing Pipeline

### Integrating with Python Generators

```python
from Generators.GStoryIdeas import StoryIdeaGenerator
from Tools.MicrostepValidator import MicrostepValidator

def generate_ideas_with_validation(gender: str, age: str):
    """Generate ideas with built-in validation."""
    validator = MicrostepValidator()
    step = 2
    
    # Start
    validator.update_progress(step, "started", "Generating ideas", gender, age)
    validator.log_config(step, gender=gender, age=age)
    
    try:
        # Your existing generation logic
        generator = StoryIdeaGenerator()
        ideas = generator.generate(gender, age)
        
        # Create artifacts
        artifacts = []
        for i, idea in enumerate(ideas, 1):
            path = validator.create_artifact(
                step, f"idea_{i:03d}.json", idea, gender, age
            )
            artifacts.append(path.name)
        
        # Complete
        validator.update_progress(
            step, "completed",
            f"Generated {len(ideas)} ideas",
            gender, age,
            artifacts=artifacts
        )
        
    except Exception as e:
        # Failed
        validator.update_progress(
            step, "failed",
            f"Error: {str(e)}",
            gender, age
        )
        raise
    
    # Validate
    return validator.copilot_check(step, gender, age)
```

### Integrating with C# Pipeline

Call the validation from C# using Python interop:

```csharp
// C# code
var pythonScript = "python -c \"from Tools.MicrostepValidator import copilot_check_microstep; " +
                   $"copilot_check_microstep({stepNumber}, '{gender}', '{age}')\"";

var process = Process.Start(new ProcessStartInfo
{
    FileName = "python",
    Arguments = pythonScript,
    UseShellExecute = false,
    RedirectStandardOutput = true
});

var output = process.StandardOutput.ReadToEnd();
Console.WriteLine(output);
```

## Best Practices

### 1. **Always Log Configuration**
Log the configuration at the start of each microstep to ensure reproducibility.

```python
validator.log_config(step_number, gender=gender, age=age)
```

### 2. **Track Progress Frequently**
Update progress at key milestones (started, in_progress, completed, failed).

```python
validator.update_progress(step, "in_progress", "Processing...", gender, age)
```

### 3. **Validate After Completion**
Always validate after completing a microstep.

```python
validator.copilot_check(step, gender, age)
```

### 4. **Use Descriptive Artifact Names**
Name artifacts clearly to indicate their purpose.

```python
# Good
validator.create_artifact(step, "idea_001_mystery_theme.json", content)

# Less clear
validator.create_artifact(step, "file1.json", content)
```

### 5. **Handle Errors Gracefully**
Track failures in the progress log.

```python
try:
    # Process
    pass
except Exception as e:
    validator.update_progress(
        step, "failed",
        f"Error: {str(e)}",
        gender, age
    )
    raise
```

## Running the Demo

A comprehensive demo is available to see all features in action:

```bash
cd /home/runner/work/StoryGenerator/StoryGenerator
python examples/microstep_validation_demo.py
```

The demo shows:
1. Basic usage and listing microsteps
2. Creating artifacts
3. Logging configuration
4. Progress tracking
5. Validation checks
6. @copilot check functionality
7. Complete workflow example
8. Batch processing multiple audiences

## Troubleshooting

### Issue: Config file not found

**Solution:** Ensure the config file exists at `data/config/pipeline.yaml` or provide a custom path:

```python
validator = MicrostepValidator(config_path="/path/to/config.yaml")
```

### Issue: Folder doesn't exist

**Solution:** The validator creates folders automatically. Ensure you have write permissions:

```python
# Folders are created automatically
validator.create_artifact(step, "file.json", content, gender, age)
```

### Issue: Validation fails

**Solution:** Check the validation report for specific failures:

```python
report = validator.validate_step(step, gender, age)
print(report['checks'])  # See which checks failed
```

## Next Steps

1. **Integrate with existing generators** - Add validation to your pipeline stages
2. **Customize validation checks** - Add domain-specific validation logic
3. **Automate batch processing** - Use the validator in your automation scripts
4. **Monitor progress** - Review `progress.md` files regularly
5. **Review validation reports** - Check validation reports before moving to the next stage

## See Also

- [GENERATOR_STRUCTURE.md](GENERATOR_STRUCTURE.md) - Folder organization
- [PIPELINE.md](PIPELINE.md) - Pipeline overview
- [MicrostepValidator.py](../src/Python/Tools/MicrostepValidator.py) - Source code
- [microstep_validation_demo.py](../examples/microstep_validation_demo.py) - Demo script
