# Title Improvement System

## Overview

The Title Improvement system generates and scores improved title variants using GPT or local LLM. It automatically:
- Generates 5 variants per title (configurable)
- Scores each variant using the existing scoring rubric
- Selects the best-performing variant
- Saves results to `/titles/{segment}/{age}/{title_id}_improved.json`
- Updates a centralized title registry with changes

## Quick Start

### Prerequisites

**Option A: Using Local LLM (Ollama)**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the recommended model
ollama pull qwen2.5:14b-instruct

# Verify Ollama is running
ollama list
```

**Option B: Using OpenAI GPT**
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

### Basic Usage

**Improve a specific title:**
```bash
python scripts/title_improve.py women 18-23 --title-id example_title_001
```

**Improve all titles in a segment:**
```bash
python scripts/title_improve.py women 18-23
```

**Improve all titles across all segments:**
```bash
python scripts/title_improve.py
```

**Generate custom number of variants:**
```bash
python scripts/title_improve.py women 18-23 --variant-count 10
```

## Input

The script looks for title files in:
```
data/titles/{segment}/{age}/
```

Supported formats:
- **JSON files** with `title`, `story_title`, or `video_title` keys
- **Text files** with title as first line
- **Subdirectories** with `idea.json` files

Example input file (`data/titles/women/18-23/my_title_001.json`):
```json
{
  "title": "5 Simple Ways to Stay Motivated",
  "created_at": "2025-01-15T10:30:00",
  "topic_cluster_id": "motivation_001"
}
```

## Output

### 1. Improved Title Results

**Location:** `data/titles/{segment}/{age}/{title_id}_improved.json`

**Structure:**
```json
{
  "metadata": {
    "title_id": "example_title_001",
    "source_file": "example_title_001.json",
    "segment": "women",
    "age": "18-23",
    "improved_at": "2025-10-07T12:14:04.050410",
    "variant_count": 5
  },
  "original_title": {
    "title": "5 Simple Ways to Stay Motivated",
    "score": 63.5,
    "scores": {
      "hook_strength": 60,
      "clarity": 70,
      "relevance": 60,
      "length_format": 80,
      "viral_potential": 50
    },
    "rationale": "Hook could be more compelling..."
  },
  "best_title": {
    "title": "Why 5 Simple Ways to Stay Motivated?",
    "score": 72.5,
    "scores": {
      "hook_strength": 90,
      "clarity": 70,
      "relevance": 60,
      "length_format": 80,
      "viral_potential": 50
    },
    "rationale": "Strong hook with curiosity-inducing elements...",
    "is_original": false,
    "variant_number": 1,
    "improvement_pct": 14.17
  },
  "all_variants": [
    // All scored variants including original
  ]
}
```

### 2. Title Registry

**Location:** `data/titles/title_registry.json`

Tracks all improved titles with slugs and change history:

```json
{
  "metadata": {
    "created_at": "2025-10-07T12:14:04.050798",
    "updated_at": "2025-10-07T12:14:04.050813",
    "total_titles": 2
  },
  "titles": {
    "women/18-23/example_title_001": {
      "title_id": "example_title_001",
      "segment": "women",
      "age": "18-23",
      "original_title": "5 Simple Ways to Stay Motivated",
      "improved_title": "Why 5 Simple Ways to Stay Motivated?",
      "slug": "why-5-simple-ways-to-stay-motivated",
      "original_score": 63.5,
      "improved_score": 72.5,
      "improvement_pct": 14.17,
      "is_changed": true,
      "improved_at": "2025-10-07T12:14:04.050410"
    }
  }
}
```

## Configuration

### LLM Configuration

Create `data/config/llm_config.yaml` (optional):

```yaml
# LLM Provider: 'ollama' or 'openai'
provider: ollama

# Model to use
model: qwen2.5:14b-instruct  # For Ollama
# model: gpt-4                # For OpenAI

# Ollama settings
ollama_host: http://localhost:11434

