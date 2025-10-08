# Content: Source Attribution System

**ID:** `02-content-06-attribution`  
**Priority:** P1  
**Effort:** 1-2 hours  
**Status:** ✅ Completed

## Overview

Implements a comprehensive source attribution system that tracks and stores metadata about scraped content sources. This system ensures proper attribution, license tracking, and compliance with content usage policies. Attribution files are generated for each piece of content, containing source URLs, author information, license details, and usage rights.

## Dependencies

**Requires:**
- `02-content-01` - Reddit Scraper (provides content to attribute)

**Blocks:**
- Video metadata generation (needs attribution for compliance)
- Distribution stages (require source attribution for legal compliance)

## Acceptance Criteria

- [x] Attribution generator script implemented
- [x] JSON schema defined for attribution metadata
- [x] Automatic extraction from scraped content
- [x] Support for multiple source types (Reddit, Twitter, Quora)
- [x] License determination logic
- [x] Usage rights documentation
- [x] Comprehensive test suite (10 tests)
- [x] Documentation updated
- [x] Tests passing (100% pass rate)
- [x] Example attribution file provided

## Task Details

### Implementation

The attribution system is implemented in `scripts/generate_attribution.py` with the following features:

#### Core Functions

1. **License Determination**: Automatically determines appropriate license based on source type
2. **Usage Rights**: Documents usage rights and fair use justification
3. **Metadata Extraction**: Extracts attribution data from scraped content
4. **File Generation**: Creates individual attribution files per content item

#### Attribution Metadata Schema

```json
{
  "content_id": "string",           // Unique content identifier
  "source_url": "string",            // Full URL to original content
  "author": "string",                // Original author/creator
  "source_type": "string",           // 'reddit', 'twitter', 'quora', etc.
  "license": "string",               // License information
  "date_scraped": "ISO-8601",        // When content was scraped
  "usage_rights": "string",          // Usage rights description
  "attribution_generated": "ISO-8601", // When attribution was generated
  "subreddit": "string",             // (Optional) For Reddit sources
  "additional_info": {               // (Optional) Extra metadata
    "title": "string",
    "upvotes": number,
    "num_comments": number,
    "awards": number
  }
}
```

#### Usage Examples

**Process single scraped file:**
```bash
python3 scripts/generate_attribution.py \
  scraped_data.json \
  --output-dir src/Generator \
  --verbose
```

**Process directory of scraped files:**
```bash
python3 scripts/generate_attribution.py \
  src/Generator/sources/reddit/ \
  --output-dir src/Generator \
  --pattern "reddit_scraped_*.json" \
  --verbose
```

**Programmatic usage:**
```python
from scripts.generate_attribution import create_attribution_metadata, save_attribution_file

# Create attribution for a story
attribution = create_attribution_metadata(
    content_id="abc123",
    source_url="https://reddit.com/r/relationships/comments/abc123",
    author="throwaway_user",
    source_type="reddit",
    subreddit="relationships"
)

# Save to file
save_attribution_file(attribution, output_dir, "abc123")
```

### Testing

```bash
# Run all attribution tests
python3 tests/test_attribution.py

# Run with pytest (if available)
pytest tests/test_attribution.py -v
```

**Test Coverage:**
- License determination for different sources
- Usage rights generation
- Attribution metadata creation
- File saving and structure
- Reddit story processing
- Deleted author handling
- Date format validation
- Full workflow integration

## Output Files

**Location:** `Generator/sources/reddit/{gender}/{age_bucket}/`

**Files Created:**
- `attribution_{content_id}.json` - Attribution metadata for each content item
  - Contains: source_url, author, license, date_scraped, usage_rights
  - Format: JSON with proper UTF-8 encoding
  - Example: `attribution_abc123xyz.json`

**Example file:** `examples/attribution_example.json`

## Related Files

**Implementation:**
- `scripts/generate_attribution.py` - Main attribution generator script

**Tests:**
- `tests/test_attribution.py` - Comprehensive test suite (10 tests)

**Examples:**
- `examples/attribution_example.json` - Sample attribution file

**Documentation:**
- `docs/PIPELINE_OUTPUT_FILES.md` - Output file specifications

## Notes

### License Information
- **Reddit**: Content subject to Reddit User Agreement; used under Fair Use for transformative works
- **Twitter**: Subject to Twitter Terms of Service; Fair Use applies
- **Quora**: Subject to Quora Terms of Service; Fair Use applies

### Usage Rights
All content is used transformatively for creative storytelling purposes. Original attribution is preserved and sources are credited appropriately. This ensures:
- Legal compliance with platform terms
- Ethical content usage
- Transparency in content sourcing
- Proper credit to original creators

### Best Practices
1. Always generate attribution files immediately after scraping
2. Preserve attribution through the entire pipeline
3. Include attribution in final video metadata
4. Never modify or remove attribution data
5. Regularly audit attribution files for completeness

## Next Steps

After completion:
- **03-ideas-01**: Idea generation can now include attribution references
- **Video Metadata**: Attribution can be embedded in final videos
- **Distribution**: Compliance-ready content with proper attribution
- **Analytics**: Track which sources produce best-performing content
