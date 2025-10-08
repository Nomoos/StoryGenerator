# Image Generation Group

**Phase:** 3 - Implementation  
**Tasks:** 4  
**Priority:** P1/P2  
**Duration:** 2-3 days  
**Team Size:** 3 developers

## Overview

Generate keyframe images for each video shot using SDXL.

## Tasks

1. **09-images-01-prompt-builder** (P1) - Build SDXL prompts from shots
2. **09-images-02-keyframe-gen-a** (P1) - Generate keyframes batch A
3. **09-images-03-keyframe-gen-b** (P2) - Generate keyframes batch B
4. **09-images-04-selection** (P2) - Select best keyframes

## Dependencies

**Requires:** Scene Planning (shot lists), Phase 2 (SDXL client)  
**Blocks:** Video Production

## Output Files

```
Generator/
├── images/
│   ├── prompts/{gender}/{age}/
│   ├── keyframes_v1/{gender}/{age}/
│   ├── keyframes_v2/{gender}/{age}/
│   └── selected/{gender}/{age}/
```
