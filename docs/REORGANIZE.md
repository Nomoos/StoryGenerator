# 🗂️ Repository Reorganization & Deduplication — Step-by-Step Checklist

> Save this as `REORGANIZE.md`. Follow in order. Each step has copy‑pasteable commands and dry‑runs first.

---

## 🎯 Goals

- Keep the repository **top-level clean**.
- **Deduplicate** identical or near-identical files.
- **Normalize layout** into conventional folders.
- Add **automation** to prevent future clutter.

**Allowed top-level items (adjust as needed):**  
`src/`, `tests/`, `docs/`, `scripts/`, `assets/`, `.github/`, `.gitignore`, `.gitattributes`, `.editorconfig`, `README.md`, `LICENSE`, one project manifest (`package.json` or `pyproject.toml` or `pom.xml`/`build.gradle`).

---

## 0) Prep & Safety

- [ ] **Create reorg branch & backup tag**
  ```bash
  BRANCH="chore/reorg-structure-$(date +%F)"
  TAG="backup/pre-reorg-structure-$(date +%F)"
  git checkout -b "$BRANCH"
  git tag "$TAG"
  git push -u origin "$BRANCH"
  git push --tags
  ```

---

## 1) Detect & Review Duplicates (Dry Runs)

> Use multiple methods; keep *one canonical* copy per logical file.

- [ ] **Exact duplicate files by content (portable shell)**  
  ```bash
  # Show duplicates (same SHA-256) across repo (tracked + untracked)
  find . -type f -not -path "./.git/*" -print0 \
  | xargs -0 -I{} sh -c 'sha256sum "{}"' \
  | sort | awk "{h=\$1; \$1=\"\"; sub(/^ +/ , \"\"); files[h]=files[h] \"\n\" \$0} END{for (k in files) {n=split(files[k], a, \"\n\"); if (n>2) {print \"# Duplicates (\" n-1 \"):\"; for (i=2;i<=n;i++) print a[i]}}}"
  ```

- [ ] **Git-tracked duplicates (same blob ID)**  
  ```bash
  git ls-files -s \
    | awk '{print $2, $4}' \
    | sort | uniq -c \
    | awk '$1>1{print "count="$1,"blob="$2}'
  # To list paths for a blob:
  # git ls-files -s | awk -v b=<<BLOB_SHA>> '$2==b{print $4}'
  ```

- [ ] **Case-insensitive name collisions (macOS/Windows risk)**  
  ```bash
  git ls-files \
    | awk '{low=tolower($0); map[low]=map[low] ? map[low] "\n" $0 : $0} END{for(k in map){n=split(map[k],a,"\n"); if(n>1){print "Collision:"; for(i=1;i<=n;i++) print "  " a[i]}}}'
  ```

- [ ] **Optional: Use system tools if available**
  ```bash
  # Debian/Ubuntu: sudo apt-get install fdupes rdfind
  fdupes -r .           # list exact dupes
  rdfind -dryrun true -makeresultsfile false -checksum sha1 .
  ```

- [ ] **Windows PowerShell alternative**
  ```powershell
  Get-ChildItem -Recurse -File | Group-Object { (Get-FileHash $_.FullName -Algorithm SHA256).Hash } | Where-Object { $_.Count -gt 1 } | ForEach-Object {
    Write-Host "Duplicates:"
    $_.Group | Select-Object -ExpandProperty FullName
  }
  ```

---

## 2) Choose Canonical Locations

> Decide where each type of file should live. Use this baseline; tweak as needed.

- Code → `src/`  
- Tests → `tests/`  
- CLI/utility scripts → `scripts/`  
- Docs/diagrams/specs → `docs/`  
- Static files (images, fonts, public assets) → `assets/`  
- CI/CD → `.github/workflows/`

- [ ] **Create folders**
  ```bash
  mkdir -p src tests scripts docs assets .github/workflows
  ```

---

## 3) Deduplicate by Replacing with Canonical Files

> For each duplicate group: keep **one** path (canonical), replace others.

- [ ] **Example helper: replace duplicates with the canonical path (interactive)**  
  ```bash
  # Usage: ./scripts/replace_dupes.sh <canonical_file> <dupe_file1> <dupe_file2> ...
  mkdir -p scripts
  cat > scripts/replace_dupes.sh <<'SH'
  #!/usr/bin/env bash
  set -euo pipefail
  canon="$1"; shift
  for f in "$@"; do
    if [ "$f" != "$canon" ]; then
      git rm --cached "$f" 2>/dev/null || true
      rm -f "$f"
      ln -s "$(realpath --relative-to="$(dirname "$f")" "$canon")" "$f"
      git add "$f"
      echo "Replaced $f -> symlink to $canon"
    fi
  done
  SH
  chmod +x scripts/replace_dupes.sh
  git add scripts/replace_dupes.sh && git commit -m "chore: add duplicate replacement helper"
  ```

- [ ] **If symlinks are undesirable (cross-platform), copy instead**
  ```bash
  # Replace duplicates with copies (keeps working on Windows)
  # rm dupes then `git add` canonical + new copies if needed.
  ```

