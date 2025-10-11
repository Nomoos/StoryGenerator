using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using PrismQ.Shared.Core;
using PrismQ.Shared.Core.Collectors;
using PrismQ.Shared.Models;
using PrismQ.Shared.Core.Services;
using Xunit;

namespace StoryGenerator.Tests.Collectors;

/// <summary>
/// Tests for IdeaCollector functionality.
/// </summary>
public class IdeaCollectorTests
{
    [Fact]
    public void IdeaSource_Creation_SetsDefaultValues()
    {
        // Arrange & Act
        var source = new IdeaSource
        {
            Title = "Test Story",
            OriginalText = "This is a test story about friendship.",
            SourceType = "test"
        };

        // Assert
        Assert.NotNull(source.Id);
        Assert.Equal("Test Story", source.Title);
        Assert.Equal("This is a test story about friendship.", source.OriginalText);
        Assert.Equal("test", source.SourceType);
        Assert.False(source.QuestionableAuthorship);
        Assert.NotNull(source.ImageLinks);
        Assert.NotNull(source.Tags);
    }

    [Fact]
    public void CollectedIdea_CalculatesOverallScore()
    {
        // Arrange
        var idea = new CollectedIdea
        {
            IdeaContent = "A story about unexpected friendship",
            ViralPotential = new ViralPotential()
        };

        // Set some scores
        idea.ViralPotential.Gender["woman"] = 80;
        idea.ViralPotential.Gender["man"] = 70;
        idea.ViralPotential.AgeGroups["15_20"] = 85;
        idea.ViralPotential.AgeGroups["20_25"] = 75;
        idea.ViralPotential.Platforms["tiktok"] = 90;
        idea.ViralPotential.Regions["US"] = 80;

        // Act
        idea.CalculateOverallScore();

        // Assert
        Assert.True(idea.ViralPotential.Overall > 0);
        // Average of 80, 70, 85, 75, 90, 80 = 80
        Assert.Equal(80, idea.ViralPotential.Overall);
    }

    [Fact]
    public void ViralPotential_CalculateOverall_HandlesZeroScores()
    {
        // Arrange
        var potential = new ViralPotential();
        
        // Set mix of zero and non-zero scores
        potential.Gender["woman"] = 0;
        potential.Gender["man"] = 60;
        potential.AgeGroups["15_20"] = 80;

        // Act
        var overall = potential.CalculateOverall();

        // Assert
        // Should only average non-zero scores: (60 + 80) / 2 = 70
        Assert.Equal(70, overall);
    }

    [Fact]
    public void ViralPotential_CalculateOverall_AllZeros_ReturnsZero()
    {
        // Arrange
        var potential = new ViralPotential();
        // All scores are 0 by default

        // Act
        var overall = potential.CalculateOverall();

        // Assert
        Assert.Equal(0, overall);
    }

    [Fact]
    public async Task ManualIdeaCollector_CollectsAndTransforms()
    {
        // Arrange
        var collector = new ManualIdeaCollector();
        var sources = new List<IdeaSource>
        {
            new IdeaSource
            {
                Title = "A Story About Friendship",
                OriginalText = "Two friends discover something unexpected.",
                SourceType = "manual",
                Tags = new List<string> { "friendship", "discovery" }
            }
        };

        var parameters = new Dictionary<string, object>
        {
            { "sources", sources }
        };

        // Act
        var ideas = await collector.CollectAndTransformAsync(parameters);

        // Assert
        Assert.NotEmpty(ideas);
        Assert.Single(ideas);
        var idea = ideas[0];
        Assert.NotNull(idea.IdeaContent);
        Assert.NotNull(idea.Source);
        Assert.Equal("ManualIdeaCollector", idea.CollectorName);
        Assert.True(idea.ViralPotential.Overall >= 0);
    }

    [Fact]
    public async Task ManualIdeaCollector_ValidatesSource()
    {
        // Arrange
        var collector = new ManualIdeaCollector();
        var sources = new List<IdeaSource>
        {
            new IdeaSource
            {
                Title = "Valid Source",
                OriginalText = "Valid content",
                QuestionableAuthorship = false
            },
            new IdeaSource
            {
                Title = "Questionable Source",
                OriginalText = "Questionable content",
                QuestionableAuthorship = true // Should be filtered out
            }
        };

        var parameters = new Dictionary<string, object>
        {
            { "sources", sources }
        };

        // Act
        var ideas = await collector.CollectAndTransformAsync(parameters);

        // Assert
        Assert.Single(ideas); // Only one idea should pass validation
        Assert.Contains(ideas, i => i.Source?.Title == "Valid Source");
        Assert.DoesNotContain(ideas, i => i.Source?.Title == "Questionable Source");
    }

