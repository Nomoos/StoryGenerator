# Step 7: Voiceover

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 4 (Final Scripts), Step 2 (Voice Recommendations)

## Overview

Generate voiceovers using local TTS and normalize audio to YouTube standards (-14 LUFS).

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`
- Apply voice recommendations from Step 2
- Generate for all 30 final scripts

## Checklist

### 7.1 Generate Voiceover (Local TTS)
- [ ] Use **voice decision** (F/M) per segment from Step 2
- [ ] Generate voiceover from final script text
- [ ] Configure TTS parameters:
  - Sample rate: 48 kHz
  - Format: WAV (stereo)
  - Quality: Highest available
- [ ] Save WAV to: `/audio/tts/{segment}/{age}/{title_id}.wav`
- [ ] Log generation metadata (voice_id, model, duration)

### 7.2 Normalize to YouTube LUFS
- [ ] Apply `ffmpeg loudnorm` filter to **-14 LUFS** target
- [ ] Use two-pass loudnorm for accuracy
- [ ] Save normalized WAV to: `/audio/normalized/{segment}/{age}/{title_id}_lufs.wav`
- [ ] Log loudnorm parameters JSON alongside file
- [ ] Verify final LUFS measurement

## Audio Specifications

### TTS Output
- **Sample Rate:** 48000 Hz
- **Channels:** Stereo (2)
- **Bit Depth:** 16-bit or 24-bit
- **Format:** WAV (uncompressed)

### Normalization Target
- **Target LUFS:** -14 LUFS (YouTube standard)
- **True Peak:** -1.0 dBTP
- **LRA (Loudness Range):** Maintain natural dynamics

## FFmpeg Loudnorm Command

```bash
# Two-pass loudnorm for accurate -14 LUFS
# Pass 1: Measure
ffmpeg -i input.wav -af loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json -f null -

# Pass 2: Apply (using measured values)
ffmpeg -i input.wav -af loudnorm=I=-14:TP=-1.0:LRA=11:measured_I=-23.0:measured_TP=-5.0:measured_LRA=7.0:measured_thresh=-33.5:offset=-0.5 -ar 48000 output.wav
```

## Metadata JSON

### TTS Metadata (`{title_id}_tts_metadata.json`)
```json
{
  "title_id": "uuid",
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "voice": {
    "gender": "female|male",
    "voice_id": "voice_identifier",
    "engine": "local_tts_engine_name",
    "model": "model_version"
  },
  "audio": {
    "duration_s": 52.3,
    "sample_rate": 48000,
    "channels": 2,
    "bit_depth": 16,
    "format": "wav",
    "file_size_mb": 9.5
  },
  "generated_at": "2024-01-01T12:00:00Z"
}
```

### Loudnorm Metadata (`{title_id}_loudnorm_params.json`)
```json
{
  "input_file": "title_id.wav",
  "output_file": "title_id_lufs.wav",
  "target": {
    "integrated": -14.0,
    "true_peak": -1.0,
    "lra": 11.0
  },
  "measured": {
    "input_i": -23.5,
    "input_tp": -5.2,
    "input_lra": 7.3,
    "input_thresh": -33.8
  },
  "output": {
    "output_i": -14.0,
    "output_tp": -1.0,
    "output_lra": 7.3,
    "output_thresh": -24.5
  },
  "offset": -0.5,
  "normalized_at": "2024-01-01T12:15:00Z"
}
```

## Voice Selection

Use recommendations from Step 2 (`/voices/choice/{segment}/{age}/`):
- **Women segments:** Typically female voice (verify from notes)
- **Men segments:** Typically male voice (verify from notes)
- **Age consideration:** Voice should match age group maturity

## Acceptance Criteria

- [ ] TTS audio files exist for all 30 scripts
- [ ] All TTS files are 48 kHz stereo WAV
- [ ] TTS metadata JSON files exist
- [ ] Normalized audio files exist for all 30 scripts
- [ ] All normalized files meet -14 LUFS target (±0.5 LU tolerance)
- [ ] Loudnorm parameters logged for all files
- [ ] Audio duration matches script length (45-60 seconds)
- [ ] Voice gender matches recommendations from Step 2

## Related Files

- `/audio/tts/{segment}/{age}/` - TTS audio directory
- `/audio/normalized/{segment}/{age}/` - Normalized audio directory
- `/voices/choice/{segment}/{age}/` - Voice recommendation notes
- `/scripts/gpt_improved/{segment}/{age}/` - Final scripts (input)
- `/config/pipeline.yaml` - TTS model configuration

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 10: audio_tts
- Step 11: audio_normalized

Comment `@copilot check` when all audio is generated and normalized.

## Notes

- Total audio files to generate: 30 (5 titles × 6 combinations)
- Verify no clipping or distortion after normalization
- Keep uncompressed WAV for quality in next steps
- Compression to MP3/AAC happens in Step 11 (Post-Production)
