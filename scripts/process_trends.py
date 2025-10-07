#!/usr/bin/env python3
"""
Trends Processor for StoryGenerator
Processes Google Trends CSV files to extract trending topics for content generation.
"""

import os
import csv
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def load_csv_file(file_path):
    """Load and parse a CSV file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return []


def process_trending_data(csv_data, data_type="trending"):
    """
    Process trending data from CSV.
    
    Args:
        csv_data: List of dictionaries from CSV
        data_type: Type of data (trending, entities, queries)
    
    Returns:
        List of processed trend items
    """
    trends = []
    
    for row in csv_data:
        if data_type == "trending":
            trend = {
                "query": row.get("query", ""),
                "value": int(row.get("value", 0)),
                "link": row.get("link", ""),
                "time": row.get("time", ""),
                "geo": row.get("geo", ""),
                "property": row.get("property", "")
            }
        elif data_type == "entities":
            trend = {
                "entity": row.get("entity", ""),
                "value": int(row.get("value", 0)) if row.get("value") else 0,
                "link": row.get("link", ""),
                "property": row.get("property", "")
            }
        elif data_type == "queries":
            trend = {
                "query": row.get("query", ""),
                "value": int(row.get("value", 0)) if row.get("value") else 0,
                "link": row.get("link", ""),
                "property": row.get("property", "")
            }
        else:
            continue
        
        trends.append(trend)
    
    return trends


def aggregate_trends(all_trends, min_value=50):
    """
    Aggregate and filter trends by value.
    
    Args:
        all_trends: List of all trend items
        min_value: Minimum trend value to include
    
    Returns:
        Sorted list of aggregated trends
    """
    # Group by query/entity
    aggregated = defaultdict(lambda: {"value": 0, "count": 0, "data": []})
    
    for trend in all_trends:
        key = trend.get("query") or trend.get("entity", "")
        if key:
            aggregated[key]["value"] += trend.get("value", 0)
            aggregated[key]["count"] += 1
            aggregated[key]["data"].append(trend)
    
    # Calculate average and filter
    result = []
    for key, data in aggregated.items():
        avg_value = data["value"] / data["count"]
        if avg_value >= min_value:
            result.append({
                "topic": key,
                "average_value": round(avg_value, 2),
                "occurrences": data["count"],
                "total_value": data["value"],
                "details": data["data"]
            })
    
    # Sort by average value
    result.sort(key=lambda x: x["average_value"], reverse=True)
    return result


def generate_content_suggestions(trends, max_suggestions=10):
    """
    Generate content suggestions from trends.
    
    Args:
        trends: List of aggregated trends
        max_suggestions: Maximum number of suggestions to generate
    
    Returns:
        List of content suggestions
    """
    suggestions = []
    
    for i, trend in enumerate(trends[:max_suggestions], 1):
        suggestion = {
            "rank": i,
            "topic": trend["topic"],
            "trend_score": trend["average_value"],
            "content_type": categorize_topic(trend["topic"]),
            "suggested_title": generate_title(trend["topic"]),
            "keywords": extract_keywords(trend["topic"]),
            "target_audiences": suggest_audiences(trend["topic"])
        }
        suggestions.append(suggestion)
    
    return suggestions


def categorize_topic(topic):
    """Categorize topic based on keywords."""
    topic_lower = topic.lower()
    
    categories = {
        "technology": ["ai", "artificial intelligence", "machine learning", "tech", "software", "app", "digital"],
        "entertainment": ["music", "movie", "game", "gaming", "sport", "nfl", "celebrity"],
        "science": ["space", "climate", "energy", "research", "discovery"],
        "finance": ["crypto", "stock", "investment", "money", "economy"],
        "lifestyle": ["health", "fitness", "food", "travel", "fashion"],
        "education": ["learning", "course", "tutorial", "how to", "what is"]
    }
    
    for category, keywords in categories.items():
        if any(keyword in topic_lower for keyword in keywords):
            return category
    
    return "general"


def generate_title(topic):
    """Generate a suggested title from topic."""
    # Capitalize first letter of each word
    words = topic.split()
    title = " ".join(word.capitalize() for word in words)
    
    # Add engaging prefix
    prefixes = [
        f"Understanding {title}",
        f"The Ultimate Guide to {title}",
        f"What You Need to Know About {title}",
        f"Exploring {title}",
        f"The Future of {title}"
    ]
    
    # Choose based on topic type
    if "how" in topic.lower() or "what" in topic.lower():
        return title
    
    return prefixes[len(topic) % len(prefixes)]


def extract_keywords(topic):
    """Extract keywords from topic."""
    # Simple keyword extraction (can be enhanced with NLP)
    words = topic.lower().split()
    # Remove common words
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return keywords[:5]  # Top 5 keywords


def suggest_audiences(topic):
    """Suggest target audiences based on topic."""
    topic_lower = topic.lower()
    
    # Default audiences
    audiences = []
    
    # Technology topics
    if any(word in topic_lower for word in ["ai", "tech", "software", "coding", "app"]):
        audiences = ["men/20-24", "men/25-29", "women/20-24"]
    
    # Entertainment topics
    elif any(word in topic_lower for word in ["music", "movie", "game", "celebrity"]):
        audiences = ["women/15-19", "men/15-19", "women/20-24", "men/20-24"]
    
    # Education topics
    elif any(word in topic_lower for word in ["learning", "education", "how", "what"]):
        audiences = ["men/20-24", "women/20-24", "men/25-29", "women/25-29"]
    
    # Science topics
    elif any(word in topic_lower for word in ["space", "science", "climate", "research"]):
        audiences = ["men/20-24", "men/25-29", "women/20-24"]
    
    # Default
    else:
        audiences = ["men/20-24", "women/20-24", "men/25-29"]
    
    return audiences[:3]  # Top 3 audiences


def save_processed_trends(trends, suggestions, output_dir, country="global"):
    """Save processed trends to JSON files."""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save aggregated trends
    trends_file = os.path.join(output_dir, f"trends_{country}_{timestamp}.json")
    with open(trends_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": timestamp,
            "country": country,
            "trends_count": len(trends),
            "trends": trends
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved aggregated trends: {trends_file}")
    
    # Save content suggestions
    suggestions_file = os.path.join(output_dir, f"content_suggestions_{country}_{timestamp}.json")
    with open(suggestions_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": timestamp,
            "country": country,
            "suggestions_count": len(suggestions),
            "suggestions": suggestions
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved content suggestions: {suggestions_file}")
    
    return trends_file, suggestions_file


def process_trends_directory(trends_dir, output_dir, min_value=50):
    """
    Process all CSV files in trends directory.
    
    Args:
        trends_dir: Directory containing CSV files
        output_dir: Directory to save processed files
        min_value: Minimum trend value to include
    """
    print("=" * 60)
    print("Google Trends Processor")
    print("=" * 60)
    print()
    
    # Find all CSV files
    csv_files = list(Path(trends_dir).glob("*.csv"))
    
    if not csv_files:
        print(f"⚠️  No CSV files found in {trends_dir}")
        print(f"Please add Google Trends CSV files to process.")
        return
    
    print(f"Found {len(csv_files)} CSV file(s)")
    print()
    
    all_trends = []
    countries = set()
    
    # Process each CSV file
    for csv_file in csv_files:
        print(f"Processing: {csv_file.name}")
        
        csv_data = load_csv_file(csv_file)
        if not csv_data:
            continue
        
        # Determine data type from filename
        filename = csv_file.stem.lower()
        if "entity" in filename or "entities" in filename:
            data_type = "entities"
        elif "query" in filename or "queries" in filename:
            data_type = "queries"
        else:
            data_type = "trending"
        
        # Extract country from filename (e.g., trending_US_7d.csv -> US)
        parts = filename.split("_")
        country = "global"
        for part in parts:
            if len(part) == 2 and part.isupper():
                country = part
                countries.add(country)
                break
        
        trends = process_trending_data(csv_data, data_type)
        all_trends.extend(trends)
        print(f"  - Loaded {len(trends)} trends")
    
    print()
    print("=" * 60)
    print(f"Total trends loaded: {len(all_trends)}")
    print()
    
    # Aggregate trends
    aggregated = aggregate_trends(all_trends, min_value)
    print(f"Aggregated trends (≥{min_value}): {len(aggregated)}")
    print()
    
    # Generate content suggestions
    suggestions = generate_content_suggestions(aggregated, max_suggestions=20)
    print(f"Generated content suggestions: {len(suggestions)}")
    print()
    
    # Display top suggestions
    print("Top 10 Content Suggestions:")
    print("-" * 60)
    for i, suggestion in enumerate(suggestions[:10], 1):
        print(f"{i}. {suggestion['topic']}")
        print(f"   Score: {suggestion['trend_score']:.1f} | Category: {suggestion['content_type']}")
        print(f"   Title: {suggestion['suggested_title']}")
        print()
    
    # Save results for each country
    if countries:
        for country in countries:
            country_trends = [t for t in aggregated if any(
                d.get("geo") == country for d in t.get("details", [])
            )]
            if country_trends:
                country_suggestions = generate_content_suggestions(country_trends, max_suggestions=20)
                save_processed_trends(country_trends, country_suggestions, output_dir, country)
    
    # Save global results
    save_processed_trends(aggregated, suggestions, output_dir, "global")
    
    print()
    print("=" * 60)
    print("✅ Trends processing complete!")
    print("=" * 60)


def main():
    """Main entry point."""
    # Default paths
    root_dir = Path(__file__).parent.absolute()
    trends_dir = root_dir / "trends" / "raw"
    output_dir = root_dir / "trends" / "processed"
    
    # Check for command-line arguments
    if len(sys.argv) > 1:
        trends_dir = Path(sys.argv[1])
    
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    
    # Process trends
    process_trends_directory(trends_dir, output_dir)


if __name__ == "__main__":
    main()
