using StoryGenerator.Pipeline.Stages;
using StoryGenerator.Pipeline.Stages.Models;
using StoryGenerator.Core.Models;
using Xunit;

namespace StoryGenerator.Tests.Pipeline;

/// <summary>
/// Tests for Phase 3 Group 1: Idea Generation Stages
/// </summary>
public class IdeaGenerationStagesTests
{
    #region Test Data Setup

    private List<CollectedIdea> CreateTestCollectedIdeas()
    {
        return new List<CollectedIdea>
        {
            new CollectedIdea
            {
                Id = "test1",
                IdeaContent = "A heartwarming story about friendship and trust between unlikely companions.",
                CreatedAt = DateTime.UtcNow,
                CollectorName = "TestCollector"
            },
            new CollectedIdea
            {
                Id = "test2",
                IdeaContent = "An unexpected twist reveals a long-held secret that changes everything.",
                CreatedAt = DateTime.UtcNow,
                CollectorName = "TestCollector"
            }
        };
    }

    #endregion

    #region Stage 1: Reddit Adaptation Tests

    [Fact]
    public async Task RedditAdaptationStage_ValidInput_AdaptsSuccessfully()
    {
        // Arrange
        var stage = new RedditAdaptationStage();
        var input = new RedditAdaptationInput
        {
            CollectedIdeas = CreateTestCollectedIdeas()
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.NotNull(output);
        Assert.Equal(2, output.AdaptedIdeas.Count);
        Assert.All(output.AdaptedIdeas, idea =>
        {
            Assert.NotEmpty(idea.Content);
            Assert.NotNull(idea.Themes);
            Assert.NotNull(idea.EmotionalHooks);
        });
    }

    [Fact]
    public async Task RedditAdaptationStage_ExtractsThemes()
    {
        // Arrange
        var stage = new RedditAdaptationStage();
        var input = new RedditAdaptationInput
        {
            CollectedIdeas = CreateTestCollectedIdeas()
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        var firstIdea = output.AdaptedIdeas[0];
        Assert.Contains("friendship", firstIdea.Themes);
        // Note: "trust" is extracted from "betray" or "trust" keywords
        // The test content has "trust" so it should also extract "betrayal" theme
    }

    [Fact]
    public async Task RedditAdaptationStage_EmptyInput_FailsValidation()
    {
        // Arrange
        var stage = new RedditAdaptationStage();
        var input = new RedditAdaptationInput
        {
            CollectedIdeas = new List<CollectedIdea>()
        };

        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(
            () => stage.ExecuteAsync(input, null, CancellationToken.None));
    }

    #endregion

    #region Stage 2: LLM Idea Generation Tests

    [Fact]
    public async Task LLMIdeaGenerationStage_ValidInput_GeneratesVariations()
    {
        // Arrange
        var stage = new LLMIdeaGenerationStage();
        var adaptedIdeas = new List<AdaptedIdea>
        {
            new AdaptedIdea
            {
                Content = "Test content about friendship",
                Themes = new List<string> { "friendship", "trust" },
                EmotionalHooks = new List<string> { "joy", "surprise" }
            }
        };
        var input = new LLMIdeaGenerationInput
        {
            AdaptedIdeas = adaptedIdeas,
            VariationsPerIdea = 3
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.NotNull(output);
        Assert.Equal(3, output.GeneratedIdeas.Count);
        Assert.All(output.GeneratedIdeas, idea =>
        {
            Assert.NotEmpty(idea.StoryTitle);
            Assert.NotNull(idea.Tone);
        });
    }

    [Fact]
    public async Task LLMIdeaGenerationStage_CreatesDistinctVariations()
    {
        // Arrange
        var stage = new LLMIdeaGenerationStage();
        var input = new LLMIdeaGenerationInput
        {
            AdaptedIdeas = new List<AdaptedIdea>
            {
                new AdaptedIdea
                {
                    Content = "Test content",
                    Themes = new List<string> { "test" }
                }
            },
            VariationsPerIdea = 3
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        var titles = output.GeneratedIdeas.Select(i => i.StoryTitle).ToList();
        Assert.Equal(3, titles.Distinct().Count()); // All titles should be unique
    }

    #endregion

    #region Stage 3: Idea Clustering Tests

    [Fact]
    public async Task IdeaClusteringStage_GroupsByTheme()
    {
        // Arrange
        var stage = new IdeaClusteringStage();
        var ideas = new List<StoryIdea>
        {
            new StoryIdea { StoryTitle = "Story 1", Theme = "friendship" },
            new StoryIdea { StoryTitle = "Story 2", Theme = "friendship" },
            new StoryIdea { StoryTitle = "Story 3", Theme = "romance" }
        };
        var input = new IdeaClusteringInput { Ideas = ideas };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.NotNull(output);
        Assert.Equal(2, output.Clusters.Count); // friendship and romance
        var friendshipCluster = output.Clusters.First(c => c.Name == "friendship");
        Assert.Equal(2, friendshipCluster.Ideas.Count);
    }

    [Fact]
    public async Task IdeaClusteringStage_CalculatesAverageScores()
    {
        // Arrange
        var stage = new IdeaClusteringStage();
        var ideas = new List<StoryIdea>
        {
            new StoryIdea
            {
                StoryTitle = "Story 1",
                Theme = "test",
                Potential = new ViralPotential { Overall = 80 }
            },
            new StoryIdea
            {
                StoryTitle = "Story 2",
                Theme = "test",
                Potential = new ViralPotential { Overall = 60 }
            }
        };
        var input = new IdeaClusteringInput { Ideas = ideas };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        var cluster = output.Clusters.First();
        Assert.Equal(0.7, cluster.AverageViralScore); // (80 + 60) / 2 / 100 = 0.7
    }

    #endregion

    #region Stage 4: Idea Ranking Tests

    [Fact]
    public async Task IdeaRankingStage_RanksIdeasByScore()
    {
        // Arrange
        var stage = new IdeaRankingStage();
        var cluster = new IdeaCluster
        {
            Ideas = new List<StoryIdea>
            {
                new StoryIdea
                {
                    StoryTitle = "Low Score",
                    Potential = new ViralPotential { Overall = 30 }
                },
                new StoryIdea
                {
                    StoryTitle = "High Score",
                    Potential = new ViralPotential { Overall = 90 }
                },
                new StoryIdea
                {
                    StoryTitle = "Mid Score",
                    Potential = new ViralPotential { Overall = 60 }
                }
            }
        };
        var input = new IdeaRankingInput { Clusters = new List<IdeaCluster> { cluster } };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.Equal(3, output.RankedIdeas.Count);
        Assert.Equal("High Score", output.RankedIdeas[0].Idea.StoryTitle);
        Assert.Equal(1, output.RankedIdeas[0].Rank);
        Assert.Equal("Low Score", output.RankedIdeas[2].Idea.StoryTitle);
        Assert.Equal(3, output.RankedIdeas[2].Rank);
    }

    #endregion

    #region Stage 5: Idea Selection Tests

    [Fact]
    public async Task IdeaSelectionStage_SelectsTopIdeas()
    {
        // Arrange
        var stage = new IdeaSelectionStage();
        var rankedIdeas = Enumerable.Range(1, 10)
            .Select(i => new RankedIdea
            {
                Idea = new StoryIdea { StoryTitle = $"Idea {i}" },
                Rank = i,
                Score = 1.0 - (i * 0.1)
            })
            .ToList();
        var input = new IdeaSelectionInput
        {
            RankedIdeas = rankedIdeas,
            SelectCount = 3
        };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.Equal(3, output.SelectedIdeas.Count);
        Assert.Equal("Idea 1", output.SelectedIdeas[0].StoryTitle);
        Assert.Equal("Idea 2", output.SelectedIdeas[1].StoryTitle);
        Assert.Equal("Idea 3", output.SelectedIdeas[2].StoryTitle);
    }

    #endregion

    #region Stage 6: Idea Validation Tests

    [Fact]
    public async Task IdeaValidationStage_ValidatesRequiredFields()
    {
        // Arrange
        var stage = new IdeaValidationStage();
        var ideas = new List<StoryIdea>
        {
            new StoryIdea
            {
                StoryTitle = "Valid Idea",
                Tone = "emotional",
                Theme = "friendship",
                Potential = new ViralPotential { Overall = 70 }
            },
            new StoryIdea
            {
                StoryTitle = "", // Invalid - empty title
                Tone = "dramatic"
            }
        };
        var input = new IdeaValidationInput { Ideas = ideas };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        Assert.Equal(2, output.ValidatedIdeas.Count);
        Assert.True(output.ValidatedIdeas[0].IsValid);
        Assert.False(output.ValidatedIdeas[1].IsValid);
        Assert.Contains("Story title is required", output.ValidatedIdeas[1].ValidationMessages);
    }

    [Fact]
    public async Task IdeaValidationStage_WarnsLowViralScore()
    {
        // Arrange
        var stage = new IdeaValidationStage();
        var ideas = new List<StoryIdea>
        {
            new StoryIdea
            {
                StoryTitle = "Low Score Idea",
                Potential = new ViralPotential { Overall = 20 }
            }
        };
        var input = new IdeaValidationInput { Ideas = ideas };

        // Act
        var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

        // Assert
        var validated = output.ValidatedIdeas[0];
        Assert.True(validated.IsValid); // Still valid, but with warnings
        Assert.Contains("Warning: Low viral potential score", validated.ValidationMessages);
    }

    #endregion

    #region Stage 7: Idea Registry Update Tests

    [Fact]
    public async Task IdeaRegistryUpdateStage_SavesValidIdeas()
    {
        // Arrange
        var tempPath = Path.Combine(Path.GetTempPath(), $"test_registry_{Guid.NewGuid()}.json");
        var stage = new IdeaRegistryUpdateStage(tempPath);
        
        var validatedIdeas = new List<ValidatedIdea>
        {
            new ValidatedIdea
            {
                Idea = new StoryIdea { StoryTitle = "Test Idea 1" },
                IsValid = true
            },
            new ValidatedIdea
            {
                Idea = new StoryIdea { StoryTitle = "Test Idea 2" },
                IsValid = false // Should be filtered out
            }
        };
        var input = new IdeaRegistryUpdateInput { ValidatedIdeas = validatedIdeas };

        try
        {
            // Act
            var output = await stage.ExecuteAsync(input, null, CancellationToken.None);

            // Assert
            Assert.Equal(1, output.RegisteredCount);
            Assert.True(File.Exists(output.RegistryPath));

            // Verify file contents
            var json = await File.ReadAllTextAsync(output.RegistryPath);
            Assert.Contains("Test Idea 1", json);
            Assert.DoesNotContain("Test Idea 2", json);
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
    public async Task IdeaRegistryUpdateStage_AvoidsDuplicates()
    {
        // Arrange
        var tempPath = Path.Combine(Path.GetTempPath(), $"test_registry_{Guid.NewGuid()}.json");
        var stage = new IdeaRegistryUpdateStage(tempPath);
        
        var idea = new StoryIdea { StoryTitle = "Duplicate Test" };
        var input = new IdeaRegistryUpdateInput
        {
            ValidatedIdeas = new List<ValidatedIdea>
            {
                new ValidatedIdea { Idea = idea, IsValid = true }
            }
        };

        try
        {
            // Act - Add once
            var output1 = await stage.ExecuteAsync(input, null, CancellationToken.None);
            Assert.Equal(1, output1.RegisteredCount);

            // Act - Try to add same idea again
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
