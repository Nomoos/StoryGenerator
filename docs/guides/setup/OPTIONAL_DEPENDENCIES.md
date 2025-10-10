# Optional Dependencies Guide - Windows

This guide covers installation of optional dependencies for local model inference and research features on Windows. These tools enable you to run StoryGenerator with local models instead of cloud APIs, which can be more cost-effective and privacy-friendly for experimentation.

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

**Option 1: Using Chocolatey (Recommended)**
```powershell
# Install Chocolatey if not already installed
# Run in PowerShell as Administrator:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg

# Verify installation
ffmpeg -version
```

**Option 2: Manual Installation**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
2. Extract to `C:\Program Files\ffmpeg`
3. Add `C:\Program Files\ffmpeg\bin` to PATH:
   - Open System Properties → Environment Variables
   - Edit "Path" under System variables
   - Add new entry: `C:\Program Files\ffmpeg\bin`
   - Click OK to save
4. Restart terminal and verify: `ffmpeg -version`

**Verification**

After installation, open PowerShell or Command Prompt and run:
```powershell
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

### Windows Installation

1. Download the Ollama installer from [ollama.com/download/windows](https://ollama.com/download/windows)
2. Run the installer (OllamaSetup.exe)
3. Ollama will start automatically as a Windows service
4. Open Command Prompt or PowerShell and verify:
   ```powershell
   ollama --version
   ```

### Installing Models

After installing Ollama, download models you want to use:

```powershell
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

```powershell
# Test with a simple prompt
ollama run llama2 "Write a short story about a robot."

# Test from C# code (after running tests)
cd src\CSharp
dotnet test --filter "Category=Integration&FullyQualifiedName~OllamaClient"
```

### Ollama Configuration

Ollama runs as a service on `http://localhost:11434` by default.

**Check if Ollama is running**:
```powershell
curl http://localhost:11434/api/version
```

**Restart Ollama service** (if needed):
```powershell
# Stop Ollama
net stop Ollama

# Start Ollama
net start Ollama
```

### Troubleshooting Ollama

**Issue**: "Failed to connect to Ollama"
```powershell
# Check if service is running
Get-Service Ollama

# Restart service
Restart-Service Ollama
```

**Issue**: "Model not found"
```powershell
# List installed models
ollama list

# Pull the required model
ollama pull llama2
```

**Issue**: "Out of memory"
- Use smaller models (7B instead of 13B or 70B)
- Close other applications
- Increase system virtual memory
- Consider using quantized models

---

## Python + faster-whisper Installation

faster-whisper provides high-quality automatic speech recognition (ASR) for subtitle generation and audio transcription.

### Prerequisites

- Python 3.8 or higher
- (Optional) CUDA-capable GPU for faster processing

### Installation

**Step 1: Install Python**

