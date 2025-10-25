# Reference Guide for Small Projects

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [SOLID Principles Cheat Sheet](#solid-principles-cheat-sheet)
- [Common Patterns](#common-patterns)
- [Code Templates](#code-templates)
- [Architecture Decision Guide](#architecture-decision-guide)
- [Best Practices Summary](#best-practices-summary)
- [Troubleshooting Quick Reference](#troubleshooting-quick-reference)

## Quick Start

### 30-Second Overview

**StoryGenerator** is a reference implementation showing how to build modular, SOLID-compliant systems. Use it to:

1. ✅ **Learn SOLID principles** - See real-world examples
2. ✅ **Extract components** - Take what you need for smaller projects
3. ✅ **Follow patterns** - Copy proven architecture patterns
4. ✅ **Avoid mistakes** - See anti-patterns and how to fix them

### 5-Minute Quick Reference

**Key Concepts**:
- **Pipeline Architecture**: Sequential stages (Idea → Text → Audio → Image → Video)
- **Interface-Based Design**: Depend on abstractions, not implementations
- **Dependency Injection**: Pass dependencies through constructors
- **Single Responsibility**: Each class does one thing well

**Most Useful Components to Extract**:
1. **Title Scorer** - Simple, no dependencies
2. **LLM Provider Interface** - Swap between OpenAI, local models, etc.
3. **Retry Logic** - Reusable error handling
4. **Pipeline Stage Interface** - Build your own pipelines

## SOLID Principles Cheat Sheet

### Quick Reference Table

| Principle | Question to Ask | How to Fix |
|-----------|----------------|------------|
| **Single Responsibility** | Does this class have multiple reasons to change? | Split into separate classes |
| **Open/Closed** | Must I modify existing code to add features? | Use interfaces and inheritance |
| **Liskov Substitution** | Can I swap implementations without breaking? | Ensure implementations honor contracts |
| **Interface Segregation** | Do clients depend on methods they don't use? | Create smaller, focused interfaces |
| **Dependency Inversion** | Does high-level code depend on low-level details? | Depend on interfaces, inject dependencies |

### One-Line Summaries

```python
# Single Responsibility Principle (SRP)
# One class = One responsibility = One reason to change
class TitleScorer:  # ✅ Only scores titles
    def score(self, title: str) -> float: pass

class TitleGenerator:  # ✅ Only generates titles
    def generate(self, topic: str) -> str: pass


# Open/Closed Principle (OCP)
# Open for extension, closed for modification
class ILLMProvider(ABC):  # ✅ Interface never changes
    @abstractmethod
    def generate(self, prompt: str) -> str: pass

class OpenAIProvider(ILLMProvider):  # ✅ Extension, not modification
    def generate(self, prompt: str) -> str: pass


# Liskov Substitution Principle (LSP)
# Derived classes must be substitutable for base classes
def process(provider: ILLMProvider):  # ✅ Works with any provider
    return provider.generate("prompt")


# Interface Segregation Principle (ISP)
# Don't force clients to depend on unused methods
class IReader(ABC):  # ✅ Small, focused interface
    @abstractmethod
    def read(self, path: str) -> bytes: pass

class IWriter(ABC):  # ✅ Separate interface
    @abstractmethod
    def write(self, path: str, data: bytes) -> None: pass


# Dependency Inversion Principle (DIP)
# Depend on abstractions, not concretions
class Service:
    def __init__(self, provider: ILLMProvider):  # ✅ Depends on interface
        self.provider = provider
```

## Common Patterns

### Pattern 1: Provider Pattern (Most Common)

**Use When**: You need to swap implementations (e.g., different APIs, services)

**Template**:

```python
# 1. Define interface
from abc import ABC, abstractmethod

class IDataProvider(ABC):
    @abstractmethod
    def fetch_data(self, query: str) -> dict:
        """Fetch data from source."""
        pass

# 2. Implement providers
class APIProvider(IDataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def fetch_data(self, query: str) -> dict:
        # Call real API
        return {"data": "from API"}

class MockProvider(IDataProvider):
    def fetch_data(self, query: str) -> dict:
        # Return mock data for testing
        return {"data": "mock data"}

# 3. Use via dependency injection
class DataService:
    def __init__(self, provider: IDataProvider):
        self.provider = provider  # Depends on interface
    
    def get_data(self, query: str) -> dict:
        return self.provider.fetch_data(query)

# 4. Configure for different environments
# Production
service = DataService(APIProvider(api_key="sk-..."))

# Testing
service = DataService(MockProvider())
```

**Examples in StoryGenerator**:
- `ILLMProvider` - Swap between OpenAI, Anthropic, local models
- `IPlatformProvider` - Swap between YouTube, TikTok, Instagram
- `IStorageProvider` - Swap between S3, local storage, in-memory

### Pattern 2: Pipeline/Chain Pattern

**Use When**: You need sequential processing steps

**Template**:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TInput = TypeVar('TInput')
TOutput = TypeVar('TOutput')

# 1. Define stage interface
class IPipelineStage(ABC, Generic[TInput, TOutput]):
    @abstractmethod
    def execute(self, input_data: TInput) -> TOutput:
        """Execute this stage."""
        pass

# 2. Implement stages
class ValidationStage(IPipelineStage[dict, dict]):
    def execute(self, input_data: dict) -> dict:
        # Validate input
        if not input_data.get("required_field"):
            raise ValueError("Missing required field")
        return input_data

class TransformStage(IPipelineStage[dict, dict]):
    def execute(self, input_data: dict) -> dict:
        # Transform data
        return {
            **input_data,
            "transformed": True
        }

class OutputStage(IPipelineStage[dict, str]):
    def execute(self, input_data: dict) -> str:
        # Generate output
        return f"Result: {input_data}"

# 3. Create pipeline runner
class Pipeline:
    def __init__(self, stages: list[IPipelineStage]):
        self.stages = stages
    
    def run(self, initial_input):
        current_data = initial_input
        for stage in self.stages:
            current_data = stage.execute(current_data)
        return current_data

# 4. Use pipeline
pipeline = Pipeline([
    ValidationStage(),
    TransformStage(),
    OutputStage()
])

result = pipeline.run({"required_field": "value"})
```

**Examples in StoryGenerator**:
- 5-stage content pipeline (Idea → Text → Audio → Image → Video)
- Each stage is independently testable
- Easy to add/remove/reorder stages

### Pattern 3: Repository Pattern

**Use When**: You need to abstract data access

**Template**:

```python
from abc import ABC, abstractmethod
from typing import Optional, List

# 1. Define entity
class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

# 2. Define repository interface
class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def save(self, user: User) -> None:
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
    
    @abstractmethod
    def find_all(self) -> List[User]:
        pass

# 3. Implement repositories
class SQLUserRepository(IUserRepository):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        # SQL query
        row = self.db.query("SELECT * FROM users WHERE id = ?", user_id)
        return User(**row) if row else None
    
    def save(self, user: User) -> None:
        # SQL insert/update
        pass
    
    def delete(self, user_id: int) -> None:
        # SQL delete
        pass
    
    def find_all(self) -> List[User]:
        # SQL query
        pass

class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)
    
    def save(self, user: User) -> None:
        if user.id == 0:
            user.id = self.next_id
            self.next_id += 1
        self.users[user.id] = user
    
    def delete(self, user_id: int) -> None:
        self.users.pop(user_id, None)
    
    def find_all(self) -> List[User]:
        return list(self.users.values())

# 4. Use via dependency injection
class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository
    
    def register_user(self, name: str, email: str) -> User:
        user = User(id=0, name=name, email=email)
        self.repository.save(user)
        return user

# Production: Use SQL
service = UserService(SQLUserRepository(db_connection))

# Testing: Use in-memory
service = UserService(InMemoryUserRepository())
```

**Examples in StoryGenerator**:
- `StoryDatabase` - Abstract database access
- Swap between SQLite, PostgreSQL, in-memory

### Pattern 4: Strategy Pattern

**Use When**: You have multiple algorithms for same task

**Template**:

```python
from abc import ABC, abstractmethod

# 1. Define strategy interface
class IScoringStrategy(ABC):
    @abstractmethod
    def calculate_score(self, data: dict) -> float:
        pass

# 2. Implement strategies
class SimpleScoringStrategy(IScoringStrategy):
    def calculate_score(self, data: dict) -> float:
        # Simple scoring algorithm
        return len(data.get("content", "")) / 100.0

class AdvancedScoringStrategy(IScoringStrategy):
    def calculate_score(self, data: dict) -> float:
        # Advanced scoring with multiple factors
        score = 0.0
        score += self._score_length(data)
        score += self._score_keywords(data)
        score += self._score_sentiment(data)
        return score / 3.0
    
    def _score_length(self, data: dict) -> float:
        # Length scoring logic
        pass
    
    def _score_keywords(self, data: dict) -> float:
        # Keyword scoring logic
        pass
    
    def _score_sentiment(self, data: dict) -> float:
        # Sentiment scoring logic
        pass

# 3. Use strategy
class ContentScorer:
    def __init__(self, strategy: IScoringStrategy):
        self.strategy = strategy
    
    def score_content(self, content: dict) -> float:
        return self.strategy.calculate_score(content)
    
    def set_strategy(self, strategy: IScoringStrategy) -> None:
        """Change strategy at runtime."""
        self.strategy = strategy

# 4. Configure
# Use simple strategy for drafts
scorer = ContentScorer(SimpleScoringStrategy())
draft_score = scorer.score_content({"content": "Draft text"})

# Switch to advanced for production
scorer.set_strategy(AdvancedScoringStrategy())
final_score = scorer.score_content({"content": "Final text"})
```

**Examples in StoryGenerator**:
- Title scoring strategies
- Content ranking algorithms
- Video synthesis methods

## Code Templates

### Template 1: Basic Service with Dependency Injection

```python
"""
My Service Module

Description of what this service does.
"""
from abc import ABC, abstractmethod
from typing import Optional


# 1. Define dependencies as interfaces
class IDependency(ABC):
    @abstractmethod
    def do_something(self, data: str) -> str:
        """Do something with data."""
        pass


# 2. Create service with injected dependencies
class MyService:
    """Service description."""
    
    def __init__(
        self,
        dependency: IDependency,
        optional_param: str = "default"
    ):
        """
        Initialize service.
        
        Args:
            dependency: The required dependency
            optional_param: Optional configuration
        """
        self.dependency = dependency
        self.optional_param = optional_param
    
    def process(self, input_data: str) -> str:
        """
        Process input data.
        
        Args:
            input_data: Data to process
            
        Returns:
            Processed result
            
        Raises:
            ValueError: If input is invalid
        """
        # Validate input
        if not input_data:
            raise ValueError("Input cannot be empty")
        
        # Use dependency
        result = self.dependency.do_something(input_data)
        
        # Process and return
        return f"{self.optional_param}: {result}"


# 3. Create concrete implementation
class ConcreteDependency(IDependency):
    def do_something(self, data: str) -> str:
        return f"Processed: {data}"


# 4. Usage
if __name__ == "__main__":
    # Production
    dependency = ConcreteDependency()
    service = MyService(dependency, optional_param="prod")
    result = service.process("test data")
    print(result)
```

### Template 2: Provider with Interface

```python
"""
Provider Interface and Implementation

Example of provider pattern for external service integration.
"""
from abc import ABC, abstractmethod
from typing import Optional


# 1. Define provider interface
class IExternalProvider(ABC):
    """Interface for external service providers."""
    
    @abstractmethod
    def fetch(self, query: str) -> dict:
        """
        Fetch data from external service.
        
        Args:
            query: Search query
            
        Returns:
            Result data
            
        Raises:
            ProviderError: If fetch fails
        """
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get provider name."""
        pass


# 2. Create concrete provider
class RealProvider(IExternalProvider):
    """Real provider implementation."""
    
    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize provider.
        
        Args:
            api_key: API authentication key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
    
    def fetch(self, query: str) -> dict:
        """Fetch from real API."""
        # Real API call here
        return {
            "query": query,
            "results": ["result1", "result2"]
        }
    
    @property
    def provider_name(self) -> str:
        return "real-provider"


# 3. Create mock provider for testing
class MockProvider(IExternalProvider):
    """Mock provider for testing."""
    
    def __init__(self, mock_data: Optional[dict] = None):
        self.mock_data = mock_data or {"results": ["mock"]}
    
    def fetch(self, query: str) -> dict:
        """Return mock data."""
        return self.mock_data
    
    @property
    def provider_name(self) -> str:
        return "mock-provider"


# 4. Usage
def process_data(provider: IExternalProvider, query: str):
    """Process data using any provider."""
    print(f"Using provider: {provider.provider_name}")
    data = provider.fetch(query)
    return data


if __name__ == "__main__":
    # Production
    real_provider = RealProvider(api_key="sk-...")
    result = process_data(real_provider, "search query")
    
    # Testing
    mock_provider = MockProvider({"results": ["test1", "test2"]})
    test_result = process_data(mock_provider, "test query")
```

### Template 3: Pipeline Stage

```python
"""
Pipeline Stage Template

Example of pipeline stage following IPipelineStage interface.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar


# 1. Define types
TInput = TypeVar('TInput')
TOutput = TypeVar('TOutput')


@dataclass
class StageResult(Generic[TOutput]):
    """Result from stage execution."""
    data: TOutput
    success: bool
    error_message: str = ""


# 2. Define stage interface
class IPipelineStage(ABC, Generic[TInput, TOutput]):
    """Interface for pipeline stages."""
    
    @property
    @abstractmethod
    def stage_name(self) -> str:
        """Get stage name."""
        pass
    
    @abstractmethod
    def execute(self, input_data: TInput) -> StageResult[TOutput]:
        """Execute stage."""
        pass
    
    @abstractmethod
    def validate_input(self, input_data: TInput) -> bool:
        """Validate input data."""
        pass


# 3. Implement concrete stage
class MyProcessingStage(IPipelineStage[dict, dict]):
    """Example processing stage."""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
    
    @property
    def stage_name(self) -> str:
        return "MyProcessingStage"
    
    def validate_input(self, input_data: dict) -> bool:
        """Validate input has required fields."""
        required_fields = ["field1", "field2"]
        return all(field in input_data for field in required_fields)
    
    def execute(self, input_data: dict) -> StageResult[dict]:
        """Execute processing logic."""
        # Validate
        if not self.validate_input(input_data):
            return StageResult(
                data={},
                success=False,
                error_message="Invalid input data"
            )
        
        try:
            # Process
            output_data = {
                **input_data,
                "processed": True,
                "stage": self.stage_name
            }
            
            return StageResult(
                data=output_data,
                success=True
            )
        
        except Exception as e:
            return StageResult(
                data={},
                success=False,
                error_message=str(e)
            )


# 4. Create pipeline
class SimplePipeline:
    """Simple pipeline runner."""
    
    def __init__(self, stages: list[IPipelineStage]):
        self.stages = stages
    
    def run(self, input_data):
        """Run all stages."""
        current_data = input_data
        
        for stage in self.stages:
            print(f"Running stage: {stage.stage_name}")
            result = stage.execute(current_data)
            
            if not result.success:
                print(f"Stage failed: {result.error_message}")
                return None
            
            current_data = result.data
        
        return current_data


# 5. Usage
if __name__ == "__main__":
    pipeline = SimplePipeline([
        MyProcessingStage({"option": "value"}),
        # Add more stages here
    ])
    
    result = pipeline.run({
        "field1": "value1",
        "field2": "value2"
    })
    
    print(f"Final result: {result}")
```

### Template 4: Complete Module with Tests

```python
# my_module.py
"""
My Module

Complete example with interface, implementation, and documentation.
"""
from abc import ABC, abstractmethod
from typing import Optional


class IProcessor(ABC):
    """Interface for processors."""
    
    @abstractmethod
    def process(self, data: str) -> str:
        """Process data."""
        pass


class TextProcessor(IProcessor):
    """Process text data."""
    
    def __init__(self, uppercase: bool = False):
        """
        Initialize processor.
        
        Args:
            uppercase: Whether to convert to uppercase
        """
        self.uppercase = uppercase
    
    def process(self, data: str) -> str:
        """
        Process text data.
        
        Args:
            data: Input text
            
        Returns:
            Processed text
            
        Raises:
            ValueError: If data is empty
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        result = data.strip()
        if self.uppercase:
            result = result.upper()
        
        return result


# test_my_module.py
"""Tests for my_module."""
import pytest
from my_module import TextProcessor


def test_process_basic():
    """Test basic processing."""
    processor = TextProcessor()
    result = processor.process("  hello  ")
    assert result == "hello"


def test_process_uppercase():
    """Test uppercase conversion."""
    processor = TextProcessor(uppercase=True)
    result = processor.process("hello")
    assert result == "HELLO"


def test_process_empty_raises_error():
    """Test that empty data raises error."""
    processor = TextProcessor()
    with pytest.raises(ValueError):
        processor.process("")


def test_processor_implements_interface():
    """Test that processor implements IProcessor."""
    from my_module import IProcessor
    processor = TextProcessor()
    assert isinstance(processor, IProcessor)
```

## Architecture Decision Guide

### Decision Tree for Component Design

```
Need to add new functionality?
├─ Is it a new external service integration?
│  └─ Yes → Create Provider (IProvider interface + implementations)
│
├─ Is it a processing step in a sequence?
│  └─ Yes → Create Pipeline Stage (IPipelineStage)
│
├─ Is it a reusable utility?
│  └─ Yes → Create Service class (injected dependencies)
│
├─ Is it data access?
│  └─ Yes → Create Repository (IRepository interface)
│
└─ Is it an algorithm that might change?
   └─ Yes → Create Strategy (IStrategy interface)
```

### When to Use Each Pattern

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Provider** | External service integration | API clients, database connections |
| **Pipeline** | Sequential processing | Data transformation, content creation |
| **Repository** | Data access | CRUD operations, database queries |
| **Strategy** | Swappable algorithms | Sorting, scoring, validation |
| **Factory** | Object creation logic | Creating different types based on config |
| **Decorator** | Adding behavior dynamically | Logging, caching, retry logic |

### Dependency Injection Decision

```
Should I inject this dependency?
├─ Is it an external service?        → YES (inject)
├─ Is it configurable?                → YES (inject)
├─ Does it need different implementations? → YES (inject)
├─ Do I need to mock it in tests?    → YES (inject)
├─ Is it a simple value type?        → NO (pass as parameter)
└─ Is it a constant?                  → NO (use directly)
```

## Best Practices Summary

### Code Organization

```python
my_project/
├── my_package/
│   ├── __init__.py           # Package exports
│   ├── interfaces/           # Abstract interfaces
│   │   └── providers.py
│   ├── providers/            # Concrete implementations
│   │   ├── real_provider.py
│   │   └── mock_provider.py
│   ├── services/             # Business logic
│   │   └── my_service.py
│   └── utils/                # Utilities
│       ├── logging.py
│       └── validation.py
├── tests/                    # Tests mirror src structure
│   ├── test_providers.py
│   └── test_services.py
├── examples/                 # Usage examples
│   └── basic_usage.py
├── requirements.txt          # Dependencies
├── setup.py                  # Package setup
└── README.md                 # Documentation
```

### Naming Conventions

```python
# Interfaces start with 'I'
class ILLMProvider(ABC): pass

# Abstract base classes start with 'Base' or 'Abstract'
class BaseProvider(ABC): pass

# Concrete implementations are descriptive
class OpenAIProvider(ILLMProvider): pass

# Services end with 'Service'
class AuthenticationService: pass

# Repositories end with 'Repository'
class UserRepository: pass

# Managers end with 'Manager'
class ConnectionManager: pass
```

### Testing Best Practices

```python
# 1. Test file naming: test_<module>.py
# test_title_scorer.py

# 2. Test class naming: Test<ClassName>
class TestTitleScorer:
    pass

# 3. Test method naming: test_<what>_<condition>_<expected>
def test_score_title_empty_string_raises_error():
    pass

def test_score_title_optimal_length_returns_high_score():
    pass

# 4. Use fixtures for common setup
@pytest.fixture
def scorer():
    return TitleScorer()

def test_something(scorer):
    # Use scorer fixture
    pass

# 5. Test interfaces with all implementations
@pytest.mark.parametrize("provider_class", [
    OpenAIProvider,
    AnthropicProvider,
    LocalProvider
])
def test_all_providers_implement_interface(provider_class):
    provider = provider_class()
    assert isinstance(provider, ILLMProvider)
```

### Documentation Best Practices

```python
class MyService:
    """
    One-line summary.
    
    Detailed description of what this class does, when to use it,
    and any important considerations.
    
    Attributes:
        dependency: Description of dependency
        config: Description of configuration
    
    Example:
        >>> service = MyService(dependency=MyDependency())
        >>> result = service.process("data")
        >>> print(result)
        'Processed: data'
    """
    
    def __init__(self, dependency: IDependency, config: dict = None):
        """
        Initialize service.
        
        Args:
            dependency: Required dependency for processing
            config: Optional configuration dict
        
        Raises:
            ValueError: If dependency is None
        """
        if dependency is None:
            raise ValueError("Dependency is required")
        
        self.dependency = dependency
        self.config = config or {}
    
    def process(self, data: str) -> str:
        """
        Process input data.
        
        This method validates input, processes it using the dependency,
        and returns the result.
        
        Args:
            data: Input data to process
        
        Returns:
            Processed result string
        
        Raises:
            ValueError: If data is empty or invalid
            ProcessingError: If processing fails
        
        Example:
            >>> service.process("test")
            'Processed: test'
        """
        pass
```

## Troubleshooting Quick Reference

### Common Issues and Solutions

| Problem | Quick Fix |
|---------|-----------|
| `ModuleNotFoundError` | Check imports, install dependencies |
| Circular imports | Extract common interface to separate file |
| Can't mock dependency | Use dependency injection |
| Tests are slow | Use mocks instead of real services |
| Hard to change implementation | Depend on interface, not concrete class |
| Class has too many methods | Split by responsibility (SRP) |
| Must modify code to add feature | Use interfaces and inheritance (OCP) |
| Can't swap implementations | Use dependency injection (DIP) |

### Quick Debugging Commands

```bash
# Check imports
python -c "import my_module; print(my_module.__file__)"

# List all dependencies
pipdeptree -p my_package

# Run specific test
pytest tests/test_my_module.py::test_specific_function -v

# Check code coverage
pytest --cov=my_package --cov-report=term-missing

# Type check
mypy my_package/

# Lint check
flake8 my_package/
black --check my_package/
```

## Summary

### Key Takeaways

1. **Always use interfaces** for dependencies
2. **Inject dependencies** through constructors
3. **Keep classes focused** on single responsibility
4. **Write tests first** or alongside code
5. **Document with examples** for clarity
6. **Extract what you need** from StoryGenerator
7. **Follow naming conventions** for consistency

### Quick Links

- **Full Repository Overview**: [REPOSITORY_OVERVIEW.md](./REPOSITORY_OVERVIEW.md)
- **SOLID Implementation Details**: [SOLID_PRINCIPLES_IMPLEMENTATION.md](./SOLID_PRINCIPLES_IMPLEMENTATION.md)
- **Component Extraction Guide**: [PROJECT_SPLITTING_GUIDE.md](./PROJECT_SPLITTING_GUIDE.md)
- **Complete Documentation**: [PrismQ/Development/Documentation/INDEX.md](./PrismQ/Development/Documentation/INDEX.md)

### Next Steps

1. **Learn**: Read SOLID_PRINCIPLES_IMPLEMENTATION.md
2. **Explore**: Browse StoryGenerator codebase
3. **Extract**: Follow PROJECT_SPLITTING_GUIDE.md
4. **Build**: Use templates and patterns from this guide
5. **Contribute**: Share improvements back to the project

---

**Last Updated**: October 2025  
**Repository**: [StoryGenerator](https://github.com/Nomoos/StoryGenerator)
