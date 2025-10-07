using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace StoryGenerator.Pipeline.Config;

/// <summary>
/// Loads and manages pipeline configuration from YAML files.
/// Follows Single Responsibility Principle - only handles configuration loading.
/// </summary>
public static class ConfigLoader
{
    private static readonly IDeserializer YamlDeserializer = new DeserializerBuilder()
        .WithNamingConvention(UnderscoredNamingConvention.Instance)
        .Build();

    /// <summary>
    /// Load configuration from YAML file
    /// </summary>
    /// <param name="configPath">Path to YAML configuration file</param>
    /// <returns>Loaded pipeline configuration</returns>
    /// <exception cref="ArgumentException">Thrown when configPath is null or empty</exception>
    /// <exception cref="FileNotFoundException">Thrown when configuration file doesn't exist</exception>
    /// <exception cref="InvalidOperationException">Thrown when deserialization fails</exception>
    public static PipelineConfig LoadFromFile(string configPath)
    {
        if (string.IsNullOrWhiteSpace(configPath))
        {
            throw new ArgumentException("Configuration path cannot be empty", nameof(configPath));
        }

        if (!File.Exists(configPath))
        {
            throw new FileNotFoundException($"Configuration file not found: {configPath}");
        }

        var yaml = File.ReadAllText(configPath);
        var config = YamlDeserializer.Deserialize<PipelineConfig>(yaml);
        
        if (config == null)
        {
            throw new InvalidOperationException($"Failed to deserialize configuration from: {configPath}");
        }

        return config;
    }

    /// <summary>
    /// Load configuration from YAML file or use default
    /// </summary>
    /// <param name="configPath">Path to YAML configuration file (optional)</param>
    /// <returns>Loaded pipeline configuration or default</returns>
    public static PipelineConfig LoadOrDefault(string? configPath = null)
    {
        if (configPath != null && File.Exists(configPath))
        {
            return LoadFromFile(configPath);
        }

        // Return default configuration
        return new PipelineConfig();
    }

    /// <summary>
    /// Validate configuration
    /// </summary>
    /// <param name="config">Configuration to validate</param>
    /// <returns>List of validation errors (empty if valid)</returns>
    /// <exception cref="ArgumentNullException">Thrown when config is null</exception>
    public static List<string> Validate(PipelineConfig config)
    {
        if (config == null)
        {
            throw new ArgumentNullException(nameof(config));
        }

        var errors = new List<string>();

        // Validate paths
        if (string.IsNullOrWhiteSpace(config.Paths.StoryRoot))
        {
            errors.Add("Story root path cannot be empty");
        }

        if (string.IsNullOrWhiteSpace(config.Paths.PythonRoot))
        {
            errors.Add("Python root path cannot be empty");
        }

        // Validate generation settings
        if (config.Generation.Story.Count < 1)
        {
            errors.Add("Story count must be at least 1");
        }

        if (config.Generation.Story.TargetLength < 50)
        {
            errors.Add("Target script length must be at least 50 words");
        }

        // Validate video settings
        if (config.Generation.Video.Resolution.Width < 1 || config.Generation.Video.Resolution.Height < 1)
        {
            errors.Add("Video resolution must be positive");
        }

        if (config.Generation.Video.Fps < 1 || config.Generation.Video.Fps > 120)
        {
            errors.Add("Video FPS must be between 1 and 120");
        }

        // Validate processing settings
        if (config.Processing.Parallel.MaxWorkers < 1)
        {
            errors.Add("Max workers must be at least 1");
        }

        if (config.Processing.ErrorHandling.RetryCount < 0)
        {
            errors.Add("Retry count cannot be negative");
        }

        return errors;
    }
}
