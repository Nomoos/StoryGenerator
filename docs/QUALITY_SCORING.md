# Content Quality Scoring System

## Overview

The Content Quality Scoring System assesses the viral potential and quality of generated content (ideas, topics, titles, scripts) using a multi-dimensional scoring algorithm. Content is scored from 0-100 based on five key metrics weighted according to viral potential.

## Scoring Metrics

### 1. Novelty (25% weight)
**Purpose**: Measures uniqueness, surprise, and curiosity-inducing elements.

**Evaluation Factors**:
- Presence of novelty keywords: "secret", "hidden", "revealed", "shocking", "amazing", "unexpected", "surprising", "mystery", "discovery"
- Question format (creates curiosity)
- Content length and detail level
- Unique themes and keywords

**Score Range**: 0-100
- 80-100: Highly novel and surprising content
- 60-79: Good novelty with some unique elements
- 40-59: Average novelty
- 0-39: Generic or too simple

### 2. Emotional Impact (25% weight)
**Purpose**: Measures emotional resonance and ability to connect with audience.

**Evaluation Factors**:
- Positive emotion triggers: "love", "joy", "amazing", "inspiring", "incredible"
- Negative emotion triggers: "fear", "danger", "loss", "shocking", "heartbreaking"
- Curiosity triggers: "mystery", "secret", "truth", "revelation", "discover"
- Personal/relatable elements: "you", "your", "my", "everyone"
- Genre/category emotional content

**Score Range**: 0-100
- 80-100: Strong emotional impact across multiple dimensions
- 60-79: Good emotional resonance
- 40-59: Moderate emotional content
- 0-39: Lacks emotional connection

### 3. Clarity (20% weight)
**Purpose**: Assesses how clear, understandable, and well-structured the content is.

**Evaluation Factors**:
- Presence of required fields (title, synopsis, description, etc.)
- Content length appropriateness (not too short or verbose)
- Language complexity (simpler is clearer)
- Structure indicators: colons, bullets, numbering, connectors
- Title length constraints (20-100 characters optimal)

**Score Range**: 0-100
- 80-100: Crystal clear, well-structured
- 60-79: Clear with good structure
- 40-59: Somewhat clear but could improve
- 0-39: Unclear or poorly structured

### 4. Replay Value (15% weight)
**Purpose**: Measures rewatchability, depth, and lasting interest.

**Evaluation Factors**:
- Content depth and complexity indicators
- Multiple themes or keywords (indicates layers)
- Mystery/suspense elements: "mystery", "secret", "twist", "puzzle"
- Educational value: "learn", "discover", "explained", "how", "why"
- Narrative complexity: "because", "however", "therefore"

**Score Range**: 0-100
- 80-100: High replay value with depth
- 60-79: Good replay value
- 40-59: Moderate replay value
- 0-39: Low replay value

### 5. Shareability (15% weight)
**Purpose**: Measures viral potential and likelihood of being shared.

**Evaluation Factors**:
- Shareable hook words: "truth", "revealed", "exposed", "secret", "shocking"
- Question format (highly shareable)
- Universal/relatable topics: "everyone", "people", "life", "world"
- Controversial elements: "truth", "lie", "fake", "real", "expose"
- Numbers and lists (clickbait elements)

**Score Range**: 0-100
- 80-100: Extremely shareable/viral potential
- 60-79: Good shareability
- 40-59: Moderate shareability
- 0-39: Low viral potential

## Weighted Scoring Formula

```python
final_score = (
    novelty_score * 0.25 +
    emotional_score * 0.25 +
    clarity_score * 0.20 +
    replay_score * 0.15 +
    share_score * 0.15
)
```

The weights are configurable in `config/scoring.yaml`:

```yaml
viral:
  novelty: 0.25
  emotional: 0.25
  clarity: 0.20
  replay: 0.15
  share: 0.15
```

## Quality Thresholds

Content is categorized based on final score:

| Category | Score Range | Action |
|----------|-------------|--------|
| Excellent | 85-100 | Keep as-is, ready for production |
| Good | 70-84 | Keep as-is, acceptable quality |
| Acceptable | 55-69 | Mark for reprocessing (underscore prefix) |
| Poor | 40-54 | Mark for reprocessing or move to previous stage |
| Very Poor | 0-39 | Move back to previous pipeline stage |

Thresholds are configurable in `data/config/audience_config.json`:

```json
{
  "quality_thresholds": {
    "min_score": 70,
    "reprocess_score": 50,
    "underscore_prefix": "_"
  }
}
```

## Content Type Detection

The system automatically detects content type based on fields present:

- **Idea**: Has `idea_id`, `synopsis`, or `hook` fields
- **Topic**: Has `topic_id`, `category`, and `keywords` fields
- **Title**: Has only `title` or `text` field (minimal structure)
- **Script**: Has `script` or `scenes` fields
- **Generic**: Fallback for unrecognized content

Different content types may have slightly different scoring emphasis. For example:
- Titles emphasize shareability and emotional impact
- Ideas emphasize novelty and clarity
- Scripts emphasize replay value and emotional impact

