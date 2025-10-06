"""
SDXL Configuration for Keyframe Generation

This file contains configuration settings for SDXL-based keyframe generation,
including model parameters, resolution settings, and optimization options.
"""

# SDXL Model Configuration
SDXL_BASE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
SDXL_REFINER_MODEL = "stabilityai/stable-diffusion-xl-refiner-1.0"

# Generation Settings
DEFAULT_WIDTH = 1080  # 9:16 aspect ratio for vertical video
DEFAULT_HEIGHT = 1920
DEFAULT_STEPS = 40
DEFAULT_REFINER_STEPS = 20
DEFAULT_GUIDANCE_SCALE = 7.5
DEFAULT_REFINER_GUIDANCE_SCALE = 7.5

# Target FPS for video (for keyframe density calculation)
TARGET_FPS = 60

# Performance Settings
USE_REFINER = True  # Whether to use the refiner model
ENABLE_ATTENTION_SLICING = True  # Reduce VRAM usage
ENABLE_VAE_SLICING = True  # Further reduce VRAM usage
ENABLE_CPU_OFFLOAD = False  # Offload models to CPU when not in use (slower but saves VRAM)
TORCH_DTYPE = "float16"  # Use float16 for faster inference on GPU

# Quality Settings
DEFAULT_STYLE = "cinematic"  # Default style preset from style_presets.json
USE_NEGATIVE_PROMPTS = True  # Whether to use negative prompts
SEED = 42  # Default seed for reproducibility (None for random)

# Keyframe Generation Strategy
# Number of keyframes based on scene duration
KEYFRAMES_SHORT_SCENE = 2  # < 5s
KEYFRAMES_MEDIUM_SCENE = 3  # 5-10s
KEYFRAMES_LONG_SCENE_BASE = 4  # > 10s
KEYFRAMES_PER_4_SECONDS = 1  # Add 1 keyframe per 4 seconds for long scenes
MAX_KEYFRAMES_PER_SCENE = 8  # Maximum keyframes for any scene

# Batch Processing
BATCH_SIZE = 1  # Process this many keyframes at once (increase if VRAM allows)

# Output Settings
SAVE_METADATA = True  # Save generation metadata with each keyframe
IMAGE_FORMAT = "PNG"  # Output image format (PNG or JPEG)
JPEG_QUALITY = 95  # JPEG quality if using JPEG format

# Prompt Engineering
QUALITY_BOOST_KEYWORDS = (
    "high quality, highly detailed, professional, 8k uhd, sharp focus"
)

FORMAT_SPECIFICATION = (
    "vertical format, 9:16 aspect ratio, mobile video format, "
    "portrait orientation, suitable for Reels/Shorts/TikTok"
)

# LoRA and ControlNet Settings (for future expansion)
ENABLE_LORA = False  # Whether to use LoRA models
LORA_MODELS = []  # List of LoRA model paths
LORA_WEIGHTS = []  # Corresponding weights for LoRA models

ENABLE_CONTROLNET = False  # Whether to use ControlNet
CONTROLNET_MODELS = []  # List of ControlNet model types

# IP-Adapter Settings (for character consistency)
ENABLE_IP_ADAPTER = False  # Whether to use IP-Adapter for consistency
IP_ADAPTER_MODEL = None  # IP-Adapter model path

# Model Caching
CACHE_DIR = None  # Use default HuggingFace cache (or specify custom path)