- [ ] **Commit after each dedupe batch**
  ```bash
  git commit -m "refactor: deduplicate files; keep canonical paths"
  ```

---

## 4) Move Files into the Clean Top-Level Layout

- [ ] **Move implementation code**
  ```bash
  [ -d "app" ] && git mv app src || true
  [ -d "lib" ] && git mv lib src || true
  for f in *.py; do [ -f "$f" ] && git mv "$f" src/; done
  for f in *.js *.ts *.tsx *.jsx; do [ -f "$f" ] && git mv "$f" src/; done
  ```

- [ ] **Move tests**
  ```bash
  find . -type d -name "test*" -maxdepth 2 -not -path "./tests" -exec bash -lc 'for d; do git mv "$d" tests/$(basename "$d") || true; done' bash {} +
  ```

- [ ] **Move docs & assets**
  ```bash
  [ -d "documentation" ] && git mv documentation docs || true
  for d in public static images img media; do
    [ -d "$d" ] && git mv "$d" assets/$(basename "$d") || true
  done
  ```

- [ ] **Move scripts/CLIs**
  ```bash
  [ -d "bin" ] && git mv bin scripts || true
  ```

- [ ] **Commit structural moves**
  ```bash
  git commit -m "refactor: enforce clean top-level structure"
  ```

---

## 5) Normalize & Prevent Future Clutter

- [ ] **`.gitattributes` for line endings & text normalization**
  ```bash
  cat > .gitattributes <<'ATTR'
  * text=auto eol=lf
  *.bat eol=crlf
  *.ps1 eol=crlf
  ATTR
  git add .gitattributes && git commit -m "chore: add .gitattributes"
  ```

- [ ] **`.editorconfig` for consistent editors**
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

- [ ] **Root guard: fail CI if unexpected files appear at repo root**
  ```bash
  mkdir -p scripts .github/workflows
  cat > scripts/check-clean-root.sh <<'SH'
  #!/usr/bin/env bash
  set -euo pipefail
  allowed_regex='^(\.gitignore|\.gitattributes|\.editorconfig|README\.md|LICENSE|package\.json|pyproject\.toml|pom\.xml|build\.gradle|src|tests|docs|scripts|assets|\.github)$'
  bad=0
  while IFS= read -r entry; do
    base="$(basename "$entry")"
    [[ "$base" =~ $allowed_regex ]] || { echo "❌ Unexpected root item: $base"; bad=1; }
  done < <(find . -maxdepth 1 -mindepth 1 -printf "%f\n")
  exit $bad
  SH
  chmod +x scripts/check-clean-root.sh
  ```

- [ ] **CI workflow to enforce root guard**
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
  git add scripts/check-clean-root.sh .github/workflows/root-guard.yml
  git commit -m "ci: enforce clean top-level via root guard"
  ```

- [ ] **Pre-commit hooks (optional, recommended)**
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

## 6) Language-Specific Fixups (adjust as needed)

- [ ] **Node/TypeScript**
  ```bash
  # Ensure main/types/scripts paths in package.json and tsconfig rootDir/outDir
  jq '.main="dist/index.js" | .types="dist/index.d.ts"' package.json > package.tmp && mv package.tmp package.json || true
  jq '.compilerOptions |= (.outDir="dist" | .rootDir="src")' tsconfig.json > tsconfig.tmp && mv tsconfig.tmp tsconfig.json || true
  git add package.json tsconfig.json 2>/dev/null || true
  git commit -m "chore(node): align paths for src layout" || true
  ```

- [ ] **Python**
  ```bash
  touch src/__init__.py
  printf "[tool.pytest.ini_options]\npythonpath = [\"src\"]\n" > pytest.ini
  git add src/__init__.py pytest.ini
  git commit -m "chore(python): src-layout + pytest config"
  ```

- [ ] **Java**
  ```bash
  mkdir -p src/main/java src/test/java
  # Move packages accordingly, then:
  git commit -m "refactor(java): maven/gradle standard layout" || true
  ```

---

## 7) Final Checks

- [ ] **List top-level to verify cleanliness**
  ```bash
  ls -la
  tree -L 2 || find . -maxdepth 2 -type d -print
  ```

- [ ] **Run CI locally (if applicable)**
  ```bash
  npm test 2>/dev/null || true
  pytest -q 2>/dev/null || true
  ```

- [ ] **Push & open PR**
  ```bash
  git push -u origin "$BRANCH"
  ```

- [ ] **After merge: prune & clean**
  ```bash
  git checkout main
  git pull --ff-only
  git branch -d "$BRANCH"
  git remote prune origin
  ```

---

## Notes

- When removing duplicates, **preserve import paths** used by consumers; prefer redirecting callers to the canonical file in a follow-up refactor.
- If your platform dislikes symlinks (Windows), use copies or refactor imports to point to the canonical location and delete dupes outright.
- Keep root strict: any new top-level item should be justified (and added to `check-clean-root.sh` if truly needed).
