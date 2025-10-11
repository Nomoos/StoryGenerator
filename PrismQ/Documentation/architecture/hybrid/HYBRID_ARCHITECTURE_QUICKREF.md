# Hybrid Architecture Quick Reference

> **Quick decision guide**: When to use C#, when to use Python, and how to integrate them.

**Related Documents**:
- [Full Comparison Analysis](./CSHARP_VS_PYTHON_COMPARISON.md) - Comprehensive comparison
- [Visual Diagrams](./HYBRID_ARCHITECTURE_DIAGRAMS.md) - Flowcharts and architecture diagrams

---

```
Need to perform a task?
│
├─ Is it ML model inference? (PyTorch/Diffusers/Transformers)
│  │
│  ├─ YES → Use Python subprocess
│  │         Examples: SDXL, LTX-Video, Whisper, LLaVA
│  │
│  └─ NO → Continue...
│
├─ Is it an API call? (OpenAI, ElevenLabs, etc.)
│  │
│  ├─ YES → Use C#
│  │         Reason: Better HTTP/JSON handling, type safety
│  │
│  └─ NO → Continue...
│
├─ Is it FFmpeg/media processing?
│  │
│  ├─ YES → Use C# with FFmpeg wrapper
│  │         Reason: Better process management
│  │
│  └─ NO → Continue...
│
└─ Default → Use C#
            Reason: Better for orchestration, I/O, configuration
```

---

## 📋 Stage-by-Stage Guide

| Stage | Use | Integration |
|-------|-----|-------------|
| 0. Idea Collection | 🔷 **C#** | Pure C# - API calls, JSON |
| 1. Story Ideas | 🔷 **C#** | OpenAI API via HttpClient |
| 2. Script Generation | 🔷 **C#** | OpenAI API via HttpClient |
| 3. Script Revision | 🔷 **C#** | OpenAI API + string processing |
| 4. Voice Generation | 🔷 **C#** | ElevenLabs API + FFmpeg |
| 5. Subtitle/ASR | 🔶 **Hybrid** | C# → Python (faster-whisper) |
| 6. Scene Planning | 🔷 **C#** | OpenAI API or Ollama subprocess |
| 7. Vision Guidance | 🔶 **Hybrid** | C# → Python (LLaVA/Phi-3.5) |
| 8. Keyframes (SDXL) | 🔶 **Hybrid** | C# → Python (diffusers) |
| 9. Video (LTX) | 🔶 **Hybrid** | C# → Python (diffusers) |
| 10. Post-Production | 🔷 **C#** | FFmpeg orchestration |

**Legend**:
- 🔷 **C#**: Pure C# implementation
- 🔶 **Hybrid**: C# orchestration + Python subprocess

---

## 🔧 Implementation Patterns

### Pattern 1: Pure C# (API Calls)

**Use for**: OpenAI, ElevenLabs, HTTP APIs

```csharp
public class ScriptGenerator : IScriptGenerator
{
    private readonly HttpClient _httpClient;
    private readonly string _apiKey;

    public async Task<string> GenerateScriptAsync(
        IStoryIdea idea,
        CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, 
            "https://api.openai.com/v1/chat/completions")
        {
            Headers = { 
                Authorization = new AuthenticationHeaderValue("Bearer", _apiKey) 
            },
            Content = JsonContent.Create(new {
                model = "gpt-4o-mini",
                messages = new[] {
                    new { role = "system", content = "You are a script writer..." },
                    new { role = "user", content = $"Write a script for: {idea.Title}" }
                }
            })
        };

        var response = await _httpClient.SendAsync(request, cancellationToken);
        var result = await response.Content.ReadFromJsonAsync<OpenAIResponse>();
        
        return result.Choices[0].Message.Content;
    }
}
```

**Advantages**: Fast, type-safe, easy to test

### Pattern 2: C# + FFmpeg

**Use for**: Audio/video processing, LUFS normalization, compositing

```csharp
public class AudioProcessor : IAudioProcessor
{
    private readonly ILogger<AudioProcessor> _logger;

    public async Task<string> NormalizeAudioAsync(
        string inputPath,
        string outputPath,
        double targetLufs = -16.0,
        CancellationToken cancellationToken = default)
    {
        // Two-pass LUFS normalization
        var ffmpegArgs = $"-i \"{inputPath}\" " +
                        $"-af loudnorm=I={targetLufs}:TP=-1.5:LRA=11:print_format=summary " +
                        $"-f null -";

        var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = "ffmpeg",
                Arguments = ffmpegArgs,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false
            }
        };

        process.Start();
        var output = await process.StandardError.ReadToEndAsync();
        await process.WaitForExitAsync(cancellationToken);

        // Parse loudnorm output and apply
        // ... (implementation details)

        return outputPath;
    }
}
```

