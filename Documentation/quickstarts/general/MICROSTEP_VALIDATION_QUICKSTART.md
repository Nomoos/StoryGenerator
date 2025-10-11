# Microstep Validation - Quick Reference

## Quick Start

### Installation
```bash
# Already included in src/Python/Tools/
# No additional installation needed
```

### Basic Usage
```python
from Tools.MicrostepValidator import MicrostepValidator

validator = MicrostepValidator()
validator.list_microsteps()  # Show all 19 steps
```

## Common Operations

### 1. Complete Workflow for a Microstep

```python
from Tools.MicrostepValidator import (
    create_microstep_artifact,
    log_microstep_config,
    update_microstep_progress,
    copilot_check_microstep
)

step = 2  # Ideas generation
gender = "women"
age = "18-23"

# Start
update_microstep_progress(step, "started", "Starting...", gender, age)

# Log config
log_microstep_config(step, gender=gender, age=age)

# Create artifacts
idea = {"id": "idea_001", "title": "Story idea", "viral_potential": 85}
create_microstep_artifact(step, "idea_001.json", idea, gender, age)

# Complete
update_microstep_progress(
    step, "completed", "Done!", gender, age,
    artifacts=["idea_001.json"]
)

# Validate
copilot_check_microstep(step, gender, age)
```

### 2. Single Artifact Creation

```python
from Tools.MicrostepValidator import create_microstep_artifact

# Create JSON artifact
create_microstep_artifact(
    step_number=2,
    artifact_name="idea.json",
    content={"id": "001", "title": "My Idea"},
    gender="women",
    age="18-23"
)

# Create text artifact
create_microstep_artifact(
    step_number=6,
    artifact_name="script.txt",
    content="This is my script content...",
    gender="men",
    age="24-29"
)
```

### 3. Log Configuration Only

```python
from Tools.MicrostepValidator import log_microstep_config

# Auto-extract relevant config
log_microstep_config(2, gender="women", age="18-23")

# Or provide custom config
custom_config = {"model": "gpt-4", "temperature": 0.7}
log_microstep_config(2, config_subset=custom_config, gender="women", age="18-23")
```

### 4. Update Progress Only

```python
from Tools.MicrostepValidator import update_microstep_progress

# Simple status update
update_microstep_progress(2, "started", "Beginning generation")

# With demographic info
update_microstep_progress(
    2, "in_progress", "Generated 10 ideas", "women", "18-23"
)

# With artifacts list
update_microstep_progress(
    2, "completed", "All done!", "women", "18-23",
    artifacts=["idea_001.json", "idea_002.json"]
)
```

### 5. Validate Only

```python
from Tools.MicrostepValidator import copilot_check_microstep

# Quick validation check
copilot_check_microstep(2, "women", "18-23")

# Or get detailed report
from Tools.MicrostepValidator import MicrostepValidator
validator = MicrostepValidator()
report = validator.validate_step(2, "women", "18-23")
print(f"Valid: {report['is_valid']}")
print(f"Artifacts: {len(report['artifacts'])}")
```

## All 19 Microsteps

| # | Name | Folder | Use Case |
|---|------|--------|----------|
| 1 | trends | trends | Google Trends processing |
| 2 | ideas | ideas | Story idea generation |
| 3 | topics | topics | Topic classification |
| 4 | titles | titles | Video title creation |
| 5 | scores | scores | Quality scoring |
| 6 | scripts_raw | scripts/raw_local | Initial scripts |
| 7 | scripts_iter | scripts/iter_local | Refined scripts |
| 8 | scripts_gpt | scripts/gpt_improved | GPT-improved scripts |
| 9 | voice_choice | voices/choice | Voice selection |
| 10 | audio_tts | audio/tts | TTS generation |
| 11 | audio_normalized | audio/normalized | Audio normalization |
| 12 | subtitles_srt | subtitles/srt | SRT generation |
| 13 | subtitles_timed | subtitles/timed | Timed subtitles |
| 14 | scenes | scenes/json | Scene descriptions |
| 15 | keyframes_v1 | images/keyframes_v1 | First keyframes |
| 16 | keyframes_v2 | images/keyframes_v2 | Refined keyframes |
| 17 | videos_ltx | videos/ltx | LTX videos |
| 18 | videos_interp | videos/interp | Interpolated videos |
| 19 | final | final | Final output |

## Status Values

Use these standard status values for consistency:
- `"started"` - Process has begun
- `"in_progress"` - Currently processing
- `"completed"` - Successfully finished
- `"failed"` - Process failed
- `"validated"` - Passed validation

## File Structure Created

```
src/Generator/
└── {microstep_folder}/
    └── {gender}/
        └── {age}/
            ├── artifact_001.json        # Your artifacts
            ├── artifact_002.json
            ├── config_{name}_{timestamp}.yaml  # Config log
            ├── progress.md              # Progress tracking
            └── validation_report_{timestamp}.json  # Validation report
```

## Integration Pattern

### For New Generators

```python
def my_generator_function(gender: str, age: str):
    from Tools.MicrostepValidator import (
        log_microstep_config,
        update_microstep_progress,
        create_microstep_artifact,
        copilot_check_microstep
    )
    
    step = 2  # Your step number
    
    # Start
    update_microstep_progress(step, "started", "Starting generation", gender, age)
    log_microstep_config(step, gender=gender, age=age)
    
    try:
        # Your generation logic here
        results = generate_content(gender, age)
        
        # Save artifacts
        artifacts = []
        for i, result in enumerate(results):
            path = create_microstep_artifact(
                step, f"result_{i:03d}.json", result, gender, age
            )
            artifacts.append(path.name)
        
        # Complete
        update_microstep_progress(
            step, "completed", f"Generated {len(results)} items",
            gender, age, artifacts=artifacts
        )
        
    except Exception as e:
        # Failed
        update_microstep_progress(
            step, "failed", f"Error: {str(e)}", gender, age
        )
        raise
    
    # Validate
    return copilot_check_microstep(step, gender, age)
```

## Running Tests

```bash
# Run test suite
python tests/test_microstep_validator.py

# Run demo
python examples/microstep_validation_demo.py
```

## Validation Output Example

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
  - config_ideas_20240101.yaml
  - progress.md
  - validation_report_20240101.json

============================================================
Overall Status: ✅ VALID
============================================================
```

## Troubleshooting

### Problem: Config file not found
**Solution:** Ensure `data/config/pipeline.yaml` exists or provide custom path

### Problem: Permission denied
**Solution:** Check write permissions on `src/Generator/` directory

### Problem: Validation fails
**Solution:** Check validation report for specific failures:
```python
report = validator.validate_step(step, gender, age)
print(report['checks'])  # See which checks failed
```

## Full Documentation

See [MICROSTEP_VALIDATION.md](../docs/MICROSTEP_VALIDATION.md) for complete documentation.
