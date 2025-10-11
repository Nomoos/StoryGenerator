#!/usr/bin/env python3
"""
Example: Scene Planning - Beat Sheet and Draft Subtitle Generation

This example demonstrates how to use the scene planning module to generate
beat sheets (shot lists) and draft subtitles from a script.
"""

import sys
import os
from pathlib import Path

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core"))

from scene_planning import ScenePlanner


def example_basic_usage():
    """Basic usage example."""
    print("=" * 70)
    print("Example 1: Basic Scene Planning")
    print("=" * 70)

    # Sample script
    script = """In a world where books are banned and libraries are just distant memories, 
one woman refuses to let knowledge die. She discovers a hidden underground library 
beneath the ruins of the old city. Every night, she risks her life to share stories 
with those who dare to listen. But the authorities are closing in on her secret. 
Will she escape with the forbidden knowledge, or will the last library burn forever?"""

    # Create scene planner
    planner = ScenePlanner(output_root="./example_output")

    # Generate beat sheet
    print("\n1. Generating beat sheet...")
    beat_sheet = planner.generate_beat_sheet(
        script_text=script, title_id="forbidden_library_001", total_duration=30.0  # 30 seconds
    )

    print(f"   ✅ Generated {beat_sheet.total_shots} shots")
    print(f"   Total duration: {beat_sheet.total_duration}s")

    # Display shots
    print("\n   Shots:")
    for shot in beat_sheet.shots:
        print(
            f"   - Shot {shot.shot_number}: {shot.start_time:.1f}s - {shot.end_time:.1f}s ({shot.duration:.1f}s)"
        )
        print(f"     Description: {shot.scene_description[:60]}...")

    # Generate draft subtitles
    print("\n2. Generating draft subtitles...")
    subtitles = planner.generate_draft_subtitles(script_text=script, total_duration=30.0)

    print(f"   ✅ Generated {len(subtitles)} subtitle entries")

    # Display first few subtitles
    print("\n   First 3 subtitles:")
    for sub in subtitles[:3]:
        print(f"   [{sub.index}] {sub.start_time:.2f}s - {sub.end_time:.2f}s")
        print(f"       {sub.text}")

    print(f"\n   ... and {len(subtitles) - 3} more subtitle entries")


def example_complete_scene_plan():
    """Complete scene plan generation example."""
    print("\n" + "=" * 70)
    print("Example 2: Complete Scene Plan (Beat Sheet + Subtitles)")
    print("=" * 70)

    script = """The year is 2157. Humanity has colonized Mars, but a mysterious signal 
from deep space changes everything. Dr. Sarah Chen, a linguist aboard the research 
station Galileo, decodes the message. It's a warning. An ancient alien civilization 
left clues scattered across the solar system. Now, Sarah must race against time to 
find these artifacts before a rogue faction uses them to unleash an unstoppable force. 
The fate of two worlds hangs in the balance."""

    # Create scene planner with custom output directory
    planner = ScenePlanner(output_root="./example_output")

    print("\n1. Generating complete scene plan...")
    paths = planner.generate_scene_plan(
        script_text=script,
        title_id="space_warning_042",
        gender="women",
        age="25-34",
        total_duration=45.0,  # 45 seconds
    )

    print(f"   ✅ Beat sheet saved to: {paths['beat_sheet']}")
    print(f"   ✅ Subtitles saved to: {paths['subtitles']}")

    # Read and display beat sheet
    print("\n2. Beat Sheet Contents:")
    import json

    with open(paths["beat_sheet"], "r") as f:
        beat_data = json.load(f)
        print(f"   Title ID: {beat_data['titleId']}")
        print(f"   Total Duration: {beat_data['totalDuration']}s")
        print(f"   Total Shots: {beat_data['totalShots']}")

    # Read and display subtitles
    print("\n3. Draft Subtitles (SRT format):")
    with open(paths["subtitles"], "r") as f:
        srt_content = f.read()
        # Show first subtitle block
        first_block = "\n".join(srt_content.split("\n\n")[0].split("\n"))
        print(f"   {first_block}")
        print("   ...")


def example_json_export():
    """Example of working with JSON output."""
    print("\n" + "=" * 70)
    print("Example 3: JSON Export and Processing")
    print("=" * 70)

    script = """Ancient wisdom meets modern technology. In the heart of Tokyo, 
a quantum computer achieves consciousness. Its first words? A haiku. Scientists 
scramble to understand as the AI begins composing poetry that moves hearts and 
minds. Is this true consciousness, or an elaborate simulation?"""

    planner = ScenePlanner(output_root="./example_output")

    # Generate beat sheet
    beat_sheet = planner.generate_beat_sheet(
        script_text=script, title_id="ai_haiku_007", total_duration=25.0
    )

    # Convert to JSON
    print("\n1. Beat Sheet as JSON:")
    json_output = beat_sheet.to_json(indent=2)
    print(json_output[:400] + "...")

    # Access as dictionary
    print("\n2. Processing beat sheet data:")
    beat_dict = beat_sheet.to_dict()

    # Calculate statistics
    avg_shot_duration = sum(s["duration"] for s in beat_dict["shots"]) / len(beat_dict["shots"])
    print(f"   Average shot duration: {avg_shot_duration:.2f}s")

    # Find longest shot
    longest_shot = max(beat_dict["shots"], key=lambda s: s["duration"])
    print(f"   Longest shot: #{longest_shot['shotNumber']} ({longest_shot['duration']:.2f}s)")


def example_custom_parameters():
    """Example with custom parameters."""
    print("\n" + "=" * 70)
    print("Example 4: Custom Parameters")
    print("=" * 70)

    script = """Breaking news: Scientists have discovered a way to reverse aging at 
the cellular level. But there's a catch - the treatment works only once. Who deserves 
to be young again? The debate divides nations as people face an impossible choice."""

    planner = ScenePlanner(output_root="./example_output")

    # Custom shots per minute
    print("\n1. High shot frequency (8 shots/minute):")
    beat_sheet_fast = planner.generate_beat_sheet(
        script_text=script,
        title_id="aging_cure_fast",
        total_duration=20.0,
        shots_per_minute=8.0,  # More cuts
    )
    print(f"   Generated {beat_sheet_fast.total_shots} shots")

    print("\n2. Low shot frequency (3 shots/minute):")
    beat_sheet_slow = planner.generate_beat_sheet(
        script_text=script,
        title_id="aging_cure_slow",
        total_duration=20.0,
        shots_per_minute=3.0,  # Fewer, longer shots
    )
    print(f"   Generated {beat_sheet_slow.total_shots} shots")

    # Custom subtitle character limit
    print("\n3. Custom subtitle length (60 chars):")
    subtitles_long = planner.generate_draft_subtitles(
        script_text=script, total_duration=20.0, max_chars=60  # Longer subtitles
    )
    print(f"   Generated {len(subtitles_long)} subtitle entries")
    print(f"   Average chars: {sum(len(s.text) for s in subtitles_long) / len(subtitles_long):.1f}")


def main():
    """Run all examples."""
    print("\n" + "█" * 70)
    print("Scene Planning Module - Usage Examples")
    print("█" * 70)

    try:
        example_basic_usage()
        example_complete_scene_plan()
        example_json_export()
        example_custom_parameters()

        print("\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)
        print("\nOutput files created in: ./example_output/")
        print("  - scenes/json/")
        print("  - subtitles/srt/")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
