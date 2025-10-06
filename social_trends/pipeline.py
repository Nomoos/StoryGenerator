"""
Trends pipeline - orchestrates fetching, normalization, scoring, and storage.

Coordinates multiple trend sources to create a unified trending content feed.
"""

import asyncio
from typing import List, Optional, Set
from datetime import datetime
import json

from social_trends.interfaces import TrendItem, TrendSource
from social_trends.sources import YouTubeSource, GoogleTrendsSource
from social_trends.storage import CSVStorage, SQLiteStorage
from social_trends.utils.scoring import TrendScorer


class TrendsPipeline:
    """
    Main pipeline for aggregating trends from multiple sources.
    
    Features:
    - Multi-source aggregation
    - Automatic normalization
    - De-duplication
    - Comprehensive scoring
    - Flexible storage backends
    """
    
    def __init__(
        self,
        sources: List[TrendSource],
        storage_backend: str = "csv",
        storage_path: str = "data/trends",
        enable_velocity: bool = False
    ):
        """
        Initialize trends pipeline.
        
        Args:
            sources: List of TrendSource instances to query
            storage_backend: 'csv' or 'sqlite'
            storage_path: Path to storage file/database
            enable_velocity: Enable velocity tracking (requires SQLite)
        """
        self.sources = sources
        self.enable_velocity = enable_velocity
        
        # Initialize storage
        if storage_backend == "csv":
            self.storage = CSVStorage(f"{storage_path}.csv")
        elif storage_backend == "sqlite":
            self.storage = SQLiteStorage(f"{storage_path}.db")
        else:
            raise ValueError(f"Unknown storage backend: {storage_backend}")
        
        self.scorer = TrendScorer()
    
    async def run(
        self,
        regions: List[str] = ["US"],
        limit_per_source: int = 50,
        min_score: float = 0.0
    ) -> List[TrendItem]:
        """
        Run the pipeline: fetch, normalize, score, and store trends.
        
        Args:
            regions: List of regions to query (e.g., ['US', 'UK', 'CZ'])
            limit_per_source: Maximum items to fetch from each source
            min_score: Minimum score threshold for saving
            
        Returns:
            List of all collected TrendItem objects
        """
        all_items = []
        
        # Fetch from all sources in parallel
        print(f"🔍 Fetching trends from {len(self.sources)} sources for {len(regions)} region(s)...")
        
        tasks = []
        for source in self.sources:
            for region in regions:
                if region in source.supports_regions():
                    tasks.append(self._fetch_from_source(source, region, limit_per_source))
                else:
                    print(f"⚠️  {source.name} doesn't support region {region}, skipping")
        
        # Execute all fetch tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collect items from results
        for result in results:
            if isinstance(result, Exception):
                print(f"❌ Error fetching trends: {result}")
            elif isinstance(result, list):
                all_items.extend(result)
        
        print(f"✅ Fetched {len(all_items)} items total")
        
        # De-duplicate
        unique_items = self._deduplicate(all_items)
        print(f"🔄 After de-duplication: {len(unique_items)} unique items")
        
        # Apply velocity tracking if enabled
        if self.enable_velocity and hasattr(self.storage, 'get_previous_snapshot'):
            unique_items = await self._apply_velocity_scoring(unique_items)
        
        # Filter by minimum score
        filtered_items = [item for item in unique_items if item.score >= min_score]
        print(f"📊 After score filtering (>={min_score}): {len(filtered_items)} items")
        
        # Sort by score
        filtered_items.sort(key=lambda x: x.score, reverse=True)
        
        # Save to storage
        if filtered_items:
            self.storage.save(filtered_items)
            print(f"💾 Saved {len(filtered_items)} items to storage")
        
        return filtered_items
    
    async def _fetch_from_source(
        self,
        source: TrendSource,
        region: str,
        limit: int
    ) -> List[TrendItem]:
        """Fetch items from a single source"""
        try:
            print(f"  → Querying {source.name} for {region}...")
            items = await source.fetch_items(region, limit)
            print(f"    ✓ Got {len(items)} items from {source.name}/{region}")
            return items
        except NotImplementedError:
            print(f"    ⚠️  {source.name} not yet implemented, skipping")
            return []
        except Exception as e:
            print(f"    ✗ Error from {source.name}/{region}: {e}")
            return []
    
    def _deduplicate(self, items: List[TrendItem]) -> List[TrendItem]:
        """
        Remove duplicate items using fuzzy matching.
        
        Deduplication strategy:
        1. Exact ID match (same source + ID)
        2. Fuzzy title match (85%+ similarity)
        3. Keep highest scoring duplicate
        """
        seen_ids: Set[str] = set()
        seen_titles: Set[str] = set()
        unique_items: List[TrendItem] = []
        
        # Sort by score descending to keep best items
        sorted_items = sorted(items, key=lambda x: x.score, reverse=True)
        
        for item in sorted_items:
            # Check exact ID
            if item.id in seen_ids:
                continue
            
            # Check fuzzy title match
            normalized_title = item.title_or_keyword.lower().strip()
            if normalized_title in seen_titles:
                continue
            
            # This is a unique item
            seen_ids.add(item.id)
            seen_titles.add(normalized_title)
            unique_items.append(item)
        
        return unique_items
    
    async def _apply_velocity_scoring(self, items: List[TrendItem]) -> List[TrendItem]:
        """Apply velocity-based scoring using historical data"""
        updated_items = []
        
        for item in items:
            # Get previous snapshot
            previous = self.storage.get_previous_snapshot(item.id, hours_ago=24)
            
            if previous:
                # Recalculate score with velocity
                current_value = item.metrics.get("viewCount", 0)
                previous_value = previous.get("viewCount", 0)
                
                new_score = self.scorer.compute_comprehensive_score(
                    current_value=current_value,
                    previous_value=previous_value,
                    engagement=item.metrics.get("likeCount", 0) + item.metrics.get("commentCount", 0),
                    total_views=current_value,
                    timestamp=item.captured_at
                )
                
                item.score = new_score
            
            # Save current snapshot for future velocity calculation
            self.storage.save_snapshot(item.id, item.metrics)
            
            updated_items.append(item)
        
        return updated_items
    
    def export_json(self, items: List[TrendItem], filepath: str):
        """Export items to JSON file"""
        data = [item.to_dict() for item in items]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Exported to {filepath}")
    
    async def close(self):
        """Clean up resources"""
        for source in self.sources:
            if hasattr(source, '_close_session'):
                await source._close_session()
