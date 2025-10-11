#!/usr/bin/env python3
"""
Tests for vision guidance utilities.
Tests data models, utility functions, and basic GVision functionality.
"""

import os
import sys
import tempfile
from pathlib import Path
from PIL import Image

# Add Python directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "Python"))
# Add project root to path for config
sys.path.insert(0, str(Path(__file__).parent.parent))

from Models.VisionAnalysis import (
    QualityScore,
    ConsistencyScore,
    ImageCaption,
    VisionAnalysisResult,
    StoryboardValidation
)
from Tools.VisionUtils import (
    load_image,
    validate_image_dimensions,
    resize_image_for_vision_model,
    parse_quality_scores,
    parse_consistency_scores,
    validate_caption_alignment,
    calculate_image_quality_heuristics,
    check_gpu_available
)


def create_test_image(width: int = 512, height: int = 512) -> Image.Image:
    """Create a test image."""
    return Image.new('RGB', (width, height), color=(100, 150, 200))


def test_data_models():
    """Test vision analysis data models."""
    print("\n" + "="*60)
    print("Testing Data Models")
    print("="*60)
    
    # Test QualityScore
    print("\n1. Testing QualityScore...")
    quality = QualityScore(
        overall_quality=8.5,
        sharpness=8.0,
        clarity=8.5,
        composition=9.0,
        lighting=7.5,
        subject_clarity=8.0,
        artifacts_detected=False,
        reasoning="High quality image with good composition"
    )
    
    avg = quality.average_score()
    print(f"   Average score: {avg:.2f}")
    
    if 7.5 < avg < 9.0:
        print("   ✅ QualityScore working correctly")
    else:
        print("   ❌ QualityScore average calculation incorrect")
        return False
    
    # Test ConsistencyScore
    print("\n2. Testing ConsistencyScore...")
    consistency = ConsistencyScore(
        character_consistency=9.0,
        style_consistency=8.5,
        lighting_consistency=8.0,
        visual_continuity=9.0,
        inconsistencies=["Minor lighting shift"],
        reasoning="Good consistency overall"
    )
    
    avg = consistency.average_score()
    print(f"   Average score: {avg:.2f}")
    
    if 8.0 < avg < 9.5:
        print("   ✅ ConsistencyScore working correctly")
    else:
        print("   ❌ ConsistencyScore average calculation incorrect")
        return False
    
    # Test ImageCaption
    print("\n3. Testing ImageCaption...")
    caption = ImageCaption(
        caption="A beautiful landscape with mountains",
        confidence=0.95,
        model_used="phi-3.5-vision"
    )
    
    caption_dict = caption.to_dict()
    if "caption" in caption_dict and "confidence" in caption_dict:
        print("   ✅ ImageCaption working correctly")
    else:
        print("   ❌ ImageCaption to_dict failed")
        return False
    
    # Test VisionAnalysisResult
    print("\n4. Testing VisionAnalysisResult...")
    result = VisionAnalysisResult(image_path="/test/image.jpg")
    result.caption = caption
    result.quality_score = quality
    result.add_warning("Test warning")
    
    result_dict = result.to_dict()
    if result_dict["caption"] is not None and len(result.warnings) == 1:
        print("   ✅ VisionAnalysisResult working correctly")
    else:
        print("   ❌ VisionAnalysisResult failed")
        return False
    
    # Test StoryboardValidation
    print("\n5. Testing StoryboardValidation...")
    validation = StoryboardValidation(
        story_name="test_story",
        scene_count=3
    )
    
    for i in range(3):
        scene_result = VisionAnalysisResult(image_path=f"/test/scene_{i}.jpg")
        scene_result.quality_score = quality
        validation.add_scene_analysis(scene_result)
    
    if validation.scene_count == 3 and len(validation.scene_analyses) == 3:
        print(f"   Scenes: {validation.scene_count}")
        print(f"   Avg quality: {validation.overall_quality_avg:.2f}")
        print("   ✅ StoryboardValidation working correctly")
    else:
        print("   ❌ StoryboardValidation failed")
        return False
    
    print("\n✅ All data model tests passed!")
    return True


