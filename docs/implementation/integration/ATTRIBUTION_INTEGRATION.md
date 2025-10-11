# Attribution System Integration Guide

## Overview

This guide explains how the source attribution system integrates with the StoryGenerator pipeline and how to use it in your workflow.

## Pipeline Position

The attribution system is task **02-content-06-attribution** in the content pipeline:

```
02-content-01: Reddit Scraper
      ↓
02-content-02: Alternative Sources
      ↓
02-content-03: Quality Scorer
      ↓
02-content-04: Deduplication
      ↓
02-content-05: Ranking
      ↓
02-content-06: Attribution ← YOU ARE HERE
      ↓
03-ideas-01: Idea Generation
```

## Integration Points

### 1. After Content Scraping (Recommended)

Generate attribution immediately after scraping:

```bash
# Step 1: Scrape content
python3 scripts/reddit_scraper.py --segment women --age 18-23

# Step 2: Generate attribution
python3 scripts/generate_attribution.py \
  src/Generator/sources/reddit/women/18-23/reddit_scraped_*.json \
  --output-dir src/Generator \
  --verbose
```

### 2. Batch Processing Existing Content

Process all existing scraped content:

```bash
# Process all Reddit content
python3 scripts/generate_attribution.py \
  src/Generator/sources/reddit/ \
  --output-dir src/Generator \
  --pattern "reddit_scraped_*.json" \
  --verbose
```

### 3. Programmatic Integration

Integrate into your scraping script:

```python
from scripts.generate_attribution import process_reddit_story
from pathlib import Path

# After scraping a story
output_dir = Path("src/Generator")
attribution_file = process_reddit_story(
    story_data,
    gender="women",
    age_bucket="18-23",
    base_output_dir=output_dir
)

print(f"Attribution saved: {attribution_file}")
```

## Automated Pipeline Integration

### Option 1: Post-Scraping Hook

Add to your scraper script at the end:

```python
def scrape_and_attribute(gender: str, age: str):
    """Scrape content and generate attribution."""
    # Run scraper
    scraped_file = scrape_segment(reddit, gender, age)
    
    # Generate attribution
    from generate_attribution import process_scraped_content_file
    attribution_files = process_scraped_content_file(
        scraped_file,
        base_output_dir=Path("src/Generator"),
        verbose=True
    )
    
    print(f"Created {len(attribution_files)} attribution files")
    return scraped_file, attribution_files
```

### Option 2: Pipeline Orchestration

Use in a master pipeline script:

```python
#!/usr/bin/env python3
"""Complete content pipeline with attribution."""

from pathlib import Path
import subprocess

def run_content_pipeline():
    """Run the full content pipeline."""
    
    segments = [
        ("women", "10-13"),
        ("women", "14-17"),
        ("women", "18-23"),
        ("men", "10-13"),
        ("men", "14-17"),
        ("men", "18-23"),
    ]
    
    for gender, age in segments:
        print(f"\n{'='*60}")
        print(f"Processing: {gender}/{age}")
        print('='*60)
        
        # Step 1: Scrape
        print("\n1. Scraping content...")
        subprocess.run([
            "python3", "scripts/reddit_scraper.py",
            "--gender", gender,
            "--age", age
        ])
        
        # Step 2: Generate attribution
        print("\n2. Generating attribution...")
        subprocess.run([
            "python3", "scripts/generate_attribution.py",
            f"src/Generator/sources/reddit/{gender}/{age}/",
            "--output-dir", "src/Generator",
            "--verbose"
        ])
        
        # Step 3: Score quality
        print("\n3. Scoring quality...")
        # ... quality scorer ...
        
        # Step 4-6: Continue pipeline...

if __name__ == "__main__":
    run_content_pipeline()
```

## Directory Structure

After running attribution, your directory structure will look like:

```
src/Generator/
└── sources/
    └── reddit/
        ├── women/
        │   ├── 10-13/
        │   │   ├── reddit_scraped_women_10-13.json (from scraper)
        │   │   ├── attribution_abc123.json (generated)
        │   │   ├── attribution_def456.json (generated)
        │   │   └── attribution_ghi789.json (generated)
        │   ├── 14-17/
        │   └── 18-23/
        └── men/
            ├── 10-13/
            ├── 14-17/
            └── 18-23/
```

