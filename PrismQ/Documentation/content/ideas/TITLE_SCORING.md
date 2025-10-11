# Title Scoring System

Automated viral potential scoring for video titles using configurable rubric.

## Overview

The title scoring system evaluates video titles for viral potential using a comprehensive rubric defined in `config/scoring.yaml`. For each audience segment (gender/age), it:

1. **Scores titles** (0-100) based on multiple criteria
2. **Provides rationale** for each score
3. **Recommends voice gender** (F/M) for narration
4. **Selects top 5 titles** per segment
5. **Generates reports** in JSON and Markdown formats

## Files

- **`title_score.py`** - Main scoring script
- **`config/scoring.yaml`** - Scoring rubric configuration
- **`test_title_score.py`** - Test suite

## Usage

### Score All Segments

Process all audience segments defined in `config/audience_config.json`:

```bash
python title_score.py
```

### Score Specific Segment

Process a single gender/age segment:

```bash
python title_score.py women 18-23
python title_score.py men 25-29
```

## Input

The script looks for title files in:

```
Generator/titles/{gender}/{age}/
```

Supported formats:
- **JSON files** with `title`, `story_title`, or `video_title` keys
- **Text files** with title as first line
- **Subdirectories** with `idea.json` files

## Output

### Scores (JSON)

```
Generator/scores/{gender}/{age}/YYYYMMDD_title_scores.json
```

Example structure:
```json
{
  "metadata": {
    "generated_at": "2025-10-06T19:53:25",
    "segment": {
      "gender": "women",
      "age": "18-23"
    },
    "total_titles": 5
  },
  "scores": [
    {
      "title": "5 Secrets You Need to Know",
      "source_file": "title1.json",
      "target_audience": {
        "gender": "women",
        "age": "18-23"
      },
      "scores": {
        "hook_strength": 75,
        "clarity": 80,
        "relevance": 85,
        "length_format": 95,
        "viral_potential": 70
      },
      "overall_score": 79.5,
      "rationale": "Strong hook with curiosity-inducing elements...",
      "voice_recommendation": {
        "gender": "F",
        "reasoning": "Female voice matches target audience..."
      }
    }
  ]
}
```

### Voice Notes (Markdown)

```
Generator/voices/choice/{gender}/{age}/YYYYMMDD_voice_notes.md
```

Contains top 5 titles with:
- Overall score
- Voice recommendation and reasoning
- Detailed scores for all criteria
- Rationale

## Scoring Criteria

The system evaluates titles on 5 criteria (defined in `config/scoring.yaml`):

1. **Hook Strength (30%)** - Curiosity, emotional appeal, urgency
2. **Clarity (20%)** - Easy to understand, no ambiguity
3. **Relevance (20%)** - Alignment with target audience and trends
4. **Length & Format (15%)** - Optimal length for social media (40-60 chars)
5. **Viral Potential (15%)** - Shareability, controversy, surprise elements

### Score Ranges

- **90-100**: Excellent - High viral potential
- **70-89**: Good - Strong performance expected
- **50-69**: Average - May need improvement
- **0-49**: Poor - Consider regenerating

## Voice Recommendation

The system recommends narrator voice gender (M/F) based on:

- **Content type**: Mystery/thriller → deeper voice (often M)
- **Target audience**: Matches demographic preferences
- **Genre conventions**: Beauty/wellness often F, tech/gaming often M
- **Emotional tone**: Authority vs. relatability

## Configuration

### Scoring Rubric

Edit `config/scoring.yaml` to customize:

- Scoring criteria and weights
- Score thresholds
- Voice recommendation guidelines
- Top title selection count

### Audience Segments

Defined in `config/audience_config.json`:

```json
{
  "audience": {
    "genders": [
      {"name": "men", "preference_percentage": 50},
      {"name": "women", "preference_percentage": 50}
    ],
    "age_groups": [
      {"range": "18-23", "preference_percentage": 20},
      {"range": "25-29", "preference_percentage": 20}
    ]
  }
}
```

## Testing

Run the test suite:

```bash
python test_title_score.py
```

Tests cover:
- Module imports
- Configuration loading
- Title scoring logic
- Voice recommendations
- File extraction
- End-to-end workflow

## Integration

The title scoring system integrates with the content pipeline:

```
Pipeline Stage 4: Titles
    ↓
[title_score.py]
    ↓
Pipeline Stage 5: Scores → JSON results
Pipeline Stage 9: Voice Choice → Markdown notes
```

Use with quality control:

```bash
# Score titles
python title_score.py

# Process quality thresholds
python process_quality.py
```

## Examples

### High-Scoring Title Examples

- "5 Secrets Nobody Tells You About Success" (85/100)
- "Why Everyone Is Talking About This" (82/100)
- "How I Changed My Life in 30 Days" (78/100)

### Common Issues

**Low hook strength**: Generic titles without curiosity elements
- ❌ "My Day at the Park"
- ✅ "What I Found at the Park Changed Everything"

**Poor length**: Too short or too long for social media
- ❌ "Tech" (too short)
- ❌ "This is an extremely long title that goes on and on..." (too long)
- ✅ "5 Tech Hacks That Will Change Your Life"

**Low relevance**: Doesn't match target audience
- ❌ "Retirement Planning Tips" for age 18-23
- ✅ "College Life Hacks Every Student Needs"

## Troubleshooting

### No titles found

Check that title files exist in correct location:
```
Generator/titles/{gender}/{age}/
```

### Low scores across all titles

Review scoring criteria in `config/scoring.yaml` and adjust weights if needed.

### Missing dependencies

```bash
pip install -r requirements.txt
```

## Future Enhancements

Potential improvements:

1. **LLM Integration**: Use GPT-4 or Claude for more nuanced scoring
2. **A/B Testing**: Track actual performance vs. predicted scores
3. **Trend Analysis**: Incorporate current viral trends
4. **Multi-language**: Support for non-English titles
5. **Historical Learning**: Improve scoring based on past performance

## License

Part of the StoryGenerator project.