def test_vision_utils():
    """Test vision utility functions."""
    print("\n" + "="*60)
    print("Testing Vision Utils")
    print("="*60)
    
    # Test image creation and loading
    print("\n1. Testing image operations...")
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test image
        test_img = create_test_image(800, 600)
        test_path = os.path.join(tmpdir, "test.jpg")
        test_img.save(test_path)
        
        # Test load_image
        loaded = load_image(test_path)
        if loaded is not None and loaded.size == (800, 600):
            print("   ✅ Image loading works")
        else:
            print("   ❌ Image loading failed")
            return False
        
        # Test validate_image_dimensions
        is_valid, msg = validate_image_dimensions(loaded, min_width=512, min_height=512)
        if is_valid:
            print(f"   ✅ Image dimension validation works: {msg}")
        else:
            print(f"   ❌ Image dimension validation failed: {msg}")
            return False
        
        # Test resize_image_for_vision_model
        resized = resize_image_for_vision_model(loaded, max_size=512)
        if resized.size[0] <= 512 and resized.size[1] <= 512:
            print(f"   ✅ Image resizing works: {resized.size}")
        else:
            print(f"   ❌ Image resizing failed: {resized.size}")
            return False
    
    # Test parse_quality_scores
    print("\n2. Testing quality score parsing...")
    test_response = """
    Overall: 8.5/10
    Composition: 9.0/10
    Lighting: 7.5/10
    Subject: 8.0/10
    Artifacts: no
    Reasoning: High quality image with good composition and lighting.
    """
    
    parsed = parse_quality_scores(test_response)
    if (parsed["overall_quality"] == 8.5 and 
        parsed["composition"] == 9.0 and
        not parsed["artifacts_detected"]):
        print("   ✅ Quality score parsing works")
    else:
        print(f"   ❌ Quality score parsing failed: {parsed}")
        return False
    
    # Test parse_consistency_scores
    print("\n3. Testing consistency score parsing...")
    test_response = """
    Character: 9.0/10
    Style: 8.5/10
    Lighting: 8.0/10
    Continuity: 9.0/10
    Inconsistencies: Minor lighting shift, Slight color variation
    Reasoning: Good consistency with minor variations.
    """
    
    parsed = parse_consistency_scores(test_response)
    if (parsed["character_consistency"] == 9.0 and 
        len(parsed["inconsistencies"]) == 2):
        print("   ✅ Consistency score parsing works")
    else:
        print(f"   ❌ Consistency score parsing failed: {parsed}")
        return False
    
    # Test validate_caption_alignment
    print("\n4. Testing caption alignment validation...")
    caption = "A young girl walking down a dimly lit school hallway looking sad"
    keywords = ["girl", "hallway", "sad", "school"]
    
    is_valid, matched, missing = validate_caption_alignment(caption, keywords, min_keyword_matches=3)
    if is_valid and len(matched) >= 3:
        print(f"   Matched: {matched}")
        print("   ✅ Caption alignment validation works")
    else:
        print(f"   ❌ Caption alignment validation failed: {matched}, {missing}")
        return False
    
    # Test calculate_image_quality_heuristics
    print("\n5. Testing image quality heuristics...")
    test_img = create_test_image(512, 512)
    metrics = calculate_image_quality_heuristics(test_img)
    
    if "brightness" in metrics and "contrast" in metrics:
        print(f"   Brightness: {metrics['brightness']:.2f}")
        print(f"   Contrast: {metrics['contrast']:.2f}")
        print("   ✅ Image quality heuristics work")
    else:
        print("   ❌ Image quality heuristics failed")
        return False
    
    # Test check_gpu_available
    print("\n6. Testing GPU availability check...")
    gpu_available, device_name = check_gpu_available()
    print(f"   GPU Available: {gpu_available}")
    print(f"   Device: {device_name}")
    print("   ✅ GPU check works")
    
    print("\n✅ All vision utils tests passed!")
    return True


def test_gvision_init():
    """Test GVision initialization without loading models."""
    print("\n" + "="*60)
    print("Testing GVision Initialization")
    print("="*60)
    
    try:
        from Generators.GVision import GVision
        
        # Test initialization without loading model
        print("\n1. Testing GVision init (no model load)...")
        generator = GVision(model_name="phi-3.5-vision", load_model=False)
        
        if generator.model is None and generator.processor is None:
            print("   ✅ GVision initialized without loading model")
        else:
            print("   ❌ Model should not be loaded")
            return False
        
        # Test supported models
        print("\n2. Testing supported models list...")
        if len(GVision.SUPPORTED_MODELS) > 0:
            print(f"   Supported models: {list(GVision.SUPPORTED_MODELS.keys())}")
            print("   ✅ Supported models list available")
        else:
            print("   ❌ No supported models found")
            return False
        
        print("\n✅ GVision initialization tests passed!")
        return True
        
    except ImportError as e:
        print(f"   ⚠️  Cannot test GVision: {e}")
        print("   (This is expected if transformers is not installed)")
        return True  # Don't fail test if library not installed
    except Exception as e:
        print(f"   ❌ GVision initialization failed: {e}")
        return False


def test_vision_prompts():
    """Test vision prompts configuration."""
    print("\n" + "="*60)
    print("Testing Vision Prompts")
    print("="*60)
    
    try:
        from config.vision_prompts import PROMPTS, get_prompt
        
        print("\n1. Testing prompt availability...")
        required_prompts = ["quality", "consistency", "caption"]
        
        for prompt_type in required_prompts:
            if prompt_type in PROMPTS:
                print(f"   ✅ {prompt_type} prompt available")
            else:
                print(f"   ❌ {prompt_type} prompt missing")
                return False
        
        print("\n2. Testing get_prompt function...")
        quality_prompt = get_prompt("quality")
        if len(quality_prompt) > 0 and "quality" in quality_prompt.lower():
            print("   ✅ get_prompt works correctly")
        else:
            print("   ❌ get_prompt failed")
            return False
        
        print("\n3. Testing prompt formatting...")
        try:
            formatted = get_prompt("prompt_alignment", prompt="test prompt")
            if "test prompt" in formatted:
                print("   ✅ Prompt formatting works")
            else:
                print("   ❌ Prompt formatting failed")
                return False
        except Exception as e:
            print(f"   ❌ Prompt formatting error: {e}")
            return False
        
        print("\n✅ All vision prompts tests passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Vision prompts test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("VISION GUIDANCE - FUNCTIONALITY TESTS")
    print("="*60)
    
    results = []
    
    # Test data models
    results.append(("Data Models", test_data_models()))
    
    # Test vision utils
    results.append(("Vision Utils", test_vision_utils()))
    
    # Test vision prompts
    results.append(("Vision Prompts", test_vision_prompts()))
    
    # Test GVision initialization
    results.append(("GVision Init", test_gvision_init()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
