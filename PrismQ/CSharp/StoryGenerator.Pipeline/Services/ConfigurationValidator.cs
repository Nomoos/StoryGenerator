using StoryGenerator.Pipeline.Config;

namespace StoryGenerator.Pipeline.Services;

/// <summary>
/// Validates pipeline configuration for correctness and completeness.
/// </summary>
public class ConfigurationValidator
{
    private readonly List<string> _errors = new();
    private readonly List<string> _warnings = new();

    /// <summary>
    /// Validate the pipeline configuration
    /// </summary>
    /// <param name="config">Configuration to validate</param>
    /// <returns>True if valid, false otherwise</returns>
    public bool Validate(PipelineConfig config)
    {
        _errors.Clear();
        _warnings.Clear();

        if (config == null)
        {
            _errors.Add("Configuration cannot be null");
            return false;
        }

        ValidatePathsConfig(config.Paths);
        ValidateGenerationConfig(config.Generation);
        ValidateProcessingConfig(config.Processing);
        ValidateLoggingConfig(config.Logging);
        ValidatePipelineSettings(config.Pipeline);

        return _errors.Count == 0;
    }

    /// <summary>
    /// Get validation errors
    /// </summary>
    public IReadOnlyList<string> Errors => _errors.AsReadOnly();

    /// <summary>
    /// Get validation warnings
    /// </summary>
    public IReadOnlyList<string> Warnings => _warnings.AsReadOnly();

    private void ValidatePathsConfig(PathsConfig paths)
    {
        if (paths == null)
        {
            _errors.Add("Paths configuration cannot be null");
            return;
        }

        // Validate required paths
        if (string.IsNullOrWhiteSpace(paths.StoryRoot))
        {
            _errors.Add("StoryRoot path must be specified");
        }

        if (string.IsNullOrWhiteSpace(paths.PythonRoot))
        {
            _errors.Add("PythonRoot path must be specified");
        }

        // Check if paths are absolute or relative
        if (!string.IsNullOrWhiteSpace(paths.StoryRoot))
        {
            try
            {
                var fullPath = Path.GetFullPath(paths.StoryRoot);
                if (!Path.IsPathRooted(paths.StoryRoot))
                {
                    _warnings.Add($"StoryRoot is relative: {paths.StoryRoot} -> {fullPath}");
                }
            }
            catch (Exception ex)
            {
                _errors.Add($"Invalid StoryRoot path: {ex.Message}");
            }
        }
    }

    private void ValidateGenerationConfig(GenerationConfig generation)
    {
        if (generation == null)
        {
            _errors.Add("Generation configuration cannot be null");
            return;
        }

        // Validate story config
        if (generation.Story.Count < 1)
        {
            _errors.Add("Story count must be at least 1");
        }

        if (generation.Story.TargetLength < 50)
        {
            _warnings.Add($"Story target length ({generation.Story.TargetLength}) is very short");
        }

        // Validate voice config
        if (generation.Voice.Stability < 0 || generation.Voice.Stability > 1)
        {
            _errors.Add("Voice stability must be between 0 and 1");
        }

        if (generation.Voice.SimilarityBoost < 0 || generation.Voice.SimilarityBoost > 1)
        {
            _errors.Add("Voice similarity boost must be between 0 and 1");
        }

        // Validate video config
        if (generation.Video.Resolution.Width < 1 || generation.Video.Resolution.Height < 1)
        {
            _errors.Add("Video resolution must be positive");
        }

        if (generation.Video.Fps < 1 || generation.Video.Fps > 120)
        {
            _errors.Add("Video FPS must be between 1 and 120");
        }

        // Validate synthesis method
        if (!string.IsNullOrWhiteSpace(generation.Video.SynthesisMethod))
        {
            var method = generation.Video.SynthesisMethod.ToLowerInvariant().Trim();
            if (method != "ltx" && method != "keyframe")
            {
                _errors.Add($"Invalid synthesis method '{generation.Video.SynthesisMethod}'. Must be 'ltx' or 'keyframe'");
            }
        }
    }

    private void ValidateProcessingConfig(ProcessingConfig processing)
    {
        if (processing == null)
        {
            _errors.Add("Processing configuration cannot be null");
            return;
        }

        // Validate error handling settings
        if (processing.ErrorHandling.RetryCount < 0)
        {
            _errors.Add("Max retry attempts cannot be negative");
        }

        if (processing.ErrorHandling.RetryDelay < 0)
        {
            _errors.Add("Retry delay cannot be negative");
        }

        // Validate parallel processing
        if (processing.Parallel.Enabled && processing.Parallel.MaxWorkers < 1)
        {
            _errors.Add("Max workers must be at least 1 when parallel processing is enabled");
        }
    }

    private void ValidateLoggingConfig(LoggingConfig logging)
    {
        if (logging == null)
        {
            _errors.Add("Logging configuration cannot be null");
            return;
        }

        // Validate log level
        var validLevels = new[] { "DEBUG", "INFO", "WARNING", "ERROR" };
        if (!validLevels.Contains(logging.Level?.ToUpperInvariant()))
        {
            _errors.Add($"Invalid log level '{logging.Level}'. Must be one of: {string.Join(", ", validLevels)}");
        }

        // Validate log file path if specified
        if (!string.IsNullOrWhiteSpace(logging.File))
        {
            try
            {
                var directory = Path.GetDirectoryName(Path.GetFullPath(logging.File));
                if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
                {
                    _warnings.Add($"Log file directory does not exist: {directory}");
                }
            }
            catch (Exception ex)
            {
                _errors.Add($"Invalid log file path: {ex.Message}");
            }
        }
    }

    private void ValidatePipelineSettings(PipelineSettings pipeline)
    {
        if (pipeline == null)
        {
            _errors.Add("Pipeline settings cannot be null");
            return;
        }

        if (string.IsNullOrWhiteSpace(pipeline.Name))
        {
            _warnings.Add("Pipeline name is not set");
        }

        // Check if at least one step is enabled
        var steps = pipeline.Steps;
        bool anyStepEnabled = steps.StoryIdea || steps.ScriptGeneration || steps.ScriptRevision ||
                              steps.ScriptEnhancement || steps.VoiceSynthesis || steps.AsrSubtitles ||
                              steps.SceneAnalysis || steps.SceneDescription || steps.KeyframeGeneration ||
                              steps.VideoInterpolation || steps.VideoComposition;

        if (!anyStepEnabled)
        {
            _warnings.Add("No pipeline steps are enabled");
        }
    }
}
