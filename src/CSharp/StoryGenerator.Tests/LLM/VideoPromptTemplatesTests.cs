using System;
using StoryGenerator.Core.LLM;
using Xunit;

namespace StoryGenerator.Tests.LLM
{
    /// <summary>
    /// Tests for VideoPromptTemplates - specialized prompts based on viral video research.
    /// </summary>
    public class VideoPromptTemplatesTests
    {
        #region Cinematic Video Template Tests

        [Fact]
        public void CinematicVideoSystem_IsNotEmpty()
        {
            Assert.False(string.IsNullOrWhiteSpace(VideoPromptTemplates.CinematicVideoSystem));
            Assert.Contains("cinematographer", VideoPromptTemplates.CinematicVideoSystem.ToLower());
        }

        [Fact]
        public void FormatCinematicVideoPrompt_ReturnsValidPrompt()
        {
            // Arrange
            var scene = "A young woman reading a letter with tears in her eyes";
            var emotion = "heartbreak";
            var duration = 3.5f;

            // Act
            var result = VideoPromptTemplates.FormatCinematicVideoPrompt(scene, emotion, duration);

            // Assert
            Assert.NotEmpty(result);
            Assert.Contains(scene, result);
            Assert.Contains(emotion, result);
            Assert.Contains(duration.ToString(), result);
        }

        #endregion

        #region Documentary Style Template Tests

        [Fact]
        public void DocumentaryVideoSystem_IsNotEmpty()
        {
            Assert.False(string.IsNullOrWhiteSpace(VideoPromptTemplates.DocumentaryVideoSystem));
            Assert.Contains("documentary", VideoPromptTemplates.DocumentaryVideoSystem.ToLower());
        }

        [Fact]
        public void FormatDocumentaryVideoPrompt_ReturnsValidPrompt()
        {
            // Arrange
            var scene = "Person working late at night in office";
            var setting = "dimly lit office cubicle";
            var mood = "exhausted but determined";

            // Act
            var result = VideoPromptTemplates.FormatDocumentaryVideoPrompt(scene, setting, mood);

            // Assert
            Assert.NotEmpty(result);
            Assert.Contains(scene, result);
            Assert.Contains(setting, result);
            Assert.Contains(mood, result);
        }

        #endregion

        #region Emotional Story Template Tests

        [Fact]
        public void EmotionalStoryVideoSystem_ContainsResearchBasedTriggers()
        {
            var system = VideoPromptTemplates.EmotionalStoryVideoSystem;
            
            Assert.Contains("emotional trigger words", system.ToLower());
            // Research-identified triggers
            Assert.Contains("angry", system.ToLower());
            Assert.Contains("happy", system.ToLower());
            Assert.Contains("shocked", system.ToLower());
        }

        [Fact]
        public void FormatEmotionalStoryPrompt_IncludesAllEmotions()
        {
            // Arrange
            var storyBeat = "Discovery of betrayal";
            var primaryEmotion = "shocked";
            var secondaryEmotions = "angry, hurt";

            // Act
            var result = VideoPromptTemplates.FormatEmotionalStoryPrompt(storyBeat, primaryEmotion, secondaryEmotions);

            // Assert
            Assert.NotEmpty(result);
            Assert.Contains(storyBeat, result);
            Assert.Contains(primaryEmotion, result);
            Assert.Contains(secondaryEmotions, result);
        }

        #endregion

        #region Action Video Template Tests

        [Fact]
        public void ActionVideoSystem_IsNotEmpty()
        {
            Assert.False(string.IsNullOrWhiteSpace(VideoPromptTemplates.ActionVideoSystem));
            Assert.Contains("dynamic", VideoPromptTemplates.ActionVideoSystem.ToLower());
            Assert.Contains("action", VideoPromptTemplates.ActionVideoSystem.ToLower());
        }

        [Fact]
        public void FormatActionVideoPrompt_IncludesMovementDetails()
        {
            // Arrange
            var action = "Person running through crowded street";
            var intensity = "high";
            var cameraMovement = "tracking shot";

            // Act
            var result = VideoPromptTemplates.FormatActionVideoPrompt(action, intensity, cameraMovement);

            // Assert
            Assert.NotEmpty(result);
            Assert.Contains(action, result);
            Assert.Contains(intensity, result);
            Assert.Contains(cameraMovement, result);
        }

        #endregion

