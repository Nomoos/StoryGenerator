# Reddit Story Scraper (Enhanced)

## Overview

The Enhanced Reddit Story Scraper (`reddit_scraper.py`) mines high-quality stories from target subreddits, filtered by audience segment (gender) and age demographics. Version 2.0 adds incremental scraping, persistent duplicate tracking, and advanced rate limiting for production use.

## Features

### Core Features
- ✅ **Demographic Targeting**: Scrapes content for 6 segments (women/men × 10-13/14-17/18-23)
- ✅ **Quality Filtering**: Configurable thresholds per age group (upvotes, comments, text length)
- ✅ **Age Appropriateness**: Keyword-based filtering for younger audiences
- ✅ **Rich Metadata**: Captures upvotes, comments, awards, and top comment context
- ✅ **JSON Output**: Structured data ready for downstream processing

### ✨ Enhanced Features (v2.0)
- ✅ **Incremental Scraping**: Only fetch new posts since last run (saves API calls)
- ✅ **Persistent Duplicate Tracking**: SQLite database tracks seen posts across scrapes
- ✅ **Exponential Backoff**: Automatic retry with exponential backoff on rate limits
- ✅ **Configurable Thresholds**: Different quality bars for each age demographic
- ✅ **Flexible CLI**: Command-line options for single segments or full scrapes
- ✅ **Detailed Statistics**: Track duplicates, filtering stats, and scrape metrics

## Prerequisites

### 1. Install PRAW Library

```bash
pip install praw==7.8.1
```

### 2. Get Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - **Name**: StoryGenerator
   - **App type**: Select "script"
   - **Description**: Story mining for content generation
   - **About URL**: (leave blank)
   - **Redirect URI**: http://localhost:8080
4. Click "Create app"
5. Note your credentials:
   - **Client ID**: The string under "personal use script"
   - **Client Secret**: The secret key shown

### 3. Set Environment Variables

**Linux/Mac:**
```bash
export REDDIT_CLIENT_ID="your_client_id_here"
export REDDIT_CLIENT_SECRET="your_secret_here"
```

**Windows (Command Prompt):**
```cmd
set REDDIT_CLIENT_ID=your_client_id_here
set REDDIT_CLIENT_SECRET=your_secret_here
```

**Windows (PowerShell):**
```powershell
$env:REDDIT_CLIENT_ID="your_client_id_here"
$env:REDDIT_CLIENT_SECRET="your_secret_here"
```

**Or create a `.env` file:**
```bash
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_secret_here
```

## Usage

### Basic Usage

Run the scraper for all segments (with incremental mode and duplicate tracking enabled by default):

```bash
python3 scripts/reddit_scraper.py
```

This will:
1. Check last scrape time for each subreddit (incremental mode)
2. Scrape only new stories from all 18 target subreddits (3 per segment)
3. Filter by age-appropriate quality thresholds and content keywords
4. Skip duplicate posts (tracked in SQLite database)
5. Save top 100 stories per segment to JSON files
6. Output files to `Generator/sources/reddit/{gender}/{age}/YYYYMMDD_reddit_stories.json`

### Advanced Usage

#### Scrape a Single Segment

```bash
# Scrape only women/18-23
python3 scripts/reddit_scraper.py --segment women --age 18-23
```

#### Force Full Scrape (Disable Incremental Mode)

```bash
# Get all top posts from last week, not just new ones
python3 scripts/reddit_scraper.py --force-full
# Or equivalently:
python3 scripts/reddit_scraper.py --no-incremental
```

#### Disable Duplicate Tracking

```bash
# Don't check for duplicates (useful for testing)
python3 scripts/reddit_scraper.py --no-dedup
```

#### Combine Options

