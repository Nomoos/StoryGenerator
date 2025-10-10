# 🧹 Repository Cleanup & Maintenance Guide

> **Canonical cleanup guide** combining deduplication, reorganization, and maintenance procedures.  
> Follow in order. All steps use GitHub-style checkboxes and copy-pasteable commands.  
> ⚠️ Destructive steps include **dry-runs first**; only run the "apply" command when you're sure.

---

## 🎯 Goals

- Keep the repository **top-level clean** and maintainable
- **Deduplicate** identical or near-identical files
- **Normalize layout** into conventional folders
- Remove **dead code** and unused assets
- Add **automation** to prevent future clutter
- Maintain consistency between CI/CD and local environment

**Allowed top-level items:**  
`src/`, `tests/`, `docs/`, `scripts/`, `assets/`, `examples/`, `data/`, `issues/`, `obsolete/`, `research/`, `.github/`, `.gitignore`, `.gitattributes`, `.editorconfig`, `README.md`, `LICENSE`, `QUICKSTART.md`, one project manifest (`package.json`, `pyproject.toml`, `pom.xml`, or `build.gradle`), `requirements.txt`.

---

## 0) Prep & Safety

- [ ] **Confirm clean worktree (commit or stash everything).**
  ```bash
  git status
  ```

- [ ] **Create a dedicated cleanup branch (date-stamped) & backup tag.**
  ```bash
  BRANCH="chore/cleanup-$(date +%F)"
  TAG="backup/pre-cleanup-$(date +%F)"
  git checkout -b "$BRANCH"
  git tag "$TAG"
  git push -u origin "$BRANCH"
  git push --tags
  ```

---

## 1) Inventory & Size

- [ ] **List largest tracked blobs (find accidental binaries).**
  ```bash
  git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize:disk) %(rest)' \
  | awk '$1=="blob"{print $3, $4}' \
  | numfmt --to=iec --suffix=B --padding=7 | sort -h | tail -n 30
  ```

- [ ] **Dry-run: what would `git clean` remove (untracked/ignored)?**
  ```bash
  git clean -n -d -x
  # If OK, apply:
  # git clean -f -d -x
  ```

---

## 2) .gitignore & De-track Generated Files

- [ ] **Ensure a sane `.gitignore` (append baseline entries).**
  ```bash
  printf "%s\n" \
  "# OS" ".DS_Store" "Thumbs.db" \
  "" "# Editors" ".idea/" ".vscode/" \
  "" "# Dependencies" "node_modules/" "venv/" ".venv/" \
  "" "# Builds" "dist/" "build/" "out/" "coverage/" \
  "" "# Logs" "*.log" "npm-debug.log*" "yarn-debug.log*" \
  >> .gitignore
  git add .gitignore && git commit -m "chore: update .gitignore"
  ```

- [ ] **Untrack committed generated/dep folders (keep locally).**
  ```bash
  git rm -r --cached node_modules dist build out coverage 2>/dev/null || true
  git commit -m "chore: stop tracking generated/dep folders" || true
  ```

---

## 3) Standard Directory Layout (keep top level clean)

- [ ] **Create folders.**
  ```bash
  mkdir -p src tests scripts docs assets .github/workflows
  ```

- [ ] **Move implementation code into `src/` (examples; edit!).**
  ```bash
  [ -d "app" ] && git mv app src || true
  [ -d "lib" ] && git mv lib src || true
  for f in *.py; do [ -f "$f" ] && git mv "$f" src/; done
  for f in *.js *.ts *.jsx *.tsx; do [ -f "$f" ] && git mv "$f" src/; done
  ```

- [ ] **Move tests to `tests/`.**
  ```bash
  find . -type d -name "test*" -maxdepth 2 -not -path "./tests" -exec bash -lc 'for d; do git mv "$d" tests/$(basename "$d") || true; done' bash {} +
  ```

- [ ] **Move docs & assets.**
  ```bash
  [ -d "documentation" ] && git mv documentation docs || true
  for d in public static images img media; do
    [ -d "$d" ] && git mv "$d" assets/$(basename "$d") || true
  done
  ```

