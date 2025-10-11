using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using Microsoft.Extensions.Logging;
using PrismQ.Shared.Models;
using PrismQ.Shared.Interfaces;

namespace PrismQ.Shared.Core.Services
{
    /// <summary>
    /// Content filtering service to detect demonetized words and inappropriate content.
    /// Helps ensure content is advertiser-friendly for platforms like YouTube.
    /// 
    /// Based on YouTube's advertiser-friendly content guidelines and community research:
    /// - Google Spreadsheet: https://docs.google.com/spreadsheets/d/1ozg1Cnm6SdtM4M5rATkANAi07xAzYWaKL7HKxyvoHzk/htmlview#gid=1380702445
    /// - Reddit discussion: https://www.reddit.com/r/youtubers/comments/db5kgt/tips_tricks_list_of_youtube_demonetized_words_for/
    /// </summary>
    public class ContentFilter : IContentFilter
    {
        private readonly ILogger<ContentFilter> _logger;
        private readonly HashSet<string> _demonetizedWords;
        private readonly List<Regex> _demonetizedPatterns;
        private readonly ContentFilterOptions _options;

        public ContentFilter(ILogger<ContentFilter> logger, ContentFilterOptions? options = null)
        {
            _logger = logger;
            _options = options ?? new ContentFilterOptions();
            _demonetizedWords = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            _demonetizedPatterns = new List<Regex>();
            
            InitializeDemonetizedWords();
            InitializeDemonetizedPatterns();
        }

        /// <summary>
        /// Check if content contains demonetized words or patterns.
        /// </summary>
        /// <param name="content">Text content to check (script, title, description)</param>
        /// <returns>Result containing validation status and details</returns>
        public ContentFilterResult CheckContent(string content)
        {
            if (string.IsNullOrWhiteSpace(content))
            {
                return new ContentFilterResult
                {
                    IsClean = true,
                    Message = "Content is empty"
                };
            }

            var flaggedWords = new List<FlaggedWord>();
            var words = content.Split(new[] { ' ', '\n', '\r', '\t', '.', ',', '!', '?', ';', ':' }, 
                StringSplitOptions.RemoveEmptyEntries);

            // Check individual words
            foreach (var word in words)
            {
                var cleanWord = word.Trim().ToLowerInvariant();
                if (_demonetizedWords.Contains(cleanWord))
                {
                    flaggedWords.Add(new FlaggedWord
                    {
                        Word = word,
                        Category = "Demonetized",
                        Severity = GetSeverity(cleanWord)
                    });
                }
            }

            // Check patterns (phrases, context-dependent)
            foreach (var pattern in _demonetizedPatterns)
            {
                var matches = pattern.Matches(content);
                foreach (Match match in matches)
                {
                    flaggedWords.Add(new FlaggedWord
                    {
                        Word = match.Value,
                        Category = "Pattern",
                        Severity = FlagSeverity.Medium
                    });
                }
            }

            var result = new ContentFilterResult
            {
                IsClean = flaggedWords.Count == 0,
                FlaggedWords = flaggedWords,
                Message = flaggedWords.Count == 0 
                    ? "Content passed all checks" 
                    : $"Found {flaggedWords.Count} potentially problematic word(s)"
            };

            if (!result.IsClean)
            {
                _logger.LogWarning("Content filter found {Count} flagged words: {Words}", 
                    flaggedWords.Count, 
                    string.Join(", ", flaggedWords.Take(5).Select(f => f.Word)));
            }

            return result;
        }

        /// <summary>
        /// Get suggested replacements for flagged content.
        /// </summary>
        public string SuggestReplacements(string content, ContentFilterResult filterResult)
        {
            if (filterResult.IsClean)
            {
                return content;
            }

            var modified = content;
            foreach (var flagged in filterResult.FlaggedWords)
            {
                var replacement = GetReplacement(flagged.Word);
                if (!string.IsNullOrEmpty(replacement))
                {
                    modified = Regex.Replace(modified, $@"\b{Regex.Escape(flagged.Word)}\b", 
                        replacement, RegexOptions.IgnoreCase);
                }
            }

            return modified;
        }

