# Windows Pipeline Quick Reference

## Setup (One-Time)

```cmd
REM 1. Create virtual environment
python -m venv env

REM 2. Activate and install dependencies
env\Scripts\activate
pip install -r requirements.txt

REM 3. Configure environment
copy .env.example .env
REM Edit .env with your settings
```

## Common Commands

### Run Complete Pipeline
```cmd
.\pipeline\scripts\all.bat
.\pipeline\scripts\all.bat STORY-123
```

### Run Individual Steps
```cmd
.\pipeline\scripts\01_ingest.bat
.\pipeline\scripts\02_preprocess.bat STORY-123
.\pipeline\scripts\03_generate.bat STORY-123
.\pipeline\scripts\04_postprocess.bat STORY-123
.\pipeline\scripts\05_package.bat STORY-123
```

### Direct Python Usage
```cmd
REM Pick a story
env\Scripts\python.exe pipeline/orchestration/run_step.py --step 01_ingest --action pick-one

REM Run a step
env\Scripts\python.exe pipeline/orchestration/run_step.py --step 03_generate --run-id test-001 --story-id DEMO-001 --action run

REM Check acceptance
env\Scripts\python.exe pipeline/orchestration/run_step.py --step 03_generate --story-id DEMO-001 --action check-acceptance
```

## Configuration (.env)

```env
# Retry & Timing
MAX_TRIES=3          # Number of retries per step
SLEEP_SECS=5         # Seconds between retries

# Directories
RUN_ROOT=.runs       # Execution metadata
OUTPUT_DIR=outputs   # Step outputs

# Step Configuration
STEP_01_INGEST_MIN_LENGTH=100
STEP_02_PREPROCESS_MIN_WORDS=50
STEP_02_PREPROCESS_MAX_WORDS=500
STEP_03_GENERATE_MODEL_NAME=gpt-4o-mini
STEP_04_POSTPROCESS_MIN_QUALITY=0.7
STEP_05_PACKAGE_OUTPUT_FORMAT=mp4
```

## Exit Codes

- **0** = Success (step completed, acceptance met)
- **1** = Config/usage error (no story available)
- **2** = Runtime error (execution failed after retries)
- **3** = Acceptance not met (after max checks)

## File Locations

```
outputs/
├── 01_ingest/STORY-123.json
├── 02_preprocess/STORY-123.json
├── 03_generate/STORY-123.json
├── 04_postprocess/STORY-123.json
└── 05_package/STORY-123.json

.runs/
└── 20241010-143022/
    ├── 01_ingest_STORY-123.json
    └── ...
```

## Troubleshooting

### Python not found
```cmd
REM Check virtual environment exists
dir env\Scripts\python.exe

REM Recreate if needed
rmdir /s /q env
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

### No story available
```cmd
REM First step creates stories automatically
.\pipeline\scripts\01_ingest.bat

REM Or specify one
.\pipeline\scripts\01_ingest.bat STORY-NEW
```

### Acceptance failing
```cmd
REM Check output
type outputs\03_generate\STORY-123.json

REM Review criteria in run_step.py
REM Adjust thresholds in .env
```

## Documentation

- **Full README**: `pipeline/scripts/README.md`
- **Examples**: `pipeline/scripts/EXAMPLES.md`
- **Implementation**: `pipeline/IMPLEMENTATION_SUMMARY.md`
- **Main Project**: `README.md`

## Pipeline Steps

1. **01_ingest** - Load raw data
2. **02_preprocess** - Clean and validate
3. **03_generate** - Generate content (scripts, scenes)
4. **04_postprocess** - Validate and enhance output
5. **05_package** - Create final packaged output

## Getting Help

```cmd
REM View Python script help
env\Scripts\python.exe pipeline/orchestration/run_step.py --help

REM Check test suite
python tests/test_pipeline_orchestration.py
```
