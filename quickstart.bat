@echo off
setlocal enabledelayedexpansion

REM ====================================================================
REM StoryGenerator Quick Start Script for Windows
REM ====================================================================
REM This script will:
REM   1. Check if Python is installed
REM   2. Create a virtual environment (if not exists)
REM   3. Install all dependencies
REM   4. Run tests to verify the installation
REM ====================================================================

echo.
echo ========================================================================
echo           StoryGenerator Quick Start - Windows Setup
echo ========================================================================
echo.

REM ====== Step 1: Check Python ======
echo [1/4] Checking Python installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo    ✓ Python %PYTHON_VERSION% found
echo.

REM Check Python version is 3.10+
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo ERROR: Python 3.10 or higher is required
    echo Current version: %PYTHON_VERSION%
    pause
    exit /b 1
)

if %MAJOR% EQU 3 if %MINOR% LSS 10 (
    echo ERROR: Python 3.10 or higher is required
    echo Current version: %PYTHON_VERSION%
    pause
    exit /b 1
)

REM ====== Step 2: Create Virtual Environment ======
echo [2/4] Setting up virtual environment...
echo.

if exist "env\Scripts\activate.bat" (
    echo    ✓ Virtual environment already exists
) else (
    echo    Creating virtual environment...
    python -m venv env
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo    ✓ Virtual environment created
)
echo.

REM Activate virtual environment
call env\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo    ✓ Virtual environment activated
echo.

REM ====== Step 3: Install Dependencies ======
echo [3/4] Installing dependencies...
echo.

REM Upgrade pip first
echo    Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)

REM Install main dependencies
echo    Installing main dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install main dependencies
    echo.
    echo Try running manually:
    echo   env\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo    ✓ Main dependencies installed
echo.

REM Install development dependencies
echo    Installing development dependencies from requirements-dev.txt...
pip install -r requirements-dev.txt
if errorlevel 1 (
    echo WARNING: Failed to install dev dependencies
    echo Tests may not run properly without these dependencies.
    echo.
    echo Try running manually:
    echo   env\Scripts\activate
    echo   pip install -r requirements-dev.txt
    echo.
    set SKIP_TESTS=1
) else (
    echo    ✓ Development dependencies installed
    echo.
)

REM ====== Step 4: Run Tests ======
if defined SKIP_TESTS (
    echo [4/4] Skipping tests due to missing dev dependencies
    echo.
    goto end_setup
)

echo [4/4] Running tests to verify installation...
echo.

REM Check if pytest is available
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo WARNING: pytest not found, skipping tests
    echo.
    goto end_setup
)

REM Run pipeline tests (quick smoke tests)
echo    Running pipeline orchestration tests...
python tests\test_pipeline_orchestration.py
if errorlevel 1 (
    echo WARNING: Pipeline orchestration tests failed
    echo This may indicate an installation issue.
    set TEST_FAILED=1
) else (
    echo    ✓ Pipeline orchestration tests passed
)
echo.

REM Run database tests
echo    Running database tests...
python tests\test_story_database.py
if errorlevel 1 (
    echo WARNING: Database tests failed
    echo This may indicate an installation issue.
    set TEST_FAILED=1
) else (
    echo    ✓ Database tests passed
)
echo.

REM Run full test suite (optional, can be slow)
set /p RUN_FULL_TESTS="Run full test suite? (y/N): "
if /i "%RUN_FULL_TESTS%"=="y" (
    echo.
    echo    Running full test suite with pytest...
    echo    (This may take a few minutes...)
    echo.
    pytest -v --tb=short -m "not slow"
    if errorlevel 1 (
        echo WARNING: Some tests failed
        set TEST_FAILED=1
    ) else (
        echo    ✓ Full test suite passed
    )
    echo.
)

:end_setup

REM ====== Setup Complete ======
echo.
echo ========================================================================
echo                        Setup Complete!
echo ========================================================================
echo.

if defined TEST_FAILED (
    echo ⚠  Setup completed with warnings
    echo    Some tests failed. Review the output above.
) else (
    echo ✓ All checks passed successfully!
)

echo.
echo Next Steps:
echo -----------
echo.
echo 1. Configure your environment:
echo    copy .env.example .env
echo    (Edit .env with your API keys)
echo.
echo 2. Run the pipeline:
echo    .\pipeline\scripts\all.bat
echo.
echo 3. Or run individual steps:
echo    .\pipeline\scripts\01_ingest.bat
echo    .\pipeline\scripts\02_preprocess.bat
echo    .\pipeline\scripts\03_generate.bat
echo.
echo 4. Query pipeline status:
echo    python pipeline\orchestration\run_step.py --action stats
echo.
echo 5. Run tests:
echo    pytest
echo.
echo Documentation:
echo   - Main README: README.md
echo   - Pipeline Guide: pipeline\scripts\README.md
echo   - Database Tracking: pipeline\DATABASE_TRACKING.md
echo.
echo ========================================================================
echo.

if defined TEST_FAILED (
    echo Note: Setup completed but some tests failed.
    echo      Check the output above for details.
    echo.
)

echo Virtual environment is already activated.
echo To deactivate, run: deactivate
echo.
pause
