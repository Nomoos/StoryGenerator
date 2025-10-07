using System;
using System.Collections.Generic;
using StoryGenerator.Models;
using Xunit;

namespace StoryGenerator.Tests.Models
{
    /// <summary>
    /// Unit tests for ScriptVersion model.
    /// Tests the Prototype pattern (ICloneable) implementation and deep cloning.
    /// </summary>
    public class ScriptVersionTests
    {
        [Fact]
        public void DeepClone_CreatesIndependentCopy()
        {
            // Arrange
            var original = new ScriptVersion
            {
                TitleId = "test_001",
                Version = "v1",
                Content = "Original content",
                FilePath = "/path/to/script.md",
                TargetAudience = new AudienceSegment("men", "18-23"),
                Score = 85.5,
                PreviousVersion = "v0",
                AppliedFeedback = "Improve pacing",
                GenerationSource = "local_llm"
            };

            // Act
            var clone = original.DeepClone();

            // Assert
            Assert.NotSame(original, clone);
            Assert.Equal(original.TitleId, clone.TitleId);
            Assert.Equal(original.Version, clone.Version);
            Assert.Equal(original.Content, clone.Content);
            Assert.Equal(original.Score, clone.Score);
            
            // Verify audience is deep cloned
            Assert.NotSame(original.TargetAudience, clone.TargetAudience);
            Assert.Equal(original.TargetAudience.Gender, clone.TargetAudience.Gender);
            Assert.Equal(original.TargetAudience.Age, clone.TargetAudience.Age);
        }

        [Fact]
        public void DeepClone_ModifyingClone_DoesNotAffectOriginal()
        {
            // Arrange
            var original = new ScriptVersion
            {
                TitleId = "test_001",
                Version = "v1",
                Content = "Original content",
                TargetAudience = new AudienceSegment("men", "18-23")
            };
            var clone = original.DeepClone();

            // Act
            clone.Content = "Modified content";
            clone.Version = "v2";
            clone.TargetAudience.Gender = "women";

            // Assert
            Assert.Equal("Original content", original.Content);
            Assert.Equal("v1", original.Version);
            Assert.Equal("men", original.TargetAudience.Gender);
        }
    }

    /// <summary>
    /// Unit tests for ScriptScoringResult model.
    /// Tests the Prototype pattern (ICloneable) implementation and deep cloning.
    /// </summary>
    public class ScriptScoringResultTests
    {
        [Fact]
        public void DeepClone_CreatesIndependentCopy()
        {
            // Arrange
            var original = new ScriptScoringResult
            {
                TitleId = "test_001",
                Version = "v2",
                OverallScore = 85.5,
                NarrativeCohesion = 82.0,
                Feedback = "Strong pacing",
                TargetAudience = new AudienceSegment("men", "18-23"),
                AreasForImprovement = new List<string> { "Improve hook", "Better dialogue" },
                Strengths = new List<string> { "Good structure", "Clear pacing" },
                RubricScores = new ScriptRubricScores
                {
                    HookQuality = 80,
                    Clarity = 90
                }
            };
            original.Metadata.Add("scorer", "qwen2.5");

            // Act
            var clone = original.DeepClone();

            // Assert
            Assert.NotSame(original, clone);
            Assert.Equal(original.TitleId, clone.TitleId);
            Assert.Equal(original.OverallScore, clone.OverallScore);
            
            // Verify collections are deep cloned
            Assert.NotSame(original.AreasForImprovement, clone.AreasForImprovement);
            Assert.NotSame(original.Strengths, clone.Strengths);
            Assert.NotSame(original.Metadata, clone.Metadata);
            Assert.NotSame(original.RubricScores, clone.RubricScores);
        }
    }
}
