"""
SQLite storage backend for trend data.

Structured storage with querying capabilities, suitable for production use.
"""

import sqlite3
import json
from typing import List, Optional
from datetime import datetime
from contextlib import contextmanager

from social_trends.interfaces import TrendItem, TrendType


class SQLiteStorage:
    """
    Store trend data in SQLite database.
    
    Features:
    - Structured storage with indexing
    - SQL querying capabilities
    - Suitable for medium-scale deployments (< 10M items)
    - Single-file portability
    - Historical tracking with timestamps
    """
    
    def __init__(self, db_path: str):
        """
        Initialize SQLite storage.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create tables if they don't exist"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trends (
                    id TEXT PRIMARY KEY,
                    title_or_keyword TEXT NOT NULL,
                    type TEXT NOT NULL,
                    source TEXT NOT NULL,
                    score REAL NOT NULL,
                    region TEXT NOT NULL,
                    locale TEXT NOT NULL,
                    captured_at TIMESTAMP NOT NULL,
                    url TEXT,
                    metrics TEXT,
                    keywords TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for common queries
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_source_region ON trends(source, region)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_score ON trends(score DESC)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_captured_at ON trends(captured_at DESC)"
            )
            
            # Historical snapshots table for velocity tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trend_id TEXT NOT NULL,
                    snapshot_at TIMESTAMP NOT NULL,
                    metrics TEXT NOT NULL,
                    FOREIGN KEY (trend_id) REFERENCES trends(id)
                )
            """)
            
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_snapshot_time ON snapshots(snapshot_at DESC)"
            )
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def save(self, items: List[TrendItem]):
        """
        Save trend items to database.
        
        Args:
            items: List of TrendItem objects to save
        """
        with self._get_connection() as conn:
            for item in items:
                conn.execute("""
                    INSERT OR REPLACE INTO trends
                    (id, title_or_keyword, type, source, score, region, locale,
                     captured_at, url, metrics, keywords, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.id,
                    item.title_or_keyword,
                    item.type.value,
                    item.source,
                    item.score,
                    item.region,
                    item.locale,
                    item.captured_at.isoformat(),
                    item.url,
                    json.dumps(item.metrics),
                    json.dumps(item.keywords),
                    json.dumps(item.metadata)
                ))
            
            conn.commit()
    
    def save_snapshot(self, trend_id: str, metrics: dict):
        """
        Save a historical snapshot for velocity tracking.
        
        Args:
            trend_id: ID of the trend
            metrics: Current metrics snapshot
        """
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO snapshots (trend_id, snapshot_at, metrics)
                VALUES (?, ?, ?)
            """, (trend_id, datetime.utcnow().isoformat(), json.dumps(metrics)))
            conn.commit()
    
    def load(
        self,
        source: Optional[str] = None,
        region: Optional[str] = None,
        min_score: float = 0.0,
        limit: int = 100
    ) -> List[dict]:
        """
        Load trend items from database with filtering.
        
        Args:
            source: Filter by source (e.g., 'youtube', 'google_trends')
            region: Filter by region (e.g., 'US', 'UK')
            min_score: Minimum score threshold
            limit: Maximum number of items to return
            
        Returns:
            List of dictionaries representing trend items
        """
        query = "SELECT * FROM trends WHERE score >= ?"
        params = [min_score]
        
        if source:
            query += " AND source = ?"
            params.append(source)
        
        if region:
            query += " AND region = ?"
            params.append(region)
        
        query += " ORDER BY score DESC, captured_at DESC LIMIT ?"
        params.append(limit)
        
        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_previous_snapshot(self, trend_id: str, hours_ago: int = 24) -> Optional[dict]:
        """
        Get previous snapshot for velocity calculation.
        
        Args:
            trend_id: ID of the trend
            hours_ago: How many hours back to look
            
        Returns:
            Previous snapshot metrics or None
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT metrics FROM snapshots
                WHERE trend_id = ?
                AND snapshot_at >= datetime('now', '-{} hours')
                ORDER BY snapshot_at ASC
                LIMIT 1
            """.format(hours_ago), (trend_id,))
            
            row = cursor.fetchone()
            if row:
                return json.loads(row['metrics'])
            return None
    
    def clear(self):
        """Clear all data from database"""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM snapshots")
            conn.execute("DELETE FROM trends")
            conn.commit()