- [ ] **Move scripts/CLIs to `scripts/`.**
  ```bash
  [ -d "bin" ] && git mv bin scripts || true
  ```

- [ ] **Commit structure moves.**
  ```bash
  git commit -m "refactor: enforce clean top-level structure (src/tests/docs/scripts/assets)"
  ```

---

## 4) Deduplication (keep one canonical)

### 4.1 Detect Duplicates

- [ ] **Find exact duplicates by content (portable shell).**
  ```bash
  find . -type f -not -path "./.git/*" -print0 \
  | xargs -0 -I{} sh -c 'sha256sum "{}"' \
  | sort | awk '{h=$1;$1="";sub(/^ +/,"");files[h]=files[h] "\n" $0} END{for(k in files){n=split(files[k],a,"\n"); if(n>2){print "# Duplicates (" n-1 "):"; for(i=2;i<=n;i++) print a[i]}}}'
  ```

- [ ] **Git-tracked duplicates (same blob ID).**
  ```bash
  git ls-files -s \
    | awk '{print $2, $4}' \
    | sort | uniq -c \
    | awk '$1>1{print "count="$1,"blob="$2}'
  # To list paths for a blob:
  # git ls-files -s | awk -v b=<<BLOB_SHA>> '$2==b{print $4}'
  ```

- [ ] **Case-insensitive name collisions (macOS/Windows risk).**
  ```bash
  git ls-files \
    | awk '{low=tolower($0); map[low]=map[low] ? map[low] "\n" $0 : $0} END{for(k in map){n=split(map[k],a,"\n"); if(n>1){print "Collision:"; for(i=1;i<=n;i++) print "  " a[i]}}}'
  ```

### 4.2 Resolve Duplicates

- [ ] **Resolve duplicates: keep a canonical path, remove others.**
  ```bash
  # Example (edit paths):
  CANON="src/utils/helpers.ts"; git add "$CANON"
  git rm path/to/duplicate/helpers.ts
  git commit -m "refactor: deduplicate helpers.ts (use $CANON)"
  ```

---

## 5) Detect & Remove Orphaned Files

### 5.1 Identify Core Scope

- [ ] **Determine main entrypoints** (production build/run).
- [ ] **Include essential folders:**
  - `src/` (production code)
  - `config/`, `.env.example`
  - `migrations/`
  - CI/CD (`.github/`, `Dockerfile`, `helm/`, `infra/`)
  - License and legal files (`LICENSE`, `NOTICE`, `CHANGELOG`)

### 5.2 Detect Orphaned Files by Stack

**JavaScript/TypeScript:**
```bash
npx ts-prune || true
npx depcheck || true
npx madge --circular src/ || true
```

**Python:**
```bash
pip install vulture unimport
vulture src/ --min-confidence 80
unimport --check src/
```

**C#:**
```bash
# Use Resharper/Rider or dotnet-format
dotnet format analyzers --verify-no-changes || true
```

### 5.3 Find Unreferenced Files

- [ ] **Find files not referenced anywhere (manual check).**
  ```bash
  # dependencies: ripgrep (rg)
  PROTECT='(migrations|infra|deploy|.github|docs/legal|LICENSE|NOTICE|CHANGELOG)'
  
  mapfile -t CANDIDATES < <(git ls-files \
    | grep -E '\.(js|jsx|ts|tsx|css|scss|png|jpg|svg|json)$' \
    | grep -Ev "$PROTECT")
  
  echo "=== DRY RUN: unreferenced files ==="
  > /tmp/orphans.txt
  for f in "${CANDIDATES[@]}"; do
    if ! rg -n --hidden --glob '!.git' --fixed-strings "$(basename "$f")" \
      --no-ignore --ignore-file .gitignore -g '!'"$f" >/dev/null; then
      echo "$f" | tee -a /tmp/orphans.txt
    fi
  done
  ```

### 5.4 Safe Removal with .trash Folder

- [ ] **Move orphans to `.trash` folder for review.**
  ```bash
  mkdir -p .trash
  while read -r f; do
    test -n "$f" && mkdir -p ".trash/$(dirname "$f")" \
      && git mv -k "$f" ".trash/$f" 2>/dev/null || true
  done </tmp/orphans.txt
  ```

