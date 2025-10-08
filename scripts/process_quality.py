#!/usr/bin/env python3
"""
Iterative Quality Processor for StoryGenerator

Handles quality scoring and iterative refinement of generated content.
Low-scoring items are moved back to previous pipeline stages with underscore prefix.
"""

import os
import json
import shutil
import yaml
from pathlib import Path
from datetime import datetime


def load_config():
    """Load configuration including quality thresholds."""
    config_path = Path(__file__).parent.parent / "data" / "config" / "audience_config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("⚠️  Config file not found, using defaults")
        return {
            "quality_thresholds": {
                "min_score": 70,
                "reprocess_score": 50,
                "underscore_prefix": "_"
            }
        }


def load_scoring_config():
    """Load viral scoring configuration from YAML file."""
    config_path = Path(__file__).parent.parent / "config" / "scoring.yaml"
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print("⚠️  Scoring config not found, using defaults")
        return {
            "viral": {
                "novelty": 0.25,
                "emotional": 0.25,
                "clarity": 0.20,
                "replay": 0.15,
                "share": 0.15
            },
            "thresholds": {
                "excellent": 85,
                "good": 70,
                "acceptable": 55,
                "poor": 40
            }
        }


def assess_content_quality(content_data, content_type="generic"):
    """
    Assess content quality based on various metrics.
    
    Args:
        content_data: Dictionary with content information
        content_type: Type of content (idea, topic, title, script, etc.)
        
    Returns:
        Dictionary with individual metric scores
    """
    scores = {}
    
    # Extract relevant content text
    content_text = ""
    if content_type == "idea":
        content_text = content_data.get("title", "") + " " + content_data.get("synopsis", "") + " " + content_data.get("hook", "")
    elif content_type == "topic":
        content_text = content_data.get("title", "") + " " + content_data.get("description", "")
    elif content_type == "title":
        content_text = content_data.get("title", "") or content_data.get("text", "")
    elif content_type == "script":
        content_text = content_data.get("script", "") or content_data.get("content", "")
    else:
        # Generic content - look for common fields
        content_text = (content_data.get("title", "") + " " + 
                       content_data.get("description", "") + " " +
                       content_data.get("text", "") + " " +
                       content_data.get("content", ""))
    
    content_text = content_text.strip()
    
    # Novelty: Unique, surprising content
    scores["novelty"] = assess_novelty(content_data, content_text, content_type)
    
    # Emotional: Emotional impact and resonance
    scores["emotional"] = assess_emotional_impact(content_data, content_text, content_type)
    
    # Clarity: Clear, easy to understand
    scores["clarity"] = assess_clarity(content_data, content_text, content_type)
    
    # Replay: Rewatchability factor
    scores["replay"] = assess_replay_value(content_data, content_text, content_type)
    
    # Share: Shareability and virality
    scores["share"] = assess_shareability(content_data, content_text, content_type)
    
    return scores


def assess_novelty(content_data, content_text, content_type):
    """Assess novelty/uniqueness of content (0-100)."""
    score = 50  # Baseline
    
    # Check for unique or surprising elements
    novelty_keywords = ["secret", "hidden", "revealed", "shocking", "amazing", "unexpected", 
                       "surprising", "unbelievable", "mystery", "discovery", "unknown"]
    
    text_lower = content_text.lower()
    keyword_count = sum(1 for kw in novelty_keywords if kw in text_lower)
    score += min(keyword_count * 5, 25)  # Up to +25 for keywords
    
    # Check for question format (creates curiosity)
    if "?" in content_text:
        score += 10
    
    # Penalize very short content (likely lacks detail)
    if len(content_text) < 50:
        score -= 15
    elif len(content_text) > 200:
        score += 10
    
    # Check for unique themes/keywords if available
    if "themes" in content_data or "keywords" in content_data:
        themes = content_data.get("themes", []) + content_data.get("keywords", [])
        if len(themes) >= 3:
            score += 15
    
    return min(max(score, 0), 100)


