# Step 8: Subtitle Timing

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 6 (Draft Subtitles), Step 7 (Audio Voiceovers)

## Overview

Use forced alignment with faster-whisper to time subtitles precisely to the audio voiceovers, then map subtitle timing to scene shots.

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Process all 30 audio files

## Checklist

### 8.1 Time Subtitles to Audio
- [ ] Use **faster-whisper** with `word_timestamps=True`
- [ ] Load draft SRT from Step 6 as reference
- [ ] Perform forced alignment on normalized audio
- [ ] Generate word-level timestamps
- [ ] Group words into subtitle phrases (logical breaks)
- [ ] Produce aligned SRT/VTT files
- [ ] Save to: `/subtitles/timed/{segment}/{age}/{title_id}.srt`

### 8.2 Map Subtitles → Scenes
- [ ] Load shot definitions from Step 6
- [ ] Attach subtitle time ranges to shot IDs
- [ ] Verify subtitle-to-shot mapping
- [ ] Save to: `/scenes/json/{segment}/{age}/{title_id}_subs_to_shots.json`
- [ ] Validate no timing overlaps

## ASR Configuration

### Faster-Whisper Settings
```python
{
  "model_size": "large-v3",
  "device": "cuda",  # or "cpu"
  "compute_type": "float16",  # or "int8" for CPU
  "word_timestamps": True,
  "vad_filter": True,
  "vad_parameters": {
    "threshold": 0.5,
    "min_speech_duration_ms": 250
  }
}
```

### Subtitle Timing Guidelines
- **Min duration:** 1.0 seconds
- **Max duration:** 7.0 seconds
- **Max chars per subtitle:** 42 (readable on mobile)
- **Gap between subtitles:** 0.1 seconds minimum
- **Reading speed:** 17-21 characters per second

## Output Formats

### Timed SRT (`{title_id}.srt`)
```srt
1
00:00:00,123 --> 00:00:03,456
Hook line that grabs attention

2
00:00:03,556 --> 00:00:07,890
Next phrase continuing

3
00:00:08,012 --> 00:00:12,345
Building the narrative further
```

### Subtitles to Shots Mapping (`{title_id}_subs_to_shots.json`)
```json
{
  "title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "total_duration_s": 52.3,
  "mappings": [
    {
      "shot_id": "shot-001",
      "shot_start_s": 0.0,
      "shot_end_s": 6.0,
      "subtitle_ids": [1, 2],
      "subtitle_times": [
        {"id": 1, "start": 0.123, "end": 3.456, "text": "Hook line..."},
        {"id": 2, "start": 3.556, "end": 5.890, "text": "Next phrase..."}
      ]
    },
    {
      "shot_id": "shot-002",
      "shot_start_s": 6.0,
      "shot_end_s": 14.0,
      "subtitle_ids": [3, 4],
      "subtitle_times": [
        {"id": 3, "start": 6.012, "end": 9.345, "text": "Building..."},
        {"id": 4, "start": 9.445, "end": 13.778, "text": "Further..."}
      ]
    }
  ],
  "aligned_at": "2024-01-01T12:00:00Z"
}
```

## Alignment Process

### Step-by-Step
1. **Load audio:** Normalized audio from Step 7
2. **Run ASR:** faster-whisper with word timestamps
3. **Extract words:** Get word-level timing
4. **Group into phrases:** Logical breaks (punctuation, pauses)
5. **Create SRT:** Format with proper timing
6. **Validate:** Check duration, gaps, readability
7. **Map to shots:** Match subtitle times to shot boundaries

### Quality Checks
- [ ] All words from script are captured
- [ ] Timing matches audio precisely (±100ms tolerance)
- [ ] No overlapping subtitles
- [ ] Readable duration for each subtitle
- [ ] Natural phrase breaks
- [ ] Shot boundaries align with subtitle transitions

## Acceptance Criteria

- [ ] Timed SRT files exist for all 30 audio files
- [ ] All subtitles have precise word-level timing
- [ ] Subtitle phrases follow natural speech breaks
- [ ] Subtitle-to-shot mapping JSON files exist for all
- [ ] All mappings validated (no timing conflicts)
- [ ] Subtitle durations are readable (1-7 seconds)
- [ ] Character count per subtitle ≤ 42
- [ ] Shot transitions occur at subtitle boundaries when possible

## Related Files

- `/subtitles/timed/{segment}/{age}/` - Timed subtitles directory
- `/subtitles/srt/{segment}/{age}/` - Draft subtitles (from Step 6)
- `/scenes/json/{segment}/{age}/` - Scene shots and mappings
- `/audio/normalized/{segment}/{age}/` - Normalized audio (input)
- `/research/python/asr_whisper.py` - ASR implementation

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 13: subtitles_timed

Comment `@copilot check` when subtitle timing is complete.

## Notes

- Use faster-whisper large-v3 for best accuracy
- INT8 quantization acceptable for CPU inference
- Total files to process: 30 (5 titles × 6 combinations)
- Keep word-level timestamps for future editing
- Consider voice activity detection (VAD) for cleaner timing
