# Setup: Configuration Files (YAML)

**ID:** `00-setup-02`  
**Priority:** P0 (Critical Path)  
**Effort:** 2-3 hours  
**Status:** Not Started

## Overview

Create the base configuration files (`pipeline.yaml` and `scoring.yaml`) that define models, paths, seeds, and scoring rubrics for the entire pipeline.

## Dependencies

**Requires:**
- `00-setup-01`: Repository folder structure must exist

**Blocks:**
- All content generation tasks (need config)
- All research prototypes (need model definitions)

## Acceptance Criteria

- [ ] `/config/pipeline.yaml` created with all required keys
- [ ] `/config/scoring.yaml` created with viral scoring weights
- [ ] YAML files are valid and parseable
- [ ] Test script can load both configs
- [ ] Documentation added to config files

## Task Details

### File 1: `/config/pipeline.yaml`

```yaml
# StoryGenerator Pipeline Configuration

models:
  # Local LLM for content generation
  llm: qwen2_5_14b  # Options: qwen2_5_14b | llama3_1_8b
  
  # Vision model for image understanding (optional)
  vision: llava_onevision_7b  # Options: llava_onevision_7b | phi_3_5_vision
  
  # Text-to-speech engine
  tts: local_tts_engine_name  # TODO: Define specific TTS model
  
  # Automatic speech recognition
  asr: faster-whisper-large-v3
  
  # Image generation
  image: sdxl_base_refiner
  
  # Video generation
  video: ltx_video_2b  # Options: ltx_video_2b | ltx_video_13b | stable_video_diffusion

video:
  width: 1080
  height: 1920
  fps: 30
  safe_margins_pct:
    top: 8
    bottom: 10

audio:
  target_lufs: -14
  sample_rate: 48000

seeds:
  image: 1234
  video: 5678
  llm: 42

paths:
  weights: ./models/weights
  cache: ./models/cache
  tmp: ./tmp

switches:
  use_ltx: true
  use_interpolation: false

# API Keys (use environment variables in production)
apis:
  reddit:
    client_id: ${REDDIT_CLIENT_ID}
    client_secret: ${REDDIT_CLIENT_SECRET}
    user_agent: "StoryGenerator/1.0"
  
  youtube:
    api_key: ${YOUTUBE_API_KEY}
  
  # Add other API configs as needed
```

### File 2: `/config/scoring.yaml`

```yaml
# Viral Scoring Configuration

viral:
  # Weights must sum to 1.0
  novelty: 0.25      # Unique, surprising content
  emotional: 0.25    # Emotional impact and resonance
  clarity: 0.20      # Clear, easy to understand
  replay: 0.15       # Rewatchability factor
  share: 0.15        # Shareability and virality

# Scoring thresholds
thresholds:
  excellent: 85      # Top-tier content
  good: 70           # Solid, publishable
  acceptable: 55     # Needs improvement
  poor: 40           # Significant rework needed

# Title scoring specifics
title:
  max_length: 100
  min_length: 20
  prefer_questions: true
  bonus_keywords:
    - "secret"
    - "truth"
    - "revealed"
    - "shocking"
    - "amazing"

# Script scoring specifics
script:
  ideal_duration_seconds: 45
  min_duration_seconds: 30
  max_duration_seconds: 60
  narrative_arc_weight: 0.3
  pacing_weight: 0.2
  hook_weight: 0.25
  resolution_weight: 0.25
```

### Implementation

Create the files and test:

```python
#!/usr/bin/env python3
"""Validate configuration files."""

import yaml
from pathlib import Path

def validate_pipeline_config():
    """Validate pipeline.yaml structure."""
    config_path = Path("config/pipeline.yaml")
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    required_keys = ["models", "video", "audio", "seeds", "paths", "switches"]
    for key in required_keys:
        assert key in config, f"Missing key: {key}"
    
    # Validate model choices
    assert config["models"]["llm"] in ["qwen2_5_14b", "llama3_1_8b"]
    assert config["models"]["asr"] == "faster-whisper-large-v3"
    
    # Validate video settings
    assert config["video"]["width"] == 1080
    assert config["video"]["height"] == 1920
    assert config["video"]["fps"] == 30
    
    # Validate audio
    assert config["audio"]["target_lufs"] == -14
    assert config["audio"]["sample_rate"] == 48000
    
    print("✅ pipeline.yaml is valid")

def validate_scoring_config():
    """Validate scoring.yaml structure."""
    config_path = Path("config/scoring.yaml")
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Check viral weights sum to 1.0
    viral = config["viral"]
    total = sum(viral.values())
    assert abs(total - 1.0) < 0.01, f"Weights sum to {total}, not 1.0"
    
    # Check all required weights exist
    required_weights = ["novelty", "emotional", "clarity", "replay", "share"]
    for weight in required_weights:
        assert weight in viral, f"Missing weight: {weight}"
    
    print("✅ scoring.yaml is valid")

if __name__ == "__main__":
    validate_pipeline_config()
    validate_scoring_config()
    print("\n✨ All configs valid!")
```

## Output Files

- `/config/pipeline.yaml` - Pipeline configuration
- `/config/scoring.yaml` - Scoring rubric
- `/config/README.md` - Configuration documentation

## Validation

```bash
# Test YAML parsing
python -c "import yaml; yaml.safe_load(open('config/pipeline.yaml'))"
python -c "import yaml; yaml.safe_load(open('config/scoring.yaml'))"

# Run validation script
python scripts/validate_config.py
```

## Related Files

- `tests/test_config.py` - Existing config tests
- `docs/CONFIGURATION.md` - Config documentation

## Notes

- Use environment variables for API keys in production
- Seeds can be changed for reproducibility
- Weights in scoring.yaml must sum to 1.0
- Model choices affect GPU memory requirements

## Next Steps

After completion:
- Research prototypes can use model definitions
- Content generation scripts can load configs
- Proceed to `00-setup-03-python-env`
