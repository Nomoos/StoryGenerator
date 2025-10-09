"""
Topic Clustering Module.

This module handles clustering story ideas into cohesive topics/themes
using LLM-based analysis.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from core.interfaces.llm_provider import ILLMProvider

logger = logging.getLogger(__name__)


class TopicClusterer:
    """
    Clusters ideas into topics using LLM-based analysis.
    
    Groups similar ideas together and generates thematic topics
    that can be used for title generation.
    """
    
    def __init__(self, llm_provider: ILLMProvider):
        """
        Initialize TopicClusterer.
        
        Args:
            llm_provider: LLM provider for clustering analysis
        """
        self.llm = llm_provider
        logger.info(f"Initialized TopicClusterer with model: {llm_provider.model_name}")
    
    def cluster_ideas(
        self,
        ideas: List[Dict],
        min_clusters: int = 8,
        max_clusters: int = 12
    ) -> List[Dict]:
        """
        Cluster ideas into topics.
        
        Args:
            ideas: List of idea dicts
            min_clusters: Minimum number of clusters to create
            max_clusters: Maximum number of clusters to create
        
        Returns:
            List of topic dicts with clustered ideas
        """
        if len(ideas) < min_clusters:
            logger.warning(
                f"Only {len(ideas)} ideas provided, less than min_clusters {min_clusters}"
            )
            min_clusters = max(1, len(ideas))
        
        prompt = self._build_clustering_prompt(ideas, min_clusters, max_clusters)
        
        try:
            response = self.llm.generate_completion(
                prompt=prompt,
                temperature=0.5,  # Lower temp for consistency
                max_tokens=2000
            )
            
            topics = self._parse_topics(response, ideas)
            logger.info(f"Clustered {len(ideas)} ideas into {len(topics)} topics")
            return topics
            
        except Exception as e:
            logger.error(f"Failed to cluster ideas: {e}")
            raise
    
    def save_topics(
        self,
        topics: List[Dict],
        output_dir: Path,
        filename: str = "topics_clustered.json"
    ) -> Path:
        """
        Save clustered topics to JSON file.
        
        Args:
            topics: List of topic dicts
            output_dir: Output directory path
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        output_data = {
            "total_topics": len(topics),
            "clustered_at": datetime.now().isoformat(),
            "topics": topics
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(topics)} topics to {output_path}")
        return output_path
    
    def _build_clustering_prompt(
        self,
        ideas: List[Dict],
        min_clusters: int,
        max_clusters: int
    ) -> str:
        """Build prompt for idea clustering."""
        # Format ideas for prompt
        ideas_text = "\n".join([
            f"{i+1}. {idea.get('content', '')[:200]}"
            for i, idea in enumerate(ideas)
        ])
        
        prompt = f"""Analyze these video ideas and group them into {min_clusters}-{max_clusters} thematic topics/clusters.

Video Ideas:
{ideas_text}

Task: Create logical topic clusters based on shared themes, emotions, or narrative elements.

For each cluster, provide:
1. A clear, descriptive topic name (3-6 words)
2. A brief theme description (1-2 sentences)
3. The idea numbers that belong to this cluster (comma-separated)

Format each cluster as:
Topic N: [Topic Name]
Theme: [Theme description]
Ideas: [idea numbers, e.g., 1, 3, 7, 12]

Clusters:"""
        
        return prompt
    
    def _parse_topics(
        self,
        response: str,
        ideas: List[Dict]
    ) -> List[Dict]:
        """
        Parse LLM response into structured topic dicts.
        
        Args:
            response: LLM response text
            ideas: Original list of ideas
        
        Returns:
            List of structured topic dicts
        """
        topics = []
        lines = response.strip().split('\n')
        current_topic = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for topic line
            if line.startswith('Topic'):
                # Save previous topic if exists
                if current_topic:
                    topics.append(current_topic)
                
                # Start new topic
                topic_name = line.split(':', 1)[1].strip() if ':' in line else line
                current_topic = {
                    "id": f"topic_{len(topics)+1:02d}",
                    "name": topic_name,
                    "theme": "",
                    "idea_ids": [],
                    "idea_count": 0
                }
            
            # Check for theme line
            elif line.startswith('Theme:'):
                if current_topic:
                    current_topic["theme"] = line.split(':', 1)[1].strip()
            
            # Check for ideas line
            elif line.startswith('Ideas:'):
                if current_topic:
                    idea_numbers_str = line.split(':', 1)[1].strip()
                    idea_numbers = self._extract_idea_numbers(idea_numbers_str)
                    
                    # Map idea numbers to actual idea IDs
                    for num in idea_numbers:
                        if 0 < num <= len(ideas):
                            idea_id = ideas[num-1].get('id', f'idea_{num}')
                            current_topic["idea_ids"].append(idea_id)
                    
                    current_topic["idea_count"] = len(current_topic["idea_ids"])
        
        # Save last topic
        if current_topic:
            topics.append(current_topic)
        
        return topics
    
    def _extract_idea_numbers(self, text: str) -> List[int]:
        """Extract idea numbers from comma-separated string."""
        numbers = []
        parts = text.replace(' ', '').split(',')
        
        for part in parts:
            try:
                num = int(part.strip())
                numbers.append(num)
            except ValueError:
                continue
        
        return numbers
