"""
CSV storage backend for trend data.

Simple file-based storage for development and small-scale deployments.
"""

import csv
import os
from typing import List
from datetime import datetime

from social_trends.interfaces import TrendItem


class CSVStorage:
    """
    Store trend data in CSV files.
    
    Simple, portable storage format suitable for:
    - Development and testing
    - Small datasets (< 100K items)
    - Easy data inspection and sharing
    """
    
    FIELDNAMES = [
        "id", "title_or_keyword", "type", "source", "score",
        "region", "locale", "captured_at", "url",
        "viewCount", "likeCount", "commentCount", "shareCount",
        "keywords", "metadata"
    ]
    
    def __init__(self, filepath: str):
        """
        Initialize CSV storage.
        
        Args:
            filepath: Path to CSV file
        """
        self.filepath = filepath
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.filepath):
            # Create parent directories
            os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)
            
            # Write headers
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writeheader()
    
    def save(self, items: List[TrendItem]):
        """
        Save trend items to CSV.
        
        Args:
            items: List of TrendItem objects to save
        """
        with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            
            for item in items:
                row = {
                    "id": item.id,
                    "title_or_keyword": item.title_or_keyword,
                    "type": item.type.value,
                    "source": item.source,
                    "score": f"{item.score:.2f}",
                    "region": item.region,
                    "locale": item.locale,
                    "captured_at": item.captured_at.isoformat(),
                    "url": item.url or "",
                    "viewCount": item.metrics.get("viewCount", ""),
                    "likeCount": item.metrics.get("likeCount", ""),
                    "commentCount": item.metrics.get("commentCount", ""),
                    "shareCount": item.metrics.get("shareCount", ""),
                    "keywords": ",".join(item.keywords),
                    "metadata": str(item.metadata)
                }
                writer.writerow(row)
    
    def load(self) -> List[dict]:
        """
        Load trend items from CSV.
        
        Returns:
            List of dictionaries representing trend items
        """
        items = []
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(row)
        
        return items
    
    def clear(self):
        """Clear all data from CSV (keep headers)"""
        with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writeheader()
