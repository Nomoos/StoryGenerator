#!/usr/bin/env python3
"""
Demonstration of the Microstep Validation system.

Shows how to:
1. Create artifacts for a microstep
2. Log configuration used
3. Update progress tracking
4. Perform validation checks
"""

import sys
import os
from pathlib import Path

# Add src/Python to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "Python"))

from Tools.MicrostepValidator import (
    MicrostepValidator,
    create_microstep_artifact,
    log_microstep_config,
    update_microstep_progress,
    copilot_check_microstep,
)


def demo_basic_usage():
    """Demonstrate basic usage of MicrostepValidator."""
    print("\n" + "=" * 70)
    print("DEMO 1: Basic Microstep Validation Usage")
    print("=" * 70)

    # Initialize validator
    validator = MicrostepValidator()

    # List all available microsteps
    print("\n📋 Available Microsteps:")
    validator.list_microsteps()


def demo_create_artifacts():
    """Demonstrate creating artifacts for a microstep."""
    print("\n" + "=" * 70)
    print("DEMO 2: Creating Artifacts")
    print("=" * 70)

    # Example: Create artifacts for Step 2 (Ideas generation)
    step = 2
    gender = "women"
    age = "18-23"

    print(f"\n📝 Creating artifacts for Step {step}: Ideas Generation")
    print(f"   Target: {gender}/{age}")

    # Create a sample idea artifact
    idea_content = {
        "id": "idea_001",
        "title": "A mysterious letter arrives",
        "description": "A woman receives a letter that reveals a family secret",
        "themes": ["mystery", "family", "secrets"],
        "viral_potential": 85,
        "timestamp": "2024-01-01T12:00:00",
    }

    artifact_path = create_microstep_artifact(
        step_number=step,
        artifact_name="idea_001.json",
        content=idea_content,
        gender=gender,
        age=age,
    )

    print(f"✅ Created artifact: {artifact_path}")


def demo_log_config():
    """Demonstrate logging configuration for a microstep."""
    print("\n" + "=" * 70)
    print("DEMO 3: Logging Configuration")
    print("=" * 70)

    step = 2
    gender = "women"
    age = "18-23"

    print(f"\n⚙️  Logging config for Step {step}: Ideas Generation")

    # Log configuration (will auto-extract relevant config)
    config_path = log_microstep_config(step_number=step, gender=gender, age=age)

    print(f"✅ Logged config: {config_path}")

    # You can also provide custom config subset
    custom_config = {"model": "gpt-4", "temperature": 0.7, "max_tokens": 500}

    config_path2 = log_microstep_config(
        step_number=step, config_subset=custom_config, gender=gender, age=age
    )

    print(f"✅ Logged custom config: {config_path2}")


def demo_progress_tracking():
    """Demonstrate progress tracking for a microstep."""
    print("\n" + "=" * 70)
    print("DEMO 4: Progress Tracking")
    print("=" * 70)

    step = 2
    gender = "women"
    age = "18-23"

    print(f"\n📊 Tracking progress for Step {step}: Ideas Generation")

    # Step 1: Mark as started
    progress_path = update_microstep_progress(
        step_number=step,
        status="started",
        details="Beginning idea generation with GPT-4",
        gender=gender,
        age=age,
    )
    print(f"✅ Progress updated (started): {progress_path}")

    # Step 2: Mark as in progress with artifacts
    progress_path = update_microstep_progress(
        step_number=step,
        status="in_progress",
        details="Generated 5 ideas so far",
        gender=gender,
        age=age,
        artifacts=["idea_001.json", "idea_002.json", "idea_003.json"],
    )
    print(f"✅ Progress updated (in progress): {progress_path}")

    # Step 3: Mark as completed
    progress_path = update_microstep_progress(
        step_number=step,
        status="completed",
        details="Successfully generated 20 ideas with high viral potential",
        gender=gender,
        age=age,
        artifacts=[
            "idea_001.json",
            "idea_002.json",
            "idea_003.json",
            "idea_004.json",
            "idea_005.json",
            "idea_006.json",
            "config_ideas_20240101_120000.yaml",
        ],
    )
    print(f"✅ Progress updated (completed): {progress_path}")


def demo_validation():
    """Demonstrate validation checks for a microstep."""
    print("\n" + "=" * 70)
    print("DEMO 5: Validation Checks")
    print("=" * 70)

    step = 2
    gender = "women"
    age = "18-23"

    print(f"\n🔍 Validating Step {step}: Ideas Generation")

    # Perform validation
    validator = MicrostepValidator()
    report = validator.validate_step(step, gender, age)

    print(f"\n📄 Validation Report:")
    print(f"   Step: {report['step_name']}")
    print(f"   Folder: {report['folder']}")
    print(f"   Valid: {report['is_valid']}")
    print(f"   Artifacts: {len(report['artifacts'])}")

    print(f"\n   Checks:")
    for check, result in report["checks"].items():
        status = "✅" if result else "❌"
        print(f"      {status} {check}: {result}")


def demo_copilot_check():
    """Demonstrate @copilot check functionality."""
    print("\n" + "=" * 70)
    print("DEMO 6: @copilot Check")
    print("=" * 70)

    step = 2
    gender = "women"
    age = "18-23"

    print(f"\n🤖 Performing @copilot check for Step {step}")

    # Perform copilot check (prints formatted report)
    copilot_check_microstep(step, gender, age)