- [ ] **Test build & tests still pass.**
  ```bash
  npm run build && npm test || true
  pytest -q || true
  dotnet build || true
  ```

- [ ] **If tests pass, permanently remove `.trash` content.**
  ```bash
  git rm -r .trash/*
  git commit -m "chore(cleanup): remove orphaned and unused files"
  ```

---

## 6) Language-Specific Touch-Ups (optional)

- [ ] **Node/TypeScript.**
  ```bash
  # Ensure main/types/scripts paths in package.json and tsconfig rootDir/outDir
  jq '.main="dist/index.js" | .types="dist/index.d.ts"' package.json > package.tmp && mv package.tmp package.json || true
  jq '.compilerOptions |= (.outDir="dist" | .rootDir="src")' tsconfig.json > tsconfig.tmp && mv tsconfig.tmp tsconfig.json || true
  git add package.json tsconfig.json 2>/dev/null || true
  git commit -m "chore(node): align paths for src layout" || true
  ```

- [ ] **Python.**
  ```bash
  touch src/__init__.py
  printf "[tool.pytest.ini_options]\npythonpath = [\"src\"]\n" > pytest.ini
  git add src/__init__.py pytest.ini
  git commit -m "chore(python): src-layout + pytest path"
  ```

- [ ] **Java.**
  ```bash
  mkdir -p src/main/java src/test/java
  # Move packages accordingly, then:
  git commit -m "refactor(java): maven/gradle standard layout" || true
  ```

---

## 7) SOLID Principles Check (design hygiene)

- [ ] **S (Single Responsibility):** Each class/module has one reason to change.
  - Split "god" files into cohesive modules
  - Extract side-effects (I/O, logging) from pure logic

- [ ] **O (Open/Closed):** Extend behavior via new types, not edits.
  - Replace `switch`/`if` dispatch with polymorphism or strategy maps
  - Prefer composition over deep inheritance

- [ ] **L (Liskov Substitution):** Subtypes don't violate base expectations.
  - Avoid weakening preconditions / strengthening postconditions
  - Remove "not implemented" branches in subclasses

- [ ] **I (Interface Segregation):** Smaller, purpose-built interfaces.
  - Split fat interfaces; keep consumer-centric contracts
  - Use optional capabilities via adapters

- [ ] **D (Dependency Inversion):** Depend on abstractions, inject concretes.
  - Introduce ports/adapters; pass dependencies via constructor/factory
  - Hide third-party SDKs behind your interfaces

---

## 8) Code Hygiene Check (practical checklist)

- [ ] **Naming & structure:** Clear, consistent naming; modules < ~500 LOC; functions < ~50 LOC (guideline).
- [ ] **Dead code:** Remove unused files, exports, params.
  ```bash
  # JS/TS (requires depcheck): npx depcheck || true
  # Python (optional): pip install vulture && vulture src || true
  ```
- [ ] **Secrets & keys:** Ensure no secrets in repo.
  ```bash
  git secrets --scan 2>/dev/null || true
  trufflehog filesystem --no-update --fail || true
  ```
- [ ] **Dependencies:** Audit vulnerabilities / prune.
  ```bash
  npm audit --audit-level=high 2>/dev/null || true
  pip install pip-audit >/dev/null 2>&1 || true; pip-audit || true
  # Python alt: pip install safety && safety check || true
  ```
- [ ] **Lint & format (one-off run).**
  ```bash
  npx prettier -w . 2>/dev/null || true
  npx eslint . --fix 2>/dev/null || true
  black src tests 2>/dev/null || true
  flake8 src tests 2>/dev/null || true
  ```
- [ ] **Tests:** Ensure unit tests run from `tests/`; add smoke tests if missing.
- [ ] **Logging & errors:** Use structured logging; avoid swallowing exceptions.
- [ ] **Boundaries:** Validate inputs at public boundaries (API/controllers/CLIs).
- [ ] **Performance & complexity:** Hot paths measured; cyclomatic complexity reasonable.
- [ ] **Docs:** README updated to reflect new structure and commands.

---

## 9) Normalize & Prevent Future Clutter

