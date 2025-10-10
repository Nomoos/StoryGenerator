# Post: Background Music & SFX

**ID:** `11-post-03-bgm-sfx`  
**Priority:** P2  
**Effort:** 2-3 hours  
**Status:** ✅ Implementation Complete

## Overview

Add background music and sound effects to video with audio ducking (automatic volume reduction during voiceover) to maintain voice clarity while enhancing production value.

**Implementation:** `Tools.VideoPostProducer.AddBackgroundMusic()` - FFmpeg audio mixing with ducking.

## Dependencies

**Requires:** `11-post-01` (cropped video), `07-audio-02` (voiceover)  
**Blocks:** `11-post-04` (concatenation)

## Status

✅ **Complete:** Full implementation with ducking support

## Features

- Background music mixing
- Audio ducking during voiceover
- Configurable volume levels
- Multi-track audio support

## Next Steps

- `11-post-04-concatenation`

**Documentation:** `/src/CSharp/POST_PRODUCTION_CSHARP.md`
