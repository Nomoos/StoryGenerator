using Microsoft.Extensions.Logging;
using PrismQ.Shared.Core.Services;
using StoryGenerator.Providers.OpenAI;

namespace PrismQ.StoryGenerator;

/// <summary>
/// Revises scripts for AI voice clarity and natural speech patterns.
/// Ported from Python Generators/GRevise.py with C# enhancements.
/// </summary>
public class RevisionGenerator : IRevisionGenerator
{
    private readonly OpenAIClient _openAIClient;
    private readonly ILogger<RevisionGenerator> _logger;
    private readonly PerformanceMonitor _performanceMonitor;

    public string Name => "RevisionGenerator";
    public string Version => "1.0.0";

    public RevisionGenerator(
        OpenAIClient openAIClient,
        ILogger<RevisionGenerator> logger,
        PerformanceMonitor performanceMonitor)
    {
        _openAIClient = openAIClient;
        _logger = logger;
        _performanceMonitor = performanceMonitor;
    }

    public async Task<string> ReviseScriptAsync(
        string scriptText,
        string storyTitle,
        CancellationToken cancellationToken = default)
    {
        return await _performanceMonitor.MeasureAsync(
            "Script_Revision",
            storyTitle,
            async () => await ReviseScriptInternalAsync(scriptText, cancellationToken),
            new Dictionary<string, object>
            {
                { "original_length", scriptText.Length },
                { "original_word_count", scriptText.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length }
            });
    }

    private async Task<string> ReviseScriptInternalAsync(
        string scriptText,
        CancellationToken cancellationToken)
    {
        var messages = new List<ChatMessage>
        {
            ChatMessage.System(BuildSystemPrompt()),
            ChatMessage.User(BuildUserPrompt(scriptText))
        };

        _logger.LogInformation("Revising script ({Words} words)", 
            scriptText.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length);

        var response = await _openAIClient.CreateChatCompletionAsync(
            messages,
            cancellationToken: cancellationToken);

        var revisedScript = response.Choices.FirstOrDefault()?.Message.Content?.Trim()
            ?? throw new InvalidOperationException("No response from OpenAI");

        var wordCount = revisedScript.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;
        _logger.LogInformation("✅ Script revised: {WordCount} words", wordCount);

        return revisedScript;
    }

    public async Task<string> ReviseAndSaveScriptAsync(
        string scriptDirectory,
        string outputDirectory,
        string storyTitle,
        CancellationToken cancellationToken = default)
    {
        // Load original script
        var scriptPath = Path.Combine(scriptDirectory, "Script.txt");
        if (!File.Exists(scriptPath))
        {
            throw new FileNotFoundException($"Script file not found: {scriptPath}");
        }

        var originalScript = await File.ReadAllTextAsync(scriptPath, cancellationToken);

        // Revise the script
        var revisedScript = await ReviseScriptAsync(originalScript, storyTitle, cancellationToken);

        // Create output directory
        var sanitizedTitle = FileHelper.SanitizeFilename(storyTitle);
        var revisedFolder = Path.Combine(outputDirectory, sanitizedTitle);
        Directory.CreateDirectory(revisedFolder);

        // Save revised script
        var revisedPath = Path.Combine(revisedFolder, "Revised.txt");
        await File.WriteAllTextAsync(revisedPath, revisedScript, cancellationToken);

        // Copy idea file if it exists
        var ideaSourcePath = Path.Combine(scriptDirectory, "Idea.json");
        if (File.Exists(ideaSourcePath))
        {
            var ideaDestPath = Path.Combine(revisedFolder, "Idea.json");
            File.Copy(ideaSourcePath, ideaDestPath, overwrite: true);
        }

        _logger.LogInformation("Saved revised script to: {RevisedPath}", revisedPath);

        return revisedPath;
    }

    private string BuildSystemPrompt()
    {
        return @"You are a professional viral storyteller. Your job is to rewrite and improve real-life or Reddit-style stories for short-form videos on TikTok, YouTube Shorts, and Instagram Reels. These stories must sound like someone is telling them out loud — naturally, emotionally, and conversationally. You are not writing for the page. You are writing for the ear.
        
            The target audience is people in the United States between ten and thirty years old. They care about emotional drama, awkward moments, rebellion, identity, and finding connection in a chaotic world.
        
            The final output must be a single block of clean, natural spoken narration. No formatting, no tags, no stage directions, no emojis, no labels — just what would be said aloud.
        
            Avoid all abbreviations and shorthand like ""IDK,"" ""LOL,"" ""'00s,"" ""etc.,"" or ""TBH."" Always write them out fully. Say ""I don't know"" instead of ""IDK"" and ""the early two-thousands"" instead of ""'00s.""
        
            🟢 **Always prioritize clarity and flow in speech.** Avoid clunky phrasing, stacked consonants, or abstract terms that sound stiff or overly formal when read aloud. Don't use phrases like ""a force of unapologetic self-expression"" or ""platform flip-flops"" unless they truly roll off the tongue. Choose vivid, concrete, human language.
        
            Use simple grammar and everyday words. Keep sentences short to medium-length. Break thoughts into natural pauses. No semicolons or stacked punctuation. Think rhythm, not rules.
        
            Start with a strong hook — a moment of emotion, confusion, or tension. Build curiosity. Let feelings unfold naturally. Show emotion through thoughts and choices, not by labeling it.
        
            End with power — a shift, a twist, a realization, or a moment that lingers. The final line should make the listener stop and think.
        
            Output only the clean, finished spoken narration. Nothing else.".Trim();
    }

    private string BuildUserPrompt(string script)
    {
        return $@"Please rewrite the following story into a natural, emotionally engaging narration for short-form video. Follow all the style and formatting rules from the system prompt.
        
            Make sure it reads smoothly when spoken by realistic AI voices like ElevenLabs. Use clean, expressive phrasing with a natural rhythm. Favor short, clear sentences. Use commas or new lines to guide pacing, but avoid overusing punctuation.
        
            🟢 Polish every line for spoken clarity. Remove or rephrase anything that might sound stiff, robotic, or awkward when read aloud. Replace abstract, heavy phrases with vivid, human language. Watch out for clunky word combinations like ""platform flip-flops,"" ""unapologetic self-expression,"" or long noun strings. Everything should feel like something a real person would say confidently and smoothly.
        
            No tags, no formatting, no headings — just the final spoken narration. Return only the clean text.
        
            Story:
            {script.Trim()}".Trim();
    }
}
