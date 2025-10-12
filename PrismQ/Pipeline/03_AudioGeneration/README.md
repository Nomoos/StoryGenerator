# Stage 03: Audio Generation

## Purpose

Convert text content into audio (voice-over) and generate synchronized subtitles.

## Independence

This stage is **fully independent** and can be developed, tested, and deployed separately.

## Input Contract

```python
@dataclass
class AudioGenerationInput:
    text_content: TextContent       # From Stage 02
    voice_id: str | None = None     # Voice to use
    generate_subtitles: bool = True
    audio_format: str = "mp3"
    additional_params: dict = field(default_factory=dict)
```

## Output Contract

```python
@dataclass
class AudioGenerationOutput:
    audio: AudioContent
    metadata: dict = field(default_factory=dict)

@dataclass
class AudioContent:
    audio_file_path: str            # Path to generated audio
    duration_seconds: float
    subtitles: list[SubtitleSegment]
    voice_id: str | None
    metadata: dict = field(default_factory=dict)

@dataclass
class SubtitleSegment:
    start_time: float               # Seconds
    end_time: float                 # Seconds
    text: str
```

## Dependencies

- ✅ `IPipelineStage`, `IVoiceProvider` from shared interfaces
- ✅ `TextContent` from stage contracts (data structure only)
- ❌ NO imports from other pipeline stage implementations

## Usage Example

```python
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    AudioGenerationInput,
    TextContent,
)

# Input from Stage 02
text_content = TextContent(
    story_script="In the heart of the city...",
    title="Journey to Self-Discovery",
    description="A powerful story...",
    tags=["inspiration"],
    scenes=[]
)

# Create input for Stage 03
input_data = AudioGenerationInput(
    text_content=text_content,
    voice_id="female_1",
    generate_subtitles=True,
    audio_format="mp3"
)

# Execute stage
result = await audio_stage.execute(input_data)

# Access output
audio = result.data.audio
print(f"Audio: {audio.audio_file_path}")
print(f"Duration: {audio.duration_seconds}s")
print(f"Subtitles: {len(audio.subtitles)} segments")
```

## Input JSON Example

```json
{
  "text_content": {
    "story_script": "In the heart of the city, a young woman discovers...",
    "title": "Journey to Self-Discovery",
    "description": "A powerful story about finding your true self...",
    "tags": ["inspiration", "personal-growth"]
  },
  "voice_id": "female_1",
  "generate_subtitles": true,
  "audio_format": "mp3"
}
```

## Output JSON Example

```json
{
  "audio": {
    "audio_file_path": "/path/to/audio.mp3",
    "duration_seconds": 45.5,
    "subtitles": [
      {
        "start_time": 0.0,
        "end_time": 3.5,
        "text": "In the heart of the city,"
      },
      {
        "start_time": 3.5,
        "end_time": 7.2,
        "text": "a young woman discovers her true potential."
      }
    ],
    "voice_id": "female_1",
    "metadata": {
      "sample_rate": 44100,
      "bitrate": 192
    }
  }
}
```

## Testing

```python
@pytest.mark.asyncio
async def test_audio_generation():
    """Test audio generation stage independently."""
    
    mock_voice = Mock()
    mock_voice.synthesize.return_value = b"fake_audio_data"
    
    stage = AudioGenerationStage(voice_provider=mock_voice)
    
    text_content = TextContent(
        story_script="Test script",
        title="Test",
        description="Test description"
    )
    
    input_data = AudioGenerationInput(text_content=text_content)
    result = await stage.execute(input_data)
    
    assert result.data.audio.audio_file_path.endswith('.mp3')
    assert result.data.audio.duration_seconds > 0
```

## Repository Structure (When Independent)

```
prismq-stage-03-audio-generation/
├── src/
│   ├── stage.py                 # Main stage implementation
│   ├── voice_synthesizer.py    # Voice synthesis
│   ├── subtitle_generator.py   # Subtitle generation
│   └── audio_processor.py      # Audio processing
├── tests/
│   └── test_stage.py
├── requirements.txt
│   └── prismq-core>=1.0.0
└── README.md
```
