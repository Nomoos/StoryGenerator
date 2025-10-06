#!/usr/bin/env python3
"""
Verification script to ensure all required folders exist.
"""

import os
from pathlib import Path


def verify_folder_structure():
    """Verify that all required folders exist."""
    
    root_dir = Path(__file__).parent.absolute()
    
    genders = ["women", "men"]
    age_buckets = ["10-13", "14-17", "18-23"]
    research_categories = ["python", "csharp"]
    
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
    
    simple_folders = ["config"]
    
    missing = []
    found = 0
    
    # Check simple folders
    for folder in simple_folders:
        folder_path = root_dir / folder
        if folder_path.exists() and folder_path.is_dir():
            found += 1
        else:
            missing.append(str(folder_path))
    
    # Check folders with gender and age buckets
    for base_folder in folders_with_gender_age:
        for gender in genders:
            for age_bucket in age_buckets:
                folder_path = root_dir / base_folder / gender / age_bucket
                if folder_path.exists() and folder_path.is_dir():
                    found += 1
                else:
                    missing.append(str(folder_path))
    
    # Check research folders
    for category in research_categories:
        folder_path = root_dir / "research" / category
        if folder_path.exists() and folder_path.is_dir():
            found += 1
        else:
            missing.append(str(folder_path))
    
    # Report results
    total = 1 + (len(folders_with_gender_age) * len(genders) * len(age_buckets)) + len(research_categories)
    
    print(f"Folder Structure Verification")
    print(f"=" * 60)
    print(f"Expected folders: {total}")
    print(f"Found folders: {found}")
    print(f"Missing folders: {len(missing)}")
    print()
    
    if missing:
        print("❌ Missing folders:")
        for folder in missing:
            print(f"  - {folder}")
        return False
    else:
        print("✅ All required folders exist!")
        return True


if __name__ == "__main__":
    success = verify_folder_structure()
    exit(0 if success else 1)
