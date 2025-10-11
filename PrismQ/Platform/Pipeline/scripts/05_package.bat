@echo off
setlocal enabledelayedexpansion

REM ====== CONFIG ======
set STEP=05_package

REM Resolve script and repo roots
set HERE=%~dp0
for %%I in ("%HERE%\..") do set ROOT=%%~fI

REM ====== Load .env ======
if exist "%ROOT%\.env" (
  for /f "usebackq tokens=* delims=" %%a in ("%ROOT%\.env") do (
    if not "%%a"=="" (
      set "line=%%a"
      REM Skip comments
      echo !line!| findstr /b "#">nul
      if errorlevel 1 (
        for /f "tokens=1,2 delims==" %%k in ("!line!") do set "%%k=%%l"
      )
    )
  )
)

REM ====== Inputs & Defaults ======
set STORY_ID=%1
if "%RUN_ID%"=="" (
  for /f "tokens=1-3 delims=/- " %%a in ("%date%") do (set d=%%c%%a%%b)
  for /f "tokens=1-3 delims=:." %%a in ("%time%") do (set t=%%a%%b%%c)
  set RUN_ID=%d%-%t%
)
if "%MAX_TRIES%"=="" set MAX_TRIES=3
if "%SLEEP_SECS%"=="" set SLEEP_SECS=5

REM ====== Determine story if not provided ======
if "%STORY_ID%"=="" (
  if not "%DEFAULT_STORY_ID%"=="" (
    set STORY_ID=%DEFAULT_STORY_ID%
  ) else (
    for /f "delims=" %%s in ('"%ROOT%\env\Scripts\python.exe" "%ROOT%\pipeline\orchestration\run_step.py" --step "%STEP%" --action pick-one') do set STORY_ID=%%s
  )
)

if "%STORY_ID%"=="" (
  echo [%STEP%] No story available to process.
  exit /b 1
)

echo [%STEP%] run_id=%RUN_ID% story_id=%STORY_ID%

REM ====== Execute step (retry on failure) ======
set /a tries=0
:run_step
"%ROOT%\env\Scripts\python.exe" "%ROOT%\pipeline\orchestration\run_step.py" --step "%STEP%" --run-id "%RUN_ID%" --story-id "%STORY_ID%" --action run
if errorlevel 1 (
  set /a tries+=1
  echo [%STEP%] execution failed (try=!tries!)
  if !tries! GEQ %MAX_TRIES% (
    echo [%STEP%] giving up after !tries! tries
    exit /b 2
  )
  timeout /t %SLEEP_SECS% >nul
  goto run_step
)

REM ====== Acceptance loop ======
set /a tries=0
:check_accept
"%ROOT%\env\Scripts\python.exe" "%ROOT%\pipeline\orchestration\run_step.py" --step "%STEP%" --run-id "%RUN_ID%" --story-id "%STORY_ID%" --action check-acceptance
if errorlevel 1 (
  set /a tries+=1
  echo [%STEP%] acceptance not met (try=!tries!)
  if !tries! GEQ %MAX_TRIES% (
    echo [%STEP%] acceptance not met after !tries! checks
    exit /b 3
  )
  "%ROOT%\env\Scripts\python.exe" "%ROOT%\pipeline\orchestration\run_step.py" --step "%STEP%" --run-id "%RUN_ID%" --story-id "%STORY_ID%" --action run
  timeout /t %SLEEP_SECS% >nul
  goto check_accept
)

echo [%STEP%] acceptance met for story_id=%STORY_ID%
exit /b 0
