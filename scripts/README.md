# Scripts Directory

This directory contains various utility scripts for the StoryGenerator project.

## 📦 Cleanup & Maintenance Scripts

### `detect-orphans.sh`
Detects orphaned files (files not referenced anywhere in the codebase).

**Usage:**
```bash
# Dry run (no changes)
./scripts/detect-orphans.sh --dry-run

# Interactive mode (moves files to .trash after confirmation)
./scripts/detect-orphans.sh
```

**Features:**
- Scans for unreferenced `.py`, `.js`, `.ts`, `.tsx`, `.css`, `.scss`, `.png`, `.jpg`, `.svg`, `.json`, `.md` files
- Protects critical files (migrations, infra, legal)
- Moves candidates to `.trash/` for safe review
- Requires `ripgrep` (rg) to be installed

**Safety:**
- Always test builds after moving files
- Review `.trash/` contents before permanent deletion
- Use `git restore` to recover if needed

### `detect-dead-code.py`
Analyzes Python codebase for potentially unused functions and classes.

**Usage:**
```bash
# Analyze entire src directory
python3 scripts/detect-dead-code.py src/

# Analyze specific directory
python3 scripts/detect-dead-code.py src/Python
```

**Features:**
- Finds unused functions and classes
- Simple heuristic analysis
- Saves report to `/tmp/dead-code-report.txt`

**Limitations:**
- May not detect dynamic imports
- String-based references not detected
- Always verify manually before deletion

### `check-clean-root.sh`
Validates that the repository root contains only allowed files/directories.

**Usage:**
```bash
./scripts/check-clean-root.sh
```

**Allowed root items:**
- Configuration files: `.gitignore`, `.editorconfig`, `pyproject.toml`, etc.
- Documentation: `README.md`, `QUICKSTART.md`, `CLEANUP_REPO.md`, etc.
- Directories: `src/`, `tests/`, `docs/`, `scripts/`, `assets/`, `examples/`, etc.

## 🎬 Content Generation Scripts

### `setup_folders.py`
Sets up the folder structure for content generation.

### `verify_folders.py`
Verifies the folder structure is correct.

### `deduplicate_content.py`
Removes duplicate content files.

### `title_score.py`
Scores generated titles for quality.

### `title_improve.py`
Improves titles based on feedback.

### `content_ranking.py`
Ranks content for selection.

### `process_quality.py`
Processes quality metrics for generated content.

### `check_video_quality.py`
Checks video quality metrics.

## 🌐 Data Collection Scripts

### `reddit_scraper.py`
Scrapes content from Reddit for story ideas.
See [README_REDDIT_SCRAPER.md](./README_REDDIT_SCRAPER.md) for details.

### `process_trends.py`
Processes trending topics.

## 🔬 Development & Testing Scripts

### `generate_atomic_issues.py`
Generates atomic GitHub issues from larger issues.

### `microstep_validate.py`
Validates microstep completion.

### `generate_attribution.py`
Generates attribution information for content sources.

## 📁 Directory Structure

```
scripts/
├── README.md                    # This file
├── detect-orphans.sh           # Orphaned file detector
├── detect-dead-code.py         # Dead code analyzer
├── check-clean-root.sh         # Root cleanliness validator
├── setup_folders.py            # Folder structure setup
├── verify_folders.py           # Folder structure verification
├── deduplicate_content.py      # Content deduplication
├── title_score.py              # Title scoring
├── title_improve.py            # Title improvement
├── content_ranking.py          # Content ranking
├── process_quality.py          # Quality processing
├── check_video_quality.py      # Video quality checking
├── reddit_scraper.py           # Reddit content scraper
├── process_trends.py           # Trend processing
├── generate_atomic_issues.py   # Issue generation
├── microstep_validate.py       # Microstep validation
├── generate_attribution.py     # Attribution generation
├── run_pipeline.sh             # Pipeline runner (Linux/Mac)
├── run_pipeline.bat            # Pipeline runner (Windows)
├── pipeline/                   # Pipeline-related scripts
└── scrapers/                   # Web scraping utilities
```

## 🔧 Requirements

### System Tools
- **bash** (for shell scripts)
- **ripgrep** (`rg`) - Fast text search tool
  - Install: `brew install ripgrep` (Mac) or `apt install ripgrep` (Ubuntu)
- **git** - Version control

### Python Packages
Most scripts require Python 3.10+ and packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Optional Tools for Advanced Cleanup
- **vulture** - Python dead code finder: `pip install vulture`
- **unimport** - Find unused imports: `pip install unimport`
- **depcheck** - Node.js dependency checker: `npm install -g depcheck`
- **ts-prune** - TypeScript unused exports: `npm install -g ts-prune`

## 📚 Related Documentation

- [CLEANUP_REPO.md](../CLEANUP_REPO.md) - Comprehensive cleanup and maintenance guide
- [CLEANUP_REPO.md](../CLEANUP_REPO.md) - Repository cleanup checklist
- [docs/REORGANIZATION_GUIDE.md](../docs/REORGANIZATION_GUIDE.md) - Reorganization guide
- [README_REDDIT_SCRAPER.md](./README_REDDIT_SCRAPER.md) - Reddit scraper documentation

## 🚀 Quick Start

### Running a Cleanup Check
```bash
# 1. Check root cleanliness
./scripts/check-clean-root.sh

# 2. Find dead Python code
python3 scripts/detect-dead-code.py src/Python

# 3. Find orphaned files (dry run)
./scripts/detect-orphans.sh --dry-run
```

### After Finding Issues
1. Review the findings carefully
2. Test your build after any changes
3. Use `.trash/` for safe removal
4. Commit incrementally

## ⚠️ Safety Guidelines

1. **Always backup** before bulk operations
2. **Test builds** after moving/deleting files
3. **Review carefully** - tools may have false positives
4. **Commit often** - easier to roll back small changes
5. **Team review** - get approval for large cleanups

## 💡 Tips

- Run cleanup scripts regularly (monthly/quarterly)
- Combine multiple tools for better coverage
- Document why files were removed (commit messages)
- Keep track of cleanup metrics (files removed, space freed)

## 🐛 Troubleshooting

### Script Permission Denied
```bash
chmod +x scripts/*.sh
```

### ripgrep Not Found
```bash
# Ubuntu/Debian
sudo apt-get install ripgrep

# macOS
brew install ripgrep

# Or download from: https://github.com/BurntSushi/ripgrep
```

### Python Module Not Found
```bash
pip install -r requirements.txt
```

## 📞 Support

For issues or questions:
1. Check the related documentation
2. Review script comments and usage
3. Create an issue with the `cleanup` label
