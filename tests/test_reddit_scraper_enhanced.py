#!/usr/bin/env python3
"""
Tests for Enhanced Reddit Scraper features.
Tests incremental scraping, duplicate tracking, and rate limiting.
"""

import json
import os
import sqlite3
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
import reddit_scraper


class TestDuplicateTracker:
    """Tests for the DuplicateTracker class."""

    def test_init_creates_database(self):
        """Test that DuplicateTracker creates database on init."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_duplicates.db"
            tracker = reddit_scraper.DuplicateTracker(db_path)
            
            assert db_path.exists()
            
            # Check schema
            conn = sqlite3.connect(db_path)
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='seen_posts'"
            )
            assert cursor.fetchone() is not None
            conn.close()

    def test_is_duplicate_first_time(self):
        """Test that first occurrence is not marked as duplicate."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_duplicates.db"
            tracker = reddit_scraper.DuplicateTracker(db_path)
            
            is_dup = tracker.is_duplicate("post_123", "Test Title", "r/test")
            assert is_dup is False

    def test_is_duplicate_second_time(self):
        """Test that second occurrence is marked as duplicate."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_duplicates.db"
            tracker = reddit_scraper.DuplicateTracker(db_path)
            
            # First time
            tracker.is_duplicate("post_123", "Test Title", "r/test")
            
            # Second time
            is_dup = tracker.is_duplicate("post_123", "Test Title", "r/test")
            assert is_dup is True

    def test_get_stats(self):
        """Test that stats are correctly calculated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_duplicates.db"
            tracker = reddit_scraper.DuplicateTracker(db_path)
            
            # Add some posts
            tracker.is_duplicate("post_1", "Title 1", "r/test")
            tracker.is_duplicate("post_2", "Title 2", "r/test")
            tracker.is_duplicate("post_1", "Title 1", "r/test")  # Duplicate
            
            stats = tracker.get_stats()
            assert stats["total_seen"] == 2
            assert stats["avg_scrapes"] == 1.5  # (1+2)/2


