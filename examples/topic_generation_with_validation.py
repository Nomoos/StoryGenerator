#!/usr/bin/env python3
"""
Example: Topic Generation with Integrated Validation

This example demonstrates how to use the TopicGeneratorWithValidation
to generate topics for different audience segments with automatic
progress tracking, configuration logging, and validation.

Features demonstrated:
1. Single segment topic generation
2. Batch processing multiple segments
3. Validation and @copilot check integration
4. Artifact tracking and progress monitoring
"""

import sys
from pathlib import Path

# Add src/Python to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "Python"))

from Generators.GTopics import TopicGeneratorWithValidation


def example_1_single_segment():
    """Example 1: Generate topics for a single segment."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Single Segment Topic Generation")
    print("=" * 70)

    generator = TopicGeneratorWithValidation()

    # Sample ideas for women aged 18-23
    sample_ideas = [
        "A woman discovers her best friend has been keeping a life-changing secret",
        "Two friends make a pact that tests their loyalty to each other",
        "A mysterious letter arrives revealing a family secret from the past",
        "A chance encounter at a coffee shop leads to an unexpected friendship",
        "Someone must choose between career success and personal relationships",
        "A family reunion brings long-hidden tensions to the surface",
        "A long-lost relative shows up with surprising news",
        "A workplace rivalry turns into an unexpected partnership",
        "Someone's social media post goes viral for unexpected reasons",
        "A travel adventure leads to profound personal transformation",
        "A secret talent is discovered that changes everything",
        "Two people from different worlds find common ground",
        "A misunderstanding threatens to destroy a close friendship",
        "Someone takes a risk that could change their life forever",
        "A childhood dream resurfaces with new possibilities",
        "An unexpected opportunity forces a difficult decision",
        "A life-changing conversation happens in an unlikely place",
        "Someone discovers their true calling through adversity",
        "A chance to make amends comes at an unexpected time",
        "A journey of self-discovery leads to surprising revelations",
    ]

    print(f"\n📝 Generating topics from {len(sample_ideas)} ideas...")
    print(f"   Target: women/18-23")
    print(f"   Minimum topics: 8")

    result = generator.generate_topics_for_segment(
        gender="women", age="18-23", ideas_data=sample_ideas, min_topics=8, validate=True
    )

    if result["success"]:
        print(f"\n✅ Success!")
        print(f"   Topics generated: {len(result['topics'])}")
        print(f"   Topics file: {result['topics_file']}")
        print(f"   Artifacts created: {len(result['artifacts'])}")

        print(f"\n📊 Generated Topics:")
        for i, topic in enumerate(result["topics"], 1):
            print(f"   {i}. {topic['topicName']} (Viral: {topic['viralPotential']}/100)")
            print(f"      - {len(topic['ideaIds'])} ideas assigned")

        if "validation_report" in result:
            print(
                f"\n✅ Validation: {'VALID' if result['validation_report']['is_valid'] else 'INVALID'}"
            )
    else:
        print(f"\n❌ Failed to generate topics")


def example_2_batch_processing():
    """Example 2: Batch process multiple segments."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Batch Processing Multiple Segments")
    print("=" * 70)

    generator = TopicGeneratorWithValidation()

    # Define segments to process
    segments = [("women", "18-23"), ("women", "24-29"), ("men", "18-23"), ("men", "24-29")]

    print(f"\n🎯 Processing {len(segments)} segments...")

    # Create sample ideas directory structure for demo
    # In production, this would be your actual ideas directory
    import tempfile
    import os

    temp_dir = tempfile.mkdtemp()
    print(f"   Using temp directory: {temp_dir}")

    # Create sample ideas files for each segment
    for gender, age in segments:
        segment_dir = Path(temp_dir) / gender / age
        segment_dir.mkdir(parents=True, exist_ok=True)

        ideas_file = segment_dir / f"20251007_ideas.md"
        with open(ideas_file, "w") as f:
            f.write(f"# Sample Ideas for {gender}/{age}\n\n")
            f.write("- A life-changing discovery that changes everything\n")
            f.write("- An unexpected friendship forms in unlikely circumstances\n")
            f.write("- A secret is revealed that impacts everyone\n")
            f.write("- A difficult choice must be made\n")
            f.write("- A journey leads to self-discovery\n")
            f.write("- An opportunity arises at the perfect moment\n")
            f.write("- A challenge becomes a blessing in disguise\n")
            f.write("- A relationship is tested by circumstances\n")
            f.write("- A dream becomes reality through perseverance\n")
            f.write("- A mistake leads to an important lesson\n")

    # Run batch processing
    results = generator.batch_generate_topics(
        segments=segments, ideas_directory=temp_dir, min_topics=8
    )

    print(f"\n📊 Batch Processing Results:")
    for segment_key, result in results.items():
        if result.get("success"):
            print(f"   ✅ {segment_key}: {len(result['topics'])} topics generated")
        else:
            print(f"   ❌ {segment_key}: {result.get('error', 'Unknown error')}")

    # Cleanup temp directory
    import shutil

    shutil.rmtree(temp_dir)
    print(f"\n🧹 Cleaned up temporary directory")


