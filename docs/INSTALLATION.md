# Installation Guide

This guide provides detailed instructions for setting up the StoryGenerator AI Video Pipeline.

## System Requirements

### Hardware Requirements

**Minimum**:
- CPU: 4+ cores
- RAM: 16GB
- GPU: NVIDIA GPU with 8GB VRAM (for image/video generation)
- Storage: 50GB free space (for models and output)

**Recommended**:
- CPU: 8+ cores
- RAM: 32GB
- GPU: NVIDIA GPU with 16GB+ VRAM (RTX 3090, RTX 4090, or better)
- Storage: 100GB+ free space (SSD recommended)

### Software Requirements

- **OS**: Ubuntu 22.04+ / Windows 10+ / macOS 12+
- **Python**: 3.8 or higher
- **CUDA**: 11.8 or 12.1 (for GPU support)
- **FFmpeg**: Latest version
- **Git**: Latest version

## Installation Steps

### 1. Install System Dependencies

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install FFmpeg
sudo apt install ffmpeg

# Install Git
sudo apt install git

# Install CUDA (if using GPU)
# Follow: https://developer.nvidia.com/cuda-downloads
```

#### Windows
```powershell
# Install Python from python.org
# Install FFmpeg from ffmpeg.org or via chocolatey:
choco install ffmpeg

# Install Git from git-scm.com

# Install CUDA Toolkit from NVIDIA
# Follow: https://developer.nvidia.com/cuda-downloads
```

#### macOS
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Install FFmpeg
brew install ffmpeg

# Install Git
brew install git
```

### 2. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator
```

### 3. Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 4. Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install base requirements
pip install -r requirements.txt

# Install GPU-specific dependencies (if using CUDA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install additional dependencies for full pipeline
pip install transformers accelerate diffusers whisperx
```

### 5. Configure API Keys

Create a `.env` file in the project root:

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your API keys
nano .env  # or use your preferred editor
```

Add your API keys:

```env
# OpenAI API Key (for GPT-4o-mini)
OPENAI_API_KEY=sk-your-openai-key-here

# ElevenLabs API Key (for voice synthesis)
ELEVENLABS_API_KEY=sk-your-elevenlabs-key-here

# Optional: HuggingFace Token (for private models)
HUGGINGFACE_TOKEN=hf_your-token-here
```

**⚠️ Security Note**: Never commit the `.env` file to version control!

### 6. Download Models (Optional)

Some models will download automatically on first use. To pre-download:

```bash
# Create a script to download models
python scripts/download_models.py
```

This will download:
- WhisperX models
- (Future) SDXL models
- (Future) Vision models

### 7. Verify Installation

Run the verification script:

```bash
python scripts/verify_setup.py
```

This will check:
- ✅ Python version
- ✅ Required packages installed
- ✅ GPU availability (if applicable)
- ✅ FFmpeg installation
- ✅ API keys configured
- ✅ Model availability

Expected output:
```
🔍 Verifying StoryGenerator Setup...

✅ Python 3.10.12
✅ pip 24.0
✅ FFmpeg installed
✅ GPU detected: NVIDIA GeForce RTX 3090 (24GB VRAM)
✅ CUDA 11.8 available
✅ All required packages installed
✅ OpenAI API key configured
✅ ElevenLabs API key configured
⚠️  SDXL model not found (will download on first use)

✨ Setup verification complete!
```

## Directory Structure

After installation, your directory should look like:

```
StoryGenerator/
├── venv/                  # Virtual environment (created by you)
├── .env                   # API keys (created by you)
├── Generators/            # Core pipeline generators
├── Models/                # Data models
├── Tools/                 # Utility functions
├── Generation/            # Manual scripts
├── Stories/               # Output directory (created automatically)
│   ├── 0_Ideas/
│   ├── 1_Scripts/
│   ├── 2_Revised/
│   ├── 3_VoiceOver/
│   └── 4_Titles/
├── config/                # Configuration files
├── docs/                  # Documentation
├── scripts/               # Setup and utility scripts
├── requirements.txt       # Python dependencies
├── README.md              # Project overview
└── .gitignore
```

## Troubleshooting

### Issue: "CUDA not available"

**Solution**:
```bash
# Verify CUDA installation
nvidia-smi

