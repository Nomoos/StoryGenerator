# Pipeline Orchestration - P1 High Priority

**Status:** Implementation Guide  
**Priority:** P1 (High)  
**Phase:** 4 - Pipeline Orchestration

## Overview

This document describes the complete pipeline orchestration system for StoryGenerator, integrating all 41 P1-High priority tasks across 10 implementation groups. The pipeline transforms raw content ideas into finished videos ready for distribution.

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     StoryGenerator Pipeline                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐     │
│  │   Content    │──────▶│     Idea     │──────▶│   Script     │     │
│  │  Collection  │      │  Generation  │      │ Development  │     │
│  └──────────────┘      └──────────────┘      └──────────────┘     │
│         │                     │                     │               │
│         │                     │                     │               │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐     │
│  │    Scene     │──────▶│    Audio     │──────▶│  Subtitle    │     │
│  │   Planning   │      │  Production  │      │  Creation    │     │
│  └──────────────┘      └──────────────┘      └──────────────┘     │
│         │                     │                     │               │
│         │                     │                     │               │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐     │
│  │    Image     │──────▶│    Video     │──────▶│     Post     │     │
│  │  Generation  │      │  Production  │      │ Production   │     │
│  └──────────────┘      └──────────────┘      └──────────────┘     │
│         │                     │                     │               │
│         │                     │                     │               │
│  ┌──────────────┐      ┌──────────────┐                           │
│  │   Quality    │──────▶│    Export    │                           │
│  │   Control    │      │  & Delivery  │                           │
│  └──────────────┘      └──────────────┘                           │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Pipeline Groups

### 1. Idea Generation (7 tasks)
**Location:** `issues/p1-high/idea-generation/`  
**Purpose:** Transform raw content into structured video ideas with viral potential scoring

**Tasks:**
1. `03-ideas-01-reddit-adaptation` - Adapt Reddit stories into video ideas
2. `03-ideas-02-llm-generation` - Generate original ideas using LLM
3. `03-ideas-03-clustering` - Cluster ideas into topics
4. `03-ideas-04-title-generation` - Generate clickable titles from topics
5. `04-scoring-01-title-scorer` - Score titles for viral potential (0-100)
6. `04-scoring-02-voice-recommendation` - Recommend narrator voice (F/M)
7. `04-scoring-03-top-selection` - Select top 5 titles per segment

**Dependencies:** Content Pipeline (P0)  
**Outputs:** `selected/{gender}/{age}/top_5_titles.json`

### 2. Script Development (5 tasks)
**Location:** `issues/p1-high/script-development/`  
**Purpose:** Generate, score, and iteratively improve scripts for selected titles

**Tasks:**
1. `05-script-01-raw-generation` - Generate initial script (v0)
2. `05-script-02-script-scorer` - Score script quality
3. `05-script-03-iteration` - Iterate locally until quality plateau
4. `05-script-04-gpt-improvement` - Enhance with GPT/local LLM (v2+)
5. `05-script-05-title-improvement` - Generate improved title variants

**Dependencies:** Idea Generation (top 5 titles)  
**Outputs:** `scripts/{title}/script_v2.txt`

### 3. Scene Planning (3 tasks)
**Location:** `issues/p1-high/scene-planning/`  
**Purpose:** Create visual storyboard and shot planning for scripts

**Tasks:**
1. `06-scenes-01-beat-sheet` - Generate story beat sheet
2. `06-scenes-02-shotlist` - Create detailed shot list
3. `06-scenes-03-draft-subtitles` - Prepare draft subtitle lines

**Dependencies:** Script Development (improved script)  
**Outputs:** `scenes/{title}/beat_sheet.json`, `scenes/{title}/shot_list.json`

### 4. Audio Production (2 tasks)
**Location:** `issues/p1-high/audio-production/`  
**Purpose:** Generate high-quality voiceover with proper audio normalization

**Tasks:**
1. `07-audio-01-tts-generation` - Generate TTS voiceover (ElevenLabs)
2. `07-audio-02-normalization` - Normalize audio levels (LUFS -14.0)

**Dependencies:** Script Development, Voice Recommendation  
**Outputs:** `audio/{title}/voiceover_normalized.wav`

### 5. Subtitle Creation (2 tasks)
**Location:** `issues/p1-high/subtitle-creation/`  
**Purpose:** Create precisely timed subtitles synchronized with audio

**Tasks:**
1. `08-subtitles-01-forced-alignment` - Forced alignment with Whisper
2. `08-subtitles-02-scene-mapping` - Map subtitles to scene beats

**Dependencies:** Audio Production, Scene Planning  
**Outputs:** `subtitles/{title}/subtitles.srt`, `subtitles/{title}/scene_mapping.json`

### 6. Image Generation (4 tasks)
**Location:** `issues/p1-high/image-generation/`  
**Purpose:** Generate SDXL keyframes for each scene

**Tasks:**
1. `09-images-01-prompt-builder` - Build SDXL prompts from shot list
2. `09-images-02-keyframe-gen-a` - Generate keyframes (Batch A)
3. `09-images-03-keyframe-gen-b` - Generate variants (Batch B)
4. `09-images-04-selection` - Select best keyframe per scene

