# Hybrid Architecture Visual Guide

> Visual diagrams and flowcharts to understand the C# + Python hybrid architecture.

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         StoryGenerator Pipeline                          │
│                     (C# Primary Orchestration Layer)                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
         ┌────────────────┐ ┌─────────────┐ ┌────────────────┐
         │   Pure C#      │ │   Hybrid    │ │  Infrastructure│
         │   Generators   │ │ Generators  │ │   Services     │
         └────────────────┘ └─────────────┘ └────────────────┘
                  │                 │                 │
                  │                 │                 │
         ┌────────┴────────┐       │        ┌────────┴────────┐
         ▼                 ▼       │        ▼                 ▼
    ┌─────────┐      ┌──────────┐ │   ┌────────┐      ┌──────────┐
    │ OpenAI  │      │ElevenLabs│ │   │ Config │      │  Logging │
    │   API   │      │   API    │ │   │  Mgmt  │      │  Service │
    └─────────┘      └──────────┘ │   └────────┘      └──────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Python Bridge  │
                          │   (Subprocess)  │
                          └─────────────────┘
                                   │
                     ┌─────────────┼─────────────┐
                     ▼             ▼             ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │ Whisper  │  │   SDXL   │  │ LTX-Video│
              │   ASR    │  │ Keyframe │  │Synthesis │
              └──────────┘  └──────────┘  └──────────┘
```

---

## 📊 Pipeline Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          Video Generation Pipeline                        │
└──────────────────────────────────────────────────────────────────────────┘

Stage 0: Idea Collection
┌─────────────────────────┐
│  C# - IdeaCollector     │ ← Reddit/Instagram/TikTok APIs
│  • API Integration      │
│  • Data Processing      │
│  • JSON Storage         │
└────────┬────────────────┘
         │
         ▼
Stage 1: Story Ideas
┌─────────────────────────┐
│  C# - IdeaGenerator     │ ← OpenAI GPT-4o-mini API
│  • LLM API Call         │
│  • Idea Structuring     │
└────────┬────────────────┘
         │
         ▼
Stage 2: Script Generation
┌─────────────────────────┐
│  C# - ScriptGenerator   │ ← OpenAI GPT-4o-mini API
│  • Prompt Engineering   │
│  • ~360 word script     │
└────────┬────────────────┘
         │
         ▼
Stage 3: Script Revision
┌─────────────────────────┐
│  C# - RevisionGen       │ ← OpenAI API
│  • TTS Optimization     │
│  • Voice Tag Addition   │
└────────┬────────────────┘
         │
         ▼
Stage 4: Voice Generation
┌─────────────────────────┐
│  C# - VoiceGenerator    │ ← ElevenLabs API
│  • TTS API Call         │
│  • FFmpeg Normalize     │ ← FFmpeg (subprocess)
└────────┬────────────────┘
         │
         ▼
Stage 5: Subtitle Generation
┌─────────────────────────┐
│  C# - SubtitleGen       │
│  ├─ Orchestration (C#)  │
│  └─ ASR (Python)        │ ← faster-whisper subprocess
│     • Word timestamps   │
│     • SRT generation    │
└────────┬────────────────┘
         │
         ▼
Stage 6: Scene Planning
┌─────────────────────────┐
│  C# - ShotlistGen       │ ← OpenAI API or Ollama
│  • Scene Analysis       │
│  • Visual Prompts       │
└────────┬────────────────┘
         │
         ▼
Stage 7: Vision Guidance (Optional)
┌─────────────────────────┐
│  C# - VisionGen         │
│  ├─ Orchestration (C#)  │
│  └─ Vision (Python)     │ ← LLaVA/Phi-3.5 subprocess
│     • Scene Validation  │
└────────┬────────────────┘
         │
         ▼
Stage 8: Keyframe Generation
┌─────────────────────────┐
│  C# - KeyframeGen       │
│  ├─ Orchestration (C#)  │
│  │  • Prompt batching   │
│  │  • File management   │
│  └─ SDXL (Python)       │ ← diffusers subprocess
│     • Image generation  │
│     • 1024×1024 output  │
└────────┬────────────────┘
         │
         ▼
Stage 9: Video Synthesis
┌─────────────────────────┐
│  C# - VideoSynthesizer  │
│  ├─ Orchestration (C#)  │
│  │  • Scene coordination│
│  │  • Timing control    │
│  └─ LTX-Video (Python)  │ ← diffusers subprocess
│     • Video generation  │
│     • 1080×1920 output  │
└────────┬────────────────┘
         │
         ▼
Stage 10: Post-Production
┌─────────────────────────┐
│  C# - Compositor        │ ← FFmpeg (subprocess)
│  • Subtitle Overlay     │
│  • Audio Sync           │
│  • Final Export         │
│  • Metadata Generation  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Final Video Output     │
│  • 1080×1920 MP4        │
│  • Subtitles embedded   │
│  • Metadata JSON        │
│  • Thumbnail image      │
└─────────────────────────┘
```

---

## 🔄 C# ↔ Python Integration Pattern

### Pattern: Subprocess Communication

```
┌───────────────────────────────────────────────────────────────┐
│                      C# Application                           │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  PipelineOrchestrator                                │    │
│  │  ├─ Manages workflow state                           │    │
│  │  ├─ Handles errors & retries                         │    │
│  │  └─ Coordinates all generators                       │    │
│  └──────────────────┬───────────────────────────────────┘    │
│                     │                                         │
│  ┌──────────────────▼───────────────────────────────────┐    │
│  │  KeyframeGenerator (C#)                              │    │
│  │  ├─ Prepare prompts & config                         │    │
│  │  ├─ Validate inputs                                  │    │
│  │  ├─ Create JSON args file                            │    │
│  │  ├─ Execute Python subprocess ──────────────┐        │    │
│  │  ├─ Parse JSON results                      │        │    │
│  │  └─ Validate outputs                        │        │    │
│  └────────────────────────────────────────────┼────────┘    │
│                                                │             │
└────────────────────────────────────────────────┼─────────────┘
                                                 │
                    Process Boundary             │
                                                 │
┌────────────────────────────────────────────────┼─────────────┐
│                 Python Subprocess              │             │
│                                                ▼             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  sdxl_generate.py                                     │  │
│  │  ├─ Read JSON args from file                         │  │
│  │  ├─ Load SDXL model (diffusers)                      │  │
│  │  ├─ Generate images (PyTorch)                        │  │
│  │  ├─ Save to disk                                     │  │
│  │  └─ Print JSON results to stdout ─────────────┐      │  │
│  └───────────────────────────────────────────────┼──────┘  │
│                                                   │         │
└───────────────────────────────────────────────────┼─────────┘
                                                    │
                                                    │
                        Return to C# ◄──────────────┘
```

### Communication Flow

```
Step 1: C# prepares request
┌─────────────────────────────────────────┐
│ C# Dictionary<string, object>           │
│ {                                       │
│   "prompts": ["scene 1", "scene 2"],    │
│   "model": "sdxl-base-1.0",            │
│   "output_dir": "./keyframes/"         │
│ }                                       │
└────────────┬────────────────────────────┘
             │ JsonSerializer.Serialize()
             ▼
Step 2: Write JSON to temp file
┌─────────────────────────────────────────┐
│ /tmp/args_abc123.json                   │
│ {"prompts":["scene 1","scene 2"],       │
│  "model":"sdxl-base-1.0",...}           │
└────────────┬────────────────────────────┘
             │
             ▼
Step 3: Execute Python subprocess
┌─────────────────────────────────────────┐
│ Process.Start()                          │
│ python sdxl_generate.py                  │
│   --input /tmp/args_abc123.json         │
└────────────┬────────────────────────────┘
             │
             ▼
Step 4: Python reads & processes
┌─────────────────────────────────────────┐
│ Python:                                  │
│ 1. Load JSON args                        │
│ 2. Load SDXL model                       │
│ 3. Generate images                       │
│ 4. Save to disk                          │
│ 5. Build result JSON                     │
└────────────┬────────────────────────────┘
             │
             ▼
Step 5: Python outputs JSON to stdout
┌─────────────────────────────────────────┐
│ stdout:                                  │
│ {                                        │
│   "success": true,                       │
│   "image_paths": [                       │
│     "./keyframes/frame_000.png",         │
│     "./keyframes/frame_001.png"          │
│   ]                                      │
│ }                                        │
└────────────┬────────────────────────────┘
             │
             ▼
Step 6: C# reads stdout
┌─────────────────────────────────────────┐
│ var json = await                         │
│   process.StandardOutput               │
│     .ReadToEndAsync();                   │
└────────────┬────────────────────────────┘
             │ JsonSerializer.Deserialize()
             ▼
Step 7: C# gets result object
┌─────────────────────────────────────────┐
│ KeyframeResult {                         │
│   Success = true,                        │
│   ImagePaths = [                         │
│     "./keyframes/frame_000.png",         │
│     "./keyframes/frame_001.png"          │
│   ]                                      │
│ }                                        │
└─────────────────────────────────────────┘
```

---

## 🎯 Decision Flow for Technology Choice

```
┌─────────────────────────────────────┐
│   Need to implement a feature?      │
└────────────┬────────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │ Is it ML inference?│
    │ (PyTorch/Diffusers)│
    └────┬──────────┬────┘
         │          │
      YES│          │NO
         │          │
         ▼          ▼
  ┌──────────┐  ┌────────────────────┐
  │  Python  │  │ Is it an API call? │
  │subprocess│  └────┬──────────┬────┘
  └──────────┘       │          │
                  YES│          │NO
                     │          │
                     ▼          ▼
              ┌──────────┐  ┌─────────────────┐
              │    C#    │  │Is it FFmpeg?    │
              │HttpClient│  └────┬──────┬─────┘
              └──────────┘       │      │
                              YES│      │NO
                                 │      │
                                 ▼      ▼
                          ┌──────────┐  ┌──────────┐
                          │C# FFmpeg │  │   C#     │
                          │subprocess│  │ Default  │
                          └──────────┘  └──────────┘
```

---

## 📈 Performance Characteristics

### Subprocess Overhead Analysis

```
Pipeline Stage Timeline
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  SDXL Image Generation (1024×1024)                        │
│  ┌──┬───────────────────────────────────────────────┐    │
│  │  │                                                │    │
│  │50│            5-10 seconds (GPU)                  │    │
│  │ms│                                                │    │
│  └──┴───────────────────────────────────────────────┘    │
│  ↑                                                         │
│  Subprocess overhead (50-200ms) = ~1-4% of total time     │
│                                                            │
│  LTX-Video Generation (5s @ 1080×1920)                    │
│  ┌──┬──────────────────────────────────────────────────┐ │
│  │  │                                                   │ │
│  │50│            15-30 seconds (GPU)                    │ │
│  │ms│                                                   │ │
│  └──┴──────────────────────────────────────────────────┘ │
│  ↑                                                         │
│  Subprocess overhead = ~0.3-1% of total time              │
│                                                            │
│  Whisper ASR (60s audio)                                  │
│  ┌──┬──────────────────────┐                             │
│  │  │                      │                             │
│  │50│    2-5 seconds       │                             │
│  │ms│                      │                             │
│  └──┴──────────────────────┘                             │
│  ↑                                                         │
│  Subprocess overhead = ~1-10% of total time               │
│                                                            │
└────────────────────────────────────────────────────────────┘

Conclusion: Subprocess overhead is negligible for GPU-bound tasks
```

### Memory Usage Comparison

```
Memory Footprint Over Time
┌────────────────────────────────────────────────────────────┐
│ 16GB                                                        │
│    │                                                        │
│ 12GB   Python.NET (Shared Memory)                          │
│    │   ┌──────────────────────────────────────────┐       │
│    │   │ C# + Python in same process              │       │
│  8GB   │ High memory pressure                     │       │
│    │   │ GIL contention                           │       │
│  4GB   └──────────────────────────────────────────┘       │
│    │                                                        │
│  0GB   Subprocess Pattern (Separate Processes)             │
│    │   ┌────────┐  ┌────────┐  ┌────────┐                │
│ 16GB   │        │  │        │  │        │                 │
│ 12GB   │  C#    │  │ Python │  │  C#    │                 │
│  8GB   │Process │  │Subprocess  │Process │                 │
│  4GB   │        │  │(temp)  │  │        │                 │
│  0GB   └────────┘  └────────┘  └────────┘                 │
│        ↑           ↑           ↑                           │
│        Start       GPU Work    End                         │
│                    (Python     (Cleanup)                   │
│                    spawned)                                │
└────────────────────────────────────────────────────────────┘

Advantage: Subprocess pattern has better memory isolation
```

---

## 🔒 Error Handling Strategy

```
Error Handling Flow
┌──────────────────────────────────────────────────────────┐
│  C# Orchestrator                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Try                                               │  │
│  │  {                                                 │  │
│  │    ExecutePythonSubprocess();                      │  │
│  │  }                                                 │  │
│  │  Catch (PythonExecutionException ex)               │  │
│  │  {                                                 │  │
│  │    ┌─────────────────────────────────────────┐    │  │
│  │    │ Retry Strategy                          │    │  │
│  │    │ ├─ Attempt 1: Immediate retry           │    │  │
│  │    │ ├─ Attempt 2: Wait 5s, retry            │    │  │
│  │    │ ├─ Attempt 3: Wait 15s, retry           │    │  │
│  │    │ └─ If all fail: Checkpoint & alert      │    │  │
│  │    └─────────────────────────────────────────┘    │  │
│  │    Log(ex);                                        │  │
│  │    SaveCheckpoint(currentState);                   │  │
│  │    throw new PipelineException("Stage failed", ex);│  │
│  │  }                                                 │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘

Python Subprocess
┌──────────────────────────────────────────────────────────┐
│  try:                                                     │
│      result = generate_image(prompt)                     │
│      print(json.dumps({"success": True, "data": result}))│
│  except Exception as e:                                  │
│      error_response = {                                  │
│          "success": False,                               │
│          "error": str(e),                                │
│          "traceback": traceback.format_exc()             │
│      }                                                   │
│      print(json.dumps(error_response), file=sys.stderr)  │
│      sys.exit(1)  # Non-zero exit code                  │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Architecture

### Development Environment
```
Developer Machine
┌─────────────────────────────────────────────────────┐
│  C# Application (.NET 8)                             │
│  ├─ src/CSharp/                                      │
│  └─ bin/Debug/net8.0/                                │
│                                                       │
│  Python Scripts                                      │
│  ├─ scripts/sdxl_generate.py                         │
│  ├─ scripts/ltx_generate.py                          │
│  └─ scripts/whisper_subprocess.py                    │
│                                                       │
│  Python Environment                                  │
│  └─ venv/                                            │
│     ├─ torch==2.1.0                                  │
│     ├─ diffusers==0.24.0                             │
│     └─ transformers==4.35.0                          │
└─────────────────────────────────────────────────────┘
```

### Production Deployment (Docker)
```
Docker Container
┌─────────────────────────────────────────────────────┐
│  FROM mcr.microsoft.com/dotnet/runtime:8.0           │
│                                                       │
│  # Install Python 3.11                               │
│  RUN apt-get update && apt-get install -y python3.11│
│                                                       │
│  # Copy C# application                               │
│  COPY --from=build /app/publish /app                 │
│                                                       │
│  # Copy Python scripts                               │
│  COPY scripts/ /app/scripts/                         │
│                                                       │
│  # Install Python dependencies                       │
│  RUN pip install -r /app/scripts/requirements.txt    │
│                                                       │
│  # Run C# application                                │
│  ENTRYPOINT ["dotnet", "/app/StoryGenerator.dll"]    │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Component Responsibility Matrix

```
┌────────────────────┬─────────────┬──────────────┬─────────────┐
│ Component          │ Language    │ Reason       │ Integration │
├────────────────────┼─────────────┼──────────────┼─────────────┤
│ Pipeline           │ C#          │ Orchestration│ Native      │
│ Orchestration      │             │ Type safety  │             │
├────────────────────┼─────────────┼──────────────┼─────────────┤
│ Idea Collection    │ C#          │ API calls    │ Native      │
│                    │             │ JSON handling│             │
├────────────────────┼─────────────┼──────────────┼─────────────┤
│ Script Gen         │ C#          │ OpenAI API   │ Native      │
│                    │             │ Simple HTTP  │             │
├────────────────────┼─────────────┼──────────────┼─────────────┤
│ Voice Gen          │ C#          │ ElevenLabs   │ Native      │
│                    │             │ API + FFmpeg │             │
├────────────────────┼─────────────┼──────────────┼─────────────┤
│ ASR (Whisper)      │ C# → Python │ ML inference │ Subprocess  │
│                    │             │ PyTorch req. │             │
├────────────────────┼─────────────┼──────────────┼─────────────┤
│ Keyframe (SDXL)    │ C# → Python │ ML inference │ Subprocess  │
│                    │             │ Diffusers    │             │
├────────────────────┼─────────────┼──────────────┼─────────────┤
│ Video (LTX)        │ C# → Python │ ML inference │ Subprocess  │
│                    │             │ Diffusers    │             │
├────────────────────┼─────────────┼──────────────┼─────────────┤
│ Post-Production    │ C#          │ FFmpeg       │ Native      │
│                    │             │ orchestration│             │
└────────────────────┴─────────────┴──────────────┴─────────────┘
```

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-08  
**Purpose**: Visual supplement to CSHARP_VS_PYTHON_COMPARISON.md
