# Video Export and Metadata Generation

## Overview

The video pipeline automatically exports final videos to an organized production directory with accompanying thumbnails and metadata files for easy publishing to social media platforms.

## Export Structure

All exported files are organized in `/data/final/{segment}/{age}/` directories:

```
data/final/
├── women/
│   ├── 18-23/
│   │   ├── a1b2c3d4.mp4               # Final video (1080×1920)
│   │   ├── a1b2c3d4_thumbnail.jpg     # Thumbnail (1080×1920)
│   │   └── a1b2c3d4_metadata.json     # Video metadata
│   ├── 24-30/
│   └── ...
└── men/
    ├── 18-23/
    └── ...
```

### Path Components

- **`{segment}`**: Target gender audience
  - `women` - Female audience
  - `men` - Male audience

- **`{age}`**: Target age group
  - `10-13` - Pre-teens
  - `14-17` - Teenagers
  - `18-23` - Young adults
  - `24-30` - Adults

- **`{title_id}`**: Unique 8-character identifier (MD5 hash of story title)
  - Consistent: Same title always generates the same ID
  - Unique: Different titles generate different IDs
  - URL-safe: Only contains alphanumeric characters

## Automatic Export

Export happens automatically after video composition:

```python
from Models.StoryIdea import StoryIdea
from Generators.GVideoPipeline import VideoPipeline

# Load story
story = StoryIdea.from_file("path/to/story.json")

# Generate video (export happens automatically)
pipeline = VideoPipeline()
final_video = pipeline.generate_video(
    story_idea=story,
    add_subtitles=True
)
# After this completes, files are exported to /data/final/
```

## Manual Export

You can also manually export an existing video:

```python
from Generators.GVideoCompositor import VideoCompositor

compositor = VideoCompositor()

# Export with thumbnail and metadata
video_path, thumb_path, meta_path = compositor.export_final_video(
    story_idea=story,
    source_video_path="path/to/video.mp4",
    export_thumbnail=True,
    export_metadata=True
)

print(f"Exported to: {video_path}")
print(f"Thumbnail: {thumb_path}")
print(f"Metadata: {meta_path}")
```

## Metadata Structure

The metadata JSON file contains all information needed for publishing:

```json
{
  "title_id": "a1b2c3d4",
  "title": "My Amazing Story",
  "description": "My Amazing Story\n\nTheme: adventure\nTone: exciting\n\nA thrilling adventure...",
  "tags": [
    "adventure",
    "exciting",
    "shorts",
    "viral",
    "story"
  ],
  "segment": "women",
  "age_group": "18-23",
  "narrator_gender": "F",
  "theme": "adventure",
  "tone": "exciting",
  "language": "en",
  "potencial_score": 85,
  "video_format": {
    "resolution": "1080x1920",
    "aspect_ratio": "9:16",
    "format": "mp4"
  }
}
```

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `title_id` | string | Unique 8-character identifier |
| `title` | string | Story title |
| `description` | string | Full description with theme, tone, and goal |
| `tags` | array | Tags for social media (theme, tone, platform tags) |
| `segment` | string | Target gender segment |
| `age_group` | string | Target age group |
| `narrator_gender` | string | Gender of narrator (F/M) |
| `theme` | string | Story theme |
| `tone` | string | Story tone |
| `language` | string | Language code (e.g., "en") |
| `potencial_score` | number | Overall viral potential score (0-100) |
| `video_format` | object | Video format specifications |

## Thumbnail Generation

Thumbnails are automatically generated from the video:

- **Resolution:** 1080×1920 (9:16 aspect ratio)
- **Format:** JPEG (high quality)
- **Timestamp:** 0.5 seconds into the video
- **Quality:** High (suitable for social media)

### Custom Thumbnail Timing

To generate a thumbnail at a different timestamp:

```python
compositor = VideoCompositor()
compositor._generate_thumbnail(
    video_path="video.mp4",
    output_path="thumbnail.jpg",
    timestamp=2.5  # 2.5 seconds into video
)
```

## Publishing Workflow

### 1. Locate Exported Files

```bash
cd data/final/women/18-23/
ls -lh a1b2c3d4*
```

### 2. Read Metadata