- [ ] **`.gitattributes` for line endings & text normalization.**
  ```bash
  cat > .gitattributes <<'ATTR'
  * text=auto eol=lf
  *.bat eol=crlf
  *.ps1 eol=crlf
  ATTR
  git add .gitattributes && git commit -m "chore: add .gitattributes"
  ```

- [ ] **`.editorconfig` for consistent editors.**
  ```bash
  cat > .editorconfig <<'INI'
  root = true

  [*]
  charset = utf-8
  end_of_line = lf
  insert_final_newline = true
  indent_style = space
  indent_size = 2
  trim_trailing_whitespace = true

  [*.py]
  indent_size = 4

  [*.md]
  trim_trailing_whitespace = false
  INI
  git add .editorconfig && git commit -m "chore: add .editorconfig"
  ```

- [ ] **Root guard: fail CI if unexpected files appear at repo root.**
  ```bash
  mkdir -p scripts .github/workflows
  cat > scripts/check-clean-root.sh <<'SH'
  #!/usr/bin/env bash
  set -euo pipefail
  allowed_regex='^(\.git|\.gitignore|\.gitattributes|\.editorconfig|README\.md|LICENSE|QUICKSTART\.md|CLEANUP_REPO\.md|package\.json|pyproject\.toml|pom\.xml|build\.gradle|requirements\.txt|\.env\.example|src|tests|docs|scripts|assets|examples|data|issues|obsolete|research|\.github|\.idea|\.pre-commit-config\.yaml|\.flake8|coverage\.xml|core|providers|config)$'
  bad=0
  while IFS= read -r entry; do
    base="$(basename "$entry")"
    [[ "$base" =~ $allowed_regex ]] || { echo "❌ Unexpected root item: $base"; bad=1; }
  done < <(find . -maxdepth 1 -mindepth 1 -printf "%f\n")
  exit $bad
  SH
  chmod +x scripts/check-clean-root.sh
  ```

- [ ] **Test the guard.**
  ```bash
  bash scripts/check-clean-root.sh
  ```

- [ ] **CI workflow to enforce root guard (optional).**
  ```bash
  cat > .github/workflows/root-guard.yml <<'YML'
  name: Root Guard
  on: [push, pull_request]
  jobs:
    guard:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - run: bash scripts/check-clean-root.sh
  YML
  git add .github/workflows/root-guard.yml
  git commit -m "ci: enforce clean top-level via root guard"
  ```

- [ ] **Pre-commit hooks (optional, recommended).**
  ```bash
  cat > .pre-commit-config.yaml <<'YAML'
  repos:
    - repo: https://github.com/pre-commit/pre-commit-hooks
      rev: v5.0.0
      hooks:
        - id: end-of-file-fixer
        - id: trailing-whitespace
        - id: check-merge-conflict
        - id: detect-private-key
        - id: mixed-line-ending
    - repo: https://github.com/psf/black
      rev: 24.8.0
      hooks:
        - id: black
          language_version: python3
  YAML
  pip install pre-commit >/dev/null 2>&1 || true
  pre-commit install || true
  git add .pre-commit-config.yaml && git commit -m "chore: add pre-commit hooks"
  ```

---

## 10) Finalize

- [ ] **Run test/build (best effort).**
  ```bash
  npm test 2>/dev/null || true
  pytest -q 2>/dev/null || true
  dotnet build 2>/dev/null || true
  ```

- [ ] **Push branch & open PR for the cleanup.**
  ```bash
  git push -u origin "$BRANCH"
  ```

- [ ] **After merge: prune local/remote and clean up.**
  ```bash
  git checkout main
  git pull --ff-only
  git branch -d "$BRANCH"
  git remote prune origin
  ```

---

## 📊 Reporting and Metrics

After cleanup, record:
- Number of files removed
- Space freed (MB/GB)
- Lines of code removed
- Build time before/after

```bash
# Example report
echo "### Cleanup Results" > cleanup-report.md
echo "- Files removed: $(cat /tmp/orphans.txt | wc -l)" >> cleanup-report.md
echo "- Space freed: $(du -sh .trash/ 2>/dev/null || echo '0')" >> cleanup-report.md
echo "- Date: $(date)" >> cleanup-report.md
```

