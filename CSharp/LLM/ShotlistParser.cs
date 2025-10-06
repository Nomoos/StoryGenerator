using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.RegularExpressions;
using StoryGenerator.Core.Interfaces;

namespace StoryGenerator.Core.LLM
{
    /// <summary>
    /// Utilities for parsing LLM output into structured shotlist format.
    /// Handles JSON parsing with error recovery and validation.
    /// </summary>
    public static class ShotlistParser
    {
        private static readonly JsonSerializerOptions JsonOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
            DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
            WriteIndented = true,
            Converters = { new JsonStringEnumConverter(JsonNamingPolicy.CamelCase) }
        };

        /// <summary>
        /// Parses LLM output into a structured shotlist.
        /// Attempts to extract JSON from mixed text/JSON output.
        /// </summary>
        /// <param name="llmOutput">Raw LLM output text.</param>
        /// <returns>Parsed structured shotlist.</returns>
        /// <exception cref="JsonException">Thrown if parsing fails.</exception>
        public static StructuredShotlist ParseShotlist(string llmOutput)
        {
            if (string.IsNullOrWhiteSpace(llmOutput))
            {
                throw new ArgumentException("LLM output is empty", nameof(llmOutput));
            }

            // Try to extract JSON from the output
            string jsonText = ExtractJson(llmOutput);

            try
            {
                var shotlistData = JsonSerializer.Deserialize<ShotlistJsonData>(jsonText, JsonOptions);
                if (shotlistData == null)
                {
                    throw new JsonException("Deserialized shotlist is null");
                }

                return ConvertToStructuredShotlist(shotlistData);
            }
            catch (JsonException ex)
            {
                throw new JsonException($"Failed to parse shotlist JSON: {ex.Message}\nJSON: {jsonText}", ex);
            }
        }

        /// <summary>
        /// Validates a shotlist for correctness and consistency.
        /// </summary>
        /// <param name="shotlist">The shotlist to validate.</param>
        /// <returns>List of validation errors (empty if valid).</returns>
        public static List<string> ValidateShotlist(StructuredShotlist shotlist)
        {
            var errors = new List<string>();

            if (shotlist == null)
            {
                errors.Add("Shotlist is null");
                return errors;
            }

            if (shotlist.Shots == null || shotlist.Shots.Count == 0)
            {
                errors.Add("Shotlist has no shots");
                return errors;
            }

            float totalCalculated = 0;
            for (int i = 0; i < shotlist.Shots.Count; i++)
            {
                var shot = shotlist.Shots[i];

                // Validate shot timing
                if (shot.Duration <= 0)
                {
                    errors.Add($"Shot {shot.ShotNumber}: Duration must be positive");
                }

                if (shot.StartTime < 0)
                {
                    errors.Add($"Shot {shot.ShotNumber}: Start time cannot be negative");
                }

                if (shot.EndTime <= shot.StartTime)
                {
                    errors.Add($"Shot {shot.ShotNumber}: End time must be after start time");
                }

                if (Math.Abs(shot.EndTime - shot.StartTime - shot.Duration) > 0.1f)
                {
                    errors.Add($"Shot {shot.ShotNumber}: Duration doesn't match start/end times");
                }

                // Check for gaps or overlaps
                if (i > 0)
                {
                    var prevShot = shotlist.Shots[i - 1];
                    if (Math.Abs(shot.StartTime - prevShot.EndTime) > 0.1f)
                    {
                        errors.Add($"Shot {shot.ShotNumber}: Gap or overlap with previous shot");
                    }
                }

                totalCalculated += shot.Duration;

                // Validate content
                if (string.IsNullOrWhiteSpace(shot.SceneDescription))
                {
                    errors.Add($"Shot {shot.ShotNumber}: Missing scene description");
                }

                if (string.IsNullOrWhiteSpace(shot.VisualPrompt))
                {
                    errors.Add($"Shot {shot.ShotNumber}: Missing visual prompt");
                }
            }

            // Validate total duration
            if (Math.Abs(totalCalculated - shotlist.TotalDuration) > 0.5f)
            {
                errors.Add($"Total duration mismatch: expected {shotlist.TotalDuration}s, got {totalCalculated}s");
            }

            return errors;
        }

