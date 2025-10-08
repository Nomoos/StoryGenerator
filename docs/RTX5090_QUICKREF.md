# RTX 5090 Quick Reference Guide

Quick reference for optimizing StoryGenerator on NVIDIA RTX 5090 (32GB VRAM).

## 🎯 Quick Setup

### Prerequisites
```bash
# CUDA Toolkit
sudo apt install nvidia-driver-535 nvidia-cuda-toolkit

# Python environment
python3.10 -m venv venv
source venv/bin/activate

# Core dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers diffusers accelerate safetensors xformers
pip install faster-whisper openai
```

### Verify GPU
```bash
nvidia-smi
# Should show: RTX 5090, 32GB VRAM

python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
# Should output: True, NVIDIA GeForce RTX 5090
```

## 🚀 Three Main Workflows

### 1. Maximum Throughput (Parallel)
**Best for**: High-volume content production  
**Models**: Llama-3.1-8B (8GB) + SDXL Base (12GB)  
**VRAM Used**: 20GB + 12GB buffer  
**Speed**: 1.6x faster than sequential

```python
# Load all models at startup
text_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto"
)

image_pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16
).to("cuda")

# Generate in parallel using ThreadPoolExecutor
```

### 2. Maximum Quality (Sequential)
**Best for**: Premium content  
**Models**: Switch between Qwen-32B (32GB) → SDXL+Refiner (16GB) → LTX-Video (24GB)  
**VRAM Used**: One at a time (sequential)  
**Quality**: 1.3x better output

```python
# Stage 1: Premium text (32GB)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-32B-Instruct", ...)
script = model.generate(...)
del model; torch.cuda.empty_cache()

# Stage 2: Images with refiner (16GB)
base = load_sdxl_base()
refiner = load_sdxl_refiner()
images = generate_and_refine(...)
del base, refiner; torch.cuda.empty_cache()

# Stage 3: High-quality video (24GB)
video_pipe = load_ltx_video()
videos = video_pipe.generate(...)
```

### 3. Batch Production (Balanced)
**Best for**: Moderate volume, good quality  
**Models**: Qwen-14B (14GB) + SDXL Base (12GB)  
**VRAM Used**: 26GB + 6GB buffer  
**Efficiency**: 2.5x throughput for batches

```python
# Load persistent models
text_model = load_qwen_14b()  # 14GB
image_pipe = load_sdxl_with_refiner()  # 16GB

# Batch generate scripts
scripts = text_model.generate_batch(topics)  # 4 scripts in ~15s

# Batch generate images
for script in scripts:
    images = image_pipe(prompts[:4], ...)  # 4 images in ~8s
```

## 📊 Performance Targets

| Task | RTX 4090 | RTX 5090 | Speedup |
|------|----------|----------|---------|
| Script (360 words) | 15s | 8s | 1.9x |
| Image (1024x1024) | 3.5s | 2.0s | 1.75x |
| Batch 2 Images | N/A | 4.5s | Batch enabled |
| Video 5s (LTX) | 2.5min | 1.2min | 2.1x |
| Video 8s (LTX) | N/A | 2.0min | Extended |
| Full Pipeline (30 videos) | ~6 hrs | ~3.5 hrs | 1.7x |

## 🎛️ Configuration Quick Switch

Use the RTX 5090 optimized config:
```bash
# Copy optimized config
cp config/rtx5090.yaml config/pipeline.yaml

# Or specify at runtime
python generate.py --config config/rtx5090.yaml
```

## 💡 Memory Management Tips

### Monitor VRAM Usage
```bash
# Real-time monitoring
watch -n 1 nvidia-smi

# Or use nvtop (better UI)
sudo apt install nvtop
nvtop
```

### Clear Memory Between Stages
```python
import torch
import gc

# After each model use
del model
gc.collect()
torch.cuda.empty_cache()
torch.cuda.synchronize()
```

### Batch Size Recommendations
```python
# Text generation (Qwen-14B)
batch_size = 1  # Single video generation

# Image generation (SDXL)
batch_size = 4-6  # RTX 5090 can handle 6 images

# Video generation (LTX-Video)
batch_size = 1  # Videos are memory intensive
```

## 🔧 Optimization Flags

### PyTorch Optimization
```python
import torch

# Enable TF32 (faster matrix operations)
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

# Compile models (PyTorch 2.0+)
model = torch.compile(model)

# Enable cuDNN benchmark
torch.backends.cudnn.benchmark = True
```

