"""
Unit tests for top selection module.
"""

import pytest
import json
from pathlib import Path

from core.pipeline.top_selection import TopSelector


class TestTopSelector:
    """Tests for TopSelector class."""
    
    def test_init(self):
        """Test TopSelector initialization."""
        selector = TopSelector()
        assert selector is not None
    
    def test_select_top_titles_basic(self):
        """Test basic top title selection."""
        selector = TopSelector()
        
        titles_by_topic = {
            "topic_01": [
                {"id": "t1", "text": "Title 1", "score": 85, "topic_id": "topic_01"},
                {"id": "t2", "text": "Title 2", "score": 75, "topic_id": "topic_01"}
            ],
            "topic_02": [
                {"id": "t3", "text": "Title 3", "score": 90, "topic_id": "topic_02"},
                {"id": "t4", "text": "Title 4", "score": 60, "topic_id": "topic_02"}
            ]
        }
        
        result = selector.select_top_titles(titles_by_topic, top_n=3, min_score=55)
        
        assert len(result) <= 3
        assert all(title["score"] >= 55 for title in result)
        # Should be sorted by score descending
        if len(result) > 1:
            assert result[0]["score"] >= result[1]["score"]
    
    def test_select_top_titles_filters_low_scores(self):
        """Test that low-scoring titles are filtered out."""
        selector = TopSelector()
        
        titles_by_topic = {
            "topic_01": [
                {"id": "t1", "text": "Title 1", "score": 85, "topic_id": "topic_01"},
                {"id": "t2", "text": "Title 2", "score": 40, "topic_id": "topic_01"},  # Too low
                {"id": "t3", "text": "Title 3", "score": 30, "topic_id": "topic_01"}   # Too low
            ]
        }
        
        result = selector.select_top_titles(titles_by_topic, top_n=5, min_score=50)
        
        assert len(result) == 1
        assert result[0]["score"] == 85
    
    def test_select_with_diversity(self):
        """Test selection with topic diversity."""
        selector = TopSelector()
        
        # Create titles from different topics
        titles = [
            {"id": "t1", "score": 95, "topic_id": "topic_01"},
            {"id": "t2", "score": 94, "topic_id": "topic_01"},  # Same topic as t1
            {"id": "t3", "score": 93, "topic_id": "topic_02"},
            {"id": "t4", "score": 92, "topic_id": "topic_03"},
            {"id": "t5", "score": 91, "topic_id": "topic_04"}
        ]
        
        result = selector._select_with_diversity(titles, top_n=3)
        
        assert len(result) <= 3
        # Should try to select from different topics first
        topic_ids = [t["topic_id"] for t in result]
        assert len(set(topic_ids)) >= 2  # At least 2 different topics
    
    def test_select_per_segment(self):
        """Test selecting top titles per segment."""
        selector = TopSelector()
        
        titles_by_segment = {
            "women_18-23": {
                "topic_01": [
                    {"id": "t1", "score": 85, "topic_id": "topic_01"},
                    {"id": "t2", "score": 75, "topic_id": "topic_01"}
                ]
            },
            "men_18-23": {
                "topic_02": [
                    {"id": "t3", "score": 90, "topic_id": "topic_02"},
                    {"id": "t4", "score": 80, "topic_id": "topic_02"}
                ]
            }
        }
        
        result = selector.select_per_segment(titles_by_segment, top_n_per_segment=2)
        
        assert len(result) == 2
        assert "women_18-23" in result
        assert "men_18-23" in result
        assert len(result["women_18-23"]) <= 2
        assert len(result["men_18-23"]) <= 2
    
    def test_save_selected_titles(self, tmp_path):
        """Test saving selected titles to file."""
        selector = TopSelector()
        
        selected_titles = [
            {
                "id": "t1",
                "text": "Top title 1",
                "score": 90,
                "score_tier": "excellent",
                "topic_id": "topic_01"
            },
            {
                "id": "t2",
                "text": "Top title 2",
                "score": 85,
                "score_tier": "excellent",
                "topic_id": "topic_02"
            }
        ]
        
        output_path = selector.save_selected_titles(
            selected_titles,
            tmp_path,
            "women",
            "18-23"
        )
        
        assert output_path.exists()
        assert output_path.name == "top_5_titles.json"
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert data["total_selected"] == 2
        assert data["segment"]["gender"] == "women"
        assert data["segment"]["age_bucket"] == "18-23"
        assert data["topics_represented"] == 2
        assert len(data["titles"]) == 2
    
    def test_generate_summary_report(self, tmp_path):
        """Test generating summary report."""
        selector = TopSelector()
        
        selected_by_segment = {
            "women_18-23": [
                {
                    "id": "t1",
                    "score": 90,
                    "score_tier": "excellent",
                    "voice_recommendation": {"gender": "female"}
                },
                {
                    "id": "t2",
                    "score": 85,
                    "score_tier": "excellent",
                    "voice_recommendation": {"gender": "female"}
                }
            ],
            "men_18-23": [
                {
                    "id": "t3",
                    "score": 75,
                    "score_tier": "good",
                    "voice_recommendation": {"gender": "male"}
                }
            ]
        }
        
        output_path = selector.generate_summary_report(selected_by_segment, tmp_path)
        
        assert output_path.exists()
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert data["summary"]["total_segments"] == 2
        assert data["summary"]["total_titles_selected"] == 3
        assert "average_score" in data["summary"]
        assert "score_distribution" in data["summary"]
        assert "voice_gender_distribution" in data["summary"]
        assert "by_segment" in data
        assert "women_18-23" in data["by_segment"]
        assert "men_18-23" in data["by_segment"]
    
    def test_select_empty_titles(self):
        """Test selection with no titles."""
        selector = TopSelector()
        
        result = selector.select_top_titles({}, top_n=5)
        
        assert result == []
    
    def test_select_all_below_threshold(self):
        """Test selection when all titles below minimum score."""
        selector = TopSelector()
        
        titles_by_topic = {
            "topic_01": [
                {"id": "t1", "score": 30},
                {"id": "t2", "score": 40}
            ]
        }
        
        result = selector.select_top_titles(titles_by_topic, top_n=5, min_score=50)
        
        assert result == []
