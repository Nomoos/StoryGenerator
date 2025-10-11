using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Models;

namespace PrismQ.StoryTitleProcessor
{
    /// <summary>
    /// Concrete implementation of ITitleGenerator for generating clickable titles.
    /// </summary>
    public class TitleGenerator : ITitleGenerator
    {
        private readonly string _name = "TitleGenerator";
        private readonly string _version = "1.0.0";

        /// <summary>
        /// Gets the name of the generator.
        /// </summary>
        public string Name => _name;

        /// <summary>
        /// Gets the version of the generator.
        /// </summary>
        public string Version => _version;

        /// <summary>
        /// Generates clickable titles from topic clusters for a specific audience segment.
        /// </summary>
        public async Task<ClickableTitleCollection> GenerateTitlesFromTopicsAsync(
            TopicClusterCollection topics,
            AudienceSegment segment,
            int minTitles = 10,
            CancellationToken cancellationToken = default)
        {
            if (topics == null || topics.Topics == null || topics.Topics.Count == 0)
                throw new ArgumentException("Topics collection cannot be empty", nameof(topics));

            if (segment == null)
                throw new ArgumentNullException(nameof(segment));

            if (minTitles < 1)
                throw new ArgumentException("Minimum titles must be at least 1", nameof(minTitles));

            var titles = new List<ClickableTitle>();
            var titlesPerTopic = Math.Max(1, minTitles / topics.Topics.Count);

            foreach (var topic in topics.Topics)
            {
                cancellationToken.ThrowIfCancellationRequested();

                var topicTitles = await GenerateTitlesFromTopicAsync(
                    topic,
                    segment,
                    titlesPerTopic,
                    cancellationToken);

                titles.AddRange(topicTitles);
            }

            // If we need more titles, generate additional ones from high-potential topics
            while (titles.Count < minTitles)
            {
                var topTopic = topics.Topics.OrderByDescending(t => t.ViralPotential).First();
                var additionalTitle = await GenerateTitlesFromTopicAsync(topTopic, segment, 1, cancellationToken);
                titles.AddRange(additionalTitle);
            }

            // Take only the required number and order by viral potential
            var finalTitles = titles
                .OrderByDescending(t => t.ViralPotential)
                .Take(minTitles)
                .ToList();

            var collection = new ClickableTitleCollection
            {
                Segment = segment,
                Titles = finalTitles,
                GeneratedAt = DateTime.UtcNow,
                Metadata = new Dictionary<string, object>
                {
                    { "sourceTopics", topics.TopicCount },
                    { "generationMethod", "template-based" },
                    { "version", _version }
                }
            };

            return await Task.FromResult(collection);
        }

        /// <summary>
        /// Generates titles from a single topic cluster.
        /// </summary>
        public async Task<List<ClickableTitle>> GenerateTitlesFromTopicAsync(
            TopicCluster topic,
            AudienceSegment segment,
            int titlesPerTopic = 2,
            CancellationToken cancellationToken = default)
        {
            if (topic == null)
                throw new ArgumentNullException(nameof(topic));

            var titles = new List<ClickableTitle>();
            var templates = GetTitleTemplates(segment);

            for (int i = 0; i < titlesPerTopic; i++)
            {
                cancellationToken.ThrowIfCancellationRequested();

                var template = templates[i % templates.Count];
                var titleText = FormatTitleFromTopic(template, topic, segment);

                var title = new ClickableTitle
                {
                    Title = titleText,
                    TopicClusterId = topic.Id,
                    Segment = segment,
                    GeneratedAt = DateTime.UtcNow,
                    Keywords = topic.Keywords.Take(3).ToList(),
                    EmotionalHook = DetermineEmotionalHook(titleText),
                    TitleFormat = DetermineTitleFormat(titleText),
                    ViralPotential = EstimateTitleViralPotential(titleText, segment),
                    ClickabilityScore = CalculateClickabilityScore(titleText)
                };

                titles.Add(title);
            }

            return await Task.FromResult(titles);
        }

        /// <summary>
        /// Generates titles and saves them to a JSON file.
        /// </summary>
        public async Task<string> GenerateAndSaveTitlesAsync(
            TopicClusterCollection topics,
            AudienceSegment segment,
            string outputDirectory,
            int minTitles = 10,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(outputDirectory))
                throw new ArgumentException("Output directory cannot be empty", nameof(outputDirectory));

            // Generate titles
            var collection = await GenerateTitlesFromTopicsAsync(topics, segment, minTitles, cancellationToken);

            // Build output path
            var outputPath = BuildOutputPath(outputDirectory, segment, "titles", "json");

