# Topic Generation with Validation Integration

## Overview

This document describes the integration of the MicrostepValidator system with the Topic Generator (Step 3 of the pipeline). This integration provides automatic progress tracking, configuration logging, artifact management, and validation for the topic generation process.

## Components

### 1. TopicGeneratorWithValidation

**Location:** `src/Python/Generators/GTopics.py`

A Python wrapper that integrates the topic generation process with the MicrostepValidator system. It provides:

- **Automatic Progress Tracking**: Logs start, progress, and completion
- **Configuration Logging**: Records all parameters used for reproducibility
- **Artifact Management**: Creates JSON topics file and summary text file
- **Validation**: Runs @copilot check to verify successful completion

### 2. Example Script

**Location:** `examples/topic_generation_with_validation.py`

Demonstrates 4 key usage patterns:
1. Single segment topic generation
2. Batch processing multiple segments
3. Detailed validation inspection
4. Custom configuration logging

## Quick Start

### Basic Usage

```python
from Generators.GTopics import TopicGeneratorWithValidation

generator = TopicGeneratorWithValidation()

# Generate topics from sample ideas
sample_ideas = [
    "A woman discovers a life-changing secret",
    "Two friends must make a difficult choice",
    # ... more ideas
]

result = generator.generate_topics_for_segment(
    gender="women",
    age="18-23",
    ideas_data=sample_ideas,
    min_topics=8,
    validate=True
)

if result["success"]:
    print(f"Generated {len(result['topics'])} topics")
    print(f"Topics file: {result['topics_file']}")
```

### Batch Processing

```python
# Process multiple segments at once
segments = [
    ("women", "18-23"),
    ("women", "24-29"),
    ("men", "18-23"),
    ("men", "24-29")
]

results = generator.batch_generate_topics(
    segments=segments,
    ideas_directory="/path/to/ideas",
    min_topics=8
)
```

### From Ideas File

```python
# Generate from existing markdown ideas file
result = generator.generate_topics_for_segment(
    gender="women",
    age="18-23",
    ideas_file="/path/to/ideas/women/18-23/20251007_ideas.md",
    min_topics=8
)
```

## Features

### Automatic Artifact Creation

For each topic generation, the following artifacts are created:

1. **Topics JSON File** (`YYYYMMDD_topics.json`)
   - Complete topic clusters with metadata
   - Includes idea assignments and viral potential scores
   
2. **Summary Text File** (`YYYYMMDD_topics_summary.txt`)
   - Human-readable summary of generated topics
   - Shows keywords, idea counts, and viral potential

3. **Configuration Log** (`config_topics_YYYYMMDD_HHMMSS.yaml`)
   - Records all parameters used
   - Enables reproducibility

4. **Progress Log** (`progress.md`)
   - Tracks generation lifecycle (started → completed)
   - Lists all artifacts created

5. **Validation Report** (`validation_report_YYYYMMDD_HHMMSS.json`)
   - Detailed validation results
   - Checks for folder existence, artifacts, config, and progress

### Progress Tracking

The system automatically tracks progress at key milestones:

```markdown
## 2025-10-07 20:36:38 - Step 3: topics - STARTED
**Description:** Classify and organize topics
**Target:** women/18-23
**Details:** Starting topic generation for women/18-23

---

## 2025-10-07 20:36:38 - Step 3: topics - COMPLETED
**Description:** Classify and organize topics
**Target:** women/18-23
**Details:** Generated 8 topics for women/18-23
**Artifacts Created:**
- config_topics_20251007_203638.yaml
- 20251007_topics.json
- 20251007_topics_summary.txt

---
```

### Validation

The `@copilot check` validation ensures:

✅ **Folder Exists**: Target directory is created
✅ **Has Artifacts**: Output files are present
✅ **Has Progress**: Progress.md is tracking execution
✅ **Has Config**: Configuration is logged

Example output:

```
============================================================
@copilot CHECK - Step 3: topics
============================================================

📁 Folder: /path/to/Generator/topics/women/18-23
📅 Timestamp: 2025-10-07T20:36:38

✅ Validation Checks:
  ✅ Folder Exists: True
  ✅ Has Artifacts: True
  ✅ Has Progress: True
  ✅ Has Config: True

📦 Artifacts (5):
  - 20251007_topics.json
  - 20251007_topics_summary.txt
  - config_topics_20251007_203638.yaml
  - progress.md
  - validation_report_20251007_203638.json

============================================================
Overall Status: ✅ VALID
============================================================
```

