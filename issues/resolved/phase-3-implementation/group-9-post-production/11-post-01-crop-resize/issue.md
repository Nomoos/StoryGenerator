# Post: Crop to 9:16

**ID:** `11-post-01-crop-resize`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** ✅ Implementation Complete

## Overview

Crop and resize video clips to 9:16 vertical aspect ratio optimized for mobile platforms (TikTok, Instagram Reels, YouTube Shorts). Includes intelligent cropping with face detection and safe zone management.

**Implementation:** `Tools.VideoPostProducer.CropAndResize()` - FFmpeg-based cropping with configurable safe zones.

## Dependencies

**Requires:** `10-video-03` (selected video clips)  
**Blocks:** `11-post-02` (subtitle burn-in)

## Status

✅ **Complete:** Full implementation with intelligent cropping

## Features

- 9:16 aspect ratio (1080x1920)
- Face detection for optimal framing
- Configurable safe zones
- Maintains video quality

## Next Steps

- `11-post-02-subtitle-burn`

**Documentation:** `/src/CSharp/POST_PRODUCTION_CSHARP.md`
