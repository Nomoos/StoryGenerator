using System.Diagnostics;
using System.Text;
using StoryGenerator.Pipeline.Config;

namespace StoryGenerator.Pipeline.Core;

/// <summary>
/// Master orchestrator for the complete StoryGenerator pipeline
/// Chains all steps from story idea to final video
/// </summary>
public class PipelineOrchestrator
{
    private readonly PipelineConfig _config;
    private readonly PipelineLogger _logger;
    private readonly string _pythonExecutable;

    public PipelineOrchestrator(PipelineConfig config)
    {
        _config = config;
        _logger = new PipelineLogger(config.Logging);
        _pythonExecutable = FindPythonExecutable();
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
        var checkpointFile = Path.Combine(_config.Paths.StoryRoot, "pipeline_checkpoint.json");
        var checkpoint = LoadCheckpoint(checkpointFile);

        try
        {
            // Step 1: Generate Story Idea
            if (_config.Pipeline.Steps.StoryIdea && !checkpoint.IsStepComplete("story_idea"))
            {
                _logger.LogInfo("\n📝 STEP 1: Story Idea Generation");
                _logger.LogInfo(new string('-', 80));
                storyTitle = await GenerateStoryIdeaAsync();
                checkpoint.CompleteStep("story_idea", storyTitle);
                SaveCheckpoint(checkpointFile, checkpoint);
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
                SaveCheckpoint(checkpointFile, checkpoint);
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
                SaveCheckpoint(checkpointFile, checkpoint);
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
                SaveCheckpoint(checkpointFile, checkpoint);
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
                SaveCheckpoint(checkpointFile, checkpoint);
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
                SaveCheckpoint(checkpointFile, checkpoint);
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
                SaveCheckpoint(checkpointFile, checkpoint);
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
                SaveCheckpoint(checkpointFile, checkpoint);
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
                SaveCheckpoint(checkpointFile, checkpoint);
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
                SaveCheckpoint(checkpointFile, checkpoint);
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
                SaveCheckpoint(checkpointFile, checkpoint);
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
            if (File.Exists(checkpointFile))
            {
                File.Delete(checkpointFile);
            }

            return Path.Combine(_config.Paths.StoryRoot, _config.Paths.Final, storyTitle);
        }
        catch (Exception ex)
        {
            _logger.LogError($"Pipeline failed: {ex.Message}");
            _logger.LogError($"Stack trace: {ex.StackTrace}");
            
            if (_config.Processing.Checkpointing.Enabled)
            {
                _logger.LogInfo($"Checkpoint saved to: {checkpointFile}");
                _logger.LogInfo("Resume with: --resume");
            }
            
            throw;
        }
    }

    private async Task<string> GenerateStoryIdeaAsync()
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MIdea.py");
        var result = await ExecutePythonScriptAsync(scriptPath, "");
        
        // Extract story title from output (assuming it's returned)
        // For now, use a placeholder
        return $"Story_{_config.Seeds.RandomSeed}";
    }

