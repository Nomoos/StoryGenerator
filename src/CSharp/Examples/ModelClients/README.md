# Model Client Examples

This directory contains example implementations of the model interfaces defined in `../Interfaces/`. These examples demonstrate different approaches to integrating AI models with C#.

## 📁 Contents

### FasterWhisperClientExample.cs

Example implementation of `ISpeechRecognitionClient` that shows how to:
- Call Python's faster-whisper library from C#
- Execute Python scripts via process
- Parse JSON responses
- Handle async operations and cancellation

**Implementation Approach**: Process-based Python interop

**Key Features**:
- Simple to understand and debug
- No additional dependencies
- Works with existing Python ecosystem
- Includes Python script template

**Usage**:

```csharp
var client = new FasterWhisperClientExample(
    pythonPath: "python",
    scriptPath: "./scripts/faster_whisper_service.py",
    modelName: "large-v3"
);

var result = await client.TranscribeAsync(
    "/path/to/audio.mp3",
    language: "en",
    wordTimestamps: true
);

Console.WriteLine($"Transcription: {result.Text}");
```

## 🔧 Implementation Approaches

### 1. Process-Based (Current Example)

**Pros**:
- ✅ Simple implementation
- ✅ Language agnostic
- ✅ Easy to debug
- ✅ Uses existing Python tools

**Cons**:
- ❌ Process overhead
- ❌ JSON serialization cost
- ❌ No direct memory sharing

**Best For**: Development, prototyping, simple use cases

### 2. Python.NET (Recommended for Production)

**Pros**:
- ✅ Direct Python integration
- ✅ Minimal overhead
- ✅ Access to all Python features
- ✅ Better error handling

**Cons**:
- ❌ Requires Python.NET package
- ❌ More complex setup
- ❌ Python runtime dependency

**Example**:

```csharp
using Python.Runtime;

public class FasterWhisperPythonNet : ISpeechRecognitionClient
{
    private dynamic _whisper;
    private dynamic _model;

    public void Initialize()
    {
        PythonEngine.Initialize();
        _whisper = Py.Import("faster_whisper");
        _model = _whisper.WhisperModel("large-v3", device: "cuda");
    }

    public async Task<TranscriptionResult> TranscribeAsync(string audioPath, ...)
    {
        using (Py.GIL())
        {
            dynamic segments = _model.transcribe(audioPath);
            // Convert Python objects to C# objects
        }
    }
}
```

### 3. gRPC Service (Best for Scaling)

**Pros**:
- ✅ Scalable architecture
- ✅ Language agnostic
- ✅ Can run on separate machines
- ✅ Load balancing support

**Cons**:
- ❌ More infrastructure
- ❌ Network latency
- ❌ More complex deployment

**Architecture**:

```
┌─────────────┐           ┌──────────────┐
│   C# App    │  gRPC     │ Python Server│
│             │ ────────> │              │
│ (Client)    │           │ (Models)     │
└─────────────┘           └──────────────┘
```

### 4. ONNX Runtime (Native C#)

**Pros**:
- ✅ No Python dependency
- ✅ Cross-platform
- ✅ High performance
- ✅ Direct .NET integration

**Cons**:
- ❌ Requires model conversion
- ❌ Not all models supported
- ❌ May lose features

**Example**:

```csharp
using Microsoft.ML.OnnxRuntime;

public class WhisperOnnxClient : ISpeechRecognitionClient
{
    private InferenceSession _session;

    public void Initialize()
    {
        _session = new InferenceSession("whisper-large-v3.onnx");
    }

    public async Task<TranscriptionResult> TranscribeAsync(string audioPath, ...)
    {
        // Preprocess audio
        var inputs = PreprocessAudio(audioPath);
        
        // Run inference
        var outputs = _session.Run(inputs);
        
        // Post-process results
        return ParseOutput(outputs);
    }
}
```

## 📋 Creating Your Own Implementation

### Step 1: Choose Your Approach

Consider:
- Development vs. production
- Performance requirements
- Deployment complexity
- Team expertise

### Step 2: Implement the Interface

