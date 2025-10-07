# AI Model Interfaces for C#

This document provides comprehensive documentation for the C# interfaces designed to integrate AI models for the StoryGenerator pipeline. These interfaces define contracts for speech recognition, text generation, vision-language understanding, image generation, video synthesis, and model management.

## 📋 Table of Contents

- [Overview](#overview)
- [Interface Descriptions](#interface-descriptions)
  - [ISpeechRecognitionClient](#ispeechrecognitionclient)
  - [ITextGenerationClient](#itextgenerationclient)
  - [IVisionLanguageClient](#ivisionlanguageclient)
  - [IImageGenerationClient](#iimagegenerationclient)
  - [IVideoGenerationClient](#ivideogenerationclient)
  - [IModelLoader](#imodelloader)
  - [IModelConfiguration](#imodelconfiguration)
- [Usage Examples](#usage-examples)
- [Model Requirements](#model-requirements)
- [Integration Guide](#integration-guide)

---

## Overview

These interfaces provide a unified, type-safe way to interact with various AI models in C#. They support:

- ✅ **Async/await** patterns for non-blocking operations
- ✅ **CancellationToken** support for long-running operations
- ✅ **Strongly-typed** return values and parameters
- ✅ **Dependency Injection** ready design
- ✅ **Comprehensive** model information and metadata
- ✅ **Flexible** configuration and optimization options

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Model Management Layer                      │
│  ┌──────────────────┐         ┌─────────────────────┐          │
│  │  IModelLoader    │         │ IModelConfiguration │          │
│  │  - Download      │         │  - Load/Save Config │          │
│  │  - Verify        │         │  - Validate         │          │
│  │  - Load/Unload   │         │  - Defaults         │          │
│  └──────────────────┘         └─────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ manages
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Inference Clients                          │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │ISpeechRecognition    │  │ITextGeneration       │            │
│  │  - Transcribe        │  │  - Generate          │            │
│  │  - Generate SRT      │  │  - Chat              │            │
│  │  - Detect Language   │  │  - Stream            │            │
│  └──────────────────────┘  └──────────────────────┘            │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │IVisionLanguage       │  │IImageGeneration      │            │
│  │  - Analyze Image     │  │  - Generate Image    │            │
│  │  - Validate Scene    │  │  - With Refiner      │            │
│  │  - Check Consistency │  │  - Batch Generation  │            │
│  └──────────────────────┘  └──────────────────────┘            │
│  ┌──────────────────────┐                                       │
│  │IVideoGeneration      │                                       │
│  │  - Generate Video    │                                       │
│  │  - From Keyframes    │                                       │
│  │  - Transitions       │                                       │
│  └──────────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Interface Descriptions

### ISpeechRecognitionClient

**Purpose**: Automatic speech recognition and subtitle generation using faster-whisper or similar models.

**Recommended Model**: [Systran/faster-whisper-large-v3](https://huggingface.co/Systran/faster-whisper-large-v3)

**Key Features**:
- Word-level timestamp alignment (±50ms accuracy)
- Multi-language support with auto-detection
- SRT subtitle generation
- 4x faster than original Whisper
- 50% less VRAM usage

**Key Methods**:

```csharp
// Transcribe audio with word-level timestamps
Task<TranscriptionResult> TranscribeAsync(
    string audioPath,
    string? language = null,
    int beamSize = 5,
    bool wordTimestamps = true,
    CancellationToken cancellationToken = default);

// Generate SRT subtitle file
Task<string> TranscribeToSrtAsync(
    string audioPath,
    string outputPath,
    string? language = null,
    int maxWordsPerLine = 10,
    CancellationToken cancellationToken = default);

// Detect audio language
Task<LanguageDetectionResult> DetectLanguageAsync(
    string audioPath,
    CancellationToken cancellationToken = default);
```

**Usage Example**:

```csharp
var speechClient = serviceProvider.GetRequiredService<ISpeechRecognitionClient>();

// Transcribe audio
var result = await speechClient.TranscribeAsync(
    "/path/to/audio.mp3",
    language: "en",
    wordTimestamps: true
);

Console.WriteLine($"Transcribed: {result.Text}");
Console.WriteLine($"Language: {result.Language} (confidence: {result.LanguageConfidence:P0})");

foreach (var segment in result.Segments)
{
    Console.WriteLine($"[{segment.Start:F2}s - {segment.End:F2}s]: {segment.Text}");
}

// Generate SRT subtitles
var srtPath = await speechClient.TranscribeToSrtAsync(
    "/path/to/audio.mp3",
    "/path/to/output.srt"
);
```

---

### ITextGenerationClient

**Purpose**: Text generation using large language models for script creation and content generation.

**Recommended Models**:
- [Qwen/Qwen2.5-14B-Instruct](https://huggingface.co/Qwen/Qwen2.5-14B-Instruct) - 32K context, strong instruction following
- [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) - 128K context, lower VRAM

**Key Features**:
- Completion and chat formats
- Streaming support for real-time output
- Long context support (32K-128K tokens)
- Temperature and top-p sampling control

**Key Methods**:

```csharp
// Simple text generation
Task<TextGenerationResult> GenerateAsync(
    string prompt,
    int maxTokens = 1024,
    double temperature = 0.7,
    double topP = 0.9,
    List<string>? stopSequences = null,
    CancellationToken cancellationToken = default);

// Chat-style generation
Task<TextGenerationResult> ChatAsync(
    List<ChatMessage> messages,
    int maxTokens = 1024,
    double temperature = 0.7,
    double topP = 0.9,
    CancellationToken cancellationToken = default);

// Streaming generation
IAsyncEnumerable<string> GenerateStreamAsync(
    string prompt,
    int maxTokens = 1024,
    double temperature = 0.7,
    CancellationToken cancellationToken = default);
```

**Usage Example**:

```csharp
var textClient = serviceProvider.GetRequiredService<ITextGenerationClient>();

// Chat-style generation
var messages = new List<ChatMessage>
{
    ChatMessage.System("You are a creative scriptwriter for short-form videos."),
    ChatMessage.User("Write a 60-second script about the history of coffee.")
};

var result = await textClient.ChatAsync(messages, maxTokens: 500, temperature: 0.9);

Console.WriteLine(result.Text);
Console.WriteLine($"Generated {result.TokensGenerated} tokens in {result.GenerationTimeMs}ms");
Console.WriteLine($"Speed: {result.TokensPerSecond:F1} tokens/sec");

// Streaming generation
await foreach (var chunk in textClient.GenerateStreamAsync(
    "Write a mysterious opening line:", 
    maxTokens: 100))
{
    Console.Write(chunk);
}
```

---

### IVisionLanguageClient

**Purpose**: Image understanding and scene validation using vision-language models.

**Recommended Models**:
- [LLaVA-OneVision](https://huggingface.co/docs/transformers/en/model_doc/llava_onevision) - Unified image/video understanding
- [microsoft/Phi-3.5-vision-instruct](https://huggingface.co/microsoft/Phi-3.5-vision-instruct) - Lightweight alternative

**Key Features**:
- Image analysis and description
- Multi-image support for consistency checking
- Scene validation against descriptions
- Visual consistency analysis across keyframes

**Key Methods**:

```csharp
// Analyze a single image
Task<VisionLanguageResult> AnalyzeImageAsync(
    string imagePath,
    string prompt,
    int maxTokens = 512,
    double temperature = 0.7,
    CancellationToken cancellationToken = default);

// Validate scene matches description
Task<SceneValidationResult> ValidateSceneAsync(
    string imagePath,
    string sceneDescription,
    CancellationToken cancellationToken = default);

// Check consistency across keyframes
Task<ConsistencyAnalysisResult> CheckConsistencyAsync(
    List<string> keyframePaths,
    CancellationToken cancellationToken = default);
```

**Usage Example**:

```csharp
var visionClient = serviceProvider.GetRequiredService<IVisionLanguageClient>();

// Analyze image
var analysis = await visionClient.AnalyzeImageAsync(
    "/path/to/keyframe.png",
    "Describe this scene in detail, including mood and atmosphere."
);
Console.WriteLine($"Analysis: {analysis.Text}");

// Validate scene
var validation = await visionClient.ValidateSceneAsync(
    "/path/to/keyframe.png",
    "A dark, mysterious forest at twilight with fog"
);

Console.WriteLine($"Valid: {validation.IsValid} (score: {validation.MatchScore:P0})");
Console.WriteLine($"Explanation: {validation.Explanation}");

if (!validation.IsValid)
{
    Console.WriteLine("Mismatched elements:");
    foreach (var element in validation.MismatchedElements)
    {
        Console.WriteLine($"  - {element}");
    }
}

// Check consistency across multiple keyframes
var keyframes = new List<string> 
{ 
    "/path/to/keyframe1.png", 
    "/path/to/keyframe2.png", 
    "/path/to/keyframe3.png" 
};

var consistency = await visionClient.CheckConsistencyAsync(keyframes);
Console.WriteLine($"Consistency score: {consistency.ConsistencyScore:P0}");
Console.WriteLine($"Analysis: {consistency.Analysis}");
```

---

### IImageGenerationClient

**Purpose**: High-quality image generation using Stable Diffusion XL.

**Recommended Model**: [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)

**Key Features**:
- Native 1024x1024 resolution
- Optional refiner for enhanced quality
- Batch generation for variety
- LoRA support for style transfer
- Reproducible results with seeds

**Key Methods**:

```csharp
// Generate single image
Task<ImageGenerationResult> GenerateImageAsync(
    string prompt,
    string? negativePrompt = null,
    int width = 1024,
    int height = 1024,
    int numInferenceSteps = 30,
    double guidanceScale = 7.5,
    int? seed = null,
    CancellationToken cancellationToken = default);

// Generate with refiner for higher quality
Task<ImageGenerationResult> GenerateImageWithRefinerAsync(
    string prompt,
    string? negativePrompt = null,
    int width = 1024,
    int height = 1024,
    int baseSteps = 40,
    int refinerSteps = 20,
    double guidanceScale = 7.5,
    int? seed = null,
    CancellationToken cancellationToken = default);

// Generate multiple variations
Task<List<ImageGenerationResult>> GenerateImageBatchAsync(
    string prompt,
    string? negativePrompt = null,
    int count = 4,
    int width = 1024,
    int height = 1024,
    int numInferenceSteps = 30,
    double guidanceScale = 7.5,
    CancellationToken cancellationToken = default);
```

**Usage Example**:

```csharp
var imageClient = serviceProvider.GetRequiredService<IImageGenerationClient>();

// Generate keyframe image
var result = await imageClient.GenerateImageAsync(
    prompt: "A mysterious dark forest at twilight, cinematic lighting, atmospheric fog, 4k quality",
    negativePrompt: "blurry, low quality, distorted, ugly",
    width: 1024,
    height: 1024,
    numInferenceSteps: 30,
    guidanceScale: 7.5,
    seed: 42 // For reproducibility
);

// Save the image
var imagePath = await imageClient.SaveImageAsync(result, "/path/to/output.png");
Console.WriteLine($"Generated image saved to: {imagePath}");
Console.WriteLine($"Generation took {result.GenerationTimeMs}ms");

// Generate with refiner for higher quality
var refinedResult = await imageClient.GenerateImageWithRefinerAsync(
    prompt: "High quality portrait of a wise old wizard, detailed, 8k",
    width: 1024,
    height: 1024,
    baseSteps: 40,
    refinerSteps: 20
);

// Generate batch for variety
var batch = await imageClient.GenerateImageBatchAsync(
    prompt: "Scenic landscape at sunset",
    count: 4
);

for (int i = 0; i < batch.Count; i++)
{
    await imageClient.SaveImageAsync(batch[i], $"/path/to/variation_{i}.png");
}
```

---

### IVideoGenerationClient

**Purpose**: Video generation and synthesis using LTX-Video or similar models.

**Recommended Model**: [Lightricks/LTX-Video](https://huggingface.co/Lightricks/LTX-Video)

**Key Features**:
- Text-to-video generation
- Image-to-video (keyframe animation)
- Keyframe interpolation for transitions
- Multi-scene sequence generation
- Motion hints and camera controls

**Key Methods**:

```csharp
// Generate video from text
Task<VideoGenerationResult> GenerateVideoAsync(
    string prompt,
    int numFrames = 121,
    int fps = 24,
    int width = 768,
    int height = 512,
    int numInferenceSteps = 50,
    double guidanceScale = 7.5,
    int? seed = null,
    CancellationToken cancellationToken = default);

// Generate video from keyframe
Task<VideoGenerationResult> GenerateVideoFromKeyframeAsync(
    string keyframePath,
    string prompt,
    int numFrames = 121,
    int fps = 24,
    int numInferenceSteps = 50,
    double guidanceScale = 7.5,
    int? seed = null,
    CancellationToken cancellationToken = default);

// Generate transition between keyframes
Task<VideoGenerationResult> GenerateVideoTransitionAsync(
    string startKeyframePath,
    string endKeyframePath,
    string prompt,
    int numFrames = 121,
    int fps = 24,
    CancellationToken cancellationToken = default);

// Generate complete video sequence
Task<VideoGenerationResult> GenerateVideoSequenceAsync(
    List<VideoScene> scenes,
    int fps = 24,
    int transitionFrames = 24,
    CancellationToken cancellationToken = default);
```

**Usage Example**:

```csharp
var videoClient = serviceProvider.GetRequiredService<IVideoGenerationClient>();

// Generate video from keyframe
var result = await videoClient.GenerateVideoFromKeyframeAsync(
    keyframePath: "/path/to/keyframe.png",
    prompt: "Camera slowly pans across a mysterious forest at twilight",
    numFrames: 121, // 5 seconds at 24fps
    fps: 24
);

// Save video with audio
var videoPath = await videoClient.SaveVideoAsync(
    result,
    "/path/to/output.mp4",
    audioPath: "/path/to/narration.mp3"
);

Console.WriteLine($"Video saved to: {videoPath}");
Console.WriteLine($"Duration: {result.DurationSeconds:F1}s");
Console.WriteLine($"Resolution: {result.Width}x{result.Height}");
Console.WriteLine($"Generation took {result.GenerationTimeMs / 1000.0:F1}s");

// Generate multi-scene sequence
var scenes = new List<VideoScene>
{
    new VideoScene
    {
        SceneNumber = 1,
        Description = "Opening shot of forest",
        KeyframePath = "/path/to/keyframe1.png",
        DurationFrames = 72, // 3 seconds
        MotionHint = "slow zoom in"
    },
    new VideoScene
    {
        SceneNumber = 2,
        Description = "Close-up of mysterious artifact",
        KeyframePath = "/path/to/keyframe2.png",
        DurationFrames = 96, // 4 seconds
        MotionHint = "rotate camera"
    }
};

var sequence = await videoClient.GenerateVideoSequenceAsync(
    scenes,
    fps: 24,
    transitionFrames: 24 // 1 second transitions
);
```

---

### IModelLoader

**Purpose**: Download, verify, and load AI models.

**Key Features**:
- Download models from Hugging Face
- Verify model integrity
- Load/unload models from memory
- Manage model cache
- Progress tracking

**Key Methods**:

```csharp
// Download model
Task<string> DownloadModelAsync(
    string modelName,
    string destination,
    Action<double>? progressCallback = null,
    CancellationToken cancellationToken = default);

// Verify model integrity
Task<ModelVerificationResult> VerifyModelAsync(string modelPath);

// Load model into memory
Task<string> LoadModelAsync(
    string modelPath,
    string device = "auto",
    string computeType = "auto",
    CancellationToken cancellationToken = default);

// List cached models
Task<List<CachedModelInfo>> ListCachedModelsAsync();
```

**Usage Example**:

```csharp
var modelLoader = serviceProvider.GetRequiredService<IModelLoader>();

// Download model with progress tracking
var modelPath = await modelLoader.DownloadModelAsync(
    "Systran/faster-whisper-large-v3",
    "/path/to/models",
    progressCallback: progress => Console.WriteLine($"Download progress: {progress:P0}")
);

// Verify model
var verification = await modelLoader.VerifyModelAsync(modelPath);
if (!verification.IsValid)
{
    Console.WriteLine($"Model verification failed: {verification.Message}");
    return;
}

Console.WriteLine($"Model size: {verification.SizeBytes / 1024.0 / 1024.0:F1} MB");

// Load model
var modelHandle = await modelLoader.LoadModelAsync(
    modelPath,
    device: "cuda",
    computeType: "float16"
);

Console.WriteLine($"Model loaded with handle: {modelHandle}");

// List all cached models
var cachedModels = await modelLoader.ListCachedModelsAsync();
foreach (var model in cachedModels)
{
    Console.WriteLine($"{model.ModelName}: {model.SizeBytes / 1024.0 / 1024.0:F1} MB");
    Console.WriteLine($"  Downloaded: {model.DownloadedAt}");
    Console.WriteLine($"  Last accessed: {model.LastAccessedAt}");
}
```

---

### IModelConfiguration

**Purpose**: Manage model configurations and settings.

**Key Features**:
- Load/save configurations
- Default configurations per model type
- Configuration validation
- VRAM estimation
- Hardware-based recommendations

**Key Methods**:

```csharp
// Load configuration
Task<ModelConfig> LoadConfigurationAsync(string configPath);

// Save configuration
Task<bool> SaveConfigurationAsync(ModelConfig config, string configPath);

// Get default configuration
ModelConfig GetDefaultConfiguration(string modelType);

// Validate configuration
Task<ConfigurationValidationResult> ValidateConfigurationAsync(ModelConfig config);
```

**Usage Example**:

```csharp
var configManager = serviceProvider.GetRequiredService<IModelConfiguration>();

// Get default configuration
var config = configManager.GetDefaultConfiguration("speech-recognition");
config.ModelName = "Systran/faster-whisper-large-v3";
config.Device = "cuda";
config.ComputeType = "float16";
config.BatchSize = 16;

// Validate configuration
var validation = await configManager.ValidateConfigurationAsync(config);

if (!validation.IsValid)
{
    Console.WriteLine("Configuration errors:");
    foreach (var error in validation.Errors)
    {
        Console.WriteLine($"  - {error}");
    }
}

if (validation.Warnings.Any())
{
    Console.WriteLine("Warnings:");
    foreach (var warning in validation.Warnings)
    {
        Console.WriteLine($"  - {warning}");
    }
}

Console.WriteLine($"Estimated VRAM usage: {validation.EstimatedVRAMGB:F1} GB");

if (validation.Recommendations.Any())
{
    Console.WriteLine("Recommendations:");
    foreach (var kvp in validation.Recommendations)
    {
        Console.WriteLine($"  {kvp.Key}: {kvp.Value}");
    }
}

// Save configuration
await configManager.SaveConfigurationAsync(config, "/path/to/config.json");
```

---

## Model Requirements

### System Requirements by Model

#### Speech Recognition (faster-whisper-large-v3)
- **VRAM**: ~5 GB (float16)
- **GPU**: NVIDIA RTX 3060 or better
- **CPU**: 4+ cores recommended
- **RAM**: 8 GB minimum

#### Text Generation (Qwen2.5-14B)
- **VRAM**: ~28 GB (float16), ~14 GB (int8), ~7 GB (int4)
- **GPU**: NVIDIA RTX 3090/4090 or better
- **CPU**: 8+ cores recommended
- **RAM**: 16 GB minimum

#### Text Generation (Llama-3.1-8B)
- **VRAM**: ~16 GB (float16), ~8 GB (int8), ~4 GB (int4)
- **GPU**: NVIDIA RTX 3060 Ti or better
- **CPU**: 4+ cores recommended
- **RAM**: 16 GB minimum

#### Vision-Language (LLaVA-OneVision 7B)
- **VRAM**: ~14 GB (float16)
- **GPU**: NVIDIA RTX 3090 or better
- **CPU**: 8+ cores recommended
- **RAM**: 16 GB minimum

#### Vision-Language (Phi-3.5-vision)
- **VRAM**: ~8 GB (float16), ~4 GB (int8)
- **GPU**: NVIDIA RTX 3060 or better
- **CPU**: 4+ cores recommended
- **RAM**: 8 GB minimum

#### Image Generation (SDXL Base)
- **VRAM**: ~12 GB (float16)
- **GPU**: NVIDIA RTX 3090 or better
- **CPU**: 4+ cores recommended
- **RAM**: 16 GB minimum

#### Image Generation (SDXL + Refiner)
- **VRAM**: ~16 GB (float16)
- **GPU**: NVIDIA RTX 3090 or better
- **CPU**: 8+ cores recommended
- **RAM**: 16 GB minimum

#### Video Generation (LTX-Video)
- **VRAM**: ~24 GB (bfloat16)
- **GPU**: NVIDIA RTX 3090/4090 or better
- **CPU**: 8+ cores recommended
- **RAM**: 32 GB minimum
- **Storage**: Fast SSD recommended

---

## Integration Guide

### Dependency Injection Setup

```csharp
// In your Startup.cs or Program.cs
services.AddScoped<ISpeechRecognitionClient, FasterWhisperClient>();
services.AddScoped<ITextGenerationClient, QwenTextClient>();
services.AddScoped<IVisionLanguageClient, LlavaVisionClient>();
services.AddScoped<IImageGenerationClient, SDXLImageClient>();
services.AddScoped<IVideoGenerationClient, LTXVideoClient>();
services.AddSingleton<IModelLoader, HuggingFaceModelLoader>();
services.AddSingleton<IModelConfiguration, JsonModelConfiguration>();
```

### Complete Pipeline Example

```csharp
public class StoryGenerationPipeline
{
    private readonly ITextGenerationClient _textClient;
    private readonly ISpeechRecognitionClient _speechClient;
    private readonly IImageGenerationClient _imageClient;
    private readonly IVideoGenerationClient _videoClient;
    private readonly IVisionLanguageClient _visionClient;

    public StoryGenerationPipeline(
        ITextGenerationClient textClient,
        ISpeechRecognitionClient speechClient,
        IImageGenerationClient imageClient,
        IVideoGenerationClient videoClient,
        IVisionLanguageClient visionClient)
    {
        _textClient = textClient;
        _speechClient = speechClient;
        _imageClient = imageClient;
        _videoClient = videoClient;
        _visionClient = visionClient;
    }

    public async Task<string> GenerateStoryVideoAsync(
        string storyIdea,
        CancellationToken cancellationToken = default)
    {
        // 1. Generate script
        var scriptResult = await _textClient.ChatAsync(
            new List<ChatMessage>
            {
                ChatMessage.System("You are a creative scriptwriter."),
                ChatMessage.User($"Write a 60-second script about: {storyIdea}")
            },
            maxTokens: 500,
            temperature: 0.9,
            cancellationToken: cancellationToken
        );

        // 2. Generate keyframes
        var keyframes = new List<string>();
        var scenePrompts = ExtractSceneDescriptions(scriptResult.Text);
        
        foreach (var scenePrompt in scenePrompts)
        {
            var imageResult = await _imageClient.GenerateImageAsync(
                prompt: scenePrompt,
                negativePrompt: "blurry, low quality",
                cancellationToken: cancellationToken
            );
            
            var keyframePath = $"/path/to/keyframe_{keyframes.Count}.png";
            await _imageClient.SaveImageAsync(imageResult, keyframePath);
            
            // Validate keyframe matches scene
            var validation = await _visionClient.ValidateSceneAsync(
                keyframePath,
                scenePrompt,
                cancellationToken
            );
            
            if (validation.IsValid)
            {
                keyframes.Add(keyframePath);
            }
        }

        // 3. Generate video from keyframes
        var scenes = keyframes.Select((path, i) => new VideoScene
        {
            SceneNumber = i + 1,
            KeyframePath = path,
            Description = scenePrompts[i],
            DurationFrames = 96 // 4 seconds per scene at 24fps
        }).ToList();

        var videoResult = await _videoClient.GenerateVideoSequenceAsync(
            scenes,
            fps: 24,
            transitionFrames: 24,
            cancellationToken: cancellationToken
        );

        // 4. Save final video
        var outputPath = "/path/to/final_video.mp4";
        await _videoClient.SaveVideoAsync(videoResult, outputPath);

        return outputPath;
    }

    private List<string> ExtractSceneDescriptions(string script)
    {
        // Logic to extract visual scene descriptions from script
        // This is a simplified example
        return new List<string>();
    }
}
```

---

## Best Practices

### 1. Error Handling

Always use try-catch blocks and handle cancellation:

```csharp
try
{
    var result = await client.GenerateAsync(prompt, cancellationToken: cts.Token);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Operation was cancelled");
}
catch (Exception ex)
{
    Console.WriteLine($"Error: {ex.Message}");
}
```

### 2. Resource Management

Unload models when not in use:

```csharp
using var scope = serviceProvider.CreateScope();
var client = scope.ServiceProvider.GetRequiredService<ITextGenerationClient>();
// Use client
// Resources automatically cleaned up when scope is disposed
```

### 3. Progress Tracking

Use progress callbacks for long operations:

```csharp
var progress = new Progress<double>(p => 
    Console.WriteLine($"Progress: {p:P0}")
);

await modelLoader.DownloadModelAsync(
    modelName,
    destination,
    progressCallback: progress.Report
);
```

### 4. Batch Processing

Process multiple items efficiently:

```csharp
var tasks = prompts.Select(prompt => 
    imageClient.GenerateImageAsync(prompt)
);
var results = await Task.WhenAll(tasks);
```

---

## Testing

### Unit Testing with Mocks

```csharp
[Fact]
public async Task GenerateScript_ReturnsValidScript()
{
    // Arrange
    var mockClient = new Mock<ITextGenerationClient>();
    mockClient
        .Setup(x => x.ChatAsync(
            It.IsAny<List<ChatMessage>>(),
            It.IsAny<int>(),
            It.IsAny<double>(),
            It.IsAny<double>(),
            It.IsAny<CancellationToken>()))
        .ReturnsAsync(new TextGenerationResult
        {
            Text = "Test script content",
            TokensGenerated = 100,
            GenerationTimeMs = 1000
        });

    var pipeline = new StoryGenerationPipeline(mockClient.Object, /*...*/);

    // Act
    var result = await pipeline.GenerateScriptAsync("Test idea");

    // Assert
    Assert.NotNull(result);
    Assert.Contains("Test script", result);
}
```

---

## License Information

See [docs/MODELS.md](../docs/MODELS.md) for detailed license information for each model.

---

**Last Updated**: 2024-12-19
