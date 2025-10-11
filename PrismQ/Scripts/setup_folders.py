#!/usr/bin/env python3
"""
Setup script to create the required folder structure for StoryGenerator.
Creates folders for organizing artifacts and project outputs based on configuration.
Supports configurable audience demographics (gender, age, country) with preference percentages.
"""

import os
import json
import sys
from pathlib import Path


def load_config(config_path=None):
    """Load audience configuration from JSON file."""
    if config_path is None:
        # Default config path
        root_dir = Path(__file__).parent.absolute()
        config_path = root_dir / "config" / "audience_config.json"

    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        print("Creating default configuration...")
        return create_default_config()
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing config file: {e}")
        sys.exit(1)


def create_default_config():
    """Create a default configuration if none exists."""
    return {
        "audience": {
            "genders": [
                {"name": "men", "preference_percentage": 50},
                {"name": "women", "preference_percentage": 50},
            ],
            "countries": [{"name": "US", "preference_percentage": 100}],
            "age_groups": [
                {"range": "10-14", "preference_percentage": 10},
                {"range": "15-19", "preference_percentage": 20},
                {"range": "20-24", "preference_percentage": 30},
                {"range": "25-29", "preference_percentage": 25},
                {"range": "30-34", "preference_percentage": 15},
            ],
        },
        "folder_structure": {
            "content_folders": ["ideas", "topics", "titles", "scores"],
            "script_folders": ["data/raw_local"],
            "simple_folders": ["config"],
        },
    }


def create_folder_structure(config_path=None):
    """
    Creates the complete folder structure for the StoryGenerator project based on configuration.

    Args:
        config_path: Optional path to configuration JSON file
    """

    # Load configuration
    config = load_config(config_path)

    # Get the root directory (where this script is located)
    root_dir = Path(__file__).parent.absolute()

    # Extract audience configuration
    audience = config.get("audience", {})
    genders = [g["name"] for g in audience.get("genders", [])]
    age_groups = [a["range"] for a in audience.get("age_groups", [])]
    countries = [c["name"] for c in audience.get("countries", [])]

    # Extract folder structure configuration
    folder_structure = config.get("folder_structure", {})
    base_path = folder_structure.get("base_path", "")

    # Collect all folders that need gender/age structure
    folders_with_gender_age = []
    folders_with_gender_age.extend(folder_structure.get("content_folders", []))
    folders_with_gender_age.extend(folder_structure.get("script_folders", []))
    folders_with_gender_age.extend(folder_structure.get("voice_folders", []))
    folders_with_gender_age.extend(folder_structure.get("audio_folders", []))
    folders_with_gender_age.extend(folder_structure.get("subtitle_folders", []))
    folders_with_gender_age.extend(folder_structure.get("scene_folders", []))
    folders_with_gender_age.extend(folder_structure.get("image_folders", []))
    folders_with_gender_age.extend(folder_structure.get("video_folders", []))
    folders_with_gender_age.extend(folder_structure.get("final_folders", []))

    # Research and simple folders
    research_folders = folder_structure.get("research_folders", [])
    simple_folders = folder_structure.get("simple_folders", [])

    created_count = 0

    # Create base Generator folder if specified
    if base_path:
        base_folder = root_dir / base_path
        base_folder.mkdir(parents=True, exist_ok=True)
        print(f"Creating base folder: {base_path}/")
        print()
    else:
        base_folder = root_dir

    # Create simple folders
    print("Creating simple folders...")
    for folder in simple_folders:
        folder_path = base_folder / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        # Add .gitkeep to preserve empty directories
        gitkeep = folder_path / ".gitkeep"
        gitkeep.touch(exist_ok=True)
        print(f"  ✓ Created: {base_path + '/' if base_path else ''}{folder}/")
        created_count += 1

    # Create folders with gender and age buckets
    print("\nCreating folders with gender and age group subdirectories...")
    for base_folder_name in folders_with_gender_age:
        for gender in genders:
            for age_group in age_groups:
                folder_path = base_folder / base_folder_name / gender / age_group
                folder_path.mkdir(parents=True, exist_ok=True)
                # Add .gitkeep to preserve empty directories
                gitkeep = folder_path / ".gitkeep"
                gitkeep.touch(exist_ok=True)
                print(
                    f"  ✓ Created: {base_path + '/' if base_path else ''}{base_folder_name}/{gender}/{age_group}/"
                )
                created_count += 1

    # Create research folders
    print("\nCreating research folders...")
    for research_folder in research_folders:
        folder_path = base_folder / research_folder
        folder_path.mkdir(parents=True, exist_ok=True)
        # Add .gitkeep to preserve empty directories
        gitkeep = folder_path / ".gitkeep"
        gitkeep.touch(exist_ok=True)
        print(f"  ✓ Created: {base_path + '/' if base_path else ''}{research_folder}/")
        created_count += 1

    print(f"\n{'=' * 60}")
    print(f"✅ Successfully created {created_count} folder structures!")
    print(f"{'=' * 60}")

    # Print summary
    print("\n📊 Folder Structure Summary:")
    print(f"  - Base path: {base_path if base_path else 'root'}")
    print(f"  - Simple folders: {len(simple_folders)}")
    print(
        f"  - Folders with gender/age structure: {len(folders_with_gender_age)} × {len(genders)} × {len(age_groups)} = {len(folders_with_gender_age) * len(genders) * len(age_groups)}"
    )
    print(f"  - Research folders: {len(research_folders)}")
    print(f"  - Total: {created_count} folders")
    print(f"\n📋 Configuration:")
    print(f"  - Genders: {', '.join(genders)}")
    print(f"  - Age Groups: {', '.join(age_groups)}")
    print(f"  - Countries: {', '.join(countries)}")

    # Extract quality thresholds if present
    quality_thresholds = config.get("quality_thresholds", {})
    if quality_thresholds:
        print(f"\n📈 Quality Thresholds:")
        print(f"  - Minimum Score: {quality_thresholds.get('min_score', 'N/A')}")
        print(f"  - Reprocess Score: {quality_thresholds.get('reprocess_score', 'N/A')}")
        print(f"  - Underscore Prefix: {quality_thresholds.get('underscore_prefix', 'N/A')}")


if __name__ == "__main__":
    print("=" * 60)
    print("StoryGenerator - Folder Structure Setup")
    print("=" * 60)
    print()

    # Check for config file argument
    config_path = None
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        print(f"Using config file: {config_path}\n")

    create_folder_structure(config_path)

    print("\n✨ Setup complete! All folders are ready for use.")