        /// <summary>
        /// Attempts to fix common issues in a shotlist.
        /// </summary>
        /// <param name="shotlist">The shotlist to fix.</param>
        /// <param name="targetDuration">Target total duration in seconds.</param>
        /// <returns>Fixed shotlist.</returns>
        public static StructuredShotlist FixShotlistTiming(StructuredShotlist shotlist, float targetDuration)
        {
            if (shotlist == null || shotlist.Shots == null || shotlist.Shots.Count == 0)
            {
                return shotlist;
            }

            float totalDuration = 0;
            foreach (var shot in shotlist.Shots)
            {
                totalDuration += shot.Duration;
            }

            // If total duration doesn't match, scale all shots proportionally
            if (Math.Abs(totalDuration - targetDuration) > 0.5f)
            {
                float scaleFactor = targetDuration / totalDuration;
                float currentTime = 0;

                foreach (var shot in shotlist.Shots)
                {
                    shot.Duration *= scaleFactor;
                    shot.StartTime = currentTime;
                    shot.EndTime = currentTime + shot.Duration;
                    currentTime = shot.EndTime;
                }

                shotlist.TotalDuration = targetDuration;
            }

            return shotlist;
        }

        /// <summary>
        /// Serializes a structured shotlist to JSON.
        /// </summary>
        /// <param name="shotlist">The shotlist to serialize.</param>
        /// <returns>JSON string.</returns>
        public static string SerializeToJson(StructuredShotlist shotlist)
        {
            var data = ConvertToJsonData(shotlist);
            return JsonSerializer.Serialize(data, JsonOptions);
        }

        private static string ExtractJson(string text)
        {
            // Try to find JSON object in the text
            var jsonMatch = Regex.Match(text, @"\{[\s\S]*\}", RegexOptions.Multiline);
            if (jsonMatch.Success)
            {
                return jsonMatch.Value;
            }

            // If no JSON found, assume the entire text is JSON
            return text.Trim();
        }

        private static StructuredShotlist ConvertToStructuredShotlist(ShotlistJsonData data)
        {
            var shotlist = new StructuredShotlist
            {
                StoryTitle = data.StoryTitle ?? string.Empty,
                TotalDuration = data.TotalDuration,
                OverallMood = data.OverallMood ?? string.Empty,
                Style = data.Style ?? string.Empty,
                TargetAudience = data.TargetAudience ?? string.Empty,
                Shots = new List<StructuredShot>()
            };

            if (data.Shots != null)
            {
                foreach (var shotData in data.Shots)
                {
                    shotlist.Shots.Add(ConvertToStructuredShot(shotData));
                }
            }

            return shotlist;
        }

        private static StructuredShot ConvertToStructuredShot(ShotJsonData data)
        {
            return new StructuredShot
            {
                ShotNumber = data.ShotNumber,
                StartTime = data.StartTime,
                EndTime = data.EndTime,
                Duration = data.Duration,
                SceneDescription = data.SceneDescription ?? string.Empty,
                VisualPrompt = data.VisualPrompt ?? string.Empty,
                PrimaryEmotion = data.PrimaryEmotion ?? string.Empty,
                SecondaryEmotions = data.SecondaryEmotions ?? new List<string>(),
                Mood = data.Mood ?? string.Empty,
                CameraDirection = ConvertToCameraDirection(data.CameraDirection),
                MovementType = data.MovementType ?? string.Empty,
                Transition = data.Transition ?? string.Empty,
                AudioDescription = data.AudioDescription ?? string.Empty,
                CharacterFocus = data.CharacterFocus ?? new List<string>(),
                KeyElements = data.KeyElements ?? new List<string>(),
                Lighting = data.Lighting ?? string.Empty,
                ColorPalette = data.ColorPalette ?? string.Empty,
                Importance = data.Importance
            };
        }

        private static CameraDirection ConvertToCameraDirection(CameraDirectionJsonData? data)
        {
            if (data == null)
            {
                return new CameraDirection();
            }

            return new CameraDirection
            {
                ShotType = data.ShotType ?? string.Empty,
                Angle = data.Angle ?? string.Empty,
                Movement = data.Movement ?? string.Empty,
                FocusPoint = data.FocusPoint ?? string.Empty,
                DepthOfField = data.DepthOfField ?? string.Empty,
                Composition = data.Composition ?? string.Empty,
                Notes = data.Notes ?? string.Empty
            };
        }

        private static ShotlistJsonData ConvertToJsonData(StructuredShotlist shotlist)
        {
            var data = new ShotlistJsonData
            {
                StoryTitle = shotlist.StoryTitle,
                TotalDuration = shotlist.TotalDuration,
                OverallMood = shotlist.OverallMood,
                Style = shotlist.Style,
                TargetAudience = shotlist.TargetAudience,
                Shots = new List<ShotJsonData>()
            };

            foreach (var shot in shotlist.Shots)
            {
                data.Shots.Add(ConvertToShotJsonData(shot));
            }

            return data;
        }

