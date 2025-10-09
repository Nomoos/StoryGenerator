"""
Title Generation Module.

This module handles generating multiple title variants for each topic
using LLM-based creative generation.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from core.interfaces.llm_provider import ILLMProvider

logger = logging.getLogger(__name__)


class TitleGenerator:
    """
    Generates multiple title variants for topics.
    
    Creates engaging, viral-ready titles optimized for short-form video content.
    """
    
    def __init__(self, llm_provider: ILLMProvider):
        """
        Initialize TitleGenerator.
        
        Args:
            llm_provider: LLM provider for title generation
        """
        self.llm = llm_provider
        logger.info(f"Initialized TitleGenerator with model: {llm_provider.model_name}")
    
    def generate_titles(
        self,
        topic: Dict,
        count: int = 10
    ) -> List[Dict]:
        """
        Generate title variants for a topic.
        
        Args:
            topic: Topic dict with 'name', 'theme', etc.
            count: Number of title variants to generate
        
        Returns:
            List of title dicts
        """
        prompt = self._build_generation_prompt(topic, count)
        
        try:
            response = self.llm.generate_completion(
                prompt=prompt,
                temperature=0.85,  # High temp for creativity
                max_tokens=1000
            )
            
            titles = self._parse_titles(response, topic)
            logger.info(f"Generated {len(titles)} titles for topic {topic.get('id')}")
            return titles
            
        except Exception as e:
            logger.error(f"Failed to generate titles for topic {topic.get('id')}: {e}")
            raise
    
    def generate_all_titles(
        self,
        topics: List[Dict],
        titles_per_topic: int = 10
    ) -> Dict[str, List[Dict]]:
        """
        Generate titles for all topics.
        
        Args:
            topics: List of topic dicts
            titles_per_topic: Number of titles per topic
        
        Returns:
            Dict mapping topic_id to list of title dicts
        """
        all_titles = {}
        
        for topic in topics:
            topic_id = topic.get('id', 'unknown')
            try:
                titles = self.generate_titles(topic, titles_per_topic)
                all_titles[topic_id] = titles
            except Exception as e:
                logger.warning(f"Skipping topic {topic_id} due to error: {e}")
                all_titles[topic_id] = []
        
        total_titles = sum(len(titles) for titles in all_titles.values())
        logger.info(f"Generated {total_titles} titles across {len(topics)} topics")
        
        return all_titles
    
    def save_titles(
        self,
        titles_by_topic: Dict[str, List[Dict]],
        output_dir: Path,
        filename: str = "titles_raw.json"
    ) -> Path:
        """
        Save generated titles to JSON file.
        
        Args:
            titles_by_topic: Dict mapping topic_id to title lists
            output_dir: Output directory path
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        total_titles = sum(len(titles) for titles in titles_by_topic.values())
        
        output_data = {
            "total_titles": total_titles,
            "total_topics": len(titles_by_topic),
            "generated_at": datetime.now().isoformat(),
            "titles_by_topic": titles_by_topic
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {total_titles} titles to {output_path}")
        return output_path
    
    def _build_generation_prompt(
        self,
        topic: Dict,
        count: int
    ) -> str:
        """Build prompt for title generation."""
        topic_name = topic.get('name', 'Unknown Topic')
        theme = topic.get('theme', '')
        
        prompt = f"""Generate {count} compelling video titles for this topic.

Topic: {topic_name}
Theme: {theme}

Requirements for each title:
1. 20-100 characters long
2. Creates curiosity, urgency, or emotional hook
3. Uses viral keywords when appropriate (revealed, secret, shocking, truth, etc.)
4. Clear and easy to understand
5. Makes viewers want to click and watch
6. Suitable for short-form video content (30-60 seconds)

Techniques to use:
- Questions that spark curiosity
- Bold statements or claims
- Emotional triggers (surprise, humor, drama)
- Numbers or lists ("5 Signs...", "3 Reasons...")
- Personal angle ("I discovered...", "Nobody told me...")

Format: Number each title (1., 2., 3., etc.)

Titles:"""
        
        return prompt
    
    def _parse_titles(
        self,
        response: str,
        topic: Dict
    ) -> List[Dict]:
        """
        Parse LLM response into structured title dicts.
        
        Args:
            response: LLM response text
            topic: Topic dict
        
        Returns:
            List of structured title dicts
        """
        titles = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line starts with a number (new title)
            if line and line[0].isdigit() and '.' in line[:4]:
                # Extract title text
                title_text = line.split('.', 1)[1].strip() if '.' in line else line
                
                # Remove quotes if present
                title_text = title_text.strip('"\'')
                
                if title_text and len(title_text) >= 10:  # Minimum viable title
                    titles.append({
                        "id": f"{topic.get('id', 'topic')}_title_{len(titles)+1:02d}",
                        "topic_id": topic.get('id'),
                        "topic_name": topic.get('name'),
                        "text": title_text,
                        "length": len(title_text),
                        "generated_at": datetime.now().isoformat()
                    })
        
        return titles
