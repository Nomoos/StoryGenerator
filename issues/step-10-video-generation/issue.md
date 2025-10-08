# Step 10: Video Generation

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 9 (Keyframes), Step 6 (Shot Descriptions)

## Overview

Generate video clips for each shot using either LTX-Video (AI video generation) or interpolation between keyframes. Compare methods and select default approach.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Generate for all shots across 30 scripts

## Checklist

### 10.1 Variant A — LTX-Video per Shot
- [ ] Configure LTX-Video model (2B or 13B variant)
- [ ] Generate **10-20 second clips** per shot from prompts
- [ ] Use keyframes as conditioning (optional)
- [ ] Apply shot-specific parameters (camera movement, style)
- [ ] Save to: `/videos/ltx/{segment}/{age}/{title_id}/shot_{k}.mp4`
- [ ] Log generation metadata (model, seed, params)

### 10.2 Variant B — Interpolation
- [ ] Select interpolation method: RIFE, DAIN, or FILM
- [ ] Interpolate between chosen keyframes
- [ ] Generate intermediate frames (24-30 fps)
- [ ] Add subtle motion/zoom for dynamism
- [ ] Assemble frames into MP4
- [ ] Save to: `/videos/interp/{segment}/{age}/{title_id}/shot_{k}.mp4`
- [ ] Log interpolation parameters

### 10.3 Choose Default Method
- [ ] Compare quality, speed, and consistency
- [ ] Test sample outputs from both methods
- [ ] Set `switches.use_ltx` in `/config/pipeline.yaml`
  - `true`: Use LTX-Video as default
  - `false`: Use Interpolation as default
- [ ] Document decision rationale

## LTX-Video Configuration

### Model Options
- **LTX-Video 2B:** Faster, good quality
- **LTX-Video 13B:** Higher quality, slower
- **Stable Video Diffusion:** Alternative option

### Settings
```yaml
ltx_video:
  model: "ltx_video_2b"  # or "ltx_video_13b"
  num_frames: 25         # for 1 second at 25fps
  width: 1080
  height: 1920
  fps: 25
  num_inference_steps: 50
  guidance_scale: 7.5
  seed: 5678            # from config
  motion_bucket_id: 127  # 1-255, higher = more motion
```

## Interpolation Configuration

### Method Options
- **RIFE (Real-Time Intermediate Flow Estimation):** Fast, good quality
- **DAIN (Depth-Aware Video Frame Interpolation):** High quality, slower
- **FILM (Frame Interpolation for Large Motion):** Google's method, balanced

### Settings
```yaml
interpolation:
  method: "rife"        # or "dain" or "film"
  source_fps: 2         # keyframes per second (e.g., 2 keyframes = 0.5fps)
  target_fps: 30        # output fps
  smooth_motion: true   # apply motion smoothing
  ken_burns: false      # add zoom/pan effects
```

## Video Specifications

### Output Format
- **Resolution:** 1080×1920 (9:16 vertical)
- **FPS:** 30 (configurable in pipeline.yaml)
- **Codec:** H.264
- **Pixel Format:** yuv420p
- **Bitrate:** 8-12 Mbps (high quality)
- **Audio:** None (audio added in Step 11)

### Duration per Shot
- Match shot duration from Step 6 scene planning
- Typical: 5-12 seconds per shot
- Total video: 45-60 seconds (sum of all shots)

## Generation Metadata

### LTX Metadata (`{title_id}_ltx_metadata.json`)
```json
{
  "title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "shots": [
    {
      "shot_id": "shot-001",
      "video_file": "shot_001.mp4",
      "method": "ltx_video",
      "model": "ltx_video_2b",
      "duration_s": 6.0,
      "fps": 30,
      "num_frames": 180,
      "seed": 5678,
      "guidance_scale": 7.5,
      "motion_bucket_id": 127,
      "generation_time_s": 45.3,
      "generated_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### Interpolation Metadata (`{title_id}_interp_metadata.json`)
```json
{
  "title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "shots": [
    {
      "shot_id": "shot-001",
      "video_file": "shot_001.mp4",
      "method": "interpolation",
      "interpolation_method": "rife",
      "source_keyframes": ["shot_001_A.png", "shot_001_A_end.png"],
      "source_fps": 2,
      "target_fps": 30,
      "duration_s": 6.0,
      "num_frames": 180,
      "generation_time_s": 12.1,
      "generated_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## Comparison Criteria

### Quality
- [ ] Visual coherence and consistency
- [ ] Motion smoothness
- [ ] Artifact presence (flickering, warping)
- [ ] Alignment with prompt/description

### Performance
- [ ] Generation time per shot
- [ ] GPU memory usage
- [ ] Total pipeline time for 30 videos

### Flexibility
- [ ] Ease of customization
- [ ] Control over motion
- [ ] Reproducibility

## Acceptance Criteria

- [ ] LTX video clips generated for test set (at least 5 shots)
- [ ] Interpolation clips generated for same test set
- [ ] Metadata logged for both methods
- [ ] Side-by-side comparison completed
- [ ] Default method selected and documented
- [ ] Config switch `use_ltx` set appropriately
- [ ] Full generation completed using selected method
- [ ] All video clips: 1080×1920, 30fps, H.264, yuv420p
- [ ] Total clips: ~180-300 (6-10 shots × 30 scripts)

## Related Files

- `/videos/ltx/{segment}/{age}/` - LTX-generated videos
- `/videos/interp/{segment}/{age}/` - Interpolated videos
- `/images/keyframes_v1/{segment}/{age}/` - Source keyframes
- `/scenes/json/{segment}/{age}/` - Shot descriptions
- `/config/pipeline.yaml` - Video generation configuration
- `/research/python/ltx_generate.py` - LTX implementation
- `/research/python/interpolation.py` - Interpolation implementation

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 17: videos_ltx
- Step 18: videos_interp

Comment `@copilot check` when video generation is complete.

## Notes

- LTX-Video pros: AI-generated motion, creative control
- LTX-Video cons: Slower, higher GPU requirements
- Interpolation pros: Fast, predictable results
- Interpolation cons: Limited motion variety, keyframe dependent
- Hybrid approach possible: Use both based on shot requirements
- Estimated generation time: 30-120 minutes per method (30 scripts)
- GPU VRAM requirement: 16-24GB for LTX-13B, 8-12GB for LTX-2B or interpolation
