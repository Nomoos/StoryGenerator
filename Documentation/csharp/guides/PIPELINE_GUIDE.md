# Pipeline Architecture Guide

**StoryGenerator Pipeline** - Complete end-to-end video generation pipeline

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Pipeline Stages](#pipeline-stages)
- [Checkpoint Management](#checkpoint-management)
- [Error Handling](#error-handling)
- [Configuration](#configuration)
- [Testing](#testing)
- [Performance](#performance)

## Overview

The StoryGenerator pipeline is a comprehensive system for generating short-form video content from story ideas. It implements a multi-stage pipeline that transforms raw content into polished, subtitled videos ready for distribution.

### Key Features

- **11 Pipeline Stages**: From idea generation to final video composition
- **Checkpoint System**: Resume from any stage after interruption
- **Error Handling**: Automatic retry with exponential backoff
- **Progress Tracking**: Real-time progress reporting with timing
- **Configuration**: Flexible JSON-based configuration
- **SOLID Architecture**: Clean, testable, maintainable code

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────────┐
│                   StoryGenerator Pipeline                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐              │
│  │   Story    │──▶│   Script   │──▶│  Revision  │              │
│  │    Idea    │   │ Generation │   │            │              │
│  └────────────┘   └────────────┘   └────────────┘              │
│        │                 │                 │                     │
│        ▼                 ▼                 ▼                     │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐              │
│  │Enhancement │──▶│   Voice    │──▶│ Subtitles  │              │
│  │            │   │ Synthesis  │   │    (ASR)   │              │
│  └────────────┘   └────────────┘   └────────────┘              │
│        │                 │                 │                     │
│        ▼                 ▼                 ▼                     │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐              │
│  │   Scene    │──▶│   Scene    │──▶│  Keyframe  │              │
│  │  Analysis  │   │Description │   │ Generation │              │
│  └────────────┘   └────────────┘   └────────────┘              │
│        │                 │                 │                     │
│        ▼                 ▼                 ▼                     │
│  ┌────────────┐   ┌────────────┐                               │
│  │   Video    │──▶│   Final    │                               │
│  │Interpolate │   │Composition │                               │
│  └────────────┘   └────────────┘                               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Core Components

#### PipelineOrchestrator

The main orchestrator that coordinates all pipeline stages.

**Location:** `StoryGenerator.Pipeline/Core/PipelineOrchestrator.cs`

**Responsibilities:**
- Execute pipeline stages in sequence
- Manage checkpoint state
- Handle errors and recovery
- Track progress and timing
- Coordinate service dependencies

**Key Methods:**
```csharp
public async Task<string> RunFullPipelineAsync(string? storyTitle = null)
```

#### PipelineCheckpointManager

Manages pipeline state persistence and recovery.

**Location:** `StoryGenerator.Pipeline/Services/PipelineCheckpointManager.cs`

**Responsibilities:**
- Save checkpoint after each stage
- Load checkpoint on resume
- Validate checkpoint integrity
- Provide atomic save operations

**Key Methods:**
```csharp
public async Task SaveCheckpointAsync(PipelineCheckpoint checkpoint, CancellationToken cancellationToken = default)
public async Task<PipelineCheckpoint> LoadCheckpointAsync(CancellationToken cancellationToken = default)
```

#### ErrorHandlingService

Provides retry logic and circuit breaker pattern.

**Location:** `StoryGenerator.Pipeline/Services/ErrorHandlingService.cs`

**Responsibilities:**
- Execute operations with retry logic
- Implement exponential backoff
- Circuit breaker for failing operations
- Classify retriable vs. non-retriable errors

**Key Methods:**
```csharp
public async Task<T> ExecuteWithRetryAsync<T>(string operationName, Func<Task<T>> operation, CancellationToken cancellationToken = default)
```

#### PipelineLogger

Structured logging for pipeline operations.

**Location:** `StoryGenerator.Pipeline/Core/PipelineLogger.cs`

**Responsibilities:**
- Log pipeline events
- Track stage timing
- Record metrics
- Provide debug information

## Pipeline Stages

### Stage 1: Story Idea Generation

**Purpose:** Generate or select a story idea for the video.

**Input:** Topic or manual selection  
**Output:** Story title and metadata  
**Python Script:** `Generation/Manual/MIdea.py`

**Configuration:**
```json
{
  "Pipeline": {
    "Steps": {
      "StoryIdea": true
    }
  },
  "Generation": {
    "Story": {
      "Count": 1,
      "Tone": "emotional",
      "Theme": "friendship"
    }
  }
}
```

### Stage 2: Script Generation

**Purpose:** Generate initial ~360-word script from story idea.

**Input:** Story title  
**Output:** Raw script text  
**Python Script:** `Generation/Manual/MScript.py`

**Configuration:**
```json
{
  "Pipeline": {
    "Steps": {
      "ScriptGeneration": true
    }
  },
  "Generation": {
    "Story": {
      "TargetLength": 360
    }
  }
}
```

### Stage 3: Script Revision

**Purpose:** Revise script for voice clarity and AI TTS optimization.

**Input:** Raw script  
**Output:** Revised script  
**Python Script:** `Generation/Manual/MRevise.py`

### Stage 4: Script Enhancement

**Purpose:** Add ElevenLabs voice tags for emphasis and emotion.

**Input:** Revised script  
**Output:** Enhanced script with voice tags  
**Python Script:** `Generation/Manual/MEnhance.py`

### Stage 5: Voice Synthesis

**Purpose:** Generate high-quality TTS voiceover using ElevenLabs.

**Input:** Enhanced script  
**Output:** Audio file (WAV/MP3)  
**Python Script:** `Generation/Manual/MVoice.py`

**Configuration:**
```json
{
  "Pipeline": {
    "Steps": {
      "VoiceSynthesis": true
    }
  },
  "Generation": {
    "Voice": {
      "Model": "eleven_v3",
      "VoiceId": "BZgkqPqms7Kj9ulSkVzn",
      "Stability": 0.5,
      "SimilarityBoost": 0.75,
      "NormalizeAudio": true,
      "TargetLufs": -14.0
    }
  }
}
```

### Stage 6: ASR & Subtitles

**Purpose:** Generate word-level subtitles using forced alignment.

**Input:** Audio file + script  
**Output:** SRT subtitle file  
**Python Script:** `Generation/Manual/MSubtitles.py`

### Stage 7: Scene Analysis

**Purpose:** Analyze script to identify scene boundaries and beats.

**Input:** Revised script  
**Output:** Scene structure JSON  
**Service:** `SceneAnalysisService`

### Stage 8: Scene Description

**Purpose:** Generate visual descriptions for each scene.

**Input:** Scene structure  
**Output:** Scene descriptions with prompts  
**Service:** `SceneDescriptionService`

### Stage 9: Keyframe Generation

**Purpose:** Generate keyframe images for each scene.

**Input:** Scene descriptions  
**Output:** Keyframe images (PNG/JPG)  
**Python Script:** `Generation/Video/MKeyframes.py`

**Configuration:**
```json
{
  "Pipeline": {
    "Steps": {
      "KeyframeGeneration": true
    }
  },
  "Generation": {
    "Image": {
      "Model": "sdxl",
      "Width": 1024,
      "Height": 1024,
      "Steps": 30,
      "GuidanceScale": 7.5
    }
  }
}
```

### Stage 10: Video Interpolation

**Purpose:** Generate video clips from keyframes using LTX-Video or frame interpolation.

**Input:** Keyframe images  
**Output:** Video clips (MP4)  
**Service:** `VideoGenerationService`

**Methods:**
- **LTX:** AI-powered video synthesis
- **Keyframe:** Traditional frame interpolation (RIFE/FILM)

**Configuration:**
```json
{
  "Pipeline": {
    "Steps": {
      "VideoInterpolation": true
    }
  },
  "Generation": {
    "Video": {
      "SynthesisMethod": "ltx",
      "Resolution": {
        "Width": 1080,
        "Height": 1920
      },
      "Fps": 30
    }
  }
}
```

### Stage 11: Final Video Composition

**Purpose:** Compose all video clips into final video with audio and subtitles.

**Input:** Video clips + audio + subtitles  
**Output:** Final video file  
**Service:** `VideoCompositionService`

**Configuration:**
```json
{
  "Pipeline": {
    "Steps": {
      "VideoComposition": true
    }
  },
  "Generation": {
    "Video": {
      "Codec": "libx264",
      "AudioCodec": "aac",
      "Bitrate": "8M",
      "Quality": "high"
    }
  }
}
```

## Checkpoint Management

### Checkpoint Format

Checkpoints are stored as JSON files:

```json
{
  "completedSteps": {
    "story_idea": true,
    "script_generation": true,
    "script_revision": true
  },
  "stepData": {
    "story_idea": "Falling_For_Someone",
    "script_generation": "Falling_For_Someone",
    "script_revision": "Falling_For_Someone"
  },
  "lastUpdated": "2025-01-15T10:30:00Z"
}
```

### Default Location

```
./Stories/pipeline_checkpoint.json
```

### Configuration

```json
{
  "Processing": {
    "Checkpointing": {
      "Enabled": true,
      "ResumeFromCheckpoint": true
    }
  }
}
```

### Resume Behavior

When resuming from a checkpoint:

1. Load checkpoint file
2. Validate checkpoint integrity
3. Skip completed stages
4. Continue from next incomplete stage
5. Update checkpoint after each stage

### Atomic Operations

Checkpoint saves use atomic operations:

1. Write to temporary file
2. Verify write success
3. Backup existing checkpoint (if any)
4. Replace with new checkpoint
5. Clean up backup on success

## Error Handling

### Retry Strategy

The pipeline implements automatic retry with exponential backoff:

**Configuration:**
```json
{
  "Processing": {
    "ErrorHandling": {
      "RetryCount": 3,
      "RetryDelay": 2
    }
  }
}
```

**Behavior:**
- Attempt 1: Immediate
- Attempt 2: Wait 2 seconds
- Attempt 3: Wait 4 seconds
- Attempt 4: Wait 8 seconds

### Circuit Breaker

Operations that fail repeatedly trigger a circuit breaker:

- **Threshold:** 5 consecutive failures
- **Open State:** Block operation for 5 minutes
- **Half-Open:** Try again after timeout
- **Closed:** Reset on success

### Retriable Errors

The following errors are automatically retried:
- Network errors (`HttpRequestException`)
- Timeout errors (`TaskCanceledException`, `TimeoutException`)
- IO errors (`IOException`)

### Non-Retriable Errors

The following errors fail immediately:
- Authentication errors (invalid API keys)
- Validation errors (invalid input)
- Logic errors (ArgumentException, InvalidOperationException)

### Error Recovery

When a stage fails:

1. Log error with full stack trace
2. Save checkpoint with current progress
3. Display recovery instructions
4. Exit with error code

**Recovery:**
```bash
# Pipeline automatically saves checkpoint
dotnet run -- pipeline-resume
```

## Configuration

### Complete Configuration Example

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
  },
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
    "Final": "final",
    "PythonRoot": "./Python",
    "Resources": "./resources",
    "BackgroundImage": "./resources/background.jpg"
  },
  "Generation": {
    "Story": {
      "Count": 1,
      "Tone": "emotional",
      "Theme": "friendship",
      "TargetLength": 360
    },
    "Voice": {
      "Model": "eleven_v3",
      "VoiceId": "BZgkqPqms7Kj9ulSkVzn",
      "Stability": 0.5,
      "SimilarityBoost": 0.75,
      "NormalizeAudio": true,
      "TargetLufs": -14.0
    },
    "Video": {
      "Resolution": {
        "Width": 1080,
        "Height": 1920
      },
      "Fps": 30,
      "Codec": "libx264",
      "AudioCodec": "aac",
      "Bitrate": "8M",
      "Quality": "high",
      "SynthesisMethod": "ltx"
    },
    "Image": {
      "Model": "sdxl",
      "Width": 1024,
      "Height": 1024,
      "Steps": 30,
      "GuidanceScale": 7.5
    }
  },
  "Processing": {
    "Checkpointing": {
      "Enabled": true,
      "ResumeFromCheckpoint": true
    },
    "ErrorHandling": {
      "RetryCount": 3,
      "RetryDelay": 2
    }
  }
}
```

### Environment Variables

Override configuration with environment variables:

```bash
export STORY_ROOT="./custom-output"
export OPENAI_API_KEY="sk-..."
export ELEVENLABS_API_KEY="..."
export ELEVENLABS_VOICE_ID="custom-voice-id"
```

## Testing

### Unit Tests

Test individual components:

```bash
cd src/CSharp
dotnet test --filter "Category=Pipeline"
```

**Example Tests:**
- `PipelineCheckpoint_CompleteStep_UpdatesState`
- `CheckpointManager_SaveAndLoad_PreservesData`
- `ErrorHandlingService_RetryWithBackoff`

### Integration Tests

Test complete pipeline flows:

```bash
cd src/CSharp
dotnet test --filter "Category=Integration"
```

**Example Tests:**
- `FullPipeline_GeneratesCompleteVideo`
- `Pipeline_ResumesFromCheckpoint`
- `Pipeline_HandlesStageFailure`

### Test Configuration

Use test-specific configuration:

```json
{
  "Pipeline": {
    "Name": "Test Pipeline",
    "Steps": {
      "StoryIdea": true,
      "ScriptGeneration": true,
      "ScriptRevision": false,
      "ScriptEnhancement": false,
      "VoiceSynthesis": false,
      "AsrSubtitles": false,
      "SceneAnalysis": false,
      "SceneDescription": false,
      "KeyframeGeneration": false,
      "VideoInterpolation": false,
      "VideoComposition": false
    }
  },
  "Paths": {
    "StoryRoot": "./test-output"
  }
}
```

## Performance

### Typical Execution Times

**Full Pipeline:** ~20-30 minutes
- Story Idea: 10-30 seconds
- Script Generation: 1-2 minutes
- Script Revision: 30-60 seconds
- Script Enhancement: 30-60 seconds
- Voice Synthesis: 2-3 minutes
- ASR & Subtitles: 1-2 minutes
- Scene Analysis: 10-30 seconds
- Scene Description: 1-2 minutes
- Keyframe Generation: 5-10 minutes
- Video Interpolation: 5-15 minutes
- Final Composition: 1-2 minutes

### Optimization Tips

1. **Parallel Processing:** Run multiple stories in parallel
2. **Caching:** Reuse generated assets when possible
3. **GPU Acceleration:** Use GPU for image/video generation
4. **Batch Operations:** Process multiple scenes together
5. **Checkpoint Cleanup:** Remove checkpoints after success

### Resource Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Disk: 10GB free space
- GPU: Optional (for faster image/video generation)

**Recommended:**
- CPU: 8+ cores
- RAM: 16GB+
- Disk: 50GB+ free space
- GPU: NVIDIA with 8GB+ VRAM (for LTX-Video)

## Additional Resources

- [CLI Usage Guide](./CLI_USAGE.md)
- [Configuration Reference](../docs/PIPELINE_ORCHESTRATION.md)
- [SOLID Principles Guide](./SOLID_OOP_CLEAN_CODE_GUIDE.md)
- [Testing Guide](./TESTING_GUIDE.md)

## Support

For issues or questions:

1. Check this documentation
2. Review [CLI_USAGE.md](./CLI_USAGE.md)
3. Search [existing issues](https://github.com/Nomoos/StoryGenerator/issues)
4. Create a new issue with:
   - Pipeline stage where issue occurred
   - Error messages and logs
   - Configuration used
   - Steps to reproduce

---

**Last Updated:** January 2025  
**Version:** Phase 4 - Pipeline Orchestration