**Advantages**: Native process control, async/await support

### Pattern 3: C# → Python Subprocess (ML Inference)

**Use for**: Whisper ASR, SDXL, LTX-Video, Vision models

```csharp
// C# Side - Executor
public class PythonScriptExecutor : IPythonScriptExecutor
{
    private readonly string _pythonPath;
    private readonly ILogger<PythonScriptExecutor> _logger;

    public async Task<TResult> ExecuteAsync<TResult>(
        string scriptPath,
        Dictionary<string, object> args,
        CancellationToken cancellationToken = default)
    {
        // 1. Serialize input
        var inputJson = JsonSerializer.Serialize(args);
        var inputFile = Path.GetTempFileName();
        await File.WriteAllTextAsync(inputFile, inputJson, cancellationToken);

        try
        {
            // 2. Execute Python
            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = _pythonPath,
                    Arguments = $"\"{scriptPath}\" --input \"{inputFile}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false
                }
            };

            process.Start();
            var outputJson = await process.StandardOutput.ReadToEndAsync();
            var errorOutput = await process.StandardError.ReadToEndAsync();
            await process.WaitForExitAsync(cancellationToken);

            if (process.ExitCode != 0)
            {
                _logger.LogError("Python script failed: {Error}", errorOutput);
                throw new PythonExecutionException(errorOutput);
            }

            // 3. Deserialize result
            return JsonSerializer.Deserialize<TResult>(outputJson)!;
        }
        finally
        {
            // 4. Cleanup
            if (File.Exists(inputFile))
                File.Delete(inputFile);
        }
    }
}

// C# Side - Usage
public class KeyframeGenerator : IKeyframeGenerator
{
    private readonly IPythonScriptExecutor _executor;

    public async Task<List<string>> GenerateKeyframesAsync(
        List<string> prompts,
        string outputDir,
        CancellationToken cancellationToken = default)
    {
        var args = new Dictionary<string, object>
        {
            ["prompts"] = prompts,
            ["output_dir"] = outputDir,
            ["model"] = "stabilityai/stable-diffusion-xl-base-1.0",
            ["num_inference_steps"] = 50
        };

        var result = await _executor.ExecuteAsync<KeyframeResult>(
            "scripts/sdxl_generate.py",
            args,
            cancellationToken
        );

        return result.ImagePaths;
    }
}
```

