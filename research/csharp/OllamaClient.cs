using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Research
{
    /// <summary>
    /// Client for interacting with Ollama local LLM service.
    /// Research prototype for local-only model orchestration.
    /// </summary>
    public class OllamaClient : IOllamaClient
    {
        private readonly string _model;
        private readonly string _baseUrl;

        /// <summary>
        /// Initialize Ollama client.
        /// </summary>
        /// <param name="model">Name of the Ollama model to use (e.g., "llama2", "mistral")</param>
        /// <param name="baseUrl">Base URL of the Ollama server</param>
        public OllamaClient(string model = "llama2", string baseUrl = "http://localhost:11434")
        {
            _model = model;
            _baseUrl = baseUrl;
        }

        /// <summary>
        /// Generate text using Ollama model via CLI.
        /// </summary>
        /// <param name="prompt">Input prompt</param>
        /// <param name="system">Optional system message</param>
        /// <param name="temperature">Sampling temperature (0.0-1.0)</param>
        /// <param name="maxTokens">Maximum tokens to generate</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Generated text</returns>
        public async Task<string> GenerateAsync(
            string prompt,
            string system = null,
            float temperature = 0.7f,
            int? maxTokens = null,
            CancellationToken cancellationToken = default)
        {
            // Build full prompt with system message if provided
            var fullPrompt = prompt;
            if (!string.IsNullOrEmpty(system))
            {
                fullPrompt = $"{system}\n\n{prompt}";
            }

            // Execute Ollama CLI
            var startInfo = new ProcessStartInfo
            {
                FileName = "ollama",
                Arguments = $"run {_model}",
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
                var output = await process.StandardOutput.ReadToEndAsync();
                var error = await process.StandardError.ReadToEndAsync();

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

        /// <summary>
        /// Chat completion using Ollama API format.
        /// </summary>
        /// <param name="messages">List of chat messages</param>
        /// <param name="temperature">Sampling temperature</param>
        /// <param name="maxTokens">Maximum tokens to generate</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Assistant's response</returns>
        public async Task<string> ChatAsync(
            List<ChatMessage> messages,
            float temperature = 0.7f,
            int? maxTokens = null,
            CancellationToken cancellationToken = default)
        {
            // Convert messages to single prompt for CLI
            var promptBuilder = new StringBuilder();
            string systemMessage = null;

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

            promptBuilder.Append("Assistant:");
            
            return await GenerateAsync(
                promptBuilder.ToString(),
                systemMessage,
                temperature,
                maxTokens,
                cancellationToken);
        }

        /// <summary>
        /// List available Ollama models.
        /// </summary>
        /// <returns>List of model names</returns>
        public async Task<List<string>> ListModelsAsync()
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
                var output = await process.StandardOutput.ReadToEndAsync();
                await process.WaitForExitAsync();

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
                throw new Exception($"Failed to list models: {ex.Message}", ex);
            }
        }

        /// <summary>
        /// Download an Ollama model.
        /// </summary>
        /// <param name="modelName">Name of the model to download</param>
        /// <returns>True if successful</returns>
        public async Task<bool> PullModelAsync(string modelName)
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
                await process.WaitForExitAsync();
                return process.ExitCode == 0;
            }
            catch
            {
                return false;
            }
        }
    }

    /// <summary>
    /// Represents a chat message.
    /// </summary>
    public class ChatMessage
    {
        public string Role { get; set; }
        public string Content { get; set; }

        public ChatMessage(string role, string content)
        {
            Role = role;
            Content = content;
        }
    }
}
