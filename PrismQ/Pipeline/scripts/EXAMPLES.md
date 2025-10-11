# Windows Pipeline Usage Examples

This document provides concrete examples of using the Windows batch pipeline.

## Example 1: Running the Complete Pipeline

Process a single story through all 5 steps:

```cmd
C:\StoryGenerator> .\pipeline\scripts\all.bat
========================================
StoryGenerator Pipeline - All Steps
========================================

No story_id provided - will be selected by first step

========================================
Step 01: Ingest
========================================
[01_ingest] run_id=20241010-143022 story_id=STORY-20241010143022
[01_ingest] execution succeeded
[01_ingest] acceptance met for story_id=STORY-20241010143022

========================================
Step 02: Preprocess
========================================
[02_preprocess] run_id=20241010-143022 story_id=STORY-20241010143022
[02_preprocess] execution succeeded
[02_preprocess] acceptance met for story_id=STORY-20241010143022

========================================
Step 03: Generate
========================================
[03_generate] run_id=20241010-143022 story_id=STORY-20241010143022
[03_generate] execution succeeded
[03_generate] acceptance met for story_id=STORY-20241010143022

========================================
Step 04: Postprocess
========================================
[04_postprocess] run_id=20241010-143022 story_id=STORY-20241010143022
[04_postprocess] execution succeeded
[04_postprocess] acceptance met for story_id=STORY-20241010143022

========================================
Step 05: Package
========================================
[05_package] run_id=20241010-143022 story_id=STORY-20241010143022
[05_package] execution succeeded
[05_package] acceptance met for story_id=STORY-20241010143022

========================================
Pipeline completed successfully!
========================================
```

## Example 2: Processing a Specific Story

Process story "STORY-ABC123" through all steps:

```cmd
C:\StoryGenerator> .\pipeline\scripts\all.bat STORY-ABC123
========================================
StoryGenerator Pipeline - All Steps
========================================

Processing story_id: STORY-ABC123

========================================
Step 01: Ingest
========================================
[01_ingest] run_id=20241010-143522 story_id=STORY-ABC123
[01_ingest] execution succeeded
[01_ingest] acceptance met for story_id=STORY-ABC123

... (continues through all steps)
```

## Example 3: Running Individual Steps

Run just the generate step for a specific story:

```cmd
C:\StoryGenerator> .\pipeline\scripts\03_generate.bat STORY-ABC123
[03_generate] run_id=20241010-144022 story_id=STORY-ABC123
[03_generate] execution succeeded
[03_generate] acceptance met for story_id=STORY-ABC123
```

## Example 4: Retry on Failure

If a step fails, it retries automatically (configured via MAX_TRIES):

```cmd
C:\StoryGenerator> .\pipeline\scripts\03_generate.bat STORY-XYZ789
[03_generate] run_id=20241010-144522 story_id=STORY-XYZ789
[03_generate] execution failed (try=1)
[03_generate] execution succeeded
[03_generate] acceptance not met (try=1)
[03_generate] execution succeeded
[03_generate] acceptance met for story_id=STORY-XYZ789
```

## Example 5: Acceptance Criteria Not Met

If acceptance criteria cannot be met after MAX_TRIES, the script exits with code 3:

```cmd
C:\StoryGenerator> .\pipeline\scripts\04_postprocess.bat STORY-FAIL
[04_postprocess] run_id=20241010-145022 story_id=STORY-FAIL
[04_postprocess] execution succeeded
[04_postprocess] acceptance not met (try=1)
[04_postprocess] execution succeeded
[04_postprocess] acceptance not met (try=2)
[04_postprocess] execution succeeded
[04_postprocess] acceptance not met (try=3)
[04_postprocess] acceptance not met after 3 checks

C:\StoryGenerator> echo %errorlevel%
3
```

## Example 6: Using Environment Variables

Configure the pipeline via .env:

```env
# .env
MAX_TRIES=5
SLEEP_SECS=10
DEFAULT_STORY_ID=STORY-DEFAULT-001

STEP_03_GENERATE_MODEL_NAME=gpt-4
STEP_03_GENERATE_TEMPERATURE=0.7
STEP_04_POSTPROCESS_MIN_QUALITY=0.85
```

Then run:

```cmd
C:\StoryGenerator> .\pipeline\scripts\all.bat
[01_ingest] run_id=20241010-145522 story_id=STORY-DEFAULT-001
... (uses DEFAULT_STORY_ID from .env)
```

## Example 7: Checking Output Files

After a successful run, check the outputs:

