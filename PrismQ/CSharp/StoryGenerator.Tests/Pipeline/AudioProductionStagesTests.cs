using StoryGenerator.Pipeline.Stages;
using StoryGenerator.Pipeline.Stages.Models;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

/// <summary>
/// Tests for Phase 3 Group 5: Audio Production Stages
/// </summary>
public class AudioProductionStagesTests
{
    #region TTS Generation Tests

    [Fact]
    public async Task TtsGenerationStage_WithValidScript_GeneratesAudio()
    {
        // Arrange
        var stage = new TtsGenerationStage();
        var input = new TtsGenerationInput
        {
            ScriptContent = "This is a test script for video narration. It should be converted to speech.",
            TitleId = "test_001",
            Gender = "male",
            AgeGroup = "18-24",
            VoiceId = "default",
            Provider = "openai"
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.NotNull(output);
        Assert.NotEmpty(output.AudioPath);
        Assert.True(output.DurationSeconds > 0);
        Assert.Equal("mp3", output.Format);
        Assert.Equal(44100, output.SampleRate);
    }

    [Fact]
    public async Task TtsGenerationStage_EmptyScript_ThrowsException()
    {
        // Arrange
        var stage = new TtsGenerationStage();
        var input = new TtsGenerationInput
        {
            ScriptContent = "",
            TitleId = "test_002",
            Gender = "female",
            AgeGroup = "25-34"
        };

        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(
            async () => await stage.ExecuteAsync(input, null, CancellationToken.None));
    }

    [Fact]
    public async Task TtsGenerationStage_LongerScript_LongerDuration()
    {
        // Arrange
        var stage = new TtsGenerationStage();
        var shortScript = "Short script.";
        var longScript = string.Join(" ", Enumerable.Repeat("This is a longer script with more words.", 10));

        var shortInput = new TtsGenerationInput
        {
            ScriptContent = shortScript,
            TitleId = "test_003_short",
            Gender = "male",
            AgeGroup = "18-24"
        };

        var longInput = new TtsGenerationInput
        {
            ScriptContent = longScript,
            TitleId = "test_003_long",
            Gender = "male",
            AgeGroup = "18-24"
        };

        // Act
        var shortOutput = await stage.ExecuteAsync(shortInput, null, CancellationToken.None);
        var longOutput = await stage.ExecuteAsync(longInput, null, CancellationToken.None);

        // Assert
        Assert.True(longOutput.DurationSeconds > shortOutput.DurationSeconds);
    }

    [Fact]
    public async Task TtsGenerationStage_DifferentProviders_GeneratesAudio()
    {
        // Arrange
        var stage = new TtsGenerationStage();
        var providers = new[] { "openai", "elevenlabs", "azure" };
        var outputs = new List<TtsGenerationOutput>();

        // Act
        foreach (var provider in providers)
        {
            var input = new TtsGenerationInput
            {
                ScriptContent = "Test script for different providers.",
                TitleId = $"test_004_{provider}",
                Gender = "male",
                AgeGroup = "18-24",
                Provider = provider
            };
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);
            outputs.Add(output);
        }

        // Assert
        Assert.Equal(3, outputs.Count);
        Assert.All(outputs, o => Assert.NotEmpty(o.AudioPath));
        Assert.All(outputs, o => Assert.True(o.DurationSeconds > 0));
    }

    #endregion

    #region Audio Normalization Tests

