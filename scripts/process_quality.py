#!/usr/bin/env python3
"""
Iterative Quality Processor for StoryGenerator

Handles quality scoring and iterative refinement of generated content.
Low-scoring items are moved back to previous pipeline stages with underscore prefix.
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime


def load_config():
    """Load configuration including quality thresholds."""
    config_path = Path(__file__).parent / "config" / "audience_config.json"
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


def calculate_score(content_data):
    """
    Calculate quality score for content.
    
    Args:
        content_data: Dictionary with content metrics
        
    Returns:
        Score from 0-100
    """
    # Example scoring logic - customize based on your metrics
    score = 0
    weights = {
        "clarity": 0.3,
        "engagement": 0.3,
        "relevance": 0.2,
        "technical_quality": 0.2
    }
    
    for metric, weight in weights.items():
        if metric in content_data:
            score += content_data[metric] * weight
    
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
            score = content_data.get("score", calculate_score(content_data))
            
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