def demo_complete_workflow():
    """Demonstrate a complete workflow for a microstep."""
    print("\n" + "=" * 70)
    print("DEMO 7: Complete Microstep Workflow")
    print("=" * 70)

    step = 10  # Audio TTS
    gender = "men"
    age = "24-29"

    print(f"\n🎬 Running complete workflow for Step {step}: Audio TTS")
    print(f"   Target: {gender}/{age}")

    validator = MicrostepValidator()

    # 1. Start the process
    print("\n1️⃣  Starting process...")
    update_microstep_progress(
        step_number=step,
        status="started",
        details="Initializing ElevenLabs TTS with voice selection",
        gender=gender,
        age=age,
    )

    # 2. Log configuration
    print("2️⃣  Logging configuration...")
    log_microstep_config(step_number=step, gender=gender, age=age)

    # 3. Create artifacts (simulated)
    print("3️⃣  Creating artifacts...")
    artifacts = []

    # Create sample audio metadata
    audio_metadata = {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
        "model": "eleven_multilingual_v2",
        "duration_seconds": 45.3,
        "sample_rate": 48000,
        "bitrate": "128kbps",
        "format": "mp3",
    }

    artifact_path = create_microstep_artifact(
        step_number=step,
        artifact_name="audio_metadata.json",
        content=audio_metadata,
        gender=gender,
        age=age,
    )
    artifacts.append(artifact_path.name)

    # Create sample audio info text
    audio_info = """Audio Generation Summary
    
Voice: Professional Male (Rachel)
Duration: 45.3 seconds
Quality: High (128kbps)
Status: Successfully generated
"""

    artifact_path = create_microstep_artifact(
        step_number=step, artifact_name="audio_info.txt", content=audio_info, gender=gender, age=age
    )
    artifacts.append(artifact_path.name)

    # 4. Update progress with artifacts
    print("4️⃣  Updating progress...")
    update_microstep_progress(
        step_number=step,
        status="completed",
        details="Audio generated successfully with ElevenLabs API",
        gender=gender,
        age=age,
        artifacts=artifacts,
    )

    # 5. Perform validation
    print("5️⃣  Performing validation...")
    copilot_check_microstep(step, gender, age)

    print("\n✅ Complete workflow finished!")


def demo_batch_processing():
    """Demonstrate batch processing across multiple audiences."""
    print("\n" + "=" * 70)
    print("DEMO 8: Batch Processing Multiple Audiences")
    print("=" * 70)

    step = 4  # Titles
    audiences = [("women", "18-23"), ("women", "24-29"), ("men", "18-23"), ("men", "24-29")]

    print(f"\n🎯 Processing Step {step}: Titles for {len(audiences)} audiences")

    for gender, age in audiences:
        print(f"\n   Processing {gender}/{age}...")

        # Create sample title
        title_data = {
            "id": f"title_{gender}_{age}_001",
            "title": f"You Won't Believe What Happened Next!",
            "target": f"{gender}/{age}",
            "viral_score": 88,
        }

        # Create artifact
        create_microstep_artifact(
            step_number=step,
            artifact_name=f"title_{gender}_{age}_001.json",
            content=title_data,
            gender=gender,
            age=age,
        )

        # Log config
        log_microstep_config(step, gender=gender, age=age)

        # Update progress
        update_microstep_progress(
            step_number=step,
            status="completed",
            details=f"Generated viral title for {gender}/{age}",
            gender=gender,
            age=age,
            artifacts=[f"title_{gender}_{age}_001.json"],
        )

        print(f"      ✅ Completed {gender}/{age}")

    print("\n✅ Batch processing complete!")

    # Validate all audiences
    print("\n🔍 Validating all audiences...")
    for gender, age in audiences:
        print(f"\n   Checking {gender}/{age}:")
        validator = MicrostepValidator()
        report = validator.validate_step(step, gender, age)
        status = "✅ VALID" if report["is_valid"] else "❌ INVALID"
        print(f"      Status: {status}")
        print(f"      Artifacts: {len(report['artifacts'])}")


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("MICROSTEP VALIDATION SYSTEM - COMPREHENSIVE DEMO")
    print("=" * 70)

    demos = [
        ("Basic Usage", demo_basic_usage),
        ("Create Artifacts", demo_create_artifacts),
        ("Log Configuration", demo_log_config),
        ("Progress Tracking", demo_progress_tracking),
        ("Validation", demo_validation),
        ("@copilot Check", demo_copilot_check),
        ("Complete Workflow", demo_complete_workflow),
        ("Batch Processing", demo_batch_processing),
    ]

    print("\nAvailable Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print(f"  0. Run All Demos")

    try:
        choice = input("\nSelect demo to run (0-8): ").strip()

        if choice == "0":
            # Run all demos
            for name, demo_func in demos:
                try:
                    demo_func()
                except Exception as e:
                    print(f"\n❌ Error in {name}: {e}")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            # Run selected demo
            name, demo_func = demos[int(choice) - 1]
            demo_func()
        else:
            print("❌ Invalid choice. Running all demos...")
            for name, demo_func in demos:
                try:
                    demo_func()
                except Exception as e:
                    print(f"\n❌ Error in {name}: {e}")
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
        return

    print("\n" + "=" * 70)
    print("DEMO COMPLETE!")
    print("=" * 70)
    print("\n📚 For more information, see:")
    print("   - docs/MICROSTEP_VALIDATION.md")
    print("   - src/Python/Tools/MicrostepValidator.py")
    print("\n")


if __name__ == "__main__":
    main()
