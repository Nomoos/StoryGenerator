# Configuration Files

This directory contains YAML configuration files for the StoryGenerator pipeline.

## Files

### pipeline.yaml

Main pipeline configuration including:
- **Models**: LLM, Vision, TTS, ASR, Image, and Video generation models
- **Video Settings**: Resolution (1080x1920), FPS (30), safe margins
- **Audio Settings**: Target LUFS (-14), sample rate (48000)
- **Seeds**: Reproducible generation with image, video, and LLM seeds
- **Paths**: Model weights, cache, and temporary files
- **Switches**: Feature flags (LTX video, interpolation)
- **APIs**: External service configurations (Reddit, YouTube)

### scoring.yaml

Content scoring and quality assessment configuration:
- **Viral Scoring**: Weights for novelty, emotional impact, clarity, replay value, and shareability
- **Thresholds**: Quality levels (excellent: 85+, good: 70+, acceptable: 55+, poor: 40+)
- **Title Scoring**: Length constraints, question preference, bonus keywords
- **Script Scoring**: Duration targets, narrative arc, pacing, hook, and resolution weights

## Usage

Load configuration in Python:
```python
import yaml

with open('config/pipeline.yaml', 'r') as f:
    pipeline_config = yaml.safe_load(f)

with open('config/scoring.yaml', 'r') as f:
    scoring_config = yaml.safe_load(f)
```

Load configuration in C#:
```csharp
// Use YamlDotNet or similar library
var deserializer = new DeserializerBuilder().Build();
var pipelineConfig = deserializer.Deserialize<PipelineConfig>(
    File.ReadAllText("config/pipeline.yaml"));
```

## Environment Variables

API keys and sensitive values use environment variable substitution (e.g., `${REDDIT_CLIENT_ID}`).

Set environment variables before running:
```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export YOUTUBE_API_KEY="your_api_key"
```

## Validation

Validate YAML files:
```bash
# Using Python
python -c "import yaml; yaml.safe_load(open('config/pipeline.yaml'))"
python -c "import yaml; yaml.safe_load(open('config/scoring.yaml'))"

# Check viral weights sum to 1.0
python -c "import yaml; c=yaml.safe_load(open('config/scoring.yaml')); print(sum(c['viral'].values()))"
```
