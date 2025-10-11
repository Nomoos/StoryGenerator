# Hardware Requirements

This guide helps you choose the right hardware setup for running the StoryGenerator pipeline.

## Overview

StoryGenerator can run in different modes depending on your hardware:
- **Cloud/API-based**: Minimal hardware, uses cloud services (OpenAI, ElevenLabs)
- **Hybrid**: Local orchestration with some cloud services
- **Full Local**: All processing done locally including ML models

## Minimum Requirements (Cloud/API-based workflow)

For users who primarily use cloud APIs (OpenAI, ElevenLabs):

- **CPU**: Any modern processor (4+ cores recommended)
- **RAM**: 8GB
- **GPU**: Not required (uses cloud APIs)
- **Storage**: 50GB for codebase and generated content
- **Network**: Stable internet connection for API calls

## Recommended for Local AI Models

If you want to run ML models locally (Whisper ASR, SDXL, LTX-Video):

### RTX 3060 Ti / RTX 3070 (8GB VRAM)

**Capabilities**:
- **Text Generation**: Llama-3.1-8B (quantized)
- **Image Generation**: SDXL Base only (no refiner)
- **Video Generation**: Not recommended
- **Workflow**: Sequential only, limited batch sizes

**Best For**: Experimentation, development, small-scale projects

### RTX 3090 / RTX 4070 Ti (24GB VRAM)

**Capabilities**:
- **Text Generation**: Qwen2.5-14B or Llama-3.1-8B
- **Image Generation**: SDXL Base + Refiner
- **Video Generation**: LTX-Video (5-second clips)
- **Workflow**: Sequential processing, some parallel capability

**Best For**: Serious development, moderate content production

### RTX 4090 (24GB VRAM)

**Capabilities**:
- **Text Generation**: Qwen2.5-14B (full float16)
- **Image Generation**: SDXL Base + Refiner + LoRAs
- **Video Generation**: LTX-Video (5-second clips) or SVD (2-second clips)
- **Workflow**: Limited parallel processing
- **Performance**: Good for 1-2 videos per hour

**Best For**: Professional content creation, high-quality output

### 🚀 RTX 5090 (32GB VRAM) - **OPTIMAL**

**Capabilities**:
- **Text Generation**: Qwen2.5-14B with good headroom
- **Image Generation**: SDXL Base + Refiner or batch generation (2 images)
- **Video Generation**: LTX-Video (8-second clips) or SVD (short clips)
- **Workflow**: Some parallel processing capability
- **Performance**: 1.7-2x faster than RTX 4090
- **Pipeline**: Complete 30-video pipeline in ~3.5 hours
- **Multi-tasking**: Run text + image generation simultaneously with careful memory management
- **Quality**: Extended video lengths, higher resolutions compared to 24GB cards

**Best For**: Professional studios, high-volume production, optimal quality

**💡 For detailed RTX 5090 optimization**:
- [RTX 5090 Quick Reference Guide](RTX5090_QUICKREF.md)
- [RTX 5090 Configuration File](../config/rtx5090.yaml)
- [GPU Comparison Guide](GPU_COMPARISON.md)

## Multi-GPU Setups

### 2x RTX 5090 (64GB total VRAM)

**Capabilities**:
- **Performance**: 60-70% faster pipeline compared to single GPU
- **Setup**: GPU 0 for text/vision, GPU 1 for image/video
- **Workflow**: True parallel processing
- **Use Case**: High-volume content production

**Configuration**:
```bash
# Set specific GPUs for different tasks
export CUDA_VISIBLE_DEVICES=0  # For text generation
export CUDA_VISIBLE_DEVICES=1  # For image/video generation
```

### 3x RTX 5090 (96GB total VRAM)

**Capabilities**:
- **Performance**: 80-85% faster pipeline compared to single GPU
- **Setup**: Dedicated GPU per stage (text, image, video)
- **Workflow**: Full parallel processing
- **Use Case**: Enterprise-level content production
- **Bonus**: Can run larger models with multi-GPU configurations

**Configuration**:
```bash
# Dedicated GPUs
export TEXT_GPU=0
export IMAGE_GPU=1
export VIDEO_GPU=2
```

## Memory Requirements by Task