**Dependencies:** Scene Planning  
**Outputs:** `images/{title}/scene_{n}/keyframe.png`

### 7. Video Production (3 tasks)
**Location:** `issues/p1-high/video-production/`  
**Purpose:** Synthesize video clips from keyframes

**Tasks:**
1. `10-video-01-ltx-generation` - Generate video with LTX-Video
2. `10-video-02-interpolation` - Frame interpolation (RIFE/FILM)
3. `10-video-03-variant-selection` - Select best video variant

**Dependencies:** Image Generation  
**Outputs:** `videos/{title}/scene_{n}/video.mp4`

### 8. Post-Production (6 tasks)
**Location:** `issues/p1-high/post-production/`  
**Purpose:** Finalize video with effects, subtitles, and audio

**Tasks:**
1. `11-post-01-crop-resize` - Crop to 9:16 aspect ratio
2. `11-post-02-subtitle-burn` - Burn/soft-code subtitles
3. `11-post-03-bgm-sfx` - Add background music and sound effects
4. `11-post-04-concatenation` - Concatenate all scene clips
5. `11-post-05-transitions` - Add transitions between scenes
6. `11-post-06-color-grading` - Apply color grading

**Dependencies:** Video Production, Subtitle Creation  
**Outputs:** `post/{title}/video_final.mp4`

### 9. Quality Control (3 tasks)
**Location:** `issues/p1-high/quality-control/`  
**Purpose:** Validate video quality and A/V sync

**Tasks:**
1. `12-qc-01-device-preview` - Generate device previews
2. `12-qc-02-sync-check` - Verify A/V synchronization
3. `12-qc-03-quality-report` - Generate quality assessment report

**Dependencies:** Post-Production  
**Outputs:** `qc/{title}/quality_report.json`

### 10. Export & Delivery (3 tasks)
**Location:** `issues/p1-high/export-delivery/`  
**Purpose:** Prepare final deliverables for distribution

**Tasks:**
1. `13-export-01-final-encode` - Final video encoding
2. `13-export-02-thumbnail` - Generate thumbnail image
3. `13-export-03-metadata` - Create metadata JSON

**Dependencies:** Quality Control  
**Outputs:** `export/{title}/final.mp4`, `export/{title}/thumbnail.jpg`, `export/{title}/metadata.json`

## Pipeline Configuration

### Stage Configuration

Each pipeline stage can be individually enabled/disabled in `appsettings.json`:

```json
{
  "Pipeline": {
    "Name": "StoryGenerator Full Pipeline",
    "Steps": {
      "StoryIdea": true,
      "ScriptGeneration": true,
      "ScriptRevision": true,
      "ScriptEnhancement": true,
      "VoiceSynthesis": true,
      "AsrSubtitles": true,
      "SceneAnalysis": true,
      "SceneDescription": true,
      "KeyframeGeneration": true,
      "VideoInterpolation": true,
      "VideoComposition": true
    }
  }
}
```

### Path Configuration

```json
{
  "Paths": {
    "StoryRoot": "./Stories",
    "Ideas": "0_Ideas",
    "Scripts": "1_Scripts",
    "Revised": "2_Revised",
    "Voiceover": "3_VoiceOver",
    "Titles": "4_Titles",
    "Scenes": "scenes",
    "Images": "images",
    "Videos": "videos",
    "Final": "final"
  }
}
```

## Execution Workflow

### Sequential Execution (Basic)

```bash
# Run complete pipeline
dotnet run --project src/CSharp/StoryGenerator.CLI -- full-pipeline

# Run with specific story idea
dotnet run --project src/CSharp/StoryGenerator.CLI -- full-pipeline --idea "falling for someone"
```

### Resume from Checkpoint

```bash
# Pipeline saves checkpoints after each stage
# Resume from last checkpoint
dotnet run --project src/CSharp/StoryGenerator.CLI -- full-pipeline --resume
```

### Stage-by-Stage Execution

```bash
# Run individual stages
dotnet run --project src/CSharp/StoryGenerator.CLI -- generate-ideas --topic "friendship" --count 5
dotnet run --project src/CSharp/StoryGenerator.CLI -- generate-script --idea-file ./0_Ideas/story.json
dotnet run --project src/CSharp/StoryGenerator.CLI -- revise-script --script-file ./1_Scripts/story.txt
dotnet run --project src/CSharp/StoryGenerator.CLI -- generate-voice --script-file ./2_Revised/story.txt
dotnet run --project src/CSharp/StoryGenerator.CLI -- generate-subtitles --audio-file ./3_VoiceOver/story.wav
```

## State Management

### Checkpoint System

The pipeline automatically saves checkpoints after completing each stage:

