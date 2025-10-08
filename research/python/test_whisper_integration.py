#!/usr/bin/env python3
"""
Simple test script to verify whisper_subprocess.py is working correctly.
This tests the Python component without requiring C# compilation.
"""

import sys
import json
import tempfile
import subprocess
from pathlib import Path

# Test script path
SCRIPT_DIR = Path(__file__).parent
SUBPROCESS_SCRIPT = SCRIPT_DIR / "whisper_subprocess.py"


def create_test_audio():
    """
    Create a simple test audio file (1 second of silence).
    Returns path to temporary audio file.
    """
    import wave
    import array
    
    # Create 1 second of silence at 16kHz
    sample_rate = 16000
    duration = 1  # seconds
    samples = array.array('h', [0] * (sample_rate * duration))
    
    # Create temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    with wave.open(temp_path, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())
    
    return temp_path


def test_python_import():
    """Test 1: Check if faster-whisper can be imported."""
    print("Test 1: Checking faster-whisper installation...")
    try:
        import faster_whisper
        print("✓ faster-whisper is installed")
        print(f"  Version: {faster_whisper.__version__ if hasattr(faster_whisper, '__version__') else 'unknown'}")
        return True
    except ImportError as e:
        print("✗ faster-whisper is not installed")
        print(f"  Error: {e}")
        print("\nTo install: pip install faster-whisper")
        return False


def test_script_exists():
    """Test 2: Check if whisper_subprocess.py exists."""
    print("\nTest 2: Checking if whisper_subprocess.py exists...")
    if SUBPROCESS_SCRIPT.exists():
        print(f"✓ Script found at: {SUBPROCESS_SCRIPT}")
        return True
    else:
        print(f"✗ Script not found at: {SUBPROCESS_SCRIPT}")
        return False


def test_script_help():
    """Test 3: Check if script can display help."""
    print("\nTest 3: Testing script help command...")
    try:
        result = subprocess.run(
            ["python3", str(SUBPROCESS_SCRIPT), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ Script help command works")
            return True
        else:
            print(f"✗ Script help command failed with code {result.returncode}")
            print(f"  stderr: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error running script: {e}")
        return False


def test_transcription_dry_run():
    """Test 4: Test transcription with a simple audio file."""
    print("\nTest 4: Testing transcription (this may take a minute)...")
    
    # Create test audio
    print("  Creating test audio file...")
    try:
        audio_path = create_test_audio()
        print(f"  Test audio created: {audio_path}")
    except Exception as e:
        print(f"✗ Failed to create test audio: {e}")
        return False
    
    try:
        # Run transcription with tiny model for speed
        print("  Running transcription with tiny model...")
        result = subprocess.run(
            [
                "python3", str(SUBPROCESS_SCRIPT),
                "transcribe",
                "--audio-path", audio_path,
                "--model-size", "tiny",
                "--device", "cpu",
                "--no-word-timestamps"
            ],
            capture_output=True,
            text=True,
            timeout=120  # 2 minutes timeout
        )
        
        # Clean up test file
        Path(audio_path).unlink()
        
        if result.returncode == 0:
            # Parse JSON response
            try:
                response = json.loads(result.stdout)
                if response.get("success"):
                    print("✓ Transcription successful")
                    print(f"  Language: {response.get('language', 'unknown')}")
                    print(f"  Confidence: {response.get('languageProbability', 0):.2%}")
                    return True
                else:
                    print(f"✗ Transcription failed: {response.get('error', 'unknown error')}")
                    return False
            except json.JSONDecodeError as e:
                print(f"✗ Failed to parse JSON response: {e}")
                print(f"  stdout: {result.stdout}")
                return False
        else:
            print(f"✗ Script failed with exit code {result.returncode}")
            print(f"  stderr: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Transcription timed out after 2 minutes")
        Path(audio_path).unlink()
        return False
    except Exception as e:
        print(f"✗ Error during transcription: {e}")
        if Path(audio_path).exists():
            Path(audio_path).unlink()
        return False


def test_language_detection():
    """Test 5: Test language detection."""
    print("\nTest 5: Testing language detection...")
    
    # Create test audio
    try:
        audio_path = create_test_audio()
    except Exception as e:
        print(f"✗ Failed to create test audio: {e}")
        return False
    
    try:
        # Run language detection with tiny model
        result = subprocess.run(
            [
                "python3", str(SUBPROCESS_SCRIPT),
                "detect_language",
                "--audio-path", audio_path,
                "--model-size", "tiny"
            ],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Clean up test file
        Path(audio_path).unlink()
        
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                if response.get("success"):
                    print("✓ Language detection successful")
                    print(f"  Language: {response.get('language', 'unknown')}")
                    print(f"  Confidence: {response.get('confidence', 0):.2%}")
                    return True
                else:
                    print(f"✗ Language detection failed: {response.get('error', 'unknown error')}")
                    return False
            except json.JSONDecodeError as e:
                print(f"✗ Failed to parse JSON response: {e}")
                return False
        else:
            print(f"✗ Script failed with exit code {result.returncode}")
            print(f"  stderr: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Language detection timed out")
        Path(audio_path).unlink()
        return False
    except Exception as e:
        print(f"✗ Error during language detection: {e}")
        if Path(audio_path).exists():
            Path(audio_path).unlink()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("ASR Module Python Component Tests")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Import faster-whisper", test_python_import()))
    results.append(("Script exists", test_script_exists()))
    results.append(("Script help", test_script_help()))
    
    # Only run transcription tests if basic tests pass
    if all(r[1] for r in results):
        results.append(("Transcription", test_transcription_dry_run()))
        results.append(("Language detection", test_language_detection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n✓ All tests passed! ASR module is ready to use.")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
