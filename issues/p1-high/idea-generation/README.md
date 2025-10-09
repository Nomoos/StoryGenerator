# Idea Generation Group

**Phase:** 3 - Implementation  
**Tasks:** 7  
**Priority:** P1  
**Duration:** 2-3 days  
**Team Size:** 3-4 developers  
**Status:** ✅ **COMPLETE**

## Overview

This group transforms raw content into structured video ideas, topics, and clickable titles. It includes scoring and selection of the best titles for script development.

**Implementation Complete:** All 7 tasks implemented with 48 unit tests passing.

## Tasks

1. ✅ **03-ideas-01-reddit-adaptation** (P1) - Adapt Reddit stories into video ideas
2. ✅ **03-ideas-02-llm-generation** (P1) - Generate original ideas using LLM
3. ✅ **03-ideas-03-clustering** (P1) - Cluster ideas into topics
4. ✅ **03-ideas-04-title-generation** (P1) - Generate titles from topics
5. ✅ **04-scoring-01-title-scorer** (P1) - Score titles for viral potential
6. ✅ **04-scoring-02-voice-recommendation** (P1) - Recommend voice gender (F/M)
7. ✅ **04-scoring-03-top-selection** (P1) - Select top 5 titles per segment

## Dependencies

**Requires:**
- Content Pipeline group (ranked stories) - Required for Reddit adaptation (Task 1)
- OpenAI API or compatible LLM provider
- Python 3.10+, pytest

**Blocks:**
- Script Development group (needs selected titles)

## Quick Start

### Installation

```bash
# Install dependencies (if using OpenAI)
pip install openai tenacity pyyaml

# Or run tests with mock provider (no API key needed)
pytest tests/pipeline/ -v
```

### Running the Pipeline

```bash
# With mock provider (for testing)
python -m scripts.pipeline.generate_ideas \
  --gender women \
  --age 18-23 \
  --mock \
  --ideas-count 20 \
  --titles-per-topic 10 \
  --top-n 5

# With OpenAI (requires OPENAI_API_KEY environment variable)
export OPENAI_API_KEY="your-api-key"
python -m scripts.pipeline.generate_ideas \
  --gender women \
  --age 18-23 \
  --ideas-count 20 \
  --titles-per-topic 10 \
  --top-n 5

# Process all segments
python -m scripts.pipeline.generate_ideas --all-segments --model gpt-4o-mini
```

## Execution Strategy

```
Day 1:
├── Dev 1: Reddit adaptation + LLM generation
├── Dev 2: Topic clustering + Title generation
└── Dev 3: Title scoring + Voice recommendation

Day 2:
├── Dev 1: Top selection + Integration testing
├── Dev 2: Documentation + Issue updates
└── Dev 3: Pipeline orchestration + CLI

Day 3:
└── All: Code review, testing, deployment
```

## Success Criteria

- [x] 20+ ideas per segment (6 segments total)
- [x] Ideas clustered into 8+ topics per segment
- [x] 10+ titles generated per topic
- [x] All titles scored 0-100 with viral rubric
- [x] Voice recommendations (F/M) for each title
- [x] Top 5 titles selected per segment (30 total)
- [x] 48 unit tests passing
- [x] Complete pipeline orchestration script

## Implementation Details

### Core Modules

All modules located in `core/pipeline/`:

1. **idea_generation.py**
   - `IdeaAdapter` - Adapts Reddit stories
   - `IdeaGenerator` - Generates original LLM ideas
   - `merge_and_save_all_ideas()` - Combines both sources

2. **topic_clustering.py**
   - `TopicClusterer` - Clusters ideas into topics using LLM

3. **title_generation.py**
   - `TitleGenerator` - Generates title variants per topic

4. **title_scoring.py**
   - `TitleScorer` - Scores titles across 5 dimensions
   - Viral rubric: novelty, emotional, clarity, replay, shareability

5. **voice_recommendation.py**
   - `VoiceRecommender` - Recommends voice characteristics