# Generation settings
temperature: 0.7
max_tokens: 200
```

If no config file exists, the script uses sensible defaults (Ollama with qwen2.5:14b-instruct).

### Scoring Configuration

The system uses the existing scoring rubric from `data/config/scoring.yaml`. No additional configuration needed.

## How It Works

1. **Load Title**: Extracts title from input file
2. **Generate Variants**: Creates 5 improved versions using:
   - **Ollama**: Local LLM generates creative variants
   - **OpenAI**: GPT generates creative variants
   - **Fallback**: Rule-based patterns (questions, lists, hooks)
3. **Score Variants**: Applies scoring rubric to each variant + original
4. **Select Best**: Chooses highest-scoring title
5. **Save Results**: Writes detailed JSON with all scores
6. **Update Registry**: Tracks changes with slugs

## Variant Generation Strategies

The LLM is prompted to generate variants using proven viral patterns:

- **Questions**: "Why...?", "What If...?", "How To...?"
- **Numbers**: "5 Things...", "7 Secrets..."
- **Curiosity**: "The Truth About...", "You Won't Believe..."
- **Personal**: "How I...", "My Experience With..."
- **Authority**: "Everyone...", "Nobody Tells You..."

## Scoring Criteria

Each variant is scored on:
- **Hook Strength** (30%): Curiosity and emotional appeal
- **Clarity** (20%): Easy to understand
- **Relevance** (20%): Audience alignment
- **Length & Format** (15%): Optimal for social media (40-60 chars)
- **Viral Potential** (15%): Shareability

See [TITLE_SCORING.md](TITLE_SCORING.md) for detailed scoring information.

## Command-Line Options

```bash
usage: title_improve.py [segment] [age] [options]

positional arguments:
  segment               Target segment (men/women)
  age                   Target age range (e.g., 18-23)

optional arguments:
  --title-id ID         Specific title ID to improve
  --variant-count N     Number of variants to generate (default: 5)
  --titles-dir PATH     Custom titles directory path
  --output-dir PATH     Custom output directory path
```

## Examples

### Example 1: Single Title Improvement

```bash
python scripts/title_improve.py women 18-23 --title-id my_story_001
```

Output:
```
============================================================
Improving Title: my_story_001
Original: 5 Simple Tips for Life
============================================================

Generating 5 title variants...
✅ Generated 5 variants

Scoring variants...
  Original: 5 Simple Tips for Life
    Score: 61.5/100
  Variant 1: Why You Need These 5 Life-Changing Tips
    Score: 75.2/100
  ...

🏆 Best Title: Why You Need These 5 Life-Changing Tips
   Score: 75.2/100
   Improvement: +22.3%

✅ Saved results to data/titles/women/18-23/my_story_001_improved.json
```

### Example 2: Batch Processing

```bash
python scripts/title_improve.py men 24-30
```

Processes all titles in the men/24-30 segment and updates the registry.

### Example 3: Custom Variant Count

```bash
python scripts/title_improve.py women 18-23 --variant-count 10
```

Generates 10 variants instead of the default 5 for more options.

## Integration with Pipeline

The title improvement system integrates with the content pipeline:

```
Pipeline Stage 4: Titles
    ↓
[title_improve.py] ← NEW
    ↓
Enhanced Titles + Registry
    ↓
Pipeline Stage 5: Scripts
```

## Testing

Run the test suite:

```bash
python tests/test_title_improve.py
```

Tests cover:
- Module imports
- Local variant generation
- LLM variant generation
- Scoring and selection
- File I/O
- Registry updates
- End-to-end workflow

## Troubleshooting

### Issue: "Connection refused" to Ollama

**Solution:**
```bash
# Check if Ollama is running
ollama list

# If not, start it (usually auto-starts)
ollama serve
```

### Issue: LLM generates no variants

**Solution:**
- The system automatically falls back to rule-based generation
- Check LLM configuration in logs
- Verify API keys for OpenAI
- Ensure Ollama model is pulled: `ollama pull qwen2.5:14b-instruct`

### Issue: Low improvement scores

**Solution:**
- Original titles may already be well-optimized
- Try increasing `--variant-count` for more options
- Review scoring criteria in `data/config/scoring.yaml`
- Check that variants align with target audience

### Issue: No titles found

**Solution:**
- Verify title files exist in correct location:
  ```
  data/titles/{segment}/{age}/
  ```
- Check file format (JSON with `title` key or text file)
- Ensure files don't start with underscore (ignored)

## Performance

- **Per Title**: ~5-10 seconds (depends on LLM)
  - Variant Generation: 2-5 seconds
  - Scoring: 1-2 seconds
  - File I/O: <1 second
- **Batch Processing**: Scales linearly with number of titles
- **Registry Updates**: O(1) per title

## Future Enhancements

Potential improvements:
1. **A/B Testing**: Track actual performance vs. predicted scores
2. **Learning**: Improve variant generation based on past successes
3. **Multi-language**: Support for non-English titles
4. **Custom Patterns**: User-defined variant generation rules
5. **API Integration**: Real-time title improvement endpoint

## License

Part of the StoryGenerator project.
