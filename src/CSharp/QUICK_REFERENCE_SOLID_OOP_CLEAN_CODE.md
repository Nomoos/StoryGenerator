# Quick Reference: SOLID + OOP + Clean Code

> **One-page cheat sheet for daily development**

---

## 🎯 The Golden Rules

1. **Use all three together** - SOLID + OOP + Clean Code are complementary
2. **Interfaces first** - Define contracts before implementations
3. **Dependency injection** - Never `new` up dependencies in constructors
4. **Async all the way** - All I/O operations must be async
5. **Validate early** - Check inputs at method boundaries

---

## SOLID Principles (Quick)

| Principle | Rule | Example |
|-----------|------|---------|
| **S**ingle Responsibility | One class = one job | `ScriptScorer` only scores, doesn't generate |
| **O**pen/Closed | Extend, don't modify | Add new `IVideoSynthesizer` impl, don't change interface |
| **L**iskov Substitution | Swap implementations freely | Any `ILLMModelProvider` works in `ScriptGenerator` |
| **I**nterface Segregation | Small, focused interfaces | `IIdeaGenerator` vs giant `IContentGenerator` |
| **D**ependency Inversion | Depend on abstractions | Constructor takes `ILogger`, not `ConsoleLogger` |

---

## OOP Quick Checks

### ✅ DO

```csharp
// Encapsulation
public class VideoConfig
{
    private int _width;
    public int Width 
    { 
        get => _width;
        set => _width = value > 0 ? value : throw new ArgumentException();
    }
}

// Polymorphism
public interface IVideoSynthesizer { }
public class LTXVideoSynthesizer : IVideoSynthesizer { }
public class CogVideoXSynthesizer : IVideoSynthesizer { }

// Composition over inheritance
public class VideoProcessor
{
    private readonly IVideoSynthesizer _synthesizer; // Composed, not inherited
}
```

### ❌ DON'T

```csharp
// NO public fields
public class VideoConfig { public int Width; }

// NO deep inheritance
public class A { }
public class B : A { }
public class C : B { }
public class D : C { } // Too deep!

// NO inheritance for code reuse only
public class VideoProcessor : StringHelper { } // Use composition instead
```

---

## Clean Code Quick Checks

### Naming

```csharp
// ✅ GOOD
public async Task<ScriptScoringResult> ScoreScriptAsync(string scriptPath)
public class VideoSynthesizerFactory { }
private readonly ILLMModelProvider _llmProvider;

// ❌ BAD
public async Task<SSR> Score(string p)
public class VSF { }
private ILLMModelProvider llm;
```

### Function Size

```csharp
// ✅ GOOD: Small, focused
public async Task<Video> GenerateVideoAsync(string prompt)
{
    ValidateInput(prompt);
    var script = await GenerateScriptAsync(prompt);
    var voice = await GenerateVoiceAsync(script);
    return await ComposeVideoAsync(script, voice);
}

// ❌ BAD: Too large (> 30 lines)
public async Task<Video> GenerateVideoAsync(string prompt)
{
    // 100 lines of code doing everything...
}
```

### Error Handling

```csharp
// ✅ GOOD
public async Task<string> ProcessAsync(string input)
{
    if (string.IsNullOrWhiteSpace(input))
        throw new ArgumentException("Input cannot be empty", nameof(input));
    
    try
    {
        return await _service.ProcessAsync(input);
    }
    catch (HttpRequestException ex)
    {
        _logger.LogError(ex, "Network error processing {Input}", input);
        throw new ProcessingException("Network error occurred", ex);
    }
}

// ❌ BAD
public async Task<string> ProcessAsync(string input)
{
    try
    {
        return await _service.ProcessAsync(input); // No validation
    }
    catch (Exception ex)
    {
        return null; // Swallowed exception!
    }
}
```

---

## Common Patterns in Our Codebase

### 1. Interface + Implementation

```csharp
// 1. Define interface
public interface IScriptGenerator
{
    Task<string> GenerateScriptAsync(StoryIdea idea, CancellationToken ct = default);
}

// 2. Implement
public class ScriptGenerator : IScriptGenerator
{
    private readonly ILLMModelProvider _llmProvider;
    private readonly ILogger<ScriptGenerator> _logger;
    
    public ScriptGenerator(ILLMModelProvider llmProvider, ILogger<ScriptGenerator> logger)
    {
        _llmProvider = llmProvider ?? throw new ArgumentNullException(nameof(llmProvider));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }
    
    public async Task<string> GenerateScriptAsync(StoryIdea idea, CancellationToken ct = default)
    {
        if (idea == null) throw new ArgumentNullException(nameof(idea));
        // Implementation...
    }
}

// 3. Register in DI
services.AddScoped<IScriptGenerator, ScriptGenerator>();

// 4. Use via interface
public class MyService
{
    private readonly IScriptGenerator _scriptGenerator;
    
    public MyService(IScriptGenerator scriptGenerator)
    {
        _scriptGenerator = scriptGenerator;
    }
}
```

