# Research: C# Ollama Client

**ID:** `01-research-06-csharp-ollama`  
**Priority:** P1  
**Effort:** 4-6 hours  
**Status:** ✅ Complete

## Overview

C# client implementation for Ollama local LLM service integration. This research prototype validates the approach for calling local language models (Qwen2.5, Llama3.1, Mistral) from C# using the Ollama CLI interface. The implementation serves as a foundation for content generation tasks that require local-only LLM orchestration.

## Dependencies

**Requires:**
- `00-setup-04`: C# project structure
- Ollama installed locally (`ollama` command available in PATH)

**Blocks:**
- Phase 3 content generation tasks that use LLM
- Script generation and improvement tasks

## Acceptance Criteria

- [x] C# client can call Ollama CLI successfully
- [x] Supports configurable models (llama2, mistral, qwen2.5, etc.)
- [x] Handles system messages and temperature settings
- [x] Async/await pattern with cancellation support
- [x] Error handling and process management
- [x] Documentation and code examples provided

## Task Details

### Implementation

The `OllamaClient` class in `StoryGenerator.Research` provides a simple interface to Ollama:

```csharp
public class OllamaClient : IOllamaClient
{
    private readonly string _model;
    private readonly string _baseUrl;

    public OllamaClient(string model = "llama2", string baseUrl = "http://localhost:11434")
    {
        _model = model;
        _baseUrl = baseUrl;
    }

    public async Task<string> GenerateAsync(
        string prompt,
        string system = null,
        float temperature = 0.7f,
        int? maxTokens = null,
        CancellationToken cancellationToken = default)
    {
        // Executes: ollama run {model}
        // Writes prompt to stdin, reads response from stdout
    }

    public async IAsyncEnumerable<string> GenerateStreamAsync(
        string prompt,
        string system = null,
        float temperature = 0.7f,
        int? maxTokens = null,
        CancellationToken cancellationToken = default)
    {
        // Streams tokens as they're generated
    }
}
```

**Key Features:**
- **Model Selection**: Configurable at initialization (llama2, mistral, qwen2.5, etc.)
- **System Messages**: Optional system prompts for context/behavior
- **Temperature Control**: Sampling randomness (0.0 = deterministic, 1.0 = creative)
- **Token Limits**: Optional max tokens for generation control
- **Streaming**: Real-time token streaming via `IAsyncEnumerable`
- **Cancellation**: Proper cancellation token support
- **Error Handling**: Captures stderr and provides meaningful error messages

**Process Management:**
- Uses `System.Diagnostics.Process` to spawn `ollama run` subprocess
- Redirects stdin/stdout/stderr for communication
- Properly disposes resources and handles cleanup
- Supports cancellation mid-generation

### Testing

```bash
# Build the research project
cd src/CSharp
dotnet build StoryGenerator.Research/StoryGenerator.Research.csproj

# Verify Ollama is installed
ollama --version

# Pull a model (if not already available)
ollama pull llama2

# Run the orchestrator demo (includes Ollama test)
cd StoryGenerator.Research
dotnet run

# Test specific model
ollama run llama2 "What is C#?"
```

**Example Usage:**
```csharp
var client = new OllamaClient(model: "qwen2_5_14b");

// Simple generation
var response = await client.GenerateAsync(
    prompt: "Write a short story about a robot.",
    system: "You are a creative storyteller.",
    temperature: 0.8f
);

// Streaming generation
await foreach (var token in client.GenerateStreamAsync(
    prompt: "Count from 1 to 5",
    temperature: 0.1f))
{
    Console.Write(token);
}
```

## Output Files

- `/src/CSharp/StoryGenerator.Research/OllamaClient.cs` - Main implementation (100+ lines)
- `/src/CSharp/StoryGenerator.Research/IOllamaClient.cs` - Interface definition
- `/src/CSharp/StoryGenerator.Research/Orchestrator.cs` - Demo/test orchestrator

## Related Files

- `/config/pipeline.yaml` - Model configuration (qwen2_5_14b defined)
- `/src/CSharp/StoryGenerator.Research/Models.cs` - Shared data models
- Ollama documentation: https://github.com/ollama/ollama

## Validation

```bash
# Verify implementation exists
ls -la src/CSharp/StoryGenerator.Research/OllamaClient.cs

# Check project builds
cd src/CSharp && dotnet build StoryGenerator.Research/StoryGenerator.Research.csproj

# Test Ollama connectivity
ollama list  # Should show installed models
```

## Notes

**Integration Approach:**
- Uses CLI subprocess rather than HTTP API for simplicity
- Suitable for local development and research
- Production may want to use Ollama HTTP API for better performance

**Model Requirements:**
- Ollama must be installed and running
- Models must be pulled before use (`ollama pull <model>`)
- GPU support automatic if CUDA available

**Performance Considerations:**
- Process spawn has small overhead (~100ms)
- Streaming recommended for long generations
- Token generation speed depends on model size and hardware

**Known Limitations:**
- Requires Ollama CLI in PATH
- No built-in retry logic (add via Polly if needed)
- Error messages from Ollama CLI may be terse

## Next Steps

After completion:
- Phase 3 script generation can use this client
- Content improvement tasks can leverage different models
- Consider HTTP API version for production
