# Test-Driven Development (TDD) Guide

## Overview

This guide provides practical examples and best practices for Test-Driven Development in the StoryGenerator project.

## Table of Contents

- [Python TDD](#python-tdd)
- [C# TDD](#c-tdd)
- [Running Tests](#running-tests)
- [Coverage Reports](#coverage-reports)
- [Best Practices](#best-practices)

---

## Python TDD

### Setup

The project uses pytest as the testing framework with the following tools:

- **pytest**: Test runner and framework
- **pytest-cov**: Coverage reporting
- **pytest-xdist**: Parallel test execution
- **pytest-mock**: Mocking utilities
- **black**: Code formatting
- **ruff**: Linting
- **mypy**: Type checking

### Installation

```bash
pip install -r requirements-dev.txt
```

### Running Python Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_tdd_example.py

# Run tests in parallel
pytest -n auto

# Run only unit tests
pytest -m unit

# Run with verbose output
pytest -v
```

### Python Test Structure

```python
import pytest
from typing import List

# Production code
class Calculator:
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

# Test class
class TestCalculator:
    """Test suite for Calculator."""
    
    def test_add_positive_numbers(self):
        """Test adding positive numbers."""
        calc = Calculator()
        assert calc.add(2, 3) == 5
    
    @pytest.mark.parametrize("a,b,expected", [
        (0, 0, 0),
        (1, 2, 3),
        (-1, 1, 0),
    ])
    def test_add_parameterized(self, a, b, expected):
        """Parameterized test for various inputs."""
        calc = Calculator()
        assert calc.add(a, b) == expected
    
    def test_add_raises_on_invalid_type(self):
        """Test error handling."""
        calc = Calculator()
        with pytest.raises(TypeError):
            calc.add("2", 3)

# Fixtures
@pytest.fixture
def calculator():
    """Provide a Calculator instance."""
    return Calculator()

def test_with_fixture(calculator):
    """Test using fixture."""
    assert calculator.add(1, 1) == 2
```

### Type Hints

Use type hints for better code quality:

```python
from typing import Optional, List, Dict, Union

def process_items(items: List[str]) -> Dict[str, int]:
    """Process a list of items and return counts."""
    return {item: len(item) for item in items}

def find_item(items: List[str], target: str) -> Optional[str]:
    """Find an item or return None."""
    return next((item for item in items if item == target), None)
```

---

## C# TDD

### Setup

The project uses xUnit as the testing framework with:

- **xUnit**: Test framework
- **Moq**: Mocking library
- **coverlet**: Coverage tool
- **FluentAssertions** (optional): Expressive assertions

### Running C# Tests

```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"

# Run specific test
dotnet test --filter "FullyQualifiedName~CalculatorTests"

# Run with verbose output
dotnet test -v detailed

# Run tests in specific project
dotnet test src/CSharp/StoryGenerator.Tests/StoryGenerator.Tests.csproj
```

### C# Test Structure

```csharp
using System;
using Xunit;
using Moq;

namespace StoryGenerator.Tests
{
    public class CalculatorTests
    {
        // Simple test
        [Fact]
        public void Add_TwoPositiveNumbers_ReturnsSum()
        {
            // Arrange
            var calculator = new Calculator();

            // Act
            var result = calculator.Add(2, 3);

            // Assert
            Assert.Equal(5, result);
        }

        // Parameterized test
        [Theory]
        [InlineData(0, 0, 0)]
        [InlineData(1, 2, 3)]
        [InlineData(-1, 1, 0)]
        public void Add_VariousInputs_ReturnsExpectedSum(int a, int b, int expected)
        {
            // Arrange
            var calculator = new Calculator();

            // Act
            var result = calculator.Add(a, b);

            // Assert
            Assert.Equal(expected, result);
        }

        // Exception testing
        [Fact]
        public void Divide_ByZero_ThrowsException()
        {
            // Arrange
            var calculator = new Calculator();

            // Act & Assert
            var ex = Assert.Throws<DivideByZeroException>(() => calculator.Divide(5, 0));
            Assert.Contains("Cannot divide by zero", ex.Message);
        }

        // Using Moq for mocking
        [Fact]
        public void ProcessData_CallsLogger_WhenError()
        {
            // Arrange
            var mockLogger = new Mock<ILogger>();
            var service = new DataService(mockLogger.Object);

            // Act
            service.ProcessData(null);

            // Assert
            mockLogger.Verify(x => x.LogError(It.IsAny<string>()), Times.Once);
        }
    }

    // Fixture for test setup/teardown
    public class DatabaseTests : IDisposable
    {
        private readonly string _testDirectory;

        public DatabaseTests()
        {
            _testDirectory = Path.Combine(Path.GetTempPath(), Guid.NewGuid().ToString());
            Directory.CreateDirectory(_testDirectory);
        }

        public void Dispose()
        {
            if (Directory.Exists(_testDirectory))
            {
                Directory.Delete(_testDirectory, recursive: true);
            }
        }

        [Fact]
        public void SaveData_CreatesFile()
        {
            // Test implementation
        }
    }
}
```

---

## Running Tests

### Quick Commands

**Python:**
```bash
# Run all Python tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html --cov-report=term-missing

# Run specific marker
pytest -m "not slow"
```

**C#:**
```bash
# Run all C# tests
cd src/CSharp
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage" --results-directory ./coverage

# Generate coverage report (requires reportgenerator)
reportgenerator -reports:"coverage/**/coverage.cobertura.xml" -targetdir:"coverage/report" -reporttypes:Html
```

---

## Coverage Reports

### Python Coverage

After running `pytest --cov=src --cov-report=html`:
- View report: `htmlcov/index.html`
- Terminal output shows line-by-line coverage
- Aim for >70% coverage for production code

### C# Coverage

After running with coverage collection:
- Reports in: `coverage/` directory
- Use `reportgenerator` for HTML reports
- Aim for >70% coverage for production code

---

## Best Practices

### General TDD Principles

1. **Red-Green-Refactor Cycle**
   - Red: Write a failing test first
   - Green: Write minimal code to pass
   - Refactor: Improve code while keeping tests green

2. **Test Organization**
   - One test class per production class
   - Group related tests with regions (C#) or classes (Python)
   - Use descriptive test names: `Method_Scenario_ExpectedBehavior`

3. **Arrange-Act-Assert (AAA)**
   - Arrange: Set up test data and dependencies
   - Act: Execute the code under test
   - Assert: Verify the expected outcome

4. **Test Independence**
   - Each test should be independent
   - Tests should not rely on execution order
   - Use setup/teardown or fixtures for shared state

5. **Parameterized Tests**
   - Use `@pytest.mark.parametrize` (Python) or `[Theory]` (C#)
   - Test multiple scenarios with one test method
   - Reduces code duplication

### Python-Specific Best Practices

1. **Type Hints**: Use type hints for all function signatures
2. **Docstrings**: Document test purpose in docstrings
3. **Markers**: Use pytest markers (`@pytest.mark.slow`, `@pytest.mark.integration`)
4. **Fixtures**: Use fixtures for shared setup logic
5. **Mocking**: Use `pytest-mock` or `unittest.mock` for external dependencies

### C#-Specific Best Practices

1. **Nullable Reference Types**: Enable `<Nullable>enable</Nullable>`
2. **Async Tests**: Use `async Task` for async operations
3. **IDisposable**: Implement for cleanup in fixture classes
4. **Moq**: Use for mocking interfaces and abstract classes
5. **Theory Data**: Use `[Theory]` with `[InlineData]`, `[MemberData]`, or `[ClassData]`

### Code Quality

1. **Keep Tests Small**: Each test should verify one behavior
2. **Avoid Test Logic**: Tests should be simple and straightforward
3. **Clear Assertions**: Use meaningful assertion messages
4. **Test Edge Cases**: Empty inputs, null values, boundaries
5. **Fast Tests**: Unit tests should run in milliseconds

### What to Test

✅ **Do Test:**
- Public APIs and interfaces
- Business logic and algorithms
- Error handling and validation
- Edge cases and boundary conditions

❌ **Don't Test:**
- Private methods (test through public API)
- Third-party library internals
- Getters/setters without logic
- Framework code

---

## Examples in This Repository

### Python Examples
- `tests/test_tdd_example.py` - Calculator with parameterized tests
- `tests/test_config.py` - Configuration validation

### C# Examples
- `src/CSharp/StoryGenerator.Tests/Examples/TddCalculatorTests.cs` - Calculator with Theory tests
- `src/CSharp/StoryGenerator.Tests/Services/OutputValidatorTests.cs` - File validation with mocking

---

## Continuous Integration

### GitHub Actions (Future Enhancement)

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  python-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3

  csharp-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-dotnet@v3
        with:
          dotnet-version: '8.0'
      - run: dotnet test --collect:"XPlat Code Coverage"
```

---

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [xUnit documentation](https://xunit.net/)
- [Moq documentation](https://github.com/moq/moq4)
- [Test-Driven Development by Example (Kent Beck)](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)

---

## Getting Help

If you encounter issues:
1. Check existing test examples in `tests/` directory
2. Review this guide for common patterns
3. Consult the official documentation for tools
4. Ask in team discussions
