# Step 9: Key Images per Scene (SDXL)

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 6 (Scene Planning with Shot Descriptions)

## Overview

Generate keyframe images for each scene shot using SDXL (Stable Diffusion XL) with optional refinement and consistency passes.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Generate for all shots across 30 scripts

## Checklist

### 9.1 Prompt Builder
- [ ] Load shot descriptions from Step 6
- [ ] Create per-shot prompts optimized for SDXL
- [ ] Include: style, camera angle, mood, age-safe content
- [ ] Apply segment/age-appropriate modifiers
- [ ] Save prompts to: `/images/keyframes_v1/{segment}/{age}/{title_id}_prompts.json`

### 9.2 Generate Keyframes (Batch A)
- [ ] Use **SDXL base + refiner** pipeline
- [ ] Apply seed per shot (from config or sequential)
- [ ] Generate 1080×1920 (9:16 vertical format)
- [ ] Save to: `/images/keyframes_v1/{segment}/{age}/{title_id}/shot_{k}_A.png`
- [ ] Log generation parameters (seed, steps, cfg, etc.)

### 9.3 Consistency & Variants (Batch B - Optional)
- [ ] Apply LoRA for style consistency (optional)
- [ ] Use ControlNet for character consistency (optional)
- [ ] Generate alternative variants per shot
- [ ] Save to: `/images/keyframes_v2/{segment}/{age}/{title_id}/shot_{k}_B.png`
- [ ] Compare quality with Batch A

### 9.4 Pick Top N per Shot
- [ ] Implement aesthetic filter or manual selection
- [ ] Optional: Use LLM for image quality assessment
- [ ] Select best keyframe per shot
- [ ] Save selection manifest JSON with rationale

## SDXL Configuration

### Model Settings
```yaml
model:
  base: "stabilityai/stable-diffusion-xl-base-1.0"
  refiner: "stabilityai/stable-diffusion-xl-refiner-1.0"
  vae: "madebyollin/sdxl-vae-fp16-fix"

generation:
  width: 1080
  height: 1920
  num_inference_steps: 50
  guidance_scale: 7.5
  refiner_start: 0.85
  negative_prompt: "text, watermark, blurry, low quality, distorted"

seeds:
  base_seed: 1234  # from config/pipeline.yaml
  per_shot: true   # increment seed per shot
```

### Age-Safe Content Filters
- **10-13:** No mature themes, violence, or adult content
- **14-17:** Mild themes acceptable, no explicit content
- **18-23:** Wider range acceptable, still platform-appropriate

## Prompt Structure

### Template
```
{style_prefix} {subject} {action} {setting} {mood} {camera_angle} {lighting} {quality_tags}
```

### Example Prompts JSON (`{title_id}_prompts.json`)
```json
{
  "title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "style": "cinematic, photorealistic",
  "prompts": [
    {
      "shot_id": "shot-001",
      "sequence": 1,
      "positive": "cinematic photograph of a young woman looking surprised, mysterious lighting, close-up portrait, dramatic shadows, 9:16 vertical composition, high quality, detailed",
      "negative": "text, watermark, blurry, low quality, distorted, deformed",
      "seed": 1234,
      "cfg_scale": 7.5,
      "steps": 50
    }
  ]
}
```

## Image Specifications

- **Resolution:** 1080×1920 (9:16 vertical)
- **Format:** PNG (lossless)
- **Color Space:** sRGB
- **Bit Depth:** 8-bit per channel
- **DPI:** 72 (screen resolution)

## Selection Manifest

### Format (`{title_id}_selection.json`)
```json
{
  "title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "selections": [
    {
      "shot_id": "shot-001",
      "selected_image": "shot_001_A.png",
      "alternatives": ["shot_001_B.png"],
      "selection_method": "aesthetic_score",
      "aesthetic_score": 0.85,
      "rationale": "Best composition and clarity",
      "selected_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## Quality Criteria

### Aesthetic Scores
- **Composition:** Rule of thirds, balance
- **Clarity:** Sharp focus, no blur
- **Color:** Appropriate saturation, contrast
- **Relevance:** Matches shot description
- **Age-appropriate:** No unsafe content

## Acceptance Criteria

- [ ] Prompt JSON files exist for all 30 scripts
- [ ] Batch A keyframes generated for all shots (~180-300 images)
- [ ] All images are 1080×1920 PNG format
- [ ] Generation parameters logged per image
- [ ] Optional: Batch B variants generated with LoRA/ControlNet
- [ ] Selection manifest exists for all scripts
- [ ] Best keyframe selected per shot with rationale
- [ ] All images age-appropriate and segment-relevant

## Related Files

- `/images/keyframes_v1/{segment}/{age}/` - Initial keyframes
- `/images/keyframes_v2/{segment}/{age}/` - Refined variants (optional)
- `/scenes/json/{segment}/{age}/` - Shot descriptions (input)
- `/config/pipeline.yaml` - SDXL model configuration
- `/research/python/sdxl_keyframe.py` - SDXL generation implementation

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 15: keyframes_v1
- Step 16: keyframes_v2 (if using batch B)

Comment `@copilot check` when keyframe generation is complete.

## Notes

- Estimated shots per video: 6-10
- Total shots across 30 scripts: ~180-300
- With variants (A+B): ~360-600 images total
- Use GPU for faster generation (CUDA recommended)
- Consider disk space: ~50-100GB for all images
- Batch processing recommended for efficiency
