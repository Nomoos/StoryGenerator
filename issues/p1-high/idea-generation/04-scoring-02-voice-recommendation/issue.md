# Scoring: Voice Recommendation

**ID:** `04-scoring-02-voice-recommendation`  
**Priority:** P1  
**Effort:** 2-3 hours  
**Status:** ✅ Complete

## Overview

Recommends voice characteristics (gender, style, pitch, speed, emotion) for each title based on content analysis and target audience.

## Dependencies

**Requires:**
- `04-scoring-01` - Title scoring

**Blocks:**
- `04-scoring-03` - Top selection (optional)

## Acceptance Criteria

- [x] VoiceRecommender class implemented
- [x] Voice characteristics recommended
- [x] 18 unit tests passing
- [x] Code reviewed and merged

## Implementation

**Module:** `core/pipeline/voice_recommendation.py`
**Class:** `VoiceRecommender`

```python
from core.pipeline.voice_recommendation import VoiceRecommender

recommender = VoiceRecommender()
titles_with_voices = recommender.recommend_all_voices(scored_titles)
recommender.save_recommendations(titles_with_voices, output_dir)
```

**Recommendation Factors:**
- **Gender**: Matches target audience with content analysis
- **Style**: dramatic, inspirational, humorous, intimate, conversational
- **Pitch**: low, medium, high based on content tone
- **Speed**: slow, medium, fast based on urgency
- **Emotion**: excited, concerned, empathetic, curious, confident

## Output Files

**File:** `data/voices/choice/{gender}/{age_bucket}/titles_with_voices.json`

```json
{
  "titles_by_topic": {
    "topic_01": [
      {
        "id": "topic_01_title_01",
        "text": "Why this shocking discovery changed everything",
        "score": 85.5,
        "voice_recommendation": {
          "gender": "female",
          "style": "dramatic",
          "pitch": "medium-low",
          "speed": "medium",
          "emotion": "excited"
        }
      }
    ]
  }
}
```

## Next Steps

- `04-scoring-03` - Select top 5 titles per segment
