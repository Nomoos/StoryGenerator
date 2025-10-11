"""
Voice Recommendation Module.

This module handles recommending voice characteristics (gender, style, tone)
for each title based on content analysis.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


class VoiceRecommender:
    """
    Recommends voice characteristics for titles.
    
    Analyzes title content and target audience to recommend appropriate
    voice gender, style, pitch, speed, and emotional tone.
    """
    
    def __init__(self):
        """Initialize VoiceRecommender."""
        logger.info("Initialized VoiceRecommender")
    
    def recommend_voice(self, title: Dict) -> Dict:
        """
        Recommend voice characteristics for a title.
        
        Args:
            title: Title dict with 'text', 'topic_id', 'target_gender', etc.
        
        Returns:
            Title dict with added voice recommendation
        """
        text = title.get('text', '')
        target_gender = title.get('target_gender', 'women')  # From idea metadata
        
        # Analyze content for voice characteristics
        voice_rec = {
            'gender': self._recommend_gender(text, target_gender),
            'style': self._recommend_style(text),
            'pitch': self._recommend_pitch(text),
            'speed': self._recommend_speed(text),
            'emotion': self._recommend_emotion(text),
            'recommended_at': datetime.now().isoformat()
        }
        
        # Add recommendation to title
        title_with_voice = title.copy()
        title_with_voice['voice_recommendation'] = voice_rec
        
        logger.debug(f"Recommended voice for title: {voice_rec['gender']}, {voice_rec['style']}")
        return title_with_voice
    
    def recommend_all_voices(
        self,
        titles_by_topic: Dict[str, List[Dict]]
    ) -> Dict[str, List[Dict]]:
        """
        Recommend voices for all titles.
        
        Args:
            titles_by_topic: Dict mapping topic_id to title lists
        
        Returns:
            Dict with voice recommendations for each title
        """
        titles_with_voices = {}
        total_count = 0
        
        for topic_id, titles in titles_by_topic.items():
            titles_with_voices[topic_id] = [
                self.recommend_voice(title) for title in titles
            ]
            total_count += len(titles)
        
        logger.info(f"Generated voice recommendations for {total_count} titles")
        return titles_with_voices
    
    def save_recommendations(
        self,
        titles_with_voices: Dict[str, List[Dict]],
        output_dir: Path,
        filename: str = "titles_with_voices.json"
    ) -> Path:
        """
        Save titles with voice recommendations to JSON file.
        
        Args:
            titles_with_voices: Dict with titles and voice recs by topic
            output_dir: Output directory path
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        total_titles = sum(len(titles) for titles in titles_with_voices.values())
        
        output_data = {
            "total_titles": total_titles,
            "total_topics": len(titles_with_voices),
            "recommended_at": datetime.now().isoformat(),
            "titles_by_topic": titles_with_voices
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {total_titles} voice recommendations to {output_path}")
        return output_path
    
    def _recommend_gender(self, text: str, target_gender: str) -> str:
        """
        Recommend voice gender.
        
        Generally matches target audience gender, but can vary based on content.
        """
        text_lower = text.lower()
        
        # Strong male voice indicators
        male_indicators = ['father', 'dad', 'boyfriend', 'husband', 'brother',
                          'man', 'guy', 'he ', 'his ']
        
        # Strong female voice indicators
        female_indicators = ['mother', 'mom', 'girlfriend', 'wife', 'sister',
                           'woman', 'girl', 'she ', 'her ']
        
        # Count indicators
        male_count = sum(1 for ind in male_indicators if ind in text_lower)
        female_count = sum(1 for ind in female_indicators if ind in text_lower)
        
        # If content strongly suggests a gender, use that
        if male_count > female_count + 1:
            return 'male'
        elif female_count > male_count + 1:
            return 'female'
        
        # Otherwise match target audience
        return 'female' if target_gender == 'women' else 'male'
    
    def _recommend_style(self, text: str) -> str:
        """
        Recommend voice style/tone.
        
        Options: conversational, dramatic, inspirational, humorous, intimate
        """
        text_lower = text.lower()
        
        # Dramatic indicators
        if any(word in text_lower for word in 
               ['shocking', 'terrible', 'disaster', 'nightmare', 'devastating']):
            return 'dramatic'
        
        # Inspirational indicators
        if any(word in text_lower for word in
               ['amazing', 'incredible', 'transform', 'overcome', 'success']):
            return 'inspirational'
        
        # Humorous indicators
        if any(word in text_lower for word in
               ['funny', 'hilarious', 'joke', 'laugh', 'awkward']):
            return 'humorous'
        
        # Intimate/confessional indicators
        if any(text_lower.startswith(phrase) for phrase in
               ['i ', 'my ', 'nobody knows']):
            return 'intimate'
        
        # Default to conversational
        return 'conversational'
    
    def _recommend_pitch(self, text: str) -> str:
        """
        Recommend voice pitch.
        
        Options: low, medium, high
        """
        text_lower = text.lower()
        
        # High pitch for exciting/surprising content
        if any(word in text_lower for word in
               ['exciting', 'amazing', 'shocking', '!', 'wow']):
            return 'medium-high'
        
        # Low pitch for serious/dramatic content
        if any(word in text_lower for word in
               ['serious', 'terrible', 'disaster', 'truth', 'secret']):
            return 'medium-low'
        
        # Medium for most content
        return 'medium'
    
    def _recommend_speed(self, text: str) -> str:
        """
        Recommend voice speed.
        
        Options: slow, medium, fast
        """
        text_lower = text.lower()
        
        # Fast for exciting/energetic content
        if any(word in text_lower for word in
               ['quick', 'fast', 'urgent', 'now', 'immediately']):
            return 'medium-fast'
        
        # Slow for dramatic/serious content
        if any(word in text_lower for word in
               ['slowly', 'careful', 'important', 'remember']):
            return 'medium-slow'
        
        # Medium for most content
        return 'medium'
    
    def _recommend_emotion(self, text: str) -> str:
        """
        Recommend primary emotion.
        
        Options: neutral, excited, concerned, empathetic, curious, confident
        """
        text_lower = text.lower()
        
        # Excited
        if any(word in text_lower for word in
               ['amazing', 'incredible', 'exciting', '!', 'wow']):
            return 'excited'
        
        # Concerned
        if any(word in text_lower for word in
               ['warning', 'careful', 'danger', 'mistake', 'wrong']):
            return 'concerned'
        
        # Empathetic
        if any(word in text_lower for word in
               ['feel', 'understand', 'relate', 'struggle', 'difficult']):
            return 'empathetic'
        
        # Curious
        if '?' in text or any(text_lower.startswith(w) for w in
                             ['what', 'why', 'how', 'when', 'where']):
            return 'curious'
        
        # Confident
        if any(word in text_lower for word in
               ['definitely', 'absolutely', 'must', 'always', 'never']):
            return 'confident'
        
        # Default to neutral
        return 'neutral'
