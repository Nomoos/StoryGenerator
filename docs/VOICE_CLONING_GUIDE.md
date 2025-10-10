# Voice Cloning System Guide

Comprehensive guide for using the Voice Cloning System to create custom voices for different audience segments.

## Overview

The Voice Cloning System uses Coqui TTS to create custom voice profiles from reference audio samples. These profiles can then be used to generate voiceovers with consistent, branded voices tailored to specific demographics.

## Installation

### Prerequisites

1. **Python 3.8+** with pip
2. **CUDA/GPU** (recommended for faster processing, but CPU works too)
3. **FFmpeg** for audio processing

### Install Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# Verify TTS installation
python -c "from TTS.api import TTS; print('TTS installed successfully')"
```

## Quick Start

### 1. Basic Voice Cloning

```python
from pathlib import Path
from core.pipeline.voice_cloning import VoiceCloner

# Initialize cloner
cloner = VoiceCloner(voice_profiles_dir=Path("data/voices/cloned"))

# Clone a voice from reference audio (5-10 minutes recommended)
profile = cloner.clone_voice(
    reference_audio=Path("path/to/reference.wav"),
    voice_name="young_male_energetic",
    target_gender="Male",
    target_age="18-25",
    metadata={"style": "energetic", "accent": "american"}
)

print(f"Voice cloned: {profile.name}")
print(f"Quality score: {profile.quality_score:.2f}")
```

### 2. Generate Speech with Cloned Voice

```python
# Synthesize speech using the cloned voice
output_path = cloner.synthesize_with_voice(
    text="This is a test of the cloned voice system.",
    voice_name="young_male_energetic",
    output_path=Path("output/test_audio.wav")
)

print(f"Audio generated: {output_path}")
```

### 3. A/B Testing Multiple Voices

```python
# Compare multiple voices with the same script
results = cloner.compare_voices(
    voice_names=["young_male_energetic", "mid_female_calm", "senior_male_wise"],
    test_text="Welcome to our video series on artificial intelligence.",
    output_dir=Path("output/ab_test")
)

for voice_name, audio_path in results.items():
    print(f"{voice_name}: {audio_path}")
```

## Advanced Usage

### Demographic Filtering

Get voices for specific demographics:

```python
# Get all male voices
male_voices = cloner.get_profiles_by_demographic(gender="Male")

# Get voices for specific age group
young_adult_voices = cloner.get_profiles_by_demographic(age_bracket="18-25")

# Combined filter
young_male_voices = cloner.get_profiles_by_demographic(
    gender="Male",
    age_bracket="18-25"
)

for profile in young_male_voices:
    print(f"{profile.name}: Quality {profile.quality_score:.2f}")
```

### Voice Profile Management

#### Export Profiles

```python
# Export all profiles to a file for backup or sharing
cloner.export_profiles(Path("backups/voice_profiles_2024.json"))
```

#### Import Profiles

```python
# Import profiles from a backup or another system
cloner.import_profiles(Path("backups/voice_profiles_2024.json"))
```

### Quality Validation

Voice quality is automatically assessed during cloning:

```python
profile = cloner.clone_voice(...)

if profile.quality_score < 0.7:
    print(f"Warning: Low quality score ({profile.quality_score:.2f})")
    print("Consider using longer or higher quality reference audio")
```

## Best Practices

### Reference Audio Quality

1. **Duration**: 5-10 minutes of speech is recommended
   - Minimum: 30 seconds (acceptable for testing)
   - Optimal: 5-10 minutes (best quality)
   - More is better for quality, but diminishing returns after 10 minutes

2. **Content**: Clear, natural speech without:
   - Background noise or music
   - Multiple speakers
   - Excessive pauses or silence
   - Emotional extremes (unless desired for the target voice)

3. **Technical Quality**:
   - Sample rate: 44.1kHz or 48kHz
   - Bit depth: 16-bit or higher
   - Format: WAV or FLAC (lossless)
   - Mono or stereo (mono preferred)

### Voice Profile Organization

Organize voices by demographics:

```
data/voices/cloned/
├── male/
│   ├── 18-25/
│   │   ├── energetic_voice_profile.json
│   │   └── casual_voice_profile.json
│   ├── 26-35/
│   │   └── professional_voice_profile.json
│   └── 50+/
│       └── authoritative_voice_profile.json
└── female/
    ├── 18-25/
    ├── 26-35/
    └── 36-50/