## Topic Generation Algorithm

The generator uses a keyword-based clustering approach:

1. **Extract Keywords**: Parse keywords from all ideas
2. **Generate Topic Names**: Age-appropriate topics for the segment
3. **Assign Ideas**: Match ideas to topics based on keyword overlap
4. **Balance Distribution**: Ensure all ideas are assigned
5. **Estimate Viral Potential**: Score topics based on emotional appeal

### Topic Names by Age Group

**18-23:**
- Romantic Relationships
- Career & Ambitions
- Friendship Dynamics
- Personal Independence
- Life Transitions
- Mental Health Journey
- Travel & Adventure
- Self-Care & Wellness
- Social Justice
- Finding Purpose

**24-29:**
- Career Success Stories
- Relationship Milestones
- Work-Life Balance
- Financial Independence
- Personal Growth
- Family Planning
- Friendship Evolution
- Health & Fitness
- Entrepreneurship
- Life Achievements

## Output Format

### Topics JSON Structure

```json
{
  "segment": {
    "gender": "women",
    "age": "18-23"
  },
  "topics": [
    {
      "id": "topic_001",
      "topicName": "Romantic Relationships",
      "description": "Stories about romantic relationships relevant to women aged 18-23",
      "keywords": ["relationships", "romantic", "love", "dating"],
      "ideaIds": ["idea_001", "idea_005", "idea_012"],
      "viralPotential": 85,
      "createdAt": "2025-10-07T20:36:38.142278"
    }
  ],
  "topicCount": 8,
  "generatedAt": "2025-10-07T20:36:38.142477",
  "minTopicsRequested": 8,
  "metadata": {
    "min_topics": 8,
    "clustering_method": "keyword-based",
    "generator": "TopicGenerator",
    "version": "1.0.0"
  }
}
```

### Summary Text Format

```
Topic Generation Summary
========================

Segment: women/18-23
Generated: 2025-10-07T20:36:38.142477
Total Topics: 8

Topics:
-------

1. Romantic Relationships
   Description: Stories about romantic relationships relevant to women aged 18-23
   Keywords: relationships, romantic, love, dating
   Ideas: 3 ideas
   Viral Potential: 85/100

2. Career & Ambitions
   Description: Stories about career & ambitions relevant to women aged 18-23
   Keywords: career, professional, work, ambitions
   Ideas: 2 ideas
   Viral Potential: 70/100

...
```

## Integration with Existing Pipeline

### Step 2 (Ideas) → Step 3 (Topics)

The topic generator can read ideas from the previous step:

```python
# Read ideas from Step 2 output
ideas_file = "src/Generator/ideas/women/18-23/20251007_ideas.md"

generator = TopicGeneratorWithValidation()
result = generator.generate_topics_for_segment(
    gender="women",
    age="18-23",
    ideas_file=ideas_file,
    min_topics=8
)
```

### Step 3 (Topics) → Step 4 (Titles)

The generated topics can be used for title generation:

```python
import json

# Load topics from Step 3
topics_file = "src/Generator/topics/women/18-23/20251007_topics.json"
with open(topics_file, 'r') as f:
    topics_data = json.load(f)

# Use topics for title generation
for topic in topics_data['topics']:
    # Generate titles for each topic
    generate_titles_for_topic(topic)
```

## API Reference

### TopicGeneratorWithValidation

#### `__init__(base_path=None, config_path=None)`

Initialize the generator with optional custom paths.

#### `generate_topics_for_segment(gender, age, ideas_file=None, ideas_data=None, min_topics=8, validate=True)`

Generate topics for a specific audience segment.

**Parameters:**
- `gender` (str): Target gender ('women', 'men')
- `age` (str): Target age group ('18-23', '24-29', etc.)
- `ideas_file` (str, optional): Path to markdown file with ideas
- `ideas_data` (list, optional): List of idea strings
- `min_topics` (int): Minimum topics to generate (default: 8)
- `validate` (bool): Run validation after generation (default: True)

