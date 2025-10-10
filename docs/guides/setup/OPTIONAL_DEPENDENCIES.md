# Optional Dependencies Guide

This guide covers installation of optional dependencies for local model inference and research features. These tools enable you to run StoryGenerator with local models instead of cloud APIs, which can be more cost-effective and privacy-friendly for experimentation.

## Overview

The optional dependencies are:

| Tool | Purpose | Required For | Priority |
|------|---------|--------------|----------|
| **FFmpeg** | Audio/video processing | Research prototypes, media manipulation | High |
| **Ollama** | Local LLM inference | Local script generation, research | Medium |
| **Python + faster-whisper** | Speech-to-text | Local ASR, subtitle generation | Medium |

**Note**: Core pipeline functionality in `StoryGenerator.Core` and `StoryGenerator.Pipeline` works without these tools. They are primarily for:
- Running integration tests
- Research and prototyping features
- Local model inference (alternative to cloud APIs)
- Fine-tuning workflows

---

## FFmpeg Installation

FFmpeg is used for audio and video processing in research prototypes.

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

### Windows

**Option 1: Using Chocolatey (Recommended)**
```powershell
# Install Chocolatey if not already installed
# See: https://chocolatey.org/install

# Install FFmpeg
choco install ffmpeg

# Verify installation
ffmpeg -version
```

**Option 2: Manual Installation**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\Program Files\ffmpeg`
3. Add `C:\Program Files\ffmpeg\bin` to PATH
4. Restart terminal and verify: `ffmpeg -version`

### macOS

```bash
# Using Homebrew
brew install ffmpeg

# Verify installation
ffmpeg -version
```

### Verification

After installation, run:
```bash
ffmpeg -version
ffprobe -version
```

Both commands should display version information.

---

## Ollama Installation

Ollama enables local LLM inference for script generation and experimentation. This allows you to run models like Llama 2, Mistral, and others locally without API costs.

### Why Use Ollama?

- **Cost-effective**: No API costs for experimentation
- **Privacy**: Run models locally on your hardware
- **Fine-tuning**: Experiment with custom models and prompts
- **Offline**: Works without internet connection
- **Fast iteration**: Test prompts and models quickly

### System Requirements

- **CPU**: Modern multi-core processor (8+ cores recommended)
- **RAM**: 16GB minimum, 32GB+ recommended
- **Storage**: 10GB+ per model
- **GPU** (optional): NVIDIA GPU with 8GB+ VRAM for faster inference

### Ubuntu/Debian

```bash
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve &

# Verify installation
ollama --version
```

### Windows

1. Download installer from [ollama.com](https://ollama.com/download/windows)
2. Run the installer
3. Ollama will start automatically as a service
4. Open Command Prompt or PowerShell and verify:
   ```powershell
   ollama --version
   ```

### macOS

```bash
# Download and install
# Visit https://ollama.com/download/mac
# Or use:
brew install ollama

# Start Ollama
ollama serve &

# Verify installation
ollama --version
```

### Installing Models

After installing Ollama, download models you want to use:

```bash
# For script generation (recommended for StoryGenerator)
ollama pull llama2          # Meta's Llama 2 (7B)
ollama pull mistral         # Mistral 7B
ollama pull llama3.1        # Meta's Llama 3.1 (8B)

# Larger models (better quality, requires more resources)
ollama pull llama2:13b      # Llama 2 13B
ollama pull llama2:70b      # Llama 2 70B (requires 48GB+ RAM)

# List installed models
ollama list
```

**Recommended for StoryGenerator**:
- Start with `llama2` (7B) or `mistral` (7B) for testing
- Use `llama3.1` for better quality
- Fine-tune prompts before upgrading to larger models

### Testing Ollama

```bash
# Test with a simple prompt
ollama run llama2 "Write a short story about a robot."

# Test from C# code (after running tests)
cd /home/runner/work/StoryGenerator/StoryGenerator/src/CSharp
dotnet test --filter "Category=Integration&FullyQualifiedName~OllamaClient"
```

### Ollama Configuration

Ollama runs as a service on `http://localhost:11434` by default.

**Check if Ollama is running**:
```bash
curl http://localhost:11434/api/version
```

**Start Ollama manually** (if not running as service):
```bash
ollama serve
```

### Troubleshooting Ollama

**Issue**: "Failed to connect to Ollama"
```bash
# Check if service is running
ps aux | grep ollama

# Start service
ollama serve &

# Or restart service
sudo systemctl restart ollama  # Linux with systemd
```