---

## 🔄 Maintenance Schedule

Recommended frequency:
- **Monthly:** Quick dead code check with automated tools
- **Quarterly:** Thorough manual review
- **After major refactors:** Always run cleanup

---

## ⚠️ Safety Net

**Never delete:**
- **Migrations / schema** - even if not called, may be critical
- **Infrastructure** (`infra/`, `deploy/`, `.github/`, Dockerfile, helm charts)
- **Legal files** (`LICENSE`, `NOTICE`, `docs/legal`)
- **Generated files** (verify `.gitattributes`, code generators)
- **Historical documents** (audit requirements)

---

## 💡 Best Practices

1. **Always start with dry-run** - Never delete files outright
2. **Use `.trash` folder** - Allows easy recovery
3. **Commit in small steps** - Easier rollback
4. **Document reasons** - Why files were removed
5. **Review with team** - Important for larger changes
6. **Test before and after** - Build and tests must pass
7. **Backup branch** - Before starting cleanup process

---

## 🚨 Troubleshooting

### Build fails after cleanup
```bash
# Restore files from .trash
git restore --source=HEAD~1 path/to/file

# Or revert entire commit
git revert HEAD
```

### Lost important file
```bash
# Find in history
git log --all --full-history -- path/to/file

# Restore from specific commit
git checkout <commit-hash> -- path/to/file
```

### False positives in detection
```bash
# Add to whitelist file
echo "path/to/file" >> .cleanup-whitelist

# Or add comment in code
# KEEP: This file is needed for [reason]
```

---

## 🎓 Example Scripts

### Example 1: Detect unused Python modules
```bash
cd /path/to/project
vulture src/Python/ --min-confidence 80 > /tmp/dead-code.txt
cat /tmp/dead-code.txt
```

### Example 2: Find files not imported anywhere
```bash
#!/bin/bash
for file in $(find src/Python -name "*.py"); do
  filename=$(basename "$file" .py)
  if ! rg -q "import.*$filename|from.*$filename" --glob "*.py" .; then
    echo "Orphaned: $file"
  fi
done
```

### Example 3: Find unreferenced images
```bash
#!/bin/bash
for img in $(find assets -type f -name "*.png" -o -name "*.jpg"); do
  imgname=$(basename "$img")
  if ! rg -q "$imgname" --glob "*.{md,html,jsx,tsx}" .; then
    echo "Unused image: $img"
  fi
done
```

---

## 📝 Related Documentation

- `scripts/README.md` - Documentation for cleanup and utility scripts
- `scripts/detect-orphans.sh` - Script for detecting orphaned files (if exists)
- `scripts/detect-dead-code.py` - Python dead code detector (if exists)
- `scripts/check-clean-root.sh` - Root cleanliness validation script
- `docs/REORGANIZATION_SUMMARY.md` - Summary of completed reorganization work
- `docs/FINAL_REORGANIZATION.md` - Recent reorganization documentation
- `docs/TEST_FILES.md` - Git tracking policy for test and content files

---

## 📞 Support

For questions or issues:
1. Review this document and related guides
2. Consult with team before major changes
3. Create issue with label `cleanup` for discussion

---

## Notes

- **Backup first:** The backup tag created in step 0 allows quick rollback if needed
- **Incremental commits:** Commit after each major step to track progress
- **Team coordination:** Communicate with team members before major restructuring
- **CI/CD updates:** After restructuring, update any CI/CD scripts that reference old paths
- **Documentation:** Keep documentation in sync with the new structure
- When removing duplicates, **preserve import paths** used by consumers; prefer redirecting callers to the canonical file in a follow-up refactor
- If your platform dislikes symlinks (Windows), use copies or refactor imports to point to the canonical location and delete dupes outright
- Keep root strict: any new top-level item should be justified (and added to `check-clean-root.sh` if truly needed)

---

**Last Updated:** 2025-10-10  
**Version:** 2.0.0  
**Replaces:** `CLEANUP.md`, `REPOSITORY_CLEANUP_GUIDE.md`, `docs/REORGANIZE.md`
