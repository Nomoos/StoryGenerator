#!/usr/bin/env python3
"""
Topic Generator with Microstep Validation Integration.

This module provides a Python wrapper around the C# TopicGenerator with
integrated validation, progress tracking, and artifact logging using the
MicrostepValidator system.

Usage:
    from Generators.GTopics import TopicGeneratorWithValidation
    
    generator = TopicGeneratorWithValidation()
    result = generator.generate_topics_for_segment(
        gender="women",
        age="18-23",
        ideas_file="/path/to/ideas.md"
    )
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add Tools to path for MicrostepValidator
sys.path.insert(0, str(Path(__file__).parent.parent))

from Tools.MicrostepValidator import (
    MicrostepValidator,
    create_microstep_artifact,
    log_microstep_config,
    update_microstep_progress,
    copilot_check_microstep
)


class TopicGeneratorWithValidation:
    """
    Topic Generator with integrated validation and progress tracking.
    
    This class wraps the C# TopicGenerator and adds:
    - Automatic progress tracking via MicrostepValidator
    - Configuration logging for reproducibility
    - Artifact creation and validation
    - @copilot check integration
    """
    
    MICROSTEP_NUMBER = 3  # Topics is step 3 in the pipeline
    
    def __init__(self, base_path: str = None, config_path: str = None):
        """
        Initialize the topic generator with validation.
        
        Args:
            base_path: Base path for Generator folder (optional)
            config_path: Path to pipeline.yaml config (optional)
        """
        self.validator = MicrostepValidator(base_path, config_path)
        self.csharp_dll = self._find_csharp_dll()
        
    def _find_csharp_dll(self) -> Optional[str]:
        """Find the compiled C# TopicGenerator DLL."""
        # Look for the DLL in common locations
        possible_paths = [
            Path(__file__).parent.parent.parent / "CSharp" / "StoryGenerator.Generators" / "bin" / "Debug" / "net8.0" / "StoryGenerator.Generators.dll",
            Path(__file__).parent.parent.parent / "CSharp" / "StoryGenerator.Generators" / "bin" / "Release" / "net8.0" / "StoryGenerator.Generators.dll",
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        return None
    
    def generate_topics_for_segment(
        self,
        gender: str,
        age: str,
        ideas_file: str = None,
        ideas_data: List[str] = None,
        min_topics: int = 8,
        validate: bool = True
    ) -> Dict[str, Any]:
        """
        Generate topics for a specific audience segment with validation.
        
        Args:
            gender: Target gender (e.g., 'women', 'men')
            age: Target age group (e.g., '18-23', '24-29')
            ideas_file: Path to markdown file with ideas (optional)
            ideas_data: List of idea strings (optional, alternative to ideas_file)
            min_topics: Minimum number of topics to generate (default: 8)
            validate: Whether to run validation after generation (default: True)
        
        Returns:
            Dictionary with:
                - 'success': bool
                - 'topics_file': path to generated topics JSON
                - 'topics': list of generated topics
                - 'validation_report': validation report (if validate=True)
                - 'artifacts': list of created artifacts
        """
        step = self.MICROSTEP_NUMBER
        
        # Start progress tracking
        self.validator.update_progress(
            step, "started",
            f"Starting topic generation for {gender}/{age}",
            gender, age
        )
        
        # Log configuration
        custom_config = {
            "min_topics": min_topics,
            "clustering_method": "keyword-based",
            "generator": "TopicGenerator",
            "version": "1.0.0"
        }
        config_path = self.validator.log_config(
            step,
            config_subset=custom_config,
            gender=gender,
            age=age
        )
        
        artifacts = [config_path.name]
        
        try:
            # Generate topics
            if ideas_data:
                topics = self._generate_topics_from_data(
                    ideas_data, gender, age, min_topics
                )
            elif ideas_file:
                topics = self._generate_topics_from_file(
                    ideas_file, gender, age, min_topics
                )
            else:
                raise ValueError("Either ideas_file or ideas_data must be provided")
            
            # Save topics to JSON artifact
            topics_data = {
                "segment": {
                    "gender": gender,
                    "age": age
                },
                "topics": topics,
                "topicCount": len(topics),
                "generatedAt": datetime.utcnow().isoformat(),
                "minTopicsRequested": min_topics,
                "metadata": custom_config
            }
            
            timestamp = datetime.now().strftime("%Y%m%d")
            topics_filename = f"{timestamp}_topics.json"
            
            topics_path = self.validator.create_artifact(
                step,
                topics_filename,
                topics_data,
                gender,
                age
            )
            artifacts.append(topics_filename)
            
            # Create summary text file
            summary = self._create_summary(topics_data)
            summary_filename = f"{timestamp}_topics_summary.txt"
            summary_path = self.validator.create_artifact(
                step,
                summary_filename,
                summary,
                gender,
                age
            )
            artifacts.append(summary_filename)
            
            # Update progress - completed
            self.validator.update_progress(
                step, "completed",
                f"Generated {len(topics)} topics for {gender}/{age}",
                gender, age,
                artifacts=artifacts
            )
            
            result = {
                "success": True,
                "topics_file": str(topics_path),
                "topics": topics,
                "artifacts": artifacts
            }
            
            # Validate if requested
            if validate:
                validation_report = self.validator.validate_step(step, gender, age)
                result["validation_report"] = validation_report
                
                # Print copilot check
                self.validator.copilot_check(step, gender, age)
            
            return result
            
        except Exception as e:
            # Log failure
            self.validator.update_progress(
                step, "failed",
                f"Error generating topics: {str(e)}",
                gender, age,
                artifacts=artifacts
            )
            raise
    
    def _generate_topics_from_data(
        self,
        ideas: List[str],
        gender: str,
        age: str,
        min_topics: int
    ) -> List[Dict[str, Any]]:
        """
        Generate topics from a list of idea strings.
        
        Uses keyword-based clustering to group ideas into topics.
        """
        from collections import Counter
        import re
        
        # Extract keywords from all ideas
        all_keywords = []
        for idea in ideas:
            keywords = self._extract_keywords(idea)
            all_keywords.extend(keywords)
        
        # Get most common keywords
        keyword_counts = Counter(all_keywords)
        common_keywords = [kw for kw, _ in keyword_counts.most_common(20)]
        
        # Generate topic names based on segment
        topic_names = self._generate_topic_names(gender, age, min_topics)
        
        # Create topics
        topics = []
        used_idea_indices = set()
        
        for i, topic_name in enumerate(topic_names[:min_topics]):
            topic_keywords = self._get_topic_keywords(topic_name)
            
            topic = {
                "id": f"topic_{i+1:03d}",
                "topicName": topic_name,
                "description": self._generate_topic_description(topic_name, gender, age),
                "keywords": topic_keywords[:5],
                "ideaIds": [],
                "viralPotential": self._estimate_viral_potential(topic_name, gender, age),
                "createdAt": datetime.utcnow().isoformat()
            }
            
            # Assign relevant ideas to this topic
            for idx, idea in enumerate(ideas):
                if idx in used_idea_indices:
                    continue
                
                if self._is_idea_relevant_to_topic(idea, topic_keywords):
                    topic["ideaIds"].append(f"idea_{idx+1:03d}")
                    used_idea_indices.add(idx)
                
                # Limit ideas per topic
                if len(topic["ideaIds"]) >= 5:
                    break
            
            topics.append(topic)
        
        # Assign remaining ideas to topics with fewest ideas
        for idx in range(len(ideas)):
            if idx not in used_idea_indices:
                # Find topic with fewest ideas
                min_topic = min(topics, key=lambda t: len(t["ideaIds"]))
                min_topic["ideaIds"].append(f"idea_{idx+1:03d}")
        
        return topics
    
    def _generate_topics_from_file(
        self,
        ideas_file: str,
        gender: str,
        age: str,
        min_topics: int
    ) -> List[Dict[str, Any]]:
        """Generate topics from a markdown file of ideas."""
        # Parse ideas from markdown
        with open(ideas_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        ideas = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('*'):
                # Remove markdown list marker
                idea = line[1:].strip()
                if idea:
                    ideas.append(idea)
        
        return self._generate_topics_from_data(ideas, gender, age, min_topics)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        import re
        # Simple keyword extraction - split on spaces and filter
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        
        # Filter out common stop words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all',
            'can', 'her', 'was', 'one', 'our', 'out', 'day', 'get',
            'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old',
            'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let',
            'put', 'say', 'she', 'too', 'use', 'with', 'that', 'this'
        }
        
        return [w for w in words if w not in stop_words]
    
    def _generate_topic_names(self, gender: str, age: str, count: int) -> List[str]:
        """Generate topic names appropriate for the segment."""
        topics_by_age = {
            "10-13": [
                "Friendship & School Life",
                "Family Bonds",
                "Personal Growth & Discovery",
                "Adventures & Mysteries",
                "Overcoming Challenges",
                "Learning & Education",
                "Hobbies & Talents",
                "Helping Others",
                "Animal Friends",
                "Magic & Fantasy"
            ],
            "14-17": [
                "Friendship Drama & Loyalty",
                "First Love & Romance",
                "Identity & Self-Discovery",
                "Family Conflicts",
                "School & Future Dreams",
                "Social Media & Technology",
                "Peer Pressure & Choices",
                "Creativity & Expression",
                "Mental Health Awareness",
                "Standing Up for Beliefs"
            ],
            "18-23": [
                "Romantic Relationships",
                "Career & Ambitions",
                "Friendship Dynamics",
                "Personal Independence",
                "Life Transitions",
                "Mental Health Journey",
                "Travel & Adventure",
                "Self-Care & Wellness",
                "Social Justice",
                "Finding Purpose"
            ],
            "24-29": [
                "Career Success Stories",
                "Relationship Milestones",
                "Work-Life Balance",
                "Financial Independence",
                "Personal Growth",
                "Family Planning",
                "Friendship Evolution",
                "Health & Fitness",
                "Entrepreneurship",
                "Life Achievements"
            ],
            "30-34": [
                "Parenting & Family",
                "Career Advancement",
                "Marriage & Partnerships",
                "Home & Lifestyle",
                "Health & Wellness",
                "Financial Planning",
                "Personal Fulfillment",
                "Community Involvement",
                "Balancing Priorities",
                "Legacy Building"
            ]
        }
        
        # Get topics for age group or use 18-23 as default
        base_topics = topics_by_age.get(age, topics_by_age["18-23"])
        
        # Return requested count
        return base_topics[:count] if len(base_topics) >= count else base_topics + base_topics[:count-len(base_topics)]
    
    def _get_topic_keywords(self, topic_name: str) -> List[str]:
        """Get keywords associated with a topic name."""
        # Extract keywords from topic name
        import re
        words = re.findall(r'\b[a-zA-Z]{3,}\b', topic_name.lower())
        
        # Add related keywords based on topic
        keyword_map = {
            "friendship": ["friend", "loyalty", "trust", "bond", "support"],
            "love": ["romance", "relationship", "heart", "couple", "dating"],
            "family": ["parent", "sibling", "home", "relative", "bond"],
            "career": ["job", "work", "professional", "success", "ambition"],
            "school": ["education", "learning", "student", "class", "study"],
            "health": ["wellness", "fitness", "mental", "physical", "care"],
            "adventure": ["travel", "explore", "journey", "discovery", "quest"],
            "growth": ["development", "improvement", "change", "progress", "evolve"]
        }
        
        keywords = words.copy()
        for word in words:
            if word in keyword_map:
                keywords.extend(keyword_map[word][:3])
        
        return list(set(keywords))[:10]
    
    def _generate_topic_description(self, topic_name: str, gender: str, age: str) -> str:
        """Generate a description for a topic."""
        return f"Stories about {topic_name.lower()} relevant to {gender} aged {age}"
    
    def _is_idea_relevant_to_topic(self, idea: str, topic_keywords: List[str]) -> bool:
        """Check if an idea is relevant to a topic based on keywords."""
        idea_lower = idea.lower()
        matches = sum(1 for keyword in topic_keywords if keyword in idea_lower)
        return matches >= 1
    
    def _estimate_viral_potential(self, topic_name: str, gender: str, age: str) -> int:
        """Estimate viral potential (0-100) for a topic."""
        # Base score
        score = 70
        
        # High-interest topics
        high_interest = ["love", "romance", "drama", "mystery", "secret", "betrayal"]
        if any(word in topic_name.lower() for word in high_interest):
            score += 15
        
        # Emotional topics
        emotional = ["friendship", "family", "loss", "success", "failure"]
        if any(word in topic_name.lower() for word in emotional):
            score += 10
        
        # Cap at 100
        return min(score, 100)
    
    def _create_summary(self, topics_data: Dict[str, Any]) -> str:
        """Create a human-readable summary of topics."""
        lines = []
        lines.append(f"Topic Generation Summary")
        lines.append(f"========================")
        lines.append(f"")
        lines.append(f"Segment: {topics_data['segment']['gender']}/{topics_data['segment']['age']}")
        lines.append(f"Generated: {topics_data['generatedAt']}")
        lines.append(f"Total Topics: {topics_data['topicCount']}")
        lines.append(f"")
        lines.append(f"Topics:")
        lines.append(f"-------")
        
        for i, topic in enumerate(topics_data['topics'], 1):
            lines.append(f"")
            lines.append(f"{i}. {topic['topicName']}")
            lines.append(f"   Description: {topic['description']}")
            lines.append(f"   Keywords: {', '.join(topic['keywords'])}")
            lines.append(f"   Ideas: {len(topic['ideaIds'])} ideas")
            lines.append(f"   Viral Potential: {topic['viralPotential']}/100")
        
        return '\n'.join(lines)
    
    def batch_generate_topics(
        self,
        segments: List[tuple],
        ideas_directory: str,
        min_topics: int = 8
    ) -> Dict[str, Any]:
        """
        Generate topics for multiple segments in batch.
        
        Args:
            segments: List of (gender, age) tuples
            ideas_directory: Base directory containing idea files
            min_topics: Minimum topics per segment
        
        Returns:
            Dictionary with results for each segment
        """
        results = {}
        
        for gender, age in segments:
            # Find ideas file for this segment
            ideas_path = Path(ideas_directory) / gender / age
            if not ideas_path.exists():
                print(f"⚠️  Skipping {gender}/{age} - no ideas directory found")
                continue
            
            # Find most recent ideas file
            ideas_files = list(ideas_path.glob("*_ideas.md"))
            if not ideas_files:
                print(f"⚠️  Skipping {gender}/{age} - no ideas files found")
                continue
            
            ideas_file = max(ideas_files, key=lambda p: p.name)
            
            print(f"📊 Generating topics for {gender}/{age}...")
            
            try:
                result = self.generate_topics_for_segment(
                    gender=gender,
                    age=age,
                    ideas_file=str(ideas_file),
                    min_topics=min_topics
                )
                results[f"{gender}/{age}"] = result
                print(f"✅ Completed {gender}/{age}: {len(result['topics'])} topics")
            except Exception as e:
                print(f"❌ Failed {gender}/{age}: {e}")
                results[f"{gender}/{age}"] = {"success": False, "error": str(e)}
        
        return results


def main():
    """Example usage of the topic generator with validation."""
    print("="*70)
    print("Topic Generator with Microstep Validation")
    print("="*70)
    
    generator = TopicGeneratorWithValidation()
    
    # Example 1: Generate from sample ideas
    print("\n📝 Example 1: Generate topics from sample ideas")
    sample_ideas = [
        "A woman discovers her best friend has been keeping a life-changing secret",
        "Two friends make a pact that tests their loyalty",
        "A mysterious letter reveals a family secret from the past",
        "A chance encounter leads to an unexpected friendship",
        "Someone must choose between career success and personal relationships",
        "A family reunion brings hidden tensions to the surface",
        "A long-lost relative shows up with surprising news",
        "A workplace rivalry turns into an unexpected partnership",
        "Someone's social media post goes viral for unexpected reasons",
        "A travel adventure leads to personal transformation"
    ]
    
    result = generator.generate_topics_for_segment(
        gender="women",
        age="18-23",
        ideas_data=sample_ideas,
        min_topics=8
    )
    
    if result["success"]:
        print(f"✅ Success! Generated {len(result['topics'])} topics")
        print(f"📄 Topics file: {result['topics_file']}")
        print(f"📦 Artifacts: {', '.join(result['artifacts'])}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
