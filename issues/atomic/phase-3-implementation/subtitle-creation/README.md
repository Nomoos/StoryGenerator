# Subtitle Creation Group

**Phase:** 3 - Implementation  
**Tasks:** 2  
**Priority:** P1  
**Duration:** 1 day  
**Team Size:** 1-2 developers

## Overview

Create precisely timed subtitles using forced alignment and map them to scenes.

## Tasks

1. **08-subtitles-01-forced-alignment** (P1) - Time subtitles to audio with Whisper
2. **08-subtitles-02-scene-mapping** (P1) - Map subtitle timings to shots

## Dependencies

**Requires:** Audio Production (normalized audio), Scene Planning (draft subtitles)  
**Blocks:** Post-Production

## Output Files

```
Generator/
├── subtitles/
│   ├── timed/{gender}/{age}/*.srt
│   └── mapped/{gender}/{age}/scene_subs.json
```
