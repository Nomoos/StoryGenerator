# EngagementOptimizer

Research-based video engagement optimization for maximizing watch time on short-form vertical video platforms (TikTok, Reels, Shorts).

## Overview

The **EngagementOptimizer** module implements visual engagement principles from [PrismQ.Research.Generator.Video](https://github.com/PrismQDev/PrismQ.Research.Generator.Video) research repository. This research is based on analysis of 10,000+ high-performing short-form videos.

## Key Features

### 1. Constant Motion
- **Nothing remains static for >300ms**
- Micro-movements: 1-3px oscillation at 0.5-2Hz
- Parallax drift: Slow background movement
- Micro-zoom: Gradual 0-5% zoom throughout video
- Research shows 23-47% higher retention rates

### 2. High Contrast + Saturated Accents
- **Dark base layer**: RGB 20-60 (crushed blacks)
- **Neon edge detection**: Canny edges with glow effect
- **Color palette**: Cyan, Magenta, Electric Blue, Neon Green, Hot Pink
- **Contrast ratio**: 1:12+ for maximum impact
- Research shows 31-43% increase in initial engagement

### 3. Pattern + Surprise
- **Minor breaks** (every ~1.3s): Small rotation twirl (±45°)
- **Major breaks** (every ~2.7s): Zoom pop (1.2x scale)
- **Speed pulses**: 1.4x speed at major breaks
- **Smooth blending**: 5-8 frame transitions
- Optimal pattern break timing based on research

### 4. Enhanced Overlays
- **Story captions**: Fade in/out with scale animation
- **Progress bar**: Slim bottom-edge design (2-3px)
  - Deep red/burgundy foreground
  - Translucent gray background
  - Glowing end marker
  - Goal-gradient effect (acceleration at ~80%)

## Components

### `config.py`
Configuration dataclass with all generation parameters including video settings, motion effects, visual style, and overlay options.

### `visual_style.py`
Visual processing pipeline that applies:
- Dark base layer
- High contrast boost
- Saturation enhancement
- Neon edge detection and glow

### `motion.py`
Motion effects including:
- Micro-movements (prevent static appearance)
- Parallax drift
- Micro-zoom with oscillation
- Pattern breaks (minor and major)

### `overlay.py`
Overlay system for:
- Captions with fade animations
- Research-optimized progress bar
- Goal-gradient effect for retention

### `generator.py`
Base video generation:
- Abstract procedural patterns (demo)
- Placeholder for SDXL + AnimateDiff integration (production)

### `pipeline.py`
Main orchestration pipeline that combines all components.

## Usage

### Basic Example

```python
from PrismQ.Pipeline.VideoGeneration.EngagementOptimizer import (
    GenerationConfig,
    VideoPipeline
)

# Create configuration
config = GenerationConfig(
    output_resolution=(1080, 1920),  # 9:16 vertical
    fps=30,
    target_duration=27,  # seconds
    seed=42,
)

# Initialize pipeline
pipeline = VideoPipeline(config)

# Add captions
captions = [
    ("Your Message Here", 0),
    ("Second Caption", 120),
    ("Final Caption", 480),
]

# Generate video
pipeline.run_full_pipeline("output/my_video.mp4", captions)
```

### Running the Example

```bash
cd PrismQ/Pipeline/05_VideoGeneration
python engagement_optimizer_example.py
```

This will generate a demo video at `output/engagement_demo.mp4`.

## Configuration Options

### Video Settings
- `output_resolution`: Tuple (width, height) - default (1080, 1920)
- `fps`: Frame rate - default 30
- `target_duration`: Video length in seconds - default 27
- `seed`: Random seed for reproducibility - default 42

### Motion Settings
- `micro_movement_amplitude`: Pixels - default 2.0
- `micro_movement_frequency`: Hz - default 1.0
- `parallax_speed`: Pixels per frame - default 0.3
- `micro_zoom_range`: (min, max) zoom - default (1.0, 1.05)
- `minor_break_interval`: Frames between minor breaks - default 40
- `major_break_interval`: Frames between major breaks - default 80

### Visual Style Settings
- `base_darkness`: (min, max) RGB values - default (20, 60)
- `contrast_boost`: Multiplier - default 1.5
- `saturation_boost`: Multiplier - default 1.4
- `neon_colors`: List of RGB tuples for neon accents

### Overlay Settings
- `caption_font_size`: Font size - default 48
- `caption_duration`: Seconds - default 2.5
- `progress_bar_height`: Pixels - default 3
- `progress_bar_opacity`: 0.0-1.0 - default 0.85
- `progress_bar_fg_color`: BGR tuple - default (25, 25, 139)

## Output Specifications

- **Resolution**: 1080×1920 (9:16 vertical)
- **Frame Rate**: 30 fps
- **Duration**: Configurable (default 27 seconds)
- **Format**: MP4 (H.264)
- **Optimized for**: TikTok, Instagram Reels, YouTube Shorts

## Research Foundation

This implementation is based on comprehensive research covering:
- Visual attention mechanisms
- Motion perception psychology
- Color psychology
- Platform algorithm behavior
- Cognitive engagement patterns

For detailed research findings, see:
- [Visual Engagement Research](https://github.com/PrismQDev/PrismQ.Research.Generator.Video/blob/main/docs/research/RESEARCH.md)
- [Audio-to-Video Guide](https://github.com/PrismQDev/PrismQ.Research.Generator.Video/blob/main/docs/guides/AUDIO_TO_VIDEO_GUIDE.md)
- [Complete Documentation Index](https://github.com/PrismQDev/PrismQ.Research.Generator.Video/blob/main/docs/INDEX.md)

## Integration with StoryGenerator Pipeline

The EngagementOptimizer can be used as the final stage in the StoryGenerator pipeline:

1. **Stage 02** (TextGeneration): Generate story script
2. **Stage 03** (AudioGeneration): Create voice-over and subtitles
3. **Stage 04** (ImageGeneration): Generate keyframes
4. **Stage 05** (VideoGeneration): Assemble video
5. **EngagementOptimizer**: Apply research-based engagement optimizations

## Future Enhancements

- SDXL + AnimateDiff integration for AI-generated backgrounds
- Integration with keyframe generation from Stage 04
- Subtitle rendering from Stage 03
- Platform-specific optimization presets
- A/B testing framework for different configurations

## Credits

Based on research from [PrismQ.Research.Generator.Video](https://github.com/PrismQDev/PrismQ.Research.Generator.Video)

## License

MIT License - See main repository LICENSE file for details.
