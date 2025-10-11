using PrismQ.Shared.Models;

namespace StoryGenerator.Pipeline.Stages.Models;

/// <summary>
/// Input for Script Generation Stage
/// </summary>
public class ScriptGenerationInput
{
    /// <summary>
    /// Story ideas to generate scripts from
    /// </summary>
    public List<StoryIdea> StoryIdeas { get; set; } = new();
}

/// <summary>
/// Output from Script Generation Stage
/// </summary>
public class ScriptGenerationOutput
{
    /// <summary>
    /// Generated scripts
    /// </summary>
    public List<GeneratedScript> GeneratedScripts { get; set; } = new();
}

/// <summary>
/// Represents a generated script
/// </summary>
public class GeneratedScript
{
    /// <summary>
    /// Unique identifier
    /// </summary>
    public string Id { get; set; } = Guid.NewGuid().ToString();

    /// <summary>
    /// Source story idea
    /// </summary>
    public StoryIdea? SourceIdea { get; set; }

    /// <summary>
    /// Script content
    /// </summary>
    public string Content { get; set; } = string.Empty;

    /// <summary>
    /// Script title
    /// </summary>
    public string Title { get; set; } = string.Empty;

    /// <summary>
    /// Word count
    /// </summary>
    public int WordCount { get; set; }

    /// <summary>
    /// Generation timestamp
    /// </summary>
    public DateTime GeneratedAt { get; set; } = DateTime.UtcNow;
}

/// <summary>
/// Input for Script Improvement Stage
/// </summary>
public class ScriptImprovementInput
{
    /// <summary>
    /// Scripts to improve
    /// </summary>
    public List<GeneratedScript> Scripts { get; set; } = new();

    /// <summary>
    /// Number of improvement iterations per script
    /// </summary>
    public int ImprovementIterations { get; set; } = 3;
}

/// <summary>
/// Output from Script Improvement Stage
/// </summary>
public class ScriptImprovementOutput
{
    /// <summary>
    /// Improved script versions
    /// </summary>
    public List<ImprovedScript> ImprovedScripts { get; set; } = new();
}

/// <summary>
/// Represents an improved script version
/// </summary>
public class ImprovedScript
{
    /// <summary>
    /// Original script
    /// </summary>
    public GeneratedScript? OriginalScript { get; set; }

    /// <summary>
    /// Version identifier (v1, v2, v3, v4)
    /// </summary>
    public string Version { get; set; } = "v1";

    /// <summary>
    /// Improved content
    /// </summary>
    public string Content { get; set; } = string.Empty;

    /// <summary>
    /// Improvements made
    /// </summary>
    public List<string> Improvements { get; set; } = new();

    /// <summary>
    /// Improvement timestamp
    /// </summary>
    public DateTime ImprovedAt { get; set; } = DateTime.UtcNow;
}

/// <summary>
/// Input for Script Scoring Stage
/// </summary>
public class ScriptScoringInput
{
    /// <summary>
    /// Improved scripts to score
    /// </summary>
    public List<ImprovedScript> Scripts { get; set; } = new();
}

/// <summary>
/// Output from Script Scoring Stage
/// </summary>
public class ScriptScoringOutput
{
    /// <summary>
    /// Scored scripts
    /// </summary>
    public List<ScoredScript> ScoredScripts { get; set; } = new();
}

/// <summary>
/// Represents a scored script
/// </summary>
public class ScoredScript
{
    /// <summary>
    /// The improved script
    /// </summary>
    public ImprovedScript Script { get; set; } = new();

    /// <summary>
    /// Overall quality score (0-100)
    /// </summary>
    public double QualityScore { get; set; }

    /// <summary>
    /// Emotional impact score (0-100)
    /// </summary>
    public double EmotionalImpact { get; set; }

    /// <summary>
    /// Narrative flow score (0-100)
    /// </summary>
    public double NarrativeFlow { get; set; }

    /// <summary>
    /// Clarity score (0-100)
    /// </summary>
    public double Clarity { get; set; }
}

/// <summary>
/// Input for Script Selection Stage
/// </summary>
public class ScriptSelectionInput
{
    /// <summary>
    /// Scored scripts to select from
    /// </summary>
    public List<ScoredScript> ScoredScripts { get; set; } = new();