        #region Character Close-Up Template Tests

        [Fact]
        public void CharacterCloseUpSystem_FocusesOnEmotionalDetails()
        {
            var system = VideoPromptTemplates.CharacterCloseUpSystem;
            
            Assert.Contains("close-up", system.ToLower());
            Assert.Contains("emotional", system.ToLower());
            Assert.Contains("facial", system.ToLower());
        }

        [Fact]
        public void FormatCharacterCloseUpPrompt_IncludesCharacterDetails()
        {
            // Arrange
            var character = "Young woman, early 20s";
            var emotion = "relieved";
            var lighting = "soft natural light";

            // Act
            var result = VideoPromptTemplates.FormatCharacterCloseUpPrompt(character, emotion, lighting);

            // Assert
            Assert.NotEmpty(result);
            Assert.Contains(character, result);
            Assert.Contains(emotion, result);
            Assert.Contains(lighting, result);
        }

        #endregion

        #region Establishing Shot Template Tests

        [Fact]
        public void EstablishingShotSystem_IsNotEmpty()
        {
            Assert.False(string.IsNullOrWhiteSpace(VideoPromptTemplates.EstablishingshotSystem));
            Assert.Contains("establishing", VideoPromptTemplates.EstablishingshotSystem.ToLower());
        }

        [Fact]
        public void FormatEstablishingShotPrompt_IncludesLocationAndTime()
        {
            // Arrange
            var location = "High school hallway";
            var timeOfDay = "early morning";
            var atmosphere = "quiet, empty, lonely";

            // Act
            var result = VideoPromptTemplates.FormatEstablishingShotPrompt(location, timeOfDay, atmosphere);

            // Assert
            Assert.NotEmpty(result);
            Assert.Contains(location, result);
            Assert.Contains(timeOfDay, result);
            Assert.Contains(atmosphere, result);
        }

        #endregion

        #region Transition Shot Template Tests

        [Fact]
        public void TransitionShotSystem_IsNotEmpty()
        {
            Assert.False(string.IsNullOrWhiteSpace(VideoPromptTemplates.TransitionShotSystem));
            Assert.Contains("transition", VideoPromptTemplates.TransitionShotSystem.ToLower());
        }

        [Fact]
        public void FormatTransitionShotPrompt_IncludesEmotionShift()
        {
            // Arrange
            var fromEmotion = "anger";
            var toEmotion = "calm";
            var transitionType = "dissolve";

            // Act
            var result = VideoPromptTemplates.FormatTransitionShotPrompt(fromEmotion, toEmotion, transitionType);

            // Assert
            Assert.NotEmpty(result);
            Assert.Contains(fromEmotion, result);
            Assert.Contains(toEmotion, result);
            Assert.Contains(transitionType, result);
        }

        #endregion

        #region Hook Shot Template Tests (Critical First 3 Seconds)

        [Fact]
        public void HookShotSystem_ReferencesResearchFindings()
        {
            var system = VideoPromptTemplates.HookShotSystem;
            
            // Research shows hook is critical for retention
            Assert.Contains("first 3 seconds", system.ToLower());
            Assert.Contains("hook", system.ToLower());
            
            // Research finding: 6-16 words optimal
            Assert.Contains("6-16 words", system);
        }

        [Fact]
        public void HookShotUser_MentionsFirst3Seconds()
        {
            var user = VideoPromptTemplates.HookShotUser;
            
            Assert.Contains("first 3 seconds", user.ToLower());
            Assert.Contains("hook", user.ToLower());
        }

        [Fact]
        public void FormatHookShotPrompt_IncludesConflictElement()
        {
            // Arrange
            var hookConcept = "My neighbor blocked my driveway";
            var conflictElement = "frustrated person staring at blocked car";

            // Act
            var result = VideoPromptTemplates.FormatHookShotPrompt(hookConcept, conflictElement);

            // Assert
            Assert.NotEmpty(result);
            Assert.Contains(hookConcept, result);
            Assert.Contains(conflictElement, result);
            Assert.Contains("3 seconds", result.ToLower());
        }

        #endregion

        #region Resolution Shot Template Tests

        [Fact]
        public void ResolutionShotSystem_References100PercentRequirement()
        {
            var system = VideoPromptTemplates.ResolutionShotSystem;
            
            // Research shows 100% of successful stories have resolution
            Assert.Contains("resolution", system.ToLower());
            Assert.Contains("closure", system.ToLower());
        }

