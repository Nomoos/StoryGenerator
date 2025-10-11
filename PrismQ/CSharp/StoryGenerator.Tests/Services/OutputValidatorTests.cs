using System;
using System.IO;
using System.Linq;
using Microsoft.Extensions.Logging;
using Moq;
using PrismQ.Shared.Core.Services;
using Xunit;

namespace StoryGenerator.Tests.Services
{
    public class OutputValidatorTests : IDisposable
    {
        private readonly string _testDirectory;
        private readonly OutputValidator _validator;
        private readonly Mock<ILogger<OutputValidator>> _mockLogger;

        public OutputValidatorTests()
        {
            _testDirectory = Path.Combine(Path.GetTempPath(), "OutputValidatorTests", Guid.NewGuid().ToString());
            Directory.CreateDirectory(_testDirectory);
            
            _mockLogger = new Mock<ILogger<OutputValidator>>();
            _validator = new OutputValidator(_mockLogger.Object);
        }

        public void Dispose()
        {
            if (Directory.Exists(_testDirectory))
            {
                try { Directory.Delete(_testDirectory, recursive: true); } catch { }
            }
        }

        [Fact]
        public void ValidateTextFile_ValidContent_ReturnsTrue()
        {
            var validFile = Path.Combine(_testDirectory, "valid.txt");
            var content = string.Join(" ", Enumerable.Repeat("word", 50));
            File.WriteAllText(validFile, content);

            var (isValid, metrics) = _validator.ValidateTextFile(validFile, minLength: 100);

            Assert.True(isValid);
            Assert.True(metrics.IsValid);
        }

        [Fact]
        public void ValidateAudioFile_ValidSize_ReturnsTrue()
        {
            var validFile = Path.Combine(_testDirectory, "valid.mp3");
            File.WriteAllBytes(validFile, new byte[100000]);

            var (isValid, metrics) = _validator.ValidateAudioFile(validFile);

            Assert.True(isValid);
            Assert.True(metrics.IsValid);
        }
    }
}
