# StoryGenerator Pipeline Orchestrator (C#)

## 🎯 One-Click Pipeline Execution

The C# Pipeline Orchestrator provides a complete end-to-end automation solution for the StoryGenerator project. Run the entire pipeline from story idea to final video with a single command!

## ✨ Features

- **One-Command Execution**: Run the complete pipeline with a single command
- **YAML Configuration**: Flexible configuration via YAML files
- **Checkpointing**: Automatically resume from last successful step on failure
- **Error Handling**: Robust error handling with retry logic
- **Comprehensive Logging**: Console and file logging with colored output
- **Python Integration**: Seamlessly calls existing Python generators
- **Configurable Steps**: Enable/disable specific pipeline steps
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- .NET 8.0 SDK or later
- Python 3.8+ with StoryGenerator dependencies
- OpenAI API key
- ElevenLabs API key

### Installation

```bash
# Clone the repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator

# Set up environment variables
export OPENAI_API_KEY="your-openai-api-key"
export ELEVENLABS_API_KEY="your-elevenlabs-api-key"

# Run the pipeline (builds automatically on first run)
./run_pipeline.sh
```

Or on Windows:

```batch
run_pipeline.bat
```

That's it! The orchestrator will:
1. Build the project if needed
2. Load configuration from `config/pipeline_config.yaml`
3. Execute all enabled pipeline steps in sequence
4. Generate the final video output

## 📋 Pipeline Steps

The orchestrator chains the following steps:

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

Each step can be individually enabled/disabled via configuration.

## ⚙️ Configuration

### Basic Configuration

Edit `config/pipeline_config.yaml` to customize:

```yaml
pipeline:
  steps:
    story_idea: true
    script_generation: true
    # ... more steps
    keyframe_generation: false  # Disable if no GPU

paths:
  story_root: "./Stories"
  python_root: "./Python"

generation:
  story:
    tone: "emotional"
    theme: "friendship"
  video:
    resolution:
      width: 1080
      height: 1920
    fps: 30
```

### Command-Line Usage

```bash
# Use default configuration
./run_pipeline.sh

# Use custom configuration
./run_pipeline.sh --config my_config.yaml

# Specify story title
./run_pipeline.sh --story "My Amazing Story"

# Resume from checkpoint
./run_pipeline.sh --resume

# Combined options
./run_pipeline.sh --config my_config.yaml --story "Epic Tale" --resume
```

### Direct .NET Usage

```bash
cd CSharp/StoryGenerator.Pipeline
dotnet build
dotnet run -- --config ../../config/pipeline_config.yaml
```

## 📂 Output Structure

The pipeline generates organized output:

```
Stories/
├── 0_Ideas/          # Story ideas (JSON)
├── 1_Scripts/        # Initial scripts
├── 2_Revised/        # Revised scripts
├── 3_VoiceOver/      # Audio files
├── 4_Titles/         # Subtitles
├── scenes/           # Scene descriptions
├── images/           # Keyframe images
├── videos/           # Interpolated videos
└── final/            # Final composed videos
```

## 🔄 Checkpointing & Recovery

The orchestrator automatically saves progress:

- Checkpoint file: `Stories/pipeline_checkpoint.json`
- Automatically created after each successful step
- Resume with: `./run_pipeline.sh --resume`
- Skips already completed steps

## 📊 Logging

Comprehensive logging to console and file:

```
[2025-01-15 14:30:00] INFO: Starting pipeline: StoryGenerator Full Pipeline
[2025-01-15 14:30:05] INFO: ✅ STEP 1: Story Idea Generation
[2025-01-15 14:30:42] INFO: ✅ STEP 2: Script Generation
...
```

Configure logging in YAML:

```yaml
logging:
  level: "INFO"     # DEBUG, INFO, WARNING, ERROR
  file: "pipeline.log"
  console: true
```

## 🛠️ Advanced Usage

### Partial Pipeline Execution

Run only specific steps by disabling others in configuration:

```yaml
pipeline:
  steps:
    story_idea: false        # Skip - use existing
    script_generation: false # Skip - use existing
    voice_synthesis: true    # Run this
    asr_subtitles: true      # And this
    # ... rest disabled
```

### Batch Processing

Process multiple stories by adjusting configuration:

```yaml
generation:
  story:
    count: 5  # Generate 5 stories
```

### Custom Paths

Point to different directories:

```yaml
paths:
  story_root: "/path/to/my/stories"
  python_root: "/path/to/python/generators"
```

## 🐛 Troubleshooting

### Python Not Found

**Error**: "Python executable not found"

**Solution**: Ensure Python is in PATH. The orchestrator tries `python3`, `python`, and `py`.

### Build Errors

**Error**: Build failures

**Solution**:
```bash
cd CSharp/StoryGenerator.Pipeline
dotnet clean
dotnet restore
dotnet build
```

### Python Script Failures

**Solution**:
1. Check logs for detailed errors
2. Verify Python dependencies: `pip install -r requirements.txt`
3. Test Python scripts manually
4. Verify API keys are set

### Configuration Errors

**Solution**:
- Validate YAML syntax (use online validator)
- Check all required fields are present
- Review validation error messages

## 📖 Documentation

- **Pipeline Orchestrator README**: `CSharp/StoryGenerator.Pipeline/README.md`
- **Configuration Guide**: `CONFIGURATION.md`
- **Python Integration**: `Python/README.md`
- **Pipeline Architecture**: `PIPELINE.md`

## ⏱️ Performance

Approximate execution times:

- **Story Idea**: ~10-30 seconds
- **Script Generation**: ~30-60 seconds
- **Voice Synthesis**: ~1-2 minutes
- **Keyframe Generation**: ~5-10 minutes (with GPU)
- **Video Interpolation**: ~10-20 minutes
- **Total**: ~20-40 minutes per story

## 🔮 Future Enhancements

- [ ] Web API for remote execution
- [ ] Real-time progress updates via WebSocket
- [ ] Docker containerization
- [ ] Cloud deployment support (Azure, AWS)
- [ ] Parallel processing for multiple stories
- [ ] Advanced retry strategies
- [ ] Performance profiling tools

## 💡 Tips

1. **Start Simple**: Use example configuration for initial testing
2. **Enable Checkpointing**: Always enable for long-running pipelines
3. **Monitor Logs**: Watch console output for real-time progress
4. **Test Steps Individually**: Disable most steps to test one at a time
5. **Use Resume**: Don't restart from scratch on failures

## 📝 Example Workflow

```bash
# 1. Initial setup
export OPENAI_API_KEY="your-key"
export ELEVENLABS_API_KEY="your-key"

# 2. Test with minimal steps
./run_pipeline.sh --config config/pipeline_config_example.yaml

# 3. Run full pipeline
./run_pipeline.sh

# 4. If it fails, resume
./run_pipeline.sh --resume

# 5. Process a specific story
./run_pipeline.sh --story "My Epic Tale"
```

## 🤝 Contributing

Contributions welcome! The orchestrator is designed to be extensible:

- Add custom pipeline steps
- Enhance error handling
- Improve logging
- Add new configuration options

See `CSharp/StoryGenerator.Pipeline/Core/PipelineOrchestrator.cs` for implementation details.

## 📄 License

[Specify license]

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: January 2025  

For detailed technical documentation, see `CSharp/StoryGenerator.Pipeline/README.md`
