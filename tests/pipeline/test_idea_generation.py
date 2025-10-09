"""
Unit tests for idea generation module.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock

from core.pipeline.idea_generation import (
    IdeaAdapter,
    IdeaGenerator,
    merge_and_save_all_ideas
)


class TestIdeaAdapter:
    """Tests for IdeaAdapter class."""
    
    def test_init(self):
        """Test IdeaAdapter initialization."""
        mock_llm = Mock()
        mock_llm.model_name = "test-model"
        
        adapter = IdeaAdapter(mock_llm)
        
        assert adapter.llm == mock_llm
    
    def test_adapt_story_success(self):
        """Test successful story adaptation."""
        mock_llm = Mock()
        mock_llm.model_name = "test-model"
        mock_llm.generate_completion.return_value = "This is an adapted video idea."
        
        adapter = IdeaAdapter(mock_llm)
        
        story = {
            "id": "test123",
            "title": "Test Story",
            "selftext": "Story content here",
            "url": "https://reddit.com/test",
            "score": 100,
            "subreddit": "testsubreddit"
        }
        
        result = adapter.adapt_story(story, "women", "18-23")
        
        assert result["id"] == "reddit_test123"
        assert result["source"] == "reddit_adapted"
        assert result["content"] == "This is an adapted video idea."
        assert result["target_gender"] == "women"
        assert result["target_age"] == "18-23"
        assert result["original_title"] == "Test Story"
        assert result["metadata"]["score"] == 100
        
        mock_llm.generate_completion.assert_called_once()
    
    def test_adapt_stories_multiple(self):
        """Test adapting multiple stories."""
        mock_llm = Mock()
        mock_llm.model_name = "test-model"
        mock_llm.generate_completion.side_effect = [
            "Idea 1",
            "Idea 2",
            "Idea 3"
        ]
        
        adapter = IdeaAdapter(mock_llm)
        
        stories = [
            {"id": "1", "title": "Story 1", "selftext": "Content 1"},
            {"id": "2", "title": "Story 2", "selftext": "Content 2"},
            {"id": "3", "title": "Story 3", "selftext": "Content 3"},
        ]
        
        result = adapter.adapt_stories(stories, "men", "24-29")
        
        assert len(result) == 3
        assert result[0]["content"] == "Idea 1"
        assert result[1]["content"] == "Idea 2"
        assert result[2]["content"] == "Idea 3"
        assert mock_llm.generate_completion.call_count == 3
    
    def test_save_ideas(self, tmp_path):
        """Test saving ideas to file."""
        mock_llm = Mock()
        adapter = IdeaAdapter(mock_llm)
        
        ideas = [
            {"id": "1", "content": "Idea 1"},
            {"id": "2", "content": "Idea 2"}
        ]
        
        output_path = adapter.save_ideas(ideas, tmp_path)
        
        assert output_path.exists()
        assert output_path.name == "reddit_adapted.json"
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 2
        assert data[0]["id"] == "1"


class TestIdeaGenerator:
    """Tests for IdeaGenerator class."""
    
    def test_init(self):
        """Test IdeaGenerator initialization."""
        mock_llm = Mock()
        mock_llm.model_name = "test-model"
        
        generator = IdeaGenerator(mock_llm)
        
        assert generator.llm == mock_llm
    
    def test_generate_ideas_success(self):
        """Test successful idea generation."""
        mock_llm = Mock()
        mock_llm.model_name = "test-model"
        mock_llm.generate_completion.return_value = """1. First video idea about relationships
2. Second video idea about career
3. Third video idea about personal growth"""
        
        generator = IdeaGenerator(mock_llm)
        
        result = generator.generate_ideas("women", "18-23", count=3)
        
        assert len(result) == 3
        assert result[0]["id"] == "llm_001"
        assert result[0]["source"] == "llm_generated"
        assert "relationships" in result[0]["content"].lower()
        assert result[1]["id"] == "llm_002"
        assert "career" in result[1]["content"].lower()
        
        mock_llm.generate_completion.assert_called_once()
    
    def test_parse_ideas_various_formats(self):
        """Test parsing ideas from different formats."""
        mock_llm = Mock()
        mock_llm.model_name = "test-model"
        
        generator = IdeaGenerator(mock_llm)
        
        # Test with numbered list
        response = """1. First idea here
2. Second idea here
3. Third idea here"""
        
        result = generator._parse_ideas(response, "women", "18-23")
        
        assert len(result) == 3
        assert "First idea here" in result[0]["content"]
        assert "Second idea here" in result[1]["content"]
    
    def test_save_ideas(self, tmp_path):
        """Test saving generated ideas to file."""
        mock_llm = Mock()
        generator = IdeaGenerator(mock_llm)
        
        ideas = [
            {"id": "llm_001", "content": "Idea 1"},
            {"id": "llm_002", "content": "Idea 2"}
        ]
        
        output_path = generator.save_ideas(ideas, tmp_path)
        
        assert output_path.exists()
        assert output_path.name == "llm_generated.json"
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 2


class TestMergeAndSaveAllIdeas:
    """Tests for merge_and_save_all_ideas function."""
    
    def test_merge_ideas(self, tmp_path):
        """Test merging adapted and generated ideas."""
        adapted = [
            {"id": "reddit_1", "source": "reddit_adapted"}
        ]
        generated = [
            {"id": "llm_001", "source": "llm_generated"},
            {"id": "llm_002", "source": "llm_generated"}
        ]
        
        output_path = merge_and_save_all_ideas(adapted, generated, tmp_path)
        
        assert output_path.exists()
        assert output_path.name == "all_ideas.json"
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert data["total_count"] == 3
        assert data["adapted_count"] == 1
        assert data["generated_count"] == 2
        assert len(data["ideas"]) == 3
