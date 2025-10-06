# C# Interfaces for Video Synthesis

## Overview

This document describes the C# interfaces designed for the video synthesis system. These interfaces provide a clean abstraction layer, enabling flexible implementation switching, dependency injection, and easier testing.

## Interface Hierarchy

```
IVideoSynthesizer (Core interface)
├── ISceneVideoSynthesizer (Extended for motion control)
└── IKeyframeVideoSynthesizer (Extended for keyframe-based synthesis)

IVideoSynthesisConfig (Configuration interface)
IVideoSynthesisComparator (Comparison interface)
IVideoSynthesizerFactory (Factory interface)
```

## Core Interfaces

### 1. IVideoSynthesizer

**Purpose**: Core interface defining basic video synthesis capabilities

**Key Methods**:
```csharp
Task<bool> GenerateVideoAsync(string prompt, string outputPath, int duration, int? fps = null);
Task<bool> GenerateVideoAsync(string prompt, string outputPath, string keyframePath, int duration, int? fps = null);
```

**Implementations**:
- `LTXVideoSynthesizer`
- `KeyframeVideoSynthesizer`

**Use Cases**:
- Basic video generation from text prompts
- Polymorphic handling of different synthesis methods
- Dependency injection in larger systems

### 2. ISceneVideoSynthesizer

**Purpose**: Extended interface for scene-based video synthesis with motion control

**Extends**: `IVideoSynthesizer`

**Key Methods**:
```csharp
Task<bool> GenerateSceneClipAsync(
    string sceneDescription,
    string motionHint,
    string outputPath,
    string startKeyframe = null,
    string endKeyframe = null,
    double duration = 5.0);
```

**Implementations**:
- `LTXVideoSynthesizer`

**Use Cases**:
- Scene-based video generation with camera movement
- Motion-controlled video synthesis
- Cinematic shot creation

### 3. IKeyframeVideoSynthesizer

**Purpose**: Interface for keyframe-based video synthesis with interpolation

**Extends**: `IVideoSynthesizer`

**Key Methods**:
```csharp
Task<bool> GenerateFromKeyframesAsync(
    List<string> keyframePaths,
    string outputPath,
    double totalDuration,
    string audioPath = null);

Task<bool> GenerateSceneAsync(
    string sceneDescription,
    string outputPath,
    double duration,
    string audioPath = null,
    List<string> stylePrompts = null);
```

**Implementations**:
- `KeyframeVideoSynthesizer`

**Use Cases**:
- High-quality video from keyframe images
- SDXL-based video generation
- Frame interpolation workflows

### 4. IVideoSynthesisConfig

**Purpose**: Configuration interface for video synthesis settings

**Key Properties**:
```csharp
int TargetFps { get; set; }
int Width { get; set; }
int Height { get; set; }
bool Validate();
```

**Implementations**:
- `KeyframeVideoConfig`

**Use Cases**:
- Configurable video synthesis settings
- Validation of configuration parameters
- Extensible configuration system

### 5. IVideoSynthesisComparator

**Purpose**: Interface for comparing different video synthesis approaches

**Key Methods**:
```csharp
Task<Dictionary<string, VideoClip>> CompareApproachesAsync(
    string testPrompt,
    string testKeyframe = null,
    double duration = 10.0,
    string outputDir = null);
```

**Implementations**:
- `VideoSynthesisComparator`

**Use Cases**:
- Automated testing of synthesis methods
- Performance comparison
- Quality evaluation

### 6. IVideoSynthesizerFactory

**Purpose**: Factory interface for creating video synthesizer instances

**Key Methods**:
```csharp
IVideoSynthesizer CreateSynthesizer(VideoSynthesisMethod method, int width, int height, int fps);
ISceneVideoSynthesizer CreateSceneSynthesizer(VideoSynthesisMethod method, int width, int height, int fps);
IKeyframeVideoSynthesizer CreateKeyframeSynthesizer(InterpolationMethod method, KeyframeVideoConfig config);
```

**Implementations**:
- `VideoSynthesizerFactory`

