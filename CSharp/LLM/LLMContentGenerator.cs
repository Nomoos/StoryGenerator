using System;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;

namespace StoryGenerator.Core.LLM
{
    /// <summary>
    /// LLM-based content generator implementation.
    /// Generates scripts, scene breakdowns, and video descriptions using LLMs.
    /// </summary>
    public class LLMContentGenerator : ILLMContentGenerator
    {
        private readonly ILLMModelProvider _modelProvider;
        private readonly string _modelName;

        /// <inheritdoc/>
        public string Name => "LLM Content Generator";

        /// <inheritdoc/>
        public string Version => "1.0.0";

        /// <inheritdoc/>
        public string ModelName => _modelName;

        /// <inheritdoc/>
        public string Provider => _modelProvider.ProviderName;

        /// <summary>
        /// Initializes a new instance of the LLMContentGenerator class.
        /// </summary>
        /// <param name="modelProvider">The LLM model provider to use.</param>
        /// <param name="modelName">The model name to use (optional, uses provider default if not specified).</param>
        public LLMContentGenerator(ILLMModelProvider modelProvider, string? modelName = null)
        {
            _modelProvider = modelProvider ?? throw new ArgumentNullException(nameof(modelProvider));
            _modelName = modelName ?? modelProvider.CurrentModel;
        }

        /// <inheritdoc/>
        public async Task<string> GenerateScriptAsync(
            IStoryIdea storyIdea,
            int targetLength = 360,
            float temperature = 0.7f,
            CancellationToken cancellationToken = default)
        {
            if (storyIdea == null)
            {
                throw new ArgumentNullException(nameof(storyIdea));
            }

            var systemPrompt = PromptTemplates.ScriptGenerationSystem;
            var userPrompt = PromptTemplates.FormatScriptPrompt(
                storyIdea.Title,
                storyIdea.Description,
                storyIdea.Tone ?? "engaging",
                targetLength
            );

            return await _modelProvider.GenerateAsync(
                _modelName,
                systemPrompt,
                userPrompt,
                temperature,
                maxTokens: targetLength * 2, // Rough estimate: 1 token ≈ 0.75 words
                cancellationToken
            );
        }

        /// <inheritdoc/>
        public async Task<string> GenerateSceneBreakdownAsync(
            string scriptText,
            float temperature = 0.5f,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(scriptText))
            {
                throw new ArgumentException("Script text cannot be empty", nameof(scriptText));
            }

            var systemPrompt = PromptTemplates.SceneBreakdownSystem;
            var userPrompt = PromptTemplates.FormatSceneBreakdownPrompt(scriptText, 60); // Default 60 seconds

            return await _modelProvider.GenerateAsync(
                _modelName,
                systemPrompt,
                userPrompt,
                temperature,
                cancellationToken: cancellationToken
            );
        }

        /// <inheritdoc/>
        public async Task<string> GenerateVideoDescriptionAsync(
            string sceneDescription,
            string mood,
            float temperature = 0.6f,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(sceneDescription))
            {
                throw new ArgumentException("Scene description cannot be empty", nameof(sceneDescription));
            }

            var systemPrompt = PromptTemplates.VideoDescriptionSystem;
            var userPrompt = PromptTemplates.FormatVideoDescriptionPrompt(sceneDescription, mood);

            return await _modelProvider.GenerateAsync(
                _modelName,
                systemPrompt,
                userPrompt,
                temperature,
                cancellationToken: cancellationToken
            );
        }

        /// <inheritdoc/>
        public async Task<string> GenerateAsync(
            string systemPrompt,
            string userPrompt,
            float temperature = 0.7f,
            int? maxTokens = null,
            CancellationToken cancellationToken = default)
        {
            if (string.IsNullOrWhiteSpace(userPrompt))
            {
                throw new ArgumentException("User prompt cannot be empty", nameof(userPrompt));
            }

            return await _modelProvider.GenerateAsync(
                _modelName,
                systemPrompt ?? string.Empty,
                userPrompt,
                temperature,
                maxTokens,
                cancellationToken
            );
        }
    }
}
