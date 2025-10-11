#!/usr/bin/env python3
"""
Test script for MicrostepValidator.

Tests all core functionality of the microstep validation system.
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil
import json

# Add src/Python to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "Python"))

from Tools.MicrostepValidator import (
    MicrostepValidator,
    create_microstep_artifact,
    log_microstep_config,
    update_microstep_progress,
    copilot_check_microstep
)


def test_initialization():
    """Test MicrostepValidator initialization."""
    print("\n" + "="*60)
    print("TEST 1: Initialization")
    print("="*60)
    
    try:
        validator = MicrostepValidator()
        assert validator is not None
        assert validator.base_path is not None
        assert validator.config_path is not None
        print("✅ PASSED: Validator initialized successfully")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_list_microsteps():
    """Test listing all microsteps."""
    print("\n" + "="*60)
    print("TEST 2: List Microsteps")
    print("="*60)
    
    try:
        validator = MicrostepValidator()
        result = validator.list_microsteps()
        assert result is not None
        assert "Step 1" in result or "1." in result
        print("✅ PASSED: Listed all microsteps")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_get_microstep_folder():
    """Test getting microstep folder paths."""
    print("\n" + "="*60)
    print("TEST 3: Get Microstep Folder")
    print("="*60)
    
    try:
        validator = MicrostepValidator()
        
        # Test without gender/age
        folder = validator.get_microstep_folder(2)
        assert folder is not None
        assert "ideas" in str(folder)
        print(f"   ✓ Folder without demographics: {folder}")
        
        # Test with gender/age
        folder = validator.get_microstep_folder(2, "women", "18-23")
        assert folder is not None
        assert "ideas" in str(folder)
        assert "women" in str(folder)
        assert "18-23" in str(folder)
        print(f"   ✓ Folder with demographics: {folder}")
        
        print("✅ PASSED: Get microstep folder works")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_create_artifact():
    """Test creating artifacts."""
    print("\n" + "="*60)
    print("TEST 4: Create Artifact")
    print("="*60)
    
    try:
        validator = MicrostepValidator()
        step = 2
        gender = "women"
        age = "18-23"
        
        # Test JSON artifact
        json_content = {"id": "test_001", "title": "Test Idea"}
        json_path = validator.create_artifact(
            step, "test_idea.json", json_content, gender, age
        )
        assert json_path.exists()
        print(f"   ✓ Created JSON artifact: {json_path}")
        
        # Test text artifact
        text_content = "This is a test text file."
        text_path = validator.create_artifact(
            step, "test_text.txt", text_content, gender, age
        )
        assert text_path.exists()
        print(f"   ✓ Created text artifact: {text_path}")
        
        # Verify JSON content
        with open(json_path, 'r') as f:
            loaded = json.load(f)
            assert loaded["id"] == "test_001"
        print(f"   ✓ Verified JSON content")
        
        # Verify text content
        with open(text_path, 'r') as f:
            loaded_text = f.read()
            assert loaded_text == text_content
        print(f"   ✓ Verified text content")
        
        print("✅ PASSED: Create artifact works")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_log_config():
    """Test logging configuration."""
    print("\n" + "="*60)
    print("TEST 5: Log Configuration")
    print("="*60)
    
    try:
        validator = MicrostepValidator()
        step = 2
        gender = "women"
        age = "18-23"
        
        # Test auto-extract config
        config_path = validator.log_config(step, gender=gender, age=age)
        assert config_path.exists()
        print(f"   ✓ Created config log: {config_path}")
        
        # Test custom config
        custom_config = {"test_key": "test_value"}
        custom_path = validator.log_config(
            step, config_subset=custom_config, gender=gender, age=age
        )
        assert custom_path.exists()
        print(f"   ✓ Created custom config log: {custom_path}")
        
        print("✅ PASSED: Log configuration works")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_update_progress():
    """Test updating progress."""
    print("\n" + "="*60)
    print("TEST 6: Update Progress")
    print("="*60)
    
    try:
        validator = MicrostepValidator()
        step = 2
        gender = "women"
        age = "18-23"
        
        # Test started status
        progress_path = validator.update_progress(
            step, "started", "Test started", gender, age
        )
        assert progress_path.exists()
        print(f"   ✓ Created progress file: {progress_path}")
        
        # Test with artifacts
        progress_path = validator.update_progress(
            step, "completed", "Test completed", gender, age,
            artifacts=["test_file1.json", "test_file2.json"]
        )
        assert progress_path.exists()
        print(f"   ✓ Updated progress with artifacts")
        
        # Verify content
        with open(progress_path, 'r') as f:
            content = f.read()
            assert "started" in content.lower()
            assert "completed" in content.lower()
            assert "test_file1.json" in content
        print(f"   ✓ Verified progress content")
        
        print("✅ PASSED: Update progress works")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_validate_step():
    """Test validating a step."""
    print("\n" + "="*60)
    print("TEST 7: Validate Step")
    print("="*60)
    
    try:
        validator = MicrostepValidator()
        step = 2
        gender = "women"
        age = "18-23"
        
        # Create a complete setup
        validator.create_artifact(step, "test.json", {"test": "data"}, gender, age)
        validator.log_config(step, gender=gender, age=age)
        validator.update_progress(step, "completed", "Test", gender, age)
        
        # Validate
        report = validator.validate_step(step, gender, age)
        
        assert report is not None
        assert "step_number" in report
        assert report["step_number"] == step
        assert "checks" in report
        assert report["checks"]["folder_exists"] == True
        assert report["checks"]["has_artifacts"] == True
        assert report["checks"]["has_progress"] == True
        assert report["checks"]["has_config"] == True
        assert report["is_valid"] == True
        
        print(f"   ✓ Validation report generated")
        print(f"   ✓ All checks passed")
        print(f"   ✓ Overall status: {'VALID' if report['is_valid'] else 'INVALID'}")
        
        print("✅ PASSED: Validate step works")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_copilot_check():
    """Test @copilot check functionality."""
    print("\n" + "="*60)
    print("TEST 8: @copilot Check")
    print("="*60)
    
    try:
        validator = MicrostepValidator()
        step = 2
        gender = "women"
        age = "18-23"
        
        # Ensure step is set up
        validator.create_artifact(step, "test.json", {"test": "data"}, gender, age)
        validator.log_config(step, gender=gender, age=age)
        validator.update_progress(step, "completed", "Test", gender, age)
        
        # Perform copilot check
        result = validator.copilot_check(step, gender, age)
        
        assert result is not None
        assert "@copilot CHECK" in result
        assert "Step 2" in result
        assert "ideas" in result
        
        print(f"   ✓ Copilot check executed")
        print(f"   ✓ Report generated")
        
        print("✅ PASSED: @copilot check works")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_convenience_functions():
    """Test convenience functions."""
    print("\n" + "="*60)
    print("TEST 9: Convenience Functions")
    print("="*60)
    
    try:
        step = 3
        gender = "men"
        age = "24-29"
        
        # Test create_microstep_artifact
        artifact_path = create_microstep_artifact(
            step, "test.json", {"test": "data"}, gender, age
        )
        assert artifact_path.exists()
        print(f"   ✓ create_microstep_artifact works")
        
        # Test log_microstep_config
        config_path = log_microstep_config(step, gender=gender, age=age)
        assert config_path.exists()
        print(f"   ✓ log_microstep_config works")
        
        # Test update_microstep_progress
        progress_path = update_microstep_progress(
            step, "completed", "Test", gender, age
        )
        assert progress_path.exists()
        print(f"   ✓ update_microstep_progress works")
        
        # Test copilot_check_microstep
        result = copilot_check_microstep(step, gender, age)
        assert result is not None
        print(f"   ✓ copilot_check_microstep works")
        
        print("✅ PASSED: Convenience functions work")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_invalid_step():
    """Test handling of invalid step numbers."""
    print("\n" + "="*60)
    print("TEST 10: Invalid Step Handling")
    print("="*60)
    
    try:
        validator = MicrostepValidator()
        
        # Test invalid step number
        try:
            validator.get_microstep_folder(99)
            print(f"   ❌ Should have raised ValueError")
            return False
        except ValueError as e:
            print(f"   ✓ Correctly raised ValueError for invalid step")
        
        try:
            validator.get_microstep_folder(0)
            print(f"   ❌ Should have raised ValueError")
            return False
        except ValueError as e:
            print(f"   ✓ Correctly raised ValueError for step 0")
        
        print("✅ PASSED: Invalid step handling works")
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("MICROSTEP VALIDATOR TEST SUITE")
    print("="*70)
    
    tests = [
        ("Initialization", test_initialization),
        ("List Microsteps", test_list_microsteps),
        ("Get Microstep Folder", test_get_microstep_folder),
        ("Create Artifact", test_create_artifact),
        ("Log Configuration", test_log_config),
        ("Update Progress", test_update_progress),
        ("Validate Step", test_validate_step),
        ("@copilot Check", test_copilot_check),
        ("Convenience Functions", test_convenience_functions),
        ("Invalid Step Handling", test_invalid_step),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ EXCEPTION in {name}: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")
    
    print("\n" + "="*70)
    print(f"Total: {len(results)} tests")
    print(f"Passed: {passed} ({passed/len(results)*100:.1f}%)")
    print(f"Failed: {failed} ({failed/len(results)*100:.1f}%)")
    print("="*70)
    
    # Return exit code
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