def assess_emotional_impact(content_data, content_text, content_type):
    """Assess emotional resonance of content (0-100)."""
    score = 50  # Baseline
    
    # Emotional trigger words
    positive_emotions = ["love", "joy", "amazing", "beautiful", "inspiring", "incredible", 
                        "awesome", "wonderful", "heartwarming", "uplifting"]
    negative_emotions = ["fear", "danger", "loss", "tragedy", "shocking", "horrifying",
                        "devastating", "heartbreaking", "terrifying", "crisis"]
    curiosity_emotions = ["mystery", "secret", "hidden", "unknown", "revelation", "truth",
                         "discover", "uncover", "expose", "reveal"]
    
    text_lower = content_text.lower()
    
    # Count emotional triggers
    emotion_score = 0
    emotion_score += sum(3 for word in positive_emotions if word in text_lower)
    emotion_score += sum(3 for word in negative_emotions if word in text_lower)
    emotion_score += sum(4 for word in curiosity_emotions if word in text_lower)
    
    score += min(emotion_score, 30)
    
    # Check for personal/relatable elements
    personal_words = ["you", "your", "my", "our", "we", "us", "everyone", "people"]
    if any(word in text_lower for word in personal_words):
        score += 10
    
    # Check genre/category for emotional content
    genre = content_data.get("genre", "").lower()
    category = content_data.get("category", "").lower()
    
    if genre in ["drama", "romance", "thriller", "horror"] or category in ["human interest", "emotional"]:
        score += 15
    
    return min(max(score, 0), 100)


def assess_clarity(content_data, content_text, content_type):
    """Assess clarity and understandability (0-100)."""
    score = 70  # Start higher for clarity
    
    # Check if content has proper structure
    if content_type == "idea":
        required_fields = ["title", "synopsis", "hook"]
        present = sum(1 for field in required_fields if content_data.get(field))
        score += (present / len(required_fields)) * 15
    elif content_type == "topic":
        required_fields = ["title", "description"]
        present = sum(1 for field in required_fields if content_data.get(field))
        score += (present / len(required_fields)) * 15
    elif content_type == "title":
        # Title-specific clarity checks
        title = content_data.get("title", "") or content_data.get("text", "")
        if 20 <= len(title) <= 100:
            score += 15
        else:
            score -= 10
    
    # Check for overly complex or jargon-heavy text
    if len(content_text) > 0:
        words = content_text.split()
        if len(words) > 0:
            avg_word_length = sum(len(word) for word in words) / len(words)
            if avg_word_length < 6:
                score += 10  # Simple, clear language
            elif avg_word_length > 9:
                score -= 15  # Potentially complex
    
    # Check for clear structure indicators
    structure_indicators = [":", "-", "•", "\n", "1.", "2.", "first", "then", "finally"]
    if any(indicator in content_text for indicator in structure_indicators):
        score += 5
    
    # Penalize very short content (lacks detail)
    if len(content_text) < 30:
        score -= 20
    
    return min(max(score, 0), 100)


def assess_replay_value(content_data, content_text, content_type):
    """Assess rewatchability/replay value (0-100)."""
    score = 50  # Baseline
    
    # Content with depth and layers has higher replay value
    complexity_indicators = ["because", "however", "although", "while", "despite",
                            "therefore", "moreover", "furthermore", "additionally"]
    
    text_lower = content_text.lower()
    complexity_count = sum(1 for indicator in complexity_indicators if indicator in text_lower)
    score += min(complexity_count * 3, 20)
    
    # Multiple themes or keywords suggest depth
    themes_count = len(content_data.get("themes", [])) + len(content_data.get("keywords", []))
    if themes_count >= 4:
        score += 15
    elif themes_count >= 2:
        score += 10
    
    # Mystery/suspense elements increase replay value
    replay_keywords = ["mystery", "secret", "twist", "reveal", "hidden", "clue",
                      "puzzle", "enigma", "riddle", "code"]
    keyword_match = sum(1 for kw in replay_keywords if kw in text_lower)
    score += min(keyword_match * 5, 15)
    
    # Educational or informative content has replay value
    educational_keywords = ["learn", "discover", "understand", "explained", "guide",
                           "how", "why", "what", "tips", "tricks"]
    edu_match = sum(1 for kw in educational_keywords if kw in text_lower)
    score += min(edu_match * 3, 15)
    
    return min(max(score, 0), 100)


def assess_shareability(content_data, content_text, content_type):
    """Assess shareability and viral potential (0-100)."""
    score = 50  # Baseline
    
    # Shareable content often has strong hook/headline
    shareable_keywords = ["truth", "revealed", "exposed", "secret", "shocking",
                         "everyone", "nobody", "never", "always", "you won't believe",
                         "this is why", "the real reason", "what happens when"]
    
    text_lower = content_text.lower()
    keyword_count = sum(1 for kw in shareable_keywords if kw in text_lower)
    score += min(keyword_count * 6, 25)
    
    # Questions are highly shareable
    question_count = content_text.count("?")
    score += min(question_count * 8, 15)
    
    # Universal/relatable topics are more shareable
    universal_keywords = ["everyone", "all", "anyone", "nobody", "people", "we", "us",
                         "human", "life", "world", "society"]
    universal_count = sum(1 for kw in universal_keywords if kw in text_lower)
    score += min(universal_count * 4, 15)
    
    # Controversy or strong opinions increase shares
    controversial_keywords = ["wrong", "truth", "lie", "fake", "real", "actually",
                             "truth is", "reality", "expose", "hidden"]
    controversy_count = sum(1 for kw in controversial_keywords if kw in text_lower)
    score += min(controversy_count * 3, 10)
    
    # Numbers and lists are shareable
    if any(char.isdigit() for char in content_text):
        score += 10
    
    return min(max(score, 0), 100)