```bash
# Full scrape of single segment without dedup
python3 scripts/reddit_scraper.py --segment men --age 14-17 --force-full --no-dedup
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `--segment SEGMENT` | Target specific gender (e.g., 'women', 'men') |
| `--age AGE` | Target specific age (e.g., '10-13', '14-17', '18-23') |
| `--no-incremental` | Disable incremental scraping (fetch all top posts) |
| `--no-dedup` | Disable duplicate tracking |
| `--force-full` | Alias for --no-incremental |
| `--help` | Show help message and exit |

### Target Subreddits

The scraper uses predefined subreddit mappings:

| Segment | Age Range | Subreddits |
|---------|-----------|------------|
| Women | 10-13 | r/TrueOffMyChest, r/relationships, r/AmItheAsshole |
| Women | 14-17 | r/teenagers, r/AmItheAsshole, r/TrueOffMyChest |
| Women | 18-23 | r/relationships, r/dating_advice, r/confession |
| Men | 10-13 | r/teenagers, r/stories, r/confession |
| Men | 14-17 | r/teenagers, r/confession, r/TrueOffMyChest |
| Men | 18-23 | r/relationships, r/AskMen, r/confession |

## Output Format

Each segment gets a JSON file with this structure (enhanced fields marked with 🆕):

```json
{
  "segment": "women",
  "age_bucket": "18-23",
  "subreddits": ["r/relationships", "r/dating_advice", "r/confession"],
  "quality_thresholds": {
    "min_upvotes": 500,
    "min_comments": 40,
    "min_text_length": 200
  },
  "total_scraped": 250,
  "after_filtering": 180,
  "selected": 100,
  "scraped_at": "2024-01-15T10:30:00",
  "incremental_mode": true,
  "duplicate_tracking": true,
  "duplicate_stats": {
    "total_seen": 1523,
    "avg_scrapes": 1.8
  },
  "stories": [
    {
      "id": "abc123",
      "title": "Story title",
      "text": "Full story text...",
      "url": "https://reddit.com/r/...",
      "upvotes": 1250,
      "num_comments": 340,
      "created_utc": "2024-01-10T15:20:00",
      "created_utc_timestamp": 1704892800.0,
      "subreddit": "r/relationships",
      "author": "username",
      "awards": 5,
      "is_self": true,
      "top_comments": [
        {"text": "Comment text", "score": 450}
      ]
    }
  ]
}
```

## Enhanced Features Detail

### Incremental Scraping

The scraper maintains state in `data/reddit_scraper_state.json`:

```json
{
  "r/relationships": 1704892800.0,
  "r/dating_advice": 1704889200.0,
  "r/confession": 1704895400.0
}
```

On subsequent runs:
- Only fetches posts newer than the stored timestamp
- Significantly reduces API usage
- Faster execution for regular scrapes
- Automatically updates timestamps after each successful scrape

### Duplicate Tracking

The scraper uses SQLite database at `data/reddit_scraper_duplicates.db` to track:
- Post IDs seen across all scrapes
- First seen timestamp
- Number of times encountered
- Original title and subreddit

Benefits:
- Prevents re-processing the same stories
- Works across multiple scrape sessions
- Provides statistics on duplicate rate
- Helps identify frequently reposted content

### Quality Thresholds

Different age demographics have different thresholds:

| Age Group | Min Upvotes | Min Comments | Min Text Length |
|-----------|-------------|--------------|-----------------|
| 10-13 | 300 | 20 | 100 chars |
| 14-17 | 400 | 30 | 150 chars |
| 18-23 | 500 | 40 | 200 chars |

This ensures:
- More engaging content for each demographic
- Age-appropriate complexity
- Better quality stories for production use

## Age Filtering

The scraper implements keyword-based filtering for age-appropriateness:

- **10-13**: Filters out content with keywords: "sex", "drugs", "violence", "nsfw", "explicit"
- **14-17**: Filters out content with keywords: "explicit", "nsfw"
- **18-23**: No filtering (adult content allowed)

> **Note**: This is basic filtering. For production, consider integrating ML-based content classification.

## Testing

### Basic Tests

Run the basic test suite to verify setup:

```bash
python3 tests/test_reddit_scraper.py
```

This tests:
- ✅ PRAW library installation
- ✅ Subreddit map configuration
- ✅ Age filtering logic (backward compatible)
- ✅ Environment variable setup (warnings only)
- ✅ Output directory creation

### Enhanced Feature Tests

Run the comprehensive test suite for v2.0 features:

```bash
python3 -m pytest tests/test_reddit_scraper_enhanced.py -v
```

This tests:
- ✅ DuplicateTracker: Database creation, duplicate detection, statistics
- ✅ ScraperState: State persistence, timestamp tracking
- ✅ Rate Limiting: Exponential backoff, retry logic
- ✅ Quality Thresholds: Configuration and age-appropriate filtering
- ✅ Enhanced Filtering: Text length, quality thresholds

**Test Results:**
- 16 tests total
- Covers all new features
- Includes integration scenarios

## Rate Limiting (Enhanced)

The scraper respects Reddit's API rate limits with advanced handling:

- **Base Rate Limiting**: 2-second delay between subreddit scrapes
- **Exponential Backoff**: Automatic retry on 429 (rate limit) errors
  - 1st retry: 5 seconds
  - 2nd retry: 10 seconds
  - 3rd retry: 20 seconds
- **Error Detection**: Recognizes rate limit errors from PRAW exceptions
- **Graceful Degradation**: Continues with next subreddit on persistent errors

## Error Handling

The scraper handles common errors gracefully:

- **Missing credentials**: Clear error message with setup instructions
- **API errors**: Logs warning and continues with next subreddit
- **Network issues**: Automatic retry with exponential backoff (via PRAW)
- **Rate limiting**: Automatic throttling

## Troubleshooting

### "PRAW library not installed"
```bash
pip install praw==7.8.1
```

### "Reddit API credentials not found"
Make sure environment variables are set:
```bash
echo $REDDIT_CLIENT_ID
echo $REDDIT_CLIENT_SECRET
```

### "403 Forbidden" or "401 Unauthorized"
- Verify your Reddit API credentials
- Ensure app type is "script" not "web app"
- Check that credentials haven't expired

### "429 Too Many Requests"
- Reddit's rate limit exceeded
- The scraper includes automatic delays, but if this occurs:
  - Wait 10-15 minutes before retrying
  - Reduce the number of posts per subreddit

## Best Practices

1. **Run Periodically**: Scrape once per day or week to get fresh content
2. **Respect Reddit**: Follow Reddit's terms of service and API guidelines
3. **Store Credentials Safely**: Never commit credentials to version control
4. **Monitor Storage**: Each run generates ~18 JSON files, plan storage accordingly
5. **Legal Compliance**: Respect user privacy and GDPR when storing Reddit data

## Next Steps

After running the scraper:

1. **Quality Scoring**: Use `process_quality.py` to score story quality
2. **Deduplication**: Use `deduplicate_content.py` to remove duplicates
3. **Ranking**: Use `content_ranking.py` to rank by viral potential
4. **Idea Generation**: Use scraped stories as input for idea generation

## Related Files

- `scripts/process_quality.py` - Quality scoring
- `scripts/deduplicate_content.py` - Duplicate detection
- `scripts/content_ranking.py` - Content ranking
- `config/pipeline.yaml` - Reddit API configuration
- `issues/p0-critical/content-PrismQ/Pipeline/02-content-01-reddit-scraper/issue.md` - Issue specification

## License

Part of the StoryGenerator project. See main repository LICENSE file.

## Support

For issues or questions:
1. Check this README
2. Review the issue spec: `issues/p0-critical/content-PrismQ/Pipeline/02-content-01-reddit-scraper/issue.md`
3. Run the test suite: `python3 tests/test_reddit_scraper.py`
4. Check Reddit API documentation: https://www.reddit.com/dev/api
