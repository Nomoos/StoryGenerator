# Images: SDXL Prompt Builder

**ID:** `09-images-01-prompt-builder`  
**Priority:** P1  
**Effort:** 3-4 hours  
**Status:** ✅ Implementation Complete (Integration Required)

## Overview

Generate detailed SDXL-optimized prompts from shot descriptions in the shotlist. This task transforms high-level scene descriptions into precise, structured prompts that guide the AI image generation process to create consistent, high-quality keyframes.

**Implementation:** C# service `Generators.KeyframeGenerationService` includes prompt building functionality that converts shot descriptions into SDXL-compatible prompts with style modifiers, quality tags, and negative prompts.

## Dependencies

**Requires:**
- `06-scenes-02` - Shot list with scene descriptions and visual specifications

**Blocks:**
- `09-images-02` - Keyframe generation batch A requires prompts
- `09-images-03` - Keyframe generation batch B requires prompts

## Acceptance Criteria

- [x] C# implementation complete (part of `KeyframeGenerationService`)
- [ ] Integration testing with real shotlists
- [ ] Prompts generated for all shots in shotlist
- [ ] SDXL-optimized format with quality tags
- [ ] Negative prompts included for each shot
- [ ] Style consistency maintained across prompts
- [ ] Character/setting descriptions preserved
- [ ] JSON manifest generated
- [ ] Documentation updated

## Task Details

### Implementation

**C# Service:** `Generators.KeyframeGenerationService`

The prompt builder is integrated into the keyframe generation pipeline:

```csharp
public class KeyframeGenerationConfig
{
    public string BasePrompt { get; set; }  // Character/style description
    public string NegativePrompt { get; set; }  // Things to avoid
    public string LoraPath { get; set; }  // Optional LoRA for style
    public int VariantsPerShot { get; set; } = 3;
    public int TopNPerShot { get; set; } = 1;
}
```

**Prompt Construction Algorithm:**

```
For each shot in shotlist:
  1. Extract shot description and visual details
  2. Combine with base character/style description
  3. Add SDXL quality tags (masterpiece, best quality, etc.)
  4. Append shot-specific camera and framing instructions
  5. Add negative prompt (common artifacts, unwanted elements)
  6. Format for SDXL API compatibility
```

**Example Usage:**

```csharp
var service = new KeyframeGenerationService(imageClient);

var config = new KeyframeGenerationConfig
{
    BasePrompt = "young woman, brunette, casual clothing, indoor apartment setting",
    NegativePrompt = "ugly, deformed, blurry, text, watermark, low quality",
    VariantsPerShot = 3,
    TopNPerShot = 1
};

// Prompts are built automatically during keyframe generation
var manifest = await service.GenerateKeyframesAsync(
    shotlist: shotlist,
    titleId: "story_001",
    segment: "women",
    age: "18-23",
    config: config
);

// Access generated prompts
foreach (var keyframe in manifest.Keyframes)
{
    Console.WriteLine($"Shot {keyframe.ShotNumber}: {keyframe.Prompt}");
}
```

### Prompt Templates

**Template Structure:**

```
[Character/Setting Base] + [Shot-Specific Description] + [Camera/Framing] + [Quality Tags]

Example:
"young woman, brunette, casual clothing, looking worried at phone screen, 
close-up shot, indoor apartment, soft lighting, cinematic composition, 
masterpiece, best quality, highly detailed, 8k"
```

**Quality Tags (SDXL optimization):**
```
Positive: masterpiece, best quality, highly detailed, sharp focus, 8k, cinematic
Negative: ugly, deformed, blurry, low quality, distorted, bad anatomy, text, watermark
```

**Camera/Framing Keywords:**
```
- "close-up shot" - Face/detail focus
- "medium shot" - Upper body
- "wide shot" - Full scene
- "over-the-shoulder" - POV perspective
- "establishing shot" - Scene setting
```

### Prompt Examples

**Shot 1 - Opening Scene:**
```json
{
  "shot_number": 1,
  "description": "Young woman looking worried at her phone",
  "prompt": "young woman, brunette, casual clothing, looking worried at phone screen, anxious expression, close-up shot, indoor apartment, soft window lighting, cinematic composition, masterpiece, best quality, highly detailed, sharp focus",
  "negative_prompt": "ugly, deformed, blurry, low quality, distorted, bad anatomy, text, watermark, cartoon, anime"
}
```

