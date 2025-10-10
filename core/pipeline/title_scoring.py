"""
Title Scoring Module.

This module handles scoring titles for viral potential using a multi-factor rubric.
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


class TitleScorer:
    """
    Scores titles for viral potential using a comprehensive rubric.
    
    Evaluates titles across multiple dimensions: novelty, emotional impact,
    clarity, replay value, and shareability.
    """
    
    def __init__(self, config_path: Path | None = None):
        """
        Initialize TitleScorer.
        
        Args:
            config_path: Path to scoring configuration YAML file
        """
        self.config = self._load_config(config_path)
        logger.info("Initialized TitleScorer with viral scoring rubric")
    
    def score_title(self, title: dict[str, object]) -> dict[str, object]:
        """
        Score a single title across all dimensions.
        
        Args:
            title: Title dict with 'text', 'topic_id', etc.
        
        Returns:
            Title dict with added scoring information
        """
        text = title.get('text', '')
        
        # Calculate individual dimension scores
        scores = {
            'novelty': self._score_novelty(text),
            'emotional': self._score_emotional(text),
            'clarity': self._score_clarity(text),
            'replay': self._score_replay(text),
            'share': self._score_shareability(text)
        }
        
        # Calculate weighted total score
        weights = self.config.get('viral', {})
        total_score = sum(
            scores[dim] * weights.get(dim, 0.2)
            for dim in scores
        )
        
        # Round to 2 decimal places
        total_score = round(total_score, 2)
        
        # Add scoring info to title
        scored_title = title.copy()
        scored_title.update({
            'score': total_score,
            'score_breakdown': scores,
            'score_tier': self._get_score_tier(total_score),
            'scored_at': datetime.now().isoformat()
        })
        
        logger.debug(f"Scored title '{text[:50]}...': {total_score}")
        return scored_title
    
    def score_all_titles(
        self,
        titles_by_topic: dict[str, list[dict[str, object]]]
    ) -> dict[str, list[dict[str, object]]]:
        """
        Score all titles across all topics.
        
        Args:
            titles_by_topic: Dict mapping topic_id to title lists
        
        Returns:
            Dict with scored titles for each topic
        """
        scored_titles = {}
        total_count = 0
        
        for topic_id, titles in titles_by_topic.items():
            scored_titles[topic_id] = [
                self.score_title(title) for title in titles
            ]
            total_count += len(titles)
        
        logger.info(f"Scored {total_count} titles across {len(titles_by_topic)} topics")
        return scored_titles
    
    def save_scored_titles(
        self,
        scored_titles: dict[str, list[dict[str, object]]],
        output_dir: Path,
        filename: str = "titles_scored.json"
    ) -> Path:
        """
        Save scored titles to JSON file.
        
        Args:
            scored_titles: Dict with scored titles by topic
            output_dir: Output directory path
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        total_titles = sum(len(titles) for titles in scored_titles.values())
        
        # Calculate average score
        all_scores = [
            title.get('score', 0)
            for titles in scored_titles.values()
            for title in titles
        ]
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
        
        output_data = {
            "total_titles": total_titles,
            "total_topics": len(scored_titles),
            "average_score": round(avg_score, 2),
            "scored_at": datetime.now().isoformat(),
            "titles_by_topic": scored_titles
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {total_titles} scored titles to {output_path}")
        return output_path
    
    def _load_config(self, config_path: Path | None) -> dict[str, object]:
        """Load scoring configuration from YAML file."""
        if config_path is None:
            # Use default config path
            config_path = Path(__file__).parent.parent.parent / 'config' / 'scoring.yaml'
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded scoring config from {config_path}")
            return config
        else:
            logger.warning(f"Config not found at {config_path}, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict[str, object]:
        """Return default scoring configuration."""
        return {
            'viral': {
                'novelty': 0.25,
                'emotional': 0.25,
                'clarity': 0.20,
                'replay': 0.15,
                'share': 0.15
            },
            'thresholds': {
                'excellent': 85,
                'good': 70,
                'acceptable': 55,
                'poor': 40
            },
            'title': {
                'max_length': 100,
                'min_length': 20,
                'prefer_questions': True,
                'bonus_keywords': [
                    'secret', 'truth', 'revealed', 'shocking', 'amazing'
                ]
            }
        }
    
    def _score_novelty(self, text: str) -> float:
        """
        Score novelty/uniqueness of title (0-100).
        
        Factors: unusual word combinations, unexpected angles, fresh perspectives
        """
        score = 50.0  # Base score
        
        # Bonus for surprise words
        surprise_words = ['secret', 'revealed', 'nobody', 'hidden', 'truth', 
                         'discovered', 'shocking', 'unexpected', 'never']
        for word in surprise_words:
            if word.lower() in text.lower():
                score += 5
                break
        
        # Bonus for specific numbers (more specific = more novel)
        if re.search(r'\b[0-9]+\b', text):
            score += 5
        
        # Bonus for personal perspective
        personal_words = ['i ', 'my ', 'me ']
        for word in personal_words:
            if word.lower() in text.lower():
                score += 5
                break
        
        # Penalty for very common generic words
        generic_words = ['things', 'stuff', 'ways', 'tips']
        for word in generic_words:
            if word.lower() in text.lower():
                score -= 5
        
        return min(100.0, max(0.0, score))
    
    def _score_emotional(self, text: str) -> float:
        """
        Score emotional impact (0-100).
        
        Factors: emotional words, dramatic language, personal connection
        """
        score = 50.0  # Base score
        
        # High-emotion words
        positive_emotions = ['amazing', 'incredible', 'beautiful', 'love', 
                           'happy', 'joy', 'perfect']
        negative_emotions = ['terrible', 'awful', 'nightmare', 'disaster',
                           'regret', 'mistake', 'wrong']
        intense_emotions = ['shocking', 'devastating', 'mind-blowing',
                          'life-changing', 'unbelievable']
        
        for word in positive_emotions + negative_emotions:
            if word.lower() in text.lower():
                score += 5
                break
        
        for word in intense_emotions:
            if word.lower() in text.lower():
                score += 10
                break
        
        # Bonus for exclamation marks (but not too many)
        exclamation_count = text.count('!')
        if exclamation_count == 1:
            score += 5
        elif exclamation_count > 1:
            score -= 5  # Too many is annoying
        
        # Bonus for question marks (creates curiosity)
        if '?' in text:
            score += 10
        
        return min(100.0, max(0.0, score))
    
    def _score_clarity(self, text: str) -> float:
        """
        Score clarity/readability (0-100).
        
        Factors: length, word complexity, sentence structure
        """
        score = 70.0  # Base score (assume good clarity)
        
        length = len(text)
        title_config = self.config.get('title', {})
        min_length = title_config.get('min_length', 20)
        max_length = title_config.get('max_length', 100)
        
        # Ideal length check
        if min_length <= length <= max_length:
            score += 10
        elif length < min_length:
            score -= 15
        elif length > max_length:
            score -= 10
        
        # Word count check (ideal: 5-12 words)
        word_count = len(text.split())
        if 5 <= word_count <= 12:
            score += 5
        elif word_count < 5:
            score -= 10
        elif word_count > 15:
            score -= 5
        
        # Penalty for very long words (harder to read)
        long_words = [w for w in text.split() if len(w) > 12]
        score -= len(long_words) * 5
        
        # Bonus for active voice indicators
        active_indicators = ['you', 'i', 'we']
        for word in active_indicators:
            if word.lower() in text.lower():
                score += 3
                break
        
        return min(100.0, max(0.0, score))
    
    def _score_replay(self, text: str) -> float:
        """
        Score replay/rewatchability (0-100).
        
        Factors: reference to details, list format, lesson/insight promise
        """
        score = 50.0  # Base score
        
        # Bonus for list/number format (implies multiple insights)
        if re.search(r'\b[0-9]+\s+(things|ways|reasons|signs|tips)', text.lower()):
            score += 15
        
        # Bonus for "how to" (instructional, reference value)
        if 'how to' in text.lower() or 'how i' in text.lower():
            score += 10
        
        # Bonus for "what" questions (factual content)
        if text.lower().startswith('what '):
            score += 5
        
        # Bonus for lesson/learning indicators
        learning_words = ['learn', 'discover', 'realize', 'understand', 'lesson']
        for word in learning_words:
            if word.lower() in text.lower():
                score += 5
                break
        
        return min(100.0, max(0.0, score))
    
    def _score_shareability(self, text: str) -> float:
        """
        Score shareability/virality (0-100).
        
        Factors: relatable topics, conversation starters, social triggers
        """
        score = 50.0  # Base score
        
        # Bonus for relatable topics
        relatable_topics = ['relationship', 'friend', 'family', 'work',
                          'dating', 'job', 'boss', 'ex']
        for topic in relatable_topics:
            if topic.lower() in text.lower():
                score += 10
                break
        
        # Bonus for questions (encourage sharing opinions)
        if '?' in text:
            score += 10
        
        # Bonus for controversial/debate elements
        debate_words = ['vs', 'versus', 'debate', 'why', 'should']
        for word in debate_words:
            if word.lower() in text.lower():
                score += 5
                break
        
        # Bonus for call-to-action elements
        action_words = ['tell', 'share', 'comment', 'think']
        for word in action_words:
            if word.lower() in text.lower():
                score += 5
                break
        
        # Bonus for trending/timely keywords
        trending_words = ['trending', 'viral', 'everyone', 'nobody']
        for word in trending_words:
            if word.lower() in text.lower():
                score += 5
                break
        
        return min(100.0, max(0.0, score))
    
    def _get_score_tier(self, score: float) -> str:
        """Determine score tier based on thresholds."""
        thresholds = self.config.get('thresholds', {})
        
        if score >= thresholds.get('excellent', 85):
            return 'excellent'
        elif score >= thresholds.get('good', 70):
            return 'good'
        elif score >= thresholds.get('acceptable', 55):
            return 'acceptable'
        else:
            return 'poor'
