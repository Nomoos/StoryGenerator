# Obsolete Issues - Python Implementation

This directory contains issue tracking files for the obsolete Python-based implementation of StoryGenerator.

## Overview

These issues represented the original Python implementation plan for the StoryGenerator pipeline. They have been archived here as the project has migrated to C# as the primary implementation.

## Archived Issue Types

### Sequential Step Issues (`step-XX/`)

The sequential step issues (step-00 through step-14) were comprehensive, Python-based implementation plans:

- **step-00-research/** - Research prototypes for Python implementations
- **step-01-ideas/** - Ideas → Topics → Titles generation
- **step-02-viral-score/** - Viral score calculation for titles
- **step-03-raw-script/** - Raw script generation and iteration
- **step-04-improve-script/** - Script improvement using GPT/Local models
- **step-05-improve-title/** - Title improvement using GPT/Local models
- **step-06-scene-planning/** - Scene planning and shot definitions
- **step-07-voiceover/** - Voiceover generation
- **step-08-subtitle-timing/** - Subtitle timing and forced alignment
- **step-09-key-images/** - Key image generation using SDXL
- **step-10-video-generation/** - Video generation from keyframes
- **step-11-post-production/** - Post-production and video assembly
- **step-12-quality-checks/** - Quality control and validation
- **step-13-final-export/** - Final export and platform encoding
- **step-14-distribution-analytics/** - Platform distribution and analytics

Each step includes:
- Python code examples
- Implementation checklists
- Acceptance criteria
- Dependencies and blockers
- Output file specifications

### Python-Specific Atomic Tasks (`atomic/phase-X-prototype/`)

Python-specific atomic research tasks that were part of the Python implementation:

- **phase-1-interface/00-setup-03-python-env/** - Python environment setup
- **phase-2-prototype/01-research-01-ollama-client/** - Python Ollama client
- **phase-2-prototype/01-research-02-whisper-client/** - Python Whisper client
- **phase-2-prototype/01-research-03-ffmpeg-client/** - Python FFmpeg client
- **phase-2-prototype/01-research-04-sdxl-client/** - Python SDXL client
- **phase-2-prototype/01-research-05-ltx-client/** - Python LTX-Video client

## Active Issues

The active C# implementation issues are located in the main `issues/` directory:

```
issues/
├── atomic/                    # C# atomic tasks (phase-based)
├── csharp-master-roadmap/     # C# implementation roadmap
├── csharp-phase3-complete-generators/  # C# Phase 3 tasks
├── csharp-phase4-pipeline-orchestration/  # C# Phase 4 tasks
└── csharp-video-generators/   # C# video generation tasks
```

## Why These Were Archived

1. **Implementation Migration**: The project has fully migrated to C# as the primary implementation
2. **Python Obsolescence**: The Python implementation is no longer maintained
3. **Different Architecture**: C# uses a different architectural approach with atomic, parallelizable tasks
4. **Historical Reference**: These issues are preserved for understanding the original design decisions

## Using These Issues

⚠️ **OBSOLETE - Historic Reference Only**

These issues are maintained solely for historical reference. They should **NOT** be used for:
- New development work
- Planning new features
- Active task tracking

**For active development**, use the issues in the main `issues/` directory which focus on the C# implementation.

## Related Documentation

- [/issues/README.md](../../issues/README.md) - Active C# issue tracking
- [/issues/atomic/README.md](../../issues/atomic/README.md) - Active C# atomic tasks
- [/obsolete/Python/README.md](../Python/README.md) - Obsolete Python implementation
- [/obsolete/docs/PYTHON_OBSOLETE_NOTICE.md](../docs/PYTHON_OBSOLETE_NOTICE.md) - Python obsolescence notice

---

**Last Updated:** 2025-10-08  
**Status:** Archived  
**Reason:** Python implementation obsoleted in favor of C#