```csharp
public class MyCustomClient : ISpeechRecognitionClient
{
    // Implement all interface methods
    public async Task<TranscriptionResult> TranscribeAsync(...)
    {
        // Your implementation
    }
    
    // ... other methods
}
```

### Step 3: Add Configuration

```csharp
public class MyCustomClient : ISpeechRecognitionClient
{
    private readonly MyClientConfig _config;
    
    public MyCustomClient(MyClientConfig config)
    {
        _config = config;
    }
}
```

### Step 4: Register with DI

```csharp
services.AddScoped<ISpeechRecognitionClient, MyCustomClient>();
services.Configure<MyClientConfig>(configuration.GetSection("SpeechRecognition"));
```

### Step 5: Add Unit Tests

```csharp
[Fact]
public async Task TranscribeAsync_WithValidAudio_ReturnsTranscription()
{
    var client = new MyCustomClient(config);
    var result = await client.TranscribeAsync("test.mp3");
    Assert.NotNull(result.Text);
}
```

## 🧪 Testing Examples

### Mock for Unit Tests

```csharp
var mockClient = new Mock<ISpeechRecognitionClient>();
mockClient
    .Setup(x => x.TranscribeAsync(
        It.IsAny<string>(),
        It.IsAny<string>(),
        It.IsAny<int>(),
        It.IsAny<bool>(),
        It.IsAny<CancellationToken>()))
    .ReturnsAsync(new TranscriptionResult
    {
        Text = "Test transcription",
        Language = "en"
    });
```

### Integration Test

```csharp
[Fact]
public async Task EndToEnd_TranscriptionPipeline()
{
    // Arrange
    var client = new FasterWhisperClientExample();
    var audioPath = "test-audio.mp3";
    
    // Act
    var result = await client.TranscribeAsync(audioPath);
    
    // Assert
    Assert.NotEmpty(result.Text);
    Assert.NotEmpty(result.Segments);
}
```

## 🚀 Getting Started

### 1. For Process-Based Approach

```bash
# Install Python dependencies
pip install faster-whisper

# Copy the Python script template
cat > scripts/faster_whisper_service.py << 'EOF'
# (Use the template from FasterWhisperClientExample.PythonScriptTemplate)
EOF

# Make it executable
chmod +x scripts/faster_whisper_service.py

# Test it
python scripts/faster_whisper_service.py transcribe audio.mp3 --model large-v3
```

### 2. For Python.NET Approach

```bash
# Install Python.NET
dotnet add package Python.Runtime.NETStandard

# Install Python dependencies
pip install faster-whisper
```

### 3. For gRPC Approach

```bash
# Install gRPC tools
dotnet add package Grpc.Net.Client
dotnet add package Google.Protobuf
dotnet add package Grpc.Tools

# Define proto file
cat > protos/speech_recognition.proto << 'EOF'
syntax = "proto3";

service SpeechRecognition {
  rpc Transcribe (TranscribeRequest) returns (TranscribeResponse);
}
EOF
```

## 📚 Additional Resources

- **Python.NET**: https://github.com/pythonnet/pythonnet
- **ONNX Runtime**: https://onnxruntime.ai/
- **gRPC .NET**: https://grpc.io/docs/languages/csharp/
- **TorchSharp**: https://github.com/dotnet/TorchSharp

## 🤝 Contributing

When adding new examples:

1. Follow the interface contract exactly
2. Include comprehensive XML documentation
3. Add error handling and logging
4. Include configuration examples
5. Provide Python/script templates if needed
6. Add unit tests

## 📝 Next Steps

To implement other interfaces:

1. **ITextGenerationClient** - Use transformers library or Ollama API
2. **IVisionLanguageClient** - Use LLaVA or Phi-3.5-vision
3. **IImageGenerationClient** - Use diffusers library (SDXL)
4. **IVideoGenerationClient** - Use LTX-Video or SVD
5. **IModelLoader** - Use Hugging Face Hub API

See [../Interfaces/MODEL_INTERFACES.md](../Interfaces/MODEL_INTERFACES.md) for complete documentation.

---

**Created**: 2024-12-19  
**Last Updated**: 2024-12-19
