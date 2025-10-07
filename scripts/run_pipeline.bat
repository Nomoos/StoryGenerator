@echo off
REM StoryGenerator Pipeline Runner
REM Quick launcher for the pipeline orchestrator

echo ================================
echo StoryGenerator Pipeline Runner
echo ================================
echo.

REM Change to script directory
cd /d %~dp0

REM Check if .NET is installed
where dotnet >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: .NET SDK not found
    echo Please install .NET 8.0 or later from https://dotnet.microsoft.com/download
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    where python3 >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Python not found
        echo Please install Python 3.8 or later
        exit /b 1
    )
)

REM Build the project if needed
if not exist "CSharp\StoryGenerator.Pipeline\bin" (
    echo Building pipeline orchestrator...
    cd CSharp\StoryGenerator.Pipeline
    dotnet build --configuration Release
    if %ERRORLEVEL% NEQ 0 (
        echo Build failed
        exit /b 1
    )
    cd ..\..
)

REM Run the pipeline
echo Starting pipeline...
echo.

cd CSharp\StoryGenerator.Pipeline
dotnet run --configuration Release -- %*

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Pipeline completed successfully!
) else (
    echo.
    echo Pipeline failed with exit code %ERRORLEVEL%
)

exit /b %ERRORLEVEL%