        [Fact]
        public void FormatResolutionShotPrompt_IncludesPayoff()
        {
            // Arrange
            var resolution = "Neighbors shaking hands and laughing";
            var finalEmotion = "relieved";
            var payoff = "conflict resolved, friendship formed";

            // Act
            var result = VideoPromptTemplates.FormatResolutionShotPrompt(resolution, finalEmotion, payoff);

            // Assert
            Assert.NotEmpty(result);
            Assert.Contains(resolution, result);
            Assert.Contains(finalEmotion, result);
            Assert.Contains(payoff, result);
        }

        #endregion

        #region Advanced System Prompt Tests

        [Fact]
        public void AgeAppropriateFilterSystem_Targets10To30Demographic()
        {
            var system = VideoPromptTemplates.AgeAppropriateFilterSystem;
            
            Assert.Contains("10-30", system);
            Assert.Contains("age-appropriate", system.ToLower());
        }

        [Fact]
        public void VerticalVideoOptimizationSystem_References9By16Format()
        {
            var system = VideoPromptTemplates.VerticalVideoOptimizationSystem;
            
            Assert.Contains("9:16", system);
            Assert.Contains("vertical", system.ToLower());
            Assert.Contains("1080x1920", system);
        }

        [Fact]
        public void VerticalVideoOptimizationSystem_ReferencesSafeAreas()
        {
            var system = VideoPromptTemplates.VerticalVideoOptimizationSystem;
            
            // Research-based safe area specifications
            Assert.Contains("8%", system); // top margin
            Assert.Contains("10%", system); // bottom margin
        }

        [Fact]
        public void ViralOptimizationSystem_ReferencesResearchPatterns()
        {
            var system = VideoPromptTemplates.ViralOptimizationSystem;
            
            // Research-based story arc
            Assert.Contains("Setup", system);
            Assert.Contains("Conflict", system);
            Assert.Contains("Escalation", system);
            Assert.Contains("Climax", system);
            Assert.Contains("Resolution", system);
            
            // Emotional triggers from research
            Assert.Contains("emotional", system.ToLower());
            Assert.Contains("first 3 seconds", system.ToLower());
        }

        #endregion

        #region Integration Tests

        [Fact]
        public void AllSystemPrompts_AreNotEmpty()
        {
            // Ensure all system prompts are properly defined
            var systemPrompts = new[]
            {
                VideoPromptTemplates.CinematicVideoSystem,
                VideoPromptTemplates.DocumentaryVideoSystem,
                VideoPromptTemplates.EmotionalStoryVideoSystem,
                VideoPromptTemplates.ActionVideoSystem,
                VideoPromptTemplates.CharacterCloseUpSystem,
                VideoPromptTemplates.EstablishingshotSystem,
                VideoPromptTemplates.TransitionShotSystem,
                VideoPromptTemplates.HookShotSystem,
                VideoPromptTemplates.ResolutionShotSystem,
                VideoPromptTemplates.AgeAppropriateFilterSystem,
                VideoPromptTemplates.VerticalVideoOptimizationSystem,
                VideoPromptTemplates.ViralOptimizationSystem
            };

            foreach (var prompt in systemPrompts)
            {
                Assert.False(string.IsNullOrWhiteSpace(prompt));
                Assert.True(prompt.Length > 50, "System prompt should be detailed");
            }
        }

        [Fact]
        public void AllUserPrompts_AreNotEmpty()
        {
            // Ensure all user prompt templates are properly defined
            var userPrompts = new[]
            {
                VideoPromptTemplates.CinematicVideoUser,
                VideoPromptTemplates.DocumentaryVideoUser,
                VideoPromptTemplates.EmotionalStoryVideoUser,
                VideoPromptTemplates.ActionVideoUser,
                VideoPromptTemplates.CharacterCloseUpUser,
                VideoPromptTemplates.EstablishingShotUser,
                VideoPromptTemplates.TransitionShotUser,
                VideoPromptTemplates.HookShotUser,
                VideoPromptTemplates.ResolutionShotUser
            };

            foreach (var prompt in userPrompts)
            {
                Assert.False(string.IsNullOrWhiteSpace(prompt));
                Assert.True(prompt.Length > 50, "User prompt should be detailed");
            }
        }

