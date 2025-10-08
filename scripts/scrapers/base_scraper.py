#!/usr/bin/env python3
"""
Base scraper interface for alternative content sources.

Provides a common interface for all content scrapers (Quora, Twitter, etc.)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import json


class BaseScraper(ABC):
    """Abstract base class for content scrapers."""
    
    def __init__(self, source_name: str):
        """Initialize the scraper.
        
        Args:
            source_name: Name of the content source (e.g., 'quora', 'twitter')
        """
        self.source_name = source_name
        # Use absolute path to the repository root
        repo_root = Path(__file__).parent.parent.parent
        self.base_output_dir = repo_root / "src" / "Generator" / "sources" / source_name
    
    @abstractmethod
    def scrape_content(self, 
                      topic: str, 
                      gender: str, 
                      age_bucket: str, 
                      limit: int = 50) -> List[Dict]:
        """Scrape content from the source.
        
        Args:
            topic: Topic or keywords to search for
            gender: Target gender ('men' or 'women')
            age_bucket: Target age bucket ('10-13', '14-17', or '18-23')
            limit: Maximum number of items to fetch
            
        Returns:
            List of dictionaries containing scraped content
        """
        pass
    
    def filter_age_appropriate(self, 
                              content_items: List[Dict], 
                              age_bucket: str) -> List[Dict]:
        """Filter content for age-appropriateness.
        
        Args:
            content_items: List of content items to filter
            age_bucket: Target age bucket ('10-13', '14-17', or '18-23')
            
        Returns:
            Filtered list of content items
        """
        # Simple keyword filtering
        inappropriate_keywords = {
            "10-13": ["sex", "drugs", "violence", "nsfw", "explicit", "porn", "adult"],
            "14-17": ["explicit", "nsfw", "porn", "adult"],
            "18-23": []  # No filtering for adults
        }
        
        keywords = inappropriate_keywords.get(age_bucket, [])
        if not keywords:
            return content_items
        
        filtered = []
        for item in content_items:
            # Check title and text content
            text_lower = (item.get("title", "") + " " + item.get("text", "")).lower()
            if not any(kw in text_lower for kw in keywords):
                filtered.append(item)
        
        return filtered
    
    def save_content(self, 
                    content_items: List[Dict], 
                    gender: str, 
                    age_bucket: str) -> Path:
        """Save scraped content to JSON file.
        
        Args:
            content_items: List of content items to save
            gender: Target gender
            age_bucket: Target age bucket
            
        Returns:
            Path to saved file
        """
        # Create output directory
        output_dir = self.base_output_dir / gender / age_bucket
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        output_file = output_dir / f"{timestamp}_{self.source_name}_content.json"
        
        # Prepare data structure
        data = {
            "source": self.source_name,
            "gender": gender,
            "age_bucket": age_bucket,
            "total_items": len(content_items),
            "scraped_at": datetime.now().isoformat(),
            "content": content_items
        }
        
        # Save to file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def run(self, 
           topic: str, 
           gender: str, 
           age_bucket: str, 
           limit: int = 50) -> Dict:
        """Run the complete scraping pipeline.
        
        Args:
            topic: Topic or keywords to search for
            gender: Target gender
            age_bucket: Target age bucket
            limit: Maximum number of items to fetch
            
        Returns:
            Dictionary with scraping results and statistics
        """
        print(f"\n🔍 Scraping {self.source_name} for {gender}/{age_bucket}...")
        print(f"   Topic: {topic}")
        print(f"   Limit: {limit}")
        
        # Scrape content
        content_items = self.scrape_content(topic, gender, age_bucket, limit)
        print(f"   ✓ Scraped {len(content_items)} items")
        
        # Filter for age-appropriateness
        filtered_items = self.filter_age_appropriate(content_items, age_bucket)
        print(f"   ✓ Filtered to {len(filtered_items)} age-appropriate items")
        
        # Save to file
        output_file = self.save_content(filtered_items, gender, age_bucket)
        print(f"   ✓ Saved to {output_file}")
        
        return {
            "source": self.source_name,
            "gender": gender,
            "age_bucket": age_bucket,
            "topic": topic,
            "scraped": len(content_items),
            "filtered": len(filtered_items),
            "output_file": str(output_file),
            "timestamp": datetime.now().isoformat()
        }
