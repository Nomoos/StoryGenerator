# Input/Output Examples

This document provides comprehensive examples of inputs and outputs at each stage of the StoryGenerator pipeline, including transcripts, shotlists, keyframes, and videos.

## 📋 Table of Contents

- [Pipeline Overview](#pipeline-overview)
- [Stage 1: Story Idea](#stage-1-story-idea)
- [Stage 2: Script Generation](#stage-2-script-generation)
- [Stage 3: Script Revision](#stage-3-script-revision)
- [Stage 4: Voice Generation](#stage-4-voice-generation)
- [Stage 5: Subtitle Generation (ASR)](#stage-5-subtitle-generation-asr)
- [Stage 6: Shotlist Generation (Planned)](#stage-6-shotlist-generation-planned)
- [Stage 7: Keyframe Generation (Planned)](#stage-7-keyframe-generation-planned)
- [Stage 8: Video Synthesis (Planned)](#stage-8-video-synthesis-planned)
- [Complete Example Walkthrough](#complete-example-walkthrough)

---

## Pipeline Overview

```
Story Idea → Script → Revision → Voice → Subtitles → Shotlist → Keyframes → Video
    ↓         ↓         ↓          ↓         ↓           ↓           ↓         ↓
  JSON      TXT       TXT        MP3       SRT       JSON        PNG       MP4
```

---

## Stage 1: Story Idea

### Input: Story Parameters

```python
from Models.StoryIdea import StoryIdea

story = StoryIdea(
    story_title="The Unexpected Friend",
    narrator_gender="female",
    tone="emotional, heartwarming",
    theme="friendship, acceptance",
    narrator_type="first-person",
    other_character="a shy classmate",
    outcome="positive, emotional revelation",
    emotional_core="loneliness, connection, acceptance",
    power_dynamic="equals discovering common ground",
    timeline="one school day",
    twist_type="emotional reveal - shared struggles",
    character_arc="isolation to connection",
    voice_style="conversational, vulnerable, authentic",
    target_moral="we're not as alone as we think",
    locations="school cafeteria, library, hallway",
    mentioned_brands=None,
    goal="Create an emotionally engaging story about unexpected friendship"
)
```

### Output: Story Idea JSON

**File**: `Stories/0_Ideas/The_Unexpected_Friend/idea.json`

```json
{
  "story_title": "The Unexpected Friend",
  "narrator_gender": "female",
  "tone": "emotional, heartwarming",
  "theme": "friendship, acceptance",
  "narrator_type": "first-person",
  "other_character": "a shy classmate",
  "outcome": "positive, emotional revelation",
  "emotional_core": "loneliness, connection, acceptance",
  "power_dynamic": "equals discovering common ground",
  "timeline": "one school day",
  "twist_type": "emotional reveal - shared struggles",
  "character_arc": "isolation to connection",
  "voice_style": "conversational, vulnerable, authentic",
  "target_moral": "we're not as alone as we think",
  "locations": "school cafeteria, library, hallway",
  "mentioned_brands": null,
  "goal": "Create an emotionally engaging story about unexpected friendship",
  "potencial": {
    "overall": 8.5,
    "platforms": {
      "tiktok": 9.0,
      "youtube_shorts": 8.5,
      "instagram_reels": 8.0
    },
    "regions": {
      "us": 9.0,
      "canada": 8.5,
      "australia": 8.0
    },
    "age_groups": {
      "10_13": 7.5,
      "14_17": 9.5,
      "18_24": 8.5,
      "25_30": 7.0
    },
    "gender": {
      "female": 9.0,
      "male": 7.5,
      "non_binary": 8.5
    }
  }
}
```

---

## Stage 2: Script Generation

### Input: Story Idea + Prompt

The script generator uses the story idea JSON and creates a GPT-4o-mini prompt.

**System Prompt** (excerpt):
```
You are a professional TikTok/Instagram Reels scriptwriter...
Write a compelling, emotional story that hooks viewers in the first 3 seconds...
Target length: ~360 words (~60 seconds of speech)
```

**User Prompt**:
```
Write a story with these parameters:
- Title: The Unexpected Friend
- Tone: emotional, heartwarming
- Theme: friendship, acceptance
- Narrator: first-person female
...
```

### Output: Initial Script

**File**: `Stories/1_Scripts/The_Unexpected_Friend/script.txt`

```
I always ate lunch alone. Not because I wanted to, but because that's just how it was. 
Until the day everything changed.

It was a Tuesday, I remember because it was pizza day—my one bright spot in the week. 
I grabbed my tray and headed to my usual corner table in the cafeteria. That's when I 
noticed her. The new girl. She was standing there, looking just as lost as I felt every 
single day.

Our eyes met for just a second, and I could see it—that same loneliness I saw in the 
mirror every morning. Before I could think about it, I nodded toward the empty seat 
across from me. She smiled, a small, grateful smile, and sat down.

We didn't talk much at first. Just the occasional "this pizza sucks" or "do you have 
math next?" kind of stuff. But there was something comforting about not being alone.

The next day, she found me again. And the day after that. We started talking more—about 
teachers we couldn't stand, shows we both watched, that weird smell in the science lab. 
Little things that made the day feel less heavy.

Then one day in the library, while we were supposed to be studying, she said something 
that changed everything. "You know," she started, her voice barely above a whisper, 
"I was really scared to come to this school. I thought no one would talk to me."

My throat tightened. "I'm glad you sat with me," I said. "I was scared too. Every day."

She looked at me, her eyes getting glassy. "Really? But you always seemed so... 
confident. Like you chose to sit alone."

I almost laughed. "I was just trying to look like it didn't bother me."

We sat there for a moment, just looking at each other, and suddenly it all made sense. 
We were both hiding the same pain. Both pretending we were okay with being invisible.

"Well," she said, wiping her eyes and smiling, "I guess we're not alone anymore."

And for the first time in forever, I actually believed that. Because sometimes, the 
person you need is the one who needs you just as much. And that's when I realized—
being lonely doesn't mean you're alone. Sometimes you just haven't found your person yet. 
And when you do, everything changes.
```

**Statistics**:
- Word count: 382 words
- Estimated duration: ~65 seconds
- Emotional hooks: Opening (loneliness), Middle (connection), End (revelation)

---

## Stage 3: Script Revision

### Input: Initial Script

The revision process optimizes the script for AI voice synthesis.

### Output: Revised Script

**File**: `Stories/2_Revised/The_Unexpected_Friend/revised_script.txt`

```
I always ate lunch alone. Not because I wanted to, but because that's just how it was. 
Until the day everything changed.

It was a Tuesday—I remember because it was pizza day, my one bright spot in the week. 
I grabbed my tray and headed to my usual corner table in the cafeteria. That's when I 
noticed her. The new girl. She was standing there, looking just as lost as I felt every 
single day.

Our eyes met for just a second, and I could see it: that same loneliness I saw in the 
mirror every morning. Before I could think about it, I nodded toward the empty seat 
across from me. She smiled—a small, grateful smile—and sat down.

We didn't talk much at first. Just the occasional "this pizza sucks" or "do you have 
math next" kind of stuff. But there was something comforting about not being alone.

The next day, she found me again. And the day after that. We started talking more: about 
teachers we couldn't stand, shows we both watched, that weird smell in the science lab. 
Little things that made the day feel less heavy.

Then one day in the library, while we were supposed to be studying, she said something 
that changed everything. "You know," she started, her voice barely above a whisper, 
"I was really scared to come to this school. I thought no one would talk to me."

My throat tightened. "I'm glad you sat with me," I said. "I was scared too. Every day."

She looked at me, her eyes getting glassy. "Really? But you always seemed so confident. 
Like you chose to sit alone."

I almost laughed. "I was just trying to look like it didn't bother me."

We sat there for a moment, just looking at each other, and suddenly it all made sense. 
We were both hiding the same pain. Both pretending we were okay with being invisible.

"Well," she said, wiping her eyes and smiling, "I guess we're not alone anymore."

And for the first time in forever, I actually believed that. Because sometimes the 
person you need is the one who needs you just as much. And that's when I realized: 
being lonely doesn't mean you're alone. Sometimes you just haven't found your person yet. 
And when you do? Everything changes.
```

**Changes Made**:
- Replaced em-dashes with commas or colons for better TTS pronunciation
- Simplified punctuation for clearer pauses
- Removed ambiguous contractions
- Enhanced sentence flow for natural speech patterns

---

## Stage 4: Voice Generation

### Input: Revised Script + Voice Settings

**Configuration**:
```python
voice_settings = {
    "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel (female, young adult)
    "model_id": "eleven_multilingual_v2",
    "stability": 0.5,
    "similarity_boost": 0.75
}
```

### Output: Audio File

**File**: `Stories/3_VoiceOver/The_Unexpected_Friend/voiceover.mp3`

**Audio Specifications**:
- Format: MP3
- Bitrate: 192 kbps
- Sample Rate: 44.1 kHz
- Channels: Mono
- Duration: 62.8 seconds
- File Size: ~1.5 MB

**Post-Processing Applied**:
1. LUFS normalization to -16.0 dB
2. Silence trimming (threshold: -40 dB)
3. Padding: 0.5s start, 1.0s end

**Audio Characteristics**:
- Emotional tone: Matches script (vulnerable, warm)
- Pacing: Natural conversational speed (~350 words/min)
- Emphasis: Appropriate on key emotional moments
- Clarity: High intelligibility for subtitles

---

## Stage 5: Subtitle Generation (ASR)

### Input: Audio File + Revised Script

WhisperX processes the audio and aligns it with the script.

### Output: Word-Level SRT File

**File**: `Stories/4_Titles/The_Unexpected_Friend/subtitles.srt`

```srt
1
00:00:00,500 --> 00:00:01,200
I

2
00:00:01,200 --> 00:00:01,600
always

3
00:00:01,600 --> 00:00:01,800
ate

4
00:00:01,800 --> 00:00:02,100
lunch

5
00:00:02,100 --> 00:00:02,500
alone.

6
00:00:02,800 --> 00:00:03,000
Not

7
00:00:03,000 --> 00:00:03,300
because

8
00:00:03,300 --> 00:00:03,400
I

9
00:00:03,400 --> 00:00:03,700
wanted

10
00:00:03,700 --> 00:00:03,900
to,

...

178
00:01:01,500 --> 00:01:01,900
Everything

179
00:01:01,900 --> 00:01:02,400
changes.
```

**Statistics**:
- Total words: 179
- Average word duration: ~350ms
- Alignment accuracy: 98.5%
- Timing precision: ±50ms

**Metadata File**: `Stories/4_Titles/The_Unexpected_Friend/metadata.json`

```json
{
  "story_title": "The Unexpected Friend",
  "audio_duration": 62.8,
  "word_count": 179,
  "alignment_quality": 0.985,
  "model_used": "whisperx-large-v2",
  "language": "en",
  "generated_at": "2024-10-06T10:30:45Z"
}
```

---

## Stage 6: Shotlist Generation (Planned)

### Input: Script + Story Idea

A specialized LLM (Qwen2.5 or Llama-3.1) will analyze the script and create a shotlist.

### Output: Shotlist JSON (Example)

**File**: `Stories/5_Shotlist/The_Unexpected_Friend/shotlist.json`

```json
{
  "story_title": "The_Unexpected_Friend",
  "total_duration": 62.8,
  "shots": [
    {
      "shot_number": 1,
      "start_time": 0.0,
      "end_time": 8.5,
      "duration": 8.5,
      "scene_description": "School cafeteria, wide shot, protagonist sitting alone at corner table",
      "visual_prompt": "A teenage girl sitting alone at a cafeteria corner table, looking down at her tray, soft natural lighting from windows, other students in blurred background, emotional atmosphere",
      "mood": "lonely, isolated",
      "camera_angle": "medium wide shot",
      "lighting": "soft natural light",
      "color_palette": "muted blues and grays",
      "key_elements": ["cafeteria", "lone figure", "empty chairs", "distant crowd"]
    },
    {
      "shot_number": 2,
      "start_time": 8.5,
      "end_time": 18.2,
      "duration": 9.7,
      "scene_description": "New girl standing with tray, looking uncertain, protagonist's POV",
      "visual_prompt": "A shy new girl standing in cafeteria with lunch tray, looking lost and anxious, soft focus background, teenage school setting, warm undertones beginning to emerge",
      "mood": "uncertain, hopeful",
      "camera_angle": "medium shot, eye level",
      "lighting": "soft warm light",
      "color_palette": "transitioning from cool to warm tones",
      "key_elements": ["new student", "lunch tray", "uncertain expression", "eye contact moment"]
    },
    {
      "shot_number": 3,
      "start_time": 18.2,
      "end_time": 28.5,
      "duration": 10.3,
      "scene_description": "Two girls sitting across from each other, starting to talk",
      "visual_prompt": "Two teenage girls sitting across from each other at cafeteria table, beginning to smile and talk, pizza on trays, warm lighting, connection forming",
      "mood": "warming, tentative friendship",
      "camera_angle": "over-shoulder shot alternating between characters",
      "lighting": "warm natural light",
      "color_palette": "warm yellows and oranges",
      "key_elements": ["two figures", "shared table", "food", "emerging smiles"]
    },
    {
      "shot_number": 4,
      "start_time": 28.5,
      "end_time": 42.1,
      "duration": 13.6,
      "scene_description": "Library scene, intimate conversation, emotional reveal",
      "visual_prompt": "School library, two friends sitting close together at study table, books around them, soft lamp light, emotional conversation, tears in eyes, warm intimate atmosphere",
      "mood": "emotional, intimate, vulnerable",
      "camera_angle": "close-up, focus on faces",
      "lighting": "soft warm lamp light",
      "color_palette": "warm browns and soft golds",
      "key_elements": ["library", "books", "intimate space", "emotional expressions", "vulnerability"]
    },
    {
      "shot_number": 5,
      "start_time": 42.1,
      "end_time": 62.8,
      "duration": 20.7,
      "scene_description": "Realization moment, friends together, hopeful ending",
      "visual_prompt": "Two teenage friends sitting together, genuine smiles, connection visible, warm golden hour lighting, school hallway or cafeteria background softly blurred, uplifting atmosphere, friendship realized",
      "mood": "hopeful, warm, connected",
      "camera_angle": "medium shot, both characters in frame",
      "lighting": "golden hour warm light",
      "color_palette": "warm golds and soft pinks",
      "key_elements": ["two friends", "genuine smiles", "togetherness", "bright future feeling"]
    }
  ],
  "visual_themes": [
    "isolation to connection",
    "cool to warm color transition",
    "expanding frame as friendship develops"
  ],
  "transition_notes": "Gradual color temperature shift from cool (lonely) to warm (connected)"
}
```

**Shotlist Statistics**:
- Total shots: 5
- Average shot duration: 12.6 seconds
- Visual theme: Isolation → Connection
- Color progression: Cool → Warm tones

---

## Stage 7: Keyframe Generation (Planned)

### Input: Shotlist JSON

SDXL generates keyframes based on visual prompts from the shotlist.

### Output: Keyframe Images (Example)

**Shot 1 Keyframe**: `Stories/6_Keyframes/The_Unexpected_Friend/shot_001.png`

**SDXL Prompt**:
```
Positive: A teenage girl sitting alone at a cafeteria corner table, looking down at her 
tray, soft natural lighting from windows, other students in blurred background, emotional 
atmosphere, cinematic lighting, high quality, realistic, detailed

Negative: text, watermark, low quality, blurry, distorted, ugly, deformed, multiple 
people in focus, bright harsh lighting
```

**Image Specifications**:
- Resolution: 1024x1024 (will be cropped to 1080x1920 for vertical video)
- Format: PNG
- Quality: High (SDXL base + refiner)
- Style: Photorealistic, cinematic
- File Size: ~2-3 MB per image

**Generation Settings**:
```python
{
    "num_inference_steps": 30,
    "guidance_scale": 7.5,
    "num_images": 1,
    "seed": 42  # For reproducibility
}
```

**Additional Keyframes**:
- `shot_002.png` - New girl with tray
- `shot_003.png` - Girls talking at table
- `shot_004.png` - Library emotional moment
- `shot_005.png` - Friends together, happy ending

**Keyframe Metadata**: `Stories/6_Keyframes/The_Unexpected_Friend/metadata.json`

```json
{
  "story_title": "The_Unexpected_Friend",
  "total_keyframes": 5,
  "model_used": "stable-diffusion-xl-base-1.0",
  "resolution": "1024x1024",
  "keyframes": [
    {
      "filename": "shot_001.png",
      "shot_number": 1,
      "prompt": "A teenage girl sitting alone...",
      "negative_prompt": "text, watermark...",
      "seed": 42,
      "generation_time": 3.2,
      "quality_score": 0.92
    }
  ],
  "generated_at": "2024-10-06T11:15:30Z"
}
```

---

## Stage 8: Video Synthesis (Planned)

### Input: Keyframes + Shotlist + Audio

LTX-Video or SVD interpolates between keyframes to create smooth video.

### Output: Final Video

**File**: `Stories/7_Video/The_Unexpected_Friend/final_video.mp4`

**Video Specifications**:
- Resolution: 1080x1920 (vertical, 9:16 aspect ratio)
- Frame Rate: 30 fps
- Duration: 62.8 seconds
- Video Codec: H.264
- Audio Codec: AAC
- Bitrate: 8 Mbps (video) + 192 kbps (audio)
- File Size: ~65 MB

**Composition**:
1. **Video Layers**:
   - Background: Generated/interpolated video from keyframes
   - Subtitle overlay: Word-by-word from SRT file
   - Optional: Background music (low volume)

2. **Subtitle Styling**:
   - Font: Montserrat Bold
   - Size: 72pt
   - Color: White with black stroke
   - Position: Center, slightly below middle
   - Animation: Fade in per word, highlight current word

3. **Transitions**:
   - Shot transitions: 0.5s cross-fade
   - Subtitle transitions: 0.1s fade in/out per word
   - Audio: Continuous, no cuts

**Video Metadata**: Embedded in MP4

```json
{
  "title": "The Unexpected Friend",
  "description": "An emotional story about unexpected friendship and finding connection",
  "artist": "Nom",
  "album": "Noms Stories",
  "genre": "Short Story",
  "duration": 62.8,
  "aspect_ratio": "9:16",
  "tags": ["friendship", "emotional", "school", "connection", "heartwarming"]
}
```

**Thumbnail**: `Stories/7_Video/The_Unexpected_Friend/thumbnail.jpg`

- Resolution: 1080x1920
- Extracted from: 10-second mark (emotional peak)
- Format: JPEG
- Quality: 90%
- File Size: ~300 KB

---

## Complete Example Walkthrough

### Story: "The Secret Note"

#### 1. Story Idea
```json
{
  "story_title": "The Secret Note",
  "narrator_gender": "female",
  "tone": "mysterious, romantic",
  "theme": "romance, secrets, revelation",
  "emotional_core": "curiosity, anticipation, surprise",
  "twist_type": "identity reveal"
}
```

#### 2. Script (Excerpt)
```
I found the note in my locker on a Monday morning. No name, just three words: 
"I see you." At first, I thought it was creepy. But then Tuesday came, and there 
was another one...
```

#### 3. Voice Generated
- Duration: 58.3 seconds
- Voice: Rachel (warm, mysterious tone)
- File: `voiceover.mp3`

#### 4. Subtitles
```srt
1
00:00:00,500 --> 00:00:00,600
I

2
00:00:00,600 --> 00:00:00,900
found

3
00:00:00,900 --> 00:00:01,000
the

4
00:00:01,000 --> 00:00:01,200
note
...
```

#### 5. Shotlist (Excerpt)
```json
{
  "shots": [
    {
      "shot_number": 1,
      "scene_description": "Close-up of mysterious note in locker",
      "visual_prompt": "Hand holding a folded note, school locker in background..."
    }
  ]
}
```

#### 6. Keyframes
- `shot_001.png` - Note in locker
- `shot_002.png` - Girl reading note
- `shot_003.png` - Searching hallways
- `shot_004.png` - The reveal moment

#### 7. Final Video
- Resolution: 1080x1920
- Duration: 58.3s
- With subtitles and transitions
- File: `final_video.mp4`

---

## Example File Structure

Complete file structure for "The Unexpected Friend" story:

```
Stories/
└── The_Unexpected_Friend/
    ├── 0_Ideas/
    │   └── idea.json
    ├── 1_Scripts/
    │   └── script.txt
    ├── 2_Revised/
    │   └── revised_script.txt
    ├── 3_VoiceOver/
    │   ├── voiceover.mp3
    │   └── metadata.json
    ├── 4_Titles/
    │   ├── subtitles.srt
    │   └── metadata.json
    ├── 5_Shotlist/           # Planned
    │   └── shotlist.json
    ├── 6_Keyframes/          # Planned
    │   ├── shot_001.png
    │   ├── shot_002.png
    │   ├── shot_003.png
    │   ├── shot_004.png
    │   ├── shot_005.png
    │   └── metadata.json
    └── 7_Video/              # Planned
        ├── final_video.mp4
        ├── thumbnail.jpg
        └── metadata.json
```

---

## Testing Examples

### Test Data for Development

The `examples/` directory contains runnable Python scripts:

1. **`basic_pipeline.py`**
   - Demonstrates complete pipeline (currently implemented stages)
   - Creates example story "The Unexpected Friend"
   - Runs through: Idea → Script → Revision → Voice → Subtitles

2. **`batch_processing.py`**
   - Processes multiple stories in batch
   - Examples: "The Secret Note", "The Last Text", "Wrong Number"
   - Handles errors gracefully

3. **`custom_story_ideas.py`**
   - Shows how to create custom story parameters
   - Various themes and tones
   - Different narrator types and outcomes

### Running Examples

```bash
# Basic pipeline
cd /home/runner/work/StoryGenerator/StoryGenerator
python examples/basic_pipeline.py

# Batch processing
python examples/batch_processing.py

# Custom ideas
python examples/custom_story_ideas.py
```

---

## Quality Metrics

### Expected Output Quality

| Stage | Metric | Target | Actual |
|-------|--------|--------|--------|
| Script | Word count | 350-380 words | 360-382 words ✅ |
| Script | Duration estimate | 58-65 seconds | 60-65 seconds ✅ |
| Voice | Audio quality | 192 kbps MP3 | 192 kbps ✅ |
| Voice | LUFS level | -16.0 dB | -16.0 ±0.5 dB ✅ |
| ASR | Word alignment | >95% accuracy | 98.5% ✅ |
| ASR | Timing precision | ±100ms | ±50ms ✅ |

### Future Stage Targets

| Stage | Metric | Target |
|-------|--------|--------|
| Shotlist | Shot count | 4-6 shots per story |
| Shotlist | Avg shot duration | 10-15 seconds |
| Keyframes | Resolution | 1024x1024 (SDXL) |
| Keyframes | Quality score | >0.85 |
| Video | Resolution | 1080x1920 |
| Video | Frame rate | 30 fps |
| Video | File size | <100 MB for 60s |

---

## Troubleshooting Common Issues

### Issue: Script too long

**Problem**: Generated script exceeds 65 seconds
**Solution**: 
- Adjust max_tokens in GPT call
- Post-process to trim to 380 words max
- Use more concise system prompt

### Issue: Poor subtitle alignment

**Problem**: Subtitles not matching audio
**Solution**:
- Check audio quality (no background noise)
- Verify script revision removed problematic punctuation
- Use latest WhisperX model (large-v2 or upgrade to faster-whisper large-v3)

### Issue: Keyframe generation fails (Future)

**Problem**: SDXL generates low-quality or incorrect images
**Solution**:
- Improve shotlist visual prompts with more detail
- Add negative prompts to avoid common issues
- Use SDXL refiner for higher quality
- Increase inference steps (30 → 50)

---

## Additional Resources

- See [MODELS.md](MODELS.md) for model documentation
- See [PIPELINE.md](../PIPELINE.md) for technical details
- See [examples/](../examples/) for runnable code
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

---

**Last Updated**: 2024-10-06