def calculate_score(content_data, scoring_config=None):
    """
    Calculate quality score for content.
    
    Args:
        content_data: Dictionary with content metrics
        scoring_config: Scoring configuration (viral weights, thresholds)
        
    Returns:
        Score from 0-100
    """
    # Load scoring config if not provided
    if scoring_config is None:
        scoring_config = load_scoring_config()
    
    # Determine content type from data
    content_type = "generic"
    if "idea_id" in content_data or "synopsis" in content_data:
        content_type = "idea"
    elif "topic_id" in content_data or ("category" in content_data and "keywords" in content_data):
        content_type = "topic"
    elif "title" in content_data and len(content_data) <= 3:
        content_type = "title"
    elif "script" in content_data or "scenes" in content_data:
        content_type = "script"
    
    # Check if content already has metric scores
    if all(metric in content_data for metric in ["novelty", "emotional", "clarity", "replay", "share"]):
        # Use existing scores
        metric_scores = {
            "novelty": content_data.get("novelty", 50),
            "emotional": content_data.get("emotional", 50),
            "clarity": content_data.get("clarity", 50),
            "replay": content_data.get("replay", 50),
            "share": content_data.get("share", 50)
        }
    else:
        # Assess content quality
        metric_scores = assess_content_quality(content_data, content_type)
    
    # Get viral scoring weights
    viral_weights = scoring_config.get("viral", {
        "novelty": 0.25,
        "emotional": 0.25,
        "clarity": 0.20,
        "replay": 0.15,
        "share": 0.15
    })
    
    # Calculate weighted score
    score = 0
    for metric, weight in viral_weights.items():
        if metric in metric_scores:
            score += metric_scores[metric] * weight
    
    return score


def mark_for_reprocessing(file_path, prefix="_"):
    """
    Rename file with underscore prefix to mark for reprocessing.
    
    Args:
        file_path: Path to file
        prefix: Prefix to add (default: "_")
        
    Returns:
        New file path
    """
    file_path = Path(file_path)
    parent = file_path.parent
    name = file_path.name
    
    # Don't re-prefix if already underscored
    if name.startswith(prefix):
        return file_path
    
    new_name = f"{prefix}{name}"
    new_path = parent / new_name
    
    # Rename the file
    try:
        file_path.rename(new_path)
        print(f"  ✓ Marked for reprocessing: {name} → {new_name}")
        return new_path
    except Exception as e:
        print(f"  ❌ Error renaming {name}: {e}")
        return file_path


def move_to_previous_stage(file_path, current_stage, previous_stage, base_path="Generator"):
    """
    Move low-scoring content back to previous pipeline stage.
    
    Args:
        file_path: Path to current file
        current_stage: Current pipeline stage (e.g., "topics")
        previous_stage: Previous pipeline stage (e.g., "ideas")
        base_path: Base path for generator folders
        
    Returns:
        New file path or None if failed
    """
    file_path = Path(file_path)
    
    # Extract audience segments (gender/age) from path
    parts = file_path.parts
    try:
        # Find the audience segments
        gender = None
        age = None
        for i, part in enumerate(parts):
            if part in ["men", "women"]:
                gender = part
                if i + 1 < len(parts):
                    age = parts[i + 1]
                break
        
        if not gender or not age:
            print(f"  ⚠️ Could not extract audience from path: {file_path}")
            return None
        
        # Build destination path
        root = Path(__file__).parent
        if base_path:
            dest_dir = root / base_path / previous_stage / gender / age
        else:
            dest_dir = root / previous_stage / gender / age
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Move file
        dest_path = dest_dir / file_path.name
        shutil.move(str(file_path), str(dest_path))
        print(f"  ✓ Moved to {previous_stage}: {file_path.name}")
        return dest_path
        
    except Exception as e:
        print(f"  ❌ Error moving file: {e}")
        return None


