# Source Attribution System

## Overview

The Source Attribution System is a critical component of the StoryGenerator pipeline that tracks and stores metadata about content sources. This ensures legal compliance, ethical content usage, and transparency in content sourcing.

## Purpose

- **Legal Compliance**: Track sources for proper attribution and fair use
- **Transparency**: Document content origins and usage rights
- **Credit**: Properly attribute original creators
- **Auditing**: Enable content source tracking and verification

## Features

### Automatic Attribution Generation
- Extracts metadata from scraped content automatically
- Creates individual attribution files for each content item
- Supports multiple source types (Reddit, Twitter, Quora, etc.)

### License Management
- Automatically determines appropriate licenses based on source
- Documents fair use justification
- Tracks usage rights and restrictions

### Metadata Tracking
- Source URLs and permalinks
- Author/creator information
- Scraping timestamps
- Content metrics (upvotes, comments, awards)

## Quick Start

### Basic Usage

Generate attribution for a scraped content file:

```bash
python3 scripts/generate_attribution.py scraped_data.json
```

Process an entire directory:

```bash
python3 scripts/generate_attribution.py src/Generator/sources/reddit/ \
  --pattern "reddit_scraped_*.json" \
  --verbose
```

### Programmatic Usage

```python
from scripts.generate_attribution import (
    create_attribution_metadata,
    save_attribution_file,
    process_reddit_story
)

# Create attribution metadata
attribution = create_attribution_metadata(
    content_id="abc123",
    source_url="https://reddit.com/r/relationships/comments/abc123",
    author="throwaway_user",
    source_type="reddit",
    subreddit="relationships"
)

# Save to file
output_dir = Path("src/Generator")
filepath = save_attribution_file(attribution, output_dir, "abc123")
print(f"Attribution saved to: {filepath}")
```

## Attribution File Schema

Each attribution file contains:

```json
{
  "content_id": "abc123xyz",
  "source_url": "https://reddit.com/r/relationships/comments/abc123xyz/title",
  "author": "throwaway_user123",
  "source_type": "reddit",
  "license": "Reddit User Agreement - Fair Use for Transformative Works",
  "date_scraped": "2024-01-15T10:30:00Z",
  "usage_rights": "Transformative use for creative storytelling. Original attribution preserved.",
  "attribution_generated": "2024-01-15T10:35:00Z",
  "subreddit": "relationships",
  "additional_info": {
    "title": "Story Title",
    "upvotes": 1250,
    "num_comments": 340,
    "awards": 5
  }
}
```

## File Organization

Attribution files are stored in the following structure:

```
Generator/sources/{source_type}/{gender}/{age_bucket}/
└── attribution_{content_id}.json
```

Example:
```
Generator/sources/reddit/women/18-23/
├── attribution_abc123.json
├── attribution_def456.json
└── attribution_ghi789.json
```

## Command-Line Options

```
usage: generate_attribution.py [-h] [--output-dir OUTPUT_DIR] 
                                [--pattern PATTERN] [-v] input

positional arguments:
  input                 Input file or directory containing scraped content

optional arguments:
  -h, --help            Show help message
  --output-dir DIR      Base output directory (default: src/Generator)
  --pattern PATTERN     File pattern for directory processing
                        (default: reddit_scraped_*.json)
  -v, --verbose         Enable verbose output
```

## Testing

Run the test suite:

```bash
# Run all attribution tests
python3 tests/test_attribution.py

# Or with pytest
pytest tests/test_attribution.py -v
```

The test suite includes:
- License determination tests
- Usage rights generation tests
- Metadata creation tests
- File I/O tests
- Integration tests
- Edge case handling

## License Information

### Reddit Content
- **License**: Reddit User Agreement
- **Usage**: Fair Use for Transformative Works
- **Rights**: Transformative use for creative storytelling with attribution

### Twitter Content
- **License**: Twitter Terms of Service
- **Usage**: Fair Use
- **Rights**: Transformative use with original source credited

### Quora Content
- **License**: Quora Terms of Service
- **Usage**: Fair Use
- **Rights**: Transformative use for educational and entertainment purposes

## Best Practices

1. **Generate Immediately**: Create attribution files right after scraping content
2. **Preserve Throughout Pipeline**: Maintain attribution through all processing stages
3. **Include in Final Metadata**: Embed attribution in final video metadata
4. **Never Modify**: Don't alter or remove attribution data
5. **Regular Audits**: Periodically verify attribution completeness

## Integration with Pipeline

The attribution system integrates with:

1. **Reddit Scraper** (02-content-01): Primary input source
2. **Alternative Sources** (02-content-02): Other content sources
3. **Idea Generation**: References attribution for context
4. **Video Metadata**: Embeds attribution in final videos
5. **Distribution**: Ensures compliance-ready content

## Troubleshooting

### Common Issues

**Attribution files not created:**
- Check input file format matches expected schema
- Verify output directory permissions
- Enable verbose mode for detailed error messages

**Missing metadata:**
- Ensure scraped content includes required fields (id, url, author)
- Check for malformed JSON in input files

**Incorrect file paths:**
- Verify gender and age_bucket values in scraped data
- Check output-dir parameter is correct

## Examples

See `examples/attribution_example.json` for a complete sample attribution file.

## API Reference

### Functions

#### `create_attribution_metadata()`
Creates attribution metadata dictionary.

**Parameters:**
- `content_id` (str): Unique identifier for the content
- `source_url` (str): Full URL to the original content
- `author` (str): Author/creator of the original content
- `source_type` (str): Type of source (default: 'reddit')
- `subreddit` (str, optional): Subreddit name for Reddit sources
- `scraped_date` (str, optional): ISO-8601 formatted date
- `additional_metadata` (dict, optional): Extra metadata to include

**Returns:** Dictionary containing attribution metadata

#### `save_attribution_file()`
Saves attribution metadata to a JSON file.

**Parameters:**
- `attribution_data` (dict): Attribution metadata dictionary
- `output_dir` (Path): Directory where file should be saved
- `content_id` (str): Unique identifier for the content

**Returns:** Path to the saved attribution file

#### `process_reddit_story()`
Processes a Reddit story and generates its attribution file.

**Parameters:**
- `story` (dict): Dictionary containing story data
- `gender` (str): Target gender segment
- `age_bucket` (str): Target age bucket
- `base_output_dir` (Path): Base directory for output files

**Returns:** Path to the created attribution file

## Support

For issues or questions:
1. Check this documentation
2. Review examples in `examples/` directory
3. Run test suite to verify setup
4. Check related issue: `issues/p0-critical/content-pipeline/02-content-06-attribution/`

## Related Documentation

- [Pipeline Output Files](../../docs/PIPELINE_OUTPUT_FILES.md)
- [Content Pipeline Overview](../../issues/p0-critical/content-pipeline/README.md)
- [Reddit Scraper](../../issues/p0-critical/content-pipeline/02-content-01-reddit-scraper/)