**Shot 2 - Reaction Scene:**
```json
{
  "shot_number": 2,
  "description": "Close-up of woman's shocked face",
  "prompt": "young woman, brunette, shocked expression, wide eyes, mouth slightly open, extreme close-up, dramatic lighting, emotional, cinematic, masterpiece, best quality, highly detailed, 8k",
  "negative_prompt": "ugly, deformed, blurry, low quality, distorted, multiple faces, text, watermark"
}
```

**Shot 3 - Flashback Scene:**
```json
{
  "shot_number": 3,
  "description": "Happier times with friend",
  "prompt": "two young women, smiling, laughing together, casual outdoor setting, park bench, sunny day, warm tones, medium shot, nostalgic mood, soft focus background, masterpiece, best quality, highly detailed",
  "negative_prompt": "ugly, deformed, blurry, sad, dark, low quality, distorted, text, watermark"
}
```

### Testing

```bash
# C# unit tests
cd src/CSharp
dotnet test --filter "FullyQualifiedName~KeyframeGeneration"

# Integration test - generates prompts for all shots
cd src/CSharp/Examples
dotnet run --project KeyframeGenerationExample.csproj

# Verify prompts in manifest
cat data/Generator/images/prompts/women/18-23/story_001_prompts.json | jq

# Python tests (if needed)
pytest tests/pipeline/test_image_generation.py::test_prompt_builder -v
```

## Output Files

**Primary Outputs:**
```
data/Generator/images/prompts/{gender}/{age}/
└── {title_id}_prompts.json    # Complete prompt manifest
```

**Prompt Manifest Structure:**

```json
{
  "titleId": "story_001",
  "segment": "women",
  "age": "18-23",
  "generatedAt": "2024-01-15T10:30:00Z",
  "basePrompt": "young woman, brunette, casual clothing, indoor apartment setting",
  "negativePrompt": "ugly, deformed, blurry, text, watermark, low quality",
  "shots": [
    {
      "shotNumber": 1,
      "description": "Looking worried at phone",
      "prompt": "young woman, brunette, casual clothing, looking worried at phone screen...",
      "negativePrompt": "ugly, deformed, blurry, low quality, distorted...",
      "cameraAngle": "close-up",
      "lighting": "soft window light"
    }
  ]
}
```

**Example:**
```
data/Generator/images/prompts/women/18-23/
└── story_001_prompts.json
```

## Related Files

**C# Implementation:**
- `src/CSharp/Generators/KeyframeGenerationService.cs`
- `src/CSharp/Interfaces/IKeyframeGenerationService.cs`
- `src/CSharp/Examples/KeyframeGenerationExample.cs`

**Documentation:**
- `src/CSharp/KEYFRAME_GENERATION_README.md`
- `docs/PIPELINE_ORCHESTRATION.md` (Section: Image Generation)

**Tests:**
- `tests/pipeline/test_image_generation.py`

## Notes

### SDXL Best Practices

**Prompt Length:**
- Optimal: 75-150 tokens
- Maximum: 77 tokens per CLIP encoder
- Use concise, descriptive phrases

**Quality Tags:**
Always include these for best results:
- "masterpiece" - High quality indicator
- "best quality" - Quality reinforcement  
- "highly detailed" - Detail emphasis
- "8k" or "4k" - Resolution hint

**Negative Prompts:**
Essential exclusions:
- "ugly, deformed, blurry" - Artifact prevention
- "low quality" - Quality floor
- "text, watermark" - Clean images
- "bad anatomy" - Human subjects

### Style Consistency

**Character Descriptions:**
- Define once in `basePrompt`
- Reuse across all shots
- Update only for dramatic changes (costume, age)

**Setting/Environment:**
- Maintain consistent location descriptions
- Update lighting per shot
- Vary camera angles for visual interest

**LoRA Integration:**
- Use LoRA for character consistency
- Specify LoRA path in config
- LoRA weight: 0.7-0.9 for subtle style

### Common Issues

**Problem:** Inconsistent character appearance
**Solution:** Use LoRA or detailed character description in basePrompt

**Problem:** Low quality outputs
**Solution:** Ensure quality tags and negative prompts are included

**Problem:** Unwanted text in images  
**Solution:** Add "text, watermark, letters" to negative prompt

**Problem:** Incorrect framing/composition
**Solution:** Be explicit with camera angles and shot types

## Next Steps

After completion:
- ✅ `09-images-02-keyframe-gen-a` - Generate keyframes using prompts (shots 1-N/2)
- ✅ `09-images-03-keyframe-gen-b` - Generate keyframes using prompts (shots N/2+1-N)
- Test prompt quality with sample generations
- Refine prompt templates based on output quality
- Create prompt library for common scene types
- Document best practices for different video genres
