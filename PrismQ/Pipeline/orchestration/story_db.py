"""
Pipeline Story Tracking Database.

This module provides database-backed story tracking for the pipeline:
- Story registration and metadata
- Step completion tracking
- Status history and timestamps
- Progress queries

Uses SQLite for simple, zero-configuration storage.

Usage:
    from pipeline.orchestration.story_db import StoryDatabase
    
    # Default SQLite database
    db = StoryDatabase()
    db.initialize()
    
    # Custom SQLite database path
    db = StoryDatabase(db_path="path/to/custom.db")
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
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class StoryDatabase:
    """
    SQLite database for pipeline story tracking.
    
    Tracks:
    - Story registration and metadata
    - Step execution status (pending, running, completed, failed)
    - Step timestamps and run history
    - Acceptance check results
    """

    def __init__(self, db_path: Optional[str] = None, db_url: Optional[str] = None):
        """
        Initialize SQLite database connection.
        
        Args:
            db_path: Path to SQLite database file. 
                    If None, uses data/pipeline_stories.db
            db_url: Database URL (backward compatibility). 
                   Format: sqlite:///path/to/db.db
                   If provided, db_path is ignored.
        """
        # Support both db_path and db_url for backward compatibility
        if db_url:
            if not db_url.startswith("sqlite:///"):
                raise ValueError("Only SQLite databases are supported. Use sqlite:///path/to/db.db format")
            db_path = db_url.replace("sqlite:///", "")
        
        if db_path is None:
            db_path = os.getenv("DB_PATH", "data/pipeline_stories.db")
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
    
    def initialize(self) -> None:
        """Initialize SQLite database schema."""
        cursor = self.connection.cursor()
        
        # Stories table - main story registry
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
        
        # Step status table - tracks each step's status for each story
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
        
        # Step history table - tracks all executions
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
        
        # Indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_stories_story_id 
            ON stories(story_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_step_status_story_id 
            ON step_status(story_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_step_status_step_name 
            ON step_status(step_name)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_step_status_status 
            ON step_status(status)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_step_history_story_id 
            ON step_history(story_id)
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
        metadata_value = json.dumps(metadata or {})
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO stories (story_id, title, source, metadata, updated_at)
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
        
        cursor.execute("""
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
        cursor.execute("""
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
        # Extract step number
        step_num = int(step_name.split("_")[0])
        
        if step_num == 1:
            # First step - get stories without step_status entry for this step
            cursor.execute(f"""
                SELECT s.story_id
                FROM stories s
                LEFT JOIN step_status ss 
                    ON s.story_id = ss.story_id AND ss.step_name = {'?'}
                WHERE ss.story_id IS NULL OR ss.status != {'?'}
                ORDER BY s.created_at
                LIMIT {'?'}
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
                FROM stories s
                JOIN step_status ss_prev 
                    ON s.story_id = ss_prev.story_id 
                    AND ss_prev.step_name = {'?'}
                    AND ss_prev.status = {'?'}
                LEFT JOIN step_status ss_curr 
                    ON s.story_id = ss_curr.story_id 
                    AND ss_curr.step_name = {'?'}
                WHERE ss_curr.story_id IS NULL OR ss_curr.status != {'?'}
                ORDER BY s.created_at
                LIMIT {'?'}
            """, (prev_step_name, "completed", step_name, "completed", limit))
        
        rows = cursor.fetchall()
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
        # Get story info
        cursor.execute(f"""
            SELECT * FROM stories
            WHERE story_id = {'?'}
        """, (story_id,))
        
        story_row = cursor.fetchone()
        if not story_row:
            return {}
        
        story = dict(story_row)
        
        # Get step statuses
        cursor.execute(f"""
            SELECT * FROM step_status
            WHERE story_id = {'?'}
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
        cursor.execute(f"""
            SELECT 
                step_name,
                status,
                COUNT(*) as count
            FROM step_status
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
