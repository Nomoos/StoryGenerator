# Contributing to StoryGenerator

Thank you for your interest in contributing to StoryGenerator! We welcome contributions from the community.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/StoryGenerator.git
   cd StoryGenerator
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🔧 Development Setup

### Prerequisites

- .NET 9.0 SDK or later
- Git
- A code editor (Visual Studio, VS Code, or Rider)

### Build and Test

```bash
# Navigate to C# implementation
cd src/CSharp

# Restore dependencies
dotnet restore

# Build the solution
dotnet build StoryGenerator.sln

# Run tests
dotnet test
```

## 📋 Contribution Guidelines

### Code Style

- Follow the [C# Coding Standards](src/CSharp/SOLID_OOP_CLEAN_CODE_GUIDE.md)
- Use SOLID principles and clean code practices
- Write XML documentation for public APIs
- Keep methods focused and functions small
- Use meaningful names for variables and methods

### Coding Standards

```csharp
// ✅ Good: Clear, well-documented code
/// <summary>
/// Generates a script from a story idea.
/// </summary>
/// <param name="storyIdea">The story idea to generate from.</param>
/// <param name="cancellationToken">Cancellation token.</param>
/// <returns>The generated script text.</returns>
public async Task<string> GenerateScriptAsync(
    StoryIdea storyIdea,
    CancellationToken cancellationToken = default)
{
    ArgumentNullException.ThrowIfNull(storyIdea);
    
    // Implementation...
}

// ❌ Bad: No documentation, unclear names
public async Task<string> Gen(StoryIdea si)
{
    // Implementation...
}
```

### Testing

- Write unit tests for new features
- Ensure all tests pass before submitting
- Aim for high code coverage
- Use meaningful test names that describe what is being tested

Example test:
```csharp
[Fact]
public async Task GenerateScriptAsync_WithValidIdea_ReturnsScript()
{
    // Arrange
    var generator = new ScriptGenerator(/* dependencies */);
    var storyIdea = new StoryIdea { /* properties */ };
    
    // Act
    var result = await generator.GenerateScriptAsync(storyIdea);
    
    // Assert
    Assert.NotNull(result);
    Assert.NotEmpty(result);
}
```

### Commit Messages

Use clear, descriptive commit messages:

```bash
# ✅ Good
git commit -m "Add viral scoring to story ideas"
git commit -m "Fix null reference in script generator"
git commit -m "Update documentation for pipeline stages"

# ❌ Bad
git commit -m "fix stuff"
git commit -m "update"
git commit -m "wip"
```

### Pull Request Process

1. **Update your branch** with the latest changes from `main`:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Ensure all tests pass**:
   ```bash
   dotnet test
   ```

3. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Reference any related issues (e.g., "Fixes #123")
   - Screenshots for UI changes (if applicable)

5. **Respond to feedback** from reviewers

## 📝 Documentation

- Update documentation for any changed functionality
- Add examples for new features
- Update the relevant README files
- Keep documentation clear and concise

## 🐛 Reporting Bugs

When reporting bugs, include:

1. **Description** of the bug
2. **Steps to reproduce** the issue
3. **Expected behavior**
4. **Actual behavior**
5. **Environment** (OS, .NET version, etc.)
6. **Stack trace** or error messages (if applicable)

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md) when creating an issue.

## 💡 Suggesting Features

We welcome feature suggestions! When suggesting a feature:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** and its use case
3. **Explain why** it would be valuable
4. **Provide examples** of how it would work

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md).

## 🔒 Security

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email the maintainers privately
3. Follow the [Security Policy](SECURITY_CHECKLIST.md)

## 📚 Resources

- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Architecture Documentation](docs/ARCHITECTURE.md)
- [C# Implementation Guide](src/CSharp/IMPLEMENTATION_GUIDE.md)
- [SOLID Principles Guide](src/CSharp/SOLID_OOP_CLEAN_CODE_GUIDE.md)
- [Testing Guide](docs/TDD_GUIDE.md)

## 🎯 Areas to Contribute

We especially welcome contributions in these areas:

- **Pipeline Stages**: Implementing remaining pipeline stages (keyframe generation, video synthesis)
- **Testing**: Adding unit and integration tests
- **Documentation**: Improving guides and examples
- **Performance**: Optimizing existing code
- **Bug Fixes**: Resolving open issues

## 📊 Code Review Checklist

Before submitting, ensure your code:

- [ ] Follows the coding standards
- [ ] Includes appropriate tests
- [ ] Has XML documentation for public APIs
- [ ] Passes all existing tests
- [ ] Builds without warnings
- [ ] Updates relevant documentation
- [ ] Handles errors appropriately
- [ ] Uses async/await properly
- [ ] Follows SOLID principles

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Give constructive feedback
- Focus on the code, not the person
- Be open to different perspectives

## 📞 Getting Help

- **Questions**: Use [GitHub Discussions](https://github.com/Nomoos/StoryGenerator/discussions)
- **Issues**: Check [existing issues](https://github.com/Nomoos/StoryGenerator/issues)
- **Documentation**: Start with [INDEX.md](docs/INDEX.md)

## 🎉 Recognition

Contributors will be recognized in:
- The project's README
- Release notes for their contributions
- The contributors page on GitHub

Thank you for contributing to StoryGenerator! 🙏
