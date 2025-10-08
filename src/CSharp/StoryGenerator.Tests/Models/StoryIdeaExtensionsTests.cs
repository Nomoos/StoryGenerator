using System;
using System.Collections.Generic;
using System.Text.Json;
using StoryGenerator.Core.Models;
using Xunit;

namespace StoryGenerator.Tests.Models;

/// <summary>
/// Tests for StoryIdea model with source stats and scored strings.
/// </summary>
public class StoryIdeaExtensionsTests
{
    [Fact]
    public void StoryIdea_WithSourceStats_SerializesCorrectly()
    {
        // Arrange
        var storyIdea = new StoryIdea
        {
            StoryTitle = "My Amazing Story",
            SourceStats = new SourceStats
            {
                Platform = "reddit",
                SourceUrl = "https://reddit.com/r/test/comments/123",
                Views = 50000,
                Likes = 5000,
                Comments = 250,
                Shares = 100,
                EngagementRate = 10.7,
                NormalizedScore = 82.5
            }
        };

        // Act
        var json = JsonSerializer.Serialize(storyIdea, new JsonSerializerOptions { WriteIndented = true });
        var deserialized = JsonSerializer.Deserialize<StoryIdea>(json);

        // Assert
        Assert.NotNull(deserialized);
        Assert.NotNull(deserialized.SourceStats);
        Assert.Equal("reddit", deserialized.SourceStats.Platform);
        Assert.Equal(50000, deserialized.SourceStats.Views);
        Assert.Equal(82.5, deserialized.SourceStats.NormalizedScore);
    }

    [Fact]
    public void StoryIdea_WithTitleSuggestions_SerializesCorrectly()
    {
        // Arrange
        var storyIdea = new StoryIdea
        {
            StoryTitle = "Original Title",
            TitleSuggestions = new List<ScoredString>
            {
                new ScoredString("Amazing Title Option 1", 92.0, "llm_generated"),
                new ScoredString("Great Title Option 2", 87.5, "llm_generated"),
                new ScoredString("Original Title", 75.0, "source_title")
            }
        };

        // Act
        var json = JsonSerializer.Serialize(storyIdea, new JsonSerializerOptions { WriteIndented = true });
        var deserialized = JsonSerializer.Deserialize<StoryIdea>(json);

        // Assert
        Assert.NotNull(deserialized);
        Assert.NotNull(deserialized.TitleSuggestions);
        Assert.Equal(3, deserialized.TitleSuggestions.Count);
        Assert.Equal("Amazing Title Option 1", deserialized.TitleSuggestions[0].Value);
        Assert.Equal(92.0, deserialized.TitleSuggestions[0].Score);
    }

    [Fact]
    public void StoryIdea_WithScoredTags_SerializesCorrectly()
    {
        // Arrange
        var storyIdea = new StoryIdea
        {
            StoryTitle = "Test Story",
            ScoredTags = new List<ScoredString>
            {
                new ScoredString("friendship", 85.0, "ai_extracted"),
                new ScoredString("betrayal", 80.0, "ai_extracted"),
                new ScoredString("trust", 75.0, "ai_extracted")
            }
        };

        // Act
        var json = JsonSerializer.Serialize(storyIdea, new JsonSerializerOptions { WriteIndented = true });
        var deserialized = JsonSerializer.Deserialize<StoryIdea>(json);

        // Assert
        Assert.NotNull(deserialized);
        Assert.NotNull(deserialized.ScoredTags);
        Assert.Equal(3, deserialized.ScoredTags.Count);
        Assert.Equal("friendship", deserialized.ScoredTags[0].Value);
        Assert.Equal(85.0, deserialized.ScoredTags[0].Score);
    }

    [Fact]
    public void StoryIdea_WithCompleteData_SerializesCorrectly()
    {
        // Arrange
        var storyIdea = new StoryIdea
        {
            StoryTitle = "Complete Story Example",
            NarratorGender = "female",
            Tone = "emotional",
            Theme = "friendship",
            SourceStats = new SourceStats
            {
                Platform = "youtube",
                Views = 2000000,
                Likes = 100000,
                NormalizedScore = 88.0
            },
            TitleSuggestions = new List<ScoredString>
            {
                new ScoredString("Best Friend Betrayal", 90.0, "llm_generated")
            },
            ScoredTags = new List<ScoredString>
            {
                new ScoredString("friendship", 85.0, "ai_extracted"),
                new ScoredString("betrayal", 82.0, "ai_extracted")
            }
        };

        // Act
        var json = JsonSerializer.Serialize(storyIdea, new JsonSerializerOptions { WriteIndented = true });
        var deserialized = JsonSerializer.Deserialize<StoryIdea>(json);

        // Assert
        Assert.NotNull(deserialized);
        Assert.Equal("Complete Story Example", deserialized.StoryTitle);
        Assert.NotNull(deserialized.SourceStats);
        Assert.NotNull(deserialized.TitleSuggestions);
        Assert.NotNull(deserialized.ScoredTags);
        Assert.Single(deserialized.TitleSuggestions);
        Assert.Equal(2, deserialized.ScoredTags.Count);
    }

    [Fact]
    public void StoryIdea_BackwardCompatibility_WorksWithoutNewFields()
    {
        // Arrange - Create a story idea without new fields
        var storyIdea = new StoryIdea
        {
            StoryTitle = "Simple Story",
            NarratorGender = "male",
            Tone = "humorous"
        };

        // Act
        var json = JsonSerializer.Serialize(storyIdea);
        var deserialized = JsonSerializer.Deserialize<StoryIdea>(json);

        // Assert - Should work without the new optional fields
        Assert.NotNull(deserialized);
        Assert.Equal("Simple Story", deserialized.StoryTitle);
        Assert.Null(deserialized.SourceStats);
        Assert.Null(deserialized.TitleSuggestions);
        Assert.Null(deserialized.ScoredTags);
    }

    [Fact]
    public void StoryIdea_ToFile_IncludesNewFields()
    {
        // Arrange
        var tempFile = System.IO.Path.GetTempFileName();
        var storyIdea = new StoryIdea
        {
            StoryTitle = "File Test Story",
            SourceStats = new SourceStats
            {
                Platform = "tiktok",
                Views = 5000000,
                NormalizedScore = 90.0
            },
            TitleSuggestions = new List<ScoredString>
            {
                new ScoredString("Viral Title", 95.0, "ai_generated")
            }
        };

        try
        {
            // Act
            storyIdea.ToFileAsync(tempFile).Wait();
            var loaded = StoryIdea.FromFileAsync(tempFile).Result;

            // Assert
            Assert.NotNull(loaded);
            Assert.NotNull(loaded.SourceStats);
            Assert.Equal("tiktok", loaded.SourceStats.Platform);
            Assert.NotNull(loaded.TitleSuggestions);
            Assert.Single(loaded.TitleSuggestions);
            Assert.Equal("Viral Title", loaded.TitleSuggestions[0].Value);
        }
        finally
        {
            // Cleanup
            if (System.IO.File.Exists(tempFile))
            {
                System.IO.File.Delete(tempFile);
            }
        }
    }
}