def example_3_validation_details():
    """Example 3: Detailed validation inspection."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Detailed Validation Inspection")
    print("=" * 70)

    generator = TopicGeneratorWithValidation()

    sample_ideas = [
        "A life-changing secret is revealed",
        "An unexpected friendship changes everything",
        "A difficult choice must be made",
        "A journey of self-discovery begins",
        "An opportunity arises at the perfect time",
        "A challenge becomes a blessing",
        "A relationship is tested",
        "A dream becomes reality",
    ]

    print(f"\n📝 Generating topics with detailed validation...")

    result = generator.generate_topics_for_segment(
        gender="men", age="24-29", ideas_data=sample_ideas, min_topics=8, validate=True
    )

    if result["success"] and "validation_report" in result:
        report = result["validation_report"]

        print(f"\n📋 Validation Report:")
        print(f"   Step: {report['step_name']} (#{report['step_number']})")
        print(f"   Folder: {report['folder']}")
        print(f"   Timestamp: {report['timestamp']}")

        print(f"\n✅ Validation Checks:")
        for check, passed in report["checks"].items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check.replace('_', ' ').title()}: {passed}")

        print(f"\n📦 Artifacts ({len(report['artifacts'])}):")
        for artifact in report["artifacts"]:
            print(f"   - {artifact}")

        print(f"\n🎯 Overall Status: {'✅ VALID' if report['is_valid'] else '❌ INVALID'}")


def example_4_custom_config():
    """Example 4: Custom configuration logging."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Custom Configuration")
    print("=" * 70)

    from Tools.MicrostepValidator import MicrostepValidator
    from Generators.GTopics import TopicGeneratorWithValidation

    generator = TopicGeneratorWithValidation()

    # You can customize the configuration that gets logged
    custom_config = {
        "min_topics": 10,
        "clustering_method": "keyword-based",
        "generator": "TopicGenerator",
        "version": "1.0.0",
        "custom_parameters": {
            "min_ideas_per_topic": 3,
            "max_ideas_per_topic": 7,
            "keyword_threshold": 0.5,
        },
    }

    print(f"\n⚙️  Custom Configuration:")
    print(f"   Min Topics: {custom_config['min_topics']}")
    print(f"   Clustering: {custom_config['clustering_method']}")
    print(f"   Version: {custom_config['version']}")

    # The configuration will be automatically logged when you generate topics
    # You can also manually log configuration using the validator
    validator = MicrostepValidator()
    config_path = validator.log_config(
        step_number=3, config_subset=custom_config, gender="women", age="18-23"
    )

    print(f"\n✅ Configuration logged to: {config_path}")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("TOPIC GENERATION WITH VALIDATION - EXAMPLES")
    print("=" * 70)
    print("\nThese examples demonstrate the integration of MicrostepValidator")
    print("with the Topic Generator for comprehensive progress tracking.")

    # Run examples
    try:
        example_1_single_segment()
        example_2_batch_processing()
        example_3_validation_details()
        example_4_custom_config()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 70)
    print("EXAMPLES COMPLETE")
    print("=" * 70)
    print("\n📚 For more information:")
    print("   - Documentation: docs/MICROSTEP_VALIDATION.md")
    print("   - Topic Generator: src/Python/Generators/GTopics.py")
    print("   - Validator: src/Python/Tools/MicrostepValidator.py")
    print()


if __name__ == "__main__":
    main()
