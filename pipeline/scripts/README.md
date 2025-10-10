# Windows Pipeline Scripts

This directory contains Windows batch scripts for running the StoryGenerator pipeline in a step-based manner.

## Overview

The pipeline is split into 5 discrete steps, each with its own `.bat` script:

1. **01_ingest.bat** - Ingest raw data
2. **02_preprocess.bat** - Clean and validate data  
3. **03_generate.bat** - Generate content (scripts, scenes)
4. **04_postprocess.bat** - Validate and enhance output
5. **05_package.bat** - Create final packaged output

## Prerequisites

1. **Python Environment**: Set up a Python virtual environment at `<repo_root>\env\`
   ```cmd
   python -m venv env
   env\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**: Copy `.env.example` to `.env` and configure:
   ```cmd
   copy .env.example .env
   ```
   
   Edit `.env` to set your API keys and pipeline parameters.

## Quick Start

### Run the complete pipeline (all steps)

Process one story end-to-end:

```cmd
.\pipeline\scripts\all.bat
```

Or process a specific story:

```cmd
.\pipeline\scripts\all.bat STORY-123
```

### Run individual steps

Process a single step:

```cmd
.\pipeline\scripts\03_generate.bat
```

Or with a specific story ID:

```cmd
.\pipeline\scripts\03_generate.bat STORY-123
```

## How It Works

Each `.bat` script:

1. **Loads configuration** from `.env` file at repo root
2. **Picks a story ID** if not provided (using `pick-one` action)
3. **Executes the step** with retry logic (up to `MAX_TRIES`)
4. **Checks acceptance criteria** in a loop until satisfied
5. **Uses exit codes**: 
   - `0` = success
   - `1` = usage/config error
   - `2` = runtime error (retries exhausted)
   - `3` = acceptance criteria not met

## Configuration

Edit `.env` to configure pipeline behavior:

```env
# Core settings
RUN_ROOT=.runs
OUTPUT_DIR=outputs
MAX_TRIES=3
SLEEP_SECS=5

# Step-specific configuration
STEP_03_GENERATE_MODEL_NAME=gpt-4o-mini
STEP_04_POSTPROCESS_MIN_QUALITY=0.7
```

## Outputs

Pipeline outputs are organized by step:

```
outputs/
├── 01_ingest/
│   └── STORY-123.json
├── 02_preprocess/
│   └── STORY-123.json
├── 03_generate/
│   └── STORY-123.json
├── 04_postprocess/
│   └── STORY-123.json
└── 05_package/
    └── STORY-123.json

.runs/
└── 20241010-123456/
    ├── 01_ingest_STORY-123.json
    ├── 02_preprocess_STORY-123.json
    └── ...
```

## Acceptance Criteria

Each step has specific acceptance criteria that must be met:

- **01_ingest**: Output file exists, has required fields, content length >= min
- **02_preprocess**: Data marked as processed, word count in acceptable range
- **03_generate**: Generated script and scenes exist, minimum scene count
- **04_postprocess**: Quality score >= threshold, validation passed
- **05_package**: Final output path exists, data marked as packaged

## Troubleshooting

### Python not found

If you get "python not found" errors, ensure:
1. Python is installed
2. Virtual environment is created at `<repo_root>\env\`
3. The path in the `.bat` scripts matches your setup

Default path used: `%ROOT%\env\Scripts\python.exe`

### Permission denied

Run the batch scripts from a Command Prompt with appropriate permissions:

```cmd
cd /d C:\path\to\StoryGenerator
.\pipeline\scripts\all.bat
```

### Step keeps failing

Check the logs:
1. Console output shows which acceptance criteria failed
2. Check `.runs\<run_id>\` for execution metadata
3. Verify `.env` configuration is correct

### Acceptance criteria not met

If acceptance checks fail repeatedly:
1. Check step output in `outputs\<step_name>\`
2. Review acceptance criteria in `pipeline/orchestration/run_step.py`
3. Adjust configuration in `.env` if needed

## Advanced Usage

### Custom retry configuration

In your `.env`:

```env
MAX_TRIES=5
SLEEP_SECS=10
```

### Default story ID

Process the same story across pipeline runs:

```env
DEFAULT_STORY_ID=STORY-123
```

### Debugging

Enable debug mode:

```env
DEBUG=true
```

Run Python script directly:

```cmd
python pipeline\orchestration\run_step.py --step 03_generate --story-id STORY-123 --action run
```

## Development

The orchestration logic is in `pipeline/orchestration/run_step.py`.

To modify step behavior:
1. Edit the appropriate handler in `run_step.py` (e.g., `_run_generate()`)
2. Update acceptance criteria in the checker (e.g., `_check_generate_acceptance()`)
3. Test with individual step scripts

## See Also

- [Main README](../../README.md) - Project overview
- [Pipeline Documentation](../../docs/pipeline/PIPELINE.md) - Pipeline architecture
- [Contributing Guide](../../CONTRIBUTING.md) - How to contribute
