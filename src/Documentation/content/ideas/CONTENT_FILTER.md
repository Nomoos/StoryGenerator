# Content Filtering and Demonetization Prevention

This document describes the content filtering system implemented to help ensure generated content is advertiser-friendly and compliant with platform guidelines (YouTube, TikTok, Instagram, etc.).

## Overview

The `ContentFilter` service scans text content (scripts, titles, descriptions) for words and phrases that may trigger demonetization or content restrictions on social media platforms. It is based on:

1. **YouTube Advertiser-Friendly Guidelines**: Community-sourced list from [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1ozg1Cnm6SdtM4M5rATkANAi07xAzYWaKL7HKxyvoHzk/htmlview#gid=1380702445)
2. **Reddit Community Discussion**: [r/youtubers thread on demonetized words](https://www.reddit.com/r/youtubers/comments/db5kgt/tips_tricks_list_of_youtube_demonetized_words_for/)
3. **Platform Content Policies**: YouTube, TikTok, Instagram content guidelines

## Features

### 1. Word-Level Detection
Scans for individual problematic words across categories:
- **Violence & Weapons**: kill, murder, gun, terrorist, etc.
- **Profanity**: Explicit language and vulgar terms
- **Drugs & Substances**: References to illegal substances, alcohol
- **Controversial Topics**: Sensitive political/social issues
- **Medical Terms**: Context-dependent medical terminology

### 2. Pattern Detection
Identifies multi-word phrases that may be problematic:
- "commit suicide"
- "school shooting"
- "terrorist attack"
- "sexual assault"
- And more...

### 3. Severity Levels
Flagged content is categorized by severity:
- **High**: Explicit content, extreme violence, illegal activities
- **Medium**: Profanity, substances, general violence
- **Low**: Medical terms, contextual words (may be acceptable in proper context)

### 4. Smart Replacements
Suggests safer alternatives for flagged words:
- "kill" → "stop"
- "murder" → "harm"
- "die" → "pass away"
- "gun" → "weapon"
- etc.

## Usage

### Basic Content Check

```csharp
using StoryGenerator.Core.Services;

// Create the filter
var contentFilter = new ContentFilter(logger);

// Check content
var content = "This is a story about...";
var result = contentFilter.CheckContent(content);

if (!result.IsClean)
{
    Console.WriteLine($"Found {result.FlaggedWords.Count} issues:");
    foreach (var flag in result.FlaggedWords)
    {
        Console.WriteLine($"  - {flag.Word} ({flag.Severity})");
    }
}
```

### With Automatic Replacements

```csharp
var content = "The character was killed in action.";
var result = contentFilter.CheckContent(content);

if (!result.IsClean)
{
    var cleaned = contentFilter.SuggestReplacements(content, result);
    Console.WriteLine($"Modified: {cleaned}");
    // Output: "The character was stopped in action."
}
```

### Integrated with Script Generation

The content filter is automatically integrated into the pipeline:

1. **Script Generation**: Filter checks generated scripts
2. **Quality Control**: Additional validation before export
3. **Manual Review**: Flagged content can be manually reviewed

```csharp
// In script generation
var script = await scriptGenerator.GenerateScriptAsync(idea);
var filterResult = contentFilter.CheckContent(script);

if (!filterResult.IsClean)
{
    // Log warning and optionally regenerate or modify
    logger.LogWarning("Script contains demonetized content");
}
```

### Configuration Options

```csharp
var options = new ContentFilterOptions
{
    Sensitivity = FilterSensitivity.Moderate, // Lenient, Moderate, or Strict
    AutoReplace = false,                       // Automatically apply replacements
    LogAllFlags = true                         // Log every flagged word
};

var contentFilter = new ContentFilter(logger, options);
```

## Integration Points

### 1. Script Development (Group 3)
Primary integration point during script generation and improvement:

```csharp
public async Task<string> GenerateScriptAsync(StoryIdea idea)
{
    var script = await GenerateRawScript(idea);
    
    // Check for demonetized content
    var filterResult = _contentFilter.CheckContent(script);
    
    if (!filterResult.IsClean && filterResult.HasHighSeverityFlags())
    {
        // Regenerate with additional constraints
        script = await RegenerateWithContentGuidelines(idea);
    }
    
    return script;
}
```

### 2. Quality Control (Group 10)
Final check before video export:

```csharp
public async Task<QualityControlReport> ValidateVideo(VideoAsset video)
{
    var report = new QualityControlReport();
    
    // Check script content
    var scriptResult = _contentFilter.CheckContent(video.Script);
    report.ContentIssues = scriptResult.FlaggedWords;
    
    // Check title and description
    var titleResult = _contentFilter.CheckContent(video.Title);
    report.TitleIssues = titleResult.FlaggedWords;
    
    return report;
}
```

### 3. OutputValidator Integration

```csharp
// Validate script file with content filtering
var (isValid, metrics) = outputValidator.ValidateTextFile(
    scriptPath, 
    minLength: 100,
    checkDemonetization: true  // Enable content filtering
);

if (metrics.ContentFilterResult != null && !metrics.ContentFilterResult.IsClean)
{
    // Handle flagged content
}
```

## Best Practices

### 1. Use During Development
- Run filter on all generated scripts
- Review flagged high-severity content
- Consider regenerating or modifying problematic content

### 2. Balance Creativity and Safety
- Don't over-filter - some flagged words may be acceptable in context
- Use severity levels to prioritize issues
- Manual review for edge cases

### 3. Platform-Specific Considerations
- YouTube: Strict on violence, drugs, profanity
- TikTok: Additional restrictions on political content
- Instagram: Focus on visual and textual harassment

### 4. Testing
- Test with known problematic content
- Verify false positives are minimal
- Update word list as platform policies evolve

## Extending the Filter

### Adding New Words

```csharp
// In InitializeDemonetizedWords()
var customWords = new[] { "newword1", "newword2" };
foreach (var word in customWords)
{
    _demonetizedWords.Add(word);
}
```

### Adding New Patterns

```csharp
// In InitializeDemonetizedPatterns()
var newPattern = @"\bcustom\s+pattern\b";
_demonetizedPatterns.Add(new Regex(newPattern, RegexOptions.IgnoreCase));
```

### Custom Severity Rules

```csharp
private FlagSeverity GetSeverity(string word)
{
    // Add custom logic
    if (MyCustomHighSeverityCheck(word))
        return FlagSeverity.High;
    
    // ... existing logic
}
```

## Future Enhancements

1. **Google Sheets Integration**: Automatically sync word list from the community spreadsheet
2. **Machine Learning**: Use ML models to detect context-dependent issues
3. **Multi-Language Support**: Extend filtering to non-English content
4. **Platform-Specific Profiles**: Different filter rules for YouTube vs TikTok
5. **Allowlist**: Whitelist certain words in specific contexts
6. **Real-time Updates**: Subscribe to platform policy updates

## Limitations

- **Context Blind**: Cannot understand context (e.g., "cancer research" vs "spreading like cancer")
- **False Positives**: Some legitimate content may be flagged
- **Language Specific**: Currently only supports English
- **Not Exhaustive**: Cannot catch all potentially problematic content
- **Platform Updates**: Platform policies change frequently

## Testing

Run the test suite:

```bash
cd src/CSharp
dotnet test --filter "FullyQualifiedName~ContentFilterTests"
```

Test coverage includes:
- Clean content detection
- Demonetized word flagging
- Pattern matching
- Severity classification
- Replacement suggestions
- Case insensitivity
- Edge cases

## References

- [YouTube Advertiser-Friendly Guidelines](https://support.google.com/youtube/answer/6162278)
- [Community Spreadsheet](https://docs.google.com/spreadsheets/d/1ozg1Cnm6SdtM4M5rATkANAi07xAzYWaKL7HKxyvoHzk/htmlview#gid=1380702445)
- [Reddit Discussion](https://www.reddit.com/r/youtubers/comments/db5kgt/tips_tricks_list_of_youtube_demonetized_words_for/)
- [TikTok Community Guidelines](https://www.tiktok.com/community-guidelines)
- [Instagram Community Guidelines](https://help.instagram.com/477434105621119)

## Support

For issues or questions about the content filter:
1. Check the test suite for examples
2. Review the inline code documentation
3. Open a GitHub issue with the `content-filter` label