            // Ensure directory exists
            var directory = Path.GetDirectoryName(outputPath);
            if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            // Serialize to JSON
            var options = new JsonSerializerOptions
            {
                WriteIndented = true,
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            };

            var json = JsonSerializer.Serialize(collection, options);
            await File.WriteAllTextAsync(outputPath, json, cancellationToken);

            return outputPath;
        }

        /// <summary>
        /// Loads topics from a JSON file and generates clickable titles.
        /// </summary>
        public async Task<string> LoadTopicsAndGenerateTitlesAsync(
            string topicsFilePath,
            AudienceSegment segment,
            string outputDirectory,
            int minTitles = 10,
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(topicsFilePath))
                throw new FileNotFoundException($"Topics file not found: {topicsFilePath}");

            // Load topics from JSON
            var json = await File.ReadAllTextAsync(topicsFilePath, cancellationToken);
            var options = new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase
            };

            var topics = JsonSerializer.Deserialize<TopicClusterCollection>(json, options);
            if (topics == null)
                throw new InvalidOperationException("Failed to deserialize topics from JSON");

            // Generate and save titles
            return await GenerateAndSaveTitlesAsync(topics, segment, outputDirectory, minTitles, cancellationToken);
        }

        /// <summary>
        /// Processes all topic files in a directory and generates titles for each segment.
        /// </summary>
        public async Task<Dictionary<AudienceSegment, string>> GenerateTitlesForAllSegmentsAsync(
            string topicsDirectory,
            string outputDirectory,
            int minTitles = 10,
            CancellationToken cancellationToken = default)
        {
            var results = new Dictionary<AudienceSegment, string>();
            var genders = new[] { "women", "men" };
            var ageRanges = new[] { "10-13", "14-17", "18-23", "24-30" };

            foreach (var gender in genders)
            {
                foreach (var age in ageRanges)
                {
                    cancellationToken.ThrowIfCancellationRequested();

                    var segment = new AudienceSegment(gender, age);
                    var segmentPath = Path.Combine(topicsDirectory, gender, age);

                    if (!Directory.Exists(segmentPath))
                        continue;

                    // Find the most recent topics file
                    var topicsFile = Directory.GetFiles(segmentPath, "*_topics.json")
                        .OrderByDescending(f => f)
                        .FirstOrDefault();

                    if (topicsFile == null)
                        continue;

                    var titlesPath = await LoadTopicsAndGenerateTitlesAsync(
                        topicsFile,
                        segment,
                        outputDirectory,
                        minTitles,
                        cancellationToken);

                    results[segment] = titlesPath;
                }
            }

            return results;
        }

        /// <summary>
        /// Optimizes a title for clickability and viral potential.
        /// </summary>
        public async Task<ClickableTitle> OptimizeTitleAsync(
            string title,
            AudienceSegment segment,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(title))
                throw new ArgumentException("Title cannot be empty", nameof(title));

            // Apply optimization rules
            var optimized = title;

            // Ensure first letter is capitalized
            if (optimized.Length > 0 && char.IsLower(optimized[0]))
            {
                optimized = char.ToUpper(optimized[0]) + optimized.Substring(1);
            }

            // Remove excessive punctuation
            optimized = optimized.Replace("!!", "!").Replace("??", "?");

            // Ensure proper length (aim for 40-60 characters)
            if (optimized.Length > 70)
            {
                optimized = optimized.Substring(0, 67) + "...";
            }

            var optimizedTitle = new ClickableTitle
            {
                Title = optimized,
                Segment = segment,
                GeneratedAt = DateTime.UtcNow,
                EmotionalHook = DetermineEmotionalHook(optimized),
                TitleFormat = DetermineTitleFormat(optimized),
                ViralPotential = EstimateTitleViralPotential(optimized, segment),
                ClickabilityScore = CalculateClickabilityScore(optimized)
            };

            return await Task.FromResult(optimizedTitle);
        }

        /// <summary>
        /// Validates that a title meets clickability criteria.
        /// </summary>
        public bool ValidateTitleClickability(string title)
        {
            if (string.IsNullOrWhiteSpace(title))
                return false;

            // Check length (20-70 characters is ideal)
            if (title.Length < 20 || title.Length > 80)
                return false;

            // Check for at least one emotional keyword
            var emotionalKeywords = new[]
            {
                "secret", "truth", "never", "always", "unexpected", "shocking",
                "incredible", "amazing", "powerful", "heartbreaking", "surprising"
            };

            var hasEmotionalWord = emotionalKeywords.Any(k =>
                title.ToLower().Contains(k));

            return hasEmotionalWord;
        }

        /// <summary>
        /// Gets title templates appropriate for the segment.
        /// </summary>
        private List<string> GetTitleTemplates(AudienceSegment segment)
        {
            var templates = new List<string>
            {
                "The Secret About {0} That Changed Everything",
                "What {0} Taught Me About Life",
                "I Never Expected {0} to Lead to This",
                "The Truth About {0} No One Talks About",
                "How {0} Revealed Someone's True Colors",
                "The Moment {0} Changed My Perspective",
                "Why {0} Matters More Than You Think",
                "The Surprising Truth Behind {0}",
                "When {0} Led to an Unexpected Discovery",
                "The Real Story of {0}",
                "{0} That Left Me Speechless",
                "What Happens When {0} Goes Too Far",
                "The Hidden Meaning Behind {0}",
                "How {0} Saved My Most Important Relationship",
                "{0} Taught Me This Powerful Lesson",
                "The Day {0} Changed Everything",
                "Why Everyone Needs to Hear About {0}",
                "The Incredible Truth About {0}",
                "{0} That No One Saw Coming",
                "What {0} Really Means"
            };

            return templates;
        }

        /// <summary>
        /// Formats a title from a topic and template.
        /// </summary>
        private string FormatTitleFromTopic(string template, TopicCluster topic, AudienceSegment segment)
        {
            var topicPhrase = topic.TopicName.ToLower();

            // Simplify topic name for title
            topicPhrase = topicPhrase
                .Replace("&", "and")
                .Replace(" - ", " ")
                .Trim();

            return string.Format(template, topicPhrase);
        }

        /// <summary>
        /// Determines the emotional hook of a title.
        /// </summary>
        private string DetermineEmotionalHook(string title)
        {
            var titleLower = title.ToLower();

            if (titleLower.Contains("secret") || titleLower.Contains("truth"))
                return "curiosity";
            if (titleLower.Contains("unexpected") || titleLower.Contains("surprising"))
                return "surprise";
            if (titleLower.Contains("powerful") || titleLower.Contains("incredible"))
                return "inspiration";
            if (titleLower.Contains("heartbreak") || titleLower.Contains("sad"))
                return "emotion";
            if (titleLower.Contains("never") || titleLower.Contains("shocking"))
                return "shock";

            return "curiosity"; // Default
        }

        /// <summary>
        /// Determines the format/pattern of a title.
        /// </summary>
        private string DetermineTitleFormat(string title)
        {
            var titleLower = title.ToLower();

            if (titleLower.Contains("what") || titleLower.Contains("why") || titleLower.Contains("how"))
                return "question";
            if (titleLower.Contains("secret") || titleLower.Contains("truth"))
                return "revelation";
            if (titleLower.Contains("the day") || titleLower.Contains("the moment"))
                return "story";
            if (titleLower.Contains("taught me") || titleLower.Contains("learned"))
                return "lesson";

            return "statement"; // Default
        }

        /// <summary>
        /// Estimates the viral potential of a title.
        /// </summary>
        private int EstimateTitleViralPotential(string title, AudienceSegment segment)
        {
            int score = 5; // Base score

            // High-value keywords boost score
            var viralKeywords = new[]
            {
                "secret", "truth", "never", "shocking", "incredible",
                "unexpected", "surprising", "powerful", "changed everything"
            };

            foreach (var keyword in viralKeywords)
            {
                if (title.ToLower().Contains(keyword))
                {
                    score += 1;
                }
            }

            // Length matters (40-60 is ideal)
            if (title.Length >= 40 && title.Length <= 60)
            {
                score += 1;
            }

            // Question format can boost engagement
            if (title.Contains("?"))
            {
                score += 1;
            }

            return Math.Min(score, 10);
        }

        /// <summary>
        /// Calculates the clickability score of a title.
        /// </summary>
        private int CalculateClickabilityScore(string title)
        {
            int score = 5; // Base score

            // Emotional words increase clickability
            var emotionalWords = new[] { "secret", "truth", "never", "always", "incredible", "shocking" };
            foreach (var word in emotionalWords)
            {
                if (title.ToLower().Contains(word))
                {
                    score += 1;
                }
            }

            // Proper capitalization
            if (char.IsUpper(title[0]))
            {
                score += 1;
            }

            // Good length (not too short, not too long)
            if (title.Length >= 30 && title.Length <= 70)
            {
                score += 1;
            }

            return Math.Min(score, 10);
        }

        /// <summary>
        /// Builds the output file path.
        /// </summary>
        private string BuildOutputPath(string baseDirectory, AudienceSegment segment, string fileType, string extension)
        {
            var date = DateTime.UtcNow.ToString("yyyyMMdd");
            var fileName = $"{date}_{fileType}.{extension}";
            return Path.Combine(baseDirectory, segment.Gender, segment.Age, fileName);
        }
    }
}
