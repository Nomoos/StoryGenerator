using Microsoft.Extensions.Logging;
using PrismQ.Shared.Models;
using PrismQ.Shared.Core;
using PrismQ.Shared.Core.Configuration;
using PrismQ.Shared.Core.Services;
using StoryGenerator.Providers.OpenAI;

namespace PrismQ.StoryGenerator;

/// <summary>
/// Generates ~360 word scripts from story ideas.
/// Ported from Python Generators/GScript.py with C# enhancements.
/// </summary>
public class ScriptGenerator : IScriptGenerator
{
    private readonly OpenAIClient _openAIClient;
    private readonly ILogger<ScriptGenerator> _logger;
    private readonly PerformanceMonitor _performanceMonitor;
    private readonly PathConfiguration _pathConfiguration;

    public string Name => "ScriptGenerator";
    public string Version => "1.0.0";

    public ScriptGenerator(
        OpenAIClient openAIClient,
        ILogger<ScriptGenerator> logger,
        PerformanceMonitor performanceMonitor,
        PathConfiguration pathConfiguration)
    {
        _openAIClient = openAIClient;
        _logger = logger;
        _performanceMonitor = performanceMonitor;
        _pathConfiguration = pathConfiguration;
    }

    public async Task<string> GenerateScriptAsync(
        StoryIdea storyIdea,
        CancellationToken cancellationToken = default)
    {
        return await _performanceMonitor.MeasureAsync(
            "Script_Generation",
            storyIdea.StoryTitle,
            async () => await GenerateScriptInternalAsync(storyIdea, cancellationToken),
            new Dictionary<string, object> { { "language", storyIdea.Language } });
    }

    private async Task<string> GenerateScriptInternalAsync(
        StoryIdea storyIdea,
        CancellationToken cancellationToken)
    {
        var systemPrompt = BuildSystemPrompt(storyIdea);
        var userPrompt = BuildUserPrompt(storyIdea);

        var messages = new List<ChatMessage>
        {
            ChatMessage.System(systemPrompt),
            ChatMessage.User(userPrompt)
        };

        _logger.LogInformation("Generating script for: {Title}", storyIdea.StoryTitle);

        var response = await _openAIClient.CreateChatCompletionAsync(
            messages,
            cancellationToken: cancellationToken);

        var script = response.Choices.FirstOrDefault()?.Message.Content?.Trim()
            ?? throw new InvalidOperationException("No response from OpenAI");

        var wordCount = script.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;
        _logger.LogInformation("✅ Script generated: {WordCount} words", wordCount);

        return script;
    }

    public async Task<string> GenerateAndSaveScriptAsync(
        StoryIdea storyIdea,
        string outputDirectory,
        CancellationToken cancellationToken = default)
    {
        var script = await GenerateScriptAsync(storyIdea, cancellationToken);

        var sanitizedTitle = FileHelper.SanitizeFilename(storyIdea.StoryTitle);
        var storyFolder = Path.Combine(outputDirectory, sanitizedTitle);
        Directory.CreateDirectory(storyFolder);

        // Save script
        var scriptPath = Path.Combine(storyFolder, "Script.txt");
        await File.WriteAllTextAsync(scriptPath, script, cancellationToken);

        // Save idea file
        var ideaPath = Path.Combine(storyFolder, "Idea.json");
        await storyIdea.ToFileAsync(ideaPath);

        _logger.LogInformation("Saved script to: {ScriptPath}", scriptPath);

        return scriptPath;
    }