        private void InitializeDemonetizedWords()
        {
            // Violence and weapons (from Reddit thread and Google Sheet)
            var violence = new[]
            {
                "kill", "killed", "killing", "murder", "murdered", "suicide", "die", "died", "death", "dead",
                "gun", "guns", "shoot", "shooting", "shot", "weapon", "weapons", "bomb", "bombing", 
                "terrorist", "terrorism", "violence", "violent", "attack", "attacked", "war", "warfare"
            };

            // Profanity and explicit language
            var profanity = new[]
            {
                "damn", "hell", "crap", "shit", "fuck", "bitch", "ass", "bastard", "dick", "pussy",
                "cock", "penis", "vagina", "sexual", "sex", "porn", "pornography", "nude", "naked"
            };

            // Drugs and substances
            var drugs = new[]
            {
                "drug", "drugs", "cocaine", "heroin", "marijuana", "weed", "cannabis", "meth",
                "alcohol", "alcoholic", "drunk", "drinking", "beer", "vodka", "whiskey",
                "cigarette", "smoking", "tobacco", "vape", "vaping"
            };

            // Controversial topics (lighter severity)
            var controversial = new[]
            {
                "abortion", "racist", "racism", "nazi", "hitler", "isis", "rape", "raped",
                "abuse", "abused", "victim", "tragedy", "disaster", "crisis", "pandemic"
            };

            // Health and medical (context-dependent, lower severity)
            var medical = new[]
            {
                "cancer", "disease", "illness", "sick", "pain", "injury", "injured",
                "blood", "bleeding", "emergency", "hospital"
            };

            // Add all categories
            foreach (var word in violence.Concat(profanity).Concat(drugs).Concat(controversial).Concat(medical))
            {
                _demonetizedWords.Add(word);
            }

            _logger.LogInformation("Initialized content filter with {Count} demonetized words", _demonetizedWords.Count);
        }

        private void InitializeDemonetizedPatterns()
        {
            // Multi-word phrases that should be flagged
            var patterns = new[]
            {
                @"\bkill(ed|ing)?\s+(himself|herself|themselves)\b",
                @"\bcommit(ted)?\s+suicide\b",
                @"\bschool\s+shooting\b",
                @"\bmass\s+shooting\b",
                @"\bterrorist\s+attack\b",
                @"\bdrug\s+abuse\b",
                @"\bsexual\s+(assault|harassment|abuse)\b",
                @"\bdomestic\s+(violence|abuse)\b"
            };

            foreach (var pattern in patterns)
            {
                _demonetizedPatterns.Add(new Regex(pattern, RegexOptions.IgnoreCase | RegexOptions.Compiled));
            }
        }

        private FlagSeverity GetSeverity(string word)
        {
            // High severity: explicit content, violence, drugs
            var highSeverity = new[] { "fuck", "shit", "kill", "murder", "suicide", "terrorist", "rape", "nazi" };
            if (highSeverity.Any(w => word.Contains(w)))
            {
                return FlagSeverity.High;
            }

            // Medium severity: profanity, substances
            var mediumSeverity = new[] { "damn", "hell", "drug", "alcohol", "weapon", "violence" };
            if (mediumSeverity.Any(w => word.Contains(w)))
            {
                return FlagSeverity.Medium;
            }

            // Low severity: medical, controversial but contextual
            return FlagSeverity.Low;
        }

        private string GetReplacement(string word)
        {
            var replacements = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
            {
                { "kill", "stop" },
                { "killed", "stopped" },
                { "murder", "harm" },
                { "die", "pass away" },
                { "died", "passed away" },
                { "death", "passing" },
                { "gun", "weapon" },
                { "shoot", "fire" },
                { "damn", "darn" },
                { "hell", "heck" },
                { "crap", "nonsense" },
                { "drug", "substance" },
                { "drunk", "intoxicated" }
            };

            return replacements.TryGetValue(word, out var replacement) ? replacement : string.Empty;
        }
    }

    /// <summary>
    /// Configuration options for content filter.
    /// </summary>
    public class ContentFilterOptions
    {
        /// <summary>
        /// Sensitivity level: Strict, Moderate, or Lenient.
        /// </summary>
        public FilterSensitivity Sensitivity { get; set; } = FilterSensitivity.Moderate;

        /// <summary>
        /// Whether to automatically attempt replacements.
        /// </summary>
        public bool AutoReplace { get; set; } = false;

        /// <summary>
        /// Whether to log all flagged content.
        /// </summary>
        public bool LogAllFlags { get; set; } = true;
    }

    /// <summary>
    /// Filter sensitivity levels.
    /// </summary>
    public enum FilterSensitivity
    {
        Lenient,   // Only flag high-severity words
        Moderate,  // Flag high and medium severity
        Strict     // Flag all potentially problematic content
    }
}
