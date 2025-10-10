# Alternative Content Source Scrapers (Enhanced v2.0)

This directory contains scrapers for alternative content sources beyond Reddit, designed to gather story content for the StoryGenerator pipeline.

## Available Scrapers

### 1. Quora Scraper
Scrapes questions and answers from Quora based on demographic-specific topics.

**Features:**
- Searches for trending questions
- Extracts top answers
- Filters by engagement metrics
- Age-appropriate content filtering

**Output:** `src/Generator/sources/quora/{gender}/{age}/YYYYMMDD_quora_content.json`

### 2. Twitter/X Scraper
Scrapes story threads from Twitter/X that contain narrative content.

**Features:**
- Finds viral story threads
- Extracts full thread content
- Tracks engagement metrics
- Thread detection (🧵 emoji, "thread" keywords)

**Output:** `src/Generator/sources/twitter/{gender}/{age}/YYYYMMDD_twitter_content.json`

### 3. Instagram Scraper 🆕
Scrapes Instagram stories/posts from hashtags and accounts on specific topics.

**Features:**
- Searches trending hashtags
- Extracts post captions and stories
- Tracks engagement (likes, comments, views)
- Mock data implementation for testing
- Age-specific hashtag targeting

**Output:** `src/Generator/sources/instagram/{gender}/{age}/YYYYMMDD_instagram_content.json`

**Dependencies:** `pip install instagrapi` (optional, uses mock data by default)

### 4. TikTok Scraper 🆕
Scrapes TikTok video descriptions and captions on specific topics.

**Features:**
- Searches trending hashtags
- Extracts video descriptions/captions
- Tracks engagement (likes, comments, shares, views)
- Mock data implementation for testing
- Age-specific hashtag targeting

**Output:** `src/Generator/sources/tiktok/{gender}/{age}/YYYYMMDD_tiktok_content.json`

**Dependencies:** `pip install TikTokApi` (optional, uses mock data by default)

## Quick Start

### Basic Usage

```bash
# Scrape Quora for women aged 18-23
python alt_sources_scraper.py --sources quora --gender women --age 18-23

# Scrape Instagram and TikTok for men aged 14-17
python alt_sources_scraper.py --sources instagram,tiktok --gender men --age 14-17

# Scrape all sources for all demographics
python alt_sources_scraper.py --sources all --all-demographics

# Run individual scrapers
python instagram_scraper.py  # Scrapes all demographics with mock data
python tiktok_scraper.py     # Scrapes all demographics with mock data
```

### Python API

```python
from quora_scraper import QuoraScraper
from twitter_scraper import TwitterScraper
from instagram_scraper import InstagramScraper
from tiktok_scraper import TikTokScraper

# Initialize scraper (Instagram/TikTok use mock data by default)
scraper = InstagramScraper(use_mock=True)

# Scrape content
result = scraper.run(
    topic="relationships",
    gender="women",
    age_bucket="18-23",
    limit=50
)

print(f"Scraped {result['filtered']} items")
print(f"Saved to: {result['output_file']}")
```

## Command-Line Options

```
python alt_sources_scraper.py [OPTIONS]

Options:
  --sources TEXT              Comma-separated sources (quora,twitter,instagram,tiktok,all)
  --gender [men|women]        Target gender
  --age [10-13|14-17|18-23]   Target age bucket
  --all-demographics          Scrape all gender/age combinations
  --topic TEXT                Topic or keywords (default: "life stories")
  --limit INT                 Max items per source (default: 50)
  --delay FLOAT               Delay between requests in seconds (default: 2.0)
  --help                      Show help message
```

## Examples

### Single Demographic
```bash
python alt_sources_scraper.py \
  --sources quora,twitter,instagram,tiktok \
  --gender women \
  --age 18-23 \
  --topic "relationships" \
  --limit 100
```

### All Demographics (Batch)
```bash
python alt_sources_scraper.py \
  --sources all \
  --all-demographics \
  --limit 50 \
  --delay 3
```

### Instagram Only
```bash
python alt_sources_scraper.py \
  --sources instagram \
  --gender men \
  --age 14-17 \
  --topic "gaming" \
  --limit 30
```

### TikTok Only
```bash
python alt_sources_scraper.py \
  --sources tiktok \
  --gender women \
  --age 18-23 \
  --topic "college life" \
  --limit 40
```

### Custom Topic
```bash
python alt_sources_scraper.py \
  --sources twitter \
  --gender men \
  --age 14-17 \
  --topic "gaming" \
  --limit 30
```

## Implementation Notes

### Current Status: Mock Data
The scrapers currently use **mock data** for demonstration and testing purposes. This allows:
- Development without API credentials
- Consistent testing
- Understanding of data structures
- Integration with downstream pipeline stages