```json
{
  "pipelineId": "story-123",
  "startTime": "2025-01-15T10:00:00Z",
  "currentStage": "script_revision",
  "completedStages": [
    "story_idea",
    "script_generation"
  ],
  "stageData": {
    "story_idea": {
      "storyTitle": "A Tale of Friendship",
      "completedAt": "2025-01-15T10:05:00Z"
    },
    "script_generation": {
      "scriptPath": "./1_Scripts/A_Tale_of_Friendship.txt",
      "completedAt": "2025-01-15T10:15:00Z"
    }
  }
}
```

### Error Recovery

If a stage fails, the pipeline:
1. Logs the error with full stack trace
2. Saves checkpoint with current progress
3. Provides resume command
4. Allows retry with `--resume` flag

## Parallelization Strategy

### Within Groups (Horizontal Scaling)

Multiple titles can be processed in parallel:

```bash
# Process 5 titles simultaneously
for title in title1 title2 title3 title4 title5; do
  dotnet run --project src/CSharp/StoryGenerator.CLI -- full-pipeline --idea "$title" &
done
wait
```

### Cross-Stage Optimization

Independent stages can run in parallel:
- Scene Planning + Audio Production (both depend on Script)
- Image Generation (multiple scenes in parallel)
- Video Production (multiple clips in parallel)
- Quality Control checks (multiple validations in parallel)

## Performance Considerations

### Resource Management

- **Memory**: Each stage has configurable memory limits
- **GPU**: Image and video generation stages require GPU
- **Disk**: Monitor disk space for intermediate artifacts
- **Network**: API rate limits for OpenAI, ElevenLabs

### Optimization Tips

1. **Batch Processing**: Process multiple titles together
2. **Caching**: Reuse generated assets when possible
3. **Parallel Execution**: Run independent stages concurrently
4. **Checkpoint Frequency**: Balance between safety and performance
5. **Artifact Cleanup**: Clean intermediate files after successful completion

## Monitoring & Logging

### Progress Tracking

```
📝 STEP 1: Story Idea Generation
────────────────────────────────────────────────────────────────────────────────
✓ Generated story idea: "A Tale of Friendship"
✓ Checkpoint saved

📝 STEP 2: Script Generation
────────────────────────────────────────────────────────────────────────────────
✓ Generated script (1250 words)
✓ Checkpoint saved

✏️ STEP 3: Script Revision
────────────────────────────────────────────────────────────────────────────────
✓ Script revised (1280 words, +2.4% improvement)
✓ Checkpoint saved
```

### Logging Levels

- **Info**: Stage start/completion, checkpoints
- **Debug**: Detailed operation logs
- **Warning**: Recoverable errors, retries
- **Error**: Stage failures, critical issues

## Testing Strategy

### Unit Tests

Test individual stage implementations:

```csharp
[Fact]
public async Task IdeaGenerationStage_ValidInput_ReturnsIdeas()
{
    // Arrange
    var stage = new IdeaGenerationStage(mockGenerator, mockLogger);
    var input = new IdeaGenerationInput { Topic = "friendship", Count = 5 };
    
    // Act
    var output = await stage.ExecuteAsync(input, CancellationToken.None);
    
    // Assert
    Assert.Equal(5, output.Ideas.Count);
}
```

### Integration Tests

Test complete pipeline flows:

```csharp
[Fact]
public async Task FullPipeline_GeneratesCompleteVideo()
{
    // Arrange
    var orchestrator = CreateTestOrchestrator();
    
    // Act
    var result = await orchestrator.RunFullPipelineAsync("test story");
    
    // Assert
    Assert.True(File.Exists(result.VideoPath));
    Assert.True(File.Exists(result.ThumbnailPath));
    Assert.True(File.Exists(result.MetadataPath));
}
```

### Performance Tests

Measure pipeline execution time:

```csharp
[Fact]
public async Task FullPipeline_CompletesInReasonableTime()
{
    var stopwatch = Stopwatch.StartNew();
    await orchestrator.RunFullPipelineAsync();
    stopwatch.Stop();
    
    Assert.True(stopwatch.Elapsed < TimeSpan.FromMinutes(30));
}
```

## Troubleshooting

### Common Issues

1. **Pipeline Hangs**: Check for network timeouts, increase timeout values
2. **Out of Memory**: Reduce batch sizes, enable cleanup of intermediate files
3. **API Rate Limits**: Implement exponential backoff, use local models
4. **GPU Out of Memory**: Reduce image/video batch sizes
5. **Checkpoint Corruption**: Delete checkpoint file and restart

### Debug Mode

Enable detailed logging:

```bash
export LOG_LEVEL=Debug
dotnet run --project src/CSharp/StoryGenerator.CLI -- full-pipeline
```

## Next Steps

1. **P2 Tasks**: Distribution (YouTube, TikTok, Instagram)
2. **Analytics**: Track performance metrics
3. **Optimization**: Pipeline performance tuning
4. **Scale**: Multi-machine distributed processing
5. **Monitoring**: Production monitoring and alerting

## Related Documentation

- [P1 High Priority Overview](../issues/p1-high/README.md)
- [Pipeline Configuration Guide](./PIPELINE_CONFIGURATION.md)
- [CLI Usage Guide](./CLI_USAGE.md)
- [Checkpoint System](./CHECKPOINT_SYSTEM.md)
