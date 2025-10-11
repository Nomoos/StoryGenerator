# CLI Usage Guide

**StoryGenerator.CLI** - Command-line interface for the StoryGenerator pipeline

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Commands](#commands)
  - [Pipeline Commands](#pipeline-commands)
  - [Stage Commands](#stage-commands)
- [Examples](#examples)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview

The StoryGenerator CLI provides a comprehensive command-line interface for running the complete video generation pipeline or individual stages. It supports:

- Full end-to-end pipeline execution
- Individual stage execution for testing
- Pipeline resume from checkpoints
- Configuration validation
- Progress tracking and reporting

## Installation

### Prerequisites

- .NET 9.0 SDK or later
- FFmpeg (for audio/video processing)
- Python 3.10+ (for some pipeline stages)

### Build

```bash
cd src/CSharp
dotnet build StoryGenerator.sln
```

### Run

```bash
cd src/CSharp/StoryGenerator.CLI
dotnet run -- [command] [options]
```

Or build and use the executable:

```bash
cd src/CSharp
dotnet publish StoryGenerator.CLI -c Release -o ./publish
./publish/StoryGenerator.CLI [command] [options]
```

## Environment Setup

The CLI requires environment variables for API access:

### Required Variables

```bash
export OPENAI_API_KEY="your-openai-api-key"
export ELEVENLABS_API_KEY="your-elevenlabs-api-key"
```

### Optional Variables

```bash
export ELEVENLABS_VOICE_ID="BZgkqPqms7Kj9ulSkVzn"  # Default voice
export STORY_ROOT="./Stories"                       # Output directory
```

### .env File Support

Create a `.env` file in your project root:

```env
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=BZgkqPqms7Kj9ulSkVzn
STORY_ROOT=./Stories
```

## Commands

### Pipeline Commands

#### full-pipeline

Run the complete pipeline from idea generation to final video with subtitles.

```bash
dotnet run -- full-pipeline --topic "your story topic" [--output-root ./Stories]
```

**Options:**
- `--topic` (required): Topic for story generation
- `--output-root` (optional): Root directory for outputs (default: `./Stories`)

**Example:**
```bash
dotnet run -- full-pipeline --topic "falling for someone" --output-root ./output
```

**Pipeline Stages:**
1. Generate story idea
2. Generate script (~360 words)
3. Revise script for voice clarity
4. Enhance script with voice tags
5. Generate voiceover (ElevenLabs TTS)
6. Generate word-level subtitles

#### pipeline-resume

Resume a pipeline from a saved checkpoint.

```bash
dotnet run -- pipeline-resume [--checkpoint-path ./Stories/pipeline_checkpoint.json]
```

**Options:**
- `--checkpoint-path` (optional): Path to checkpoint file (default: `./Stories/pipeline_checkpoint.json`)

**Example:**
```bash
dotnet run -- pipeline-resume --checkpoint-path ./my-checkpoint.json
```

**Note:** Currently shows information about checkpointing. Full integration with PipelineOrchestrator is planned.

#### pipeline-validate

Validate pipeline configuration and environment setup.

```bash
dotnet run -- pipeline-validate [--config ./appsettings.json]
```

**Options:**
- `--config` (optional): Path to configuration file (default: `./appsettings.json`)

**Example:**
```bash
dotnet run -- pipeline-validate --config ./appsettings.Development.json
```

**Checks:**
- ✅ Configuration file is valid JSON
- ✅ Required environment variables are set
- ✅ API keys are configured

### Stage Commands

Run individual pipeline stages for testing or custom workflows.

#### generate-ideas

Generate story ideas with viral potential scoring.

```bash
dotnet run -- generate-ideas --topic "friendship" [options]
```

**Options:**
- `--topic` (required): Topic for idea generation
- `--count` (optional): Number of ideas to generate (default: 5)
- `--tone` (optional): Tone for stories (e.g., emotional, witty, dramatic)
- `--theme` (optional): Theme for stories (e.g., friendship, love, betrayal)
- `--output` (optional): Output directory (default: `./0_Ideas`)

**Example:**
```bash
dotnet run -- generate-ideas \
  --topic "unexpected friendship" \
  --count 3 \
  --tone "emotional" \
  --theme "friendship" \
  --output ./ideas
```

#### generate-script

Generate a ~360 word script from a story idea.

```bash
dotnet run -- generate-script --idea-file ./0_Ideas/story.json [--output ./1_Scripts]
```

**Options:**
- `--idea-file` (required): Path to story idea JSON file
- `--output` (optional): Output directory (default: `./1_Scripts`)

**Example:**
```bash
dotnet run -- generate-script \
  --idea-file ./ideas/falling_for_someone.json \
  --output ./scripts
```

#### revise-script

Revise a script for AI voice clarity.

```bash
dotnet run -- revise-script --script-dir ./1_Scripts/story [--output ./2_Revised]
```

**Options:**
- `--script-dir` (required): Directory containing script.txt and metadata.json
- `--output` (optional): Output directory (default: `./2_Revised`)

**Example:**
```bash
dotnet run -- revise-script \
  --script-dir ./scripts/my_story \
  --output ./revised
```

#### enhance-script

Add ElevenLabs voice tags to a revised script.

```bash
dotnet run -- enhance-script --script-dir ./2_Revised/story
```

**Options:**
- `--script-dir` (required): Directory containing revised script

**Example:**
```bash
dotnet run -- enhance-script \
  --script-dir ./revised/my_story
```

#### generate-voice

Generate voiceover audio from a script.

```bash
dotnet run -- generate-voice --script-file ./script.txt [--output ./audio.mp3]
```

**Options:**
- `--script-file` (required): Path to script file
- `--output` (optional): Output audio file path (default: same dir as script)

**Example:**
```bash
dotnet run -- generate-voice \
  --script-file ./revised/my_story/script_enhanced.txt \
  --output ./audio/voiceover.mp3
```

#### generate-subtitles

Generate word-level SRT subtitles from audio and script.

```bash
dotnet run -- generate-subtitles \
  --audio-file ./audio.mp3 \
  --script-file ./script.txt \
  [--output ./subtitles.srt]
```

**Options:**
- `--audio-file` (required): Path to audio file
- `--script-file` (required): Path to script file
- `--output` (optional): Output SRT file path (default: same dir as audio)

**Example:**
```bash
dotnet run -- generate-subtitles \
  --audio-file ./audio/voiceover.mp3 \
  --script-file ./revised/my_story/script_enhanced.txt \
  --output ./subtitles/final.srt
```

## Examples

### Example 1: Complete Pipeline

Generate a complete video from topic to subtitled video:

```bash
# Set environment variables
export OPENAI_API_KEY="sk-..."
export ELEVENLABS_API_KEY="..."

# Run full pipeline
cd src/CSharp/StoryGenerator.CLI
dotnet run -- full-pipeline \
  --topic "falling for someone" \
  --output-root ./output
```

### Example 2: Custom Workflow

Run stages individually for more control:

```bash
# 1. Generate ideas
dotnet run -- generate-ideas \
  --topic "unexpected kindness" \
  --count 5 \
  --output ./ideas

# 2. Generate script from best idea
dotnet run -- generate-script \
  --idea-file ./ideas/best_idea.json \
  --output ./scripts

# 3. Revise script
dotnet run -- revise-script \
  --script-dir ./scripts/unexpected_kindness \
  --output ./revised

# 4. Enhance with voice tags
dotnet run -- enhance-script \
  --script-dir ./revised/unexpected_kindness

# 5. Generate voiceover
dotnet run -- generate-voice \
  --script-file ./revised/unexpected_kindness/script_enhanced.txt \
  --output ./audio/voiceover.mp3

# 6. Generate subtitles
dotnet run -- generate-subtitles \
  --audio-file ./audio/voiceover.mp3 \
  --script-file ./revised/unexpected_kindness/script_enhanced.txt \
  --output ./subtitles.srt
```

### Example 3: Validate Configuration

Before running the pipeline, validate your setup:

```bash
# Check configuration and environment
dotnet run -- pipeline-validate

# Output:
# ✅ Validating configuration: ./appsettings.json
# ⚠️  Warning: Missing environment variables:
#     - OPENAI_API_KEY
# ✅ Configuration is valid
```

### Example 4: Resume from Checkpoint

If a pipeline fails, resume from the last checkpoint:

```bash
# Pipeline saves checkpoints automatically
dotnet run -- full-pipeline --topic "my story"

# If it fails at step 3, resume:
dotnet run -- pipeline-resume --checkpoint-path ./Stories/pipeline_checkpoint.json
```

## Configuration

### appsettings.json

The CLI uses `appsettings.json` for configuration:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "System": "Warning"
    }
  },
  "Python": {
    "InterpreterPath": "python3",
    "ScriptsPath": "../../scripts",
    "TimeoutSeconds": 300
  },
  "FFmpeg": {
    "ExecutablePath": "ffmpeg",
    "FfprobePath": "ffprobe",
    "TimeoutSeconds": 600
  }
}
```

### Development Configuration

Use `appsettings.Development.json` for development-specific settings:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  }
}
```

## Troubleshooting

### Common Issues

#### 1. Missing API Keys

**Error:**
```
❌ Error: OPENAI_API_KEY environment variable not set
```

**Solution:**
```bash
export OPENAI_API_KEY="your-key-here"
export ELEVENLABS_API_KEY="your-key-here"
```

#### 2. FFmpeg Not Found

**Error:**
```
System.ComponentModel.Win32Exception: No such file or directory
```

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Verify installation
ffmpeg -version
```

#### 3. Python Script Errors

**Error:**
```
Python script execution failed: ...
```

**Solution:**
- Ensure Python 3.10+ is installed
- Install required packages: `pip install -r requirements.txt`
- Check `appsettings.json` for correct Python path

#### 4. Checkpoint Not Found

**Error:**
```
❌ Checkpoint file not found: ./Stories/pipeline_checkpoint.json
```

**Solution:**
- Checkpoint file is created during pipeline execution
- If manually resuming, ensure the path is correct
- Run validation: `dotnet run -- pipeline-validate`

### Debug Mode

Enable detailed logging for troubleshooting:

```bash
# Set log level in appsettings.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  }
}
```

### Getting Help

```bash
# General help
dotnet run -- --help

# Command-specific help
dotnet run -- full-pipeline --help
dotnet run -- generate-ideas --help
```

## Additional Resources

- [Pipeline Architecture Documentation](./PIPELINE_GUIDE.md)
- [Configuration Guide](../docs/PIPELINE_ORCHESTRATION.md)
- [Troubleshooting Guide](../docs/PIPELINE_ORCHESTRATION.md#troubleshooting)
- [GitHub Issues](https://github.com/Nomoos/StoryGenerator/issues)

## Support

For issues or questions:

1. Check this documentation
2. Review [PIPELINE_GUIDE.md](./PIPELINE_GUIDE.md)
3. Search [existing issues](https://github.com/Nomoos/StoryGenerator/issues)
4. Create a new issue if needed

---

**Last Updated:** January 2025  
**Version:** Phase 4 - Pipeline Orchestration
