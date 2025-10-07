# Implementation Guide: AI Model C# Interfaces

This guide provides step-by-step instructions for implementing the AI model interfaces defined for the StoryGenerator project.

## 📋 Overview

This implementation addresses the requirements from Issue: **Environment & Model Setup**

The following C# interfaces have been created to integrate AI models:

1. ✅ **ISpeechRecognitionClient** - faster-whisper-large-v3
2. ✅ **ITextGenerationClient** - Qwen2.5-14B / Llama-3.1-8B
3. ✅ **IVisionLanguageClient** - LLaVA-OneVision / Phi-3.5-vision
4. ✅ **IImageGenerationClient** - SDXL base + refiner
5. ✅ **IVideoGenerationClient** - LTX-Video
6. ✅ **IModelLoader** - Model download and management
7. ✅ **IModelConfiguration** - Configuration management

## 📁 File Structure

```
CSharp/
├── Interfaces/
│   ├── ISpeechRecognitionClient.cs       # ASR interface
│   ├── ITextGenerationClient.cs           # LLM interface
│   ├── IVisionLanguageClient.cs           # Vision-language interface
│   ├── IImageGenerationClient.cs          # Image generation interface
│   ├── IVideoGenerationClient.cs          # Video synthesis interface
│   ├── IModelLoader.cs                    # Model management interfaces
│   ├── MODEL_INTERFACES.md                # Complete API documentation
│   └── README_MODEL_INTERFACES.md         # Quick start guide
│
└── Examples/
    └── ModelClients/
        ├── FasterWhisperClientExample.cs  # Example implementation
        └── README.md                       # Implementation approaches guide
```

## 🚀 Quick Start

### 1. Review the Interfaces

Start by reading the interface definitions:

```bash
# Read the main documentation
cat CSharp/Interfaces/MODEL_INTERFACES.md

# Review quick start guide
cat CSharp/Interfaces/README_MODEL_INTERFACES.md

# Check example implementation
cat CSharp/Examples/ModelClients/FasterWhisperClientExample.cs
```

### 2. Choose Implementation Approach

Four main approaches are available:

#### A. Process-Based Python Interop (Easiest)
- ✅ Simple to implement
- ✅ Uses existing Python ecosystem
- ✅ Good for development/prototyping
- See: `FasterWhisperClientExample.cs`

#### B. Python.NET (Recommended)
- ✅ Direct Python integration
- ✅ Better performance
- ✅ Production-ready
- Requires: Python.Runtime.NETStandard package

#### C. gRPC Service (Best for Scale)
- ✅ Language-agnostic
- ✅ Scalable architecture
- ✅ Can run on separate machines
- Requires: Server infrastructure

#### D. ONNX Runtime (Native C#)
- ✅ No Python dependency
- ✅ Cross-platform
- ✅ High performance
- Requires: Model conversion to ONNX

### 3. Set Up Python Environment

For Python-based approaches (A, B, C):

```bash
# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install faster-whisper transformers diffusers torch

# For specific models
pip install transformers[torch]  # For Qwen/Llama
pip install diffusers[torch]     # For SDXL
```

### 4. Set Up .NET Environment

```bash
# Install .NET 8.0 SDK (if not already installed)
# https://dotnet.microsoft.com/download

# Add NuGet packages (if using Python.NET or gRPC)
dotnet add package Python.Runtime.NETStandard  # For Python.NET
dotnet add package Grpc.Net.Client             # For gRPC
```

## 📖 Implementation Steps

### Step 1: Implement ISpeechRecognitionClient

**Using Process-Based Approach** (Easiest to start):

1. Create Python script:
```bash
mkdir -p scripts
# Copy template from FasterWhisperClientExample.PythonScriptTemplate
```

2. Create C# implementation:
```csharp
public class FasterWhisperClient : ISpeechRecognitionClient
{
    // Use FasterWhisperClientExample as reference
}
```

3. Test:
```csharp
var client = new FasterWhisperClient();
var result = await client.TranscribeAsync("test.mp3");
Assert.NotNull(result.Text);
```

**Using Python.NET** (Better performance):

```csharp
using Python.Runtime;

public class FasterWhisperPythonNetClient : ISpeechRecognitionClient
{
    private dynamic _model;

    public void Initialize()
    {
        PythonEngine.Initialize();
        using (Py.GIL())
        {
            dynamic whisper = Py.Import("faster_whisper");
            _model = whisper.WhisperModel("large-v3", device: "cuda");
        }
    }

    public async Task<TranscriptionResult> TranscribeAsync(...)
    {
        return await Task.Run(() =>
        {
            using (Py.GIL())
            {
                dynamic segments = _model.transcribe(audioPath);
                return ConvertToTranscriptionResult(segments);
            }
        });
    }
}
```

