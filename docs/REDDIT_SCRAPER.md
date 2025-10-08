# Reddit Story Scraper Documentation

## Overview

The Reddit Story Scraper is a Python script that mines stories from target subreddits, filtered by demographic segments (gender and age). It uses the PRAW (Python Reddit API Wrapper) library to access Reddit's API.

## Features

- **Demographic Filtering**: Scrapes stories for 6 different demographic segments (2 genders × 3 age groups)
- **Age-Appropriate Content**: Filters stories based on age bucket using keyword filtering
- **Engagement-Based Selection**: Prioritizes stories with high upvotes and comments
- **Comment Context**: Includes top 5 comments for each story
- **Rate Limit Compliance**: Built-in delays to respect Reddit's API rate limits
- **Structured Output**: Saves stories in organized JSON format

## Installation

### 1. Install Dependencies

```bash
pip install praw==7.7.1
```

Or install all project dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Reddit API Credentials

#### Get Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - **name**: StoryGenerator
   - **type**: script
   - **description**: Story scraping for video generation
   - **redirect uri**: http://localhost:8080
4. Click "Create app"
5. Note your **client_id** (under the app name) and **client_secret**

#### Set Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
```

Or set environment variables directly:

```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_secret"
```

## Usage

### Run for All Segments

```bash
cd /path/to/StoryGenerator
python scripts/reddit_scraper.py
```

This will scrape stories for all 6 demographic segments:
- women/10-13
- women/14-17
- women/18-23
- men/10-13
- men/14-17
- men/18-23

### Output Files

Stories are saved to:
```
Generator/sources/reddit/{gender}/{age}/{YYYYMMDD}_reddit_stories.json
```

Example:
```
Generator/sources/reddit/women/18-23/20240115_reddit_stories.json
```

## Target Subreddits

The scraper targets different subreddits for each demographic:

| Segment | Subreddits |
|---------|-----------|
| women/10-13 | r/TrueOffMyChest, r/relationships, r/AmItheAsshole |
| women/14-17 | r/teenagers, r/AmItheAsshole, r/TrueOffMyChest |
| women/18-23 | r/relationships, r/dating_advice, r/confession |
| men/10-13 | r/teenagers, r/stories, r/confession |
| men/14-17 | r/teenagers, r/confession, r/TrueOffMyChest |
| men/18-23 | r/relationships, r/AskMen, r/confession |

## Content Filtering

### Engagement Filter

- Minimum upvotes: 500
- Fetches top posts from last week
- Sorts by total engagement (upvotes + comments)

### Age-Appropriate Filtering

Content is filtered based on age bucket:

- **10-13**: Filters out stories containing: sex, drugs, violence, nsfw, explicit
- **14-17**: Filters out stories containing: explicit, nsfw
- **18-23**: No content filtering

### Selection

- Takes top 100 stories after filtering
- Includes story metadata, full text, and top 5 comments

## Output Format

### JSON Structure

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
      "url": "https://reddit.com/r/relationships/comments/abc123/...",
      "upvotes": 1250,
      "num_comments": 340,
      "created_utc": "2024-01-10T15:20:00",
      "subreddit": "r/relationships",
      "author": "username",
      "awards": 5,
      "is_self": true,
      "top_comments": [
        {
          "text": "Comment text",
          "score": 450
        }
      ]
    }
  ]
}
```

## Testing

Run the test suite to verify installation and configuration:

```bash
python tests/test_reddit_scraper.py
```

The test suite checks:
- ✅ Required libraries are installed
- ✅ Subreddit map is configured for all segments
- ✅ Age filtering works correctly
- ✅ Environment variables are set (warnings if not)
- ✅ Output directories can be created

## Rate Limits and Best Practices

### Reddit API Rate Limits

- Reddit allows 60 requests per minute for authenticated users
- The scraper includes 2-second delays between subreddit requests
- Total runtime: ~2-3 minutes for all segments

### Best Practices

1. **Don't abuse the API**: Run the scraper at most once per day
2. **Respect privacy**: Stories are public, but be mindful of user privacy
3. **Content attribution**: Always maintain source URLs and author information
4. **Store responsibly**: Don't redistribute scraped data publicly

## Troubleshooting

### Error: "Reddit API credentials not found"

Make sure you've set the environment variables:
```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_secret"
```

### Error: "PRAW library not installed"

Install PRAW:
```bash
pip install praw==7.7.1
```

### Error: "Rate limit exceeded"

Wait a few minutes and try again. The scraper includes delays, but if you run it multiple times quickly, you may hit rate limits.

### Empty results

- Check that your Reddit credentials are valid
- Some subreddits may have fewer high-quality posts in a given week
- Try reducing `min_upvotes` in the code if needed

## Integration with Pipeline

The Reddit scraper is part of the content pipeline:

```
[Reddit Scraper] → Stories in JSON
        ↓
[Content Adapter] → Adapted ideas
        ↓
[Quality Scorer] → Scored stories
        ↓
[Topic Generator] → Video topics
```

## Next Steps

After scraping stories:

1. **Alternative Sources** (02-content-02): Add Quora, Twitter, etc.
2. **Quality Scorer** (02-content-03): Score and rank scraped stories
3. **Content Adapter** (03-ideas-01): Adapt Reddit stories into video ideas

## License

Part of the StoryGenerator project.