class TestScraperState:
    """Tests for the ScraperState class."""

    def test_init_creates_state_file(self):
        """Test that ScraperState creates state file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "test_state.json"
            state = reddit_scraper.ScraperState(state_file)
            
            # Initially should be empty
            assert state.last_scraped == {}

    def test_save_and_load_state(self):
        """Test that state is persisted correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "test_state.json"
            
            # Save state
            state1 = reddit_scraper.ScraperState(state_file)
            state1.update_scrape_time("r/test", 1234567890.0)
            
            # Load state in new instance
            state2 = reddit_scraper.ScraperState(state_file)
            assert state2.get_last_scrape_time("r/test") == 1234567890.0

    def test_get_last_scrape_time_default(self):
        """Test that default is 0 for unseen subreddit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "test_state.json"
            state = reddit_scraper.ScraperState(state_file)
            
            assert state.get_last_scrape_time("r/unseen") == 0


class TestRateLimiting:
    """Tests for rate limiting decorator."""

    def test_rate_limit_success_on_first_try(self):
        """Test that function succeeds normally."""
        @reddit_scraper.rate_limit_with_backoff(max_retries=3, base_delay=1)
        def test_func():
            return "success"
        
        result = test_func()
        assert result == "success"

    def test_rate_limit_retries_on_rate_limit_error(self):
        """Test that function retries on rate limit error."""
        from praw.exceptions import PRAWException
        
        call_count = [0]
        
        @reddit_scraper.rate_limit_with_backoff(max_retries=3, base_delay=0.1)
        def test_func():
            call_count[0] += 1
            if call_count[0] < 2:
                raise PRAWException("429 Rate limit exceeded")
            return "success"
        
        result = test_func()
        assert result == "success"
        assert call_count[0] == 2

    def test_rate_limit_gives_up_after_max_retries(self):
        """Test that function gives up after max retries."""
        from praw.exceptions import PRAWException
        
        @reddit_scraper.rate_limit_with_backoff(max_retries=2, base_delay=0.1)
        def test_func():
            raise PRAWException("429 Rate limit exceeded")
        
        with pytest.raises(PRAWException):
            test_func()


class TestQualityThresholds:
    """Tests for quality thresholds."""

    def test_quality_thresholds_exist_for_all_age_buckets(self):
        """Test that thresholds are defined for all age buckets."""
        ages = ["10-13", "14-17", "18-23"]
        
        for age in ages:
            assert age in reddit_scraper.QUALITY_THRESHOLDS
            thresholds = reddit_scraper.QUALITY_THRESHOLDS[age]
            assert "min_upvotes" in thresholds
            assert "min_comments" in thresholds
            assert "min_text_length" in thresholds

    def test_quality_thresholds_increase_with_age(self):
        """Test that thresholds generally increase with age."""
        threshold_10_13 = reddit_scraper.QUALITY_THRESHOLDS["10-13"]
        threshold_14_17 = reddit_scraper.QUALITY_THRESHOLDS["14-17"]
        threshold_18_23 = reddit_scraper.QUALITY_THRESHOLDS["18-23"]
        
        # Upvotes should increase
        assert threshold_10_13["min_upvotes"] <= threshold_14_17["min_upvotes"]
        assert threshold_14_17["min_upvotes"] <= threshold_18_23["min_upvotes"]


class TestFilterAgeAppropriate:
    """Tests for enhanced filter_age_appropriate function."""

    def test_filter_with_quality_threshold(self):
        """Test filtering with quality threshold enabled."""
        stories = [
            {"id": "1", "title": "Good story", "text": "A" * 150},  # Long enough for 10-13
            {"id": "2", "title": "Short story", "text": "Too short"},  # Too short
            {"id": "3", "title": "Another good", "text": "B" * 200},  # Long enough
        ]
        
        filtered = reddit_scraper.filter_age_appropriate(
            stories, "10-13", apply_quality_threshold=True
        )
        
        # Should filter out the short story
        assert len(filtered) == 2
        assert filtered[0]["id"] == "1"
        assert filtered[1]["id"] == "3"

    def test_filter_without_quality_threshold(self):
        """Test filtering without quality threshold (backward compatible)."""
        stories = [
            {"id": "1", "title": "Good story", "text": "Short"},
            {"id": "2", "title": "NSFW story", "text": "Contains nsfw content"},
            {"id": "3", "title": "Another good", "text": "Also short"},
        ]
        
        filtered = reddit_scraper.filter_age_appropriate(stories, "10-13")
        
        # Should only filter NSFW, not by length
        assert len(filtered) == 2
        assert filtered[0]["id"] == "1"
        assert filtered[1]["id"] == "3"

    def test_filter_with_explicit_min_text_length(self):
        """Test filtering with explicit min_text_length parameter."""
        stories = [
            {"id": "1", "title": "Story", "text": "A" * 50},
            {"id": "2", "title": "Story", "text": "B" * 100},
            {"id": "3", "title": "Story", "text": "C" * 150},
        ]
        
        filtered = reddit_scraper.filter_age_appropriate(
            stories, "18-23", min_text_length=75
        )
        
        # Should filter out story 1 (< 75 chars)
        assert len(filtered) == 2
        assert filtered[0]["id"] == "2"
        assert filtered[1]["id"] == "3"


class TestCommandLineArguments:
    """Tests for command-line argument parsing."""

    @patch('reddit_scraper.init_reddit')
    @patch('reddit_scraper.scrape_segment')
    def test_cli_segment_and_age_arguments(self, mock_scrape, mock_init):
        """Test that --segment and --age arguments work."""
        mock_init.return_value = Mock()
        mock_scrape.return_value = {
            "segment": "women",
            "age_bucket": "18-23",
            "stories": []
        }
        
        # This would normally be tested with subprocess, but we'll test argument parsing
        # by checking that the right parameters are passed to scrape_segment
        # In a real test, you'd use subprocess to test the CLI
        pass  # CLI integration test would go here


def run_all_tests():
    """Run all tests using pytest."""
    print("\n" + "="*60)
    print("Running Enhanced Reddit Scraper Tests")
    print("="*60)
    print()
    
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_all_tests()