```cmd
C:\StoryGenerator> dir outputs

Directory of C:\StoryGenerator\outputs

10/10/2024  02:45 PM    <DIR>          01_ingest
10/10/2024  02:45 PM    <DIR>          02_preprocess
10/10/2024  02:46 PM    <DIR>          03_generate
10/10/2024  02:46 PM    <DIR>          04_postprocess
10/10/2024  02:47 PM    <DIR>          05_package

C:\StoryGenerator> dir outputs\05_package

Directory of C:\StoryGenerator\outputs\05_package

10/10/2024  02:47 PM             1,234 STORY-20241010143022.json
```

## Example 8: Direct Python Orchestrator Usage

For debugging or manual control, call run_step.py directly:

```cmd
C:\StoryGenerator> env\Scripts\python.exe pipeline\orchestration\run_step.py --help
usage: run_step.py [-h] --step STEP [--run-id RUN_ID] [--story-id STORY_ID]
                   --action {pick-one,run,check-acceptance}

Pipeline Step Orchestrator
...

C:\StoryGenerator> env\Scripts\python.exe pipeline\orchestration\run_step.py ^
    --step 03_generate ^
    --run-id test-001 ^
    --story-id DEMO-001 ^
    --action run
2025-10-10 14:50:22,139 - __main__ - INFO - [03_generate] Running step for story: DEMO-001
2025-10-10 14:50:22,139 - __main__ - INFO - [03_generate] Generating content for DEMO-001
...

C:\StoryGenerator> env\Scripts\python.exe pipeline\orchestration\run_step.py ^
    --step 03_generate ^
    --story-id DEMO-001 ^
    --action check-acceptance
2025-10-10 14:50:28,239 - __main__ - INFO - [03_generate] Checking acceptance for DEMO-001
2025-10-10 14:50:28,239 - __main__ - INFO - [03_generate] Acceptance check passed for DEMO-001

C:\StoryGenerator> echo %errorlevel%
0
```

## Example 9: Pick One Candidate Story

Find a pending story for a specific step:

```cmd
C:\StoryGenerator> env\Scripts\python.exe pipeline\orchestration\run_step.py ^
    --step 02_preprocess ^
    --action pick-one
STORY-20241010143022

C:\StoryGenerator> .\pipeline\scripts\02_preprocess.bat STORY-20241010143022
[02_preprocess] run_id=20241010-151022 story_id=STORY-20241010143022
...
```

## Example 10: Batch Processing Multiple Stories

Process multiple stories in sequence:

```cmd
@echo off
setlocal

REM Process a list of stories
set STORIES=STORY-001 STORY-002 STORY-003

for %%S in (%STORIES%) do (
  echo Processing story: %%S
  call .\pipeline\scripts\all.bat %%S
  if errorlevel 1 (
    echo ERROR: Failed to process %%S
    exit /b 1
  )
)

echo All stories processed successfully!
```

## Exit Codes Reference

- **0**: Success - step completed and acceptance criteria met
- **1**: Usage/configuration error (no story available, missing parameters)
- **2**: Runtime error (step execution failed after MAX_TRIES retries)
- **3**: Acceptance criteria not met (after MAX_TRIES checks)

## Troubleshooting

### "Python not found"

Ensure your virtual environment is set up:

```cmd
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

The .bat scripts expect Python at `%ROOT%\env\Scripts\python.exe`.

### "No story available to process"

First step (01_ingest) creates a new story if none exist. For other steps, ensure the previous step has completed:

```cmd
REM Run steps in order
.\pipeline\scripts\01_ingest.bat STORY-TEST
.\pipeline\scripts\02_preprocess.bat STORY-TEST
.\pipeline\scripts\03_generate.bat STORY-TEST
```

### Acceptance criteria keep failing

Check the logs to understand what's failing:

```cmd
C:\StoryGenerator> type outputs\03_generate\STORY-TEST.json
{
  "story_id": "STORY-TEST",
  "generated_script": "...",
  "generated_scenes": [...]
}
```

Then check the acceptance criteria in `PrismQ/Pipeline/orchestration/run_step.py` for that step.

### Adjust configuration

Edit `.env` to adjust acceptance thresholds:

```env
STEP_04_POSTPROCESS_MIN_QUALITY=0.6  # Lower quality threshold
MAX_TRIES=5  # More retries
```

## See Also

- [Pipeline Scripts README](README.md) - Main documentation
- [Main README](../../README.md) - Project overview
- [Troubleshooting Guide](../../docs/guides/general/TROUBLESHOOTING.md)