```python
import json

with open("a1b2c3d4_metadata.json") as f:
    metadata = json.load(f)

print(f"Title: {metadata['title']}")
print(f"Description: {metadata['description']}")
print(f"Tags: {', '.join(metadata['tags'])}")
```

### 3. Upload to Platform

- **Video:** `a1b2c3d4.mp4`
- **Thumbnail:** `a1b2c3d4_thumbnail.jpg` (custom thumbnail)
- **Title:** From `metadata['title']`
- **Description:** From `metadata['description']`
- **Tags/Hashtags:** From `metadata['tags']`

## Utility Functions

The export system provides several utility functions:

### Get Segment from Gender

```python
from Tools.Utils import get_segment_from_gender

segment = get_segment_from_gender("F")  # Returns: "women"
segment = get_segment_from_gender("M")  # Returns: "men"
```

### Get Age Group from Potencial

```python
from Tools.Utils import get_age_group_from_potencial

potencial = {
    "age_groups": {
        "10_15": 20,
        "20_25": 85,  # Highest score
        "25_30": 40
    }
}

age_group = get_age_group_from_potencial(potencial)
# Returns: "18-23"
```

### Generate Title ID

```python
from Tools.Utils import generate_title_id

title_id = generate_title_id("My Story Title")
# Returns: "a1b2c3d4" (consistent for same title)
```

### Get Export Path

```python
from Tools.Utils import get_final_export_path

video_path = get_final_export_path(
    story_title="My Story",
    segment="women",
    age_group="18-23",
    filename="a1b2c3d4.mp4"
)
# Returns: "/path/to/data/final/women/18-23/a1b2c3d4.mp4"
# Creates directory if it doesn't exist
```

## Configuration

### Export Settings in VideoCompositor

```python
compositor = VideoCompositor(
    output_format="mp4",           # Video format
    enable_transitions=True,       # Smooth transitions
    transition_duration=0.5,       # Transition length
    apply_ken_burns=False          # Ken Burns effect
)
```

### Disable Automatic Export

If you don't want automatic export, modify the export call in `compose_final_video()`:

```python
# In GVideoCompositor.py, comment out the export call:
# self.export_final_video(...)
```

## Troubleshooting

### Export Directory Not Created

The directory is created automatically. If it fails, check permissions:

```bash
chmod -R 755 data/final/
```

### Thumbnail Generation Fails

Ensure FFmpeg is installed and accessible:

```bash
ffmpeg -version
```

If missing, install:

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Metadata Missing Fields

Ensure your `StoryIdea` object has all required fields:
- `story_title`
- `narrator_gender`
- `potencial` (with age_groups)

## Best Practices

### 1. Verify Exports

After generation, always verify the exports:

```python
import os

def verify_export(title_id, segment, age_group):
    base = f"data/final/{segment}/{age_group}/{title_id}"
    
    checks = {
        "Video": f"{base}.mp4",
        "Thumbnail": f"{base}_thumbnail.jpg",
        "Metadata": f"{base}_metadata.json"
    }
    
    for name, path in checks.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ {name}: {path} ({size} bytes)")
        else:
            print(f"❌ {name}: Missing")

verify_export("a1b2c3d4", "women", "18-23")
```

### 2. Organize by Campaign

Group videos for specific campaigns:

```python
# Tag videos in metadata for campaigns
metadata["campaign"] = "summer_2024"
metadata["platform"] = "instagram"
```

### 3. Backup Before Publishing

Always backup original files before publishing:

```bash
cp -r data/final/ data/final_backup_$(date +%Y%m%d)/
```

### 4. Track Published Videos

Maintain a registry of published videos:

```python
import json
from datetime import datetime

registry = {
    "a1b2c3d4": {
        "published_date": datetime.now().isoformat(),
        "platforms": ["instagram", "tiktok"],
        "performance": {
            "views": 0,
            "likes": 0,
            "shares": 0
        }
    }
}

with open("data/final/publish_registry.json", "w") as f:
    json.dump(registry, f, indent=2)
```

## See Also

- [VIDEO_PIPELINE.md](VIDEO_PIPELINE.md) - Complete pipeline documentation
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Integration with other systems
- [VIDEO_SPECS.md](VIDEO_SPECS.md) - Video format specifications
