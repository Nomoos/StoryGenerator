using System;
using System.Collections.Generic;
using System.Text.Json;
using StoryGenerator.Core.Models;
using Xunit;

namespace StoryGenerator.Tests.Models;

/// <summary>
/// Tests for SourceStats model and related functionality.
/// </summary>
public class SourceStatsTests
{
    [Fact]
    public void SourceStats_DefaultConstructor_SetsDefaults()
    {
        // Arrange & Act
        var stats = new SourceStats();

        // Assert
        Assert.Equal(string.Empty, stats.Platform);
        Assert.Equal(string.Empty, stats.SourceUrl);
        Assert.Equal(0, stats.Views);
        Assert.Equal(0, stats.Likes);
        Assert.Equal(0, stats.Shares);
        Assert.Equal(0, stats.Comments);
        Assert.NotNull(stats.RawData);
        Assert.Empty(stats.RawData);
    }

    [Fact]
    public void SourceStats_CalculateEngagementRate_ReturnsCorrectValue()
    {
        // Arrange
        var stats = new SourceStats
        {
            Views = 10000,
            Likes = 500,
            Comments = 100,
            Shares = 50,
            Saves = 25
        };

        // Act
        var rate = stats.CalculateEngagementRate();

        // Assert
        // (500 + 100 + 50 + 25) / 10000 * 100 = 6.75%
        Assert.Equal(6.75, rate);
        Assert.Equal(6.75, stats.EngagementRate);
    }

    [Fact]
    public void SourceStats_CalculateEngagementRate_WithZeroViews_ReturnsZero()
    {
        // Arrange
        var stats = new SourceStats
        {
            Views = 0,
            Likes = 100
        };

        // Act
        var rate = stats.CalculateEngagementRate();

        // Assert
        Assert.Equal(0, rate);
    }

    [Fact]
    public void SourceStats_ToString_ReturnsFormattedString()
    {
        // Arrange
        var stats = new SourceStats
        {
            Platform = "reddit",
            Views = 15000,
            Likes = 1200,
            NormalizedScore = 85.5
        };

        // Act
        var result = stats.ToString();

        // Assert
        Assert.Contains("reddit", result);
        Assert.Contains("15,000", result);
        Assert.Contains("1,200", result);
        Assert.Contains("85.5", result);
    }

    [Fact]
    public void SourceStats_JsonSerialization_RoundTrips()
    {
        // Arrange
        var original = new SourceStats
        {
            Platform = "youtube",
            SourceUrl = "https://youtube.com/watch?v=test123",
            Views = 1000000,
            Likes = 50000,
            Dislikes = 500,
            Shares = 10000,
            Comments = 5000,
            EngagementRate = 6.5,
            NormalizedScore = 87.3
        };
        original.RawData["video_id"] = "test123";
        original.RawData["category"] = "Entertainment";

        // Act
        var json = JsonSerializer.Serialize(original);
        var deserialized = JsonSerializer.Deserialize<SourceStats>(json);

        // Assert
        Assert.NotNull(deserialized);
        Assert.Equal(original.Platform, deserialized.Platform);
        Assert.Equal(original.SourceUrl, deserialized.SourceUrl);
        Assert.Equal(original.Views, deserialized.Views);
        Assert.Equal(original.Likes, deserialized.Likes);
        Assert.Equal(original.Dislikes, deserialized.Dislikes);
        Assert.Equal(original.NormalizedScore, deserialized.NormalizedScore);
    }
}

/// <summary>
/// Tests for ScoredString model.
/// </summary>
public class ScoredStringTests
{
    [Fact]
    public void ScoredString_DefaultConstructor_SetsDefaults()
    {
        // Arrange & Act
        var scored = new ScoredString();

        // Assert
        Assert.Equal(string.Empty, scored.Value);
        Assert.Equal(0, scored.Score);
        Assert.Equal("unknown", scored.Source);
        Assert.NotNull(scored.Metadata);
        Assert.Empty(scored.Metadata);
    }

    [Fact]
    public void ScoredString_ConstructorWithValueAndScore_SetsProperties()
    {
        // Arrange & Act
        var scored = new ScoredString("Test Title", 87.5);

        // Assert
        Assert.Equal("Test Title", scored.Value);
        Assert.Equal(87.5, scored.Score);
        Assert.Equal("unknown", scored.Source);
    }

    [Fact]
    public void ScoredString_ConstructorWithAllFields_SetsProperties()
    {
        // Arrange & Act
        var scored = new ScoredString(
            "Amazing Story Title",
            92.0,
            "llm_generated",
            "Strong hook and emotional appeal"
        );

        // Assert
        Assert.Equal("Amazing Story Title", scored.Value);
        Assert.Equal(92.0, scored.Score);
        Assert.Equal("llm_generated", scored.Source);
        Assert.Equal("Strong hook and emotional appeal", scored.Rationale);
    }

