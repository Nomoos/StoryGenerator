# Quick Start Guide - Pipeline Orchestrator

Get the StoryGenerator pipeline running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:

```bash
# Check .NET SDK
dotnet --version
# Should be 8.0 or later

# Check Python
python3 --version
# Should be 3.8 or later

# Check Python dependencies
pip list | grep -E "openai|elevenlabs|whisper"
```

## 5-Minute Setup

### Step 1: Clone and Navigate

```bash
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set API Keys

```bash
# Linux/Mac
export OPENAI_API_KEY="your-openai-key-here"
export ELEVENLABS_API_KEY="your-elevenlabs-key-here"

# Windows PowerShell
$env:OPENAI_API_KEY="your-openai-key-here"
$env:ELEVENLABS_API_KEY="your-elevenlabs-key-here"

# Windows CMD
set OPENAI_API_KEY=your-openai-key-here
set ELEVENLABS_API_KEY=your-elevenlabs-key-here
```

### Step 4: Build the Orchestrator

```bash
cd CSharp/StoryGenerator.Pipeline
dotnet build --configuration Release
cd ../..
```

### Step 5: Run the Pipeline!

```bash
# Linux/Mac
./run_pipeline.sh

# Windows
run_pipeline.bat
```

## First Run Options

### Test Configuration (Faster)

Use the example config that skips heavy steps:

```bash
./run_pipeline.sh --config config/pipeline_config_example.yaml
```

This configuration:
- ✅ Generates story ideas
- ✅ Creates scripts
- ✅ Revises scripts
- ⏭️ Skips voice generation (saves time)
- ⏭️ Skips video generation (requires GPU)

Perfect for testing the setup!

### Custom Story

Generate a specific story:

```bash
./run_pipeline.sh --story "The Mysterious Stranger"
```

### Resume After Failure

If the pipeline fails, resume from the last successful step:

```bash
./run_pipeline.sh --resume
```

## Expected Output

During execution, you'll see:

```
================================================================================
StoryGenerator - Complete Pipeline Orchestrator
================================================================================

Loading configuration from: config/pipeline_config.yaml
Configuration loaded successfully
Pipeline: StoryGenerator Full Pipeline
Story Root: ./Stories

[2025-01-15 14:30:00] INFO: Starting pipeline: StoryGenerator Full Pipeline
[2025-01-15 14:30:00] INFO: ================================================================================

📝 STEP 1: Story Idea Generation
--------------------------------------------------------------------------------
  Generating story ideas...
  ✓ Created story: My_Amazing_Story
  
✅ STEP 2: Script Generation
--------------------------------------------------------------------------------
  Generating script for: My_Amazing_Story
  ✓ Script saved to: Stories/1_Scripts/My_Amazing_Story/script.txt
  
...

================================================================================
🎉 PIPELINE COMPLETE!
================================================================================
Story: My_Amazing_Story
Total time: 00:25:30
Output: Stories/final/My_Amazing_Story
```

## Output Files

After completion, find your files in:

```
Stories/
├── 0_Ideas/
│   └── My_Amazing_Story/
│       └── idea.json
├── 1_Scripts/
│   └── My_Amazing_Story/
│       └── script.txt
├── 2_Revised/
│   └── My_Amazing_Story/
│       └── revised.txt
├── 3_VoiceOver/
│   └── My_Amazing_Story/
│       └── voiceover.mp3
└── final/
    └── My_Amazing_Story/
        └── final_video.mp4
```

## Troubleshooting

### "Python not found"

**Solution:**
```bash
# Check Python installation
which python3  # Linux/Mac
where python   # Windows

# Add to PATH if needed
export PATH="/usr/local/bin:$PATH"  # Linux/Mac
```

### "API key not set"

**Solution:**
```bash
# Verify environment variables
echo $OPENAI_API_KEY      # Linux/Mac
echo %OPENAI_API_KEY%     # Windows CMD
$env:OPENAI_API_KEY       # Windows PowerShell
```

### "Configuration file not found"

**Solution:**
```bash
# Create default config
cp config/pipeline_config_example.yaml config/pipeline_config.yaml

# Or specify full path
./run_pipeline.sh --config /full/path/to/config.yaml
```

### Build Errors

**Solution:**
```bash
# Clean and rebuild
cd CSharp/StoryGenerator.Pipeline
dotnet clean
dotnet restore
dotnet build --configuration Release
```

## Common Scenarios

### Scenario 1: Test Without API Keys

Use mock mode (requires code modification) or skip steps:

```yaml
# Edit config/pipeline_config_example.yaml
pipeline:
  steps:
    story_idea: false       # Skip (requires OpenAI)
    script_generation: false # Skip (requires OpenAI)
    voice_synthesis: false   # Skip (requires ElevenLabs)
```

### Scenario 2: Only Generate Scripts

```yaml
pipeline:
  steps:
    story_idea: true
    script_generation: true
    script_revision: true
    # Disable all other steps
```

### Scenario 3: Batch Processing

```yaml
generation:
  story:
    count: 10  # Generate 10 stories
```

Then run:
```bash
./run_pipeline.sh
```

## Configuration Tips

### Minimal Config for Testing

```yaml
pipeline:
  steps:
    story_idea: true
    script_generation: true
    script_revision: true
    # Rest disabled

paths:
  story_root: "./Stories"
  python_root: "./Python"

generation:
  story:
    count: 1
    target_length: 100  # Shorter for faster testing
```

### Full Pipeline Config

Use the default `config/pipeline_config.yaml` for complete generation including video.

## Performance Expectations

| Step | Time | Requirements |
|------|------|-------------|
| Story Idea | 10-30s | OpenAI API |
| Script | 30-60s | OpenAI API |
| Revision | 30-60s | OpenAI API |
| Voice | 1-2 min | ElevenLabs API |
| Subtitles | 1-2 min | WhisperX, CUDA recommended |
| Keyframes | 5-10 min | GPU required |
| Video | 10-20 min | GPU recommended |
| **Total** | **20-40 min** | Full setup |

## Next Steps

1. **Review Output**: Check generated files in `Stories/`
2. **Customize Config**: Edit `config/pipeline_config.yaml`
3. **Batch Process**: Set `story.count: 5` for multiple stories
4. **Read Docs**: See `PIPELINE_ORCHESTRATOR.md` for advanced features

## Getting Help

- **Full Documentation**: `PIPELINE_ORCHESTRATOR.md`
- **C# Project README**: `CSharp/StoryGenerator.Pipeline/README.md`
- **Configuration Guide**: `CONFIGURATION.md`
- **Issue Tracker**: GitHub Issues

## Pro Tips

1. **Start Small**: Use example config first
2. **Check Logs**: Watch console output for progress
3. **Enable Checkpointing**: Always enabled by default
4. **Use Resume**: Don't restart from scratch on failures
5. **Monitor Resources**: GPU/RAM usage for video generation

---

**Ready to generate your first story?**

```bash
# One command to rule them all!
./run_pipeline.sh
```

Happy story generating! 🎬✨