### 2. Factory Pattern

```csharp
public interface IVideoSynthesizerFactory
{
    IVideoSynthesizer CreateSynthesizer(VideoSynthesisMethod method);
}

public class VideoSynthesizerFactory : IVideoSynthesizerFactory
{
    public IVideoSynthesizer CreateSynthesizer(VideoSynthesisMethod method)
    {
        return method switch
        {
            VideoSynthesisMethod.LTXVideo => new LTXVideoSynthesizer(...),
            VideoSynthesisMethod.CogVideoX => new CogVideoXSynthesizer(...),
            _ => throw new ArgumentException($"Unsupported: {method}")
        };
    }
}
```

### 3. Options Pattern

```csharp
// 1. Define options class
public class OpenAIOptions
{
    public string ApiKey { get; set; }
    public string Model { get; set; } = "gpt-4o-mini";
    public double Temperature { get; set; } = 0.7;
}

// 2. Configure in appsettings.json
{
  "OpenAI": {
    "ApiKey": "sk-...",
    "Model": "gpt-4o-mini",
    "Temperature": 0.7
  }
}

// 3. Register
services.Configure<OpenAIOptions>(configuration.GetSection("OpenAI"));

// 4. Use
public class OpenAIClient
{
    private readonly OpenAIOptions _options;
    
    public OpenAIClient(IOptions<OpenAIOptions> options)
    {
        _options = options.Value;
    }
}
```

---

## Code Review Checklist

Copy this for every PR:

```markdown
### SOLID
- [ ] Single Responsibility: Each class has one job
- [ ] Open/Closed: Can extend without modifying
- [ ] Liskov Substitution: Implementations are interchangeable
- [ ] Interface Segregation: Small, focused interfaces
- [ ] Dependency Inversion: Depends on abstractions

### OOP
- [ ] No public fields (use properties)
- [ ] Proper encapsulation with validation
- [ ] Composition preferred over inheritance
- [ ] Polymorphism used where appropriate

### Clean Code
- [ ] Meaningful names (no abbreviations)
- [ ] Small functions (< 20 lines)
- [ ] XML docs on public APIs
- [ ] No code duplication
- [ ] Proper error handling with logging
- [ ] Early input validation

### Testing
- [ ] Unit tests added
- [ ] Tests are independent
- [ ] Arrange-Act-Assert structure
- [ ] Coverage > 80%

### Documentation
- [ ] XML docs updated
- [ ] README updated if needed
- [ ] Breaking changes noted
```

---

## Common Mistakes to Avoid

### ❌ 1. God Classes

```csharp
// BAD: One class does everything
public class VideoManager
{
    public void GenerateIdea() { }
    public void GenerateScript() { }
    public void GenerateVoice() { }
    public void GenerateVideo() { }
    public void SaveToDatabase() { }
    public void SendEmail() { }
    public void LogEverything() { }
}
```

**Fix**: Split into focused classes (IdeaGenerator, ScriptGenerator, etc.)

### ❌ 2. Tight Coupling

```csharp
// BAD: Directly instantiating dependencies
public class ScriptGenerator
{
    private readonly OpenAIClient _client = new OpenAIClient(); // Hard-coded!
}
```

**Fix**: Use dependency injection

```csharp
// GOOD
public class ScriptGenerator
{
    private readonly ILLMModelProvider _llmProvider;
    
    public ScriptGenerator(ILLMModelProvider llmProvider)
    {
        _llmProvider = llmProvider;
    }
}
```

### ❌ 3. Magic Numbers/Strings

```csharp
// BAD
if (score > 75) { }
var path = "/scripts/raw_local";
```

**Fix**: Use constants or configuration

```csharp
// GOOD
private const int MinimumPassingScore = 75;
private readonly string _scriptsPath = _options.Paths.RawScripts;

if (score > MinimumPassingScore) { }
var path = _scriptsPath;
```

### ❌ 4. Swallowed Exceptions

```csharp
// BAD
try
{
    await ProcessAsync();
}
catch (Exception)
{
    return null; // Silent failure!
}
```

**Fix**: Log and rethrow or throw custom exception

```csharp
// GOOD
try
{
    return await ProcessAsync();
}
catch (HttpRequestException ex)
{
    _logger.LogError(ex, "Network error in ProcessAsync");
    throw new ProcessingException("Failed to process due to network error", ex);
}
```

### ❌ 5. No Input Validation

```csharp
// BAD
public async Task ProcessAsync(string input)
{
    // Direct use without validation
    return await _service.CallAsync(input);
}
```

**Fix**: Validate early

