# StoryGenerator Pipeline - C# Orchestrator

A master orchestrator written in C# that chains all steps of the StoryGenerator pipeline from story idea to final video output.

## Features

- ✅ **One-Click Execution**: Run the complete pipeline with a single command
- ✅ **YAML Configuration**: Flexible configuration via YAML files
- ✅ **Checkpointing**: Resume from last successful step on failure
- ✅ **Error Handling**: Continue on non-critical errors with retry logic
- ✅ **Logging**: Comprehensive logging to console and file
- ✅ **Python Integration**: Seamlessly calls existing Python generators
- ✅ **Configurable Steps**: Enable/disable specific pipeline steps
- ✅ **Progress Tracking**: Real-time progress updates

## Pipeline Steps

The orchestrator executes the following steps in order:

1. **Story Idea Generation** - Generate creative story concepts
2. **Script Generation** - Create initial scripts (~360 words)
3. **Script Revision** - Refine scripts for voice clarity
4. **Script Enhancement** - Add voice performance tags
5. **Voice Synthesis** - Generate voiceover audio (ElevenLabs)
6. **ASR & Subtitles** - Generate word-level subtitles (WhisperX)
7. **Scene Analysis** - Analyze scenes from subtitles
8. **Scene Description** - Generate visual descriptions
9. **Keyframe Generation** - Create keyframe images (Stable Diffusion)
10. **Video Interpolation** - Interpolate between keyframes
11. **Final Composition** - Compose final video with audio and subtitles

## Prerequisites

- .NET 8.0 SDK or later
- Python 3.8+ with StoryGenerator dependencies installed
- OpenAI API key (for script generation)
- ElevenLabs API key (for voice generation)
- CUDA-capable GPU (optional, for faster image generation)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator/CSharp/StoryGenerator.Pipeline
```

### 2. Build the Project

```bash
dotnet build
```

### 3. Set Up Configuration

Copy the example configuration file:

```bash
cp ../../config/pipeline_config.yaml ../../config/my_pipeline.yaml
```

Edit the configuration file to match your setup:
- Set correct paths for your environment
- Configure API keys (or set environment variables)
- Enable/disable specific pipeline steps
- Adjust generation settings

### 4. Set Environment Variables

```bash
export OPENAI_API_KEY="your-openai-api-key"
export ELEVENLABS_API_KEY="your-elevenlabs-api-key"
```

## Usage

### Basic Usage (Default Configuration)

```bash
dotnet run
```

This will use the default configuration file at `config/pipeline_config.yaml` if it exists.

### Custom Configuration

```bash
dotnet run -- --config /path/to/custom_config.yaml
```

### Specify Story Title

```bash
dotnet run -- --story "My Amazing Story"
```

### Resume from Checkpoint

If the pipeline fails, resume from the last successful step:

```bash
dotnet run -- --resume
```

### Combined Options

```bash
dotnet run -- --config my_config.yaml --story "Epic Adventure" --resume
```

## Configuration

The pipeline is configured via YAML files. See `config/pipeline_config.yaml` for a complete example with comments.

### Key Configuration Sections

#### Pipeline Steps

Enable/disable specific steps:

```yaml
pipeline:
  steps:
    story_idea: true
    script_generation: true
    voice_synthesis: true
    keyframe_generation: false  # Disable if no GPU
    # ... more steps
```

#### Paths

Configure input/output directories:

```yaml
paths:
  story_root: "./Stories"
  python_root: "./Python"
  # ... more paths
```

#### Generation Settings

Control generation parameters:

```yaml
generation:
  story:
    count: 1
    tone: "emotional"
    theme: "friendship"
  video:
    resolution:
      width: 1080
      height: 1920
    fps: 30
```

#### Processing Options

Configure error handling and checkpointing:

```yaml
processing:
  error_handling:
    continue_on_error: true
    retry_count: 3
  checkpointing:
    enabled: true
    resume_from_checkpoint: true
```

## Command-Line Arguments

```
Usage: StoryGenerator.Pipeline [options]

Options:
  --config, -c <path>    Path to YAML configuration file
  --story, -s <title>    Story title (generates new if not provided)
  --resume               Resume from last checkpoint
  --help, -h             Show help message

Examples:
  dotnet run
  dotnet run -- --config custom_config.yaml
  dotnet run -- --story "My Amazing Story"
  dotnet run -- --resume
