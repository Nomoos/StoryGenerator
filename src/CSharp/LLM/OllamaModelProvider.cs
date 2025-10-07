using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;

namespace StoryGenerator.Core.LLM
{
    /// <summary>
    /// Ollama-based LLM model provider implementation.
    /// Uses Ollama CLI for local model inference.
    /// </summary>
    public class OllamaModelProvider : ILLMModelProvider
    {
        private readonly string _defaultModel;
        private readonly string _baseUrl;

        /// <inheritdoc/>
        public string ProviderName => "Ollama";

        /// <inheritdoc/>
        public string CurrentModel => _defaultModel;

        /// <inheritdoc/>
        public string? BaseUrl { get; set; }

        /// <summary>
        /// Initializes a new instance of the OllamaModelProvider class.
        /// </summary>
        /// <param name="defaultModel">Default model to use (e.g., "qwen2.5:14b-instruct").</param>
        /// <param name="baseUrl">Base URL for Ollama server (default: http://localhost:11434).</param>
        public OllamaModelProvider(string defaultModel = "qwen2.5:14b-instruct", string baseUrl = "http://localhost:11434")
        {
            _defaultModel = defaultModel;
            _baseUrl = baseUrl;
            BaseUrl = baseUrl;
        }

        /// <inheritdoc/>
        public async Task<List<string>> ListAvailableModelsAsync(CancellationToken cancellationToken = default)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = "ollama",
                Arguments = "list",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = startInfo };
            
            try
            {
                process.Start();
                var output = await process.StandardOutput.ReadToEndAsync(cancellationToken);
                await process.WaitForExitAsync(cancellationToken);

                if (process.ExitCode != 0)
                {
                    return new List<string>();
                }

                var models = new List<string>();
                var lines = output.Split('\n', StringSplitOptions.RemoveEmptyEntries);
                
                // Skip header line
                for (int i = 1; i < lines.Length; i++)
                {
                    var parts = lines[i].Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
                    if (parts.Length > 0)
                    {
                        models.Add(parts[0]);
                    }
                }

                return models;
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to list Ollama models: {ex.Message}", ex);
            }
        }

        /// <inheritdoc/>
        public async Task<bool> IsModelAvailableAsync(string modelName, CancellationToken cancellationToken = default)
        {
            var models = await ListAvailableModelsAsync(cancellationToken);
            return models.Any(m => m.Equals(modelName, StringComparison.OrdinalIgnoreCase));
        }

        /// <inheritdoc/>
        public async Task<bool> PullModelAsync(string modelName, CancellationToken cancellationToken = default)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = "ollama",
                Arguments = $"pull {modelName}",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = startInfo };
            
            try
            {
                process.Start();
                await process.WaitForExitAsync(cancellationToken);
                return process.ExitCode == 0;
            }
            catch
            {
                return false;
            }
        }

        /// <inheritdoc/>
        public async Task<string> GenerateAsync(
            string modelName,
            string systemPrompt,
            string userPrompt,
            float temperature = 0.7f,
            int? maxTokens = null,
            CancellationToken cancellationToken = default)
        {
            var messages = new List<ChatMessage>
            {
                new ChatMessage("system", systemPrompt),
                new ChatMessage("user", userPrompt)
            };

            return await ChatAsync(modelName, messages, temperature, maxTokens, cancellationToken);
        }

        /// <inheritdoc/>
        public async Task<string> ChatAsync(
            string modelName,
            List<ChatMessage> messages,
            float temperature = 0.7f,
            int? maxTokens = null,
            CancellationToken cancellationToken = default)
        {
            // Build prompt from messages
            var promptBuilder = new StringBuilder();
            string? systemMessage = null;

            foreach (var message in messages)
            {
                switch (message.Role.ToLower())
                {
                    case "system":
                        systemMessage = message.Content;
                        break;
                    case "user":
                        promptBuilder.AppendLine($"User: {message.Content}");
                        break;
                    case "assistant":
                        promptBuilder.AppendLine($"Assistant: {message.Content}");
                        break;
                }
            }

            if (!string.IsNullOrEmpty(systemMessage))
            {
                promptBuilder.Insert(0, $"{systemMessage}\n\n");
            }

            promptBuilder.Append("Assistant:");
            var fullPrompt = promptBuilder.ToString();

            // Execute Ollama CLI
            var arguments = $"run {modelName}";
            if (maxTokens.HasValue)
            {
                arguments += $" --num-predict {maxTokens.Value}";
            }

            var startInfo = new ProcessStartInfo
            {
                FileName = "ollama",
                Arguments = arguments,
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = startInfo };
            
            try
            {
                process.Start();

                // Write prompt to stdin
                await process.StandardInput.WriteAsync(fullPrompt);
                await process.StandardInput.FlushAsync();
                process.StandardInput.Close();

                // Read output
                var output = await process.StandardOutput.ReadToEndAsync(cancellationToken);
                var error = await process.StandardError.ReadToEndAsync(cancellationToken);

                await process.WaitForExitAsync(cancellationToken);

                if (process.ExitCode != 0)
                {
                    throw new Exception($"Ollama CLI error: {error}");
                }

                return output.Trim();
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to execute Ollama: {ex.Message}", ex);
            }
        }

        /// <inheritdoc/>
        public async Task<ModelInfo> GetModelInfoAsync(string modelName, CancellationToken cancellationToken = default)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = "ollama",
                Arguments = $"show {modelName}",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = startInfo };
            
            try
            {
                process.Start();
                var output = await process.StandardOutput.ReadToEndAsync(cancellationToken);
                await process.WaitForExitAsync(cancellationToken);

                if (process.ExitCode != 0)
                {
                    throw new Exception($"Model {modelName} not found");
                }

                // Parse basic info from model name
                var info = new ModelInfo
                {
                    Name = modelName,
                    Family = ExtractModelFamily(modelName),
                    ParameterSize = ExtractParameterSize(modelName),
                    Quantization = ExtractQuantization(modelName),
                    IsInstructionTuned = modelName.ToLower().Contains("instruct"),
                    ContextLength = 4096 // Default, could be parsed from output
                };

                return info;
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to get model info: {ex.Message}", ex);
            }
        }

        private static string ExtractModelFamily(string modelName)
        {
            var parts = modelName.Split(':', '-', '_');
            return parts.Length > 0 ? parts[0] : modelName;
        }

        private static string ExtractParameterSize(string modelName)
        {
            var match = System.Text.RegularExpressions.Regex.Match(modelName, @"(\d+[bB])");
            return match.Success ? match.Value.ToUpper() : "Unknown";
        }

        private static string ExtractQuantization(string modelName)
        {
            var match = System.Text.RegularExpressions.Regex.Match(modelName, @"(q\d+_[kKmM]_[mM]|fp\d+)", System.Text.RegularExpressions.RegexOptions.IgnoreCase);
            return match.Success ? match.Value.ToUpper() : "Unknown";
        }
    }
}