    [Fact]
    public void ScoredString_CompareTo_SortsByScoreDescending()
    {
        // Arrange
        var list = new List<ScoredString>
        {
            new ScoredString("Low", 50.0),
            new ScoredString("High", 90.0),
            new ScoredString("Medium", 70.0)
        };

        // Act
        list.Sort((a, b) => a.CompareTo(b));

        // Assert
        Assert.Equal("High", list[0].Value);
        Assert.Equal("Medium", list[1].Value);
        Assert.Equal("Low", list[2].Value);
    }

    [Fact]
    public void ScoredString_ToString_ReturnsFormattedString()
    {
        // Arrange
        var scored = new ScoredString("Test", 75.5, "manual");

        // Act
        var result = scored.ToString();

        // Assert
        Assert.Contains("Test", result);
        Assert.Contains("75.5", result);
        Assert.Contains("manual", result);
    }

    [Fact]
    public void ScoredString_JsonSerialization_RoundTrips()
    {
        // Arrange
        var original = new ScoredString
        {
            Value = "Test Title",
            Score = 88.5,
            Source = "ai_generated",
            Rationale = "Good emotional hook"
        };
        original.Metadata["platform"] = "youtube";
        original.Metadata["test_group"] = "A";

        // Act
        var json = JsonSerializer.Serialize(original);
        var deserialized = JsonSerializer.Deserialize<ScoredString>(json);

        // Assert
        Assert.NotNull(deserialized);
        Assert.Equal(original.Value, deserialized.Value);
        Assert.Equal(original.Score, deserialized.Score);
        Assert.Equal(original.Source, deserialized.Source);
        Assert.Equal(original.Rationale, deserialized.Rationale);
    }
}

/// <summary>
/// Tests for SourceStatsNormalizer utility.
/// </summary>
public class SourceStatsNormalizerTests
{
    [Fact]
    public void NormalizeReddit_WithHighUpvotes_ReturnsHighScore()
    {
        // Arrange
        var stats = new SourceStats
        {
            Platform = "reddit",
            Views = 100000,
            Likes = 10000, // High upvotes
            Comments = 500,
            Shares = 100
        };
        stats.CalculateEngagementRate();

        // Act
        var score = SourceStatsNormalizer.NormalizeReddit(stats);

        // Assert
        Assert.InRange(score, 70, 100);
    }

    [Fact]
    public void NormalizeYouTube_WithHighViews_ReturnsHighScore()
    {
        // Arrange
        var stats = new SourceStats
        {
            Platform = "youtube",
            Views = 5000000, // 5M views
            Likes = 250000,
            Comments = 10000
        };
        stats.CalculateEngagementRate();

        // Act
        var score = SourceStatsNormalizer.NormalizeYouTube(stats);

        // Assert
        Assert.InRange(score, 60, 100);
    }

    [Fact]
    public void NormalizeTikTok_WithViralMetrics_ReturnsHighScore()
    {
        // Arrange
        var stats = new SourceStats
        {
            Platform = "tiktok",
            Views = 10000000, // 10M views
            Likes = 1000000,
            Shares = 50000 // High share count (viral indicator)
        };
        stats.CalculateEngagementRate();

        // Act
        var score = SourceStatsNormalizer.NormalizeTikTok(stats);

        // Assert
        Assert.InRange(score, 70, 100);
    }

    [Fact]
    public void Normalize_RoutesToCorrectPlatform()
    {
        // Arrange
        var redditStats = new SourceStats { Platform = "reddit", Likes = 5000, Views = 50000 };
        var youtubeStats = new SourceStats { Platform = "youtube", Views = 1000000 };

        // Act
        var redditScore = SourceStatsNormalizer.Normalize(redditStats);
        var youtubeScore = SourceStatsNormalizer.Normalize(youtubeStats);

        // Assert
        Assert.InRange(redditScore, 0, 100);
        Assert.InRange(youtubeScore, 0, 100);
    }

    [Fact]
    public void UpdateScores_CalculatesBothMetrics()
    {
        // Arrange
        var stats = new SourceStats
        {
            Platform = "reddit",
            Views = 10000,
            Likes = 1000,
            Comments = 100,
            Shares = 50
        };

        // Act
        SourceStatsNormalizer.UpdateScores(stats);

        // Assert
        Assert.InRange(stats.EngagementRate, 0, 100);
        Assert.InRange(stats.NormalizedScore, 0, 100);
        Assert.True(stats.EngagementRate > 0);
        Assert.True(stats.NormalizedScore > 0);
    }

    [Fact]
    public void NormalizeGeneric_HandlesUnknownPlatform()
    {
        // Arrange
        var stats = new SourceStats
        {
            Platform = "unknown_platform",
            Views = 50000,
            Likes = 5000
        };
        stats.CalculateEngagementRate();

        // Act
        var score = SourceStatsNormalizer.NormalizeGeneric(stats);

        // Assert
        Assert.InRange(score, 0, 100);
    }
}
