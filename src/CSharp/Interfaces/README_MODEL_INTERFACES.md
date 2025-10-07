# C# Model Interfaces Implementation

This directory contains C# interfaces for integrating AI models into the StoryGenerator pipeline. These interfaces provide a clean, type-safe way to interact with various AI models from C# code.

## 🎯 What's Included

### Core Interfaces

1. **ISpeechRecognitionClient** - Speech-to-text transcription
   - Model: faster-whisper-large-v3
   - Features: Word-level timestamps, SRT generation, language detection
   - File: `ISpeechRecognitionClient.cs`

2. **ITextGenerationClient** - Text generation with LLMs
   - Models: Qwen2.5-14B-Instruct, Llama-3.1-8B-Instruct
   - Features: Completion, chat, streaming generation
   - File: `ITextGenerationClient.cs`

3. **IVisionLanguageClient** - Image understanding and analysis
   - Models: LLaVA-OneVision, Phi-3.5-vision
   - Features: Scene validation, consistency checking, image description
   - File: `IVisionLanguageClient.cs`

4. **IImageGenerationClient** - Image generation from text
   - Model: Stable Diffusion XL (base + refiner)
   - Features: Text-to-image, batch generation, LoRA support
   - File: `IImageGenerationClient.cs`

5. **IVideoGenerationClient** - Video synthesis
   - Model: LTX-Video
   - Features: Text-to-video, keyframe animation, transitions
   - File: `IVideoGenerationClient.cs`

6. **IModelLoader** - Model management
   - Features: Download, verify, load/unload models
   - File: `IModelLoader.cs`

7. **IModelConfiguration** - Configuration management
   - Features: Load/save configs, validation, defaults
   - File: `IModelLoader.cs`

## 📚 Documentation

See **[MODEL_INTERFACES.md](MODEL_INTERFACES.md)** for comprehensive documentation including:
- Detailed interface descriptions
- Usage examples
- Model requirements (VRAM, GPU, etc.)
- Integration guide
- Best practices
- Testing examples

## 🚀 Quick Start

### 1. Add to Dependency Injection

```csharp
services.AddScoped<ISpeechRecognitionClient, FasterWhisperClient>();
services.AddScoped<ITextGenerationClient, QwenTextClient>();
services.AddScoped<IVisionLanguageClient, LlavaVisionClient>();
services.AddScoped<IImageGenerationClient, SDXLImageClient>();
services.AddScoped<IVideoGenerationClient, LTXVideoClient>();
services.AddSingleton<IModelLoader, HuggingFaceModelLoader>();
services.AddSingleton<IModelConfiguration, JsonModelConfiguration>();
```

### 2. Use in Your Code

```csharp
public class StoryGenerator
{
    private readonly ITextGenerationClient _textClient;
    private readonly IImageGenerationClient _imageClient;

    public StoryGenerator(
        ITextGenerationClient textClient,
        IImageGenerationClient imageClient)
    {
        _textClient = textClient;
        _imageClient = imageClient;
    }

    public async Task<string> GenerateStoryAsync(string idea)
    {
        // Generate script
        var script = await _textClient.GenerateAsync(
            $"Write a short story about: {idea}",
            maxTokens: 500
        );

        // Generate keyframe
        var image = await _imageClient.GenerateImageAsync(
            "Cinematic scene from the story",
            width: 1024,
            height: 1024
        );

        return script.Text;
    }
}
```

## 🔧 Implementation Status

| Interface | Status | Notes |
|-----------|--------|-------|
| ISpeechRecognitionClient | ✅ Defined | Ready for implementation |
| ITextGenerationClient | ✅ Defined | Ready for implementation |
| IVisionLanguageClient | ✅ Defined | Ready for implementation |
| IImageGenerationClient | ✅ Defined | Ready for implementation |
| IVideoGenerationClient | ✅ Defined | Ready for implementation |
| IModelLoader | ✅ Defined | Ready for implementation |
| IModelConfiguration | ✅ Defined | Ready for implementation |

## 📋 Next Steps

### For Implementation

1. **Choose Implementation Approach**:
   - Option A: Python interop (call Python libraries from C#)
   - Option B: Native C# libraries (TorchSharp, ONNX Runtime)
   - Option C: API-based (REST/gRPC services)

2. **Create Concrete Implementations**:
   ```
   CSharp/Implementations/
   ├── FasterWhisperClient.cs
   ├── QwenTextClient.cs
   ├── LlavaVisionClient.cs
   ├── SDXLImageClient.cs
   └── LTXVideoClient.cs
   ```

3. **Add Unit Tests**:
   ```
   CSharp/Tests/
   ├── SpeechRecognitionTests.cs
   ├── TextGenerationTests.cs
   ├── VisionLanguageTests.cs
   ├── ImageGenerationTests.cs
   └── VideoGenerationTests.cs
   ```

### For Python Interop (Recommended)

Python has the best support for these models. You can use:

1. **Python.NET** - Call Python from C#
   ```csharp
   using Python.Runtime;
   
   dynamic whisper = Py.Import("faster_whisper");
   dynamic model = whisper.WhisperModel("large-v3");
   ```

2. **Process-based** - Run Python scripts
   ```csharp
   var process = Process.Start(new ProcessStartInfo
   {
       FileName = "python",
       Arguments = "transcribe.py audio.mp3",
       RedirectStandardOutput = true
   });
   ```

3. **gRPC Service** - Python server, C# client
   - Most production-ready
   - Best for scaling
   - Clear separation of concerns

### For Native C# (Alternative)

1. **TorchSharp** - PyTorch bindings for .NET
   - https://github.com/dotnet/TorchSharp
   - Good for inference
   - Limited model support

2. **ONNX Runtime** - Cross-platform ML inference
   - https://onnxruntime.ai/
   - Convert models to ONNX format
   - High performance

## 🔗 Related Files

- **[IGenerators.cs](IGenerators.cs)** - Existing generator interfaces (script, voice, subtitle generation)
- **[../Generators/](../Generators/)** - Video synthesis implementations
- **[../../docs/MODELS.md](../../docs/MODELS.md)** - Detailed model documentation

## 📝 Design Principles

These interfaces follow these principles:

1. **Async/Await First** - All I/O operations are async
2. **CancellationToken Support** - All async operations support cancellation
3. **Strongly Typed** - Rich return types with metadata
4. **Dependency Injection Ready** - Interface-based design
5. **Testability** - Easy to mock and test
6. **Extensibility** - Easy to add new implementations

## 🤝 Contributing

When implementing these interfaces:

1. Follow the existing patterns in `IGenerators.cs`
2. Add comprehensive XML documentation
3. Include usage examples in comments
4. Write unit tests with mocks
5. Document VRAM/hardware requirements
6. Add error handling examples

## 📄 License

See individual model licenses in [docs/MODELS.md](../../docs/MODELS.md)

---

**Created**: 2024-12-19  
**Last Updated**: 2024-12-19  
**Status**: ✅ Interfaces Defined, Ready for Implementation
