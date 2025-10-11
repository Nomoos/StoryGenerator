# Stage 05: Video Generation

## Purpose

Assemble final video from text, audio, and images. This is the final stage that produces the complete video content.

## Independence

This stage is **fully independent** and can be developed, tested, and deployed separately.

## Input Contract

```python
@dataclass
class VideoGenerationInput:
    text_content: TextContent       # From Stage 02
    audio_content: AudioContent     # From Stage 03
    keyframes: list[KeyFrame]       # From Stage 04
    video_format: str = "mp4"
    resolution: str = "1080x1920"   # Vertical video default
    fps: int = 30
    additional_params: dict = field(default_factory=dict)
```

## Output Contract

```python
@dataclass
class VideoGenerationOutput:
    video: VideoContent
    metadata: dict = field(default_factory=dict)

@dataclass
class VideoContent:
    video_file_path: str
    duration_seconds: float
    resolution: str
    fps: int
    file_size_bytes: int
    metadata: dict = field(default_factory=dict)
```

## Dependencies

- ✅ `IPipelineStage` from shared interfaces
- ✅ `TextContent`, `AudioContent`, `KeyFrame` from stage contracts (data structures only)
- ❌ NO imports from other pipeline stage implementations

## Usage Example

```python
from PrismQ.Infrastructure.Core.Shared.interfaces import (
    VideoGenerationInput,
    TextContent,
    AudioContent,
    KeyFrame,
)

# Input from previous stages
text_content = TextContent(...)
audio_content = AudioContent(...)
keyframes = [KeyFrame(...), KeyFrame(...)]

# Create input for Stage 05
input_data = VideoGenerationInput(
    text_content=text_content,
    audio_content=audio_content,
    keyframes=keyframes,
    video_format="mp4",
    resolution="1080x1920",
    fps=30
)

# Execute stage
result = await video_stage.execute(input_data)

# Access output
video = result.data.video
print(f"Video: {video.video_file_path}")
print(f"Duration: {video.duration_seconds}s")
print(f"Size: {video.file_size_bytes / 1024 / 1024:.2f} MB")
```

## Input JSON Example

```json
{
  "text_content": {
    "story_script": "In the heart of the city...",
    "title": "Journey to Self-Discovery"
  },
  "audio_content": {
    "audio_file_path": "/path/to/audio.mp3",
    "duration_seconds": 45.5,
    "subtitles": [...]
  },
  "keyframes": [
    {
      "id": "kf_001",
      "image_path": "/path/to/keyframe_001.png",
      "timestamp": 0.0,
      "description": "Opening scene"
    }
  ],
  "video_format": "mp4",
  "resolution": "1080x1920",
  "fps": 30
}
```

## Output JSON Example

```json
{
  "video": {
    "video_file_path": "/path/to/final_video.mp4",
    "duration_seconds": 45.5,
    "resolution": "1080x1920",
    "fps": 30,
    "file_size_bytes": 15728640,
    "metadata": {
      "codec": "h264",
      "bitrate": 2500000,
      "audio_codec": "aac"
    }
  }
}
```

## Testing

```python
@pytest.mark.asyncio
async def test_video_generation():
    """Test video generation stage independently."""
    
    mock_video_gen = Mock()
    
    stage = VideoGenerationStage(video_generator=mock_video_gen)
    
    text_content = TextContent(story_script="Test", title="Test")
    audio_content = AudioContent(
        audio_file_path="/test/audio.mp3",
        duration_seconds=30.0
    )
    keyframes = [
        KeyFrame(
            id="kf_001",
            image_path="/test/img.png",
            timestamp=0.0,
            description="Test"
        )
    ]
    
    input_data = VideoGenerationInput(
        text_content=text_content,
        audio_content=audio_content,
        keyframes=keyframes
    )
    
    result = await stage.execute(input_data)
    
    assert result.data.video.video_file_path.endswith('.mp4')
    assert result.data.video.duration_seconds > 0
    assert result.data.video.resolution == "1080x1920"
    assert result.data.video.fps == 30
```

## Repository Structure (When Independent)

```
prismq-stage-05-video-generation/
├── src/
│   ├── stage.py              # Main stage implementation
│   ├── video_assembler.py    # Video assembly
│   ├── frame_interpolator.py # Frame interpolation
│   ├── subtitle_renderer.py  # Subtitle rendering
│   └── video_finalizer.py    # Final processing
├── tests/
│   └── test_stage.py
├── requirements.txt
│   └── prismq-core>=1.0.0
│   └── ffmpeg-python>=0.2.0  # For video processing
└── README.md
```

## Video Assembly Process

1. **Load Audio**: Import audio file from Stage 03
2. **Prepare Keyframes**: Load images from Stage 04
3. **Interpolate Frames**: Create smooth transitions between keyframes
4. **Render Subtitles**: Overlay subtitles from audio content
5. **Encode Video**: Combine all elements into final video
6. **Finalize**: Apply any post-processing and optimization

## Performance Considerations

- Video generation is typically the slowest stage
- Consider async processing for better performance
- May benefit from GPU acceleration
- Cache intermediate results when possible
