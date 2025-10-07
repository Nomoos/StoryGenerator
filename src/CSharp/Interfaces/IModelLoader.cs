using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Core.Interfaces
{
    /// <summary>
    /// Interface for managing and loading AI models.
    /// Handles model downloading, verification, and initialization.
    /// </summary>
    public interface IModelLoader
    {
        /// <summary>
        /// Download a model from Hugging Face or other sources.
        /// </summary>
        /// <param name="modelName">Model identifier (e.g., "Systran/faster-whisper-large-v3")</param>
        /// <param name="destination">Local path to save the model</param>
        /// <param name="progressCallback">Optional callback for download progress (0.0-1.0)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Path to the downloaded model</returns>
        Task<string> DownloadModelAsync(
            string modelName,
            string destination,
            Action<double>? progressCallback = null,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Verify that a model is correctly downloaded and not corrupted.
        /// </summary>
        /// <param name="modelPath">Path to the model</param>
        /// <returns>Verification result</returns>
        Task<ModelVerificationResult> VerifyModelAsync(string modelPath);

        /// <summary>
        /// Load a model into memory and prepare it for inference.
        /// </summary>
        /// <param name="modelPath">Path to the model</param>
        /// <param name="device">Device to load on ("cuda", "cpu", "auto")</param>
        /// <param name="computeType">Compute type ("float16", "int8", "auto")</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Model handle or identifier</returns>
        Task<string> LoadModelAsync(
            string modelPath,
            string device = "auto",
            string computeType = "auto",
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Unload a model from memory.
        /// </summary>
        /// <param name="modelHandle">Model handle returned from LoadModelAsync</param>
        /// <returns>True if successfully unloaded</returns>
        Task<bool> UnloadModelAsync(string modelHandle);

        /// <summary>
        /// Get information about a loaded model.
        /// </summary>
        /// <param name="modelHandle">Model handle</param>
        /// <returns>Model information</returns>
        Task<ModelInfo> GetModelInfoAsync(string modelHandle);

        /// <summary>
        /// List all downloaded models in the cache.
        /// </summary>
        /// <returns>List of cached models with their information</returns>
        Task<List<CachedModelInfo>> ListCachedModelsAsync();

        /// <summary>
        /// Remove a cached model from disk.
        /// </summary>
        /// <param name="modelName">Model identifier</param>
        /// <returns>True if successfully removed</returns>
        Task<bool> RemoveCachedModelAsync(string modelName);
    }

    /// <summary>
    /// Interface for managing model configurations and settings.
    /// </summary>
    public interface IModelConfiguration
    {
        /// <summary>
        /// Load model configuration from file.
        /// </summary>
        /// <param name="configPath">Path to configuration file (JSON or YAML)</param>
        /// <returns>Loaded configuration</returns>
        Task<ModelConfig> LoadConfigurationAsync(string configPath);

        /// <summary>
        /// Save model configuration to file.
        /// </summary>
        /// <param name="config">Configuration to save</param>
        /// <param name="configPath">Path to save configuration</param>
        /// <returns>True if successfully saved</returns>
        Task<bool> SaveConfigurationAsync(ModelConfig config, string configPath);

        /// <summary>
        /// Get default configuration for a specific model type.
        /// </summary>
        /// <param name="modelType">Type of model (e.g., "speech-recognition", "text-generation")</param>
        /// <returns>Default configuration</returns>
        ModelConfig GetDefaultConfiguration(string modelType);

        /// <summary>
        /// Validate a model configuration.
        /// </summary>
        /// <param name="config">Configuration to validate</param>
        /// <returns>Validation result</returns>
        Task<ConfigurationValidationResult> ValidateConfigurationAsync(ModelConfig config);
    }

    /// <summary>
    /// Result of model verification.
    /// </summary>
    public class ModelVerificationResult
    {
        /// <summary>
        /// Whether the model passed verification.
        /// </summary>
        public bool IsValid { get; set; }

        /// <summary>
        /// Verification message or error details.
        /// </summary>
        public string Message { get; set; } = string.Empty;

        /// <summary>
        /// Model size in bytes.
        /// </summary>
        public long SizeBytes { get; set; }

        /// <summary>
        /// Checksum or hash of the model (if available).
        /// </summary>
        public string? Checksum { get; set; }

        /// <summary>
        /// List of files found in the model directory.
        /// </summary>
        public List<string> Files { get; set; } = new();
    }

    /// <summary>
    /// Information about a cached model.
    /// </summary>
    public class CachedModelInfo
    {
        /// <summary>
        /// Model identifier (e.g., "Systran/faster-whisper-large-v3").
        /// </summary>
        public string ModelName { get; set; } = string.Empty;

        /// <summary>
        /// Local path to the cached model.
        /// </summary>
        public string LocalPath { get; set; } = string.Empty;

        /// <summary>
        /// Model size in bytes.
        /// </summary>
        public long SizeBytes { get; set; }

        /// <summary>
        /// When the model was downloaded.
        /// </summary>
        public DateTime DownloadedAt { get; set; }

        /// <summary>
        /// Last time the model was accessed.
        /// </summary>
        public DateTime LastAccessedAt { get; set; }

        /// <summary>
        /// Model version or commit hash.
        /// </summary>
        public string? Version { get; set; }

        /// <summary>
        /// Model type (e.g., "speech-recognition", "text-generation").
        /// </summary>
        public string? ModelType { get; set; }
    }

    /// <summary>
    /// Model configuration settings.
    /// </summary>
    public class ModelConfig
    {
        /// <summary>
        /// Model identifier or path.
        /// </summary>
        public string ModelName { get; set; } = string.Empty;

        /// <summary>
        /// Model type (e.g., "speech-recognition", "text-generation", "image-generation").
        /// </summary>
        public string ModelType { get; set; } = string.Empty;

        /// <summary>
        /// Device to run on ("cuda", "cpu", "auto").
        /// </summary>
        public string Device { get; set; } = "auto";

        /// <summary>
        /// Compute type ("float16", "float32", "int8", "auto").
        /// </summary>
        public string ComputeType { get; set; } = "auto";

        /// <summary>
        /// Maximum batch size for inference.
        /// </summary>
        public int? BatchSize { get; set; }

        /// <summary>
        /// Additional model-specific parameters.
        /// </summary>
        public Dictionary<string, object> Parameters { get; set; } = new();

        /// <summary>
        /// Whether to enable automatic mixed precision.
        /// </summary>
        public bool EnableAMP { get; set; } = true;

        /// <summary>
        /// Whether to use Flash Attention if available.
        /// </summary>
        public bool UseFlashAttention { get; set; } = false;

        /// <summary>
        /// Memory optimization level (0-3, higher = more optimization).
        /// </summary>
        public int MemoryOptimizationLevel { get; set; } = 1;
    }

    /// <summary>
    /// Result of configuration validation.
    /// </summary>
    public class ConfigurationValidationResult
    {
        /// <summary>
        /// Whether the configuration is valid.
        /// </summary>
        public bool IsValid { get; set; }

        /// <summary>
        /// Validation errors (if any).
        /// </summary>
        public List<string> Errors { get; set; } = new();

        /// <summary>
        /// Validation warnings (if any).
        /// </summary>
        public List<string> Warnings { get; set; } = new();

        /// <summary>
        /// Estimated VRAM usage in GB.
        /// </summary>
        public double? EstimatedVRAMGB { get; set; }

        /// <summary>
        /// Recommended settings based on available hardware.
        /// </summary>
        public Dictionary<string, string> Recommendations { get; set; } = new();
    }
}
