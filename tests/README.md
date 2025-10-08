# Testing Quick Start

## Running Tests

### Python Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_tdd_example.py

# Run tests in parallel (faster)
pytest -n auto

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### C# Tests

```bash
# Run all tests
cd src/CSharp
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage" --results-directory ./coverage

# Run specific test
dotnet test --filter "FullyQualifiedName~TddCalculatorTests"

# Run in verbose mode
dotnet test -v detailed
```

## Code Quality

### Python

```bash
# Format code
black .

# Check formatting (without changing)
black --check .

# Lint code
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Type check
mypy src --ignore-missing-imports
```

### C#

```bash
# Build with warnings as errors
dotnet build /p:TreatWarningsAsErrors=true

# Format code (requires dotnet format tool)
dotnet format
```

## Creating New Tests

### Python Test Template

```python
import pytest

class TestMyFeature:
    """Test suite for MyFeature."""
    
    def test_basic_functionality(self):
        """Test basic case."""
        # Arrange
        input_data = "test"
        
        # Act
        result = my_function(input_data)
        
        # Assert
        assert result == "expected"
    
    @pytest.mark.parametrize("input,expected", [
        ("a", "A"),
        ("b", "B"),
    ])
    def test_parameterized(self, input, expected):
        """Test multiple cases."""
        assert my_function(input) == expected
```

### C# Test Template

```csharp
using Xunit;

namespace StoryGenerator.Tests
{
    public class MyFeatureTests
    {
        [Fact]
        public void Method_Scenario_ExpectedBehavior()
        {
            // Arrange
            var input = "test";
            
            // Act
            var result = MyMethod(input);
            
            // Assert
            Assert.Equal("expected", result);
        }

        [Theory]
        [InlineData("a", "A")]
        [InlineData("b", "B")]
        public void Method_MultipleInputs_ReturnsExpected(string input, string expected)
        {
            // Arrange & Act
            var result = MyMethod(input);
            
            // Assert
            Assert.Equal(expected, result);
        }
    }
}
```

## CI/CD

Tests run automatically on:
- Push to main/develop
- Pull requests
- Push to copilot/** branches

View results in GitHub Actions tab.

## Learn More

See [TDD_GUIDE.md](../docs/TDD_GUIDE.md) for comprehensive guide.
