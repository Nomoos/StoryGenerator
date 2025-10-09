using StoryGenerator.Pipeline.Stages;
using StoryGenerator.Pipeline.Stages.Models;
using StoryGenerator.Core.Models;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

/// <summary>
/// Tests for Phase 3 Group 2: Script Development Stages
/// </summary>
public class ScriptDevelopmentStagesTests
{
    #region Test Data Setup

    private List<StoryIdea> CreateTestStoryIdeas()
    {
        return new List<StoryIdea>
        {
            new StoryIdea
            {
                StoryTitle = "The Unexpected Friend",
                Tone = "emotional, heartwarming",
                Theme = "friendship, acceptance",
                Outcome = "found an unexpected ally",
                Timeline = "last summer",
                EmotionalCore = "connection beyond differences",
                PowerDynamic = "unlikely companionship",
                TwistType = "heartwarming revelation",
                TargetMoral = "never judge by appearances"
            }
        };
    }

    #endregion

    #region Stage 1: Script Generation Tests

    [Fact]
    public async Task ScriptGenerationStage_ValidInput_GeneratesScripts()
    {
        // Arrange
        var stage = new ScriptGenerationStage();
        var input = new ScriptGenerationInput
        {
            StoryIdeas = CreateTestStoryIdeas()
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.NotNull(output);
        Assert.Single(output.GeneratedScripts);
        var script = output.GeneratedScripts[0];
        Assert.NotEmpty(script.Content);
        Assert.Equal("The Unexpected Friend", script.Title);
        Assert.True(script.WordCount > 0);
    }

    [Fact]
    public async Task ScriptGenerationStage_GeneratesTargetWordCount()
    {
        // Arrange
        var stage = new ScriptGenerationStage();
        var input = new ScriptGenerationInput
        {
            StoryIdeas = CreateTestStoryIdeas()
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        var script = output.GeneratedScripts[0];
        Assert.InRange(script.WordCount, 300, 400); // Target ~360 words
    }

    #endregion

    #region Stage 2: Script Improvement Tests

    [Fact]
    public async Task ScriptImprovementStage_CreatesMultipleVersions()
    {
        // Arrange
        var stage = new ScriptImprovementStage();
        var generatedScript = new GeneratedScript
        {
            Title = "Test Script",
            Content = "Initial content for testing.",
            WordCount = 4
        };
        var input = new ScriptImprovementInput
        {
            Scripts = new List<GeneratedScript> { generatedScript },
            ImprovementIterations = 3
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.Equal(3, output.ImprovedScripts.Count);
        Assert.Equal("v1", output.ImprovedScripts[0].Version);
        Assert.Equal("v2", output.ImprovedScripts[1].Version);
        Assert.Equal("v3", output.ImprovedScripts[2].Version);
    }

    [Fact]
    public async Task ScriptImprovementStage_RecordsImprovements()
    {
        // Arrange
        var stage = new ScriptImprovementStage();
        var input = new ScriptImprovementInput
        {
            Scripts = new List<GeneratedScript>
            {
                new GeneratedScript { Content = "Test content" }
            },
            ImprovementIterations = 1
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        var improved = output.ImprovedScripts[0];
        Assert.NotEmpty(improved.Improvements);
        Assert.Contains(improved.Improvements, i => i.Contains("Enhanced"));
    }

    #endregion

    #region Stage 3: Script Scoring Tests

    [Fact]
    public async Task ScriptScoringStage_ScoresMultipleDimensions()
    {
        // Arrange
        var stage = new ScriptScoringStage();
        var improvedScript = new ImprovedScript
        {
            Content = new string('a', 360 * 5), // Approximate 360 words
            Version = "v2",
            Improvements = new List<string> { "imp1", "imp2", "imp3" }
        };
        var input = new ScriptScoringInput
        {
            Scripts = new List<ImprovedScript> { improvedScript }
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        var scored = output.ScoredScripts[0];
        Assert.InRange(scored.QualityScore, 0, 100);
        Assert.InRange(scored.EmotionalImpact, 0, 100);
        Assert.InRange(scored.NarrativeFlow, 0, 100);
        Assert.InRange(scored.Clarity, 0, 100);
    }

    [Fact]
    public async Task ScriptScoringStage_HigherImprovementsGetBetterScores()
    {
        // Arrange
        var stage = new ScriptScoringStage();
        var scriptV1 = new ImprovedScript
        {
            Content = new string('a', 360 * 5),
            Version = "v1",
            Improvements = new List<string> { "imp1" }
        };
        var scriptV3 = new ImprovedScript
        {
            Content = new string('a', 360 * 5),
            Version = "v3",
            Improvements = new List<string> { "imp1", "imp2", "imp3" }
        };
        var input = new ScriptScoringInput
        {
            Scripts = new List<ImprovedScript> { scriptV1, scriptV3 }
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        var scoreV1 = output.ScoredScripts[0].QualityScore;
        var scoreV3 = output.ScoredScripts[1].QualityScore;
        Assert.True(scoreV3 > scoreV1, "v3 should score higher than v1");
    }

    #endregion

    #region Stage 4: Script Selection Tests

    [Fact]
    public async Task ScriptSelectionStage_SelectsBestScript()
    {
        // Arrange
        var stage = new ScriptSelectionStage();
        var scoredScripts = new List<ScoredScript>
        {
            new ScoredScript
            {
                Script = new ImprovedScript { Content = "Low quality", Version = "v1" },
                QualityScore = 60
            },
            new ScoredScript
            {
                Script = new ImprovedScript { Content = "High quality", Version = "v3" },
                QualityScore = 90
            },
            new ScoredScript
            {
                Script = new ImprovedScript { Content = "Medium quality", Version = "v2" },
                QualityScore = 75
            }
        };
        var input = new ScriptSelectionInput
        {
            ScoredScripts = scoredScripts,
            SelectCount = 1
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.Single(output.SelectedScripts);
        Assert.Equal("High quality", output.SelectedScripts[0].Content);
    }

    [Fact]
    public async Task ScriptSelectionStage_SelectsMultipleScripts()
    {
        // Arrange
        var stage = new ScriptSelectionStage();
        var scoredScripts = Enumerable.Range(1, 5)
            .Select(i => new ScoredScript
            {
                Script = new ImprovedScript { Content = $"Script {i}" },
                QualityScore = i * 10
            })
            .ToList();
        var input = new ScriptSelectionInput
        {
            ScoredScripts = scoredScripts,
            SelectCount = 3
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.Equal(3, output.SelectedScripts.Count);
    }

    #endregion

    #region Stage 5: Script Revision Tests

    [Fact]
    public async Task ScriptRevisionStage_RevisesForVoice()
    {
        // Arrange
        var stage = new ScriptRevisionStage();
        var improvedScript = new ImprovedScript
        {
            Content = "Original script content for revision",
            Version = "v3"
        };
        var input = new ScriptRevisionInput
        {
            Scripts = new List<ImprovedScript> { improvedScript }
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.Single(output.RevisedScripts);
        var revised = output.RevisedScripts[0];
        Assert.NotEmpty(revised.Content);
        Assert.NotEmpty(revised.Revisions);
        Assert.Contains(revised.Revisions, r => r.Contains("voice") || r.Contains("clarity"));
    }

    #endregion

    #region Stage 6: Script Enhancement Tests

    [Fact]
    public async Task ScriptEnhancementStage_AddsVoiceTags()
    {
        // Arrange
        var stage = new ScriptEnhancementStage();
        var revisedScript = new RevisedScript
        {
            Content = "I never expected that things would turn out this way.",
            Revisions = new List<string> { "revision1" }
        };
        var input = new ScriptEnhancementInput
        {
            Scripts = new List<RevisedScript> { revisedScript }
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.Single(output.EnhancedScripts);
        var enhanced = output.EnhancedScripts[0];
        Assert.Contains("<emphasis", enhanced.Content);
        Assert.NotEmpty(enhanced.Enhancements);
    }

    #endregion

    #region Stage 7: Script Validation Tests

    [Fact]
    public async Task ScriptValidationStage_ValidatesRequiredFields()
    {
        // Arrange
        var stage = new ScriptValidationStage();
        var validScript = new EnhancedScript
        {
            Content = new string('a', 360 * 5), // ~360 words
            Enhancements = new List<string> { "enhancement1" }
        };
        var invalidScript = new EnhancedScript
        {
            Content = "", // Empty content
            Enhancements = new List<string>()
        };
        var input = new ScriptValidationInput
        {
            Scripts = new List<EnhancedScript> { validScript, invalidScript }
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.Equal(2, output.ValidatedScripts.Count);
        Assert.True(output.ValidatedScripts[0].IsValid);
        Assert.False(output.ValidatedScripts[1].IsValid);
        Assert.Contains("Script content is empty", output.ValidatedScripts[1].ValidationMessages);
    }

    [Fact]
    public async Task ScriptValidationStage_WarnsAboutWordCount()
    {
        // Arrange
        var stage = new ScriptValidationStage();
        var shortScript = new EnhancedScript
        {
            Content = "Too short",
            Enhancements = new List<string> { "e1" }
        };
        var input = new ScriptValidationInput
        {
            Scripts = new List<EnhancedScript> { shortScript }
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        var validated = output.ValidatedScripts[0];
        Assert.True(validated.IsValid); // Still valid but with warning
        Assert.Contains(validated.ValidationMessages, m => m.Contains("short"));
    }

    #endregion

    #region Stage 8: Script Registry Update Tests

    [Fact]
    public async Task ScriptRegistryUpdateStage_SavesValidScripts()
    {
        // Arrange
        var tempPath = Path.Combine(Path.GetTempPath(), $"test_script_registry_{Guid.NewGuid()}.json");
        var stage = new ScriptRegistryUpdateStage(tempPath);
        
        var validatedScripts = new List<ValidatedScript>
        {
            new ValidatedScript
            {
                Script = new EnhancedScript { Content = "Test Script Content 1" },
                IsValid = true
            },
            new ValidatedScript
            {
                Script = new EnhancedScript { Content = "Test Script Content 2" },
                IsValid = false // Should be filtered out
            }
        };
        var input = new ScriptRegistryUpdateInput { ValidatedScripts = validatedScripts };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.Equal(1, output.RegisteredCount);
            Assert.True(File.Exists(output.RegistryPath));

            // Verify file contents
            var json = await File.ReadAllTextAsync(output.RegistryPath);
            Assert.Contains("Test Script Content 1", json);
            Assert.DoesNotContain("Test Script Content 2", json);
        }
        finally
        {
            // Cleanup
            if (File.Exists(tempPath))
            {
                File.Delete(tempPath);
            }
        }
    }

    [Fact]
    public async Task ScriptRegistryUpdateStage_AvoidsDuplicates()
    {
        // Arrange
        var tempPath = Path.Combine(Path.GetTempPath(), $"test_script_registry_{Guid.NewGuid()}.json");
        var stage = new ScriptRegistryUpdateStage(tempPath);
        
        var script = new EnhancedScript { Content = "Duplicate Test Script" };
        var input = new ScriptRegistryUpdateInput
        {
            ValidatedScripts = new List<ValidatedScript>
            {
                new ValidatedScript { Script = script, IsValid = true }
            }
        };

        try
        {
            // Act - Add once
            var output1 = await stage.ExecuteAsync(input, null, CancellationToken.None);
            Assert.Equal(1, output1.RegisteredCount);

            // Act - Try to add same script again
            var output2 = await stage.ExecuteAsync(input, null, CancellationToken.None);
            
            // Assert - Should not add duplicate
            Assert.Equal(0, output2.RegisteredCount);
        }
        finally
        {
            // Cleanup
            if (File.Exists(tempPath))
            {
                File.Delete(tempPath);
            }
        }
    }

    #endregion
}
