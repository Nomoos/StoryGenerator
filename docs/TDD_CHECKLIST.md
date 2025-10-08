# TDD Implementation Checklist

Use this checklist when implementing new features using Test-Driven Development.

## Pre-Development

- [ ] Understand the requirement clearly
- [ ] Define acceptance criteria
- [ ] Identify edge cases and error conditions
- [ ] Choose appropriate test type (unit/integration)
- [ ] Set up test environment (Python: pytest, C#: xUnit)

---

## Red Phase - Write Failing Tests

### Test File Creation

**Python:**
- [ ] Create `test_<feature_name>.py` in `tests/` directory
- [ ] Import necessary modules and fixtures
- [ ] Add docstring describing what's being tested

**C#:**
- [ ] Create `<FeatureName>Tests.cs` in appropriate test project folder
- [ ] Add using statements for Xunit, tested classes
- [ ] Add class-level XML documentation

### Test Structure

- [ ] Write test class with descriptive name
- [ ] Use AAA pattern (Arrange, Act, Assert)
- [ ] Name tests: `Method_Scenario_ExpectedBehavior`
- [ ] Start with simplest happy path test
- [ ] Add one test at a time

### Initial Test Run

- [ ] Run test - **it should FAIL** (Red phase)
- [ ] Verify test fails for the right reason
- [ ] Check error message is clear

---

## Green Phase - Make Tests Pass

### Implementation

- [ ] Write minimal code to pass the test
- [ ] No premature optimization
- [ ] Keep it simple and focused
- [ ] Run tests frequently

### Validation

- [ ] Run test - **it should PASS** (Green phase)
- [ ] Run all tests to ensure nothing broke
- [ ] Commit if all tests pass: `git commit -m "feat: implement <feature>"`

---

## Refactor Phase - Improve Code

### Code Quality

- [ ] Remove duplication (DRY principle)
- [ ] Improve naming (variables, methods, classes)
- [ ] Extract methods/functions if needed
- [ ] Add/improve comments for complex logic
- [ ] Follow language conventions (PEP 8 for Python, C# conventions)

### Type Safety (if applicable)

**Python:**
- [ ] Add type hints to function signatures
- [ ] Run mypy type checker
- [ ] Fix any type errors

**C#:**
- [ ] Ensure nullable reference types are handled
- [ ] Use nullable annotations where appropriate
- [ ] Run compiler with warnings as errors

### Validation After Refactor

- [ ] Run all tests - **they should still PASS**
- [ ] Run linters/formatters:
  - Python: `black .` and `ruff check .`
  - C#: `dotnet format`
- [ ] Fix any code quality issues
- [ ] Commit: `git commit -m "refactor: improve <aspect>"`

---

## Edge Cases and Error Handling

### Additional Tests

- [ ] Null/None inputs
- [ ] Empty collections/strings
- [ ] Boundary values (min, max)
- [ ] Invalid inputs (wrong type, format)
- [ ] Concurrent access (if applicable)

### Exception Handling

**Python:**
```python
- [ ] Use pytest.raises for expected exceptions
- [ ] Verify exception message/type
- [ ] Test exception arguments
```

**C#:**
```csharp
- [ ] Use Assert.Throws for expected exceptions
- [ ] Verify exception message/type
- [ ] Test ArgumentNullException with ThrowIfNull
```

### Validation

- [ ] All edge case tests pass
- [ ] Error messages are clear and helpful
- [ ] Commit: `git commit -m "test: add edge cases for <feature>"`

---

## Parameterized Tests

### When to Use

- [ ] Multiple similar test cases
- [ ] Testing with various inputs
- [ ] Reducing test duplication

### Implementation

**Python:**
```python
- [ ] Use @pytest.mark.parametrize
- [ ] Provide descriptive parameter names
- [ ] Include representative test cases
```

**C#:**
```csharp
- [ ] Use [Theory] with [InlineData]
- [ ] Or use [MemberData] for complex data
- [ ] Include representative test cases
```

### Validation

- [ ] Each parameter combination tested
- [ ] All parameterized tests pass
- [ ] Commit: `git commit -m "test: parameterize <feature> tests"`

---

## Mocking External Dependencies

### Identify Dependencies

- [ ] Database access
- [ ] File system operations
- [ ] HTTP/API calls
- [ ] Time-dependent operations
- [ ] Random number generation

### Create Mocks

**Python:**
```python
- [ ] Use pytest-mock or unittest.mock
- [ ] Create fixtures for mocked dependencies
- [ ] Verify mock calls with assert_called_with
```

**C#:**
```csharp
- [ ] Use Moq for interface mocking
- [ ] Set up expected behavior with .Setup()
- [ ] Verify calls with .Verify()
```

### Validation

- [ ] Tests are isolated and fast
- [ ] No external dependencies in unit tests
- [ ] Commit: `git commit -m "test: add mocks for <dependency>"`

---

## Integration Tests (Optional)

### When Needed

- [ ] Testing multiple components together
- [ ] Verifying external service integration
- [ ] End-to-end workflows

### Implementation

**Python:**
```python
- [ ] Mark with @pytest.mark.integration
- [ ] Use fixtures for setup/teardown
- [ ] May use testcontainers for databases
```

**C#:**
```csharp
- [ ] Create separate test class or project
- [ ] Use IClassFixture for shared setup
- [ ] Consider WebApplicationFactory for APIs
```

### Validation

- [ ] Integration tests can be run separately: `pytest -m integration`
- [ ] Integration tests pass
- [ ] Commit: `git commit -m "test(integration): add <scenario> tests"`

---

## Documentation

### Code Documentation

- [ ] Add XML docs (C#) or docstrings (Python)
- [ ] Document complex algorithms
- [ ] Add usage examples in comments
- [ ] Update README if needed

### Test Documentation

- [ ] Test docstrings/comments explain "why"
- [ ] Complex test setup is explained
- [ ] Edge cases are documented

### Validation

- [ ] Documentation is clear and helpful
- [ ] Examples are accurate
- [ ] Commit: `git commit -m "docs: document <feature>"`

---

## Coverage

### Run Coverage

**Python:**
```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
```

**C#:**
```bash
dotnet test --collect:"XPlat Code Coverage"
```

### Review Coverage

- [ ] Check coverage report
- [ ] Aim for >70% coverage for new code
- [ ] Identify untested paths
- [ ] Add tests for uncovered code (if important)

### Update Configuration

- [ ] Exclude generated code from coverage
- [ ] Update coverage thresholds if needed
- [ ] Commit: `git commit -m "test: improve coverage to X%"`

---

## CI/CD Integration

### Local Validation

- [ ] Run all tests locally: `pytest` or `dotnet test`
- [ ] Run linters: `ruff check .` or `dotnet format`
- [ ] Run formatters: `black .`
- [ ] Fix all issues

### Push to CI

- [ ] Push to feature branch
- [ ] Check GitHub Actions status
- [ ] Fix any CI failures
- [ ] Ensure coverage meets threshold

### Merge

- [ ] Create pull request
- [ ] Request code review
- [ ] Address review comments
- [ ] Merge when approved and CI passes

---

## Final Checklist

Before marking the feature as complete:

- [ ] All tests pass (unit + integration)
- [ ] Code coverage meets project standards
- [ ] No linting errors
- [ ] Code is properly formatted
- [ ] Documentation is complete
- [ ] Edge cases are tested
- [ ] Error handling is tested
- [ ] Performance is acceptable
- [ ] Code is reviewed and approved
- [ ] CI/CD pipeline passes

---

## Example Workflow

Here's a complete example of implementing a new feature:

```bash
# 1. RED - Write failing test
# Create test file and write test
# Run: pytest tests/test_calculator.py
# Result: Test fails ❌

# 2. GREEN - Make it pass
# Implement minimal code
# Run: pytest tests/test_calculator.py
# Result: Test passes ✅

# 3. REFACTOR - Improve
# Clean up code, remove duplication
# Run: pytest tests/test_calculator.py
# Result: Test still passes ✅

# 4. EDGE CASES
# Add tests for null, empty, boundaries
# Run: pytest tests/test_calculator.py
# Result: All tests pass ✅

# 5. PARAMETERIZE
# Convert to parameterized tests
# Run: pytest tests/test_calculator.py -v
# Result: Multiple test cases pass ✅

# 6. COVERAGE
# Check coverage
pytest --cov=src --cov-report=term-missing
# Result: Coverage >70% ✅

# 7. FORMAT & LINT
black . && ruff check --fix .
# Result: No issues ✅

# 8. COMMIT & PUSH
git add .
git commit -m "feat(calculator): add division with error handling"
git push origin feature/calculator
# Result: CI passes ✅
```

---

## Common Pitfalls to Avoid

- ❌ Writing implementation before tests
- ❌ Writing too many tests at once
- ❌ Making tests dependent on each other
- ❌ Ignoring failing tests
- ❌ Not running tests frequently
- ❌ Testing private methods directly
- ❌ Mocking everything (over-mocking)
- ❌ Writing tests that are too complex
- ❌ Not testing edge cases
- ❌ Skipping the refactor phase

---

## Resources

- [TDD_GUIDE.md](TDD_GUIDE.md) - Comprehensive TDD guide
- [tests/README.md](../tests/README.md) - Quick start guide
- [test_tdd_example.py](../tests/test_tdd_example.py) - Python examples
- [TddCalculatorTests.cs](../src/CSharp/StoryGenerator.Tests/Examples/TddCalculatorTests.cs) - C# examples
