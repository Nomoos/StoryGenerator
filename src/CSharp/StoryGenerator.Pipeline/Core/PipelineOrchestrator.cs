using StoryGenerator.Pipeline.Config;
using StoryGenerator.Pipeline.Interfaces;
using StoryGenerator.Pipeline.Services;

namespace StoryGenerator.Pipeline.Core;

/// <summary>
/// Master orchestrator for the complete StoryGenerator pipeline.
/// Chains all steps from story idea to final video.
/// Refactored to follow SOLID principles with dependency injection.
/// </summary>
public class PipelineOrchestrator
{
    private readonly PipelineConfig _config;
    private readonly PipelineLogger _logger;
    private readonly IPythonExecutor _pythonExecutor;
    private readonly IPipelineCheckpointManager _checkpointManager;
    private readonly SceneAnalysisService _sceneAnalysisService;
    private readonly SceneDescriptionService _sceneDescriptionService;
    private readonly VideoGenerationService _videoGenerationService;
    private readonly VideoCompositionService _videoCompositionService;

    public PipelineOrchestrator(
        PipelineConfig config,
        PipelineLogger logger,
        IPythonExecutor pythonExecutor,
        IPipelineCheckpointManager checkpointManager)
    {
        _config = config ?? throw new ArgumentNullException(nameof(config));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _pythonExecutor = pythonExecutor ?? throw new ArgumentNullException(nameof(pythonExecutor));
        _checkpointManager = checkpointManager ?? throw new ArgumentNullException(nameof(checkpointManager));
        
        // Initialize video pipeline services
        _sceneAnalysisService = new SceneAnalysisService(_config.Paths);
        _sceneDescriptionService = new SceneDescriptionService(_config.Paths);
        _videoGenerationService = new VideoGenerationService(
            _config.Paths, 
            _config.Generation.Video, 
            useLTX: true); // Configure via config later
        _videoCompositionService = new VideoCompositionService(
            _config.Paths, 
            _config.Generation.Video);
    }