```python
# Python Side - scripts/sdxl_generate.py
import json
import sys
from pathlib import Path
from diffusers import StableDiffusionXLPipeline
import torch

def main():
    # 1. Parse input
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    
    with open(args.input, 'r') as f:
        config = json.load(f)
    
    # 2. Load model
    pipe = StableDiffusionXLPipeline.from_pretrained(
        config['model'],
        torch_dtype=torch.float16,
        variant="fp16"
    ).to("cuda")
    
    # 3. Generate images
    image_paths = []
    for i, prompt in enumerate(config['prompts']):
        image = pipe(
            prompt,
            num_inference_steps=config['num_inference_steps']
        ).images[0]
        
        output_path = Path(config['output_dir']) / f"frame_{i:03d}.png"
        image.save(output_path)
        image_paths.append(str(output_path))
    
    # 4. Return result as JSON
    result = {
        "image_paths": image_paths,
        "success": True
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

**Advantages**: 
- Access to mature Python ML ecosystem
- Clean separation
- Easy to test independently

---

## 🚀 When to Use Each Approach

### ✅ Use Pure C# When:

1. **API Integrations**
   - OpenAI, Claude, GPT-4
   - ElevenLabs, Resemble AI
   - Any REST API

2. **File Operations**
   - Reading/writing files
   - JSON serialization
   - Path management

3. **Orchestration**
   - Pipeline coordination
   - State management
   - Error handling

4. **Media Processing (via FFmpeg)**
   - Audio normalization
   - Video encoding
   - Subtitle overlay

5. **Configuration & Logging**
   - appsettings.json
   - Structured logging
   - Dependency injection

### ⚠️ Use Python Subprocess When:

1. **ML Model Inference**
   - PyTorch models (SDXL, LTX-Video)
   - Transformers models (Whisper, LLaVA)
   - Diffusers pipelines

2. **Specialized ML Libraries**
   - faster-whisper (ASR)
   - diffusers (image/video generation)
   - transformers (vision models)

3. **GPU-Bound Tasks**
   - Where subprocess overhead (50-200ms) is negligible
   - Tasks taking 5+ seconds

### ❌ Avoid Python When:

1. **Simple I/O Operations**
   - C# is faster and more type-safe

2. **API Calls**
   - C# HttpClient is excellent

3. **Configuration Management**
   - C# config system is superior

4. **Orchestration Logic**
   - C# provides better structure

---

## 📊 Performance Comparison

| Task Type | C# | Python | Overhead |
|-----------|-----|--------|----------|
| **API Call** | 100-500ms | 150-700ms | +50% |
| **File I/O** | 10-50ms | 20-100ms | +100% |
| **JSON Parse** | 5-20ms | 10-50ms | +100% |
| **Subprocess Start** | N/A | 50-200ms | Fixed cost |
| **SDXL (1 image)** | N/A | 5-10s | 200ms/5s = 4% |
| **LTX-Video** | N/A | 15-30s | 200ms/20s = 1% |
| **Whisper ASR** | N/A | 2-5s | 200ms/3s = 6% |

**Key Insight**: Subprocess overhead is negligible for GPU-bound tasks.

---

## 🔒 Best Practices

### C# Best Practices

1. **Use Interfaces**
   ```csharp
   public interface IScriptGenerator
   {
       Task<string> GenerateAsync(IStoryIdea idea);
   }
   ```

2. **Dependency Injection**
   ```csharp
   services.AddSingleton<IScriptGenerator, ScriptGenerator>();
   ```

3. **Async/Await**
   ```csharp
   public async Task<string> ProcessAsync()
   {
       var result = await _client.GetAsync("...");
       return await result.Content.ReadAsStringAsync();
   }
   ```

4. **Configuration**
   ```csharp
   var config = _configuration.GetSection("OpenAI").Get<OpenAIConfig>();
   ```

5. **Logging**
   ```csharp
   _logger.LogInformation("Generated script for {Title}", idea.Title);
   ```

### Python Integration Best Practices

1. **Use Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Pin Dependencies**
   ```txt
   # requirements.txt
   torch==2.1.0
   diffusers==0.24.0
   transformers==4.35.0
   ```

3. **JSON I/O Only**
   - Input: JSON file
   - Output: JSON to stdout
   - Errors: stderr

4. **Exit Codes**
   - 0 = Success
   - Non-zero = Error

5. **Stateless Scripts**
   - No global state
   - Pure functions
   - Easy to test

---

## 🐛 Common Pitfalls & Solutions

### Pitfall 1: Hardcoding Python Path
❌ **Bad**:
```csharp
FileName = "python"  // Might not work on all systems
```

✅ **Good**:
```csharp
FileName = _configuration["Pipeline:PythonExecutable"] ?? "python3"
```

### Pitfall 2: Not Handling Errors
❌ **Bad**:
```csharp
await process.WaitForExitAsync();
var output = await process.StandardOutput.ReadToEndAsync();
```

✅ **Good**:
```csharp
await process.WaitForExitAsync();
if (process.ExitCode != 0)
{
    var error = await process.StandardError.ReadToEndAsync();
    throw new PythonExecutionException(error);
}
var output = await process.StandardOutput.ReadToEndAsync();
```

### Pitfall 3: Forgetting Cleanup
❌ **Bad**:
```csharp
var tempFile = Path.GetTempFileName();
await File.WriteAllTextAsync(tempFile, json);
// Execute...
// Temp file left behind!
```

✅ **Good**:
```csharp
var tempFile = Path.GetTempFileName();
try
{
    await File.WriteAllTextAsync(tempFile, json);
    // Execute...
}
finally
{
    if (File.Exists(tempFile))
        File.Delete(tempFile);
}
```

### Pitfall 4: Using Python.NET Unnecessarily
❌ **Bad**: Using Python.NET for GPU-bound tasks

✅ **Good**: Subprocess is simpler and sufficient

---

## 📚 Additional Resources

### Documentation
- [Full Comparison Document](./CSHARP_VS_PYTHON_COMPARISON.md)
- [C# Implementation Complete](./CSHARP_IMPLEMENTATION_COMPLETE.md)
- [C# Research](./CSHARP_RESEARCH.md)
- [SOLID OOP Guide](../src/CSharp/SOLID_OOP_CLEAN_CODE_GUIDE.md)

### Code Examples
- [C# Examples](../src/CSharp/Examples/)
- [Python Research Scripts](../research/python/)
- [Integration Tests](../tests/)

---

**Last Updated**: 2025-10-08  
**Version**: 1.0  
**Status**: Production Guide