### Production Implementation

To implement actual scraping:

#### Quora
1. Install dependencies: `pip install beautifulsoup4 requests`
2. Update `_search_quora()` method with actual web scraping
3. Implement rate limiting and error handling
4. Consider using Quora's official API if available

**Challenges:**
- Quora has anti-scraping measures
- May require rotating proxies or user agents
- Rate limiting is essential
- Alternative: Use Quora Spaces API (if accessible)

#### Twitter/X
1. Install dependencies: `pip install tweepy`
2. Get Twitter API credentials:
   - Apply for Twitter Developer Account
   - Create an app and get Bearer Token
3. Set environment variable: `export TWITTER_BEARER_TOKEN="your_token"`
4. Update `_search_threads()` to use Twitter API v2

**API Endpoints:**
- Search tweets: `/2/tweets/search/recent`
- Get conversation thread: Using `conversation_id` field
- Rate limits: 300 requests per 15-minute window

## Architecture

```
base_scraper.py          # Abstract base class
    │
    ├── quora_scraper.py     # Quora implementation
    │
    └── twitter_scraper.py   # Twitter implementation

alt_sources_scraper.py   # Unified CLI interface
```

### Base Scraper Features
- Abstract interface for consistency
- Age-appropriate content filtering
- Automatic file saving with timestamps
- Result tracking and statistics

### Filtering System
Age-appropriate filtering based on keyword detection:
- **10-13**: Strict filtering (explicit, violence, etc.)
- **14-17**: Moderate filtering (explicit content)
- **18-23**: Minimal filtering

## Testing

Run the test suite:
```bash
cd /home/runner/work/StoryGenerator/StoryGenerator
python tests/test_alt_sources.py
```

**Test Coverage:**
- ✅ Base scraper abstract interface
- ✅ Quora scraper initialization and scraping
- ✅ Twitter scraper initialization and scraping
- ✅ Content structure validation
- ✅ Age-appropriate filtering
- ✅ File saving and JSON structure
- ✅ Demographic variations

## Output Format

All scrapers produce JSON files with this structure:

```json
{
  "source": "quora|twitter",
  "gender": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "total_items": 50,
  "scraped_at": "2025-10-08T19:42:35.123456",
  "content": [
    {
      "id": "unique_id",
      "title": "Content title",
      "url": "https://...",
      "source": "quora|twitter",
      // ... source-specific fields
    }
  ]
}
```

## Adding New Sources

To add a new content source:

1. Create `new_source_scraper.py`
2. Inherit from `BaseScraper`
3. Implement `scrape_content()` method
4. Add to `alt_sources_scraper.py`
5. Update tests

Example:
```python
from base_scraper import BaseScraper

class NewSourceScraper(BaseScraper):
    def __init__(self):
        super().__init__("newsource")
    
    def scrape_content(self, topic, gender, age_bucket, limit):
        # Your scraping logic here
        return content_items
```

## Best Practices

1. **Rate Limiting**: Always respect rate limits and add delays
2. **Error Handling**: Catch and log exceptions gracefully
3. **Authentication**: Store API keys in environment variables
4. **Privacy**: Follow GDPR and data privacy regulations
5. **Caching**: Cache responses to minimize API calls
6. **Logging**: Log activities for debugging and monitoring

## Troubleshooting

### Import Errors
Make sure you're in the `scripts/scrapers` directory or add it to PYTHONPATH:
```bash
export PYTHONPATH=/home/runner/work/StoryGenerator/StoryGenerator/scripts/scrapers:$PYTHONPATH
```

### Missing Dependencies
Install required packages:
```bash
pip install beautifulsoup4 tweepy requests
```

### API Authentication
For production use, set up environment variables:
```bash
export TWITTER_BEARER_TOKEN="your_token"
export QUORA_API_KEY="your_key"  # if applicable
```

## Future Enhancements

- [ ] Add Medium article scraper
- [ ] Add Tumblr story scraper
- [ ] Implement actual Quora scraping
- [ ] Implement actual Twitter API integration
- [ ] Add proxy support for web scraping
- [ ] Implement caching layer
- [ ] Add retry logic with exponential backoff
- [ ] Create scraper scheduler for automated runs
- [ ] Add metrics and monitoring

## License & Legal

When scraping content:
- Always respect `robots.txt`
- Follow terms of service for each platform
- Attribute content to original sources
- Consider copyright and fair use
- Respect rate limits and be a good citizen

## Support

For questions or issues:
1. Check test output: `python tests/test_alt_sources.py`
2. Review logs for error messages
3. Consult source-specific documentation
4. Check API status pages (Twitter, etc.)
