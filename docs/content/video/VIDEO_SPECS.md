# Video Specifications & Platform Constraints

This document defines the video specifications and constraints for generating vertical short-form videos optimized for Instagram Reels, TikTok, and YouTube Shorts (as of 2025).

## Platform Specifications

### Video Format
- **Aspect Ratio**: 9:16 (vertical)
- **Resolution**: 1080×1920 pixels
- **Orientation**: Portrait/Vertical

### Platform-Specific Details

#### Instagram Reels
- **Recommended Size**: 1080×1920 (9:16 aspect ratio)
- **Max Duration**: 3 minutes (expanded in early 2025)
- **Reference**: [Instagram Help Center - Reel size & aspect ratios](https://help.instagram.com/1038071743007909)

#### TikTok
- **Recommended Format**: Vertical video (9:16 aspect ratio)
- **Max Duration**: ~3 minutes
- **Supported Formats**: MP4, MOV

#### YouTube Shorts
- **Default Orientation**: Vertical (9:16)
- **Max Duration**: 3 minutes (expanded from 60 seconds)
- **Reference**: [YouTube Support - Shorts upload requirements](https://support.google.com/youtube/answer/10059070)

## Video Encoding Settings

### Codec
- **Primary Codec**: H.264 (libx264)
- **Alternative**: H.265 (if platform supports)
- **Reference**: [FFmpeg H.264 Encoding Guide](https://trac.ffmpeg.org/wiki/Encode/H.264)

### Bitrate & Quality
- **Target Bitrate**: 5-10 Mbps for 1080×1920 vertical video
- **Encoding**: Two-pass encoding recommended for optimal quality
- **Pixel Format**: yuv420p (ensures broad compatibility across platforms)

### Frame Rate
- **Standard**: 30 fps (frames per second)
- **Alternative**: 60 fps (supported by some apps, but not required)

### Current Implementation
The `convert_to_mp4()` function in `Tools/Utils.py` currently uses:
- Codec: libx264
- Pixel format: yuv420p
- Frame rate: 30 fps
- Audio codec: AAC at 192k

## Audio Specifications

### Audio Settings
- **Sample Rate**: 48 kHz (recommended)
- **Current**: 44.1 kHz (mp3_44100_192)
- **Channels**: Stereo
- **Loudness Normalization**: -14 LUFS (platform standard)

### Current Implementation
The `VoiceMaker` class in `Generators/GVoice.py` implements:
- LUFS normalization at -14.0 LUFS (see `normalize_lufs()` method)
- Sample rate: 44.1 kHz
- Format: MP3 at 192 kbps

## Safe Zones & UI Overlays

### Recommended Margins
To avoid overlap with platform UI elements (titles, captions, controls):
- **Top**: Avoid critical content in top ~5-10% (avoid notch overlap)
- **Bottom**: Avoid critical content in bottom ~10-15% (controls, captions)
- **Sides**: Keep 5% margin on left/right for safe viewing

### Best Practices
- Place key visual elements in the center 70% of the screen
- Position text and captions considering platform-specific UI
- Test on actual devices to verify safe zones

## Subtitles & Captions

### Tools in Use
- **WhisperX**: Used for word-level transcription and alignment
  - Model: large-v2
  - Generates word-by-word subtitles with timestamps
  - Implementation in `Generators/GTitles.py`

### Subtitle Formats
- **SRT Export**: Word-level subtitles exported to SRT format
- **Hard-coded**: On-screen text burned into video
- **Time-aligned**: Using forced alignment for precise timing

### Alternative Tools (for consideration)
- **Gentle**: Forced aligner for text-to-audio alignment
- **Montreal Forced Aligner (MFA)**: Version 3.0+ for high-quality alignment
- **Whisper**: OpenAI's speech recognition model (already integrated via WhisperX)

## Additional Video Generation Tools

### Emerging Technologies
- **LTX-Video**: Emerging model for video generation
  - Supports 30 fps video generation
  - Note: Native resolution is not vertical (requires adaptation)

### Video Editing Libraries
- **MoviePy**: Python library for video editing
  - Version: 2.2.0 (as of May 2025, available on PyPI)
  - Maintained and actively developed

## Action Items & Verification

### Official Documentation to Review
1. **Instagram**: [Reels specifications and upload requirements](https://help.instagram.com/)
2. **TikTok**: [Video upload specifications](https://support.tiktok.com/)
3. **YouTube**: [Shorts upload requirements](https://support.google.com/youtube/)

### Recommended Updates
1. ✅ Update video resolution to 1080×1920 in `convert_to_mp4()`
2. ✅ Increase bitrate to 5-10 Mbps for better quality
3. ✅ Verify LUFS normalization at -14.0 (already implemented)
4. Consider upgrading audio sample rate to 48 kHz
5. Consider implementing two-pass encoding for quality

### Testing Checklist
- [ ] Test video playback on Instagram Reels
- [ ] Test video playback on TikTok
- [ ] Test video playback on YouTube Shorts
- [ ] Verify safe zones on actual devices
- [ ] Confirm duration limits (up to 3 minutes)
- [ ] Validate audio loudness levels

## Technical References

### FFmpeg Commands
Example command for vertical video encoding:
```bash
ffmpeg -i input.mp3 -i background.jpg \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -preset slow -crf 18 \
  -b:v 8M -maxrate 10M -bufsize 10M \
  -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -ar 48000 \
  -shortest output.mp4
```

### Key Parameters
- `-vf scale=1080:1920`: Sets vertical resolution
- `-b:v 8M`: Sets video bitrate to 8 Mbps
- `-maxrate 10M`: Maximum bitrate cap
- `-pix_fmt yuv420p`: Compatibility pixel format
- `-r 30`: Frame rate at 30 fps
- `-ar 48000`: Audio sample rate at 48 kHz

## Version History
- **2025-10**: Initial documentation based on latest platform specs
- Platforms have expanded Reels/Shorts duration to 3 minutes
- LUFS normalization implemented at -14.0
- WhisperX integrated for subtitle generation