**Issue**: "Model not found"
```bash
# List installed models
ollama list

# Pull the required model
ollama pull llama2
```

**Issue**: "Out of memory"
- Use smaller models (7B instead of 13B or 70B)
- Close other applications
- Increase system swap space
- Consider using quantized models

---

## Python + faster-whisper Installation

faster-whisper provides high-quality automatic speech recognition (ASR) for subtitle generation and audio transcription.

### Prerequisites

- Python 3.8 or higher
- (Optional) CUDA-capable GPU for faster processing

### Installation

**Step 1: Verify Python Installation**
```bash
python3 --version
# Should show Python 3.8 or higher
```

**Step 2: Install faster-whisper**
```bash
# Using pip
pip install faster-whisper>=0.10.0

# Or install from requirements
pip install -r research/python/requirements.txt
```

**Step 3: Install GPU Support (Optional)**

If you have an NVIDIA GPU with CUDA:
```bash
# Install CUDA Toolkit first
# See: https://developer.nvidia.com/cuda-downloads

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify CUDA is available
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Testing faster-whisper

```bash
# Test from Python
python3 << EOF
from faster_whisper import WhisperModel

# Load model (will download on first use)
model = WhisperModel("base", device="cpu", compute_type="int8")
print("✅ faster-whisper is working!")
EOF

# Test from C# integration tests
cd /home/runner/work/StoryGenerator/StoryGenerator/src/CSharp
dotnet test --filter "Category=Integration&FullyQualifiedName~WhisperClient"
```

### Available Models

faster-whisper supports multiple model sizes:

| Model | Parameters | VRAM | Speed | Quality |
|-------|-----------|------|-------|---------|
| tiny | 39M | ~1GB | Fastest | Basic |
| base | 74M | ~1GB | Fast | Good |
| small | 244M | ~2GB | Medium | Better |
| medium | 769M | ~5GB | Slow | Great |
| large-v3 | 1550M | ~10GB | Slowest | Best |

**Recommendation**:
- **CPU-only**: Use `base` or `small`
- **GPU (8GB VRAM)**: Use `medium` or `large-v3`
- **GPU (16GB+ VRAM)**: Use `large-v3` for best quality

### Configuration in Code

The WhisperClient in StoryGenerator.Research automatically:
- Detects Python executable (`python` vs `python3`)
- Finds the `whisper_subprocess.py` script
- Uses appropriate device (CPU/CUDA)

Example usage:
```csharp
// Basic usage (auto-detects everything)
var client = new WhisperClient();

// Custom configuration
var client = new WhisperClient(
    modelSize: "large-v3",
    device: "cuda",           // or "cpu", "auto"
    computeType: "float16",   // or "int8", "float32"
    pythonExecutable: "python3",
    scriptPath: "/path/to/whisper_subprocess.py"
);

// Transcribe audio
var result = await client.TranscribeAsync(
    audioPath: "audio.mp3",
    language: "en",
    wordTimestamps: true
);
```

---

## Running Integration Tests

After installing the optional dependencies, you can run the full integration test suite:

### Run All Integration Tests
```bash
cd src/CSharp
dotnet test --filter "Category=Integration"
```

### Run Specific Integration Tests
```bash
# Test FFmpeg functionality
dotnet test --filter "Category=Integration&FullyQualifiedName~FFmpegClient"

# Test Ollama functionality
dotnet test --filter "Category=Integration&FullyQualifiedName~OllamaClient"

# Test Whisper functionality
dotnet test --filter "Category=Integration&FullyQualifiedName~WhisperClient"
```

### Run Unit Tests Only (No Dependencies Required)
```bash
dotnet test --filter "Category!=Integration"
```

---

## Verifying Installation

Use this script to verify all optional dependencies are installed correctly:

```bash
#!/bin/bash
# save as: scripts/verify_optional_deps.sh

echo "🔍 Verifying Optional Dependencies..."
echo ""

# Check FFmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg installed: $(ffmpeg -version | head -n1)"
else
    echo "❌ FFmpeg not found"
fi

# Check Ollama
if command -v ollama &> /dev/null; then
    echo "✅ Ollama installed: $(ollama --version)"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/version &> /dev/null; then
        echo "✅ Ollama service is running"
        
        # List installed models
        echo "📦 Installed Ollama models:"
        ollama list
    else
        echo "⚠️  Ollama installed but not running (run: ollama serve)"
    fi
