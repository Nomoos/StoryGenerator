"""
Unit tests for voice recommendation module.
"""

import pytest
import json
from pathlib import Path

from PrismQ.VoiceOverGenerator.voice_recommendation import VoiceRecommender


class TestVoiceRecommender:
    """Tests for VoiceRecommender class."""
    
    def test_init(self):
        """Test VoiceRecommender initialization."""
        recommender = VoiceRecommender()
        assert recommender is not None
    
    def test_recommend_voice_basic(self):
        """Test basic voice recommendation."""
        recommender = VoiceRecommender()
        
        title = {
            "id": "test_title_01",
            "text": "Why I discovered this amazing secret",
            "target_gender": "women"
        }
        
        result = recommender.recommend_voice(title)
        
        assert "voice_recommendation" in result
        voice_rec = result["voice_recommendation"]
        assert "gender" in voice_rec
        assert "style" in voice_rec
        assert "pitch" in voice_rec
        assert "speed" in voice_rec
        assert "emotion" in voice_rec
    
    def test_recommend_gender_female_target(self):
        """Test gender recommendation for female target."""
        recommender = VoiceRecommender()
        
        gender = recommender._recommend_gender("A story about something", "women")
        assert gender == "female"
    
    def test_recommend_gender_male_target(self):
        """Test gender recommendation for male target."""
        recommender = VoiceRecommender()
        
        gender = recommender._recommend_gender("A story about something", "men")
        assert gender == "male"
    
    def test_recommend_gender_content_override(self):
        """Test gender recommendation with content override."""
        recommender = VoiceRecommender()
        
        # Strong male indicator should override target
        gender = recommender._recommend_gender(
            "My boyfriend and his father helped me",
            "women"
        )
        assert gender == "male"
        
        # Strong female indicator
        gender = recommender._recommend_gender(
            "My girlfriend and her mother were there",
            "men"
        )
        assert gender == "female"
    
    def test_recommend_style_dramatic(self):
        """Test dramatic style recommendation."""
        recommender = VoiceRecommender()
        
        style = recommender._recommend_style("This shocking disaster changed everything")
        assert style == "dramatic"
    
    def test_recommend_style_inspirational(self):
        """Test inspirational style recommendation."""
        recommender = VoiceRecommender()
        
        style = recommender._recommend_style("How I transformed my life with this amazing technique")
        assert style == "inspirational"
    
    def test_recommend_style_humorous(self):
        """Test humorous style recommendation."""
        recommender = VoiceRecommender()
        
        style = recommender._recommend_style("The hilarious moment when I realized")
        assert style == "humorous"
    
    def test_recommend_style_intimate(self):
        """Test intimate style recommendation."""
        recommender = VoiceRecommender()
        
        style = recommender._recommend_style("I never told anyone about this secret")
        assert style == "intimate"
    
    def test_recommend_style_conversational_default(self):
        """Test conversational style as default."""
        recommender = VoiceRecommender()
        
        style = recommender._recommend_style("A regular story about everyday life")
        assert style == "conversational"
    
    def test_recommend_pitch(self):
        """Test pitch recommendation."""
        recommender = VoiceRecommender()
        
        # High pitch for exciting content
        pitch_high = recommender._recommend_pitch("Amazing shocking discovery!")
        assert "high" in pitch_high.lower() or pitch_high == "medium-high"
        
        # Low pitch for serious content
        pitch_low = recommender._recommend_pitch("The terrible truth about this serious issue")
        assert "low" in pitch_low.lower() or pitch_low == "medium-low"
    
    def test_recommend_speed(self):
        """Test speed recommendation."""
        recommender = VoiceRecommender()
        
        # Fast for urgent content
        speed_fast = recommender._recommend_speed("Quick urgent action needed now!")
        assert "fast" in speed_fast.lower() or speed_fast == "medium-fast"
        
        # Slow for important content
        speed_slow = recommender._recommend_speed("Remember this important lesson carefully")
        assert "slow" in speed_slow.lower() or speed_slow == "medium-slow"
    
    def test_recommend_emotion_excited(self):
        """Test excited emotion recommendation."""
        recommender = VoiceRecommender()
        
        emotion = recommender._recommend_emotion("This is amazing and incredible!")
        assert emotion == "excited"
    
    def test_recommend_emotion_curious(self):
        """Test curious emotion recommendation."""
        recommender = VoiceRecommender()
        
        emotion = recommender._recommend_emotion("Why does this always happen?")
        assert emotion == "curious"
    
    def test_recommend_emotion_empathetic(self):
        """Test empathetic emotion recommendation."""
        recommender = VoiceRecommender()
        
        emotion = recommender._recommend_emotion("I understand how you feel about this struggle")
        assert emotion == "empathetic"
    
    def test_recommend_all_voices(self):
        """Test recommending voices for all titles."""
        recommender = VoiceRecommender()
        
        titles_by_topic = {
            "topic_01": [
                {"id": "t1", "text": "Amazing story here", "target_gender": "women"},
                {"id": "t2", "text": "Another story", "target_gender": "women"}
            ]
        }
        
        result = recommender.recommend_all_voices(titles_by_topic)
        
        assert len(result) == 1
        assert len(result["topic_01"]) == 2
        assert all(
            "voice_recommendation" in title
            for titles in result.values()
            for title in titles
        )
    
    def test_save_recommendations(self, tmp_path):
        """Test saving voice recommendations to file."""
        recommender = VoiceRecommender()
        
        titles_with_voices = {
            "topic_01": [
                {
                    "id": "t1",
                    "text": "Test title",
                    "voice_recommendation": {
                        "gender": "female",
                        "style": "conversational",
                        "pitch": "medium",
                        "speed": "medium",
                        "emotion": "neutral"
                    }
                }
            ]
        }
        
        output_path = recommender.save_recommendations(titles_with_voices, tmp_path)
        
        assert output_path.exists()
        
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert data["total_titles"] == 1
        assert data["total_topics"] == 1
