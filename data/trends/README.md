# Google Trends Processing for StoryGenerator

## Overview

This directory contains tools for processing Google Trends data to generate content ideas for the StoryGenerator pipeline. The trends processor analyzes CSV files from Google Trends and generates content suggestions based on trending topics.

## Directory Structure

```
trends/
├── raw/              # Place your Google Trends CSV files here
├── processed/        # Processed trends and content suggestions (JSON)
├── samples/          # Sample CSV files for reference
└── {gender}/{age}/   # Organized trends by audience (auto-created)
```

## Getting Google Trends Data

### Manual Export from Google Trends

1. Visit [Google Trends](https://trends.google.com/trends/)
2. Search for topics or explore trending searches
3. Select time range (e.g., Past day, Past 7 days, Past month)
4. Select region/country (e.g., US, UK, CZ)
5. Click the download icon (⬇) to export as CSV
6. Save the CSV file to `trends/raw/` directory

### CSV File Formats

The processor supports three types of Google Trends CSV files:

#### 1. Trending Topics
```csv
query,value,link,time,geo,property
artificial intelligence,100,https://trends.google.com/...,2024-10-06,US,
machine learning,85,https://trends.google.com/...,2024-10-06,US,
```

#### 2. Related Entities
```csv
entity,value,link,property
Technology,100,,
Artificial Intelligence,95,,
```

#### 3. Related Queries
```csv
query,value,link,property
how does ai work,100,,
what is machine learning,95,,
```

## Processing Trends

### Quick Start

```bash
# Process trends from raw directory
python process_trends.py

# Process trends from custom directory
python process_trends.py path/to/csv/files

# Specify output directory
python process_trends.py path/to/csv/files path/to/output
```

### Example

```bash
# 1. Download Google Trends CSV files to trends/raw/
cp ~/Downloads/trending_US_7d.csv trends/raw/

# 2. Run the processor
python process_trends.py

# 3. Check results in trends/processed/
ls trends/processed/
```

## Output Files

The processor generates two types of JSON files in `trends/processed/`:

### 1. Aggregated Trends
`trends_{country}_{timestamp}.json`

Contains all trending topics with aggregated values:
```json
{
  "timestamp": "20241006_193000",
  "country": "US",
  "trends_count": 25,
  "trends": [
    {
      "topic": "artificial intelligence",
      "average_value": 95.5,
      "occurrences": 2,
      "total_value": 191,
      "details": [...]
    }
  ]
}
```

### 2. Content Suggestions
`content_suggestions_{country}_{timestamp}.json`

Contains ready-to-use content suggestions:
```json
{
  "timestamp": "20241006_193000",
  "country": "US",
  "suggestions_count": 20,
  "suggestions": [
    {
      "rank": 1,
      "topic": "artificial intelligence",
      "trend_score": 95.5,
      "content_type": "technology",
      "suggested_title": "Understanding Artificial Intelligence",
      "keywords": ["artificial", "intelligence"],
      "target_audiences": ["men/20-24", "men/25-29", "women/20-24"]
    }
  ]
}
```

## Features

### Automatic Categorization

Topics are automatically categorized into:
- **Technology**: AI, software, apps, digital
- **Entertainment**: Music, movies, gaming, sports
- **Science**: Space, climate, research
- **Finance**: Crypto, stocks, investment
- **Lifestyle**: Health, fitness, food, travel
- **Education**: Learning, tutorials, guides
- **General**: Other topics

### Smart Title Generation

Generates engaging titles:
- "Understanding {Topic}"
- "The Ultimate Guide to {Topic}"
- "What You Need to Know About {Topic}"
- "Exploring {Topic}"
- "The Future of {Topic}"

### Audience Targeting

Suggests target audiences based on topic type:
- Technology → Men/Women 20-29
- Entertainment → Men/Women 15-24
- Education → Men/Women 20-29
- Science → Men 20-29, Women 20-24

### Trend Aggregation

- Combines data from multiple CSV files
- Calculates average trend values
- Filters by minimum threshold (default: 50)
- Sorts by trend score

## Integration with StoryGenerator

### 1. Run Trends Processor

```bash
python process_trends.py
```

### 2. Review Content Suggestions

Check `trends/processed/content_suggestions_*.json` files

### 3. Select Topics for Ideas

Copy trending topics to ideas generation:

```python
import json

# Load content suggestions
with open('trends/processed/content_suggestions_US_20241006_193000.json') as f:
    data = json.load(f)

# Extract top 5 topics
top_topics = [s['topic'] for s in data['suggestions'][:5]]

# Use in story generation
for topic in top_topics:
    print(f"Generate story about: {topic}")
```

### 4. Automate with Pipeline

Add to your content generation pipeline:

```bash
#!/bin/bash
# 1. Process trends
python process_trends.py

# 2. Generate ideas (coming soon)
python generate_ideas_from_trends.py

# 3. Continue with story generation
python Generators/GStoryIdeas.py
```

## Sample Data

Sample CSV files are provided in `trends/samples/`:
- `trending_CZ_1d_sample.csv` - Czech Republic daily trends
- `trending_US_7d_sample.csv` - US weekly trends
- `relatedEntities_sample.csv` - Related entities example
- `relatedQueries_sample.csv` - Related queries example

Test with sample data:
```bash
python process_trends.py trends/samples trends/processed
```

## Advanced Usage

### Filter by Minimum Value

Edit `process_trends.py` to adjust `min_value`:
```python
aggregated = aggregate_trends(all_trends, min_value=70)  # Only trends ≥70
```

### Customize Content Suggestions

Edit suggestion parameters:
```python
suggestions = generate_content_suggestions(aggregated, max_suggestions=50)
```

### Add Custom Categories

Edit `categorize_topic()` function to add your categories:
```python
categories = {
    "your_category": ["keyword1", "keyword2"],
    # ...
}
```

## Naming Convention

CSV files should follow this naming pattern for automatic country detection:
- `trending_{COUNTRY}_{PERIOD}.csv` (e.g., `trending_US_7d.csv`)
- `trending_{COUNTRY}_{DATE}.csv` (e.g., `trending_CZ_20241006.csv`)
- `relatedEntities.csv`
- `relatedQueries.csv`

Country codes must be 2 letters uppercase (US, UK, CZ, etc.)

## Tips

1. **Regular Updates**: Process trends weekly or daily for fresh content ideas
2. **Multiple Countries**: Export trends from different countries to diversify content
3. **Combine Data**: Use both trending topics and related queries for comprehensive analysis
4. **Filter Noise**: Adjust `min_value` to filter out low-value trends
5. **Track History**: Keep processed files to analyze trend evolution over time

## Troubleshooting

### No CSV files found
- Ensure CSV files are in `trends/raw/` directory
- Check file extensions are `.csv`

### Empty trends list
- Check CSV file format matches expected structure
- Verify CSV has proper headers

### Country not detected
- Use naming pattern: `trending_{COUNTRY}_*.csv`
- Country code must be 2 letters uppercase

## See Also

- [CONFIGURATION.md](../CONFIGURATION.md) - Main configuration guide
- [FOLDER_STRUCTURE.md](../FOLDER_STRUCTURE.md) - Folder structure documentation
- [Google Trends](https://trends.google.com/trends/) - Official Google Trends website
