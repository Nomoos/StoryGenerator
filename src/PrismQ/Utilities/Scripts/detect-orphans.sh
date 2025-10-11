#!/usr/bin/env bash
# Script for detecting orphaned files in the repository
# Usage: ./scripts/detect-orphans.sh [--dry-run]

set -euo pipefail

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Repository Cleanup - Orphaned File Detector"
echo "=============================================="
echo ""

# Protected patterns (never delete these)
PROTECT='(migrations?|infra|deploy|\.github|docs/legal|LICENSE|NOTICE|CHANGELOG|\.git|node_modules|venv|\.venv|__pycache__|\.pytest_cache|\.idea|dist|build|out|coverage|\.trash)'

# File extensions to check
EXTENSIONS='(py|js|jsx|ts|tsx|css|scss|png|jpg|jpeg|svg|json|md)'

echo "📋 Step 1: Identifying candidate files..."
mapfile -t CANDIDATES < <(git ls-files \
  | grep -E "\.${EXTENSIONS}\$" \
  | grep -Ev "$PROTECT" \
  | sort)

echo "Found ${#CANDIDATES[@]} candidate files to analyze"
echo ""

# Check if ripgrep is available
if ! command -v rg &> /dev/null; then
  echo -e "${RED}❌ Error: ripgrep (rg) is not installed${NC}"
  echo "Please install it: https://github.com/BurntSushi/ripgrep"
  exit 1
fi

echo "📊 Step 2: Analyzing file references..."
ORPHANS_FILE="/tmp/orphans-$(date +%s).txt"
> "$ORPHANS_FILE"

total=0
orphaned=0

for f in "${CANDIDATES[@]}"; do
  total=$((total + 1))
  filename=$(basename "$f")
  
  # Skip if file doesn't exist (edge case)
  if [[ ! -f "$f" ]]; then
    continue
  fi
  
  # Search for references to this file (by filename)
  # Exclude the file itself and common generated/cache directories
  if ! rg -q --hidden \
    --glob '!.git' \
    --glob '!node_modules' \
    --glob '!venv' \
    --glob '!.venv' \
    --glob '!__pycache__' \
    --glob '!dist' \
    --glob '!build' \
    --glob '!coverage' \
    --glob '!.pytest_cache' \
    --glob "!$f" \
    --fixed-strings "$filename" 2>/dev/null; then
    
    echo "$f" >> "$ORPHANS_FILE"
    orphaned=$((orphaned + 1))
    echo -e "${YELLOW}🔸 Potentially orphaned: $f${NC}"
  fi
  
  # Progress indicator
  if (( total % 10 == 0 )); then
    echo "   ... processed $total/$total files"
  fi
done

echo ""
echo "✅ Analysis complete!"
echo "   Total files analyzed: $total"
echo "   Potentially orphaned: $orphaned"
echo ""

if [[ $orphaned -eq 0 ]]; then
  echo -e "${GREEN}🎉 No orphaned files found!${NC}"
  rm -f "$ORPHANS_FILE"
  exit 0
fi

echo "📄 Orphaned files saved to: $ORPHANS_FILE"
echo ""

# Display summary by directory
echo "📊 Orphaned files by directory:"
awk -F/ '{dir=$1; for(i=2;i<NF;i++) dir=dir"/"$i; print dir}' "$ORPHANS_FILE" | sort | uniq -c | sort -rn

echo ""
echo "⚠️  IMPORTANT SAFETY CHECKS:"
echo "   - Review the list carefully before deletion"
echo "   - Some files may be referenced dynamically"
echo "   - Check for string-based imports or requires"
echo "   - Test builds after moving to .trash"
echo ""

if [[ "$DRY_RUN" == true ]]; then
  echo "✅ DRY RUN MODE - No files will be moved"
  echo "   To move files to .trash, run without --dry-run"
  exit 0
fi

# Interactive confirmation
echo -e "${YELLOW}❓ Do you want to move these files to .trash/ for review? (y/N)${NC}"
read -r response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
  echo "Aborted. No files were moved."
  exit 0
fi

# Move orphaned files to .trash
echo ""
echo "🗑️  Moving orphaned files to .trash/..."
mkdir -p .trash

moved=0
while IFS= read -r f; do
  if [[ -n "$f" && -f "$f" ]]; then
    target_dir=".trash/$(dirname "$f")"
    mkdir -p "$target_dir"
    
    if git mv "$f" ".trash/$f" 2>/dev/null; then
      moved=$((moved + 1))
      echo -e "${GREEN}✓${NC} Moved: $f"
    else
      echo -e "${RED}✗${NC} Failed to move: $f"
    fi
  fi
done < "$ORPHANS_FILE"

echo ""
echo "📦 Moved $moved files to .trash/"
echo ""
echo "🔍 Next steps:"
echo "   1. Review files in .trash/"
echo "   2. Run your build: npm run build / pytest / dotnet build"
echo "   3. Run your tests: npm test / pytest / dotnet test"
echo "   4. If everything works:"
echo "      git rm -r .trash/"
echo "      git commit -m 'chore: remove orphaned files'"
echo "   5. If something broke:"
echo "      git restore --staged .trash/"
echo "      git restore .trash/"
echo "      Investigate which files are needed"
echo ""
echo -e "${YELLOW}⚠️  Remember: Always test before committing deletions!${NC}"