def process_content_folder(folder_path, stage_name, previous_stage=None, config=None):
    """
    Process all content in a folder, scoring and handling low-quality items.
    
    Args:
        folder_path: Path to folder to process
        stage_name: Current stage name
        previous_stage: Previous stage to move low-scoring items to
        config: Configuration dictionary
    """
    if config is None:
        config = load_config()
    
    # Load scoring configuration
    scoring_config = load_scoring_config()
    
    thresholds = config.get("quality_thresholds", {})
    min_score = thresholds.get("min_score", 70)
    reprocess_score = thresholds.get("reprocess_score", 50)
    prefix = thresholds.get("underscore_prefix", "_")
    
    print(f"\nProcessing {stage_name} folder: {folder_path}")
    print(f"  - Minimum Score: {min_score}")
    print(f"  - Reprocess Score: {reprocess_score}")
    print()
    
    folder_path = Path(folder_path)
    if not folder_path.exists():
        print(f"  ⚠️ Folder does not exist: {folder_path}")
        return
    
    processed_count = 0
    reprocessed_count = 0
    moved_count = 0
    
    # Process all JSON files in folder
    for json_file in folder_path.glob("*.json"):
        # Skip underscored files (already marked for reprocessing)
        if json_file.name.startswith(prefix):
            continue
        
        try:
            with open(json_file, 'r') as f:
                content_data = json.load(f)
            
            # Calculate score
            score = content_data.get("score", calculate_score(content_data, scoring_config))
            
            print(f"  {json_file.name}: Score {score:.1f}")
            
            # Handle based on score
            if score >= min_score:
                # Good quality, keep as is
                processed_count += 1
            elif score >= reprocess_score:
                # Moderate quality, mark for reprocessing
                mark_for_reprocessing(json_file, prefix)
                reprocessed_count += 1
            else:
                # Low quality, move back to previous stage
                if previous_stage:
                    new_path = move_to_previous_stage(json_file, stage_name, previous_stage)
                    if new_path:
                        # Mark it in the previous stage
                        mark_for_reprocessing(new_path, prefix)
                        moved_count += 1
                else:
                    # No previous stage, just mark for reprocessing
                    mark_for_reprocessing(json_file, prefix)
                    reprocessed_count += 1
        
        except Exception as e:
            print(f"  ❌ Error processing {json_file.name}: {e}")
    
    print()
    print(f"📊 Processing Summary:")
    print(f"  - Processed: {processed_count}")
    print(f"  - Marked for reprocessing: {reprocessed_count}")
    print(f"  - Moved to previous stage: {moved_count}")


def batch_process_pipeline(base_path="Generator", config=None):
    """
    Process entire pipeline, scoring and handling quality iteratively.
    
    Args:
        base_path: Base path for generator folders
        config: Configuration dictionary
    """
    if config is None:
        config = load_config()
    
    root = Path(__file__).parent
    if base_path:
        generator_root = root / base_path
    else:
        generator_root = root
    
    print("=" * 60)
    print("Iterative Quality Processor")
    print("=" * 60)
    
    # Define pipeline stages with their previous stages
    pipeline_stages = [
        ("trends", None),
        ("ideas", "trends"),
        ("topics", "ideas"),
        ("titles", "topics"),
        ("data/raw_local", "topics"),
        ("data/iter_local", "data/raw_local"),
        ("data/gpt_improved", "data/iter_local"),
    ]
    
    # Get audience configuration
    audience = config.get("audience", {})
    genders = [g["name"] for g in audience.get("genders", [])]
    age_groups = [a["range"] for a in audience.get("age_groups", [])]
    
    # Process each stage for each audience segment
    for stage_name, previous_stage in pipeline_stages:
        for gender in genders:
            for age_group in age_groups:
                folder_path = generator_root / stage_name / gender / age_group
                if folder_path.exists():
                    process_content_folder(folder_path, stage_name, previous_stage, config)
    
    print("\n" + "=" * 60)
    print("✅ Pipeline processing complete!")
    print("=" * 60)


def main():
    """Main entry point."""
    import sys
    
    config = load_config()
    
    if len(sys.argv) > 1:
        # Process specific folder
        folder_path = sys.argv[1]
        stage_name = sys.argv[2] if len(sys.argv) > 2 else "content"
        previous_stage = sys.argv[3] if len(sys.argv) > 3 else None
        process_content_folder(folder_path, stage_name, previous_stage, config)
    else:
        # Process entire pipeline
        base_path = config.get("folder_structure", {}).get("base_path", "Generator")
        batch_process_pipeline(base_path, config)


if __name__ == "__main__":
    main()
