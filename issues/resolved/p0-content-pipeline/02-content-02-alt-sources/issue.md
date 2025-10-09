# Content: Alternative Sources (Quora, Twitter, etc.)

**ID:** `02-content-02-alt-sources`  
**Priority:** P1  
**Effort:** 6-8 hours  
**Status:** Completed

## Overview

Implements alternative content source scrapers (Quora and Twitter) to gather story content beyond Reddit. These scrapers provide a base implementation with mock data that can be extended to use actual APIs when credentials are available.

The implementation includes:
- Base scraper interface for consistency across sources
- Quora scraper for questions and answers
- Twitter/X scraper for story threads
- Age-appropriate content filtering
- JSON output with structured data
- Unified CLI interface for batch scraping

## Dependencies

**Requires:**
- `00-setup-01` - Folder structure (✅ sources directory created)
- `00-setup-02` - Config files (Optional: API credentials for production use)

**Blocks:**
- `02-content-03`: Quality scorer (can now score alternative source content)
- `03-ideas-01`: Content adaptation (can adapt from multiple sources)

## Acceptance Criteria

- [x] Base scraper interface implemented
- [x] Quora scraper implemented with mock data
- [x] Twitter scraper implemented with mock data  
- [x] Age-appropriate content filtering
- [x] JSON output files created in correct directory structure
- [x] Documentation updated
- [x] Tests passing (5/5 tests passed)
- [x] Example scripts for usage

## Task Details

### Implementation

The implementation consists of three main components:

1. **BaseScraper** (`scripts/scrapers/base_scraper.py`)
   - Abstract base class defining common interface
   - Age-appropriate filtering
   - JSON file saving with proper structure
   - Run pipeline orchestration

2. **QuoraScraper** (`scripts/scrapers/quora_scraper.py`)
   - Scrapes Quora questions and answers
   - Currently uses mock data (production would use BeautifulSoup4 or API)
   - Generates demographic-appropriate search terms
   - Output: `quora_question_{id}.json`

3. **TwitterScraper** (`scripts/scrapers/twitter_scraper.py`)
   - Scrapes Twitter/X story threads
   - Currently uses mock data (production would use tweepy/Twitter API v2)
   - Focuses on narrative threads
   - Output: `twitter_thread_{id}.json`

4. **Unified CLI** (`scripts/scrapers/alt_sources_scraper.py`)
   - Single entry point for all sources
   - Batch processing support
   - Configurable demographics and topics
   - Progress reporting

### JSON Output Schema

**Quora Questions:**
```json
{
  "source": "quora",
  "gender": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "total_items": 50,
  "scraped_at": "2025-10-08T19:42:35",
  "content": [
    {
      "id": "quora_123",
      "title": "Question title",
      "url": "https://www.quora.com/...",
      "question_text": "Full question text",
      "views": 10000,
      "followers": 50,
      "answers_count": 5,
      "top_answer": {
        "text": "Answer text...",
        "author": "Expert_1",
        "upvotes": 100
      },
      "created_at": "2025-10-08T...",
      "source": "quora"
    }
  ]
}
```

**Twitter Threads:**
```json
{
  "source": "twitter",
  "gender": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "total_items": 50,
  "scraped_at": "2025-10-08T19:43:31",
  "content": [
    {
      "id": "twitter_456",
      "thread_id": "thread_123",
      "title": "Thread title",
      "url": "https://twitter.com/user/status/123",
      "author": "@username",
      "author_followers": 10000,
      "created_at": "2025-10-08T...",
      "tweets_count": 8,
      "first_tweet": "🧵 THREAD: ...",
      "full_thread": ["Tweet 1...", "Tweet 2..."],
      "engagement": {
        "likes": 1000,
        "retweets": 200,
        "replies": 100,
        "views": 50000
      },
      "hashtags": ["#thread", "#story"],
      "source": "twitter"
    }
  ]
}
```

### Testing

```bash
# Run all tests
cd /home/runner/work/StoryGenerator/StoryGenerator
python tests/test_alt_sources.py

# Test single source and demographic
cd scripts/scrapers
python alt_sources_scraper.py --sources quora --gender women --age 18-23

# Test all sources for all demographics
python alt_sources_scraper.py --sources all --all-demographics

# Test with custom topic and limit
python alt_sources_scraper.py --sources twitter --gender men --age 14-17 --topic gaming --limit 20
```

### Usage Examples

**Basic Usage:**
```python
from scripts.scrapers.quora_scraper import QuoraScraper

scraper = QuoraScraper()
result = scraper.run("relationships", "women", "18-23", limit=50)
print(f"Scraped {result['filtered']} items to {result['output_file']}")
```

**Batch Processing:**
```bash
# Scrape all sources for all demographics
python scripts/scrapers/alt_sources_scraper.py --sources all --all-demographics --limit 50
```

## Output Files

- `src/Generator/sources/quora/{gender}/{age_bucket}/YYYYMMDD_quora_content.json` - Quora questions and answers
- `src/Generator/sources/twitter/{gender}/{age_bucket}/YYYYMMDD_twitter_content.json` - Twitter story threads
- 12 files total (2 sources × 2 genders × 3 age buckets)

## Related Files

- `/scripts/scrapers/base_scraper.py` - Base scraper interface
- `/scripts/scrapers/quora_scraper.py` - Quora implementation
- `/scripts/scrapers/twitter_scraper.py` - Twitter implementation
- `/scripts/scrapers/alt_sources_scraper.py` - Unified CLI
- `/tests/test_alt_sources.py` - Test suite
- `/requirements.txt` - Updated with beautifulsoup4, tweepy
- `/docs/PIPELINE_OUTPUT_FILES.md` - Output documentation

## Notes

### Current Implementation (Mock Data)
- The scrapers currently generate mock data for demonstration
- This allows development and testing without API credentials
- Mock data follows the expected schema for real implementations

### Production Considerations
When implementing actual scraping:

**Quora:**
- Use BeautifulSoup4 for web scraping OR official API if available
- Implement rate limiting (respect robots.txt)
- Handle anti-scraping measures (rotate user agents, delays)
- Consider using Quora Spaces API if accessible

**Twitter/X:**
- Requires Twitter API v2 credentials (Bearer Token)
- Use tweepy library for API access
- Rate limits: 300 requests per 15-min window (varies by endpoint)
- Focused on conversation threads (conversation_id field)
- Consider Twitter Premium/Enterprise API for higher limits

**General:**
- Store API credentials in environment variables or config files
- Implement proper error handling and retries
- Log scraping activities for debugging
- Consider GDPR and data privacy regulations
- Cache responses to minimize API calls

## Next Steps

After completion:
- Content available for quality scoring (`02-content-03`)
- Can be used alongside Reddit content for idea generation
- Consider adding more sources (Medium, Tumblr, etc.)
- Implement actual API integration when credentials available
