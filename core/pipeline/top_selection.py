"""
Top Selection Module.

This module handles selecting the top-N titles per segment based on scores
and other criteria.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class TopSelector:
    """
    Selects top titles from scored and voice-recommended titles.
    
    Picks the best titles per segment based on viral scores and ensures
    diversity across topics.
    """
    
    def __init__(self):
        """Initialize TopSelector."""
        logger.info("Initialized TopSelector")
    
    def select_top_titles(
        self,
        titles_by_topic: Dict[str, List[Dict]],
        top_n: int = 5,
        min_score: float = 55.0
    ) -> List[Dict]:
        """
        Select top N titles across all topics.
        
        Args:
            titles_by_topic: Dict mapping topic_id to title lists
            top_n: Number of top titles to select
            min_score: Minimum acceptable score
        
        Returns:
            List of top N selected titles
        """
        # Flatten all titles into single list
        all_titles = []
        for topic_id, titles in titles_by_topic.items():
            for title in titles:
                # Only consider titles above minimum score
                if title.get('score', 0) >= min_score:
                    all_titles.append(title)
        
        if not all_titles:
            logger.warning(f"No titles found with score >= {min_score}")
            return []
        
        # Sort by score descending
        all_titles.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # Select top N with diversity
        selected = self._select_with_diversity(all_titles, top_n)
        
        logger.info(f"Selected top {len(selected)} titles from {len(all_titles)} candidates")
        return selected
    
    def select_per_segment(
        self,
        titles_by_segment: Dict[str, Dict[str, List[Dict]]],
        top_n_per_segment: int = 5,
        min_score: float = 55.0
    ) -> Dict[str, List[Dict]]:
        """
        Select top titles for each audience segment.
        
        Args:
            titles_by_segment: Dict mapping segment to titles_by_topic
            top_n_per_segment: Number of titles per segment
            min_score: Minimum acceptable score
        
        Returns:
            Dict mapping segment to list of selected titles
        """
        selected_by_segment = {}
        
        for segment, titles_by_topic in titles_by_segment.items():
            selected = self.select_top_titles(
                titles_by_topic,
                top_n=top_n_per_segment,
                min_score=min_score
            )
            selected_by_segment[segment] = selected
        
        total_selected = sum(len(titles) for titles in selected_by_segment.values())
        logger.info(
            f"Selected {total_selected} titles across {len(selected_by_segment)} segments"
        )
        
        return selected_by_segment
    
    def save_selected_titles(
        self,
        selected_titles: List[Dict],
        output_dir: Path,
        gender: str,
        age_bucket: str,
        filename: str = "top_5_titles.json"
    ) -> Path:
        """
        Save selected titles to JSON file.
        
        Args:
            selected_titles: List of selected title dicts
            output_dir: Output directory path
            gender: Target gender segment
            age_bucket: Target age bucket
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        # Calculate statistics
        avg_score = (
            sum(t.get('score', 0) for t in selected_titles) / len(selected_titles)
            if selected_titles else 0
        )
        
        # Get unique topics
        unique_topics = set(t.get('topic_id') for t in selected_titles if t.get('topic_id'))
        
        output_data = {
            "segment": {
                "gender": gender,
                "age_bucket": age_bucket
            },
            "total_selected": len(selected_titles),
            "average_score": round(avg_score, 2),
            "topics_represented": len(unique_topics),
            "selected_at": datetime.now().isoformat(),
            "titles": selected_titles
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(selected_titles)} selected titles to {output_path}")
        return output_path
    
    def _select_with_diversity(
        self,
        sorted_titles: List[Dict],
        top_n: int
    ) -> List[Dict]:
        """
        Select top N titles while ensuring topic diversity.
        
        Tries to select titles from different topics when possible.
        
        Args:
            sorted_titles: List of titles sorted by score (descending)
            top_n: Number of titles to select
        
        Returns:
            List of selected titles with diversity
        """
        selected = []
        used_topics = set()
        
        # First pass: select one title per topic (up to top_n)
        for title in sorted_titles:
            if len(selected) >= top_n:
                break
            
            topic_id = title.get('topic_id')
            if topic_id and topic_id not in used_topics:
                selected.append(title)
                used_topics.add(topic_id)
        
        # Second pass: fill remaining slots with highest scores
        if len(selected) < top_n:
            for title in sorted_titles:
                if len(selected) >= top_n:
                    break
                
                if title not in selected:
                    selected.append(title)
        
        # Final sort by score to maintain ranking
        selected.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return selected[:top_n]
    
    def generate_summary_report(
        self,
        selected_by_segment: Dict[str, List[Dict]],
        output_dir: Path,
        filename: str = "selection_summary.json"
    ) -> Path:
        """
        Generate a summary report of all selections.
        
        Args:
            selected_by_segment: Dict of selected titles by segment
            output_dir: Output directory path
            filename: Output filename
        
        Returns:
            Path to saved report
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        # Calculate overall statistics
        all_selected = [
            title
            for titles in selected_by_segment.values()
            for title in titles
        ]
        
        total_count = len(all_selected)
        avg_score = (
            sum(t.get('score', 0) for t in all_selected) / total_count
            if total_count > 0 else 0
        )
        
        # Score distribution
        score_tiers = {'excellent': 0, 'good': 0, 'acceptable': 0, 'poor': 0}
        for title in all_selected:
            tier = title.get('score_tier', 'poor')
            score_tiers[tier] = score_tiers.get(tier, 0) + 1
        
        # Voice distribution
        voice_genders = {}
        for title in all_selected:
            voice_rec = title.get('voice_recommendation', {})
            gender = voice_rec.get('gender', 'unknown')
            voice_genders[gender] = voice_genders.get(gender, 0) + 1
        
        report = {
            "summary": {
                "total_segments": len(selected_by_segment),
                "total_titles_selected": total_count,
                "average_score": round(avg_score, 2),
                "score_distribution": score_tiers,
                "voice_gender_distribution": voice_genders
            },
            "by_segment": {
                segment: {
                    "count": len(titles),
                    "avg_score": round(
                        sum(t.get('score', 0) for t in titles) / len(titles)
                        if titles else 0, 
                        2
                    ),
                    "top_title": titles[0].get('text') if titles else None
                }
                for segment, titles in selected_by_segment.items()
            },
            "generated_at": datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Generated selection summary report at {output_path}")
        return output_path