**Returns:**
```python
{
    "success": bool,
    "topics_file": str,  # Path to generated JSON
    "topics": list,      # List of topic dictionaries
    "artifacts": list,   # List of created artifact filenames
    "validation_report": dict  # Validation results (if validate=True)
}
```

#### `batch_generate_topics(segments, ideas_directory, min_topics=8)`

Generate topics for multiple segments in batch.

**Parameters:**
- `segments` (list): List of (gender, age) tuples
- `ideas_directory` (str): Base directory containing idea files
- `min_topics` (int): Minimum topics per segment (default: 8)

**Returns:**
```python
{
    "women/18-23": {
        "success": True,
        "topics_file": "...",
        "topics": [...]
    },
    "women/24-29": {
        "success": True,
        "topics_file": "...",
        "topics": [...]
    }
}
```

## Error Handling

The generator handles errors gracefully and logs failures:

```python
try:
    result = generator.generate_topics_for_segment(
        gender="women",
        age="18-23",
        ideas_data=sample_ideas
    )
except Exception as e:
    # Error is logged to progress.md as "failed"
    # Validation report shows failure details
    print(f"Generation failed: {e}")
```

Failed runs are logged in progress.md:

```markdown
## 2025-10-07 20:36:38 - Step 3: topics - FAILED
**Description:** Classify and organize topics
**Target:** women/18-23
**Details:** Error generating topics: No ideas provided
```

## Testing

### Run Unit Tests

```bash
python tests/test_microstep_validator.py
```

### Run Examples

```bash
python examples/topic_generation_with_validation.py
```

### Manual Testing

```bash
cd /home/runner/work/StoryGenerator/StoryGenerator
python src/Python/Generators/GTopics.py
```

## File Locations

```
StoryGenerator/
├── src/
│   └── Python/
│       ├── Generators/
│       │   └── GTopics.py              # Topic generator with validation
│       └── Tools/
│           └── MicrostepValidator.py   # Validation system
├── examples/
│   └── topic_generation_with_validation.py  # Example usage
├── tests/
│   └── test_microstep_validator.py     # Validation tests
└── src/Generator/
    └── topics/                         # Generated topics
        ├── women/
        │   ├── 18-23/
        │   │   ├── 20251007_topics.json
        │   │   ├── 20251007_topics_summary.txt
        │   │   ├── config_topics_20251007_203638.yaml
        │   │   ├── progress.md
        │   │   └── validation_report_20251007_203638.json
        │   └── 24-29/
        └── men/
            ├── 18-23/
            └── 24-29/
```

## Best Practices

1. **Always validate after generation**
   ```python
   result = generator.generate_topics_for_segment(..., validate=True)
   ```

2. **Check validation reports**
   ```python
   if result["validation_report"]["is_valid"]:
       print("✅ Topics validated successfully")
   ```

3. **Use batch processing for multiple segments**
   ```python
   results = generator.batch_generate_topics(segments, ideas_dir)
   ```

4. **Review progress logs regularly**
   ```bash
   cat src/Generator/topics/women/18-23/progress.md
   ```

5. **Preserve configuration logs for reproducibility**
   - Never delete config_*.yaml files
   - Use them to reproduce exact results

## Troubleshooting

### Issue: No topics generated

**Solution:** Check that ideas are provided and min_topics is <= available topics

### Issue: Validation fails

**Solution:** Check validation report for specific failures:
```python
report = result["validation_report"]
print(report["checks"])
```

### Issue: Ideas not properly distributed

**Solution:** Ensure min_topics is appropriate for the number of ideas (typically 8-10 topics for 20+ ideas)

## See Also

- [MICROSTEP_VALIDATION.md](MICROSTEP_VALIDATION.md) - Complete validation system documentation
- [MICROSTEP_VALIDATION_QUICKSTART.md](MICROSTEP_VALIDATION_QUICKSTART.md) - Quick reference
- [GENERATOR_STRUCTURE.md](GENERATOR_STRUCTURE.md) - Pipeline structure overview
- [src/CSharp/Generators/TopicGenerator.cs](../src/CSharp/Generators/TopicGenerator.cs) - C# implementation
