# Setup: Python Environment

**ID:** `00-setup-03-python-env`  
**Priority:** P0  
**Effort:** 1-2 hours  
**Status:** Not Started

## Overview

Set up a Python virtual environment with all required dependencies for the StoryGenerator pipeline. This includes packages for AI/ML models (Whisper, SDXL, LTX Video), data processing, and API integrations.

## Dependencies

**Requires:**
- `00-setup-01`: Repository folder structure must exist
- `00-setup-02`: Config files must be defined

**Blocks:**
- All Phase 2 Python research prototypes
- All Phase 3 Python-based content generation tasks

## Acceptance Criteria

- [ ] Python 3.10+ virtual environment created
- [ ] All dependencies from `requirements.txt` installed successfully
- [ ] Virtual environment can be activated
- [ ] Test script imports all major packages without errors
- [ ] Environment activation documented in README

## Task Details

### Implementation

#### 1. Create Virtual Environment

```bash
# From project root
cd /home/runner/work/StoryGenerator/StoryGenerator

# Create virtual environment
python3 -m venv venv

# Activate environment (Linux/Mac)
source venv/bin/activate

# Activate environment (Windows)
# venv\Scripts\activate
```

#### 2. Install Dependencies

The project already has a `requirements.txt` at the root with the following categories of dependencies:

**Core Dependencies:**
- `openai` - OpenAI API client
- `elevenlabs` - ElevenLabs TTS API
- `PyYAML` - Configuration file parsing
- `requests` - HTTP client

**AI/ML Models:**
- `torch>=2.0.0` - PyTorch for deep learning
- `torchvision>=0.15.0` - Vision models
- `diffusers>=0.25.0` - Stable Diffusion/SDXL
- `transformers>=4.35.0` - Hugging Face transformers
- `accelerate>=0.25.0` - Model acceleration
- `faster-whisper>=0.10.0` - Speech recognition
- `whisperx>=3.0.0` - Enhanced Whisper

**Media Processing:**
- `ffmpeg-python` - Video processing
- `moviepy` - Video editing
- `pydub` - Audio manipulation
- `pyloudnorm` - Audio normalization
- `Pillow` - Image processing

**Data & Analytics:**
- `pandas` - Data analysis
- `numpy` - Numerical computing
- `pytrends` - Google Trends API
- `google-search-results` - SerpAPI client

```bash
# Install all dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Verify Installation

Create a verification script `scripts/verify_python_env.py`:

```python
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
        return 0
    else:
        print(f"❌ Failed to import {len(failed)} package(s):")
        for pkg in failed:
            print(f"   - {pkg}")
        return 1

if __name__ == "__main__":
    sys.exit(check_imports())
```

### Testing

```bash
# Activate virtual environment
source venv/bin/activate

# Run verification script
python scripts/verify_python_env.py

# Test Python version
python --version  # Should be 3.10+

# Test pip packages
pip list | grep -E "(torch|transformers|diffusers|whisper)"

# Deactivate when done
deactivate
```

## Output Files

- `venv/` - Python virtual environment directory (add to .gitignore)
- `scripts/verify_python_env.py` - Environment verification script
- `docs/PYTHON_SETUP.md` - Setup documentation (optional)

## Related Files

- `/requirements.txt` - Package dependencies
- `/examples/*.py` - Example scripts that use the environment
- `/scripts/setup_folders.py` - Folder setup script
- `/.gitignore` - Should exclude `venv/`

## Notes

- **Python Version**: Requires Python 3.10+ for best compatibility with AI/ML libraries
- **GPU Support**: If using CUDA/GPU, ensure PyTorch is installed with CUDA support:
  ```bash
  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
  ```
- **Memory**: Some models (SDXL, LTX Video) require significant RAM/VRAM
- **Virtual Environment**: Always use a virtual environment to avoid system package conflicts
- **Environment Variables**: API keys should be set via `.env` file or environment variables, not hardcoded

## Next Steps

After completion:
- Proceed to `00-setup-04-csharp-projects` for C# environment
- Begin Phase 2 research tasks:
  - `01-research-01-ollama-client` (Python)
  - `01-research-02-whisper-client` (Python)
  - `01-research-03-ffmpeg-client` (Python)
  - `01-research-04-sdxl-client` (Python)
  - `01-research-05-ltx-client` (Python)
