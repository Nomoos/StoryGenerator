"""
Comprehensive tests for the enhancement features.
Run this to validate all enhancements are working correctly.
"""
import sys
import os

def test_imports():
    """Test that all modules can be imported."""
    print("=" * 60)
    print("TEST: Module Imports")
    print("=" * 60)
    
    try:
        from Tools.VideoEffects import VideoEffects
        from Models.StoryIdea import StoryIdea
        from Generators.GScript import ScriptGenerator
        from Generators.GVoice import VoiceMaker
        from Tools.Utils import convert_to_mp4, sanitize_filename
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_story_idea_enhancements():
    """Test StoryIdea with new enhancement fields."""
    print("\n" + "=" * 60)
    print("TEST: StoryIdea Enhancement Fields")
    print("=" * 60)
    
    from Models.StoryIdea import StoryIdea
    
    # Test with all new fields
    idea = StoryIdea(
        story_title="Test Story {name}",
        narrator_gender="female",
        language="es",
        personalization={"name": "Maria", "city": "Barcelona"},
        video_style="dramatic",
        voice_stability=0.6,
        voice_similarity_boost=0.8,
        voice_style_exaggeration=0.3
    )
    
    # Verify all fields
    assert idea.language == "es", "Language not set"
    assert idea.personalization == {"name": "Maria", "city": "Barcelona"}, "Personalization not set"
    assert idea.video_style == "dramatic", "Video style not set"
    assert idea.voice_stability == 0.6, "Voice stability not set"
    assert idea.voice_similarity_boost == 0.8, "Voice similarity boost not set"
    assert idea.voice_style_exaggeration == 0.3, "Voice style exaggeration not set"
    
    print("✅ All enhancement fields working correctly")
    return True


def test_personalization():
    """Test personalization replacement."""
    print("\n" + "=" * 60)
    print("TEST: Personalization")
    print("=" * 60)
    
    from Generators.GScript import ScriptGenerator
    
    gen = ScriptGenerator()
    
    # Test basic replacement
    text = "Hello {name}, welcome to {city}!"
    result = gen._apply_personalization(text, {"name": "Alice", "city": "Paris"})
    assert result == "Hello Alice, welcome to Paris!", f"Got: {result}"
    
    # Test multiple occurrences
    text = "{name} loves {name}'s home in {city}"
    result = gen._apply_personalization(text, {"name": "Bob", "city": "NYC"})
    assert result == "Bob loves Bob's home in NYC", f"Got: {result}"
    
    # Test no personalization
    text = "Hello world"
    result = gen._apply_personalization(text, {})
    assert result == "Hello world", f"Got: {result}"
    
    print("✅ Personalization replacement works correctly")
    return True


def test_multi_lingual():
    """Test multi-lingual support."""
    print("\n" + "=" * 60)
    print("TEST: Multi-lingual Support")
    print("=" * 60)
    
    from Generators.GScript import ScriptGenerator
    
    gen = ScriptGenerator()
    
    # Test all supported languages
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'ru': 'Russian'
    }
    
    for code, name in languages.items():
        result = gen._get_language_name(code)
        assert result == name, f"Language {code} mapped to {result}, expected {name}"
        print(f"  ✓ {code} → {name}")
    
    print("✅ All languages mapped correctly")
    return True


def test_video_effects():
    """Test VideoEffects class."""
    print("\n" + "=" * 60)
    print("TEST: VideoEffects Class")
    print("=" * 60)
    
    from Tools.VideoEffects import VideoEffects
    
    # Test pan parameters
    directions = ['center', 'right', 'left', 'up', 'down']
    for direction in directions:
        params = VideoEffects._get_pan_params(direction)
        assert 'start' in params, f"Missing 'start' in {direction}"
        assert 'end' in params, f"Missing 'end' in {direction}"
        print(f"  ✓ Pan direction '{direction}' has valid parameters")
    
    # Test method existence
    methods = [
        'apply_ken_burns_effect',
        'add_video_transition',
        'apply_style_filter',
        'add_background_music'
    ]
    
    for method in methods:
        assert hasattr(VideoEffects, method), f"Missing method: {method}"
        print(f"  ✓ Method '{method}' exists")
    
    print("✅ VideoEffects class working correctly")
    return True


def test_backward_compatibility():
    """Test that changes are backward compatible."""
    print("\n" + "=" * 60)
    print("TEST: Backward Compatibility")
    print("=" * 60)
    
    from Models.StoryIdea import StoryIdea
    from Tools.Utils import convert_to_mp4
    import inspect
    
    # Test StoryIdea can be created without new fields
    try:
        idea = StoryIdea(
            story_title="Old Style Story",
            narrator_gender="male"
        )
        # Check defaults
        assert idea.language == "en", "Default language not 'en'"
        assert idea.personalization == {}, "Default personalization not empty dict"
        assert idea.video_style == "cinematic", "Default video_style not 'cinematic'"
        print("  ✓ StoryIdea works with old signature")
    except Exception as e:
        print(f"  ❌ StoryIdea backward compatibility failed: {e}")
        return False
    
    # Test convert_to_mp4 signature
    sig = inspect.signature(convert_to_mp4)
    params = sig.parameters
    
    # Check new params have defaults
    assert params['use_ken_burns'].default == False
    assert params['video_style'].default == "cinematic"
    assert params['background_music'].default == None
    print("  ✓ convert_to_mp4 has backward compatible signature")
    
    print("✅ All changes are backward compatible")
    return True


def test_video_style_filters():
    """Test video style filter options."""
    print("\n" + "=" * 60)
    print("TEST: Video Style Filters")
    print("=" * 60)
    
    from Models.StoryIdea import StoryIdea
    
    styles = ["cinematic", "warm", "cold", "vintage", "dramatic", "none"]
    
    for style in styles:
        idea = StoryIdea(
            story_title="Test",
            narrator_gender="female",
            video_style=style
        )
        assert idea.video_style == style, f"Video style {style} not set correctly"
        print(f"  ✓ Style '{style}' works")
    
    print("✅ All video style filters work")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "🧪" * 30)
    print("RUNNING COMPREHENSIVE ENHANCEMENT TESTS")
    print("🧪" * 30 + "\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("StoryIdea Enhancements", test_story_idea_enhancements),
        ("Personalization", test_personalization),
        ("Multi-lingual Support", test_multi_lingual),
        ("VideoEffects Class", test_video_effects),
        ("Backward Compatibility", test_backward_compatibility),
        ("Video Style Filters", test_video_style_filters),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        return 0
    else:
        print("\n⚠️ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
