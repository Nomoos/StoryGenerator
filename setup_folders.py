#!/usr/bin/env python3
"""
Setup script to create the required folder structure for StoryGenerator.
Creates folders for organizing artifacts and project outputs by gender and age buckets.
"""

import os
from pathlib import Path


def create_folder_structure():
    """
    Creates the complete folder structure for the StoryGenerator project.
    
    Folder structure includes:
    - /config/
    - /ideas/{women|men}/{10-13|14-17|18-23}/
    - /topics/{women|men}/{10-13|14-17|18-23}/
    - /titles/{women|men}/{10-13|14-17|18-23}/
    - /scores/{women|men}/{10-13|14-17|18-23}/
    - /scripts/raw_local/{women|men}/{10-13|14-17|18-23}/
    - /scripts/iter_local/{women|men}/{10-13|14-17|18-23}/
    - /scripts/gpt_improved/{women|men}/{10-13|14-17|18-23}/
    - /voices/choice/{women|men}/{10-13|14-17|18-23}/
    - /audio/tts/{women|men}/{10-13|14-17|18-23}/
    - /audio/normalized/{women|men}/{10-13|14-17|18-23}/
    - /subtitles/srt/{women|men}/{10-13|14-17|18-23}/
    - /subtitles/timed/{women|men}/{10-13|14-17|18-23}/
    - /scenes/json/{women|men}/{10-13|14-17|18-23}/
    - /images/keyframes_v1/{women|men}/{10-13|14-17|18-23}/
    - /images/keyframes_v2/{women|men}/{10-13|14-17|18-23}/
    - /videos/ltx/{women|men}/{10-13|14-17|18-23}/
    - /videos/interp/{women|men}/{10-13|14-17|18-23}/
    - /final/{women|men}/{10-13|14-17|18-23}/
    - /research/{python|csharp}/
    """
    
    # Get the root directory (where this script is located)
    root_dir = Path(__file__).parent.absolute()
    
    # Define gender categories
    genders = ["women", "men"]
    
    # Define age buckets
    age_buckets = ["10-13", "14-17", "18-23"]
    
    # Define research categories
    research_categories = ["python", "csharp"]
    
    # Define folder structures with gender and age bucket patterns
    folders_with_gender_age = [
        "ideas",
        "topics",
        "titles",
        "scores",
        "scripts/raw_local",
        "scripts/iter_local",
        "scripts/gpt_improved",
        "voices/choice",
        "audio/tts",
        "audio/normalized",
        "subtitles/srt",
        "subtitles/timed",
        "scenes/json",
        "images/keyframes_v1",
        "images/keyframes_v2",
        "videos/ltx",
        "videos/interp",
        "final",
    ]
    
    # Simple folders (no gender/age buckets)
    simple_folders = [
        "config",
    ]
    
    created_count = 0
    
    # Create simple folders
    print("Creating simple folders...")
    for folder in simple_folders:
        folder_path = root_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        # Add .gitkeep to preserve empty directories
        gitkeep = folder_path / ".gitkeep"
        gitkeep.touch(exist_ok=True)
        print(f"  ✓ Created: {folder}/")
        created_count += 1
    
    # Create folders with gender and age buckets
    print("\nCreating folders with gender and age bucket subdirectories...")
    for base_folder in folders_with_gender_age:
        for gender in genders:
            for age_bucket in age_buckets:
                folder_path = root_dir / base_folder / gender / age_bucket
                folder_path.mkdir(parents=True, exist_ok=True)
                # Add .gitkeep to preserve empty directories
                gitkeep = folder_path / ".gitkeep"
                gitkeep.touch(exist_ok=True)
                print(f"  ✓ Created: {base_folder}/{gender}/{age_bucket}/")
                created_count += 1
    
    # Create research folders
    print("\nCreating research folders...")
    for category in research_categories:
        folder_path = root_dir / "research" / category
        folder_path.mkdir(parents=True, exist_ok=True)
        # Add .gitkeep to preserve empty directories
        gitkeep = folder_path / ".gitkeep"
        gitkeep.touch(exist_ok=True)
        print(f"  ✓ Created: research/{category}/")
        created_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"✅ Successfully created {created_count} folder structures!")
    print(f"{'=' * 60}")
    
    # Print summary
    print("\n📊 Folder Structure Summary:")
    print(f"  - Simple folders: {len(simple_folders)}")
    print(f"  - Folders with gender/age buckets: {len(folders_with_gender_age)} × {len(genders)} × {len(age_buckets)} = {len(folders_with_gender_age) * len(genders) * len(age_buckets)}")
    print(f"  - Research folders: {len(research_categories)}")
    print(f"  - Total: {created_count} folders")


if __name__ == "__main__":
    print("=" * 60)
    print("StoryGenerator - Folder Structure Setup")
    print("=" * 60)
    print()
    
    create_folder_structure()
    
    print("\n✨ Setup complete! All folders are ready for use.")
