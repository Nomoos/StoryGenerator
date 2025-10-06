# Video Generation Pipeline

Complete automated pipeline for generating 1080×1920 vertical videos (Reels/Shorts/TikTok) from story scripts.

## Pipeline Overview

```
Ideas → Script (GPT) → Revision (GPT) → Audio (ElevenLabs) → Subtitles (WhisperX)
  ↓
Scene Analysis → Scene Descriptions → Keyframe Generation → Video Interpolation → Final Composition
```

## Pipeline Stages

### Stage 1: Scene Analysis
**Module:** `GSceneAnalyzer.py`

Analyzes subtitle timing to create logical scene segments:
- Parses word-by-word subtitles (SRT format)
- Segments story based on natural pauses and content
- Creates scenes with timing metadata (start, end, duration)
- Configurable scene duration (3-15 seconds default)

**Output:** `scenes.json` - Scene segments with timing

### Stage 2: Visual Scene Description
**Module:** `GSceneDescriber.py`

Generates detailed visual descriptions for each scene using GPT:
- Creates image generation prompts for each scene
- Considers narrative arc position (opening, rising action, climax, resolution)
- Optimized for 1080×1920 vertical format
- Photorealistic, cinematic style (35mm film aesthetic)

**Output:** Updated `scenes.json` with visual descriptions

### Stage 3: Keyframe Generation
**Module:** `GKeyframeGenerator.py`

Creates keyframe images using Stable Diffusion:
- Generates 2-6 keyframes per scene (based on duration)
- Short scenes (< 5s): 2 keyframes
- Medium scenes (5-10s): 3 keyframes
- Long scenes (> 10s): 4+ keyframes
- 1080×1920 resolution, vertical format
- Saves metadata (timestamp, prompt, position)

**Output:** 
- Keyframe images (PNG) in `keyframes/` directory
- Keyframe metadata (JSON)

### Stage 4: Video Interpolation
**Module:** `GVideoInterpolator.py`

Creates smooth transitions between keyframes:
- Linear interpolation with ease-in-out timing
- 30 FPS output
- Optional motion blur for smoothness
- Generates MP4 segments for each scene

**Output:** Video segments in `video_segments/` directory

### Stage 5: Final Composition
**Module:** `GVideoCompositor.py`

Assembles final video with all elements:
- Concatenates video segments
- Syncs voiceover audio
- Adds styled subtitles overlay
- Optional background music
- Final output: 1080×1920 MP4

**Output:** `final_video.mp4`

## Incremental Improvement System

**Module:** `GIncrementalImprover.py`

Analyzes and improves generated videos:

### Features:
1. **Automated Quality Checks**
   - Scene duration consistency
   - Description quality (length, detail)
   - Keyframe coverage
   - Overall scoring

2. **GPT-Based Analysis**
   - User feedback integration
   - Contextual quality assessment
   - Specific improvement suggestions

3. **Improvement Actions**
   - `regenerate_scenes` - Re-segment with different parameters
   - `improve_descriptions` - Regenerate visual descriptions
   - `regenerate_keyframes` - Recreate all keyframes
   - `adjust_pacing` - Modify scene timing

4. **Iteration Tracking**
   - Maintains improvement history
   - Compares iterations
   - Tracks score progression

## Usage

### Generate Video for Single Story

```python
from Models.StoryIdea import StoryIdea
from Generators.GVideoPipeline import VideoPipeline

# Load story
story_idea = StoryIdea.from_file("path/to/Idea.json")

# Initialize pipeline
pipeline = VideoPipeline(
    use_gpu=True,
    num_inference_steps=30,
    target_fps=30
)

# Generate video
final_video = pipeline.generate_video(
    story_idea=story_idea,
    skip_existing=True,
    add_subtitles=True
)
```

### Command Line Interface

```bash
# Generate single video
python Generation/Manual/MVideoPipeline.py "Story_Title"

# Generate all videos
python Generation/Manual/MVideoPipeline.py all

# Check pipeline status
python Generation/Manual/MVideoPipeline.py status "Story_Title"

# Improve existing video
python Generation/Manual/MVideoPipeline.py improve "Story_Title"
```

### Batch Generation

```python
from Generators.GVideoPipeline import VideoPipeline

pipeline = VideoPipeline()
results = pipeline.generate_batch(
    story_ideas=[story1, story2, story3],
    skip_existing=True,
    add_subtitles=True
)
```

### Video Improvement

```python
from Generators.GIncrementalImprover import IncrementalImprover

improver = IncrementalImprover()

# Analyze quality
analysis = improver.analyze_video_quality(
    story_idea=story_idea,
    user_feedback="The pacing feels too slow in the middle"
)

# Apply improvements
results = improver.apply_improvements(
    story_idea=story_idea,
    improvements=['regenerate_scenes', 'adjust_pacing']
)

# Compare iterations
comparison = improver.compare_iterations(story_idea)
```

