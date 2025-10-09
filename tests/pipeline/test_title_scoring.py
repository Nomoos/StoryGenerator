"""
Unit tests for title scoring module.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import json

from core.pipeline.title_scoring import TitleScorer


class TestTitleScorer:
    """Tests for TitleScorer class."""
    
    def test_init_with_default_config(self):
        """Test TitleScorer initialization with default config."""
        scorer = TitleScorer()
        
        assert scorer.config is not None
        assert 'viral' in scorer.config
        assert 'thresholds' in scorer.config
    
    def test_score_title_basic(self):
        """Test basic title scoring."""
        scorer = TitleScorer()
        
        title = {
            "id": "test_title_01",
            "text": "Why nobody tells you about this shocking secret?",
            "topic_id": "topic_01"
        }
        
        result = scorer.score_title(title)
        
        assert "score" in result
        assert "score_breakdown" in result
        assert "score_tier" in result
        assert 0 <= result["score"] <= 100
        assert len(result["score_breakdown"]) == 5  # 5 dimensions
    
    def test_score_novelty(self):
        """Test novelty scoring."""
        scorer = TitleScorer()
        
        # High novelty (secret, specific number)
        high_score = scorer._score_novelty("The 3 secrets nobody told me about")
        
        # Low novelty (generic)
        low_score = scorer._score_novelty("Some things about stuff")
        
        assert high_score > low_score
        assert 0 <= high_score <= 100
        assert 0 <= low_score <= 100
    
    def test_score_emotional(self):
        """Test emotional impact scoring."""
        scorer = TitleScorer()
        
        # High emotion (shocking + question)
        high_score = scorer._score_emotional("Why this shocking discovery changed everything?")
        
        # Low emotion (neutral)
        low_score = scorer._score_emotional("A regular day at work")
        
        assert high_score > low_score
    
    def test_score_clarity(self):
        """Test clarity scoring."""
        scorer = TitleScorer()
        
        # Good clarity (ideal length, clear)
        good_score = scorer._score_clarity("How I learned to overcome my biggest fear")
        
        # Poor clarity (too short)
        poor_score = scorer._score_clarity("Thing")
        
        assert good_score > poor_score
    
    def test_score_replay(self):
        """Test replay value scoring."""
        scorer = TitleScorer()
        
        # High replay (list format, lesson)
        high_score = scorer._score_replay("5 things I learned about success")
        
        # Low replay (one-time)
        low_score = scorer._score_replay("I went to the store today")
        
        assert high_score > low_score
    
    def test_score_shareability(self):
        """Test shareability scoring."""
        scorer = TitleScorer()
        
        # High shareability (question, relatable topic)
        high_score = scorer._score_shareability("Why do all relationships end like this?")
        
        # Low shareability (personal, not relatable)
        low_score = scorer._score_shareability("My specific thing happened")
        
        assert high_score > low_score
    
    def test_score_tier_excellent(self):
        """Test score tier classification for excellent scores."""
        scorer = TitleScorer()
        
        tier = scorer._get_score_tier(90.0)
        assert tier == "excellent"
    
    def test_score_tier_good(self):
        """Test score tier classification for good scores."""
        scorer = TitleScorer()
        
        tier = scorer._get_score_tier(75.0)
        assert tier == "good"
    
    def test_score_tier_acceptable(self):
        """Test score tier classification for acceptable scores."""
        scorer = TitleScorer()
        
        tier = scorer._get_score_tier(60.0)
        assert tier == "acceptable"
    
    def test_score_tier_poor(self):
        """Test score tier classification for poor scores."""
        scorer = TitleScorer()
        
        tier = scorer._get_score_tier(45.0)
        assert tier == "poor"
    
    def test_score_all_titles(self):
        """Test scoring multiple titles."""
        scorer = TitleScorer()
        
        titles_by_topic = {
            "topic_01": [
                {"id": "t1", "text": "Amazing discovery revealed!"},
                {"id": "t2", "text": "5 shocking truths about life"}
            ],
            "topic_02": [
                {"id": "t3", "text": "Why nobody told me this?"}
            ]
        }
        
        result = scorer.score_all_titles(titles_by_topic)
        
        assert len(result) == 2
        assert len(result["topic_01"]) == 2
        assert len(result["topic_02"]) == 1
        assert all("score" in title for titles in result.values() for title in titles)
    
    def test_save_scored_titles(self, tmp_path):
        """Test saving scored titles to file."""
        scorer = TitleScorer()
        
        scored_titles = {
            "topic_01": [
                {
                    "id": "t1",
                    "text": "Test title",
                    "score": 75.5,
                    "score_tier": "good"
                }
            ]
        }
        
        output_path = scorer.save_scored_titles(scored_titles, tmp_path)
        
        assert output_path.exists()
        assert output_path.name == "titles_scored.json"
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert data["total_titles"] == 1
        assert data["total_topics"] == 1
        assert "average_score" in data