```

### Naming Conventions

Use descriptive, consistent names:

```python
# Good naming patterns
"young_male_energetic_us"
"mid_female_calm_uk"
"senior_male_authoritative_neutral"

# Avoid
"voice1"
"test"
"my_voice"
```

## Production Workflow

### 1. Voice Library Creation

```python
from pathlib import Path
from core.pipeline.voice_cloning import VoiceCloner

# Initialize
cloner = VoiceCloner()

# Define voice profiles for your content
voice_specs = [
    {
        "ref": "references/jake_young_male.wav",
        "name": "jake_young_tech",
        "gender": "Male",
        "age": "18-25",
        "meta": {"style": "energetic", "topics": ["tech", "gaming"]}
    },
    {
        "ref": "references/sarah_mid_female.wav",
        "name": "sarah_mid_lifestyle",
        "gender": "Female",
        "age": "26-35",
        "meta": {"style": "calm", "topics": ["lifestyle", "wellness"]}
    }
]

# Clone all voices
for spec in voice_specs:
    profile = cloner.clone_voice(
        reference_audio=Path(spec["ref"]),
        voice_name=spec["name"],
        target_gender=spec["gender"],
        target_age=spec["age"],
        metadata=spec["meta"]
    )
    print(f"✓ Cloned: {profile.name} (Quality: {profile.quality_score:.2f})")

# Export for backup
cloner.export_profiles(Path("voice_library_v1.json"))
```

### 2. Content Production

```python
# Select voice based on video topic and audience
def select_voice_for_content(topic: str, target_audience: dict):
    cloner = VoiceCloner()
    
    # Get voices matching demographics
    candidates = cloner.get_profiles_by_demographic(
        gender=target_audience.get("gender"),
        age_bracket=target_audience.get("age")
    )
    
    # Filter by topic/style from metadata
    matching = [
        p for p in candidates
        if topic in p.metadata.get("topics", [])
    ]
    
    # Return highest quality match
    if matching:
        return max(matching, key=lambda p: p.quality_score)
    return None

# Use in production
voice = select_voice_for_content("tech", {"gender": "Male", "age": "18-25"})
if voice:
    cloner.synthesize_with_voice(
        text=script_content,
        voice_name=voice.name,
        output_path=Path(f"output/{video_id}_voiceover.wav")
    )
```

### 3. A/B Testing & Optimization

```python
# Test voice performance
def ab_test_voices(script_text: str, candidate_voices: list):
    cloner = VoiceCloner()
    
    results = cloner.compare_voices(
        voice_names=candidate_voices,
        test_text=script_text,
        output_dir=Path("ab_tests")
    )
    
    print(f"\nGenerated {len(results)} test variations")
    print("Listen to each and gather audience feedback:")
    for voice, path in results.items():
        print(f"  - {voice}: {path}")
    
    return results

