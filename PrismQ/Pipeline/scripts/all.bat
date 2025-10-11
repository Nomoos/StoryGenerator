@echo off
setlocal

REM ====== End-to-end Pipeline Launcher ======
REM Runs all pipeline steps (01-05) in order for the same story_id
REM If no story_id is provided, the first step will pick one

set HERE=%~dp0
set STORY_ID=%1

echo ========================================
echo StoryGenerator Pipeline - All Steps
echo ========================================
echo.

if "%STORY_ID%"=="" (
  echo No story_id provided - will be selected by first step
) else (
  echo Processing story_id: %STORY_ID%
)
echo.

REM Step 01: Ingest
echo ========================================
echo Step 01: Ingest
echo ========================================
call "%HERE%01_ingest.bat" %STORY_ID%
if errorlevel 1 (
  echo ERROR: Step 01 failed with exit code %errorlevel%
  exit /b %errorlevel%
)
echo.

REM Step 02: Preprocess
echo ========================================
echo Step 02: Preprocess
echo ========================================
call "%HERE%02_preprocess.bat" %STORY_ID%
if errorlevel 1 (
  echo ERROR: Step 02 failed with exit code %errorlevel%
  exit /b %errorlevel%
)
echo.

REM Step 03: Generate
echo ========================================
echo Step 03: Generate
echo ========================================
call "%HERE%03_generate.bat" %STORY_ID%
if errorlevel 1 (
  echo ERROR: Step 03 failed with exit code %errorlevel%
  exit /b %errorlevel%
)
echo.

REM Step 04: Postprocess
echo ========================================
echo Step 04: Postprocess
echo ========================================
call "%HERE%04_postprocess.bat" %STORY_ID%
if errorlevel 1 (
  echo ERROR: Step 04 failed with exit code %errorlevel%
  exit /b %errorlevel%
)
echo.

REM Step 05: Package
echo ========================================
echo Step 05: Package
echo ========================================
call "%HERE%05_package.bat" %STORY_ID%
if errorlevel 1 (
  echo ERROR: Step 05 failed with exit code %errorlevel%
  exit /b %errorlevel%
)
echo.

echo ========================================
echo Pipeline completed successfully!
echo ========================================
exit /b 0