    /// <summary>
    /// Run the complete end-to-end pipeline
    /// </summary>
    /// <param name="storyTitle">Optional story title (generates new if not provided)</param>
    /// <returns>Path to final video output</returns>
    public async Task<string> RunFullPipelineAsync(string? storyTitle = null)
    {
        _logger.LogInfo($"Starting pipeline: {_config.Pipeline.Name}");
        _logger.LogInfo(new string('=', 80));

        var startTime = DateTime.Now;
        var checkpoint = await _checkpointManager.LoadCheckpointAsync();

        try
        {
            // Step 1: Generate Story Idea
            if (_config.Pipeline.Steps.StoryIdea && !checkpoint.IsStepComplete("story_idea"))
            {
                _logger.LogInfo("\n📝 STEP 1: Story Idea Generation");
                _logger.LogInfo(new string('-', 80));
                storyTitle = await GenerateStoryIdeaAsync();
                checkpoint.CompleteStep("story_idea", storyTitle);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 1: Story Idea (skipped)");
                storyTitle ??= checkpoint.GetStepData("story_idea");
            }

            if (string.IsNullOrEmpty(storyTitle))
            {
                throw new InvalidOperationException("Story title is required");
            }

            // Step 2: Generate Script
            if (_config.Pipeline.Steps.ScriptGeneration && !checkpoint.IsStepComplete("script_generation"))
            {
                _logger.LogInfo("\n📝 STEP 2: Script Generation");
                _logger.LogInfo(new string('-', 80));
                await GenerateScriptAsync(storyTitle);
                checkpoint.CompleteStep("script_generation", storyTitle);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 2: Script Generation (skipped)");
            }

            // Step 3: Revise Script
            if (_config.Pipeline.Steps.ScriptRevision && !checkpoint.IsStepComplete("script_revision"))
            {
                _logger.LogInfo("\n✏️ STEP 3: Script Revision");
                _logger.LogInfo(new string('-', 80));
                await ReviseScriptAsync(storyTitle);
                checkpoint.CompleteStep("script_revision", storyTitle);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 3: Script Revision (skipped)");
            }

            // Step 4: Enhance Script
            if (_config.Pipeline.Steps.ScriptEnhancement && !checkpoint.IsStepComplete("script_enhancement"))
            {
                _logger.LogInfo("\n🎭 STEP 4: Script Enhancement");
                _logger.LogInfo(new string('-', 80));
                await EnhanceScriptAsync(storyTitle);
                checkpoint.CompleteStep("script_enhancement", storyTitle);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 4: Script Enhancement (skipped)");
            }

            // Step 5: Generate Voice
            if (_config.Pipeline.Steps.VoiceSynthesis && !checkpoint.IsStepComplete("voice_synthesis"))
            {
                _logger.LogInfo("\n🎤 STEP 5: Voice Synthesis");
                _logger.LogInfo(new string('-', 80));
                await GenerateVoiceAsync(storyTitle);
                checkpoint.CompleteStep("voice_synthesis", storyTitle);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 5: Voice Synthesis (skipped)");
            }

            // Step 6: Generate Subtitles
            if (_config.Pipeline.Steps.AsrSubtitles && !checkpoint.IsStepComplete("asr_subtitles"))
            {
                _logger.LogInfo("\n💬 STEP 6: ASR & Subtitles");
                _logger.LogInfo(new string('-', 80));
                await GenerateSubtitlesAsync(storyTitle);
                checkpoint.CompleteStep("asr_subtitles", storyTitle);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 6: ASR & Subtitles (skipped)");
            }

            // Step 7: Analyze Scenes
            if (_config.Pipeline.Steps.SceneAnalysis && !checkpoint.IsStepComplete("scene_analysis"))
            {
                _logger.LogInfo("\n📊 STEP 7: Scene Analysis");
                _logger.LogInfo(new string('-', 80));
                await AnalyzeScenesAsync(storyTitle);
                checkpoint.CompleteStep("scene_analysis", storyTitle);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 7: Scene Analysis (skipped)");
            }

            // Step 8: Describe Scenes
            if (_config.Pipeline.Steps.SceneDescription && !checkpoint.IsStepComplete("scene_description"))
            {
                _logger.LogInfo("\n🎨 STEP 8: Scene Description");
                _logger.LogInfo(new string('-', 80));
                await DescribeScenesAsync(storyTitle);
                checkpoint.CompleteStep("scene_description", storyTitle);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 8: Scene Description (skipped)");
            }

            // Step 9: Generate Keyframes
            if (_config.Pipeline.Steps.KeyframeGeneration && !checkpoint.IsStepComplete("keyframe_generation"))
            {
                _logger.LogInfo("\n🖼️ STEP 9: Keyframe Generation");
                _logger.LogInfo(new string('-', 80));
                await GenerateKeyframesAsync(storyTitle);
                checkpoint.CompleteStep("keyframe_generation", storyTitle);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 9: Keyframe Generation (skipped)");
            }

            // Step 10: Video Interpolation
            if (_config.Pipeline.Steps.VideoInterpolation && !checkpoint.IsStepComplete("video_interpolation"))
            {
                _logger.LogInfo("\n🎬 STEP 10: Video Interpolation");
                _logger.LogInfo(new string('-', 80));
                await InterpolateVideoAsync(storyTitle);
                checkpoint.CompleteStep("video_interpolation", storyTitle);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 10: Video Interpolation (skipped)");
            }

            // Step 11: Compose Final Video
            if (_config.Pipeline.Steps.VideoComposition && !checkpoint.IsStepComplete("video_composition"))
            {
                _logger.LogInfo("\n🎥 STEP 11: Final Video Composition");
                _logger.LogInfo(new string('-', 80));
                var finalVideoPath = await ComposeVideoAsync(storyTitle);
                checkpoint.CompleteStep("video_composition", finalVideoPath);
                await _checkpointManager.SaveCheckpointAsync(checkpoint);
            }
            else
            {
                _logger.LogInfo("\n✅ STEP 11: Final Video Composition (skipped)");
            }

            var elapsed = DateTime.Now - startTime;
            _logger.LogInfo($"\n\n{new string('=', 80)}");
            _logger.LogInfo($"🎉 PIPELINE COMPLETE!");
            _logger.LogInfo($"{new string('=', 80)}");
            _logger.LogInfo($"Story: {storyTitle}");
            _logger.LogInfo($"Total time: {elapsed:hh\\:mm\\:ss}");
            _logger.LogInfo($"Output: {Path.Combine(_config.Paths.StoryRoot, _config.Paths.Final, storyTitle)}");

            // Cleanup checkpoint on success
            await _checkpointManager.DeleteCheckpointAsync();

            return Path.Combine(_config.Paths.StoryRoot, _config.Paths.Final, storyTitle);
        }
        catch (Exception ex)
        {
            _logger.LogError($"Pipeline failed: {ex.Message}");
            _logger.LogError($"Stack trace: {ex.StackTrace}");
            
            if (_config.Processing.Checkpointing.Enabled)
            {
                _logger.LogInfo("Checkpoint saved. Resume with: --resume");
            }
            
            throw;
        }
    }