    private string BuildSystemPrompt(StoryIdea storyIdea)
    {
        var narratorType = storyIdea.NarratorType ?? "first-person";
        var voiceNote = !string.IsNullOrEmpty(storyIdea.VoiceStyle)
            ? $@"Use a voice style that feels ""{storyIdea.VoiceStyle}""."
            : "";

        var toneNote = storyIdea.NarratorGender.ToLowerInvariant() switch
        {
            "female" => "Favor emotionally layered, introspective delivery — vulnerability is strength.",
            "male" => "Lean into emotional honesty — let tension and reflection carry the story.",
            _ => ""
        };

        return $@"You are a professional viral storyteller writing scripts designed for TikTok, YouTube Shorts, and Reels.
                
                Your stories should be written in a {narratorType}, emotionally engaging, voiceover-friendly style.
                {voiceNote}
                {toneNote}
                
                Focus on stories where a person from a modest or working-class background interacts with wealth, power, or privilege — often through dating someone rich, meeting their family, or being exposed to a different world.
                
                Every story must follow this structure:
                
                1. Hook:
                Start with a strong, attention-grabbing first line (within 1–2 sentences) that sparks curiosity or tension.
                Examples:
                – ""I dated a billionaire's daughter. Her dad taught me more than school ever did.""
                – ""I wore a $20 Target shirt to dinner with millionaires. Here's what happened.""
                
                2. Conflict / Insecurity:
                Describe a moment where the narrator feels out of place, ashamed, judged, or underestimated.
                Use vivid emotional cues and sensory details — let the audience feel their discomfort or doubt.
                
                3. Shift or Reveal:
                Include an unexpected moment of connection, irony, or reversal.
                Either the rich person reveals humility… or the narrator discovers who truly holds power or value.
                
                4. Payoff / Moral / Quote:
                End with a single emotionally satisfying line, quote, or realization.
                Something that lingers — a mic-drop moment, bittersweet truth, or shift in self-worth.
                
                The voice should be casual, emotionally raw, and paced for vertical video — short paragraphs, natural rhythm.
                
                ✸ Avoid overexplaining — let the story unfold naturally.        
                ✸ Include subtle emotional ironies or details that viewers may only notice on second watch.
                ✸ Leave just enough unsaid to spark comments and debate (""Was the dad testing him?"", ""Did she already know?"").
                ✸ Avoid camera directions or formatting — output only the character's inner narration.
                ✸ Avoid polished ""writerly"" structure
                ✸ Include human-level imperfection, memory fuzziness, or honesty".Trim();
    }

    private string BuildUserPrompt(StoryIdea storyIdea)
    {
        var narratorType = storyIdea.NarratorType ?? "first-person";
        var prompt = $@"Write a {narratorType} voiceover story for a vertical video titled: ""{storyIdea.StoryTitle}""

";

        if (!string.IsNullOrEmpty(storyIdea.Goal))
        {
            prompt += $"Goal: {storyIdea.Goal}\n\n";
        }

        if (!string.IsNullOrEmpty(storyIdea.Language) && storyIdea.Language != "en")
        {
            var languageName = FileHelper.GetLanguageName(storyIdea.Language);
            prompt += $"Language: Write the story in {languageName}\n\n";
        }

        if (storyIdea.Personalization != null && storyIdea.Personalization.Count > 0)
        {
            prompt += "Personalization: ";
            foreach (var kvp in storyIdea.Personalization)
            {
                prompt += $"Use '{kvp.Value}' for {kvp.Key}. ";
            }
            prompt += "\n\n";
        }

        var fields = new Dictionary<string, string?>
        {
            ["Style and Tone"] = storyIdea.Tone,
            ["Theme"] = storyIdea.Theme,
            ["Narrator Type"] = storyIdea.NarratorType,
            ["Narrator Gender"] = storyIdea.NarratorGender,
            ["Other Main Character"] = storyIdea.OtherCharacter,
            ["Key Plot Outcome"] = storyIdea.Outcome,
            ["Emotional Core"] = storyIdea.EmotionalCore,
            ["Power Dynamic"] = storyIdea.PowerDynamic,
            ["Timeline"] = storyIdea.Timeline,
            ["Twist Type"] = storyIdea.TwistType,
            ["Character Arc"] = storyIdea.CharacterArc,
            ["Voice Style"] = storyIdea.VoiceStyle,
            ["Target Moral or Theme"] = storyIdea.TargetMoral,
            ["Locations"] = storyIdea.Locations,
            ["Mentioned Brands"] = storyIdea.MentionedBrands
        };

        foreach (var (label, value) in fields)
        {
            if (!string.IsNullOrEmpty(value))
            {
                prompt += $"{label}: {value}\n";
            }
        }

        prompt += @"
            Script Requirements:
            1. Hook the viewer in the first 1–2 lines — something emotional, weird, or intriguing.
            2. Follow a simple structure: setup → rising tension/emotion → twist/reveal → emotional payoff.
            3. Keep the story around ~360 words. A slight overflow is okay if it helps with emotional payoff.
            4. Use spoken, conversational English — short, vivid sentences with natural rhythm.
            5. Use **clear, easy-to-understand language** — avoid abbreviations, decade references like ""'00s"", technical terms, or anything that might sound awkward or confusing when read aloud.
            6. Do not use any voice tags or technical formatting. Just the raw, natural storytelling.
            7. Output only the final voiceover narration — no explanations, labels, or instructions.
            
            Audience: Viewers aged 10–30 in the US, Canada, and Australia who binge emotional or dramatic vertical stories on TikTok, YouTube Shorts, and Instagram Reels.
            
            Final Output: The complete spoken narration, natural and clean. Just text — nothing else.
            ".Trim();

        return prompt;
    }
}
