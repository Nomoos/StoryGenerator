#!/usr/bin/env python3
"""
Tests for pipeline story tracking database.

These tests validate the database module's ability to:
- Register stories
- Track step status
- Query pending stories
- Maintain history
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PrismQ.Pipeline.orchestration.story_db import StoryDatabase


class TestStoryDatabase:
    """Test cases for StoryDatabase."""
    
    def setup_method(self):
        """Set up test environment."""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_url = f"sqlite:///{self.temp_db.name}"
        
    def test_sqlite_initialization(self):
        """Test that SQLite database initializes correctly."""
        db = StoryDatabase(db_url=self.db_url)
        db.initialize()
        
        assert db.db_path.exists()
        
        # Check tables were created
        cursor = db.connection.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('stories', 'step_status', 'step_history')
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        assert "stories" in tables
        assert "step_status" in tables
        assert "step_history" in tables
        
        db.close()
        print("✓ SQLite initialization test passed")
    
    def test_register_story(self):
        """Test registering a story."""
        db = StoryDatabase(db_url=self.db_url)
        db.initialize()
        
        story_id = db.register_story(
            "TEST-001",
            title="Test Story",
            source="test",
            metadata={"key": "value"}
        )
        
        assert story_id == "TEST-001"
        
        # Verify in database
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM stories WHERE story_id = ?", (story_id,))
        row = cursor.fetchone()
        
        assert row is not None
        assert dict(row)["story_id"] == "TEST-001"
        assert dict(row)["title"] == "Test Story"
        
        db.close()
        print("✓ Register story test passed")
    
    def test_update_step_status(self):
        """Test updating step status."""
        db = StoryDatabase(db_url=self.db_url)
        db.initialize()
        
        story_id = db.register_story("TEST-002")
        
        # Update to running
        db.update_step_status(story_id, "01_ingest", "running", run_id="run-001")
        
        # Update to completed
        db.update_step_status(story_id, "01_ingest", "completed", run_id="run-001", 
                            acceptance_passed=True, acceptance_details="All checks passed")
        
        # Verify
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM step_status WHERE story_id = ?", (story_id,))
        row = cursor.fetchone()
        
        assert row is not None
        row_dict = dict(row)
        assert row_dict["status"] == "completed"
        assert row_dict["acceptance_passed"] == 1
        
        db.close()
        print("✓ Update step status test passed")
    
    def test_add_step_history(self):
        """Test adding step history."""
        db = StoryDatabase(db_url=self.db_url)
        db.initialize()
        
        story_id = db.register_story("TEST-003")
        
        # Add history entries
        db.add_step_history(story_id, "01_ingest", "run-001", "completed", execution_time_ms=1500)
        db.add_step_history(story_id, "01_ingest", "run-002", "completed", execution_time_ms=1200)
        
        # Verify
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM step_history WHERE story_id = ?", (story_id,))
        rows = cursor.fetchall()
        
        assert len(rows) == 2
        
        db.close()
        print("✓ Add step history test passed")
    
    def test_get_pending_stories_first_step(self):
        """Test getting pending stories for first step."""
        db = StoryDatabase(db_url=self.db_url)
        db.initialize()
        
        # Register stories
        db.register_story("PENDING-001")
        db.register_story("PENDING-002")
        
        # Mark one as completed
        db.update_step_status("PENDING-002", "01_ingest", "completed")
        
        # Get pending
        pending = db.get_pending_stories("01_ingest")
        
        assert "PENDING-001" in pending
        assert "PENDING-002" not in pending
        
        db.close()
        print("✓ Get pending stories (first step) test passed")
    
    def test_get_pending_stories_subsequent_step(self):
        """Test getting pending stories for subsequent steps."""
        db = StoryDatabase(db_url=self.db_url)
        db.initialize()
        
        # Register stories
        db.register_story("STORY-A")
        db.register_story("STORY-B")
        db.register_story("STORY-C")
        
        # Complete step 1 for all
        db.update_step_status("STORY-A", "01_ingest", "completed")
        db.update_step_status("STORY-B", "01_ingest", "completed")
        db.update_step_status("STORY-C", "01_ingest", "completed")
        
        # Complete step 2 for one
        db.update_step_status("STORY-B", "02_preprocess", "completed")
        
        # Get pending for step 2
        pending = db.get_pending_stories("02_preprocess")
        
        assert "STORY-A" in pending
        assert "STORY-B" not in pending  # Already completed
        assert "STORY-C" in pending
        
        db.close()
        print("✓ Get pending stories (subsequent step) test passed")
    
    def test_get_story_status(self):
        """Test getting story status."""
        db = StoryDatabase(db_url=self.db_url)
        db.initialize()
        
        story_id = db.register_story("STATUS-TEST", title="Status Test")
        db.update_step_status(story_id, "01_ingest", "completed")
        db.update_step_status(story_id, "02_preprocess", "running")
        
        status = db.get_story_status(story_id)
        
        assert status is not None
        assert status["story"]["story_id"] == story_id
        assert len(status["steps"]) == 2
        
        db.close()
        print("✓ Get story status test passed")
    
    def test_get_step_statistics(self):
        """Test getting step statistics."""
        db = StoryDatabase(db_url=self.db_url)
        db.initialize()
        
        # Create test data
        for i in range(5):
            story_id = db.register_story(f"STATS-{i}")
            db.update_step_status(story_id, "01_ingest", "completed")
        
        for i in range(3):
            story_id = f"STATS-{i}"
            db.update_step_status(story_id, "02_preprocess", "completed")
        
        stats = db.get_step_statistics()
        
        assert "01_ingest" in stats
        assert stats["01_ingest"]["completed"] == 5
        assert "02_preprocess" in stats
        assert stats["02_preprocess"]["completed"] == 3
        
        db.close()
        print("✓ Get step statistics test passed")
    
    def test_context_manager(self):
        """Test database context manager."""
        with StoryDatabase(db_url=self.db_url) as db:
            db.initialize()
            db.register_story("CTX-TEST")
        
        # Database should be closed
        assert db.connection is None
        
        print("✓ Context manager test passed")


def run_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Pipeline Story Database Tests")
    print("=" * 60 + "\n")
    
    test_suite = TestStoryDatabase()
    
    tests = [
        test_suite.test_sqlite_initialization,
        test_suite.test_register_story,
        test_suite.test_update_step_status,
        test_suite.test_add_step_history,
        test_suite.test_get_pending_stories_first_step,
        test_suite.test_get_pending_stories_subsequent_step,
        test_suite.test_get_story_status,
        test_suite.test_get_step_statistics,
        test_suite.test_context_manager,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test_suite.setup_method()  # Reset for each test
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        finally:
            # Cleanup
            if hasattr(test_suite, 'temp_db') and test_suite.temp_db:
                try:
                    os.unlink(test_suite.temp_db.name)
                except:
                    pass
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