```csharp
// GOOD
public async Task ProcessAsync(string input)
{
    if (string.IsNullOrWhiteSpace(input))
        throw new ArgumentException("Input cannot be empty", nameof(input));
    
    return await _service.CallAsync(input);
}
```

---

## Quick Decision Trees

### "Should I create an interface?"

```
Is it a public API? ───YES──→ Create interface
       │
       NO
       │
Will I have multiple implementations? ───YES──→ Create interface
       │
       NO
       │
Do I need to mock it for testing? ───YES──→ Create interface
       │
       NO
       │
    Use concrete class
```

### "Should I use inheritance or composition?"

```
Is it a true "is-a" relationship? ───NO──→ Use composition
       │
      YES
       │
Do I need to share implementation code? ───NO──→ Use interface + composition
       │
      YES
       │
    Use inheritance (base class)
```

### "Should I extract a method?"

```
Is code duplicated? ───YES──→ Extract method
       │
       NO
       │
Is the method > 20 lines? ───YES──→ Extract logical chunks
       │
       NO
       │
Does it do multiple things? ───YES──→ Extract each thing
       │
       NO
       │
    Keep as is
```

---

## Testing Quick Reference

### Unit Test Structure

```csharp
[Fact]
public async Task MethodName_Scenario_ExpectedResult()
{
    // Arrange - Set up test data and mocks
    var mockProvider = new Mock<ILLMModelProvider>();
    mockProvider.Setup(x => x.GenerateTextAsync(It.IsAny<string>(), default))
                .ReturnsAsync("Generated script");
    
    var generator = new ScriptGenerator(mockProvider.Object);
    var idea = new StoryIdea { StoryTitle = "Test" };
    
    // Act - Execute the method being tested
    var result = await generator.GenerateScriptAsync(idea);
    
    // Assert - Verify the results
    Assert.NotNull(result);
    Assert.NotEmpty(result);
    mockProvider.Verify(x => x.GenerateTextAsync(It.IsAny<string>(), default), Times.Once);
}
```

### Common Test Scenarios

```csharp
// Test: Normal case
[Fact]
public async Task GenerateAsync_ValidInput_ReturnsResult() { }

// Test: Null/empty input
[Fact]
public async Task GenerateAsync_NullInput_ThrowsArgumentNullException() { }

// Test: Invalid input
[Fact]
public async Task GenerateAsync_InvalidInput_ThrowsArgumentException() { }

// Test: External service failure
[Fact]
public async Task GenerateAsync_ServiceFails_ThrowsServiceException() { }

// Test: Cancellation
[Fact]
public async Task GenerateAsync_Cancelled_ThrowsOperationCancelledException() { }
```

---

## Performance Tips

### 1. Use Async/Await Correctly

```csharp
// ✅ GOOD
public async Task<string> ProcessAsync()
{
    var result1 = await GetDataAsync();
    var result2 = await ProcessDataAsync(result1);
    return result2;
}

// ❌ BAD: Blocking
public string Process()
{
    var result1 = GetDataAsync().Result; // Deadlock risk!
    var result2 = ProcessDataAsync(result1).Result;
    return result2;
}
```

### 2. Parallel Processing

```csharp
// ✅ GOOD: Parallel independent operations
var tasks = new[]
{
    GenerateVideoAsync(prompt1),
    GenerateVideoAsync(prompt2),
    GenerateVideoAsync(prompt3)
};
var results = await Task.WhenAll(tasks);

// ❌ BAD: Sequential when parallel possible
var result1 = await GenerateVideoAsync(prompt1);
var result2 = await GenerateVideoAsync(prompt2);
var result3 = await GenerateVideoAsync(prompt3);
```

### 3. Resource Cleanup

```csharp
// ✅ GOOD: Using statement
public async Task ProcessAsync(string videoPath)
{
    using var resourceManager = new VideoResourceManager();
    var tempFile = resourceManager.GetTempFilePath(".mp4");
    // Process...
    // Automatic cleanup
}

// ❌ BAD: Manual cleanup (easy to forget)
public async Task ProcessAsync(string videoPath)
{
    var tempFile = GetTempFilePath();
    // Process...
    File.Delete(tempFile); // What if exception thrown?
}
```

---

## When in Doubt

1. **Keep it simple** - Don't over-engineer
2. **Make it work** - Then make it better
3. **Write tests** - They document intent
4. **Ask for review** - Two heads > one
5. **Refactor continuously** - Don't wait for "perfect"

---

## Resources

- **Full Guide**: See `SOLID_OOP_CLEAN_CODE_GUIDE.md` for detailed explanations
- **Migration Guide**: See `MIGRATION_GUIDE.md` for Python → C# patterns
- **Code Quality**: See `CODE_QUALITY_IMPROVEMENTS.md` for improvements
- **Interfaces**: See `INTERFACES_GUIDE.md` for interface patterns

---

**Quick Reference Version**: 1.0  
**Last Updated**: January 2025
