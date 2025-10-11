"""
Idea Generation Module.

This module handles generating story ideas from various sources including
Reddit stories and LLM-based original ideas.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from PrismQ.Shared.interfaces.llm_provider import ILLMProvider

logger = logging.getLogger(__name__)


class IdeaAdapter:
    """
    Adapts Reddit stories into video ideas.
    
    Takes ranked Reddit stories and adapts them into structured video ideas
    suitable for the target audience segment.
    """
    
    def __init__(self, llm_provider: ILLMProvider):
        """
        Initialize IdeaAdapter.
        
        Args:
            llm_provider: LLM provider for story adaptation
        """
        self.llm = llm_provider
        logger.info(f"Initialized IdeaAdapter with model: {llm_provider.model_name}")
    
    def adapt_story(
        self, 
        story: dict[str, object], 
        gender: str, 
        age_bucket: str
    ) -> dict[str, object]:
        """
        Adapt a Reddit story into a video idea.
        
        Args:
            story: Reddit story dict with 'title', 'content', 'url', etc.
            gender: Target gender segment (e.g., 'women', 'men')
            age_bucket: Target age bucket (e.g., '18-23', '24-29')
        
        Returns:
            Adapted idea dict with 'id', 'source', 'content', 'metadata'
        """
        prompt = self._build_adaptation_prompt(story, gender, age_bucket)
        
        try:
            adapted_content = self.llm.generate_completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=500
            )
            
            idea = {
                "id": f"reddit_{story.get('id', 'unknown')}",
                "source": "reddit_adapted",
                "original_title": story.get("title", ""),
                "original_url": story.get("url", ""),
                "content": adapted_content.strip(),
                "target_gender": gender,
                "target_age": age_bucket,
                "adapted_at": datetime.now().isoformat(),
                "metadata": {
                    "score": story.get("score", 0),
                    "subreddit": story.get("subreddit", "")
                }
            }
            
            logger.debug(f"Adapted Reddit story: {idea['id']}")
            return idea
            
        except Exception as e:
            logger.error(f"Failed to adapt story {story.get('id')}: {e}")
            raise
    
    def adapt_stories(
        self,
        stories: list[dict[str, object]],
        gender: str,
        age_bucket: str
    ) -> list[dict[str, object]]:
        """
        Adapt multiple Reddit stories into video ideas.
        
        Args:
            stories: List of Reddit story dicts
            gender: Target gender segment
            age_bucket: Target age bucket
        
        Returns:
            List of adapted idea dicts
        """
        ideas = []
        for story in stories:
            try:
                idea = self.adapt_story(story, gender, age_bucket)
                ideas.append(idea)
            except Exception as e:
                logger.warning(f"Skipping story {story.get('id')} due to error: {e}")
                continue
        
        logger.info(f"Adapted {len(ideas)} stories out of {len(stories)}")
        return ideas
    
    def save_ideas(
        self,
        ideas: list[dict[str, object]],
        output_dir: Path,
        filename: str = "reddit_adapted.json"
    ) -> Path:
        """
        Save adapted ideas to JSON file.
        
        Args:
            ideas: List of adapted idea dicts
            output_dir: Output directory path
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(ideas, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(ideas)} adapted ideas to {output_path}")
        return output_path
    
    def _build_adaptation_prompt(
        self,
        story: dict[str, object],
        gender: str,
        age_bucket: str
    ) -> str:
        """Build prompt for story adaptation."""
        title = story.get("title", "")
        content = story.get("selftext", story.get("content", ""))
        
        prompt = f"""Adapt this Reddit story into a compelling video idea for {gender} aged {age_bucket}.

Original Title: {title}

Original Content:
{content[:1000]}  # Limit content length

Task: Create a brief, engaging video idea (2-3 sentences) that:
1. Captures the core narrative or emotional hook
2. Is relatable to {gender} aged {age_bucket}
3. Has strong viral potential for short-form video content
4. Maintains the essence of the original story

Video Idea:"""
        
        return prompt