### Step 2: Implement ITextGenerationClient

**Using transformers library**:

1. Create Python service script:
```python
# scripts/text_generation_service.py
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-14B-Instruct",
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-14B-Instruct")

# Implement generate, chat, stream methods
```

2. Create C# client to call the script

### Step 3: Implement IVisionLanguageClient

Similar approach using LLaVA or Phi-3.5-vision:

```python
# scripts/vision_language_service.py
from transformers import LlavaOnevisionForConditionalGeneration, AutoProcessor

model = LlavaOnevisionForConditionalGeneration.from_pretrained(
    "llava-hf/llava-onevision-qwen2-7b-ov-hf"
)
processor = AutoProcessor.from_pretrained(...)

# Implement analyze_image, validate_scene, check_consistency
```

### Step 4: Implement IImageGenerationClient

Using Stable Diffusion XL:

```python
# scripts/image_generation_service.py
from diffusers import StableDiffusionXLPipeline

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0"
)

# Implement generate_image, with_refiner, batch_generate
```

### Step 5: Implement IVideoGenerationClient

Using LTX-Video:

```python
# scripts/video_generation_service.py
from diffusers import LTXPipeline

pipe = LTXPipeline.from_pretrained("Lightricks/LTX-Video")

# Implement generate_video, from_keyframe, transition, sequence
```

### Step 6: Implement IModelLoader

```csharp
public class HuggingFaceModelLoader : IModelLoader
{
    public async Task<string> DownloadModelAsync(
        string modelName,
        string destination,
        Action<double>? progressCallback = null,
        CancellationToken cancellationToken = default)
    {
        // Use huggingface-cli or snapshot_download
        // Call: huggingface-cli download {modelName}
    }

    public async Task<ModelVerificationResult> VerifyModelAsync(string modelPath)
    {
        // Check for required files
        // Verify checksums if available
        // Return verification result
    }
}
```

### Step 7: Implement IModelConfiguration

```csharp
public class JsonModelConfiguration : IModelConfiguration
{
    public async Task<ModelConfig> LoadConfigurationAsync(string configPath)
    {
        var json = await File.ReadAllTextAsync(configPath);
        return JsonSerializer.Deserialize<ModelConfig>(json);
    }

    public ModelConfig GetDefaultConfiguration(string modelType)
    {
        return modelType switch
        {
            "speech-recognition" => new ModelConfig
            {
                ModelType = "speech-recognition",
                Device = "cuda",
                ComputeType = "float16",
                BatchSize = 16
            },
            // ... other model types
        };
    }
}
```

## 🧪 Testing

### Unit Tests

```csharp
public class SpeechRecognitionClientTests
{
    [Fact]
    public async Task TranscribeAsync_WithValidAudio_ReturnsTranscription()
    {
        // Arrange
        var client = new FasterWhisperClient();
        var audioPath = "test-audio.mp3";

        // Act
        var result = await client.TranscribeAsync(audioPath);

        // Assert
        Assert.NotNull(result);
        Assert.NotEmpty(result.Text);
        Assert.NotEmpty(result.Segments);
    }

    [Fact]
    public async Task DetectLanguageAsync_WithEnglishAudio_ReturnsEnglish()
    {
        // Arrange
        var client = new FasterWhisperClient();

        // Act
        var result = await client.DetectLanguageAsync("english-audio.mp3");

        // Assert
        Assert.Equal("en", result.Language);
        Assert.True(result.Confidence > 0.8);
    }
}
```

### Integration Tests

```csharp
public class EndToEndPipelineTests
{
    [Fact]
    public async Task CompleteStoryGeneration_ProducesVideo()
    {
        // Arrange
        var textClient = new QwenTextClient();
        var imageClient = new SDXLImageClient();
        var videoClient = new LTXVideoClient();

        // Act
        var script = await textClient.GenerateAsync("A mysterious story");
        var keyframe = await imageClient.GenerateImageAsync("Dark forest scene");
        var video = await videoClient.GenerateVideoFromKeyframeAsync(
            keyframePath: "keyframe.png",
            prompt: "Pan through mysterious forest"
        );

        // Assert
        Assert.NotNull(video);
        Assert.True(video.Frames.Count > 0);
    }
}
```

## 📦 Dependency Injection Setup

In your `Program.cs` or `Startup.cs`:

