#!/usr/bin/env bash
# Example workflow for repository cleanup
# This demonstrates the safe cleanup process from REPOSITORY_CLEANUP_GUIDE.md

set -euo pipefail

echo "🧹 Repository Cleanup - Example Workflow"
echo "========================================"
echo ""
echo "This script demonstrates a safe cleanup workflow."
echo "It will NOT make permanent changes without confirmation."
echo ""

# Step 1: Check root cleanliness
echo "📋 Step 1: Checking root directory cleanliness..."
if bash scripts/check-clean-root.sh; then
  echo "✅ Root directory is clean"
else
  echo "⚠️  Root directory has unexpected items"
  echo "   Review and move items to appropriate directories"
fi
echo ""

# Step 2: Detect dead Python code
echo "📋 Step 2: Detecting dead Python code..."
if [ -d "src/Python" ]; then
  python3 scripts/detect-dead-code.py src/Python
elif [ -d "core" ]; then
  python3 scripts/detect-dead-code.py core
else
  echo "ℹ️  No Python source directories found to analyze"
fi
echo ""

# Step 3: Detect orphaned files (DRY RUN)
echo "📋 Step 3: Detecting orphaned files (DRY RUN)..."
echo "⚠️  This will analyze the repository but NOT move any files"
echo ""
bash scripts/detect-orphans.sh --dry-run
echo ""

# Step 4: Summary
echo "✅ Cleanup analysis complete!"
echo ""
echo "📊 Next steps:"
echo "   1. Review the reports in /tmp/"
echo "   2. Manually verify potentially orphaned files"
echo "   3. For actual cleanup, run: ./scripts/detect-orphans.sh"
echo "   4. Test builds after moving files to .trash/"
echo "   5. Commit changes incrementally"
echo ""
echo "📚 For more information, see:"
echo "   - REPOSITORY_CLEANUP_GUIDE.md"
echo "   - CLEANUP.md"
echo "   - scripts/README.md"
