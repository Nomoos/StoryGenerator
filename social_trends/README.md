# Social Trends - Multi-Platform Trends Aggregation

A modular, extensible Python package for gathering trending content from multiple social media platforms.

## Features

- **Multi-Platform Support**: YouTube, Google Trends, TikTok, Instagram, Exploding Topics
- **Async-First**: All I/O operations use async/await for efficiency
- **Modular Design**: Each source is a plug-in implementing the `TrendSource` interface
- **Flexible Storage**: CSV and SQLite backends with easy extensibility
- **Velocity Tracking**: Historical data comparison for trend growth metrics
- **Comprehensive Scoring**: Weighted formula combining velocity, volume, engagement, and recency
- **De-duplication**: Intelligent matching across sources
- **CLI Interface**: Easy command-line usage

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up API keys (for YouTube)
export YOUTUBE_API_KEY="your_youtube_api_key_here"
```

## Quick Start

### Command Line Usage

```bash
# Fetch trends from YouTube and Google Trends
python -m social_trends --sources youtube,google_trends --region US --limit 50

# Multiple regions
python -m social_trends --sources youtube --region US,UK,CZ --limit 100

# Export to JSON
python -m social_trends --sources youtube --region US --out trends.json --format json

# Use SQLite with velocity tracking
python -m social_trends --sources youtube --region US --storage sqlite --enable-velocity
```

### Python API Usage

```python
import asyncio
from social_trends.pipeline import TrendsPipeline
from social_trends.sources import YouTubeSource, GoogleTrendsSource

async def main():
    # Initialize sources
    sources = [
        YouTubeSource(),
        GoogleTrendsSource()
    ]
    
    # Create pipeline
    pipeline = TrendsPipeline(
        sources=sources,
        storage_backend="sqlite",
        storage_path="data/trends",
        enable_velocity=True
    )
    
    # Run pipeline
    items = await pipeline.run(
        regions=["US", "UK"],
        limit_per_source=50,
        min_score=50.0
    )
    
    # Export results
    pipeline.export_json(items, "trends_output.json")
    
    # Clean up
    await pipeline.close()

asyncio.run(main())
```

## Architecture

### Design Principles

1. **Modular**: Each source is a separate plug-in
2. **Atomic**: Small, focused classes and methods (SRP)
3. **Extensible**: Add new sources without modifying existing code (Open/Closed)
4. **Async-First**: All I/O uses async/await
5. **DI Everywhere**: Dependency injection for testability

### Package Structure

```
social_trends/
├── __init__.py           # Package initialization
├── __main__.py           # Module entry point
├── interfaces.py         # TrendItem and TrendSource base class
├── pipeline.py           # Main orchestration pipeline
├── cli.py                # Command-line interface
├── sources/              # Source implementations
│   ├── __init__.py
│   ├── youtube.py        # YouTube Data API v3
│   ├── google_trends.py  # Google Trends via pytrends
│   ├── tiktok.py         # TikTok (stub)
│   ├── instagram.py      # Instagram (stub)
│   └── exploding_topics.py  # Exploding Topics (stub)
├── storage/              # Storage backends
│   ├── __init__.py
│   ├── csv_storage.py    # CSV file storage
│   └── sqlite_storage.py # SQLite database
├── utils/                # Utilities
│   ├── __init__.py
│   ├── keywords.py       # Keyword extraction
│   └── scoring.py        # Trend scoring algorithms
└── tests/                # Unit tests
    └── __init__.py
```

## Implemented Sources

### YouTube Data API v3 ✅

- **Status**: Fully implemented
- **Requirements**: `YOUTUBE_API_KEY` environment variable
- **Quota**: 10,000 units/day (free)
- **Features**: Trending videos, metrics, keyword extraction

### Google Trends ✅

- **Status**: Fully implemented
- **Requirements**: `pytrends` library
- **Quota**: Rate-limited, use with delays
- **Features**: Trending searches, today's searches

### TikTok ⏳

- **Status**: Stub implementation
- **Options**: 
  - TikTok Business API (official, requires business account)
  - RapidAPI ($10-50/month)
  - Apify ($49+/month)

### Instagram ⏳

- **Status**: Stub implementation
- **Options**:
  - Instagram Graph API (requires business account)
  - CrowdTangle (free with approval)

### Exploding Topics ⏳

- **Status**: Stub implementation
- **Options**: API subscription ($99+/month)

## Trend Scoring

Comprehensive score formula (0-100):

```
score = (0.40 × velocity) + (0.30 × volume) + (0.20 × engagement) + (0.10 × recency)
```

- **Velocity**: 24-hour growth rate
- **Volume**: Absolute views/engagement (logarithmic scale)
- **Engagement**: (likes + comments + shares) / views
- **Recency**: Freshness bonus for recent content

## Storage

### CSV Storage

- Simple file-based storage
- Good for: Development, small datasets, data sharing
- Limitations: No querying, no velocity tracking

### SQLite Storage

- Structured database with indexes
- Good for: Production, medium-scale (< 10M items)
- Features: SQL querying, velocity tracking, historical snapshots

## Testing

```bash
# Run unit tests
python -m pytest social_trends/tests/

# Run specific test
python -m pytest social_trends/tests/ -k test_trend_scoring
```

## Examples

### Example 1: YouTube Trends for Multiple Regions

```bash
python -m social_trends \
  --sources youtube \
  --region US,UK,CZ,CA,AU \
  --limit 50 \
  --min-score 60 \
  --storage sqlite \
  --enable-velocity
```

### Example 2: Combined Sources

```bash
python -m social_trends \
  --sources youtube,google_trends \
  --region US \
  --limit 100 \
  --out data/combined_trends \
  --format json
```

### Example 3: High-Quality Trends Only

```bash
python -m social_trends \
  --sources youtube \
  --region US \
  --limit 50 \
  --min-score 80 \
  --out data/high_quality_trends.csv
```

## API Keys

### YouTube Data API v3

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create credentials (API key)
5. Set environment variable: `export YOUTUBE_API_KEY="your_key"`

## Contributing

To add a new trend source:

1. Create a new file in `social_trends/sources/`
2. Implement the `TrendSource` abstract class
3. Implement `fetch_items()` and `compute_score()` methods
4. Add to `sources/__init__.py`
5. Update CLI to include new source

## License

MIT License

## See Also

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3/docs)
- [pytrends Documentation](https://github.com/GeneralMills/pytrends)
- [Research: Social Platform Trends](../research/SOCIAL_PLATFORMS_TRENDS.md)
- [Research: Viral Video Requirements](../research/VIRAL_VIDEO_REQUIREMENTS.md)
