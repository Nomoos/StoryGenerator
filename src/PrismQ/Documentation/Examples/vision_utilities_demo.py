#!/usr/bin/env python3
"""
Simple demo of vision guidance utilities without requiring model download.
Demonstrates data models, parsing, and utility functions.
"""

import sys
from pathlib import Path

# Add Python directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "Python"))
# Add project root for config
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 60)
print("Vision Guidance Utilities Demo")
print("=" * 60)

# Demo 1: Data Models
print("\n1. Data Models Demo")
print("-" * 60)

from Models.VisionAnalysis import QualityScore, ConsistencyScore, ImageCaption

# Create quality score
quality = QualityScore(
    overall_quality=8.5,
    sharpness=8.0,
    clarity=8.5,
    composition=9.0,
    lighting=7.5,
    subject_clarity=8.0,
    artifacts_detected=False,
    reasoning="High quality image with excellent composition",
)

print(f"Quality Score: {quality.average_score():.1f}/10")
print(f"  - Composition: {quality.composition}/10")
print(f"  - Lighting: {quality.lighting}/10")
print(f"  - Reasoning: {quality.reasoning}")

# Create consistency score
consistency = ConsistencyScore(
    character_consistency=9.0,
    style_consistency=8.5,
    lighting_consistency=8.0,
    visual_continuity=9.0,
    inconsistencies=["Minor lighting variation"],
    reasoning="Excellent consistency with only minor variations",
)

print(f"\nConsistency Score: {consistency.average_score():.1f}/10")
print(f"  - Character: {consistency.character_consistency}/10")
print(f"  - Style: {consistency.style_consistency}/10")
print(f"  - Issues: {', '.join(consistency.inconsistencies)}")

# Demo 2: Response Parsing
print("\n2. Response Parsing Demo")
print("-" * 60)

from Tools.VisionUtils import parse_quality_scores, parse_consistency_scores

# Simulate vision model response
model_response = """
Overall: 8.5/10
Composition: 9.0/10
Lighting: 7.5/10
Subject: 8.0/10
Artifacts: no
Reasoning: High quality image with good composition and lighting.
"""

parsed = parse_quality_scores(model_response)
print("Parsed quality scores from model response:")
print(f"  - Overall: {parsed['overall_quality']}/10")
print(f"  - Composition: {parsed['composition']}/10")
print(f"  - Artifacts: {parsed['artifacts_detected']}")

# Demo 3: Caption Validation
print("\n3. Caption Validation Demo")
print("-" * 60)

from Tools.VisionUtils import validate_caption_alignment

caption = "A young girl walking down a dimly lit school hallway looking sad"
expected_keywords = ["girl", "hallway", "sad", "school", "walking"]

is_valid, matched, missing = validate_caption_alignment(
    caption, expected_keywords, min_keyword_matches=4
)

print(f"Caption: '{caption}'")
print(f"Expected keywords: {expected_keywords}")
print(f"Matched: {matched}")
print(f"Missing: {missing}")
print(f"Valid: {is_valid}")

# Demo 4: Vision Prompts
print("\n4. Vision Prompts Demo")
print("-" * 60)

from config.vision_prompts import get_prompt, PROMPTS

print(f"Available prompt types: {list(PROMPTS.keys())}")
print("\nSample quality prompt:")
quality_prompt = get_prompt("quality")
print(quality_prompt[:200] + "...")

# Demo 5: System Checks
print("\n5. System Checks Demo")
print("-" * 60)

from Tools.VisionUtils import check_gpu_available, estimate_vram_usage

gpu_available, device = check_gpu_available()
print(f"GPU Available: {gpu_available}")
print(f"Device: {device}")

print("\nVRAM estimates for different models:")
models = ["phi-3.5-vision", "llava-onevision", "llava-v1.5-7b"]
for model in models:
    vram = estimate_vram_usage(model)
    print(f"  - {model}: {vram}")

# Demo 6: GVision Info (without loading model)
print("\n6. GVision Generator Info")
print("-" * 60)

try:
    from Generators.GVision import GVision

    print("Supported models:")
    for name, model_id in GVision.SUPPORTED_MODELS.items():
        vram = estimate_vram_usage(name)
        print(f"  - {name}")
        print(f"    Model ID: {model_id}")
        print(f"    VRAM: {vram}")

    print("\n✅ GVision generator available")
    print("Note: transformers library required for actual inference")

except ImportError as e:
    print(f"⚠️  GVision not fully available: {e}")
    print("This is expected if transformers is not installed")

print("\n" + "=" * 60)
print("Demo Complete!")
print("=" * 60)
print("\nFor full examples with model inference, see:")
print("  - examples/vision_guidance_example.py")
print("  - docs/VISION_GUIDANCE.md")
print("  - tests/test_vision.py")
print()
