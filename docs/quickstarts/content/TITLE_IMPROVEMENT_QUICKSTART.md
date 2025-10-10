# Title Improvement - Quick Reference

## Quick Start Commands

### Improve a Single Title
```bash
python scripts/title_improve.py women 18-23 --title-id my_title_001
```

### Improve All Titles in a Segment
```bash
python scripts/title_improve.py women 18-23
```

### Improve All Titles (All Segments)
```bash
python scripts/title_improve.py
```

### Generate More Variants
```bash
python scripts/title_improve.py women 18-23 --variant-count 10
```

## Output Files

### Improved Title Results
```
data/titles/{segment}/{age}/{title_id}_improved.json
```

Contains:
- Original title with score
- Best improved title with score
- All variants tested
- Improvement percentage
- Rationale for each score

### Title Registry
```
data/titles/title_registry.json
```

Contains:
- Centralized tracking of all improved titles
- Slugs for URL-friendly names
- Change history (which titles were improved)
- Score improvements

## Configuration

### LLM Configuration
Edit `data/config/llm_config.yaml`:

```yaml
# For Ollama (local)
provider: ollama
model: qwen2.5:14b-instruct
ollama_host: http://localhost:11434

# For OpenAI
provider: openai
model: gpt-4
# Set OPENAI_API_KEY environment variable
```

### Prerequisites

**For Ollama:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull qwen2.5:14b-instruct
```

**For OpenAI:**
```bash
export OPENAI_API_KEY="your-key-here"
```

## Testing

```bash
# Run tests
python tests/test_title_improve.py

# Run examples
python examples/title_improvement_examples.py
```

## Common Issues

### Issue: "Connection refused" to Ollama
**Solution:** Start Ollama server
```bash
ollama serve
```

### Issue: No variants generated
**Solution:** System automatically falls back to rule-based generation

### Issue: Low improvement scores
**Solution:** Original titles may already be optimal
- Try increasing `--variant-count`
- Review scoring criteria in `data/config/scoring.yaml`

## Integration

Add to your pipeline:
```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
import title_improve

# Improve a title
result = title_improve.improve_title(
    title_file=Path("data/titles/women/18-23/my_title.json"),
    segment="women",
    age="18-23",
    output_dir=Path("data/titles"),
    llm_config=title_improve.load_llm_config(),
    scoring_config=title_score.load_scoring_config(),
    variant_count=5
)
```

## Documentation

- **Full Guide:** [docs/TITLE_IMPROVEMENT.md](../docs/TITLE_IMPROVEMENT.md)
- **Scoring System:** [docs/TITLE_SCORING.md](../docs/TITLE_SCORING.md)
- **Examples:** [examples/title_improvement_examples.py](../examples/title_improvement_examples.py)
- **Tests:** [tests/test_title_improve.py](../tests/test_title_improve.py)
