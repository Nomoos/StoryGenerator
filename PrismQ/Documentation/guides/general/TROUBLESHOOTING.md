# Troubleshooting Guide

Common issues and solutions for the StoryGenerator pipeline.

## Table of Contents

- [Installation Issues](#installation-issues)
- [API Key Issues](#api-key-issues)
- [GPU and CUDA Issues](#gpu-and-cuda-issues)
- [Model Loading Issues](#model-loading-issues)
- [Audio Generation Issues](#audio-generation-issues)
- [Subtitle Generation Issues](#subtitle-generation-issues)
- [Memory Issues](#memory-issues)
- [Pipeline Errors](#pipeline-errors)

---

## Installation Issues

### Issue: `pip install` fails with dependency conflicts

**Symptoms**:
```
ERROR: pip's dependency resolver does not currently take into account all the packages...
```

**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Install in order
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

### Issue: WhisperX installation fails

**Symptoms**:
```
ERROR: Could not build wheels for whisperx
```

**Solution**:
```bash
# Install PyTorch first
pip install torch torchvision torchaudio

# Install system dependencies (Ubuntu)
sudo apt install ffmpeg

# Then install WhisperX
pip install whisperx
```

---

## API Key Issues

### Issue: "OpenAI API key not found"

**Symptoms**:
```
openai.error.AuthenticationError: No API key provided
```

**Solution**:

1. Check `.env` file exists:
   ```bash
   ls -la .env
   ```

2. Verify `.env` format (no quotes):
   ```env
   OPENAI_API_KEY=sk-your-key-here
   ```

3. Restart Python session/IDE after creating `.env`

### Issue: "ElevenLabs authentication failed"

**Symptoms**:
```
elevenlabs.error.UnauthenticatedError: Invalid API key
```

**Solution**:

1. Verify API key in `.env`:
   ```env
   ELEVENLABS_API_KEY=sk-your-key-here
   ```

2. Check key is valid at [ElevenLabs Dashboard](https://elevenlabs.io/)

3. Ensure no extra spaces or quotes around key

### Issue: API keys in code instead of environment

**Symptoms**:
Hardcoded keys visible in `Generators/GScript.py`, etc.

**Solution**:

Replace hardcoded keys with environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
```

---

## GPU and CUDA Issues

### Issue: "CUDA not available" when GPU is present

**Symptoms**:
```python
>>> import torch
>>> torch.cuda.is_available()
False
```

**Solution**:

1. Check NVIDIA driver:
   ```bash
   nvidia-smi
   ```

2. Check CUDA version:
   ```bash
   nvcc --version
   ```

3. Reinstall PyTorch with correct CUDA version:
   ```bash
   # For CUDA 11.8
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   
   # For CUDA 12.1
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

4. Verify installation:
   ```python
   import torch
   print(torch.cuda.is_available())
   print(torch.cuda.get_device_name(0))
   ```

### Issue: "CUDA out of memory"

**Symptoms**:
```
RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB
```

**Solution**:

1. **Close other GPU applications**:
   ```bash
   nvidia-smi  # Check what's using GPU
   ```

2. **Use smaller models**:
   - WhisperX: Use "medium" instead of "large-v2"
   - SDXL: Enable model offloading

3. **Enable model offloading**:
   ```python
   pipe.enable_model_cpu_offload()
   ```

4. **Reduce batch size**:
   ```python
   # In generation code
   batch_size = 1  # or smaller
   ```

5. **Clear GPU cache**:
   ```python
   import torch
   torch.cuda.empty_cache()
   ```

---

## Model Loading Issues

### Issue: Models download repeatedly

**Symptoms**:
Models download every time script runs

**Solution**:

Set HuggingFace cache directory:
```bash
export HF_HOME=/path/to/cache
# Or in .env file
HF_HOME=/path/to/cache
```

### Issue: "Model not found" error

**Symptoms**:
```
OSError: We couldn't connect to 'https://huggingface.co'
```

**Solution**:

1. Check internet connection
2. Try manual download:
   ```python
   from huggingface_hub import snapshot_download
   snapshot_download("model-name", cache_dir="./models")
   ```

3. Use local model path:
   ```python
   model = WhisperModel("./models/model-name")
   ```

---

## Audio Generation Issues

### Issue: Voiceover generation fails

**Symptoms**:
```
Error generating voiceover: Connection timeout
```

**Solution**:

1. Check ElevenLabs API status
2. Verify API key quota
3. Check internet connection
4. Retry with timeout:
   ```python
   import time
   max_retries = 3
   for attempt in range(max_retries):
       try:
           audio = client.generate(...)
           break
       except Exception as e:
           if attempt < max_retries - 1:
               time.sleep(5)
           else:
               raise
   ```

### Issue: Audio normalization fails

**Symptoms**:
```
Error normalizing audio: Could not read file
```

**Solution**:

1. Verify FFmpeg is installed:
   ```bash
   ffmpeg -version
   ```

2. Check audio file exists and is valid:
   ```bash
   ffprobe voiceover.mp3
   ```

3. Install pydub dependencies:
   ```bash
   pip install pydub
   ```

---

## Subtitle Generation Issues

### Issue: Word alignment is inaccurate

**Symptoms**:
Subtitles don't match audio timing

**Solution**:

1. **Use better audio quality**:
   - Ensure clear narration
   - Remove background noise
   - Use normalized audio

2. **Adjust alignment parameters**:
   ```python
   title_gen = TitleGenerator(model_size="large-v2")
   # Try with different model sizes
   ```

3. **Check script matches audio**:
   - Ensure Revised.txt matches actual voiceover
   - Re-generate if script was modified after voiceover

### Issue: Subtitle generation takes too long

**Symptoms**:
WhisperX transcription is very slow

**Solution**:

1. **Use GPU**:
   ```python
   device = "cuda" if torch.cuda.is_available() else "cpu"
   model = whisperx.load_model(model_size, device)
   ```

2. **Use smaller model**:
   ```python
   model = whisperx.load_model("base", device)  # Faster but less accurate
   ```

3. **Reduce audio length**:
   - Split long audio files
   - Process in chunks

---

## Memory Issues

### Issue: "Out of memory" errors (RAM)

**Symptoms**:
```
MemoryError: Unable to allocate array
```

**Solution**:

1. **Close unnecessary programs**

2. **Process in smaller batches**:
   ```python
   # Don't process all stories at once
   for story in stories[:5]:  # Process 5 at a time
       process_story(story)
   ```

3. **Enable swap space** (Linux):
   ```bash
   sudo fallocate -l 8G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

4. **Use streaming/generators** where possible

---

## Pipeline Errors

### Issue: Pipeline stops mid-execution

**Symptoms**:
Pipeline exits without completing all stages

**Solution**:

1. **Check error messages**:
   - Look for exceptions in output
   - Check log files

2. **Run stages individually**:
   ```python
   # Test each stage separately
   script_gen.generate_from_storyidea(story)
   # If this works, continue to next stage
   ```

3. **Add error handling**:
   ```python
   try:
       voice_maker.generate_audio()
   except Exception as e:
       print(f"Error: {e}")
       # Handle or log error
   ```

### Issue: Generated files are missing

**Symptoms**:
Expected output files don't exist

**Solution**:

1. **Check folder structure**:
   ```bash
   ls -R Stories/
   ```

2. **Verify each stage completed**:
   - Look for success messages
   - Check intermediate folders

3. **Check file permissions**:
   ```bash
   ls -la Stories/
   chmod -R u+w Stories/
   ```

### Issue: FFmpeg errors during conversion

**Symptoms**:
```
ffmpeg.Error: Command failed
```

**Solution**:

1. **Check FFmpeg installation**:
   ```bash
   ffmpeg -version
   ```

2. **Verify input files exist**:
   ```bash
   ls -lh Stories/3_VoiceOver/*/
   ```

3. **Check file format**:
   ```bash
   ffprobe input_file.mp3
   ```

4. **Update FFmpeg**:
   ```bash
   # Ubuntu
   sudo apt update && sudo apt upgrade ffmpeg
   
   # macOS
   brew upgrade ffmpeg
   ```

---

## General Tips

### Enable Debug Mode

Add to your script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check System Resources

```bash
# CPU and memory
htop

# GPU
nvidia-smi -l 1

# Disk space
df -h
```

### Test Components Individually

Before running full pipeline, test each component:

```python
# Test OpenAI
import openai
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "test"}]
)

# Test ElevenLabs
from elevenlabs import ElevenLabs
client = ElevenLabs()
voices = client.voices.get_all()

# Test WhisperX
import whisperx
model = whisperx.load_model("base", "cpu")
```

---

## Still Having Issues?

1. **Check logs**: Look in `logs/` directory (if logging enabled)
2. **Search issues**: [GitHub Issues](https://github.com/Nomoos/StoryGenerator/issues)
3. **Create issue**: Include:
   - Python version: `python --version`
   - OS: `uname -a` (Linux/Mac) or `systeminfo` (Windows)
   - GPU: `nvidia-smi`
   - Error message and full traceback
   - Steps to reproduce

---

*Last Updated: 2025-10-06*
