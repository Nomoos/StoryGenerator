"""
Pipeline Story Tracking Database.

This module provides database-backed story tracking for the pipeline:
- Story registration and metadata
- Step completion tracking
- Status history and timestamps
- Progress queries

Supports both SQLite (default) and PostgreSQL (optional).

Usage:
    from pipeline.orchestration.story_db import StoryDatabase
    
    # SQLite (default)
    db = StoryDatabase()
    db.initialize()
    
    # PostgreSQL (optional)
    db = StoryDatabase(db_url="postgresql+psycopg://user:pass@localhost/storygen")
    db.initialize()
    
    # Register a story
    story_id = db.register_story("STORY-001", metadata={"source": "manual"})
    
    # Update step status
    db.update_step_status(story_id, "01_ingest", "completed")
    
    # Get pending stories for a step
    pending = db.get_pending_stories("02_preprocess")
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse


class StoryDatabase:
    """
    Database for pipeline story tracking.
    
    Tracks:
    - Story registration and metadata
    - Step execution status (pending, running, completed, failed)
    - Step timestamps and run history
    - Acceptance check results
    """

    def __init__(self, db_url: Optional[str] = None, schema: str = "public"):
        """
        Initialize database connection.
        
        Args:
            db_url: Database URL. If None, uses SQLite at data/pipeline_stories.db.
                   Format: sqlite:///path/to/db.db or postgresql+psycopg://user:pass@host/db
            schema: Schema name for PostgreSQL (default: public)
        """
        self.db_url = db_url or os.getenv("DB_URL", "sqlite:///data/pipeline_stories.db")
        self.schema = schema or os.getenv("DB_SCHEMA", "public")
        self.connection = None
        self.engine = None
        
        # Determine database type
        parsed = urlparse(self.db_url)
        self.db_type = parsed.scheme.split("+")[0]  # sqlite or postgresql
        
        # Setup based on database type
        if self.db_type == "sqlite":
            self._setup_sqlite()
        elif self.db_type == "postgresql":
            self._setup_postgresql()
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
    
    def _setup_sqlite(self):
        """Setup SQLite connection."""
        import sqlite3
        
        # Extract path from URL
        db_path = self.db_url.replace("sqlite:///", "")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
    
    def _setup_postgresql(self):
        """Setup PostgreSQL connection."""
        try:
            import psycopg
            from psycopg.rows import dict_row
            
            # Remove the +psycopg prefix for psycopg3
            conn_url = self.db_url.replace("postgresql+psycopg://", "postgresql://")
            self.connection = psycopg.connect(conn_url, row_factory=dict_row)
        except ImportError:
            raise ImportError(
                "psycopg is required for PostgreSQL support. "
                "Install it with: pip install psycopg[binary]"
            )
    
    def initialize(self) -> None:
        """Initialize database schema."""
        cursor = self.connection.cursor()
        
        # Stories table - main story registry
        if self.db_type == "sqlite":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    story_id TEXT UNIQUE NOT NULL,
                    title TEXT,
                    source TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:  # postgresql
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.schema}.stories (
                    id SERIAL PRIMARY KEY,
                    story_id TEXT UNIQUE NOT NULL,
                    title TEXT,
                    source TEXT,
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        # Step status table - tracks each step's status for each story
        if self.db_type == "sqlite":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS step_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    story_id TEXT NOT NULL,
                    step_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    run_id TEXT,
                    error_message TEXT,
                    acceptance_passed INTEGER DEFAULT 0,
                    acceptance_details TEXT,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories(story_id),
                    UNIQUE(story_id, step_name)
                )
            """)
        else:  # postgresql
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.schema}.step_status (
                    id SERIAL PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    step_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    run_id TEXT,
                    error_message TEXT,
                    acceptance_passed BOOLEAN DEFAULT FALSE,
                    acceptance_details TEXT,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES {self.schema}.stories(story_id),
                    UNIQUE(story_id, step_name)
                )
            """)
        
        # Step history table - tracks all executions
        if self.db_type == "sqlite":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS step_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    story_id TEXT NOT NULL,
                    step_name TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    error_message TEXT,
                    execution_time_ms INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES stories(story_id)
                )
            """)
        else:  # postgresql
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.schema}.step_history (
                    id SERIAL PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    step_name TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    error_message TEXT,
                    execution_time_ms INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (story_id) REFERENCES {self.schema}.stories(story_id)
                )
            """)
        
        # Indexes for performance
        table_prefix = f"{self.schema}." if self.db_type == "postgresql" else ""
        
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_stories_story_id 
            ON {table_prefix}stories(story_id)
        """)
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_step_status_story_id 
            ON {table_prefix}step_status(story_id)
        """)
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_step_status_step_name 
            ON {table_prefix}step_status(step_name)
        """)
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_step_status_status 
            ON {table_prefix}step_status(status)
        """)
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_step_history_story_id 
            ON {table_prefix}step_history(story_id)
        """)
        
        self.connection.commit()
    
    def register_story(
        self,
        story_id: str,
        title: Optional[str] = None,
        source: str = "manual",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Register a new story in the database.
        
        Args:
            story_id: Unique story identifier
            title: Story title (optional)
            source: Source of the story (manual, reddit, etc.)
            metadata: Additional metadata as dict
            
        Returns:
            str: The story_id
        """
        cursor = self.connection.cursor()
        table_prefix = f"{self.schema}." if self.db_type == "postgresql" else ""
        
        metadata_value = json.dumps(metadata or {}) if self.db_type == "sqlite" else metadata or {}
        
        try:
            cursor.execute(f"""
                INSERT INTO {table_prefix}stories (story_id, title, source, metadata)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (story_id) DO UPDATE
                SET updated_at = CURRENT_TIMESTAMP
            """ if self.db_type == "postgresql" else f"""
                INSERT OR REPLACE INTO {table_prefix}stories (story_id, title, source, metadata, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (story_id, title, source, metadata_value))
            
            self.connection.commit()
            return story_id
        except Exception as e:
            self.connection.rollback()
            raise
    
    def update_step_status(
        self,
        story_id: str,
        step_name: str,
        status: str,
        run_id: Optional[str] = None,
        error_message: Optional[str] = None,
        acceptance_passed: bool = False,
        acceptance_details: Optional[str] = None
    ) -> None:
        """
        Update the status of a step for a story.
        
        Args:
            story_id: Story identifier
            step_name: Name of the step (e.g., "01_ingest")
            status: Status (pending, running, completed, failed)
            run_id: Run identifier
            error_message: Error message if failed
            acceptance_passed: Whether acceptance criteria passed
            acceptance_details: Details about acceptance check
        """
        cursor = self.connection.cursor()
        table_prefix = f"{self.schema}." if self.db_type == "postgresql" else ""
        
        # Update step_status table
        if status == "running":
            started_at = datetime.now()
            completed_at = None
        elif status in ("completed", "failed"):
            started_at = None  # Don't update started_at
            completed_at = datetime.now()
        else:
            started_at = None
            completed_at = None
        
        if self.db_type == "postgresql":
            cursor.execute(f"""
                INSERT INTO {self.schema}.step_status 
                (story_id, step_name, status, run_id, error_message, acceptance_passed, 
                 acceptance_details, started_at, completed_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (story_id, step_name) DO UPDATE
                SET status = EXCLUDED.status,
                    run_id = COALESCE(EXCLUDED.run_id, {self.schema}.step_status.run_id),
                    error_message = EXCLUDED.error_message,
                    acceptance_passed = EXCLUDED.acceptance_passed,
                    acceptance_details = EXCLUDED.acceptance_details,
                    started_at = COALESCE(EXCLUDED.started_at, {self.schema}.step_status.started_at),
                    completed_at = COALESCE(EXCLUDED.completed_at, {self.schema}.step_status.completed_at),
                    created_at = CURRENT_TIMESTAMP
            """, (story_id, step_name, status, run_id, error_message, acceptance_passed,
                  acceptance_details, started_at, completed_at))
        else:
            cursor.execute(f"""
                INSERT OR REPLACE INTO step_status 
                (story_id, step_name, status, run_id, error_message, acceptance_passed, 
                 acceptance_details, started_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (story_id, step_name, status, run_id, error_message, 
                  1 if acceptance_passed else 0, acceptance_details, 
                  started_at, completed_at))
        
        self.connection.commit()
    
    def add_step_history(
        self,
        story_id: str,
        step_name: str,
        run_id: str,
        status: str,
        error_message: Optional[str] = None,
        execution_time_ms: Optional[int] = None
    ) -> None:
        """
        Add an entry to step history.
        
        Args:
            story_id: Story identifier
            step_name: Name of the step
            run_id: Run identifier
            status: Execution status
            error_message: Error message if failed
            execution_time_ms: Execution time in milliseconds
        """
        cursor = self.connection.cursor()
        table_prefix = f"{self.schema}." if self.db_type == "postgresql" else ""
        
        if self.db_type == "postgresql":
            cursor.execute(f"""
                INSERT INTO {self.schema}.step_history 
                (story_id, step_name, run_id, status, error_message, execution_time_ms)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (story_id, step_name, run_id, status, error_message, execution_time_ms))
        else:
            cursor.execute(f"""
                INSERT INTO step_history 
                (story_id, step_name, run_id, status, error_message, execution_time_ms)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (story_id, step_name, run_id, status, error_message, execution_time_ms))
        
        self.connection.commit()
    
    def get_pending_stories(self, step_name: str, limit: int = 10) -> List[str]:
        """
        Get list of stories pending for a specific step.
        
        A story is pending for a step if:
        - Previous step is completed
        - Current step is not completed (or doesn't exist)
        
        Args:
            step_name: Name of the step (e.g., "02_preprocess")
            limit: Maximum number of stories to return
            
        Returns:
            List of story IDs
        """
        cursor = self.connection.cursor()
        table_prefix = f"{self.schema}." if self.db_type == "postgresql" else ""
        
        # Extract step number
        step_num = int(step_name.split("_")[0])
        
        if step_num == 1:
            # First step - get stories without step_status entry for this step
            cursor.execute(f"""
                SELECT s.story_id
                FROM {table_prefix}stories s
                LEFT JOIN {table_prefix}step_status ss 
                    ON s.story_id = ss.story_id AND ss.step_name = {'%s' if self.db_type == 'postgresql' else '?'}
                WHERE ss.story_id IS NULL OR ss.status != {'%s' if self.db_type == 'postgresql' else '?'}
                ORDER BY s.created_at
                LIMIT {'%s' if self.db_type == 'postgresql' else '?'}
            """, (step_name, "completed", limit))
        else:
            # Subsequent steps - previous step must be completed, current step not completed
            prev_step_num = step_num - 1
            step_names = {
                1: "01_ingest",
                2: "02_preprocess",
                3: "03_generate",
                4: "04_postprocess",
                5: "05_package"
            }
            prev_step_name = step_names.get(prev_step_num)
            
            cursor.execute(f"""
                SELECT s.story_id
                FROM {table_prefix}stories s
                JOIN {table_prefix}step_status ss_prev 
                    ON s.story_id = ss_prev.story_id 
                    AND ss_prev.step_name = {'%s' if self.db_type == 'postgresql' else '?'}
                    AND ss_prev.status = {'%s' if self.db_type == 'postgresql' else '?'}
                LEFT JOIN {table_prefix}step_status ss_curr 
                    ON s.story_id = ss_curr.story_id 
                    AND ss_curr.step_name = {'%s' if self.db_type == 'postgresql' else '?'}
                WHERE ss_curr.story_id IS NULL OR ss_curr.status != {'%s' if self.db_type == 'postgresql' else '?'}
                ORDER BY s.created_at
                LIMIT {'%s' if self.db_type == 'postgresql' else '?'}
            """, (prev_step_name, "completed", step_name, "completed", limit))
        
        rows = cursor.fetchall()
        if self.db_type == "postgresql":
            return [row["story_id"] for row in rows]
        else:
            return [row[0] for row in rows]
    
    def get_story_status(self, story_id: str) -> Dict[str, Any]:
        """
        Get the status of all steps for a story.
        
        Args:
            story_id: Story identifier
            
        Returns:
            Dict with story info and step statuses
        """
        cursor = self.connection.cursor()
        table_prefix = f"{self.schema}." if self.db_type == "postgresql" else ""
        
        # Get story info
        cursor.execute(f"""
            SELECT * FROM {table_prefix}stories
            WHERE story_id = {'%s' if self.db_type == 'postgresql' else '?'}
        """, (story_id,))
        
        story_row = cursor.fetchone()
        if not story_row:
            return {}
        
        story = dict(story_row)
        
        # Get step statuses
        cursor.execute(f"""
            SELECT * FROM {table_prefix}step_status
            WHERE story_id = {'%s' if self.db_type == 'postgresql' else '?'}
            ORDER BY step_name
        """, (story_id,))
        
        steps = [dict(row) for row in cursor.fetchall()]
        
        return {
            "story": story,
            "steps": steps
        }
    
    def get_step_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about step execution.
        
        Returns:
            Dict with statistics per step
        """
        cursor = self.connection.cursor()
        table_prefix = f"{self.schema}." if self.db_type == "postgresql" else ""
        
        cursor.execute(f"""
            SELECT 
                step_name,
                status,
                COUNT(*) as count
            FROM {table_prefix}step_status
            GROUP BY step_name, status
            ORDER BY step_name, status
        """)
        
        rows = cursor.fetchall()
        
        # Organize by step
        stats = {}
        for row in rows:
            row_dict = dict(row)
            step = row_dict["step_name"]
            if step not in stats:
                stats[step] = {}
            stats[step][row_dict["status"]] = row_dict["count"]
        
        return stats
    
    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