    [Fact]
    public async Task AudioNormalizationStage_WithValidAudio_NormalizesAudio()
    {
        // Arrange
        var stage = new AudioNormalizationStage();
        var testAudioPath = CreateTestAudioFile();
        var input = new AudioNormalizationInput
        {
            InputAudioPath = testAudioPath,
            TitleId = "test_005",
            Gender = "male",
            AgeGroup = "18-24",
            TargetLufs = -14.0,
            TwoPass = true
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output);
            Assert.NotEmpty(output.NormalizedAudioPath);
            Assert.True(output.InputLufs != 0);
            Assert.True(output.OutputLufs != 0);
            Assert.Equal(-14.0, output.TargetLufs);
            Assert.True(output.DurationSeconds > 0);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testAudioPath);
        }
    }

    [Fact]
    public async Task AudioNormalizationStage_InvalidAudioPath_ThrowsException()
    {
        // Arrange
        var stage = new AudioNormalizationStage();
        var input = new AudioNormalizationInput
        {
            InputAudioPath = "nonexistent.mp3",
            TitleId = "test_006",
            Gender = "male",
            AgeGroup = "18-24"
        };

        // Act & Assert
        await Assert.ThrowsAsync<FileNotFoundException>(
            async () => await stage.ExecuteAsync(input, null, CancellationToken.None));
    }

    [Fact]
    public async Task AudioNormalizationStage_MeetsTargetLufs()
    {
        // Arrange
        var stage = new AudioNormalizationStage();
        var testAudioPath = CreateTestAudioFile();
        var input = new AudioNormalizationInput
        {
            InputAudioPath = testAudioPath,
            TitleId = "test_007",
            Gender = "female",
            AgeGroup = "25-34",
            TargetLufs = -14.0,
            TwoPass = true
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            // Output LUFS should be close to target (within ±1.0 LUFS)
            var difference = Math.Abs(output.OutputLufs - output.TargetLufs);
            Assert.True(difference <= 1.0, $"Output LUFS {output.OutputLufs} differs from target {output.TargetLufs} by {difference}");
            Assert.True(output.MeetsTarget);
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testAudioPath);
        }
    }

    [Fact]
    public async Task AudioNormalizationStage_DifferentTargetLufs_AdjustsCorrectly()
    {
        // Arrange
        var stage = new AudioNormalizationStage();
        var testAudioPath1 = CreateTestAudioFile();
        var testAudioPath2 = CreateTestAudioFile();

        var input1 = new AudioNormalizationInput
        {
            InputAudioPath = testAudioPath1,
            TitleId = "test_008_a",
            Gender = "male",
            AgeGroup = "18-24",
            TargetLufs = -14.0
        };

        var input2 = new AudioNormalizationInput
        {
            InputAudioPath = testAudioPath2,
            TitleId = "test_008_b",
            Gender = "male",
            AgeGroup = "18-24",
            TargetLufs = -16.0
        };

        try
        {
            // Act
            var output1 = await stage.ExecuteAsync(input1, null, CancellationToken.None);
            var output2 = await stage.ExecuteAsync(input2, null, CancellationToken.None);

            // Assert
            Assert.NotEqual(output1.OutputLufs, output2.OutputLufs);
            Assert.True(output1.OutputLufs > output2.OutputLufs); // -14 is louder than -16
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testAudioPath1);
            CleanupTestFile(testAudioPath2);
        }
    }

    [Fact]
    public async Task AudioNormalizationStage_TwoPassMode_GeneratesOutput()
    {
        // Arrange
        var stage = new AudioNormalizationStage();
        var testAudioPath = CreateTestAudioFile();
        var input = new AudioNormalizationInput
        {
            InputAudioPath = testAudioPath,
            TitleId = "test_009",
            Gender = "male",
            AgeGroup = "18-24",
            TargetLufs = -14.0,
            TwoPass = true // Enable two-pass for better accuracy
        };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.NotNull(output);
            Assert.NotEmpty(output.NormalizedAudioPath);
            Assert.True(File.Exists(output.NormalizedAudioPath));
        }
        finally
        {
            // Cleanup
            CleanupTestFile(testAudioPath);
        }
    }

    #endregion

    #region Integration Tests

    [Fact]
    public async Task AudioPipeline_TtsToNormalization_ProducesNormalizedAudio()
    {
        // Arrange
        var ttsStage = new TtsGenerationStage();
        var normalizationStage = new AudioNormalizationStage();

        var ttsInput = new TtsGenerationInput
        {
            ScriptContent = "This is an integration test for the full audio pipeline.",
            TitleId = "test_010",
            Gender = "male",
            AgeGroup = "18-24",
            Provider = "openai"
        };

        // Act
        // Step 1: Generate TTS audio
        var ttsOutput = await ttsStage.ExecuteAsync(ttsInput, null, CancellationToken.None);

        // Step 2: Normalize the generated audio
        var normalizationInput = new AudioNormalizationInput
        {
            InputAudioPath = ttsOutput.AudioPath,
            TitleId = "test_010",
            Gender = "male",
            AgeGroup = "18-24",
            TargetLufs = -14.0
        };
        var normalizationOutput = await normalizationStage.ExecuteAsync(
            normalizationInput, null, CancellationToken.None);

        // Assert
        Assert.NotEmpty(ttsOutput.AudioPath);
        Assert.NotEmpty(normalizationOutput.NormalizedAudioPath);
        Assert.True(normalizationOutput.MeetsTarget);
        Assert.Equal(-14.0, normalizationOutput.TargetLufs);
    }

    #endregion

    #region Helper Methods

    private string CreateTestAudioFile()
    {
        var tempFile = Path.Combine(Path.GetTempPath(), $"test_audio_{Guid.NewGuid()}.mp3");
        File.WriteAllText(tempFile, "test audio content");
        return tempFile;
    }

    private void CleanupTestFile(string filePath)
    {
        if (File.Exists(filePath))
        {
            try
            {
                File.Delete(filePath);
            }
            catch
            {
                // Ignore cleanup errors
            }
        }
    }

    #endregion
}
