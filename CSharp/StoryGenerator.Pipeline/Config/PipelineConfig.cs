namespace StoryGenerator.Pipeline.Config;

/// <summary>
/// Root configuration for the StoryGenerator pipeline
/// </summary>
public class PipelineConfig
{
    public PipelineSettings Pipeline { get; set; } = new();
    public PathsConfig Paths { get; set; } = new();
    public GenerationConfig Generation { get; set; } = new();
    public ModelsConfig Models { get; set; } = new();
    public ProcessingConfig Processing { get; set; } = new();
    public OutputConfig Output { get; set; } = new();
    public LoggingConfig Logging { get; set; } = new();
    public SeedsConfig Seeds { get; set; } = new();
}

public class PipelineSettings
{
    public string Name { get; set; } = "StoryGenerator Full Pipeline";
    public PipelineSteps Steps { get; set; } = new();
}

public class PipelineSteps
{
    public bool StoryIdea { get; set; } = true;
    public bool ScriptGeneration { get; set; } = true;
    public bool ScriptRevision { get; set; } = true;
    public bool ScriptEnhancement { get; set; } = true;
    public bool VoiceSynthesis { get; set; } = true;
    public bool AsrSubtitles { get; set; } = true;
    public bool SceneAnalysis { get; set; } = true;
    public bool SceneDescription { get; set; } = true;
    public bool KeyframeGeneration { get; set; } = true;
    public bool VideoInterpolation { get; set; } = true;
    public bool VideoComposition { get; set; } = true;
}

public class PathsConfig
{
    public string StoryRoot { get; set; } = "./Stories";
    public string Ideas { get; set; } = "0_Ideas";
    public string Scripts { get; set; } = "1_Scripts";
    public string Revised { get; set; } = "2_Revised";
    public string Voiceover { get; set; } = "3_VoiceOver";
    public string Titles { get; set; } = "4_Titles";
    public string Scenes { get; set; } = "scenes";
    public string Images { get; set; } = "images";
    public string Videos { get; set; } = "videos";
    public string Final { get; set; } = "final";
    public string PythonRoot { get; set; } = "./Python";
    public string Resources { get; set; } = "./resources";
    public string BackgroundImage { get; set; } = "./resources/background.jpg";
}

public class GenerationConfig
{
    public StoryConfig Story { get; set; } = new();
    public VoiceConfig Voice { get; set; } = new();
    public VideoConfig Video { get; set; } = new();
    public ImageConfig Image { get; set; } = new();
    public SceneConfig Scene { get; set; } = new();
}

public class StoryConfig
{
    public int Count { get; set; } = 1;
    public string Tone { get; set; } = "emotional";
    public string Theme { get; set; } = "friendship";
    public int TargetLength { get; set; } = 360;
}

public class VoiceConfig
{
    public string Model { get; set; } = "eleven_v3";
    public string VoiceId { get; set; } = "BZgkqPqms7Kj9ulSkVzn";
    public double Stability { get; set; } = 0.5;
    public double SimilarityBoost { get; set; } = 0.75;
    public bool NormalizeAudio { get; set; } = true;
    public double TargetLufs { get; set; } = -14.0;
}

public class VideoConfig
{
    public Resolution Resolution { get; set; } = new();
    public int Fps { get; set; } = 30;
    public string Codec { get; set; } = "libx264";
    public string AudioCodec { get; set; } = "aac";
    public string Bitrate { get; set; } = "8M";
    public string Quality { get; set; } = "high";
}

public class Resolution
{
    public int Width { get; set; } = 1080;
    public int Height { get; set; } = 1920;
}

public class ImageConfig
{
    public string Model { get; set; } = "stabilityai/stable-diffusion-xl-base-1.0";
    public int NumInferenceSteps { get; set; } = 30;
    public double GuidanceScale { get; set; } = 7.5;
    public bool UseGpu { get; set; } = true;
    public int BatchSize { get; set; } = 1;
}

public class SceneConfig
{
    public double MinDuration { get; set; } = 3.0;
    public double MaxDuration { get; set; } = 10.0;
    public double TransitionDuration { get; set; } = 0.5;
}

public class ModelsConfig
{
    public OpenAIConfig OpenAI { get; set; } = new();
    public ElevenLabsConfig ElevenLabs { get; set; } = new();
    public WhisperConfig Whisper { get; set; } = new();
}

public class OpenAIConfig
{
    public string Model { get; set; } = "gpt-4o-mini";
    public double Temperature { get; set; } = 0.9;
    public int MaxTokens { get; set; } = 1000;
    public string ApiKeyEnv { get; set; } = "OPENAI_API_KEY";
}

public class ElevenLabsConfig
{
    public string ApiKeyEnv { get; set; } = "ELEVENLABS_API_KEY";
}

public class WhisperConfig
{
    public string ModelSize { get; set; } = "large-v2";
    public string Language { get; set; } = "en";
    public string Device { get; set; } = "cuda";
}

public class ProcessingConfig
{
    public ParallelConfig Parallel { get; set; } = new();
    public ErrorHandlingConfig ErrorHandling { get; set; } = new();
    public CheckpointingConfig Checkpointing { get; set; } = new();
    public CachingConfig Caching { get; set; } = new();
}

public class ParallelConfig
{
    public bool Enabled { get; set; } = false;
    public int MaxWorkers { get; set; } = 2;
}

public class ErrorHandlingConfig
{
    public bool ContinueOnError { get; set; } = true;
    public int RetryCount { get; set; } = 3;
    public int RetryDelay { get; set; } = 5;
}

public class CheckpointingConfig
{
    public bool Enabled { get; set; } = true;
    public bool ResumeFromCheckpoint { get; set; } = true;
}

public class CachingConfig
{
    public bool SkipExisting { get; set; } = true;
    public bool ForceRegenerate { get; set; } = false;
}

public class OutputConfig
{
    public NamingConfig Naming { get; set; } = new();
    public MetadataConfig Metadata { get; set; } = new();
    public ThumbnailsConfig Thumbnails { get; set; } = new();
    public CleanupConfig Cleanup { get; set; } = new();
}

public class NamingConfig
{
    public bool UseSanitizedNames { get; set; } = true;
    public bool IncludeTimestamp { get; set; } = false;
}

public class MetadataConfig
{
    public bool EmbedInVideo { get; set; } = true;
    public bool SaveJson { get; set; } = true;
}

public class ThumbnailsConfig
{
    public bool Generate { get; set; } = true;
    public int Width { get; set; } = 1080;
    public int Height { get; set; } = 1920;
    public double Timestamp { get; set; } = 0.5;
}

public class CleanupConfig
{
    public bool RemoveIntermediates { get; set; } = false;
    public bool KeepFailed { get; set; } = true;
}

public class LoggingConfig
{
    public string Level { get; set; } = "INFO";
    public string File { get; set; } = "pipeline.log";
    public bool Console { get; set; } = true;
    public string Format { get; set; } = "[{timestamp}] {level}: {message}";
}

public class SeedsConfig
{
    public int RandomSeed { get; set; } = 42;
    public int ImageSeed { get; set; } = 12345;
    public bool UseSeeds { get; set; } = false;
}