else
    echo "❌ Ollama not found"
fi

# Check Python and faster-whisper
if command -v python3 &> /dev/null; then
    echo "✅ Python installed: $(python3 --version)"
    
    # Check faster-whisper
    if python3 -c "import faster_whisper" 2>/dev/null; then
        echo "✅ faster-whisper installed"
    else
        echo "❌ faster-whisper not found (run: pip install faster-whisper)"
    fi
else
    echo "❌ Python 3 not found"
fi

echo ""
echo "✨ Verification complete!"
```

Make it executable and run:
```bash
chmod +x scripts/verify_optional_deps.sh
./scripts/verify_optional_deps.sh
```

---

## Local vs Cloud Models

### When to Use Local Models (Ollama, faster-whisper)

**Advantages**:
- ✅ No API costs for experimentation
- ✅ Complete privacy (data stays local)
- ✅ Fast iteration and testing
- ✅ No rate limits
- ✅ Works offline
- ✅ Good for fine-tuning prompts

**Disadvantages**:
- ❌ Requires more local resources (RAM, GPU)
- ❌ Initial model download time
- ❌ Generally lower quality than cloud APIs
- ❌ Slower inference on CPU

**Best for**:
- Research and prototyping
- Testing new prompts and workflows
- Privacy-sensitive projects
- High-volume processing
- Learning and experimentation

### When to Use Cloud APIs (OpenAI, ElevenLabs)

**Advantages**:
- ✅ Higher quality output
- ✅ Faster inference
- ✅ No local resource requirements
- ✅ Always latest models
- ✅ Professional-grade results

**Disadvantages**:
- ❌ API costs
- ❌ Rate limits
- ❌ Requires internet connection
- ❌ Data sent to external services

**Best for**:
- Production content
- Final video generation
- When quality is critical
- Limited local resources

### Recommended Workflow

1. **Prototype locally**: Use Ollama for script generation testing
2. **Refine prompts**: Iterate quickly with local models
3. **Validate quality**: Test with cloud APIs (GPT-4) occasionally
4. **Production**: Use cloud APIs for final content generation
5. **Fine-tune**: Adjust local models based on cloud results

---

## Performance Tips

### FFmpeg
- Use hardware acceleration where available (`-hwaccel cuda`)
- Process videos in batches
- Use appropriate codecs for your use case

### Ollama
- Start with smaller models (7B) for testing
- Use GPU acceleration when available
- Keep models in memory between requests
- Monitor RAM usage with large models

### faster-whisper
- Use GPU acceleration for 5-10x speedup
- Choose model size based on your hardware
- Use `compute_type="int8"` on CPU for speed
- Use `compute_type="float16"` on GPU for best quality
- Enable VAD filtering to skip silence

---

## Troubleshooting

### General Issues

**Issue**: Command not found after installation
```bash
# Restart your terminal
# Or reload PATH
source ~/.bashrc  # Linux/macOS
# Or restart PowerShell on Windows
```

**Issue**: Permission denied
```bash
# Linux/macOS: Use sudo for system-wide installation
sudo apt install ffmpeg

# Or install in user space
pip install --user faster-whisper
```

### FFmpeg Issues

See [INSTALLATION.md](INSTALLATION.md#troubleshooting) for FFmpeg-specific issues.

### Ollama Issues

**Issue**: Models download slowly
- Use wired connection instead of WiFi
- Download during off-peak hours
- Use `ollama pull model_name` to pre-download

**Issue**: Inference is slow
- Use GPU-accelerated models
- Use smaller models for testing
- Close other GPU applications
- Increase system RAM/swap

### faster-whisper Issues

**Issue**: ImportError after installation
```bash
# Reinstall with dependencies
pip uninstall faster-whisper
pip install faster-whisper>=0.10.0 --no-cache-dir
```

**Issue**: CUDA not available
```bash
# Install CUDA toolkit
# See: https://developer.nvidia.com/cuda-downloads

# Verify CUDA
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

---

## Support

For issues with optional dependencies:

1. Check this guide first
2. See [TROUBLESHOOTING.md](../general/TROUBLESHOOTING.md)
3. Check tool-specific documentation:
   - [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
   - [Ollama Documentation](https://github.com/ollama/ollama/blob/main/README.md)
   - [faster-whisper Documentation](https://github.com/guillaumekln/faster-whisper)
4. Create a [GitHub Issue](https://github.com/Nomoos/StoryGenerator/issues)

---

*Last Updated: 2025-10-10*