## Using Attribution Data

### In Video Metadata

Include attribution when creating video metadata:

```python
import json
from pathlib import Path

def create_video_metadata(content_id: str, gender: str, age: str):
    """Create video metadata with attribution."""
    
    # Load attribution
    attr_file = Path(f"src/Generator/sources/reddit/{gender}/{age}/attribution_{content_id}.json")
    with open(attr_file) as f:
        attribution = json.load(f)
    
    # Create video metadata
    metadata = {
        "title": "Story Title",
        "description": f"Story adapted from Reddit\n\nOriginal: {attribution['source_url']}",
        "attribution": {
            "source": attribution['source_type'],
            "author": attribution['author'],
            "license": attribution['license'],
            "original_url": attribution['source_url']
        }
    }
    
    return metadata
```

### In Distribution

Include attribution in upload metadata:

```python
def upload_with_attribution(video_file: Path, content_id: str):
    """Upload video with proper attribution."""
    
    # Load attribution
    attribution = load_attribution(content_id)
    
    # Add to description
    description = f"""
    {video_description}
    
    ---
    Source Attribution:
    Original content from: {attribution['source_url']}
    License: {attribution['license']}
    Usage Rights: {attribution['usage_rights']}
    """
    
    # Upload with attribution
    youtube.upload(
        video_file,
        title=title,
        description=description
    )
```

## Best Practices

### 1. Always Generate Immediately
Generate attribution right after scraping, while data is fresh.

### 2. Version Control Attribution
Keep attribution files in version control alongside source data.

### 3. Audit Regularly
Periodically verify all content has attribution:

```bash
# Check for content without attribution
python3 scripts/audit_attribution.py
```

### 4. Include in Backups
Ensure attribution files are included in your backup strategy.

### 5. Reference in Analytics
Track which sources produce best-performing content:

```python
def analyze_by_source():
    """Analyze performance by source."""
    for attr_file in Path("src/Generator/sources").rglob("attribution_*.json"):
        with open(attr_file) as f:
            attr = json.load(f)
        
        # Analyze performance metrics for this content
        subreddit = attr.get('subreddit')
        # ... track performance by subreddit ...
```

## Troubleshooting

### Attribution Files Not Created

**Problem**: Script completes but no files generated.

**Solution**: 
```bash
# Run with verbose flag to see errors
python3 scripts/generate_attribution.py input.json --verbose
```

### Missing Source Data

**Problem**: Attribution created but missing metadata.

**Solution**: Ensure scraped data includes all required fields:
- `id` (required)
- `url` (required)
- `author` (required)
- `subreddit` (recommended)
- `created_utc` (recommended)

### File Path Issues

**Problem**: Can't find generated attribution files.

**Solution**: Check the output directory structure:
```bash
ls -la src/Generator/sources/reddit/*/*/attribution_*.json
```

## Advanced Usage

### Custom Attribution Fields

Extend attribution metadata:

```python
from scripts.generate_attribution import create_attribution_metadata

attribution = create_attribution_metadata(
    content_id="abc123",
    source_url="https://reddit.com/...",
    author="user",
    additional_metadata={
        "title": "Story Title",
        "upvotes": 1000,
        "viral_score": 8.5,  # Custom field
        "target_audience": "women_18-23",  # Custom field
        "processing_stage": "ranked"  # Custom field
    }
)
```

### Bulk Attribution Updates

Update existing attribution files:

```python
from pathlib import Path
import json

def update_attribution_field(field_name: str, field_value: any):
    """Update a field in all attribution files."""
    for attr_file in Path("src/Generator/sources").rglob("attribution_*.json"):
        with open(attr_file, 'r+') as f:
            data = json.load(f)
            data[field_name] = field_value
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
```

## Support

For issues:
1. Check logs with `--verbose` flag
2. Review example files in `examples/`
3. Run test suite: `python3 tests/test_attribution.py`
4. See documentation: `issues/p0-critical/content-PrismQ/Pipeline/02-content-06-attribution/README.md`
