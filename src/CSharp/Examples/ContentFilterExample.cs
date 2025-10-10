using Microsoft.Extensions.Logging;
using StoryGenerator.Core.Services;

namespace StoryGenerator.Examples
{
    /// <summary>
    /// Example demonstrating the ContentFilter service.
    /// Shows how to detect and handle demonetized content.
    /// </summary>
    public class ContentFilterExample
    {
        public static void RunExample()
        {
            // Create logger
            var loggerFactory = LoggerFactory.Create(builder => builder.AddConsole());
            var logger = loggerFactory.CreateLogger<ContentFilter>();

            // Create content filter
            var contentFilter = new ContentFilter(logger);

            Console.WriteLine("=== Content Filter Example ===\n");

            // Example 1: Clean content
            Console.WriteLine("Example 1: Clean Content");
            var cleanContent = "This is a wonderful story about friendship and adventure.";
            var result1 = contentFilter.CheckContent(cleanContent);
            Console.WriteLine($"Content: {cleanContent}");
            Console.WriteLine($"Is Clean: {result1.IsClean}");
            Console.WriteLine($"Message: {result1.Message}\n");

            // Example 2: Content with demonetized words
            Console.WriteLine("Example 2: Content with Demonetized Words");
            var problematicContent = "The character was killed in a violent attack.";
            var result2 = contentFilter.CheckContent(problematicContent);
            Console.WriteLine($"Content: {problematicContent}");
            Console.WriteLine($"Is Clean: {result2.IsClean}");
            Console.WriteLine($"Flagged Words: {result2.FlaggedWords.Count}");
            foreach (var flag in result2.FlaggedWords)
            {
                Console.WriteLine($"  - {flag.Word} (Severity: {flag.Severity}, Category: {flag.Category})");
            }
            Console.WriteLine();

            // Example 3: Suggest replacements
            Console.WriteLine("Example 3: Suggested Replacements");
            var modified = contentFilter.SuggestReplacements(problematicContent, result2);
            Console.WriteLine($"Original: {problematicContent}");
            Console.WriteLine($"Modified: {modified}\n");

            // Example 4: Multiple issues
            Console.WriteLine("Example 4: Multiple Issues");
            var multipleIssues = "The terrorist attack killed many people with guns and caused death.";
            var result4 = contentFilter.CheckContent(multipleIssues);
            Console.WriteLine($"Content: {multipleIssues}");
            Console.WriteLine($"Flagged Words: {result4.FlaggedWords.Count}");
            foreach (var flag in result4.FlaggedWords)
            {
                Console.WriteLine($"  - {flag.Word} (Severity: {flag.Severity})");
            }
            var modifiedMultiple = contentFilter.SuggestReplacements(multipleIssues, result4);
            Console.WriteLine($"Suggested: {modifiedMultiple}\n");

            // Example 5: Pattern detection
            Console.WriteLine("Example 5: Pattern Detection");
            var patternContent = "The story discusses how someone committed suicide.";
            var result5 = contentFilter.CheckContent(patternContent);
            Console.WriteLine($"Content: {patternContent}");
            Console.WriteLine($"Flagged Items: {result5.FlaggedWords.Count}");
            foreach (var flag in result5.FlaggedWords)
            {
                Console.WriteLine($"  - {flag.Word} (Category: {flag.Category})");
            }
            Console.WriteLine();

            // Example 6: Severity levels
            Console.WriteLine("Example 6: Different Severity Levels");
            var examples = new[]
            {
                ("High Severity", "fuck"),
                ("Medium Severity", "damn"),
                ("Low Severity", "cancer")
            };

            foreach (var (label, word) in examples)
            {
                var testContent = $"This story mentions {word}.";
                var testResult = contentFilter.CheckContent(testContent);
                if (testResult.FlaggedWords.Any())
                {
                    var severity = testResult.FlaggedWords[0].Severity;
                    Console.WriteLine($"{label}: '{word}' -> {severity}");
                }
            }
            Console.WriteLine();

            // Example 7: Integration with script validation
            Console.WriteLine("Example 7: Script Validation Workflow");
            var script = @"
                Once upon a time, there was a brave hero who fought against evil.
                The hero faced many challenges but never gave up.
                In the end, friendship and courage won the day.
            ";
            var scriptResult = contentFilter.CheckContent(script);
            if (scriptResult.IsClean)
            {
                Console.WriteLine("✅ Script passed content filter - safe to proceed");
            }
            else
            {
                Console.WriteLine($"⚠️ Script has {scriptResult.FlaggedWords.Count} issue(s):");
                foreach (var flag in scriptResult.FlaggedWords.Take(5))
                {
                    Console.WriteLine($"  - {flag.Word} ({flag.Severity})");
                }
                Console.WriteLine("Consider regenerating or modifying the script.");
            }

            Console.WriteLine("\n=== Example Complete ===");
        }

        /// <summary>
        /// Example showing how to integrate with script generation pipeline.
        /// </summary>
        public static async Task<string> GenerateFilteredScriptExample()
        {
            var loggerFactory = LoggerFactory.Create(builder => builder.AddConsole());
            var logger = loggerFactory.CreateLogger<ContentFilter>();
            var contentFilter = new ContentFilter(logger);

            // Simulate script generation
            var generatedScript = "The character was killed during the violent attack.";
            
            Console.WriteLine($"Generated Script: {generatedScript}");

            // Check for demonetized content
            var filterResult = contentFilter.CheckContent(generatedScript);

            if (!filterResult.IsClean)
            {
                Console.WriteLine($"⚠️ Script contains {filterResult.FlaggedWords.Count} flagged word(s)");
                
                // Option 1: Suggest replacements
                var modifiedScript = contentFilter.SuggestReplacements(generatedScript, filterResult);
                Console.WriteLine($"Modified Script: {modifiedScript}");
                
                // Option 2: Regenerate with additional constraints
                // (In real implementation, would call script generator with stricter guidelines)
                Console.WriteLine("Alternatively: Regenerate script with content guidelines");

                return modifiedScript;
            }

            Console.WriteLine("✅ Script is clean - proceeding with pipeline");
            return generatedScript;
        }
    }
}
