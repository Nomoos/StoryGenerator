#!/usr/bin/env python3
"""Verify Python environment has all required packages."""

import sys

def check_imports():
    """Test importing all critical packages."""
    packages = [
        ('openai', 'OpenAI API'),
        ('elevenlabs', 'ElevenLabs TTS'),
        ('yaml', 'PyYAML'),
        ('torch', 'PyTorch'),
        ('diffusers', 'Diffusers (SDXL)'),
        ('transformers', 'Transformers'),
        ('faster_whisper', 'Faster Whisper'),
        ('PIL', 'Pillow'),
        ('ffmpeg', 'FFmpeg Python'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
    ]
    
    print("🔍 Checking Python environment...\n")
    failed = []
    
    for package, name in packages:
        try:
            __import__(package)
            print(f"✅ {name:30} OK")
        except ImportError as e:
            print(f"❌ {name:30} FAILED: {e}")
            failed.append(name)
    
    print(f"\n{'='*60}")
    if not failed:
        print("✅ All packages installed successfully!")
        print("\n💡 Python environment is ready for StoryGenerator!")
        return 0
    else:
        print(f"❌ Failed to import {len(failed)} package(s):")
        for pkg in failed:
            print(f"   - {pkg}")
        print("\n💡 Install missing packages:")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(check_imports())