Download and install Python from [python.org](https://www.python.org/downloads/windows/)

During installation:
- ✅ Check "Add Python to PATH"
- ✅ Check "Install pip"

Verify installation:
```powershell
python --version
# Should show Python 3.8 or higher
```

**Step 2: Install faster-whisper**
```powershell
# Using pip
pip install faster-whisper>=0.10.0

# Or install from requirements
cd StoryGenerator\research\python
pip install -r requirements.txt
```

**Step 3: Install GPU Support (Optional)**

If you have an NVIDIA GPU with CUDA:

1. Install CUDA Toolkit from [NVIDIA](https://developer.nvidia.com/cuda-downloads)
2. Install PyTorch with CUDA support:
   ```powershell
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
3. Verify CUDA is available:
   ```powershell
   python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
   ```

### Testing faster-whisper

```powershell
# Test from Python
python -c "from faster_whisper import WhisperModel; model = WhisperModel('base', device='cpu', compute_type='int8'); print('✅ faster-whisper is working!')"

# Test from C# integration tests
cd src\CSharp
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
- Detects Python executable
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
    pythonExecutable: "python",
    scriptPath: @"C:\path\to\whisper_subprocess.py"
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
```powershell
cd src\CSharp
dotnet test --filter "Category=Integration"
```

### Run Specific Integration Tests
```powershell
# Test FFmpeg functionality
dotnet test --filter "Category=Integration&FullyQualifiedName~FFmpegClient"

# Test Ollama functionality
dotnet test --filter "Category=Integration&FullyQualifiedName~OllamaClient"

# Test Whisper functionality
dotnet test --filter "Category=Integration&FullyQualifiedName~WhisperClient"
```

### Run Unit Tests Only (No Dependencies Required)
```powershell
dotnet test --filter "Category!=Integration"
```

---

## Verifying Installation

Use this PowerShell script to verify all optional dependencies are installed correctly:

```powershell
# Save as: scripts\verify_optional_deps.ps1

Write-Host "🔍 Verifying Optional Dependencies..." -ForegroundColor Cyan
Write-Host ""

# Check FFmpeg
if (Get-Command ffmpeg -ErrorAction SilentlyContinue) {
    $ffmpegVersion = (ffmpeg -version 2>&1 | Select-Object -First 1)
    Write-Host "✅ FFmpeg installed: $ffmpegVersion" -ForegroundColor Green
} else {
    Write-Host "❌ FFmpeg not found" -ForegroundColor Red
}

# Check Ollama
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    $ollamaVersion = (ollama --version 2>&1)
    Write-Host "✅ Ollama installed: $ollamaVersion" -ForegroundColor Green
    
    # Check if Ollama is running
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434/api/version" -UseBasicParsing -ErrorAction SilentlyContinue
        Write-Host "✅ Ollama service is running" -ForegroundColor Green
        
        # List installed models
        Write-Host "📦 Installed Ollama models:" -ForegroundColor Cyan
        ollama list
    } catch {
        Write-Host "⚠️  Ollama installed but not running (run: ollama serve)" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Ollama not found" -ForegroundColor Red
}

# Check Python and faster-whisper
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = (python --version 2>&1)
    Write-Host "✅ Python installed: $pythonVersion" -ForegroundColor Green
    
    # Check faster-whisper
    $whisperCheck = python -c "import faster_whisper" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ faster-whisper installed" -ForegroundColor Green
    } else {
        Write-Host "❌ faster-whisper not found (run: pip install faster-whisper)" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Python not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "✨ Verification complete!" -ForegroundColor Cyan
```

Run the script:
```powershell
.\scripts\verify_optional_deps.ps1
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
- Use hardware acceleration where available (NVENC for NVIDIA GPUs)
- Process videos in batches
- Use appropriate codecs for your use case
- Example: `ffmpeg -hwaccel cuda -i input.mp4 output.mp4`

### Ollama
- Start with smaller models (7B) for testing
- Use GPU acceleration when available
- Keep models in memory between requests
- Monitor RAM usage with large models
- Use Windows Task Manager to monitor resource usage

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
```powershell
# Restart PowerShell or Command Prompt
# Or reload PATH environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

**Issue**: Permission denied
```powershell
# Run PowerShell or Command Prompt as Administrator
# Right-click → "Run as administrator"
```

### FFmpeg Issues

**Issue**: FFmpeg not in PATH
```powershell
# Add to PATH manually
$env:Path += ";C:\Program Files\ffmpeg\bin"

# Or add permanently via System Properties → Environment Variables
```

**Issue**: Codec not found
```powershell
# Verify FFmpeg build includes required codecs
ffmpeg -codecs | findstr h264
```

### Ollama Issues

**Issue**: Models download slowly
- Use wired connection instead of WiFi
- Download during off-peak hours
- Use `ollama pull model_name` to pre-download

**Issue**: Inference is slow
- Use GPU-accelerated models (requires NVIDIA GPU)
- Use smaller models for testing
- Close other GPU applications
- Increase system RAM/virtual memory

**Issue**: Service won't start
```powershell
# Check Windows services
Get-Service Ollama

# Restart service
Restart-Service Ollama

# Check event logs
Get-EventLog -LogName Application -Source Ollama -Newest 10
```

### faster-whisper Issues

**Issue**: ImportError after installation
```powershell
# Reinstall with dependencies
pip uninstall faster-whisper
pip install faster-whisper>=0.10.0 --no-cache-dir
```

**Issue**: CUDA not available
```powershell
# Install CUDA toolkit
# Download from: https://developer.nvidia.com/cuda-downloads

# Verify CUDA
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

**Issue**: Python not found
```powershell
# Verify Python installation
python --version

# If not found, reinstall Python and check "Add to PATH"
# Download from: https://www.python.org/downloads/windows/
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
*Platform: Windows*