## Configuration

### Pipeline Parameters

- `use_gpu`: Use GPU for image generation (default: True)
- `num_inference_steps`: Stable Diffusion steps (default: 30, range: 20-50)
- `target_fps`: Output video FPS (default: 30)

### Scene Analysis Parameters

- `min_scene_duration`: Minimum scene length in seconds (default: 3.0)
- `max_scene_duration`: Maximum scene length in seconds (default: 15.0)

### Image Generation

- Model: `runwayml/stable-diffusion-v1-5`
- Resolution: 1080×1920 (vertical)
- Style: Photorealistic, cinematic, 35mm aesthetic
- Negative prompts: Avoid blurry, low quality, distorted images

## File Structure

```
Stories/
├── 4_Titles/
│   └── Story_Title/
│       ├── Idea.json                      # Story metadata
│       ├── Revised.txt                    # Final script
│       ├── voiceover_normalized.mp3       # Audio
│       ├── Subtitles_Word_By_Word.txt     # SRT subtitles
│       ├── scenes.json                    # Scene analysis
│       ├── keyframes/                     # Generated keyframes
│       │   ├── scene_001_keyframe_00_t0.00.png
│       │   ├── scene_001_keyframe_00_t0.00.json
│       │   └── ...
│       ├── video_segments/                # Interpolated videos
│       │   ├── scene_001.mp4
│       │   └── ...
│       ├── final_video.mp4                # Final output
│       ├── pipeline_state.json            # Pipeline progress
│       └── improvement_history.json       # Quality iterations
```

## Dependencies

### Core Requirements
- Python 3.8+
- CUDA-capable GPU (recommended for image generation)
- FFmpeg (for video processing)

### Python Packages
```
torch>=2.0.0
diffusers>=0.21.0
transformers>=4.30.0
opencv-python>=4.8.0
ffmpeg-python>=0.2.0
whisperx>=3.1.0
Pillow>=10.0.0
openai>=1.50.0
elevenlabs>=1.9.0
```

See `requirements.txt` for complete list.

## Performance

### Timing Estimates (per story, ~60s duration)

With GPU (NVIDIA RTX 3080+):
- Scene Analysis: < 1 minute
- Scene Description: 2-3 minutes
- Keyframe Generation: 10-20 minutes (30 steps)
- Video Interpolation: 5-10 minutes
- Final Composition: 2-3 minutes
- **Total: ~20-40 minutes**

Without GPU (CPU only):
- Keyframe generation may take 2-4 hours
- Other stages similar to GPU timing
- **Total: ~2-5 hours**

### Optimization Tips

1. **Reduce inference steps** (20-25 for faster, 40-50 for higher quality)
2. **Use GPU** for image generation
3. **Enable skip_existing** to avoid regenerating existing assets
4. **Batch processing** for multiple stories
5. **Lower FPS** (24 instead of 30) for smaller file sizes

## Troubleshooting

### Common Issues

**Out of GPU Memory**
- Reduce inference steps
- Use lower resolution temporarily
- Enable `pipe.enable_attention_slicing()`

**FFmpeg Errors**
- Ensure FFmpeg is installed and in PATH
- Check video segment compatibility

**Subtitle Alignment Issues**
- Verify WhisperX is installed correctly
- Check audio file quality
- Ensure script text matches audio

**Poor Image Quality**
- Increase inference steps (30-50)
- Improve scene descriptions
- Adjust prompts to be more specific

## Advanced Features

### Custom Styles

Modify scene descriptions to apply different visual styles:
- Film noir: "black and white, high contrast, dramatic shadows"
- Anime: "anime style, cel shading, vibrant colors"
- Documentary: "raw footage, handheld camera, natural lighting"

### Background Music

```python
final_video = compositor.compose_final_video(
    story_idea=story_idea,
    background_music="path/to/music.mp3"
)
```

### Custom Interpolation

Extend `VideoInterpolator` class to implement:
- Optical flow-based interpolation
- AI-powered frame generation (FILM, RIFE)
- Custom motion effects

## Future Enhancements

- [ ] Integration with video hosting APIs (YouTube, TikTok)
- [ ] Real-time preview generation
- [ ] A/B testing different visual styles
- [ ] Automated thumbnail generation
- [ ] Analytics integration
- [ ] Voice cloning for consistent narration
- [ ] Advanced motion graphics and transitions
- [ ] Multi-language support

## License

See project LICENSE file for details.

## Support

For issues, questions, or contributions, see the project repository.