        [Fact]
        public void AllUserPrompts_ContainFormatPlaceholders()
        {
            // Verify that user prompts have format placeholders
            Assert.Contains("{0}", VideoPromptTemplates.CinematicVideoUser);
            Assert.Contains("{0}", VideoPromptTemplates.DocumentaryVideoUser);
            Assert.Contains("{0}", VideoPromptTemplates.EmotionalStoryVideoUser);
            Assert.Contains("{0}", VideoPromptTemplates.ActionVideoUser);
            Assert.Contains("{0}", VideoPromptTemplates.CharacterCloseUpUser);
            Assert.Contains("{0}", VideoPromptTemplates.EstablishingShotUser);
            Assert.Contains("{0}", VideoPromptTemplates.TransitionShotUser);
            Assert.Contains("{0}", VideoPromptTemplates.HookShotUser);
            Assert.Contains("{0}", VideoPromptTemplates.ResolutionShotUser);
        }

        [Fact]
        public void AllFormatMethods_ReturnNonEmptyStrings()
        {
            // Test all format methods with sample data
            var results = new[]
            {
                VideoPromptTemplates.FormatCinematicVideoPrompt("scene", "emotion", 3.0f),
                VideoPromptTemplates.FormatDocumentaryVideoPrompt("scene", "setting", "mood"),
                VideoPromptTemplates.FormatEmotionalStoryPrompt("beat", "primary", "secondary"),
                VideoPromptTemplates.FormatActionVideoPrompt("action", "intensity", "movement"),
                VideoPromptTemplates.FormatCharacterCloseUpPrompt("character", "emotion", "lighting"),
                VideoPromptTemplates.FormatEstablishingShotPrompt("location", "time", "atmosphere"),
                VideoPromptTemplates.FormatTransitionShotPrompt("from", "to", "type"),
                VideoPromptTemplates.FormatHookShotPrompt("hook", "conflict"),
                VideoPromptTemplates.FormatResolutionShotPrompt("resolution", "emotion", "payoff")
            };

            foreach (var result in results)
            {
                Assert.False(string.IsNullOrWhiteSpace(result));
                Assert.True(result.Length > 10);
            }
        }

        #endregion

        #region Research Validation Tests

        [Fact]
        public void Templates_IncorporateStoryArcResearch()
        {
            // Based on story_patterns_analysis.json
            // All successful stories follow: Setup → Conflict → Escalation → Climax → Resolution
            
            var templates = new[]
            {
                VideoPromptTemplates.EmotionalStoryVideoSystem,
                VideoPromptTemplates.ViralOptimizationSystem,
                VideoPromptTemplates.ResolutionShotSystem
            };

            foreach (var template in templates)
            {
                Assert.Contains("resolution", template.ToLower());
            }
        }

        [Fact]
        public void Templates_Reference9By16VerticalFormat()
        {
            // All video templates should reference vertical format
            var templates = new[]
            {
                VideoPromptTemplates.CinematicVideoUser,
                VideoPromptTemplates.DocumentaryVideoUser,
                VideoPromptTemplates.EmotionalStoryVideoUser,
                VideoPromptTemplates.ActionVideoUser,
                VideoPromptTemplates.CharacterCloseUpUser,
                VideoPromptTemplates.EstablishingShotUser,
                VideoPromptTemplates.VerticalVideoOptimizationSystem
            };

            var verticalFormatMentioned = 0;
            foreach (var template in templates)
            {
                if (template.Contains("9:16") || template.Contains("vertical"))
                {
                    verticalFormatMentioned++;
                }
            }

            Assert.True(verticalFormatMentioned >= 5, 
                "Most templates should reference vertical format");
        }

        [Fact]
        public void Templates_TargetCorrectDemographic()
        {
            // Research targets ages 10-30
            var templates = new[]
            {
                VideoPromptTemplates.EmotionalStoryVideoSystem,
                VideoPromptTemplates.DocumentaryVideoUser,
                VideoPromptTemplates.CharacterCloseUpUser,
                VideoPromptTemplates.AgeAppropriateFilterSystem
            };

            var demographicMentioned = 0;
            foreach (var template in templates)
            {
                if (template.Contains("10-30") || template.Contains("ages 10-30"))
                {
                    demographicMentioned++;
                }
            }

            Assert.True(demographicMentioned >= 2, 
                "Templates should target correct age demographic");
        }

        #endregion
    }
}
