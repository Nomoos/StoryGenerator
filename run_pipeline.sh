#!/bin/bash
# StoryGenerator Pipeline Runner
# Quick launcher for the pipeline orchestrator

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}StoryGenerator Pipeline Runner${NC}"
echo -e "${GREEN}================================${NC}"
echo

# Change to script directory
cd "$(dirname "$0")"

# Check if .NET is installed
if ! command -v dotnet &> /dev/null; then
    echo -e "${RED}Error: .NET SDK not found${NC}"
    echo "Please install .NET 8.0 or later from https://dotnet.microsoft.com/download"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python not found${NC}"
    echo "Please install Python 3.8 or later"
    exit 1
fi

# Build the project if needed
if [ ! -d "CSharp/StoryGenerator.Pipeline/bin" ]; then
    echo -e "${YELLOW}Building pipeline orchestrator...${NC}"
    cd CSharp/StoryGenerator.Pipeline
    dotnet build --configuration Release
    if [ $? -ne 0 ]; then
        echo -e "${RED}Build failed${NC}"
        exit 1
    fi
    cd ../..
fi

# Run the pipeline
echo -e "${GREEN}Starting pipeline...${NC}"
echo

cd CSharp/StoryGenerator.Pipeline
dotnet run --configuration Release -- "$@"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo
    echo -e "${GREEN}Pipeline completed successfully!${NC}"
else
    echo
    echo -e "${RED}Pipeline failed with exit code $exit_code${NC}"
fi

exit $exit_code
