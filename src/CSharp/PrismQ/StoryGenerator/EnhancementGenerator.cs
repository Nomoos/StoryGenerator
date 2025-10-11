using Microsoft.Extensions.Logging;
using PrismQ.Shared.Core.Services;
using StoryGenerator.Providers.OpenAI;

namespace PrismQ.StoryGenerator;

/// <summary>
/// Enhances scripts with ElevenLabs voice performance tags.
/// Ported from Python Generators/GEnhanceScript.py with C# enhancements.
/// </summary>
public class EnhancementGenerator : IEnhancementGenerator
{
    private readonly OpenAIClient _openAIClient;
    private readonly ILogger<EnhancementGenerator> _logger;
    private readonly PerformanceMonitor _performanceMonitor;

    public string Name => "EnhancementGenerator";
    public string Version => "1.0.0";

    public EnhancementGenerator(
        OpenAIClient openAIClient,
        ILogger<EnhancementGenerator> logger,
        PerformanceMonitor performanceMonitor)
    {
        _openAIClient = openAIClient;
        _logger = logger;
        _performanceMonitor = performanceMonitor;
    }

    public async Task<string> EnhanceScriptAsync(
        string revisedScript,
        string storyTitle,
        CancellationToken cancellationToken = default)
    {
        return await _performanceMonitor.MeasureAsync(
            "Script_Enhancement",
            storyTitle,
            async () => await EnhanceScriptInternalAsync(revisedScript, cancellationToken),
            new Dictionary<string, object>
            {
                { "script_length", revisedScript.Length }
            });
    }

    private async Task<string> EnhanceScriptInternalAsync(
        string revisedScript,
        CancellationToken cancellationToken)
    {
        var messages = new List<ChatMessage>
        {
            ChatMessage.System(BuildSystemPrompt()),
            ChatMessage.User(BuildUserPrompt(revisedScript))
        };

        _logger.LogInformation("Enhancing script with ElevenLabs tags");

        var response = await _openAIClient.CreateChatCompletionAsync(
            messages,
            cancellationToken: cancellationToken);

        var enhancedScript = response.Choices.FirstOrDefault()?.Message.Content?.Trim()
            ?? throw new InvalidOperationException("No response from OpenAI");

        _logger.LogInformation("✅ Script enhanced with voice tags");

        return enhancedScript;
    }

    public async Task<string> EnhanceAndSaveScriptAsync(
        string revisedDirectory,
        string storyTitle,
        CancellationToken cancellationToken = default)
    {
        // Load revised script
        var revisedPath = Path.Combine(revisedDirectory, "Revised.txt");
        if (!File.Exists(revisedPath))
        {
            throw new FileNotFoundException($"Revised script file not found: {revisedPath}");
        }

        var revisedScript = await File.ReadAllTextAsync(revisedPath, cancellationToken);

        // Enhance the script
        var enhancedScript = await EnhanceScriptAsync(revisedScript, storyTitle, cancellationToken);

        // Save enhanced script in the same directory
        var enhancedPath = Path.Combine(revisedDirectory, "Revised_with_eleven_labs_tags.txt");
        await File.WriteAllTextAsync(enhancedPath, enhancedScript, cancellationToken);

        _logger.LogInformation("Saved enhanced script to: {EnhancedPath}", enhancedPath);

        return enhancedPath;
    }

    private string BuildSystemPrompt()
    {
        return @"You are a voice performance director. Your task is to enhance a narration script by inserting **non-spoken ElevenLabs v3 audio tags** into the original story — **without rewriting or changing any text**.
        
            🎯 Objective:  
            Make the story sound like it's being told by a real 12–18-year-old girl in the U.S. — emotional, relatable, and believable. Add tags only where emotion, pacing, or realism clearly improves the narration.
        
            🛑 Do NOT:
            - Reword, rewrite, or fix anything
            - Change punctuation, grammar, or spelling
            - Add comments, explanations, or formatting
            - Tag every line — use tags only where needed
        
            ✅ Use only these tags, in this order of relevance for teen voice:
        
            **💖 Emotional tone & relatability**  
            [embarrassed], [hopeful], [sad], [excited], [relieved], [confused], [disappointed], [sincere]
        
            **🧠 Internal reactions & anxiety**  
            [hesitates], [sighs], [gulps], [gasps], [crying], [starts to say something], [trailing off]
        
            **🎭 Tone & style**  
            [playfully], [sarcastic], [speaking softly], [whispers], [deadpan], [matter-of-fact]
        
            **⏱️ Rhythm & pacing**  
            [pause], [long pause], [slowly], [rushed]
        
            **⚠️ Rare or intense**  
            [angry], [shouting], [terrified], [laughs], [groans], [clears throat], [inhales], [exhales], [snorts]
        
            📏 Tagging rules:
            - Max **3 tags per paragraph**
            - Max **2 tags stacked**
            - Tags go **before** the line or phrase they affect
            - If unsure, **leave it untagged**
            - Use order: **[emotion][reaction][pacing]**
        
            📘 Example:
            > [hesitates][sad] I looked at him and said I was done.  
            > [pause][playfully] You're kidding… right?  
            > I made breakfast and sat on the couch. (no tags — neutral)
        
            🎯 Final Output:  
            Return the full story with inline tags. Do not change anything else.".Trim();
    }

    private string BuildUserPrompt(string script)
    {
        return $@"Please enhance the story below by inserting **non-spoken ElevenLabs v3 audio tags**. These tags should help guide how the story is read aloud by an AI voice — **without rewriting the story in any way**.
        
            🎯 Voice Style:  
            The narrator is a girl aged 12–18 in the U.S., telling a real-life or Reddit-style story on TikTok or YouTube Shorts. Keep it emotionally honest, conversational, and rhythmically engaging.
        
            🛑 Do NOT:
            - Change, fix, rephrase, or remove any text
            - Adjust grammar, spelling, or punctuation
            - Add explanations or formatting
            - Tag every sentence — use tags **only where needed**
        
            ✅ Insert only these tags, in square brackets, before the line they affect:
        
            **💖 Emotional tone & relatability**  
            [embarrassed], [hopeful], [sad], [excited], [relieved], [confused], [disappointed], [sincere]
        
            **🧠 Internal reactions & anxiety**  
            [hesitates], [sighs], [gulps], [gasps], [crying], [starts to say something], [trailing off]
        
            **🎭 Tone & style**  
            [playfully], [sarcastic], [speaking softly], [whispers], [deadpan], [matter-of-fact]
        
            **⏱️ Rhythm & pacing**  
            [pause], [long pause], [slowly], [rushed]
        
            **⚠️ Rare or intense**  
            [angry], [shouting], [terrified], [laughs], [groans], [clears throat], [inhales], [exhales], [snorts]
        
            📏 Rules:
            - Max 3 tags per paragraph
            - Max 2 tags stacked
            - Place each tag **before** the affected line
            - If emotion or pacing is unclear — do **not** add a tag
            - Tag order: [emotion][reaction][pacing]
        
            📘 Examples:
        
            > [pause][hopeful] Maybe… this could actually work.  
            > [embarrassed][laughs] I seriously said that — out loud.  
            > I made toast and walked to school. *(no tags added)*
        
            🎯 Return only the story with tags. Do not explain, wrap, or format the output.
        
            Story:
            {script.Trim()}".Trim();
    }
}