6. **top_selection.py**
   - `TopSelector` - Selects top N titles with diversity

### Pipeline Script

**Location:** `scripts/pipeline/generate_ideas.py`

**Features:**
- CLI interface with argparse
- Support for mock and OpenAI providers
- Single segment or all-segments processing
- Configurable parameters (ideas count, titles per topic, etc.)
- Comprehensive logging

### Testing

```bash
# Run all pipeline tests (48 tests)
pytest tests/pipeline/ -v

# Run specific test module
pytest tests/pipeline/test_title_scoring.py -v

# Run with coverage
pytest tests/pipeline/ --cov=core/pipeline --cov-report=term-missing
```

**Test Coverage:**
- `test_idea_generation.py` - 9 tests
- `test_title_scoring.py` - 12 tests
- `test_voice_recommendation.py` - 18 tests
- `test_top_selection.py` - 9 tests

## Output Files

```
data/
├── ideas/{gender}/{age}/
│   ├── reddit_adapted.json      # Task 1 output
│   ├── llm_generated.json        # Task 2 output
│   └── all_ideas.json            # Merged ideas
├── topics/{gender}/{age}/
│   └── topics_clustered.json     # Task 3 output
├── titles/{gender}/{age}/
│   ├── titles_raw.json           # Task 4 output
│   └── titles_scored.json        # Task 5 output
├── voices/choice/{gender}/{age}/
│   └── titles_with_voices.json   # Task 6 output
└── selected/{gender}/{age}/
    └── top_5_titles.json         # Task 7 output
```

## Configuration

**Scoring Config:** `config/scoring.yaml`

```yaml
viral:
  novelty: 0.25
  emotional: 0.25
  clarity: 0.20
  replay: 0.15
  share: 0.15

thresholds:
  excellent: 85
  good: 70
  acceptable: 55
  poor: 40
```

## Architecture

### LLM Provider Interface

Uses abstraction for easy provider swapping:

```python
from core.interfaces.llm_provider import ILLMProvider
from providers.openai_provider import OpenAIProvider
from providers.mock_provider import MockLLMProvider

# Production
llm = OpenAIProvider(model="gpt-4o-mini")

# Testing
llm = MockLLMProvider()
```

### Data Flow

```
Reddit Stories (optional) ──┐
                            ├──> Ideas ──> Topics ──> Titles ──> Scored Titles ──> +Voices ──> Top 5
LLM Generation ─────────────┘
```

## Performance

**Estimated Runtime (per segment):**
- With mock provider: < 1 second
- With OpenAI API:
  - Ideas: ~30 seconds (20 ideas)
  - Clustering: ~10 seconds  
  - Titles: ~60 seconds (80 titles across 8 topics)
  - Scoring: < 1 second (local)
  - Voice: < 1 second (local)
  - Selection: < 1 second (local)
  - **Total:** ~2 minutes per segment (includes API latency)

**Cost Estimates (OpenAI gpt-4o-mini):**
- Per segment: ~$0.10-0.20
- All 6 segments: ~$0.60-1.20

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'openai'**
   ```bash
   pip install openai tenacity
   ```

2. **ValueError: OpenAI API key is required**
   ```bash
   export OPENAI_API_KEY="your-key"
   # Or use --mock flag for testing
   ```

3. **No topics created / No titles generated**
   - Ensure enough ideas generated (min 8 for clustering)
   - Check LLM responses are being parsed correctly
   - Use --mock flag to debug with predictable responses

## Next Steps

After completion, the **Script Development** group can begin generating scripts for the selected titles.

**Handoff Artifacts:**
- 30 top-selected titles (5 per segment × 6 segments)
- Complete metadata (scores, voice recommendations)
- Topic context for each title
- Source idea attribution

## Related Documentation

- `/docs/PIPELINE_OUTPUT_FILES.md` - Complete output file specs
- `/config/scoring.yaml` - Viral scoring configuration
- `/tests/pipeline/` - Test suite documentation
- Individual task `issue.md` files - Detailed implementation notes