# Reinstall PyTorch with CUDA support
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Issue: "FFmpeg not found"

**Solution**:
```bash
# Ubuntu
sudo apt install ffmpeg

# Windows (with chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Verify installation
ffmpeg -version
```

### Issue: "ImportError: No module named 'whisperx'"

**Solution**:
```bash
pip install whisperx
```

### Issue: "API key not found"

**Solution**:
1. Ensure `.env` file exists in project root
2. Check `.env` file has correct format (no quotes around values)
3. Restart your terminal/IDE to reload environment variables

### Issue: "Out of memory" during generation

**Solution**:
1. Reduce batch size in configuration
2. Enable model offloading
3. Use smaller models
4. Close other GPU-intensive applications
5. Increase system swap space

### Issue: WhisperX installation fails

**Solution**:
```bash
# Install PyTorch first
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Then install WhisperX
pip install whisperx

# If still failing, install dependencies manually
pip install faster-whisper
```

## Next Steps

Once installation is complete:

1. **Quick Start**: See [QUICKSTART.md](QUICKSTART.md) for your first video
2. **Usage Guide**: See [USAGE.md](USAGE.md) for detailed usage
3. **Configuration**: See [CONFIGURATION.md](CONFIGURATION.md) for customization
4. **Examples**: Check the `examples/` directory for sample scripts

## Getting API Keys

### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API keys section
4. Create a new secret key
5. Copy the key to your `.env` file

**Pricing**: Pay-as-you-go (GPT-4o-mini is cost-effective)

### ElevenLabs API Key

1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up or log in
3. Navigate to Profile → API Keys
4. Copy your API key to `.env` file

**Pricing**: Free tier available, paid plans for more characters

### HuggingFace Token (Optional)

1. Go to [HuggingFace](https://huggingface.co/)
2. Sign up or log in
3. Navigate to Settings → Access Tokens
4. Create a read token
5. Copy to `.env` file

**Note**: Only needed for private/gated models

## Development Setup (Optional)

For contributors:

```bash
# Install development dependencies
pip install -r requirements/dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Run linting
flake8 Generators/ Models/ Tools/

# Format code
black Generators/ Models/ Tools/
```

## Docker Installation (Optional)

```bash
# Build Docker image
docker build -t storygenerator .

# Run container
docker run -it --gpus all -v $(pwd)/Stories:/app/Stories storygenerator

# With environment file
docker run -it --gpus all --env-file .env -v $(pwd)/Stories:/app/Stories storygenerator
```

## Cloud Setup (Optional)

### AWS EC2

1. Launch g4dn.xlarge or better instance
2. Use Deep Learning AMI (Ubuntu)
3. Follow Ubuntu installation steps above
4. Configure security groups for API access (if needed)

### Google Cloud Platform

1. Launch instance with NVIDIA T4 or better GPU
2. Use Deep Learning VM Image
3. Follow Ubuntu installation steps above
4. Configure firewall rules for API access (if needed)

### Azure

1. Launch NC-series VM with GPU
2. Use Data Science Virtual Machine image
3. Follow Ubuntu installation steps above
4. Configure network security group for API access (if needed)

## Performance Optimization

For optimal performance:

1. **Use SSD**: Store models and output on SSD for faster I/O
2. **GPU Memory**: Close other GPU applications before running
3. **Model Caching**: Let models download to default cache location
4. **Batch Processing**: Process multiple stories in one session
5. **Offloading**: Enable model offloading in config for lower VRAM usage

## Support

If you encounter issues:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Check [FAQ.md](FAQ.md)
3. Search [GitHub Issues](https://github.com/Nomoos/StoryGenerator/issues)
4. Create a new issue with:
   - System information
   - Error message
   - Steps to reproduce

---

*Last Updated: 2025-10-06*