## Usage

### Scoring Individual Content

```python
from process_quality import calculate_score

content_data = {
    "idea_id": "001",
    "title": "The Secret Nobody Tells You",
    "synopsis": "A shocking revelation...",
    "hook": "What if everything was a lie?",
    "themes": ["mystery", "truth", "revelation"]
}

score = calculate_score(content_data)
print(f"Quality Score: {score:.1f}/100")
```

### Batch Processing

```bash
# Process specific folder
python scripts/process_quality.py /path/to/content/folder stage_name previous_stage

# Process entire pipeline
python scripts/process_quality.py
```

### Getting Individual Metrics

```python
from process_quality import assess_content_quality

scores = assess_content_quality(content_data, "idea")
print(f"Novelty: {scores['novelty']:.1f}")
print(f"Emotional: {scores['emotional']:.1f}")
print(f"Clarity: {scores['clarity']:.1f}")
print(f"Replay: {scores['replay']:.1f}")
print(f"Share: {scores['share']:.1f}")
```

## Iterative Quality Improvement

The system supports iterative refinement:

1. **High Quality (≥70)**: Content passes and continues to next stage
2. **Medium Quality (50-69)**: File renamed with underscore prefix (`_filename.json`) for reprocessing
3. **Low Quality (<50)**: File moved back to previous pipeline stage with underscore prefix

This allows content to be regenerated or improved until it meets quality standards.

## Examples

### High Quality Idea (Score: 96.9)

```json
{
  "title": "The Secret Truth Nobody Wants You to Know",
  "synopsis": "A shocking discovery reveals the hidden mysteries behind everyday life",
  "hook": "What if everything you believed was a lie?",
  "themes": ["mystery", "revelation", "truth", "conspiracy"],
  "genre": "thriller"
}
```

**Analysis**:
- Novelty: 95/100 (multiple novelty keywords, question format)
- Emotional: 92/100 (strong curiosity triggers, personal connection)
- Clarity: 95/100 (well-structured, clear message)
- Replay: 88/100 (multiple themes, mystery elements)
- Share: 100/100 (highly shareable hooks, universal appeal)

### Medium Quality Topic (Score: 68.9)

```json
{
  "topic_id": "002",
  "title": "Space Exploration Adventures",
  "description": "Discovering the wonders of space",
  "keywords": ["space", "planets", "exploration"]
}
```

**Analysis**:
- Novelty: 60/100 (some interesting elements but generic)
- Emotional: 55/100 (moderate appeal)
- Clarity: 85/100 (clear and structured)
- Replay: 70/100 (educational value)
- Share: 50/100 (moderate viral potential)

### Low Quality Content (Score: 46.2)

```json
{
  "title": "Test"
}
```

**Analysis**:
- Novelty: 35/100 (too simple, no detail)
- Emotional: 40/100 (no emotional connection)
- Clarity: 55/100 (too brief)
- Replay: 35/100 (no depth)
- Share: 40/100 (not shareable)

## Testing

Run the test suite to validate scoring:

```bash
python tests/test_content_quality.py
```

The test suite validates:
- Scoring accuracy for different content types
- Individual metric calculations
- Content type detection
- Configuration loading
- Score ranking and thresholds

## Configuration

### Adjusting Weights

To emphasize different aspects of quality, modify `config/scoring.yaml`:

```yaml
viral:
  novelty: 0.30      # Increased from 0.25
  emotional: 0.25
  clarity: 0.20
  replay: 0.10       # Decreased from 0.15
  share: 0.15
```

Weights must sum to 1.0.

### Adjusting Thresholds

To change quality gates, modify `data/config/audience_config.json`:

```json
{
  "quality_thresholds": {
    "min_score": 75,        # Stricter acceptance (was 70)
    "reprocess_score": 60,  # Higher reprocess threshold (was 50)
    "underscore_prefix": "_"
  }
}
```

## Best Practices

1. **Start Lenient**: Begin with lower thresholds (min: 65, reprocess: 45) and gradually increase
2. **Monitor Distribution**: Track score distributions to identify if thresholds need adjustment
3. **Content-Specific Tuning**: Different content types may benefit from different weight configurations
4. **Iterative Improvement**: Let low-scoring content cycle through reprocessing to learn what works
5. **Manual Review**: Periodically review edge cases (scores near thresholds) to validate scoring accuracy

## Limitations

- **Keyword-Based**: Relies on keyword detection, may miss subtle quality indicators
- **Language-Specific**: Optimized for English content
- **Context-Agnostic**: Doesn't consider broader context or trends
- **No Semantic Analysis**: Uses pattern matching rather than deep semantic understanding

For production use, consider augmenting with:
- LLM-based quality assessment
- Audience testing and feedback
- A/B testing of scored content
- Historical performance data

## Related Files

- `scripts/process_quality.py` - Main quality scoring implementation
- `config/scoring.yaml` - Viral scoring weights and thresholds
- `data/config/audience_config.json` - Quality thresholds and pipeline config
- `tests/test_content_quality.py` - Test suite for quality scorer