    private async Task<string> GenerateStoryIdeaAsync()
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MIdea.py");
        var result = await _pythonExecutor.ExecuteScriptAsync(scriptPath, "");
        
        // Extract story title from output (assuming it's returned)
        // For now, use a placeholder
        return $"Story_{_config.Seeds.RandomSeed}";
    }

    private async Task GenerateScriptAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MScript.py");
        await _pythonExecutor.ExecuteScriptAsync(scriptPath, storyTitle);
    }

    private async Task ReviseScriptAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MRevise.py");
        await _pythonExecutor.ExecuteScriptAsync(scriptPath, storyTitle);
    }

    private async Task EnhanceScriptAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MEnhanceScript.py");
        await _pythonExecutor.ExecuteScriptAsync(scriptPath, storyTitle);
    }

    private async Task GenerateVoiceAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MVoice.py");
        await _pythonExecutor.ExecuteScriptAsync(scriptPath, storyTitle);
    }

    private async Task GenerateSubtitlesAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MTitles.py");
        await _pythonExecutor.ExecuteScriptAsync(scriptPath, storyTitle);
    }

    private async Task AnalyzeScenesAsync(string storyTitle)
    {
        await _sceneAnalysisService.AnalyzeScenesAsync(storyTitle);
    }

    private async Task DescribeScenesAsync(string storyTitle)
    {
        await _sceneDescriptionService.DescribeScenesAsync(storyTitle);
    }

    private async Task GenerateKeyframesAsync(string storyTitle)
    {
        // Keyframe generation is handled as part of video generation
        // This step can be skipped or used for pre-generating keyframes
        _logger.LogInfo("  (Keyframes will be generated during video synthesis)");
    }

    private async Task InterpolateVideoAsync(string storyTitle)
    {
        // Generate video clips using selected method
        await _videoGenerationService.GenerateVideoClipsAsync(storyTitle);
    }

    private async Task<string> ComposeVideoAsync(string storyTitle)
    {
        // Load generated clips
        var videoDir = Path.Combine(_config.Paths.StoryRoot, _config.Paths.Videos, storyTitle);
        var clipPaths = Directory.GetFiles(videoDir, "clip_*.mp4")
            .OrderBy(f => f)
            .ToList();

        if (clipPaths.Count == 0)
        {
            throw new InvalidOperationException($"No video clips found for {storyTitle}");
        }

        // Compose final video
        var finalVideoPath = await _videoCompositionService.ComposeVideoAsync(storyTitle, clipPaths);
        return finalVideoPath;
    }
}