    private async Task GenerateScriptAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MScript.py");
        await ExecutePythonScriptAsync(scriptPath, storyTitle);
    }

    private async Task ReviseScriptAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MRevise.py");
        await ExecutePythonScriptAsync(scriptPath, storyTitle);
    }

    private async Task EnhanceScriptAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MEnhanceScript.py");
        await ExecutePythonScriptAsync(scriptPath, storyTitle);
    }

    private async Task GenerateVoiceAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MVoice.py");
        await ExecutePythonScriptAsync(scriptPath, storyTitle);
    }

    private async Task GenerateSubtitlesAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MTitles.py");
        await ExecutePythonScriptAsync(scriptPath, storyTitle);
    }

    private async Task AnalyzeScenesAsync(string storyTitle)
    {
        // Call Python scene analyzer
        var args = $"-c \"from Generators.GSceneAnalyzer import SceneAnalyzer; from Models.StoryIdea import StoryIdea; analyzer = SceneAnalyzer(); idea = StoryIdea(story_title='{storyTitle}'); analyzer.analyze_story(idea)\"";
        await ExecutePythonCommandAsync(args);
    }

    private async Task DescribeScenesAsync(string storyTitle)
    {
        var args = $"-c \"from Generators.GSceneDescriber import SceneDescriber; from Models.StoryIdea import StoryIdea; describer = SceneDescriber(); idea = StoryIdea(story_title='{storyTitle}'); describer.describe_scenes(idea)\"";
        await ExecutePythonCommandAsync(args);
    }

    private async Task GenerateKeyframesAsync(string storyTitle)
    {
        var args = $"-c \"from Generators.GKeyframeGenerator import KeyframeGenerator; from Models.StoryIdea import StoryIdea; generator = KeyframeGenerator(); idea = StoryIdea(story_title='{storyTitle}'); generator.generate_keyframes(idea)\"";
        await ExecutePythonCommandAsync(args);
    }

    private async Task InterpolateVideoAsync(string storyTitle)
    {
        var args = $"-c \"from Generators.GVideoInterpolator import VideoInterpolator; from Models.StoryIdea import StoryIdea; interpolator = VideoInterpolator(); idea = StoryIdea(story_title='{storyTitle}'); interpolator.interpolate_scenes(idea)\"";
        await ExecutePythonCommandAsync(args);
    }

    private async Task<string> ComposeVideoAsync(string storyTitle)
    {
        var scriptPath = Path.Combine(_config.Paths.PythonRoot, "Generation", "Manual", "MVideoPipeline.py");
        await ExecutePythonScriptAsync(scriptPath, storyTitle);
        return Path.Combine(_config.Paths.StoryRoot, _config.Paths.Final, $"{storyTitle}.mp4");
    }

    private async Task<string> ExecutePythonScriptAsync(string scriptPath, string args)
    {
        if (!File.Exists(scriptPath))
        {
            throw new FileNotFoundException($"Python script not found: {scriptPath}");
        }

        var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = _pythonExecutable,
                Arguments = $"\"{scriptPath}\" {args}",
                WorkingDirectory = _config.Paths.PythonRoot,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            }
        };

        var outputBuilder = new StringBuilder();
        var errorBuilder = new StringBuilder();

        process.OutputDataReceived += (sender, e) =>
        {
            if (!string.IsNullOrEmpty(e.Data))
            {
                outputBuilder.AppendLine(e.Data);
                _logger.LogInfo($"  {e.Data}");
            }
        };

        process.ErrorDataReceived += (sender, e) =>
        {
            if (!string.IsNullOrEmpty(e.Data))
            {
                errorBuilder.AppendLine(e.Data);
                _logger.LogWarning($"  {e.Data}");
            }
        };

        _logger.LogDebug($"Executing: {_pythonExecutable} {scriptPath} {args}");
        
        process.Start();
        process.BeginOutputReadLine();
        process.BeginErrorReadLine();
        
        await process.WaitForExitAsync();

        if (process.ExitCode != 0 && !_config.Processing.ErrorHandling.ContinueOnError)
        {
            var errorMessage = errorBuilder.ToString();
            throw new InvalidOperationException($"Python script failed with exit code {process.ExitCode}\n{errorMessage}");
        }

        return outputBuilder.ToString();
    }

    private async Task<string> ExecutePythonCommandAsync(string args)
    {
        var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = _pythonExecutable,
                Arguments = args,
                WorkingDirectory = _config.Paths.PythonRoot,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            }
        };

        var outputBuilder = new StringBuilder();
        var errorBuilder = new StringBuilder();

        process.OutputDataReceived += (sender, e) =>
        {
            if (!string.IsNullOrEmpty(e.Data))
            {
                outputBuilder.AppendLine(e.Data);
                _logger.LogInfo($"  {e.Data}");
            }
        };

        process.ErrorDataReceived += (sender, e) =>
        {
            if (!string.IsNullOrEmpty(e.Data))
            {
                errorBuilder.AppendLine(e.Data);
                _logger.LogWarning($"  {e.Data}");
            }
        };

        _logger.LogDebug($"Executing: {_pythonExecutable} {args}");
        
        process.Start();
        process.BeginOutputReadLine();
        process.BeginErrorReadLine();
        
        await process.WaitForExitAsync();

        if (process.ExitCode != 0 && !_config.Processing.ErrorHandling.ContinueOnError)
        {
            var errorMessage = errorBuilder.ToString();
            throw new InvalidOperationException($"Python command failed with exit code {process.ExitCode}\n{errorMessage}");
        }

        return outputBuilder.ToString();
    }

    private string FindPythonExecutable()
    {
        var candidates = new[] { "python3", "python", "py" };
        
        foreach (var candidate in candidates)
        {
            try
            {
                var process = Process.Start(new ProcessStartInfo
                {
                    FileName = candidate,
                    Arguments = "--version",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    CreateNoWindow = true
                });

                if (process != null)
                {
                    process.WaitForExit();
                    if (process.ExitCode == 0)
                    {
                        _logger.LogDebug($"Found Python executable: {candidate}");
                        return candidate;
                    }
                }
            }
            catch
            {
                // Try next candidate
            }
        }

        throw new InvalidOperationException("Python executable not found. Please ensure Python is installed and in PATH.");
    }

    private PipelineCheckpoint LoadCheckpoint(string checkpointFile)
    {
        if (!_config.Processing.Checkpointing.Enabled || !_config.Processing.Checkpointing.ResumeFromCheckpoint)
        {
            return new PipelineCheckpoint();
        }

        if (!File.Exists(checkpointFile))
        {
            return new PipelineCheckpoint();
        }

        try
        {
            var json = File.ReadAllText(checkpointFile);
            return System.Text.Json.JsonSerializer.Deserialize<PipelineCheckpoint>(json) ?? new PipelineCheckpoint();
        }
        catch (Exception ex)
        {
            _logger.LogWarning($"Failed to load checkpoint: {ex.Message}");
            return new PipelineCheckpoint();
        }
    }

    private void SaveCheckpoint(string checkpointFile, PipelineCheckpoint checkpoint)
    {
        if (!_config.Processing.Checkpointing.Enabled)
        {
            return;
        }

        try
        {
            var json = System.Text.Json.JsonSerializer.Serialize(checkpoint, new System.Text.Json.JsonSerializerOptions 
            { 
                WriteIndented = true 
            });
            File.WriteAllText(checkpointFile, json);
        }
        catch (Exception ex)
        {
            _logger.LogWarning($"Failed to save checkpoint: {ex.Message}");
        }
    }
}
