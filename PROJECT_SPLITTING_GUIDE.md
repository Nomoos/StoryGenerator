# Project Splitting Guide

## 📋 Table of Contents
- [Overview](#overview)
- [Why Split Projects](#why-split-projects)
- [What Can Be Extracted](#what-can-be-extracted)
- [Extraction Strategies](#extraction-strategies)
- [Step-by-Step Extraction Process](#step-by-step-extraction-process)
- [Common Extraction Patterns](#common-extraction-patterns)
- [Real-World Examples](#real-world-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The **StoryGenerator** repository is designed as a **modular monorepo** where individual components can be extracted and used in smaller, focused projects. This guide shows you how to identify, extract, and reuse components while maintaining SOLID principles.

### What Makes This Repository Splittable?

1. **Clear Module Boundaries**: Each component has well-defined inputs/outputs
2. **Interface-Based Design**: Dependencies are abstracted through interfaces
3. **Minimal Coupling**: Components don't directly depend on each other
4. **Self-Contained Logic**: Each module can operate independently
5. **Standardized Patterns**: Consistent architecture across all components

## Why Split Projects

### Benefits of Extraction

- **Reduced Complexity**: Smaller projects are easier to understand and maintain
- **Faster Development**: Work on specific features without full pipeline overhead
- **Independent Deployment**: Deploy components separately
- **Focused Testing**: Test only what you need
- **Reusability**: Use components across multiple projects
- **Learning**: Understand specific parts without learning entire system
- **Microservices**: Build microservice architecture from monolith

### When to Extract

Extract components when you need to:
- ✅ Build a specialized tool focusing on one pipeline stage
- ✅ Create a lightweight service with minimal dependencies
- ✅ Learn a specific technology without full system complexity
- ✅ Deploy a component as a microservice
- ✅ Share functionality across multiple projects
- ✅ Prototype new features quickly

## What Can Be Extracted

### Extractable Components by Category

#### 1. Pipeline Stages (Easiest to Extract)

Each pipeline stage is designed for independent operation:

```
PrismQ/Pipeline/
├── 01_IdeaGeneration/      ✅ Extractable as "Idea Generator Service"
├── 02_TextGeneration/      ✅ Extractable as "Content Generator Service"
│   ├── StoryGenerator/     ✅ Extractable as "Story Generator Library"
│   ├── StoryTitleProcessor/ ✅ Extractable as "Title Generator Tool"
│   ├── StoryTitleScoring/  ✅ Extractable as "Title Scorer Library"
│   └── TagsGenerator/      ✅ Extractable as "Tag Generator Service"
├── 03_AudioGeneration/     ✅ Extractable as "Audio Generator Service"
│   ├── VoiceOverGenerator/ ✅ Extractable as "Voice Synthesis Library"
│   └── SubtitleGenerator/  ✅ Extractable as "Subtitle Generator Tool"
├── 04_ImageGeneration/     ✅ Extractable as "Image Generator Service"
└── 05_VideoGeneration/     ✅ Extractable as "Video Assembly Service"
```

#### 2. Infrastructure Services (Core Utilities)

Shared services that can be extracted as libraries:

```
PrismQ/Infrastructure/Core/Shared/
├── logging.py              ✅ Extractable as "Logging Library"
├── cache.py                ✅ Extractable as "Cache Service"
├── retry.py                ✅ Extractable as "Retry Utility"
├── validation.py           ✅ Extractable as "Validation Library"
└── database.py             ✅ Extractable as "Database Abstraction Layer"
```

#### 3. Provider Integrations

External service integrations:

```
PrismQ/Infrastructure/Platform/Providers/
├── openai_provider.py      ✅ Extractable as "OpenAI Client Library"
├── youtube_provider.py     ✅ Extractable as "YouTube Publisher"
├── tiktok_provider.py      ✅ Extractable as "TikTok Publisher"
└── wordpress_provider.py   ✅ Extractable as "WordPress Publisher"
```

#### 4. Interfaces (Most Important for SOLID)

Abstract interfaces that define contracts:

```
PrismQ/Infrastructure/Core/Shared/interfaces/
├── pipeline_stage.py       ✅ Must extract with any pipeline stage
├── llm_provider.py         ✅ Must extract with any LLM-using component
├── platform_provider.py    ✅ Must extract with any publisher
├── storage_provider.py     ✅ Must extract with any storage component
└── voice_provider.py       ✅ Must extract with any voice component
```

## Extraction Strategies

### Strategy 1: Single Component Extraction

Extract one focused component with minimal dependencies.

**Best For**: Learning, prototyping, microservices

**Example**: Extract just the Title Scorer

```
new-project/
├── title_scorer/
│   ├── __init__.py
│   ├── scorer.py           # From StoryTitleScoring/
│   └── validators.py       # From Core/Shared/validation.py
├── tests/
│   └── test_scorer.py
├── requirements.txt        # Minimal dependencies
└── README.md
```

### Strategy 2: Vertical Slice Extraction

Extract a complete pipeline stage with its dependencies.

**Best For**: Building a complete service around one stage

**Example**: Extract complete Text Generation stage

```
text-generator-service/
├── generators/
│   ├── story_generator.py
│   ├── title_processor.py
│   └── tags_generator.py
├── interfaces/
│   ├── llm_provider.py     # Required interface
│   └── storage_provider.py # Required interface
├── providers/
│   ├── openai_provider.py  # Concrete implementation
│   └── mock_provider.py    # For testing
├── utils/
│   ├── logging.py
│   ├── validation.py
│   └── retry.py
├── tests/
├── requirements.txt
└── README.md
```

### Strategy 3: Horizontal Layer Extraction

Extract all components at one layer (e.g., all providers).

**Best For**: Creating a library of utilities or integrations

**Example**: Extract all platform providers

```
platform-publishers/
├── publishers/
│   ├── __init__.py
│   ├── youtube.py
│   ├── tiktok.py
│   ├── instagram.py
│   └── wordpress.py
├── interfaces/
│   └── platform_provider.py
├── common/
│   ├── retry.py
│   └── logging.py
├── tests/
├── requirements.txt
└── README.md
```

### Strategy 4: Interface + Multiple Implementations

Extract an interface with multiple implementations.

**Best For**: Creating pluggable libraries

**Example**: Extract LLM provider interface with implementations

```
llm-providers/
├── interfaces/
│   └── llm_provider.py
├── providers/
│   ├── openai_provider.py
│   ├── anthropic_provider.py
│   ├── local_provider.py
│   └── mock_provider.py
├── utils/
│   ├── retry.py
│   └── caching.py
├── tests/
├── requirements.txt
└── README.md
```

## Step-by-Step Extraction Process

### Step 1: Identify the Component

**Goal**: Determine what you want to extract and why.

**Questions to Ask**:
- What functionality do I need?
- What are the inputs and outputs?
- What dependencies does it have?
- Will it run standalone or integrate with other code?

**Example**: Extract Title Scorer

```python
# Identify the target component
Target: PrismQ/Pipeline/02_TextGeneration/StoryTitleScoring/title_scoring.py

# Check what it does
Purpose: Score title quality on a scale of 0.0 to 1.0

# Check inputs/outputs
Input: str (title text)
Output: float (quality score)

# Check dependencies
Dependencies:
- Minimal - mostly self-contained
- Uses validation.py for input validation
- No LLM required (rule-based scoring)
```

### Step 2: Map Dependencies

**Goal**: Identify all direct and transitive dependencies.

**Create a Dependency Map**:

```
title_scoring.py
├── validation.py           # Direct dependency
│   └── (no dependencies)   # Leaf node
└── logging.py              # Direct dependency (optional)
    └── (no dependencies)   # Leaf node
```

**Tool**: Use Python's dependency analysis:

```bash
# In the repository root
python -c "
import ast
import sys

def get_imports(filename):
    with open(filename) as f:
        tree = ast.parse(f.read())
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports

# Analyze target file
imports = get_imports('PrismQ/Pipeline/02_TextGeneration/StoryTitleScoring/title_scoring.py')
print('Dependencies:')
for imp in imports:
    if 'PrismQ' in imp or 'core' in imp:
        print(f'  - {imp}')
"
```

### Step 3: Create Project Structure

**Goal**: Set up the new project structure.

**Template**:

```bash
# Create new project
mkdir title-scorer
cd title-scorer

# Create directory structure
mkdir -p title_scorer tests docs

# Initialize Python package
touch title_scorer/__init__.py
touch tests/__init__.py

# Create essential files
cat > requirements.txt << 'EOF'
# Core dependencies (if any)
# Add only what's actually needed
EOF

cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="title-scorer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.10",
)
EOF

cat > README.md << 'EOF'
# Title Scorer

Scores title quality based on length, keywords, and emotional appeal.

## Installation

```bash
pip install -e .
```

## Usage

```python
from title_scorer import TitleScorer

scorer = TitleScorer()
score = scorer.score_title("Amazing Python Tips for Beginners")
print(f"Score: {score:.2f}")
```
EOF

cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "title-scorer"
version = "0.1.0"
description = "Title quality scoring library"
requires-python = ">=3.10"
EOF
```

### Step 4: Copy and Adapt Code

**Goal**: Copy source code and adapt imports.

**Process**:

```bash
# Copy main file
cp ../StoryGenerator/PrismQ/Pipeline/02_TextGeneration/StoryTitleScoring/title_scoring.py \
   title_scorer/scorer.py

# Copy dependencies
cp ../StoryGenerator/PrismQ/Infrastructure/Core/Shared/validation.py \
   title_scorer/validation.py

# Optional: Copy logging (or remove if not needed)
# cp ../StoryGenerator/PrismQ/Infrastructure/Core/Shared/logging.py \
#    title_scorer/logging.py
```

**Adapt Imports**:

```python
# Original (in StoryGenerator)
from PrismQ.Infrastructure.Core.Shared.validation import validate_string

# Adapted (in extracted project)
from .validation import validate_string

# OR if you removed validation.py, inline the validation
def validate_string(value: str, min_length: int = 1) -> bool:
    return isinstance(value, str) and len(value) >= min_length
```

### Step 5: Simplify and Remove Unused Code

**Goal**: Remove code that's not needed in the extracted component.

**Example**:

```python
# Original title_scoring.py (in StoryGenerator)
from PrismQ.Infrastructure.Core.Shared.validation import validate_string
from PrismQ.Infrastructure.Core.Shared.logging import get_logger
from PrismQ.Infrastructure.Core.Shared.cache import CacheService

logger = get_logger(__name__)

class TitleScorer:
    def __init__(self, cache: CacheService = None):
        self.cache = cache
        logger.info("TitleScorer initialized")
    
    def score_title(self, title: str) -> float:
        # Check cache
        if self.cache:
            cached_score = self.cache.get(f"score:{title}")
            if cached_score:
                return cached_score
        
        # Score title
        score = self._calculate_score(title)
        
        # Cache result
        if self.cache:
            self.cache.set(f"score:{title}", score)
        
        return score
    
    def _calculate_score(self, title: str) -> float:
        validate_string(title)
        # Scoring logic...


# Simplified (in extracted project)
class TitleScorer:
    """Simplified title scorer without caching and logging."""
    
    def score_title(self, title: str) -> float:
        """Score a title on a scale of 0.0 to 1.0."""
        if not isinstance(title, str) or len(title) == 0:
            raise ValueError("Title must be a non-empty string")
        
        return self._calculate_score(title)
    
    def _calculate_score(self, title: str) -> float:
        score = 0.0
        
        # Length check (20-60 characters is optimal)
        length = len(title)
        if 20 <= length <= 60:
            score += 0.4
        elif 10 <= length < 20 or 60 < length <= 80:
            score += 0.2
        
        # Keyword check (presence of power words)
        power_words = ["amazing", "ultimate", "essential", "proven", "secret"]
        if any(word in title.lower() for word in power_words):
            score += 0.3
        
        # Emotional appeal (questions, numbers, specificity)
        if "?" in title:
            score += 0.15
        if any(char.isdigit() for char in title):
            score += 0.15
        
        return min(score, 1.0)  # Cap at 1.0
```

### Step 6: Write Tests

**Goal**: Ensure extracted component works correctly.

**Create Tests**:

```python
# tests/test_title_scorer.py
import pytest
from title_scorer import TitleScorer


def test_score_empty_title():
    """Test that empty title raises error."""
    scorer = TitleScorer()
    with pytest.raises(ValueError):
        scorer.score_title("")


def test_score_optimal_length():
    """Test that optimal length titles score well."""
    scorer = TitleScorer()
    score = scorer.score_title("Amazing Python Tips for Beginners")
    assert score >= 0.5  # Should score well


def test_score_with_power_words():
    """Test that power words increase score."""
    scorer = TitleScorer()
    score_with = scorer.score_title("Ultimate Guide to Python")
    score_without = scorer.score_title("Guide to Python")
    assert score_with > score_without


def test_score_with_question():
    """Test that questions increase score."""
    scorer = TitleScorer()
    score_with = scorer.score_title("How to Learn Python?")
    score_without = scorer.score_title("How to Learn Python")
    assert score_with > score_without


def test_score_with_numbers():
    """Test that numbers increase score."""
    scorer = TitleScorer()
    score_with = scorer.score_title("10 Python Tips")
    score_without = scorer.score_title("Python Tips")
    assert score_with > score_without


def test_score_returns_float():
    """Test that score is always a float between 0 and 1."""
    scorer = TitleScorer()
    score = scorer.score_title("Test Title")
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
```

**Run Tests**:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=title_scorer --cov-report=term-missing
```

### Step 7: Document the Extracted Component

**Goal**: Provide clear documentation for standalone use.

**Create Comprehensive README**:

```markdown
# Title Scorer

A lightweight Python library for scoring title quality based on best practices for engaging content.

## Features

- **Length Optimization**: Scores titles based on optimal character length (20-60 chars)
- **Power Words Detection**: Identifies engaging keywords that attract attention
- **Emotional Appeal**: Checks for questions and specific numbers
- **No Dependencies**: Pure Python implementation with no external dependencies
- **Fast**: Rule-based scoring provides instant results

## Installation

```bash
pip install title-scorer
```

Or install from source:

```bash
git clone https://github.com/yourusername/title-scorer.git
cd title-scorer
pip install -e .
```

## Quick Start

```python
from title_scorer import TitleScorer

# Create scorer instance
scorer = TitleScorer()

# Score a title
score = scorer.score_title("10 Amazing Python Tips for Beginners")
print(f"Title score: {score:.2f}")  # Output: Title score: 0.85
```

## Scoring Criteria

The scorer evaluates titles on three main criteria:

1. **Length (40% weight)**
   - Optimal: 20-60 characters
   - Acceptable: 10-20 or 60-80 characters
   - Poor: <10 or >80 characters

2. **Power Words (30% weight)**
   - Detects engaging keywords: "amazing", "ultimate", "essential", "proven", "secret"

3. **Emotional Appeal (30% weight)**
   - Questions (15%): Titles ending with "?"
   - Numbers (15%): Titles containing specific numbers

## Examples

```python
scorer = TitleScorer()

# Excellent title
score = scorer.score_title("7 Secret Python Tricks You Need to Know")
# Score: ~0.95 (optimal length + power word + number)

# Good title
score = scorer.score_title("How to Master Python in 2024?")
# Score: ~0.70 (good length + question + number)

# Average title
score = scorer.score_title("Python Tutorial")
# Score: ~0.20 (too short, no power words)
```

## API Reference

### `TitleScorer`

Main class for title scoring.

#### `score_title(title: str) -> float`

Score a title on a scale of 0.0 to 1.0.

**Parameters:**
- `title` (str): The title to score

**Returns:**
- float: Quality score between 0.0 and 1.0

**Raises:**
- `ValueError`: If title is empty or not a string

**Example:**
```python
scorer = TitleScorer()
score = scorer.score_title("Amazing Python Guide")
```

## Testing

Run the test suite:

```bash
pytest tests/
```

With coverage:

```bash
pytest tests/ --cov=title_scorer --cov-report=html
```

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Origin

Extracted from the [StoryGenerator](https://github.com/Nomoos/StoryGenerator) project,
which demonstrates SOLID principles in a production content generation pipeline.
```

### Step 8: Verify and Publish

**Goal**: Ensure everything works and optionally publish.

**Final Verification Checklist**:

```bash
# 1. Check code quality
python -m black title_scorer/
python -m flake8 title_scorer/
python -m mypy title_scorer/

# 2. Run all tests
pytest tests/ -v --cov=title_scorer

# 3. Test installation
pip install -e .
python -c "from title_scorer import TitleScorer; print(TitleScorer().score_title('Test'))"

# 4. Build package
python -m build

# 5. Test package installation
pip install dist/title_scorer-0.1.0-py3-none-any.whl

# 6. Optionally publish to PyPI
python -m twine upload dist/*
```

## Common Extraction Patterns

### Pattern 1: Extract Utility Library

**Use Case**: Create a reusable utility library

**Example**: Extract Retry Logic

```
retry-utils/
├── retry_utils/
│   ├── __init__.py
│   ├── retry.py          # Retry with exponential backoff
│   ├── circuit_breaker.py # Circuit breaker pattern
│   └── decorators.py     # Retry decorators
├── tests/
│   ├── test_retry.py
│   └── test_circuit_breaker.py
├── examples/
│   └── basic_usage.py
├── requirements.txt       # No dependencies!
└── README.md
```

**Key Files to Extract**:
- `PrismQ/Infrastructure/Core/Shared/retry.py`

**Dependencies**: None (self-contained)

### Pattern 2: Extract LLM Integration

**Use Case**: Create a unified LLM client library

**Example**: Extract LLM Providers

```
llm-client/
├── llm_client/
│   ├── __init__.py
│   ├── interfaces/
│   │   └── provider.py       # ILLMProvider interface
│   ├── providers/
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   ├── local.py
│   │   └── mock.py
│   └── utils/
│       ├── retry.py
│       └── caching.py
├── tests/
├── examples/
├── requirements.txt
└── README.md
```

**Key Files to Extract**:
- `PrismQ/Infrastructure/Core/Shared/interfaces/llm_provider.py`
- `PrismQ/Infrastructure/Platform/Providers/openai_provider.py`
- `PrismQ/Infrastructure/Platform/Providers/mock_provider.py`

**Dependencies**:
- `openai` package
- `retry.py` from infrastructure

### Pattern 3: Extract Pipeline Stage

**Use Case**: Create a microservice for one pipeline stage

**Example**: Extract Voice Over Generator

```
voiceover-service/
├── voiceover/
│   ├── __init__.py
│   ├── generator.py          # Main generator
│   ├── interfaces/
│   │   └── voice_provider.py # Voice provider interface
│   ├── providers/
│   │   ├── elevenlabs.py
│   │   └── google_tts.py
│   └── utils/
│       ├── audio_processing.py
│       └── validation.py
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   └── models.py            # Pydantic models
├── tests/
├── docker/
│   └── Dockerfile
├── requirements.txt
└── README.md
```

**Key Files to Extract**:
- `PrismQ/Pipeline/03_AudioGeneration/VoiceOverGenerator/`
- `PrismQ/Infrastructure/Core/Shared/interfaces/voice_provider.py`

**Dependencies**:
- `elevenlabs` or `google-cloud-texttospeech`
- `fastapi` and `uvicorn` (for API)
- `pydantic` (for validation)

### Pattern 4: Extract Configuration Management

**Use Case**: Create a configuration library

**Example**: Extract Config System

```
config-manager/
├── config_manager/
│   ├── __init__.py
│   ├── config.py            # Configuration loader
│   ├── validators.py        # Configuration validation
│   └── schemas/
│       ├── base.py
│       └── custom.py
├── tests/
├── examples/
│   ├── basic_config.py
│   └── custom_schema.py
├── requirements.txt
└── README.md
```

**Key Files to Extract**:
- `PrismQ/Infrastructure/Core/Shared/config.py`
- `PrismQ/Infrastructure/Core/Shared/validation.py`

**Dependencies**:
- `pydantic` or `python-dotenv`

## Real-World Examples

### Example 1: Extract Title Generator for Blog Platform

**Scenario**: You're building a blog platform and need automatic title generation.

**What to Extract**:
- Title Generator
- Title Scorer
- LLM Provider Interface

**Project Structure**:

```
blog-title-generator/
├── blog_titles/
│   ├── __init__.py
│   ├── generator.py          # Title generation
│   ├── scorer.py             # Title scoring
│   ├── interfaces/
│   │   └── llm_provider.py   # LLM interface
│   └── providers/
│       ├── openai.py
│       └── mock.py           # For testing
├── api/
│   └── app.py                # FastAPI endpoint
├── tests/
├── requirements.txt
└── README.md
```

**Usage in Your Blog Platform**:

```python
from blog_titles import TitleGenerator, TitleScorer, OpenAIProvider

# Initialize
llm = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
generator = TitleGenerator(llm)
scorer = TitleScorer()

# Generate and score titles
article_content = "Article about Python best practices..."
titles = generator.generate_titles(article_content, count=5)

# Score and rank titles
scored_titles = [(title, scorer.score_title(title)) for title in titles]
scored_titles.sort(key=lambda x: x[1], reverse=True)

# Use best title
best_title = scored_titles[0][0]
```

### Example 2: Extract Reddit Scraper for Market Research

**Scenario**: You need to collect market research data from Reddit.

**What to Extract**:
- Idea Scraper (Reddit integration)
- Topic Clustering
- Data Storage

**Project Structure**:

```
reddit-market-research/
├── reddit_research/
│   ├── __init__.py
│   ├── scraper.py           # Reddit scraping
│   ├── clustering.py        # Topic clustering
│   └── storage.py           # Data persistence
├── analysis/
│   ├── sentiment.py         # Sentiment analysis
│   └── trends.py            # Trend detection
├── cli/
│   └── research_cli.py      # Command-line tool
├── tests/
├── requirements.txt
└── README.md
```

**Usage**:

```python
from reddit_research import RedditScraper, TopicClusterer

# Scrape subreddit
scraper = RedditScraper(client_id="...", client_secret="...")
posts = scraper.scrape_subreddit("python", limit=100)

# Cluster topics
clusterer = TopicClusterer()
topics = clusterer.cluster_posts(posts)

# Analyze trends
for topic in topics:
    print(f"Topic: {topic.name}")
    print(f"Mentions: {topic.post_count}")
    print(f"Sentiment: {topic.avg_sentiment}")
```

### Example 3: Extract Video Assembly for Different Platform

**Scenario**: You're building a TikTok content creation tool.

**What to Extract**:
- Video Generator
- Frame Interpolation
- Platform Provider (TikTok)

**Project Structure**:

```
tiktok-video-creator/
├── tiktok_creator/
│   ├── __init__.py
│   ├── video_assembler.py   # Video assembly
│   ├── effects.py           # TikTok-specific effects
│   ├── publisher.py         # TikTok publishing
│   └── utils/
│       ├── audio.py
│       └── rendering.py
├── templates/
│   ├── trending/
│   └── educational/
├── cli/
│   └── create_video.py
├── tests/
├── requirements.txt
└── README.md
```

## Best Practices

### 1. Always Extract Interfaces

When extracting a component that depends on external services, **always extract the interface**:

```python
# ✅ Good: Extract interface + implementation
my_service/
├── interfaces/
│   └── llm_provider.py      # Abstract interface
└── providers/
    ├── openai_provider.py   # Concrete implementation
    └── mock_provider.py     # For testing
```

**Why**: Maintains SOLID principles and allows easy swapping of implementations.

### 2. Minimize Dependencies

Only include dependencies that are **absolutely necessary**:

```python
# ❌ Bad: Including unused dependencies
requirements.txt:
openai>=1.0.0
anthropic>=0.5.0
google-cloud-storage>=2.0.0
redis>=4.0.0
sqlalchemy>=2.0.0

# ✅ Good: Only what's needed
requirements.txt:
openai>=1.0.0
```

### 3. Make Configuration Explicit

Don't rely on hidden configuration files:

```python
# ❌ Bad: Hidden dependency on config file
class MyService:
    def __init__(self):
        # Assumes config.yaml exists!
        self.config = load_config("config.yaml")

# ✅ Good: Explicit configuration
class MyService:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
```

### 4. Keep Tests Lightweight

Extracted components should have **fast, isolated tests**:

```python
# ✅ Good: Fast, isolated test
def test_title_scorer():
    scorer = TitleScorer()
    score = scorer.score_title("Test Title")
    assert 0.0 <= score <= 1.0

# ❌ Bad: Slow, integration test
def test_title_generator():
    # Don't call real OpenAI API in unit tests!
    generator = TitleGenerator(OpenAIProvider(api_key="..."))
    title = generator.generate("topic")  # Slow and costs money
```

### 5. Document the Origin

Always mention where the code came from:

```python
"""
Title Scorer

Extracted from StoryGenerator project (https://github.com/Nomoos/StoryGenerator)
Original location: PrismQ/Pipeline/02_TextGeneration/StoryTitleScoring/

This component demonstrates SOLID principles through interface-based design.
"""
```

### 6. Version Independently

Give extracted components their own versioning:

```python
# setup.py or pyproject.toml
version = "1.0.0"  # Independent of StoryGenerator version
```

### 7. Provide Examples

Always include working examples:

```
examples/
├── basic_usage.py          # Simple example
├── advanced_usage.py       # Complex example
└── integration_example.py  # Integration example
```

## Troubleshooting

### Problem: Import Errors After Extraction

**Symptom**:
```python
ModuleNotFoundError: No module named 'PrismQ'
```

**Solution**: Update imports to relative or package-based:

```python
# Before (in StoryGenerator)
from PrismQ.Infrastructure.Core.Shared.validation import validate_string

# After (in extracted project)
from .validation import validate_string
# OR
from my_package.validation import validate_string
```

### Problem: Missing Dependencies

**Symptom**:
```python
ModuleNotFoundError: No module named 'openai'
```

**Solution**: Add to `requirements.txt`:

```bash
# Check what imports are used
grep -r "^import\|^from" my_package/ | grep -v "^from \."

# Add to requirements.txt
echo "openai>=1.0.0" >> requirements.txt
```

### Problem: Circular Dependencies

**Symptom**:
```python
ImportError: cannot import name 'X' from partially initialized module 'Y'
```

**Solution**: Restructure to eliminate cycles:

```python
# ❌ Bad: Circular dependency
# a.py
from .b import B

# b.py
from .a import A

# ✅ Good: Extract common interface
# interfaces.py
class IService(ABC):
    pass

# a.py
from .interfaces import IService

# b.py
from .interfaces import IService
```

### Problem: Complex Dependency Tree

**Symptom**: Component has many nested dependencies

**Solution**: Consider extracting a larger vertical slice or simplifying:

```python
# If dependency tree is:
# component.py
#   ├── service_a.py
#   │   ├── util_a.py
#   │   └── util_b.py
#   ├── service_b.py
#   │   ├── util_c.py
#   │   └── util_d.py
#   └── service_c.py

# Either extract all (vertical slice)
# OR simplify by inlining simple utilities
```

### Problem: Environment-Specific Code

**Symptom**: Code depends on specific environment setup

**Solution**: Make environment explicit:

```python
# ❌ Bad: Assumes specific environment
def load_model():
    return torch.load("/home/user/models/model.pt")  # Hard-coded path

# ✅ Good: Configurable
def load_model(model_path: str):
    return torch.load(model_path)
```

## Summary

### Extraction Checklist

- [ ] **Identify component** and its purpose
- [ ] **Map dependencies** and create dependency graph
- [ ] **Create project structure** with standard layout
- [ ] **Copy source files** and adapt imports
- [ ] **Extract interfaces** along with implementations
- [ ] **Minimize dependencies** - only include what's needed
- [ ] **Write tests** with good coverage
- [ ] **Document thoroughly** with README and examples
- [ ] **Verify independently** - can it run standalone?
- [ ] **Credit original source** in documentation

### Key Principles

1. **Interface First**: Always extract interfaces with implementations
2. **Minimal Dependencies**: Only include necessary dependencies
3. **Self-Contained**: Component should work without the original repo
4. **Well-Tested**: Include comprehensive tests
5. **Well-Documented**: Provide clear usage examples
6. **SOLID Compliant**: Maintain design principles in extraction

---

**Related Documentation**:
- [REPOSITORY_OVERVIEW.md](./REPOSITORY_OVERVIEW.md) - Full repository structure
- [SOLID_PRINCIPLES_IMPLEMENTATION.md](./SOLID_PRINCIPLES_IMPLEMENTATION.md) - SOLID examples
- [REFERENCE_GUIDE_FOR_SMALL_PROJECTS.md](./REFERENCE_GUIDE_FOR_SMALL_PROJECTS.md) - Quick reference

**Last Updated**: October 2025