        private static ShotJsonData ConvertToShotJsonData(StructuredShot shot)
        {
            return new ShotJsonData
            {
                ShotNumber = shot.ShotNumber,
                StartTime = shot.StartTime,
                EndTime = shot.EndTime,
                Duration = shot.Duration,
                SceneDescription = shot.SceneDescription,
                VisualPrompt = shot.VisualPrompt,
                PrimaryEmotion = shot.PrimaryEmotion,
                SecondaryEmotions = shot.SecondaryEmotions,
                Mood = shot.Mood,
                CameraDirection = new CameraDirectionJsonData
                {
                    ShotType = shot.CameraDirection.ShotType,
                    Angle = shot.CameraDirection.Angle,
                    Movement = shot.CameraDirection.Movement,
                    FocusPoint = shot.CameraDirection.FocusPoint,
                    DepthOfField = shot.CameraDirection.DepthOfField,
                    Composition = shot.CameraDirection.Composition,
                    Notes = shot.CameraDirection.Notes
                },
                MovementType = shot.MovementType,
                Transition = shot.Transition,
                AudioDescription = shot.AudioDescription,
                CharacterFocus = shot.CharacterFocus,
                KeyElements = shot.KeyElements,
                Lighting = shot.Lighting,
                ColorPalette = shot.ColorPalette,
                Importance = shot.Importance
            };
        }

        // Internal JSON data classes for serialization
        private class ShotlistJsonData
        {
            [JsonPropertyName("story_title")]
            public string? StoryTitle { get; set; }

            [JsonPropertyName("total_duration")]
            public float TotalDuration { get; set; }

            [JsonPropertyName("overall_mood")]
            public string? OverallMood { get; set; }

            [JsonPropertyName("style")]
            public string? Style { get; set; }

            [JsonPropertyName("target_audience")]
            public string? TargetAudience { get; set; }

            [JsonPropertyName("shots")]
            public List<ShotJsonData>? Shots { get; set; }
        }

        private class ShotJsonData
        {
            [JsonPropertyName("shot_number")]
            public int ShotNumber { get; set; }

            [JsonPropertyName("start_time")]
            public float StartTime { get; set; }

            [JsonPropertyName("end_time")]
            public float EndTime { get; set; }

            [JsonPropertyName("duration")]
            public float Duration { get; set; }

            [JsonPropertyName("scene_description")]
            public string? SceneDescription { get; set; }

            [JsonPropertyName("visual_prompt")]
            public string? VisualPrompt { get; set; }

            [JsonPropertyName("primary_emotion")]
            public string? PrimaryEmotion { get; set; }

            [JsonPropertyName("secondary_emotions")]
            public List<string>? SecondaryEmotions { get; set; }

            [JsonPropertyName("mood")]
            public string? Mood { get; set; }

            [JsonPropertyName("camera_direction")]
            public CameraDirectionJsonData? CameraDirection { get; set; }

            [JsonPropertyName("movement_type")]
            public string? MovementType { get; set; }

            [JsonPropertyName("transition")]
            public string? Transition { get; set; }

            [JsonPropertyName("audio_description")]
            public string? AudioDescription { get; set; }

            [JsonPropertyName("character_focus")]
            public List<string>? CharacterFocus { get; set; }

            [JsonPropertyName("key_elements")]
            public List<string>? KeyElements { get; set; }

            [JsonPropertyName("lighting")]
            public string? Lighting { get; set; }

            [JsonPropertyName("color_palette")]
            public string? ColorPalette { get; set; }

            [JsonPropertyName("importance")]
            public int Importance { get; set; } = 5;
        }

        private class CameraDirectionJsonData
        {
            [JsonPropertyName("shot_type")]
            public string? ShotType { get; set; }

            [JsonPropertyName("angle")]
            public string? Angle { get; set; }

            [JsonPropertyName("movement")]
            public string? Movement { get; set; }

            [JsonPropertyName("focus_point")]
            public string? FocusPoint { get; set; }

            [JsonPropertyName("depth_of_field")]
            public string? DepthOfField { get; set; }

            [JsonPropertyName("composition")]
            public string? Composition { get; set; }

            [JsonPropertyName("notes")]
            public string? Notes { get; set; }
        }
    }
}
