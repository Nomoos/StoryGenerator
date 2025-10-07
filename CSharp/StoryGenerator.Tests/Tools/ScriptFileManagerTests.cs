using System;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Moq;
using StoryGenerator.Models;
using StoryGenerator.Tools;
using Xunit;

namespace StoryGenerator.Tests.Tools
{
    /// <summary>
    /// Unit tests for ScriptFileManager.
    /// Tests file I/O operations, null-safety, and directory management.
    /// </summary>
    public class ScriptFileManagerTests : IDisposable
    {
        private readonly string _testBasePath;
        private readonly ScriptFileManager _fileManager;

        public ScriptFileManagerTests()
        {
            _testBasePath = Path.Combine(Path.GetTempPath(), "StoryGeneratorTests", Guid.NewGuid().ToString());
            _fileManager = new ScriptFileManager();
            Directory.CreateDirectory(_testBasePath);
        }

        public void Dispose()
        {
            if (Directory.Exists(_testBasePath))
            {
                Directory.Delete(_testBasePath, true);
            }
        }

        [Fact]
        public void Constructor_CreatesInstance()
        {
            // Act
            var manager = new ScriptFileManager();

            // Assert
            Assert.NotNull(manager);
        }

        [Fact]
        public void GenerateScriptFileName_WithoutVersion_ReturnsCorrectName()
        {
            // Arrange
            var titleId = "test_story_001";

            // Act
            var fileName = _fileManager.GenerateScriptFileName(titleId);

            // Assert
            Assert.Equal("test_story_001.md", fileName);
        }

        [Fact]
        public void GenerateScriptFileName_WithVersion_ReturnsCorrectName()
        {
            // Arrange
            var titleId = "test_story_001";
            var version = "v2";

            // Act
            var fileName = _fileManager.GenerateScriptFileName(titleId, version);

            // Assert
            Assert.Equal("test_story_001_v2.md", fileName);
        }

        [Fact]
        public void GenerateScriptFileName_NullTitleId_ThrowsArgumentException()
        {
            // Act & Assert
            Assert.Throws<ArgumentException>(() => _fileManager.GenerateScriptFileName(null!));
        }

        [Fact]
        public void EnsureScriptDirectory_CreatesDirectory()
        {
            // Arrange
            var segment = new AudienceSegment("men", "18-23");
            var scriptType = "gpt_improved";

            // Act
            var directory = _fileManager.EnsureScriptDirectory(_testBasePath, segment, scriptType);

            // Assert
            Assert.True(Directory.Exists(directory));
            Assert.Contains("men", directory);
            Assert.Contains("18-23", directory);
            Assert.Contains("gpt_improved", directory);
        }

        [Fact]
        public void EnsureScriptDirectory_NullBasePath_ThrowsArgumentException()
        {
            // Arrange
            var segment = new AudienceSegment("men", "18-23");

            // Act & Assert
            Assert.Throws<ArgumentException>(() => 
                _fileManager.EnsureScriptDirectory(null!, segment, "gpt_improved"));
        }

        [Fact]
        public async Task SaveRawScriptAsync_SavesFile()
        {
            // Arrange
            var scriptVersion = new ScriptVersion
            {
                TitleId = "test_001",
                Version = "v1",
                Content = "# Test Script\n\nThis is a test script.",
                TargetAudience = new AudienceSegment("men", "18-23")
            };

            // Act
            var filePath = await _fileManager.SaveRawScriptAsync(scriptVersion, _testBasePath);

            // Assert
            Assert.True(File.Exists(filePath));
            var content = await File.ReadAllTextAsync(filePath);
            Assert.Equal(scriptVersion.Content, content);
        }

        [Fact]
        public async Task LoadScriptAsync_LoadsFile()
        {
            // Arrange
            var testContent = "# Test Script\n\nTest content.";
            var testFile = Path.Combine(_testBasePath, "test.md");
            await File.WriteAllTextAsync(testFile, testContent);

            // Act
            var content = await _fileManager.LoadScriptAsync(testFile);

            // Assert
            Assert.Equal(testContent, content);
        }

        [Fact]
        public async Task LoadScriptAsync_FileNotFound_ThrowsFileNotFoundException()
        {
            // Arrange
            var nonExistentFile = Path.Combine(_testBasePath, "nonexistent.md");

            // Act & Assert
            await Assert.ThrowsAsync<FileNotFoundException>(async () => 
                await _fileManager.LoadScriptAsync(nonExistentFile));
        }

        [Fact]
        public async Task FindScriptFilesAsync_FindsMatchingFiles()
        {
            // Arrange
            var testDir = Path.Combine(_testBasePath, "scripts");
            Directory.CreateDirectory(testDir);
            await File.WriteAllTextAsync(Path.Combine(testDir, "script1.md"), "Content 1");
            await File.WriteAllTextAsync(Path.Combine(testDir, "script2.md"), "Content 2");
            await File.WriteAllTextAsync(Path.Combine(testDir, "readme.txt"), "Readme");

            // Act
            var files = await _fileManager.FindScriptFilesAsync(testDir, "*.md");

            // Assert
            Assert.Equal(2, files.Count());
        }
    }
}
