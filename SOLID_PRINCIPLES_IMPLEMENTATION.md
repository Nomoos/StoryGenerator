# SOLID Principles Implementation Guide

## 📋 Table of Contents
- [Overview](#overview)
- [Single Responsibility Principle (SRP)](#single-responsibility-principle-srp)
- [Open/Closed Principle (OCP)](#openclosed-principle-ocp)
- [Liskov Substitution Principle (LSP)](#liskov-substitution-principle-lsp)
- [Interface Segregation Principle (ISP)](#interface-segregation-principle-isp)
- [Dependency Inversion Principle (DIP)](#dependency-inversion-principle-dip)
- [SOLID in Action: Real Examples](#solid-in-action-real-examples)
- [Best Practices](#best-practices)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

## Overview

This document demonstrates how the **StoryGenerator** repository implements SOLID principles throughout its codebase. Each principle is explained with:
- ✅ **Good examples** from our codebase
- ❌ **Anti-patterns** to avoid
- 🎯 **Real-world applications**
- 💡 **Key takeaways**

### What is SOLID?

SOLID is an acronym for five design principles that make software designs more understandable, flexible, and maintainable:

- **S**ingle Responsibility Principle
- **O**pen/Closed Principle
- **L**iskov Substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Inversion Principle

### Why SOLID Matters

- **Maintainability**: Changes are localized and predictable
- **Testability**: Components can be tested in isolation
- **Flexibility**: Easy to extend without modifying existing code
- **Reusability**: Components can be used in different contexts
- **Understandability**: Clear responsibilities and relationships

## Single Responsibility Principle (SRP)

> **A class should have only one reason to change.**

Each class should have a **single, well-defined responsibility**. If a class has multiple reasons to change, it violates SRP.

### ✅ Good Example: Separated Concerns

Our infrastructure components each handle **one specific concern**:

```python
# File: PrismQ/Infrastructure/Core/Shared/logging.py
class LoggingService:
    """Handles ONLY logging operations."""
    
    def log_info(self, message: str, context: dict = None) -> None:
        """Log informational message."""
        pass
    
    def log_error(self, message: str, error: Exception = None) -> None:
        """Log error message."""
        pass
    
    def configure_logger(self, config: dict) -> None:
        """Configure logging settings."""
        pass


# File: PrismQ/Infrastructure/Core/Shared/cache.py
class CacheService:
    """Handles ONLY caching operations."""
    
    def get(self, key: str) -> Any:
        """Retrieve cached value."""
        pass
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Store value in cache."""
        pass
    
    def invalidate(self, key: str) -> None:
        """Invalidate cached value."""
        pass


# File: PrismQ/Infrastructure/Core/Shared/retry.py
class RetryService:
    """Handles ONLY retry logic and circuit breaker."""
    
    def execute_with_retry(self, func, max_retries: int = 3) -> Any:
        """Execute function with retry logic."""
        pass
    
    def create_circuit_breaker(self, threshold: int = 5) -> Any:
        """Create circuit breaker for failure protection."""
        pass
```

**Why This Works**:
- Each class has **one reason to change**
- Changes to logging don't affect caching
- Changes to retry logic don't affect logging
- Easy to test independently
- Clear, focused responsibilities

### ❌ Anti-Pattern: God Class

```python
# BAD: God class that does everything
class VideoProcessor:
    """Violates SRP - too many responsibilities!"""
    
    def process_video(self, input_file: str) -> str:
        """Process video file."""
        pass
    
    def generate_script(self, topic: str) -> str:
        """Generate script (should be separate)."""
        pass
    
    def call_openai(self, prompt: str) -> str:
        """Call OpenAI API (should be separate)."""
        pass
    
    def save_to_database(self, data: dict) -> None:
        """Save to database (should be separate)."""
        pass
    
    def log_metrics(self, metrics: dict) -> None:
        """Log metrics (should be separate)."""
        pass
    
    def retry_on_failure(self, func) -> Any:
        """Retry logic (should be separate)."""
        pass
    
    def validate_input(self, data: dict) -> bool:
        """Validate input (should be separate)."""
        pass
```

**Problems**:
- **Multiple reasons to change**: API changes, database schema, logging format, validation rules
- **Hard to test**: Must mock all dependencies at once
- **Hard to reuse**: Can't use just the retry logic elsewhere
- **Poor maintainability**: Changes affect unrelated functionality

### 🎯 Real-World Application: Pipeline Stages

Each pipeline stage has **one responsibility**:

```python
# File: PrismQ/Pipeline/02_TextGeneration/StoryTitleProcessor/title_generation.py
class TitleGenerator:
    """Single Responsibility: Generate story titles."""
    
    def __init__(self, llm_provider: ILLMProvider):
        self.llm = llm_provider
    
    def generate_title(self, story_content: str) -> str:
        """Generate title from story content."""
        prompt = self._build_prompt(story_content)
        return self.llm.generate_completion(prompt)
    
    def _build_prompt(self, content: str) -> str:
        """Build prompt for title generation."""
        return f"Generate an engaging title for: {content}"


# File: PrismQ/Pipeline/02_TextGeneration/StoryTitleScoring/title_scoring.py
class TitleScorer:
    """Single Responsibility: Score title quality."""
    
    def score_title(self, title: str) -> float:
        """Calculate quality score for title."""
        score = 0.0
        score += self._check_length(title)
        score += self._check_keywords(title)
        score += self._check_emotional_appeal(title)
        return score / 3.0
    
    def _check_length(self, title: str) -> float:
        """Check if title length is optimal."""
        pass
    
    def _check_keywords(self, title: str) -> float:
        """Check for engaging keywords."""
        pass
    
    def _check_emotional_appeal(self, title: str) -> float:
        """Check emotional resonance."""
        pass
```

**Benefits**:
- `TitleGenerator` changes only when generation logic changes
- `TitleScorer` changes only when scoring criteria change
- Easy to test each component independently
- Can reuse `TitleScorer` in other contexts

### 💡 Key Takeaways

1. **One Responsibility**: Each class should do one thing well
2. **One Reason to Change**: If a class changes for multiple reasons, split it
3. **Easy to Name**: If you struggle to name a class, it probably does too much
4. **Focused Tests**: Each class should have focused, simple tests

## Open/Closed Principle (OCP)

> **Software entities should be open for extension, but closed for modification.**

You should be able to **extend behavior** without **modifying existing code**.

### ✅ Good Example: Provider Interface

Our `ILLMProvider` interface allows adding new providers **without modifying existing code**:

```python
# File: PrismQ/Infrastructure/Core/Shared/interfaces/llm_provider.py
class ILLMProvider(ABC):
    """Abstract interface for LLM providers - CLOSED for modification."""
    
    @abstractmethod
    def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion."""
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get model name."""
        pass


# File: PrismQ/Infrastructure/Platform/Providers/openai_provider.py
class OpenAIProvider(ILLMProvider):
    """EXTENSION: OpenAI implementation - no modification of base."""
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        # OpenAI-specific implementation
        return openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
    
    @property
    def model_name(self) -> str:
        return "gpt-4"


# File: PrismQ/Infrastructure/Platform/Providers/local_model_provider.py
class LocalModelProvider(ILLMProvider):
    """EXTENSION: Local model - no modification of base or OpenAI."""
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        # Local model implementation
        return self.local_model.generate(prompt, **kwargs)
    
    @property
    def model_name(self) -> str:
        return "local-llama-2"


# File: PrismQ/Infrastructure/Platform/Providers/mock_provider.py
class MockLLMProvider(ILLMProvider):
    """EXTENSION: Mock for testing - no modification needed."""
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        return "Mock response"
    
    @property
    def model_name(self) -> str:
        return "mock-model"
```

**Why This Works**:
- **Interface is closed**: `ILLMProvider` never changes
- **Implementations are extensions**: Each new provider is a separate class
- **No ripple effects**: Adding `LocalModelProvider` doesn't affect `OpenAIProvider`
- **Easy to test**: Use `MockLLMProvider` in tests

### ❌ Anti-Pattern: Modifying Existing Code

```python
# BAD: Must modify this class for each new provider
class LLMService:
    def __init__(self, provider_type: str):
        self.provider_type = provider_type
    
    def generate(self, prompt: str) -> str:
        # Must modify this method to add new providers!
        if self.provider_type == "openai":
            return self._call_openai(prompt)
        elif self.provider_type == "local":
            return self._call_local(prompt)
        elif self.provider_type == "anthropic":  # Must add this!
            return self._call_anthropic(prompt)  # Must add this!
        # ... more modifications for each new provider
    
    def _call_openai(self, prompt: str) -> str:
        pass
    
    def _call_local(self, prompt: str) -> str:
        pass
    
    def _call_anthropic(self, prompt: str) -> str:  # Must add this!
        pass
```

**Problems**:
- **Violates OCP**: Must modify `LLMService` for each new provider
- **Risk of bugs**: Each modification can break existing functionality
- **Growing complexity**: `generate()` method becomes harder to maintain
- **Tight coupling**: All provider logic in one class

### 🎯 Real-World Application: Platform Providers

Platform providers follow OCP:

```python
# File: PrismQ/Infrastructure/Core/Shared/interfaces/platform_provider.py
class IPlatformProvider(ABC):
    """Interface for platform providers - CLOSED."""
    
    @abstractmethod
    def publish(self, content: dict) -> str:
        """Publish content to platform."""
        pass
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Get platform name."""
        pass


# EXTENSION: YouTube provider
class YouTubeProvider(IPlatformProvider):
    def publish(self, content: dict) -> str:
        # YouTube-specific publishing
        pass
    
    def get_platform_name(self) -> str:
        return "youtube"


# EXTENSION: TikTok provider
class TikTokProvider(IPlatformProvider):
    def publish(self, content: dict) -> str:
        # TikTok-specific publishing
        pass
    
    def get_platform_name(self) -> str:
        return "tiktok"


# EXTENSION: Instagram provider (added later without modifying existing code)
class InstagramProvider(IPlatformProvider):
    def publish(self, content: dict) -> str:
        # Instagram-specific publishing
        pass
    
    def get_platform_name(self) -> str:
        return "instagram"
```

**Benefits**:
- Add new platforms without touching existing code
- Each provider is independent
- Easy to test each platform separately
- Low risk when adding features

### 💡 Key Takeaways

1. **Use Interfaces**: Define contracts that are stable
2. **Extend, Don't Modify**: Add new functionality in new classes
3. **Polymorphism**: Use inheritance and interfaces for variation
4. **Strategy Pattern**: Encapsulate algorithms in separate classes

## Liskov Substitution Principle (LSP)

> **Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.**

Derived classes must be **substitutable** for their base classes.

### ✅ Good Example: Substitutable Providers

All LLM providers can be used interchangeably:

```python
# File: PrismQ/Pipeline/02_TextGeneration/StoryGenerator/script_generator.py
class ScriptGenerator:
    def __init__(self, llm_provider: ILLMProvider):
        # Accepts ANY ILLMProvider implementation
        self.llm = llm_provider
    
    def generate_script(self, topic: str) -> str:
        # Works with ANY provider that implements ILLMProvider
        prompt = f"Generate a script about: {topic}"
        return self.llm.generate_completion(prompt)


# All of these work correctly (LSP satisfied):
# Production
generator1 = ScriptGenerator(OpenAIProvider())
script1 = generator1.generate_script("AI technology")

# Testing
generator2 = ScriptGenerator(MockLLMProvider())
script2 = generator2.generate_script("AI technology")

# Local development
generator3 = ScriptGenerator(LocalModelProvider())
script3 = generator3.generate_script("AI technology")

# All produce valid scripts - LSP satisfied!
```

**Why This Works**:
- All providers implement the same **contract** (`ILLMProvider`)
- Behavior is **consistent** across implementations
- **No surprises**: Each provider does what's expected
- **Fully substitutable**: Can swap providers without code changes

### ❌ Anti-Pattern: Violating LSP

```python
# BAD: Violates LSP
class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class WorkingProvider(BaseLLMProvider):
    def generate(self, prompt: str) -> str:
        return "Generated text"


class BrokenProvider(BaseLLMProvider):
    def generate(self, prompt: str) -> str:
        # Violates LSP: Throws exception instead of generating text
        raise NotImplementedError("This provider doesn't support generation!")


# This breaks LSP:
def generate_content(provider: BaseLLMProvider, prompt: str) -> str:
    # This works with WorkingProvider but fails with BrokenProvider
    # Violates LSP - not truly substitutable!
    return provider.generate(prompt)
```

**Problems**:
- **Unexpected behavior**: `BrokenProvider` doesn't fulfill the contract
- **Runtime errors**: Code that works with `WorkingProvider` fails with `BrokenProvider`
- **Not substitutable**: Can't use `BrokenProvider` where `BaseLLMProvider` is expected

### 🎯 Real-World Application: Pipeline Stages

All pipeline stages are substitutable:

```python
# File: PrismQ/Infrastructure/Core/Shared/interfaces/pipeline_stage.py
class IPipelineStage(ABC, Generic[TInput, TOutput]):
    """All stages follow the same contract."""
    
    @abstractmethod
    async def execute(self, input_data: TInput) -> StageResult[TOutput]:
        """Execute the stage."""
        pass
    
    @abstractmethod
    async def validate_input(self, input_data: TInput) -> bool:
        """Validate input."""
        pass


# File: PrismQ/Infrastructure/Platform/Pipeline/orchestration/pipeline_runner.py
class PipelineRunner:
    def __init__(self, stages: list[IPipelineStage]):
        self.stages = stages
    
    async def run(self, initial_input: Any) -> Any:
        """Run all stages - works with ANY IPipelineStage implementation."""
        current_data = initial_input
        
        for stage in self.stages:
            # LSP: Every stage can be used the same way
            result = await stage.execute(current_data)
            current_data = result.data
        
        return current_data


# All stages are substitutable:
pipeline = PipelineRunner([
    IdeaGenerationStage(),
    TextGenerationStage(),
    AudioGenerationStage(),
    ImageGenerationStage(),
    VideoGenerationStage(),
])
```

**Benefits**:
- Any stage can be replaced with another implementation
- Pipeline orchestration works with any conforming stage
- Easy to add custom stages
- Consistent behavior across all stages

### 💡 Key Takeaways

1. **Honor the Contract**: Derived classes must fulfill base class promises
2. **Consistent Behavior**: Substitutions should not surprise users
3. **No Exceptions**: Don't throw exceptions in derived classes when base doesn't
4. **Same Preconditions**: Don't require more than the base class

## Interface Segregation Principle (ISP)

> **Clients should not be forced to depend on interfaces they do not use.**

Create **focused interfaces** rather than one large interface with many methods.

### ✅ Good Example: Segregated Interfaces

We separate sync and async LLM providers:

```python
# File: PrismQ/Infrastructure/Core/Shared/interfaces/llm_provider.py

# Synchronous interface - for simple use cases
class ILLMProvider(ABC):
    """Synchronous LLM provider - minimal interface."""
    
    @abstractmethod
    def generate_completion(self, prompt: str, **kwargs) -> str:
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        pass


# Asynchronous interface - for high-throughput use cases
class IAsyncLLMProvider(ABC):
    """Asynchronous LLM provider - separate from sync."""
    
    @abstractmethod
    async def generate_completion(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def generate_chat(self, messages: list, **kwargs) -> str:
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        pass


# Clients use only what they need:

# Simple script uses sync interface
class SimpleScriptGenerator:
    def __init__(self, llm: ILLMProvider):
        self.llm = llm  # Only needs sync methods
    
    def generate(self, topic: str) -> str:
        return self.llm.generate_completion(f"Write about: {topic}")


# High-performance pipeline uses async interface
class AsyncPipelineStage:
    def __init__(self, llm: IAsyncLLMProvider):
        self.llm = llm  # Only needs async methods
    
    async def process_batch(self, topics: list[str]) -> list[str]:
        tasks = [self.llm.generate_completion(f"Write about: {t}") for t in topics]
        return await asyncio.gather(*tasks)
```

**Why This Works**:
- **Focused interfaces**: Each interface has only necessary methods
- **No unused dependencies**: Sync clients don't need async methods
- **Easier to implement**: Providers only implement what they support
- **Clear intent**: Interface name indicates capabilities

### ❌ Anti-Pattern: Fat Interface

```python
# BAD: Fat interface forces unnecessary dependencies
class ILLMProvider(ABC):
    """Fat interface - violates ISP!"""
    
    # Sync methods
    @abstractmethod
    def generate_completion(self, prompt: str) -> str:
        pass
    
    # Async methods (not all clients need these!)
    @abstractmethod
    async def generate_completion_async(self, prompt: str) -> str:
        pass
    
    # Streaming (not all clients need this!)
    @abstractmethod
    def generate_stream(self, prompt: str) -> Iterator[str]:
        pass
    
    # Batch processing (not all clients need this!)
    @abstractmethod
    def generate_batch(self, prompts: list[str]) -> list[str]:
        pass
    
    # Fine-tuning (definitely not all clients need this!)
    @abstractmethod
    def fine_tune_model(self, training_data: list) -> str:
        pass
    
    # Model management (most clients don't need this!)
    @abstractmethod
    def list_models(self) -> list[str]:
        pass


# Problems:
# 1. Simple clients must implement ALL methods (or raise NotImplementedError)
# 2. Changes to any method affect all clients
# 3. Hard to understand which methods are actually needed
# 4. Forces unnecessary dependencies
```

### 🎯 Real-World Application: Storage Providers

We segregate storage interfaces:

```python
# File: PrismQ/Infrastructure/Core/Shared/interfaces/storage_provider.py

# Basic storage interface
class IStorageProvider(ABC):
    """Basic storage operations."""
    
    @abstractmethod
    def save(self, path: str, content: bytes) -> None:
        pass
    
    @abstractmethod
    def load(self, path: str) -> bytes:
        pass
    
    @abstractmethod
    def exists(self, path: str) -> bool:
        pass


# Extended interface for advanced features
class ICloudStorageProvider(IStorageProvider):
    """Cloud storage with additional features."""
    
    @abstractmethod
    def get_public_url(self, path: str) -> str:
        pass
    
    @abstractmethod
    def set_permissions(self, path: str, permissions: dict) -> None:
        pass


# Local storage only needs basic interface
class LocalStorageProvider(IStorageProvider):
    def save(self, path: str, content: bytes) -> None:
        with open(path, 'wb') as f:
            f.write(content)
    
    def load(self, path: str) -> bytes:
        with open(path, 'rb') as f:
            return f.read()
    
    def exists(self, path: str) -> bool:
        return os.path.exists(path)
    # No need to implement cloud-specific methods!


# Cloud storage implements both
class S3StorageProvider(ICloudStorageProvider):
    def save(self, path: str, content: bytes) -> None:
        self.s3_client.put_object(Bucket=self.bucket, Key=path, Body=content)
    
    def load(self, path: str) -> bytes:
        response = self.s3_client.get_object(Bucket=self.bucket, Key=path)
        return response['Body'].read()
    
    def exists(self, path: str) -> bool:
        try:
            self.s3_client.head_object(Bucket=self.bucket, Key=path)
            return True
        except:
            return False
    
    def get_public_url(self, path: str) -> str:
        return f"https://{self.bucket}.s3.amazonaws.com/{path}"
    
    def set_permissions(self, path: str, permissions: dict) -> None:
        self.s3_client.put_object_acl(Bucket=self.bucket, Key=path, ACL=permissions['acl'])
```

**Benefits**:
- Local storage doesn't implement unnecessary cloud methods
- Clear separation between basic and advanced features
- Easy to add new storage types
- Clients depend only on what they need

### 💡 Key Takeaways

1. **Small Interfaces**: Keep interfaces focused and minimal
2. **Role-Based**: Create interfaces based on client roles
3. **Composition**: Build complex interfaces from simpler ones
4. **Single Purpose**: Each interface should serve one client type

## Dependency Inversion Principle (DIP)

> **High-level modules should not depend on low-level modules. Both should depend on abstractions.**

Depend on **interfaces**, not **concrete implementations**.

### ✅ Good Example: Dependency Injection

Our components depend on abstractions:

```python
# File: PrismQ/Pipeline/02_TextGeneration/StoryGenerator/script_generator.py

# High-level module depends on abstraction
class ScriptGenerator:
    def __init__(
        self,
        llm_provider: ILLMProvider,  # Abstraction, not OpenAIProvider!
        cache_service: ICacheService,  # Abstraction, not RedisCache!
        logger: ILogger  # Abstraction, not ConsoleLogger!
    ):
        self.llm = llm_provider
        self.cache = cache_service
        self.logger = logger
    
    def generate_script(self, topic: str) -> str:
        # Check cache
        cached = self.cache.get(f"script:{topic}")
        if cached:
            self.logger.log_info(f"Cache hit for topic: {topic}")
            return cached
        
        # Generate new script
        self.logger.log_info(f"Generating script for topic: {topic}")
        script = self.llm.generate_completion(f"Write a script about: {topic}")
        
        # Cache result
        self.cache.set(f"script:{topic}", script)
        return script


# Production configuration
production_generator = ScriptGenerator(
    llm_provider=OpenAIProvider(api_key="sk-..."),
    cache_service=RedisCache(host="localhost"),
    logger=CloudLogger(project_id="prod")
)

# Testing configuration
test_generator = ScriptGenerator(
    llm_provider=MockLLMProvider(),
    cache_service=InMemoryCache(),
    logger=ConsoleLogger()
)

# Local development configuration
dev_generator = ScriptGenerator(
    llm_provider=LocalModelProvider(),
    cache_service=FileCache(path="/tmp/cache"),
    logger=FileLogger(path="/var/log/app.log")
)
```

**Why This Works**:
- **High-level module** (`ScriptGenerator`) doesn't know about concrete implementations
- **Abstractions** (`ILLMProvider`, `ICacheService`, `ILogger`) are stable
- **Easy to swap**: Change implementations without modifying `ScriptGenerator`
- **Testable**: Use mocks in tests, real implementations in production

### ❌ Anti-Pattern: Direct Dependencies

```python
# BAD: High-level module depends on concrete implementations
class ScriptGenerator:
    def __init__(self):
        # Direct dependencies on concrete classes!
        self.llm = OpenAIProvider(api_key="sk-...")  # Hard-coded!
        self.cache = RedisCache(host="localhost")  # Hard-coded!
        self.logger = CloudLogger(project_id="prod")  # Hard-coded!
    
    def generate_script(self, topic: str) -> str:
        # Hard to test - must connect to real OpenAI, Redis, Cloud!
        cached = self.cache.get(f"script:{topic}")
        if cached:
            self.logger.log_info(f"Cache hit: {topic}")
            return cached
        
        script = self.llm.generate_completion(f"Write about: {topic}")
        self.cache.set(f"script:{topic}", script)
        return script
```

**Problems**:
- **Tight coupling**: Can't change providers without modifying class
- **Hard to test**: Must mock OpenAI, Redis, and Cloud services
- **No flexibility**: Can't use different implementations in different environments
- **Violates DIP**: High-level module depends on low-level implementations

### 🎯 Real-World Application: Pipeline Orchestration

Pipeline orchestration uses DIP:

```python
# File: PrismQ/Infrastructure/Platform/Pipeline/orchestration/pipeline_runner.py

class PipelineOrchestrator:
    """High-level orchestration depends on abstractions."""
    
    def __init__(
        self,
        stages: list[IPipelineStage],  # Abstraction!
        storage: IStorageProvider,  # Abstraction!
        logger: ILogger,  # Abstraction!
        metrics: IMetricsCollector  # Abstraction!
    ):
        self.stages = stages
        self.storage = storage
        self.logger = logger
        self.metrics = metrics
    
    async def run_pipeline(self, input_data: dict) -> dict:
        """Run all stages - depends only on abstractions."""
        current_data = input_data
        
        for stage in self.stages:
            self.logger.log_info(f"Running stage: {stage.stage_name}")
            self.metrics.increment(f"stage.{stage.stage_id}.started")
            
            result = await stage.execute(current_data)
            
            # Save intermediate results
            self.storage.save(
                f"stage_{stage.stage_id}_output.json",
                json.dumps(result.data).encode()
            )
            
            self.metrics.increment(f"stage.{stage.stage_id}.completed")
            current_data = result.data
        
        return current_data


# Production setup with real implementations
prod_orchestrator = PipelineOrchestrator(
    stages=[
        IdeaGenerationStage(llm=OpenAIProvider()),
        TextGenerationStage(llm=OpenAIProvider()),
        AudioGenerationStage(voice=ElevenLabsProvider()),
        VideoGenerationStage(renderer=FFmpegRenderer()),
    ],
    storage=S3StorageProvider(bucket="prod-videos"),
    logger=CloudLogger(project="prod"),
    metrics=PrometheusMetrics()
)

# Testing setup with mocks
test_orchestrator = PipelineOrchestrator(
    stages=[
        MockIdeaStage(),
        MockTextStage(),
        MockAudioStage(),
        MockVideoStage(),
    ],
    storage=InMemoryStorage(),
    logger=ConsoleLogger(),
    metrics=NoOpMetrics()
)
```

**Benefits**:
- Orchestrator doesn't depend on concrete implementations
- Easy to test with mock stages
- Flexible configuration for different environments
- Clear separation of concerns

### 💡 Key Takeaways

1. **Depend on Abstractions**: Use interfaces, not concrete classes
2. **Inject Dependencies**: Pass dependencies through constructor
3. **Inversion of Control**: Let caller decide implementations
4. **Testability**: Easy to substitute mocks in tests

## SOLID in Action: Real Examples

### Example 1: Adding a New LLM Provider

Following SOLID principles makes it easy to add new providers:

```python
# Step 1: Implement the interface (OCP, LSP)
class AnthropicProvider(ILLMProvider):
    def __init__(self, api_key: str):
        self.client = anthropic.Client(api_key)
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        return self.client.completions.create(
            prompt=prompt,
            model="claude-2",
            **kwargs
        ).completion
    
    @property
    def model_name(self) -> str:
        return "claude-2"


# Step 2: Use it anywhere ILLMProvider is expected (DIP)
generator = ScriptGenerator(
    llm_provider=AnthropicProvider(api_key="sk-ant-...")
)

# No modifications to ScriptGenerator needed!
script = generator.generate_script("AI ethics")
```

### Example 2: Testing with Mocks

SOLID principles make testing easy:

```python
# Mock provider for testing
class MockLLMProvider(ILLMProvider):
    def __init__(self, responses: dict):
        self.responses = responses
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        return self.responses.get(prompt, "Default response")
    
    @property
    def model_name(self) -> str:
        return "mock"


# Test with predictable responses
def test_script_generator():
    mock_llm = MockLLMProvider({
        "Write a script about: AI": "Mock AI script"
    })
    
    generator = ScriptGenerator(llm_provider=mock_llm)
    result = generator.generate_script("AI")
    
    assert result == "Mock AI script"
```

### Example 3: Composing Pipeline Stages

SOLID enables flexible composition:

```python
# Different pipelines for different use cases
def create_youtube_pipeline() -> PipelineOrchestrator:
    return PipelineOrchestrator(
        stages=[
            IdeaGenerationStage(),
            LongFormTextStage(),  # YouTube needs longer content
            VoiceOverStage(),
            HighResImageStage(),  # YouTube supports high res
            VideoAssemblyStage(),
        ]
    )


def create_tiktok_pipeline() -> PipelineOrchestrator:
    return PipelineOrchestrator(
        stages=[
            IdeaGenerationStage(),
            ShortFormTextStage(),  # TikTok needs short content
            VoiceOverStage(),
            MobileImageStage(),  # Optimized for mobile
            ShortVideoStage(),  # 60 second limit
        ]
    )


# Same orchestrator works with different stage configurations!
```

## Best Practices

### 1. Start with Interfaces

Define interfaces **before** implementations:

```python
# Define contract first
class IContentGenerator(ABC):
    @abstractmethod
    def generate(self, input_data: dict) -> str:
        pass

# Then implement
class AIContentGenerator(IContentGenerator):
    def generate(self, input_data: dict) -> str:
        # Implementation
        pass
```

### 2. Use Dependency Injection

Inject dependencies through constructors:

```python
# Good: Dependencies injected
class MyService:
    def __init__(self, logger: ILogger, storage: IStorage):
        self.logger = logger
        self.storage = storage

# Avoid: Dependencies created internally
class MyService:
    def __init__(self):
        self.logger = FileLogger()  # Hard-coded!
        self.storage = S3Storage()  # Hard-coded!
```

### 3. Keep Interfaces Small

Create focused, role-based interfaces:

```python
# Good: Focused interfaces
class IReader(ABC):
    @abstractmethod
    def read(self, path: str) -> bytes:
        pass

class IWriter(ABC):
    @abstractmethod
    def write(self, path: str, content: bytes) -> None:
        pass

# Implement what you need
class ReadOnlyStorage(IReader):
    def read(self, path: str) -> bytes:
        pass

class FullStorage(IReader, IWriter):
    def read(self, path: str) -> bytes:
        pass
    
    def write(self, path: str, content: bytes) -> None:
        pass
```

### 4. Favor Composition Over Inheritance

```python
# Good: Composition
class ScriptGenerator:
    def __init__(self, llm: ILLMProvider, validator: IValidator):
        self.llm = llm
        self.validator = validator

# Avoid: Deep inheritance hierarchies
class BaseGenerator:
    pass

class TextGenerator(BaseGenerator):
    pass

class ScriptGenerator(TextGenerator):
    pass
```

## Anti-Patterns to Avoid

### 1. God Classes

Avoid classes that do everything:

```python
# BAD: God class
class ApplicationManager:
    def generate_content(self): pass
    def save_to_database(self): pass
    def send_email(self): pass
    def process_video(self): pass
    def handle_payments(self): pass
    # ... 50 more methods
```

**Fix**: Split into focused classes following SRP.

### 2. Tight Coupling

Avoid direct dependencies on concrete classes:

```python
# BAD: Tight coupling
class MyService:
    def __init__(self):
        self.db = PostgreSQLDatabase()  # Concrete!
        self.api = OpenAIAPI()  # Concrete!

# Good: Loose coupling
class MyService:
    def __init__(self, db: IDatabase, api: ILLMProvider):
        self.db = db
        self.api = api
```

### 3. Leaky Abstractions

Interfaces should hide implementation details:

```python
# BAD: Leaky abstraction
class IStorageProvider(ABC):
    @abstractmethod
    def get_s3_client(self):  # Exposes S3!
        pass

# Good: Clean abstraction
class IStorageProvider(ABC):
    @abstractmethod
    def save(self, path: str, content: bytes) -> None:
        pass
```

### 4. Feature Envy

Methods that use more data from another class than their own:

```python
# BAD: Feature envy
class TitleGenerator:
    def score_title(self, scorer: TitleScorer, title: str) -> float:
        # Uses scorer's data more than own data
        return (
            scorer.check_length(title) +
            scorer.check_keywords(title) +
            scorer.check_appeal(title)
        ) / 3

# Good: Let TitleScorer do its job
class TitleGenerator:
    def score_title(self, scorer: TitleScorer, title: str) -> float:
        return scorer.score(title)  # Delegate to scorer
```

## Summary

SOLID principles work together to create:
- **Maintainable**: Easy to modify and extend
- **Testable**: Components can be tested in isolation
- **Flexible**: Easy to swap implementations
- **Understandable**: Clear responsibilities and relationships
- **Reusable**: Components work in different contexts

### Quick Reference

| Principle | Key Question | Solution |
|-----------|--------------|----------|
| **SRP** | Does this class have multiple reasons to change? | Split into focused classes |
| **OCP** | Do I need to modify existing code to add features? | Use interfaces and inheritance |
| **LSP** | Can I substitute derived classes without breaking code? | Ensure derived classes honor base class contracts |
| **ISP** | Do clients depend on methods they don't use? | Create small, focused interfaces |
| **DIP** | Does high-level code depend on low-level details? | Depend on abstractions, inject dependencies |

---

**Related Documentation**:
- [REPOSITORY_OVERVIEW.md](./REPOSITORY_OVERVIEW.md) - Overall architecture
- [PROJECT_SPLITTING_GUIDE.md](./PROJECT_SPLITTING_GUIDE.md) - How to extract components
- [REFERENCE_GUIDE_FOR_SMALL_PROJECTS.md](./REFERENCE_GUIDE_FOR_SMALL_PROJECTS.md) - Quick reference

**Last Updated**: October 2025
