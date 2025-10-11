using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;
using System.Text.Json;

namespace StoryGenerator.Pipeline.Config;

/// <summary>
/// Loads pipeline orchestration configuration from YAML or JSON files
/// </summary>
public class PipelineOrchestrationConfigLoader
{
    private readonly IDeserializer _yamlDeserializer;
    private readonly JsonSerializerOptions _jsonOptions;

    public PipelineOrchestrationConfigLoader()
    {
        _yamlDeserializer = new DeserializerBuilder()
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .IgnoreUnmatchedProperties()
            .Build();

        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            AllowTrailingCommas = true,
            ReadCommentHandling = JsonCommentHandling.Skip
        };
    }

    /// <summary>
    /// Load configuration from a file (auto-detects YAML or JSON based on extension)
    /// </summary>
    public async Task<PipelineOrchestrationConfig> LoadFromFileAsync(string path)
    {
        if (!File.Exists(path))
        {
            throw new FileNotFoundException($"Configuration file not found: {path}");
        }

        var content = await File.ReadAllTextAsync(path);
        var extension = Path.GetExtension(path).ToLowerInvariant();

        return extension switch
        {
            ".yaml" or ".yml" => LoadFromYaml(content),
            ".json" => LoadFromJson(content),
            _ => throw new NotSupportedException($"Unsupported configuration file format: {extension}. Use .yaml, .yml, or .json")
        };
    }

    /// <summary>
    /// Load configuration from YAML string
    /// </summary>
    public PipelineOrchestrationConfig LoadFromYaml(string yaml)
    {
        // Replace environment variables
        yaml = ReplaceEnvironmentVariables(yaml);
        
        var config = _yamlDeserializer.Deserialize<PipelineOrchestrationConfig>(yaml);
        
        if (config == null)
        {
            throw new InvalidOperationException("Failed to deserialize YAML configuration");
        }

        return config;
    }

    /// <summary>
    /// Load configuration from JSON string
    /// </summary>
    public PipelineOrchestrationConfig LoadFromJson(string json)
    {
        // Replace environment variables
        json = ReplaceEnvironmentVariables(json);
        
        var config = JsonSerializer.Deserialize<PipelineOrchestrationConfig>(json, _jsonOptions);
        
        if (config == null)
        {
            throw new InvalidOperationException("Failed to deserialize JSON configuration");
        }

        return config;
    }

    /// <summary>
    /// Save configuration to a file
    /// </summary>
    public async Task SaveToFileAsync(PipelineOrchestrationConfig config, string path)
    {
        var extension = Path.GetExtension(path).ToLowerInvariant();
        
        var content = extension switch
        {
            ".yaml" or ".yml" => SerializeToYaml(config),
            ".json" => SerializeToJson(config),
            _ => throw new NotSupportedException($"Unsupported configuration file format: {extension}")
        };

        // Ensure directory exists
        var directory = Path.GetDirectoryName(path);
        if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
        {
            Directory.CreateDirectory(directory);
        }

        await File.WriteAllTextAsync(path, content);
    }

    /// <summary>
    /// Serialize configuration to YAML
    /// </summary>
    public string SerializeToYaml(PipelineOrchestrationConfig config)
    {
        var serializer = new SerializerBuilder()
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .Build();
        
        return serializer.Serialize(config);
    }

    /// <summary>
    /// Serialize configuration to JSON
    /// </summary>
    public string SerializeToJson(PipelineOrchestrationConfig config)
    {
        return JsonSerializer.Serialize(config, new JsonSerializerOptions
        {
            WriteIndented = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        });
    }

    /// <summary>
    /// Replace environment variable references in format ${VAR_NAME} or $VAR_NAME
    /// </summary>
    private static string ReplaceEnvironmentVariables(string content)
    {
        // Replace ${VAR_NAME} format
        var result = System.Text.RegularExpressions.Regex.Replace(
            content,
            @"\$\{([^}]+)\}",
            match =>
            {
                var varName = match.Groups[1].Value;
                return Environment.GetEnvironmentVariable(varName) ?? match.Value;
            });

        // Also support $VAR_NAME format (without braces) for simple cases
        result = System.Text.RegularExpressions.Regex.Replace(
            result,
            @"\$([A-Z_][A-Z0-9_]*)",
            match =>
            {
                var varName = match.Groups[1].Value;
                var value = Environment.GetEnvironmentVariable(varName);
                return value ?? match.Value;
            },
            System.Text.RegularExpressions.RegexOptions.Multiline);

        return result;
    }

    /// <summary>
    /// Validate configuration
    /// </summary>
    public static List<string> ValidateConfiguration(PipelineOrchestrationConfig config)
    {
        var errors = new List<string>();

        if (config.Stages.Count == 0)
        {
            errors.Add("Pipeline must have at least one stage");
        }

        var stageIds = new HashSet<string>();
        foreach (var stage in config.Stages)
        {
            if (string.IsNullOrWhiteSpace(stage.Id))
            {
                errors.Add("Stage ID cannot be empty");
            }
            else if (stageIds.Contains(stage.Id))
            {
                errors.Add($"Duplicate stage ID: {stage.Id}");
            }
            else
            {
                stageIds.Add(stage.Id);
            }

            if (stage.Order < 0)
            {
                errors.Add($"Stage '{stage.Id}' has invalid order: {stage.Order}");
            }

            if (stage.MaxRetries.HasValue && stage.MaxRetries.Value < 0)
            {
                errors.Add($"Stage '{stage.Id}' has invalid MaxRetries: {stage.MaxRetries}");
            }

            if (stage.RetryDelaySeconds.HasValue && stage.RetryDelaySeconds.Value < 0)
            {
                errors.Add($"Stage '{stage.Id}' has invalid RetryDelaySeconds: {stage.RetryDelaySeconds}");
            }

            if (stage.TimeoutSeconds < 0)
            {
                errors.Add($"Stage '{stage.Id}' has invalid TimeoutSeconds: {stage.TimeoutSeconds}");
            }
        }

        return errors;
    }
}