| Task | Minimum VRAM | Recommended VRAM | Optimal VRAM |
|------|--------------|------------------|--------------|
| GPT-like Models (8B) | 6GB | 12GB | 16GB |
| GPT-like Models (14B) | 12GB | 24GB | 32GB |
| SDXL Base | 6GB | 10GB | 12GB |
| SDXL Base + Refiner | 10GB | 16GB | 24GB |
| LTX-Video (5s) | 12GB | 24GB | 32GB |
| LTX-Video (8s) | 20GB | 32GB | 48GB |
| Whisper ASR | 2GB | 4GB | 6GB |

## Storage Requirements

| Content Type | Storage per Video | 100 Videos | 1000 Videos |
|-------------|-------------------|------------|-------------|
| Story Ideas | 10KB | 1MB | 10MB |
| Scripts | 5KB | 500KB | 5MB |
| Audio (1min) | 2MB | 200MB | 2GB |
| Keyframes (5-10) | 20MB | 2GB | 20GB |
| Video (1min, 1080p) | 50MB | 5GB | 50GB |
| **Total per Video** | ~75MB | ~7.5GB | ~75GB |

**Recommendation**: 
- Development: 100GB SSD
- Production: 500GB-1TB SSD
- Archive: HDD or cloud storage

## CPU Requirements

| Task | Minimum | Recommended | Optimal |
|------|---------|-------------|---------|
| Orchestration | 4 cores | 8 cores | 16+ cores |
| Video Encoding | 4 cores | 8 cores | 16+ cores |
| Parallel Processing | 8 cores | 16 cores | 32+ cores |

**Note**: More cores help with FFmpeg encoding, parallel task execution, and general system responsiveness.

## RAM Requirements

| Workload | Minimum | Recommended | Optimal |
|----------|---------|-------------|---------|
| Cloud APIs Only | 8GB | 16GB | 32GB |
| Local Models | 16GB | 32GB | 64GB |
| Large-Scale Production | 32GB | 64GB | 128GB |

**Tip**: More RAM allows for larger batch sizes and better multi-tasking.

## Network Requirements

| Task | Bandwidth | Latency | Notes |
|------|-----------|---------|-------|
| API Calls (Cloud) | 10+ Mbps | <100ms | Stable connection required |
| Model Downloads | 100+ Mbps | Any | One-time downloads can be large (10-50GB) |
| Asset Downloads | 50+ Mbps | Any | Optional, for external resources |

## Operating System

StoryGenerator is cross-platform and supports:

- **Windows 10/11**: Full support, recommended for NVIDIA GPUs
- **Linux (Ubuntu 20.04+)**: Full support, optimal for servers
- **macOS**: Supported for orchestration, limited GPU acceleration

**GPU Support**:
- **NVIDIA GPUs**: Full CUDA support (required for local ML models)
- **AMD GPUs**: Limited support via ROCm (experimental)
- **Apple Silicon**: CPU inference only, no GPU acceleration for ML models

## Choosing Your Setup

### For Beginners
- Start with **Cloud/API-based** approach
- Minimal hardware investment
- Learn the pipeline before committing to hardware

### For Developers
- **RTX 3060 Ti or better** for local development
- Enables faster iteration and testing
- Good for understanding model behavior

### For Content Creators
- **RTX 4090 or RTX 5090** for production
- Balance of performance and cost
- Can produce high-quality content efficiently

### For Studios/Enterprises
- **Multi-GPU setup (2-3x RTX 5090)**
- Maximum throughput
- Professional-grade quality and reliability

## Cost Considerations

### Cloud/API Approach
- **Pros**: No upfront hardware cost, pay-as-you-go, always up-to-date
- **Cons**: Ongoing costs, dependent on internet, limited customization
- **Cost**: $0.50-$2.00 per video (varies by complexity)

### Local GPU Approach
- **Pros**: One-time cost, unlimited generation, full control, no internet required
- **Cons**: High upfront cost, maintenance, power consumption
- **Cost**: $1,500-$4,000 per GPU (RTX 4090/5090), $0.10-$0.20 per video in electricity

### Hybrid Approach (Recommended)
- Use cloud APIs for initial development and testing
- Invest in local GPUs once workflow is established
- Use local for high-volume, cloud for occasional/special tasks

## See Also

- [GPU Comparison Guide](GPU_COMPARISON.md) - Detailed GPU benchmarks
- [RTX 5090 Quick Reference](RTX5090_QUICKREF.md) - Optimization guide for RTX 5090
- [Models Documentation](MODELS.md) - Model requirements and specifications
- [Installation Guide](INSTALLATION.md) - Software setup instructions