    /// <summary>
    /// Number of scripts to select
    /// </summary>
    public int SelectCount { get; set; } = 1;
}

/// <summary>
/// Output from Script Selection Stage
/// </summary>
public class ScriptSelectionOutput
{
    /// <summary>
    /// Selected best scripts
    /// </summary>
    public List<ImprovedScript> SelectedScripts { get; set; } = new();
}

/// <summary>
/// Input for Script Revision Stage
/// </summary>
public class ScriptRevisionInput
{
    /// <summary>
    /// Scripts to revise for voice clarity
    /// </summary>
    public List<ImprovedScript> Scripts { get; set; } = new();
}

/// <summary>
/// Output from Script Revision Stage
/// </summary>
public class ScriptRevisionOutput
{
    /// <summary>
    /// Revised scripts
    /// </summary>
    public List<RevisedScript> RevisedScripts { get; set; } = new();
}

/// <summary>
/// Represents a revised script
/// </summary>
public class RevisedScript
{
    /// <summary>
    /// Source improved script
    /// </summary>
    public ImprovedScript? SourceScript { get; set; }

    /// <summary>
    /// Revised content (optimized for voice)
    /// </summary>
    public string Content { get; set; } = string.Empty;

    /// <summary>
    /// Revisions made
    /// </summary>
    public List<string> Revisions { get; set; } = new();

    /// <summary>
    /// Revision timestamp
    /// </summary>
    public DateTime RevisedAt { get; set; } = DateTime.UtcNow;
}

/// <summary>
/// Input for Script Enhancement Stage
/// </summary>
public class ScriptEnhancementInput
{
    /// <summary>
    /// Revised scripts to enhance with voice tags
    /// </summary>
    public List<RevisedScript> Scripts { get; set; } = new();
}

/// <summary>
/// Output from Script Enhancement Stage
/// </summary>
public class ScriptEnhancementOutput
{
    /// <summary>
    /// Enhanced scripts
    /// </summary>
    public List<EnhancedScript> EnhancedScripts { get; set; } = new();
}

/// <summary>
/// Represents an enhanced script with voice tags
/// </summary>
public class EnhancedScript
{
    /// <summary>
    /// Source revised script
    /// </summary>
    public RevisedScript? SourceScript { get; set; }

    /// <summary>
    /// Enhanced content with ElevenLabs voice tags
    /// </summary>
    public string Content { get; set; } = string.Empty;

    /// <summary>
    /// Enhancements applied
    /// </summary>
    public List<string> Enhancements { get; set; } = new();

    /// <summary>
    /// Enhancement timestamp
    /// </summary>
    public DateTime EnhancedAt { get; set; } = DateTime.UtcNow;
}

/// <summary>
/// Input for Script Validation Stage
/// </summary>
public class ScriptValidationInput
{
    /// <summary>
    /// Enhanced scripts to validate
    /// </summary>
    public List<EnhancedScript> Scripts { get; set; } = new();
}

/// <summary>
/// Output from Script Validation Stage
/// </summary>
public class ScriptValidationOutput
{
    /// <summary>
    /// Validated scripts
    /// </summary>
    public List<ValidatedScript> ValidatedScripts { get; set; } = new();
}

/// <summary>
/// Represents a validated script
/// </summary>
public class ValidatedScript
{
    /// <summary>
    /// The enhanced script
    /// </summary>
    public EnhancedScript Script { get; set; } = new();

    /// <summary>
    /// Whether the script is valid
    /// </summary>
    public bool IsValid { get; set; }

    /// <summary>
    /// Validation messages
    /// </summary>
    public List<string> ValidationMessages { get; set; } = new();
}

/// <summary>
/// Input for Script Registry Update Stage
/// </summary>
public class ScriptRegistryUpdateInput
{
    /// <summary>
    /// Validated scripts to register
    /// </summary>
    public List<ValidatedScript> ValidatedScripts { get; set; } = new();
}

/// <summary>
/// Output from Script Registry Update Stage
/// </summary>
public class ScriptRegistryUpdateOutput
{
    /// <summary>
    /// Number of scripts registered
    /// </summary>
    public int RegisteredCount { get; set; }

    /// <summary>
    /// Registry file path
    /// </summary>
    public string RegistryPath { get; set; } = string.Empty;
}
