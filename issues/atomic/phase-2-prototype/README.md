# Phase 2: Prototype & Research

**Purpose:** Build proof-of-concept implementations and validate technical approaches.

**Duration:** 2-3 days  
**Team Size:** 4-8 developers  
**Priority:** P0 - Critical Path

## Overview

This phase creates research prototypes to validate integration patterns with external services and tools. These are minimal, working implementations that prove feasibility before full production code.

## Phase Objectives

- Build working prototypes for all external service integrations
- Validate API patterns and data flows
- Test local model performance (Ollama, Whisper, SDXL, LTX)
- Establish best practices for Python and C# implementations

## Tasks in This Phase

### Python Research (5 tasks)
1. **01-research-01-ollama-client** - Ollama LLM client (Qwen2.5, Llama3.1)
2. **01-research-02-whisper-client** - faster-whisper ASR with word timestamps
3. **01-research-03-ffmpeg-client** - FFmpeg media processing wrapper
4. **01-research-04-sdxl-client** - SDXL image generation (base + refiner)
5. **01-research-05-ltx-client** - LTX-Video generation client

### C# Research (3 tasks)
6. **01-research-06-csharp-ollama** - C# Ollama integration
7. **01-research-07-csharp-whisper** - C# Whisper integration
8. **01-research-08-csharp-ffmpeg** - C# FFmpeg wrapper

## Execution Strategy

**High Parallelization:**
All 8 tasks can run simultaneously with minimal dependencies.

**Recommended Approach:**
```
Day 1-2: Full parallel execution
├── Dev 1: Ollama (Python)
├── Dev 2: Whisper (Python)
├── Dev 3: FFmpeg (Python)
├── Dev 4: SDXL (Python)
├── Dev 5: LTX (Python)
├── Dev 6: C# Ollama
├── Dev 7: C# Whisper
└── Dev 8: C# FFmpeg
```

**Alternative (Smaller Team):**
```
Day 1: Priority research
├── Dev 1-2: Ollama + Whisper
└── Dev 3-4: FFmpeg + SDXL

Day 2: Secondary research
├── Dev 1-2: LTX + C# Ollama
└── Dev 3-4: C# Whisper + C# FFmpeg
```

## Dependencies

**This Phase Requires:**
- Phase 1: Interface (config files, environment setup)

**This Phase Blocks:**
- Phase 3: Implementation (content pipeline needs working integrations)

## Success Criteria

- [ ] All Python prototypes successfully call their respective services
- [ ] All C# prototypes successfully integrate with external tools
- [ ] Performance benchmarks documented for each service
- [ ] API patterns established and documented
- [ ] Known limitations and gotchas documented

## Key Deliverables

Each prototype should include:
- Working code with minimal dependencies
- Example usage/test code
- Performance notes (speed, memory, GPU usage)
- Integration patterns for production use
- Troubleshooting guide

## Research Focus Areas

### Ollama Integration
- Token streaming vs batch
- Context window management
- Prompt engineering best practices

### Whisper ASR
- Word-level timestamp accuracy
- Language detection
- Forced alignment techniques

### FFmpeg
- 9:16 aspect ratio cropping
- LUFS normalization to -14
- Codec selection (H.264 vs H.265)

### SDXL
- Base model + refiner workflow
- LoRA integration
- Prompt engineering for consistency

### LTX-Video
- Keyframe interpolation
- Shot duration limits
- Quality vs speed tradeoffs

## Next Steps

After completing this phase:
1. Move to **Phase 3: Implementation** for production pipeline
2. Use learnings from prototypes to guide implementation decisions
3. Continue parallel execution across 13 implementation groups

## Related Documentation

- `/research/python/` - Python prototype stubs
- `/research/csharp/` - C# prototype stubs
- `/docs/PIPELINE.md` - Pipeline architecture