```

## Output

The pipeline generates the following output structure:

```
Stories/
├── 0_Ideas/              # Story ideas (JSON)
├── 1_Scripts/            # Initial scripts
├── 2_Revised/            # Revised scripts
├── 3_VoiceOver/          # Audio files
├── 4_Titles/             # Subtitles
├── scenes/               # Scene descriptions
├── images/               # Keyframe images
├── videos/               # Interpolated videos
└── final/                # Final composed videos
```

## Checkpointing

The orchestrator automatically saves progress at each step. If the pipeline fails:

1. A checkpoint file is saved: `Stories/pipeline_checkpoint.json`
2. Resume with: `dotnet run -- --resume`
3. The pipeline will skip already completed steps

## Logging

Logs are written to:
- Console (with colored output)
- File: `pipeline.log` (configurable)

Log levels: DEBUG, INFO, WARNING, ERROR

Configure logging in the YAML file:

```yaml
logging:
  level: "INFO"
  file: "pipeline.log"
  console: true
```

## Error Handling

The orchestrator includes robust error handling:

- **Retry Logic**: Automatically retries failed steps (configurable)
- **Continue on Error**: Optionally continue pipeline if non-critical step fails
- **Detailed Logging**: Full error messages and stack traces
- **Checkpoint Recovery**: Resume from last successful step

## Python Integration

The orchestrator calls existing Python generators using subprocess:

- Automatically finds Python executable (`python3`, `python`, or `py`)
- Captures stdout/stderr for logging
- Respects exit codes
- Passes parameters to Python scripts

## Development

### Project Structure

```
StoryGenerator.Pipeline/
├── Config/
│   ├── PipelineConfig.cs      # Configuration models
│   └── ConfigLoader.cs        # YAML loading & validation
├── Core/
│   ├── PipelineOrchestrator.cs # Main orchestrator
│   ├── PipelineLogger.cs       # Logging system
│   └── PipelineCheckpoint.cs   # Checkpoint management
├── Program.cs                  # Entry point
└── StoryGenerator.Pipeline.csproj
```

### Building

```bash
dotnet build
```

### Running Tests

```bash
dotnet test
```

### Publishing

Create a standalone executable:

```bash
dotnet publish -c Release -r linux-x64 --self-contained
```

Or for Windows:

```bash
dotnet publish -c Release -r win-x64 --self-contained
```

## Troubleshooting

### Python Not Found

Error: "Python executable not found"

**Solution**: Ensure Python is installed and in PATH. The orchestrator tries `python3`, `python`, and `py`.

### Configuration Errors

Error: "Configuration file not found" or validation errors

**Solution**: 
- Check file path is correct
- Validate YAML syntax
- Review configuration values

### Python Script Failures

If a Python step fails:

1. Check the logs for detailed error messages
2. Verify Python dependencies are installed: `pip install -r requirements.txt`
3. Test the Python script manually: `python Python/Generation/Manual/MScript.py`
4. Check API keys are set correctly

### Memory Issues

For large batches or high-resolution videos:

- Disable parallel processing: `parallel.enabled: false`
- Reduce resolution: `video.resolution`
- Process one story at a time: `story.count: 1`

## Advanced Usage

### Custom Pipeline Steps

Modify `PipelineOrchestrator.cs` to add custom steps:

```csharp
private async Task CustomStepAsync(string storyTitle)
{
    // Your custom logic here
}
```

### Integration with CI/CD

Use the orchestrator in automated pipelines:

```yaml
# GitHub Actions example
- name: Run StoryGenerator Pipeline
  run: |
    dotnet run -- --config production_config.yaml
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    ELEVENLABS_API_KEY: ${{ secrets.ELEVENLABS_API_KEY }}
```

## Performance

Expected execution times (approximate):

- Story Idea: ~10-30 seconds
- Script Generation: ~30-60 seconds
- Voice Synthesis: ~1-2 minutes
- Keyframe Generation: ~5-10 minutes (with GPU)
- Video Interpolation: ~10-20 minutes
- **Total**: ~20-40 minutes per story

Times vary based on:
- Hardware (GPU vs CPU)
- Script length
- Number of scenes
- Video resolution

## Roadmap

Future enhancements:

- [ ] Batch processing for multiple stories
- [ ] Web API for remote execution
- [ ] Real-time progress updates via WebSocket
- [ ] Cloud deployment support (Azure, AWS)
- [ ] Docker containerization
- [ ] Unit tests and integration tests
- [ ] Performance profiling and optimization

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow C# coding conventions
4. Add tests for new features
5. Submit a pull request

## License

[Specify license]

## Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation
- Review logs for detailed error messages

## Credits

- Pipeline orchestrator by GitHub Copilot
- Python generators by original StoryGenerator authors
- Uses YamlDotNet for YAML parsing
- Integrates OpenAI GPT models
- Integrates ElevenLabs voice synthesis

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: January 2025
