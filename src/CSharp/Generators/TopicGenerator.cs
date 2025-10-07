using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Generators
{
    /// <summary>
    /// Concrete implementation of ITopicGenerator for clustering ideas into topics.
    /// </summary>
    public class TopicGenerator : ITopicGenerator
    {
        private readonly string _name = "TopicGenerator";
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
        /// Clusters raw ideas into topic groups for a specific audience segment.
        /// </summary>
        public async Task<TopicClusterCollection> ClusterIdeasIntoTopicsAsync(
            List<RawIdea> ideas,
            AudienceSegment segment,
            int minTopics = 8,
            CancellationToken cancellationToken = default)
        {
            if (ideas == null || ideas.Count == 0)
                throw new ArgumentException("Ideas list cannot be empty", nameof(ideas));

            if (segment == null)
                throw new ArgumentNullException(nameof(segment));

            if (minTopics < 1)
                throw new ArgumentException("Minimum topics must be at least 1", nameof(minTopics));

            // Extract keywords from all ideas
            var allKeywords = ideas
                .SelectMany(i => ExtractKeywords(i.Content))
                .GroupBy(k => k)
                .OrderByDescending(g => g.Count())
                .Take(20)
                .Select(g => g.Key)
                .ToList();

            // Create topic clusters based on keyword similarity
            var topics = new List<TopicCluster>();
            var usedIdeas = new HashSet<string>();

            // Generate topics
            var topicNames = GenerateTopicNames(segment, minTopics);

            for (int i = 0; i < minTopics && i < topicNames.Count; i++)
            {
                cancellationToken.ThrowIfCancellationRequested();

                var topic = new TopicCluster
                {
                    TopicName = topicNames[i],
                    Segment = segment,
                    Keywords = new List<string>(),
                    IdeaIds = new List<string>(),
                    CreatedAt = DateTime.UtcNow
                };

                // Assign ideas to this topic based on keyword matching
                var topicKeywords = GetTopicKeywords(topicNames[i]);
                topic.Keywords.AddRange(topicKeywords.Take(5));

                foreach (var idea in ideas.Where(i => !usedIdeas.Contains(i.Id)))
                {
                    if (IsIdeaRelevantToTopic(idea, topicKeywords))
                    {
                        topic.IdeaIds.Add(idea.Id);
                        usedIdeas.Add(idea.Id);
                    }

                    // Limit ideas per topic
                    if (topic.IdeaIds.Count >= 5)
                        break;
                }

                // Add description
                topic.Description = GenerateTopicDescription(topic.TopicName, segment);

                // Estimate viral potential
                topic.ViralPotential = EstimateTopicViralPotential(topic);

                topics.Add(topic);
            }

            // Assign remaining ideas to topics with fewest ideas
            foreach (var idea in ideas.Where(i => !usedIdeas.Contains(i.Id)))
            {
                var targetTopic = topics.OrderBy(t => t.IdeaCount).First();
                targetTopic.IdeaIds.Add(idea.Id);
            }

            var collection = new TopicClusterCollection
            {
                Segment = segment,
                Topics = topics,
                GeneratedAt = DateTime.UtcNow,
                Metadata = new Dictionary<string, object>
                {
                    { "totalIdeas", ideas.Count },
                    { "clusteringMethod", "keyword-based" },
                    { "version", _version }
                }
            };

            return await Task.FromResult(collection);
        }

        /// <summary>
        /// Clusters ideas and saves the topics to a JSON file.
        /// </summary>
        public async Task<string> ClusterAndSaveTopicsAsync(
            List<RawIdea> ideas,
            AudienceSegment segment,
            string outputDirectory,
            int minTopics = 8,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(outputDirectory))
                throw new ArgumentException("Output directory cannot be empty", nameof(outputDirectory));

            // Cluster ideas
            var collection = await ClusterIdeasIntoTopicsAsync(ideas, segment, minTopics, cancellationToken);

            // Build output path
            var outputPath = BuildOutputPath(outputDirectory, segment, "topics", "json");

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
        /// Loads raw ideas from a markdown file and clusters them into topics.
        /// </summary>
        public async Task<string> LoadIdeasAndGenerateTopicsAsync(
            string ideasFilePath,
            AudienceSegment segment,
            string outputDirectory,
            int minTopics = 8,
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(ideasFilePath))
                throw new FileNotFoundException($"Ideas file not found: {ideasFilePath}");

            // Parse ideas from markdown
            var ideas = await ParseIdeasFromMarkdownAsync(ideasFilePath, segment, cancellationToken);

            // Cluster and save
            return await ClusterAndSaveTopicsAsync(ideas, segment, outputDirectory, minTopics, cancellationToken);
        }

        /// <summary>
        /// Processes all idea files in a directory and generates topics for each segment.
        /// </summary>
        public async Task<Dictionary<AudienceSegment, string>> GenerateTopicsForAllSegmentsAsync(
            string ideasDirectory,
            string outputDirectory,
            int minTopics = 8,
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
                    var segmentPath = Path.Combine(ideasDirectory, gender, age);

                    if (!Directory.Exists(segmentPath))
                        continue;

                    // Find the most recent ideas file
                    var ideasFile = Directory.GetFiles(segmentPath, "*_ideas.md")
                        .OrderByDescending(f => f)
                        .FirstOrDefault();

                    if (ideasFile == null)
                        continue;

                    var topicsPath = await LoadIdeasAndGenerateTopicsAsync(
                        ideasFile,
                        segment,
                        outputDirectory,
                        minTopics,
                        cancellationToken);

                    results[segment] = topicsPath;
                }
            }

            return results;
        }

        /// <summary>
        /// Parses raw ideas from a markdown file.
        /// </summary>
        public async Task<List<RawIdea>> ParseIdeasFromMarkdownAsync(
            string markdownFilePath,
            AudienceSegment segment,
            CancellationToken cancellationToken = default)
        {
            if (!File.Exists(markdownFilePath))
                throw new FileNotFoundException($"Markdown file not found: {markdownFilePath}");

            var ideas = new List<RawIdea>();
            var content = await File.ReadAllTextAsync(markdownFilePath, cancellationToken);
            var lines = content.Split('\n');

            foreach (var line in lines)
            {
                // Match markdown list items (lines starting with - or * followed by space)
                var match = Regex.Match(line.Trim(), @"^[-*]\s+(.+)$");
                if (match.Success)
                {
                    var ideaContent = match.Groups[1].Value.Trim();
                    if (!string.IsNullOrWhiteSpace(ideaContent))
                    {
                        var idea = new RawIdea
                        {
                            Content = ideaContent,
                            Segment = segment,
                            GeneratedAt = DateTime.UtcNow,
                            Tags = ExtractKeywords(ideaContent).ToArray()
                        };
                        ideas.Add(idea);
                    }
                }
            }

            return ideas;
        }

        /// <summary>
        /// Generates topic names appropriate for the segment.
        /// </summary>
        private List<string> GenerateTopicNames(AudienceSegment segment, int count)
        {
            var baseTopics = new List<string>();

            // Age-appropriate topics
            if (segment.Age == "10-13")
            {
                baseTopics.AddRange(new[]
                {
                    "Friendship & School Life",
                    "Family Bonds",
                    "Personal Growth & Discovery",
                    "Adventures & Mysteries",
                    "Overcoming Challenges",
                    "Learning & Education",
                    "Hobbies & Talents",
                    "Helping Others"
                });
            }
            else if (segment.Age == "14-17")
            {
                baseTopics.AddRange(new[]
                {
                    "Friendship Drama & Loyalty",
                    "First Love & Romance",
                    "Identity & Self-Discovery",
                    "Family Relationships",
                    "Social Challenges",
                    "Future & Dreams",
                    "Peer Pressure & Choices",
                    "Personal Transformation"
                });
            }
            else if (segment.Age == "18-23")
            {
                baseTopics.AddRange(new[]
                {
                    "College & Independence",
                    "Relationships & Love",
                    "Career & Life Decisions",
                    "Friendship Changes",
                    "Personal Finance",
                    "Finding Purpose",
                    "Betrayal & Trust",
                    "Life Transitions"
                });
            }
            else // 24-30
            {
                baseTopics.AddRange(new[]
                {
                    "Career Growth & Change",
                    "Serious Relationships",
                    "Work-Life Balance",
                    "Reconnecting & Nostalgia",
                    "Financial Independence",
                    "Personal Development",
                    "Adult Responsibilities",
                    "Life-Changing Decisions"
                });
            }

            return baseTopics.Take(count).ToList();
        }

        /// <summary>
        /// Gets keywords associated with a topic name.
        /// </summary>
        private List<string> GetTopicKeywords(string topicName)
        {
            var keywords = new List<string>();

            // Extract words from topic name
            var words = topicName.ToLower()
                .Split(new[] { ' ', '&', ',', '-' }, StringSplitOptions.RemoveEmptyEntries);
            keywords.AddRange(words);

            // Add common related keywords
            if (topicName.Contains("Friend"))
                keywords.AddRange(new[] { "friend", "friendship", "bond", "together" });
            if (topicName.Contains("Love") || topicName.Contains("Romance") || topicName.Contains("Relationship"))
                keywords.AddRange(new[] { "love", "relationship", "romance", "dating", "partner" });
            if (topicName.Contains("Career") || topicName.Contains("Work"))
                keywords.AddRange(new[] { "career", "work", "job", "professional" });
            if (topicName.Contains("Family"))
                keywords.AddRange(new[] { "family", "parent", "sibling", "home" });
            if (topicName.Contains("Growth") || topicName.Contains("Discovery"))
                keywords.AddRange(new[] { "growth", "discovery", "learn", "change" });

            return keywords.Distinct().ToList();
        }

        /// <summary>
        /// Generates a description for a topic.
        /// </summary>
        private string GenerateTopicDescription(string topicName, AudienceSegment segment)
        {
            return $"Stories about {topicName.ToLower()} that resonate with {segment.Gender} aged {segment.Age}";
        }

        /// <summary>
        /// Extracts keywords from content.
        /// </summary>
        private List<string> ExtractKeywords(string content)
        {
            var keywords = new List<string>();
            var words = Regex.Split(content.ToLower(), @"\W+");

            // Common story keywords
            var relevantKeywords = new[]
            {
                "friend", "love", "relationship", "family", "trust", "betrayal",
                "discover", "change", "lesson", "truth", "secret", "unexpected",
                "life", "moment", "story", "experience", "journey", "decision"
            };

            foreach (var word in words)
            {
                if (relevantKeywords.Contains(word))
                {
                    keywords.Add(word);
                }
            }

            return keywords.Distinct().ToList();
        }

        /// <summary>
        /// Checks if an idea is relevant to a topic.
        /// </summary>
        private bool IsIdeaRelevantToTopic(RawIdea idea, List<string> topicKeywords)
        {
            var ideaContent = idea.Content.ToLower();
            return topicKeywords.Any(keyword => ideaContent.Contains(keyword));
        }

        /// <summary>
        /// Estimates the viral potential of a topic cluster.
        /// </summary>
        private int EstimateTopicViralPotential(TopicCluster topic)
        {
            int score = 6; // Base score

            // More ideas = higher potential
            if (topic.IdeaCount > 3)
                score += 1;

            // Certain keywords boost score
            var highValueKeywords = new[] { "love", "secret", "betrayal", "truth", "unexpected" };
            foreach (var keyword in highValueKeywords)
            {
                if (topic.Keywords.Any(k => k.Contains(keyword)))
                {
                    score += 1;
                    break;
                }
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