# Run test
test_script = "Welcome to today's episode where we explore..."
ab_test_voices(test_script, ["voice_a", "voice_b", "voice_c"])
```

## Troubleshooting

### Issue: Low Quality Score

**Problem**: Voice profile has quality score < 0.7

**Solutions**:
1. Use longer reference audio (5-10 minutes)
2. Ensure reference audio is clean (no background noise)
3. Verify audio format (WAV, 44.1kHz, 16-bit)
4. Check reference audio has clear, natural speech

### Issue: TTS Not Available

**Problem**: `ImportError: Coqui TTS not installed`

**Solution**:
```bash
pip install TTS>=0.20.0
```

For GPU support:
```bash
pip install TTS[cuda]>=0.20.0
```

### Issue: Synthesis Fails

**Problem**: Error during `synthesize_with_voice()`

**Solutions**:
1. Verify voice profile exists: `cloner.voice_profiles.keys()`
2. Check output directory is writable
3. Ensure text is not empty
4. Try shorter text for testing
5. Check GPU/CUDA setup if using GPU

### Issue: Poor Synthesis Quality

**Problem**: Generated audio doesn't sound like reference

**Solutions**:
1. Use higher quality reference audio
2. Increase reference audio duration
3. Ensure reference audio is consistent (same recording conditions)
4. Try different TTS model
5. Adjust voice embedding parameters (advanced)

## API Reference

### VoiceCloner

Main class for voice cloning operations.

```python
VoiceCloner(
    model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2",
    voice_profiles_dir: Optional[Path] = None
)
```

**Methods**:

- `clone_voice()` - Clone voice from reference audio
- `synthesize_with_voice()` - Generate speech with cloned voice
- `get_profiles_by_demographic()` - Filter profiles by gender/age
- `compare_voices()` - A/B test multiple voices
- `export_profiles()` - Export voice profiles to JSON
- `import_profiles()` - Import voice profiles from JSON

### VoiceProfile

Dataclass representing a cloned voice profile.

**Attributes**:
- `name: str` - Unique voice name
- `gender: str` - Gender classification
- `age_bracket: str` - Age range (e.g., "18-25")
- `embedding: List[float]` - Voice embedding vector
- `reference_audio_path: str` - Path to reference audio
- `quality_score: float` - Quality metric (0-1)
- `created_at: str` - ISO timestamp
- `metadata: Dict` - Additional metadata

### VoiceQualityMetrics

Quality assessment for cloned voices.

**Attributes**:
- `clarity_score: float` - Speech clarity (0-1)
- `naturalness_score: float` - How natural voice sounds (0-1)
- `similarity_score: float` - Similarity to reference (0-1)
- `overall_score: float` - Weighted average (0-1)

## Performance Considerations

### CPU vs GPU

- **CPU**: Works but slower (2-5x synthesis time)
- **GPU**: Recommended for production (real-time synthesis)

### Memory Usage

- Model loading: ~1-2GB RAM
- Per profile: ~1-5MB
- Synthesis: Depends on text length

### Optimization Tips

1. **Lazy Loading**: TTS model loads on first use
2. **Profile Caching**: Loaded profiles stay in memory
3. **Batch Synthesis**: Generate multiple audios in one session
4. **GPU Utilization**: Use GPU for faster synthesis

## Examples

### Example 1: Simple Voice Clone

```python
from pathlib import Path
from core.pipeline.voice_cloning import VoiceCloner

cloner = VoiceCloner()
profile = cloner.clone_voice(
    Path("reference.wav"),
    "my_voice",
    "Male",
    "25-35"
)
```

### Example 2: Production Pipeline

```python
# Full production workflow
from core.pipeline.voice_cloning import VoiceCloner

# Setup
cloner = VoiceCloner(voice_profiles_dir=Path("production/voices"))

# Clone voice library
for ref_file in Path("references").glob("*.wav"):
    voice_name = ref_file.stem
    profile = cloner.clone_voice(
        ref_file,
        voice_name,
        metadata={"source": "library_2024"}
    )

# Generate content
for script_file in Path("scripts").glob("*.txt"):
    script_text = script_file.read_text()
    output_file = Path(f"output/{script_file.stem}_vo.wav")
    
    cloner.synthesize_with_voice(
        script_text,
        "my_voice",
        output_file
    )

# Backup
cloner.export_profiles(Path("backup/profiles.json"))
```

## Support

For issues or questions:
- GitHub Issues: [StoryGenerator Issues](https://github.com/Nomoos/StoryGenerator/issues)
- Documentation: [Main README](../README.md)
- Related: [Audio Production Guide](../issues/resolved/phase-3-implementation/group-5-audio-production/)

## License

Same as parent project.