    [Fact]
    public void IdeaCollectorRegistry_RegistersIdeas()
    {
        // Arrange
        var registry = new IdeaCollectorRegistry();
        var idea1 = new CollectedIdea
        {
            IdeaContent = "Idea 1",
            CollectorName = "Test1",
            ViralPotential = new ViralPotential()
        };
        idea1.ViralPotential.Gender["woman"] = 80;
        idea1.CalculateOverallScore();

        var idea2 = new CollectedIdea
        {
            IdeaContent = "Idea 2",
            CollectorName = "Test2",
            ViralPotential = new ViralPotential()
        };
        idea2.ViralPotential.Gender["man"] = 70;
        idea2.CalculateOverallScore();

        // Act
        registry.RegisterIdea(idea1);
        registry.RegisterIdea(idea2);

        // Assert
        Assert.Equal(2, registry.TotalIdeas);
        Assert.NotEmpty(registry.CollectorStats);
    }

    [Fact]
    public void IdeaCollectorRegistry_GetIdeasByMinScore()
    {
        // Arrange
        var registry = new IdeaCollectorRegistry();
        
        var idea1 = new CollectedIdea { IdeaContent = "High Score" };
        idea1.ViralPotential.Gender["woman"] = 90;
        idea1.CalculateOverallScore();
        
        var idea2 = new CollectedIdea { IdeaContent = "Low Score" };
        idea2.ViralPotential.Gender["man"] = 30;
        idea2.CalculateOverallScore();

        registry.RegisterIdeas(new[] { idea1, idea2 });

        // Act
        var highScoreIdeas = registry.GetIdeasByMinScore(50).ToList();

        // Assert
        Assert.Single(highScoreIdeas);
        Assert.Equal("High Score", highScoreIdeas[0].IdeaContent);
    }

    [Fact]
    public void IdeaCollectorRegistry_GetTopIdeas()
    {
        // Arrange
        var registry = new IdeaCollectorRegistry();
        
        for (int i = 0; i < 10; i++)
        {
            var idea = new CollectedIdea { IdeaContent = $"Idea {i}" };
            idea.ViralPotential.Gender["woman"] = 50 + i * 5;
            idea.CalculateOverallScore();
            registry.RegisterIdea(idea);
        }

        // Act
        var topIdeas = registry.GetTopIdeas(3).ToList();

        // Assert
        Assert.Equal(3, topIdeas.Count);
        // Should be in descending order
        Assert.True(topIdeas[0].ViralPotential.Overall >= topIdeas[1].ViralPotential.Overall);
        Assert.True(topIdeas[1].ViralPotential.Overall >= topIdeas[2].ViralPotential.Overall);
    }

    [Fact]
    public void IdeaCollectorRegistry_GetIdeasByCategoryScores()
    {
        // Arrange
        var registry = new IdeaCollectorRegistry();
        
        var idea1 = new CollectedIdea { IdeaContent = "Women 15-20" };
        idea1.ViralPotential.Gender["woman"] = 80;
        idea1.ViralPotential.AgeGroups["15_20"] = 75;
        idea1.CalculateOverallScore();
        
        var idea2 = new CollectedIdea { IdeaContent = "Men 20-25" };
        idea2.ViralPotential.Gender["man"] = 70;
        idea2.ViralPotential.AgeGroups["20_25"] = 65;
        idea2.CalculateOverallScore();

        registry.RegisterIdeas(new[] { idea1, idea2 });

        // Act - Filter for women with high scores
        var filters = new Dictionary<string, int>
        {
            { "gender_woman", 70 },
            { "age_15_20", 70 }
        };
        var filteredIdeas = registry.GetIdeasByCategoryScores(filters).ToList();

        // Assert
        Assert.Single(filteredIdeas);
        Assert.Equal("Women 15-20", filteredIdeas[0].IdeaContent);
    }

    [Fact]
    public void IdeaCollectorRegistry_ToJson_Serializes()
    {
        // Arrange
        var registry = new IdeaCollectorRegistry();
        var idea = new CollectedIdea
        {
            IdeaContent = "Test Idea",
            CollectorName = "TestCollector"
        };
        idea.ViralPotential.Gender["woman"] = 80;
        idea.CalculateOverallScore();
        registry.RegisterIdea(idea);

        // Act
        var json = registry.ToJson();

        // Assert
        Assert.NotNull(json);
        Assert.Contains("total_ideas", json);
        Assert.Contains("collector_stats", json);
        Assert.Contains("Test Idea", json);
    }

    [Fact]
    public void BaseIdeaCollector_IsOriginalContent_DetectsSimilarity()
    {
        // Arrange
        var collector = new ManualIdeaCollector();
        
        // Use reflection to access protected method
        var method = typeof(BaseIdeaCollector).GetMethod(
            "IsOriginalContent",
            System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance
        );
        Assert.NotNull(method);

        // Act & Assert
        // Very similar content (should fail)
        var result1 = (bool)method.Invoke(collector, new object[] 
        { 
            "This is a test story about friendship and love",
            "This is a test story about friendship and love"
        })!;
        Assert.False(result1);

        // Different content (should pass)
        var result2 = (bool)method.Invoke(collector, new object[] 
        { 
            "A completely different story about adventure",
            "This is a test story about friendship and love"
        })!;
        Assert.True(result2);
    }
}
