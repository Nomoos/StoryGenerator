#!/usr/bin/env python3
"""
Test suite for the source attribution generator.

Tests attribution metadata creation, file generation, and processing.
"""

import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime
import sys

# Add scripts directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate_attribution import (
    determine_license,
    determine_usage_rights,
    create_attribution_metadata,
    save_attribution_file,
    process_reddit_story
)


class TestAttributionGenerator(unittest.TestCase):
    """Test cases for attribution generator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_story = {
            "id": "test123",
            "title": "Test Story Title",
            "text": "Test story content",
            "url": "https://reddit.com/r/test/comments/test123",
            "upvotes": 100,
            "num_comments": 50,
            "created_utc": "2024-01-15T10:00:00Z",
            "subreddit": "r/test",
            "author": "test_user",
            "awards": 2
        }
    
    def test_determine_license_reddit(self):
        """Test license determination for Reddit sources."""
        license_text = determine_license("reddit", "relationships")
        self.assertIn("Reddit User Agreement", license_text)
        self.assertIn("Fair Use", license_text)
    
    def test_determine_license_twitter(self):
        """Test license determination for Twitter sources."""
        license_text = determine_license("twitter")
        self.assertIn("Twitter", license_text)
        self.assertIn("Fair Use", license_text)
    
    def test_determine_usage_rights_reddit(self):
        """Test usage rights determination for Reddit."""
        rights = determine_usage_rights("reddit")
        self.assertIn("Transformative", rights)
        self.assertIn("attribution", rights.lower())
    
    def test_create_attribution_metadata(self):
        """Test creation of attribution metadata."""
        attribution = create_attribution_metadata(
            content_id="test123",
            source_url="https://reddit.com/r/test/comments/test123",
            author="test_user",
            source_type="reddit",
            subreddit="test",
            scraped_date="2024-01-15T10:00:00Z"
        )
        
        # Check required fields
        self.assertEqual(attribution["content_id"], "test123")
        self.assertEqual(attribution["source_url"], "https://reddit.com/r/test/comments/test123")
        self.assertEqual(attribution["author"], "test_user")
        self.assertEqual(attribution["source_type"], "reddit")
        self.assertEqual(attribution["subreddit"], "test")
        
        # Check generated fields
        self.assertIn("license", attribution)
        self.assertIn("date_scraped", attribution)
        self.assertIn("usage_rights", attribution)
        self.assertIn("attribution_generated", attribution)
    
    def test_create_attribution_metadata_with_additional_info(self):
        """Test creation of attribution with additional metadata."""
        additional_info = {
            "title": "Test Title",
            "upvotes": 100,
            "awards": 5
        }
        
        attribution = create_attribution_metadata(
            content_id="test123",
            source_url="https://reddit.com/test",
            author="test_user",
            additional_metadata=additional_info
        )
        
        self.assertIn("additional_info", attribution)
        self.assertEqual(attribution["additional_info"]["title"], "Test Title")
        self.assertEqual(attribution["additional_info"]["upvotes"], 100)
    
    def test_save_attribution_file(self):
        """Test saving attribution data to file."""
        attribution_data = {
            "content_id": "test123",
            "source_url": "https://reddit.com/test",
            "author": "test_user"
        }
        
        output_dir = Path(self.temp_dir) / "test_output"
        filepath = save_attribution_file(attribution_data, output_dir, "test123")
        
        # Check file was created
        self.assertTrue(filepath.exists())
        self.assertEqual(filepath.name, "attribution_test123.json")
        
        # Check file contents
        with open(filepath, 'r') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data["content_id"], "test123")
        self.assertEqual(loaded_data["author"], "test_user")
    
    def test_process_reddit_story(self):
        """Test processing a Reddit story to generate attribution."""
        output_dir = Path(self.temp_dir)
        
        filepath = process_reddit_story(
            self.test_story,
            "women",
            "18-23",
            output_dir
        )
        
        # Check file was created in correct location
        self.assertTrue(filepath.exists())
        expected_path = output_dir / "sources" / "reddit" / "women" / "18-23"
        self.assertTrue(str(filepath).startswith(str(expected_path)))
        
        # Check file contents
        with open(filepath, 'r') as f:
            attribution = json.load(f)
        
        self.assertEqual(attribution["content_id"], "test123")
        self.assertEqual(attribution["author"], "test_user")
        self.assertEqual(attribution["source_type"], "reddit")
        self.assertIn("additional_info", attribution)
        self.assertEqual(attribution["additional_info"]["title"], "Test Story Title")
    
    def test_attribution_preserves_deleted_author(self):
        """Test that deleted authors are properly handled."""
        story_deleted = self.test_story.copy()
        story_deleted["author"] = "[deleted]"
        
        attribution = create_attribution_metadata(
            content_id="test123",
            source_url="https://reddit.com/test",
            author=story_deleted["author"]
        )
        
        self.assertEqual(attribution["author"], "[deleted]")
    
    def test_attribution_date_formats(self):
        """Test that attribution dates are in ISO-8601 format."""
        attribution = create_attribution_metadata(
            content_id="test123",
            source_url="https://reddit.com/test",
            author="test_user"
        )
        
        # Check date format
        date_str = attribution["attribution_generated"]
        self.assertTrue(date_str.endswith("Z"))
        
        # Verify it can be parsed
        try:
            datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            date_valid = True
        except ValueError:
            date_valid = False
        
        self.assertTrue(date_valid, "Date should be valid ISO-8601 format")


class TestAttributionIntegration(unittest.TestCase):
    """Integration tests for attribution system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def test_full_workflow(self):
        """Test complete workflow from scraped data to attribution files."""
        # Create sample scraped data file
        scraped_data = {
            "segment": "women",
            "age_bucket": "18-23",
            "subreddits": ["r/relationships"],
            "total_scraped": 3,
            "selected": 3,
            "scraped_at": "2024-01-15T10:00:00Z",
            "stories": [
                {
                    "id": "story1",
                    "title": "Story 1",
                    "url": "https://reddit.com/r/relationships/comments/story1",
                    "author": "user1",
                    "upvotes": 100,
                    "num_comments": 50,
                    "created_utc": "2024-01-15T09:00:00Z",
                    "subreddit": "r/relationships"
                },
                {
                    "id": "story2",
                    "title": "Story 2",
                    "url": "https://reddit.com/r/relationships/comments/story2",
                    "author": "user2",
                    "upvotes": 200,
                    "num_comments": 75,
                    "created_utc": "2024-01-15T08:00:00Z",
                    "subreddit": "r/relationships"
                }
            ]
        }
        
        # Save scraped data to file
        input_file = Path(self.temp_dir) / "reddit_scraped_women_18-23.json"
        with open(input_file, 'w') as f:
            json.dump(scraped_data, f)
        
        # Process the file
        from generate_attribution import process_scraped_content_file
        
        output_dir = Path(self.temp_dir) / "output"
        created_files = process_scraped_content_file(input_file, output_dir)
        
        # Verify files were created
        self.assertEqual(len(created_files), 2)
        
        # Verify each file exists and has correct content
        for filepath in created_files:
            self.assertTrue(filepath.exists())
            
            with open(filepath, 'r') as f:
                attribution = json.load(f)
            
            # Check required fields exist
            self.assertIn("content_id", attribution)
            self.assertIn("source_url", attribution)
            self.assertIn("author", attribution)
            self.assertIn("license", attribution)
            self.assertIn("usage_rights", attribution)


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("SOURCE ATTRIBUTION GENERATOR - TEST SUITE")
    print("=" * 60)
    
    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAttributionGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestAttributionIntegration))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 60 + "\n")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit(main())