**Use Cases**:
- Centralized creation of synthesizers
- Dependency injection
- Configuration-driven synthesizer selection

## Usage Examples

### Basic Video Generation with Interfaces

```csharp
// Using the interface instead of concrete class
IVideoSynthesizer synthesizer = new LTXVideoSynthesizer(1080, 1920, 30);

await synthesizer.GenerateVideoAsync(
    prompt: "A beautiful sunset over the ocean",
    outputPath: "output/video.mp4",
    duration: 10
);
```

### Factory Pattern for Creating Synthesizers

```csharp
// Create factory
IVideoSynthesizerFactory factory = new VideoSynthesizerFactory();

// Create LTX-Video synthesizer
IVideoSynthesizer ltxSynthesizer = factory.CreateSynthesizer(
    VideoSynthesisMethod.LTXVideo,
    width: 1080,
    height: 1920,
    fps: 30
);

// Create SDXL+RIFE synthesizer
IVideoSynthesizer sdxlSynthesizer = factory.CreateSynthesizer(
    VideoSynthesisMethod.SDXLWithRIFE,
    width: 1080,
    height: 1920,
    fps: 30
);

// Use polymorphically
await ltxSynthesizer.GenerateVideoAsync(prompt, output, 10);
await sdxlSynthesizer.GenerateVideoAsync(prompt, output2, 10);
```

### Scene-Based Synthesis with Motion Control

```csharp
// Create scene synthesizer
ISceneVideoSynthesizer sceneSynthesizer = factory.CreateSceneSynthesizer(
    VideoSynthesisMethod.LTXVideo
);

// Generate with motion control
await sceneSynthesizer.GenerateSceneClipAsync(
    sceneDescription: "City skyline at night",
    motionHint: "camera panning right",
    outputPath: "output/scene.mp4",
    duration: 8.0
);
```

### Keyframe-Based Synthesis

```csharp
// Create keyframe synthesizer
IKeyframeVideoSynthesizer keyframeSynthesizer = factory.CreateKeyframeSynthesizer(
    InterpolationMethod.RIFE
);

// Generate from existing keyframes
var keyframes = new List<string> { "frame1.png", "frame2.png", "frame3.png" };
await keyframeSynthesizer.GenerateFromKeyframesAsync(
    keyframes,
    "output/video.mp4",
    totalDuration: 10.0,
    audioPath: "audio.mp3"
);
```

### Dependency Injection Example

```csharp
// Register in DI container (e.g., ASP.NET Core)
services.AddSingleton<IVideoSynthesizerFactory, VideoSynthesizerFactory>();
services.AddScoped<IVideoSynthesisComparator, VideoSynthesisComparator>();

// Inject and use
public class VideoService
{
    private readonly IVideoSynthesizerFactory _factory;
    
    public VideoService(IVideoSynthesizerFactory factory)
    {
        _factory = factory;
    }
    
    public async Task<bool> GenerateVideo(string prompt, VideoSynthesisMethod method)
    {
        var synthesizer = _factory.CreateSynthesizer(method);
        return await synthesizer.GenerateVideoAsync(prompt, "output.mp4", 10);
    }
}
```

### Configuration-Driven Synthesis

```csharp
// Load configuration
var config = new KeyframeVideoConfig
{
    Method = InterpolationMethod.RIFE,
    TargetFps = 30,
    Width = 1080,
    Height = 1920,
    KeyframesPerScene = 3
};

// Validate configuration
if (!config.Validate())
{
    Console.WriteLine("Invalid configuration");
    return;
}

// Create synthesizer with configuration
IKeyframeVideoSynthesizer synthesizer = factory.CreateKeyframeSynthesizer(
    config.Method,
    config
);
```

### Comparison Framework with Interface

```csharp
IVideoSynthesisComparator comparator = new VideoSynthesisComparator();

var results = await comparator.CompareApproachesAsync(
    testPrompt: "Beautiful landscape at sunset",
    duration: 10.0,
    outputDir: "comparison"
);

foreach (var result in results)
{
    Console.WriteLine($"{result.Key}: {result.Value.GenerationTime}s");
}
```

## Benefits of Interface-Based Design

