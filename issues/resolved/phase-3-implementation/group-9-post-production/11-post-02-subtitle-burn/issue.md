# Post: Subtitle Burn-in

**ID:** `11-post-02-subtitle-burn`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** ✅ Implementation Complete

## Overview

Burn or soft-code subtitles into video with safe zone positioning, readable styling, and proper timing synchronization from aligned SRT files.

**Implementation:** `Tools.VideoPostProducer.AddSubtitles()` - FFmpeg subtitle overlay with customizable styling.

## Dependencies

**Requires:** `11-post-01` (cropped video), `08-subtitles-01` (SRT files)  
**Blocks:** `11-post-04` (concatenation)

## Status

✅ **Complete:** Full implementation with burn-in and soft-coding

## Features

- SRT/VTT subtitle support
- Safe zone positioning
- Customizable font/style
- Hard-burn or soft-code options

## Next Steps

- `11-post-03-bgm-sfx`

**Documentation:** `/src/CSharp/POST_PRODUCTION_CSHARP.md`
