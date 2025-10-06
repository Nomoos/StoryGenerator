"""
Unit tests for the social_trends package.

Run with: python -m pytest social_trends/tests/
"""

import unittest
from datetime import datetime, timedelta

from social_trends.interfaces import TrendItem, TrendType
from social_trends.utils.keywords import KeywordExtractor
from social_trends.utils.scoring import TrendScorer


class TestTrendItem(unittest.TestCase):
    """Test TrendItem dataclass"""
    
    def test_creation(self):
        """Test basic TrendItem creation"""
        item = TrendItem(
            id="test_1",
            title_or_keyword="Test Trend",
            type=TrendType.VIDEO,
            source="youtube",
            score=75.5
        )
        
        self.assertEqual(item.id, "test_1")
        self.assertEqual(item.title_or_keyword, "Test Trend")
        self.assertEqual(item.type, TrendType.VIDEO)
        self.assertEqual(item.source, "youtube")
        self.assertEqual(item.score, 75.5)
    
    def test_score_normalization(self):
        """Test that score is normalized to 0-100 range"""
        item1 = TrendItem(
            id="test_1",
            title_or_keyword="Test",
            type=TrendType.VIDEO,
            source="youtube",
            score=150.0  # Over 100
        )
        self.assertEqual(item1.score, 100.0)
        
        item2 = TrendItem(
            id="test_2",
            title_or_keyword="Test",
            type=TrendType.VIDEO,
            source="youtube",
            score=-10.0  # Below 0
        )
        self.assertEqual(item2.score, 0.0)
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        item = TrendItem(
            id="test_1",
            title_or_keyword="Test Trend",
            type=TrendType.KEYWORD,
            source="google_trends",
            score=80.0,
            region="US",
            locale="en-US"
        )
        
        d = item.to_dict()
        
        self.assertEqual(d["id"], "test_1")
        self.assertEqual(d["type"], "keyword")
        self.assertEqual(d["source"], "google_trends")
        self.assertIn("captured_at", d)


class TestKeywordExtractor(unittest.TestCase):
    """Test keyword extraction"""
    
    def setUp(self):
        self.extractor = KeywordExtractor()
    
    def test_extract_keywords(self):
        """Test basic keyword extraction"""
        text = "Python programming tutorial for beginners. Learn Python basics and advanced concepts."
        keywords = self.extractor.extract_keywords(text, top_n=5)
        
        self.assertGreater(len(keywords), 0)
        self.assertIn("python", keywords)
        self.assertIn("programming", keywords)
        
        # Stopwords should be filtered out
        self.assertNotIn("for", keywords)
        self.assertNotIn("and", keywords)
    
    def test_extract_bigrams(self):
        """Test bigram extraction"""
        text = "Machine learning and deep learning are transforming artificial intelligence."
        bigrams = self.extractor.extract_bigrams(text, top_n=5)
        
        self.assertGreater(len(bigrams), 0)
        # Should contain meaningful phrases
        self.assertTrue(any("learning" in bg for bg in bigrams))
    
    def test_stopword_filtering(self):
        """Test that stopwords are properly filtered"""
        text = "The quick brown fox jumps over the lazy dog"
        keywords = self.extractor.extract_keywords(text, top_n=10)
        
        # Stopwords should not appear
        stopwords = ["the", "over"]
        for stopword in stopwords:
            self.assertNotIn(stopword, keywords)
    
    def test_min_length_filtering(self):
        """Test minimum length filtering"""
        text = "AI ML NLP are short terms but machine learning is longer"
        keywords = self.extractor.extract_keywords(text, top_n=10, min_length=3)
        
        # Short words should be filtered
        self.assertNotIn("ai", keywords)
        self.assertNotIn("ml", keywords)


class TestTrendScorer(unittest.TestCase):
    """Test trend scoring algorithms"""
    
    def setUp(self):
        self.scorer = TrendScorer()
    
    def test_velocity_score_growth(self):
        """Test velocity score for growing trends"""
        # 100% growth
        score = self.scorer.compute_velocity_score(2000, 1000)
        self.assertGreater(score, 50)
        self.assertLessEqual(score, 100)
        
        # 500% growth
        score_high = self.scorer.compute_velocity_score(6000, 1000)
        self.assertGreater(score_high, score)
    
    def test_velocity_score_decline(self):
        """Test velocity score for declining trends"""
        score = self.scorer.compute_velocity_score(500, 1000)
        self.assertEqual(score, 0.0)
    
    def test_velocity_score_new_trend(self):
        """Test velocity score for new trends with no history"""
        score = self.scorer.compute_velocity_score(1000, 0)
        self.assertGreater(score, 0)
    
    def test_volume_score(self):
        """Test volume scoring"""
        # 1 million views
        score_1m = self.scorer.compute_volume_score(1000000, scale="views")
        self.assertGreater(score_1m, 70)
        
        # 10 million views should score higher
        score_10m = self.scorer.compute_volume_score(10000000, scale="views")
        self.assertGreater(score_10m, score_1m)
    
    def test_engagement_score(self):
        """Test engagement rate scoring"""
        # 5% engagement rate
        score = self.scorer.compute_engagement_score(5000, 100000)
        self.assertGreater(score, 40)
        self.assertLessEqual(score, 100)
        
        # 0% engagement
        score_zero = self.scorer.compute_engagement_score(0, 100000)
        self.assertEqual(score_zero, 0.0)
    
    def test_recency_score(self):
        """Test recency scoring"""
        # Very fresh (2 hours old)
        recent = datetime.utcnow() - timedelta(hours=2)
        score_fresh = self.scorer.compute_recency_score(recent)
        self.assertGreater(score_fresh, 90)
        
        # Old (30 days)
        old = datetime.utcnow() - timedelta(days=30)
        score_old = self.scorer.compute_recency_score(old)
        self.assertLess(score_old, 50)
    
    def test_comprehensive_score(self):
        """Test comprehensive scoring formula"""
        score = self.scorer.compute_comprehensive_score(
            current_value=1000000,  # 1M views
            previous_value=500000,  # Was 500K (100% growth)
            engagement=50000,  # 50K engagement
            total_views=1000000,  # 5% engagement rate
            timestamp=datetime.utcnow() - timedelta(hours=6)
        )
        
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)


class TestNormalization(unittest.TestCase):
    """Test data normalization across sources"""
    
    def test_cross_source_compatibility(self):
        """Test that items from different sources have consistent structure"""
        youtube_item = TrendItem(
            id="youtube_1",
            title_or_keyword="YouTube Video",
            type=TrendType.VIDEO,
            source="youtube",
            score=80.0
        )
        
        trends_item = TrendItem(
            id="trends_1",
            title_or_keyword="trending keyword",
            type=TrendType.KEYWORD,
            source="google_trends",
            score=75.0
        )
        
        # Both should have same core fields
        for item in [youtube_item, trends_item]:
            self.assertIsInstance(item.id, str)
            self.assertIsInstance(item.title_or_keyword, str)
            self.assertIsInstance(item.type, TrendType)
            self.assertIsInstance(item.source, str)
            self.assertIsInstance(item.score, float)
            self.assertIsInstance(item.captured_at, datetime)


if __name__ == "__main__":
    unittest.main()