### Diffusers Optimization
```python
# Enable xFormers (memory efficient attention)
pipe.enable_xformers_memory_efficient_attention()

# For RTX 5090, disable VAE tiling (not needed)
pipe.enable_vae_slicing(False)
pipe.enable_vae_tiling(False)

# Use attention slicing only for very large batches
# pipe.enable_attention_slicing(1)  # Usually not needed
```

## 🎬 Model Selection Matrix

### Text Generation
| Use Case | Model | VRAM | Speed |
|----------|-------|------|-------|
| Fast iteration | Llama-3.1-8B | 8GB | 65 tok/s |
| Balanced | Qwen2.5-14B | 14GB | 45 tok/s |
| Best quality | Qwen2.5-32B | 32GB | 25 tok/s |

### Image Generation
| Use Case | Model | VRAM | Speed |
|----------|-------|------|-------|
| Fast drafts | SDXL Base | 12GB | 2.0s |
| Production | SDXL + Refiner | 16GB | 3.5s |
| Batch | SDXL Base (6x) | 30GB | 8.0s |

### Video Generation
| Use Case | Model | VRAM | Length |
|----------|-------|------|--------|
| Standard clips | LTX-Video | 24GB | 5s |
| Extended clips | LTX-Video | 30GB | 10s |
| High quality | SVD | 20GB | 2-4s |

## 🐛 Troubleshooting

### Out of Memory (OOM)
```python
# Reduce batch size
images = pipe(prompt=prompts[:2])  # Try 2 instead of 4

# Enable gradient checkpointing (if needed)
model.gradient_checkpointing_enable()

# Use 8-bit quantization (last resort)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_8bit=True,
    device_map="auto"
)
```

### Slow Performance
```bash
# Check GPU utilization
nvidia-smi dmon -s u

# If utilization < 80%, check:
# 1. CPU bottleneck (upgrade CPU)
# 2. Storage bottleneck (use NVMe SSD)
# 3. Model not compiled (add torch.compile)
# 4. Not using xFormers (enable it)
```

### Model Loading Slow
```python
# Use local cache on fast SSD
import os
os.environ['HF_HOME'] = '/fast/ssd/huggingface_cache'

# Or specify cache dir
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir='/fast/ssd/huggingface_cache'
)
```

## 📈 Scaling Options

### Single RTX 5090
- Conservative: 28GB active + 20GB buffer
- Aggressive: 40GB active + 8GB buffer
- Quality: 32GB active + 16GB buffer (sequential)

### 2x RTX 5090 (96GB total)
- GPU 0: Text + Vision (22GB)
- GPU 1: Image + Video (40GB)
- Performance: 1.6-1.7x faster

### 3x RTX 5090 (144GB total)
- GPU 0: Text (14GB)
- GPU 1: Image (16GB)
- GPU 2: Video (24GB)
- Performance: 1.8-1.85x faster
- All stages run in parallel

## 📚 Additional Resources

- Full Documentation: [docs/MODELS.md#rtx-5090-optimization-guide](docs/MODELS.md#rtx-5090-optimization-guide)
- Configuration: [config/rtx5090.yaml](config/rtx5090.yaml)
- Model Cards: See individual model sections in MODELS.md
- Performance Benchmarks: [docs/MODELS.md#performance-benchmarks](docs/MODELS.md#performance-benchmarks)

## 🎯 Best Practices Summary

1. **Always use float16/bfloat16** - Optimal for 32GB VRAM
2. **Enable xFormers** - Memory efficient attention
3. **Enable torch.compile** - Significant speedup (PyTorch 2.0+)
4. **Monitor VRAM** - Use nvidia-smi or nvtop
5. **Clear cache between stages** - torch.cuda.empty_cache()
6. **Use fast storage** - NVMe SSD for model cache
7. **Sequential for large models** - 32GB requires careful memory management
8. **Profile your workflow** - Find bottlenecks
9. **Keep drivers updated** - Latest NVIDIA drivers for best performance
10. **Adequate cooling** - GPU will run hot under sustained load

## 💰 ROI Calculator

Monthly costs (30 videos/week):
- Cloud APIs: $50-100/month
- RTX 5090: $2,000 upfront + $50/month electricity
- Break-even: 6-8 months
- 2-year savings: $2,400-$7,200

---

**Last Updated**: 2024-10-08  
**Hardware**: NVIDIA RTX 5090 (32GB VRAM)  
**Software**: PyTorch 2.1+, CUDA 12.1+