```csharp
// Register services
services.AddScoped<ISpeechRecognitionClient, FasterWhisperClient>();
services.AddScoped<ITextGenerationClient, QwenTextClient>();
services.AddScoped<IVisionLanguageClient, LlavaVisionClient>();
services.AddScoped<IImageGenerationClient, SDXLImageClient>();
services.AddScoped<IVideoGenerationClient, LTXVideoClient>();
services.AddSingleton<IModelLoader, HuggingFaceModelLoader>();
services.AddSingleton<IModelConfiguration, JsonModelConfiguration>();

// Configure options
services.Configure<SpeechRecognitionOptions>(
    configuration.GetSection("SpeechRecognition"));
```

## 🔧 Configuration Example

Create `appsettings.json`:

```json
{
  "SpeechRecognition": {
    "ModelName": "large-v3",
    "Device": "cuda",
    "ComputeType": "float16",
    "PythonPath": "python",
    "ScriptPath": "./scripts/faster_whisper_service.py"
  },
  "TextGeneration": {
    "ModelName": "Qwen/Qwen2.5-14B-Instruct",
    "Device": "cuda",
    "ComputeType": "float16",
    "MaxTokens": 2048,
    "Temperature": 0.7
  },
  "ImageGeneration": {
    "ModelName": "stabilityai/stable-diffusion-xl-base-1.0",
    "RefinerModel": "stabilityai/stable-diffusion-xl-refiner-1.0",
    "Device": "cuda",
    "UseRefiner": true,
    "Width": 1024,
    "Height": 1024
  },
  "VideoGeneration": {
    "ModelName": "Lightricks/LTX-Video",
    "Device": "cuda",
    "DefaultFps": 24,
    "DefaultWidth": 768,
    "DefaultHeight": 512
  }
}
```

## 📊 System Requirements

### Minimum Configuration
- **CPU**: 8+ cores
- **RAM**: 32 GB
- **GPU**: NVIDIA RTX 3090 (24GB VRAM)
- **Storage**: 500 GB SSD

### Recommended Configuration
- **CPU**: 16+ cores (AMD Ryzen 9 / Intel i9)
- **RAM**: 64 GB
- **GPU**: NVIDIA RTX 4090 (24GB VRAM) or A100 (40GB/80GB)
- **Storage**: 1 TB NVMe SSD

### Per-Model VRAM Requirements

| Model | VRAM (float16) | VRAM (int8) | VRAM (int4) |
|-------|---------------|-------------|-------------|
| faster-whisper-large-v3 | 5 GB | - | - |
| Qwen2.5-14B-Instruct | 28 GB | 14 GB | 7 GB |
| Llama-3.1-8B-Instruct | 16 GB | 8 GB | 4 GB |
| LLaVA-OneVision-7B | 14 GB | - | - |
| Phi-3.5-vision | 8 GB | 4 GB | - |
| SDXL Base | 12 GB | - | - |
| SDXL + Refiner | 16 GB | - | - |
| LTX-Video | 24 GB | - | - |

## 🐛 Troubleshooting

### Python Module Not Found

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Install missing modules
pip install faster-whisper transformers diffusers
```

### CUDA Out of Memory

```python
# Use quantization
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_8bit=True,  # or load_in_4bit=True
    device_map="auto"
)
```

### Process Timeout

```csharp
// Increase timeout for long operations
var cts = new CancellationTokenSource(TimeSpan.FromMinutes(10));
var result = await client.GenerateAsync(prompt, cancellationToken: cts.Token);
```

## 📚 Additional Resources

- **Main Documentation**: [MODEL_INTERFACES.md](MODEL_INTERFACES.md)
- **Quick Start**: [README_MODEL_INTERFACES.md](README_MODEL_INTERFACES.md)
- **Example Code**: [Examples/ModelClients/](../Examples/ModelClients/)
- **Model Details**: [../../docs/MODELS.md](../../docs/MODELS.md)

## 🎯 Next Steps

1. ✅ Interfaces defined - **COMPLETE**
2. ⏳ Choose implementation approach - **IN PROGRESS**
3. ⏳ Implement speech recognition client
4. ⏳ Implement text generation client
5. ⏳ Implement vision-language client
6. ⏳ Implement image generation client
7. ⏳ Implement video generation client
8. ⏳ Implement model loader
9. ⏳ Write unit tests
10. ⏳ Write integration tests
11. ⏳ Deploy and test end-to-end

## 🤝 Contributing

When implementing:

1. Follow interface contracts exactly
2. Add comprehensive error handling
3. Include XML documentation
4. Write unit tests
5. Add integration tests
6. Document VRAM requirements
7. Provide configuration examples

---

**Created**: 2024-12-19  
**Status**: ✅ Interfaces Complete, Ready for Implementation  
**Issue Reference**: Environment & Model Setup
