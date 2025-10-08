# Reddit Story Scraper

## Overview

The Reddit Story Scraper (`reddit_scraper.py`) mines high-quality stories from target subreddits, filtered by audience segment (gender) and age demographics. It's a critical component of the content pipeline that sources raw material for story generation.

## Features

- ✅ **Demographic Targeting**: Scrapes content for 6 segments (women/men × 10-13/14-17/18-23)
- ✅ **Quality Filtering**: Minimum 500+ upvotes and engagement metrics
- ✅ **Age Appropriateness**: Keyword-based filtering for younger audiences
- ✅ **Rate Limiting**: Respects Reddit API limits with automatic delays
- ✅ **Rich Metadata**: Captures upvotes, comments, awards, and top comment context
- ✅ **JSON Output**: Structured data ready for downstream processing

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

Run the scraper for all segments:

```bash
python3 scripts/reddit_scraper.py
```

This will:
1. Scrape stories from all 18 target subreddits (3 per segment)
2. Filter by upvotes (500+) and age-appropriateness
3. Save top 100 stories per segment to JSON files
4. Output files to `Generator/sources/reddit/{gender}/{age}/YYYYMMDD_reddit_stories.json`

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

Each segment gets a JSON file with this structure:

```json
{
  "segment": "women",
  "age_bucket": "18-23",
  "subreddits": ["r/relationships", "r/dating_advice", "r/confession"],
  "total_scraped": 250,
  "after_filtering": 180,
  "selected": 100,
  "scraped_at": "2024-01-15T10:30:00",
  "stories": [
    {
      "id": "abc123",
      "title": "Story title",
      "text": "Full story text...",
      "url": "https://reddit.com/r/...",
      "upvotes": 1250,
      "num_comments": 340,
      "created_utc": "2024-01-10T15:20:00",
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

## Age Filtering

The scraper implements keyword-based filtering for age-appropriateness:

- **10-13**: Filters out content with keywords: "sex", "drugs", "violence", "nsfw", "explicit"
- **14-17**: Filters out content with keywords: "explicit", "nsfw"
- **18-23**: No filtering (adult content allowed)

> **Note**: This is basic filtering. For production, consider integrating ML-based content classification.

## Testing

Run the test suite to verify setup:

```bash
python3 tests/test_reddit_scraper.py
```

This tests:
- ✅ PRAW library installation
- ✅ Subreddit map configuration
- ✅ Age filtering logic
- ✅ Environment variable setup (warnings only)
- ✅ Output directory creation

## Rate Limiting

The scraper respects Reddit's API rate limits:

- Maximum 60 requests per minute
- 2-second delay between subreddit scrapes
- Automatic error handling and logging

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
- `issues/p0-critical/content-pipeline/02-content-01-reddit-scraper/issue.md` - Issue specification

## License

Part of the StoryGenerator project. See main repository LICENSE file.

## Support

For issues or questions:
1. Check this README
2. Review the issue spec: `issues/p0-critical/content-pipeline/02-content-01-reddit-scraper/issue.md`
3. Run the test suite: `python3 tests/test_reddit_scraper.py`
4. Check Reddit API documentation: https://www.reddit.com/dev/api