### 1. Abstraction
- Hide implementation details
- Focus on contracts rather than concrete types
- Easier to understand high-level architecture

### 2. Flexibility
- Swap implementations without changing client code
- Support multiple synthesis methods seamlessly
- Easy to add new implementations

### 3. Testability
- Mock interfaces for unit testing
- Test behavior without executing actual synthesis
- Isolated testing of components

### 4. Maintainability
- Changes to implementations don't affect interface consumers
- Clear separation of concerns
- Easier to refactor and extend

### 5. Dependency Injection
- Standard DI container support
- Constructor injection of dependencies
- Lifetime management by container

## Testing with Interfaces

### Mocking Example

```csharp
// Using Moq framework
var mockSynthesizer = new Mock<IVideoSynthesizer>();
mockSynthesizer
    .Setup(s => s.GenerateVideoAsync(It.IsAny<string>(), It.IsAny<string>(), It.IsAny<int>(), null))
    .ReturnsAsync(true);

// Use in tests
var service = new VideoService(mockSynthesizer.Object);
var result = await service.ProcessVideo("test prompt");

// Verify
mockSynthesizer.Verify(
    s => s.GenerateVideoAsync("test prompt", It.IsAny<string>(), 10, null),
    Times.Once
);
```

### Test Implementation

```csharp
// Create a test implementation
public class TestVideoSynthesizer : IVideoSynthesizer
{
    public Task<bool> GenerateVideoAsync(string prompt, string outputPath, int duration, int? fps = null)
    {
        // Simulate generation without actual processing
        File.WriteAllText(outputPath, "test video content");
        return Task.FromResult(true);
    }
    
    public Task<bool> GenerateVideoAsync(string prompt, string outputPath, string keyframePath, int duration, int? fps = null)
    {
        File.WriteAllText(outputPath, "test video content");
        return Task.FromResult(true);
    }
}

// Use in tests
IVideoSynthesizer synthesizer = new TestVideoSynthesizer();
var result = await synthesizer.GenerateVideoAsync("test", "output.mp4", 10);
Assert.True(result);
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│          Client Application                      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      IVideoSynthesizerFactory                    │
│  Creates synthesizers based on method            │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┴─────────┐
        ▼                  ▼
┌──────────────┐   ┌──────────────────┐
│IVideoSynth...|   |IKeyframeVideoSy..|
│              │   │                  │
└──────┬───────┘   └────────┬─────────┘
       │                    │
       ▼                    ▼
┌──────────────┐   ┌──────────────────┐
│LTXVideoSynt..│   │KeyframeVideoSyn..│
│              │   │                  │
└──────────────┘   └──────────────────┘
```

## Best Practices

1. **Program to Interfaces**
   - Always use interface types in method signatures
   - Depend on abstractions, not implementations

2. **Factory Pattern**
   - Use factory for creating synthesizers
   - Centralize configuration logic

3. **Configuration**
   - Validate configurations before use
   - Use interface-based configuration

4. **Error Handling**
   - Handle failures gracefully
   - Return meaningful error information

5. **Async/Await**
   - All synthesis methods are async
   - Properly await async operations

## Migration Guide

### From Concrete Classes to Interfaces

**Before**:
```csharp
var synthesizer = new LTXVideoSynthesizer(1080, 1920, 30);
await synthesizer.GenerateVideoAsync(prompt, output, 10);
```

**After**:
```csharp
IVideoSynthesizerFactory factory = new VideoSynthesizerFactory();
IVideoSynthesizer synthesizer = factory.CreateSynthesizer(
    VideoSynthesisMethod.LTXVideo,
    1080, 1920, 30
);
await synthesizer.GenerateVideoAsync(prompt, output, 10);
```

## Summary

The interface-based design provides:
- ✅ Clear abstraction boundaries
- ✅ Flexible implementation switching
- ✅ Dependency injection support
- ✅ Improved testability
- ✅ Better maintainability
- ✅ Factory pattern for creation
- ✅ Configuration validation
- ✅ Extensible architecture

All existing functionality is preserved while adding these architectural improvements.
