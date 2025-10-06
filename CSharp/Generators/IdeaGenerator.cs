using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Generators
{
    /// <summary>
    /// Concrete implementation of IIdeaGenerator for generating raw story ideas.
    /// </summary>
    public class IdeaGenerator : IIdeaGenerator
    {
        private readonly string _name = "IdeaGenerator";
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
        /// Generates raw story ideas for a specific audience segment.
        /// </summary>
        public async Task<List<RawIdea>> GenerateIdeasAsync(
            AudienceSegment segment,
            int minIdeas = 20,
            CancellationToken cancellationToken = default)
        {
            if (segment == null)
                throw new ArgumentNullException(nameof(segment));

            if (minIdeas < 1)
                throw new ArgumentException("Minimum ideas must be at least 1", nameof(minIdeas));

            var ideas = new List<RawIdea>();

            // Generate ideas based on segment characteristics
            var ideaPrompts = GenerateIdeaPrompts(segment, minIdeas);

            foreach (var prompt in ideaPrompts)
            {
                cancellationToken.ThrowIfCancellationRequested();

                var idea = new RawIdea
                {
                    Content = prompt,
                    Segment = segment,
                    GeneratedAt = DateTime.UtcNow,
                    Tags = ExtractTags(prompt, segment),
                    ViralPotential = EstimateViralPotential(prompt, segment)
                };

                ideas.Add(idea);
            }

            return await Task.FromResult(ideas);
        }

        /// <summary>
        /// Generates ideas and saves them to a markdown file.
        /// </summary>
        public async Task<string> GenerateAndSaveIdeasAsync(
            AudienceSegment segment,
            string outputDirectory,
            int minIdeas = 20,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(outputDirectory))
                throw new ArgumentException("Output directory cannot be empty", nameof(outputDirectory));

            // Generate ideas
            var ideas = await GenerateIdeasAsync(segment, minIdeas, cancellationToken);

            // Format as markdown
            var markdown = FormatIdeasAsMarkdown(ideas);

            // Build output path: {outputDirectory}/{gender}/{age}/YYYYMMDD_ideas.md
            var outputPath = BuildOutputPath(outputDirectory, segment, "ideas", "md");

            // Ensure directory exists
            var directory = Path.GetDirectoryName(outputPath);
            if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }

            // Write to file
            await File.WriteAllTextAsync(outputPath, markdown, cancellationToken);

            return outputPath;
        }

        /// <summary>
        /// Generates ideas for all predefined audience segments.
        /// </summary>
        public async Task<Dictionary<AudienceSegment, string>> GenerateIdeasForAllSegmentsAsync(
            string outputDirectory,
            int minIdeas = 20,
            CancellationToken cancellationToken = default)
        {
            var segments = GetPredefinedSegments();
            var results = new Dictionary<AudienceSegment, string>();

            foreach (var segment in segments)
            {
                cancellationToken.ThrowIfCancellationRequested();

                var filePath = await GenerateAndSaveIdeasAsync(
                    segment,
                    outputDirectory,
                    minIdeas,
                    cancellationToken);

                results[segment] = filePath;
            }

            return results;
        }

        /// <summary>
        /// Formats ideas as a markdown list.
        /// </summary>
        public string FormatIdeasAsMarkdown(List<RawIdea> ideas)
        {
            if (ideas == null || ideas.Count == 0)
                return string.Empty;

            var sb = new StringBuilder();
            var segment = ideas.First().Segment;

            // Add header
            sb.AppendLine($"# Story Ideas for {segment?.Gender ?? "Unknown"} ({segment?.Age ?? "Unknown"})");
            sb.AppendLine();
            sb.AppendLine($"Generated: {DateTime.UtcNow:yyyy-MM-dd HH:mm:ss UTC}");
            sb.AppendLine($"Total Ideas: {ideas.Count}");
            sb.AppendLine();
            sb.AppendLine("---");
            sb.AppendLine();

            // Add ideas as bullet list
            foreach (var idea in ideas)
            {
                sb.AppendLine($"- {idea.Content}");
            }

            return sb.ToString();
        }

        /// <summary>
        /// Gets the list of predefined audience segments.
        /// </summary>
        public List<AudienceSegment> GetPredefinedSegments()
        {
            var segments = new List<AudienceSegment>();
            var genders = new[] { "women", "men" };
            var ageRanges = new[] { "10-13", "14-17", "18-23", "24-30" };

            foreach (var gender in genders)
            {
                foreach (var age in ageRanges)
                {
                    segments.Add(new AudienceSegment(gender, age));
                }
            }

            return segments;
        }

        /// <summary>
        /// Generates idea prompts tailored to the audience segment.
        /// </summary>
        private List<string> GenerateIdeaPrompts(AudienceSegment segment, int count)
        {
            var ideas = new List<string>();
            var themesBySegment = GetThemesForSegment(segment);

            // Generate ideas based on themes
            var ideaTemplates = GetIdeaTemplates(segment);

            for (int i = 0; i < count; i++)
            {
                var theme = themesBySegment[i % themesBySegment.Count];
                var template = ideaTemplates[i % ideaTemplates.Count];
                var idea = string.Format(template, theme);
                ideas.Add(idea);
            }

            return ideas;
        }

        /// <summary>
        /// Gets themes appropriate for the audience segment.
        /// </summary>
        private List<string> GetThemesForSegment(AudienceSegment segment)
        {
            // Age-based themes
            var themes = new List<string>();

            if (segment.Age == "10-13")
            {
                themes.AddRange(new[]
                {
                    "discovering a hidden talent",
                    "making new friends at school",
                    "overcoming a fear",
                    "learning an important lesson",
                    "going on an adventure",
                    "solving a mystery",
                    "standing up to a bully",
                    "helping someone in need"
                });
            }
            else if (segment.Age == "14-17")
            {
                themes.AddRange(new[]
                {
                    "navigating friendship drama",
                    "first romantic feelings",
                    "finding your passion",
                    "dealing with peer pressure",
                    "family conflicts",
                    "identity and self-discovery",
                    "social media challenges",
                    "academic pressure"
                });
            }
            else if (segment.Age == "18-23")
            {
                themes.AddRange(new[]
                {
                    "college life and independence",
                    "first serious relationship",
                    "career decisions",
                    "losing touch with old friends",
                    "financial struggles",
                    "finding your purpose",
                    "dealing with betrayal",
                    "unexpected life changes"
                });
            }
            else // 24-30
            {
                themes.AddRange(new[]
                {
                    "career advancement or change",
                    "serious relationships and commitment",
                    "work-life balance",
                    "reconnecting with old friends",
                    "financial independence",
                    "personal growth journey",
                    "navigating adult responsibilities",
                    "life-changing decisions"
                });
            }

            // Gender-specific additions
            if (segment.Gender == "women")
            {
                themes.AddRange(new[]
                {
                    "supporting other women",
                    "breaking stereotypes",
                    "confidence and self-empowerment"
                });
            }
            else if (segment.Gender == "men")
            {
                themes.AddRange(new[]
                {
                    "showing vulnerability",
                    "true friendship and loyalty",
                    "taking responsibility"
                });
            }

            return themes;
        }

        /// <summary>
        /// Gets story idea templates appropriate for the segment.
        /// </summary>
        private List<string> GetIdeaTemplates(AudienceSegment segment)
        {
            return new List<string>
            {
                "A story about {0} that changes everything",
                "When {0} leads to an unexpected discovery",
                "The moment {0} tested a close relationship",
                "How {0} revealed someone's true character",
                "A life-changing experience involving {0}",
                "{0} that no one saw coming",
                "The truth about {0} that everyone needs to hear",
                "A powerful lesson learned through {0}",
                "When {0} brought two people together",
                "The surprising outcome of {0}",
                "A heartfelt story about {0}",
                "The day {0} changed my perspective",
                "An inspiring journey of {0}",
                "What {0} taught me about life",
                "A touching moment involving {0}",
                "The unexpected side of {0}",
                "Why {0} matters more than you think",
                "A stranger's {0} that left me speechless",
                "The hidden meaning behind {0}",
                "How {0} saved an important relationship",
                "A difficult choice about {0}",
                "The price of {0}",
                "What happens when {0} goes too far",
                "A second chance at {0}",
                "The real story behind {0}"
            };
        }

        /// <summary>
        /// Extracts relevant tags from the idea content.
        /// </summary>
        private string[] ExtractTags(string content, AudienceSegment segment)
        {
            var tags = new List<string>();

            // Add segment-based tags
            tags.Add(segment.Gender);
            tags.Add(segment.Age);

            // Extract common keywords
            var keywords = new[]
            {
                "friendship", "love", "betrayal", "trust", "family", "career",
                "relationship", "change", "discovery", "lesson", "truth", "secret"
            };

            foreach (var keyword in keywords)
            {
                if (content.ToLower().Contains(keyword))
                {
                    tags.Add(keyword);
                }
            }

            return tags.Take(5).ToArray();
        }

        /// <summary>
        /// Estimates the viral potential of an idea.
        /// </summary>
        private int EstimateViralPotential(string content, AudienceSegment segment)
        {
            int score = 5; // Base score

            // Boost for emotional keywords
            var emotionalKeywords = new[] { "unexpected", "secret", "truth", "heartfelt", "powerful", "surprising" };
            foreach (var keyword in emotionalKeywords)
            {
                if (content.ToLower().Contains(keyword))
                {
                    score += 1;
                }
            }

            // Boost for relationship themes
            if (content.ToLower().Contains("friend") || content.ToLower().Contains("relationship"))
            {
                score += 1;
            }

            // Cap at 10
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
