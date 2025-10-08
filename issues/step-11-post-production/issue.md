# Step 11: Post-Production

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 7 (Audio), Step 8 (Timed Subtitles), Step 10 (Video Clips)

## Overview

Combine video clips, audio voiceover, and subtitles into final videos with proper formatting, effects, and transitions.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Process all 30 final videos

## Checklist

### 11.1 Video Processing
- [ ] Crop all clips to **9:16 (1080×1920)** if needed
- [ ] Ensure consistent fps=30 across all clips
- [ ] Apply color grading (optional, consistent style)
- [ ] Verify no letterboxing or pillarboxing

### 11.2 Safe Text Margins
- [ ] Apply safe margins for subtitle overlay
  - **Top margin:** 8% (153 pixels)
  - **Bottom margin:** 10% (192 pixels)
- [ ] Create margin overlay template
- [ ] Test subtitle visibility on sample devices

### 11.3 Subtitle Integration
- [ ] Burn-in subtitles OR prepare soft subtitles
- [ ] Use timed SRT from Step 8
- [ ] Configure subtitle style:
  - Font: Bold, sans-serif (e.g., Arial, Roboto)
  - Size: 60-80px (readable on mobile)
  - Color: White with black outline/shadow
  - Position: Bottom center (within safe margin)
  - Background: Semi-transparent box (optional)

### 11.4 Audio Integration
- [ ] Load normalized audio from Step 7
- [ ] Sync audio with video timeline
- [ ] Add background music (BGM) if available
  - Licensed music only
  - Volume: -20 to -24 LUFS (under voiceover)
- [ ] Apply audio ducking (BGM dips during VO)
- [ ] Add sound effects (SFX) if appropriate
  - Keep subtle and non-distracting

### 11.5 Shot Concatenation
- [ ] Concatenate shots in sequence order
- [ ] Add transitions between shots:
  - Gentle cross-dissolve (0.3-0.5 seconds)
  - OR direct cuts (based on pacing)
- [ ] Verify total duration: 45-60 seconds
- [ ] Ensure smooth flow

### 11.6 Draft Export
- [ ] Export draft video with all elements
- [ ] Save to: `/final/{segment}/{age}/{title_id}_draft.mp4`
- [ ] Log export parameters
- [ ] Create preview thumbnail (frame at 3 seconds)

## Video Export Specifications

### Codec Settings
```
Video:
  - Codec: H.264 (libx264)
  - Profile: High
  - Level: 4.1
  - Preset: slow (better quality)
  - CRF: 18-23 (18=highest quality, 23=good quality)
  - Pixel Format: yuv420p
  - Color Space: bt709
  - FPS: 30

Audio:
  - Codec: AAC
  - Bitrate: 192 kbps (stereo)
  - Sample Rate: 48000 Hz
  - Channels: 2 (stereo)
```

### FFmpeg Command Example
```bash
ffmpeg -i video_concat.mp4 -i audio_normalized.wav \
  -filter_complex "[0:v]subtitles=subtitles.srt:force_style='FontName=Arial Bold,FontSize=70,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=3,Outline=2,Shadow=1,MarginV=192'[v]" \
  -map "[v]" -map 1:a \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart \
  output_draft.mp4
```

## Subtitle Style Configuration

### SRT Force Style
```
FontName=Arial Bold
FontSize=70
PrimaryColour=&HFFFFFF&     # White
OutlineColour=&H000000&     # Black outline
BorderStyle=3               # Opaque box
Outline=2                   # 2px outline
Shadow=1                    # Drop shadow
MarginV=192                 # Bottom margin (10% of 1920)
Alignment=2                 # Bottom center
```

## Audio Mixing Guidelines

### Volume Levels
- **Voiceover (VO):** -14 LUFS (primary)
- **Background Music (BGM):** -20 to -24 LUFS (under VO)
- **Sound Effects (SFX):** -16 to -18 LUFS (accent)

### Ducking Parameters
- **Threshold:** -30 dB
- **Ratio:** 3:1
- **Attack:** 10 ms
- **Release:** 200 ms
- **Knee:** 2 dB

## Transition Guidelines

### When to Use Cross-Dissolve
- Scene changes with different settings
- Mood transitions
- Time passage indication

### When to Use Direct Cuts
- Fast-paced action
- Matching action between shots
- Maintaining high energy

## Draft Metadata

### Export Log (`{title_id}_draft_metadata.json`)
```json
{
  "title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "draft": {
    "file": "{title_id}_draft.mp4",
    "duration_s": 52.3,
    "resolution": "1080x1920",
    "fps": 30,
    "codec": "h264",
    "bitrate_mbps": 10.5,
    "file_size_mb": 68.7
  },
  "components": {
    "video_clips": 7,
    "audio_file": "{title_id}_lufs.wav",
    "subtitle_file": "{title_id}.srt",
    "bgm_file": "background_music.mp3",
    "transition_type": "cross_dissolve"
  },
  "export_settings": {
    "preset": "slow",
    "crf": 20,
    "pixel_format": "yuv420p",
    "audio_codec": "aac",
    "audio_bitrate": 192
  },
  "exported_at": "2024-01-01T12:00:00Z"
}
```

## Acceptance Criteria

- [ ] All 30 draft videos exported successfully
- [ ] Video format: 1080×1920, 30fps, H.264, yuv420p
- [ ] Audio integrated: voiceover + BGM (if used) + SFX (if used)
- [ ] Subtitles visible and readable on mobile devices
- [ ] Safe margins respected (top 8%, bottom 10%)
- [ ] Shot transitions smooth and appropriate
- [ ] Total duration: 45-60 seconds per video
- [ ] File size reasonable: 50-100MB per video
- [ ] Export metadata logged for all videos
- [ ] Preview thumbnails generated

## Related Files

- `/final/{segment}/{age}/` - Final video output directory
- `/videos/ltx/` or `/videos/interp/` - Source video clips
- `/audio/normalized/{segment}/{age}/` - Source audio
- `/subtitles/timed/{segment}/{age}/` - Timed subtitles
- `/scenes/json/{segment}/{age}/` - Shot sequence information
- `/research/csharp/FFmpegClient.cs` - FFmpeg wrapper (C#)

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 19: final (draft stage)

Comment `@copilot check` when all draft videos are complete.

## Notes

- Use `movflags +faststart` for web streaming optimization
- Test on actual mobile devices before Step 12 (Quality Checks)
- Consider aspect ratio safe zones for platform upload
- BGM should be licensed or royalty-free
- Total output: 30 draft videos (~2-3GB total)
- Processing time: ~2-4 hours for all videos