class IdeaGenerator:
    """
    Generates original story ideas using LLM.
    
    Creates fresh, original video ideas tailored to specific audience segments
    without relying on existing content sources.
    """
    
    def __init__(self, llm_provider: ILLMProvider):
        """
        Initialize IdeaGenerator.
        
        Args:
            llm_provider: LLM provider for idea generation
        """
        self.llm = llm_provider
        logger.info(f"Initialized IdeaGenerator with model: {llm_provider.model_name}")
    
    def generate_ideas(
        self,
        gender: str,
        age_bucket: str,
        count: int = 20
    ) -> list[dict[str, object]]:
        """
        Generate original video ideas.
        
        Args:
            gender: Target gender segment
            age_bucket: Target age bucket
            count: Number of ideas to generate
        
        Returns:
            List of generated idea dicts
        """
        prompt = self._build_generation_prompt(gender, age_bucket, count)
        
        try:
            response = self.llm.generate_completion(
                prompt=prompt,
                temperature=0.8,  # Higher temp for creativity
                max_tokens=2000
            )
            
            ideas = self._parse_ideas(response, gender, age_bucket)
            logger.info(f"Generated {len(ideas)} original ideas for {gender} {age_bucket}")
            return ideas
            
        except Exception as e:
            logger.error(f"Failed to generate ideas: {e}")
            raise
    
    def save_ideas(
        self,
        ideas: list[dict[str, object]],
        output_dir: Path,
        filename: str = "llm_generated.json"
    ) -> Path:
        """
        Save generated ideas to JSON file.
        
        Args:
            ideas: List of generated idea dicts
            output_dir: Output directory path
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(ideas, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(ideas)} generated ideas to {output_path}")
        return output_path
    
    def _build_generation_prompt(
        self,
        gender: str,
        age_bucket: str,
        count: int
    ) -> str:
        """Build prompt for idea generation."""
        prompt = f"""Generate {count} original, creative video ideas for short-form content (30-60 seconds).

Target Audience: {gender} aged {age_bucket}

Requirements:
1. Each idea should be compelling and have high viral potential
2. Focus on relatable life experiences, emotions, or scenarios
3. Include elements of surprise, humor, drama, or inspiration
4. Be specific and vivid (not generic)
5. Suitable for a single narrator storytelling format

Format: Number each idea (1., 2., 3., etc.) with a 2-3 sentence description.

Video Ideas:"""
        
        return prompt
    
    def _parse_ideas(
        self,
        response: str,
        gender: str,
        age_bucket: str
    ) -> List[Dict]:
        """
        Parse LLM response into structured idea dicts.
        
        Args:
            response: LLM response text
            gender: Target gender
            age_bucket: Target age bucket
        
        Returns:
            List of structured idea dicts
        """
        ideas = []
        lines = response.strip().split('\n')
        current_idea = ""
        idea_number = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line starts with a number (new idea)
            if line and line[0].isdigit() and '.' in line[:4]:
                # Save previous idea if exists
                if current_idea:
                    ideas.append(self._create_idea_dict(
                        idea_number,
                        current_idea,
                        gender,
                        age_bucket
                    ))
                
                # Start new idea
                idea_number += 1
                current_idea = line.split('.', 1)[1].strip() if '.' in line else line
            else:
                # Continue current idea
                if current_idea:
                    current_idea += " " + line
        
        # Save last idea
        if current_idea:
            ideas.append(self._create_idea_dict(
                idea_number,
                current_idea,
                gender,
                age_bucket
            ))
        
        return ideas
    
    def _create_idea_dict(
        self,
        number: int,
        content: str,
        gender: str,
        age_bucket: str
    ) -> Dict:
        """Create structured idea dict."""
        return {
            "id": f"llm_{number:03d}",
            "source": "llm_generated",
            "content": content.strip(),
            "target_gender": gender,
            "target_age": age_bucket,
            "generated_at": datetime.now().isoformat(),
            "metadata": {
                "model": self.llm.model_name
            }
        }


def merge_and_save_all_ideas(
    adapted_ideas: List[Dict],
    generated_ideas: List[Dict],
    output_dir: Path,
    filename: str = "all_ideas.json"
) -> Path:
    """
    Merge adapted and generated ideas into a single file.
    
    Args:
        adapted_ideas: List of Reddit-adapted ideas
        generated_ideas: List of LLM-generated ideas
        output_dir: Output directory path
        filename: Output filename
    
    Returns:
        Path to saved file
    """
    all_ideas = {
        "total_count": len(adapted_ideas) + len(generated_ideas),
        "adapted_count": len(adapted_ideas),
        "generated_count": len(generated_ideas),
        "merged_at": datetime.now().isoformat(),
        "ideas": adapted_ideas + generated_ideas
    }
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_ideas, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Merged {all_ideas['total_count']} total ideas to {output_path}")
    return output_path
